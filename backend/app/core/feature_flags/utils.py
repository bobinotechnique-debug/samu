import re

from app.core.feature_flags.models import FeatureFlagKey


BOOLEAN_TRUE_VALUES = {"1", "true", "t", "yes", "y", "on"}
BOOLEAN_FALSE_VALUES = {"0", "false", "f", "no", "n", "off"}


def normalize_flag_key(raw_key: str) -> FeatureFlagKey:
    key = raw_key.strip().replace("-", "_")
    key = re.sub(r"[^A-Za-z0-9_]+", "_", key)
    key = re.sub(r"_+", "_", key)
    return key.strip("_").lower()


def parse_boolean_value(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in BOOLEAN_TRUE_VALUES:
        return True
    if normalized in BOOLEAN_FALSE_VALUES:
        return False
    raise ValueError(f"Invalid feature flag boolean value: {value}")
