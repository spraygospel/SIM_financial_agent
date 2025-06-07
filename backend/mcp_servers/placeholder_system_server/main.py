# backend/mcp_servers/placeholder_system_server/main.py
import os
import sys
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import Context as MCPContext # Impor Context untuk logging tool

# --- Setup Path dan .env ---
# (Sama seperti server MCP lainnya)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
dotenv_path = os.path.join(project_root, 'backend', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)
else:
    load_dotenv() # Coba muat dari direktori saat ini jika tidak ada di path utama

def debug_print(*args, **kwargs):
    # Fungsi helper untuk print ke stderr, menghindari konflik dengan stdio MCP
    other_kwargs = {k: v for k, v in kwargs.items() if k != 'file'}
    print(*args, file=sys.stderr, **other_kwargs)

debug_print("--- PLACEHOLDER MCP SERVER STARTING ---", file=sys.stderr)

# --- Pydantic Models (sesuai 1_MCP_specs.md) ---
class FormattingRule(BaseModel):
    type: str = Field(description="Tipe pemformatan, misal 'currency_IDR', 'number_with_separator', 'date_DD_MMM_YYYY'.")
    precision: Optional[int] = Field(default=None, description="Untuk angka, jumlah digit desimal.")

class FillPlaceholdersInput(BaseModel):
    response_template: str = Field(..., description="String template dengan placeholder, misal 'Total penjualan: {TOTAL_SALES}'.")
    data_values: Dict[str, Any] = Field(..., description="Dictionary berisi nilai aktual untuk setiap placeholder.")
    formatting_rules: Dict[str, FormattingRule] = Field(default_factory=dict, description="Dictionary aturan pemformatan per placeholder. Key adalah nama placeholder.")

class FillPlaceholdersOutput(BaseModel):
    final_narrative: str
    success: bool = True
    error: Optional[str] = None

# --- MCP Server Initialization (TANPA lifespan) ---
mcp = FastMCP(
    name="PlaceholderSystemServer",
    title="Placeholder System Server",
    description="Server untuk mengisi placeholder dalam template narasi dengan data aktual dan menerapkan pemformatan."
    # lifespan=None # Tidak perlu lifespan
)

# --- Helper Fungsi Pemformatan ---
def format_value(value: Any, rule: Optional[FormattingRule]) -> str:
    if rule is None:
        return str(value)

    try:
        if rule.type == "currency_IDR":
            # Pastikan value adalah angka (int atau float)
            if not isinstance(value, (int, float)):
                debug_print(f"Warning: Value '{value}' for currency_IDR is not a number. Returning as string.", file=sys.stderr)
                return str(value)
            
            num_value = float(value)
            precision = rule.precision if rule.precision is not None else 2
            # Format: Rp xxx.xxx.xxx,xx
            # Untuk angka negatif, tanda minus akan berada sebelum "Rp"
            formatted_num = f"{num_value:,.{precision}f}".replace(",", "X").replace(".", ",").replace("X", ".")
            return f"Rp {formatted_num}"
        
        elif rule.type == "number_with_separator":
            if not isinstance(value, (int, float)):
                debug_print(f"Warning: Value '{value}' for number_with_separator is not a number. Returning as string.", file=sys.stderr)
                return str(value)
            
            num_value = float(value)
            precision = rule.precision if rule.precision is not None else 0 # Default 0 desimal untuk number_with_separator
            formatted_num = f"{num_value:,.{precision}f}".replace(",", "X").replace(".", ",").replace("X", ".")
            return formatted_num

        # Tambahkan aturan pemformatan lain di sini jika perlu (misal, tanggal)
        # elif rule.type == "date_DD_MMM_YYYY":
        #     # Implementasi pemformatan tanggal
        #     pass

        else:
            debug_print(f"Warning: Unknown formatting rule type '{rule.type}'. Returning value as string.", file=sys.stderr)
            return str(value)
            
    except Exception as e:
        debug_print(f"Error formatting value '{value}' with rule '{rule.type}': {e}. Returning original value.", file=sys.stderr)
        return str(value) # Kembalikan sebagai string jika ada error format


