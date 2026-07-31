#!/usr/bin/env python3
"""Verify the KoalaBear inner-degree-12 outer-subdegree route cut.

The proof is geometric.  This replay checks the exact parent bindings,
degree ledger, complete primitive degree-five subdegree table, challenge-field
fifth-power arithmetic, surviving rows, scope guards, and fail-closed payload.
It does not enumerate endpoint records or claim a ledger payment.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import subprocess
from pathlib import Path
from typing import Any, Callable


if not __debug__:
    raise RuntimeError("verifier refuses optimized Python execution")


class VerificationError(RuntimeError):
    """Raised when an exact certificate condition fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
CERTIFICATE = (
    ROOT
    / "data"
    / "certificates"
    / "kb-mca-v4-m12-outer-subdegree-route-cut-v1"
    / "kb_mca_v4_m12_outer_subdegree_route_cut_v1.json"
)

P = 2_130_706_433
FIELD_DEGREE = 6
M = 12
N = 5
EXPECTED_SCHEMA = "kb-mca-v4-m12-outer-subdegree-route-cut-v1"
EXPECTED_STATUS = "PROVED_M12_OUTER_SUBDEGREE_ROUTE_CUT_ROW_OPEN"
EXPECTED_PARENT_HEAD = "e287c54252c7872e1745c7594cfef62b74a65cf5"
EXPECTED_PARENT_PATH = (
    "experimental/data/certificates/"
    "kb-mca-v4-degree60-source-pencil-rank-compiler-v1/"
    "kb_mca_v4_degree60_source_pencil_rank_compiler_v1.json"
)
EXPECTED_PARENT_BLOB = "5c16c7884b349d7e474b8dfc1267ab357ef0d477"
EXPECTED_PARENT_PAYLOAD = (
    "6d4bc83e40e491f02f7d265b021628ffb7d52b1978c0655f83e5a9d3e0a9f4bb"
)
EXPECTED_PARENT_TERMINAL = "TRANSVERSE_OUTER_CORRESPONDENCE_UNPAID"
EXPECTED_PARENT_NOTE = (
    "experimental/notes/frontier-adjacent/"
    "kb_mca_v4_degree60_source_pencil_rank_compiler_v1.md"
)
EXPECTED_PARENT_NOTE_BLOB = "b4a69440c518f22189ec2060cb3a3a500a23e724"

INITIAL_ROWS = [
    {"r": 1, "delta": 48},
    {"r": 2, "delta": 24},
    {"r": 3, "delta": 16},
    {"r": 4, "delta": 12},
]
SURVIVING_ROWS = [
    {"r": 2, "delta": 24},
    {"r": 4, "delta": 12},
]
DELETED_ROWS = [
    {"r": 1, "delta": 48},
    {"r": 3, "delta": 16},
]
PRIMITIVE_CATALOGUE = [
    {"group": "C5", "subdegrees": [1, 1, 1, 1, 1]},
    {"group": "D10", "subdegrees": [1, 2, 2]},
    {"group": "AGL(1,5)", "subdegrees": [1, 4]},
    {"group": "A5", "subdegrees": [1, 4]},
    {"group": "S5", "subdegrees": [1, 4]},
]
EXPECTED_BINDINGS = [
    {
        "binding_id": "KB_M12_OUTER_CUT::parent_certificate",
        "commit": EXPECTED_PARENT_HEAD,
        "path": EXPECTED_PARENT_PATH,
        "blob_oid": EXPECTED_PARENT_BLOB,
        "role": (
            "degree-twelve outer profile, transverse degree ledger, "
            "and primitive degree-five catalogue"
        ),
    },
    {
        "binding_id": "KB_M12_OUTER_CUT::parent_note",
        "commit": EXPECTED_PARENT_HEAD,
        "path": EXPECTED_PARENT_NOTE,
        "blob_oid": EXPECTED_PARENT_NOTE_BLOB,
        "role": "geometric component interpretation and challenge-field descent",
    },
]
EXPECTED_NONCLAIMS = [
    "Neither surviving inner-degree-twelve type is deleted or paid.",
    "No endpoint-record census is claimed.",
    (
        "No parameter-to-carrier, received-data, explaining-polynomial, "
        "or slope bridge is proved."
    ),
    (
        "No inner-degree-twelve, u=2, K3, or KoalaBear row closure "
        "is claimed."
    ),
    "No ledger quantity moves.",
]


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def payload_hash(value: dict[str, Any]) -> str:
    unhashed = dict(value)
    unhashed.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(unhashed).encode()).hexdigest()


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_json_text(text: str, label: str) -> dict[str, Any]:
    try:
        value = json.loads(text, object_pairs_hook=reject_duplicate_pairs)
    except (json.JSONDecodeError, VerificationError) as error:
        raise VerificationError(f"cannot parse {label}: {error}") from error
    require(isinstance(value, dict), f"{label} must contain a JSON object")
    return value


