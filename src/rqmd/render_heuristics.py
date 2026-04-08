"""Adaptive render mode heuristics for interactive latency control."""

from __future__ import annotations

import statistics
import time
from collections import deque
from dataclasses import dataclass
from typing import Literal

RenderMode = Literal["screen-write", "append"]


@dataclass
class RenderModeDecision:
    mode: RenderMode
    changed: bool
    reason: str | None
    median_ms: float | None
    p95_ms: float | None


class RenderModeController:
    """Latency-aware mode controller with smoothing, hysteresis, and cooldown."""

    def __init__(
        self,
        target_ms: float = 50.0,
        upper_ms: float = 60.0,
        hysteresis_ms: float = 5.0,
        cooldown_seconds: float = 3.0,
        window_size: int = 9,
    ) -> None:
        self.target_ms = target_ms
        self.upper_ms = upper_ms
        self.hysteresis_ms = hysteresis_ms
        self.cooldown_seconds = cooldown_seconds
        self.samples: deque[float] = deque(maxlen=max(3, window_size))
        self.mode: RenderMode = "screen-write"
        self.last_transition_at: float | None = None

    def reset(self, mode: RenderMode = "screen-write") -> None:
        self.samples.clear()
        self.mode = mode
        self.last_transition_at = None

    def _compute_stats(self) -> tuple[float | None, float | None]:
        if not self.samples:
            return None, None
        values = list(self.samples)
        median_ms = float(statistics.median(values))
        ordered = sorted(values)
        p95_index = int(round((len(ordered) - 1) * 0.95))
        p95_ms = float(ordered[p95_index])
        return median_ms, p95_ms

    def observe(self, render_ms: float, now: float | None = None) -> RenderModeDecision:
        timestamp = time.monotonic() if now is None else float(now)
        self.samples.append(float(render_ms))
        median_ms, p95_ms = self._compute_stats()

        if median_ms is None or p95_ms is None:
            return RenderModeDecision(self.mode, False, None, median_ms, p95_ms)

        in_cooldown = (
            self.last_transition_at is not None
            and (timestamp - self.last_transition_at) < self.cooldown_seconds
        )
        if in_cooldown:
            return RenderModeDecision(self.mode, False, "cooldown", median_ms, p95_ms)

        if self.mode == "screen-write":
            # Degrade only when smoothed latency is persistently above budget.
            if median_ms > self.upper_ms and p95_ms > self.upper_ms:
                self.mode = "append"
                self.last_transition_at = timestamp
                return RenderModeDecision(
                    self.mode, True, "degrade-latency", median_ms, p95_ms
                )
            return RenderModeDecision(self.mode, False, None, median_ms, p95_ms)

        # Recovery path uses hysteresis to avoid threshold oscillation.
        recovery_target = self.target_ms - self.hysteresis_ms
        recovery_upper = self.upper_ms - self.hysteresis_ms
        if median_ms <= recovery_target and p95_ms <= recovery_upper:
            self.mode = "screen-write"
            self.last_transition_at = timestamp
            return RenderModeDecision(
                self.mode, True, "recover-latency", median_ms, p95_ms
            )

        return RenderModeDecision(self.mode, False, None, median_ms, p95_ms)
