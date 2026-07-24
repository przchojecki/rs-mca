#!/usr/bin/env python3
"""Verify the M31 all-weight source-calibrated ten-packet route cut."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Callable


SCHEMA_ID = "rs-mca-m31-all-weight-source-calibrated-ten-packet-gate-v1"
THEOREM_ID = "M31_ALL_WEIGHT_SOURCE_CALIBRATED_TEN_PACKET_GATE_V1"
ARCHITECTURE_ID = (
    "DIRECT_BOUNDARY_CENSUS_GATE_OVER_"
    "GRANDE_FINALE_V4_M31_LIST_SOURCE_ADAPTER_V1"
)
STATUS = "PROVED_EXACT_COMPILER_GATE_AND_ROUTE_CUT_TWO_INPUTS_OPEN_ROW_OPEN"
PARTITION_DIGEST = (
    "816f0702925f9734d230ffdfbf51a9d77aab2e1546918c722e1cc90227feafcc"
)

P = 2**31 - 1
N = 2**21
K = 2**20
AGREEMENT = 1_116_023
RADIUS = N - AGREEMENT
SHIFT = AGREEMENT - K
BUDGET = 16_777_215
FORBIDDEN = BUDGET + 1
DEEP_CAP = 1_001_282
SHALLOW_FORCED = BUDGET - DEEP_CAP
SHALLOW_CLOSURE_RHS = SHALLOW_FORCED - 1
MIN_EXCHANGE = SHIFT + 1
MAX_EXCHANGE = RADIUS
EXCHANGE_DEGREES = MAX_EXCHANGE - MIN_EXCHANGE + 1

SOURCE_LIST_FLOOR = 6_796_405
SOURCE_COMPANION_FLOOR = SOURCE_LIST_FLOOR - 1
FOLD_DEGREE = 2_048
QUOTIENT_UNIVERSE = 1_023
QUOTIENT_SUPPORT_SIZE = 544
SOURCE_MAX_QUOTIENT_EXCHANGE = min(
    QUOTIENT_SUPPORT_SIZE,
    QUOTIENT_UNIVERSE - QUOTIENT_SUPPORT_SIZE,
)
SOURCE_MIN_QUOTIENT_EXCHANGE = (
    MIN_EXCHANGE + FOLD_DEGREE - 1
) // FOLD_DEGREE
SOURCE_POSITIVE_DEGREES = (
    SOURCE_MAX_QUOTIENT_EXCHANGE - SOURCE_MIN_QUOTIENT_EXCHANGE + 1
)

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "m31_all_weight_source_calibrated_ten_packet_gate_v1.schema.json"
)
VERIFIER_PATH = (
    ROOT
    / "experimental/scripts/"
    "verify_m31_all_weight_source_calibrated_ten_packet_gate_v1.py"
)
INDEPENDENT_PATH = (
    ROOT
    / "experimental/scripts/"
    "verify_m31_all_weight_source_calibrated_ten_packet_gate_v1_independent.py"
)
NOTE_PATH = (
    ROOT
    / "experimental/notes/thresholds/"
    "m31_all_weight_source_calibrated_ten_packet_gate_v1.md"
)
README_PATH = (
    ROOT
    / "experimental/data/certificates/"
    "m31-all-weight-source-calibrated-ten-packet-gate-v1/README.md"
)
DEFAULT_MANIFEST = README_PATH.with_name("manifest.json")

BOUNDARY_PARENT = (
    ROOT
    / "experimental/data/certificates/"
    "m31-boundary-common-v-cross-g-route-cut-v1/manifest.json"
)
ANCHOR_PARENT = (
    ROOT
    / "experimental/data/certificates/"
    "m31-all-weight-anchor-exchange-pade-bijection-v1/manifest.json"
)
FIXED_REMAINDER_PARENT = (
    ROOT
    / "experimental/data/certificates/"
    "m31-chebyshev-fixed-remainder-c1-boundary-source-route-cut-v1/manifest.json"
)
INTERLACED_PARENT = (
    ROOT
    / "experimental/data/certificates/"
    "m31-rank7-weighted-head-interlaced-source-route-cut-v1/manifest.json"
)
PROVENANCE_MIGRATION = (
    ROOT
    / "experimental/data/certificates/"
    "m31-list-v4-grande-finale-provenance-migration-v1/manifest.json"
)

PARENT_PINS = {
    "grande_finale_provenance_migration": (
        PROVENANCE_MIGRATION,
        "6ecd0eda3035aef7544646f0e3f1ddbf8b9aad4c0a1a9e0f8518ac22e3671479",
    ),
    "boundary_common_v_parent": (
        BOUNDARY_PARENT,
        "fcc630ba68c803bb67378f836a84e6bdbcefe7fd9d5b468ef48fe919bd8307e3",
    ),
    "anchor_exchange_parent": (
        ANCHOR_PARENT,
        "bf38cbae247269196395c61aeae3e9fa8b72f92ffc0b0af4650e96e98d66eb6e",
    ),
    "fixed_remainder_source_parent": (
        FIXED_REMAINDER_PARENT,
        "056dbde2614e03278c4f52db114233d2438fb097f9c495133779c92001135af7",
    ),
    "interlaced_source_parent": (
        INTERLACED_PARENT,
        "376d3ba51fc2dd5a91eaef474859364c73984b4d83474387506632166438e8b3",
    ),
}


class VerificationError(RuntimeError):
    pass


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def ceil_div(a: int, b: int) -> int:
    require(a >= 0 and b > 0, "ceil-div domain")
    return -(-a // b)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")
        + b"\n"
    )


def payload_sha256(value: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(value)
    unsigned.pop("payload_sha256", None)
    return hashlib.sha256(canonical_bytes(unsigned)).hexdigest()


def seal(value: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(value)
    out.pop("payload_sha256", None)
    out["payload_sha256"] = payload_sha256(out)
    return out


def strict_json(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    require(len(raw) <= 64 * 1024 * 1024, f"file size: {path}")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError(f"non-ASCII JSON: {path}") from exc

    def reject_float(_value: str) -> Any:
        raise VerificationError("JSON float forbidden")

    def reject_constant(_value: str) -> Any:
        raise VerificationError("JSON constant forbidden")

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in out, f"duplicate JSON key: {key}")
            out[key] = value
        return out

    value = json.loads(
        text,
        object_pairs_hook=unique,
        parse_float=reject_float,
        parse_constant=reject_constant,
    )
    require(isinstance(value, dict), f"JSON object: {path}")
    return value


def safe_repo_path(relative: str) -> Path:
    pure = PurePosixPath(relative)
    require(not pure.is_absolute(), "source path relative")
    require(".." not in pure.parts, "source path traversal")
    require("\\" not in relative, "source path separator")
    path = ROOT.joinpath(*pure.parts)
    require(path.is_file(), f"source exists: {relative}")
    return path


def source_binding(
    binding_id: str,
    path: Path,
    role: str,
    internal_payload_sha256: str | None = None,
) -> dict[str, Any]:
    relative = path.relative_to(ROOT).as_posix()
    return {
        "binding_id": binding_id,
        "path": relative,
        "role": role,
        "sha256": sha256_path(path),
        "internal_payload_sha256": internal_payload_sha256,
    }


def read_parent(role: str) -> dict[str, Any]:
    path, expected = PARENT_PINS[role]
    data = strict_json(path)
    require(data.get("payload_sha256") == expected, f"{role} payload pin")
    require(payload_sha256(data) == expected, f"{role} payload seal")
    return data


def source_bindings() -> list[dict[str, Any]]:
    bindings = [
        source_binding("packet_schema", SCHEMA_PATH, "Strict closed packet schema."),
        source_binding("packet_verifier", VERIFIER_PATH, "Primary fail-closed verifier."),
        source_binding(
            "independent_replay",
            INDEPENDENT_PATH,
            "Independent derivation of every load-bearing integer.",
        ),
        source_binding("theorem_note", NOTE_PATH, "Proof, scope, and audit."),
        source_binding("packet_readme", README_PATH, "Replay and nonclaim contract."),
    ]
    for role, (path, expected) in PARENT_PINS.items():
        bindings.append(
            source_binding(
                role,
                path,
                "Sealed exact predecessor packet.",
                expected,
            )
        )
    return bindings


def structured_cap(primitive_cap: int) -> int:
    return SHALLOW_CLOSURE_RHS - primitive_cap * EXCHANGE_DEGREES


def build_template() -> dict[str, Any]:
    migration = read_parent("grande_finale_provenance_migration")
    boundary = read_parent("boundary_common_v_parent")
    anchor = read_parent("anchor_exchange_parent")
    fixed = read_parent("fixed_remainder_source_parent")
    interlaced = read_parent("interlaced_source_parent")

    require(
        migration["manifest_audit"]["affected_manifest_count"] == 19,
        "provenance affected manifests",
    )
    require(
        migration["manifest_audit"]["all_payload_seals_valid"] is True,
        "provenance payload seals",
    )
    require(
        migration["manifest_audit"]["all_non_grande_finale_bindings_fresh"]
        is True,
        "provenance fresh sources",
    )
    require(
        boundary["whole_list_deep_cut"]["threshold_cap"] == DEEP_CAP,
        "parent deep cap",
    )
    require(
        boundary["whole_list_deep_cut"][
            "forbidden_list_shallow_nonanchors_lower"
        ]
        == SHALLOW_FORCED,
        "parent shallow count",
    )
    require(
        boundary["deployed_parameters"]["root_deficit_R_minus_w"]
        == EXCHANGE_DEGREES,
        "parent exchange degrees",
    )
    require(
        fixed["deployed_parameters"]["structured_list_floor"]
        == SOURCE_LIST_FLOOR,
        "source list floor",
    )
    require(
        fixed["deployed_parameters"]["fold_degree"] == FOLD_DEGREE,
        "source fold degree",
    )
    require(
        fixed["deployed_parameters"]["quotient_size"] == 1_024,
        "source quotient size",
    )
    require(
        fixed["deployed_parameters"]["quotient_support_size"]
        == QUOTIENT_SUPPORT_SIZE,
        "source quotient support",
    )
    require(
        anchor["row_contract"]["complete_list_budget"] == BUDGET,
        "anchor budget",
    )
    require(
        interlaced["source_consequence"]["companions"] == 7,
        "interlaced companions",
    )

    same_degree_floor = ceil_div(
        SOURCE_COMPANION_FLOOR, SOURCE_POSITIVE_DEGREES
    )
    cap9 = structured_cap(9)
    cap10 = structured_cap(10)
    cap10_excess = SOURCE_COMPANION_FLOOR - cap10
    source_slack = cap9 - SOURCE_COMPANION_FLOOR
    require(cap10_excess > 0, "cap ten obstructed")
    require(source_slack >= 0, "cap nine source compatible")

    table = [
        {
            "primitive_cap": c,
            "largest_structured_cap": structured_cap(c),
        }
        for c in (7, 8, 9, 10, 17)
    ]

    result = {
        "schema": SCHEMA_ID,
        "theorem_id": THEOREM_ID,
        "architecture_id": ARCHITECTURE_ID,
        "status": STATUS,
        "row_contract": {
            "row": "Mersenne-31 list at 2^-100",
            "object": "LIST",
            "unit": "DISTINCT_NONANCHOR_CODEWORDS_PER_RECEIVED_WORD",
            "quantifier": "UNIFORM_OVER_EVERY_BOUNDARY_FORCED_RECEIVED_WORD",
            "p": P,
            "n": N,
            "K": K,
            "agreement": AGREEMENT,
            "radius": RADIUS,
            "w": SHIFT,
            "B_star": BUDGET,
            "forbidden_size": FORBIDDEN,
            "partition_digest": PARTITION_DIGEST,
        },
        "parent_deep_tail": {
            "deep_excess_first": 366_887,
            "deep_nonanchor_cap": DEEP_CAP,
            "shallow_excess_interval": [0, 366_886],
            "forced_shallow_nonanchors": SHALLOW_FORCED,
            "direct_diagnostic_not_v4_payment": True,
        },
        "additive_gate": {
            "minimum_exchange_degree": MIN_EXCHANGE,
            "maximum_exchange_degree": MAX_EXCHANGE,
            "legal_exchange_degree_count": EXCHANGE_DEGREES,
            "forced_shallow_nonanchors": SHALLOW_FORCED,
            "closure_rhs": SHALLOW_CLOSURE_RHS,
            "closure_inequality": "C+913682*c<=15775932",
            "cap_table": table,
            "structured_cap_at_primitive_cap_9": cap9,
            "structured_cap_at_primitive_cap_10": cap10,
            "source_compatible_primitive_cap_max": 9,
            "primitive_cap_is_cross_weight":
                "sum_(s=0)^366886 #P_(m,s)<=c for each fixed m",
            "two_owner_closure_proved": False,
        },
        "fixed_remainder_source": {
            "list_floor": SOURCE_LIST_FLOOR,
            "nonanchor_companion_floor": SOURCE_COMPANION_FLOOR,
            "floor_is_existential_not_uniform": True,
            "fold_degree": FOLD_DEGREE,
            "quotient_label_universe": QUOTIENT_UNIVERSE,
            "quotient_support_size": QUOTIENT_SUPPORT_SIZE,
            "minimum_quotient_exchange": SOURCE_MIN_QUOTIENT_EXCHANGE,
            "maximum_quotient_exchange": SOURCE_MAX_QUOTIENT_EXCHANGE,
            "positive_exchange_degree_count_max": SOURCE_POSITIVE_DEGREES,
            "exchange_degrees": "m=2048*e, 33<=e<=479",
            "same_degree_companion_floor": same_degree_floor,
            "same_degree_floor_is_actual_received_word_source": True,
            "unconditional_primitive_cap_9_refuted": True,
            "unconditional_primitive_cap_17_refuted": True,
            "owner_absorbing_source_cap_min": SOURCE_COMPANION_FLOOR,
            "source_floor_slack_at_cap_9": source_slack,
            "cap_10_obstruction_excess": cap10_excess,
        },
        "interlaced_regression_fixture": {
            "anchor_codewords": 1,
            "companions": 7,
            "exchange_degree": MIN_EXCHANGE,
            "excess": 0,
            "mixed_G": True,
            "no_complete_T32_or_T2048_support_fiber": True,
            "final_first_match_primitivity_proved": False,
            "role": "EXACT_SOURCE_REGRESSION_FIXTURE_NOT_PRIMITIVE_ATOM_PAYMENT",
        },
        "ledger_state": {
            "ledger_movement": 0,
            "official_endpoint_movement": 0,
            "row_closed": False,
            "U_paid": 3_730,
            "U_Q": None,
            "U_list_int": None,
            "U_ext": None,
            "U_new": None,
            "global_terminal":
                "UNPAID_SOURCE_BOUND_STRUCTURED_CAP_OR_PRIMITIVE_TEN_PACKET",
        },
        "nonclaims": {
            "structured_owner_exhaustive": False,
            "structured_cap_7552794_proved": False,
            "primitive_cross_weight_cap_9_proved": False,
            "signed_Xi46_paid": False,
            "row_upper_bound_proved": False,
            "fixed_remainder_floor_is_upper_bound": False,
            "interlaced_fixture_is_forbidden_list": False,
            "stable_paper_modified": False,
            "lean_used": False,
        },
        "source_bindings": source_bindings(),
    }
    return seal(result)


def validate_schema_shape(data: dict[str, Any]) -> None:
    schema = strict_json(SCHEMA_PATH)
    require(schema["$id"] == SCHEMA_ID, "schema id")
    required = schema["required"]
    require(set(data) == set(required), "closed top-level keys")
    require(schema["additionalProperties"] is False, "closed schema")
    for key, spec in schema["properties"].items():
        if "const" in spec:
            require(data[key] == spec["const"], f"schema const {key}")


def deep_exact(actual: Any, expected: Any, path: str = "root") -> None:
    require(type(actual) is type(expected), f"{path} type")
    if isinstance(expected, dict):
        require(set(actual) == set(expected), f"{path} keys")
        for key in expected:
            deep_exact(actual[key], expected[key], f"{path}.{key}")
    elif isinstance(expected, list):
        require(len(actual) == len(expected), f"{path} length")
        for index, value in enumerate(expected):
            deep_exact(actual[index], value, f"{path}[{index}]")
    else:
        require(actual == expected, f"{path} value")


def validate_sources(data: dict[str, Any]) -> None:
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    for binding in data["source_bindings"]:
        binding_id = binding["binding_id"]
        relative = binding["path"]
        require(binding_id not in seen_ids, "unique binding id")
        require(relative not in seen_paths, "unique source path")
        seen_ids.add(binding_id)
        seen_paths.add(relative)
        path = safe_repo_path(relative)
        require(binding["sha256"] == sha256_path(path), f"fresh source {binding_id}")
        internal = binding["internal_payload_sha256"]
        if internal is not None:
            source = strict_json(path)
            require(source.get("payload_sha256") == internal, f"internal pin {binding_id}")
            require(payload_sha256(source) == internal, f"internal seal {binding_id}")


def validate_semantics(data: dict[str, Any]) -> None:
    row = data["row_contract"]
    deep = data["parent_deep_tail"]
    gate = data["additive_gate"]
    source = data["fixed_remainder_source"]
    fixture = data["interlaced_regression_fixture"]
    ledger = data["ledger_state"]
    nonclaims = data["nonclaims"]

    require(row["object"] == "LIST", "LIST unit")
    require(row["unit"] == "DISTINCT_NONANCHOR_CODEWORDS_PER_RECEIVED_WORD", "codeword unit")
    require(row["B_star"] == BUDGET, "budget")
    require(deep["deep_nonanchor_cap"] == DEEP_CAP, "deep cap")
    require(deep["forced_shallow_nonanchors"] == SHALLOW_FORCED, "shallow count")
    require(gate["legal_exchange_degree_count"] == EXCHANGE_DEGREES, "degree count")
    require(gate["closure_rhs"] == SHALLOW_CLOSURE_RHS, "closure rhs")
    require(gate["two_owner_closure_proved"] is False, "open two-owner theorem")

    table = {
        row_["primitive_cap"]: row_["largest_structured_cap"]
        for row_ in gate["cap_table"]
    }
    require(table == {c: structured_cap(c) for c in (7, 8, 9, 10, 17)}, "cap table")
    require(
        gate["structured_cap_at_primitive_cap_9"] == structured_cap(9),
        "cap nine",
    )
    require(
        gate["structured_cap_at_primitive_cap_10"] == structured_cap(10),
        "cap ten",
    )
    require(
        SOURCE_COMPANION_FLOOR + 10 * EXCHANGE_DEGREES
        == SHALLOW_CLOSURE_RHS + source["cap_10_obstruction_excess"],
        "cap ten obstruction identity",
    )
    require(
        structured_cap(9) - SOURCE_COMPANION_FLOOR
        == source["source_floor_slack_at_cap_9"],
        "cap nine slack identity",
    )
    require(
        source["positive_exchange_degree_count_max"]
        == SOURCE_POSITIVE_DEGREES
        == 447,
        "source degree count",
    )
    require(
        source["minimum_quotient_exchange"]
        == SOURCE_MIN_QUOTIENT_EXCHANGE
        == 33,
        "source minimum exchange",
    )
    require(
        source["maximum_quotient_exchange"]
        == SOURCE_MAX_QUOTIENT_EXCHANGE
        == 479,
        "source maximum exchange",
    )
    require(
        source["same_degree_companion_floor"]
        == ceil_div(SOURCE_COMPANION_FLOOR, SOURCE_POSITIVE_DEGREES)
        == 15_205,
        "same-degree source floor",
    )
    require(source["floor_is_existential_not_uniform"] is True, "source quantifier")
    require(fixture["companions"] == 7, "fixture companions")
    require(fixture["final_first_match_primitivity_proved"] is False, "fixture nonclaim")
    require(ledger["ledger_movement"] == 0, "zero ledger movement")
    require(ledger["row_closed"] is False, "row open")
    require(
        [ledger[name] for name in ("U_Q", "U_list_int", "U_ext", "U_new")]
        == [None, None, None, None],
        "null atoms",
    )
    require(all(value is False for value in nonclaims.values()), "all nonclaims false")


def validate(data: dict[str, Any]) -> None:
    validate_schema_shape(data)
    require(data["payload_sha256"] == payload_sha256(data), "payload seal")
    validate_sources(data)
    validate_semantics(data)
    expected = build_template()
    deep_exact(data, expected)


def mutate(
    data: dict[str, Any],
    path: tuple[str | int, ...],
    value: Any,
) -> dict[str, Any]:
    out = copy.deepcopy(data)
    cursor: Any = out
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value
    return seal(out)


def expect_rejected(label: str, candidate: dict[str, Any]) -> None:
    try:
        validate(candidate)
    except VerificationError:
        return
    raise VerificationError(f"mutation accepted: {label}")


def tamper_selftest(template: dict[str, Any]) -> None:
    mutations: list[tuple[str, dict[str, Any]]] = [
        ("deep cap", mutate(template, ("parent_deep_tail", "deep_nonanchor_cap"), DEEP_CAP - 1)),
        ("shallow count", mutate(template, ("additive_gate", "forced_shallow_nonanchors"), SHALLOW_FORCED - 1)),
        ("degree count", mutate(template, ("additive_gate", "legal_exchange_degree_count"), EXCHANGE_DEGREES - 1)),
        ("cap nine", mutate(template, ("additive_gate", "structured_cap_at_primitive_cap_9"), structured_cap(9) + 1)),
        ("cap ten", mutate(template, ("additive_gate", "structured_cap_at_primitive_cap_10"), structured_cap(10) - 1)),
        ("source floor", mutate(template, ("fixed_remainder_source", "nonanchor_companion_floor"), SOURCE_COMPANION_FLOOR - 1)),
        ("source minimum exchange", mutate(template, ("fixed_remainder_source", "minimum_quotient_exchange"), 32)),
        ("source degrees", mutate(template, ("fixed_remainder_source", "positive_exchange_degree_count_max"), 448)),
        ("same-degree floor", mutate(template, ("fixed_remainder_source", "same_degree_companion_floor"), 15_204)),
        ("ten obstruction", mutate(template, ("fixed_remainder_source", "cap_10_obstruction_excess"), 157_291)),
        ("nine slack", mutate(template, ("fixed_remainder_source", "source_floor_slack_at_cap_9"), 756_391)),
        ("fixture primitivity", mutate(template, ("interlaced_regression_fixture", "final_first_match_primitivity_proved"), True)),
        ("ledger movement", mutate(template, ("ledger_state", "ledger_movement"), 1)),
        ("row closure", mutate(template, ("ledger_state", "row_closed"), True)),
        ("atom payment", mutate(template, ("ledger_state", "U_new"), 0)),
        ("false cap theorem", mutate(template, ("nonclaims", "primitive_cross_weight_cap_9_proved"), True)),
        ("payload hash", {**template, "payload_sha256": "0" * 64}),
        ("source hash", mutate(template, ("source_bindings", 0, "sha256"), "0" * 64)),
        ("source path", mutate(template, ("source_bindings", 0, "path"), "../schema.json")),
        ("parent pin", mutate(template, ("source_bindings", 5, "internal_payload_sha256"), "0" * 64)),
    ]
    for label, candidate in mutations:
        expect_rejected(label, candidate)
    print(f"M31 ten-packet hostile controls: PASS ({len(mutations)} mutations)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--print-template", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        template = build_template()
        if args.print_template:
            sys.stdout.buffer.write(canonical_bytes(template))
        if args.check:
            validate(strict_json(args.manifest))
            print(f"M31 all-weight source-calibrated ten-packet gate: PASS ({CHECKS} checks)")
        if args.tamper_selftest:
            tamper_selftest(template)
        if not (args.print_template or args.check or args.tamper_selftest):
            validate(strict_json(args.manifest))
            print(f"M31 all-weight source-calibrated ten-packet gate: PASS ({CHECKS} checks)")
    except (OSError, KeyError, TypeError, ValueError, VerificationError) as exc:
        print(f"M31 all-weight source-calibrated ten-packet gate: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
