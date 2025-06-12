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
    model: str = Field(..., description="Nama tabel utama yang akan di-query, misal 'arbook'.")
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
        self.query_models = {model_name: self.main_model}
        # Inisialisasi query dasar di sini
        self.query = None

    def _get_model(self, name: str):
        model = self.model_map.get(name)
        if not model: raise ValueError(f"Model '{name}' tidak ditemukan.")
        return model

    def _add_join_if_needed(self, table_name: str):
        from sqlalchemy import and_
        if table_name not in self.query_models:
            target_model = self._get_model(table_name)
            # Logika JOIN yang lebih eksplisit
            # Mencari relasi dari model utama ke model target
            fk_relation = next((r for r in self.main_model.__mapper__.relationships if r.mapper.class_ == target_model), None)
            if fk_relation:
                self.query = self.query.join(target_model, fk_relation)
            else: # Mencari relasi dari model target ke model utama
                fk_relation_rev = next((r for r in target_model.__mapper__.relationships if r.mapper.class_ == self.main_model), None)
                if fk_relation_rev:
                    self.query = self.query.join(target_model, fk_relation_rev)
                else: # Jika tidak ada relasi langsung, fallback ke ON clause eksplisit (jika ada)
                    # Untuk MVP, kita bisa sederhanakan dengan asumsi join otomatis
                    self.query = self.query.join(target_model)
            self.query_models[table_name] = target_model

    def _resolve_column_or_text(self, field_path: str):
        from sqlalchemy import text
        # Jika ada kurung, ini adalah ekspresi, langsung gunakan text()
        if '(' in field_path and ')' in field_path:
            return text(field_path)

        if '.' not in field_path:
            table_name = self.main_model.__tablename__
            col_name = field_path
        else:
            table_name, col_name = field_path.split('.', 1)

        self._add_join_if_needed(table_name)
        model = self.query_models[table_name]

        if not hasattr(model, col_name): raise AttributeError(f"Kolom '{col_name}' tidak ada di tabel '{table_name}'.")
        return getattr(model, col_name)

    def apply_domain(self, domain: List[Any]):
        from sqlalchemy import and_
        op_map = {"=": "__eq__", ">": "__gt__", "<": "__lt__", ">=": "__ge__", "<=": "__le__", "!=": "__ne__", "in": "in_", "like": "like", "ilike": "ilike"}

        if not domain: return
        
        conditions = []
        for item in domain:
            field, op, val = item
            column = self._resolve_column_or_text(field)
            
            # Cek jika value adalah nama kolom lain
            if isinstance(val, str) and '.' in val and any(val.startswith(m) for m in self.model_map.keys()):
                other_column = self._resolve_column_or_text(val)
                conditions.append(getattr(column, op_map[op])(other_column))
            else:
                conditions.append(getattr(column, op_map[op])(val))
        
        self.query = self.query.where(and_(*conditions))

    def build(self, fields: List[str], domain: List[Any], order: Optional[str] = None, limit: Optional[int] = None):
        from sqlalchemy import select, text

        # Tentukan entitas yang akan di-select
        if fields:
            select_entities = [self._resolve_column_or_text(f) for f in fields]
        else:
            select_entities = [self.main_model]

        # --- PERBAIKAN UTAMA: Inisialisasi self.query SEBELUM digunakan ---
        self.query = select(*select_entities).select_from(self.main_model)
        # -------------------------------------------------------------

        # Panggil apply_domain setelah self.query diinisialisasi
        self.apply_domain(domain)

        if order:
            # Pastikan alias di-handle dengan benar
            self.query = self.query.order_by(text(order))
        
        if limit:
            self.query = self.query.limit(limit)
            
        return self.query
    
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
    Melakukan pencarian dan pembacaan data dari database dengan struktur
    mirip Odoo (domain, fields, limit, order).
    """
    print("\n--- [DEBUG] Inside search_read ---")
    try:
        params = SearchReadInput(**payload)
        print(f"Parameter tervalidasi: {params.model_dump_json(indent=2)}")
    except Exception as e:
        error_msg = f"Gagal memvalidasi parameter search_read. Error: {e}"
        print(f"\n🔥 [ERROR] {error_msg}")
        return {"success": False, "error": error_msg}

    try:
        with get_db_session() as db:
            # --- PERBAIKAN DI SINI ---
            # Inisialisasi builder hanya dengan model utama
            builder = DynamicQueryBuilder(db, params.model)
            # Kirim semua parameter ke metode build
            query = builder.build(params.fields, params.domain, params.order, params.limit)
            # --------------------------
            
            print(f"\n[DEBUG] SQL Query yang dihasilkan:")
            print(str(query.compile(compile_kwargs={"literal_binds": True})))

            res = db.execute(query).mappings().all()
            
            # Serialisasi hasil tetap penting
            serialized_data = [dict(row) for row in res]
            
            print(f"\n[DEBUG] Hasil (sudah diserialisasi): {len(serialized_data)} baris")
            return {"success": True, "data": serialized_data}
            
    except Exception as e:
        print(f"\n🔥 [ERROR] Eksekusi GAGAL: {type(e).__name__}: {e}")
        return {"success": False, "error": f"Eksekusi query gagal: {e}"}