# scripts/test_mcp_servers.py (Revisi Final dengan .bat)

import asyncio
import sys
import os
import json
from pathlib import Path
from contextlib import AsyncExitStack
from pprint import pprint

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class McpServerClient:
    def __init__(self, name: str, config: dict):
        self.name = name
        self.config = config
        self.session: ClientSession | None = None

    async def initialize(self, exit_stack: AsyncExitStack):
        print(f"🔄 Menginisialisasi server: {self.name}...")
        
        command_path = project_root / self.config["command"]
        args_list = self.config.get("args", [])

        if not command_path.exists():
            raise FileNotFoundError(f"Skrip command '{self.name}' tidak ditemukan di: {command_path}")

        params = StdioServerParameters(
            command=str(command_path),
            args=args_list,
            env=self.config.get("env")
        )
        
        transport = await exit_stack.enter_async_context(stdio_client(params))
        self.session = await exit_stack.enter_async_context(ClientSession(*transport))
        await asyncio.wait_for(self.session.initialize(), timeout=20.0)
        print(f"✅ Server '{self.name}' berhasil terhubung.")

async def main():
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    print("--- Memulai Tes Integrasi Terisolasi untuk Server MCP ---")
    
    config_path = project_root / "servers_config.json"
    if not config_path.exists():
        print(f"🔥 GAGAL: File '{config_path}' tidak ditemukan.")
        return

    with open(config_path, "r") as f:
        server_configs = json.load(f)["mcpServers"]

    server_clients: list[McpServerClient] = [
        McpServerClient(name, conf)
        for name, conf in server_configs.items()
        if not conf.get("disabled")
    ]
    
    try:
        async with AsyncExitStack() as stack:
            for client in server_clients:
                await client.initialize(stack)

            print("\n--- Semua server siap. Memulai pengujian tool... ---\n")

            graphiti_client = next(c for c in server_clients if c.name == "graphiti_server")
            mysql_client = next(c for c in server_clients if c.name == "mysql_server")

            print("--- Tes 1: Memanggil graphiti_server.get_relevant_schema ---")
            schema_payload = {"intent": "test", "entities": []}
            schema_result = await graphiti_client.session.call_tool("get_relevant_schema", schema_payload)
            assert schema_result["success"], "get_relevant_schema harus berhasil"
            print("✅ Tes 1 BERHASIL.\n")
            
            print("--- Tes 2: Memanggil mysql_server.execute_operation_plan ---")
            db_plan_payload = {"payload": {"operations": [{"operation_id": "test_select", "main_table": "mastercustomer", "select_columns": [{"field_name": "mastercustomer.Code"}], "limit": 1}]}}
            db_result = await mysql_client.session.call_tool("execute_operation_plan", db_plan_payload)
            assert db_result["success"], "execute_operation_plan harus berhasil"
            assert db_result["results"]["test_select"]["status"] == "success", "Operasi di dalam mysql_server harus sukses"
            print("✅ Tes 2 BERHASIL.")

            print("\n\n🎉🎉🎉 SEMUA TES INTEGRASI SERVER BERHASIL! 🎉🎉🎉")

    except Exception as e:
        print(f"\n🔥 GAGAL saat menjalankan tes: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())