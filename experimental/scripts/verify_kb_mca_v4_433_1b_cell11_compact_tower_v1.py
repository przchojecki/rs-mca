#!/usr/bin/env python3
"""Verify or assemble the experimental 433-1b cell-11 compact-tower packet."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = ROOT / (
    "experimental/data/certificates/"
    "kb-mca-v4-433-1b-cell11-compact-tower-v1/"
    "kb_mca_v4_433_1b_cell11_compact_tower_v1.json"
)
PRIME = 2_130_706_433
SOURCE_COMMIT = "28b3bc8ab13e94c25088e904251eb5cf49e68ad2"
SOURCE_HASHES = {
    "common": "a956656cba6c884bae665a2439666964ed468dcf9d0466e80cb825e811a6f845",
    "product": "ee4dcb25877e9101a544ee5896b9bf6890059d6398c78d7562127b0d1c53c293",
    "pilot": "1590721003b1b8c9f850064eddab82d2fa25ddb93a00ef9d71feaa4d492f16ea",
}
EXPECTED_CHARTS = [
    {
        "c_row": 5, "kernel_dimension": 1, "kernel_basis_size": 36,
        "tower_dimension": 1, "tower_basis_size": 43,
        "b_boundary_dimension": 0, "b_boundary_basis_size": 15,
        "c_boundary_dimension": 0, "c_boundary_basis_size": 15,
    },
    {
        "c_row": 6, "kernel_dimension": 1, "kernel_basis_size": 36,
        "tower_dimension": 1, "tower_basis_size": 39,
        "b_boundary_dimension": 0, "b_boundary_basis_size": 15,
        "c_boundary_dimension": 0, "c_boundary_basis_size": 21,
    },
    {
        "c_row": 7, "kernel_dimension": 1, "kernel_basis_size": 36,
        "tower_dimension": 1, "tower_basis_size": 41,
        "b_boundary_dimension": 0, "b_boundary_basis_size": 15,
        "c_boundary_dimension": 0, "c_boundary_basis_size": 35,
    },
]
EXPECTED_BOUNDARIES = {
    "b_leading": {
        "r_polynomial": [1, 2_113_994_755, 16_711_678, 2_113_994_755, 2_113_994_754],
        "r_factorization": [
            {"degree": 1, "multiplicity": 1, "coefficients": [1, 440_734_903]},
            {"degree": 3, "multiplicity": 1,
             "coefficients": [1, 1_673_259_852, 946_675_306, 700_051_530]},
        ],
        "r_deployed_roots": [1_689_971_530],
        "t_lift": 188_031_674,
        "b_polynomial": [1, 2_078_591_770, 1],
        "b_discriminant": 1_184_183_620,
        "b_discriminant_euler": 2_130_706_432,
    },
    "c_leading": {
        "r_polynomial": [1, 16_711_678, 16_711_680, 2_113_994_755, 16_711_679],
        "r_factorization": [
            {"degree": 1, "multiplicity": 1, "coefficients": [1, 1_430_654_903]},
            {"degree": 3, "multiplicity": 1,
             "coefficients": [1, 716_763_208, 230_069_660, 440_734_903]},
        ],
        "r_deployed_roots": [700_051_530],
        "t_lift": 879_708_479,
        "b_polynomial": [1, 1_529_703_515, 1],
        "b_discriminant": 140_859_139,
        "b_discriminant_euler": 2_130_706_432,
    },
}
EXPECTED_KERNEL = [
    (14, 49, "ab6bada2a728b06232468af3bedaa31428efe647fac168a64d92954b7d561261"),
    (14, 52, "1c350699a644d6dc02b908450d4bc41d2d1643ac44575c24764f67925d60b924"),
    (12, 49, "32e6b9d475bed5739ca4a87edf95f0343fc35d16e6e990a1198a74eec6da7df9"),
    (15, 49, "99c42c793118a5ea4c2836d7b24caafa699732113e332211a5f8b1403fb831e2"),
    (15, 52, "c94fee85268a1bf701598840d2c33a27757906f4ba74708d92396f110e655015"),
    (13, 49, "c98c8b449aa640bd99c01c8472ba057c4840dcd9418a050c181b6dfeb97bf5c1"),
    (14, 48, "53255e14214302fad13d6f8368927e3e8496b33ffb0a3170476b20b30e2c6718"),
    (14, 48, "f57461abacb0737df02d15b1ff95a839813472a1d646ccaa6b2eeda364155396"),
]
EXPECTED_WOLFRAM = {
    "method": "Wolfram Cloud FactorList and PowerMod over F_2130706433",
    "b_boundary_factor_degrees": [1, 3],
    "c_boundary_factor_degrees": [1, 3],
    "b_lift_discriminant": 1_184_183_620,
    "c_lift_discriminant": 140_859_139,
    "b_lift_euler": 2_130_706_432,
    "c_lift_euler": 2_130_706_432,
}


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def verify_raw(raw: dict) -> None:
    require(raw.get("schema") == "kb-mca-v4-433-1b-cell11-compact-tower-raw-v1", "raw schema")
    require(raw.get("field") == PRIME, "raw field")
    require(raw.get("source_commit") == SOURCE_COMMIT, "raw source commit")
    require(raw.get("source_sha256") == SOURCE_HASHES, "raw source hashes")
    require(raw.get("pilot_quotient_exact") is False, "pilot nonexactness lost")
    require(raw.get("selected_c_row") == 5, "selected chart")
    charts = raw.get("charts", [])
    require(len(charts) == 3, "chart coverage")
    observed = [
        {key: row.get(key) for key in EXPECTED_CHARTS[index]}
        for index, row in enumerate(charts)
    ]
    require(observed == EXPECTED_CHARTS, "chart invariants")
    for row in charts:
        require(row.get("exact") is True, "tower not exact")
        require(row.get("remainders") == ["0"] * 8, "nonzero tower remainder")
    boundaries = raw.get("boundaries", {})
    for name, expected in EXPECTED_BOUNDARIES.items():
        row = boundaries.get(name, {})
        require(
            {key: row.get(key) for key in expected} == expected,
            f"{name} boundary data",
        )
        require(row.get("deployed_boundary_empty") is True, f"{name} not empty")
        require(len(row.get("lex_basis", [])) == 5, f"{name} lex basis")
    kernel = raw.get("kernel", {})
    require(kernel.get("epsilon") == [-1, -1], "kernel sign row")
    require(kernel.get("pivot") == 1, "kernel pivot")
    profiles = [
        (row.get("degree"), row.get("terms"), row.get("sha256"))
        for row in kernel.get("kernel", [])
    ]
    require(profiles == EXPECTED_KERNEL, "kernel profiles")
    require(
        kernel.get("identically_zero_rows") == [True] * 7 + [False] * 3,
        "symbolic row profile",
    )
    require(kernel.get("remainders") == ["0"] * 10, "kernel remainder")
    require(kernel.get("all_rows_zero") is True, "kernel replay")
    require(kernel.get("common_dimension") == 1, "common dimension")
    require(kernel.get("common_basis_size") == 40, "common basis size")


def verify(payload: dict) -> None:
    require(payload.get("schema") == "kb-mca-v4-433-1b-cell11-compact-tower-v1", "schema")
    require(payload.get("field") == PRIME, "field")
    require(payload.get("status") == "EXPERIMENTAL_REVIEW_REQUIRED", "status promotion")
    provenance = payload.get("provenance", {})
    require(provenance.get("source_commit") == SOURCE_COMMIT, "source commit")
    require(provenance.get("source_sha256") == SOURCE_HASHES, "source hashes")
    verify_raw(payload.get("exact_replay", {}))
    require(payload.get("independent_checks", {}).get("wolfram") == EXPECTED_WOLFRAM, "Wolfram check")
    require(payload.get("ledger_movement") == 0, "ledger movement")
    require(payload.get("signed_pair_resultant_complete") is False, "resultant promotion")
    require(payload.get("sign_transport_complete") is False, "sign transport promotion")
    require(payload.get("role_orbit_11_closed") is False, "orbit promotion")
    require(payload.get("K3_closed") is False, "K3 promotion")
    require(payload.get("KoalaBear_row_closed") is False, "row promotion")
    require(payload.get("FLOOR_v2_used") is False, "broken first-moment route reused")
    require(payload.get("S_sparse_bound_claimed") is False, "unsupported sparse maximum")


def assemble(raw_path: Path) -> dict:
    raw = json.loads(raw_path.read_text())
    verify_raw(raw)
    payload = {
        "schema": "kb-mca-v4-433-1b-cell11-compact-tower-v1",
        "field": PRIME,
        "workboard_item": "K3/K4",
        "row": "KoalaBear MCA at target epsilon 2^-128",
        "object": "MCA",
        "target_epsilon": "2^-128",
        "agreement": 1_116_048,
        "B_star": 274_980_728_111_395_087,
        "direct_statement": (
            "For the public 433-1b source-role cell-11 pilot at epsilon=(-1,-1) "
            "and pivot 1 over F_2130706433, each of three declared reduced "
            "three-equation towers generates the guarded eight-equation common "
            "locus; the selected chart's two leading-coefficient boundaries "
            "have no deployed-field point; and one primitive eight-coordinate "
            "coefficient kernel annihilates all ten Vieta rows modulo that locus."
        ),
        "architecture": "K3 coordinate-positive 433-1b source-role workboard",
        "partition_digest": "public-DAG-433-1b-router@28b3bc8a",
        "atom_or_cell": "source-role cell 11; epsilon=(-1,-1); pivot 1",
        "quantifier": "the exact guarded common locus in the one declared source-sign chart",
        "projection_and_unit": "local common-locus parameters; not yet affine slopes or a v4 atom",
        "claimed_bound": "exact structural reduction only; no cell-11 witness count",
        "status": "EXPERIMENTAL_REVIEW_REQUIRED",
        "impact": "LOCAL_ONLY",
        "falsifier": (
            "a source mismatch, nonzero tower or kernel remainder, deployed "
            "leading-boundary point, missing sign transport, or surviving "
            "signed-pair resultant component"
        ),
        "provenance": {
            "source_repo": "https://github.com/AllenGrahamHart/rs-mca-prize-dag",
            "source_commit": SOURCE_COMMIT,
            "source_sha256": SOURCE_HASHES,
            "raw_sha256": hashlib.sha256(raw_path.read_bytes()).hexdigest(),
            "compute": "local SymPy 1.14.0 and Singular 4.4.1; no hosted source upload",
        },
        "relationship_to_upstream": (
            "The public pilot records a nonexact nine-generator quotient at "
            "all four pivots. This packet repairs the pivot-1 structural "
            "presentation with an exact three-equation tower; it does not "
            "supply the missing complete signed-pair resultant or role transport."
        ),
        "exact_replay": raw,
        "independent_checks": {
            "wolfram": EXPECTED_WOLFRAM,
            "method_note": (
                "Wolfram independently factors both boundary quartics as "
                "linear times irreducible cubic and confirms that the two "
                "quadratic b-lift discriminants are nonsquares."
            ),
        },
        "ledger_movement": 0,
        "signed_pair_resultant_complete": False,
        "sign_transport_complete": False,
        "role_orbit_11_closed": False,
        "K3_closed": False,
        "KoalaBear_row_closed": False,
        "FLOOR_v2_used": False,
        "S_sparse_bound_claimed": False,
        "nonclaims": [
            "No v4 U_paid, U_Q, U_BC, or U_new value is changed.",
            "The complete cell-11 signed-pair resultant family is not computed here.",
            "Only epsilon=(-1,-1), pivot 1 is reduced; sign and outside-role transport remain open.",
            "Exact local algebra is not an exhaustive affine-slope projection.",
            "The falsified FLOOR v2 random-word first-moment route is not used.",
            "No upper bound for the exact sparse-layer maximum S_sparse is claimed.",
            "The same model generated and audited this packet, so independent review is still required.",
        ],
    }
    verify(payload)
    return payload


def mutation_tests(payload: dict) -> int:
    mutations = []

    def add(name, mutate):
        value = copy.deepcopy(payload)
        mutate(value)
        mutations.append((name, value))

    add("field", lambda x: x.__setitem__("field", PRIME - 2))
    add("source", lambda x: x["provenance"].__setitem__("source_commit", "0" * 40))
    add("pilot", lambda x: x["exact_replay"].__setitem__("pilot_quotient_exact", True))
    add("chart", lambda x: x["exact_replay"].__setitem__("selected_c_row", 6))
    add("tower", lambda x: x["exact_replay"]["charts"][0].__setitem__("exact", False))
    add("remainder", lambda x: x["exact_replay"]["charts"][0]["remainders"].__setitem__(0, "1"))
    add("boundary", lambda x: x["exact_replay"]["boundaries"]["b_leading"].__setitem__("deployed_boundary_empty", False))
    add("root", lambda x: x["exact_replay"]["boundaries"]["c_leading"]["r_deployed_roots"].__setitem__(0, 1))
    add("kernel_hash", lambda x: x["exact_replay"]["kernel"]["kernel"][0].__setitem__("sha256", "0" * 64))
    add("kernel_row", lambda x: x["exact_replay"]["kernel"]["remainders"].__setitem__(9, "1"))
    add("wolfram", lambda x: x["independent_checks"]["wolfram"].__setitem__("b_lift_euler", 1))
    add("ledger", lambda x: x.__setitem__("ledger_movement", 1))
    add("resultant", lambda x: x.__setitem__("signed_pair_resultant_complete", True))
    add("orbit", lambda x: x.__setitem__("role_orbit_11_closed", True))
    add("K3", lambda x: x.__setitem__("K3_closed", True))
    add("sparse", lambda x: x.__setitem__("S_sparse_bound_claimed", True))
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
    parser.add_argument("--assemble", type=Path)
    parser.add_argument("--mutations", action="store_true")
    arguments = parser.parse_args()
    if arguments.assemble:
        payload = assemble(arguments.assemble)
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    else:
        payload = json.loads(CERTIFICATE.read_text())
        verify(payload)
    print("certificate: PASS")
    if arguments.mutations:
        print(f"mutations: PASS ({mutation_tests(payload)}/16 rejected)")


if __name__ == "__main__":
    main()
