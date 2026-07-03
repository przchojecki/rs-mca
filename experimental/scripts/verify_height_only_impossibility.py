#!/usr/bin/env python3
"""Verify the arithmetic in height_only_impossibility.md."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import sympy as sp


REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "experimental" / "data" / "certificates" / "height-only-impossibility" / "height_only_impossibility.json"
RATES = [(1, 2), (1, 4), (1, 8), (1, 16)]


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    details: list[str]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def phi(n: int) -> int:
    return int(sp.totient(n))


def cell_ell(n: int, rate_num: int, rate_den: int) -> int:
    require((rate_num * n) % rate_den == 0, "rate*N must be integral")
    return rate_num * n // rate_den + 1


def s_max(n: int, ell: int) -> int:
    require(0 <= ell <= n, "ell must lie in [0,N]")
    return min(ell, n - ell)


def height_bound(n: int, s: int) -> int:
    require(s >= 0, "nonnegative swap distance expected")
    return (2 * s) ** phi(n)


def certified_radius(n: int, log2_p_ceiling: int) -> int:
    """Largest s whose height bound is below the bit ceiling.

    We use the sufficient universal comparison `(2s)^phi(N) < 2^L`.
    If this fails for `s`, no prime `p < 2^L` can pass the pure height gate
    for that swap distance.  If it succeeds, a concrete row still needs
    `p > (2s)^phi(N)`.
    """

    target = 2**log2_p_ceiling
    hi = 1
    while height_bound(n, hi) < target:
        hi *= 2
    lo = hi // 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if height_bound(n, mid) < target:
            lo = mid
        else:
            hi = mid
    return lo


def witness_pair(n: int, ell: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    base = tuple(range(ell))
    sm = s_max(n, ell)
    overlap = ell - sm
    other = tuple(list(range(overlap)) + list(range(ell, ell + sm)))
    require(len(base) == len(other) == ell, "bad witness sizes")
    require(len(set(base)) == ell and len(set(other)) == ell, "witness sets not distinct")
    require(len(set(base) - set(other)) == sm, "witness does not attain s_max")
    return base, other


def check_diameter_witnesses() -> CheckResult:
    checked = 0
    for n in [16, 32, 64, 128]:
        for num, den in RATES:
            ell = cell_ell(n, num, den)
            a, b = witness_pair(n, ell)
            require(len(set(a) - set(b)) == s_max(n, ell), "diameter witness failed")
            checked += 1
    return CheckResult(
        "full-cell diameter witnesses",
        "PASS",
        [f"constructed max-swap witness pairs for {checked} official-rate toy cells"],
    )


def check_prize_frontier() -> tuple[CheckResult, list[dict[str, int | str | bool]]]:
    rows: list[dict[str, int | str | bool]] = []
    for n in [64, 128, 256, 512]:
        ph = phi(n)
        d256 = certified_radius(n, 256)
        for num, den in RATES:
            ell = cell_ell(n, num, den)
            sm = s_max(n, ell)
            bound = height_bound(n, sm)
            rows.append(
                {
                    "quotient_order": n,
                    "phi": ph,
                    "rate": f"{num}/{den}",
                    "ell": ell,
                    "s_max": sm,
                    "certified_radius_under_2_256": d256,
                    "full_cell_height_bound_below_2_256": bound < 2**256,
                    "height_bound_bit_length": bound.bit_length(),
                    "height_bound_log2_floor": bound.bit_length() - 1,
                }
            )
    n64 = [r for r in rows if r["quotient_order"] == 64]
    n128 = [r for r in rows if r["quotient_order"] == 128]
    require(all(r["full_cell_height_bound_below_2_256"] for r in n64), "N=64 should sit below the 2^256 ceiling")
    require(not any(r["full_cell_height_bound_below_2_256"] for r in n128), "N=128 should exceed the 2^256 ceiling for all rates")
    require(all(r["s_max"] > r["certified_radius_under_2_256"] for r in n128), "N=128 diameter should exceed d_*")
    return (
        CheckResult(
            "prize-range height-only frontier",
            "PASS",
            [
                "N=64 official-rate full-cell height bounds are below the 2^256 ceiling",
                "N=128 official-rate full-cell height bounds all exceed the 2^256 ceiling",
                "the obstruction strengthens for N=256 and N=512",
            ],
        ),
        rows,
    )


def check_monotonic_scoping() -> CheckResult:
    details = []
    previous_d = None
    for n in [64, 128, 256, 512]:
        d = certified_radius(n, 256)
        if previous_d is not None:
            require(d <= previous_d, "certified radius should not increase across doubled 2-power orders")
        details.append(f"N={n}: phi={phi(n)}, d_*(N,256)={d}")
        previous_d = d
    return CheckResult("2-power certified radius monotonicity", "PASS", details)


def build_result() -> dict:
    diameter_check = check_diameter_witnesses()
    frontier_check, frontier_rows = check_prize_frontier()
    monotone_check = check_monotonic_scoping()
    script = Path(__file__).resolve()
    return {
        "status": "PROVED_HEIGHT_ONLY_IMPOSSIBILITY",
        "dag_nodes": ["height_only_impossibility"],
        "depends_on": ["graded_collision_radius"],
        "object": "quotient e_1 value-set certification",
        "script": str(script.relative_to(REPO)),
        "script_sha256": file_sha256(script),
        "checks": [asdict(c) for c in [diameter_check, frontier_check, monotone_check]],
        "frontier_rows": frontier_rows,
        "non_claims": [
            "does not assert collisions exist beyond the height-only radius",
            "does not rule out exact p-specific norm checks or factorization certificates",
            "does not close the zone-b value-set lower bound",
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
        expected = json.loads(Path(args.check).read_text())
        require(expected == result, "certificate does not match verifier output; rerun with --emit")
        print(result["status"])
        for check in result["checks"]:
            print(f"  {check['name']}: {check['status']}")


if __name__ == "__main__":
    main()
