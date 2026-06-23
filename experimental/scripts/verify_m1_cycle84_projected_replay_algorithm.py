#!/usr/bin/env python3
"""Audit the projected-census replay algorithm on exact toy models.

This script supports
experimental/notes/m1/m1_cycle84_projected_replay_algorithm_audit.md.
It does not rerun the Cycle84 census. Instead it mechanically checks the
algorithmic pieces used by the generated C++ replay:

* translated circular slices in sorted modular lists;
* the tau-canonical shard partition;
* five-slot/two-slot replay against brute-force enumeration on small exact
  models with tau-pair log sums and nontrivial duplicate bins;
* the SHA256 of the generated Cycle84 C++ source for the 16-thread replay.
"""

from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import sys
from itertools import product
from pathlib import Path
from typing import Any, Dict, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import verify_m1_cycle84_projected_census_shard_replay as replay


TOY_SLOT_COUNT = 7
TOY_KEY_COUNT = 6
TOY_COLOR_MOD = 8
TOY_TARGET_COLOR = 3


def addm(a: int, b: int, mod: int) -> int:
    return (a + b) % mod


def subm(a: int, b: int, mod: int) -> int:
    return (a - b) % mod


def tau_key(key: int) -> int:
    return key ^ 1


def half_keys() -> list[int]:
    return [key for key in range(TOY_KEY_COUNT) if key < tau_key(key)]


def circular_slice(
    values: Sequence[int],
    start: int,
    low: int,
    high: int,
    mod: int,
) -> list[int]:
    if low >= high:
        return []
    aa = start + low
    bb = start + high
    a = aa % mod
    b = bb % mod
    if aa // mod == (bb - 1) // mod:
        if b == 0:
            return [value for value in values if a <= value]
        return [value for value in values if a <= value < b]
    return [value for value in values if value >= a] + [
        value for value in values if value < b
    ]


def brute_circular_slice(
    values: Sequence[int],
    start: int,
    low: int,
    high: int,
    mod: int,
) -> list[int]:
    return [value for value in values if low <= (value - start) % mod < high]


