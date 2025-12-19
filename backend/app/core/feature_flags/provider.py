from collections.abc import Iterable, Mapping
from typing import Protocol

from app.core.feature_flags.models import (
    FeatureFlagKey,
    FeatureFlagValue,
    FlagContext,
    FlagDecision,
    FlagDecisionSource,
)
from app.core.feature_flags.utils import normalize_flag_key


class FeatureFlagProvider(Protocol):
    def get_flag(self, key: FeatureFlagKey, ctx: FlagContext) -> FlagDecision:
        ...

    def get_many(self, keys: Iterable[FeatureFlagKey], ctx: FlagContext) -> dict[FeatureFlagKey, FlagDecision]:
        ...


class InMemoryFeatureFlagProvider:
    def __init__(
        self,
        *,
        env_overrides: Mapping[FeatureFlagKey, FeatureFlagValue] | None = None,
        org_overrides: Mapping[str, Mapping[FeatureFlagKey, FeatureFlagValue]] | None = None,
        global_defaults: Mapping[FeatureFlagKey, FeatureFlagValue] | None = None,
        fallback: FeatureFlagValue = False,
    ):
        self._env_overrides = self._normalize_map(env_overrides or {})
        self._org_overrides = {org: self._normalize_map(flags) for org, flags in (org_overrides or {}).items()}
        self._global_defaults = self._normalize_map(global_defaults or {})
        self._fallback = fallback

    def get_flag(self, key: FeatureFlagKey, ctx: FlagContext) -> FlagDecision:
        normalized_key = normalize_flag_key(key)
        env_value = self._env_overrides.get(normalized_key)
        if env_value is not None:
            return FlagDecision(key=normalized_key, value=env_value, source=FlagDecisionSource.ENV_OVERRIDE)

        if ctx.org_id:
            org_flags = self._org_overrides.get(ctx.org_id, {})
            if normalized_key in org_flags:
                return FlagDecision(
                    key=normalized_key, value=org_flags[normalized_key], source=FlagDecisionSource.ORG_OVERRIDE
                )

        if normalized_key in self._global_defaults:
            return FlagDecision(
                key=normalized_key, value=self._global_defaults[normalized_key], source=FlagDecisionSource.GLOBAL_DEFAULT
            )

        return FlagDecision(key=normalized_key, value=self._fallback, source=FlagDecisionSource.FALLBACK)

    def get_many(self, keys: Iterable[FeatureFlagKey], ctx: FlagContext) -> dict[FeatureFlagKey, FlagDecision]:
        return {normalize_flag_key(key): self.get_flag(key, ctx) for key in keys}

    @staticmethod
    def _normalize_map(flags: Mapping[FeatureFlagKey, FeatureFlagValue]) -> dict[FeatureFlagKey, FeatureFlagValue]:
        return {normalize_flag_key(key): bool(value) for key, value in flags.items()}
