#!/usr/bin/env python3
"""Verify the degree-60 primitive-subdegree-four K3 route cut.

The group catalogue is replayed independently by the companion Sage/GAP
script.  This Python verifier binds the exact catalogue output, checks the
functional-decomposition pole-profile ladder, rejects duplicate JSON keys,
and runs mutation tests.  It does not replace the imported component-to-
self-correspondence theorem or the primitive-group classification.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


if not __debug__:
    raise RuntimeError("verifier refuses optimized Python execution")


class VerificationError(RuntimeError):
    """Raised when a certificate condition fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
CERTIFICATE = (
    ROOT
    / "data"
    / "certificates"
    / "kb-mca-v4-degree60-primitive-subdegree4-route-cut-v1"
    / "kb_mca_v4_degree60_primitive_subdegree4_route_cut_v1.json"
)
WOLFRAM_REPLAY = (
    ROOT
    / "scripts"
    / "verify_kb_mca_v4_degree60_primitive_subdegree4_route_cut_v1.wl"
)
PARENT_CERTIFICATE = (
    ROOT
    / "data"
    / "certificates"
    / "kb-mca-v4-q6-u2-complete-source-conic-exclusion-v1"
    / "kb_mca_v4_q6_u2_complete_source_conic_exclusion_v1.json"
)

EXPECTED_ROW = "KoalaBear MCA at 2^-128"
EXPECTED_AGREEMENT = 1116048
EXPECTED_B_STAR = "274980728111395087"
EXPECTED_CHARACTERISTIC = 2130706433
EXPECTED_CLASSIFICATION_SCOPE = (
    "geometric primitive monodromy over the algebraic closure"
)
EXPECTED_PARENT_HEAD = "ad109774f7d9bc320e7e0c046ba83471f39d5cd9"
EXPECTED_PARENT_PATH = (
    "experimental/data/certificates/"
    "kb-mca-v4-q6-u2-complete-source-conic-exclusion-v1/"
    "kb_mca_v4_q6_u2_complete_source_conic_exclusion_v1.json"
)
EXPECTED_PARENT_BLOB = "61afd4534740c5ccabc6196919126c80c361e4c5"
EXPECTED_PARENT_PAYLOAD = (
    "30a5d45895957f774ef972118e227fa54522fc27a48ee0e2a99a0d5a012a5451"
)
EXPECTED_SOURCE_COMMIT = "44542e91e459364a521870ed2ebde7f6fe5055bf"
EXPECTED_SOURCE_PATH = (
    "experimental/notes/frontier-adjacent/"
    "kb_mca_v4_equality_wall_geometry_v1/proof/"
    "pole_disjoint_conic_facet_collinearity_reduction.md"
)
EXPECTED_SOURCE_BLOB = "356ff4b47d0bb429d11ea10382762a6e95b5ce24"
EXPECTED_INTEGRATION_COMMIT = "0f7476f0fcbc5d1a1d3eed0c03221aaa48f5767d"
EXPECTED_NONCLAIMS = [
    "no exclusion of geometrically decomposable endpoint maps",
    "no domain-compatible witness-data descent",
    "no chronology-valid same-record quotient owner",
    "no u=2 branch closure",
    "no u=3 theorem",
    "no cap-68 theorem",
    "no ledger movement",
    "no KoalaBear row closure",
]

EXPECTED_GROUPS = [
    (1, "A5 x A5", 3600, [1, 12, 12, 15, 20]),
    (2, "A5 : S5", 7200, [1, 15, 20, 24]),
    (3, "(A5 x A5) : C2", 7200, [1, 15, 20, 24]),
    (4, "(A5 x A5) : C2", 7200, [1, 12, 12, 15, 20]),
    (5, "(A5 x A5) : (C2 x C2)", 14400, [1, 15, 20, 24]),
    (6, "PSL(2,59)", 102660, [1, 59]),
    (7, "PSL(2,59) : C2", 205320, [1, 59]),
    (
        8,
        "A60",
        4160493556370695072138170591611682190377086303180622976224638848204800000000000000,
        [1, 59],
    ),
    (
        9,
        "S60",
        8320987112741390144276341183223364380754172606361245952449277696409600000000000000,
        [1, 59],
    ),
]

