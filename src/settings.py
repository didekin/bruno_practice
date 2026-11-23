from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_PATH = PROJECT_ROOT / "osplus_local.db"
SQL_DIR = PROJECT_ROOT / "sql"

CODEX_CONFIG_PATH = Path.home() / ".codex" / "config.toml"
MCP_SERVER_NAME = "userstory"
