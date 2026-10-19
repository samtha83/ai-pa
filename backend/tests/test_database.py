from sqlalchemy import create_engine, inspect


def test_migrations_create_isolated_provider_schema(migration_database: str):
    engine = create_engine(migration_database)
    inspector = inspect(engine)

    assert {
        "providers",
        "demo_sessions",
        "provider_preferences",
        "clients",
        "alembic_version",
    }.issubset(
        inspector.get_table_names()
    )
    assert inspector.get_foreign_keys("demo_sessions")[0]["referred_table"] == "providers"
    assert {index["name"] for index in inspector.get_indexes("demo_sessions")} == {
        "ix_demo_sessions_provider_id",
        "ix_demo_sessions_expires_at",
    }
    assert {
        "tone",
        "modality",
        "service_type",
        "template_settings",
        "boundaries",
    }.issubset({column["name"] for column in inspector.get_columns("providers")})
    preference_columns = {
        column["name"] for column in inspector.get_columns("provider_preferences")
    }
    assert {
        "provider_id",
        "working_hours",
        "session_duration",
        "buffer_time",
        "blackout_dates",
        "max_sessions_per_day",
        "summary_template",
    }.issubset(preference_columns)
    assert inspector.get_pk_constraint("provider_preferences")["constrained_columns"] == [
        "provider_id"
    ]
    assert inspector.get_foreign_keys("provider_preferences")[0]["referred_table"] == "providers"
    client_columns = {
        column["name"] for column in inspector.get_columns("clients")
    }
    assert {
        "id",
        "provider_id",
        "name",
        "email",
        "phone",
        "timezone",
        "service_type",
        "goals",
        "status",
        "created_at",
        "updated_at",
    }.issubset(client_columns)
    assert inspector.get_foreign_keys("clients")[0]["referred_table"] == "providers"
    assert {index["name"] for index in inspector.get_indexes("clients")} == {
        "ix_clients_provider_id"
    }