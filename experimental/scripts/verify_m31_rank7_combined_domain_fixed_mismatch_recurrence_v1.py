#!/usr/bin/env python3
"""Verify the M31 rank-seven combined-domain fixed-mismatch recurrence."""

from __future__ import annotations

import argparse
import copy
import hashlib
import heapq
import json
import sys
from collections import deque
from functools import lru_cache
from math import comb
from pathlib import Path, PurePosixPath
from typing import Any


SCHEMA_ID = (
    "rs-mca-m31-rank7-combined-domain-fixed-mismatch-recurrence-v1"
)
THEOREM_ID = "M31_RANK7_COMBINED_DOMAIN_FIXED_MISMATCH_RECURRENCE_V1"
ARCHITECTURE_ID = THEOREM_ID
STATUS = (
    "PROVED_LOCAL_Q147594_HEAD_Q147595_FORTY_FIVE_UNIT_ROUTE_CUT_ROW_OPEN"
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
MAX_DIRECTION_RANK = 6
PREVIOUS_PAID_Q = 29_554
LAST_COARSE_PAID_Q = 147_593
LAST_PAID_Q = 147_594
FIRST_OPEN_Q = LAST_PAID_Q + 1
PADDING_MARGIN = P - K - 2 * D + 1

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "m31_rank7_combined_domain_fixed_mismatch_recurrence_v1.schema.json"
)
VERIFIER_PATH = (
    ROOT
    / "experimental/scripts/"
    "verify_m31_rank7_combined_domain_fixed_mismatch_recurrence_v1.py"
)
INDEPENDENT_PATH = (
    ROOT
    / "experimental/scripts/"
    "verify_m31_rank7_combined_domain_fixed_mismatch_recurrence_v1_independent.py"
)
SAGE_PATH = (
    ROOT
    / "experimental/scripts/"
    "verify_m31_rank7_combined_domain_fixed_mismatch_recurrence_v1.sage"
)
NOTE_PATH = (
    ROOT
    / "experimental/notes/thresholds/"
    "m31_rank7_combined_domain_fixed_mismatch_recurrence_v1.md"
)
README_PATH = (
    ROOT
    / "experimental/data/certificates/"
    "m31-rank7-combined-domain-fixed-mismatch-recurrence-v1/README.md"
)
DEFAULT_MANIFEST = README_PATH.with_name("manifest.json")
COMBINED_PARENT_MANIFEST = (
    ROOT
    / "experimental/data/certificates/"
    "m31-rank7-combined-domain-affine-johnson-endpoint-v1/manifest.json"
)
WEIGHTED_PARENT_MANIFEST = (
    ROOT
    / "experimental/data/certificates/"
    "m31-rank7-weighted-head-interlaced-source-route-cut-v1/manifest.json"
)
RANK6_PARENT_MANIFEST = (
    ROOT
    / "experimental/data/certificates/"
    "m31-rank6-generalized-weight-codim1-closure-v1/manifest.json"
)
MIGRATION_MANIFEST = (
    ROOT
    / "experimental/data/certificates/"
    "m31-list-v4-grande-finale-provenance-migration-v1/manifest.json"
)
COMBINED_PARENT_PAYLOAD = (
    "f31401e929a3cf5e7cbe01ef6541a2be956a6a7dd2497099542a27c7b39a0eab"
)
WEIGHTED_PARENT_PAYLOAD = (
    "376d3ba51fc2dd5a91eaef474859364c73984b4d83474387506632166438e8b3"
)
RANK6_PARENT_PAYLOAD = (
    "3e0a6102795f88aa8121229bc40bcc723aa7e5cc81bbcfd5b0013adf5d11caf9"
)
MIGRATION_PAYLOAD = (
    "6ecd0eda3035aef7544646f0e3f1ddbf8b9aad4c0a1a9e0f8518ac22e3671479"
)
RANK6_PARENT_MANIFEST_SHA256 = (
    "5c9b5c6e30f4348b604ceb043c684e4b4595ac2d88d1f9da90d6c295caf3f01d"
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
    """Unconditional affine one-pivot cap intersected with Johnson."""

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


@lru_cache(maxsize=1)
def no_common_zero_recurrence_arrays() -> dict[int, list[int]]:
    """Replay Theorem 2.2/Corollary 2.3 at gap K and excess w."""

    arrays: dict[int, list[int]] = {}
    base = [0] * (D + 1)
    for dimension in range(1, D + 1):
        base[dimension] = (K + dimension) // (W + dimension)
    arrays[1] = base

    for rank in range(2, MAX_DIRECTION_RANK + 1):
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
            if not window or prefix_arg < rank - 1:
                raise VerificationError("projective recurrence window")
            recurrence = (
                (dimension - 1) * prefix_cap
                + (K + 1) * child[window[0]]
            ) // (W + dimension)
            direct = parameterized_affine_johnson_cap(
                rank,
                dimension,
                K,
                W,
            )
            exact_rank = min(recurrence, direct)
            current[dimension] = max(child[dimension], exact_rank)
        arrays[rank] = current
    return arrays


def source_dimension_caps() -> tuple[list[int], list[int]]:
    recurrence = no_common_zero_recurrence_arrays()[MAX_DIRECTION_RANK]
    return recurrence, recurrence.copy()


def prefix_arrays(class_caps: list[int]) -> tuple[list[int], list[int]]:
    caps = [0] * len(class_caps)
    args = [0] * len(class_caps)
    for size in range(1, len(class_caps)):
        if class_caps[size] > caps[size - 1]:
            caps[size] = class_caps[size]
            args[size] = size
        else:
            caps[size] = caps[size - 1]
            args[size] = args[size - 1]
    return caps, args


def class_caps_from_dimension_caps(
    dimension_caps: list[int],
    *,
    k4981_reduction: int = 0,
) -> list[int]:
    largest_class = D - MAX_DIRECTION_RANK
    class_caps = [0] * (largest_class + 1)
    for size in range(1, largest_class + 1):
        dimension = D - size
        cap = dimension_caps[dimension]
        if dimension == 4_981:
            cap -= k4981_reduction
        class_caps[size] = cap
    return class_caps


def top_six_outer_scan(
    cutoff: int,
    class_caps: list[int],
) -> dict[str, Any]:
    """Exhaust the predecessor top-six projective-line envelope."""

    largest_class = D - MAX_DIRECTION_RANK
    require(len(class_caps) == largest_class + 1, "class-cap length")
    prefix_caps, prefix_args = prefix_arrays(class_caps)
    denominator = G - cutoff
    require(denominator > 0, "positive outer denominator")

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
        if numerator // denominator > SHALLOW_TARGET:
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
    head = best_numerator // denominator
    return {
        "cutoff": cutoff,
        "agreement_denominator": denominator,
        "objective_numerator": best_numerator,
        "objective_remainder": best_numerator % denominator,
        "head_cap": head,
        "target_margin": SHALLOW_TARGET - head,
        "pre_floor_target_margin":
            SHALLOW_TARGET * denominator - best_numerator,
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
    k4981_reduction: int = 0,
) -> dict[str, Any]:
    _recurrence, safe = source_dimension_caps()
    classes = class_caps_from_dimension_caps(
        safe,
        k4981_reduction=k4981_reduction,
    )
    return top_six_outer_scan(cutoff, classes)


def exact_tail_partition(
    tail_mass: int,
    maximum_part: int,
    class_caps: list[int],
) -> dict[str, Any]:
    """Maximize sum s*F(s) over a partition with parts at most maximum_part."""

    baseline = max(class_caps[1:maximum_part + 1])
    baseline_args = [
        size
        for size in range(1, maximum_part + 1)
        if class_caps[size] == baseline
    ]
    require(baseline_args == [maximum_part], "unique tail baseline size")
    losses = [0] + [
        size * (baseline - class_caps[size])
        for size in range(1, maximum_part + 1)
    ]
    infinity = 10**100
    distance = [infinity] * maximum_part
    witness_mass = [infinity] * maximum_part
    previous: list[tuple[int, int] | None] = [None] * maximum_part
    distance[0] = 0
    witness_mass[0] = 0
    heap: list[tuple[int, int, int]] = [(0, 0, 0)]
    while heap:
        cost, mass, residue = heapq.heappop(heap)
        if (cost, mass) != (distance[residue], witness_mass[residue]):
            continue
        for part in range(1, maximum_part):
            new_residue = (residue + part) % maximum_part
            candidate = (cost + losses[part], mass + part)
            if candidate < (
                distance[new_residue],
                witness_mass[new_residue],
            ):
                distance[new_residue], witness_mass[new_residue] = candidate
                previous[new_residue] = (residue, part)
                heapq.heappush(
                    heap,
                    (candidate[0], candidate[1], new_residue),
                )

    target_residue = tail_mass % maximum_part
    require(witness_mass[target_residue] <= tail_mass, "tail witness mass")
    require(
        (tail_mass - witness_mass[target_residue]) % maximum_part == 0,
        "tail filler divisibility",
    )
    parts: list[int] = []
    residue = target_residue
    while residue:
        step = previous[residue]
        require(step is not None, "tail witness predecessor")
        old_residue, part = step
        parts.append(part)
        residue = old_residue
    filler_count = (
        tail_mass - witness_mass[target_residue]
    ) // maximum_part
    objective = tail_mass * baseline - distance[target_residue]
    return {
        "tail_mass": tail_mass,
        "maximum_part": maximum_part,
        "baseline_cap": baseline,
        "target_residue": target_residue,
        "minimum_loss": distance[target_residue],
        "witness_nonmaximum_parts": sorted(parts),
        "witness_maximum_part_count": filler_count,
        "witness_mass": witness_mass[target_residue]
            + filler_count * maximum_part,
        "objective": objective,
        "loss_array_sha256": array_sha256(losses),
        "residue_distance_sha256": array_sha256(distance),
        "residue_witness_mass_sha256": array_sha256(witness_mass),
    }


def refined_top_five_scan(
    cutoff: int,
    *,
    k4981_reduction: int = 0,
) -> dict[str, Any]:
    """Refine the unique coarse survivor by retaining s6 and tail residues."""

    _recurrence, safe = source_dimension_caps()
    class_caps = class_caps_from_dimension_caps(
        safe,
        k4981_reduction=k4981_reduction,
    )
    coarse = top_six_outer_scan(cutoff, class_caps)
    prefix_caps, prefix_args = prefix_arrays(class_caps)
    largest_size = 282_544
    top_budget = D - 1 - largest_size
    maximum_sixth = top_budget // 5
    require(maximum_sixth == 996, "maximum sixth size")

    uniform_candidates: list[tuple[int, int]] = []
    for sixth_size in range(1, maximum_sixth + 1):
        second_size_cap = top_budget - 4 * sixth_size
        require(second_size_cap >= sixth_size, "top-five size ordering")
        uniform_nonlargest = (
            (R - largest_size) * prefix_caps[sixth_size]
            + top_budget
            * (
                prefix_caps[second_size_cap]
                - prefix_caps[sixth_size]
            )
        )
        uniform_candidates.append((uniform_nonlargest, sixth_size))
    ordered = sorted(uniform_candidates, reverse=True)
    require(ordered[0][1] == maximum_sixth, "uniform maximizing sixth")
    require(ordered[1][1] in (990, 991), "uniform runner sixth")

    tail_mass = R - largest_size - top_budget
    tail = exact_tail_partition(tail_mass, maximum_sixth, class_caps)
    require(
        top_budget == 5 * maximum_sixth,
        "maximizer forces five equal top parts",
    )
    exact_nonlargest = (
        top_budget * class_caps[maximum_sixth]
        + tail["objective"]
    )
    require(
        exact_nonlargest > ordered[1][0],
        "exact maximizer beats every other uniform envelope",
    )
    numerator = (
        largest_size * class_caps[largest_size]
        + exact_nonlargest
    )
    denominator = G - cutoff
    head = numerator // denominator

    coarse_runner_numerator = -1
    coarse_runner_size = -1
    for size in range(1, len(class_caps)):
        if size == largest_size:
            continue
        other_top_mass = D - 1 - size
        other_top_size_cap = min(size, other_top_mass - 4)
        tail_size_cap = min(size, other_top_mass // 5)
        if other_top_size_cap < 1 or tail_size_cap < 1:
            continue
        value = (
            size * class_caps[size]
            + other_top_mass * prefix_caps[other_top_size_cap]
            + (R - (D - 1)) * prefix_caps[tail_size_cap]
        )
        if value > coarse_runner_numerator:
            coarse_runner_numerator = value
            coarse_runner_size = size

    return {
        "cutoff": cutoff,
        "agreement_denominator": denominator,
        "coarse": coarse,
        "coarse_runner": {
            "largest_class_size": coarse_runner_size,
            "largest_residual_dimension": D - coarse_runner_size,
            "objective_numerator": coarse_runner_numerator,
            "head_cap": coarse_runner_numerator // denominator,
            "objective_remainder": coarse_runner_numerator % denominator,
        },
        "refined_largest_class_size": largest_size,
        "refined_largest_residual_dimension": D - largest_size,
        "refined_largest_class_cap": class_caps[largest_size],
        "top_five_budget": top_budget,
        "maximum_sixth_size": maximum_sixth,
        "uniform_nonlargest_max": ordered[0][0],
        "uniform_nonlargest_runner": ordered[1][0],
        "uniform_runner_sixth_sizes": sorted(
            size
            for value, size in uniform_candidates
            if value == ordered[1][0]
        ),
        "exact_tail_partition": tail,
        "exact_nonlargest_contribution": exact_nonlargest,
        "objective_numerator": numerator,
        "objective_remainder": numerator % denominator,
        "head_cap": head,
        "target_margin": SHALLOW_TARGET - head,
        "pre_floor_target_margin":
            SHALLOW_TARGET * denominator - numerator,
        "survivor_count": 1 if head > SHALLOW_TARGET else 0,
        "class_cap_sha256": array_sha256(class_caps),
        "prefix_cap_sha256": array_sha256(prefix_caps),
        "prefix_arg_sha256": array_sha256(prefix_args),
    }


def source_bindings() -> list[dict[str, Any]]:
    return [
        source_binding("packet_schema", SCHEMA_PATH, "Closed packet schema."),
        source_binding("packet_verifier", VERIFIER_PATH, "Primary verifier."),
        source_binding(
            "independent_replay",
            INDEPENDENT_PATH,
            "Independent heap-based exact-integer replay.",
        ),
        source_binding(
            "sage_replay",
            SAGE_PATH,
            "Sage exact-integer and finite-field control.",
        ),
        source_binding("theorem_note", NOTE_PATH, "Proof, scope, and audit."),
        source_binding("packet_readme", README_PATH, "Replay contract."),
        source_binding(
            "combined_domain_parent",
            COMBINED_PARENT_MANIFEST,
            "Sealed combined-domain construction and outer compiler.",
            COMBINED_PARENT_PAYLOAD,
        ),
        source_binding(
            "weighted_recurrence_parent",
            WEIGHTED_PARENT_MANIFEST,
            "Sealed full-projective-line recurrence and source normalization.",
            WEIGHTED_PARENT_PAYLOAD,
        ),
        source_binding(
            "rank6_closure_parent",
            RANK6_PARENT_MANIFEST,
            "Sealed exclusion of the whole-family rank-at-most-six branch.",
            RANK6_PARENT_PAYLOAD,
        ),
        source_binding(
            "grande_finale_provenance_migration",
            MIGRATION_MANIFEST,
            "Exact compatibility certificate for the rank-six parent's canonical source ancestor.",
            MIGRATION_PAYLOAD,
        ),
    ]


@lru_cache(maxsize=1)
def build_template() -> dict[str, Any]:
    combined_parent = read_sealed(
        COMBINED_PARENT_MANIFEST,
        COMBINED_PARENT_PAYLOAD,
        "combined parent",
    )
    weighted_parent = read_sealed(
        WEIGHTED_PARENT_MANIFEST,
        WEIGHTED_PARENT_PAYLOAD,
        "weighted parent",
    )
    rank6_parent = read_sealed(
        RANK6_PARENT_MANIFEST,
        RANK6_PARENT_PAYLOAD,
        "rank6 parent",
    )
    migration = read_sealed(
        MIGRATION_MANIFEST,
        MIGRATION_PAYLOAD,
        "provenance migration",
    )
    migration_audit = migration["manifest_audit"]
    require(
        migration_audit["all_payload_seals_valid"] is True,
        "migration payload seals",
    )
    require(
        migration_audit["all_non_grande_finale_bindings_fresh"] is True,
        "migration non-Grande-Finale bindings",
    )
    rank6_relative = RANK6_PARENT_MANIFEST.relative_to(ROOT).as_posix()
    rank6_records = [
        record
        for record in migration_audit["records"]
        if record["path"] == rank6_relative
    ]
    require(len(rank6_records) == 1, "unique rank6 migration record")
    rank6_record = rank6_records[0]
    require(
        rank6_record["payload_sha256"] == RANK6_PARENT_PAYLOAD,
        "rank6 migrated payload",
    )
    require(
        rank6_record["manifest_sha256"]
        == RANK6_PARENT_MANIFEST_SHA256
        == sha256_path(RANK6_PARENT_MANIFEST),
        "rank6 migrated manifest",
    )
    require(
        rank6_record["validation"]
        == "PASS_EXCEPT_EXACT_CANONICAL_GRANDE_FINALE_ANCESTOR",
        "rank6 migration validation",
    )
    require(
        rank6_record["compatible_binding"]["path"]
        == migration["source_contract"]["path"]
        == "experimental/grande_finale.tex",
        "rank6 migrated source path",
    )
    require(
        rank6_record["compatible_binding"]["current_sha256"]
        == migration["source_contract"]["current_sha256"],
        "rank6 current source compatibility",
    )
    row = combined_parent["row_contract"]
    require(row["K"] == K, "parent K")
    require(row["radius"] == R, "parent radius")
    require(row["w"] == W, "parent w")
    require(row["g"] == G, "parent g")
    require(row["d"] == D, "parent d")
    require(
        combined_parent["exact_endpoint"]["last_paid_cutoff"]
        == PREVIOUS_PAID_Q,
        "parent cutoff",
    )
    require(
        weighted_parent["master_normalization"]["g"] == G,
        "weighted parent g",
    )
    require(
        weighted_parent["recursive_full_line_compiler"]["status"]
        == "PROVED_SOURCE_BOUND",
        "weighted recurrence status",
    )
    require(
        rank6_parent["rank_consequence"]["rank_1_through_6_excluded"]
        is True,
        "rank-at-most-six branch paid",
    )
    require(
        rank6_parent["rank_consequence"]["whole_rank6_chart_upper"]
        == 908_116,
        "rank-six whole-chart cap",
    )

    affine_rank_caps = [
        comb(K + rank, rank) // comb(W + rank, rank)
        for rank in range(MAX_DIRECTION_RANK + 1)
    ]
    require(
        affine_rank_caps
        == [1, 15, 241, 3_757, 58_410, 908_021, 14_115_528],
        "affine rank caps",
    )
    require(PADDING_MARGIN == 2_145_860_022, "padding margin")

    arrays = no_common_zero_recurrence_arrays()
    recurrence, safe = source_dimension_caps()
    six_values = [recurrence[k] for k in range(4_981, 4_987)]
    require(
        six_values
        == [
            9_806_438,
            9_806_312,
            9_806_186,
            9_806_060,
            9_805_934,
            9_805_807,
        ],
        "six recurrence values",
    )
    require(arrays[5][4_980] == 674_155, "rank-five child at k4980")
    recurrence_numerator = (4_981 - 1) * 674_155 + (K + 1) * 674_155
    recurrence_denominator = W + 4_981
    require(recurrence_numerator == 710_260_719_335, "k4981 numerator")
    require(recurrence_denominator == 72_428, "k4981 denominator")
    require(
        recurrence_numerator // recurrence_denominator == 9_806_438,
        "k4981 quotient",
    )
    require(
        recurrence_numerator % recurrence_denominator == 27_871,
        "k4981 remainder",
    )

    class_caps = class_caps_from_dimension_caps(safe)
    prefix_caps, prefix_args = prefix_arrays(class_caps)
    scan_previous = endpoint_scan(PREVIOUS_PAID_Q + 1)
    scan_last_coarse = endpoint_scan(LAST_COARSE_PAID_Q)
    scan_last = refined_top_five_scan(LAST_PAID_Q)
    scan_open = refined_top_five_scan(FIRST_OPEN_Q)
    scan_reduce_44 = refined_top_five_scan(
        FIRST_OPEN_Q,
        k4981_reduction=44,
    )
    scan_reduce_45 = refined_top_five_scan(
        FIRST_OPEN_Q,
        k4981_reduction=45,
    )

    require(scan_previous["head_cap"] == 10_053_521, "Q29555 head")
    require(scan_previous["target_margin"] == 5_722_411, "Q29555 margin")
    require(
        scan_last_coarse["objective_numerator"] == 3_271_586_860_242,
        "last coarse numerator",
    )
    require(
        scan_last_coarse["head_cap"] == 15_775_883,
        "last coarse paid head",
    )
    require(
        scan_last["coarse"]["survivor_count"] == 1,
        "refined coarse survivor count",
    )
    require(
        scan_last["coarse"]["survivor_size_interval"]
        == [282_544, 282_544],
        "refined coarse survivor size",
    )
    require(
        scan_last["coarse_runner"]["largest_class_size"] == 282_543,
        "coarse runner size",
    )
    require(
        scan_last["coarse_runner"]["head_cap"] == 15_775_743,
        "coarse runner head",
    )
    require(
        scan_last["uniform_nonlargest_max"] == 500_828_161_030,
        "uniform nonlargest maximum",
    )
    require(
        scan_last["uniform_nonlargest_runner"] == 500_826_095_155,
        "uniform nonlargest runner",
    )
    tail = scan_last["exact_tail_partition"]
    require(tail["tail_mass"] == 693_605, "tail mass")
    require(tail["maximum_part"] == 996, "tail maximum part")
    require(tail["baseline_cap"] == 716_918, "tail baseline cap")
    require(tail["target_residue"] == 389, "tail residue")
    require(tail["minimum_loss"] == 87_136, "tail minimum loss")
    require(tail["witness_nonmaximum_parts"] == [389], "tail witness part")
    require(tail["witness_maximum_part_count"] == 696, "tail filler count")
    require(tail["objective"] == 497_257_822_254, "tail objective")
    require(
        scan_last["exact_nonlargest_contribution"] == 500_828_073_894,
        "exact nonlargest contribution",
    )
    require(
        scan_last["objective_numerator"] == 3_271_578_292_166,
        "last refined numerator",
    )
    require(scan_last["agreement_denominator"] == 207_378, "last denominator")
    require(scan_last["objective_remainder"] == 176_540, "last remainder")
    require(scan_last["head_cap"] == 15_775_917, "last head")
    require(scan_last["target_margin"] == 15, "last margin")
    require(scan_open["agreement_denominator"] == 207_377, "open denominator")
    require(
        scan_open["objective_numerator"] == 3_271_578_292_166,
        "open numerator",
    )
    require(scan_open["objective_remainder"] == 191_805, "open remainder")
    require(scan_open["head_cap"] == 15_775_993, "open head")
    require(scan_open["target_margin"] == -61, "open excess")
    require(scan_open["survivor_count"] == 1, "open survivor count")
    require(
        scan_open["refined_largest_class_size"] == 282_544,
        "open survivor largest size",
    )
    require(
        scan_open["refined_largest_residual_dimension"] == 4_981,
        "open survivor residual dimension",
    )
    require(scan_reduce_44["head_cap"] == 15_775_933, "44 reduction fails")
    require(scan_reduce_44["target_margin"] == -1, "44 reduction excess")
    require(
        scan_reduce_44["objective_numerator"] == 3_271_565_860_230,
        "44 reduction numerator",
    )
    require(scan_reduce_45["head_cap"] == SHALLOW_TARGET, "45 reduction closes")
    require(scan_reduce_45["target_margin"] == 0, "45 reduction margin")
    require(
        scan_reduce_45["objective_numerator"] == 3_271_565_577_686,
        "45 reduction numerator",
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
            "quantifier":
                "EVERY_SURVIVING_EXACT_RANK_SEVEN_ENDPOINT_SHALLOW_FAMILY",
            "rank_at_most_six_branch_paid_separately": True,
            "rank_at_most_six_whole_chart_cap": 908_116,
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
            "partition_digest": row["partition_digest"],
        },
        "fixed_mismatch_lemma": {
            "combined_domain": "(E0\\S) disjoint_union Z(P)",
            "combined_domain_length": "K+k",
            "combined_agreement_lower_bound": "k+w",
            "counted_normalized_label_nonzero": True,
            "complete_projective_line_required": True,
            "exact_lcm_no_common_zero_on_ZP_required": True,
            "surviving_master_span_rank": 7,
            "full_label_hyperplane_used": True,
            "full_label_hyperplane_direction":
                "ker(lambda|W)/L_S",
            "full_label_hyperplane_direction_rank": 6,
            "actual_label_class_contained_in_full_hyperplane_list": True,
            "extra_hyperplane_members_need_source_factorization": False,
            "full_hyperplane_common_zero_is_fixed_mismatch": True,
            "padding_points_used": True,
            "padding_margin": PADDING_MARGIN,
            "source_cap_formula": "C6_no_common_zero(K,w;k)",
            "alignment_assumption": False,
        },
        "recurrence_certificate": {
            "ambient_gap": K,
            "excess": W,
            "maximum_dimension": D,
            "maximum_direction_rank": MAX_DIRECTION_RANK,
            "rank_caps_sha256": {
                str(rank): array_sha256(arrays[rank])
                for rank in range(1, MAX_DIRECTION_RANK + 1)
            },
            "rank_six_sha256": array_sha256(recurrence),
            "uniform_source_dimension_cap_sha256": array_sha256(safe),
            "class_cap_sha256": array_sha256(class_caps),
            "prefix_cap_sha256": array_sha256(prefix_caps),
            "prefix_arg_sha256": array_sha256(prefix_args),
            "six_residual_dimensions": list(range(4_981, 4_987)),
            "six_rank_six_caps": six_values,
            "k4981_division": {
                "rank_five_child_cap": arrays[5][4_980],
                "numerator": recurrence_numerator,
                "denominator": recurrence_denominator,
                "quotient": recurrence_numerator // recurrence_denominator,
                "remainder": recurrence_numerator % recurrence_denominator,
            },
        },
        "exact_endpoint": {
            "previous_paid_cutoff": PREVIOUS_PAID_Q,
            "first_new_cutoff": PREVIOUS_PAID_Q + 1,
            "last_coarse_paid_cutoff": LAST_COARSE_PAID_Q,
            "last_paid_cutoff": LAST_PAID_Q,
            "frontier_advance": LAST_PAID_Q - PREVIOUS_PAID_Q,
            "all_smaller_heads_paid_by_cumulative_inclusion": True,
            "Q29555": scan_previous,
            "Q147593_coarse": scan_last_coarse,
            "Q147594_refined": scan_last,
        },
        "first_unresolved_head": {
            "cutoff": FIRST_OPEN_Q,
            "compiled": scan_open,
            "unique_residual_dimension": 4_981,
            "current_class_cap": 9_806_438,
            "largest_closing_class_cap": 9_806_393,
            "required_improvement": 45,
            "forty_four_unit_control": scan_reduce_44,
            "forty_five_unit_control": scan_reduce_45,
            "forty_five_unit_improvement_proved": False,
            "route_cut_scope":
                "EXACT_FULL_HYPERPLANE_RECURRENCE_AND_REFINED_TOP_FIVE_COMPILER_ONLY",
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
            "Q147595_paid": False,
            "forty_five_unit_improvement_proved": False,
            "recurrence_cap_attained_by_source_family": False,
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
    lemma = data["fixed_mismatch_lemma"]
    endpoint = data["exact_endpoint"]
    residual = data["first_unresolved_head"]
    ledger = data["ledger_state"]
    require(lemma["counted_normalized_label_nonzero"] is True, "nonzero label")
    require(
        lemma["full_label_hyperplane_used"] is True,
        "full label hyperplane",
    )
    require(
        lemma["full_hyperplane_common_zero_is_fixed_mismatch"] is True,
        "fixed mismatch",
    )
    require(
        lemma["full_label_hyperplane_direction_rank"] == 6,
        "full hyperplane rank",
    )
    require(lemma["alignment_assumption"] is False, "no alignment")
    require(
        endpoint["Q147594_refined"]["head_cap"] <= SHALLOW_TARGET,
        "endpoint paid",
    )
    require(
        endpoint["Q147594_refined"]["target_margin"] == 15,
        "endpoint margin",
    )
    require(
        residual["compiled"]["head_cap"] > SHALLOW_TARGET,
        "next head open",
    )
    require(residual["required_improvement"] == 45, "45-unit route cut")
    require(
        residual["forty_five_unit_improvement_proved"] is False,
        "45-unit theorem open",
    )
    require(ledger["ledger_movement"] == 0, "zero ledger movement")
    require(ledger["row_closed"] is False, "row open")
    require(
        [ledger[name] for name in ("U_Q", "U_list_int", "U_ext", "U_new")]
        == [None, None, None, None],
        "null atoms",
    )
    require(
        all(value is False for value in data["nonclaims"].values()),
        "nonclaims",
    )


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
            "zero counted label",
            mutate(
                template,
                ("fixed_mismatch_lemma", "counted_normalized_label_nonzero"),
                False,
            ),
        ),
        (
            "incomplete line",
            mutate(
                template,
                ("fixed_mismatch_lemma", "complete_projective_line_required"),
                False,
            ),
        ),
        (
            "missing exact lcm",
            mutate(
                template,
                (
                    "fixed_mismatch_lemma",
                    "exact_lcm_no_common_zero_on_ZP_required",
                ),
                False,
            ),
        ),
        (
            "wrong rank gate",
            mutate(
                template,
                (
                    "fixed_mismatch_lemma",
                    "full_label_hyperplane_direction_rank",
                ),
                5,
            ),
        ),
        (
            "common agreement admitted",
            mutate(
                template,
                (
                    "fixed_mismatch_lemma",
                    "full_hyperplane_common_zero_is_fixed_mismatch",
                ),
                False,
            ),
        ),
        (
            "erase full hyperplane",
            mutate(
                template,
                ("fixed_mismatch_lemma", "full_label_hyperplane_used"),
                False,
            ),
        ),
        (
            "padding margin",
            mutate(
                template,
                ("fixed_mismatch_lemma", "padding_margin"),
                PADDING_MARGIN - 1,
            ),
        ),
        (
            "rank-six cap",
            mutate(
                template,
                ("recurrence_certificate", "six_rank_six_caps", 0),
                9_806_437,
            ),
        ),
        (
            "recurrence hash",
            mutate(
                template,
                ("recurrence_certificate", "rank_six_sha256"),
                "0" * 64,
            ),
        ),
        (
            "endpoint numerator",
            mutate(
                template,
                (
                    "exact_endpoint",
                    "Q147594_refined",
                    "objective_numerator",
                ),
                3_271_578_292_167,
            ),
        ),
        (
            "endpoint head",
            mutate(
                template,
                ("exact_endpoint", "Q147594_refined", "head_cap"),
                SHALLOW_TARGET + 1,
            ),
        ),
        (
            "tail loss",
            mutate(
                template,
                (
                    "exact_endpoint",
                    "Q147594_refined",
                    "exact_tail_partition",
                    "minimum_loss",
                ),
                87_135,
            ),
        ),
        (
            "survivor count",
            mutate(
                template,
                ("first_unresolved_head", "compiled", "survivor_count"),
                0,
            ),
        ),
        (
            "required improvement",
            mutate(
                template,
                ("first_unresolved_head", "required_improvement"),
                44,
            ),
        ),
        (
            "false closure",
            mutate(
                template,
                (
                    "first_unresolved_head",
                    "forty_five_unit_improvement_proved",
                ),
                True,
            ),
        ),
        (
            "ledger movement",
            mutate(template, ("ledger_state", "ledger_movement"), 1),
        ),
        (
            "row closure",
            mutate(template, ("ledger_state", "row_closed"), True),
        ),
        (
            "source hash",
            mutate(template, ("source_bindings", 0, "sha256"), "0" * 64),
        ),
        (
            "source traversal",
            mutate(template, ("source_bindings", 0, "path"), "../schema.json"),
        ),
        (
            "parent payload",
            mutate(
                template,
                ("source_bindings", 6, "internal_payload_sha256"),
                "0" * 64,
            ),
        ),
        (
            "rank6 parent payload",
            mutate(
                template,
                ("source_bindings", 8, "internal_payload_sha256"),
                "0" * 64,
            ),
        ),
        (
            "migration payload",
            mutate(
                template,
                ("source_bindings", 9, "internal_payload_sha256"),
                "0" * 64,
            ),
        ),
        (
            "payload hash",
            {**template, "payload_sha256": "0" * 64},
        ),
    ]
    for label, candidate in mutations:
        expect_rejected(label, candidate)
    print(
        "M31 rank7 fixed-mismatch hostile controls: "
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
                "M31 rank7 fixed-mismatch recurrence: "
                f"PASS ({CHECKS} checks)"
            )
        if args.tamper_selftest:
            tamper_selftest(template)
        if not (args.print_template or args.check or args.tamper_selftest):
            validate(strict_json(args.manifest))
            print(
                "M31 rank7 fixed-mismatch recurrence: "
                f"PASS ({CHECKS} checks)"
            )
    except (OSError, KeyError, TypeError, ValueError, VerificationError) as exc:
        print(
            f"M31 rank7 fixed-mismatch recurrence: FAIL: {exc}",
            file=sys.stderr,
        )
        raise SystemExit(1)


if __name__ == "__main__":
    main()
