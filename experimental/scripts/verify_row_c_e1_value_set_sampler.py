#!/usr/bin/env python3
"""E1 / Q3.1 Row-C slack-one quotient value-set sampler.

This is an evidence-gathering harness, not a theorem prover.  It samples the
characteristic-zero antipodal classes counted by A(N', ell') in Paper B's
quotient-exact floor, reduces their e_1 values modulo the Row-C prime
p ~= 2^250, and records collision statistics.

Run:
  python3 experimental/scripts/verify_row_c_e1_value_set_sampler.py
  python3 experimental/scripts/verify_row_c_e1_value_set_sampler.py --emit
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from collections import Counter
from math import comb
from pathlib import Path

import sympy


ROW_N = 2 ** 10
RHO_NUM, RHO_DEN = 1, 2
REQUESTED_QUOTIENT_ORDERS = [64, 96, 128, 192, 256]
DEFAULT_COMPATIBLE_ORDERS = [64, 128, 256]
DEFAULT_SAMPLES = 262_144
DEFAULT_SEED = 2026070201
OUTPUT = Path(
    "experimental/data/certificates/row-c-e1-sampling/"
    "row_c_e1_sampling_pilot.json"
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def row_c_prime() -> int:
    """Smallest prime p > 2^250 with p = 1 mod 1024."""
    modulus = ROW_N
    p = (1 << 250) + ((1 - (1 << 250)) % modulus)
    while not sympy.isprime(p):
        p += modulus
    return p


def subgroup_generator(p: int, order: int) -> int:
    """Return an element of exact order ``order`` in F_p^*."""
    assert (p - 1) % order == 0
    exponent = (p - 1) // order
    for a in range(2, 10_000):
        g = pow(a, exponent, p)
        if g != 1 and pow(g, order, p) == 1 and pow(g, order // 2, p) != 1:
            return g
    raise RuntimeError(f"no generator found for order {order}")


def antipodal_representatives(p: int, order: int) -> list[int]:
    """One representative from each pair {x, -x} in the order-N subgroup."""
    g = subgroup_generator(p, order)
    q = [pow(g, i, p) for i in range(order)]
    seen = set()
    reps = []
    for x in q:
        if x in seen:
            continue
        y = (-x) % p
        seen.add(x)
        seen.add(y)
        reps.append(min(x, y))
    assert len(reps) == order // 2
    return reps


def feasible_t_values(order: int, ell: int) -> list[tuple[int, int]]:
    """Return (t, class_count_t), where t is the number of singleton pairs."""
    n1 = order // 2
    out = []
    for t in range(0, min(ell, order - ell) + 1):
        if (ell - t) % 2 == 0:
            out.append((t, comb(n1, t) * (2 ** t)))
    return out


def plateau_count(order: int, ell: int) -> int:
    return sum(count for _, count in feasible_t_values(order, ell))


def sample_t(rng: random.Random, weighted_t: list[tuple[int, int]], total: int) -> int:
    r = rng.randrange(total)
    acc = 0
    for t, count in weighted_t:
        acc += count
        if r < acc:
            return t
    raise AssertionError("unreachable weighted sample")


def sample_value(reps: list[int], weighted_t: list[tuple[int, int]], total: int,
                 p: int, rng: random.Random) -> int:
    """Sample one characteristic-zero class uniformly and return e_1 mod p."""
    t = sample_t(rng, weighted_t, total)
    if t == 0:
        return 0
    indices = rng.sample(range(len(reps)), t)
    value = 0
    for idx in indices:
        x = reps[idx]
        value += x if rng.getrandbits(1) else -x
    return value % p


def collision_lower_bound(samples: int, alpha: float = 0.05) -> float:
    """95% lower bound on effective support when zero collisions are observed."""
    pairs = samples * (samples - 1) / 2
    return pairs / (-math.log(alpha))


def run_cell(order: int, samples: int, seed: int, p: int) -> dict:
    ell_num = RHO_NUM * order
    assert ell_num % RHO_DEN == 0
    ell = ell_num // RHO_DEN + 1
    reps = antipodal_representatives(p, order)
    weighted_t = feasible_t_values(order, ell)
    total = sum(count for _, count in weighted_t)
    rng = random.Random(seed + order * 1_000_003 + samples)
    counts = Counter(sample_value(reps, weighted_t, total, p, rng)
                     for _ in range(samples))
    duplicate_pairs = sum(c * (c - 1) // 2 for c in counts.values())
    sample_pairs = samples * (samples - 1) // 2
    lower = collision_lower_bound(samples) if duplicate_pairs == 0 else None
    interpretation = (
        "collision_hit_inspect_structure"
        if duplicate_pairs
        else "no_collision_pilot_rules_out_only_extreme_collapse"
    )
    return {
        "N_prime": order,
        "ell_prime": ell,
        "samples": samples,
        "seed": seed + order * 1_000_003 + samples,
        "plateau_count": total,
        "log2_plateau_count": math.log2(total),
        "unique_sample_values": len(counts),
        "duplicate_pairs": duplicate_pairs,
        "sample_pairs": sample_pairs,
        "empirical_pair_collision_rate": duplicate_pairs / sample_pairs,
        "zero_collision_95pct_effective_support_lower_bound": lower,
        "log2_zero_collision_95pct_lower_bound": (
            math.log2(lower) if lower is not None else None
        ),
        "interpretation": interpretation,
        "top_multiplicities": sorted(counts.values(), reverse=True)[:5],
    }


def build_report(samples: int, seed: int, orders: list[int]) -> dict:
    p = row_c_prime()
    incompatible = []
    for order in REQUESTED_QUOTIENT_ORDERS:
        if ROW_N % order != 0:
            incompatible.append({
                "N_prime": order,
                "reason": "not a divisor of Row-C n=2^10; needs a different row slate",
            })
    cells = [run_cell(order, samples, seed, p) for order in orders]
    source = Path(__file__).read_text()
    return {
        "schema": "row_c_e1_value_set_sampling_v1",
        "status": "EXPERIMENTAL_EVIDENCE",
        "dag_node": "e1_fullness",
        "evidence_task": "E1 / Q3.1 Row-C zone-(b) sampling",
        "object": (
            "uniform samples from characteristic-zero antipodal classes counted "
            "by A(N', ell'), reduced via e_1 modulo the Row-C prime"
        ),
        "row": {
            "name": "Row C small-n probe",
            "n": ROW_N,
            "rho": f"{RHO_NUM}/{RHO_DEN}",
            "p": p,
            "log2_p": math.log2(p),
            "p_mod_n": p % ROW_N,
        },
        "requested_quotient_orders": REQUESTED_QUOTIENT_ORDERS,
        "sampled_quotient_orders": orders,
        "incompatible_requested_orders": incompatible,
        "pre_registered_interpretation": {
            "density_to_one": (
                "e1_fullness prior up; corridor lands near quotient crossing"
            ),
            "heavy_collisions": (
                "averaged_slope_conversion becomes load-bearing; inspect "
                "collision structure"
            ),
            "mixed_by_N_prime": (
                "zone charts gain interval structure with per-N' gates"
            ),
        },
        "pilot_limitations": [
            "The committed run is a deterministic pilot, not the full sqrt(V) run.",
            "Zero collisions give only an effective-support lower bound.",
            "Sampling is over antipodal classes, not raw subsets, to target the "
            "Paper B quotient-exact value set directly.",
        ],
        "cells": cells,
        "script_sha256": sha256_text(source),
    }


def verify_report(report: dict) -> tuple[bool, list[str]]:
    ok = True
    details = []
    row = report["row"]
    ok &= row["p_mod_n"] == 1
    ok &= sympy.isprime(row["p"])
    details.append(
        f"Row-C prime: p = 1 mod {ROW_N}, log2 p = {row['log2_p']:.3f}"
    )
    for skipped in report["incompatible_requested_orders"]:
        ok &= ROW_N % skipped["N_prime"] != 0
    details.append(
        "requested non-dyadic cells skipped: "
        + ", ".join(str(x["N_prime"]) for x in report["incompatible_requested_orders"])
    )
    for cell in report["cells"]:
        order = cell["N_prime"]
        ell = cell["ell_prime"]
        expected = plateau_count(order, ell)
        cell_ok = (
            ROW_N % order == 0
            and expected == cell["plateau_count"]
            and cell["unique_sample_values"] + cell["duplicate_pairs"] >= cell["samples"]
        )
        ok &= cell_ok
        lower = cell["log2_zero_collision_95pct_lower_bound"]
        lower_text = f"{lower:.2f}" if lower is not None else "n/a"
        details.append(
            "N'={order:3d}, ell'={ell:3d}: samples={samples}, "
            "duplicates={dup}, log2 A={loga:.2f}, zero-collision lower log2={lower}"
            .format(
                order=order,
                ell=ell,
                samples=cell["samples"],
                dup=cell["duplicate_pairs"],
                loga=cell["log2_plateau_count"],
                lower=lower_text,
            )
        )
    return ok, details


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=DEFAULT_SAMPLES)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--orders", type=int, nargs="+", default=DEFAULT_COMPATIBLE_ORDERS)
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()

    report = build_report(args.samples, args.seed, args.orders)
    ok, details = verify_report(report)
    print("=" * 74)
    print("E1 / Q3.1 Row-C e1 value-set sampling pilot")
    print("=" * 74)
    print(f"[{'PASS' if ok else 'FAIL'}] deterministic pilot")
    for line in details:
        print(f"        {line}")
    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(f"\nwrote {OUTPUT}")
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