# --- Tool Implementation ---
@mcp.tool()
def fill_placeholders(ctx: MCPContext, payload: FillPlaceholdersInput) -> FillPlaceholdersOutput:
    """
    Mengganti semua placeholder dalam string template dengan nilai-nilai aktual dari
    dictionary data, dan menerapkan aturan pemformatan yang ditentukan.

    Args:
        ctx: Konteks MCP. (Digunakan untuk logging internal tool via ctx.info(), ctx.error())
        payload (FillPlaceholdersInput): Objek input yang berisi:
            response_template (str): Template string dengan placeholder (misal, "Total: {TOTAL_SALES}").
            data_values (Dict[str, Any]): Dictionary nilai aktual (misal, {"TOTAL_SALES": 100000}).
            formatting_rules (Dict[str, FormattingRule]): Aturan pemformatan per placeholder
                                                          (misal, {"TOTAL_SALES": {"type": "currency_IDR"}}).

    Returns:
        FillPlaceholdersOutput: Objek output yang berisi narasi final.

    Contoh Penggunaan oleh Agent (dalam format pemanggilan tool):
    ```json
    {
        "tool_name": "fill_placeholders",
        "payload": {
            "response_template": "Laporan Penjualan {PERIOD_LABEL}:\\n- Total Penjualan: {TOTAL_SALES_VALUE}\\n- Jumlah Transaksi: {TRANSACTION_COUNT_VALUE} transaksi",
            "data_values": {
                "PERIOD_LABEL": "Januari 2023",
                "TOTAL_SALES_VALUE": 125000000.50,
                "TRANSACTION_COUNT_VALUE": 456
            },
            "formatting_rules": {
                "TOTAL_SALES_VALUE": {"type": "currency_IDR", "precision": 2},
                "TRANSACTION_COUNT_VALUE": {"type": "number_with_separator"}
            }
        }
    }
    ```
    """
    ctx.info(f"Tool 'fill_placeholders' called. Template length: {len(payload.response_template)}, Data values keys: {list(payload.data_values.keys())}")
    
    final_narrative = payload.response_template
    
    try:
        for key, value in payload.data_values.items():
            placeholder = f"{{{key}}}" # Placeholder format: {KEY_NAME}
            
            # Dapatkan aturan pemformatan untuk key ini, jika ada
            rule = payload.formatting_rules.get(key)
            
            # Format nilainya
            formatted_str_value = format_value(value, rule)
            
            # Ganti placeholder di template
            if placeholder in final_narrative:
                final_narrative = final_narrative.replace(placeholder, formatted_str_value)
                ctx.info(f"Replaced placeholder '{placeholder}' with formatted value '{formatted_str_value}'")
            else:
                ctx.warning(f"Placeholder '{placeholder}' not found in response_template.")
        
        return FillPlaceholdersOutput(final_narrative=final_narrative, success=True)

    except Exception as e:
        error_msg = f"General error in fill_placeholders: {str(e)}"
        ctx.error(error_msg)
        import traceback
        tb_str = traceback.format_exc()
        ctx.error(f"Traceback: {tb_str}")
        # Kembalikan template asli jika ada error parah, dengan pesan error
        return FillPlaceholdersOutput(
            final_narrative=payload.response_template, # Atau pesan error
            success=False, 
            error=error_msg
        )

# --- Menjalankan Server ---
if __name__ == "__main__":
    debug_print("Running Placeholder System Server directly (stdio)...", file=sys.stderr)
    # Tidak ada inisialisasi resource di sini.
    # MCP CLI akan mengimpor modul dan menemukan objek 'mcp'.
    mcp.run()

debug_print("--- PLACEHOLDER MCP SERVER MODULE LOADED ---", file=sys.stderr)