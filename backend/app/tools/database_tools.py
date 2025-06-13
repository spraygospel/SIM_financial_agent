# backend/app/tools/database_tools.py

import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from contextlib import contextmanager

from sqlalchemy import text

# Impor dari config utama, bukan config lokal
from backend.app.core.config import settings
from backend.app.db_models import base # Kita asumsikan db_models akan dipindah

# --- Pydantic Models untuk Input/Output Tool ---
class SearchReadInput(BaseModel):
    model: str = Field(..., description="Nama tabel yang akan di-query, misal 'arbook'.")
    domain: List[Any] = Field(default_factory=list, description="List untuk filter WHERE, format: [['field', 'operator', 'value']].")
    fields: List[str] = Field(default_factory=list, description="List kolom yang akan diambil, misal ['Name', 'City']. Kosongkan untuk ambil semua.")
    limit: Optional[int] = Field(default=None, description="Batas jumlah hasil.")
    order: Optional[str] = Field(default=None, description="Urutan hasil, misal 'Name ASC'.")

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
    def __init__(self, session, model_name: str):
        self.session = session
        self.model_map = {m.class_.__tablename__: m.class_ for m in base.Base.registry.mappers}
        self.main_model = self._get_model(model_name)

    def _get_model(self, name: str):
        model = self.model_map.get(name)
        if not model: raise ValueError(f"Model '{name}' tidak ditemukan.")
        return model

    def apply_domain(self, query, domain: List[Any]):
        from sqlalchemy import and_
        op_map = {"=": "__eq__", ">": "__gt__", "<": "__lt__", ">=": "__ge__", "<=": "__le__", "!=": "__ne__", "in": "in_", "like": "like", "ilike": "ilike"}
        if not domain: return query
        
        conditions = []
        for item in domain:
            field, op, val = item
            # Untuk perbandingan antar kolom
            if isinstance(val, str) and hasattr(self.main_model, val):
                 conditions.append(getattr(getattr(self.main_model, field), op_map[op])(getattr(self.main_model, val)))
            else: # Untuk perbandingan dengan nilai literal
                 conditions.append(getattr(getattr(self.main_model, field), op_map[op])(val))
        
        return query.where(and_(*conditions))

    def build(self, fields: List[str], domain: List[Any], order: Optional[str] = None, limit: Optional[int] = None):
        from sqlalchemy import select, text

        if fields:
            select_entities = [getattr(self.main_model, f) for f in fields]
        else:
            select_entities = [self.main_model]

        query = select(*select_entities)
        query = self.apply_domain(query, domain)

        if order:
            query = query.order_by(text(order))
        
        if limit:
            query = query.limit(limit)
            
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
    
def search_read(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Melakukan pencarian dan pembacaan data dari satu tabel database dengan struktur
    mirip Odoo (domain, fields, limit, order).
    """
    print("\n--- [DEBUG] Inside search_read ---")
    try:
        params = SearchReadInput(**payload)
        print(f"Parameter tervalidasi: {params.model_dump_json(indent=2)}")
    except Exception as e:
        error_msg = f"Gagal memvalidasi parameter search_read. Error: {e}"
        return {"success": False, "error": error_msg}

    try:
        with get_db_session() as db:
            builder = DynamicQueryBuilder(db, params.model)
            query = builder.build(params.fields, params.domain, params.order, params.limit)
            
            print(f"\n[DEBUG] SQL Query yang dihasilkan:")
            print(str(query.compile(compile_kwargs={"literal_binds": True})))

            res = db.execute(query).mappings().all()
            serialized_data = [dict(row) for row in res]
            
            print(f"\n[DEBUG] Hasil (sudah diserialisasi): {len(serialized_data)} baris")
            return {"success": True, "data": serialized_data}
            
    except Exception as e:
        import traceback
        print(f"\n🔥 [ERROR] Eksekusi GAGAL: {type(e).__name__}: {e}")
        traceback.print_exc()
        return {"success": False, "error": f"Eksekusi query gagal: {e}"}