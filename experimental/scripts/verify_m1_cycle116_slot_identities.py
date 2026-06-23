#!/usr/bin/env python3
"""Replay the 336 Cycle116 slot identities for the M1 finite-chain contract.

This nonmutating verifier supports
experimental/notes/m1/m1_cycle116_finite_chain_contract.md. It checks, from
the explicit F_17^16 model, that the Cycle116 slot blocks have the claimed
fixed-jet shape and evaluation normalization:

    R_{t,i,a}(X) = X^16 + O(X^10),
    R_{t,i,a}(beta) = 3^t u_t(i,a).

It also emits a stable digest for the normalized 336-value table u_t(i,a).
The heavy Cycle84 product occupancy census for products of these table values
is still an imported finite computation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Set, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import verify_m1_cycle116_field_lift_contract as lift


P = lift.P
DEGREE = lift.EXTENSION_DEGREE
FIELD_SIZE = P**DEGREE
DOMAIN_ORDER = 256

ZERO = (0,) * DEGREE
ONE = (1,) + (0,) * (DEGREE - 1)
MODULUS = tuple(lift.MODULUS)
ETA = (0,) * 9 + (6,) + (0,) * (DEGREE - 10)
BETA = (2, 1) + (0,) * (DEGREE - 2)

E_SETS = {
    1: {0, 1, 2, 3, 5, 11, 12, 13},
    2: {0, 1, 2, 3, 4, 8, 9, 14},
    3: {0, 1, 2, 4, 5, 7, 11, 14},
}


FieldElt = Tuple[int, ...]
FieldPoly = List[FieldElt]


def field(poly: Sequence[int]) -> FieldElt:
    return tuple(lift.pad(poly, DEGREE))


def fadd(a: FieldElt, b: FieldElt) -> FieldElt:
    return field(lift.poly_add(a, b))


def fsub(a: FieldElt, b: FieldElt) -> FieldElt:
    return field(lift.poly_sub(a, b))


def fneg(a: FieldElt) -> FieldElt:
    return fsub(ZERO, a)


def fmul(a: FieldElt, b: FieldElt) -> FieldElt:
    return field(lift.field_mul(a, b))


def fpow(a: FieldElt, exponent: int) -> FieldElt:
    return field(lift.field_pow(a, exponent))


def emb(value: int) -> FieldElt:
    return (value % P,) + (0,) * (DEGREE - 1)


def prime_poly_from_roots(roots: Iterable[int]) -> Tuple[int, ...]:
    out = [1]
    for root in roots:
        nxt = [0] * (len(out) + 1)
        for degree, coeff in enumerate(out):
            nxt[degree] = (nxt[degree] - root * coeff) % P
            nxt[degree + 1] = (nxt[degree + 1] + coeff) % P
        out = nxt
    return tuple(out)


def peval(coeffs: Sequence[int], z: FieldElt) -> FieldElt:
    out = ZERO
    for coeff in reversed(coeffs):
        out = fadd(fmul(out, z), emb(coeff))
    return out


def poly_from_roots(roots: Sequence[FieldElt]) -> FieldPoly:
    out = [ONE]
    for root in roots:
        nxt = [ZERO] * (len(out) + 1)
        for degree, coeff in enumerate(out):
            nxt[degree] = fsub(nxt[degree], fmul(coeff, root))
            nxt[degree + 1] = fadd(nxt[degree + 1], coeff)
        out = nxt
    return out


def b_set(seed: int, shift: int) -> Set[int]:
    return {(shift + exponent) % 16 for exponent in E_SETS[seed]}


def color(seed: int, shift: int) -> int:
    return (sum(E_SETS[seed]) + 8 * (shift & 1)) % 16


def slot_product(
    beta_squared: FieldElt,
    eta_2t: FieldElt,
    exponents: Set[int],
) -> FieldElt:
    out = ONE
    for exponent in sorted(exponents):
        root_square = fmul(eta_2t, emb(pow(3, exponent, P)))
        out = fmul(out, fsub(beta_squared, root_square))
    return out


def normalized_u(
    seed_polys: Dict[int, Tuple[int, ...]],
    beta_squared: FieldElt,
    t: int,
    seed: int,
    shift: int,
) -> FieldElt:
    eta_minus_2t = fpow(ETA, (DOMAIN_ORDER - 2 * t) % DOMAIN_ORDER)
    arg = fmul(fmul(beta_squared, emb(pow(3, (-shift) % 16, P))), eta_minus_2t)
    value = peval(seed_polys[seed], arg)
    if shift & 1:
        value = fneg(value)
    return value


def table_digest(rows: Sequence[Dict[str, Any]]) -> str:
    payload = json.dumps(rows, separators=(",", ":"), sort_keys=True).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def build_report() -> Dict[str, Any]:
    beta_squared = fmul(BETA, BETA)
    seed_polys = {
        seed: prime_poly_from_roots(pow(3, exponent, P) for exponent in exponents)
        for seed, exponents in E_SETS.items()
    }

    eta_checks = {
        "modulus_irreducible": lift.is_irreducible_modulus(),
        "eta_order_256": fpow(ETA, 256) == ONE and fpow(ETA, 128) != ONE,
        "eta_128_minus_one": fpow(ETA, 128) == emb(-1),
        "eta_16_is_3": fpow(ETA, 16) == emb(3),
        "beta_outside_D0": fpow(BETA, 256) != ONE,
    }

    failed_eta = [name for name, value in eta_checks.items() if not value]
    if failed_eta:
        raise AssertionError(f"failed model checks: {', '.join(failed_eta)}")

    h32 = [fpow(ETA, 8 * index) for index in range(32)]
    cosets = [
        {fmul(fpow(ETA, t), y) for y in h32}
        for t in range(8)
    ]
    coset_checks = {
        "H32_size_32": len(set(h32)) == 32,
        "eight_cosets_size_32": all(len(coset) == 32 for coset in cosets),
        "eight_cosets_partition_D0": len(set().union(*cosets)) == 256,
        "eight_cosets_disjoint": all(
            cosets[left].isdisjoint(cosets[right])
            for left in range(8)
            for right in range(left)
        ),
    }
    failed_cosets = [name for name, value in coset_checks.items() if not value]
    if failed_cosets:
        raise AssertionError(f"failed coset checks: {', '.join(failed_cosets)}")

    seed_rows = []
    for seed, coeffs in seed_polys.items():
        if (
            len(coeffs) != 9
            or coeffs[8] != 1
            or coeffs[7] != 0
            or coeffs[6] != 0
        ):
            raise AssertionError((seed, coeffs))
        seed_rows.append(
            {
                "seed": seed,
                "E": sorted(E_SETS[seed]),
                "sum_mod_16": sum(E_SETS[seed]) % 16,
                "poly_coefficients_low_to_high": list(coeffs),
            }
        )

    all_y_sets = set()
    normalized_rows: List[Dict[str, Any]] = []
    direct_slot_values: Dict[Tuple[int, int, int], FieldElt] = {}
    slot_checks = 0

    for t in range(1, 8):
        eta_t = fpow(ETA, t)
        eta_2t = fpow(ETA, 2 * t)
        for seed in (1, 2, 3):
            for shift in range(16):
                exponents = b_set(seed, shift)
                expected_color = color(seed, shift)
                if (
                    len(exponents) != 8
                    or sum(exponents) % 16 != expected_color
                ):
                    raise AssertionError((t, seed, shift, exponents, expected_color))

                target_squares = {emb(pow(3, exponent, P)) for exponent in exponents}
                y_values = tuple(y for y in h32 if fpow(y, 2) in target_squares)
                if len(y_values) != 16 or len(set(y_values)) != 16:
                    raise AssertionError((t, seed, shift, "bad Y", len(y_values)))
                all_y_sets.add(frozenset(y_values))

                roots = [fmul(eta_t, y) for y in y_values]
                if not set(roots).issubset(cosets[t]):
                    raise AssertionError((t, seed, shift, "roots outside active coset"))

                locator = poly_from_roots(roots)
                if len(locator) != 17 or locator[16] != ONE:
                    raise AssertionError((t, seed, shift, "bad locator degree"))
                if any(locator[degree] != ZERO for degree in range(11, 16)):
                    raise AssertionError((t, seed, shift, "missing fixed jet"))

                block_at_beta = ONE
                root_product = ONE
                for root in roots:
                    block_at_beta = fmul(block_at_beta, fsub(BETA, root))
                    root_product = fmul(root_product, root)

                factored_product = slot_product(beta_squared, eta_2t, exponents)
                if block_at_beta != factored_product:
                    raise AssertionError((t, seed, shift, "block product mismatch"))
                if root_product != emb(pow(3, (t + sum(exponents)) % 16, P)):
                    raise AssertionError((t, seed, shift, "root product mismatch"))

                u_value = normalized_u(seed_polys, beta_squared, t, seed, shift)
                if block_at_beta != fmul(emb(pow(3, t, P)), u_value):
                    raise AssertionError((t, seed, shift, "normalization mismatch"))

                direct_slot_values[(t, seed, shift)] = u_value
                normalized_rows.append(
                    {
                        "t": t,
                        "seed": seed,
                        "shift": shift,
                        "color": expected_color,
                        "u": list(u_value),
                    }
                )
                slot_checks += 1

    if slot_checks != 336 or len(all_y_sets) != 48:
        raise AssertionError((slot_checks, len(all_y_sets)))

    full_product_checks = {}
    for t in range(1, 8):
        full_product = slot_product(beta_squared, fpow(ETA, 2 * t), set(range(16)))
        expected = fsub(fpow(BETA, 32), emb(pow(3, 2 * t, P)))
        full_product_checks[f"slot_{t}"] = full_product == expected
    failed_full_products = [
        name for name, value in full_product_checks.items() if not value
    ]
    if failed_full_products:
        raise AssertionError(f"failed full products: {', '.join(failed_full_products)}")

    injectivity_checks = {}
    for t in range(1, 8):
        values = {
            direct_slot_values[(t, seed, shift)]
            for seed in (1, 2, 3)
            for shift in range(16)
        }
        injectivity_checks[f"slot_{t}"] = len(values) == 48
    failed_injectivity = [
        name for name, value in injectivity_checks.items() if not value
    ]
    if failed_injectivity:
        raise AssertionError(f"failed injectivity: {', '.join(failed_injectivity)}")

    digest = table_digest(normalized_rows)

    return {
        "status": "PASS",
        "proof_status": "AUDIT / FINITE-MODEL-IDENTITY-VERIFIED",
        "theorem_problem_id": "M1 Cycle116 336 slot identities",
        "model": {
            "field": "F_17[X]/(X^16+X^8+3)",
            "field_size": FIELD_SIZE,
            "modulus_sparse_coefficients": lift.coeffs_to_sparse(MODULUS),
            "eta_sparse_coefficients": lift.coeffs_to_sparse(ETA),
            "beta_sparse_coefficients": lift.coeffs_to_sparse(BETA),
        },
        "seed_polynomials": seed_rows,
        "slot_table": {
            "rows": len(normalized_rows),
            "digest_sha256": digest,
            "entry_order": "lexicographic by (t, seed, shift)",
            "entry_format": "{t, seed, shift, color, u[16 coefficients]}",
            "distinct_Y_sets": len(all_y_sets),
        },
        "checks": {
            **eta_checks,
            **coset_checks,
            "three_seed_polynomials_have_zero_Z7_Z6": True,
            "slot_identities_checked": slot_checks,
            "all_336_locators_have_X16_O_X10_shape": True,
            "all_336_evaluations_match_3t_u_tia": True,
            "all_48_Y_sets_distinct": len(all_y_sets) == 48,
            "full_slot_product_oracles": all(full_product_checks.values()),
            "single_slot_u_maps_injective": all(injectivity_checks.values()),
        },
        "imports_required": [
            "Cycle84 color/witness replay and energy upper bound D <= 24",
            "official ABF source gate verification",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    model = report["model"]
    table = report["slot_table"]

    print("m1_cycle116_slot_identities: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(
        "model="
        f"{model['field']}, |F|={model['field_size']}, "
        f"eta={model['eta_sparse_coefficients']}, beta={model['beta_sparse_coefficients']}"
    )
    print(
        "slot_table="
        f"{table['rows']} normalized values, digest={table['digest_sha256']}, "
        f"distinct_Y_sets={table['distinct_Y_sets']}"
    )
    print(
        "checked="
        "336 block locators X^16+O(X^10), "
        "336 evaluations R_tia(beta)=3^t u_tia, "
        "full-slot products, single-slot injectivity"
    )
    print("imports_required=" + "; ".join(report["imports_required"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Replay the Cycle116 336 slot identities."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print the audit report as JSON",
    )
    args = parser.parse_args()

    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human(report)


if __name__ == "__main__":
    main()