TERMINAL = "ROUTED_TO_GEOMETRIC_FUNCTIONAL_DECOMPOSITION_ADAPTER"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def payload_hash(value: dict[str, Any]) -> str:
    unhashed = dict(value)
    unhashed.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(unhashed).encode()).hexdigest()


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise VerificationError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_pairs,
    )


def git_output(*arguments: str) -> str:
    try:
        result = subprocess.run(
            ["git", *arguments],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise VerificationError(
            "git object binding failed: " + " ".join(arguments)
        ) from error
    return result.stdout.strip()


def proper_divisors(value: int) -> list[int]:
    return [
        candidate
        for candidate in range(2, value)
        if value % candidate == 0
    ]


def decomposition_profiles() -> list[dict[str, int]]:
    profiles: list[dict[str, int]] = []
    for inner_degree in proper_divisors(60):
        outer_degree = 60 // inner_degree
        for simple_outer_poles in range(outer_degree + 1):
            remainder = outer_degree - simple_outer_poles
            if remainder < 0 or remainder % 5:
                continue
            order_five_outer_poles = remainder // 5
            if simple_outer_poles and inner_degree % 5:
                continue
            ramification_charge_numerator = (
                simple_outer_poles * 4 * inner_degree
            )
            if ramification_charge_numerator > 5 * (2 * inner_degree - 2):
                continue
            profiles.append(
                {
                    "inner_degree": inner_degree,
                    "outer_degree": outer_degree,
                    "order_five_outer_poles": order_five_outer_poles,
                    "simple_outer_poles": simple_outer_poles,
                    "forced_ramification": (
                        ramification_charge_numerator // 5
                    ),
                    "riemann_hurwitz_budget": 2 * inner_degree - 2,
                }
            )
    return profiles


EXPECTED_PROFILES = [
    {
        "inner_degree": 2,
        "outer_degree": 30,
        "order_five_outer_poles": 6,
        "simple_outer_poles": 0,
        "forced_ramification": 0,
        "riemann_hurwitz_budget": 2,
    },
    {
        "inner_degree": 3,
        "outer_degree": 20,
        "order_five_outer_poles": 4,
        "simple_outer_poles": 0,
        "forced_ramification": 0,
        "riemann_hurwitz_budget": 4,
    },
    {
        "inner_degree": 4,
        "outer_degree": 15,
        "order_five_outer_poles": 3,
        "simple_outer_poles": 0,
        "forced_ramification": 0,
        "riemann_hurwitz_budget": 6,
    },
    {
        "inner_degree": 5,
        "outer_degree": 12,
        "order_five_outer_poles": 2,
        "simple_outer_poles": 2,
        "forced_ramification": 8,
        "riemann_hurwitz_budget": 8,
    },
    {
        "inner_degree": 6,
        "outer_degree": 10,
        "order_five_outer_poles": 2,
        "simple_outer_poles": 0,
        "forced_ramification": 0,
        "riemann_hurwitz_budget": 10,
    },
    {
        "inner_degree": 10,
        "outer_degree": 6,
        "order_five_outer_poles": 1,
        "simple_outer_poles": 1,
        "forced_ramification": 8,
        "riemann_hurwitz_budget": 18,
    },
    {
        "inner_degree": 12,
        "outer_degree": 5,
        "order_five_outer_poles": 1,
        "simple_outer_poles": 0,
        "forced_ramification": 0,
        "riemann_hurwitz_budget": 22,
    },
    {
        "inner_degree": 30,
        "outer_degree": 2,
        "order_five_outer_poles": 0,
        "simple_outer_poles": 2,
        "forced_ramification": 48,
        "riemann_hurwitz_budget": 58,
    },
]


def check(data: dict[str, Any]) -> None:
    require(
        data["schema"]
        == "kb-mca-v4-degree60-primitive-subdegree4-route-cut-v1",
        "schema",
    )
    require(data["payload_sha256"] == payload_hash(data), "payload hash")

    statement = data["statement"]
    require(statement["row"] == EXPECTED_ROW, "row")
    require(statement["agreement"] == EXPECTED_AGREEMENT, "agreement")
    require(statement["B_star"] == EXPECTED_B_STAR, "B_star")
    require(
        statement["deployed_characteristic"] == EXPECTED_CHARACTERISTIC,
        "deployed characteristic",
    )
    require(statement["endpoint_degree"] == 60, "endpoint degree")
    require(statement["component_u"] == 2, "component degree")
    require(
        statement["downstairs_component_bidegree"] == [4, 4],
        "downstairs component bidegree",
    )
    require(statement["required_subdegree"] == 4, "required subdegree")
    require(statement["deployed_characteristic"] > 60, "separability")
    require(
        statement["classification_scope"] == EXPECTED_CLASSIFICATION_SCOPE,
        "classification scope",
    )

    parent = data["parent_stack"]
    require(parent["head_commit"] == EXPECTED_PARENT_HEAD, "parent head")
    require(
        parent["certificate_path"] == EXPECTED_PARENT_PATH,
        "parent certificate path",
    )
    require(
        parent["certificate_blob_oid"] == EXPECTED_PARENT_BLOB,
        "parent certificate blob",
    )
    require(
        parent["certificate_payload_sha256"] == EXPECTED_PARENT_PAYLOAD,
        "parent payload binding",
    )
    parent_data = load_json(PARENT_CERTIFICATE)
    require(
        parent_data["payload_sha256"] == payload_hash(parent_data),
        "parent payload hash",
    )
    require(
        parent_data["payload_sha256"] == parent["certificate_payload_sha256"],
        "parent certificate replay binding",
    )
    require(git_output("cat-file", "-t", parent["head_commit"]) == "commit",
            "parent commit object")
    require(
        git_output(
            "rev-parse",
            parent["head_commit"] + ":" + parent["certificate_path"],
        )
        == parent["certificate_blob_oid"],
        "parent head/path/blob binding",
    )

    defect = data["complete_source_quartic_defect_gate"]
    require(defect["complete_source_degree"] == 24, "quartic pole units")
    require(
        defect["allowed_pole_multiplicities"] == [1, 2],
        "pole multiplicities",
    )
    require(defect["local_source_rows_per_pole"] == 2, "two source rows")
    require(
        defect["local_row_order_equals_pole_order"],
        "local saturated orders",
    )
    require(
        defect["all_pole_units_map_to_twelve_line_star_vertices"],
        "complete star support",
    )
    require(
        defect["rational_plane_quartic_arithmetic_genus"] == 3,
        "quartic genus",
    )
    require(defect["minimum_distinct_star_vertices"] == 21, "vertex floor")
    require(defect["maximum_weight"] == 3, "maximum vertex weight")
    expected_histograms = [
        {
            "weight_two_vertices": 1,
            "weight_three_vertices": 0,
            "defect_cost": 1,
        },
        {
            "weight_two_vertices": 2,
            "weight_three_vertices": 0,
            "defect_cost": 2,
        },
        {
            "weight_two_vertices": 3,
            "weight_three_vertices": 0,
            "defect_cost": 3,
        },
        {
            "weight_two_vertices": 0,
            "weight_three_vertices": 1,
            "defect_cost": 3,
        },
    ]
    require(
        defect["allowed_nonsimple_weight_histograms"] == expected_histograms,
        "quartic defect histograms",
    )
    for row in expected_histograms:
        require(
            row["weight_two_vertices"]
            + 3 * row["weight_three_vertices"]
            == row["defect_cost"],
            "defect histogram arithmetic",
        )
        require(row["defect_cost"] <= 3, "delta budget")

    catalogue = data["catalogue"]
    require(catalogue["system"] == "GAP PrimGrp", "catalogue system")
    require(catalogue["sage_version"] == "10.9", "Sage version")
    require(catalogue["gap_version"] == "4.14.0", "GAP version")
    require(
        catalogue["installed_primgrp_version"] == "3.4.4",
        "PrimGrp version",
    )
    require(catalogue["degree"] == 60, "catalogue degree")
    require(catalogue["complete_group_count"] == 9, "catalogue count")
    require(
        catalogue["catalogue_completeness_import"]
        == (
            "all primitive permutation groups of degree below 4096, "
            "up to permutation isomorphism"
        ),
        "catalogue completeness scope",
    )
    require(
        catalogue["stable_identifier"] == "PrimitiveGroup(60,i)",
        "catalogue identifier",
    )

    rows = data["primitive_degree_60_groups"]
    require(len(rows) == 9, "nine primitive groups")
    observed = [
        (
            row["primitive_group_id"],
            row["structure"],
            int(row["order"]),
            row["subdegrees"],
        )
        for row in rows
    ]
    require(observed == EXPECTED_GROUPS, "primitive group rows")
    require(
        all(row["primitive"] and row["transitive"] for row in rows),
        "primitive/transitive flags",
    )
    require(
        all(sum(row["subdegrees"]) == 60 for row in rows),
        "subdegree partition",
    )
    require(
        all(4 not in row["subdegrees"] for row in rows),
        "no primitive subdegree four",
    )
    wolfram = data["wolfram_replay"]
    require(
        wolfram["path"]
        == "experimental/scripts/"
        "verify_kb_mca_v4_degree60_primitive_subdegree4_route_cut_v1.wl",
        "Wolfram replay path",
    )
    require(
        hashlib.sha256(WOLFRAM_REPLAY.read_bytes()).hexdigest()
        == wolfram["sha256"],
        "Wolfram replay hash",
    )

    profiles = decomposition_profiles()
    require(profiles == EXPECTED_PROFILES, "derived decomposition profiles")
    require(
        data["functional_decomposition_profiles"] == profiles,
        "certificate decomposition profiles",
    )
    require(
        [row["inner_degree"] for row in profiles]
        == [2, 3, 4, 5, 6, 10, 12, 30],
        "remaining inner degrees",
    )
    require(data["excluded_inner_degrees"] == [15, 20], "excluded degrees")

    conclusion = data["conclusion"]
    require(conclusion["primitive_u2_branch_empty"], "primitive route cut")
    require(
        conclusion["terminal"] == TERMINAL,
        "terminal",
    )
    require(not conclusion["u2_branch_closed"], "u2 remains open")
    require(not conclusion["row_closed"], "row remains open")
    require(conclusion["ledger_movement"] == 0, "zero ledger movement")
    require(
        conclusion["next_gate"]
        == "SOURCE_BOUND_FUNCTIONAL_DECOMPOSITION_OWNER_OR_DELETION",
        "next gate",
    )

    dependencies = data["dependencies"]
    require(
        dependencies["imported_component_descent"]
        == (
            "Corollary 9.5 of "
            "pole_disjoint_conic_facet_collinearity_reduction.md"
        ),
        "component-descent dependency",
    )
    require(
        dependencies["source_commit"] == EXPECTED_SOURCE_COMMIT,
        "source commit",
    )
    require(
        dependencies["source_path"] == EXPECTED_SOURCE_PATH,
        "source path",
    )
    require(
        dependencies["source_blob_oid"] == EXPECTED_SOURCE_BLOB,
        "source blob",
    )
    require(
        dependencies["manual_integration_commit"]
        == EXPECTED_INTEGRATION_COMMIT,
        "integration commit",
    )
    require(
        dependencies["classification"]
        == "GAP PrimGrp exhaustive primitive permutation group catalogue",
        "classification dependency",
    )
    require(
        dependencies["classical_dictionary"]
        == (
            "irreducible self-correspondence factors are point-stabilizer "
            "suborbits; rational-map indecomposability is equivalent to "
            "primitive geometric monodromy"
        ),
        "classical dictionary dependency",
    )
    require(
        git_output(
            "rev-parse",
            dependencies["source_commit"] + ":" + dependencies["source_path"],
        )
        == dependencies["source_blob_oid"],
        "source commit/path/blob binding",
    )
    require(
        git_output("cat-file", "-t", dependencies["source_commit"])
        == "commit",
        "source commit object",
    )
    require(
        git_output(
            "cat-file", "-t", dependencies["manual_integration_commit"]
        )
        == "commit",
        "integration commit object",
    )
    require(data["nonclaims"] == EXPECTED_NONCLAIMS, "nonclaims")


def mutations(data: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    result: list[tuple[str, dict[str, Any]]] = []

    def add(name: str, mutate: Any) -> None:
        forged = copy.deepcopy(data)
        mutate(forged)
        forged["payload_sha256"] = payload_hash(forged)
        result.append((name, forged))

    add("wrong endpoint degree", lambda d: d["statement"].update(endpoint_degree=59))
    add("wrong u", lambda d: d["statement"].update(component_u=3))
    add("wrong row", lambda d: d["statement"].update(row="forged"))
    add("wrong agreement", lambda d: d["statement"].update(agreement=0))
    add("wrong B_star", lambda d: d["statement"].update(B_star="0"))
    add(
        "wrong bidegree",
        lambda d: d["statement"].update(downstairs_component_bidegree=[2, 4]),
    )
    add(
        "wrong required subdegree",
        lambda d: d["statement"].update(required_subdegree=5),
    )
    add(
        "inseparable characteristic",
        lambda d: d["statement"].update(deployed_characteristic=5),
    )
    add(
        "wrong deployed characteristic",
        lambda d: d["statement"].update(deployed_characteristic=61),
    )
    add(
        "wrong classification scope",
        lambda d: d["statement"].update(classification_scope="arithmetic"),
    )
    add(
        "wrong parent head",
        lambda d: d["parent_stack"].update(head_commit="0" * 40),
    )
    add(
        "wrong parent path",
        lambda d: d["parent_stack"].update(certificate_path="forged.json"),
    )
    add(
        "wrong parent blob",
        lambda d: d["parent_stack"].update(certificate_blob_oid="0" * 40),
    )
    add(
        "wrong parent payload",
        lambda d: d["parent_stack"].update(
            certificate_payload_sha256="0" * 64
        ),
    )
    add(
        "off-star pole",
        lambda d: d["complete_source_quartic_defect_gate"].update(
            all_pole_units_map_to_twelve_line_star_vertices=False
        ),
    )
    add(
        "one source row",
        lambda d: d["complete_source_quartic_defect_gate"].update(
            local_source_rows_per_pole=1
        ),
    )
    add(
        "vertex floor",
        lambda d: d["complete_source_quartic_defect_gate"].update(
            minimum_distinct_star_vertices=20
        ),
    )
    add(
        "weight four",
        lambda d: d["complete_source_quartic_defect_gate"].update(
            maximum_weight=4
        ),
    )
    add(
        "catalogue system",
        lambda d: d["catalogue"].update(system="forged"),
    )
    add(
        "Sage version",
        lambda d: d["catalogue"].update(sage_version="0"),
    )
    add(
        "GAP version",
        lambda d: d["catalogue"].update(gap_version="0"),
    )
    add(
        "PrimGrp version",
        lambda d: d["catalogue"].update(installed_primgrp_version="0"),
    )
    add(
        "catalogue degree",
        lambda d: d["catalogue"].update(degree=59),
    )
    add(
        "catalogue count",
        lambda d: d["catalogue"].update(complete_group_count=8),
    )
    add(
        "catalogue completeness",
        lambda d: d["catalogue"].update(
            catalogue_completeness_import="forged"
        ),
    )
    add(
        "catalogue identifier",
        lambda d: d["catalogue"].update(stable_identifier="forged"),
    )
    add("missing group", lambda d: d["primitive_degree_60_groups"].pop())
    add(
        "duplicate group",
        lambda d: d["primitive_degree_60_groups"].append(
            copy.deepcopy(d["primitive_degree_60_groups"][0])
        ),
    )
    for index in range(9):
        add(
            f"group {index + 1} forged subdegree",
            lambda d, index=index: d["primitive_degree_60_groups"][index][
                "subdegrees"
            ].append(4),
        )
    add(
        "group order",
        lambda d: d["primitive_degree_60_groups"][0].update(order="3599"),
    )
    add(
        "group structure",
        lambda d: d["primitive_degree_60_groups"][1].update(structure="A5"),
    )
    add(
        "Wolfram replay hash",
        lambda d: d["wolfram_replay"].update(sha256="0" * 64),
    )
    add(
        "primitive flag",
        lambda d: d["primitive_degree_60_groups"][2].update(primitive=False),
    )
    add(
        "transitive flag",
        lambda d: d["primitive_degree_60_groups"][3].update(transitive=False),
    )
    add(
        "profile removed",
        lambda d: d["functional_decomposition_profiles"].pop(),
    )
    add(
        "profile degree",
        lambda d: d["functional_decomposition_profiles"][0].update(
            inner_degree=1
        ),
    )
    add(
        "profile pole count",
        lambda d: d["functional_decomposition_profiles"][3].update(
            simple_outer_poles=1
        ),
    )
    add(
        "profile ramification",
        lambda d: d["functional_decomposition_profiles"][3].update(
            forced_ramification=7
        ),
    )
    add(
        "excluded degree",
        lambda d: d.update(excluded_inner_degrees=[20]),
    )
    add(
        "primitive branch reopened",
        lambda d: d["conclusion"].update(primitive_u2_branch_empty=False),
    )
    add(
        "false u2 closure",
        lambda d: d["conclusion"].update(u2_branch_closed=True),
    )
    add(
        "false row closure",
        lambda d: d["conclusion"].update(row_closed=True),
    )
    add(
        "ledger movement",
        lambda d: d["conclusion"].update(ledger_movement=1),
    )
    add(
        "wrong terminal",
        lambda d: d["conclusion"].update(terminal="PAID_QUOTIENT_DESCENT"),
    )
    add(
        "wrong next gate",
        lambda d: d["conclusion"].update(next_gate="U3"),
    )
    add(
        "component dependency",
        lambda d: d["dependencies"].update(
            imported_component_descent="forged"
        ),
    )
    add(
        "source commit",
        lambda d: d["dependencies"].update(source_commit="0" * 40),
    )
    add(
        "source path",
        lambda d: d["dependencies"].update(source_path="forged"),
    )
    add(
        "source blob",
        lambda d: d["dependencies"].update(source_blob_oid="0" * 40),
    )
    add(
        "integration commit",
        lambda d: d["dependencies"].update(
            manual_integration_commit="0" * 40
        ),
    )
    add(
        "classification dependency",
        lambda d: d["dependencies"].update(classification="forged"),
    )
    add(
        "classical dictionary",
        lambda d: d["dependencies"].update(classical_dictionary="forged"),
    )
    add("nonclaims", lambda d: d["nonclaims"].pop())
    add("schema", lambda d: d.update(schema="forged"))
    forged_hash = copy.deepcopy(data)
    forged_hash["payload_sha256"] = "0" * 64
    result.append(("hash", forged_hash))
    require(len(result) == 63, "mutation count")
    return result


def tamper_selftest(data: dict[str, Any]) -> None:
    rejected = 0
    for name, forged in mutations(data):
        try:
            check(forged)
        except (VerificationError, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            raise VerificationError(f"mutation accepted: {name}")
    require(rejected == 63, "all mutations rejected")

    duplicate = '{"a":1,"a":2}'
    try:
        json.loads(duplicate, object_pairs_hook=reject_duplicate_pairs)
    except VerificationError:
        pass
    else:
        raise VerificationError("duplicate JSON key accepted")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    require(args.check or args.tamper_selftest, "choose a verification mode")

    data = load_json(CERTIFICATE)
    check(data)
    if args.tamper_selftest:
        tamper_selftest(data)

    print("status=PROVED_PRIMITIVE_SUBDEGREE4_ROUTE_CUT")
    print("primitive_degree60_groups=9")
    print("primitive_subdegree4_groups=0")
    print("decomposition_profiles=8")
    if args.tamper_selftest:
        print("tamper_mutations_rejected=63/63")
        print("duplicate_json_keys=REJECTED")
    print("terminal=" + data["conclusion"]["terminal"])
    print("ledger_movement=0")
    print("payload_sha256=" + data["payload_sha256"])


if __name__ == "__main__":
    main()
