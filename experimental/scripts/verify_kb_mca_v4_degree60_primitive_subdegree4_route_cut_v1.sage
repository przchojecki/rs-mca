#!/usr/bin/env sage
"""Independent Sage/GAP replay of the degree-60 subdegree-four route cut."""

import hashlib
import json
import subprocess
from pathlib import Path

import sage.version


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

EXPECTED_SOURCE_COMMIT = "44542e91e459364a521870ed2ebde7f6fe5055bf"
EXPECTED_SOURCE_PATH = (
    "experimental/notes/frontier-adjacent/"
    "kb_mca_v4_equality_wall_geometry_v1/proof/"
    "pole_disjoint_conic_facet_collinearity_reduction.md"
)
EXPECTED_SOURCE_BLOB = "356ff4b47d0bb429d11ea10382762a6e95b5ce24"


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def unhashed_digest(value):
    value = dict(value)
    value.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def git_output(*arguments):
    return subprocess.run(
        ["git", *arguments],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
assert data["payload_sha256"] == unhashed_digest(data)
assert (
    hashlib.sha256(WOLFRAM_REPLAY.read_bytes()).hexdigest()
    == data["wolfram_replay"]["sha256"]
)

statement = data["statement"]
assert statement["row"] == "KoalaBear MCA at 2^-128"
assert statement["agreement"] == 1116048
assert statement["B_star"] == "274980728111395087"
assert statement["deployed_characteristic"] == 2130706433
assert statement["endpoint_degree"] == 60
assert statement["component_u"] == 2
assert statement["downstairs_component_bidegree"] == [4, 4]
assert statement["required_subdegree"] == 4
assert (
    statement["classification_scope"]
    == "geometric primitive monodromy over the algebraic closure"
)

parent = data["parent_stack"]
assert parent == {
    "head_commit": "ad109774f7d9bc320e7e0c046ba83471f39d5cd9",
    "certificate_path": (
        "experimental/data/certificates/"
        "kb-mca-v4-q6-u2-complete-source-conic-exclusion-v1/"
        "kb_mca_v4_q6_u2_complete_source_conic_exclusion_v1.json"
    ),
    "certificate_blob_oid": "61afd4534740c5ccabc6196919126c80c361e4c5",
    "certificate_payload_sha256": (
        "30a5d45895957f774ef972118e227fa54522fc27a48ee0e2a99a0d5a012a5451"
    ),
}
parent_data = json.loads(PARENT_CERTIFICATE.read_text(encoding="utf-8"))
assert parent_data["payload_sha256"] == unhashed_digest(parent_data)
assert parent_data["payload_sha256"] == parent["certificate_payload_sha256"]
assert git_output("cat-file", "-t", parent["head_commit"]) == "commit"
assert (
    git_output(
        "rev-parse",
        parent["head_commit"] + ":" + parent["certificate_path"],
    )
    == parent["certificate_blob_oid"]
)

catalogue = data["catalogue"]
assert catalogue == {
    "system": "GAP PrimGrp",
    "sage_version": "10.9",
    "gap_version": "4.14.0",
    "installed_primgrp_version": "3.4.4",
    "degree": 60,
    "complete_group_count": 9,
    "catalogue_completeness_import": (
        "all primitive permutation groups of degree below 4096, "
        "up to permutation isomorphism"
    ),
    "stable_identifier": "PrimitiveGroup(60,i)",
}

defect = data["complete_source_quartic_defect_gate"]
assert defect["complete_source_degree"] == 24
assert defect["allowed_pole_multiplicities"] == [1, 2]
assert defect["local_source_rows_per_pole"] == 2
assert defect["local_row_order_equals_pole_order"]
assert defect["all_pole_units_map_to_twelve_line_star_vertices"]
assert defect["rational_plane_quartic_arithmetic_genus"] == 3
assert defect["minimum_distinct_star_vertices"] == 21
assert defect["maximum_weight"] == 3
assert defect["allowed_nonsimple_weight_histograms"] == [
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

assert libgap.PrimitiveGroupsAvailable(60)
assert Integer(libgap.NrPrimitiveGroups(60)) == 9

observed = []
for index in range(1, 10):
    gap_group = libgap.PrimitiveGroup(60, index)
    group = PermutationGroup(gap_group=gap_group)
    stabilizer = group.stabilizer(1)
    subdegrees = sorted(len(orbit) for orbit in stabilizer.orbits())
    observed.append(
        {
            "primitive_group_id": index,
            "structure": str(libgap.StructureDescription(gap_group)),
            "order": str(group.order()),
            "subdegrees": subdegrees,
            "primitive": bool(libgap.IsPrimitive(gap_group)),
            "transitive": bool(libgap.IsTransitive(gap_group)),
        }
    )

assert observed == data["primitive_degree_60_groups"]
assert all(sum(row["subdegrees"]) == 60 for row in observed)
assert all(4 not in row["subdegrees"] for row in observed)

# Independently regenerate the pole-profile ladder.  If f=F o h and every
# pole of f has order five, every outer pole has order one or five.  An
# order-one outer pole forces a full index-five ramification fibre of h.
profiles = []
for inner_degree in divisors(60):
    inner_degree = Integer(inner_degree)
    if inner_degree in (1, 60):
        continue
    outer_degree = 60 // inner_degree
    for simple_outer_poles in range(outer_degree + 1):
        remainder = outer_degree - simple_outer_poles
        if remainder < 0 or remainder % 5:
            continue
        order_five_outer_poles = remainder // 5
        if simple_outer_poles and inner_degree % 5:
            continue
        forced_ramification = simple_outer_poles * 4 * inner_degree // 5
        budget = 2 * inner_degree - 2
        if forced_ramification > budget:
            continue
        profiles.append(
            {
                "inner_degree": int(inner_degree),
                "outer_degree": int(outer_degree),
                "order_five_outer_poles": int(order_five_outer_poles),
                "simple_outer_poles": int(simple_outer_poles),
                "forced_ramification": int(forced_ramification),
                "riemann_hurwitz_budget": int(budget),
            }
        )

assert profiles == data["functional_decomposition_profiles"]
assert [row["inner_degree"] for row in profiles] == [
    2, 3, 4, 5, 6, 10, 12, 30
]
assert data["excluded_inner_degrees"] == [15, 20]

assert data["conclusion"]["primitive_u2_branch_empty"]
assert not data["conclusion"]["u2_branch_closed"]
assert not data["conclusion"]["row_closed"]
assert data["conclusion"]["ledger_movement"] == 0

dependencies = data["dependencies"]
assert dependencies == {
    "imported_component_descent": (
        "Corollary 9.5 of "
        "pole_disjoint_conic_facet_collinearity_reduction.md"
    ),
    "source_commit": EXPECTED_SOURCE_COMMIT,
    "source_path": EXPECTED_SOURCE_PATH,
    "source_blob_oid": EXPECTED_SOURCE_BLOB,
    "manual_integration_commit": (
        "0f7476f0fcbc5d1a1d3eed0c03221aaa48f5767d"
    ),
    "classification": (
        "GAP PrimGrp exhaustive primitive permutation group catalogue"
    ),
    "classical_dictionary": (
        "irreducible self-correspondence factors are point-stabilizer "
        "suborbits; rational-map indecomposability is equivalent to "
        "primitive geometric monodromy"
    ),
}
assert (
    git_output(
        "rev-parse",
        dependencies["source_commit"] + ":" + dependencies["source_path"],
    )
    == dependencies["source_blob_oid"]
)
assert git_output("cat-file", "-t", dependencies["source_commit"]) == "commit"
assert (
    git_output("cat-file", "-t", dependencies["manual_integration_commit"])
    == "commit"
)
assert data["nonclaims"] == [
    "no exclusion of geometrically decomposable endpoint maps",
    "no domain-compatible witness-data descent",
    "no chronology-valid same-record quotient owner",
    "no u=2 branch closure",
    "no u=3 theorem",
    "no cap-68 theorem",
    "no ledger movement",
    "no KoalaBear row closure",
]

print("status=PROVED_PRIMITIVE_SUBDEGREE4_ROUTE_CUT")
print("sage_version=" + sage.version.version)
print("gap_version=" + str(libgap.eval("GAPInfo.Version")))
print(
    "primgrp_version="
    + str(libgap.eval('PackageInfo("primgrp")[1].Version'))
)
print("primitive_degree60_groups=9")
for row in observed:
    print(
        "PrimitiveGroup(60,{}) order={} subdegrees={}".format(
            row["primitive_group_id"],
            row["order"],
            row["subdegrees"],
        )
    )
print("primitive_subdegree4_groups=0")
print("complete_source_quartic_minimum_distinct_vertices=21")
print("decomposition_profiles=8")
print("payload_sha256=" + data["payload_sha256"])
