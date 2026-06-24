#!/usr/bin/env python3
"""Verify the standalone Cycle84 -> Cycle120 LD_sw proof ledger.

The proof note proves the transfer

    Cycle84 finite count + Cycle116 fixed-jet identities
      -> LD_sw(RS[F_17^32,H,256],262) >= 52,747,567,092.

This verifier is intentionally nonmutating and compact.  It does not rerun the
Cycle84 26B-entry projected census.  Instead it:

* checks the existing public replay audit records the finite input;
* checks the generic fixed-jet locator transfer on exact prime-field toys;
* checks the smooth-padding transfer on exact prime-field toys;
* checks the Cycle116/Cycle120 specialization arithmetic and MCA density gate.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
from typing import Any, Iterable, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
PUBLIC_CYCLE84_AUDIT = (
    REPO_ROOT / "experimental" / "notes" / "m1" / "m1_cycle84_public_replay_audit.md"
)

NATIVE_DOMAIN_SIZE = 256
NATIVE_DIMENSION = 137
NATIVE_COSUPPORT = 113
FIXED_JET_SIGMA = 6
NATIVE_AGREEMENT = 143

PADDING_SIZE = 119
LIFT_DOMAIN_SIZE = 512
LIFT_DIMENSION = 256
LIFT_AGREEMENT = 262

BAD_PARAMETER_COUNT = 52_747_567_092
FIELD_SIZE = 17**32
EPSILON_DEN_BITS = 128


def inv_mod(a: int, p: int) -> int:
    a %= p
    if a == 0:
        raise ZeroDivisionError("inverse of zero")
    return pow(a, p - 2, p)


def trim(poly: Sequence[int], p: int) -> list[int]:
    out = [x % p for x in poly]
    while out and out[-1] == 0:
        out.pop()
    return out


def degree(poly: Sequence[int], p: int) -> int:
    return len(trim(poly, p)) - 1


def poly_add(a: Sequence[int], b: Sequence[int], p: int) -> list[int]:
    out = [0] * max(len(a), len(b))
    for i in range(len(out)):
        out[i] = ((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % p
    return trim(out, p)


def poly_sub(a: Sequence[int], b: Sequence[int], p: int) -> list[int]:
    out = [0] * max(len(a), len(b))
    for i in range(len(out)):
        out[i] = ((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % p
    return trim(out, p)


def poly_scale(c: int, poly: Sequence[int], p: int) -> list[int]:
    return trim([(c * x) % p for x in poly], p)


def poly_mul(a: Sequence[int], b: Sequence[int], p: int) -> list[int]:
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % p
    return trim(out, p)


def poly_from_roots(roots: Iterable[int], p: int) -> list[int]:
    poly = [1]
    for root in roots:
        poly = poly_mul(poly, [(-root) % p, 1], p)
    return poly


def poly_eval(poly: Sequence[int], x: int, p: int) -> int:
    acc = 0
    for coeff in reversed(poly):
        acc = (acc * x + coeff) % p
    return acc


def poly_derivative(poly: Sequence[int], p: int) -> list[int]:
    return trim([(i * poly[i]) % p for i in range(1, len(poly))], p)


def poly_divmod_monic(
    numerator: Sequence[int],
    divisor: Sequence[int],
    p: int,
) -> tuple[list[int], list[int]]:
    top = trim(numerator, p)
    bottom = trim(divisor, p)
    if not bottom or bottom[-1] != 1:
        raise AssertionError("monic divisor required")
    quotient = [0] * max(0, len(top) - len(bottom) + 1)
    while top and len(top) >= len(bottom):
        shift = len(top) - len(bottom)
        coeff = top[-1] % p
        quotient[shift] = coeff
        for i, bcoeff in enumerate(bottom):
            top[shift + i] = (top[shift + i] - coeff * bcoeff) % p
        top = trim(top, p)
    return trim(quotient, p), top


def interpolate(points: Sequence[int], values: Sequence[int], p: int) -> list[int]:
    if len(points) != len(values) or len(set(points)) != len(points):
        raise AssertionError("interpolation needs distinct points")
    out: list[int] = []
    for i, x_i in enumerate(points):
        basis = [1]
        denom = 1
        for j, x_j in enumerate(points):
            if i == j:
                continue
            basis = poly_mul(basis, [(-x_j) % p, 1], p)
            denom = denom * ((x_i - x_j) % p) % p
        out = poly_add(out, poly_scale(values[i] * inv_mod(denom, p), basis, p), p)
    return trim(out, p)


def exists_poly_degree_lt(
    points: Sequence[int],
    values: Sequence[int],
    degree_bound: int,
    p: int,
) -> bool:
    if degree_bound <= 0:
        return all(value % p == 0 for value in values)
    if len(points) <= degree_bound:
        return True
    candidate = interpolate(points[:degree_bound], values[:degree_bound], p)
    if degree(candidate, p) >= degree_bound:
        return False
    return all(poly_eval(candidate, x, p) == value % p for x, value in zip(points, values))


def top_key(subset: Sequence[int], j: int, sigma: int, p: int) -> tuple[int, ...]:
    locator = poly_from_roots(subset, p)
    return tuple(locator[j - t] for t in range(1, sigma + 1))


def find_fixed_jet_family(
    p: int,
    n: int,
    j: int,
    sigma: int,
) -> list[tuple[int, ...]]:
    buckets: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
    for subset in itertools.combinations(range(n), j):
        buckets.setdefault(top_key(subset, j, sigma, p), []).append(subset)
    family = max(buckets.values(), key=len)
    if len(family) < 2:
        raise AssertionError((p, n, j, sigma, "no nontrivial fixed-jet family"))
    return family


def syndrome(
    word: Sequence[int],
    domain: Sequence[int],
    redundancy: int,
    p: int,
) -> list[int]:
    domain_locator = poly_from_roots(domain, p)
    derivative = poly_derivative(domain_locator, p)
    lprime = {x: poly_eval(derivative, x, p) for x in domain}
    out = []
    for m in range(redundancy):
        total = 0
        for idx, x in enumerate(domain):
            total += pow(x, m, p) * word[idx] * inv_mod(lprime[x], p)
        out.append(total % p)
    return out


def build_fixed_jet_bad_line(
    *,
    p: int,
    n: int,
    j: int,
    sigma: int,
) -> dict[str, Any]:
    domain = list(range(n))
    beta = p - 1
    if beta in domain:
        raise AssertionError("beta must be outside the domain")
    family = find_fixed_jet_family(p, n, j, sigma)
    redundancy = j + sigma
    dimension = n - redundancy
    if dimension <= 0:
        raise AssertionError("toy code dimension must be positive")

    locators = {subset: poly_from_roots(subset, p) for subset in family}
    for left, right in itertools.combinations(family, 2):
        if degree(poly_sub(locators[left], locators[right], p), p) > j - sigma:
            raise AssertionError("family violates fixed-jet degree condition")

    quotient_values = []
    for m in range(redundancy):
        monomial = [0] * m + [1]
        values = []
        for subset in family:
            quotient, _ = poly_divmod_monic(monomial, locators[subset], p)
            values.append(poly_eval(quotient, beta, p))
        if len(set(values)) != 1:
            raise AssertionError("quotient value depends on the co-support")
        quotient_values.append(values[0])

    domain_locator = poly_from_roots(domain, p)
    domain_derivative = poly_derivative(domain_locator, p)
    domain_at_beta = poly_eval(domain_locator, beta, p)
    lprime = {x: poly_eval(domain_derivative, x, p) for x in domain}

    b_vector = [pow(beta, m, p) for m in range(redundancy)]
    a_vector = [(-q) % p for q in quotient_values]
    g_word = [domain_at_beta * inv_mod((beta - x) % p, p) % p for x in domain]
    if syndrome(g_word, domain, redundancy, p) != b_vector:
        raise AssertionError("Hg != B in fixed-jet toy")

    e_words: dict[tuple[int, ...], list[int]] = {}
    z_values: dict[tuple[int, ...], int] = {}
    for subset in family:
        locator_derivative = poly_derivative(locators[subset], p)
        p_beta = poly_eval(locators[subset], beta, p)
        if p_beta == 0:
            raise AssertionError("P_J(beta) vanished")
        e_word = []
        subset_set = set(subset)
        for x in domain:
            if x not in subset_set:
                e_word.append(0)
                continue
            denom = (beta - x) * poly_eval(locator_derivative, x, p)
            e_word.append(lprime[x] * inv_mod(denom, p) % p)
        z = inv_mod(p_beta, p)
        expected = [(a + z * b) % p for a, b in zip(a_vector, b_vector)]
        if syndrome(e_word, domain, redundancy, p) != expected:
            raise AssertionError("He_J != A+zB in fixed-jet toy")
        e_words[subset] = e_word
        z_values[subset] = z

    base = family[0]
    f_word = [(e_words[base][i] - z_values[base] * g_word[i]) % p for i in range(n)]
    if syndrome(f_word, domain, redundancy, p) != a_vector:
        raise AssertionError("Hf != A in fixed-jet toy")

    codewords: dict[tuple[int, ...], list[int]] = {}
    for subset in family:
        line_word = [(f_word[i] + z_values[subset] * g_word[i]) % p for i in range(n)]
        codeword = [(line_word[i] - e_words[subset][i]) % p for i in range(n)]
        if syndrome(codeword, domain, redundancy, p) != [0] * redundancy:
            raise AssertionError("line point minus e_J is not a codeword")
        support = [x for x in domain if x not in set(subset)]
        support_values = [g_word[x] for x in support]
        if exists_poly_degree_lt(support, support_values, dimension, p):
            raise AssertionError("g is code-explained on a bad support")
        codewords[subset] = codeword

    distinct_parameters = len(set(z_values.values()))
    if distinct_parameters < 2:
        raise AssertionError("toy did not produce distinct bad parameters")
    return {
        "p": p,
        "n": n,
        "j": j,
        "sigma": sigma,
        "dimension": dimension,
        "agreement": n - j,
        "family_size": len(family),
        "distinct_bad_parameters": distinct_parameters,
        "domain": domain,
        "family": family,
        "f_word": f_word,
        "g_word": g_word,
        "z_values": z_values,
        "codewords": codewords,
    }


def check_smooth_padding_toy(
    *,
    p: int,
    n: int,
    j: int,
    sigma: int,
    padding_size: int,
    unused_size: int,
) -> dict[str, Any]:
    native = build_fixed_jet_bad_line(p=p, n=n, j=j, sigma=sigma)
    domain = native["domain"]
    a_points = list(range(n, n + padding_size))
    r_points = list(range(n + padding_size, n + padding_size + unused_size))
    full_domain = domain + a_points + r_points
    if max(full_domain) >= p or len(set(full_domain)) != len(full_domain):
        raise AssertionError("bad toy padding domain")

    a_locator = poly_from_roots(a_points, p)
    lifted_dimension = native["dimension"] + padding_size
    lifted_agreement = native["agreement"] + padding_size

    lifted_g = []
    for x in full_domain:
        if x in domain:
            lifted_g.append(poly_eval(a_locator, x, p) * native["g_word"][x] % p)
        else:
            lifted_g.append(0)

    for subset in native["family"]:
        support = [x for x in domain if x not in set(subset)] + a_points
        support_indices = [full_domain.index(x) for x in support]
        support_values = [lifted_g[idx] for idx in support_indices]
        if exists_poly_degree_lt(support, support_values, lifted_dimension, p):
            raise AssertionError("lifted g is explained on padded support")

        native_poly = interpolate(domain, native["codewords"][subset], p)
        if degree(native_poly, p) >= native["dimension"]:
            raise AssertionError("native codeword has high degree")
        lifted_poly = poly_mul(a_locator, native_poly, p)
        if degree(lifted_poly, p) >= lifted_dimension:
            raise AssertionError("padded codeword has high degree")

    return {
        "p": p,
        "native_n": n,
        "native_dimension": native["dimension"],
        "native_agreement": native["agreement"],
        "padding_size": padding_size,
        "unused_size": unused_size,
        "lifted_n": len(full_domain),
        "lifted_dimension": lifted_dimension,
        "lifted_agreement": lifted_agreement,
        "bad_parameters_checked": native["distinct_bad_parameters"],
    }


def summarize_fixed_jet_toy(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "p": row["p"],
        "n": row["n"],
        "j": row["j"],
        "sigma": row["sigma"],
        "dimension": row["dimension"],
        "agreement": row["agreement"],
        "family_size": row["family_size"],
        "distinct_bad_parameters": row["distinct_bad_parameters"],
    }


def check_cycle84_public_audit() -> dict[str, Any]:
    text = PUBLIC_CYCLE84_AUDIT.read_text(encoding="utf-8")
    required = [
        "Occ(beta)               = 52,747,567,092",
        "D                       = 24",
        "double fibers           = 12",
        "m_max(beta)             = 2",
        "AUDIT / FINITE_MODEL_PROOF / PUBLIC_REPLAY",
    ]
    missing = [item for item in required if item not in text]
    if missing:
        raise AssertionError(f"Cycle84 public audit missing: {missing}")
    return {
        "path": str(PUBLIC_CYCLE84_AUDIT.relative_to(REPO_ROOT)),
        "finite_count": BAD_PARAMETER_COUNT,
        "status": "AUDIT / FINITE_MODEL_PROOF / PUBLIC_REPLAY",
        "required_markers": len(required),
    }


def build_report() -> dict[str, Any]:
    fixed_toys = [
        build_fixed_jet_bad_line(p=19, n=7, j=2, sigma=1),
        build_fixed_jet_bad_line(p=29, n=9, j=3, sigma=2),
    ]
    padding_toys = [
        check_smooth_padding_toy(
            p=31,
            n=8,
            j=2,
            sigma=1,
            padding_size=2,
            unused_size=1,
        ),
        check_smooth_padding_toy(
            p=37,
            n=9,
            j=3,
            sigma=2,
            padding_size=2,
            unused_size=2,
        ),
    ]
    cycle84_input = check_cycle84_public_audit()

    epsilon_den = 1 << EPSILON_DEN_BITS
    checks = {
        "cycle84_public_finite_input_recorded": (
            cycle84_input["finite_count"] == BAD_PARAMETER_COUNT
        ),
        "fixed_jet_toys_pass": all(row["distinct_bad_parameters"] >= 2 for row in fixed_toys),
        "smooth_padding_toys_pass": all(
            row["lifted_agreement"] == row["native_agreement"] + row["padding_size"]
            for row in padding_toys
        ),
        "cycle116_dimension_identity": (
            NATIVE_DIMENSION
            == NATIVE_DOMAIN_SIZE - NATIVE_COSUPPORT - FIXED_JET_SIGMA
        ),
        "cycle116_agreement_identity": (
            NATIVE_AGREEMENT == NATIVE_DOMAIN_SIZE - NATIVE_COSUPPORT
        ),
        "cycle120_padding_dimension_identity": (
            LIFT_DIMENSION == NATIVE_DIMENSION + PADDING_SIZE
        ),
        "cycle120_padding_agreement_identity": (
            LIFT_AGREEMENT == NATIVE_AGREEMENT + PADDING_SIZE
        ),
        "cycle120_domain_partition_identity": (
            LIFT_DOMAIN_SIZE == NATIVE_DOMAIN_SIZE + PADDING_SIZE + 137
        ),
        "abf_closed_threshold_262": ((256 - 125) * LIFT_DOMAIN_SIZE // 256 == 262),
        "density_exceeds_two_minus_128": BAD_PARAMETER_COUNT * epsilon_den > FIELD_SIZE,
        "floor_field_over_two_128_is_six": FIELD_SIZE // epsilon_den == 6,
    }
    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": "PROVED / COMPUTATION-DEPENDENT / SOURCE-CONDITIONAL",
        "theorem_problem_id": "M1 Cycle120 standalone LD_sw proof",
        "finite_input": cycle84_input,
        "proved_transfer_target": {
            "statement": "LD_sw(RS[F_17^32,H,256],262) >= 52747567092",
            "bad_parameters": BAD_PARAMETER_COUNT,
            "field_size": FIELD_SIZE,
            "domain_size": LIFT_DOMAIN_SIZE,
            "dimension": LIFT_DIMENSION,
            "agreement": LIFT_AGREEMENT,
        },
        "mca_consequence": {
            "statement": (
                "epsilon_mca(RS[F_17^32,H,256],125/256) "
                ">= 52747567092 / 17^32 > 2^-128"
            ),
            "minimum_bad_parameters_for_gate": FIELD_SIZE // epsilon_den + 1,
        },
        "fixed_jet_toys": [summarize_fixed_jet_toy(row) for row in fixed_toys],
        "smooth_padding_toys": padding_toys,
        "checks": checks,
        "remaining_inputs": [
            "reviewer acceptance of the Cycle84 finite computation",
            "official ABF source-gate verification",
            "Cycle116 slot identity and beta-not-in-domain certificates",
        ],
        "nonmutating": True,
    }


def print_human(report: dict[str, Any]) -> None:
    target = report["proved_transfer_target"]
    consequence = report["mca_consequence"]
    print("m1_cycle120_standalone_ldsw_proof: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(f"finite_input={report['finite_input']['status']}")
    print(f"target={target['statement']}")
    print(f"mca_consequence={consequence['statement']}")
    print(
        "density_gate_minimum_bad_parameters="
        f"{consequence['minimum_bad_parameters_for_gate']}"
    )
    print(
        "toy_checks="
        f"fixed_jet={len(report['fixed_jet_toys'])}, "
        f"smooth_padding={len(report['smooth_padding_toys'])}"
    )
    print("remaining_inputs=" + "; ".join(report["remaining_inputs"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the M1 Cycle120 standalone LD_sw proof."
    )
    parser.add_argument("--json", action="store_true", help="print JSON")
    args = parser.parse_args()

    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human(report)


if __name__ == "__main__":
    main()
