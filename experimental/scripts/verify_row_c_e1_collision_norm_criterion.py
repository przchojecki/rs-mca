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
import functools
import operator
from dataclasses import dataclass
from pathlib import Path

import sympy


OUTPUT = Path(
    "experimental/data/certificates/row-c-e1-sampling/"
    "row_c_e1_collision_norm_criterion.json"
)
ROW_N = 2 ** 10
ROW_C_COMPATIBLE_ORDERS = [64, 128, 256]
RHO_NUM, RHO_DEN = 1, 2
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


def row_c_prime() -> int:
    """Smallest prime p > 2^250 with p = 1 mod 1024."""
    p = (1 << 250) + ((1 - (1 << 250)) % ROW_N)
    while not sympy.isprime(p):
        p += ROW_N
    return p


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
    norm_product_abs = 1
    prime_divisors_seen: set[int] = set()
    log2_norm_sum = 0.0

    for left, right in pair_iter:
        pairs_checked += 1
        diff = coeff_sub(left.coeffs, right.coeffs)
        norm = cyclotomic_norm(order, diff)
        if norm == 0:
            zero_norm_pairs += 1
            continue
        nonzero_norm_pairs += 1
        abs_norm = abs(norm)
        max_abs_norm = max(max_abs_norm, abs_norm)
        max_norm_bits = max(max_norm_bits, abs_norm.bit_length())
        norm_product_abs *= abs_norm
        log2_norm_sum += math.log2(abs_norm)
        prime_divisors_seen.update(sympy.factorint(abs_norm).keys())
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
    prime_floor = min(primes)
    large_prime_divisors = sorted(q for q in prime_divisors_seen if q >= prime_floor)
    large_prime_product = functools.reduce(
        operator.mul, large_prime_divisors, 1
    )
    large_prime_product_divides = norm_product_abs % large_prime_product == 0
    exact_prime_budget_ok = (
        large_prime_product_divides and large_prime_product <= norm_product_abs
    )
    log_prime_count_bound = (
        math.floor(log2_norm_sum / math.log2(prime_floor))
        if nonzero_norm_pairs
        else 0
    )
    height_prime_count_bound = (
        math.floor(nonzero_norm_pairs * math.log2(height_bound) / math.log2(prime_floor))
        if nonzero_norm_pairs
        else 0
    )
    ok = max_abs_norm <= height_bound and exact_prime_budget_ok
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
        "prime_floor_for_exceptional_count": prime_floor,
        "distinct_prime_divisors_seen": sorted(prime_divisors_seen),
        "large_prime_divisors_seen": large_prime_divisors,
        "large_prime_divisor_count": len(large_prime_divisors),
        "large_prime_product_divides_norm_product": large_prime_product_divides,
        "large_prime_product_le_norm_product": exact_prime_budget_ok,
        "log_prime_count_bound": log_prime_count_bound,
        "height_prime_count_bound": height_prime_count_bound,
        "log2_norm_product": log2_norm_sum,
        "first_norm_hit": first_norm_hit,
    }


def max_certified_half_l1_radius(order: int, p: int) -> int:
    """Largest d with (2d)^phi(order) < p."""
    phi = int(sympy.totient(order))
    radius = 0
    while (2 * (radius + 1)) ** phi < p:
        radius += 1
    return radius


def max_norm_factor_root_budget(phi: int, p: int) -> int:
    """Largest R with R^phi < p."""
    root = 0
    while (root + 1) ** phi < p:
        root += 1
    return root


