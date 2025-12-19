import logging
from collections.abc import Iterable, Mapping
from functools import lru_cache
from pathlib import Path

from app.core.feature_flags.loader import build_in_memory_provider
from app.core.feature_flags.models import FeatureFlagKey, FlagContext, FlagDecision
from app.core.feature_flags.provider import FeatureFlagProvider
from app.core.feature_flags.utils import normalize_flag_key


DEFAULT_CONFIG_PATH = Path("config/feature_flags.example.json")


class FeatureFlagService:
    def __init__(self, provider: FeatureFlagProvider, environment: str, logger: logging.Logger | None = None):
        self._provider = provider
        self._environment = environment
        self._logger = logger or logging.getLogger(__name__)

    def evaluate(self, key: FeatureFlagKey, org_id: str | None = None, env: str | None = None) -> FlagDecision:
        context = FlagContext(env=env or self._environment, org_id=org_id)
        decision = self._provider.get_flag(normalize_flag_key(key), context)
        self._log_decision(decision, context)
        return decision

    def evaluate_many(
        self, keys: Iterable[FeatureFlagKey], org_id: str | None = None, env: str | None = None
    ) -> dict[FeatureFlagKey, FlagDecision]:
        context = FlagContext(env=env or self._environment, org_id=org_id)
        decisions = self._provider.get_many((normalize_flag_key(key) for key in keys), context)
        for decision in decisions.values():
            self._log_decision(decision, context)
        return decisions

    def _log_decision(self, decision: FlagDecision, context: FlagContext) -> None:
        masked_org_id = self._mask_org_id(context.org_id)
        self._logger.debug(
            "Feature flag evaluated key=%s value=%s source=%s org_id_present=%s org_id_suffix=%s env=%s",
            decision.key,
            decision.value,
            decision.source.value,
            context.org_id is not None,
            masked_org_id,
            context.env,
        )

    @staticmethod
    def _mask_org_id(org_id: str | None) -> str:
        if org_id is None:
            return ""
        return org_id[-6:]


def build_feature_flag_service(
    *,
    environment: str,
    env: Mapping[str, str] | None = None,
    config_path: Path | str | None = None,
    global_defaults: Mapping[FeatureFlagKey, bool] | None = None,
    fallback: bool = False,
) -> FeatureFlagService:
    provider = build_in_memory_provider(
        env=env,
        config_path=config_path or DEFAULT_CONFIG_PATH,
        global_defaults=global_defaults,
        fallback=fallback,
    )
    return FeatureFlagService(provider=provider, environment=environment)


@lru_cache(maxsize=1)
def get_cached_feature_flag_service(environment: str) -> FeatureFlagService:
    return build_feature_flag_service(environment=environment, config_path=DEFAULT_CONFIG_PATH)


def reset_feature_flag_service_cache() -> None:
    get_cached_feature_flag_service.cache_clear()
