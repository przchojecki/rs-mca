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
import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any


TARGET = 128
F17_Q = 17**32
F17_N = 512
F17_K = 256
OPEN_PROXIMITY = Path("open-proximity.tex")
SCANNER_CONFIG = Path(
    "experimental/notes/certificate_scanner/examples/f17_512_mca_only.json"
)
SCANNER_JSON = Path(
    "experimental/notes/certificate_scanner/outputs/f17_512_mca_only.report.json"
)
SCANNER_MD = Path(
    "experimental/notes/certificate_scanner/outputs/f17_512_mca_only.report.md"
)
PROTOCOL_SCANNER_CONFIG = Path(
    "experimental/notes/certificate_scanner/examples/f17_512.json"
)
PROTOCOL_SCANNER_JSON = Path(
    "experimental/notes/certificate_scanner/outputs/f17_512.report.json"
)
PROTOCOL_SCANNER_MD = Path(
    "experimental/notes/certificate_scanner/outputs/f17_512.report.md"
)


def parse_int(text: str) -> int:
    clean = text.strip().replace(" ", "")
    if "^" in clean:
        base, exp = clean.split("^", 1)
        return int(base) ** int(exp)
    if "**" in clean:
        base, exp = clean.split("**", 1)
        return int(base) ** int(exp)
    return int(clean, 10)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_anchor(path: Path, label: str, needle: str) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines, start=1):
        if needle in line:
            return {"label": label, "line": index, "needle": needle}
    raise ValueError(f"missing source anchor {label!r}: {needle!r}")


def source_audit() -> dict[str, Any]:
    data = OPEN_PROXIMITY.read_bytes()
    anchors = [
        source_anchor(
            OPEN_PROXIMITY,
            "support_set_agreement_size",
            r"\abs{S}\ge (1-\delta)n",
        ),
        source_anchor(
            OPEN_PROXIMITY,
            "line_family",
            r"\calF_{\mathrm{lines}}",
        ),
        source_anchor(
            OPEN_PROXIMITY,
            "grand_challenge_rates",
            r"\rho(C):=\frac{k}{\abs{L}}\in\set{\frac12,\frac14,\frac18,\frac1{16}}",
        ),
        source_anchor(
            OPEN_PROXIMITY,
            "grand_challenge_field_range",
            r"\abs{\F}<2^{256}",
        ),
        source_anchor(
            OPEN_PROXIMITY,
            "mca_error_definition",
            r"\epsmca(C,\delta):=\max_{f_1,f_2\in(\F^s)^n}",
        ),
        source_anchor(
            OPEN_PROXIMITY,
            "support_wise_exists_same_support",
            r"\exists S=S_\gamma\subseteq[n]",
        ),
        source_anchor(
            OPEN_PROXIMITY,
            "support_wise_noncontainment",
            r"\Delta_S((f_1,f_2),C^{\equiv2})>0",
        ),
        source_anchor(
            OPEN_PROXIMITY,
            "line_decoding_to_mca_denominator",
            r"\epsmca(C,\delta)\le \frac{a}{\abs{\F}}",
        ),
    ]
    return {
        "path": str(OPEN_PROXIMITY),
        "sha256": hashlib.sha256(data).hexdigest(),
        "anchors": anchors,
        "checks": {
            "source_present": OPEN_PROXIMITY.exists(),
            "all_anchors_found": len(anchors) == 8,
        },
    }