def load_json(path: Path) -> dict[str, Any]:
    try:
        return parse_json_text(path.read_text(), str(path))
    except OSError as error:
        raise VerificationError(f"cannot read certificate: {path}") from error


def git_output(*arguments: str) -> str:
    try:
        completed = subprocess.run(
            ["git", *arguments],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        raise VerificationError(
            f"git {' '.join(arguments)} failed: {error.stderr.strip()}"
        ) from error
    return completed.stdout.strip()


def exact_keys(value: Any, keys: set[str], label: str) -> None:
    require(isinstance(value, dict), f"{label} must be an object")
    actual = set(value)
    require(
        actual == keys,
        f"{label} keys mismatch: missing={sorted(keys - actual)}, "
        f"extra={sorted(actual - keys)}",
    )


def exact_schema(data: dict[str, Any]) -> None:
    exact_keys(
        data,
        {
            "schema",
            "payload_sha256",
            "statement",
            "parent_stack",
            "degree_twelve_outer_profile",
            "geometric_component_gate",
            "primitive_degree_five_catalogue",
            "subdegree_three_exclusion",
            "subdegree_one_exclusion",
            "surviving_degree_twelve_rows",
            "source_bindings",
            "conclusion",
            "nonclaims",
        },
        "certificate",
    )
    exact_keys(
        data["statement"],
        {
            "workboard_item",
            "row",
            "object",
            "agreement",
            "B_star",
            "deployed_characteristic",
            "challenge_field_degree",
            "endpoint_degree",
            "component_u",
            "inner_degree",
            "outer_degree",
            "status",
            "ledger_movement",
        },
        "statement",
    )
    exact_keys(
        data["parent_stack"],
        {
            "head_commit",
            "certificate_path",
            "certificate_blob_oid",
            "certificate_payload_sha256",
            "imported_terminal",
            "imported_transverse_type_count",
        },
        "parent_stack",
    )
    exact_keys(
        data["degree_twelve_outer_profile"],
        {
            "outer_defined_over",
            "outer_separable",
            "pole_orders",
            "unique_pole_K_rational",
            "zero_orders",
            "all_zeros_distinct_K_rational",
            "initial_rows",
        },
        "degree_twelve_outer_profile",
    )
    exact_keys(
        data["geometric_component_gate"],
        {
            "component",
            "geometrically_irreducible",
            "non_diagonal",
            "bidegree",
            "degree_identity",
            "cover_degree_upper_bound",
            "outer_component_interpretation",
        },
        "geometric_component_gate",
    )
    require(
        isinstance(data["primitive_degree_five_catalogue"], list),
        "primitive catalogue must be a list",
    )
    for index, row in enumerate(data["primitive_degree_five_catalogue"]):
        exact_keys(row, {"group", "subdegrees"}, f"catalogue[{index}]")
    exact_keys(
        data["subdegree_three_exclusion"],
        {
            "candidate_r",
            "candidate_delta",
            "outer_prime_degree_implies_geometric_indecomposability",
            "primitive_catalogue_complete",
            "catalogue_has_subdegree_three",
            "terminal",
        },
        "subdegree_three_exclusion",
    )
    exact_keys(
        data["subdegree_one_exclusion"],
        {
            "candidate_r",
            "candidate_delta",
            "component_is_graph_of_nonidentity_mobius_map",
            "nontrivial_deck_group_order",
            "cover_is_tame_cyclic_degree_five",
            "total_branch_point_count",
            "second_total_branch_point_K_rational",
            "K_rational_normal_form",
            "p_mod_5",
            "q_mod_5",
            "gcd_5_q_minus_1",
            "fifth_power_permutates_K",
            "maximum_distinct_K_rational_zeros_in_normal_form",
            "required_distinct_simple_K_rational_zeros",
            "terminal",
        },
        "subdegree_one_exclusion",
    )
    require(isinstance(data["source_bindings"], list), "bindings must be a list")
    for index, binding in enumerate(data["source_bindings"]):
        exact_keys(
            binding,
            {"binding_id", "commit", "path", "blob_oid", "role"},
            f"source_bindings[{index}]",
        )
    exact_keys(
        data["conclusion"],
        {
            "deleted_degree_twelve_rows",
            "remaining_degree_twelve_type_count",
            "remaining_global_transverse_type_count",
            "terminal",
            "m12_closed",
            "u2_closed",
            "K3_closed",
            "row_closed",
        },
        "conclusion",
    )


def verify_statement_and_parent(data: dict[str, Any]) -> None:
    statement = data["statement"]
    require(data["schema"] == EXPECTED_SCHEMA, "schema mismatch")
    require(statement["workboard_item"] == "K3", "wrong workboard item")
    require(statement["row"] == "KoalaBear MCA at 2^-128", "wrong row")
    require(statement["object"] == "MCA", "wrong object")
    require(statement["agreement"] == 1_116_048, "wrong agreement")
    require(statement["B_star"] == "274980728111395087", "wrong B_star")
    require(statement["deployed_characteristic"] == P, "wrong prime")
    require(statement["challenge_field_degree"] == FIELD_DEGREE, "field degree")
    require(statement["endpoint_degree"] == 60, "endpoint degree")
    require(statement["component_u"] == 2, "component u")
    require(statement["inner_degree"] == M, "inner degree")
    require(statement["outer_degree"] == N, "outer degree")
    require(statement["status"] == EXPECTED_STATUS, "status mismatch")
    require(statement["ledger_movement"] == 0, "ledger movement is nonzero")

    parent = data["parent_stack"]
    require(parent["head_commit"] == EXPECTED_PARENT_HEAD, "parent head")
    require(parent["certificate_path"] == EXPECTED_PARENT_PATH, "parent path")
    require(parent["certificate_blob_oid"] == EXPECTED_PARENT_BLOB, "parent blob")
    require(
        parent["certificate_payload_sha256"] == EXPECTED_PARENT_PAYLOAD,
        "parent payload",
    )
    require(parent["imported_terminal"] == EXPECTED_PARENT_TERMINAL, "parent terminal")
    require(parent["imported_transverse_type_count"] == 26, "parent type count")


def verify_degree_ledger_and_profile(data: dict[str, Any]) -> None:
    profile = data["degree_twelve_outer_profile"]
    require(profile["outer_defined_over"] == "K=F_(p^6)", "outer field")
    require(profile["outer_separable"] is True, "outer separability")
    require(profile["pole_orders"] == [5], "pole profile")
    require(profile["unique_pole_K_rational"] is True, "pole rationality")
    require(profile["zero_orders"] == [1, 1, 1, 1, 1], "zero profile")
    require(
        profile["all_zeros_distinct_K_rational"] is True,
        "zero rationality",
    )

    computed_rows = [
        {"r": r, "delta": 4 * M // r}
        for r in range(1, N)
        if (4 * M) % r == 0 and 4 * M // r <= M * M
    ]
    require(computed_rows == INITIAL_ROWS, "internal degree-ledger rows")
    require(profile["initial_rows"] == computed_rows, "certificate initial rows")
    for row in profile["initial_rows"]:
        require(row["r"] * row["delta"] == 4 * M, "delta-r identity")
        require(row["r"] <= N - 1, "outer subdegree upper bound")
        require(row["delta"] <= M * M, "cover-degree upper bound")

    gate = data["geometric_component_gate"]
    require(gate["component"] == "C=closure((h x h)(Gamma))", "component")
    require(gate["geometrically_irreducible"] is True, "geometric irreducibility")
    require(gate["non_diagonal"] is True, "non-diagonal gate")
    require(gate["bidegree"] == "(r,r)", "bidegree")
    require(gate["degree_identity"] == "delta*r=4*m", "degree identity")
    require(gate["cover_degree_upper_bound"] == "delta<=m^2", "cover bound")
    require(
        gate["outer_component_interpretation"]
        == "point-stabilizer suborbit of geometric monodromy",
        "component interpretation",
    )


def verify_subdegree_three_cut(data: dict[str, Any]) -> None:
    catalogue = data["primitive_degree_five_catalogue"]
    require(catalogue == PRIMITIVE_CATALOGUE, "primitive catalogue mismatch")
    require(len(catalogue) == 5, "primitive degree-five group count")
    for row in catalogue:
        require(sum(row["subdegrees"]) == N, f"subdegrees for {row['group']}")
        require(row["subdegrees"][0] == 1, f"diagonal subdegree for {row['group']}")
    require(
        all(3 not in row["subdegrees"] for row in catalogue),
        "catalogue unexpectedly contains subdegree three",
    )
    cut = data["subdegree_three_exclusion"]
    require(cut["candidate_r"] == 3, "r=3 candidate")
    require(cut["candidate_delta"] == 16, "r=3 delta")
    require(
        cut["outer_prime_degree_implies_geometric_indecomposability"] is True,
        "prime-degree indecomposability",
    )
    require(cut["primitive_catalogue_complete"] is True, "catalogue completeness")
    require(cut["catalogue_has_subdegree_three"] is False, "subdegree-three flag")
    require(
        cut["terminal"] == "M12_R3_PRIMITIVE_SUBDEGREE_ABSENT",
        "r=3 terminal",
    )


def verify_subdegree_one_cut(data: dict[str, Any]) -> None:
    cut = data["subdegree_one_exclusion"]
    expected = {
        "candidate_r": 1,
        "candidate_delta": 48,
        "component_is_graph_of_nonidentity_mobius_map": True,
        "nontrivial_deck_group_order": 5,
        "cover_is_tame_cyclic_degree_five": True,
        "total_branch_point_count": 2,
        "second_total_branch_point_K_rational": True,
        "K_rational_normal_form": "a*x^5+b with a nonzero",
        "p_mod_5": 3,
        "q_mod_5": 4,
        "gcd_5_q_minus_1": 1,
        "fifth_power_permutates_K": True,
        "maximum_distinct_K_rational_zeros_in_normal_form": 1,
        "required_distinct_simple_K_rational_zeros": 5,
        "terminal": "M12_R1_CYCLIC_FIFTH_POWER_FIBER_CONTRADICTION",
    }
    require(cut == expected, "subdegree-one exclusion changed")
    q = P**FIELD_DEGREE
    require(P % 5 == cut["p_mod_5"], "p modulo five")
    require(q % 5 == cut["q_mod_5"], "q modulo five")
    require(math.gcd(5, q - 1) == cut["gcd_5_q_minus_1"], "fifth-power gcd")
    require(P != 5, "cover is not tame")
    require(
        cut["maximum_distinct_K_rational_zeros_in_normal_form"]
        < cut["required_distinct_simple_K_rational_zeros"],
        "normal-form zero count is not contradictory",
    )


def verify_conclusion_and_nonclaims(data: dict[str, Any]) -> None:
    require(data["surviving_degree_twelve_rows"] == SURVIVING_ROWS, "survivors")
    survivors = [row for row in INITIAL_ROWS if row not in DELETED_ROWS]
    require(survivors == SURVIVING_ROWS, "computed survivors")
    conclusion = data["conclusion"]
    require(conclusion["deleted_degree_twelve_rows"] == DELETED_ROWS, "deleted rows")
    require(conclusion["remaining_degree_twelve_type_count"] == 2, "m12 count")
    require(
        conclusion["remaining_global_transverse_type_count"] == 24,
        "global type count",
    )
    require(26 - len(DELETED_ROWS) == 24, "global count arithmetic")
    require(
        conclusion["terminal"] == "M12_TRANSVERSE_TYPES_R2_R4_UNPAID",
        "conclusion terminal",
    )
    for key in ("m12_closed", "u2_closed", "K3_closed", "row_closed"):
        require(conclusion[key] is False, f"forbidden closure claim: {key}")
    require(data["nonclaims"] == EXPECTED_NONCLAIMS, "nonclaims changed")


def verify_bindings(data: dict[str, Any]) -> None:
    require(data["source_bindings"] == EXPECTED_BINDINGS, "source bindings")
    for binding in data["source_bindings"]:
        git_output("cat-file", "-e", f"{binding['commit']}^{{commit}}")
        actual_blob = git_output(
            "rev-parse", f"{binding['commit']}:{binding['path']}"
        )
        require(
            actual_blob == binding["blob_oid"],
            f"blob binding mismatch: {binding['binding_id']}",
        )

    parent = parse_json_text(
        git_output("show", f"{EXPECTED_PARENT_HEAD}:{EXPECTED_PARENT_PATH}"),
        "historical parent certificate",
    )
    require(payload_hash(parent) == parent["payload_sha256"], "parent self-hash")
    require(parent["payload_sha256"] == EXPECTED_PARENT_PAYLOAD, "parent payload")
    require(
        parent.get("conclusion", {}).get("terminal") == EXPECTED_PARENT_TERMINAL,
        "parent terminal",
    )
    parent_m12 = next(
        row
        for row in parent["transverse_outer_terminal"]["rows"]
        if row["m"] == M
    )
    require(
        parent_m12 == {
            "m": 12,
            "n": 5,
            "r_delta": [[1, 48], [2, 24], [3, 16], [4, 12]],
        },
        "historical parent m12 rows",
    )
    parent_degree_five = next(
        row
        for row in parent["same_fiber_route_cut"]["small_degree_catalogue"]
        if row["degree"] == 5
    )
    require(
        parent_degree_five["subdegree_rows"]
        == [[1, 1, 1, 1, 1], [1, 2, 2], [1, 4], [1, 4], [1, 4]],
        "historical parent degree-five catalogue",
    )


def verify_certificate(
    data: dict[str, Any], *, check_git_bindings: bool = True
) -> None:
    exact_schema(data)
    digest = data["payload_sha256"]
    require(
        isinstance(digest, str)
        and len(digest) == 64
        and all(character in "0123456789abcdef" for character in digest),
        "payload_sha256 is not a lowercase SHA-256 digest",
    )
    require(payload_hash(data) == digest, "payload hash mismatch")
    verify_statement_and_parent(data)
    verify_degree_ledger_and_profile(data)
    verify_subdegree_three_cut(data)
    verify_subdegree_one_cut(data)
    verify_conclusion_and_nonclaims(data)
    if check_git_bindings:
        verify_bindings(data)
    else:
        require(data["source_bindings"] == EXPECTED_BINDINGS, "bindings")


def reseal(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


def run_tamper_selftest(original: dict[str, Any]) -> int:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        (
            "restore-r3",
            lambda value: value["surviving_degree_twelve_rows"].append(
                {"r": 3, "delta": 16}
            ),
        ),
        (
            "delete-r2",
            lambda value: value["surviving_degree_twelve_rows"].pop(0),
        ),
        (
            "primitive-subdegree-three",
            lambda value: value["primitive_degree_five_catalogue"][2].__setitem__(
                "subdegrees", [1, 3, 1]
            ),
        ),
        (
            "drop-geometric-irreducibility",
            lambda value: value["geometric_component_gate"].__setitem__(
                "geometrically_irreducible", False
            ),
        ),
        (
            "non-rational-pole",
            lambda value: value["degree_twelve_outer_profile"].__setitem__(
                "unique_pole_K_rational", False
            ),
        ),
        (
            "wrong-field-residue",
            lambda value: value["subdegree_one_exclusion"].__setitem__(
                "q_mod_5", 1
            ),
        ),
        (
            "nonbijective-fifth-power",
            lambda value: value["subdegree_one_exclusion"].__setitem__(
                "fifth_power_permutates_K", False
            ),
        ),
        (
            "too-many-normal-form-zeros",
            lambda value: value["subdegree_one_exclusion"].__setitem__(
                "maximum_distinct_K_rational_zeros_in_normal_form", 5
            ),
        ),
        (
            "parent-payload",
            lambda value: value["parent_stack"].__setitem__(
                "certificate_payload_sha256", "0" * 64
            ),
        ),
        (
            "source-binding",
            lambda value: value["source_bindings"][0].__setitem__(
                "blob_oid", "0" * 40
            ),
        ),
        (
            "claim-row-closed",
            lambda value: value["conclusion"].__setitem__("row_closed", True),
        ),
        (
            "move-ledger",
            lambda value: value["statement"].__setitem__("ledger_movement", 1),
        ),
        ("drop-nonclaim", lambda value: value["nonclaims"].pop()),
        ("extra-top-level-field", lambda value: value.__setitem__("extra", 1)),
    ]
    passed = 0
    for name, mutate in mutations:
        candidate = copy.deepcopy(original)
        mutate(candidate)
        reseal(candidate)
        try:
            verify_certificate(candidate, check_git_bindings=False)
        except VerificationError:
            passed += 1
        else:
            raise VerificationError(f"tamper survived: {name}")

    bad_hash = copy.deepcopy(original)
    bad_hash["payload_sha256"] = "0" * 64
    try:
        verify_certificate(bad_hash, check_git_bindings=False)
    except VerificationError:
        passed += 1
    else:
        raise VerificationError("tamper survived: payload-hash")

    try:
        parse_json_text('{"duplicate":1,"duplicate":2}', "duplicate-key test")
    except VerificationError:
        passed += 1
    else:
        raise VerificationError("tamper survived: duplicate-json-key")
    return passed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the committed certificate",
    )
    parser.add_argument(
        "--tamper-selftest",
        action="store_true",
        help="run fail-closed semantic mutation tests",
    )
    arguments = parser.parse_args()
    if not arguments.check and not arguments.tamper_selftest:
        parser.error("at least one of --check or --tamper-selftest is required")

    certificate = load_json(CERTIFICATE)
    verify_certificate(certificate, check_git_bindings=True)
    print(
        "PASS: m=12 outer r=1 and r=3 deleted; "
        "survivors are (2,24) and (4,12)"
    )
    if arguments.tamper_selftest:
        count = run_tamper_selftest(certificate)
        print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
