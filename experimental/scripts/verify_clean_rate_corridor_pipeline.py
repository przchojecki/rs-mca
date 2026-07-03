#!/usr/bin/env python3
"""Verify the Q3R.3 clean-rate corridor certificate skeleton.

This is a packaging/replay verifier, not a new Row-C experiment.  It stitches
together committed deterministic artifacts for the clean prize rates 1/4, 1/8,
and 1/16:

* the r2 corridor arithmetic;
* E14 integrality-margin crossing rows;
* the high-agreement pinned-class adjacent power-of-two boundary;
* the Row-C e1 norm-height frontier.

The output is a per-rate certificate skeleton that later structural packets can
fill with lower-agreement, Row-C, or list-side proofs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import certify_high_agreement_threshold_package as high_agreement
import verify_roadmap_r2_numbers as r2_numbers


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / (
    "experimental/data/certificates/clean-rate-corridor-pipeline/"
    "clean_rate_corridor_pipeline_skeleton.json"
)
INTEGRALITY_CERT = ROOT / (
    "experimental/data/certificates/integrality-margin-tables/"
    "integrality_margin_tables.json"
)
HIGH_AGREEMENT_CERT = ROOT / (
    "experimental/data/certificates/high-agreement-threshold-package/"
    "f17_512_high_agreement_threshold_certificate.json"
)
ROW_C_E1_CERT = ROOT / (
    "experimental/data/certificates/row-c-e1-sampling/"
    "e1_sharp_norm_height_constants.json"
)

SCHEMA_VERSION = "clean-rate-corridor-pipeline-skeleton-v1"
K_MAX = 1 << 40
TARGET_BITS = 128
RATES = (4, 8, 16)
CAP_EXPONENT = {4: 9, 8: 9, 16: 10}
EXPECTED_INTEGRALITY_CROSSINGS = {
    4: {"relaxed_A2_crossing": 176, "dyadic_A2_crossing": 256, "planted_dyadic_crossing": 256},
    8: {"relaxed_A2_crossing": 248, "dyadic_A2_crossing": 256, "planted_dyadic_crossing": 256},
    16: {"relaxed_A2_crossing": 384, "dyadic_A2_crossing": 512, "planted_dyadic_crossing": 512},
}
EXPECTED_PINNED_BOUNDARIES = {
    4: {"last_pinned_bits": 168, "first_unpinned_bits": 169},
    8: {"last_pinned_bits": 169, "first_unpinned_bits": 170},
    16: {"last_pinned_bits": 170, "first_unpinned_bits": 171},
}
EXPECTED_ROW_C_EVEN_FRONTIERS = {4: 100, 8: 120, 16: 112}
EXPECTED_ROW_C_DYADIC_FRONTIERS = {4: 64, 8: 64, 16: 64}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def round6(value: float) -> float:
    return round(value, 6)


def corridor_row(rate_denominator: int) -> dict[str, Any]:
    rho = 1 / rate_denominator
    cap_exp = CAP_EXPONENT[rate_denominator]
    expected = r2_numbers.EXPECT[rho]
    cap = 1 - rho - 2 ** (-cap_exp)
    quotient = 1 - rho - r2_numbers.beta(rho) / TARGET_BITS
    tau = 1 - rho - r2_numbers.taustar(rho, 2 * TARGET_BITS)
    list_window = (
        1 - rho - r2_numbers.H(rho) / TARGET_BITS,
        1 - rho - r2_numbers.H(rho) / (2 * TARGET_BITS),
    )
    width_in_cap_cells = (cap - quotient) / 2 ** (-cap_exp)
    checks = {
        "cap_matches_r2_table": abs(cap - expected["cap"]) < 5e-6,
        "quotient_matches_r2_table": abs(quotient - expected["quot"]) < 5e-6,
        "tau_matches_r2_table": abs(tau - expected["tau"]) < 5e-6,
        "list_lower_matches_r2_table": abs(list_window[0] - expected["lw"][0]) < 5e-6,
        "list_upper_matches_r2_table": abs(list_window[1] - expected["lw"][1]) < 5e-6,
        "corridor_ordering": list_window[0] < quotient < tau < cap,
        "list_upper_tracks_tau": abs(list_window[1] - tau) < 3e-4,
        "width_matches_r2_table": abs(width_in_cap_cells - expected["width"]) < 0.01,
    }
    return {
        "rate": f"1/{rate_denominator}",
        "rate_denominator": rate_denominator,
        "cap_exponent": cap_exp,
        "quotient_crossing": round6(quotient),
        "tau_star_crossing": round6(tau),
        "cap_crossing": round6(cap),
        "list_window": {
            "lower": round6(list_window[0]),
            "upper": round6(list_window[1]),
        },
        "width_in_cap_cells": round(width_in_cap_cells, 2),
        "checks": checks,
    }


def selected_integrality_rows(
    integrality: dict[str, Any],
    rate_denominator: int,
) -> dict[str, Any]:
    rate = f"1/{rate_denominator}"
    scales = [
        row for row in integrality["candidate_scales"]
        if row["budget_bits"] == TARGET_BITS and row["rate"] == rate
    ]
    require(len(scales) == 1, f"missing integrality scale row for {rate}")
    rows = [
        row for row in integrality["rows"]
        if row["budget_bits"] == TARGET_BITS and row["rate"] == rate
    ]
    require(len(rows) == 3, f"expected three integrality rows for {rate}")
    by_family = {row["candidate_family"]: row for row in rows}
    expected = EXPECTED_INTEGRALITY_CROSSINGS[rate_denominator]
    checks = {
        "scale_relaxed_crossing_matches": scales[0]["mca_relaxed_a2_crossing_N"]
        == expected["relaxed_A2_crossing"],
        "scale_dyadic_crossing_matches": scales[0]["mca_dyadic_a2_crossing_N"]
        == expected["dyadic_A2_crossing"],
        "scale_planted_crossing_matches": scales[0]["list_planted_crossing_N"]
        == expected["planted_dyadic_crossing"],
        "all_margin_rows_pass": all(row["passes_n3_integrality_margin"] for row in rows),
        "all_margin_rows_positive": all(row["minus_log2_n_pow_B_times_proxy"] > 0 for row in rows),
        "row_count_is_three": len(rows) == 3,
    }
    return {
        "candidate_scales": scales[0],
        "margin_rows": [
            {
                "side": row["side"],
                "candidate_family": row["candidate_family"],
                "quotient_order_N": row["quotient_order_N"],
                "minus_log2_n_pow_B_times_proxy": row["minus_log2_n_pow_B_times_proxy"],
                "passes_n3_integrality_margin": row["passes_n3_integrality_margin"],
            }
            for row in rows
        ],
        "minimum_margin_bits_for_rate": min(
            row["minus_log2_n_pow_B_times_proxy"] for row in rows
        ),
        "crossings": {
            "relaxed_A2_crossing": by_family["relaxed_A2_crossing"]["quotient_order_N"],
            "dyadic_A2_crossing": by_family["dyadic_A2_crossing"]["quotient_order_N"],
            "planted_dyadic_crossing": by_family["planted_dyadic_crossing"]["quotient_order_N"],
        },
        "checks": checks,
    }


def high_agreement_boundary(
    high_cert: dict[str, Any],
    rate_denominator: int,
) -> dict[str, Any]:
    rho = f"1/{rate_denominator}"
    rows = [
        row for row in high_cert["row_independent_compiler"]["prize_rate_k_2^40_power2_boundaries"]
        if row["rho"] == rho
    ]
    require(len(rows) == 1, f"missing high-agreement boundary row for {rho}")
    row = rows[0]
    expected = EXPECTED_PINNED_BOUNDARIES[rate_denominator]
    last_bits = expected["last_pinned_bits"]
    next_bits = expected["first_unpinned_bits"]
    last_probe = high_agreement.prize_power2_boundary(
        rate_denominator, K_MAX, last_bits, TARGET_BITS
    )
    next_probe = high_agreement.prize_power2_boundary(
        rate_denominator, K_MAX, next_bits, TARGET_BITS
    )
    checks = {
        "certificate_last_pinned_matches": row["pinned_power2_bit_interval"]["max"]
        == last_bits,
        "certificate_first_unpinned_matches": row[
            "requires_lower_agreement_power2_bit_interval"
        ]["min"] == next_bits,
        "last_probe_is_pinned": last_probe["classifier_status"]
        == "PINNED_THRESHOLD_IN_EXACT_RANGE",
        "last_probe_inverse_pinned": last_probe["inverse_status"]
        == "PINNED_BY_HIGH_AGREEMENT_COMPILER",
        "next_probe_requires_lower_agreement": next_probe["inverse_status"]
        == "REQUIRES_LOWER_AGREEMENT_THEORY",
        "next_probe_safe_only_through_exact_range": next_probe["classifier_status"]
        == "EXACT_RANGE_SAFE_THRESHOLD_BEYOND_TANGENT",
    }
    return {
        "rho": rho,
        "k": K_MAX,
        "n": rate_denominator * K_MAX,
        "line_exact_radius": row["line_exact_radius"],
        "pinned_power2_bit_interval": row["pinned_power2_bit_interval"],
        "requires_lower_agreement_power2_bit_interval": row[
            "requires_lower_agreement_power2_bit_interval"
        ],
        "adjacent_boundary_probes": {
            "last_pinned": {
                "field_bits": last_bits,
                "budget": last_probe["budget"],
                "classifier_status": last_probe["classifier_status"],
                "inverse_status": last_probe["inverse_status"],
                "largest_safe_integer_radius": last_probe.get("largest_safe_integer_radius"),
                "first_unsafe_integer_radius": last_probe.get("first_unsafe_integer_radius"),
            },
            "first_unpinned": {
                "field_bits": next_bits,
                "budget": next_probe["budget"],
                "classifier_status": next_probe["classifier_status"],
                "inverse_status": next_probe["inverse_status"],
                "safe_through_exact_radius": next_probe.get("safe_through_exact_radius"),
            },
        },
        "checks": checks,
    }


def row_c_frontier(row_c_e1: dict[str, Any], rate_denominator: int) -> dict[str, Any]:
    rate = f"1/{rate_denominator}"
    selected = [
        row for row in row_c_e1["frontiers"]
        if row["rate"] == rate and row["bit_budget"] == 2 * TARGET_BITS
    ]
    require(len(selected) == 2, f"missing Row-C e1 frontier rows for {rate}")
    by_mode = {row["mode"]: row for row in selected}
    checks = {
        "even_frontier_matches": by_mode["even_prefix"]["max_certified"]["N_prime"]
        == EXPECTED_ROW_C_EVEN_FRONTIERS[rate_denominator],
        "dyadic_frontier_matches": by_mode["dyadic"]["max_certified"]["N_prime"]
        == EXPECTED_ROW_C_DYADIC_FRONTIERS[rate_denominator],
        "even_has_first_failing": by_mode["even_prefix"]["first_failing_after_frontier"]
        is not None,
        "dyadic_has_first_failing": by_mode["dyadic"]["first_failing_after_frontier"]
        is not None,
    }
    return {
        "rate": rate,
        "bit_budget": 2 * TARGET_BITS,
        "frontiers": {
            mode: {
                "max_certified_N_prime": row["max_certified"]["N_prime"],
                "max_certified_height_bits": row["max_certified"]["height_bound_bit_length"],
                "first_failing_N_prime": row["first_failing_after_frontier"]["N_prime"],
            }
            for mode, row in sorted(by_mode.items())
        },
        "checks": checks,
    }


def certificate_skeleton(rate_denominator: int) -> dict[str, Any]:
    rate = f"1/{rate_denominator}"
    return {
        "row_id": f"clean_rate_{rate.replace('/', '_over_')}",
        "rate": rate,
        "dag_node": "Q3R.3",
        "campaign_id": "C-2",
        "classes": [
            {
                "class": "Row-C-class",
                "required_inputs": [
                    str(INTEGRALITY_CERT.relative_to(ROOT)),
                    str(ROW_C_E1_CERT.relative_to(ROOT)),
                ],
                "status": "skeleton_ready / arithmetic replayed",
            },
            {
                "class": "pinned-class",
                "required_inputs": [
                    str(HIGH_AGREEMENT_CERT.relative_to(ROOT)),
                ],
                "status": "skeleton_ready / adjacent boundary replayed",
            },
        ],
        "safe_replay_commands": [
            "python3 experimental/scripts/verify_roadmap_r2_numbers.py",
            "python3 experimental/scripts/verify_integrality_margin_tables.py --check "
            "experimental/data/certificates/integrality-margin-tables/integrality_margin_tables.json",
            "python3 experimental/scripts/certify_high_agreement_threshold_package.py --check "
            "experimental/data/certificates/high-agreement-threshold-package/f17_512_high_agreement_threshold_certificate.json",
            "python3 experimental/scripts/verify_e1_sharp_norm_height_constants.py --check "
            "experimental/data/certificates/row-c-e1-sampling/e1_sharp_norm_height_constants.json",
        ],
    }


def rate_packet(
    integrality: dict[str, Any],
    high_cert: dict[str, Any],
    row_c_e1: dict[str, Any],
    rate_denominator: int,
) -> dict[str, Any]:
    corridor = corridor_row(rate_denominator)
    margins = selected_integrality_rows(integrality, rate_denominator)
    pinned = high_agreement_boundary(high_cert, rate_denominator)
    row_c = row_c_frontier(row_c_e1, rate_denominator)
    all_checks = []
    for block in (corridor, margins, pinned, row_c):
        all_checks.extend(block["checks"].values())
    return {
        "rate": f"1/{rate_denominator}",
        "corridor": corridor,
        "integrality_margins": margins,
        "pinned_class_boundary": pinned,
        "row_c_class_frontier": row_c,
        "certificate_skeleton": certificate_skeleton(rate_denominator),
        "all_checks_passed": all(bool(value) for value in all_checks),
    }


def build_certificate() -> dict[str, Any]:
    integrality = load_json(INTEGRALITY_CERT)
    high_cert = load_json(HIGH_AGREEMENT_CERT)
    row_c_e1 = load_json(ROW_C_E1_CERT)
    require(integrality["schema"] == "integrality-margin-tables-v1", "bad integrality schema")
    require(row_c_e1["schema"] == "e1-sharp-norm-height-constants-v1", "bad Row-C e1 schema")
    require(high_cert["all_checks_passed"] is True, "high-agreement source checks not green")
    rows = [
        rate_packet(integrality, high_cert, row_c_e1, rate_denominator)
        for rate_denominator in RATES
    ]
    payload = {
        "schema_version": SCHEMA_VERSION,
        "status": "SKELETON / REPLAYED_CERTIFICATE_PACKET",
        "campaign_id": "C-2",
        "dag_node": "Q3R.3",
        "scope": {
            "rates": [row["rate"] for row in rows],
            "k": K_MAX,
            "target_bits": TARGET_BITS,
            "classes": ["Row-C-class", "pinned-class"],
            "description": (
                "per-rate skeleton rows locating corridor crossings, replaying "
                "integrality margins, and pinning adjacent high-agreement "
                "boundary probes"
            ),
        },
        "sources": {
            "integrality_margin_tables": {
                "path": str(INTEGRALITY_CERT.relative_to(ROOT)),
                "sha256": sha256_file(INTEGRALITY_CERT),
            },
            "high_agreement_threshold_package": {
                "path": str(HIGH_AGREEMENT_CERT.relative_to(ROOT)),
                "sha256": sha256_file(HIGH_AGREEMENT_CERT),
            },
            "row_c_e1_norm_height": {
                "path": str(ROW_C_E1_CERT.relative_to(ROOT)),
                "sha256": sha256_file(ROW_C_E1_CERT),
            },
        },
        "rows": rows,
        "summary": {
            "row_count": len(rows),
            "all_rows_green": all(row["all_checks_passed"] for row in rows),
            "minimum_integrality_margin_bits": min(
                row["integrality_margins"]["minimum_margin_bits_for_rate"]
                for row in rows
            ),
            "pinned_last_bits_by_rate": {
                row["rate"]: row["pinned_class_boundary"]["pinned_power2_bit_interval"]["max"]
                for row in rows
            },
            "row_c_even_frontier_by_rate": {
                row["rate"]: row["row_c_class_frontier"]["frontiers"]["even_prefix"][
                    "max_certified_N_prime"
                ]
                for row in rows
            },
        },
        "nonclaims": [
            "does not run Row-C value-set sampling",
            "does not prove lower-agreement theory beyond the pinned class",
            "does not prove the list-side safe theorem",
            "does not promote any leaderboard row",
        ],
    }
    require(payload["summary"]["all_rows_green"], "some clean-rate skeleton row failed")
    payload["payload_sha256"] = sha256_json(payload)
    return payload


def check_certificate(path: Path, expected: dict[str, Any]) -> None:
    actual = json.loads(path.read_text(encoding="utf-8"))
    if actual != expected:
        raise AssertionError(f"certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    print("Clean-rate corridor pipeline skeleton")
    print(f"status: {certificate['status']}")
    print(f"rates: {', '.join(certificate['scope']['rates'])}")
    print(
        "minimum integrality margin bits:",
        certificate["summary"]["minimum_integrality_margin_bits"],
    )
    for row in certificate["rows"]:
        pinned = row["pinned_class_boundary"]["pinned_power2_bit_interval"]
        row_c = row["row_c_class_frontier"]["frontiers"]["even_prefix"]
        print(
            f"  {row['rate']}: pinned bits {pinned['min']}..{pinned['max']}, "
            f"Row-C even N' <= {row_c['max_certified_N_prime']}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        nargs="?",
        const=OUTPUT,
        type=Path,
        help="write deterministic skeleton JSON, optionally to PATH",
    )
    parser.add_argument(
        "--check",
        nargs="?",
        const=OUTPUT,
        type=Path,
        help="check deterministic skeleton JSON, optionally at PATH",
    )
    parser.add_argument("--json", action="store_true", help="print certificate JSON")
    args = parser.parse_args()

    certificate = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        check_certificate(args.check, certificate)
    if args.json:
        print(render(certificate), end="")
        return
    print_summary(certificate)


if __name__ == "__main__":
    main()