def scanner_replay_audit() -> dict[str, Any]:
    """Audit the committed pure-MCA scanner output against the threshold rows."""
    cfg = json.loads(SCANNER_CONFIG.read_text())
    report = json.loads(SCANNER_JSON.read_text())
    scans = {scan["a"]: scan for scan in report["scans"]}
    expected_rows = {
        506: {
            "r": 6,
            "numerator": 7,
            "safe": False,
            "unsafe": True,
            "verdict": "UNSAFE_BY_PROVED_LOWER_BOUND",
        },
        507: {
            "r": 5,
            "numerator": 6,
            "safe": True,
            "unsafe": False,
            "verdict": "SAFE_BY_PROVED_UPPER_BOUND",
        },
        508: {
            "r": 4,
            "numerator": 5,
            "safe": True,
            "unsafe": False,
            "verdict": "SAFE_BY_PROVED_UPPER_BOUND",
        },
        512: {
            "r": 0,
            "numerator": 1,
            "safe": True,
            "unsafe": False,
            "verdict": "SAFE_BY_PROVED_UPPER_BOUND",
        },
    }

    row_checks = {
        "config_is_pure_mca": (
            cfg["protocol"].get("include_line_term") is True
            and cfg["protocol"].get("include_interleaved_list_term") is False
            and cfg["protocol"].get("curve_degrees") == []
            and cfg["protocol"].get("line_sampler") == "finite"
        ),
        "config_target_is_128": int(cfg["security"]["lambda"]) == TARGET,
        "config_row_matches_f17": int(cfg["row"]["n"]) == F17_N
        and int(cfg["row"]["k"]) == F17_K,
        "report_row_matches_f17": (
            report["row"]["n"] == F17_N
            and report["row"]["k"] == F17_K
            and report["row"]["q_gen"] == F17_Q
            and report["row"]["q_line"] == F17_Q
            and report["row"]["q_chal"] == F17_Q
        ),
        "report_budget_is_6": report["row"]["budget_q_line"] == 6 and report["row"]["budget_q_chal"] == 6,
    }

    replay_rows: dict[str, Any] = {}
    for a, expected in expected_rows.items():
        scan = scans.get(a)
        if scan is None:
            replay_rows[str(a)] = {"present": False, "checks": {"present": False}}
            continue
        exact = scan["ledgers"]["tangent_high_agreement"]["finite_line_exact"]
        combined = scan["combined_protocol"]
        checks = {
            "present": True,
            "r_matches": scan["r"] == expected["r"],
            "sigma_matches": scan["sigma"] == a - F17_K,
            "exact_numerator_matches": exact["numerator"] == expected["numerator"],
            "denominator_matches": exact["denominator"] == F17_Q,
            "safe_flag_matches": exact["safe_at_target"] is expected["safe"],
            "unsafe_flag_matches": exact["unsafe_at_target"] is expected["unsafe"],
            "combined_verdict_matches": combined["verdict"] == expected["verdict"],
            "combined_has_no_unknown_terms": combined["unknown_terms"] == [],
        }
        replay_rows[str(a)] = {
            "r": scan["r"],
            "sigma": scan["sigma"],
            "finite_line_numerator": exact["numerator"],
            "safe_at_target": exact["safe_at_target"],
            "unsafe_at_target": exact["unsafe_at_target"],
            "combined_verdict": combined["verdict"],
            "checks": checks,
        }

    all_row_checks = [
        value for row in replay_rows.values() for value in row["checks"].values()
    ]
    return {
        "status": "AUDIT",
        "purpose": "replay committed pure finite-slope MCA scanner output at the threshold rows",
        "scanner_config": {
            "path": str(SCANNER_CONFIG),
            "sha256": sha256_file(SCANNER_CONFIG),
        },
        "scanner_json_report": {
            "path": str(SCANNER_JSON),
            "sha256": sha256_file(SCANNER_JSON),
        },
        "scanner_markdown_report": {
            "path": str(SCANNER_MD),
            "sha256": sha256_file(SCANNER_MD),
        },
        "row_checks": row_checks,
        "threshold_rows": replay_rows,
        "checks": {
            "row_and_protocol_checks_passed": all(row_checks.values()),
            "threshold_row_checks_passed": all(all_row_checks),
        },
    }


