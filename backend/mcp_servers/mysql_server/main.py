# backend/mcp_servers/mysql_server/main.py (Revisi 8 - Pola Final & Bersih)

import sys
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from contextlib import contextmanager

# Karena akan dijalankan oleh interpreter venv, kita bisa langsung impor
from mcp.server.fastmcp import FastMCP, Context
from config import settings
from db_models import base

# --- Pydantic Models (Definisi Input Tool yang Kuat) ---
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
    if not settings.DATABASE_URL:
        raise ConnectionError("URL Database tidak dikonfigurasi.")
    engine = create_engine(settings.DATABASE_URL)
    db = sessionmaker(bind=engine)()
    try:
        yield db
    finally:
        db.close()

class DynamicQueryBuilder:
    def __init__(self, session):
        from db_models import base
        self.session = session
        self.model_map = {m.class_.__tablename__: m.class_ for m in base.Base.registry.mappers}
        self.joined_models = {}

    def _get_model(self, name: str):
        model = self.model_map.get(name)
        if not model: 
            raise ValueError(f"Model '{name}' tidak ditemukan.")
        return model

    def _resolve_column(self, field_path: str):
        if '.' not in field_path: 
            raise ValueError(f"Path kolom tidak valid: '{field_path}'")
        table_name, col_name = field_path.split('.', 1)
        model = self.joined_models.get(table_name)
        if not model: 
            raise ValueError(f"Tabel '{table_name}' belum di-join.")
        if not hasattr(model, col_name): 
            raise AttributeError(f"Kolom '{col_name}' tidak ada di '{table_name}'.")
        return getattr(model, col_name)

    def _parse_arithmetic_expression(self, expression: str):
        """
        Parse arithmetic expression seperti '(arbook.DocValueLocal - arbook.PaymentValueLocal)'
        dan return SQLAlchemy expression object
        """
        import re
        
        expr = expression.strip()
        if expr.startswith('(') and expr.endswith(')'):
            expr = expr[1:-1].strip()
        
        pattern = r'(\w+\.\w+|[+\-*/()]|\d+(?:\.\d+)?)'
        tokens = re.findall(pattern, expr.replace(' ', ''))
        
        # This is a simple parser, for more complex math, a proper RPN/AST parser would be needed
        # For now, it handles simple 'A - B' cases.
        if len(tokens) == 3 and tokens[1] in ['+', '-', '*', '/']:
            left_operand = self._resolve_column(tokens[0])
            right_operand = self._resolve_column(tokens[2])
            operator = tokens[1]
            if operator == '+': return left_operand + right_operand
            if operator == '-': return left_operand - right_operand
            if operator == '*': return left_operand * right_operand
            if operator == '/': return left_operand / right_operand

        raise ValueError(f"Ekspresi aritmetika tidak dapat di-parse atau terlalu kompleks: {expression}")

    def build_query(self, operation: dict):
        from sqlalchemy import select, func, and_
        
        main_model = self._get_model(operation["main_table"])
        self.joined_models = {operation["main_table"]: main_model}

        for join in operation.get("joins", []):
            target_model = self._get_model(join["target_table"])
            self.joined_models[join["target_table"]] = target_model

        select_items = []
        for col_def in operation.get("select_columns", []):
            if col_def.get("is_expression"):
                attr = self._parse_arithmetic_expression(col_def["field_name"])
            else:
                attr = self._resolve_column(col_def["field_name"])
            
            if agg := col_def.get("aggregation"):
                attr = getattr(func, agg.lower())(attr)
            
            if alias := col_def.get("alias"):
                attr = attr.label(alias)
            
            select_items.append(attr)

        query = select(*select_items) if select_items else select(main_model)
        query = query.select_from(main_model)
        
        for join in operation.get("joins", []):
            target_model = self.joined_models[join["target_table"]]
            conditions = [
                self._resolve_column(on["left_table_field"]) == self._resolve_column(on["right_table_field"]) 
                for on in join["on_conditions"]
            ]
            query = query.join(
                target_model, 
                and_(*conditions), 
                isouter=(join.get("type", "INNER").upper() == "LEFT")
            )

        if filters := operation.get("filters", {}).get("conditions", []):
            op_map = {
                "=": "__eq__", ">": "__gt__", "<": "__lt__", 
                ">=": "__ge__", "<=": "__le__", "!=": "__ne__", 
                "in": "in_", "not in": "not_in"
            }
            conds = []
            for f in filters:
                val = f['value']
                op = f['operator'].lower()
                
                if f.get("is_expression"):
                    left_expr = self._parse_arithmetic_expression(f['field_or_expression'])
                    conds.append(getattr(left_expr, op_map[op])(val))
                else:
                    attr = self._resolve_column(f["field_or_expression"])
                    conds.append(getattr(attr, op_map[op])(val))
            
            if conds:
                query = query.where(and_(*conds))
        
        for order in operation.get("order_by_clauses", []):
            if order.get("is_expression"):
                col_expr = self._parse_arithmetic_expression(order["field_or_expression"])
            else:
                col_expr = self._resolve_column(order["field_or_expression"])
            
            direction = order.get("direction", "ASC").upper()
            query = query.order_by(col_expr.desc() if direction == "DESC" else col_expr.asc())

        if limit := operation.get("limit"):
            query = query.limit(limit)
            
        return query

