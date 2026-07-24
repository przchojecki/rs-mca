#!/usr/bin/env python3
"""Exact verifier for the M31 one-error root-lift census stop packet.

The verifier is self-contained.  It checks no steering file and does not read
PR_BODY.md or an agents-log entry.  All verdict-bearing comparisons are exact
integer computations; the F_37 counterexample is exhaustively enumerated.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any, Callable

SCHEMA = "m31-rootlift-bridge-stop-v1"
CERT_REL = Path(
    "experimental/data/certificates/m31-rootlift-bridge/"
    "m31_rootlift_bridge_stop.json"
)


class VerificationError(RuntimeError):
    """Raised when an exact certificate gate fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def row_arithmetic() -> dict[str, Any]:
    p = 2**31 - 1
    q_route_1 = p**4
    q_route_2 = 2**124 - 4 * 2**93 + 6 * 2**62 - 4 * 2**31 + 1
    require(q_route_1 == q_route_2, "field-size routes disagree")
    q = q_route_1

    n = 2**21
    k = 2**20
    agreement = 1_116_023
    errors = n - agreement
    w = agreement - k
    budget, budget_remainder = divmod(q, 2**100)
    require(budget == 2**24 - 1, "budget mismatch")

    root_count = 32
    fibre_size, domain_remainder = divmod(n, root_count)
    require(domain_remainder == 0, "root-count does not divide n")
    quotient_full_fibres, remainder = divmod(agreement, fibre_size)
    require(quotient_full_fibres == 17, "agreement quotient mismatch")
    require(remainder == 1_911, "agreement remainder mismatch")
    require(w == fibre_size + remainder, "w=c+r mismatch")

    multiplier, multiplier_remainder = divmod(budget + 1, n)
    require(multiplier == 8 and multiplier_remainder == 0, "8n budget identity")

    baseline = multiplier * (remainder + 1)
    offset = root_count * baseline - 1
    require(baseline == 15_296, "baseline mismatch")
    require(offset == 489_471, "offset mismatch")

    def reported_count(partner_size: int) -> int:
        return root_count * partner_size - offset

    low = 539_583
    high = low + 1
    low_count = reported_count(low)
    high_count = reported_count(high)
    max_partner, division_remainder = divmod(budget + offset, root_count)
    require(max_partner == low, "maximal partner input mismatch")
    require(division_remainder == 30, "closure slack mismatch")
    require(low_count == budget - 30, "low endpoint mismatch")
    require(high_count == budget + 2, "high endpoint mismatch")

    partner_threshold_route_1 = multiplier * (w + 1) - 1
    partner_threshold_route_2 = (budget + offset) // root_count
    require(
        partner_threshold_route_1 == partner_threshold_route_2 == low,
        "partner threshold routes disagree",
    )
    require(
        high == baseline + 2**19,
        "baseline plus half-domain decomposition mismatch",
    )

    crude_rooted_max, crude_rooted_remainder = divmod(budget, root_count)
    require(crude_rooted_max == 524_287, "crude rooted bound mismatch")
    require(crude_rooted_remainder == 31, "crude rooted remainder mismatch")
    require(root_count * crude_rooted_max == budget - 31, "crude low mismatch")
    require(
        root_count * (crude_rooted_max + 1) == budget + 1,
        "crude high mismatch",
    )

    return {
        "p": p,
        "q": q,
        "n": n,
        "k": k,
        "agreement": agreement,
        "errors": errors,
        "w": w,
        "B_star": budget,
        "B_star_remainder_mod_2^100": budget_remainder,
        "root_count": root_count,
        "fibre_size": fibre_size,
        "agreement_full_fibres": quotient_full_fibres,
        "agreement_remainder": remainder,
        "budget_multiplier": multiplier,
        "baseline": baseline,
        "offset": offset,
        "partner_low": low,
        "partner_high": high,
        "count_low": low_count,
        "count_high": high_count,
        "slack_at_low": budget - low_count,
        "excess_at_high": high_count - budget,
        "max_partner_by_floor": max_partner,
        "floor_remainder": division_remainder,
        "crude_rooted_max_without_overlap_credit": crude_rooted_max,
        "crude_rooted_low_count": root_count * crude_rooted_max,
        "crude_rooted_high_count": root_count * (crude_rooted_max + 1),
        "uniform_common_core_divisor": 31,
        "uniform_common_core_quotient": offset // 31,
        "uniform_common_core_remainder": offset % 31,
    }