def test_circular_slices() -> Dict[str, int]:
    cases = 0
    for mod in (37, 64, 101):
        values = sorted({(7 * i * i + 3 * i + 5) % mod for i in range(2 * mod)})
        for start in range(mod):
            for low in range(0, mod, max(1, mod // 8)):
                for width in range(0, mod - low + 1, max(1, mod // 9)):
                    high = low + width
                    got = circular_slice(values, start, low, high, mod)
                    want = brute_circular_slice(values, start, low, high, mod)
                    if sorted(got) != sorted(want):
                        raise AssertionError((mod, start, low, high, got, want))
                    cases += 1
    return {"cases_checked": cases}


def make_toy_model(seed: int) -> Dict[str, Any]:
    mod = 4_096 + 2 * seed
    constants = [10_000 + 2 * seed + 2 * t for t in range(TOY_SLOT_COUNT)]
    logs = [[0] * TOY_KEY_COUNT for _ in range(TOY_SLOT_COUNT)]
    colors = [[0] * TOY_KEY_COUNT for _ in range(TOY_SLOT_COUNT)]

    for t in range(TOY_SLOT_COUNT):
        for key in half_keys():
            raw = (
                104_729 * (seed + 1)
                + 15_485_863 * (t + 1)
                + 32_452_843 * (key + 3)
                + 97 * t * key
            ) % mod
            logs[t][key] = raw
            logs[t][tau_key(key)] = subm(constants[t], raw, mod)

            color = (seed + 2 * t + key) % TOY_COLOR_MOD
            colors[t][key] = color
            colors[t][tau_key(key)] = (4 - color) % TOY_COLOR_MOD

    kappa = sum(constants) % mod
    if kappa % 2:
        raise AssertionError("toy kappa should be even")
    root0 = kappa // 2
    root1 = root0 + mod // 2
    if root1 >= mod:
        root1 -= mod

    return {
        "seed": seed,
        "mod": mod,
        "shards": 32,
        "logs": logs,
        "colors": colors,
        "constants": constants,
        "kappa": kappa,
        "root0": root0,
        "root1": root1,
    }


def color_sum(keys: Sequence[int], colors: Sequence[Sequence[int]]) -> int:
    return sum(colors[t][key] for t, key in enumerate(keys)) % TOY_COLOR_MOD


def log_sum(keys: Sequence[int], logs: Sequence[Sequence[int]], mod: int) -> int:
    return sum(logs[t][key] for t, key in enumerate(keys)) % mod


def canonical_key(total: int, root: int, mod: int) -> int:
    z = subm(total, root, mod)
    return min(z, mod - z)


def shard_bounds(mod: int, shards: int, shard: int) -> tuple[int, int]:
    half = mod // 2
    return (half * shard // shards, half * (shard + 1) // shards)


def shard_for_key(key: int, mod: int, shards: int) -> int | None:
    half = mod // 2
    if not 0 <= key < half:
        return None
    # Use a short loop; toy shard count is intentionally small.
    for shard in range(shards):
        lo, hi = shard_bounds(mod, shards, shard)
        if lo <= key < hi:
            return shard
    raise AssertionError(("key did not land in a shard", key))


def energy(counts: Dict[int, int]) -> int:
    return sum(count * (count - 1) for count in counts.values())


def max_multiplicity(counts: Dict[int, int]) -> int:
    return max(counts.values(), default=1)


def brute_counts(model: Dict[str, Any]) -> Dict[str, Any]:
    logs = model["logs"]
    colors = model["colors"]
    mod = model["mod"]
    shards = model["shards"]
    root0 = model["root0"]
    root1 = model["root1"]
    counts: Dict[int, int] = {}
    fixed0 = 0
    fixed1 = 0
    entries = 0

    for rest in product(range(TOY_KEY_COUNT), repeat=TOY_SLOT_COUNT - 1):
        for first in half_keys():
            keys = (first, *rest)
            if color_sum(keys, colors) != TOY_TARGET_COLOR:
                continue
            total = log_sum(keys, logs, mod)
            if total == root0:
                fixed0 += 1
            if total == root1:
                fixed1 += 1
            key = canonical_key(total, root0, mod)
            shard = shard_for_key(key, mod, shards)
            if shard is None:
                continue
            counts[key] = counts.get(key, 0) + 1
            entries += 1

    return {
        "counts": counts,
        "entries": entries,
        "fixed_counts": [fixed0, fixed1],
        "energy": energy(counts),
        "max_multiplicity": max_multiplicity(counts),
    }


def build_base_tables(model: Dict[str, Any]) -> list[list[int]]:
    logs = model["logs"]
    colors = model["colors"]
    mod = model["mod"]
    base = [[] for _ in range(TOY_COLOR_MOD)]

    for keys in product(range(TOY_KEY_COUNT), repeat=4):
        for first in half_keys():
            prefix = (first, *keys)
            color = sum(colors[t][key] for t, key in enumerate(prefix)) % TOY_COLOR_MOD
            value = sum(logs[t][key] for t, key in enumerate(prefix)) % mod
            base[color].append(value)

    for bucket in base:
        bucket.sort()
    return base


def split_replay_counts(model: Dict[str, Any]) -> Dict[str, Any]:
    logs = model["logs"]
    colors = model["colors"]
    mod = model["mod"]
    shards = model["shards"]
    root0 = model["root0"]
    root1 = model["root1"]
    half = mod // 2
    base = build_base_tables(model)
    counts: Dict[int, int] = {}
    fixed0 = 0
    fixed1 = 0
    entries = 0

    tails = []
    for key5 in range(TOY_KEY_COUNT):
        for key6 in range(TOY_KEY_COUNT):
            log_tail = (logs[5][key5] + logs[6][key6]) % mod
            color_tail = (colors[5][key5] + colors[6][key6]) % TOY_COLOR_MOD
            tails.append((log_tail, color_tail))

    for log_tail, color_tail in tails:
        bucket = base[(TOY_TARGET_COLOR - color_tail) % TOY_COLOR_MOD]
        fixed0_target = subm(root0, log_tail, mod)
        fixed1_target = subm(root1, log_tail, mod)
        fixed0 += (
            bisect.bisect_right(bucket, fixed0_target)
            - bisect.bisect_left(bucket, fixed0_target)
        )
        fixed1 += (
            bisect.bisect_right(bucket, fixed1_target)
            - bisect.bisect_left(bucket, fixed1_target)
        )

    for shard in range(shards):
        lo, hi = shard_bounds(mod, shards, shard)
        l2 = mod - hi + 1
        u2 = min(mod, mod - lo + 1)
        for log_tail, color_tail in tails:
            bucket = base[(TOY_TARGET_COLOR - color_tail) % TOY_COLOR_MOD]
            start = subm(root0, log_tail, mod)
            selected = circular_slice(bucket, start, lo, hi, mod)
            if l2 < mod and l2 < u2:
                selected += circular_slice(bucket, start, l2, u2, mod)
            for log_base in selected:
                total = (log_base + log_tail) % mod
                key = canonical_key(total, root0, mod)
                if not lo <= key < hi:
                    raise AssertionError(("bad shard key", model["seed"], shard, key))
                counts[key] = counts.get(key, 0) + 1
                entries += 1

    if any(key >= half for key in counts):
        raise AssertionError(("boundary key entered split replay", model["seed"]))

    return {
        "counts": counts,
        "entries": entries,
        "fixed_counts": [fixed0, fixed1],
        "energy": energy(counts),
        "max_multiplicity": max_multiplicity(counts),
    }


def test_toy_model(seed: int) -> Dict[str, Any]:
    model = make_toy_model(seed)
    brute = brute_counts(model)
    split = split_replay_counts(model)
    if brute != split:
        raise AssertionError(("toy replay mismatch", seed, brute, split))
    duplicate_bins = sum(1 for count in brute["counts"].values() if count >= 2)
    if duplicate_bins == 0:
        raise AssertionError(("toy model has no duplicate bins", seed))
    return {
        "seed": seed,
        "mod": model["mod"],
        "shards": model["shards"],
        "entries": brute["entries"],
        "duplicate_bins": duplicate_bins,
        "fixed_counts": brute["fixed_counts"],
        "energy": brute["energy"],
        "max_multiplicity": brute["max_multiplicity"],
    }


def generated_source_sha256(threads: int = 16) -> str:
    log_tables = replay.load_log_tables()
    source = replay.render_cpp_source(
        log_tables["logs_mod_m"],
        log_tables["colors"],
        threads,
    )
    required_fragments = [
        "circular_slice(values, start, lo, hi",
        "uint64_t l2 = MOD - hi + 1;",
        "uint64_t canonical = std::min(z, MOD - z);",
        "energy += 2ULL * old;",
        "#pragma omp parallel num_threads(THREADS)",
    ]
    missing = [fragment for fragment in required_fragments if fragment not in source]
    if missing:
        raise AssertionError(("generated source missing fragments", missing))
    return hashlib.sha256(source.encode()).hexdigest()


def build_report() -> Dict[str, Any]:
    slice_report = test_circular_slices()
    toy_reports = [test_toy_model(seed) for seed in (3, 7, 11)]
    checks = {
        "circular_slice_matches_bruteforce": slice_report["cases_checked"] > 0,
        "toy_models_match_bruteforce": len(toy_reports) == 3,
        "toy_models_have_duplicate_bins": all(
            report["duplicate_bins"] > 0 for report in toy_reports
        ),
        "toy_models_have_nonzero_energy": all(report["energy"] > 0 for report in toy_reports),
    }
    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": "PROVED / AUDIT / FINITE-MODEL-ALGORITHM",
        "theorem_problem_id": "M1 Cycle84 projected replay algorithm audit",
        "circular_slice": slice_report,
        "toy_models": toy_reports,
        "generated_cycle84_source": {
            "threads": 16,
            "sha256": generated_source_sha256(16),
        },
        "checks": checks,
        "remaining_import": (
            "human review of the generated Cycle84 replay source against the "
            "algorithm audit note"
        ),
        "imports_required": [
            "official ABF source gate verification",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    print("m1_cycle84_projected_replay_algorithm: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(f"circular_slice_cases={report['circular_slice']['cases_checked']}")
    print(
        "toy_models="
        + "; ".join(
            "seed={seed}, entries={entries}, duplicate_bins={duplicate_bins}, "
            "energy={energy}, max={max_multiplicity}".format(**toy)
            for toy in report["toy_models"]
        )
    )
    source = report["generated_cycle84_source"]
    print(f"generated_source=threads={source['threads']}, sha256={source['sha256']}")
    print(f"remaining_import={report['remaining_import']}")
    print("imports_required=" + "; ".join(report["imports_required"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit the Cycle84 projected-census replay algorithm."
    )
    parser.add_argument("--json", action="store_true", help="print JSON report")
    args = parser.parse_args()

    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human(report)


if __name__ == "__main__":
    main()