def row_c_graded_collision_radius() -> dict:
    """Exact Row-C consequences of the norm-height gate.

    If two characteristic-zero dyadic antipodal classes differ by coefficient
    l1 norm at most 2d, then every nonzero norm has absolute value < p whenever
    (2d)^phi(N) < p.  The norm criterion then forbids fixed-embedding modular
    collisions.  For N=64 the full class diameter already satisfies the bound.
    """
    p = row_c_prime()
    rows = []
    for order in ROW_C_COMPATIBLE_ORDERS:
        assert ROW_N % order == 0
        assert (p - 1) % order == 0
        ell_num = RHO_NUM * order
        assert ell_num % RHO_DEN == 0
        ell = ell_num // RHO_DEN + 1
        phi = int(sympy.totient(order))
        full_l1_diameter = 2 * ell
        full_height_bound = full_l1_diameter ** phi
        certified_radius = max_certified_half_l1_radius(order, p)
        certified_height_bound = (2 * certified_radius) ** phi
        next_height_bound = (2 * (certified_radius + 1)) ** phi
        full_injective = full_height_bound < p
        rows.append({
            "N_prime": order,
            "ell_prime": ell,
            "phi_N": phi,
            "row_c_prime_bits": p.bit_length(),
            "full_class_l1_diameter": full_l1_diameter,
            "full_height_bound_bits": full_height_bound.bit_length(),
            "full_class_injective_mod_row_c_prime": full_injective,
            "certified_half_l1_radius_d": certified_radius,
            "certified_l1_radius_2d": 2 * certified_radius,
            "certified_height_bound_bits": certified_height_bound.bit_length(),
            "next_radius_height_bound_bits": next_height_bound.bit_length(),
            "radius_is_maximal_by_height_gate": (
                certified_height_bound < p <= next_height_bound
            ),
        })
    ok = (
        p > 2 ** 250
        and p % ROW_N == 1
        and rows[0]["N_prime"] == 64
        and rows[0]["full_class_injective_mod_row_c_prime"]
        and rows[0]["certified_half_l1_radius_d"] >= rows[0]["ell_prime"]
        and rows[1]["certified_half_l1_radius_d"] == 7
        and rows[2]["certified_half_l1_radius_d"] == 1
        and all(row["radius_is_maximal_by_height_gate"] for row in rows)
    )
    return {
        "name": "row_c_graded_collision_radius",
        "status": "PASS" if ok else "FAIL",
        "row_c_prime": p,
        "row_c_prime_sha256": sha256_text(str(p)),
        "rule": (
            "coefficient l1-distance <= 2d and (2d)^phi(N) < p "
            "implies no distinct characteristic-zero class collision modulo p"
        ),
        "dyadic_basis_note": (
            "for N=2^a, powers 1,zeta,...,zeta^(N/2-1) form the coefficient "
            "basis used by the antipodal class normal form, so distinct class "
            "keys have nonzero cyclotomic difference"
        ),
        "rows": rows,
    }


def scalar_coeffs(order: int, scalar: int) -> tuple[int, ...]:
    return (scalar,) + (0,) * (order - 1)


def coeff_mul_scalar(coeffs: tuple[int, ...], scalar: int) -> tuple[int, ...]:
    return tuple(scalar * coeff for coeff in coeffs)


