#!/usr/bin/env python3
"""
Stress how many concurrent SocAIty (FastSDK) jobs the stack tolerates.

Uses the published ``socaity`` SDK clients (Flux Schnell by default, optional
mix of DeepSeek V3) and measures wall time plus per-job latency.

Requirements
------------
- ``SOCAITY_API_KEY`` in the environment (same as other ``socaity`` tests).
- **Inference API** (this script only submits jobs here): set
  ``INFERENCE_BACKEND_URL`` to match ``socaity_backend`` / the inference gateway,
  e.g. ``http://localhost:8001``. Fallbacks: ``NUXT_PUBLIC_INFER_API_BASE_URL``,
  then legacy ``SOCAITY_API_BASE``; if none are set, production
  ``https://api.socaity.ai`` is used.
- **Service URL layout**: by default the registry uses
  ``{INFERENCE_BACKEND_URL}/services/{INFERENCE_API_VERSION}/{service_id}`` (APIPod
  gateway). Set ``INFERENCE_API_VERSION`` if not ``v1``. Use
  ``SOCAITY_INFERENCE_ADDRESS_STYLE=cache_path`` only if you must keep the legacy
  ``/v1/{org}/{model}`` path from ``sdk/cache/*.json``.
- **SocAIty web backend** (accounts, webapi, orchestrator callbacks): run at
  e.g. ``http://localhost:8000`` via ``WEB_BACKEND_URL`` / ``SOCAITY_BACKEND_URL``
  in the rest of your stack; this stress harness does not call it for Flux /
  DeepSeek predictions, but you should point those services at the same local
  URLs so the full platform stays consistent.
- Network reachability from this machine to the inference base URL.

Run (from the ``socaity`` package directory, with the package on PYTHONPATH)::

    pip install -e .
    python test/stress/simultaneous_jobs.py --jobs 40 --concurrency 10 --mixed

Or with repo root on path::

    PYTHONPATH=socaity python socaity/test/stress/simultaneous_jobs.py --help
"""

from __future__ import annotations

import argparse
import asyncio
import importlib.util
import json
import os
import random
import statistics
import sys
import time
import traceback
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Any, List, Literal, Optional, Tuple, Type
from urllib.parse import urlparse

from apipod_registry.definitions.service_definitions import ServiceDefinition
from apipod_registry.parsers.service_adress_parser import create_service_address

JobKind = Literal["flux", "deepseek"]

# Generated clients live under ``socaity/sdk/...``. Load them from disk so this
# script does not import ``socaity``'s package ``__init__`` (which pulls in
# optional ``fastsdk.service_management`` not present in every dev checkout).
_SDK_DIR = Path(__file__).resolve().parent.parent.parent / "socaity" / "sdk"
_CACHE_DIR = _SDK_DIR / "cache"
_FLUX_SERVICE_ID = "817bca01-a048-4959-84e3-f8be56044f48"
_DEEPSEEK_SERVICE_ID = "4cac0e8e-6418-4f48-b2cb-e5a237037f6a"
_CLIENT_CLASS_CACHE: dict[Tuple[str, ...], Type[Any]] = {}
_REGISTRY_BOOTSTRAPPED = False


def _inference_api_origin() -> str:
    """Resolve inference gateway origin (same env names as ``socaity_backend`` / Nuxt)."""
    for key in (
        "INFERENCE_BACKEND_URL",
        "NUXT_PUBLIC_INFER_API_BASE_URL",
        "SOCAITY_API_BASE",
    ):
        v = os.environ.get(key)
        if v and v.strip():
            return v.strip().rstrip("/")
    return "https://api.socaity.ai"


def _bootstrap_registry_from_cache(*, inference_origin: str) -> None:
    """
    Register Flux / DeepSeek service definitions from ``socaity/sdk/cache/*.json``.

    Cache files may use a legacy ``/v1/{org}/{model}`` path; the APIPod gateway
    mounts SocAIty services at ``/services/{api_version}/{service_id}``. Default
    is that layout (aligned with ``socaity_backend`` and ``apipodgate``).

    Set ``SOCAITY_INFERENCE_ADDRESS_STYLE=cache_path`` to keep only the cache
    file's URL path and swap in ``inference_origin`` as the host.
    """
    global _REGISTRY_BOOTSTRAPPED
    if _REGISTRY_BOOTSTRAPPED:
        return
    from fastsdk import FastSDK

    api_base = inference_origin.rstrip("/")
    fsdk = FastSDK()
    style = os.environ.get("SOCAITY_INFERENCE_ADDRESS_STYLE", "services").strip().lower()
    api_ver = os.environ.get("INFERENCE_API_VERSION", "v1").strip().strip("/")
    for sid in (_FLUX_SERVICE_ID, _DEEPSEEK_SERVICE_ID):
        if fsdk.get_service(sid):
            continue
        cache_file = _CACHE_DIR / f"{sid}.json"
        if not cache_file.is_file():
            raise FileNotFoundError(
                f"Missing service cache {cache_file}; run SocAIty package sync or "
                "commit cache JSON for this service id."
            )
        raw: dict[str, Any] = json.loads(cache_file.read_text())
        if style in ("cache_path", "legacy", "hierarchical"):
            url = (raw.get("service_address") or {}).get("url", "")
            parsed = urlparse(url)
            path = parsed.path or ""
            if path and not path.startswith("/"):
                path = "/" + path
            new_url = f"{api_base}{path}"
        else:
            new_url = f"{api_base}/services/{api_ver}/{sid}"
        svc = ServiceDefinition.model_validate(raw)
        svc.id = sid
        spec = (svc.specification or "socaity").lower()
        svc.service_address = create_service_address(new_url, spec)
        fsdk.add_service(svc)
    _REGISTRY_BOOTSTRAPPED = True