# --- Inisialisasi & Definisi Tool MCP ---
mcp = FastMCP("MySQL_ORM_Server_v5_Final")

@mcp.tool()
def execute_operation_plan(ctx: Context, payload: ExecutePlanInput) -> Dict[str, Any]:
    """
    Menerima dan mengeksekusi satu atau lebih operasi database (DatabaseOperation) secara aman.
    Tool ini menerjemahkan rencana abstrak JSON menjadi query ORM, mencegah SQL Injection.
    Gunakan tool ini untuk semua kebutuhan pengambilan data dari database ERP.

    Parameters:
      payload (ExecutePlanInput): Objek input yang berisi daftar operasi.
        - operations: List dari objek DatabaseOperation. Contoh satu operasi:
          {
            "operation_id": "get_outstanding_customers",
            "main_table": "arbook",
            "select_columns": [
              {"field_name": "mastercustomer.Name", "alias": "CustomerName"},
              {"field_name": "(arbook.DocValueLocal - arbook.PaymentValueLocal)", "is_expression": true, "alias": "Outstanding"}
            ],
            "joins": [{
              "target_table": "mastercustomer", "type": "INNER",
              "on_conditions": [{"left_table_field": "arbook.CustomerCode", "right_table_field": "mastercustomer.Code"}]
            }],
            "filters": {"conditions": [
              {"field_or_expression": "(arbook.DocValueLocal - arbook.PaymentValueLocal)", "operator": ">", "value": 0, "is_expression": true}
            ]}
          }

    Returns:
      Sebuah dictionary yang berisi hasil dari setiap operasi, diidentifikasi oleh operation_id.
      Contoh:
      {
        "success": true,
        "results": {
          "get_outstanding_customers": {
            "status": "success",
            "data": [{"CustomerName": "PT ABC", "Outstanding": 5000000.00}]
          }
        }
      }
    """
    ctx.info(f"Tool 'execute_operation_plan' dipanggil dengan {len(payload.operations)} operasi.")
    results = {}
    try:
        with get_db_session() as db:
            builder = DynamicQueryBuilder(db)
            for op in payload.operations:
                op_id = op.operation_id
                try:
                    query = builder.build_query(op.model_dump())
                    res = db.execute(query).mappings().all()
                    results[op_id] = {"status": "success", "data": [dict(r) for r in res]}
                except Exception as e:
                    ctx.error(f"Error operasi '{op_id}': {e}", exc_info=True)
                    results[op_id] = {"status": "error", "error": f"{type(e).__name__}: {e}"}
        return {"success": True, "results": results}
    except Exception as e:
        ctx.error(f"Gagal sesi DB: {e}", exc_info=True)
        return {"success": False, "error": f"Database Session Failed: {e}"}

# --- Main Execution Block ---
if __name__ == "__main__":
    print("Server MCP MySQL (v5 Final) siap dijalankan...", file=sys.stderr)
    mcp.run()