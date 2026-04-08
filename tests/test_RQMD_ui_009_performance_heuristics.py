"""Tests for RQMD-UI-009 latency smoothing and anti-thrashing heuristics."""

from __future__ import annotations

from rqmd.render_heuristics import RenderModeController


def test_RQMD_ui_009_degrades_only_on_sustained_latency() -> None:
    controller = RenderModeController(
        target_ms=50.0, upper_ms=60.0, cooldown_seconds=2.0, window_size=9
    )

    # Single spike should not switch modes due to smoothing.
    for sample in [30.0, 31.0, 32.0, 120.0, 30.0, 31.0, 30.0, 32.0, 31.0]:
        decision = controller.observe(sample, now=10.0 + sample / 1000.0)

    assert controller.mode == "screen-write"
    assert decision.changed is False

    # Sustained slow timings should switch to append mode.
    timestamp = 20.0
    changed = False
    for sample in [72.0, 74.0, 70.0, 73.0, 71.0, 75.0, 72.0, 74.0, 73.0]:
        decision = controller.observe(sample, now=timestamp)
        timestamp += 0.2
        changed = changed or decision.changed

    assert changed is True
    assert controller.mode == "append"


def test_RQMD_ui_009_cooldown_blocks_oscillation() -> None:
    controller = RenderModeController(
        target_ms=50.0,
        upper_ms=60.0,
        hysteresis_ms=5.0,
        cooldown_seconds=3.0,
        window_size=5,
    )

    now = 100.0
    for sample in [70.0, 71.0, 72.0, 73.0, 74.0]:
        controller.observe(sample, now=now)
        now += 0.1

    assert controller.mode == "append"

    # Fast samples inside cooldown should not immediately recover.
    for sample in [20.0, 21.0, 22.0, 23.0, 24.0]:
        decision = controller.observe(sample, now=now)
        now += 0.2

    assert controller.mode == "append"
    assert decision.changed is False


def test_RQMD_ui_009_recovery_uses_hysteresis_threshold() -> None:
    controller = RenderModeController(
        target_ms=50.0,
        upper_ms=60.0,
        hysteresis_ms=5.0,
        cooldown_seconds=1.0,
        window_size=7,
    )

    now = 200.0
    for sample in [68.0, 69.0, 70.0, 71.0, 72.0, 70.0, 69.0]:
        controller.observe(sample, now=now)
        now += 0.2

    assert controller.mode == "append"

    # Move beyond cooldown before attempting recovery.
    now += 1.5
    changed = False
    for sample in [40.0, 41.0, 42.0, 43.0, 40.0, 41.0, 42.0]:
        decision = controller.observe(sample, now=now)
        now += 0.2
        changed = changed or decision.changed

    assert changed is True
    assert decision.reason == "recover-latency"
    assert controller.mode == "screen-write"
