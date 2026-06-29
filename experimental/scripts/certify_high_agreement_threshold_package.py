#!/usr/bin/env python3
"""Certificate generator for the high-agreement threshold package.

This script verifies the exact integer arithmetic used to turn the promoted
high-agreement tangent staircase into the finite F_17^32 threshold row and the
row-independent compiler gate from towards-prize.md.

It does not reprove the tangent staircase. The proof input is the theorem
recorded in tex/slackMCA_v4.tex and experimental/notes/high_agreement/.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any


TARGET = 128
F17_Q = 17**32
F17_N = 512
F17_K = 256


def budget(denominator: int, target_bits: int = TARGET) -> int:
    return denominator // (1 << target_bits)


def radius_line_range(n: int, k: int) -> int:
    return (n - k) // 3


def exact_range_min_agreement(n: int, k: int) -> int:
    """Smallest integer a satisfying 3a - 2n >= k."""
    return (2 * n + k + 2) // 3


def frac_dict(value: Fraction) -> dict[str, int | str]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "display": f"{value.numerator}/{value.denominator}",
    }


def ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def bridge_probe(n: int, denominator: int, r: int, numerator: int) -> dict[str, Any]:
    """Check the closed-radius endpoint bridge for one grid radius."""
    delta = Fraction(r, n)
    agreement_from_floor = n - (delta.numerator * n // delta.denominator)
    agreement_from_ceil = ceil_fraction((1 - delta) * n)
    target_den = 1 << TARGET
    return {
        "r": r,
        "delta": frac_dict(delta),
        "agreement_from_closed_radius": agreement_from_floor,
        "agreement_from_ceil": agreement_from_ceil,
        "endpoint_formulas_agree": agreement_from_floor == agreement_from_ceil,
        "ld_sw_numerator": numerator,
        "epsilon_fraction": frac_dict(Fraction(numerator, denominator)),
        "safe_at_2^-128": numerator * target_den <= denominator,
        "unsafe_at_2^-128": numerator * target_den > denominator,
    }


def exact_threshold(
    n: int,
    k: int,
    denominator: int,
    target_bits: int = TARGET,
) -> dict[str, Any]:
    """Return exact finite-line threshold data if the compiler gate applies."""
    b = budget(denominator, target_bits)
    r_line = radius_line_range(n, k)
    applies = 1 <= b <= r_line
    if not applies:
        return {
            "applies": False,
            "budget": b,
            "line_exact_radius": r_line,
            "reason": "requires 1 <= floor(Q/2^lambda) <= floor((n-k)/3)",
        }

    first_unsafe_radius = b
    largest_safe_integer_radius = b - 1
    first_safe_agreement = n - largest_safe_integer_radius
    last_unsafe_agreement = n - first_unsafe_radius
    supremum = Fraction(first_unsafe_radius, n)

    safe_num = largest_safe_integer_radius + 1
    unsafe_num = first_unsafe_radius + 1
    two = 1 << target_bits

    checks = {
        "safe_grid_numerator_within_budget": safe_num <= b,
        "unsafe_grid_numerator_exceeds_budget": unsafe_num > b,
        "safe_probability_le_target": safe_num * two <= denominator,
        "unsafe_probability_gt_target": unsafe_num * two > denominator,
        "exact_agreement_inside_tangent_range": last_unsafe_agreement
        >= exact_range_min_agreement(n, k),
    }

    return {
        "applies": True,
        "budget": b,
        "line_exact_radius": r_line,
        "exact_range_min_agreement": exact_range_min_agreement(n, k),
        "largest_safe_integer_radius": largest_safe_integer_radius,
        "first_unsafe_integer_radius": first_unsafe_radius,
        "first_safe_agreement": first_safe_agreement,
        "last_unsafe_agreement": last_unsafe_agreement,
        "safe_line_numerator": safe_num,
        "unsafe_line_numerator": unsafe_num,
        "closed_real_safe_interval": {
            "left_closed": True,
            "right_open_supremum": frac_dict(supremum),
            "endpoint_attained": False,
        },
        "checks": checks,
    }


@dataclass(frozen=True)
class CompilerProbe:
    label: str
    n: int
    k: int
    denominator: int


def prize_rate_probes() -> list[CompilerProbe]:
    """Representative max-dimension prize-rate probes for common field sizes."""
    out: list[CompilerProbe] = []
    k = 1 << 40
    for rho_num, rho_den in [(1, 2), (1, 4), (1, 8), (1, 16)]:
        n = k * rho_den // rho_num
        for bits in [128, 160, 192, 256]:
            out.append(
                CompilerProbe(
                    label=f"rho={rho_num}/{rho_den}, k=2^40, Q=2^{bits}",
                    n=n,
                    k=k,
                    denominator=1 << bits,
                )
            )
    return out


def build_certificate() -> dict[str, Any]:
    finite = exact_threshold(F17_N, F17_K, F17_Q)
    projective = exact_threshold(F17_N, F17_K, F17_Q + 1)
    two = 1 << TARGET

    row_checks = {
        "floor_17_32_over_2_128_is_6": budget(F17_Q) == 6,
        "affine_budget_bracket": 6 * two < F17_Q < 7 * two,
        "projective_budget_same_as_affine": budget(F17_Q + 1) == budget(F17_Q),
        "projective_budget_bracket": 6 * two < F17_Q + 1 < 7 * two,
        "exact_line_range_radius_is_85": radius_line_range(F17_N, F17_K) == 85,
        "exact_range_min_agreement_is_427": exact_range_min_agreement(F17_N, F17_K)
        == 427,
        "affine_threshold_applies": bool(finite["applies"]),
        "projective_threshold_applies": bool(projective["applies"]),
    }

    compiler_examples = []
    for probe in prize_rate_probes():
        gate = exact_threshold(probe.n, probe.k, probe.denominator)
        compiler_examples.append(
            {
                "label": probe.label,
                "n": probe.n,
                "k": probe.k,
                "denominator": probe.denominator,
                "budget": budget(probe.denominator),
                "line_exact_radius": radius_line_range(probe.n, probe.k),
                "compiler_applies": bool(gate["applies"]),
                "first_unsafe_radius": gate.get("first_unsafe_integer_radius"),
                "largest_safe_integer_radius": gate.get("largest_safe_integer_radius"),
                "reason": gate.get("reason"),
            }
        )

    certificate = {
        "status": "PROVED-COMPILER-ARITHMETIC / AUDIT",
        "proof_input": {
            "theorem": "high-agreement tangent line staircase",
            "source": "tex/slackMCA_v4.tex, theorem B-high-agreement-line-staircase",
            "formula": "LD_sw(C,a)=r+1=n-a+1 when r=n-a <= floor((n-k)/3)",
            "nonclaim": (
                "this certificate does not prove lower-agreement M1, quotient "
                "floors, extension transfer, or L2"
            ),
        },
        "target": f"2^-{TARGET}",
        "row": {
            "code": "RS[F_17^32,H,256]",
            "n": F17_N,
            "k": F17_K,
            "rho": "1/2",
            "q_line": F17_Q,
            "q_projective": F17_Q + 1,
            "q_gen": F17_Q,
            "q_chal": F17_Q,
        },
        "definition_freeze": {
            "object": "finite-slope support-wise MCA / LD_sw",
            "bridge": "epsilon_mca(C,delta)=LD_sw(C,ceil((1-delta)n))/q_line",
            "agreement": "a=n-r",
            "closed_integer_radius": "r=n-a",
            "closed_real_radius_rule": "r(delta)=floor(delta*n)",
            "affine_denominator": "q_line=|F|",
            "projective_denominator": "|P^1(F)|=|F|+1",
            "endpoint": (
                "the supremal real transition radius is not attained when the "
                "first unsafe integer radius is reached"
            ),
        },
        "f17_512_affine": finite,
        "f17_512_projective": projective,
        "f17_512_endpoint_bridge": {
            "source": "experimental/notes/m2/m2_line_decoding_mca_bridge.md",
            "safe_endpoint": bridge_probe(
                F17_N,
                F17_Q,
                finite["largest_safe_integer_radius"],
                finite["safe_line_numerator"],
            ),
            "first_unsafe_endpoint": bridge_probe(
                F17_N,
                F17_Q,
                finite["first_unsafe_integer_radius"],
                finite["unsafe_line_numerator"],
            ),
        },
        "row_checks": row_checks,
        "row_independent_compiler": {
            "statement": (
                "if B_Q=floor(Q/2^128) and 1 <= B_Q <= floor((n-k)/3), "
                "then a single line/MCA/CA grid threshold is safe for "
                "r<=B_Q-1 and unsafe at r=B_Q"
            ),
            "examples": compiler_examples,
        },
    }

    all_checks = list(row_checks.values())
    all_checks.extend(finite.get("checks", {}).values())
    all_checks.extend(projective.get("checks", {}).values())
    all_checks.append(
        certificate["f17_512_endpoint_bridge"]["safe_endpoint"][
            "endpoint_formulas_agree"
        ]
    )
    all_checks.append(
        certificate["f17_512_endpoint_bridge"]["first_unsafe_endpoint"][
            "endpoint_formulas_agree"
        ]
    )
    all_checks.append(
        certificate["f17_512_endpoint_bridge"]["safe_endpoint"]["safe_at_2^-128"]
    )
    all_checks.append(
        certificate["f17_512_endpoint_bridge"]["first_unsafe_endpoint"][
            "unsafe_at_2^-128"
        ]
    )
    certificate["all_checks_passed"] = all(bool(x) for x in all_checks)
    return certificate


def normalized_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def check_certificate(path: Path) -> bool:
    expected = build_certificate()
    actual = json.loads(path.read_text())
    return actual == expected and bool(actual.get("all_checks_passed"))


def print_summary(cert: dict[str, Any]) -> None:
    row = cert["row"]
    aff = cert["f17_512_affine"]
    proj = cert["f17_512_projective"]
    print("High-agreement threshold package certificate")
    print(f"  row: {row['code']}, n={row['n']}, k={row['k']}, q_line={row['q_line']}")
    print(f"  target: {cert['target']}")
    print(f"  floor(q_line/2^128)={aff['budget']}")
    print(
        "  affine threshold: "
        f"safe r<={aff['largest_safe_integer_radius']}, "
        f"unsafe r={aff['first_unsafe_integer_radius']}, "
        f"safe a>={aff['first_safe_agreement']}"
    )
    print(
        "  real closed safe interval: "
        f"[0,{aff['closed_real_safe_interval']['right_open_supremum']['display']})"
    )
    print(f"  projective denominator budget={proj['budget']} (same threshold)")
    print(f"  row checks passed: {cert['all_checks_passed']}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic JSON certificate")
    parser.add_argument("--check", type=Path, help="check an existing certificate")
    parser.add_argument("--json", action="store_true", help="print JSON to stdout")
    args = parser.parse_args()

    if args.check:
        ok = check_certificate(args.check)
        print(f"{args.check}: {'PASS' if ok else 'FAIL'}")
        return 0 if ok else 1

    cert = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(normalized_json(cert))
        print(f"wrote {args.write}")

    if args.json:
        print(normalized_json(cert), end="")
    else:
        print_summary(cert)

    return 0 if cert["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