def cluster_certificate_lemmas() -> dict:
    """Machine-check the elementary cluster-certificate consequences.

    The one-check lemma is stated with an explicit algebraic-integer quotient
    factor.  That avoids confusing the certificate lemma with the later
    generator-economy design problem, where such factorizations must be built.
    """
    graded = row_c_graded_collision_radius()
    p_row = graded["row_c_prime"]
    free_clique_rows = []
    root_budget_rows = []
    for row in graded["rows"]:
        phi = row["phi_N"]
        root = max_norm_factor_root_budget(phi, p_row)
        root_budget_rows.append({
            "N_prime": row["N_prime"],
            "phi_N": phi,
            "root_budget_R": root,
            "R_power_phi_bits": (root ** phi).bit_length(),
            "next_power_phi_bits": ((root + 1) ** phi).bit_length(),
            "R_is_maximal": root ** phi < p_row <= (root + 1) ** phi,
        })
        free_clique_rows.append({
            "N_prime": row["N_prime"],
            "certified_half_l1_radius_d": row["certified_half_l1_radius_d"],
            "certified_l1_radius_2d": row["certified_l1_radius_2d"],
            "free_clique_rule": (
                "any characteristic-zero distinct class set with pairwise "
                "coefficient half-l1 distance <= d has no modular collisions"
            ),
            "full_row_c_class_is_free_clique": row[
                "full_class_injective_mod_row_c_prime"
            ],
        })

    # Toy one-check cross-cluster replay in Z[zeta_8], p=17.  The common
    # center difference is the integer 3.  The quotient factors are algebraic
    # integers with norm below p, so checking Norm(3) once certifies all
    # products 3*q.
    toy_order = 8
    toy_phi = int(sympy.totient(toy_order))
    toy_p = 17
    toy_root_budget = max_norm_factor_root_budget(toy_phi, toy_p)
    delta = scalar_coeffs(toy_order, 3)
    delta_norm = abs(cyclotomic_norm(toy_order, delta))
    quotient_factors = [
        ("1", scalar_coeffs(toy_order, 1)),
        ("2", scalar_coeffs(toy_order, 2)),
        ("1+zeta", (1, 1) + (0,) * (toy_order - 2)),
    ]
    quotient_rows = []
    for name, quotient in quotient_factors:
        quotient_norm = abs(cyclotomic_norm(toy_order, quotient))
        product = coeff_mul_scalar(quotient, 3)
        product_norm = abs(cyclotomic_norm(toy_order, product))
        quotient_rows.append({
            "quotient_factor": name,
            "quotient_norm": quotient_norm,
            "quotient_norm_lt_p": quotient_norm < toy_p,
            "product_norm": product_norm,
            "product_norm_factorization_ok": (
                product_norm == delta_norm * quotient_norm
            ),
            "product_certified_nonzero_mod_p": (
                delta_norm % toy_p != 0
                and 0 < quotient_norm < toy_p
                and product_norm % toy_p != 0
            ),
        })

    base = (1, 1) + (0,) * (toy_order - 2)
    base_norm = abs(cyclotomic_norm(toy_order, base))
    integer_rows = []
    for multiplier in [2, 3, 16]:
        multiplied = coeff_mul_scalar(base, multiplier)
        multiplied_norm = abs(cyclotomic_norm(toy_order, multiplied))
        integer_rows.append({
            "multiplier": multiplier,
            "multiplier_lt_p": 0 < multiplier < toy_p,
            "norm_factorization_ok": (
                multiplied_norm == (multiplier ** toy_phi) * base_norm
            ),
            "certified_nonzero_mod_p": (
                base_norm % toy_p != 0 and multiplier % toy_p != 0
                and multiplied_norm % toy_p != 0
            ),
        })

    ok = (
        graded["status"] == "PASS"
        and all(row["R_is_maximal"] for row in root_budget_rows)
        and all(row["certified_half_l1_radius_d"] >= 1 for row in free_clique_rows)
        and delta_norm % toy_p != 0
        and toy_root_budget == 2
        and all(row["quotient_norm_lt_p"] for row in quotient_rows)
        and all(row["product_norm_factorization_ok"] for row in quotient_rows)
        and all(row["product_certified_nonzero_mod_p"] for row in quotient_rows)
        and all(row["norm_factorization_ok"] for row in integer_rows)
        and all(row["certified_nonzero_mod_p"] for row in integer_rows)
    )
    return {
        "name": "cluster_certificate_lemmas",
        "status": "PASS" if ok else "FAIL",
        "roadmap_task": "QA.14 / cluster_certificates",
        "free_clique_from_graded_radius": free_clique_rows,
        "row_c_norm_factor_root_budgets": root_budget_rows,
        "one_check_cross_cluster_lemma": {
            "statement": (
                "if every cross difference factors as Delta*q with q an "
                "algebraic integer, p does not divide Norm(Delta), and "
                "0 < |Norm(q)| < p, then one Norm(Delta) check certifies "
                "all cross differences"
            ),
            "toy_order": toy_order,
            "toy_prime": toy_p,
            "toy_phi": toy_phi,
            "toy_root_budget_R": toy_root_budget,
            "delta_norm": delta_norm,
            "quotient_rows": quotient_rows,
        },
        "integer_factor_freebie": {
            "statement": (
                "integer multiples m*Delta are certified whenever "
                "0 < m < p and Delta is certified"
            ),
            "base_norm": base_norm,
            "rows": integer_rows,
        },
        "non_claim": (
            "This certifies the cluster-compression lemmas only; constructing "
            "large generator-economy cluster designs is a separate open task."
        ),
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
            "graded_collision_radius": (
                "if coefficient l1-distance <= 2d and (2d)^phi(N) < p, "
                "the norm criterion forbids distinct-class modular collisions"
            ),
            "cluster_certificates": (
                "free cliques follow from the graded radius; one-check "
                "cross-cluster certificates follow from a common certified "
                "factor Delta and algebraic-integer quotient factors of norm < p"
            ),
            "exceptional_prime_count": (
                "#{p >= P0 dividing some nonzero norm} <= "
                "sum_pairs log |Norm(Delta)| / log P0"
            ),
        },
        "checks": checks,
        "row_c_graded_collision_radius": row_c_graded_collision_radius(),
        "cluster_certificate_lemmas": cluster_certificate_lemmas(),
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
    radius = report["row_c_graded_collision_radius"]
    ok &= radius["status"] == "PASS"
    print(f"[{radius['status']}] {radius['name']}")
    print(f"        row_c_prime_sha256: {radius['row_c_prime_sha256']}")
    print(f"        rule: {radius['rule']}")
    for row in radius["rows"]:
        print(
            "        "
            f"N'={row['N_prime']} ell'={row['ell_prime']} "
            f"full_injective={row['full_class_injective_mod_row_c_prime']} "
            f"certified_half_l1_radius={row['certified_half_l1_radius_d']} "
            f"full_height_bits={row['full_height_bound_bits']} "
            f"next_radius_bits={row['next_radius_height_bound_bits']}"
        )
    clusters = report["cluster_certificate_lemmas"]
    ok &= clusters["status"] == "PASS"
    print(f"[{clusters['status']}] {clusters['name']}")
    print(f"        roadmap_task: {clusters['roadmap_task']}")
    print(
        "        one_check_toy: "
        f"order={clusters['one_check_cross_cluster_lemma']['toy_order']} "
        f"p={clusters['one_check_cross_cluster_lemma']['toy_prime']} "
        f"R={clusters['one_check_cross_cluster_lemma']['toy_root_budget_R']}"
    )
    print(
        "        integer_freebie_rows: "
        f"{len(clusters['integer_factor_freebie']['rows'])}"
    )
    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(f"\nwrote {OUTPUT}")
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
