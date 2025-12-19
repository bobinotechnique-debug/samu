from pathlib import Path

import pytest

from app.core import config


def _reset_settings_cache() -> None:
    config.get_settings.cache_clear()


def test_env_var_precedence_over_env_files(monkeypatch, tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "SAMU_DATABASE_URL=sqlite+pysqlite:///from-env-file",
                "SAMU_REDIS_URL=redis://env-file",
            ]
        )
    )
    env_local = tmp_path / ".env.local"
    env_local.write_text("SAMU_DATABASE_URL=sqlite+pysqlite:///from-env-local")

    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("SAMU_ENVIRONMENT", "local")
    monkeypatch.setenv("SAMU_TESTING", "false")
    monkeypatch.setenv("SAMU_DATABASE_URL", "sqlite+pysqlite:///from-env-var")
    monkeypatch.setenv("SAMU_REDIS_URL", "redis://env-var")

    _reset_settings_cache()
    settings = config.get_settings()
    assert settings.database_url == "sqlite+pysqlite:///from-env-var"
    assert settings.redis_url == "redis://env-var"

    _reset_settings_cache()
    monkeypatch.delenv("SAMU_DATABASE_URL", raising=False)
    monkeypatch.delenv("SAMU_REDIS_URL", raising=False)

    settings_from_files = config.get_settings()
    assert settings_from_files.database_url == "sqlite+pysqlite:///from-env-local"
    assert settings_from_files.redis_url == "redis://env-file"
    _reset_settings_cache()


def test_non_local_env_requires_runtime_settings(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("SAMU_ENVIRONMENT", "staging")
    monkeypatch.setenv("SAMU_TESTING", "false")
    monkeypatch.delenv("SAMU_DATABASE_URL", raising=False)
    monkeypatch.delenv("SAMU_REDIS_URL", raising=False)

    _reset_settings_cache()
    with pytest.raises(RuntimeError):
        config.get_settings()
    _reset_settings_cache()