def _load_generated_client_class(rel_parts: Tuple[str, ...], class_name: str) -> Type[Any]:
    """Load a single generated ``*.py`` client without importing ``socaity``."""
    cache_key = rel_parts + (class_name,)
    if cache_key in _CLIENT_CLASS_CACHE:
        return _CLIENT_CLASS_CACHE[cache_key]
    path = _SDK_DIR.joinpath(*rel_parts)
    if not path.is_file():
        raise FileNotFoundError(f"SDK client missing (expected file): {path}")
    mod_name = "_socaity_stress_" + "__".join(rel_parts).replace(".py", "")
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load spec for {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    cls = getattr(mod, class_name)
    _CLIENT_CLASS_CACHE[cache_key] = cls
    return cls


@dataclass
class JobOutcome:
    index: int
    kind: JobKind
    ok: bool
    seconds: float
    error: Optional[str] = None


def _run_flux(api_key: str, idx: int, timeout_s: Optional[float]) -> Any:
    flux_cls = _load_generated_client_class(
        ("replicate", "black_forest_labs", "flux_schnell.py"),
        "flux_schnell",
    )
    client = flux_cls(api_key=api_key)
    job = client.predictions(
        prompt=f"minimal abstract color stress job {idx}",
        num_outputs=1,
        num_inference_steps=1,
        aspect_ratio="1:1",
        output_format="webp",
        go_fast=True,
    )
    return job.get_result(timeout_s=timeout_s)


def _run_deepseek(api_key: str, idx: int, timeout_s: Optional[float]) -> Any:
    deepseek_cls = _load_generated_client_class(
        ("replicate", "deepseek_ai", "deepseek_v3.py"),
        "deepseek_v3",
    )
    client = deepseek_cls(api_key=api_key)
    job = client.predictions(
        prompt=f"Say OK {idx}",
        max_tokens=32,
        temperature=0.3,
    )
    return job.get_result(timeout_s=timeout_s)


def _run_one_job(
    api_key: str,
    idx: int,
    kind: JobKind,
    timeout_s: Optional[float],
) -> JobOutcome:
    t0 = time.perf_counter()
    try:
        if kind == "flux":
            _run_flux(api_key, idx, timeout_s)
        else:
            _run_deepseek(api_key, idx, timeout_s)
        dt = time.perf_counter() - t0
        return JobOutcome(index=idx, kind=kind, ok=True, seconds=dt, error=None)
    except Exception as exc:  # noqa: BLE001 — surface any SDK / HTTP failure
        dt = time.perf_counter() - t0
        return JobOutcome(
            index=idx,
            kind=kind,
            ok=False,
            seconds=dt,
            error=f"{type(exc).__name__}: {exc}\n{traceback.format_exc(limit=2)}",
        )


async def _stress_async(
    *,
    api_key: str,
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
        kind: JobKind = (
            "deepseek" if rng.random() < mixed_fraction else "flux"
        )
        async with sem:
            return await loop.run_in_executor(
                None,
                partial(_run_one_job, api_key, i, kind, timeout_s),
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


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(
        description="Concurrent SocAIty SDK jobs (Flux Schnell ± DeepSeek mix).",
    )
    p.add_argument(
        "--jobs",
        type=int,
        default=24,
        help="Total jobs to run (default: 24).",
    )
    p.add_argument(
        "--concurrency",
        type=int,
        default=8,
        help="Max jobs in flight at once (default: 8).",
    )
    p.add_argument(
        "--mixed",
        action="store_true",
        help="Send a fraction of jobs as DeepSeek V3 (short text) instead of Flux.",
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
    p.add_argument(
        "--seed",
        type=int,
        default=42,
        help="RNG seed for mixed job selection (default: 42).",
    )
    args = p.parse_args(argv)

    api_key = os.getenv("SOCAITY_API_KEY")
    if not api_key:
        print("SOCAITY_API_KEY is required.", file=sys.stderr)
        return 2

    if args.jobs < 1:
        print("--jobs must be >= 1", file=sys.stderr)
        return 2
    if args.concurrency < 1:
        print("--concurrency must be >= 1", file=sys.stderr)
        return 2
    mixed_fraction = args.mixed_fraction if args.mixed else 0.0
    if not 0.0 <= mixed_fraction <= 1.0:
        print("--mixed-fraction must be between 0 and 1", file=sys.stderr)
        return 2

    infer_origin = _inference_api_origin()
    print(
        f"Starting stress | inference_base={infer_origin} | jobs={args.jobs} "
        f"concurrency={args.concurrency} mixed_fraction={mixed_fraction} "
        f"timeout={args.timeout}"
    )

    _bootstrap_registry_from_cache(inference_origin=infer_origin)

    t0 = time.perf_counter()
    outcomes = asyncio.run(
        _stress_async(
            api_key=api_key,
            total_jobs=args.jobs,
            concurrency=args.concurrency,
            mixed_fraction=mixed_fraction,
            timeout_s=args.timeout,
            seed=args.seed,
        )
    )
    wall = time.perf_counter() - t0
    _print_summary(outcomes, wall)

    return 0 if all(o.ok for o in outcomes) else 1


if __name__ == "__main__":
    raise SystemExit(main())
