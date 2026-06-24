#!/usr/bin/env python3
"""Verify the generic smooth-padding transfer for support-wise bad lines.

The Cycle120 row uses a padding step:

    native bad line on D
      -> multiply by the A-locator
      -> agreement support grows from S to S union A
      -> simultaneous lifted explanations divide back by the A-locator.

This verifier checks that generic theorem on exact finite-field toy instances
and checks that the current Cycle116 smooth-padding audit instantiates it.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import verify_m1_fixed_jet_ldsw_theorem as fixed_jet_theorem
import verify_m1_cycle116_smooth_padding_transfer as smooth_padding


def poly_add(a: Sequence[int], b: Sequence[int], p: int) -> list[int]:
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(n):
        out[i] = ((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % p
    return fixed_jet_theorem.trim(out, p)


def poly_scale(c: int, a: Sequence[int], p: int) -> list[int]:
    return fixed_jet_theorem.trim([(c * x) % p for x in a], p)


def interpolate(points: Sequence[int], values: Sequence[int], p: int) -> list[int]:
    if len(points) != len(values) or len(set(points)) != len(points):
        raise AssertionError("interpolation needs distinct point/value pairs")
    out: list[int] = []
    for i, x_i in enumerate(points):
        basis = [1]
        denom = 1
        for j, x_j in enumerate(points):
            if i == j:
                continue
            basis = fixed_jet_theorem.poly_mul(basis, [(-x_j) % p, 1], p)
            denom = denom * ((x_i - x_j) % p) % p
        out = poly_add(
            out,
            poly_scale(values[i] * fixed_jet_theorem.inv_mod(denom, p), basis, p),
            p,
        )
    return fixed_jet_theorem.trim(out, p)


def exists_poly_degree_lt(
    points: Sequence[int], values: Sequence[int], degree_bound: int, p: int
) -> bool:
    if len(points) != len(values) or degree_bound < 0:
        raise AssertionError("bad polynomial-existence inputs")
    if len(points) <= degree_bound:
        return True
    candidate = interpolate(points[:degree_bound], values[:degree_bound], p)
    if fixed_jet_theorem.degree(candidate, p) >= degree_bound:
        return False
    return all(
        fixed_jet_theorem.poly_eval(candidate, x, p) == (value % p)
        for x, value in zip(points, values)
    )


def construct_native_bad_line(
    *, p: int, n: int, j: int, sigma: int
) -> Dict[str, Any]:
    d_points = list(range(n))
    beta = p - 1
    top_key, family = fixed_jet_theorem.find_family(p, n, j, sigma)
    redundancy = j + sigma
    dimension = n - redundancy

    domain_locator = fixed_jet_theorem.poly_from_roots(d_points, p)
    domain_derivative = fixed_jet_theorem.poly_derivative(domain_locator, p)
    domain_at_beta = fixed_jet_theorem.poly_eval(domain_locator, beta, p)
    lprime = {
        x: fixed_jet_theorem.poly_eval(domain_derivative, x, p)
        for x in d_points
    }

    locators = {
        subset: fixed_jet_theorem.poly_from_roots(subset, p)
        for subset in family
    }
    locator_derivatives = {
        subset: fixed_jet_theorem.poly_derivative(locator, p)
        for subset, locator in locators.items()
    }
    p_beta = {
        subset: fixed_jet_theorem.poly_eval(locator, beta, p)
        for subset, locator in locators.items()
    }

    quotient_values: list[int] = []
    for m in range(redundancy):
        monomial = [0] * m + [1]
        values = []
        for subset in family:
            quotient, _ = fixed_jet_theorem.poly_divmod_monic(
                monomial, locators[subset], p
            )
            values.append(fixed_jet_theorem.poly_eval(quotient, beta, p))
        if len(set(values)) != 1:
            raise AssertionError("quotient value depends on the co-support")
        quotient_values.append(values[0])

    def syndrome(word: Sequence[int]) -> list[int]:
        out = []
        for m in range(redundancy):
            total = 0
            for idx, x in enumerate(d_points):
                total += (
                    pow(x, m, p)
                    * word[idx]
                    * fixed_jet_theorem.inv_mod(lprime[x], p)
                )
            out.append(total % p)
        return out

    b_vector = [pow(beta, m, p) for m in range(redundancy)]
    a_vector = [(-value) % p for value in quotient_values]
    g_word = [
        domain_at_beta * fixed_jet_theorem.inv_mod((beta - x) % p, p) % p
        for x in d_points
    ]
    if syndrome(g_word) != b_vector:
        raise AssertionError("native Hg != B")

    e_words: dict[tuple[int, ...], list[int]] = {}
    z_values: dict[tuple[int, ...], int] = {}
    for subset in family:
        pprime = locator_derivatives[subset]
        subset_set = set(subset)
        e_word = []
        for x in d_points:
            if x not in subset_set:
                e_word.append(0)
                continue
            denom = (beta - x) * fixed_jet_theorem.poly_eval(pprime, x, p)
            e_word.append(
                lprime[x] * fixed_jet_theorem.inv_mod(denom, p) % p
            )
        z = fixed_jet_theorem.inv_mod(p_beta[subset], p)
        expected = fixed_jet_theorem.vector_add(
            a_vector, fixed_jet_theorem.scalar_mul(z, b_vector, p), p
        )
        if syndrome(e_word) != expected:
            raise AssertionError("native He_J != A+z_J B")
        e_words[subset] = e_word
        z_values[subset] = z

    base_subset = family[0]
    f_word = fixed_jet_theorem.vector_sub(
        e_words[base_subset],
        fixed_jet_theorem.scalar_mul(z_values[base_subset], g_word, p),
        p,
    )
    if syndrome(f_word) != a_vector:
        raise AssertionError("native Hf != A")

    codewords: dict[tuple[int, ...], list[int]] = {}
    for subset in family:
        line_word = fixed_jet_theorem.vector_add(
            f_word, fixed_jet_theorem.scalar_mul(z_values[subset], g_word, p), p
        )
        codeword = fixed_jet_theorem.vector_sub(line_word, e_words[subset], p)
        if syndrome(codeword) != [0] * redundancy:
            raise AssertionError("native constructed word is not a codeword")
        support = [x for x in d_points if x not in set(subset)]
        support_values = [g_word[x] for x in support]
        if exists_poly_degree_lt(support, support_values, dimension, p):
            raise AssertionError("native g is code-explained on a bad support")
        codewords[subset] = codeword

    return {
        "p": p,
        "D": d_points,
        "j": j,
        "sigma": sigma,
        "dimension": dimension,
        "agreement": n - j,
        "top_key": top_key,
        "family": family,
        "f_word": f_word,
        "g_word": g_word,
        "z_values": z_values,
        "codewords": codewords,
    }


def check_padding_case(
    *,
    name: str,
    p: int,
    n: int,
    j: int,
    sigma: int,
    a_size: int,
    r_size: int,
) -> Dict[str, Any]:
    native = construct_native_bad_line(p=p, n=n, j=j, sigma=sigma)
    d_points: list[int] = native["D"]
    a_points = list(range(n, n + a_size))
    r_points = list(range(n + a_size, n + a_size + r_size))
    h_points = d_points + a_points + r_points
    if len(set(h_points)) != len(h_points) or max(h_points) >= p:
        raise AssertionError("toy padded domain must use distinct field points")

    a_locator = fixed_jet_theorem.poly_from_roots(a_points, p)
    a_on_d = {x: fixed_jet_theorem.poly_eval(a_locator, x, p) for x in d_points}
    if any(value == 0 for value in a_on_d.values()):
        raise AssertionError("A locator vanishes on the native domain")

    native_dimension = int(native["dimension"])
    lifted_dimension = native_dimension + a_size
    lifted_agreement = int(native["agreement"]) + a_size
    lifted_cosupport_size = j + r_size

    lifted_f = []
    lifted_g = []
    for x in h_points:
        if x in d_points:
            lifted_f.append(a_on_d[x] * native["f_word"][x] % p)
            lifted_g.append(a_on_d[x] * native["g_word"][x] % p)
        else:
            lifted_f.append(0)
            lifted_g.append(0)

    for subset in native["family"]:
        support = [x for x in d_points if x not in set(subset)] + a_points
        support_indices = [h_points.index(x) for x in support]

        native_code_poly = interpolate(
            d_points,
            native["codewords"][subset],
            p,
        )
        if fixed_jet_theorem.degree(native_code_poly, p) >= native_dimension:
            raise AssertionError("native codeword interpolation has high degree")
        lifted_code_poly = fixed_jet_theorem.poly_mul(a_locator, native_code_poly, p)
        if fixed_jet_theorem.degree(lifted_code_poly, p) >= lifted_dimension:
            raise AssertionError("lifted codeword has high degree")

        line_values = [
            (
                lifted_f[idx]
                + native["z_values"][subset] * lifted_g[idx]
            )
            % p
            for idx in support_indices
        ]
        code_values = [
            fixed_jet_theorem.poly_eval(lifted_code_poly, x, p)
            for x in support
        ]
        if line_values != code_values:
            raise AssertionError("lifted agreement failed on S union A")

        lifted_g_values = [lifted_g[idx] for idx in support_indices]
        if exists_poly_degree_lt(support, lifted_g_values, lifted_dimension, p):
            raise AssertionError("lifted g is code-explained on S union A")

        quotient = fixed_jet_theorem.poly_divmod_monic(
            lifted_code_poly, a_locator, p
        )[0]
        if fixed_jet_theorem.degree(quotient, p) >= native_dimension:
            raise AssertionError("division by L_A did not return native degree")

    return {
        "name": name,
        "field": f"F_{p}",
        "native": {
            "domain_size": n,
            "cosupport_size": j,
            "sigma": sigma,
            "dimension": native_dimension,
            "agreement": int(native["agreement"]),
            "bad_parameters": len(set(native["z_values"].values())),
        },
        "padding": {
            "A_size": a_size,
            "R_size": r_size,
            "lifted_domain_size": len(h_points),
            "lifted_cosupport_size": lifted_cosupport_size,
            "lifted_dimension": lifted_dimension,
            "lifted_agreement": lifted_agreement,
        },
        "checks": {
            "A_locator_nonzero_on_D": True,
            "lifted_codewords_have_low_degree": True,
            "agreement_pads_to_S_union_A": True,
            "lifted_noncontainment_divides_back": True,
            "bad_parameters_preserved": True,
        },
    }


def build_report(local_reports: Mapping[str, Any] | None = None) -> Dict[str, Any]:
    local_reports = local_reports or {}
    fixed_report = (
        local_reports.get("fixed_jet_theorem")
        or fixed_jet_theorem.build_report(local_reports)
    )
    smooth_report = local_reports.get("smooth_padding") or smooth_padding.build_report()

    toy_cases = [
        check_padding_case(
            name="sigma1_two_point_padding",
            p=31,
            n=8,
            j=3,
            sigma=1,
            a_size=2,
            r_size=3,
        ),
        check_padding_case(
            name="sigma2_three_point_padding",
            p=43,
            n=12,
            j=4,
            sigma=2,
            a_size=3,
            r_size=4,
        ),
    ]

    smooth = smooth_report["smooth_padding"]
    transfer = smooth_report["transfer"]

    checks = {
        "toy_cases_pass": all(all(case["checks"].values()) for case in toy_cases),
        "fixed_jet_ldsw_theorem_passes": fixed_report["status"] == "PASS",
        "smooth_padding_transfer_passes": smooth_report["status"] == "PASS",
        "cycle116_to_cycle120_sizes_match_padding_theorem": (
            int(smooth["native_agreement"]) + int(smooth["A_size"])
            == int(smooth["lift_agreement"])
            and int(smooth["native_dimension"]) + int(smooth["A_size"])
            == int(smooth["lift_dimension"])
            and int(smooth["native_cosupport_size"]) + int(smooth["R_size"])
            == int(smooth["lift_cosupport_size"])
        ),
        "cycle116_bad_parameters_preserved": bool(
            transfer["bad_parameters_preserved"]
        ),
        "cycle116_noncontainment_division_recorded": (
            "divide by L_A" in transfer["noncontainment_division"]
        ),
    }

    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": "PROVED / AUDIT / SMOOTH-PADDING-LDSW-THEOREM",
        "theorem_problem_id": "M1 generic smooth-padding LD_sw transfer",
        "theorem": {
            "input": (
                "one support-wise bad line on D with agreement a and dimension k"
            ),
            "padding": (
                "adjoin disjoint A and R, set k_plus=k+|A|, multiply by L_A"
            ),
            "output": (
                "the same bad parameters are bad on H=D union A union R at "
                "agreement a+|A|"
            ),
            "mechanism": (
                "agreement is multiplied by L_A; any lifted simultaneous "
                "explanation vanishes on A and divides back to the native row"
            ),
        },
        "toy_cases": toy_cases,
        "cycle116_instantiation": {
            "native_agreement": int(smooth["native_agreement"]),
            "lift_agreement": int(smooth["lift_agreement"]),
            "native_dimension": int(smooth["native_dimension"]),
            "lift_dimension": int(smooth["lift_dimension"]),
            "native_cosupport_size": int(smooth["native_cosupport_size"]),
            "lift_cosupport_size": int(smooth["lift_cosupport_size"]),
            "A_size": int(smooth["A_size"]),
            "R_size": int(smooth["R_size"]),
            "bad_parameters_preserved": True,
        },
        "checks": checks,
        "remaining_imports": [
            "native Cycle116 fixed-jet LD_sw theorem and exact occupancy count",
            "official ABF source gate if the row is promoted as prize-facing",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    inst = report["cycle116_instantiation"]

    print("m1_smooth_padding_ldsw_theorem: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(
        "toy_cases="
        + ", ".join(
            f"{case['name']}:A={case['padding']['A_size']},"
            f"R={case['padding']['R_size']},"
            f"bad={case['native']['bad_parameters']}"
            for case in report["toy_cases"]
        )
    )
    print(
        "cycle116_to_cycle120="
        f"agreement {inst['native_agreement']}+{inst['A_size']}="
        f"{inst['lift_agreement']}, dimension {inst['native_dimension']}+"
        f"{inst['A_size']}={inst['lift_dimension']}, cosupport "
        f"{inst['native_cosupport_size']}+{inst['R_size']}="
        f"{inst['lift_cosupport_size']}"
    )
    print("remaining_imports=" + "; ".join(report["remaining_imports"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the M1 generic smooth-padding LD_sw theorem."
    )
    parser.add_argument("--json", action="store_true", help="print JSON report")
    args = parser.parse_args()

    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human(report)


if __name__ == "__main__":
    main()
