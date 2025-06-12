# File: backend/mcp_servers/mysql_server/query_builder.py

from sqlalchemy.orm import Session
from sqlalchemy.sql import Select, text
from sqlalchemy import select, func, and_, or_
from typing import Dict, Any, List

# Impor semua model dari paket db_models
from .db_models import *

class DynamicQueryBuilder:
    def __init__(self, session: Session):
        self.session = session
        # Membuat mapping dari nama tabel (string) ke kelas ORM-nya
        self.model_mapping = {
            cls.__tablename__: cls for cls in Base.registry.mappers.keys()
        }

    def _get_model_from_name(self, table_name: str):
        model = self.model_mapping.get(table_name)
        if not model:
            raise ValueError(f"Unknown table: {table_name}")
        return model

    def _resolve_field_path(self, model, field_path: str):
        # Fungsi ini akan menerjemahkan string seperti "mastercustomer.Name"
        # menjadi atribut kolom SQLAlchemy yang sebenarnya.
        if '.' in field_path:
            table_name, column_name = field_path.split('.', 1)
            related_model = self._get_model_from_name(table_name)
            return getattr(related_model, column_name)
        else:
            return getattr(model, field_path)

    def build_query_from_operation(self, operation: Dict[str, Any]) -> Select:
        main_table_name = operation.get("main_table")
        if not main_table_name:
            raise ValueError("'main_table' is required in the operation plan.")
        
        base_model = self._get_model_from_name(main_table_name)
        
        # Membangun bagian SELECT
        select_items = []
        select_defs = operation.get("select_columns", [])
        for col_def in select_defs:
            field_name = col_def.get("field_name")
            if not field_name:
                continue
            
            # Cek jika ini adalah ekspresi mentah
            if col_def.get("is_expression", False):
                # Untuk ekspresi seperti (arbook.DocValueLocal - arbook.PaymentValueLocal)
                column_attr = text(field_name)
            else:
                # Untuk nama kolom biasa
                column_attr = self._resolve_field_path(base_model, field_name)
            
            # Terapkan agregasi jika ada
            aggregation = col_def.get("aggregation")
            if aggregation:
                agg_func = getattr(func, aggregation.lower(), None)
                if not agg_func:
                    raise ValueError(f"Unsupported aggregation function: {aggregation}")
                column_attr = agg_func(column_attr)
            
            # Beri alias jika ada
            alias = col_def.get("alias")
            if alias:
                column_attr = column_attr.label(alias)
            
            select_items.append(column_attr)

        # Jika tidak ada kolom spesifik, pilih semua dari model dasar
        query = select(*select_items) if select_items else select(base_model)

        # Membangun bagian JOIN
        join_defs = operation.get("joins", [])
        for join_def in join_defs:
            target_model = self._get_model_from_name(join_def["target_table"])
            
            # Asumsi join sederhana berdasarkan relasi yang sudah ada di ORM
            # Untuk MVP, ini sudah cukup. Nanti bisa diperluas dengan on_conditions.
            query = query.join(target_model)

        # Membangun bagian WHERE (filters)
        filter_defs = operation.get("filters", {})
        if filter_defs and "conditions" in filter_defs:
            # Untuk saat ini, kita hanya support 'AND' dan operator sederhana
            conditions = []
            for cond in filter_defs["conditions"]:
                field_name = cond.get("field_or_expression")
                operator = cond.get("operator")
                value = cond.get("value")
                
                if cond.get("is_expression", False):
                    column_attr = text(field_name)
                else:
                    column_attr = self._resolve_field_path(base_model, field_name)

                if operator == "=":
                    conditions.append(column_attr == value)
                elif operator == ">":
                    conditions.append(column_attr > value)
                # Tambahkan operator lain di sini jika diperlukan
            
            if conditions:
                query = query.where(and_(*conditions))

        # Membangun bagian ORDER BY
        order_by_defs = operation.get("order_by_clauses", [])
        for order_def in order_by_defs:
            field_name = order_def.get("field_or_expression")
            direction = order_def.get("direction", "ASC")
            
            # Asumsi order by berdasarkan alias atau kolom
            order_attr = text(field_name) if '.' not in field_name else self._resolve_field_path(base_model, field_name)

            if direction.upper() == "DESC":
                query = query.order_by(order_attr.desc())
            else:
                query = query.order_by(order_attr.asc())

        # Membangun bagian LIMIT
        limit = operation.get("limit")
        if limit:
            query = query.limit(limit)
            
        return query