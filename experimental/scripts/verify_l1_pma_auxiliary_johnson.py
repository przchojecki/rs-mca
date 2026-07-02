#!/usr/bin/env python3
"""Verify the PMA auxiliary-list reduction arithmetic.

The proof is in the companion note.  This verifier checks the exact parameter
translation from a fixed sunflower defect/background layer to an auxiliary
degree-d RS list on the petal domain, the Johnson-region inequality, and a
small finite-field replay of the reduction.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from itertools import product
from math import comb
from pathlib import Path
from typing import Any


OUTPUT = Path(
    "experimental/data/certificates/l1-pma-auxiliary-johnson/"
    "l1_pma_auxiliary_johnson.json"
)


@dataclass(frozen=True)
class AuxParams:
    sigma: int
    defect_d: int
    background_r: int
    petal_count_M: int

    @property
    def ell(self) -> int:
        return self.sigma + 1

    @property
    def petal_domain_size(self) -> int:
        return self.petal_count_M * self.ell

    @property
    def required_petal_agreement(self) -> int:
        return self.sigma + self.defect_d + 1 - self.background_r

    @property
    def effective_dimension(self) -> int:
        return self.defect_d + 1

    @property
    def johnson_denominator(self) -> int:
        return (
            self.required_petal_agreement * self.required_petal_agreement
            - self.petal_domain_size * self.defect_d
        )


def aux_payload(params: AuxParams) -> dict[str, Any]:
    den = params.johnson_denominator
    if den > 0:
        numerator = params.petal_domain_size * (
            params.petal_domain_size - params.defect_d
        )
        bound: dict[str, Any] | None = {
            "numerator": numerator,
            "denominator": den,
            "ceil_integer_bound": (numerator + den - 1) // den,
        }
    else:
        bound = None
    return {
        "sigma": params.sigma,
        "ell": params.ell,
        "defect_d": params.defect_d,
        "background_r": params.background_r,
        "petal_count_M": params.petal_count_M,
        "petal_domain_size": params.petal_domain_size,
        "required_petal_agreement_a": params.required_petal_agreement,
        "effective_auxiliary_dimension": params.effective_dimension,
        "johnson_condition": "a^2 > |T| d",
        "johnson_denominator": den,
        "johnson_region": den > 0,
        "johnson_bound": bound,
    }


def max_petal_count_in_johnson_region(sigma: int, defect_d: int, background_r: int) -> int | None:
    """Largest M for which the strict Johnson inequality is guaranteed."""
    ell = sigma + 1
    a = sigma + defect_d + 1 - background_r
    if a <= 0:
        return 0
    if defect_d == 0:
        return None
    return max(0, (a * a - 1) // (defect_d * ell))


def threshold_table() -> list[dict[str, Any]]:
    rows = []
    for sigma in [1, 2, 4, 8]:
        ell = sigma + 1
        for defect_d in [ell - 1, ell, 2 * ell]:
            if defect_d <= 0:
                continue
            for background_r in sorted({0, min(sigma, 1), sigma}):
                max_m = max_petal_count_in_johnson_region(
                    sigma, defect_d, background_r
                )
                rows.append({
                    "sigma": sigma,
                    "ell": ell,
                    "defect_d": defect_d,
                    "background_r": background_r,
                    "max_M_with_a2_gt_M_ell_d": max_m,
                    "first_failing_M": None if max_m is None else max_m + 1,
                })
    return rows


def poly_eval(coeffs: tuple[int, ...], x: int, p: int) -> int:
    acc = 0
    for coeff in reversed(coeffs):
        acc = (acc * x + coeff) % p
    return acc


def poly_mul(a: tuple[int, ...], b: tuple[int, ...], p: int) -> tuple[int, ...]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % p
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out)


def locator(points: list[int], p: int) -> tuple[int, ...]:
    out = (1,)
    for x in points:
        out = poly_mul(out, ((-x) % p, 1), p)
    return out


def toy_replay() -> dict[str, Any]:
    p = 11
    sigma = 1
    ell = sigma + 1
    petal_count = 3
    defect_d = 2
    background_r = 0
    C = list(range(5))
    D = C[:defect_d]
    C_retained = C[defect_d:]
    petals = [
        list(range(5 + ell * i, 5 + ell * (i + 1))) for i in range(petal_count)
    ]
    scalars = [1, 2, 3]
    params = AuxParams(sigma, defect_d, background_r, petal_count)
    L_D = locator(D, p)
    L_retained = locator(C_retained, p)

    target = []
    for scalar, petal in zip(scalars, petals):
        for x in petal:
            target.append((x, scalar * poly_eval(L_D, x, p) % p))

    auxiliary_hits = []
    original_replay_ok = True
    k = len(C) + 1
    s = k + sigma
    for coeffs in product(range(p), repeat=defect_d + 1):
        petal_hits = sum(poly_eval(coeffs, x, p) == y for x, y in target)
        if petal_hits < params.required_petal_agreement:
            continue
        P = poly_mul(L_retained, coeffs, p)
        core_hits = sum(poly_eval(P, x, p) == 0 for x in C_retained)
        original_replay_ok &= core_hits == len(C_retained)
        original_replay_ok &= core_hits + petal_hits >= s
        auxiliary_hits.append({
            "coefficients_low_to_high": list(coeffs),
            "petal_hits": petal_hits,
            "original_agreement_lower_bound": core_hits + petal_hits,
        })

    payload = aux_payload(params)
    bound = payload["johnson_bound"]
    assert bound is not None
    ok = (
        len(auxiliary_hits) <= bound["ceil_integer_bound"]
        and len(auxiliary_hits) == 1
        and original_replay_ok
    )
    return {
        "field": f"F_{p}",
        "core_size_k_minus_1": len(C),
        "defect_set_D": D,
        "petals": petals,
        "scalars": scalars,
        "params": payload,
        "auxiliary_hit_count": len(auxiliary_hits),
        "auxiliary_hits": auxiliary_hits,
        "original_replay_ok": original_replay_ok,
        "status": "PASS" if ok else "FAIL",
    }


def self_tests() -> None:
    p = AuxParams(sigma=2, defect_d=3, background_r=0, petal_count_M=3)
    assert p.ell == 3
    assert p.petal_domain_size == 9
    assert p.required_petal_agreement == 6
    assert p.johnson_denominator == 9
    assert max_petal_count_in_johnson_region(2, 3, 0) == 3
    assert max_petal_count_in_johnson_region(2, 3, 1) == 2
    assert toy_replay()["status"] == "PASS"


def build_certificate() -> dict[str, Any]:
    self_tests()
    sample_params = [
        AuxParams(2, 3, 0, 3),
        AuxParams(2, 3, 1, 3),
        AuxParams(4, 5, 0, 4),
        AuxParams(8, 9, 0, 8),
    ]
    return {
        "schema": "l1-pma-auxiliary-johnson-v1",
        "status": "PROVED_COMPILER__CITES_LEMMA_2_AND_THEOREM_J",
        "roadmap_tasks": ["pma_aux_list_reduction", "pma_johnson_regime"],
        "auxiliary_reduction": {
            "fixed_data": "defect set D with |D|=d and background set R0 with |R0|=r",
            "petal_target": "U_D(x)=c_i L_D(x) on petal T_i",
            "required_petal_agreement": "a = sigma + d + 1 - r",
            "injection": (
                "each fixed-D,R0 mixed-petal extra maps injectively to a "
                "degree<=d auxiliary polynomial W agreeing with U_D on at "
                "least a petal points and vanishing on R0"
            ),
            "upper_bound_relaxation": (
                "dropping the R0 vanishing and exact-missed-core constraints "
                "only enlarges the auxiliary list"
            ),
        },
        "johnson_regime": {
            "petal_domain_size": "|T| = M(sigma+1)",
            "effective_auxiliary_dimension": "d+1",
            "condition": "a^2 > |T| d",
            "bound": "|T|(|T|-d)/(a^2-|T|d)",
            "max_M_formula_for_d_positive": (
                "M <= floor((a^2-1)/(d(sigma+1)))"
            ),
        },
        "sample_parameter_rows": [aux_payload(p) for p in sample_params],
        "few_petal_threshold_table": threshold_table(),
        "toy_replay": toy_replay(),
        "non_claim": (
            "This does not prove mixed-petal amplification.  It isolates the "
            "few-petal Johnson-covered part and leaves the sub-Johnson "
            "auxiliary-list regime as the residual target."
        ),
    }


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def print_summary(cert: dict[str, Any]) -> None:
    print("l1 PMA auxiliary-Johnson certificate")
    print(f"  schema: {cert['schema']}")
    for row in cert["sample_parameter_rows"]:
        print(
            f"  sigma={row['sigma']} d={row['defect_d']} r={row['background_r']} "
            f"M={row['petal_count_M']} a={row['required_petal_agreement_a']} "
            f"johnson={row['johnson_region']}"
        )
    toy = cert["toy_replay"]
    print(
        f"  toy {toy['field']}: aux_hits={toy['auxiliary_hit_count']} "
        f"status={toy['status']}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {OUTPUT}")
    if args.check:
        actual = json.loads(args.check.read_text())
        assert_same(cert, actual)
        print(f"checked {args.check}")
    if not args.emit and not args.check:
        print_summary(cert)


if __name__ == "__main__":
    main()
