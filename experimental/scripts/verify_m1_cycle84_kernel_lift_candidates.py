#!/usr/bin/env python3
"""Verify the Cycle84 kernel-lift candidates for projected duplicate bins.

This nonmutating verifier supports
experimental/notes/m1/m1_cycle116_finite_chain_contract.md. It checks the
30 projected duplicate-bin lift candidates against the current normalized
Cycle116 slot table. For each candidate it verifies:

* both normalized tuples lie in the color-4 shell;
* the supplied full logs exponentiate to the tuple products;
* the two logs are congruent modulo M=(17^16-1)/3;
* the kernel difference decides exactly whether the products are equal.

The remaining imported computation is the projected tau-folded census asserting
that these 30 bins are the complete projected duplicate list and each has count
2. This script verifies the kernel lift/filtering once that projected census is
accepted.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Sequence, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import verify_m1_cycle84_color_collision_witnesses as color_witness
import verify_m1_cycle84_projected_log_certificate as log_cert
import verify_m1_cycle116_slot_identities as slot


N = 17**16 - 1
M = N // 3
TARGET_COLOR = 4

PROJECTED_LIFT_CANDIDATES = [
    (179351812256751797, 2, False, [15, 11, 30, 14, 36, 31, 19], 40288745001897324571, [36, 28, 14, 21, 46, 38, 5], 7847950418119412251),
    (179795084433593580, 2, False, [30, 21, 14, 28, 5, 36, 2], 7848393690296254034, [9, 28, 7, 36, 24, 1, 25], 24068790982185210194),
    (222915557520769006, 2, False, [30, 21, 14, 44, 2, 23, 2], 7891514163383429460, [9, 28, 7, 6, 27, 44, 25], 24111911455272385620),
    (254958237482354612, 2, False, [15, 11, 30, 14, 38, 31, 19], 7923556843345015066, [36, 28, 14, 21, 44, 38, 5], 24143954135233971226),
    (1871222699767544580, 2, False, [15, 11, 20, 14, 36, 31, 19], 9539821305630205034, [36, 28, 8, 21, 46, 38, 5], 25760218597519161194),
    (1946829124993147395, 2, False, [15, 11, 20, 14, 38, 31, 19], 25835825022744764009, [36, 28, 8, 21, 44, 38, 5], 42056222314633720169),
    (2115829786642026153, 2, False, [15, 6, 30, 15, 36, 31, 19], 26004825684393642767, [36, 17, 14, 20, 46, 38, 5], 42225222976282598927),
    (2191436211867628968, 2, False, [15, 6, 30, 15, 38, 31, 19], 42300829401508201742, [36, 17, 14, 20, 44, 38, 5], 9860034817730289422),
    (2752876908959724607, 1, False, [8, 28, 7, 6, 24, 44, 25], 42862270098600297381, [31, 21, 14, 44, 5, 23, 2], 26641872806711341221),
    (3173541850524071265, 0, True, [4, 26, 46, 12, 32, 22, 40], 10842140456386731719, [16, 27, 7, 1, 41, 24, 14], 10842140456386731719),
    (3275293692624999094, 0, True, [26, 27, 7, 1, 41, 24, 14], 10943892298487659548, [10, 26, 46, 12, 32, 22, 40], 10943892298487659548),
    (3807700674152818936, 2, False, [15, 6, 20, 15, 36, 31, 19], 43917093863793391710, [36, 17, 8, 20, 46, 38, 5], 11476299280015479390),
    (3834149319236634720, 2, False, [15, 11, 30, 14, 36, 31, 27], 43943542508877207494, [36, 28, 14, 21, 46, 38, 13], 11502747925099295174),
    (3861193039733633404, 2, False, [30, 21, 14, 44, 5, 23, 3], 11529791645596293858, [9, 28, 7, 6, 24, 44, 24], 27750188937485250018),
    (3883307099378421751, 2, False, [15, 6, 20, 15, 38, 31, 19], 11551905705241082205, [36, 17, 8, 20, 44, 38, 5], 27772302997130038365),
    (3909755744462237535, 2, False, [15, 11, 30, 14, 38, 31, 27], 11578354350324897989, [36, 28, 14, 21, 44, 38, 13], 27798751642213854149),
    (4992786929752216345, 2, False, [30, 6, 29, 28, 5, 36, 2], 28881782827503832959, [9, 15, 20, 36, 24, 1, 25], 45102180119392789119),
    (5035907402839391771, 2, False, [30, 6, 29, 44, 2, 23, 2], 28924903300591008385, [9, 15, 20, 6, 27, 44, 25], 45145300592479964545),
    (5526020206747427503, 2, False, [15, 11, 20, 14, 36, 31, 27], 13194618812610087957, [36, 28, 8, 21, 46, 38, 13], 29415016104499044117),
    (5601626631973030318, 2, False, [15, 11, 20, 14, 38, 31, 27], 29490622529724646932, [36, 28, 8, 21, 44, 38, 13], 45711019821613603092),
    (5770627293621909076, 2, False, [15, 6, 30, 15, 36, 31, 27], 29659623191373525690, [36, 17, 14, 20, 46, 38, 13], 45880020483262481850),
    (5846233718847511891, 2, False, [15, 6, 30, 15, 38, 31, 27], 45955626908488084665, [36, 17, 14, 20, 44, 38, 13], 13514832324710172345),
    (6514369406671509109, 0, True, [4, 26, 46, 23, 33, 2, 40], 30403365304423125723, [16, 27, 7, 18, 40, 0, 14], 30403365304423125723),
    (6616121248772436938, 0, True, [26, 27, 7, 18, 40, 0, 14], 30505117146524053552, [10, 26, 46, 23, 33, 2, 40], 30505117146524053552),
    (6733442005186036094, 0, True, [4, 26, 29, 12, 33, 2, 20], 46842835194826608868, [16, 27, 38, 1, 40, 0, 32], 46842835194826608868),
    (6835193847286963923, 0, True, [26, 27, 38, 1, 40, 0, 32], 46944587036927536697, [10, 26, 29, 12, 33, 2, 20], 46944587036927536697),
    (7462498181132701859, 2, False, [15, 6, 20, 15, 36, 31, 27], 47571891370773274633, [36, 17, 8, 20, 46, 38, 13], 15131096786995362313),
    (7538104606358304674, 2, False, [15, 6, 20, 15, 38, 31, 27], 15206703212220965128, [36, 17, 8, 20, 44, 38, 13], 31427100504109921288),
    (7546212406836699991, 1, False, [8, 28, 7, 36, 27, 1, 25], 31435208304588316605, [31, 21, 14, 28, 2, 36, 2], 15214811012699360445),
    (7565868754278347372, 1, False, [8, 15, 20, 6, 24, 44, 25], 15234467360141007826, [31, 6, 29, 44, 5, 23, 2], 47675261943918920146),
]


FieldElt = Tuple[int, ...]


def tuple_product(keys: Sequence[int], table: Dict[Tuple[int, int], FieldElt]) -> FieldElt:
    return color_witness.tuple_product(keys, table)


def verify_candidate(
    candidate: Tuple[int, int, bool, list[int], int, list[int], int],
    table: Dict[Tuple[int, int], FieldElt],
) -> Tuple[bool, int]:
    _, kernel_difference, true_collision, tuple_a, log_a, tuple_b, log_b = candidate

    keys_a = tuple(tuple_a)
    keys_b = tuple(tuple_b)
    if color_witness.color_sum(keys_a) != TARGET_COLOR:
        raise AssertionError((keys_a, "wrong color"))
    if color_witness.color_sum(keys_b) != TARGET_COLOR:
        raise AssertionError((keys_b, "wrong color"))

    product_a = tuple_product(keys_a, table)
    product_b = tuple_product(keys_b, table)
    if slot.fpow(slot.BETA, log_a) != product_a:
        raise AssertionError((keys_a, "bad log"))
    if slot.fpow(slot.BETA, log_b) != product_b:
        raise AssertionError((keys_b, "bad log"))

    diff = (log_a - log_b) % N
    if diff % M != 0:
        raise AssertionError((keys_a, keys_b, "not projected collision"))
    if diff // M != kernel_difference:
        raise AssertionError((keys_a, keys_b, "wrong kernel difference"))
    if (product_a == product_b) != true_collision:
        raise AssertionError((keys_a, keys_b, "wrong true-collision flag"))
    if true_collision != (kernel_difference == 0):
        raise AssertionError((keys_a, keys_b, "kernel/product mismatch"))

    return true_collision, 2 if true_collision else 0


def build_report() -> Dict[str, Any]:
    slot_report = slot.build_report()
    log_report = log_cert.build_report()
    table = color_witness.build_slot_values()

    seen_keys = set()
    seen_tuples = set()
    true_orbits = 0
    ordered_energy = 0
    false_candidates = 0
    kernel_histogram: Dict[str, int] = {}

    for candidate in PROJECTED_LIFT_CANDIDATES:
        canonical_key = candidate[0]
        kernel_difference = candidate[1]
        if canonical_key in seen_keys:
            raise AssertionError(("duplicate canonical key", canonical_key))
        seen_keys.add(canonical_key)
        seen_tuples.add(tuple(candidate[3]))
        seen_tuples.add(tuple(candidate[5]))

        is_true, energy = verify_candidate(candidate, table)
        true_orbits += int(is_true)
        false_candidates += int(not is_true)
        ordered_energy += energy
        kernel_histogram[str(kernel_difference)] = (
            kernel_histogram.get(str(kernel_difference), 0) + 1
        )

    checks = {
        "slot_identity_replay_passes": slot_report["status"] == "PASS",
        "projected_log_certificate_passes": log_report["status"] == "PASS",
        "projected_duplicate_bins_checked": len(PROJECTED_LIFT_CANDIDATES) == 30,
        "canonical_keys_distinct": len(seen_keys) == 30,
        "normalized_tuples_distinct": len(seen_tuples) == 60,
        "true_collision_orbits_6": true_orbits == 6,
        "false_projected_collisions_24": false_candidates == 24,
        "oriented_true_energy_12": ordered_energy == 12,
        "kernel_histogram_matches": kernel_histogram == {"0": 6, "1": 3, "2": 21},
    }

    # Each true tau orbit has two true product fibers after applying tau, so
    # ordered off-diagonal energy is twice the oriented energy counted above.
    true_double_fibers = 2 * true_orbits
    true_ordered_energy = 2 * ordered_energy
    if true_ordered_energy != 24:
        raise AssertionError(("bad true ordered energy", true_ordered_energy))

    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": "AUDIT / FINITE-MODEL-KERNEL-LIFT-VERIFIED / CONDITIONAL",
        "theorem_problem_id": "M1 Cycle84 kernel lift candidates",
        "slot_table_digest": slot_report["slot_table"]["digest_sha256"],
        "projected_log_certificate_sha256": log_report["certificate_sha256"],
        "projected_lift": {
            "projected_duplicate_bins_checked": len(PROJECTED_LIFT_CANDIDATES),
            "normalized_witnesses_checked": len(seen_tuples),
            "true_collision_tau_orbits": true_orbits,
            "true_double_fibers_after_tau": true_double_fibers,
            "true_ordered_energy_after_tau": true_ordered_energy,
            "kernel_difference_histogram": kernel_histogram,
        },
        "remaining_import": (
            "projected tau-folded census completeness: exactly these 30 "
            "duplicate bins, each with count 2"
        ),
        "checks": checks,
        "imports_required": [
            "projected tau-folded duplicate-bin completeness",
            "official ABF source gate verification",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    lift = report["projected_lift"]

    print("m1_cycle84_kernel_lift_candidates: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(f"slot_table_digest={report['slot_table_digest']}")
    print(
        "projected_lift="
        f"bins={lift['projected_duplicate_bins_checked']}, "
        f"witnesses={lift['normalized_witnesses_checked']}, "
        f"true_tau_orbits={lift['true_collision_tau_orbits']}, "
        f"double_fibers={lift['true_double_fibers_after_tau']}, "
        f"true_energy={lift['true_ordered_energy_after_tau']}, "
        f"kernel_histogram={lift['kernel_difference_histogram']}"
    )
    print(f"remaining_import={report['remaining_import']}")
    print("imports_required=" + "; ".join(report["imports_required"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify Cycle84 kernel-lift candidates."
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