def inv_mod(value: int, p: int) -> int:
    value %= p
    require(value != 0, "attempted inversion of zero")
    return pow(value, p - 2, p)


def eval_affine(poly: tuple[int, int], x: int, p: int) -> int:
    intercept, slope = poly
    return (intercept + slope * x) % p


def target_list(
    *,
    p: int,
    domain: tuple[int, ...],
    word: dict[int, int],
    agreement: int,
) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for intercept in range(p):
        for slope in range(p):
            poly = (intercept, slope)
            matches = sum(
                eval_affine(poly, x, p) == word[x] for x in domain
            )
            if matches >= agreement:
                out.append(poly)
    return out


def partner_list(
    *,
    p: int,
    domain: tuple[int, ...],
    word: dict[int, int],
    alpha: int,
    agreement: int,
) -> list[int]:
    received = {
        x: word[x] * inv_mod(x - alpha, p) % p
        for x in domain
        if x != alpha
    }
    out: list[int] = []
    for constant in range(p):
        matches = sum(constant == received[x] for x in received)
        if matches >= agreement:
            out.append(constant)
    return out


def lift_constant(*, p: int, alpha: int, constant: int) -> tuple[int, int]:
    # (X-alpha)*constant = -alpha*constant + constant*X.
    return ((-alpha * constant) % p, constant % p)


def finite_counterexample() -> dict[str, Any]:
    p = 37
    domain = tuple(range(37))
    roots = tuple(range(32))
    outside = tuple(range(32, 37))
    agreement = 2
    partner_agreement = agreement - 1

    words = {
        "A": (0, 0, 0, 1, 2),
        "B": (0, 0, 0, 1, 1),
    }
    expected = {
        "A": {"target": 70, "free": 5},
        "B": {"target": 72, "free": 7},
    }
    results: dict[str, Any] = {}

    for label, outside_values in words.items():
        word = {x: 0 for x in roots}
        word.update(dict(zip(outside, outside_values, strict=True)))

        target = target_list(
            p=p, domain=domain, word=word, agreement=agreement
        )
        target_set = set(target)

        partner_sizes: list[int] = []
        slices: list[set[tuple[int, int]]] = []
        for alpha in roots:
            partner = partner_list(
                p=p,
                domain=domain,
                word=word,
                alpha=alpha,
                agreement=partner_agreement,
            )
            partner_sizes.append(len(partner))
            lifted = {
                lift_constant(p=p, alpha=alpha, constant=constant)
                for constant in partner
            }
            require(
                lifted <= target_set,
                f"root-lift image not contained in target list ({label})",
            )
            require(
                len(lifted) == len(partner),
                f"root lift not injective ({label})",
            )
            slices.append(lifted)

        require(
            partner_sizes == [3] * 32,
            f"partner sizes not uniformly three ({label})",
        )

        rooted_union = set().union(*slices)
        multiplicities = {
            poly: sum(poly in root_slice for root_slice in slices)
            for poly in rooted_union
        }
        overlap_excess = sum(value - 1 for value in multiplicities.values())
        free_residue = target_set - rooted_union
        multiplicity_histogram: dict[str, int] = {}
        for value in multiplicities.values():
            key = str(value)
            multiplicity_histogram[key] = multiplicity_histogram.get(key, 0) + 1

        require(len(rooted_union) == 65, f"rooted union mismatch ({label})")
        require(overlap_excess == 31, f"overlap mismatch ({label})")
        require(
            len(free_residue) == expected[label]["free"],
            f"free residue mismatch ({label})",
        )
        require(
            len(target) == expected[label]["target"],
            f"target count mismatch ({label})",
        )
        require(
            len(target)
            == sum(partner_sizes) + len(free_residue) - overlap_excess,
            f"correct census identity failed ({label})",
        )

        results[label] = {
            "outside_values_at_32_36": list(outside_values),
            "uniform_partner_size": 3,
            "sum_partner_sizes": sum(partner_sizes),
            "rooted_union_size": len(rooted_union),
            "overlap_excess": overlap_excess,
            "free_residue": len(free_residue),
            "target_list_size": len(target),
            "multiplicity_histogram": multiplicity_histogram,
        }

    require(
        results["A"]["uniform_partner_size"]
        == results["B"]["uniform_partner_size"],
        "counterexample partner sizes differ",
    )
    require(
        results["A"]["target_list_size"] != results["B"]["target_list_size"],
        "counterexample target sizes do not differ",
    )

    # Cross-root images are not automatically disjoint:
    # X*(X-1) = (X-1)*X over every field.
    alpha = 0
    beta = 1
    f = (p - 1, 1)  # X-1
    g = (0, 1)      # X
    lift_alpha = (
        (-alpha * f[0]) % p,
        (f[0] - alpha * f[1]) % p,
        f[1] % p,
    )
    lift_beta = (
        (-beta * g[0]) % p,
        (g[0] - beta * g[1]) % p,
        g[1] % p,
    )
    require(lift_alpha == lift_beta == (0, 36, 1), "collision witness failed")

    return {
        "field": 37,
        "domain_size": 37,
        "target_dimension": 2,
        "target_agreement": 2,
        "target_errors": 35,
        "selected_roots": 32,
        "partner_dimension": 1,
        "partner_length": 36,
        "partner_agreement": 1,
        "partner_errors": 35,
        "partner_radius": "35/36",
        "words": results,
        "cross_root_collision": {
            "alpha": alpha,
            "beta": beta,
            "f_coefficients": list(f),
            "g_coefficients": list(g),
            "common_lift_coefficients": list(lift_alpha),
        },
    }