def protocol_scanner_replay_audit() -> dict[str, Any]:
    """Audit the committed line-plus-one-list scanner output at the threshold."""
    cfg = json.loads(PROTOCOL_SCANNER_CONFIG.read_text())
    report = json.loads(PROTOCOL_SCANNER_JSON.read_text())
    scans = {scan["a"]: scan for scan in report["scans"]}
    expected_rows = {
        507: {
            "r": 5,
            "line_numerator": 6,
            "list_numerator": 1,
            "total_numerator": 7,
            "verdict": "UNSAFE_BY_PROVED_LOWER_BOUND",
        },
        508: {
            "r": 4,
            "line_numerator": 5,
            "list_numerator": 1,
            "total_numerator": 6,
            "verdict": "SAFE_BY_PROVED_UPPER_BOUND",
        },
    }

    row_checks = {
        "config_is_line_plus_one_list": (
            cfg["protocol"].get("include_line_term") is True
            and cfg["protocol"].get("include_interleaved_list_term") is True
            and int(cfg["protocol"].get("implementation_interleaving_nu")) == 1
            and cfg["protocol"].get("curve_degrees") == []
            and cfg["protocol"].get("line_sampler") == "finite"
        ),
        "config_target_is_128": int(cfg["security"]["lambda"]) == TARGET,
        "config_row_matches_f17": int(cfg["row"]["n"]) == F17_N
        and int(cfg["row"]["k"]) == F17_K,
        "report_row_matches_f17": (
            report["row"]["n"] == F17_N
            and report["row"]["k"] == F17_K
            and report["row"]["q_gen"] == F17_Q
            and report["row"]["q_line"] == F17_Q
            and report["row"]["q_chal"] == F17_Q
        ),
        "report_budget_is_6": report["row"]["budget_q_line"] == 6
        and report["row"]["budget_q_chal"] == 6,
    }

    replay_rows: dict[str, Any] = {}
    for a, expected in expected_rows.items():
        scan = scans.get(a)
        if scan is None:
            replay_rows[str(a)] = {"present": False, "checks": {"present": False}}
            continue
        terms = {
            item["name"]: item
            for item in scan["combined_protocol"]["terms_upper"]
        }
        line = terms.get("finite_line_exact", {})
        list_term = terms.get("interleaved_list_unique", {})
        total = line.get("numerator", 0) + list_term.get("numerator", 0)
        checks = {
            "present": True,
            "r_matches": scan["r"] == expected["r"],
            "sigma_matches": scan["sigma"] == a - F17_K,
            "line_numerator_matches": line.get("numerator")
            == expected["line_numerator"],
            "list_numerator_matches": list_term.get("numerator")
            == expected["list_numerator"],
            "total_numerator_matches": total == expected["total_numerator"],
            "common_denominator_matches": line.get("denominator") == F17_Q
            and list_term.get("denominator") == F17_Q,
            "budget_comparison_matches": (
                (total <= 6)
                == (expected["verdict"] == "SAFE_BY_PROVED_UPPER_BOUND")
            ),
            "combined_verdict_matches": scan["combined_protocol"]["verdict"]
            == expected["verdict"],
            "combined_has_no_unknown_terms": scan["combined_protocol"][
                "unknown_terms"
            ]
            == [],
        }
        replay_rows[str(a)] = {
            "r": scan["r"],
            "sigma": scan["sigma"],
            "line_numerator": line.get("numerator"),
            "list_numerator": list_term.get("numerator"),
            "total_numerator": total,
            "combined_verdict": scan["combined_protocol"]["verdict"],
            "checks": checks,
        }

    all_row_checks = [
        value for row in replay_rows.values() for value in row["checks"].values()
    ]
    return {
        "status": "AUDIT",
        "purpose": "replay committed line-plus-one-list scanner output at the shifted threshold rows",
        "scanner_config": {
            "path": str(PROTOCOL_SCANNER_CONFIG),
            "sha256": sha256_file(PROTOCOL_SCANNER_CONFIG),
        },
        "scanner_json_report": {
            "path": str(PROTOCOL_SCANNER_JSON),
            "sha256": sha256_file(PROTOCOL_SCANNER_JSON),
        },
        "scanner_markdown_report": {
            "path": str(PROTOCOL_SCANNER_MD),
            "sha256": sha256_file(PROTOCOL_SCANNER_MD),
        },
        "row_checks": row_checks,
        "threshold_rows": replay_rows,
        "checks": {
            "row_and_protocol_checks_passed": all(row_checks.values()),
            "threshold_row_checks_passed": all(all_row_checks),
        },
    }


def budget(denominator: int, target_bits: int = TARGET) -> int:
    return denominator // (1 << target_bits)


def radius_line_range(n: int, k: int) -> int:
    return (n - k) // 3


def floor_log2(value: int) -> int:
    if value <= 0:
        raise ValueError("floor_log2 is defined only for positive integers")
    return value.bit_length() - 1


