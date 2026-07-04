#!/usr/bin/env python3
"""Verify exceptional_density.md.

The proof is elementary.  This script checks the exact bad-prime incidence
bound on small cyclotomic value-set cells and emits official-rate arithmetic
tables for the dyadic ranges used by the roadmap.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from itertools import combinations
from pathlib import Path
from typing import Iterable

import sympy as sp


REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "experimental" / "data" / "certificates" / "exceptional-density" / "exceptional_density.json"


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
    require(n > 0, "positive quotient order expected")
    return int(sp.totient(n))


def zpoly(exponents: Iterable[int], n: int) -> sp.Poly:
    x = sp.Symbol("x")
    return sp.Poly(sum(x ** (e % n) for e in exponents), x, domain=sp.ZZ)


def reduce_poly(poly: sp.Poly, n: int) -> sp.Poly:
    x = sp.Symbol("x")
    cyclo = sp.Poly(sp.cyclotomic_poly(n, x), x, domain=sp.ZZ)
    return sp.rem(poly, cyclo, domain=sp.ZZ)


def e1_diff(a: tuple[int, ...], b: tuple[int, ...], n: int) -> sp.Poly:
    return reduce_poly(zpoly(a, n) - zpoly(b, n), n)


def norm_abs(poly: sp.Poly, n: int) -> int:
    x = sp.Symbol("x")
    reduced = reduce_poly(poly, n)
    if reduced.is_zero:
        return 0
    cyclo = sp.Poly(sp.cyclotomic_poly(n, x), x, domain=sp.ZZ)
    return abs(int(sp.resultant(reduced.as_expr(), cyclo.as_expr(), x)))


def swap_distance(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    sa, sb = set(a), set(b)
    require(len(sa) == len(a) and len(sb) == len(b), "subsets expected")
    require(len(sa) == len(sb), "equal cardinalities expected")
    return len(sa - sb)


def floor_log_base(value: int, base: int) -> int:
    require(value >= 1, "positive value expected")
    require(base >= 2, "base at least two expected")
    power = base
    out = 0
    while power <= value:
        out += 1
        power *= base
    return out


def ceil_div(a: int, b: int) -> int:
    require(b > 0, "positive divisor expected")
    return -(-a // b)


def dyadic_prime_divisor_bound(height: int, log2_p_min: int) -> int:
    """Maximum number of distinct prime divisors >= 2^L of an integer <= height."""

    require(log2_p_min > 0, "positive dyadic floor expected")
    if height < 2**log2_p_min:
        return 0
    return (height.bit_length() - 1) // log2_p_min


def check_toy_bad_prime_incidence() -> tuple[CheckResult, list[dict]]:
    rows = []
    for n, ell, floors in [(8, 3, [2, 3, 5]), (10, 4, [2, 4, 6])]:
        subsets = list(combinations(range(n), ell))
        pair_data = []
        upstairs_duplicates = 0
        for a, b in combinations(subsets, 2):
            delta = e1_diff(a, b, n)
            norm = norm_abs(delta, n)
            if norm == 0:
                upstairs_duplicates += 1
                continue
            s = swap_distance(a, b)
            height = (2 * s) ** phi(n)
            require(norm <= height, "graded height bound failed")
            factors = sorted(sp.factorint(norm).keys())
            pair_data.append((s, norm, height, factors))

        floor_rows = []
        for log2_floor in floors:
            p_min = 2**log2_floor
            exact_incidences = sum(1 for _, _, _, factors in pair_data for p in factors if p >= p_min)
            sharp_bound = sum(floor_log_base(height, p_min) for _, _, height, _ in pair_data)
            uniform_bound = len(pair_data) * dyadic_prime_divisor_bound((2 * min(ell, n - ell)) ** phi(n), log2_floor)
            require(exact_incidences <= sharp_bound, "sharp incidence bound failed")
            require(sharp_bound <= uniform_bound, "uniform incidence bound should dominate sharp bound")
            floor_rows.append(
                {
                    "log2_p_min": log2_floor,
                    "exact_large_prime_incidences": exact_incidences,
                    "sharp_height_incidence_bound": sharp_bound,
                    "uniform_height_incidence_bound": uniform_bound,
                }
            )

        rows.append(
            {
                "quotient_order": n,
                "ell": ell,
                "subsets": len(subsets),
                "nonzero_pairs": len(pair_data),
                "upstairs_duplicate_pairs": upstairs_duplicates,
                "max_swap_distance": min(ell, n - ell),
                "floor_rows": floor_rows,
            }
        )

    return (
        CheckResult(
            "toy bad-prime incidence",
            "PASS",
            [
                "factored all nonzero e_1 pair norms for N=8, ell=3 and N=10, ell=4",
                "exact large-prime incidences are bounded by the summed height floors",
                "the uniform max-swap incidence bound dominates the sharp per-pair bound",
            ],
        ),
        rows,
    )


def official_rate_rows() -> list[dict]:
    rows = []
    rates = [(1, 2), (1, 4), (1, 8), (1, 16)]
    for n in [64, 128, 256]:
        for num, den in rates:
            if (num * n) % den != 0:
                continue
            ell = num * n // den + 1
            subsets = math.comb(n, ell)
            pair_count = math.comb(subsets, 2)
            s_max = min(ell, n - ell)
            height = (2 * s_max) ** phi(n)
            for log2_floor in [192, 250, 256]:
                per_pair = dyadic_prime_divisor_bound(height, log2_floor)
                half_collision_prime_bound = 0 if pair_count == 0 else ceil_div(pair_count * per_pair, ceil_div(pair_count, 2))
                tenth_collision_prime_bound = 0 if pair_count == 0 else ceil_div(pair_count * per_pair, ceil_div(pair_count, 10))
                rows.append(
                    {
                        "quotient_order": n,
                        "rate": f"{num}/{den}",
                        "ell": ell,
                        "subsets_log2_floor": subsets.bit_length() - 1,
                        "pair_count_log2_floor": pair_count.bit_length() - 1,
                        "max_swap_distance": s_max,
                        "phi": phi(n),
                        "height_log2_floor": height.bit_length() - 1,
                        "log2_p_min": log2_floor,
                        "large_prime_divisors_per_pair_bound": per_pair,
                        "primes_colliding_at_least_half_pairs_bound": half_collision_prime_bound,
                        "primes_colliding_at_least_tenth_pairs_bound": tenth_collision_prime_bound,
                    }
                )
    return rows


def check_official_rows(rows: list[dict]) -> CheckResult:
    lookup = {
        (row["quotient_order"], row["rate"], row["log2_p_min"]): row
        for row in rows
    }
    require(
        lookup[(64, "1/2", 250)]["large_prime_divisors_per_pair_bound"] == 0,
        "N=64, rate 1/2 should be locally height-certified at L=250",
    )
    require(
        lookup[(128, "1/2", 250)]["large_prime_divisors_per_pair_bound"] == 1,
        "N=128, rate 1/2 should have at most one large bad prime per pair at L=250",
    )
    require(
        lookup[(128, "1/2", 250)]["primes_colliding_at_least_half_pairs_bound"] == 2,
        "R=1 should imply at most two half-mass bad primes",
    )
    require(
        lookup[(256, "1/2", 250)]["large_prime_divisors_per_pair_bound"] >= 3,
        "N=256 should be beyond the one-prime-per-pair range at L=250",
    )
    return CheckResult(
        "official-rate dyadic incidence table",
        "PASS",
        [
            "computed max-swap height floors for N=64,128,256 and all four official rates",
            "N=64, L=250 gives zero large bad primes per pair by height",
            "N=128, rate 1/2, L=250 gives R=1 and at most two half-mass bad primes",
            "N=256 already has several possible large bad primes per pair by pure height",
        ],
    )


def build_result() -> dict:
    toy_check, toy_rows = check_toy_bad_prime_incidence()
    official_rows = official_rate_rows()
    official_check = check_official_rows(official_rows)
    script = Path(__file__).resolve()
    source = script_source(script)
    return {
        "status": "PROVED_EXCEPTIONAL_DENSITY_BOUND",
        "dag_nodes": ["are_exceptional_density"],
        "depends_on": ["graded_collision_radius"],
        "object": "quotient e_1 value-set certification",
        "theorem": "bad-prime collision incidences are bounded by summed norm-height logarithms; large-collision primes are sparse by Markov",
        "script": script_ref(script),
        "script_sha256": sha256_text(source),
        "checks": [asdict(toy_check), asdict(official_check)],
        "toy_exact_rows": toy_rows,
        "official_rate_dyadic_rows": official_rows,
        "non_claims": [
            "does not certify the official prime is outside the exceptional set",
            "does not prove characteristic-zero injectivity of e_1 on a quotient cell",
            "does not prove a row-specific value-set lower bound",
            "does not close the generator-economy design problem",
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
