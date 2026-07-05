#!/usr/bin/env python3
"""Replay master-flatness split-locator incidence certificates.

Status: AUDIT.  The verifier is stdlib-only: it reconstructs the multiplicative
domain, recomputes signed elementary-symmetric coefficients, checks split
locator divisibility by subset-root membership, re-tags periodicity scale, and
recounts every full-enumeration row exactly.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from math import comb
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "master-flatness-incidence-v1"
THEOREM_PROBLEM_ID = "Conjecture-F-master-flatness"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value in {2, 3}:
        return True
    if value % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def prime_factors(value: int) -> list[int]:
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1 if divisor == 2 else 2
    if value > 1:
        factors.append(value)
    return factors


def primitive_root(p: int) -> int:
    require(is_prime(p), "p must be prime")
    factors = prime_factors(p - 1)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // factor, p) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root found for p={p}")


def subgroup_domain(p: int, n: int) -> list[int]:
    require((p - 1) % n == 0, "n must divide p-1")
    step = pow(primitive_root(p), (p - 1) // n, p)
    out: list[int] = []
    x = 1
    for _ in range(n):
        out.append(x)
        x = (x * step) % p
    require(x == 1 and len(set(out)) == n, "bad domain generator")
    return out


def divisors(value: int) -> list[int]:
    return [d for d in range(1, value + 1) if value % d == 0]


def signed_elementary(values: Iterable[int], j: int, p: int) -> tuple[int, ...]:
    elementary = [0] * (j + 1)
    elementary[0] = 1
    used = 0
    for value in values:
        used += 1
        for degree in range(min(used, j), 0, -1):
            elementary[degree] = (elementary[degree] + elementary[degree - 1] * value) % p
    require(used == j, "subset size mismatch")
    return tuple(((-1 if degree % 2 else 1) * elementary[degree]) % p for degree in range(1, j + 1))


def locator_coefficients(values: Iterable[int], p: int) -> tuple[int, ...]:
    roots = list(values)
    signed = signed_elementary(roots, len(roots), p)
    return tuple(reversed(signed)) + (1,)


def poly_eval(coeffs: tuple[int, ...], x: int, p: int) -> int:
    acc = 0
    for coeff in reversed(coeffs):
        acc = (acc * x + coeff) % p
    return acc


def periodicity_scale(indices: Iterable[int], n: int) -> int:
    support = set(indices)
    best = 1
    for scale in divisors(n):
        step = n // scale
        ok = True
        for index in support:
            for offset in range(scale):
                if (index + offset * step) % n not in support:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            best = max(best, scale)
    return best


def flat_accepts(coeffs: tuple[int, ...], flat: dict[str, Any], p: int) -> bool:
    if flat["kind"] == "prefix_affine":
        target = tuple(int(x) % p for x in flat["target"])
        return coeffs[: len(target)] == target
    if flat["kind"] == "linear":
        matrix = flat["matrix"]
        rhs = flat["rhs"]
        for row, value in zip(matrix, rhs, strict=True):
            if sum((int(a) % p) * c for a, c in zip(row, coeffs, strict=True)) % p != int(value) % p:
                return False
        return True
    raise ValueError(f"unknown flat kind {flat['kind']!r}")


def density_floor(total: int, p: int, codim: int) -> int:
    return total // (p ** codim)


def sha256_payload(payload: dict[str, Any]) -> str:
    clean = json.loads(json.dumps(payload, sort_keys=True))
    clean.pop("payload_sha256", None)
    blob = json.dumps(clean, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def check_witnesses(payload: dict[str, Any], p: int, n: int, j: int, flat: dict[str, Any]) -> None:
    domain = subgroup_domain(p, n)
    domain_set = set(domain)
    for witness in payload.get("argmax_witnesses", []):
        indices = tuple(int(i) for i in witness["indices"])
        require(len(indices) == j and len(set(indices)) == j, "bad witness subset size")
        roots = [domain[index] for index in indices]
        require(roots == witness["roots"], "witness roots mismatch")
        coeffs = signed_elementary(roots, j, p)
        require(list(coeffs) == witness["signed_coefficients"], "signed coefficients mismatch")
        locator = locator_coefficients(roots, p)
        require(list(locator) == witness["locator_coefficients_low_to_high"], "locator coefficients mismatch")
        require(all(poly_eval(locator, root, p) == 0 for root in roots), "locator misses a recorded root")
        require(all(root in domain_set for root in roots), "root not in domain")
        require(periodicity_scale(indices, n) == int(witness["scale"]), "periodicity scale mismatch")
        require(flat_accepts(coeffs, flat, p), "witness does not satisfy flat")
        require(bool(witness["flat_accepts"]), "recorded flat_accepts is false")


def recount_prefix(payload: dict[str, Any]) -> None:
    params = payload["parameters"]
    p = int(params["p"])
    n = int(params["n"])
    j = int(params["j"])
    codim = int(params["codim"])
    domain = subgroup_domain(p, n)
    buckets: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    scale_counter: Counter[int] = Counter()
    for indices in itertools.combinations(range(n), j):
        coeffs = signed_elementary([domain[index] for index in indices], j, p)
        buckets[coeffs[:codim]].append(indices)
        scale_counter[periodicity_scale(indices, n)] += 1
    histogram = Counter(len(items) for items in buckets.values())
    counts = payload["counts"]
    require(counts["total_locators"] == comb(n, j), "total locator mismatch")
    require(counts["distinct_flats_hit"] == len(buckets), "distinct flat count mismatch")
    require(counts["occupancy_histogram"] == {str(k): v for k, v in sorted(histogram.items())}, "occupancy histogram mismatch")
    require(counts["max_occupancy"] == (max(histogram) if histogram else 0), "max occupancy mismatch")
    require(counts["density_floor"] == density_floor(comb(n, j), p, codim), "density floor mismatch")
    require(counts["scale_histogram"] == {str(k): v for k, v in sorted(scale_counter.items())}, "scale histogram mismatch")
    regression = payload.get("oracle_regression")
    if regression:
        require(all(regression["matches"].values()), "oracle regression mismatch")
    check_witnesses(payload, p, n, j, payload["extremal_flat"])


def recount_all_j(payload: dict[str, Any]) -> None:
    params = payload["parameters"]
    p = int(params["p"])
    n = int(params["n"])
    domain = subgroup_domain(p, n)
    summaries = []
    for j in range(n + 1):
        scale_counter: Counter[int] = Counter()
        for indices in itertools.combinations(range(n), j):
            scale_counter[periodicity_scale(indices, n)] += 1
        summaries.append(
            {
                "j": j,
                "total_locators": comb(n, j),
                "scale_histogram": {str(k): v for k, v in sorted(scale_counter.items())},
            }
        )
    require(payload["domain"]["elements"] == domain, "domain mismatch")
    require(payload["j_summaries"] == summaries, "all-j summaries mismatch")


def check_witness_only(payload: dict[str, Any]) -> None:
    params = payload["parameters"]
    p = int(params["p"])
    n = int(params["n"])
    j = int(params["j"])
    codim = int(params["codim"])
    counts = payload["counts"]
    require(counts["total_locators"] == comb(n, j), "large-row total mismatch")
    require(counts["density_floor"] == density_floor(comb(n, j), p, codim), "large-row density floor mismatch")
    check_witnesses(payload, p, n, j, payload["extremal_flat"])


def check_payload(payload: dict[str, Any]) -> None:
    require(payload.get("schema_version") == SCHEMA_VERSION, "schema mismatch")
    require(payload.get("theorem_problem_id") == THEOREM_PROBLEM_ID, "theorem/problem id mismatch")
    require(payload.get("payload_sha256") == sha256_payload(payload), "payload hash mismatch")
    coverage = payload["coverage"]
    if coverage == "full-enumeration" and "j_summaries" in payload:
        recount_all_j(payload)
    elif coverage == "full-enumeration":
        recount_prefix(payload)
    elif coverage == "witness-only-large-row":
        check_witness_only(payload)
    else:
        raise AssertionError(f"unknown coverage {coverage!r}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, nargs="+", required=True, help="certificate JSON file(s)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for path in args.check:
        payload = json.loads(path.read_text(encoding="utf-8"))
        check_payload(payload)
        print(f"master_flatness_incidence: status=AUDIT result=PASS file={path.as_posix()}")


if __name__ == "__main__":
    main()
