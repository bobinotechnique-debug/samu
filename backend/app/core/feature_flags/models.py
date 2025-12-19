from dataclasses import dataclass
from enum import Enum


FeatureFlagKey = str
FeatureFlagValue = bool


class FlagDecisionSource(str, Enum):
    ENV_OVERRIDE = "env_override"
    ORG_OVERRIDE = "org_override"
    GLOBAL_DEFAULT = "global_default"
    FALLBACK = "fallback"


@dataclass(frozen=True)
class FlagContext:
    env: str
    org_id: str | None = None


@dataclass(frozen=True)
class FlagDecision:
    key: FeatureFlagKey
    value: FeatureFlagValue
    source: FlagDecisionSource
