#!/usr/bin/env python3
"""Verify the M31 LIST v4 Grande Finale provenance migration.

Commit b13de8113 changed ``experimental/grande_finale.tex`` after a family
of M31 LIST packets had sealed the preceding whole-file SHA-256.  The change
adds status clarifications; it does not change the five-atom LIST ledger or
the theorem sources used by the sealed packets.

This verifier proves that claim without weakening general source checking:

* the current source has one exact declared hash;
* six exact inverse edits reconstruct the formerly pinned bytes;
* the reconstructed bytes have the formerly pinned hash;
* the LIST formula and its four labels occur exactly once in both versions;
* every sealed manifest that pins the prior hash has a valid payload seal;
* every one of its other source bindings is fresh;
* the only tolerated stale binding is the canonical Grande Finale path with
  one manifest-specific, allow-listed binding identity.

The script is exact, standard-library-only, and never writes the manifest.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Iterable, Sequence


SCHEMA_ID = "rs-mca-m31-list-v4-grande-finale-provenance-migration-v1"
MIGRATION_ID = "M31_LIST_V4_GRANDE_FINALE_PROVENANCE_MIGRATION_V1"
ARTIFACT_KIND = "EXACT_SOURCE_PROVENANCE_COMPATIBILITY_AND_MANIFEST_AUDIT"
STATUS = "PROVED_EXACT_ANCESTOR_COMPATIBILITY_ROW_OPEN"

GRANDE_FINALE_PATH = "experimental/grande_finale.tex"
PRIOR_SHA256 = "34618918de8fc1c1aac5642393f49019c60ff7041a9efeacbf0b8ea01eb3d8cd"
CURRENT_SHA256 = "336ba3c9a6d9483d0eab74677d6224aae23adf15d84891c6099f6d2f45cf226d"
PRIOR_BYTE_COUNT = 328_284
CURRENT_BYTE_COUNT = 330_361

ARCHITECTURE_ID = "GRANDE_FINALE_V4_M31_LIST_SOURCE_ADAPTER_V1"
PARTITION_SHA256 = "816f0702925f9734d230ffdfbf51a9d77aab2e1546918c722e1cc90227feafcc"
ATOM_ORDER = ("U_paid", "U_Q", "U_list_int", "U_ext", "U_new")
OWNER_ORDER = (
    "LOW_EXACT_WEIGHT_PACKING",
    "HIGH_BOUNDARY_EXACT_CODEWORD",
    "HIGH_INTERIOR_EXACT_CODEWORD",
)
UNIT = "DISTINCT_CODEWORDS_PER_RECEIVED_WORD"
QUANTIFIER = "UNIFORM_OVER_ALL_RECEIVED_WORDS"

LIST_FORMULA = (
    "\\begin{equation}\n"
    " U_{\\rm list}\n"
    " =U_{\\rm paid}+U_Q+U_{\\rm list-int}+U_{\\rm ext}+U_{\\rm new}.\n"
    " \\label{eq:list-final-ledger}\n"
    "\\end{equation}\n"
)
LIST_LABELS = (
    "\\label{sec:list-final-certificate}",
    "\\label{eq:list-final-ledger}",
    "\\label{prob:list-completion}",
    "\\label{thm:exact-completion-certificate}",
)
LIST_CLARIFICATION = (
    "This is the final v4 successor to the arbitrary-word list-interior clause of\n"
    "the v3 \\texttt{prob:saturated-bc}; it also includes the remaining prefix and\n"
    "extension terms required by the v4 list ledger.\n\n"
)

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / (
    "experimental/data/schemas/"
    "m31_list_v4_grande_finale_provenance_migration_v1.schema.json"
)
NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_list_v4_grande_finale_provenance_migration_v1.md"
)
README_PATH = ROOT / (
    "experimental/data/certificates/"
    "m31-list-v4-grande-finale-provenance-migration-v1/README.md"
)
DEFAULT_MANIFEST = ROOT / (
    "experimental/data/certificates/"
    "m31-list-v4-grande-finale-provenance-migration-v1/manifest.json"
)
VERIFIER_PATH = Path(__file__).resolve()
GRANDE_FINALE = ROOT / GRANDE_FINALE_PATH


class VerificationError(RuntimeError):
    """Raised when a fail-closed migration gate fails."""


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


def reject_float(_token: str) -> Any:
    raise VerificationError("floating-point JSON value")


def reject_constant(_token: str) -> Any:
    raise VerificationError("non-finite JSON value")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in out, f"duplicate JSON key: {key}")
        out[key] = value
    return out


def require_ascii_strings(value: Any, path: str = "json") -> None:
    if type(value) is str:
        require(value.isascii(), f"{path}: non-ASCII string")
    elif type(value) is list:
        for index, item in enumerate(value):
            require_ascii_strings(item, f"{path}[{index}]")
    elif type(value) is dict:
        for key, item in value.items():
            require(type(key) is str and key.isascii(), f"{path}: non-ASCII key")
            require_ascii_strings(item, f"{path}.{key}")


def strict_json_bytes(raw: bytes, *, canonical: bool) -> dict[str, Any]:
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError("non-ASCII JSON") from exc
    try:
        value = json.loads(
            text,
            object_pairs_hook=unique_object,
            parse_float=reject_float,
            parse_constant=reject_constant,
        )
    except (json.JSONDecodeError, ValueError) as exc:
        raise VerificationError("invalid JSON") from exc
    require(type(value) is dict, "JSON top level must be an object")
    require_ascii_strings(value)
    if canonical:
        require(raw == canonical_json(value), "noncanonical JSON bytes")
    return value


def strict_json_path(path: Path, *, canonical: bool = True) -> tuple[dict[str, Any], bytes]:
    require(path.is_file(), f"missing JSON source: {path}")
    raw = path.read_bytes()
    return strict_json_bytes(raw, canonical=canonical), raw


def canonical_json(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        )
        + "\n"
    ).encode("ascii")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_path(path: Path) -> str:
    require(path.is_file(), f"missing source: {path}")
    return sha256_bytes(path.read_bytes())


def payload_sha256(value: dict[str, Any]) -> str:
    body = copy.deepcopy(value)
    body.pop("payload_sha256", None)
    return sha256_bytes(canonical_json(body))


def seal(value: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(value)
    out["payload_sha256"] = payload_sha256(out)
    return out


def deep_exact(actual: Any, expected: Any, path: str = "payload") -> None:
    require(type(actual) is type(expected), f"{path}: type")
    if type(expected) is dict:
        require(set(actual) == set(expected), f"{path}: keys")
        for key in expected:
            deep_exact(actual[key], expected[key], f"{path}.{key}")
    elif type(expected) is list:
        require(len(actual) == len(expected), f"{path}: length")
        for index, (left, right) in enumerate(zip(actual, expected, strict=True)):
            deep_exact(left, right, f"{path}[{index}]")
    else:
        require(actual == expected, f"{path}: exact value")


def canonical_repo_path(text: Any) -> Path:
    require(type(text) is str and 0 < len(text) <= 4096, "source path text")
    pure = PurePosixPath(text)
    require(not pure.is_absolute(), f"absolute source path: {text}")
    require(all(part not in ("", ".", "..") for part in pure.parts), f"noncanonical source path: {text}")
    allowed_tree = pure.parts[0] in {"archived", "docs", "experimental", "site", "tex"}
    allowed_root_file = tuple(pure.parts) in {
        ("RS_MCA_Paving_v9.2.tex",),
        ("open-proximity.tex",),
    }
    require(allowed_tree or allowed_root_file, f"source root: {text}")
    candidate = (ROOT / Path(*pure.parts)).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise VerificationError(f"source escapes repository: {text}") from exc
    require(candidate.is_file(), f"bound source missing: {text}")
    return candidate


# Each pair is (operation id, exact current fragment, exact prior fragment).
# Five operations delete an insertion and one restores the single replaced
# sentence.  Exact multiplicity-one checking makes the inverse transform
# fail closed.
INVERSE_OPERATIONS: tuple[tuple[str, str, str], ...] = (
    (
        "delete_spread_abundance_status",
        (
            "\\emph{Intermediate status.}\n"
            "This is the line-level abundance consequence required from the final\n"
            "spread-component routing problem \\cref{prob:mca-spread-routing}; it is not an\n"
            "additional terminal input to the completion certificate.\n\n"
        ),
        "",
    ),
    (
        "delete_next_spread_status",
        (
            "\\emph{Intermediate status.}\n"
            "This is the local correction-component form of the final\n"
            "\\cref{prob:mca-spread-routing}.  It is retained to state the geometric\n"
            "alternatives exposed by \\cref{thm:residual}, but is not a separate terminal\n"
            "input.\n\n"
        ),
        "",
    ),
    (
        "restore_audited_status_sentence",
        (
            "No theorem in this paper proves either deployed adjacent MCA-safe row or\n"
            "either deployed adjacent list-safe row.  The terminal open inputs used by the\n"
            "completion certificates are exactly\n"
            "\\cref{prob:mca-spread-routing,prob:large-owner,prob:mca-exception-routing,prob:list-completion}.\n"
            "The earlier \\cref{prob:spread-abundance,prob:next} are intermediate\n"
            "formulations subsumed by \\cref{prob:mca-spread-routing}, not additional\n"
            "terminal cells.\n"
        ),
        (
            "No theorem in this paper proves either deployed adjacent MCA-safe row or either deployed adjacent list-safe row.  "
            "The open statements are exactly the problems recorded in "
            "\\cref{prob:next,prob:large-owner,prob:mca-exception-routing,prob:list-completion}.\n"
        ),
    ),
    (
        "delete_saturated_bc_status_remark",
        (
            "\n\\begin{remark}[Status of the v3 saturated-BC problem]\n"
            "\\label{rem:saturated-bc-status}\n"
            "The v3 problem labelled \\texttt{prob:saturated-bc} is superseded in v4, not\n"
            "silently discharged.  Its primitive one-parameter MCA clause is proved by\n"
            "\\cref{cor:bc-one-pencil}.  Its higher-dimensional MCA clause remains open and\n"
            "is represented jointly by\n"
            "\\cref{prob:mca-spread-routing,prob:large-owner,prob:mca-exception-routing};\n"
            "in particular, v4 still requires exhaustive same-owner routing from every\n"
            "surviving balanced-core component into that endgame.  Its separate\n"
            "arbitrary-word list-interior clause is contained in\n"
            "\\cref{prob:list-completion}.  Thus no archived problem is being banked as a\n"
            "live theorem, and no higher-dimensional balanced-core payment is claimed\n"
            "merely from the one-pencil moving-root bound.\n"
            "\\end{remark}\n"
        ),
        "",
    ),
    (
        "delete_mca_spread_routing_clarification",
        (
            "This is the final v4 successor to the higher-dimensional MCA clause of the\n"
            "v3 \\texttt{prob:saturated-bc}.  Together with\n"
            "\\cref{prob:large-owner,prob:mca-exception-routing}, it must provide the\n"
            "exhaustive same-owner routing that the old balanced-core cell left open.  Its\n"
            "row-sharp conclusion subsumes the intermediate\n"
            "\\cref{prob:spread-abundance,prob:next} for purposes of the final certificate.\n\n"
        ),
        "",
    ),
    (
        "delete_list_completion_clarification",
        LIST_CLARIFICATION,
        "",
    ),
)


def reconstruct_prior(current_raw: bytes) -> tuple[bytes, list[dict[str, Any]]]:
    try:
        text = current_raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise VerificationError("Grande Finale is not UTF-8") from exc
    operations: list[dict[str, Any]] = []
    for operation_id, current_fragment, prior_fragment in INVERSE_OPERATIONS:
        require(text.count(current_fragment) == 1, f"inverse operation multiplicity: {operation_id}")
        before = len(text.encode("utf-8"))
        text = text.replace(current_fragment, prior_fragment, 1)
        after = len(text.encode("utf-8"))
        operations.append(
            {
                "operation_id": operation_id,
                "kind": "EXACT_REPLACEMENT" if prior_fragment else "EXACT_INSERTION_DELETION",
                "current_fragment_sha256": sha256_bytes(current_fragment.encode("utf-8")),
                "prior_fragment_sha256": sha256_bytes(prior_fragment.encode("utf-8")),
                "byte_delta": before - after,
            }
        )
    prior_raw = text.encode("utf-8")
    require(len(current_raw) == CURRENT_BYTE_COUNT, "current Grande Finale byte count")
    require(len(prior_raw) == PRIOR_BYTE_COUNT, "reconstructed prior byte count")
    require(sha256_bytes(current_raw) == CURRENT_SHA256, "current Grande Finale hash")
    require(sha256_bytes(prior_raw) == PRIOR_SHA256, "reconstructed prior Grande Finale hash")
    require(sum(row["byte_delta"] for row in operations) == CURRENT_BYTE_COUNT - PRIOR_BYTE_COUNT, "inverse byte delta")
    return prior_raw, operations


def list_contract(current_raw: bytes, prior_raw: bytes) -> dict[str, Any]:
    current = current_raw.decode("utf-8")
    prior = prior_raw.decode("utf-8")
    require(current.count(LIST_FORMULA) == 1, "current LIST formula multiplicity")
    require(prior.count(LIST_FORMULA) == 1, "prior LIST formula multiplicity")
    for label in LIST_LABELS:
        require(current.count(label) == 1, f"current LIST label: {label}")
        require(prior.count(label) == 1, f"prior LIST label: {label}")
    require(current.count(LIST_CLARIFICATION) == 1, "current LIST clarification")
    require(LIST_CLARIFICATION not in prior, "prior excludes LIST clarification")
    return {
        "architecture_id": ARCHITECTURE_ID,
        "partition_sha256": PARTITION_SHA256,
        "atom_order": list(ATOM_ORDER),
        "owner_order": list(OWNER_ORDER),
        "formula": "U_list=U_paid+U_Q+U_list_int+U_ext+U_new",
        "formula_sha256": sha256_bytes(LIST_FORMULA.encode("utf-8")),
        "formula_occurrences_current": 1,
        "formula_occurrences_prior": 1,
        "labels": [label.removeprefix("\\label{").removesuffix("}") for label in LIST_LABELS],
        "labels_unchanged": True,
        "b13de_list_change": "STATUS_CLARIFICATION_ONLY",
        "unit": UNIT,
        "quantifier": QUANTIFIER,
    }


# The exact binding identity that may consume the compatibility theorem in
# each sealed manifest.  No other path, hash, manifest, or binding identity
# is eligible.
COMPATIBLE_BINDINGS: dict[str, tuple[str | None, str, str | None]] = {
    "experimental/data/certificates/m31-all-weight-anchor-exchange-pade-bijection-v1/manifest.json": (
        "M31_ANCHOR_EXCHANGE::active_v4_ledger",
        "active_v4_ledger",
        "Active LIST owner chronology and null-atom semantics.",
    ),
    "experimental/data/certificates/m31-boundary-common-v-cross-g-route-cut-v1/manifest.json": (
        "M31_CROSS_G_CUT::active_v4_ledger",
        "active_v4_ledger",
        "Active LIST owner chronology and null-atom semantics.",
    ),
    "experimental/data/certificates/m31-c2048-65column-fixed-anchor-route-cut-v1/manifest.json": (
        "M31_C2048_65ANCHOR::active_v4_ledger",
        "active_v4_ledger",
        "Active nonnegative LIST chronology and exact target budget.",
    ),
    "experimental/data/certificates/m31-c2048-fixed-template-interleaved-quotient-route-cut-v1/manifest.json": (
        "M31_C2048_FIXED_TEMPLATE::active_v4_ledger",
        "active_v4_ledger",
        "Active nonnegative LIST chronology and row-sharp Q target.",
    ),
    "experimental/data/certificates/m31-c2048-fixed-template-module-rank-route-cut-v1/manifest.json": (
        "M31_C2048_MODULE_RANK::active_ledger",
        "active_ledger",
        "Active nonnegative LIST chronology and row-sharp target.",
    ),
    "experimental/data/certificates/m31-c2048-guarded-support-flat-separator-v1/manifest.json": (
        "M31_C2048_GUARDED_VT::active_ledger",
        "active_ledger",
        "Active nonnegative LIST chronology and row-sharp target.",
    ),
    "experimental/data/certificates/m31-c2048-multiprefix-30carrier-activation-v1/manifest.json": (
        "M31_C2048_MULTIPREFIX::active_v4_ledger",
        "active_v4_ledger",
        "Active nonnegative five-atom LIST chronology.",
    ),
    "experimental/data/certificates/m31-c2048-partial-occupancy-30carrier-v1/manifest.json": (
        "M31_C2048_30CARRIER::active_v4_ledger",
        "active_v4_ledger",
        "Active five-atom LIST chronology and deployed row.",
    ),
    "experimental/data/certificates/m31-c2048-vt-multitemplate-global-rank-route-cut-v1/manifest.json": (
        "M31_C2048_VT_MULTITEMPLATE::active_ledger",
        "active_ledger",
        "Active nonnegative LIST chronology and unchanged atoms.",
    ),
    "experimental/data/certificates/m31-canonical-masked-pade-global-route-cut-v1/manifest.json": (
        "M31_CANONICAL_MASKED_PADE::active_v4_ledger",
        "active_v4_ledger",
        "Active five-atom LIST chronology and payment semantics.",
    ),
    "experimental/data/certificates/m31-chebyshev-fixed-remainder-c1-boundary-source-route-cut-v1/manifest.json": (
        "M31_CHEB_FIXED_REMAINDER_C1::active_v4_ledger",
        "active_v4_ledger",
        "Active nonnegative five-atom LIST chronology and Q target.",
    ),
    "experimental/data/certificates/m31-full-span-forced-collision-route-cut-v1/manifest.json": (
        "M31_FULL_SPAN_FORCED_COLLISION::active_v4_ledger",
        "active_v4_ledger",
        "Active LIST owner chronology and exact completion semantics.",
    ),
    "experimental/data/certificates/m31-list-v4-global-completion-compiler-v2/manifest.json": (
        None,
        "v4_five_atom_ledger",
        None,
    ),
    "experimental/data/certificates/m31-list-v4-source-adapter-v1/manifest.json": (
        "M31_LIST_V4_SOURCE::active_v4_ledger",
        "active_v4_ledger",
        "CURRENT_V4_FIVE_ATOM_LIST_CHRONOLOGY",
    ),
    "experimental/data/certificates/m31-rank6-generalized-weight-codim1-closure-v1/manifest.json": (
        "M31_RANK6_CLOSURE::codimension_one_theorem_source",
        "codimension_one_theorem_source",
        "Two-resource recursion, profile interpolation, and MDS-soft compiler.",
    ),
    "experimental/data/certificates/m31-rank7-effective-deficit-one-pivot-route-cut-v1/manifest.json": (
        "M31_RANK7_EFFECTIVE_DEFICIT_ONE_PIVOT::affine_span_compiler_source",
        "affine_span_compiler_source",
        "Recursive affine-span compiler.",
    ),
    "experimental/data/certificates/m31-rank7-shallow-master-denominator-cut-v1/manifest.json": (
        "M31_RANK7_MASTER_DENOMINATOR_CUT::grande_finale_compilers",
        "grande_finale_compilers",
        "Affine-span and codimension-one theorems.",
    ),
    "experimental/data/certificates/m31-rank7-split-divisor-tail-route-cut-v1/manifest.json": (
        "M31_RANK7_SPLIT_DIVISOR_TAIL_ROUTE_CUT::affine_span_compiler_source",
        "affine_span_compiler_source",
        "Recursive affine-span and harmonic resource theorems.",
    ),
    "experimental/data/certificates/m31-rank7-truncated-weight-flag-route-cut-v1/manifest.json": (
        "M31_RANK7_ROUTE_CUT::grande_finale_compilers",
        "grande_finale_compilers",
        "Affine-fiber, Johnson, saturation, and codimension-one sources.",
    ),
}


def binding_identity(binding: dict[str, Any]) -> tuple[str | None, str, str | None]:
    return (
        binding.get("binding_id"),
        binding.get("role"),
        binding.get("scope"),
    )


def validate_internal_payload_pin(binding: dict[str, Any], source: Path) -> bool:
    internal = binding.get("internal_payload_sha256")
    if internal is None:
        return False
    require(type(internal) is str and len(internal) == 64, "internal payload pin type")
    source_data, _ = strict_json_path(source, canonical=False)
    candidates = (
        source_data.get("payload_sha256"),
        source_data.get("certificate_sha256"),
    )
    require(internal in candidates, f"internal payload pin mismatch: {binding.get('path')}")
    return True


def audit_manifest(relative: str) -> dict[str, Any]:
    path = canonical_repo_path(relative)
    manifest, raw = strict_json_path(path, canonical=True)
    expected_payload = manifest.get("payload_sha256")
    require(type(expected_payload) is str and len(expected_payload) == 64, f"{relative}: payload seal type")
    require(payload_sha256(manifest) == expected_payload, f"{relative}: payload seal")
    bindings = manifest.get("source_bindings")
    require(type(bindings) is list and len(bindings) > 0, f"{relative}: source bindings")

    compatible: list[dict[str, Any]] = []
    internal_pins = 0
    identities: set[tuple[Any, Any, Any]] = set()
    for index, binding in enumerate(bindings):
        require(type(binding) is dict, f"{relative}: binding object {index}")
        require(type(binding.get("path")) is str, f"{relative}: binding path {index}")
        require(type(binding.get("sha256")) is str, f"{relative}: binding hash {index}")
        identity = binding_identity(binding)
        require(identity not in identities, f"{relative}: duplicate binding identity")
        identities.add(identity)
        source = canonical_repo_path(binding["path"])
        current_hash = sha256_path(source)
        if binding["sha256"] != current_hash:
            require(binding["path"] == GRANDE_FINALE_PATH, f"{relative}: stale noncanonical source")
            require(binding["sha256"] == PRIOR_SHA256, f"{relative}: unrecognized Grande Finale ancestor")
            require(current_hash == CURRENT_SHA256, f"{relative}: unexpected current Grande Finale")
            require(identity == COMPATIBLE_BINDINGS[relative], f"{relative}: compatibility binding identity")
            compatible.append(
                {
                    "binding_id": binding.get("binding_id"),
                    "role": binding.get("role"),
                    "scope": binding.get("scope"),
                    "path": binding["path"],
                    "pinned_sha256": binding["sha256"],
                    "current_sha256": current_hash,
                    "compatibility_class": "EXACT_ANCESTOR_RECONSTRUCTION_ONLY",
                }
            )
        if validate_internal_payload_pin(binding, source):
            internal_pins += 1

    require(len(compatible) == 1, f"{relative}: exactly one compatible binding")
    require(compatible[0]["path"] == GRANDE_FINALE_PATH, f"{relative}: canonical compatible path")
    return {
        "path": relative,
        "manifest_sha256": sha256_bytes(raw),
        "payload_sha256": expected_payload,
        "status": manifest.get("status"),
        "source_binding_count": len(bindings),
        "fresh_source_binding_count": len(bindings) - 1,
        "compatible_source_binding_count": 1,
        "internal_payload_pin_count": internal_pins,
        "compatible_binding": compatible[0],
        "validation": "PASS_EXCEPT_EXACT_CANONICAL_GRANDE_FINALE_ANCESTOR",
    }


def discover_compatible_manifests() -> list[str]:
    found: list[str] = []
    certificate_root = ROOT / "experimental/data/certificates"
    for path in sorted(certificate_root.glob("**/manifest.json")):
        # Discovery ranges over unrelated historical packets, some of which
        # predate the canonical-byte convention.  Canonical bytes are
        # required below for every manifest actually admitted to this audit.
        manifest, _ = strict_json_path(path, canonical=False)
        bindings = manifest.get("source_bindings")
        if type(bindings) is not list:
            continue
        if any(
            type(binding) is dict
            and binding.get("path") == GRANDE_FINALE_PATH
            and binding.get("sha256") == PRIOR_SHA256
            for binding in bindings
        ):
            found.append(path.relative_to(ROOT).as_posix())
    require(found == sorted(COMPATIBLE_BINDINGS), "exact affected manifest census")
    return found


def source_bindings() -> list[dict[str, Any]]:
    specs = (
        ("migration_schema", SCHEMA_PATH, "Closed runtime schema."),
        ("migration_verifier", VERIFIER_PATH, "Exact inverse-source and manifest audit verifier."),
        ("migration_note", NOTE_PATH, "Proof, scope, and nonclaims."),
        ("migration_readme", README_PATH, "Replay instructions."),
    )
    return [
        {
            "binding_id": binding_id,
            "path": path.relative_to(ROOT).as_posix(),
            "role": role,
            "sha256": sha256_path(path),
        }
        for binding_id, path, role in specs
    ]


def build_template() -> dict[str, Any]:
    current_raw = GRANDE_FINALE.read_bytes()
    prior_raw, operations = reconstruct_prior(current_raw)
    affected = discover_compatible_manifests()
    records = [audit_manifest(relative) for relative in affected]
    total_bindings = sum(record["source_binding_count"] for record in records)
    total_fresh = sum(record["fresh_source_binding_count"] for record in records)
    total_compatible = sum(record["compatible_source_binding_count"] for record in records)
    total_internal = sum(record["internal_payload_pin_count"] for record in records)
    require((len(records), total_bindings, total_fresh, total_compatible, total_internal) == (19, 284, 265, 19, 40), "affected source census")
    payload: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "migration_id": MIGRATION_ID,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "payload_sha256": "",
        "source_contract": {
            "path": GRANDE_FINALE_PATH,
            "prior_sha256": PRIOR_SHA256,
            "current_sha256": CURRENT_SHA256,
            "prior_byte_count": PRIOR_BYTE_COUNT,
            "current_byte_count": CURRENT_BYTE_COUNT,
            "byte_delta": CURRENT_BYTE_COUNT - PRIOR_BYTE_COUNT,
            "inverse_operation_count": len(operations),
            "exact_insertion_deletion_count": sum(row["kind"] == "EXACT_INSERTION_DELETION" for row in operations),
            "exact_replacement_count": sum(row["kind"] == "EXACT_REPLACEMENT" for row in operations),
            "inverse_operations": operations,
            "exact_prior_reconstruction": True,
            "compatibility_scope": "ONLY_THE_CANONICAL_GRANDE_FINALE_PATH_AND_ALLOWLISTED_BINDING_IDENTITIES",
        },
        "list_contract": list_contract(current_raw, prior_raw),
        "manifest_audit": {
            "affected_manifest_count": len(records),
            "source_binding_count": total_bindings,
            "fresh_source_binding_count": total_fresh,
            "compatible_source_binding_count": total_compatible,
            "internal_payload_pin_count": total_internal,
            "all_payload_seals_valid": True,
            "all_non_grande_finale_bindings_fresh": True,
            "records": records,
        },
        "scope_guards": {
            "ledger_movement": 0,
            "official_endpoint_movement": 0,
            "row_closed": False,
            "new_atom_value_claimed": False,
            "route_cut_promoted_to_payment": False,
            "compatibility_applies_to_other_paths": False,
            "compatibility_applies_to_other_prior_hashes": False,
            "original_manifests_resealed": False,
            "standalone_predecessor_verifiers_declared_fresh": False,
        },
        "nonclaims": [
            "This packet does not prove the M31 LIST row or any adjacent deployed row.",
            "It does not change the five-atom values, owner order, partition digest, or residual state.",
            "It does not promote a rank-seven or c=2048 route cut to a codeword payment.",
            "It does not make the original standalone packet verifiers accept the new whole-file hash.",
            "A successor compiler must explicitly consume this migration certificate.",
        ],
        "source_bindings": source_bindings(),
    }
    return seal(payload)


def validate_schema() -> None:
    schema, _ = strict_json_path(SCHEMA_PATH, canonical=False)
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "schema dialect")
    require(schema.get("$id") == SCHEMA_ID, "schema id")
    require(schema.get("type") == "object", "schema type")
    require(schema.get("additionalProperties") is False, "schema closed")
    required = {
        "schema",
        "migration_id",
        "artifact_kind",
        "status",
        "payload_sha256",
        "source_contract",
        "list_contract",
        "manifest_audit",
        "scope_guards",
        "nonclaims",
        "source_bindings",
    }
    require(set(schema.get("required", [])) == required, "schema required fields")
    require(set(schema.get("properties", {})) == required, "schema property closure")


def validate_payload(payload: dict[str, Any]) -> None:
    require(payload.get("schema") == SCHEMA_ID, "schema")
    require(payload.get("migration_id") == MIGRATION_ID, "migration id")
    require(payload.get("artifact_kind") == ARTIFACT_KIND, "artifact kind")
    require(payload.get("status") == STATUS, "status")
    require(payload.get("payload_sha256") == payload_sha256(payload), "payload seal")
    deep_exact(payload, build_template())


def set_path(payload: dict[str, Any], path: Sequence[Any], value: Any) -> None:
    target: Any = payload
    for component in path[:-1]:
        target = target[component]
    target[path[-1]] = value


def mutation(path: Sequence[Any], value: Any) -> Callable[[dict[str, Any]], dict[str, Any]]:
    def apply(payload: dict[str, Any]) -> dict[str, Any]:
        out = copy.deepcopy(payload)
        set_path(out, path, value)
        return seal(out)

    return apply


def tamper_selftest(expected: dict[str, Any]) -> int:
    mutations: list[tuple[str, Callable[[dict[str, Any]], dict[str, Any]]]] = [
        ("schema", mutation(("schema",), "rs-mca-m31-list-v4-provenance-migration-v0")),
        ("status-safe", mutation(("status",), "SAFE")),
        ("current-hash", mutation(("source_contract", "current_sha256"), PRIOR_SHA256)),
        ("prior-hash", mutation(("source_contract", "prior_sha256"), CURRENT_SHA256)),
        ("inverse-count", mutation(("source_contract", "inverse_operation_count"), 5)),
        ("inverse-byte-delta", mutation(("source_contract", "inverse_operations", 0, "byte_delta"), 0)),
        ("reconstruction-false", mutation(("source_contract", "exact_prior_reconstruction"), False)),
        ("four-atoms", mutation(("list_contract", "atom_order"), list(ATOM_ORDER[:-1]))),
        ("atom-order", mutation(("list_contract", "atom_order"), ["U_paid", "U_Q", "U_ext", "U_list_int", "U_new"])),
        ("formula", mutation(("list_contract", "formula"), "U_list=U_paid+U_Q+U_list_int+U_new")),
        ("formula-count", mutation(("list_contract", "formula_occurrences_current"), 2)),
        ("label", mutation(("list_contract", "labels", 1), "eq:wrong")),
        ("partition", mutation(("list_contract", "partition_sha256"), "0" * 64)),
        ("slope-unit", mutation(("list_contract", "unit"), "DISTINCT_BAD_SLOPES_PER_RECEIVED_LINE")),
        ("received-line", mutation(("list_contract", "quantifier"), "UNIFORM_OVER_ALL_RECEIVED_LINES")),
        ("manifest-count", mutation(("manifest_audit", "affected_manifest_count"), 18)),
        ("binding-count", mutation(("manifest_audit", "source_binding_count"), 283)),
        ("fresh-count", mutation(("manifest_audit", "fresh_source_binding_count"), 264)),
        ("compat-count", mutation(("manifest_audit", "compatible_source_binding_count"), 18)),
        ("internal-pin-count", mutation(("manifest_audit", "internal_payload_pin_count"), 39)),
        ("manifest-path", mutation(("manifest_audit", "records", 0, "path"), "../manifest.json")),
        ("manifest-payload", mutation(("manifest_audit", "records", 0, "payload_sha256"), "0" * 64)),
        ("manifest-source-count", mutation(("manifest_audit", "records", 0, "source_binding_count"), 0)),
        ("compat-path", mutation(("manifest_audit", "records", 0, "compatible_binding", "path"), "experimental/agents.md")),
        ("compat-role", mutation(("manifest_audit", "records", 0, "compatible_binding", "role"), "arbitrary")),
        ("compat-prior", mutation(("manifest_audit", "records", 0, "compatible_binding", "pinned_sha256"), "0" * 64)),
        ("ledger-movement", mutation(("scope_guards", "ledger_movement"), 1)),
        ("row-closed", mutation(("scope_guards", "row_closed"), True)),
        ("atom-overclaim", mutation(("scope_guards", "new_atom_value_claimed"), True)),
        ("route-cut-payment", mutation(("scope_guards", "route_cut_promoted_to_payment"), True)),
        ("other-paths", mutation(("scope_guards", "compatibility_applies_to_other_paths"), True)),
        ("other-hashes", mutation(("scope_guards", "compatibility_applies_to_other_prior_hashes"), True)),
        ("predecessors-fresh", mutation(("scope_guards", "standalone_predecessor_verifiers_declared_fresh"), True)),
        ("source-hash", mutation(("source_bindings", 0, "sha256"), "0" * 64)),
        ("source-path", mutation(("source_bindings", 0, "path"), "../schema.json")),
    ]

    rejected = 0
    for label, mutator in mutations:
        candidate = mutator(expected)
        try:
            validate_payload(candidate)
        except (VerificationError, KeyError, IndexError, TypeError, ValueError):
            rejected += 1
        else:
            raise VerificationError(f"semantic mutation accepted: {label}")

    hostile_json = (
        b'{"a":1,"a":2}\n',
        b'{"a":1.0}\n',
        b'{"a":NaN}\n',
        b'{"a":"\\u00e9"}\n',
        b'{ "a":1 }\n',
        b'[]\n',
    )
    for index, raw in enumerate(hostile_json):
        try:
            strict_json_bytes(raw, canonical=True)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"hostile JSON accepted: {index}")

    first_manifest = next(iter(COMPATIBLE_BINDINGS))
    fake_bindings = (
        {
            "binding_id": COMPATIBLE_BINDINGS[first_manifest][0],
            "role": COMPATIBLE_BINDINGS[first_manifest][1],
            "scope": COMPATIBLE_BINDINGS[first_manifest][2],
            "path": "experimental/agents-log.md",
            "sha256": PRIOR_SHA256,
        },
        {
            "binding_id": "arbitrary",
            "role": "active_v4_ledger",
            "scope": COMPATIBLE_BINDINGS[first_manifest][2],
            "path": GRANDE_FINALE_PATH,
            "sha256": PRIOR_SHA256,
        },
        {
            "binding_id": COMPATIBLE_BINDINGS[first_manifest][0],
            "role": COMPATIBLE_BINDINGS[first_manifest][1],
            "scope": COMPATIBLE_BINDINGS[first_manifest][2],
            "path": GRANDE_FINALE_PATH,
            "sha256": "0" * 64,
        },
    )
    for binding in fake_bindings:
        identity = binding_identity(binding)
        accepted = (
            binding["path"] == GRANDE_FINALE_PATH
            and binding["sha256"] == PRIOR_SHA256
            and identity == COMPATIBLE_BINDINGS[first_manifest]
        )
        require(not accepted, "hostile compatibility binding accepted")
        rejected += 1

    expected_rejections = len(mutations) + len(hostile_json) + len(fake_bindings)
    require(rejected == expected_rejections, "all mutations rejected")
    return rejected


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true")
    group.add_argument("--print-template", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        validate_schema()
        expected = build_template()
        if args.print_template:
            sys.stdout.buffer.write(canonical_json(expected))
            return 0
        if args.tamper_selftest:
            count = tamper_selftest(expected)
            print(f"[PASS] provenance migration mutations {count}")
            return 0
        candidate, _ = strict_json_path(args.manifest, canonical=True)
        validate_payload(candidate)
        print(
            "[PASS] M31 LIST v4 Grande Finale provenance migration "
            f"manifests={candidate['manifest_audit']['affected_manifest_count']} "
            f"bindings={candidate['manifest_audit']['source_binding_count']} "
            f"payload={candidate['payload_sha256']}"
        )
        return 0
    except (VerificationError, KeyError, IndexError, OSError, TypeError, ValueError) as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
