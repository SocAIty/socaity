"""Simple process-local sliding-window rate limit for MCP tool calls."""
from __future__ import annotations

import os
import threading
import time
from collections import deque
from typing import Optional


class RateLimiter:
    """Allow at most ``rpm`` calls per rolling 60s window."""

    def __init__(self, rpm: Optional[int] = None):
        self.rpm = int(rpm if rpm is not None else os.environ.get("SOCAITY_MCP_RPM", "60"))
        self._hits: deque[float] = deque()
        self._lock = threading.Lock()

    def check(self) -> None:
        if self.rpm <= 0:
            return
        now = time.monotonic()
        with self._lock:
            while self._hits and now - self._hits[0] >= 60.0:
                self._hits.popleft()
            if len(self._hits) >= self.rpm:
                retry = 60.0 - (now - self._hits[0])
                raise RuntimeError(
                    f"MCP rate limit exceeded ({self.rpm}/min). Retry in {retry:.1f}s."
                )
            self._hits.append(now)


limiter = RateLimiter()