def expected_sections() -> dict[str, Any]:
    return {
        "row_arithmetic": row_arithmetic(),
        "finite_rs_counterexample": finite_counterexample(),
        "correct_census": {
            "general_law": (
                "N=sum_alpha L_alpha+F-Omega, where F is the unrooted "
                "free residue and Omega=sum_(g in rooted union)(m(g)-1)"
            ),
            "uniform_law": "N=32*L+F-Omega",
            "reported_affine_specialization": "Omega-F=489471",
            "one_anchor_specialization": "F=1 and Omega=489472=32*15296",
            "status": "PROVED_IDENTITY_SPECIALIZATION_UNPROVED",
        },
        "partner_object": {
            "target_code": "C=RS_F(D,K), degree<K, length n",
            "normalization": (
                "choose A subset D with |A|=32 and h in C with h|A=U|A; "
                "replace U by U-h"
            ),
            "normalization_interpolant_degree_bound": 32,
            "selected_roots": 32,
            "partner_domain": "D_alpha=D\\{alpha}, length n-1",
            "partner_code": "C^-_alpha=RS_F(D_alpha,K-1), degree<K-1",
            "deployed_partner_length": 2097151,
            "deployed_partner_dimension": 1048575,
            "partner_received_word": "V_alpha(x)=U(x)/(x-alpha)",
            "partner_agreement": "a-1",
            "deployed_partner_agreement": 1116022,
            "partner_errors": "R=(n-1)-(a-1)=n-a",
            "deployed_partner_errors": 981129,
            "partner_radius": "R/(n-1)",
            "deployed_partner_radius_num": 981129,
            "deployed_partner_radius_den": 2097151,
            "lift_map": "lambda_alpha(f)=((X-alpha)f)|D",
            "exact_bijection": (
                "P_alpha bijects with target-list codewords whose normalized "
                "polynomial vanishes at alpha"
            ),
        },
    }


def compare_exact(actual: Any, expected: Any, path: str) -> None:
    if isinstance(expected, dict):
        require(isinstance(actual, dict), f"{path} must be an object")
        require(set(actual) == set(expected), f"{path} keys differ")
        for key, value in expected.items():
            compare_exact(actual[key], value, f"{path}.{key}")
    else:
        require(actual == expected, f"{path} mismatch")


