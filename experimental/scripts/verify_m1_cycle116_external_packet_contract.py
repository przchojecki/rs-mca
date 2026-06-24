#!/usr/bin/env python3
"""Compare the external Cycle116 packet contract to the local M1 chain.

This verifier is intentionally source-facing.  It does not claim to revalidate
the whole closed PR #96 packet from GitHub; instead it checks that the compact,
hash-pinned contract extracted from that packet has exactly the same field,
slot, co-support, native-bridge, smooth-lift, and Cycle84 finite values as the
local audited verifiers in this PR.
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

import verify_m1_cycle84_exact_occupancy_chain as cycle84
import verify_m1_cycle116_field_lift_contract as field_lift
import verify_m1_cycle116_fixed_jet_bridge as fixed_jet
import verify_m1_cycle116_slot_assembly as slot_assembly
import verify_m1_cycle116_slot_identities as slot_ids


ROOT = SCRIPT_DIR.parents[1]
CONTRACT_PATH = (
    ROOT / "experimental/data/witnesses/m1-cycle116/external_packet_contract.json"
)

EXPECTED_SCHEMA = "m1.cycle116.external_packet_contract.v1"
EXPECTED_PR = 96
EXPECTED_HEAD_COMMIT = "fdb3cacece5a7f71399f12c697bd5193806f82ef"
EXPECTED_SOURCE_HASHES = {
    "fixed_jet_certificate": (
        "e5615ac29a91cc39be9d3edf1a59e0b4994c146cf7bd0d5f415fbe9c7503e1a2"
    ),
    "cycle84_anchor": (
        "4aa5baba92e62948e69e6295c19c60a3a7f50d986cc58102569026cf571c82de"
    ),
    "standalone_certificate_section": (
        "49d195155fc4f895f352d4ad0de76d12016e6ba530d873c241c3773de973d59e"
    ),
    "transfer_verifier": (
        "c8f993e19d9cb2a2314e2ac59511aaf60de89ff134c83958fb20594a927a6bd3"
    ),
}
EXPECTED_SOURCE_CLAUSES = {
    "native_co_support": "J_T={1} union union_{t=1}^7 eta^t lift(i_t,a_t)",
    "native_locator_shape": "P_T(X)=X^113-X^112+O(X^107)",
    "native_scalar": "P_T(beta)=(beta-1)3^28 Phi(T)=kappa Phi(T)",
    "native_conclusion": "LD_sw(RS[F0,D0,137],143) >= 52747567092",
    "smooth_domain": "H=<theta>=D0 disjoint_union theta D0",
    "smooth_padding": "J_T^+=J_T union R and S_T^+=(D0\\J_T) union A",
    "smooth_sizes": "|J_T^+|=250 and |S_T^+|=262",
    "smooth_conclusion": "LD_sw(RS[F_17^32,H,256],262) >= 52747567092",
    "scope": (
        "finite smooth-domain standard Reed-Solomon support-wise MCA / LD_sw "
        "lower bound"
    ),
}


def load_contract(path: Path = CONTRACT_PATH) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def padded(values: Sequence[int], size: int) -> list[int]:
    out = [int(value) % slot_ids.P for value in values]
    if len(out) > size:
        raise AssertionError(f"too many coefficients: {values}")
    return out + [0] * (size - len(out))


def inclusive_size(bounds: Sequence[int]) -> int:
    if len(bounds) != 2:
        raise AssertionError(f"bad inclusive range: {bounds}")
    start, end = (int(bounds[0]), int(bounds[1]))
    if start > end:
        raise AssertionError(f"empty inclusive range: {bounds}")
    return end - start + 1


def parse_seed_map(raw: Mapping[str, Sequence[int]]) -> Dict[int, list[int]]:
    return {int(seed): [int(value) for value in values] for seed, values in raw.items()}


def field_factorization_value(raw: Mapping[str, int]) -> int:
    product = 1
    for prime, exponent in raw.items():
        product *= int(prime) ** int(exponent)
    return product


def build_report(local_reports: Mapping[str, Any] | None = None) -> Dict[str, Any]:
    local_reports = local_reports or {}
    contract = load_contract()
    fixed_contract = contract["fixed_jet_certificate"]
    cycle84_anchor = contract["cycle84_anchor"]
    field = fixed_contract["field"]
    packet = fixed_contract["packet"]
    native_contract = fixed_contract["native"]
    smooth_contract = fixed_contract["smooth_lift"]
    expected = fixed_contract["expected"]
    finite_values = cycle84_anchor["accepted_finite_values"]

    cycle84_report = local_reports.get("cycle84") or cycle84.build_report()
    slot_report = local_reports.get("slot_ids") or slot_ids.build_report()
    assembly_report = local_reports.get("slot_assembly") or slot_assembly.build_report()
    fixed_report = local_reports.get("fixed_jet") or fixed_jet.build_report()
    lift_report = local_reports.get("field_lift") or field_lift.build_report()

    exact = cycle84_report["cycle84_exact"]
    slot_table = slot_report["slot_table"]
    assembly = assembly_report["assembly"]
    fixed_params = fixed_report["parameters"]
    formal = fixed_report["formal_reduction"]
    lift_field = lift_report["field"]
    lift_params = lift_report["parameters"]

    base_exponent_sets = parse_seed_map(packet["base_exponent_sets"])
    expected_locator_coeffs = parse_seed_map(
        packet["expected_base_locator_coefficients_low_to_high"]
    )
    color_offsets = {int(seed): int(value) for seed, value in packet["color_offsets"].items()}
    slot_indices = [int(value) for value in packet["slot_indices"]]
    state_start, state_end = (int(value) for value in packet["state_a_range"])

    computed_locator_coeffs = {
        seed: list(
            slot_ids.prime_poly_from_roots(
                pow(3, exponent, slot_ids.P) for exponent in exponents
            )
        )
        for seed, exponents in base_exponent_sets.items()
    }
    computed_color_offsets = {
        seed: sum(exponents) % int(packet["color_shell_modulus"])
        for seed, exponents in base_exponent_sets.items()
    }

    a_size = inclusive_size(smooth_contract["A_odd_coset_exponent_range_inclusive"])
    r_size = inclusive_size(smooth_contract["R_odd_coset_exponent_range_inclusive"])
    reference_states = [
        int(value) for value in packet["reference_tuple_zero_based_state_indices"]
    ]
    local_slot_count = (
        len(slot_assembly.ACTIVE_COSETS)
        * len(slot_ids.E_SETS)
        * (state_end - state_start + 1)
    )

    source_hashes = {
        name: payload["sha256"]
        for name, payload in contract["provenance"]["source_files"].items()
    }

    checks = {
        "contract_schema_matches": contract["schema"] == EXPECTED_SCHEMA,
        "source_pr_and_commit_pinned": (
            int(contract["provenance"]["pull_request"]) == EXPECTED_PR
            and contract["provenance"]["head_commit"] == EXPECTED_HEAD_COMMIT
        ),
        "source_hashes_match_expected": source_hashes == EXPECTED_SOURCE_HASHES,
        "source_clauses_match_expected": (
            contract["source_clauses"] == EXPECTED_SOURCE_CLAUSES
        ),
        "fixed_jet_schema_matches_external": (
            fixed_contract["schema"] == "cycle116.fixed_jet_and_smooth_lift.v1"
        ),
        "cycle84_anchor_schema_matches_external": (
            cycle84_anchor["schema"] == "cycle116.cycle84_anchor.v1"
        ),
        "field_prime_and_degree_match_local": (
            int(field["p"]) == slot_ids.P
            and int(field["degree"]) == slot_ids.DEGREE
        ),
        "field_modulus_matches_local": (
            [int(value) for value in field["modulus_coefficients_low_to_high"]]
            == list(slot_ids.MODULUS)
        ),
        "eta_matches_local": (
            padded(field["eta_coefficients_low_to_high"], slot_ids.DEGREE)
            == list(slot_ids.ETA)
        ),
        "beta_and_slot_log_generator_match_local": (
            padded(field["beta_coefficients_low_to_high"], slot_ids.DEGREE)
            == list(slot_ids.BETA)
            and padded(
                field["slot_log_generator_coefficients_low_to_high"],
                slot_ids.DEGREE,
            )
            == list(slot_ids.BETA)
        ),
        "multiplicative_group_factorization_matches_field": (
            field_factorization_value(field["multiplicative_group_factorization"])
            == slot_ids.FIELD_SIZE - 1
        ),
        "base_exponent_sets_match_local": (
            {seed: set(values) for seed, values in base_exponent_sets.items()}
            == slot_ids.E_SETS
        ),
        "base_locator_coefficients_match_local": (
            computed_locator_coeffs == expected_locator_coeffs
        ),
        "color_offsets_match_local": computed_color_offsets == color_offsets,
        "slot_indices_are_active_cosets": (
            slot_indices == list(slot_assembly.ACTIVE_COSETS)
            == assembly["active_cosets"]
        ),
        "state_range_has_16_shifts": (state_start, state_end) == (0, 15),
        "reference_tuple_has_one_state_per_active_slot": (
            len(reference_states) == len(slot_indices)
            and all(0 <= value < 48 for value in reference_states)
        ),
        "slot_state_count_matches_local": (
            int(expected["slot_state_count"])
            == local_slot_count
            == int(slot_table["rows"])
            == int(formal["slot_identities_required"])
        ),
        "eta_power_16_value_matches": (
            slot_ids.fpow(slot_ids.ETA, 16)
            == slot_ids.emb(int(expected["eta_power_16_prime_field_value"]))
        ),
        "three_power_28_value_matches": (
            pow(3, 28, slot_ids.P)
            == int(expected["three_power_28_prime_field_value"])
        ),
        "native_parameters_match_local": (
            int(native_contract["n"]) == int(fixed_params["native_domain_size"])
            == int(assembly["native_domain_size"])
            and int(native_contract["j"]) == int(fixed_params["native_cosupport_size"])
            == int(assembly["cosupport_size"])
            and int(native_contract["sigma"]) == int(formal["fixed_jet_sigma"])
            and int(native_contract["k"]) == int(fixed_params["native_dimension"])
            and int(native_contract["agreement"]) == int(fixed_params["native_agreement"])
        ),
        "native_delta_is_cosupport_fraction": (
            int(native_contract["delta_numerator"]) == int(native_contract["j"])
            and int(native_contract["delta_denominator"]) == int(native_contract["n"])
        ),
        "external_co_support_formula_matches_local_assembly": (
            contract["source_clauses"]["native_co_support"]
            == "J_T={1} union union_{t=1}^7 eta^t lift(i_t,a_t)"
            and assembly["cosupport_formula"] == "1 + 7*16"
            and int(assembly["cosupport_size"]) == 113
        ),
        "smooth_padding_ranges_partition_odd_coset": (
            smooth_contract["A_odd_coset_exponent_range_inclusive"] == [0, 118]
            and smooth_contract["R_odd_coset_exponent_range_inclusive"] == [119, 255]
            and a_size == int(lift_params["odd_padding_size"])
            and r_size == int(lift_params["odd_unused_size"])
            and a_size + r_size == int(native_contract["n"])
        ),
        "smooth_parameters_match_local": (
            smooth_contract["theta_relation"] == "theta^2=eta"
            and int(smooth_contract["H_order"]) == int(lift_field["domain_size"])
            and int(smooth_contract["n"]) == int(lift_field["domain_size"])
            and int(smooth_contract["j"])
            == int(native_contract["j"]) + r_size
            == 250
            and int(smooth_contract["sigma"]) == int(lift_params["fixed_jet_sigma"])
            and int(smooth_contract["k"]) == int(lift_params["lift_dimension"])
            and int(smooth_contract["agreement"]) == int(lift_params["lift_agreement"])
            and int(smooth_contract["delta_numerator"]) == 125
            and int(smooth_contract["delta_denominator"]) == 256
        ),
        "smooth_agreement_is_native_plus_padding": (
            int(smooth_contract["agreement"]) == int(native_contract["agreement"]) + a_size
        ),
        "cycle84_slot_logs_file_hash_matches_local_certificate": (
            cycle84_anchor["imported_files"]["slot_logs"]["sha256"]
            == cycle84_report["projected_log_certificate_sha256"]
        ),
        "cycle84_normalized_slot_table_digest_matches_local": (
            cycle84_report["slot_table_digest"] == slot_table["digest_sha256"]
        ),
        "cycle84_expected_values_match_local_exact_chain": (
            int(expected["packet_supports"]) == int(exact["color_shell_size"])
            and int(expected["distinct_products"]) == int(exact["distinct_products"])
            and int(finite_values["packet_supports"]) == int(exact["color_shell_size"])
            and int(finite_values["distinct_products"]) == int(exact["distinct_products"])
            and int(finite_values["ordered_offdiagonal_energy"])
            == int(exact["true_ordered_energy"])
            and int(finite_values["m_max"]) == int(exact["m_max"])
            and int(finite_values["double_fibers"]) == int(exact["true_double_fibers"])
            and int(finite_values["fibers_ge_3"]) == 0
        ),
        "finite_fiber_accounting_matches_local_exact_chain": (
            int(finite_values["singleton_fibers"])
            + int(finite_values["double_fibers"])
            == int(exact["distinct_products"])
            and int(finite_values["packet_supports"])
            - int(finite_values["double_fibers"])
            == int(exact["distinct_products"])
        ),
        "field_gate_floor_matches_lift_field": (
            int(expected["floor_17_pow_32_over_2_pow_128"])
            == int(lift_field["lifted_field_size"]) // (1 << 128)
            == 6
        ),
        "density_numerator_exceeds_gate": (
            int(expected["distinct_products"])
            > int(expected["floor_17_pow_32_over_2_pow_128"])
        ),
    }

    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": "AUDIT / EXTERNAL-CYCLE116-PACKET-CONTRACT-COMPARED",
        "theorem_problem_id": "M1 Cycle116 external packet contract comparison",
        "contract_path": str(CONTRACT_PATH.relative_to(ROOT)),
        "provenance": {
            "repository": contract["provenance"]["repository"],
            "pull_request": int(contract["provenance"]["pull_request"]),
            "head_ref": contract["provenance"]["head_ref"],
            "head_commit": contract["provenance"]["head_commit"],
            "source_hashes": source_hashes,
        },
        "external_packet": {
            "field": "F_17[X]/(X^16+X^8+3)",
            "slot_indices": slot_indices,
            "state_count": local_slot_count,
            "co_support": contract["source_clauses"]["native_co_support"],
            "native_parameters": {
                "n": int(native_contract["n"]),
                "j": int(native_contract["j"]),
                "sigma": int(native_contract["sigma"]),
                "k": int(native_contract["k"]),
                "agreement": int(native_contract["agreement"]),
            },
            "smooth_lift_parameters": {
                "n": int(smooth_contract["n"]),
                "j": int(smooth_contract["j"]),
                "sigma": int(smooth_contract["sigma"]),
                "k": int(smooth_contract["k"]),
                "agreement": int(smooth_contract["agreement"]),
                "delta": (
                    f"{smooth_contract['delta_numerator']}/"
                    f"{smooth_contract['delta_denominator']}"
                ),
            },
            "cycle84_values": {
                "packet_supports": int(expected["packet_supports"]),
                "distinct_products": int(expected["distinct_products"]),
                "ordered_offdiagonal_energy": int(
                    finite_values["ordered_offdiagonal_energy"]
                ),
                "m_max": int(finite_values["m_max"]),
            },
        },
        "checks": checks,
        "remaining_imports": [
            "reviewer acceptance that the compact contract faithfully records the "
            "hash-pinned external PR #96 files",
            "official ABF PDF/source verification for the Cycle120 row gates",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    packet = report["external_packet"]
    native = packet["native_parameters"]
    smooth = packet["smooth_lift_parameters"]
    values = packet["cycle84_values"]

    print("m1_cycle116_external_packet_contract: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(
        "provenance="
        f"PR #{report['provenance']['pull_request']} "
        f"{report['provenance']['head_ref']}@{report['provenance']['head_commit']}"
    )
    print(
        "external_packet="
        f"{packet['field']}, slots={packet['slot_indices']}, "
        f"state_count={packet['state_count']}, co_support={packet['co_support']}"
    )
    print(
        "native="
        f"n={native['n']}, j={native['j']}, sigma={native['sigma']}, "
        f"k={native['k']}, agreement={native['agreement']}"
    )
    print(
        "smooth_lift="
        f"n={smooth['n']}, j={smooth['j']}, sigma={smooth['sigma']}, "
        f"k={smooth['k']}, agreement={smooth['agreement']}, delta={smooth['delta']}"
    )
    print(
        "cycle84_values="
        f"packet_supports={values['packet_supports']}, "
        f"distinct_products={values['distinct_products']}, "
        f"energy={values['ordered_offdiagonal_energy']}, m_max={values['m_max']}"
    )
    print("remaining_imports=" + "; ".join(report["remaining_imports"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare the external Cycle116 packet contract to local audits."
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
