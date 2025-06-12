# backend/app/tools/database_tools.py

import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from contextlib import contextmanager

# Impor dari config utama, bukan config lokal
from backend.app.core.config import settings
from backend.app.db_models import base # Kita asumsikan db_models akan dipindah

# --- Pydantic Models untuk Input/Output Tool ---
class DatabaseOperation(BaseModel):
    operation_id: str
    purpose: Optional[str] = None
    main_table: str
    select_columns: List[Dict[str, Any]]
    joins: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    filters: Optional[Dict[str, Any]] = Field(default_factory=dict)
    order_by_clauses: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    limit: Optional[int] = None

class ExecutePlanInput(BaseModel):
    operations: List[DatabaseOperation]

# --- Fungsi Helper & Kelas Logika ---
@contextmanager
def get_db_session():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    # Gunakan properti DATABASE_URL dari settings
    if not settings.DATABASE_URL:
        raise ConnectionError("URL Database tidak dikonfigurasi di .env utama.")
    
    engine = create_engine(settings.DATABASE_URL)
    db = sessionmaker(bind=engine)()
    try:
        yield db
    finally:
        db.close()

class DynamicQueryBuilder:
    def __init__(self, session):
        self.session = session
        self.model_map = {m.class_.__tablename__: m.class_ for m in base.Base.registry.mappers}
        self.joined_models = {}

    def _get_model(self, name: str):
        model = self.model_map.get(name)
        if not model: raise ValueError(f"Model '{name}' tidak ditemukan.")
        return model

    def _resolve_column(self, field_path: str):
        if '.' not in field_path: raise ValueError(f"Path kolom tidak valid: '{field_path}'")
        table_name, col_name = field_path.split('.', 1)
        model = self.joined_models.get(table_name)
        if not model: raise ValueError(f"Tabel '{table_name}' belum di-join.")
        if not hasattr(model, col_name): raise AttributeError(f"Kolom '{col_name}' tidak ada di '{table_name}'.")
        return getattr(model, col_name)

    def build_query(self, operation: dict):
        from sqlalchemy import select, func, and_, text
        
        main_model = self._get_model(operation["main_table"])
        self.joined_models = {operation["main_table"]: main_model}

        # --- PERBAIKAN DI SINI: Tangani joins=None ---
        # Gunakan 'or []' untuk memastikan kita selalu punya list untuk di-loop
        joins_list = operation.get("joins") or []
        for join in joins_list:
            target_model = self._get_model(join["target_table"])
            self.joined_models[join["target_table"]] = target_model

        select_items = []
        # --- PERBAIKAN DI SINI: Tangani select_columns=["*"] ---
        # Ini adalah permintaan yang umum dari LLM. Kita tangani secara khusus.
        select_defs = operation.get("select_columns", [])
        if select_defs and isinstance(select_defs[0], str) and select_defs[0] == "*":
             # Jika ada permintaan '*', ambil semua kolom dari tabel utama
            select_items.append(self.joined_models[operation["main_table"]])
        else:
            for col_def in select_defs:
                # Ganti nama field 'column' yang mungkin dikirim LLM menjadi 'field_name'
                field_name = col_def.get("field_name") or col_def.get("column")
                if not field_name: continue
                
                # Tambahkan penanganan untuk '*' di sini juga
                if field_name == "*":
                    select_items.append(self.joined_models[operation["main_table"]])
                    continue

                if col_def.get("is_expression"):
                    attr = text(field_name)
                else:
                    attr = self._resolve_column(field_name)
                
                if agg := col_def.get("aggregation"):
                    attr = getattr(func, agg.lower())(attr)
                
                if alias := col_def.get("alias"):
                    attr = attr.label(alias)
                
                select_items.append(attr)

        query = select(*select_items) if select_items else select(main_model)
        query = query.select_from(main_model)
        
        # --- PERBAIKAN DI SINI: Gunakan joins_list yang aman ---
        for join in joins_list:
            target_model = self.joined_models[join["target_table"]]
            conditions = [
                self._resolve_column(on["left_table_field"]) == self._resolve_column(on["right_table_field"]) 
                for on in join["on_conditions"]
            ]
            query = query.join(target_model, and_(*conditions), isouter=(join.get("type", "INNER").upper() == "LEFT"))

        # --- PERBAIKAN DI SINI: Tangani filters=None ---
        filters_dict = operation.get("filters") or {}
        if conditions_list := filters_dict.get("conditions"):
            op_map = {"=": "__eq__", ">": "__gt__", "<": "__lt__", ">=": "__ge__", "<=": "__le__", "!=": "__ne__", "in": "in_"}
            conds = []
            for f in conditions_list:
                val = f['value']
                op = f['operator'].lower()
                if f.get("is_expression"):
                    conds.append(text(f"({f['field_or_expression']}) {f['operator']} :val").params(val=val))
                else:
                    attr = self._resolve_column(f["field_or_expression"])
                    conds.append(getattr(attr, op_map[op])(val))
            query = query.where(and_(*conds))
                          
        # --- PERBAIKAN DI SINI: Tangani order_by_clauses=None ---
        order_by_list = operation.get("order_by_clauses") or []
        for order in order_by_list:
            col = text(order["field_or_expression"])
            query = query.order_by(col.desc() if order.get("direction", "ASC").upper() == "DESC" else col.asc())

        if limit := operation.get("limit"): query = query.limit(limit)
        return query

