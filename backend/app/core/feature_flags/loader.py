import json
import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from app.core.feature_flags.models import FeatureFlagKey, FeatureFlagValue
from app.core.feature_flags.provider import InMemoryFeatureFlagProvider
from app.core.feature_flags.utils import normalize_flag_key, parse_boolean_value


DEFAULT_FEATURE_FLAG_CONFIG_PATH = Path("config/feature_flags.example.json")


@dataclass(frozen=True)
class FeatureFlagConfiguration:
    global_defaults: Mapping[FeatureFlagKey, FeatureFlagValue]
    org_overrides: Mapping[str, Mapping[FeatureFlagKey, FeatureFlagValue]]


def parse_env_flags(env: Mapping[str, str] | None = None, prefix: str = "FEATURE_") -> dict[FeatureFlagKey, bool]:
    source = env or os.environ
    flags: dict[FeatureFlagKey, bool] = {}
    for key, raw_value in source.items():
        if not key.startswith(prefix):
            continue
        normalized_key = normalize_flag_key(key.removeprefix(prefix))
        flags[normalized_key] = parse_boolean_value(raw_value)
    return flags


def load_feature_flag_configuration(path: Path | str | None = None) -> FeatureFlagConfiguration:
    if path is None:
        path = DEFAULT_FEATURE_FLAG_CONFIG_PATH
    config_path = Path(path)
    if not config_path.exists():
        return FeatureFlagConfiguration(global_defaults={}, org_overrides={})

    contents = json.loads(config_path.read_text())
    raw_globals = contents.get("global_defaults", {})
    raw_orgs = contents.get("org_overrides", {})
    global_defaults = {normalize_flag_key(key): bool(value) for key, value in raw_globals.items()}
    org_overrides: dict[str, dict[FeatureFlagKey, FeatureFlagValue]] = {}
    for org_id, flags in raw_orgs.items():
        org_overrides[str(org_id)] = {normalize_flag_key(key): bool(value) for key, value in flags.items()}

    return FeatureFlagConfiguration(global_defaults=global_defaults, org_overrides=org_overrides)


def build_in_memory_provider(
    *,
    env: Mapping[str, str] | None = None,
    config_path: Path | str | None = None,
    global_defaults: Mapping[FeatureFlagKey, FeatureFlagValue] | None = None,
    fallback: FeatureFlagValue = False,
) -> InMemoryFeatureFlagProvider:
    env_overrides = parse_env_flags(env)
    config = load_feature_flag_configuration(config_path)
    merged_global_defaults: dict[FeatureFlagKey, FeatureFlagValue] = {}
    merged_global_defaults.update(global_defaults or {})
    merged_global_defaults.update(config.global_defaults)
    return InMemoryFeatureFlagProvider(
        env_overrides=env_overrides,
        org_overrides=config.org_overrides,
        global_defaults=merged_global_defaults,
        fallback=fallback,
    )
