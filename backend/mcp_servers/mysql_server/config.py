# File: backend/mcp_servers/mysql_server/config.py
import os
from dotenv import load_dotenv

# Muat .env dari direktori yang sama dengan file config ini
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

class ServerSettings:
    DB_HOST: str = os.getenv("MYSQL_HOST")
    DB_USER: str = os.getenv("MYSQL_USER")
    DB_PASSWORD: str = os.getenv("MYSQL_PASSWORD")
    DB_NAME: str = os.getenv("MYSQL_DATABASE")
    DB_PORT: int = int(os.getenv("MYSQL_PORT", 3306))

    @property
    def DATABASE_URL(self) -> str:
        if all([self.DB_HOST, self.DB_USER, self.DB_PASSWORD, self.DB_NAME]):
            return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return ""

settings = ServerSettings()