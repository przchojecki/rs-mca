#!/usr/bin/env python3
"""Verify the M31 rank-seven combined-domain affine/Johnson endpoint."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections import deque
from functools import lru_cache
from math import comb
from pathlib import Path, PurePosixPath
from typing import Any


SCHEMA_ID = (
    "rs-mca-m31-rank7-combined-domain-affine-johnson-endpoint-v1"
)
THEOREM_ID = "M31_RANK7_COMBINED_DOMAIN_AFFINE_JOHNSON_ENDPOINT_V1"
ARCHITECTURE_ID = THEOREM_ID
STATUS = "PROVED_LOCAL_Q29554_HEAD_Q29555_ROUTE_CUT_ROW_OPEN"
PARTITION_DIGEST = (
    "816f0702925f9734d230ffdfbf51a9d77aab2e1546918c722e1cc90227feafcc"
)

P = 2**31 - 1
N = 2**21
K = 2**20
AGREEMENT = 1_116_023
R = N - AGREEMENT
W = AGREEMENT - K
BUDGET = 16_777_215
DEEP_CAP = 1_001_282
SHALLOW_FORCED = BUDGET - DEEP_CAP
SHALLOW_TARGET = SHALLOW_FORCED - 1
G = 354_972
D = G - W
MAX_RANK = 6
LAST_PAID_Q = 29_554
FIRST_OPEN_Q = LAST_PAID_Q + 1

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "m31_rank7_combined_domain_affine_johnson_endpoint_v1.schema.json"
)
VERIFIER_PATH = (
    ROOT
    / "experimental/scripts/"
    "verify_m31_rank7_combined_domain_affine_johnson_endpoint_v1.py"
)
INDEPENDENT_PATH = (
    ROOT
    / "experimental/scripts/"
    "verify_m31_rank7_combined_domain_affine_johnson_endpoint_v1_independent.py"
)
SAGE_PATH = (
    ROOT
    / "experimental/scripts/"
    "verify_m31_rank7_combined_domain_affine_johnson_endpoint_v1.sage"
)
NOTE_PATH = (
    ROOT
    / "experimental/notes/thresholds/"
    "m31_rank7_combined_domain_affine_johnson_endpoint_v1.md"
)
README_PATH = (
    ROOT
    / "experimental/data/certificates/"
    "m31-rank7-combined-domain-affine-johnson-endpoint-v1/README.md"
)
DEFAULT_MANIFEST = README_PATH.with_name("manifest.json")
GRANDE_FINALE = ROOT / "experimental/grande_finale.tex"
PARENT_MANIFEST = (
    ROOT
    / "experimental/data/certificates/"
    "m31-rank7-weighted-head-interlaced-source-route-cut-v1/manifest.json"
)
MIGRATION_MANIFEST = (
    ROOT
    / "experimental/data/certificates/"
    "m31-list-v4-grande-finale-provenance-migration-v1/manifest.json"
)
PARENT_PAYLOAD = (
    "376d3ba51fc2dd5a91eaef474859364c73984b4d83474387506632166438e8b3"
)
MIGRATION_PAYLOAD = (
    "6ecd0eda3035aef7544646f0e3f1ddbf8b9aad4c0a1a9e0f8518ac22e3671479"
)


class VerificationError(RuntimeError):
    pass


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


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


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def array_sha256(values: list[int]) -> str:
    return hashlib.sha256(canonical_bytes(values)).hexdigest()


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
    return {
        "binding_id": binding_id,
        "path": path.relative_to(ROOT).as_posix(),
        "role": role,
        "sha256": sha256_path(path),
        "internal_payload_sha256": internal_payload_sha256,
    }


def read_sealed(path: Path, expected: str, label: str) -> dict[str, Any]:
    data = strict_json(path)
    require(data.get("payload_sha256") == expected, f"{label} payload pin")
    require(payload_sha256(data) == expected, f"{label} payload seal")
    return data


def parameterized_affine_johnson_cap(
    rank: int,
    dimension: int,
    ambient_gap: int,
    excess: int,
) -> int:
    """Predecessor affine one-pivot cap intersected with active Johnson."""

    require(1 <= rank <= dimension, "local rank/dimension")
    require(ambient_gap >= 0 and excess >= 0, "local nonnegative gaps")
    inner = (
        comb(ambient_gap + rank - 1, rank - 1)
        // comb(excess + rank - 1, rank - 1)
    )
    result = (ambient_gap + dimension) * inner // (excess + dimension)
    denominator = (
        (excess + dimension) ** 2
        - (ambient_gap + dimension) * (dimension - 1)
    )
    if denominator > 0:
        result = min(
            result,
            (ambient_gap + dimension) * (excess + 1) // denominator,
        )
    return result


@lru_cache(maxsize=None)
def local_prefix_projective_arrays(
    cutoff: int,
) -> dict[int, list[int]]:
    """Replay the predecessor at-most-rank-six E0 cap."""

    ambient_gap = R - D
    excess = W - cutoff
    require(0 <= cutoff <= W, "cutoff range")
    require(excess >= 0, "E0 excess")
    arrays: dict[int, list[int]] = {}
    base = [0] * (D + 1)
    for dimension in range(1, D + 1):
        base[dimension] = (
            ambient_gap + dimension
        ) // (excess + dimension)
    arrays[1] = base

    for rank in range(2, MAX_RANK + 1):
        child = arrays[rank - 1]
        current = child.copy()
        prefix_cap = -1
        prefix_arg = -1
        window: deque[int] = deque()
        for dimension in range(rank, D + 1):
            added = dimension - 1
            if child[added] > prefix_cap:
                prefix_cap = child[added]
                prefix_arg = added
            while window and child[window[-1]] <= child[added]:
                window.pop()
            window.append(added)
            lower = dimension - (dimension - 1) // (rank - 1)
            while window and window[0] < lower:
                window.popleft()
            require(bool(window), "local projective window")
            require(prefix_arg >= rank - 1, "local projective prefix")
            two_tier = (
                (dimension - 1) * prefix_cap
                + (ambient_gap + 1) * child[window[0]]
            ) // (excess + dimension)
            exact = min(
                two_tier,
                parameterized_affine_johnson_cap(
                    rank,
                    dimension,
                    ambient_gap,
                    excess,
                ),
            )
            current[dimension] = max(child[dimension], exact)
        arrays[rank] = current
    return arrays


def affine_caps() -> list[int]:
    return [
        comb(K + rank, rank) // comb(W + rank, rank)
        for rank in range(MAX_RANK + 1)
    ]


def combined_johnson_denominator(dimension: int) -> int:
    return (
        (dimension + W) ** 2
        - (K + dimension) * (dimension - 1)
    )


def combined_cap(dimension: int, affine_cap: int) -> int:
    require(dimension >= 1, "combined dimension")
    result = affine_cap
    denominator = combined_johnson_denominator(dimension)
    if denominator > 0:
        result = min(
            result,
            (K + dimension) * (W + 1) // denominator,
        )
    return result


def prefix_arrays(class_caps: list[int]) -> tuple[list[int], list[int]]:
    prefix_caps = [0] * len(class_caps)
    prefix_args = [0] * len(class_caps)
    for size in range(1, len(class_caps)):
        if class_caps[size] > prefix_caps[size - 1]:
            prefix_caps[size] = class_caps[size]
            prefix_args[size] = size
        else:
            prefix_caps[size] = prefix_caps[size - 1]
            prefix_args[size] = prefix_args[size - 1]
    return prefix_caps, prefix_args


def top_six_outer_scan(
    cutoff: int,
    class_caps: list[int],
) -> dict[str, Any]:
    """Exhaust the predecessor top-six projective-line envelope."""

    largest_class = D - 6
    require(len(class_caps) == largest_class + 1, "class-cap length")
    prefix_caps, prefix_args = prefix_arrays(class_caps)
    agreement = G - cutoff
    require(agreement > 0, "outer agreement denominator")

    best_numerator = -1
    best: dict[str, int] | None = None
    survivor_sizes: list[int] = []
    for size in range(1, largest_class + 1):
        other_top_mass = D - 1 - size
        other_top_size_cap = min(size, other_top_mass - 4)
        tail_size_cap = min(size, other_top_mass // 5)
        if other_top_size_cap < 1 or tail_size_cap < 1:
            continue
        numerator = (
            size * class_caps[size]
            + other_top_mass * prefix_caps[other_top_size_cap]
            + (R - (D - 1)) * prefix_caps[tail_size_cap]
        )
        if numerator // agreement > SHALLOW_TARGET:
            survivor_sizes.append(size)
        if numerator > best_numerator:
            best_numerator = numerator
            best = {
                "largest_class_size": size,
                "largest_residual_dimension": D - size,
                "largest_class_cap": class_caps[size],
                "other_top_mass": other_top_mass,
                "other_top_size_cap": other_top_size_cap,
                "other_top_cap": prefix_caps[other_top_size_cap],
                "other_top_cap_arg_size": prefix_args[other_top_size_cap],
                "tail_mass": R - (D - 1),
                "tail_size_cap": tail_size_cap,
                "tail_cap": prefix_caps[tail_size_cap],
                "tail_cap_arg_size": prefix_args[tail_size_cap],
            }
    require(best is not None, "outer optimizer")
    head = best_numerator // agreement
    return {
        "cutoff": cutoff,
        "agreement_denominator": agreement,
        "objective_numerator": best_numerator,
        "objective_remainder": best_numerator % agreement,
        "head_cap": head,
        "target_margin": SHALLOW_TARGET - head,
        "pre_floor_target_margin":
            SHALLOW_TARGET * agreement - best_numerator,
        "survivor_count": len(survivor_sizes),
        "survivor_size_interval":
            [min(survivor_sizes), max(survivor_sizes)]
            if survivor_sizes
            else None,
        "survivor_residual_interval":
            [D - max(survivor_sizes), D - min(survivor_sizes)]
            if survivor_sizes
            else None,
        "class_cap_sha256": array_sha256(class_caps),
        "prefix_cap_sha256": array_sha256(prefix_caps),
        "prefix_arg_sha256": array_sha256(prefix_args),
        **best,
    }


def endpoint_scan(
    cutoff: int,
    *,
    affine_override: int | None = None,
    affine_override_dimensions: frozenset[int] | None = None,
) -> tuple[dict[str, Any], dict[str, str]]:
    arrays = local_prefix_projective_arrays(cutoff)
    e0_caps = arrays[MAX_RANK]
    generic_a6 = affine_caps()[MAX_RANK]
    largest_class = D - 6
    class_caps = [0] * (largest_class + 1)
    direct_caps = [0] * (D + 1)
    for dimension in range(1, D + 1):
        use_override = (
            affine_override is not None
            and (
                affine_override_dimensions is None
                or dimension in affine_override_dimensions
            )
        )
        affine_cap = affine_override if use_override else generic_a6
        direct_caps[dimension] = combined_cap(dimension, affine_cap)
    for size in range(1, largest_class + 1):
        dimension = D - size
        class_caps[size] = min(
            e0_caps[dimension],
            direct_caps[dimension],
        )
    result = top_six_outer_scan(cutoff, class_caps)
    hashes = {
        "E0_at_most_rank_six_sha256": array_sha256(e0_caps),
        "combined_direct_cap_sha256": array_sha256(direct_caps),
        "hybrid_class_cap_sha256": result["class_cap_sha256"],
        "prefix_cap_sha256": result["prefix_cap_sha256"],
        "prefix_arg_sha256": result["prefix_arg_sha256"],
    }
    return result, hashes


def exact_uniform_cap_threshold(cutoff: int) -> dict[str, Any]:
    a6 = affine_caps()[MAX_RANK]
    residual_dimensions = frozenset(range(4_981, 4_987))
    low = 0
    high = a6
    while low < high:
        middle = (low + high + 1) // 2
        result, _hashes = endpoint_scan(
            cutoff,
            affine_override=middle,
            affine_override_dimensions=residual_dimensions,
        )
        if result["head_cap"] <= SHALLOW_TARGET:
            low = middle
        else:
            high = middle - 1
    at_threshold, _ = endpoint_scan(
        cutoff,
        affine_override=low,
        affine_override_dimensions=residual_dimensions,
    )
    after_threshold, _ = endpoint_scan(
        cutoff,
        affine_override=low + 1,
        affine_override_dimensions=residual_dimensions,
    )
    return {
        "dimensions_receiving_uniform_cap": sorted(residual_dimensions),
        "largest_uniform_cap_closing_head": low,
        "improvement_from_generic_affine_cap": a6 - low,
        "head_at_threshold": at_threshold["head_cap"],
        "numerator_at_threshold": at_threshold["objective_numerator"],
        "remainder_at_threshold": at_threshold["objective_remainder"],
        "head_at_threshold_plus_one": after_threshold["head_cap"],
        "numerator_at_threshold_plus_one":
            after_threshold["objective_numerator"],
        "remainder_at_threshold_plus_one":
            after_threshold["objective_remainder"],
    }


def source_bindings() -> list[dict[str, Any]]:
    return [
        source_binding("packet_schema", SCHEMA_PATH, "Strict closed packet schema."),
        source_binding("packet_verifier", VERIFIER_PATH, "Primary fail-closed verifier."),
        source_binding(
            "independent_replay",
            INDEPENDENT_PATH,
            "Independent exact-integer recurrence replay.",
        ),
        source_binding(
            "sage_replay",
            SAGE_PATH,
            "Independent Sage exact-integer and symbolic replay.",
        ),
        source_binding("theorem_note", NOTE_PATH, "Proof, scope, and audit."),
        source_binding("packet_readme", README_PATH, "Replay and nonclaim contract."),
        source_binding(
            "current_grande_finale",
            GRANDE_FINALE,
            "Current affine-span and ordinary Johnson theorem source.",
        ),
        source_binding(
            "weighted_head_parent",
            PARENT_MANIFEST,
            "Sealed rank-seven source normalization and outer compiler.",
            PARENT_PAYLOAD,
        ),
        source_binding(
            "grande_finale_provenance_migration",
            MIGRATION_MANIFEST,
            "Exact compatibility for the parent's Grande Finale ancestors.",
            MIGRATION_PAYLOAD,
        ),
    ]


@lru_cache(maxsize=1)
def build_template() -> dict[str, Any]:
    parent = read_sealed(PARENT_MANIFEST, PARENT_PAYLOAD, "weighted parent")
    migration = read_sealed(
        MIGRATION_MANIFEST,
        MIGRATION_PAYLOAD,
        "Grande Finale migration",
    )
    require(parent["row"]["K"] == K, "parent K")
    require(parent["row"]["radius"] == R, "parent radius")
    require(parent["row"]["slack"] == W, "parent w")
    require(parent["row"]["B_star"] == BUDGET, "parent budget")
    require(parent["master_normalization"]["g"] == G, "parent g")
    require(parent["master_normalization"]["d"] == D, "parent d")
    require(
        parent["dual_domain_per_label_compiler"]["frontier"][
            "last_paid_Q"
        ]
        == 26_193,
        "parent frontier",
    )
    require(
        migration["manifest_audit"]["affected_manifest_count"] == 19,
        "migration manifest count",
    )
    require(
        migration["manifest_audit"]["all_payload_seals_valid"] is True,
        "migration payload seals",
    )
    require(
        migration["manifest_audit"]["all_non_grande_finale_bindings_fresh"]
        is True,
        "migration source freshness",
    )

    ranks = affine_caps()
    require(
        ranks
        == [1, 15, 241, 3_757, 58_410, 908_021, 14_115_528],
        "affine rank caps",
    )
    den_4980 = combined_johnson_denominator(4_980)
    den_4981 = combined_johnson_denominator(4_981)
    johnson_3145_den = combined_johnson_denominator(3_145)
    johnson_3145_num = (K + 3_145) * (W + 1)
    johnson_3145 = johnson_3145_num // johnson_3145_den
    johnson_4980 = (K + 4_980) * (W + 1) // den_4980
    require(den_4980 == 15_005, "Johnson last positive denominator")
    require(den_4981 == -898_676, "Johnson first inactive denominator")
    require(johnson_3145_den == 1_676_619_640, "Johnson k3145 denominator")
    require(johnson_3145_num == 70_936_478_008, "Johnson k3145 numerator")
    require(johnson_3145 == 42, "Johnson k3145 cap")
    require(johnson_4980 == 4_735_771, "Johnson k4980 cap")

    scan_26194, hashes_26194 = endpoint_scan(26_194)
    scan_29554, hashes_29554 = endpoint_scan(LAST_PAID_Q)
    scan_29555, hashes_29555 = endpoint_scan(FIRST_OPEN_Q)
    require(scan_26194["head_cap"] == 14_302_721, "Q26194 head")
    require(scan_26194["target_margin"] == 1_473_211, "Q26194 margin")
    require(scan_29554["head_cap"] == 15_775_891, "Q29554 head")
    require(scan_29554["target_margin"] == 41, "Q29554 margin")
    require(
        scan_29554["objective_numerator"] == 5_133_759_040_567,
        "Q29554 numerator",
    )
    require(scan_29555["head_cap"] == 15_776_139, "Q29555 head")
    require(scan_29555["target_margin"] == -207, "Q29555 excess")
    require(
        scan_29555["objective_numerator"] == 5_133_824_008_972,
        "Q29555 numerator",
    )
    require(scan_29555["survivor_count"] == 6, "Q29555 survivor count")
    require(
        scan_29555["survivor_size_interval"] == [282_539, 282_544],
        "Q29555 survivor sizes",
    )
    require(
        scan_29555["survivor_residual_interval"] == [4_981, 4_986],
        "Q29555 survivor dimensions",
    )

    threshold = exact_uniform_cap_threshold(FIRST_OPEN_Q)
    require(
        threshold["largest_uniform_cap_closing_head"] == 14_115_290,
        "uniform cap threshold",
    )
    require(
        threshold["improvement_from_generic_affine_cap"] == 238,
        "uniform improvement",
    )
    require(
        threshold["head_at_threshold"] == SHALLOW_TARGET,
        "threshold head",
    )
    require(
        threshold["head_at_threshold_plus_one"] == SHALLOW_TARGET + 1,
        "threshold sharpness",
    )

    result = {
        "schema": SCHEMA_ID,
        "theorem_id": THEOREM_ID,
        "architecture_id": ARCHITECTURE_ID,
        "status": STATUS,
        "row_contract": {
            "row": "Mersenne-31 list at 2^-100",
            "object": "LIST",
            "unit": "DISTINCT_CODEWORDS_PER_RECEIVED_WORD",
            "quantifier": "EVERY_ENDPOINT_RANK_AT_MOST_SEVEN_SHALLOW_FAMILY",
            "p": P,
            "n": N,
            "K": K,
            "agreement": AGREEMENT,
            "radius": R,
            "w": W,
            "g": G,
            "d": D,
            "B_star": BUDGET,
            "forced_shallow_nonanchors": SHALLOW_FORCED,
            "shallow_head_target": SHALLOW_TARGET,
            "partition_digest": PARTITION_DIGEST,
        },
        "combined_domain_lemma": {
            "deleted_line_size": "sigma",
            "normalized_label_size": "c<=sigma",
            "residual_dimension": "k=d-sigma",
            "domain": "(E0\\S) disjoint_union Z(P)",
            "domain_length": "K+k",
            "polynomial_degree_bound": "degree(a_i)<k",
            "affine_direction_rank_max": MAX_RANK,
            "agreement_identity":
                "(g-delta_i-c)+q_i=g+s_i-c>=g-sigma=k+w",
            "common_direction_zeros_allowed": True,
            "alignment_assumption": False,
            "affine_caps_by_rank_0_through_6": ranks,
            "at_most_rank_six_affine_cap": ranks[MAX_RANK],
            "johnson_denominator":
                "4550146385-913681*k",
            "johnson_last_active_dimension": 4_980,
            "johnson_first_inactive_dimension": 4_981,
            "johnson_k3145": {
                "numerator": johnson_3145_num,
                "denominator": johnson_3145_den,
                "cap": johnson_3145,
                "remainder": johnson_3145_num % johnson_3145_den,
            },
            "johnson_k4980_cap": johnson_4980,
            "combined_direct_cap_array_sha256":
                hashes_29554["combined_direct_cap_sha256"],
        },
        "exact_endpoint": {
            "previous_paid_cutoff": 26_193,
            "first_new_cutoff": 26_194,
            "last_paid_cutoff": LAST_PAID_Q,
            "all_smaller_heads_paid_by_cumulative_inclusion": True,
            "Q26194": {**scan_26194, "array_hashes": hashes_26194},
            "Q29554": {**scan_29554, "array_hashes": hashes_29554},
            "frontier_advance": LAST_PAID_Q - 26_193,
        },
        "first_unresolved_head": {
            "cutoff": FIRST_OPEN_Q,
            "compiled": {**scan_29555, "array_hashes": hashes_29555},
            "surviving_dimensions": [4_981, 4_982, 4_983, 4_984, 4_985, 4_986],
            "johnson_inactive_on_all_survivors": True,
            "uniform_combined_cap_threshold": threshold,
            "required_uniform_improvement": 238,
            "route_cut_scope":
                "EXACT_CURRENT_AFFINE_JOHNSON_AND_E0_OUTER_COMPILER_ONLY",
            "source_incidence_theorem_proved": False,
        },
        "ledger_state": {
            "local_rank7_frontier_moved": True,
            "ledger_movement": 0,
            "official_endpoint_movement": 0,
            "row_closed": False,
            "U_paid": 3_730,
            "U_Q": None,
            "U_list_int": None,
            "U_ext": None,
            "U_new": None,
            "signed_Xi46_paid": False,
        },
        "nonclaims": {
            "global_rank7_closed": False,
            "rank_at_least_8_treated": False,
            "v4_atom_paid": False,
            "row_upper_bound_proved": False,
            "Q29555_paid": False,
            "uniform_cap_14115290_proved": False,
            "no_common_zero_recurrence_used": False,
            "alignment_completeness_assumed": False,
            "stable_paper_modified": False,
            "lean_used": False,
        },
        "source_bindings": source_bindings(),
    }
    return seal(result)


def validate_schema_shape(data: dict[str, Any]) -> None:
    schema = strict_json(SCHEMA_PATH)
    require(schema["$id"] == SCHEMA_ID, "schema id")
    require(schema["additionalProperties"] is False, "closed schema")
    require(set(data) == set(schema["required"]), "closed top-level keys")
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
        require(
            binding["sha256"] == sha256_path(path),
            f"fresh source {binding_id}",
        )
        internal = binding["internal_payload_sha256"]
        if internal is not None:
            source = strict_json(path)
            require(
                source.get("payload_sha256") == internal,
                f"internal pin {binding_id}",
            )
            require(
                payload_sha256(source) == internal,
                f"internal seal {binding_id}",
            )


def validate_semantics(data: dict[str, Any]) -> None:
    lemma = data["combined_domain_lemma"]
    endpoint = data["exact_endpoint"]
    residual = data["first_unresolved_head"]
    ledger = data["ledger_state"]
    nonclaims = data["nonclaims"]
    require(lemma["domain_length"] == "K+k", "combined domain length")
    require(
        lemma["affine_direction_rank_max"] == MAX_RANK,
        "combined rank",
    )
    require(
        lemma["common_direction_zeros_allowed"] is True,
        "common-zero safety",
    )
    require(lemma["alignment_assumption"] is False, "no alignment")
    require(
        endpoint["Q29554"]["head_cap"] <= SHALLOW_TARGET,
        "endpoint paid",
    )
    require(endpoint["Q29554"]["target_margin"] == 41, "endpoint margin")
    require(
        residual["compiled"]["head_cap"] > SHALLOW_TARGET,
        "next head open",
    )
    require(residual["required_uniform_improvement"] == 238, "next threshold")
    require(
        residual["source_incidence_theorem_proved"] is False,
        "source theorem open",
    )
    require(ledger["ledger_movement"] == 0, "zero ledger movement")
    require(ledger["row_closed"] is False, "row open")
    require(
        [ledger[name] for name in ("U_Q", "U_list_int", "U_ext", "U_new")]
        == [None, None, None, None],
        "null atoms",
    )
    require(all(value is False for value in nonclaims.values()), "nonclaims")


def validate(data: dict[str, Any]) -> None:
    validate_schema_shape(data)
    require(data["payload_sha256"] == payload_sha256(data), "payload seal")
    validate_sources(data)
    validate_semantics(data)
    deep_exact(data, build_template())


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
    mutations = [
        (
            "combined length",
            mutate(
                template,
                ("combined_domain_lemma", "domain_length"),
                "K+k+1",
            ),
        ),
        (
            "combined rank",
            mutate(
                template,
                ("combined_domain_lemma", "affine_direction_rank_max"),
                7,
            ),
        ),
        (
            "common-zero restriction",
            mutate(
                template,
                ("combined_domain_lemma", "common_direction_zeros_allowed"),
                False,
            ),
        ),
        (
            "alignment assumption",
            mutate(
                template,
                ("combined_domain_lemma", "alignment_assumption"),
                True,
            ),
        ),
        (
            "affine cap",
            mutate(
                template,
                ("combined_domain_lemma", "at_most_rank_six_affine_cap"),
                14_115_527,
            ),
        ),
        (
            "Johnson boundary",
            mutate(
                template,
                ("combined_domain_lemma", "johnson_last_active_dimension"),
                4_981,
            ),
        ),
        (
            "endpoint head",
            mutate(
                template,
                ("exact_endpoint", "Q29554", "head_cap"),
                15_775_892,
            ),
        ),
        (
            "endpoint numerator",
            mutate(
                template,
                ("exact_endpoint", "Q29554", "objective_numerator"),
                5_133_759_040_568,
            ),
        ),
        (
            "next head",
            mutate(
                template,
                ("first_unresolved_head", "compiled", "head_cap"),
                SHALLOW_TARGET,
            ),
        ),
        (
            "survivor interval",
            mutate(
                template,
                (
                    "first_unresolved_head",
                    "compiled",
                    "survivor_residual_interval",
                ),
                [4_980, 4_986],
            ),
        ),
        (
            "uniform threshold",
            mutate(
                template,
                (
                    "first_unresolved_head",
                    "uniform_combined_cap_threshold",
                    "largest_uniform_cap_closing_head",
                ),
                14_115_291,
            ),
        ),
        (
            "false source theorem",
            mutate(
                template,
                (
                    "first_unresolved_head",
                    "source_incidence_theorem_proved",
                ),
                True,
            ),
        ),
        (
            "ledger movement",
            mutate(template, ("ledger_state", "ledger_movement"), 1),
        ),
        (
            "atom payment",
            mutate(template, ("ledger_state", "U_new"), 0),
        ),
        (
            "row closure",
            mutate(template, ("ledger_state", "row_closed"), True),
        ),
        (
            "false global claim",
            mutate(template, ("nonclaims", "global_rank7_closed"), True),
        ),
        (
            "array hash",
            mutate(
                template,
                (
                    "exact_endpoint",
                    "Q29554",
                    "array_hashes",
                    "hybrid_class_cap_sha256",
                ),
                "0" * 64,
            ),
        ),
        (
            "payload hash",
            {**template, "payload_sha256": "0" * 64},
        ),
        (
            "source hash",
            mutate(template, ("source_bindings", 0, "sha256"), "0" * 64),
        ),
        (
            "source path",
            mutate(template, ("source_bindings", 0, "path"), "../schema.json"),
        ),
        (
            "parent payload",
            mutate(
                template,
                ("source_bindings", 7, "internal_payload_sha256"),
                "0" * 64,
            ),
        ),
        (
            "migration payload",
            mutate(
                template,
                ("source_bindings", 8, "internal_payload_sha256"),
                "0" * 64,
            ),
        ),
    ]
    for label, candidate in mutations:
        expect_rejected(label, candidate)
    print(
        "M31 rank7 combined-domain hostile controls: "
        f"PASS ({len(mutations)} mutations)"
    )


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
            print(
                "M31 rank7 combined-domain endpoint: "
                f"PASS ({CHECKS} checks)"
            )
        if args.tamper_selftest:
            tamper_selftest(template)
        if not (args.print_template or args.check or args.tamper_selftest):
            validate(strict_json(args.manifest))
            print(
                "M31 rank7 combined-domain endpoint: "
                f"PASS ({CHECKS} checks)"
            )
    except (OSError, KeyError, TypeError, ValueError, VerificationError) as exc:
        print(
            f"M31 rank7 combined-domain endpoint: FAIL: {exc}",
            file=sys.stderr,
        )
        raise SystemExit(1)


if __name__ == "__main__":
    main()
