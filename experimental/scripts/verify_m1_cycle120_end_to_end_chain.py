#!/usr/bin/env python3
"""Verify the composed finite M1 Cycle120 chain.

This nonmutating verifier composes the current local M1 audit reports:

    Cycle84 exact product occupancy
      -> Cycle116 fixed-jet native support-wise line/MCA lower bound
      -> Cycle116 smooth padding lift to the [512,256] row
      -> Cycle120 ABF-facing density and agreement arithmetic.

It deliberately does not check the official ABF PDF/source wording or perform
human review of the generated Cycle84 replay source. Those remain explicit
promotion boundaries.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import verify_m1_cycle84_exact_occupancy_chain as cycle84
import verify_m1_cycle116_field_lift_contract as field_lift
import verify_m1_cycle116_external_packet_contract as external_packet
import verify_m1_cycle116_fixed_jet_bridge as fixed_jet
import verify_m1_cycle116_fixed_jet_transfer as fixed_transfer
import verify_m1_cycle116_slot_assembly as slot_assembly
import verify_m1_cycle116_slot_identities as slot_ids
import verify_m1_cycle116_smooth_padding_transfer as smooth_padding
import verify_m1_fixed_jet_ldsw_theorem as fixed_jet_theorem
import verify_m1_cycle120_domain_field_ledger as domain_ledger
import verify_m1_cycle120_gate_arithmetic as gate
import verify_m1_cycle120_supportwise_mca_bridge as mca_bridge


EXPECTED_NUMERATOR = 52_747_567_092
EXPECTED_SLOT_DIGEST = (
    "47ae84dc2df0fe0b4b43a7e0543b141fb940061fc48ccb80b40ce4e9483abc01"
)
EXPECTED_NATIVE_DOMAIN_SIZE = 256
EXPECTED_NATIVE_DIMENSION = 137
EXPECTED_NATIVE_AGREEMENT = 143
EXPECTED_NATIVE_COSUPPORT_SIZE = 113
EXPECTED_FIXED_JET_SIGMA = 6
EXPECTED_LIFT_DOMAIN_SIZE = 512
EXPECTED_LIFT_DIMENSION = 256
EXPECTED_LIFT_AGREEMENT = 262
EXPECTED_DELTA = "125/256"


def build_report() -> Dict[str, Any]:
    cycle84_report = cycle84.build_report()
    assembly_report = slot_assembly.build_report()
    slot_report = slot_ids.build_report()
    fixed_report = fixed_jet.build_report()
    transfer_report = fixed_transfer.build_report()
    lift_report = field_lift.build_report()
    smooth_report = smooth_padding.build_report()
    theorem_report = fixed_jet_theorem.build_report(
        {
            "cycle84": cycle84_report,
            "fixed_jet": fixed_report,
            "fixed_transfer": transfer_report,
            "smooth_padding": smooth_report,
        }
    )
    ledger_report = domain_ledger.build_report()
    external_report = external_packet.build_report(
        {
            "cycle84": cycle84_report,
            "slot_ids": slot_report,
            "slot_assembly": assembly_report,
            "fixed_jet": fixed_report,
            "field_lift": lift_report,
        }
    )
    gate_report = gate.build_report()
    mca_report = mca_bridge.build_report(
        {
            "cycle84": cycle84_report,
            "field_lift": lift_report,
            "gate": gate_report,
        }
    )

    exact = cycle84_report["cycle84_exact"]
    assembly = assembly_report["assembly"]
    slot_table = slot_report["slot_table"]
    native = fixed_report["parameters"]
    formal = fixed_report["formal_reduction"]
    external = external_report["external_packet"]
    lift_field = lift_report["field"]
    lift_params = lift_report["parameters"]
    gate_object = gate_report["object"]
    gate_arithmetic = gate_report["arithmetic"]
    mca_conclusion = mca_report["mca_conclusion"]
    ledger = ledger_report["field_ledger"]

    numerator = int(exact["distinct_products"])
    field_size = int(gate_object["field_size"])
    epsilon_denominator = 1 << gate.EPSILON_DEN_BITS
    minimum_bad_count = int(
        gate_arithmetic["minimum_bad_gamma_count_for_gt_2_minus_128"]
    )

    checks = {
        "cycle84_exact_occupancy_chain_passes": cycle84_report["status"] == "PASS",
        "cycle116_slot_assembly_passes": assembly_report["status"] == "PASS",
        "cycle116_slot_identities_pass": slot_report["status"] == "PASS",
        "cycle116_fixed_jet_bridge_passes": fixed_report["status"] == "PASS",
        "cycle116_fixed_jet_transfer_passes": transfer_report["status"] == "PASS",
        "cycle116_field_lift_contract_passes": lift_report["status"] == "PASS",
        "cycle116_smooth_padding_transfer_passes": (
            smooth_report["status"] == "PASS"
        ),
        "generic_fixed_jet_ldsw_theorem_passes": (
            theorem_report["status"] == "PASS"
        ),
        "cycle120_domain_field_ledger_passes": ledger_report["status"] == "PASS",
        "cycle116_external_packet_contract_passes": (
            external_report["status"] == "PASS"
        ),
        "cycle120_gate_arithmetic_passes": gate_report["status"] == "PASS",
        "cycle120_supportwise_mca_bridge_passes": mca_report["status"] == "PASS",
        "slot_digest_matches_expected": (
            slot_table["digest_sha256"] == EXPECTED_SLOT_DIGEST
        ),
        "slot_digest_matches_cycle84_certificate": (
            slot_table["digest_sha256"] == cycle84_report["slot_table_digest"]
        ),
        "slot_identity_count_336": slot_table["rows"] == 336,
        "slot_assembly_block_count_336": int(assembly["slot_block_count"]) == 336,
        "cycle84_numerator_matches_expected": numerator == EXPECTED_NUMERATOR,
        "cycle84_numerator_matches_gate_bad_gamma_count": (
            numerator == int(gate_object["bad_gamma_count"])
        ),
        "cycle84_numerator_matches_lift_bad_gamma_count": (
            numerator == int(lift_params["bad_gamma_count"])
        ),
        "cycle84_exact_has_no_triple_fibers": (
            exact["no_fibers_of_size_at_least_3"] and int(exact["m_max"]) == 2
        ),
        "native_domain_matches_contract": (
            int(native["native_domain_size"]) == EXPECTED_NATIVE_DOMAIN_SIZE
        ),
        "assembly_domain_matches_native_domain": (
            int(assembly["native_domain_size"]) == int(native["native_domain_size"])
        ),
        "native_cosupport_matches_contract": (
            int(native["native_cosupport_size"]) == EXPECTED_NATIVE_COSUPPORT_SIZE
        ),
        "assembly_cosupport_matches_native_cosupport": (
            int(assembly["cosupport_size"]) == int(native["native_cosupport_size"])
        ),
        "assembly_cosupport_formula_1_plus_7_times_16": (
            assembly["cosupport_formula"] == "1 + 7*16"
            and int(assembly["cosupport_size"]) == 1 + 7 * 16
        ),
        "external_packet_uses_verified_cosupport": (
            external["co_support"]
            == "J_T={1} union union_{t=1}^7 eta^t lift(i_t,a_t)"
            and int(external["native_parameters"]["j"]) == int(assembly["cosupport_size"])
            and external["slot_indices"] == assembly["active_cosets"]
        ),
        "fixed_jet_sigma_matches_contract": (
            int(formal["fixed_jet_sigma"]) == EXPECTED_FIXED_JET_SIGMA
        ),
        "native_dimension_matches_contract": (
            int(native["native_dimension"]) == EXPECTED_NATIVE_DIMENSION
        ),
        "native_agreement_matches_contract": (
            int(native["native_agreement"]) == EXPECTED_NATIVE_AGREEMENT
        ),
        "native_agreement_is_k_plus_sigma": (
            int(native["native_dimension"]) + int(formal["fixed_jet_sigma"])
            == int(native["native_agreement"])
        ),
        "native_agreement_is_domain_minus_cosupport": (
            int(native["native_domain_size"])
            - int(native["native_cosupport_size"])
            == int(native["native_agreement"])
        ),
        "fixed_transfer_parameters_match_native_chain": (
            int(transfer_report["transfer"]["code_dimension"])
            == int(native["native_dimension"])
            and int(transfer_report["transfer"]["agreement"])
            == int(native["native_agreement"])
            and transfer_report["transfer"]["bad_parameter_formula"]
            == "z_T=W(beta)-V_D(beta)/P_T(beta)"
        ),
        "external_packet_native_parameters_match_chain": (
            int(external["native_parameters"]["n"]) == int(native["native_domain_size"])
            and int(external["native_parameters"]["k"]) == int(native["native_dimension"])
            and int(external["native_parameters"]["agreement"])
            == int(native["native_agreement"])
            and int(external["native_parameters"]["sigma"])
            == int(formal["fixed_jet_sigma"])
        ),
        "lift_field_size_matches_gate_field_size": (
            int(lift_field["lifted_field_size"]) == field_size
        ),
        "domain_generated_field_ledgers_match_line_field": (
            int(ledger["q_gen"])
            == int(ledger["q_code"])
            == int(ledger["q_line"])
            == field_size
        ),
        "lift_domain_matches_gate_domain": (
            int(lift_field["domain_size"]) == int(gate_object["domain_size"])
            == EXPECTED_LIFT_DOMAIN_SIZE
        ),
        "lift_dimension_matches_gate_dimension": (
            int(lift_params["lift_dimension"]) == int(gate_object["dimension"])
            == EXPECTED_LIFT_DIMENSION
        ),
        "lift_delta_matches_gate_delta": (
            lift_params["delta"] == gate_object["delta"] == EXPECTED_DELTA
        ),
        "smooth_padding_reaches_closed_threshold": (
            int(lift_params["lift_agreement"])
            == int(gate_arithmetic["closed_agreement_threshold"])
            == EXPECTED_LIFT_AGREEMENT
        ),
        "smooth_padding_transfer_matches_lift_contract": (
            int(smooth_report["smooth_padding"]["lift_agreement"])
            == int(lift_params["lift_agreement"])
            and int(smooth_report["smooth_padding"]["lift_dimension"])
            == int(lift_params["lift_dimension"])
            and smooth_report["smooth_padding"]["delta"] == lift_params["delta"]
            and smooth_report["smooth_padding"]["P_R_beta_nonzero"]
        ),
        "external_packet_smooth_lift_matches_chain": (
            int(external["smooth_lift_parameters"]["n"]) == int(lift_field["domain_size"])
            and int(external["smooth_lift_parameters"]["k"])
            == int(lift_params["lift_dimension"])
            and int(external["smooth_lift_parameters"]["agreement"])
            == int(lift_params["lift_agreement"])
            and external["smooth_lift_parameters"]["delta"] == lift_params["delta"]
        ),
        "padding_is_lossless_on_agreement_count": (
            int(lift_params["native_agreement"]) + int(lift_params["odd_padding_size"])
            == int(lift_params["lift_agreement"])
        ),
        "rate_one_half_after_lift": (
            2 * int(lift_params["lift_dimension"]) == int(lift_field["domain_size"])
        ),
        "bad_gamma_count_exceeds_epsilon_gate": numerator >= minimum_bad_count,
        "external_packet_cycle84_values_match_numerator": (
            int(external["cycle84_values"]["distinct_products"]) == numerator
            and int(external["cycle84_values"]["packet_supports"])
            == int(exact["color_shell_size"])
            and int(external["cycle84_values"]["ordered_offdiagonal_energy"])
            == int(exact["true_ordered_energy"])
            and int(external["cycle84_values"]["m_max"]) == int(exact["m_max"])
        ),
        "mca_bridge_uses_same_density_numerator_and_denominator": (
            int(mca_conclusion["numerator"]) == numerator
            and int(mca_conclusion["denominator"]) == field_size
        ),
        "bad_gamma_density_strictly_exceeds_2_minus_128": (
            numerator * epsilon_denominator > field_size
        ),
    }

    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": "CONDITIONAL / AUDIT / END-TO-END-FINITE-CHAIN",
        "theorem_problem_id": "M1 Cycle120 finite-chain composition",
        "chain": {
            "cycle84_exact_occupancy": {
                "slot_table_digest": slot_table["digest_sha256"],
                "color_shell_size": int(exact["color_shell_size"]),
                "true_double_fibers": int(exact["true_double_fibers"]),
                "true_ordered_energy": int(exact["true_ordered_energy"]),
                "m_max": int(exact["m_max"]),
                "distinct_products": numerator,
            },
            "cycle116_slot_assembly": {
                "native_domain_size": int(assembly["native_domain_size"]),
                "active_cosets": assembly["active_cosets"],
                "slot_choices_per_active_coset": int(
                    assembly["slot_choices_per_active_coset"]
                ),
                "slot_block_size": int(assembly["slot_block_size"]),
                "slot_block_count": int(assembly["slot_block_count"]),
                "cosupport_formula": assembly["cosupport_formula"],
                "cosupport_size": int(assembly["cosupport_size"]),
                "all_tuple_count": int(assembly["all_tuple_count"]),
            },
            "cycle116_external_packet_contract": {
                "provenance": external_report["provenance"],
                "co_support": external["co_support"],
                "state_count": int(external["state_count"]),
                "native_parameters": external["native_parameters"],
                "smooth_lift_parameters": external["smooth_lift_parameters"],
            },
            "cycle116_native": {
                "field": slot_report["model"]["field"],
                "domain_size": int(native["native_domain_size"]),
                "dimension": int(native["native_dimension"]),
                "cosupport_size": int(native["native_cosupport_size"]),
                "fixed_jet_sigma": int(formal["fixed_jet_sigma"]),
                "agreement": int(native["native_agreement"]),
                "bad_line_parameters": numerator,
                "conclusion": "LD_sw(RS[F0,D0,137],143) >= N",
            },
            "cycle116_fixed_jet_transfer": {
                "complement_locator_truncation": (
                    transfer_report["transfer"]["complement_locator_truncation"]
                ),
                "bad_parameter_formula": (
                    transfer_report["transfer"]["bad_parameter_formula"]
                ),
                "injectivity_reason": transfer_report["transfer"]["injectivity_reason"],
                "representative_q_degree": int(
                    transfer_report["representative_check"]["q_degree"]
                ),
            },
            "cycle116_smooth_lift": {
                "field": gate_object["field"],
                "field_size": field_size,
                "domain_size": int(lift_field["domain_size"]),
                "dimension": int(lift_params["lift_dimension"]),
                "agreement": int(lift_params["lift_agreement"]),
                "delta": lift_params["delta"],
                "bad_line_parameters": numerator,
                "padding": {
                    "A_range": smooth_report["smooth_padding"]["A_range"],
                    "A_size": int(smooth_report["smooth_padding"]["A_size"]),
                    "R_range": smooth_report["smooth_padding"]["R_range"],
                    "R_size": int(smooth_report["smooth_padding"]["R_size"]),
                    "P_R_beta_nonzero": bool(
                        smooth_report["smooth_padding"]["P_R_beta_nonzero"]
                    ),
                },
                "conclusion": "LD_sw(RS[F_17^32,H,256],262) >= N",
            },
            "fixed_jet_ldsw_theorem": {
                "proof_status": theorem_report["proof_status"],
                "toy_case_count": len(theorem_report["toy_cases"]),
                "native_bad_parameters": int(
                    theorem_report["cycle116_instantiation"]["native"][
                        "distinct_bad_parameters"
                    ]
                ),
                "smooth_bad_parameters_preserved": bool(
                    theorem_report["cycle116_instantiation"]["smooth_lift"][
                        "bad_parameters_preserved"
                    ]
                ),
            },
            "cycle120_domain_field_ledger": {
                "native_generator": ledger["native_generator"],
                "native_generated_degree": int(ledger["native_generated_degree"]),
                "lift_generator": ledger["lift_generator"],
                "lift_generated_degree": int(ledger["lift_generated_degree"]),
                "q_gen": int(ledger["q_gen"]),
                "q_code": int(ledger["q_code"]),
                "q_line": int(ledger["q_line"]),
            },
            "cycle120_gate_arithmetic": {
                "closed_agreement_threshold": int(
                    gate_arithmetic["closed_agreement_threshold"]
                ),
                "distance_radius": int(gate_arithmetic["distance_radius"]),
                "epsilon_star": gate_object["epsilon_star"],
                "minimum_bad_gamma_count_for_gt_2_minus_128": minimum_bad_count,
                "bad_gamma_count": numerator,
                "density_comparison": "N / 17^32 > 2^-128",
            },
            "cycle120_supportwise_mca": {
                "statement": mca_conclusion["statement"],
                "numerator": int(mca_conclusion["numerator"]),
                "denominator": int(mca_conclusion["denominator"]),
                "epsilon_star": mca_conclusion["epsilon_star"],
            },
        },
        "checks": checks,
        "remaining_imports": [
            "official ABF PDF/source verification for the row gates, sampler, "
            "smoothness, same-support predicate, and closed threshold; the "
            "separate ABF extract-source audit hash-binds the PR #96 extract "
            "objects but does not close official ePrint review",
            "reviewer acceptance of the Cycle84 finite-source closure audit for "
            "promotion beyond audit status",
            "official review of the external PR #96 provenance if that packet is "
            "cited directly; the local fixed-jet theorem and transfer audits now "
            "cover the proof-logic core, while source-hash and transfer-replay "
            "audits check contract-to-Git binding and executable output",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    chain = report["chain"]
    cycle84_chain = chain["cycle84_exact_occupancy"]
    assembly = chain["cycle116_slot_assembly"]
    external = chain["cycle116_external_packet_contract"]
    native = chain["cycle116_native"]
    transfer = chain["cycle116_fixed_jet_transfer"]
    lifted = chain["cycle116_smooth_lift"]
    theorem = chain["fixed_jet_ldsw_theorem"]
    ledger = chain["cycle120_domain_field_ledger"]
    gate_chain = chain["cycle120_gate_arithmetic"]
    mca = chain["cycle120_supportwise_mca"]

    print("m1_cycle120_end_to_end_chain: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(
        "cycle84="
        f"N={cycle84_chain['distinct_products']}, "
        f"energy={cycle84_chain['true_ordered_energy']}, "
        f"m_max={cycle84_chain['m_max']}, "
        f"digest={cycle84_chain['slot_table_digest']}"
    )
    print(
        "cycle116_assembly="
        f"cosupport={assembly['cosupport_size']}, "
        f"blocks={assembly['slot_block_count']}, "
        f"block_size={assembly['slot_block_size']}, "
        f"all_tuples={assembly['all_tuple_count']}"
    )
    print(
        "cycle116_external_packet="
        f"PR #{external['provenance']['pull_request']} "
        f"{external['provenance']['head_ref']}, "
        f"state_count={external['state_count']}, co_support={external['co_support']}"
    )
    print(
        "cycle116_native="
        f"n={native['domain_size']}, k={native['dimension']}, "
        f"agreement={native['agreement']}, bad_parameters={native['bad_line_parameters']}"
    )
    print(
        "cycle116_fixed_jet_transfer="
        f"{transfer['complement_locator_truncation']}, "
        f"q_degree={transfer['representative_q_degree']}, "
        f"formula={transfer['bad_parameter_formula']}"
    )
    print(
        "cycle116_lift="
        f"{lifted['field']}, n={lifted['domain_size']}, "
        f"k={lifted['dimension']}, agreement={lifted['agreement']}, "
        f"delta={lifted['delta']}, A={lifted['padding']['A_size']}, "
        f"R={lifted['padding']['R_size']}"
    )
    print(
        "fixed_jet_ldsw_theorem="
        f"{theorem['proof_status']}, toy_cases={theorem['toy_case_count']}, "
        f"native_bad_parameters={theorem['native_bad_parameters']}"
    )
    print(
        "cycle120_field_ledger="
        f"{ledger['lift_generator']} generates degree "
        f"{ledger['lift_generated_degree']}, q_gen=q_code=q_line={ledger['q_line']}"
    )
    print(
        "cycle120_gate="
        f"threshold={gate_chain['closed_agreement_threshold']}, "
        f"minimum_bad_count={gate_chain['minimum_bad_gamma_count_for_gt_2_minus_128']}, "
        f"density={gate_chain['density_comparison']}"
    )
    print(
        "cycle120_supportwise_mca="
        f"{mca['numerator']} / {mca['denominator']} > {mca['epsilon_star']}"
    )
    print("remaining_imports=" + "; ".join(report["remaining_imports"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the composed M1 Cycle120 finite chain."
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
