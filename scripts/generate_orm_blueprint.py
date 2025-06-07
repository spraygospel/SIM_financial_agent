# scripts/generate_orm_blueprint.py
import sys
import os
import json
import traceback

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    # CUKUP IMPOR PACKAGE INI, __init__.py akan melakukan sisanya
    from backend.app import db_models
    print("[INFO] Berhasil mengimpor package db_models.")
except Exception as e:
    print(f"[FATAL] Gagal mengimpor atau mengkonfigurasi package db_models: {e}")
    traceback.print_exc()
    sys.exit(1)

from sqlalchemy import inspect

def generate_blueprint():
    print("[PROCESS] Memulai pembuatan blueprint ORM...")
    blueprint = {}
    
    # Base sekarang seharusnya sudah terisi penuh
    sorted_models = sorted(db_models.Base.metadata.tables.keys())

    for table_name in sorted_models:
        model_class = None
        for cls in db_models.Base.registry._class_registry.values():
            if hasattr(cls, '__tablename__') and cls.__tablename__ == table_name:
                model_class = cls
                break
        
        if not model_class:
            print(f"  [WARNING] Tidak ditemukan kelas model untuk tabel '{table_name}'. Dilewati.")
            continue
        
        model_inspector = inspect(model_class)
        print(f"  [INSPECT] Memproses model: {model_class.__name__} (tabel: {table_name})")
        
        # ... (sisa logika tetap sama) ...
        model_info = { "columns": [], "relationships": [] }
        for col in sorted(model_inspector.columns, key=lambda c: c.name):
            column_info = {
                "name": col.name,
                "type": str(col.type),
                "nullable": col.nullable,
                "primary_key": col.primary_key,
                "foreign_keys": [str(fk) for fk in col.foreign_keys] # BARIS INI YANG PENTING
            }
            model_info["columns"].append(column_info)
        for rel in sorted(model_inspector.relationships, key=lambda r: r.key):
            model_info["relationships"].append({"key": rel.key, "target_model": rel.mapper.class_.__name__})
        blueprint[model_class.__name__] = model_info

    output_path = os.path.join(project_root, 'tests', 'orm', 'orm_blueprint.json')
    print(f"\n[OUTPUT] Menyimpan blueprint ke: {output_path}")
    with open(output_path, 'w') as f:
        json.dump(blueprint, f, indent=4)
    print("[SUCCESS] Blueprint ORM berhasil dibuat!")

if __name__ == "__main__":
    generate_blueprint()