def ceil_div(numer: int, denom: int) -> int:
    if denom <= 0:
        raise ValueError("ceil_div requires a positive denominator")
    return -(-numer // denom)


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


def variant_row(label: str, denominator: int, numerator: int) -> dict[str, Any]:
    target_den = 1 << TARGET
    return {
        "label": label,
        "denominator": denominator,
        "budget": budget(denominator),
        "safe_numerator": numerator,
        "unsafe_numerator": numerator + 1,
        "safe_probability_le_target": numerator * target_den <= denominator,
        "unsafe_probability_gt_target": (numerator + 1) * target_den > denominator,
        "denominator_note": "projective slopes use |F|+1; affine/no-loss finite variants use |F|",
    }


def exact_threshold(
    n: int,
    k: int,
    denominator: int,
    target_bits: int = TARGET,
) -> dict[str, Any]:
    """Classify the high-agreement single-line compiler regime."""
    b = budget(denominator, target_bits)
    r_line = radius_line_range(n, k)
    two = 1 << target_bits

    if b == 0:
        return {
            "applies": False,
            "threshold_pinned": True,
            "compiler_status": "NO_SAFE_RADIUS",
            "budget": b,
            "line_exact_radius": r_line,
            "first_unsafe_integer_radius": 0,
            "first_unsafe_agreement": n,
            "unsafe_line_numerator": 1,
            "closed_real_safe_interval": {
                "left_closed": False,
                "right_open_supremum": frac_dict(Fraction(0, 1)),
                "endpoint_attained": False,
            },
            "reason": "floor(Q/2^lambda)=0, so the radius-zero numerator already exceeds target",
            "checks": {
                "zero_budget": b == 0,
                "radius_zero_unsafe": two > denominator,
            },
        }

    if b > r_line:
        return {
            "applies": False,
            "threshold_pinned": False,
            "compiler_status": "EXACT_RANGE_SAFE_THRESHOLD_BEYOND_TANGENT",
            "budget": b,
            "line_exact_radius": r_line,
            "safe_through_exact_radius": r_line,
            "first_safe_agreement_in_exact_range": n - r_line,
            "reason": "B_Q exceeds the exact tangent range, so this theorem proves safety only throughout that range",
            "checks": {
                "budget_exceeds_exact_range": b > r_line,
                "exact_range_numerator_within_budget": r_line + 1 <= b,
            },
        }

    first_unsafe_radius = b
    largest_safe_integer_radius = b - 1
    first_safe_agreement = n - largest_safe_integer_radius
    last_unsafe_agreement = n - first_unsafe_radius
    supremum = Fraction(first_unsafe_radius, n)

    safe_num = largest_safe_integer_radius + 1
    unsafe_num = first_unsafe_radius + 1

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
        "threshold_pinned": True,
        "compiler_status": "PINNED_THRESHOLD_IN_EXACT_RANGE",
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


def prize_power2_boundary(
    rate_denominator: int,
    k: int,
    field_bits: int,
    target_bits: int = TARGET,
) -> dict[str, Any]:
    """Classify the rate 1/d, Q=2^lambda high-agreement compiler frontier."""
    if rate_denominator <= 1:
        raise ValueError("rate_denominator must be at least 2")
    if k <= 0:
        raise ValueError("k must be positive")
    if field_bits < 0:
        raise ValueError("field_bits must be nonnegative")

    n = rate_denominator * k
    denominator = 1 << field_bits
    gate = exact_threshold(n, k, denominator, target_bits)
    line_radius = radius_line_range(n, k)

    if field_bits < target_bits:
        min_k_to_pin = None
        k_meets_inverse_boundary = False
        inverse_status = "ZERO_BUDGET_BELOW_TARGET"
        inverse_predicts_pinned = False
        inverse_condition = "lambda < target_bits, so B_Q=0"
    else:
        power_budget = 1 << (field_bits - target_bits)
        min_k_to_pin = ceil_div(3 * power_budget, rate_denominator - 1)
        k_meets_inverse_boundary = k >= min_k_to_pin
        inverse_status = (
            "PINNED_BY_HIGH_AGREEMENT_COMPILER"
            if k_meets_inverse_boundary
            else "REQUIRES_LOWER_AGREEMENT_THEORY"
        )
        inverse_predicts_pinned = k_meets_inverse_boundary
        inverse_condition = (
            "k >= ceil(3*2^(lambda-target_bits)/(d-1))"
        )

    classifier_pinned = gate["compiler_status"] == "PINNED_THRESHOLD_IN_EXACT_RANGE"
    checks = {
        "rate_denominator_valid": rate_denominator in [2, 4, 8, 16],
        "n_matches_rate": n == rate_denominator * k,
        "denominator_is_power2": denominator == 1 << field_bits,
        "line_radius_formula": line_radius == ((rate_denominator - 1) * k) // 3,
        "inverse_boundary_agrees_with_classifier": classifier_pinned
        == inverse_predicts_pinned,
    }
    if field_bits >= target_bits:
        checks["min_k_equivalence"] = (
            k_meets_inverse_boundary
            == ((1 << (field_bits - target_bits)) <= line_radius)
        )
    else:
        checks["zero_budget_matches_classifier"] = (
            gate["compiler_status"] == "NO_SAFE_RADIUS"
        )

    return {
        "rate": f"1/{rate_denominator}",
        "rate_denominator": rate_denominator,
        "k": k,
        "n": n,
        "field_bits": field_bits,
        "denominator": denominator,
        "target_bits": target_bits,
        "budget": gate["budget"],
        "line_exact_radius": line_radius,
        "inverse_condition": inverse_condition,
        "min_k_to_pin": min_k_to_pin,
        "k_meets_inverse_boundary": k_meets_inverse_boundary,
        "inverse_status": inverse_status,
        "classifier_status": gate["compiler_status"],
        "threshold_pinned": gate["threshold_pinned"],
        "largest_safe_integer_radius": gate.get("largest_safe_integer_radius"),
        "first_unsafe_integer_radius": gate.get("first_unsafe_integer_radius"),
        "safe_through_exact_radius": gate.get("safe_through_exact_radius"),
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
        for bits in [96, 128, 160, 192, 255]:
            out.append(
                CompilerProbe(
                    label=f"rho={rho_num}/{rho_den}, k=2^40, Q=2^{bits}",
                    n=n,
                    k=k,
                    denominator=1 << bits,
                )
            )
    return out


def prize_rate_boundary_rows() -> list[dict[str, Any]]:
    """Exact single-line compiler boundaries at the max prize dimension."""
    k = 1 << 40
    largest_official_power2_bits = 255
    rows: list[dict[str, Any]] = []
    for d in [2, 4, 8, 16]:
        n = d * k
        r_line = radius_line_range(n, k)
        max_q_pinned = (1 << TARGET) * (r_line + 1) - 1
        max_power2_bits = TARGET + floor_log2(r_line)
        first_power2_bits_beyond = max_power2_bits + 1
        largest_power2_probe = prize_power2_boundary(
            d, k, largest_official_power2_bits
        )
        min_k_to_pin_largest_power2 = largest_power2_probe["min_k_to_pin"]
        unresolved_min = first_power2_bits_beyond
        unresolved_max = largest_official_power2_bits
        checks = {
            "rate_denominator": d in [2, 4, 8, 16],
            "n_matches_rate": n == d * k,
            "line_range_formula": r_line == ((d - 1) * k) // 3,
            "max_power2_inside_interval": (1 << max_power2_bits) <= max_q_pinned,
            "next_power2_outside_interval": (1 << first_power2_bits_beyond)
            > max_q_pinned,
            "official_power2_upper_is_exclusive": (1 << largest_official_power2_bits)
            < (1 << 256),
            "largest_official_power2_not_pinned_at_kmax": (1 << largest_official_power2_bits)
            > max_q_pinned,
            "min_k_for_largest_official_power2_exceeds_prize_kmax": min_k_to_pin_largest_power2
            > k,
            "largest_power2_probe_agrees": largest_power2_probe[
                "inverse_status"
            ]
            == "REQUIRES_LOWER_AGREEMENT_THEORY",
        }
        rows.append(
            {
                "rho": f"1/{d}",
                "k": k,
                "n": n,
                "line_exact_radius": r_line,
                "official_field_bound": "|F| < 2^256",
                "official_power2_bits": {
                    "smallest_relevant": TARGET,
                    "largest_allowed": largest_official_power2_bits,
                },
                "pinned_denominator_min": 1 << TARGET,
                "pinned_denominator_max": max_q_pinned,
                "max_power2_field_bits_pinned": max_power2_bits,
                "first_power2_field_bits_beyond_pinned": first_power2_bits_beyond,
                "pinned_power2_bit_interval": {
                    "min": TARGET,
                    "max": max_power2_bits,
                    "count": max_power2_bits - TARGET + 1,
                },
                "requires_lower_agreement_power2_bit_interval": {
                    "min": unresolved_min,
                    "max": unresolved_max,
                    "count": unresolved_max - unresolved_min + 1,
                },
                "min_k_to_pin_largest_official_power2_field": min_k_to_pin_largest_power2,
                "largest_official_power2_probe": largest_power2_probe,
                "checks": checks,
            }
        )
    return rows


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
                "compiler_status": gate["compiler_status"],
                "threshold_pinned": bool(gate["threshold_pinned"]),
                "first_unsafe_radius": gate.get("first_unsafe_integer_radius"),
                "largest_safe_integer_radius": gate.get("largest_safe_integer_radius"),
                "safe_through_exact_radius": gate.get("safe_through_exact_radius"),
                "checks": gate.get("checks", {}),
                "reason": gate.get("reason"),
            }
        )

    boundary_rows = prize_rate_boundary_rows()
    official_source = source_audit()
    scanner_replay = scanner_replay_audit()
    protocol_replay = protocol_scanner_replay_audit()
    variant_rows = [
        variant_row("finite_supportwise_mca", F17_Q, finite["safe_line_numerator"]),
        variant_row("finite_no_loss_ca", F17_Q, finite["safe_line_numerator"]),
        variant_row("projective_supportwise_mca", F17_Q + 1, projective["safe_line_numerator"]),
    ]
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
            "official_source": official_source,
            "pure_mca_scanner_replay": scanner_replay,
            "line_plus_list_scanner_replay": protocol_replay,
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
        "f17_512_variant_denominator_audit": {
            "source": "tex/slackMCA_v4.tex, theorem B-high-agreement-line-staircase",
            "safe_agreement": finite["first_safe_agreement"],
            "unsafe_agreement": finite["last_unsafe_agreement"],
            "rows": variant_rows,
        },
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
        "f17_512_same_denominator_line_plus_list": {
            "source": "experimental/notes/high_agreement/current_row_protocol_ledger.tex",
            "same_denominator": F17_Q,
            "budget": finite["budget"],
            "list_numerator": 1,
            "largest_safe_integer_radius": 4,
            "first_unsafe_integer_radius": 5,
            "first_safe_agreement": 508,
            "last_unsafe_agreement": 507,
            "safe_total_numerator": 6,
            "unsafe_total_numerator": 7,
            "checks": {
                "safe_total_within_budget": 6 <= finite["budget"],
                "unsafe_total_exceeds_budget": 7 > finite["budget"],
                "safe_agreement_matches_radius": F17_N - 4 == 508,
                "unsafe_agreement_matches_radius": F17_N - 5 == 507,
            },
        },
        "row_checks": row_checks,
        "row_independent_compiler": {
            "statement": (
                "for B_Q=floor(Q/2^128), B_Q=0 gives no safe integer radius; "
                "1 <= B_Q <= floor((n-k)/3) pins the threshold at r=B_Q; "
                "larger B_Q proves safety throughout the exact tangent range "
                "but does not locate the later threshold"
            ),
            "power2_inverse_boundary": (
                "for rate rho=1/d and Q=2^lambda with lambda>=128, "
                "the high-agreement compiler pins the threshold exactly iff "
                "k >= ceil(3*2^(lambda-128)/(d-1))"
            ),
            "examples": compiler_examples,
            "prize_rate_k_2^40_power2_boundaries": boundary_rows,
        },
    }

    all_checks = list(row_checks.values())
    all_checks.extend(official_source["checks"].values())
    all_checks.extend(scanner_replay["checks"].values())
    all_checks.extend(scanner_replay["row_checks"].values())
    for row in scanner_replay["threshold_rows"].values():
        all_checks.extend(row["checks"].values())
    all_checks.extend(protocol_replay["checks"].values())
    all_checks.extend(protocol_replay["row_checks"].values())
    for row in protocol_replay["threshold_rows"].values():
        all_checks.extend(row["checks"].values())
    all_checks.extend(finite.get("checks", {}).values())
    all_checks.extend(projective.get("checks", {}).values())
    for row in variant_rows:
        all_checks.append(row["budget"] == finite["budget"])
        all_checks.append(row["safe_probability_le_target"])
        all_checks.append(row["unsafe_probability_gt_target"])
    for example in compiler_examples:
        all_checks.extend(example.get("checks", {}).values())
    for row in boundary_rows:
        all_checks.extend(row.get("checks", {}).values())
        all_checks.extend(
            row["largest_official_power2_probe"].get("checks", {}).values()
        )
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
    all_checks.extend(
        certificate["f17_512_same_denominator_line_plus_list"][
            "checks"
        ].values()
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
    replay = cert["definition_freeze"]["pure_mca_scanner_replay"]
    print(
        "  pure MCA scanner replay: "
        f"{'PASS' if all(replay['checks'].values()) else 'FAIL'}"
    )
    print(f"  row checks passed: {cert['all_checks_passed']}")


def print_row_classification(n: int, k: int, denominator: int, target_bits: int) -> None:
    gate = exact_threshold(n, k, denominator, target_bits)
    print("High-agreement single-line compiler classification")
    print(f"  n={n}")
    print(f"  k={k}")
    print(f"  Q={denominator}")
    print(f"  target=2^-{target_bits}")
    print(f"  B_Q=floor(Q/2^{target_bits})={gate['budget']}")
    print(f"  exact line radius floor((n-k)/3)={gate['line_exact_radius']}")
    print(f"  status={gate['compiler_status']}")
    if gate["compiler_status"] == "PINNED_THRESHOLD_IN_EXACT_RANGE":
        print(f"  safe r<={gate['largest_safe_integer_radius']}")
        print(f"  unsafe r={gate['first_unsafe_integer_radius']}")
    elif gate["compiler_status"] == "EXACT_RANGE_SAFE_THRESHOLD_BEYOND_TANGENT":
        print(f"  safe through r={gate['safe_through_exact_radius']}")
    else:
        print("  no safe integer radius")


def print_prize_power2_classification(
    rate_denominator: int,
    k: int,
    field_bits: int,
    target_bits: int,
) -> None:
    probe = prize_power2_boundary(rate_denominator, k, field_bits, target_bits)
    print("High-agreement prize-rate power-of-two boundary")
    print(f"  rho=1/{rate_denominator}")
    print(f"  k={k}")
    print(f"  n={probe['n']}")
    print(f"  Q=2^{field_bits}")
    print(f"  target=2^-{target_bits}")
    print(f"  B_Q={probe['budget']}")
    print(f"  exact line radius floor((n-k)/3)={probe['line_exact_radius']}")
    print(f"  inverse condition: {probe['inverse_condition']}")
    if probe["min_k_to_pin"] is not None:
        print(f"  min k to pin this field size={probe['min_k_to_pin']}")
    print(f"  inverse status={probe['inverse_status']}")
    print(f"  classifier status={probe['classifier_status']}")
    if probe["classifier_status"] == "PINNED_THRESHOLD_IN_EXACT_RANGE":
        print(f"  safe r<={probe['largest_safe_integer_radius']}")
        print(f"  unsafe r={probe['first_unsafe_integer_radius']}")
    elif probe["classifier_status"] == "EXACT_RANGE_SAFE_THRESHOLD_BEYOND_TANGENT":
        print(f"  safe through r={probe['safe_through_exact_radius']}")
    else:
        print("  no safe integer radius")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic JSON certificate")
    parser.add_argument("--check", type=Path, help="check an existing certificate")
    parser.add_argument(
        "--classify-row",
        nargs=3,
        metavar=("N", "K", "Q"),
        help="classify a row by exact integers; Q accepts forms like 2^192 or 17^32",
    )
    parser.add_argument(
        "--classify-prize-power2",
        nargs=3,
        metavar=("D", "K", "LAMBDA"),
        help="classify rate 1/D, dimension K, and field denominator Q=2^LAMBDA",
    )
    parser.add_argument("--target", type=int, default=TARGET, help="security target bits")
    parser.add_argument("--json", action="store_true", help="print JSON to stdout")
    args = parser.parse_args()

    if args.classify_row:
        n, k, denominator = (parse_int(part) for part in args.classify_row)
        gate = exact_threshold(n, k, denominator, args.target)
        if args.json:
            print(normalized_json(gate), end="")
        else:
            print_row_classification(n, k, denominator, args.target)
        return 0 if all(gate.get("checks", {}).values()) else 1

    if args.classify_prize_power2:
        d, k, field_bits = (parse_int(part) for part in args.classify_prize_power2)
        probe = prize_power2_boundary(d, k, field_bits, args.target)
        if args.json:
            print(normalized_json(probe), end="")
        else:
            print_prize_power2_classification(d, k, field_bits, args.target)
        return 0 if all(probe.get("checks", {}).values()) else 1

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