def validate_certificate(data: dict[str, Any]) -> None:
    require(data.get("schema") == SCHEMA, "schema mismatch")
    for section, expected in expected_sections().items():
        compare_exact(data.get(section), expected, section)

    require(data.get("object") == "LIST", "object must remain LIST")
    require(data.get("architecture") == "DIRECT", "architecture mismatch")
    require(
        data.get("terminal_verdict")
        == (
            "CERTIFIED STOP: the natural one-error root lift has an exact "
            "free-residue/overlap census, but no source proves "
            "Omega-F=489471, equality of the 32 partner lists on the "
            "deployed row, or whole-ball exhaustivity; partner-list size "
            "alone cannot yield the reported affine count law"
        ),
        "terminal verdict mismatch",
    )
    provenance = data.get("provenance")
    require(isinstance(provenance, dict), "provenance missing")
    require(
        provenance.get("steering_files_are_gating_pins") is False,
        "steering files must be provenance only",
    )
    require(
        data.get("routes_killed")
        == [
            "EXACT_NUMBER_AND_HISTORY_SEARCH",
            "TWO_ENDPOINT_AFFINE_INTERPOLATION",
            "ORDER32_QUOTIENT_FIBRE_INTERPRETATION",
            "PUNCTURE_ONLY_ONE_ERROR_BOUND",
            "MULTIPLICATION_BY_ROOT_DISJOINT_UNION",
            "UNIFORM_COMMON_CORE_SUBTRACTION",
            "FIXED_G_ORDINARY_RS_EMBEDDING",
            "CS25_SAME_CODE_CONTAINMENT",
            "CS25_LITERAL_C_MINUS_PARTNER",
            "WHOLE_BALL_BOUNDARY_OR_FROZEN_FACE",
            "PARTNER_SIZE_ONLY_CLOSURE",
        ],
        "routes-killed inventory mismatch",
    )


def load_canonical(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    require(raw == canonical_json(data), "certificate JSON is not canonical")
    return data


def run_check(cert_path: Path) -> None:
    data = load_canonical(cert_path)
    validate_certificate(data)
    print("PASS deployed M31 row and two-route field arithmetic")
    print("PASS recovered affine endpoint arithmetic and exact boundary")
    print("PASS natural punctured RS(K-1) one-error partner definition")
    print("PASS exact N=sum L_alpha+F-Omega census identity")
    print("PASS exhaustive F_37 32-root counterexample")
    print("PASS cross-root multiplication collision witness")
    print("PASS CS25/fixed-G/order-32 route separation")
    print("PASS certified-stop verdict and routes-killed inventory")


def set_path(data: dict[str, Any], path: tuple[str, ...], value: Any) -> None:
    cursor: Any = data
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value


def run_tamper_selftest(cert_path: Path) -> None:
    pristine = load_canonical(cert_path)
    validate_certificate(pristine)
    mutations = [
        ("B_star", ("row_arithmetic", "B_star"), 16_777_216),
        ("offset", ("row_arithmetic", "offset"), 489_472),
        ("partner threshold", ("row_arithmetic", "partner_low"), 539_584),
        ("low slack", ("row_arithmetic", "slack_at_low"), 31),
        (
            "word A target",
            ("finite_rs_counterexample", "words", "A", "target_list_size"),
            71,
        ),
        (
            "word B free residue",
            ("finite_rs_counterexample", "words", "B", "free_residue"),
            6,
        ),
        (
            "census specialization",
            ("correct_census", "reported_affine_specialization"),
            "Omega-F=489472",
        ),
        (
            "steering gate",
            ("provenance", "steering_files_are_gating_pins"),
            True,
        ),
    ]
    for label, path, value in mutations:
        mutated = copy.deepcopy(pristine)
        set_path(mutated, path, value)
        try:
            validate_certificate(mutated)
        except VerificationError:
            print(f"PASS tamper rejected: {label}")
        else:
            raise VerificationError(f"tamper accepted: {label}")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--certificate", type=Path, default=None)
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    cert_path = (
        args.certificate.resolve()
        if args.certificate is not None
        else repo_root / CERT_REL
    )
    try:
        if args.check:
            run_check(cert_path)
        else:
            run_tamper_selftest(cert_path)
    except (OSError, ValueError, VerificationError) as exc:
        print(f"FAIL: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
