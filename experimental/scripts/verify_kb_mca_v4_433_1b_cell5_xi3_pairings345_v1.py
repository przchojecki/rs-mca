#!/usr/bin/env python3
"""Verify or assemble the experimental cell-5 xi=3 pairings 3-5 packet."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = ROOT / (
    "experimental/data/certificates/"
    "kb-mca-v4-433-1b-cell5-xi3-pairings345-v1/"
    "kb_mca_v4_433_1b_cell5_xi3_pairings345_v1.json"
)
PRIME = 2_130_706_433
SOURCE_COMMIT = "28b3bc8ab13e94c25088e904251eb5cf49e68ad2"
SOURCE_HASHES = {
    "template_3": "ed1133214b5126f59279ccc75b91f4a572ef9cb62d6b24d8c84df8377da4ce5c",
    "template_4": "0992beedc8d85e1d7e510d40dadccd72d01e8b38325d9e6fe56c741ab50711fd",
    "template_5": "f1dd2096b7dfb7cf6a4a784ae04ef5a0fbd8b6e91f5bfa21bd584d990625f342",
    "tower": "68c18173d4133f66a85136b1ecc33235f7e979c26b6f96d8592030901a8a335c",
    "kernel": "627a8df8bb8a2da4e11488658d1c2145b8c65ef7fbcef3f0f4f53f9d05ea752d",
}
EXPECTED_WOLFRAM_CHECK = {
    "case_index": 0,
    "classification": "NO_B_ROOT",
    "r": 396_444_866,
    "t": 310_013_572,
    "b_coefficients_constant_to_quadratic": [
        1_629_468_848,
        1_735_544_835,
        1_629_468_848,
    ],
    "discriminant": 1_527_757_769,
    "euler_value": 2_130_706_432,
    "prime_q": True,
}
COUNT_KEYS = (
    "target_norm_root_count",
    "candidate_root_count",
    "source_point_count",
    "route_point_count",
    "z_candidate_count",
    "q_candidate_count",
    "final_pair_solution_count",
    "witness_count",
)
EXPECTED_SUMMARY = {
    "3": {
        "rows": 8,
        "target_norm_root_count": 32,
        "candidate_root_count": 88,
        "source_point_count": 80,
        "route_point_count": 80,
        "z_candidate_count": 0,
        "q_candidate_count": 0,
        "final_pair_solution_count": 0,
        "witness_count": 0,
        "boundary_rows": 72,
        "target_boundary_rows": 16,
        "no_lift_rows": 24,
    },
    "4": {
        "rows": 4,
        "target_norm_root_count": 40,
        "candidate_root_count": 80,
        "source_point_count": 144,
        "route_point_count": 144,
        "z_candidate_count": 24,
        "q_candidate_count": 24,
        "final_pair_solution_count": 0,
        "witness_count": 0,
        "boundary_rows": 36,
        "target_boundary_rows": 8,
        "no_lift_rows": 32,
    },
    "5": {
        "rows": 8,
        "target_norm_root_count": 48,
        "candidate_root_count": 128,
        "source_point_count": 208,
        "route_point_count": 208,
        "z_candidate_count": 0,
        "q_candidate_count": 0,
        "final_pair_solution_count": 0,
        "witness_count": 0,
        "boundary_rows": 72,
        "target_boundary_rows": 16,
        "no_lift_rows": 40,
    },
}


class VerificationError(RuntimeError):
    pass


def canonical_sha256(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def expected_cases() -> list[tuple[int, tuple[int, int], int, int | None]]:
    signs = ((-1, -1), (-1, 1), (1, -1), (1, 1))
    cases: list[tuple[int, tuple[int, int], int, int | None]] = []
    index = 0
    for epsilon in signs:
        for sigma_c in (-1, 1):
            cases.append((index, epsilon, 3, sigma_c))
            index += 1
    for epsilon in signs:
        cases.append((index, epsilon, 4, None))
        index += 1
    for epsilon in signs:
        for sigma_c in (-1, 1):
            cases.append((index, epsilon, 5, sigma_c))
            index += 1
    return cases


def row_projection(row: dict) -> dict:
    raw = dict(row)
    raw.pop("local_elapsed_seconds", None)
    raw.pop("local_case_index", None)
    return {
        "case_index": row["local_case_index"],
        "epsilon": row["epsilon"],
        "pairing_index": row["pairing_index"],
        "sigma_c": row.get("sigma_c"),
        "status": row["status"],
        **{key: row.get(key, 0) for key in COUNT_KEYS},
        "boundary_rows": len(row.get("boundary_rows", [])),
        "target_boundary_rows": len(row.get("target_boundary_rows", [])),
        "no_lift_rows": len(row.get("no_lift_rows", [])),
        "unresolved_count": len(row.get("unresolved", [])),
        "target_excluded": row.get("target_excluded"),
        "raw_row_sha256": canonical_sha256(raw),
    }


def summarize(rows: list[dict]) -> dict:
    result = {}
    for pairing in (3, 4, 5):
        selected = [row for row in rows if row["pairing_index"] == pairing]
        result[str(pairing)] = {
            "rows": len(selected),
            **{key: sum(row[key] for row in selected) for key in COUNT_KEYS},
            "boundary_rows": sum(row["boundary_rows"] for row in selected),
            "target_boundary_rows": sum(
                row["target_boundary_rows"] for row in selected
            ),
            "no_lift_rows": sum(row["no_lift_rows"] for row in selected),
        }
    return result


def verify(payload: dict) -> None:
    if payload.get("schema") != "kb-mca-v4-433-1b-cell5-xi3-pairings345-v1":
        raise VerificationError("schema mismatch")
    if payload.get("field") != PRIME:
        raise VerificationError("field mismatch")
    if payload.get("status") != "EXPERIMENTAL_REVIEW_REQUIRED":
        raise VerificationError("status promotion or mismatch")
    provenance = payload.get("provenance", {})
    if provenance.get("source_commit") != SOURCE_COMMIT:
        raise VerificationError("source commit mismatch")
    if provenance.get("source_sha256") != SOURCE_HASHES:
        raise VerificationError("source hash mismatch")

    rows = payload.get("rows")
    if not isinstance(rows, list) or len(rows) != 20:
        raise VerificationError("expected exactly 20 rows")
    observed_cases = [
        (
            row.get("case_index"),
            tuple(row.get("epsilon", [])),
            row.get("pairing_index"),
            row.get("sigma_c"),
        )
        for row in rows
    ]
    if observed_cases != expected_cases():
        raise VerificationError("case order, coverage, or uniqueness mismatch")
    for row in rows:
        if row.get("status") != "COMPLETE":
            raise VerificationError("incomplete row")
        if row.get("witness_count") != 0:
            raise VerificationError("witness found")
        if row.get("final_pair_solution_count") != 0:
            raise VerificationError("final pair solution found")
        if row.get("unresolved_count") != 0:
            raise VerificationError("unresolved branch")
        if row.get("target_excluded") is not True:
            raise VerificationError("target not excluded")
        digest = row.get("raw_row_sha256", "")
        if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
            raise VerificationError("invalid raw-row digest")
    if summarize(rows) != EXPECTED_SUMMARY:
        raise VerificationError("aggregate mismatch")
    if payload.get("summary") != EXPECTED_SUMMARY:
        raise VerificationError("printed summary mismatch")
    if payload.get("independent_checks", {}).get("wolfram") != EXPECTED_WOLFRAM_CHECK:
        raise VerificationError("Wolfram cross-check mismatch")
    if payload.get("ledger_movement") != 0:
        raise VerificationError("local route cut cannot move the v4 ledger")
    if payload.get("K3_closed") is not False:
        raise VerificationError("packet cannot close K3")
    if payload.get("KoalaBear_row_closed") is not False:
        raise VerificationError("packet cannot close the KoalaBear row")


def assemble(parts_directory: Path) -> dict:
    files = sorted(
        parts_directory.glob("cell5_xi3_part_*.json"),
        key=lambda path: int(path.stem.rsplit("_", 1)[1]),
    )
    raw_rows = []
    for path in files:
        part = json.loads(path.read_text())
        raw_rows.extend(part["rows"])
    raw_rows.sort(key=lambda row: row["local_case_index"])
    rows = [row_projection(row) for row in raw_rows]
    payload = {
        "schema": "kb-mca-v4-433-1b-cell5-xi3-pairings345-v1",
        "field": PRIME,
        "workboard_item": "K3",
        "row": "KoalaBear MCA at target epsilon 2^-128",
        "object": "MCA",
        "target_epsilon": "2^-128",
        "agreement": 1_116_048,
        "B_star": 274_980_728_111_395_087,
        "direct_statement": (
            "On the guarded product-rank-five positive 433-1b to O0a "
            "source-role cell-5 route over F_2130706433, the xi=3 "
            "pairing representatives 3, 4, and 5 are empty in all required "
            "source and colored sign rows."
        ),
        "architecture": "K3 coordinate-positive 433-1b source-role workboard",
        "partition_digest": "public-DAG-433-1b-router@28b3bc8a",
        "atom_or_cell": "source-role cell 5; xi=3; pairings 3,4,5",
        "quantifier": "all 20 exact signed rows listed in the certificate",
        "projection_and_unit": "local matching labels; not yet a v4 slope atom",
        "claimed_bound": "zero witnesses in the declared local cells",
        "status": "EXPERIMENTAL_REVIEW_REQUIRED",
        "impact": "ROUTE_CUT",
        "falsifier": (
            "any covered row with a witness, final pair solution, unresolved "
            "branch, unhandled degree-drop boundary, or source-hash mismatch"
        ),
        "provenance": {
            "source_repo": "https://github.com/AllenGrahamHart/rs-mca-prize-dag",
            "source_commit": SOURCE_COMMIT,
            "source_sha256": SOURCE_HASHES,
            "part_sha256": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files},
            "compute": "local python-flint 0.8.0 and SymPy 1.14.0; no hosted upload",
        },
        "summary": summarize(rows),
        "independent_checks": {
            "wolfram": EXPECTED_WOLFRAM_CHECK,
            "method_note": (
                "Wolfram independently evaluated the representative b "
                "quadratic, discriminant, Euler criterion, and PrimeQ[p]."
            ),
            "branch_method_reference": (
                "Chen--Moreno Maza, JSC 47 (2012), Theorems 4--6: "
                "subresultant specialization and degree-drop corner cases"
            ),
        },
        "rows": rows,
        "ledger_movement": 0,
        "K3_closed": False,
        "KoalaBear_row_closed": False,
        "nonclaims": [
            "No v4 U_paid, U_Q, U_BC, or U_new value is changed.",
            "The source-role-to-cell-8 transport and exact labeled add-back remain to be independently audited.",
            "The remaining xi=3 pairings 7, 8, and 11 are not claimed.",
            "This packet is generated by the same model that wrote the adapter and therefore requires fresh independent review.",
        ],
    }
    verify(payload)
    return payload


def mutation_tests(payload: dict) -> int:
    mutations = []
    def add(name, mutate):
        candidate = copy.deepcopy(payload)
        mutate(candidate)
        mutations.append((name, candidate))

    add("field", lambda value: value.__setitem__("field", PRIME - 2))
    add("source", lambda value: value["provenance"].__setitem__("source_commit", "0" * 40))
    add("duplicate", lambda value: value["rows"].__setitem__(1, copy.deepcopy(value["rows"][0])))
    add("status", lambda value: value["rows"][0].__setitem__("status", "INCOMPLETE"))
    add("witness", lambda value: value["rows"][0].__setitem__("witness_count", 1))
    add("unresolved", lambda value: value["rows"][0].__setitem__("unresolved_count", 1))
    add("excluded", lambda value: value["rows"][0].__setitem__("target_excluded", False))
    add("summary", lambda value: value["summary"]["4"].__setitem__("rows", 5))
    add("wolfram", lambda value: value["independent_checks"]["wolfram"].__setitem__("euler_value", 1))
    add("ledger", lambda value: value.__setitem__("ledger_movement", 1))
    rejected = 0
    for name, candidate in mutations:
        try:
            verify(candidate)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"mutation accepted: {name}")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--assemble-dir", type=Path)
    parser.add_argument("--mutations", action="store_true")
    arguments = parser.parse_args()
    if arguments.assemble_dir:
        payload = assemble(arguments.assemble_dir)
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    else:
        payload = json.loads(CERTIFICATE.read_text())
        verify(payload)
    print("certificate: PASS")
    if arguments.mutations:
        print(f"mutations: PASS ({mutation_tests(payload)}/10 rejected)")


if __name__ == "__main__":
    main()
