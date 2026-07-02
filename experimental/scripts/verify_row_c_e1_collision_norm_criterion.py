#!/usr/bin/env python3
"""E1 / Q2.15 collision-norm criterion for quotient e_1 value sets.

This is a small algebraic verifier for the Row-C E1 lane.  It checks, on
toy quotient orders, the cyclotomic norm gate behind modular e_1 collisions:
if two characteristic-zero antipodal classes have distinct e_1 values, then a
collision modulo a prime p == 1 mod N can occur only when p divides the
integer norm of their cyclotomic difference.  Conversely, if p divides that
norm, then some Galois conjugate embedding has a modular collision.

Run:
  python3 experimental/scripts/verify_row_c_e1_collision_norm_criterion.py
  python3 experimental/scripts/verify_row_c_e1_collision_norm_criterion.py --emit
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from dataclasses import dataclass
from pathlib import Path

import sympy


OUTPUT = Path(
    "experimental/data/certificates/row-c-e1-sampling/"
    "row_c_e1_collision_norm_criterion.json"
)
PRIMES_BY_ORDER = {
    8: [17, 41, 73, 89, 97],
    16: [17, 97, 113, 193, 257],
}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ClassValue:
    signed_indices: tuple[int, ...]
    coeffs: tuple[int, ...]


def primitive_root(p: int) -> int:
    factors = sympy.factorint(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise RuntimeError(f"no primitive root for F_{p}")


def primitive_order_element(p: int, order: int) -> int:
    assert (p - 1) % order == 0
    omega = pow(primitive_root(p), (p - 1) // order, p)
    assert pow(omega, order, p) == 1
    assert all(pow(omega, order // q, p) != 1 for q in sympy.factorint(order))
    return omega


def feasible_t_values(order: int, ell: int) -> list[int]:
    return [
        t for t in range(0, min(ell, order - ell) + 1)
        if (ell - t) % 2 == 0
    ]


def class_values(order: int, ell: int) -> list[ClassValue]:
    """Characteristic-zero antipodal classes, represented by singleton signs."""
    half = order // 2
    values = []
    for t in feasible_t_values(order, ell):
        for indices in itertools.combinations(range(half), t):
            for signs in itertools.product((-1, 1), repeat=t):
                coeffs = [0] * order
                signed = []
                for index, sign in zip(indices, signs):
                    coeffs[index] = sign
                    signed.append(sign * (index + 1))
                values.append(ClassValue(tuple(signed), tuple(coeffs)))
    return values


def coeff_sub(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a - b for a, b in zip(left, right))


def eval_coeffs_mod_p(coeffs: tuple[int, ...], omega: int, p: int) -> int:
    total = 0
    power = 1
    for coeff in coeffs:
        total = (total + coeff * power) % p
        power = (power * omega) % p
    return total


def cyclotomic_norm(order: int, coeffs: tuple[int, ...]) -> int:
    x = sympy.Symbol("x")
    poly = sum(coeff * x ** i for i, coeff in enumerate(coeffs) if coeff)
    if poly == 0:
        return 0
    phi = sympy.cyclotomic_poly(order, x, polys=True)
    resultant = sympy.resultant(sympy.Poly(poly, x), phi, x)
    return int(resultant)


def unit_exponents(order: int) -> list[int]:
    return [a for a in range(1, order + 1) if math.gcd(a, order) == 1]


def pair_digest(left: ClassValue, right: ClassValue) -> str:
    payload = json.dumps(
        [left.signed_indices, right.signed_indices],
        separators=(",", ":"),
    )
    return sha256_text(payload)


def check_order(order: int, ell: int, sample_limit: int | None = None) -> dict:
    values = class_values(order, ell)
    units = unit_exponents(order)
    primes = PRIMES_BY_ORDER[order]
    pair_iter = itertools.combinations(values, 2)
    if sample_limit is not None:
        pair_iter = itertools.islice(pair_iter, sample_limit)

    pairs_checked = 0
    zero_norm_pairs = 0
    nonzero_norm_pairs = 0
    fixed_collisions = 0
    norm_prime_hits = 0
    max_abs_norm = 0
    max_norm_bits = 0
    first_norm_hit = None

    for left, right in pair_iter:
        pairs_checked += 1
        diff = coeff_sub(left.coeffs, right.coeffs)
        norm = cyclotomic_norm(order, diff)
        if norm == 0:
            zero_norm_pairs += 1
            continue
        nonzero_norm_pairs += 1
        max_abs_norm = max(max_abs_norm, abs(norm))
        max_norm_bits = max(max_norm_bits, abs(norm).bit_length())
        for p in primes:
            omega = primitive_order_element(p, order)
            fixed_collision = eval_coeffs_mod_p(diff, omega, p) == 0
            norm_hit = norm % p == 0
            conjugate_collision = any(
                eval_coeffs_mod_p(diff, pow(omega, a, p), p) == 0
                for a in units
            )
            if fixed_collision and not norm_hit:
                return {
                    "name": f"collision_norm_order_{order}",
                    "status": "FAIL",
                    "reason": "fixed embedding collision without norm divisibility",
                    "p": p,
                    "pair_sha256": pair_digest(left, right),
                }
            if norm_hit and not conjugate_collision:
                return {
                    "name": f"collision_norm_order_{order}",
                    "status": "FAIL",
                    "reason": "norm divisibility without any conjugate collision",
                    "p": p,
                    "pair_sha256": pair_digest(left, right),
                }
            fixed_collisions += int(fixed_collision)
            norm_prime_hits += int(norm_hit)
            if norm_hit and first_norm_hit is None:
                first_norm_hit = {
                    "p": p,
                    "pair_sha256": pair_digest(left, right),
                    "norm_abs": abs(norm),
                    "fixed_embedding_collision": fixed_collision,
                    "some_conjugate_collision": conjugate_collision,
                    "left_signed_indices": list(left.signed_indices),
                    "right_signed_indices": list(right.signed_indices),
                }

    height_bound = (2 * ell) ** (order // 2)
    ok = max_abs_norm <= height_bound
    return {
        "name": f"collision_norm_order_{order}",
        "status": "PASS" if ok else "FAIL",
        "order": order,
        "ell_prime": ell,
        "antipodal_class_count": len(values),
        "pairs_checked": pairs_checked,
        "sample_limit": sample_limit,
        "zero_norm_pairs_same_cyclotomic_value": zero_norm_pairs,
        "nonzero_norm_pairs": nonzero_norm_pairs,
        "primes_checked": primes,
        "fixed_embedding_collisions_seen": fixed_collisions,
        "norm_prime_hits_seen": norm_prime_hits,
        "max_abs_norm": max_abs_norm,
        "max_norm_bits": max_norm_bits,
        "height_bound": height_bound,
        "height_bound_bits": height_bound.bit_length(),
        "first_norm_hit": first_norm_hit,
    }


def build_report() -> dict:
    checks = [
        check_order(order=8, ell=5),
        check_order(order=16, ell=9, sample_limit=20_000),
    ]
    return {
        "schema": "row_c_e1_collision_norm_criterion_v1",
        "status": "EXPERIMENTAL_VERIFICATION_OF_PROVED_CRITERION",
        "roadmap_task": "Q2.15 / collision_norm_criterion",
        "object": "cyclotomic norm gate for quotient e_1 value collisions",
        "criterion": {
            "fixed_embedding_collision_implies": "p divides Norm_Q(zeta_N)(Delta)",
            "norm_divisibility_implies": "some Galois conjugate embedding collides",
            "height_bound": "|Norm(Delta)| <= (2 ell')^phi(N), specialized to phi(2^a)=N/2",
        },
        "checks": checks,
        "script_sha256": sha256_text(Path(__file__).read_text()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()

    report = build_report()
    print("=" * 76)
    print("E1/Q2.15 collision-norm criterion verifier")
    print("=" * 76)
    ok = True
    for check in report["checks"]:
        ok &= check["status"] == "PASS"
        print(f"[{check['status']}] {check['name']}")
        for key, value in check.items():
            if key not in {"name", "status", "first_norm_hit"}:
                print(f"        {key}: {value}")
        print(f"        first_norm_hit: {check.get('first_norm_hit')}")
    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(f"\nwrote {OUTPUT}")
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
