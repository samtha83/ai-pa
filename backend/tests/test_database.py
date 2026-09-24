from sqlalchemy import create_engine, inspect


def test_migrations_create_isolated_provider_schema(migration_database: str):
    engine = create_engine(migration_database)
    inspector = inspect(engine)

    assert {"providers", "demo_sessions", "alembic_version"}.issubset(
        inspector.get_table_names()
    )
    assert inspector.get_foreign_keys("demo_sessions")[0]["referred_table"] == "providers"
    assert {index["name"] for index in inspector.get_indexes("demo_sessions")} == {
        "ix_demo_sessions_provider_id",
        "ix_demo_sessions_expires_at",
    }