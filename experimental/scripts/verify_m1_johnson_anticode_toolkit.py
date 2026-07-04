#!/usr/bin/env python3
"""Verify m1_johnson_anticode_toolkit.md."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from itertools import combinations
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
OUT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "m1-johnson-anticode-toolkit"
    / "m1_johnson_anticode_toolkit_certificate.json"
)


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


def exchange_distance(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return len(set(a) - set(b))


def johnson_vertices(n: int, j: int) -> list[tuple[int, ...]]:
    return list(combinations(range(n), j))


def anticode_bound_exact(n: int, j: int, s: int) -> tuple[int, int]:
    require(0 <= s <= j <= n, "expected 0 <= s <= j <= n")
    return math.comb(n, j - s), math.comb(j, s)


def density_denominator(n: int, j: int, s: int) -> int:
    return math.comb(n - j + s, s)


def max_clique_size_bitsets(adj: list[int]) -> int:
    """Maximum clique size in a small graph represented by bit adjacency."""

    best = 0

    def expand(size: int, candidates: int) -> None:
        nonlocal best
        if not candidates:
            best = max(best, size)
            return
        if size + candidates.bit_count() <= best:
            return
        while candidates:
            if size + candidates.bit_count() <= best:
                return
            v_bit = candidates & -candidates
            v = v_bit.bit_length() - 1
            candidates ^= v_bit
            expand(size + 1, candidates & adj[v])

    expand(0, (1 << len(adj)) - 1)
    return best


def exact_max_separated(n: int, j: int, s: int) -> int:
    vertices = johnson_vertices(n, j)
    adj = [0] * len(vertices)
    for a_idx, a in enumerate(vertices):
        for b_idx in range(a_idx + 1, len(vertices)):
            b = vertices[b_idx]
            if exchange_distance(a, b) > s:
                adj[a_idx] |= 1 << b_idx
                adj[b_idx] |= 1 << a_idx
    return max_clique_size_bitsets(adj)


def check_core_disjointness() -> tuple[CheckResult, list[dict]]:
    rows = []
    cases = [(6, 3, 1), (7, 3, 1), (8, 4, 2)]
    for n, j, s in cases:
        vertices = johnson_vertices(n, j)
        exact = exact_max_separated(n, j, s)
        numerator, denominator = anticode_bound_exact(n, j, s)
        bound = numerator // denominator
        require(exact <= bound, "exact separated family exceeds anticode bound")

        family: list[tuple[int, ...]] = []
        used_cores: set[tuple[int, ...]] = set()
        for vertex in vertices:
            cores = set(combinations(vertex, j - s))
            if used_cores.isdisjoint(cores):
                family.append(vertex)
                used_cores.update(cores)
        for a, b in combinations(family, 2):
            require(exchange_distance(a, b) > s, "greedy family is not separated")
        require(len(used_cores) == len(family) * math.comb(j, s), "core count mismatch")
        require(len(used_cores) <= math.comb(n, j - s), "too many cores used")

        rows.append(
            {
                "n": n,
                "j": j,
                "s": s,
                "vertices": len(vertices),
                "exact_max_separated": exact,
                "anticode_bound_floor": bound,
                "packing_numerator_binom_n_j_minus_s": numerator,
                "packing_denominator_binom_j_s": denominator,
                "greedy_family_size": len(family),
            }
        )

    return (
        CheckResult(
            "core-disjoint anticode packing",
            "PASS",
            [
                "exact maximum separated families checked for three small Johnson graphs",
                "greedy separated families use disjoint (j-s)-cores exactly as in the proof",
                "packing bound equals floor(binomial(n,j-s)/binomial(j,s))",
            ],
        ),
        rows,
    )


def check_density_identity() -> tuple[CheckResult, list[dict]]:
    rows = []
    for n, j, s in [(16, 8, 1), (16, 8, 2), (32, 16, 3), (64, 33, 4)]:
        numerator, denominator = anticode_bound_exact(n, j, s)
        total = math.comb(n, j)
        density_denom = density_denominator(n, j, s)
        require(numerator * density_denom == total * denominator, "density identity failed")
        rows.append(
            {
                "n": n,
                "j": j,
                "s": s,
                "all_j_sets_log2_floor": total.bit_length() - 1,
                "separated_bound_log2_floor": (numerator // denominator).bit_length() - 1,
                "separated_bound_floor": numerator // denominator,
                "density_denominator": density_denom,
            }
        )
    return (
        CheckResult(
            "density-loss identity",
            "PASS",
            [
                "verified binom(n,j)/binom(n-j+s,s) = binom(n,j-s)/binom(j,s)",
                "tables print the support-space saving available from pure anticode packing",
            ],
        ),
        rows,
    )


def check_mixing_scope() -> tuple[CheckResult, list[dict]]:
    rows = []
    rates = [(1, 2), (1, 4), (1, 8), (1, 16)]
    for n in [64, 128, 512, 4096]:
        for num, den in rates:
            if (num * n) % den != 0:
                continue
            j = num * n // den
            gap_num = n
            gap_den = j * (n - j)
            steps_for_128_bits = math.ceil(128 * math.log(2) * gap_den / gap_num)
            rows.append(
                {
                    "n": n,
                    "rate": f"{num}/{den}",
                    "j": j,
                    "one_step_gap_numerator": gap_num,
                    "one_step_gap_denominator": gap_den,
                    "one_step_gap_log2_floor_negative": (gap_den // gap_num).bit_length() - 1,
                    "steps_for_exp_bound_2^-128": steps_for_128_bits,
                }
            )
    require(
        next(row for row in rows if row["n"] == 512 and row["rate"] == "1/2")["steps_for_exp_bound_2^-128"] > 10000,
        "n=512, rate 1/2 should already need more than ten thousand exchange steps for 128-bit decay",
    )
    return (
        CheckResult(
            "Johnson one-step mixing scope",
            "PASS",
            [
                "computed gap=n/(j(n-j)) for official rates",
                "single-step endpoint factor is 1-O(1/n) at fixed rate",
                "128-bit decay needs more than ten thousand exchange steps even at n=512",
            ],
        ),
        rows,
    )


def build_result() -> dict:
    packing_check, packing_rows = check_core_disjointness()
    density_check, density_rows = check_density_identity()
    mixing_check, mixing_rows = check_mixing_scope()
    script = Path(__file__).resolve()
    source = script_source(script)
    return {
        "status": "PROVED_JOHNSON_ANTICODE_TOOLKIT",
        "dag_nodes": ["xr_anticode_toolkit"],
        "object": "Johnson locator graph support combinatorics for XR",
        "script": script_ref(script),
        "script_sha256": sha256_text(source),
        "checks": [asdict(packing_check), asdict(density_check), asdict(mixing_check)],
        "exact_small_packing_rows": packing_rows,
        "density_identity_rows": density_rows,
        "mixing_scope_rows": mixing_rows,
        "non_claims": [
            "does not prove an XR inverse theorem",
            "does not prove a finite-field q-scale value-set lower bound",
            "does not prove an M1 safe-side threshold",
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
