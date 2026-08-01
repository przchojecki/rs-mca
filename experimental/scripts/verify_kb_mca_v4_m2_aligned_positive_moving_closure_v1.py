#!/usr/bin/env python3
"""Fail-closed verifier for the aligned-positive moving-cell deletion.

Sage performs the load-bearing finite-field algebra.  This verifier binds the
emitted payload and source files, checks the exact 12/18 atlas fence, audits
the two balanced parity chains and the import/transport composition, and
replays semantic mutations with freshly recomputed payload hashes.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
COMPILER = (
    ROOT
    / "scripts/compile_kb_mca_v4_m2_aligned_positive_moving_closure_v1.sage"
)
CERTIFICATE = (
    ROOT
    / "data/certificates/kb-mca-v4-m2-aligned-positive-moving-closure-v1/"
    "kb_mca_v4_m2_aligned_positive_moving_closure_v1.json"
)
SCHEMA_PATH = (
    ROOT
    / "data/certificates/kb-mca-v4-m2-aligned-positive-moving-closure-v1/"
    "schema.json"
)

SCHEMA = "rs-mca-kb-v4-m2-aligned-positive-moving-closure-v1"
PRIME = 2130706433
EXPECTED_COMPILER_SHA256 = (
    "2ed13fbab353d0ac3017fa31cab68de3f3b66f190061ba63fd277dbdc7958675"
)
EXPECTED_SCHEMA_SHA256 = (
    "659772381a053d2f0e0598a0dfc91502065b07c6685f0fdebb22486f8bf6c41b"
)
EXPECTED_PAYLOAD = (
    "343b691abab47586545aca75393bea1e1fff1dfb63537f059e4faef341893145"
)
ATLAS_SHA256 = "c382adee5be3b72dcb675b4932a681f65ae958f58e24c3f5fdb8163d4d1508b7"
ATLAS_BLOB = "946308dbc014ce952c0c1cc583cc3d579a61aecf"
BASE_COMMIT = "826c0e7610604d550b8dd9b772c197a4e660e525"

DIRECT_CELL_IDS = (
    "M00-R02",
    "M00-R20",
    "M01-R02",
    "M01-R11",
    "M01-R20",
    "M03-R02",
    "M03-R11",
    "M03-R20",
)
BALANCED = {
    "M01-R11": {
        "J": {
            "polynomial": "c8223c17919b39c46a7e55cfeb99badc6f1f5a2060c19a5dd0a11e44f0b276bb",
            "basis": "ca39e61bb131e6374c40c618b593d4628685c9312c57a687d739c6d7e05ade4b",
            "localizer": "ce205ff564851d70594e436f89ad201a5158d685412f7b145fd4721f216fd080",
        },
        "I": {
            "polynomial": "b45202d5ff561fd29573f68af87e4236cfc2f764f090c730ae35e4c61bb5abcf",
            "basis": "716d41185640c419fc02323fea1ae6a4d51c56f7af7b2ebd61d0d7dc82af4da2",
            "localizer": "77c4a7906b263686268a2422e65bd5172c6b790284e55a0b4dcb027b74898c37",
        },
    },
    "M03-R11": {
        "J": {
            "polynomial": "8a77375685f0b7c5c14fe249cfe5b854a4f69c59d1220231b319e1660e2aabb0",
            "basis": "e40e327c73baf2fb8f52f6f77b06948e03d4d6bca4b1402e229d318b207765d6",
            "localizer": "3977ebccf184ea27187b5109166a40e06250afc15476c3dbb36de554c5ea03fb",
        },
        "I": {
            "polynomial": "e0dfb63e9c4120d9e85e126452404bba5d808e2a5bd22fc5075186aabe615793",
            "basis": "b5e83240875f0814497ee8378facc63dd70ae5f287ff3505dce86ce8f0636b05",
            "localizer": "3a4b3feb0c7386b7969735587edf4a024570249ceaa50581a0e7a8348578f2d5",
        },
    },
}
TRANSPORTED = {
    f"M02-{target}" for target in ("R02", "R11", "R20")
}
BASE_DELETED = {
    f"{assignment}-{target}"
    for assignment in ("F02", "F03")
    for target in ("R02", "R11", "R20")
}
MOVING_CLOSED = {
    f"{assignment}-{target}"
    for assignment in ("M00", "M01", "M02", "M03")
    for target in ("R02", "R11", "R20")
}
REMAINING = {
    f"{assignment}-{target}"
    for assignment in ("F00", "F01", "F04", "F05", "F06", "F07")
    for target in ("R02", "R11", "R20")
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def payload_sha(data: dict[str, Any]) -> str:
    copied = dict(data)
    copied.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(copied).encode()).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_balanced(cell: dict[str, Any]) -> None:
    cell_id = cell["cell_id"]
    require(
        cell["full_qslice"]["terminal"] == "SURVIVES_NAMED_LOCALIZATION",
        f"{cell_id} q-slice survivor",
    )
    require(cell["full_qslice"]["nilpotence_index"] is None, f"{cell_id} q nilpotence")
    stages = cell["parity"]
    require([stage["parity"] for stage in stages] == ["J", "I"], f"{cell_id} parity order")
    for stage in stages:
        name = stage["parity"]
        expected = BALANCED[cell_id][name]
        require(stage["polynomial"]["sha256"] == expected["polynomial"], f"{cell_id} {name} polynomial")
        require(stage["basis"]["sha256"] == expected["basis"], f"{cell_id} {name} basis")
        require(stage["reduced_localizer"]["sha256"] == expected["localizer"], f"{cell_id} {name} localizer")
        require("sha256" not in stage["remainder"], f"{cell_id} {name} noncanonical remainder hash")
        require(
            stage["remainder_provenance"]
            == {
                "input_minus_remainder_in_prior_ideal": True,
                "augmented_ideal_equals_direct_parity_ideal": True,
                "representative_sha256_is_not_pinned": True,
            },
            f"{cell_id} {name} remainder provenance",
        )
    require(stages[0]["terminal"] == "SURVIVES_NAMED_LOCALIZATION", f"{cell_id} J terminal")
    require(stages[0]["nilpotence_index"] is None, f"{cell_id} J nilpotence")
    require(stages[1]["terminal"] == "EMPTY_AFTER_NAMED_LOCALIZATION", f"{cell_id} I terminal")
    require(stages[1]["nilpotence_index"] == 2, f"{cell_id} I nilpotence")
    powers = stages[1]["reduced_localizer_powers"]
    require([item["exponent"] for item in powers] == [1, 2], f"{cell_id} I powers")
    require(powers[-1]["terms"] == 0 and powers[-1]["degree"] == -1, f"{cell_id} I zero power")


def verify_direct_cells(data: dict[str, Any]) -> None:
    cells = data["direct_cells"]
    require([cell["cell_id"] for cell in cells] == list(DIRECT_CELL_IDS), "direct cell order and uniqueness")
    for cell in cells:
        cell_id = cell["cell_id"]
        require(cell["method"] == "DIRECT_QSLICE_AND_NAMED_LOCALIZATION", f"{cell_id} method")
        require(len(cell["qslice_generators"]) == 4, f"{cell_id} generator count")
        require(cell["w_zero"]["terminal"] == "EMPTY_AFTER_NAMED_LOCALIZATION", f"{cell_id} w=0 terminal")
        require(cell["w_zero"]["nilpotence_index"] is not None, f"{cell_id} w=0 witness")
        require(cell["terminal"] == "EMPTY_AFTER_NAMED_LOCALIZATION", f"{cell_id} terminal")
        require(cell["ledger_movement"] == 0, f"{cell_id} ledger")
        if cell_id in BALANCED:
            verify_balanced(cell)
        else:
            require(cell["full_qslice"]["terminal"] == "EMPTY_AFTER_NAMED_LOCALIZATION", f"{cell_id} full terminal")
            require(cell["full_qslice"]["nilpotence_index"] is not None, f"{cell_id} full witness")
            require(cell["parity"] == [], f"{cell_id} unexpected parity")


def verify_import(data: dict[str, Any]) -> None:
    imported = data["imported_cell"]
    require(imported["pull_request"] == 1138, "import PR")
    require(imported["commit"] == "cd41c6c71b5b7d114f4ca9b2f5c853ccdd3c341d", "import commit")
    require(imported["cell_id"] == "M00-R11", "import cell")
    require(imported["terminal"] == "EMPTY_AFTER_NAMED_LOCALIZATION", "import terminal")
    require(imported["operational_dependency"] is True, "import operational")
    runtime = imported["runtime_verification"]
    for key in (
        "commit_object_exact",
        "certificate_payload_recomputed",
        "sage_bytes_sha256_exact",
        "sage_result_payload_pin_exact",
        "statement_compatibility_exact",
        "canonical_edge_target_scope_exact",
        "nonclaims_exact",
        "proof_status_exact",
        "fresh_review_green",
    ):
        require(runtime[key] is True, f"import runtime {key}")


def verify_transport(data: dict[str, Any]) -> None:
    transport = data["literal_transport"]
    require(transport["map"] == "b -> b^-1", "transport map")
    require(transport["source_assignment"] == "M01", "transport source")
    require(transport["target_assignment"] == "M02", "transport target")
    for key in ("z_exact", "V_exact", "U_exact"):
        require(transport[key] is True, f"transport {key}")
    require(
        transport["named_unit_transport"]["nonmonomial_factor_multiset_exact"] is True,
        "transport named open",
    )
    require(all(transport["label_factor_multisets_exact"].values()), "transport label factors")
    require(all(transport["computed_full_identity_transport"].values()), "transport quotient identities")
    checks = transport["qslice_checks"]
    require(
        {item["target_cell"] for item in checks} == TRANSPORTED,
        "transport target cells",
    )
    for item in checks:
        require(item["row_count"] == 4, "transport row count")
        require(item["all_cleared_numerators_transport_up_to_projective_sign"] is True, "transport numerator")
        require(item["all_full_rational_zero_loci_transport_by_named_units"] is True, "transport zero locus")


def verify_fence(data: dict[str, Any]) -> None:
    fence = data["open_cell_fence"]
    require(fence["atlas_cells"] == 36, "atlas count")
    require(set(fence["base_deleted_cells"]) == BASE_DELETED, "base deleted fence")
    require(set(fence["moving_cells_closed"]) == MOVING_CLOSED, "moving closed fence")
    require(set(fence["remaining_open_cells"]) == REMAINING, "remaining fence")
    require(fence["remaining_open_count"] == 18, "remaining count")
    require(BASE_DELETED.isdisjoint(MOVING_CLOSED), "base/moving disjoint")
    require((BASE_DELETED | MOVING_CLOSED).isdisjoint(REMAINING), "closed/open disjoint")
    conclusion = data["conclusion"]
    require(conclusion["all_twelve_moving_moving_cells_empty"] is True, "closure conclusion")
    require(set(conclusion["closed_cells"]) == MOVING_CLOSED, "conclusion closed link")
    require(set(conclusion["remaining_open_cells"]) == REMAINING, "conclusion open link")
    require(conclusion["ledger_movement"] == 0, "conclusion ledger")
    require(conclusion["K3_status"] == "OPEN", "conclusion K3")
    require(conclusion["KoalaBear_row_status"] == "OPEN", "conclusion row")


def verify(data: dict[str, Any], *, pin_payload: bool) -> None:
    require(data["payload_sha256"] == payload_sha(data), "payload recomputation")
    if pin_payload:
        require(data["payload_sha256"] == EXPECTED_PAYLOAD, "payload pin")
    require(sha256(COMPILER) == EXPECTED_COMPILER_SHA256, "compiler SHA-256")
    require(sha256(SCHEMA_PATH) == EXPECTED_SCHEMA_SHA256, "schema SHA-256")
    require(data["schema"] == SCHEMA, "schema")
    require(
        data["field"]
        == {
            "base_prime": PRIME,
            "challenge_extension_degree": 6,
            "empty_localization_is_geometric_over_base_closure": True,
        },
        "field",
    )
    require(data["atlas_dependency"]["sha256"] == ATLAS_SHA256, "atlas SHA pin")
    require(data["atlas_dependency"]["git_blob"] == ATLAS_BLOB, "atlas blob pin")
    require(data["base_dependency"]["commit"] == BASE_COMMIT, "base commit")
    require(
        data["scope"]
        == {
            "atlas_cell_count": 36,
            "direct_cell_count": 8,
            "literal_transport_cell_count": 3,
            "imported_cell_count": 1,
            "closed_cell_count": 12,
            "remaining_open_cell_count": 18,
            "ledger_movement": 0,
        },
        "scope",
    )
    require(
        data["execution"]
        == {
            "direct_cells_sharded": True,
            "fresh_sage_process_per_direct_cell": True,
            "reason": "avoid long-lived Sage-Singular IPC state across independent cells",
        },
        "execution",
    )
    require(data["ledger_movement"] == 0, "ledger movement")
    require(data["K3_closed"] is False, "K3 nonclaim")
    require(data["KoalaBear_row_closed"] is False, "row nonclaim")
    require(data["generic_saturation_used"] is False, "generic saturation")
    require(
        data["proof_status"]
        == "PROVED_EXACT_ALL_12_MOVING_MOVING_ALIGNED_POSITIVE_CELLS_EMPTY",
        "proof status",
    )
    require(data["terminal"] == "ALL_12_MOVING_MOVING_CELLS_EMPTY", "terminal")
    require(
        data["nonclaims"]
        == [
            "no deletion of the eighteen remaining fixed-moving atlas cells",
            "no owner, charge, or ledger payment",
            "no K3 or KoalaBear-row closure",
            "no theorem over arbitrary characteristics",
            "no generic saturation or undeclared covariance",
        ],
        "nonclaims",
    )
    verify_direct_cells(data)
    verify_import(data)
    verify_transport(data)
    verify_fence(data)


def repayload(data: dict[str, Any]) -> dict[str, Any]:
    data["payload_sha256"] = payload_sha(data)
    return data


def mutation(path: tuple[Any, ...], value: Any) -> Callable[[dict[str, Any]], None]:
    def apply(data: dict[str, Any]) -> None:
        current: Any = data
        for key in path[:-1]:
            current = current[key]
        current[path[-1]] = value
    return apply


def delete(path: tuple[Any, ...]) -> Callable[[dict[str, Any]], None]:
    def apply(data: dict[str, Any]) -> None:
        current: Any = data
        for key in path[:-1]:
            current = current[key]
        del current[path[-1]]
    return apply


def run_mutations(source: dict[str, Any]) -> int:
    tests: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("schema", mutation(("schema",), "wrong")),
        ("field", mutation(("field", "base_prime"), PRIME - 2)),
        ("scope", mutation(("scope", "closed_cell_count"), 11)),
        ("execution", mutation(("execution", "direct_cells_sharded"), False)),
        ("ledger", mutation(("ledger_movement",), 1)),
        ("K3", mutation(("K3_closed",), True)),
        ("row", mutation(("KoalaBear_row_closed",), True)),
        ("saturation", mutation(("generic_saturation_used",), True)),
        ("status", mutation(("proof_status",), "EXPERIMENTAL")),
        ("terminal", mutation(("terminal",), "SURVIVES")),
        ("nonclaim", delete(("nonclaims", 0))),
        ("atlas-pin", mutation(("atlas_dependency", "sha256"), "0" * 64)),
        ("base-pin", mutation(("base_dependency", "commit"), "0" * 40)),
        ("missing-cell", delete(("direct_cells", 0))),
        ("duplicate-cell", mutation(("direct_cells", 1, "cell_id"), DIRECT_CELL_IDS[0])),
        ("direct-terminal", mutation(("direct_cells", 0, "terminal"), "SURVIVES")),
        ("direct-ledger", mutation(("direct_cells", 0, "ledger_movement"), 1)),
        ("balanced-order", mutation(("direct_cells", 3, "parity", 0, "parity"), "I")),
        ("balanced-basis", mutation(("direct_cells", 3, "parity", 0, "basis", "sha256"), "0" * 64)),
        ("remainder-owner", mutation(("direct_cells", 3, "parity", 0, "remainder_provenance", "input_minus_remainder_in_prior_ideal"), False)),
        ("nilpotence", mutation(("direct_cells", 3, "parity", 1, "nilpotence_index"), None)),
        ("import", mutation(("imported_cell", "runtime_verification", "fresh_review_green"), False)),
        ("transport-map", mutation(("literal_transport", "map"), "b -> b")),
        ("transport-identity", mutation(("literal_transport", "U_exact"), False)),
        ("transport-target", mutation(("literal_transport", "qslice_checks", 0, "target_cell"), "M01-R02")),
        ("fence-count", mutation(("open_cell_fence", "remaining_open_count"), 17)),
        ("fence-overlap", mutation(("open_cell_fence", "remaining_open_cells", 0), "M00-R02")),
        ("conclusion", mutation(("conclusion", "all_twelve_moving_moving_cells_empty"), False)),
        ("conclusion-link", delete(("conclusion", "closed_cells", 0))),
    ]
    rejected = 0
    for name, mutate in tests:
        candidate = copy.deepcopy(source)
        mutate(candidate)
        repayload(candidate)
        try:
            verify(candidate, pin_payload=False)
        except (AssertionError, KeyError, IndexError, TypeError):
            rejected += 1
        else:
            raise AssertionError(f"mutation accepted: {name}")
    require(rejected == len(tests), "mutation count")
    return rejected


def main() -> None:
    if not __debug__:
        raise RuntimeError("optimized Python execution is refused")
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    data = json.loads(CERTIFICATE.read_text())
    verify(data, pin_payload=True)
    mutations = run_mutations(data) if args.tamper_selftest else 0
    print(
        "PASS aligned-positive moving closure verifier "
        f"payload_sha256={data['payload_sha256']} mutations={mutations}"
    )


if __name__ == "__main__":
    main()
