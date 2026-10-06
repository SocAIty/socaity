#!/usr/bin/env python3
"""
Stress how many concurrent catalog jobs the stack tolerates.

Flux Schnell by default, optional mix of DeepSeek V3. Measures wall time
and per-job latency.

Requirements
------------
- ``SOCAITY_API_KEY`` in the environment (same as other ``socaity`` tests).
- APIPod gate: set ``APIPOD_GATE_URL`` (default ``https://api.socaity.ai``).
- Backend at ``SOCAITY_BACKEND_URL`` / ``http://127.0.0.1:8000`` for catalog resolve.

Run from the socaity package directory::

    python test/stress/simultaneous_jobs.py --jobs 40 --concurrency 10 --mixed
"""

from __future__ import annotations

import argparse
import asyncio
import os
import random
import statistics
import sys
import time
import traceback
from dataclasses import dataclass
from functools import partial
from typing import List, Literal, Optional

from socaity import client

JobKind = Literal["flux", "deepseek"]

_FLUX = "black-forest-labs-flux-schnell/predictions"
_DEEPSEEK = "deepseek-ai-deepseek-v3/predictions"


@dataclass
class JobOutcome:
    index: int
    kind: JobKind
    ok: bool
    seconds: float
    error: Optional[str] = None


def _run_flux(idx: int, timeout_s: Optional[float]):
    job = client.run(
        _FLUX,
        prompt=f"minimal abstract color stress job {idx}",
        num_outputs=1,
        num_inference_steps=1,
        aspect_ratio="1:1",
        output_format="webp",
        go_fast=True,
    )
    return job.get_result(timeout_s=timeout_s)


def _run_deepseek(idx: int, timeout_s: Optional[float]):
    job = client.run(
        _DEEPSEEK,
        prompt=f"Say OK {idx}",
        max_tokens=32,
        temperature=0.3,
    )
    return job.get_result(timeout_s=timeout_s)


def _run_one_job(idx: int, kind: JobKind, timeout_s: Optional[float]) -> JobOutcome:
    t0 = time.perf_counter()
    try:
        if kind == "flux":
            _run_flux(idx, timeout_s)
        else:
            _run_deepseek(idx, timeout_s)
        return JobOutcome(index=idx, kind=kind, ok=True, seconds=time.perf_counter() - t0)
    except Exception as exc:
        return JobOutcome(
            index=idx,
            kind=kind,
            ok=False,
            seconds=time.perf_counter() - t0,
            error=f"{type(exc).__name__}: {exc}\n{traceback.format_exc(limit=2)}",
        )


async def _stress_async(
    *,
    total_jobs: int,
    concurrency: int,
    mixed_fraction: float,
    timeout_s: Optional[float],
    seed: int,
) -> List[JobOutcome]:
    rng = random.Random(seed)
    sem = asyncio.Semaphore(concurrency)
    loop = asyncio.get_running_loop()

    async def guarded(i: int) -> JobOutcome:
        kind: JobKind = "deepseek" if rng.random() < mixed_fraction else "flux"
        async with sem:
            return await loop.run_in_executor(
                None,
                partial(_run_one_job, i, kind, timeout_s),
            )

    return await asyncio.gather(*(guarded(i) for i in range(total_jobs)))


def _print_summary(outcomes: List[JobOutcome], wall_s: float) -> None:
    ok = [o for o in outcomes if o.ok]
    bad = [o for o in outcomes if not o.ok]
    latencies = [o.seconds for o in ok]

    print("\n=== Stress summary ===")
    print(f"Wall clock (async gather): {wall_s:.2f}s")
    print(f"Total jobs:   {len(outcomes)}")
    print(f"Succeeded:    {len(ok)}")
    print(f"Failed:       {len(bad)}")
    if latencies:
        print(f"Latency mean: {statistics.mean(latencies):.2f}s")
        print(f"Latency p50:  {statistics.median(latencies):.2f}s")
        if len(latencies) >= 2:
            s = sorted(latencies)
            idx = int(round(0.95 * (len(s) - 1)))
            print(f"Latency p95:  {s[idx]:.2f}s")
    by_kind: dict[str, list[JobOutcome]] = {"flux": [], "deepseek": []}
    for o in outcomes:
        by_kind[o.kind].append(o)
    for k, rows in by_kind.items():
        if not rows:
            continue
        ks = sum(1 for r in rows if r.ok)
        print(f"  {k}: {ks}/{len(rows)} ok")

    if bad:
        print("\n--- First failures (up to 5) ---")
        for o in bad[:5]:
            print(f"  job {o.index} ({o.kind}) after {o.seconds:.2f}s:\n{o.error}")


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(
        description="Concurrent catalog jobs (Flux Schnell plus optional DeepSeek mix).",
    )
    p.add_argument("--jobs", type=int, default=24, help="Total jobs to run (default: 24).")
    p.add_argument("--concurrency", type=int, default=8, help="Max jobs in flight (default: 8).")
    p.add_argument(
        "--mixed",
        action="store_true",
        help="Send a fraction of jobs as DeepSeek V3 instead of Flux.",
    )
    p.add_argument(
        "--mixed-fraction",
        type=float,
        default=0.25,
        help="When --mixed: probability each job is DeepSeek (0..1, default: 0.25).",
    )
    p.add_argument(
        "--timeout",
        type=float,
        default=None,
        help="Per-job wait timeout in seconds (passed to get_result). Default: no limit.",
    )
    p.add_argument("--seed", type=int, default=42, help="RNG seed for mixed job selection.")
    args = p.parse_args(argv)

    if not os.getenv("SOCAITY_API_KEY"):
        print("SOCAITY_API_KEY is required.", file=sys.stderr)
        return 2
    if args.jobs < 1 or args.concurrency < 1:
        print("--jobs and --concurrency must be >= 1", file=sys.stderr)
        return 2
    mixed_fraction = args.mixed_fraction if args.mixed else 0.0
    if not 0.0 <= mixed_fraction <= 1.0:
        print("--mixed-fraction must be between 0 and 1", file=sys.stderr)
        return 2

    gate = os.environ.get("APIPOD_GATE_URL", "https://api.socaity.ai")
    print(
        f"Starting stress | gate={gate} | jobs={args.jobs} "
        f"concurrency={args.concurrency} mixed_fraction={mixed_fraction} "
        f"timeout={args.timeout}"
    )

    t0 = time.perf_counter()
    outcomes = asyncio.run(
        _stress_async(
            total_jobs=args.jobs,
            concurrency=args.concurrency,
            mixed_fraction=mixed_fraction,
            timeout_s=args.timeout,
            seed=args.seed,
        )
    )
    _print_summary(outcomes, time.perf_counter() - t0)
    return 0 if all(o.ok for o in outcomes) else 1


if __name__ == "__main__":
    raise SystemExit(main())
