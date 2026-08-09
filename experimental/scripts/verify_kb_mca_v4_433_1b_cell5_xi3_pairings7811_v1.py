#!/usr/bin/env python3
"""Verify or assemble the experimental cell-5 xi=3 pairings 7/8/11 packet."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = ROOT / (
    "experimental/data/certificates/"
    "kb-mca-v4-433-1b-cell5-xi3-pairings7811-v1/"
    "kb_mca_v4_433_1b_cell5_xi3_pairings7811_v1.json"
)
PRIME = 2_130_706_433
SOURCE_COMMIT = "28b3bc8ab13e94c25088e904251eb5cf49e68ad2"
SOURCE_HASHES = {
    "template_7": "ed5c0a3883180e43e2f380fc76971a4a645fe0260679ed27374cd2bfc844d2df",
    "template_8": "58ed9e191436e0a629d2c7a263151d50d54910d226eee4c35c0bb55abf2a1b8b",
    "template_11": "8f2fe8ca53863b2220ae60558b3f8d64269eec0f3952138679f2bc3a7069698b",
    "tower": "68c18173d4133f66a85136b1ecc33235f7e979c26b6f96d8592030901a8a335c",
    "kernel": "627a8df8bb8a2da4e11488658d1c2145b8c65ef7fbcef3f0f4f53f9d05ea752d",
}
EXPECTED_WOLFRAM_CHECK = {
    "quadratic_resultant_difference": 0,
    "sign_free_product": "ee^2 - oo^2*y",
    "sign_free_identity": True,
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
    "7": {
        "rows": 8,
        "target_norm_root_count": 44,
        "candidate_root_count": 100,
        "source_point_count": 96,
        "route_point_count": 96,
        "z_candidate_count": 8,
        "q_candidate_count": 8,
        "final_pair_solution_count": 0,
        "witness_count": 0,
        "boundary_rows": 72,
        "target_boundary_rows": 16,
        "no_lift_rows": 40,
    },
    "8": {
        "rows": 8,
        "target_norm_root_count": 44,
        "candidate_root_count": 100,
        "source_point_count": 96,
        "route_point_count": 96,
        "z_candidate_count": 8,
        "q_candidate_count": 8,
        "final_pair_solution_count": 0,
        "witness_count": 0,
        "boundary_rows": 72,
        "target_boundary_rows": 16,
        "no_lift_rows": 40,
    },
    "11": {
        "rows": 8,
        "target_norm_root_count": 52,
        "candidate_root_count": 108,
        "source_point_count": 120,
        "route_point_count": 120,
        "z_candidate_count": 24,
        "q_candidate_count": 24,
        "final_pair_solution_count": 0,
        "witness_count": 0,
        "boundary_rows": 72,
        "target_boundary_rows": 16,
        "no_lift_rows": 44,
    },
}


class VerificationError(RuntimeError):
    pass


def canonical_sha256(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def expected_cases() -> list[tuple[int, tuple[int, int], int, int]]:
    cases = []
    index = 0
    for pairing in (7, 8, 11):
        for epsilon in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
            for sigma_c in (-1, 1):
                cases.append((index, epsilon, pairing, sigma_c))
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
        "sigma_c": row["sigma_c"],
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
    for pairing in (7, 8, 11):
        selected = [row for row in rows if row["pairing_index"] == pairing]
        result[str(pairing)] = {
            "rows": len(selected),
            **{key: sum(row[key] for row in selected) for key in COUNT_KEYS},
            "boundary_rows": sum(row["boundary_rows"] for row in selected),
            "target_boundary_rows": sum(row["target_boundary_rows"] for row in selected),
            "no_lift_rows": sum(row["no_lift_rows"] for row in selected),
        }
    return result


def verify(payload: dict) -> None:
    if payload.get("schema") != "kb-mca-v4-433-1b-cell5-xi3-pairings7811-v1":
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
    if not isinstance(rows, list) or len(rows) != 24:
        raise VerificationError("expected exactly 24 rows")
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
    if payload.get("cell_5_8_role_orbit_closed") is not False:
        raise VerificationError("fresh review is required before orbit closure")
    if payload.get("K3_closed") is not False:
        raise VerificationError("packet cannot close K3")
    if payload.get("KoalaBear_row_closed") is not False:
        raise VerificationError("packet cannot close the KoalaBear row")


def assemble(parts_directory: Path) -> dict:
    files = sorted(
        parts_directory.glob("cell5_xi3_7811_part_*.json"),
        key=lambda path: int(path.stem.rsplit("_", 1)[1]),
    )
    raw_rows = []
    for path in files:
        part = json.loads(path.read_text())
        if part.get("field") != PRIME or part.get("source_commit") != SOURCE_COMMIT:
            raise VerificationError(f"raw-part provenance mismatch: {path}")
        if part.get("source_sha256") != SOURCE_HASHES:
            raise VerificationError(f"raw-part source hash mismatch: {path}")
        raw_rows.extend(part["rows"])
    raw_rows.sort(key=lambda row: row["local_case_index"])
    rows = [row_projection(row) for row in raw_rows]
    payload = {
        "schema": "kb-mca-v4-433-1b-cell5-xi3-pairings7811-v1",
        "field": PRIME,
        "workboard_item": "K3",
        "row": "KoalaBear MCA at target epsilon 2^-128",
        "object": "MCA",
        "target_epsilon": "2^-128",
        "agreement": 1_116_048,
        "B_star": 274_980_728_111_395_087,
        "direct_statement": (
            "On the guarded product-rank-five positive 433-1b to O0a "
            "source-role cell-5 route over F_2130706433, the xi=3 pairing "
            "representatives 7, 8, and 11 are empty in all 24 signed rows."
        ),
        "architecture": "K3 coordinate-positive 433-1b source-role workboard",
        "partition_digest": "public-DAG-433-1b-router@28b3bc8a",
        "atom_or_cell": "source-role cell 5; xi=3; pairings 7,8,11",
        "quantifier": "all 24 exact source/colored sign rows listed in the certificate",
        "projection_and_unit": "local matching labels; not yet a v4 slope atom",
        "claimed_bound": "zero witnesses in the declared local cells",
        "status": "EXPERIMENTAL_REVIEW_REQUIRED",
        "impact": "ROUTE_CUT",
        "relationship_to_upstream": (
            "Independent public-source replay of the xi=3 cell-5 pairing "
            "subfrontier cited by rs-mca PR #1152; it does not replace that "
            "PR's endpoint or cell-5-to-cell-8 transport nodes."
        ),
        "falsifier": (
            "any covered row with a witness, final pair solution, unresolved "
            "branch, unhandled degree-drop boundary, or source-hash mismatch"
        ),
        "provenance": {
            "source_repo": "https://github.com/AllenGrahamHart/rs-mca-prize-dag",
            "source_commit": SOURCE_COMMIT,
            "source_sha256": SOURCE_HASHES,
            "part_sha256": {
                path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                for path in files
            },
            "compute": "local python-flint 0.8.0 and SymPy 1.14.0; no hosted upload",
        },
        "summary": summarize(rows),
        "independent_checks": {
            "wolfram": EXPECTED_WOLFRAM_CHECK,
            "method_note": (
                "Wolfram independently simplified the quadratic Sylvester "
                "resultant difference to zero and the conjugate product to "
                "E^2-y O^2 under z^2=y."
            ),
            "branch_method_reference": (
                "Chen--Moreno Maza, JSC 47 (2012), Theorems 4--6: "
                "subresultant specialization and degree-drop corner cases"
            ),
        },
        "rows": rows,
        "ledger_movement": 0,
        "cell_5_8_role_orbit_closed": False,
        "K3_closed": False,
        "KoalaBear_row_closed": False,
        "nonclaims": [
            "No v4 U_paid, U_Q, U_BC, or U_new value is changed.",
            "The source-role-to-cell-8 transport and exact labeled add-back remain to be independently audited.",
            "Pairings 3, 4, and 5 live in the predecessor packet and are not re-proved here.",
            "This packet does not validate the endpoint and duplicate-role transport nodes cited by PR #1152.",
            "The old FLOOR v2 random-word first-moment route is not used; this packet says nothing about S_sparse.",
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
    add("final_pair", lambda value: value["rows"][0].__setitem__("final_pair_solution_count", 1))
    add("unresolved", lambda value: value["rows"][0].__setitem__("unresolved_count", 1))
    add("excluded", lambda value: value["rows"][0].__setitem__("target_excluded", False))
    add("summary", lambda value: value["summary"]["11"].__setitem__("rows", 9))
    add("wolfram", lambda value: value["independent_checks"]["wolfram"].__setitem__("sign_free_identity", False))
    add("ledger", lambda value: value.__setitem__("ledger_movement", 1))
    add("promotion", lambda value: value.__setitem__("cell_5_8_role_orbit_closed", True))
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
        print(f"mutations: PASS ({mutation_tests(payload)}/12 rejected)")


if __name__ == "__main__":
    main()
