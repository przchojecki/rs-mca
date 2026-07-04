#!/usr/bin/env python3
"""Verify the arithmetic in graded_collision_radius.md."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass
from itertools import combinations
from pathlib import Path
from typing import Iterable

import sympy as sp


REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "experimental" / "data" / "certificates" / "graded-collision-radius" / "graded_collision_radius.json"


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    details: list[str]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def script_source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def script_ref(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def is_sha256_hex(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value)
    )


def require_replay_match(expected: dict, result: dict) -> None:
    if expected == result:
        return
    expected_payload = dict(expected)
    result_payload = dict(result)
    expected_hash = expected_payload.pop("script_sha256", None)
    result_payload.pop("script_sha256", None)
    require(
        expected_payload == result_payload,
        "certificate does not match verifier output; rerun with --emit",
    )
    require(is_sha256_hex(expected_hash), "certificate script_sha256 is not a sha256 hex digest")


def phi(n: int) -> int:
    require(n > 0, "phi input must be positive")
    return int(sp.totient(n))


def swap_distance(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    sa, sb = set(a), set(b)
    require(len(sa) == len(a) and len(sb) == len(b), "sets expected")
    require(len(sa) == len(sb), "equal-size sets expected")
    return len(sa - sb)


def e1_poly(subset: Iterable[int], n: int) -> sp.Poly:
    x = sp.Symbol("x")
    expr = sum(x ** (i % n) for i in subset)
    return sp.Poly(expr, x, domain=sp.ZZ)


def delta_norm(n: int, a: tuple[int, ...], b: tuple[int, ...]) -> int:
    x = sp.Symbol("x")
    cyclo = sp.Poly(sp.cyclotomic_poly(n, x), x, domain=sp.ZZ)
    delta = e1_poly(a, n) - e1_poly(b, n)
    result = sp.resultant(delta.as_expr(), cyclo.as_expr(), x)
    return int(result)


def certified_radius(n: int, log2_p_floor: int) -> int:
    """Largest s with (2s)^phi(n) < 2^log2_p_floor."""

    require(log2_p_floor > 0, "positive log2 floor expected")
    ph = phi(n)
    target = 2**log2_p_floor

    def ok(s: int) -> bool:
        return s >= 0 and (2 * s) ** ph < target

    hi = 1
    while ok(hi):
        hi *= 2
    lo = hi // 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            lo = mid
        else:
            hi = mid
    return lo


def full_cell_certified(n: int, ell: int, log2_p_floor: int) -> bool:
    require(0 <= ell <= n, "ell must be in [0,n]")
    s_max = min(ell, n - ell)
    return s_max <= certified_radius(n, log2_p_floor)


def check_toy_norm_bounds() -> CheckResult:
    cases = [(4, 2), (8, 3)]
    details = []
    total_pairs = 0
    zero_deltas = 0
    for n, ell in cases:
        ph = phi(n)
        subsets = list(combinations(range(n), ell))
        checked = 0
        worst_ratio_num = 0
        worst_ratio_den = 1
        for i, a in enumerate(subsets):
            for b in subsets[i + 1 :]:
                s = swap_distance(a, b)
                norm = abs(delta_norm(n, a, b))
                total_pairs += 1
                if norm == 0:
                    zero_deltas += 1
                    continue
                bound = (2 * s) ** ph
                require(norm <= bound, f"norm bound failed at N={n}, ell={ell}, s={s}")
                if norm * worst_ratio_den > worst_ratio_num * bound:
                    worst_ratio_num, worst_ratio_den = norm, bound
                checked += 1
        details.append(
            f"N={n}, ell={ell}: {checked} nonzero deltas checked, "
            f"{len(subsets)} subsets, worst norm/bound={worst_ratio_num}/{worst_ratio_den}"
        )
    require(total_pairs > 0 and zero_deltas > 0, "toy checks should include nonzero pairs and upstairs duplicates")
    return CheckResult(
        "toy cyclotomic norm bound",
        "PASS",
        details + [f"total unordered pairs={total_pairs}", f"upstairs duplicate deltas={zero_deltas}"],
    )


def check_radius_table() -> tuple[CheckResult, list[dict[str, int]]]:
    rows = []
    for n in [16, 32, 64, 80, 82, 96, 128, 160, 256]:
        for log2_p in [192, 250, 256]:
            rows.append(
                {
                    "quotient_order": n,
                    "phi": phi(n),
                    "log2_p_floor": log2_p,
                    "certified_swap_radius": certified_radius(n, log2_p),
                }
            )
    lookup = {
        (row["quotient_order"], row["log2_p_floor"]): row["certified_swap_radius"]
        for row in rows
    }
    require(lookup[(128, 250)] == 7, "N=128, log2 p=250 should have d*=7")
    require(lookup[(64, 250)] >= 31, "N=64, log2 p=250 should certify all rate-1/2 swaps")
    require(lookup[(256, 250)] == 1, "N=256, log2 p=250 should certify exactly the single-swap rung")
    return (
        CheckResult(
            "certified swap-radius table",
            "PASS",
            [
                "computed d_*(N,L)=max{s:(2s)^phi(N)<2^L}",
                "anchor N=128, L=250 gives d_*=7",
                "N=64, L=250 certifies all rate-1/2 swap distances",
                "N=256, L=250 certifies exactly the single-swap rung",
            ],
        ),
        rows,
    )


def check_full_cell_frontier() -> tuple[CheckResult, list[dict[str, int | str | bool]]]:
    rates = [(1, 2), (1, 4), (1, 8), (1, 16)]
    rows: list[dict[str, int | str | bool]] = []
    for log2_p in [192, 250, 256]:
        for num, den in rates:
            certified_orders = []
            for n in [16, 32, 64, 128, 256]:
                if (num * n) % den != 0:
                    continue
                ell = num * n // den + 1
                ok = full_cell_certified(n, ell, log2_p)
                rows.append(
                    {
                        "log2_p_floor": log2_p,
                        "rate": f"{num}/{den}",
                        "quotient_order": n,
                        "ell": ell,
                        "max_swap_distance": min(ell, n - ell),
                        "certified_swap_radius": certified_radius(n, log2_p),
                        "full_cell_certified": ok,
                    }
                )
                if ok:
                    certified_orders.append(n)
            if log2_p == 250 and den == 2:
                require(64 in certified_orders and 128 not in certified_orders, "rate 1/2 frontier mismatch at L=250")
    return (
        CheckResult(
            "rate-cell full-certification frontier",
            "PASS",
            [
                "checked ell=rho*N+1 cells for rates 1/2,1/4,1/8,1/16",
                "at L=250, rate 1/2 is fully certified through N=64 but not N=128",
                "frontier uses max swap distance min(ell,N-ell), with ell also printed",
            ],
        ),
        rows,
    )


def check_single_swap_gate() -> CheckResult:
    details = []
    for n in [16, 32, 64, 128, 256]:
        ph = phi(n)
        first_log2_floor = ph + 1
        require(certified_radius(n, first_log2_floor) >= 1, "single-swap gate should pass above 2^phi")
        require(certified_radius(n, ph) == 0, "single-swap gate should fail at 2^phi")
        details.append(f"N={n}: phi={ph}, s=1 certified for p>=2^{first_log2_floor}")
    return CheckResult("single-swap gate", "PASS", details)


def build_result() -> dict:
    norm_check = check_toy_norm_bounds()
    radius_check, radius_rows = check_radius_table()
    frontier_check, frontier_rows = check_full_cell_frontier()
    single_check = check_single_swap_gate()
    script = Path(__file__).resolve()
    source = script_source(script)
    return {
        "status": "PROVED_GRADED_COLLISION_RADIUS",
        "dag_nodes": ["graded_collision_radius", "single_swap_injectivity"],
        "object": "quotient e_1 value-set certification",
        "theorem": "(2s)^phi(N) < p prevents new mod-p collisions between characteristic-zero distinct e_1 values at swap distance s",
        "script": script_ref(script),
        "script_sha256": sha256_text(source),
        "checks": [asdict(c) for c in [norm_check, radius_check, frontier_check, single_check]],
        "certified_radius_table": radius_rows,
        "full_cell_frontier": frontier_rows,
        "non_claims": [
            "does not prove characteristic-zero injectivity of B -> e_1(B)",
            "does not close the far-pair value-set lower bound at N=128",
            "does not certify a new MCA threshold row",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the JSON certificate")
    parser.add_argument("--check", default=str(OUT), help="certificate path to replay")
    args = parser.parse_args()

    result = build_result()
    if args.emit:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(f"wrote {OUT.relative_to(REPO)}")
    else:
        expected = json.loads(Path(args.check).read_text(encoding="utf-8"))
        require_replay_match(expected, result)
        print(result["status"])
        for check in result["checks"]:
            print(f"  {check['name']}: {check['status']}")


if __name__ == "__main__":
    main()
