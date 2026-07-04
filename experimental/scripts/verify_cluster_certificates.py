#!/usr/bin/env python3
"""Verify the arithmetic in cluster_certificates.md."""

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
OUT = REPO / "experimental" / "data" / "certificates" / "cluster-certificates" / "cluster_certificates.json"


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
    return int(sp.totient(n))


def require_prime_with_root(p: int, n: int) -> None:
    require(bool(sp.isprime(p)), "p must be prime")
    require((p - 1) % n == 0, "p must contain an order-N root in F_p")


def zpoly(exponents: Iterable[int], n: int) -> sp.Poly:
    x = sp.Symbol("x")
    return sp.Poly(sum(x ** (e % n) for e in exponents), x, domain=sp.ZZ)


def reduce_poly(poly: sp.Poly, n: int) -> sp.Poly:
    x = sp.Symbol("x")
    cyclo = sp.Poly(sp.cyclotomic_poly(n, x), x, domain=sp.ZZ)
    return sp.rem(poly, cyclo, domain=sp.ZZ)


def mul_mod(a: sp.Poly, b: sp.Poly, n: int) -> sp.Poly:
    return reduce_poly(a * b, n)


def norm_abs(poly: sp.Poly, n: int) -> int:
    x = sp.Symbol("x")
    reduced = reduce_poly(poly, n)
    if reduced.is_zero:
        return 0
    cyclo = sp.Poly(sp.cyclotomic_poly(n, x), x, domain=sp.ZZ)
    return abs(int(sp.resultant(reduced.as_expr(), cyclo.as_expr(), x)))


def swap_distance(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return len(set(a) - set(b))


def e1_diff(a: tuple[int, ...], b: tuple[int, ...], n: int) -> sp.Poly:
    return reduce_poly(zpoly(a, n) - zpoly(b, n), n)


def certified_radius(n: int, log2_p_floor: int) -> int:
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


def check_local_free_clique() -> CheckResult:
    n = 8
    log2_p = 9
    p = 1009
    require_prime_with_root(p, n)
    radius = certified_radius(n, log2_p)
    family = [
        (0, 1, 2),
        (0, 1, 3),
        (0, 2, 3),
        (1, 2, 3),
    ]
    diameter = max(swap_distance(a, b) for a, b in combinations(family, 2))
    require(diameter <= radius, "family diameter exceeds certified radius")
    require((2 * diameter) ** phi(n) < p, "strict norm gate failed for concrete p")
    pair_rows = []
    for a, b in combinations(family, 2):
        s = swap_distance(a, b)
        norm = norm_abs(e1_diff(a, b, n), n)
        require(norm > 0, "family is not characteristic-zero injective")
        require(norm <= (2 * s) ** phi(n), "graded norm bound failed")
        require(norm % p != 0, "mod-p collision detected in certified clique")
        pair_rows.append({"a": a, "b": b, "swap_distance": s, "norm_abs": norm})
    return CheckResult(
        "local free clique",
        "PASS",
        [
            f"N={n}, p={p}, log2 floor={log2_p}, d_*={radius}, family diameter={diameter}",
            f"checked {len(pair_rows)} pair norms and nondivisibility certificates",
        ],
    )


def check_multiplicative_cluster_certificate() -> tuple[CheckResult, dict]:
    n = 8
    p = 1009
    require_prime_with_root(p, n)
    x = sp.Symbol("x")
    delta = reduce_poly(sp.Poly(1 - x, x, domain=sp.ZZ), n)
    gammas = [
        reduce_poly(sp.Poly(1, x, domain=sp.ZZ), n),
        reduce_poly(sp.Poly(1 + x, x, domain=sp.ZZ), n),
        reduce_poly(sp.Poly(2 - x**2, x, domain=sp.ZZ), n),
    ]
    delta_norm = norm_abs(delta, n)
    require(delta_norm > 0 and delta_norm % p != 0, "Delta is not certified")
    gamma_rows = []
    for gamma in gammas:
        gnorm = norm_abs(gamma, n)
        product = mul_mod(delta, gamma, n)
        pnorm = norm_abs(product, n)
        require(0 < gnorm < p, "small gamma norm gate failed")
        require(pnorm == delta_norm * gnorm, "norm multiplicativity failed")
        require(pnorm % p != 0, "product should be certified")
        gamma_rows.append(
            {
                "gamma": str(gamma.as_expr()),
                "norm_abs_gamma": gnorm,
                "norm_abs_delta_gamma": pnorm,
            }
        )
    packet = {
        "quotient_order": n,
        "prime": p,
        "delta": str(delta.as_expr()),
        "norm_abs_delta": delta_norm,
        "gamma_rows": gamma_rows,
    }
    return (
        CheckResult(
            "multiplicative cross-cluster certificate",
            "PASS",
            [
                f"N={n}, p={p}, Norm(delta)={delta_norm}",
                f"checked {len(gamma_rows)} small factor products with one Delta norm check",
            ],
        ),
        packet,
    )


def check_integer_factor_freebie() -> tuple[CheckResult, list[dict[str, int]]]:
    n = 8
    p = 1009
    require_prime_with_root(p, n)
    x = sp.Symbol("x")
    delta = reduce_poly(sp.Poly(1 - x, x, domain=sp.ZZ), n)
    delta_norm = norm_abs(delta, n)
    require(delta_norm % p != 0, "Delta should be certified at p")
    rows = []
    for m in [1, 2, 3, 4]:
        factor = sp.Poly(m, x, domain=sp.ZZ)
        product = mul_mod(delta, factor, n)
        product_norm = norm_abs(product, n)
        expected = (abs(m) ** phi(n)) * delta_norm
        require(product_norm == expected, "integer norm scaling failed")
        require(product_norm % p != 0, "integer-factor product should be certified")
        rows.append(
            {
                "integer_factor": m,
                "norm_factor": abs(m) ** phi(n),
                "norm_factor_mod_p": (abs(m) ** phi(n)) % p,
                "norm_abs_product": product_norm,
            }
        )
    return (
        CheckResult(
            "integer-factor certification",
            "PASS",
            [
                f"N={n}, p={p}, Norm(delta)={delta_norm}",
                f"checked factors {[r['integer_factor'] for r in rows]}",
            ],
        ),
        rows,
    )


def build_result() -> dict:
    local_check = check_local_free_clique()
    mult_check, mult_packet = check_multiplicative_cluster_certificate()
    int_check, int_rows = check_integer_factor_freebie()
    script = Path(__file__).resolve()
    source = script_source(script)
    return {
        "status": "PROVED_CLUSTER_CERTIFICATES",
        "dag_nodes": ["cluster_certificates"],
        "depends_on": ["graded_collision_radius"],
        "object": "quotient e_1 value-set certification",
        "script": script_ref(script),
        "script_sha256": sha256_text(source),
        "checks": [asdict(c) for c in [local_check, mult_check, int_check]],
        "multiplicative_packet": mult_packet,
        "integer_factor_rows": int_rows,
        "non_claims": [
            "does not construct large generator-economy designs",
            "does not close the far-pair value-set lower bound",
            "does not certify characteristic-zero injectivity outside the stated family",
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
