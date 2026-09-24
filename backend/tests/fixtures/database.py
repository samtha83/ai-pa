import os
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture
def migration_database(tmp_path: Path) -> str:
    database_path = tmp_path / "test.db"
    database_url = f"sqlite:///{database_path}"
    environment = os.environ.copy()
    environment["DATABASE_URL"] = database_url
    subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=Path(__file__).resolve().parents[2],
        env=environment,
        check=True,
    )
    return database_url