# --- Definisi Tool sebagai Fungsi Python Biasa ---
def execute_database_plan(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Menerima dan mengeksekusi satu batch 'DatabaseOperation' menggunakan ORM.
    Ini adalah tool utama untuk interaksi database yang aman.
    """
    try:
        validated_plan = ExecutePlanInput(**payload)
    except Exception as e:
        error_msg = f"Gagal memvalidasi rencana dari LLM. Error: {e}"
        print(f"\n🔥 [ERROR] {error_msg}")
        return {"success": False, "error": error_msg}

    print("\n--- [DEBUG] Inside execute_database_plan ---")
    try:
        print("Rencana yang diterima (setelah validasi):")
        print(json.dumps(validated_plan.model_dump(), indent=2))
    except Exception as e:
        print(f"Tidak dapat mencetak payload: {e}")
    
    results = {}
    try:
        with get_db_session() as db:
            builder = DynamicQueryBuilder(db)
            for op in validated_plan.operations:
                op_id = op.operation_id
                try:
                    query = builder.build_query(op.model_dump())
                    print(f"\n[DEBUG] SQL Query yang dihasilkan untuk op_id '{op_id}':")
                    print(str(query.compile(compile_kwargs={"literal_binds": True})))

                    res = db.execute(query).mappings().all()
                    
                    # --- PERBAIKAN UTAMA DI SINI: SERIALISASI HASIL ---
                    serialized_data = []
                    for row in res:
                        # Jika row berisi satu item dan itu adalah objek ORM (kasus SELECT *)
                        if len(row) == 1 and hasattr(list(row.values())[0], '__table__'):
                            orm_obj = list(row.values())[0]
                            # Ubah objek ORM menjadi dictionary
                            serialized_data.append({c.name: getattr(orm_obj, c.name) for c in orm_obj.__table__.columns})
                        else: # Jika tidak, row sudah merupakan dictionary-like (kasus SELECT col1, col2)
                            serialized_data.append(dict(row))
                    # ----------------------------------------------------
                    
                    results[op_id] = {"status": "success", "data": serialized_data} # Gunakan data yang sudah diserialisasi

                    print(f"\n[DEBUG] Hasil dari op_id '{op_id}' (SETELAH SERIALISASI):")
                    print(f"  -> Jumlah baris: {len(serialized_data)}")
                    print(f"  -> Contoh data: {serialized_data[:2]}")

                except Exception as e:
                    print(f"\n🔥 [ERROR] Eksekusi GAGAL untuk op_id '{op_id}': {type(e).__name__}: {e}")
                    results[op_id] = {"status": "error", "error": f"Error operasi '{op_id}': {type(e).__name__}: {e}"}
        
        print("--- [DEBUG] Selesai execute_database_plan ---\n")
        return {"success": True, "results": results}
    except Exception as e:
        print(f"\n🔥 [ERROR] Sesi DB GAGAL: {type(e).__name__}: {e}\n")
        return {"success": False, "error": f"Gagal sesi DB: {type(e).__name__}: {e}"}