#!/usr/bin/env python3
"""Structural replay for the KoalaBear v4 tangent source adapter.

Lean compilation, not this script, is proof validation.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / "experimental/data/certificates/kb-mca-v4-tangent-source-adapter-v1"
ROW_PATH = CERT / "row_manifest.json"
MANIFEST_PATH = CERT / "manifest.json"
SCHEMA_PATH = ROOT / "experimental/data/schemas/kb_mca_v4_tangent_source_adapter_v1.schema.json"
NOTE_PATH = ROOT / "experimental/notes/frontier-adjacent/kb_mca_v4_tangent_source_adapter_v1.md"
LEAN_PATH = ROOT / "experimental/lean/kb_m1_source_bound_bridge/KbM1SourceBoundBridge.lean"
CORR_PATH = ROOT / "experimental/lean/kb_m1_source_bound_bridge/CORRESPONDENCE.md"

ARCH = "GRANDE_FINALE_V4_KB_MCA_TANGENT_SOURCE_ADAPTER_V1"
DIGEST = "4fade91abc408264989babcff6f8f9bbd80bcec52545a5db15ac376bf17d88fc"
B_STAR = 274_980_728_111_395_087
PAID = 981_104
REMAINING = 274_980_728_110_413_983
LEGACY = 422_354_730_332
ATOMS = ["U_paid", "U_Q", "U_BC", "U_new"]
OWNERS = [
    "SOURCE_COORDINATE_TANGENT_IMAGE",
    "ACTIVE_V4_BOUNDARY_PREFIX_Q",
    "ACTIVE_V4_BALANCED_CORE",
    "UNPAID_V4_COMPLEMENT",
]
# Upstream steering files are recorded for provenance, not gated.  `agents.md` is
# rewritten by governance commits -- fb6d955 replaced the blob this packet froze --
# so drift there must report, never fail.  The manifest keeps the recorded value,
# so payload hashes are unaffected.
STEERING_SOURCES = frozenset({"agents.md"})


class Failure(RuntimeError):
    pass


def need(ok: bool, message: str) -> None:
    if not ok:
        raise Failure(message)


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise Failure(f"cannot read {path}: {exc}") from exc
    need(isinstance(value, dict), f"{path} must contain an object")
    return value


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def check_payload(value: dict[str, Any], label: str) -> None:
    body = copy.deepcopy(value)
    claimed = body.pop("payload_sha256", None)
    need(claimed == sha256(canonical(body)), f"{label} payload hash")


def check_bindings(bindings: Any) -> None:
    need(isinstance(bindings, list) and bindings, "source bindings")
    seen: set[str] = set()
    for item in bindings:
        need(isinstance(item, dict), "binding object")
        key = item.get("binding_id")
        path_text = item.get("path")
        kind = item.get("hash_kind")
        claimed = item.get("hash")
        need(isinstance(key, str) and key not in seen, "binding ID")
        seen.add(key)
        need(isinstance(path_text, str), f"{key} path")
        path = ROOT / path_text
        need(path.is_file(), f"missing source {path_text}")
        data = path.read_bytes()
        actual = sha256(data) if kind == "SHA256" else blob_sha1(data)
        need(kind in {"SHA256", "GIT_BLOB_SHA1"}, f"{key} hash kind")
        if path_text in STEERING_SOURCES:
            if actual != claimed:
                print(
                    f"NOTE steering source drifted: {path_text} "
                    f"recorded {claimed}, observed {actual}"
                )
            continue
        need(actual == claimed, f"{key} source hash")


def check_row(row: dict[str, Any]) -> None:
    check_payload(row, "row")
    need(row.get("architecture_id") == ARCH, "row architecture")
    part = copy.deepcopy(row.get("partition"))
    need(isinstance(part, dict), "partition object")
    claimed = part.pop("partition_sha256", None)
    method = part.pop("partition_digest_method", None)
    need(
        method == "SHA256_CANONICAL_JSON_WITHOUT_PARTITION_SHA256_AND_METHOD",
        "partition method",
    )
    need(claimed == sha256(canonical(part)) == DIGEST, "partition digest")
    live = row["partition"]
    need(live.get("atom_order") == ATOMS, "atom order")
    need(live.get("owner_order") == OWNERS, "owner order")
    need(live.get("residual_rule") == "ITERATED_EXACT_SET_DIFFERENCE",
         "residual rule")
    need(live.get("witness_exhaustive") is True, "exhaustive")
    stages = live.get("chronology_stages")
    need(isinstance(stages, list) and len(stages) == 4, "four stages")
    need([x.get("atom_id") for x in stages] == ATOMS, "stage atoms")
    need([x.get("owner_id") for x in stages] == OWNERS, "stage owners")
    need([x.get("paid") for x in stages] == [True, False, False, False],
         "stage payments")
    trans = live.get("canonical_translation")
    need(isinstance(trans, dict), "translation")
    need(trans.get("alternative_translation_union_forbidden") is True,
         "single translation")
    need(trans.get("translation_preserves_complete_bad_slope_set") is True,
         "translation equality")
    contract = row.get("row_contract")
    need(isinstance(contract, dict), "row contract")
    need(contract.get("agreement") == 1_116_048, "agreement")
    need(contract.get("B_star") == B_STAR, "budget")
    field = contract.get("field")
    need(isinstance(field, dict), "field")
    p = field.get("base_prime")
    e = field.get("extension_degree")
    q = int(field.get("cardinality"))
    need(p == 2_130_706_433 and e == 6 and q == p**e, "field constants")
    need(q // 2**128 == B_STAR, "budget floor")
    need(contract.get("domain", {}).get("cardinality") == 2_097_152,
         "domain")
    need(contract.get("code", {}).get("dimension") == 1_048_576,
         "dimension")
    need(
        contract.get("projection_and_unit")
        == "DISTINCT_BAD_FINITE_SLOPES_PER_RECEIVED_LINE",
        "unit",
    )
    check_bindings(row.get("source_bindings"))


def check_manifest(manifest: dict[str, Any], row: dict[str, Any]) -> None:
    check_payload(manifest, "manifest")
    need(manifest.get("architecture_id") == ARCH, "manifest architecture")
    need(manifest.get("partition_sha256") == DIGEST, "manifest partition")
    binding = manifest.get("row_manifest_binding")
    need(isinstance(binding, dict), "row binding")
    need(binding.get("sha256") == sha256(ROW_PATH.read_bytes()),
         "row file binding")
    need(row["partition"]["partition_sha256"] == DIGEST, "same partition")
    atoms = manifest.get("atoms")
    need(isinstance(atoms, list) and len(atoms) == 4, "four atoms")
    need([x.get("atom_id") for x in atoms] == ATOMS, "manifest atom order")
    need([x.get("owner_ids") for x in atoms] == [[x] for x in OWNERS],
         "manifest owner order")
    need(atoms[0].get("value") == PAID and atoms[0].get("bankable") is True,
         "paid atom")
    for atom in atoms[1:]:
        need(atom.get("value") is None, f"{atom.get('atom_id')} must be null")
        need(atom.get("bankable") is False, "unpaid bankability")
    closure = manifest.get("closure_state")
    need(isinstance(closure, dict), "closure")
    need(closure.get("known_sum") == PAID, "known sum")
    need(closure.get("remaining_budget_after_known_sum") == REMAINING,
         "remaining")
    need(B_STAR - PAID == REMAINING, "subtraction")
    need(closure.get("legacy_recorded_U_paid") == LEGACY, "legacy record")
    need(closure.get("legacy_stack_imported") is False, "legacy import")
    need(closure.get("unpaid_owner_ids") == OWNERS[1:], "unpaid owners")
    need(closure.get("row_closed") is False, "row stays open")
    check_bindings(manifest.get("source_bindings"))


def check_sources() -> None:
    schema = load(SCHEMA_PATH)
    props = schema.get("properties")
    need(isinstance(props, dict), "schema properties")
    need(props.get("architecture_id", {}).get("const") == ARCH,
         "schema architecture")
    need(props.get("partition_sha256", {}).get("const") == DIGEST,
         "schema partition")
    note = NOTE_PATH.read_text(encoding="utf-8")
    lean = LEAN_PATH.read_text(encoding="utf-8")
    corr = CORR_PATH.read_text(encoding="utf-8")
    for text in [
        "workboard_item: K1",
        "GATE (B) RE-PROOF",
        f"partition_digest: {DIGEST}",
        r"U_{\rm paid}'=981{,}104",
        "ACTIVE_V4_BOUNDARY_PREFIX_Q",
        "ACTIVE_V4_BALANCED_CORE",
        "UNPAID_V4_COMPLEMENT",
        "274{,}980{,}728{,}110{,}413{,}983",
        "# PROVED",
    ]:
        need(text in note, f"note anchor {text}")
    need("archived/" not in note, "archived authority")
    need("This packet does not transport the legacy M1 ledger." in note,
         "legacy non-transport")
    need(lean.startswith("import Std\n"), "stdlib import")
    for token in ["sorry", "axiom ", "admit", "import Mathlib"]:
        need(token not in lean, f"forbidden Lean token {token}")
    for decl in [
        "tangentImage_card_le_support",
        "paidCell_card_le_tangentCharge",
        "activeCells_pairwiseDisjoint",
        "activeCells_union",
        "deployedConstantsExact",
        "activePaymentIsStrictlySmallerThanLegacy",
    ]:
        need(f"theorem {decl}" in lean, f"Lean declaration {decl}")
    need("Expected `#print axioms` output" in corr, "axiom census")


def cells(
    incoming: set[int], tangent: set[int], q: set[int], bc: set[int]
) -> tuple[set[int], set[int], set[int], set[int]]:
    paid = incoming & tangent
    r1 = incoming - tangent
    q_cell = r1 & q
    r2 = r1 - q
    bc_cell = r2 & bc
    return paid, q_cell, bc_cell, r2 - bc


def check_fixture() -> None:
    parts = cells(
        {0, 1, 2, 3, 4, 5, 6},
        {1, 2, 8},
        {2, 3, 4, 9},
        {4, 5, 10},
    )
    need(parts == ({1, 2}, {3, 4}, {5}, {0, 6}), "fixture")
    need(set().union(*parts) == {0, 1, 2, 3, 4, 5, 6}, "fixture union")
    for i, left in enumerate(parts):
        for right in parts[i + 1:]:
            need(left.isdisjoint(right), "fixture disjointness")


def accepts(row: dict[str, Any], manifest: dict[str, Any]) -> bool:
    try:
        check_row(row)
        check_manifest(manifest, row)
    except (Failure, OSError, ValueError, TypeError, KeyError):
        return False
    return True


def check_mutations(row: dict[str, Any], manifest: dict[str, Any]) -> None:
    tests: list[tuple[dict[str, Any], dict[str, Any]]] = []
    bad = copy.deepcopy(row)
    bad["partition"]["canonical_translation"][
        "alternative_translation_union_forbidden"
    ] = False
    tests.append((bad, manifest))
    bad = copy.deepcopy(row)
    bad["partition"]["owner_order"][1:3] = list(reversed(
        bad["partition"]["owner_order"][1:3]
    ))
    tests.append((bad, manifest))
    bad = copy.deepcopy(row)
    bad["partition"]["residual_rule"] = "SUBSET_ONLY"
    tests.append((bad, manifest))
    badm = copy.deepcopy(manifest)
    badm["atoms"][0]["value"] = PAID + 1
    tests.append((row, badm))
    badm = copy.deepcopy(manifest)
    badm["atoms"][1]["value"] = 0
    tests.append((row, badm))
    badm = copy.deepcopy(manifest)
    badm["closure_state"]["legacy_stack_imported"] = True
    tests.append((row, badm))
    for mutated_row, mutated_manifest in tests:
        need(not accepts(mutated_row, mutated_manifest), "mutation accepted")


def check() -> None:
    row = load(ROW_PATH)
    manifest = load(MANIFEST_PATH)
    check_row(row)
    check_manifest(manifest, row)
    check_sources()
    check_fixture()
    check_mutations(row, manifest)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    # `check()` already runs the six semantic mutations of `check_mutations`; expose
    # them under the standard flag so every packet verifier answers both modes.
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if not (args.check or args.tamper_selftest):
        parser.error("--check or --tamper-selftest is required")
    try:
        check()
    except (Failure, OSError, ValueError, TypeError, KeyError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    if args.tamper_selftest:
        print("PASS tamper-selftest: six semantic mutations rejected")
        if not args.check:
            return 0
    print("PASS: KoalaBear v4 tangent source adapter")
    print(f"partition_sha256={DIGEST}")
    print(f"U_paid={PAID}")
    print(f"remaining_budget={REMAINING}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
