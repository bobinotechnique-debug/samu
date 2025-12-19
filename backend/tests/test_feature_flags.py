from app.core.feature_flags import (
    FeatureFlagConfiguration,
    InMemoryFeatureFlagProvider,
    FlagContext,
    FlagDecisionSource,
    build_in_memory_provider,
    parse_env_flags,
)


def test_env_override_precedence(monkeypatch):
    env_flags = parse_env_flags({"FEATURE_PLANNING_TIMELINE_V2": "true"})
    provider = InMemoryFeatureFlagProvider(
        env_overrides=env_flags,
        org_overrides={"org-123": {"planning_timeline_v2": False}},
        global_defaults={"planning_timeline_v2": False},
    )
    decision = provider.get_flag("planning_timeline_v2", FlagContext(env="ci", org_id="org-123"))

    assert decision.value is True
    assert decision.source is FlagDecisionSource.ENV_OVERRIDE


def test_org_override_precedence():
    provider = InMemoryFeatureFlagProvider(
        org_overrides={"org-123": {"planning_timeline_v2": True}},
        global_defaults={"planning_timeline_v2": False},
    )
    decision = provider.get_flag("planning_timeline_v2", FlagContext(env="ci", org_id="org-123"))

    assert decision.value is True
    assert decision.source is FlagDecisionSource.ORG_OVERRIDE


def test_global_default_precedence_over_fallback():
    provider = InMemoryFeatureFlagProvider(global_defaults={"planning_timeline_v2": True}, fallback=False)
    decision = provider.get_flag("planning_timeline_v2", FlagContext(env="ci"))

    assert decision.value is True
    assert decision.source is FlagDecisionSource.GLOBAL_DEFAULT


def test_env_parsing_and_normalization():
    flags = parse_env_flags({"FEATURE_PLANNING_TIMELINE_V2": "1", "FEATURE_MISSIONS-NEW_FLOW": "false"})

    assert flags["planning_timeline_v2"] is True
    assert flags["missions_new_flow"] is False


def test_decision_source_enum_values():
    assert {
        FlagDecisionSource.ENV_OVERRIDE.value,
        FlagDecisionSource.ORG_OVERRIDE.value,
        FlagDecisionSource.GLOBAL_DEFAULT.value,
        FlagDecisionSource.FALLBACK.value,
    } == {"env_override", "org_override", "global_default", "fallback"}


def test_build_in_memory_provider_merges_configuration(tmp_path):
    config_path = tmp_path / "feature_flags.json"
    config = FeatureFlagConfiguration(
        global_defaults={"missions_new_flow": True}, org_overrides={"org-abc": {"missions_new_flow": False}}
    )
    config_path.write_text(
        '{"global_defaults": {"missions_new_flow": false}, "org_overrides": {"org-abc": {"missions_new_flow": true}}}'
    )

    provider = build_in_memory_provider(config_path=config_path, global_defaults=config.global_defaults, fallback=False)
    decision = provider.get_flag("missions_new_flow", FlagContext(env="ci", org_id="org-abc"))

    assert decision.value is True
    assert decision.source is FlagDecisionSource.ORG_OVERRIDE
