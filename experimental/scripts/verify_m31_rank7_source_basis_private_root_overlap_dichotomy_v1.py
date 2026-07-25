#!/usr/bin/env python3
"""Verify the M31 rank-seven source-basis overlap dichotomy."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections import deque
from math import ceil, comb
from pathlib import Path, PurePosixPath
from typing import Any


SCHEMA_ID = (
    "rs-mca-m31-rank7-source-basis-private-root-overlap-dichotomy-v1"
)
THEOREM_ID = (
    "M31_RANK7_SOURCE_BASIS_PRIVATE_ROOT_OVERLAP_DICHOTOMY_V1"
)
STATUS = (
    "PROVED_LOCAL_TWO_BRANCH_PAYMENT_HIGH_OVERLAP_ROUTE_CUT_Q147595_OPEN"
)

P_FIELD = 2**31 - 1
N = 2**21
K = 2**20
AGREEMENT = 1_116_023
RADIUS = N - AGREEMENT
W = AGREEMENT - K
G = 354_972
D = G - W
RESIDUAL_DIMENSION = 4_981
DIRECTION_RANK = 6
SOURCE_RANK = 7
RESIDUAL_DOMAIN = K + RESIDUAL_DIMENSION
RESIDUAL_AGREEMENT = W + RESIDUAL_DIMENSION
CURRENT_CHILD_CAP = 674_155
CURRENT_PARENT_CAP = 9_806_438
CLOSING_PARENT_CAP = 9_806_393
REQUIRED_PARENT_IMPROVEMENT = 45
REQUIRED_NUMERATOR_DEFICIT = 3_214_704
MAX_UNCLOSED_DEFICIT = REQUIRED_NUMERATOR_DEFICIT - 1
PRIVATE_ROOT_CLOSING_THRESHOLD = 29
MAX_UNCLOSED_PRIVATE_ROOTS = PRIVATE_ROOT_CLOSING_THRESHOLD - 1
PAIR_COUNT = comb(SOURCE_RANK, 2)

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "m31_rank7_source_basis_private_root_overlap_dichotomy_v1.schema.json"
)
VERIFIER_PATH = (
    ROOT
    / "experimental/scripts/"
    "verify_m31_rank7_source_basis_private_root_overlap_dichotomy_v1.py"
)
INDEPENDENT_PATH = (
    ROOT
    / "experimental/scripts/"
    "verify_m31_rank7_source_basis_private_root_overlap_dichotomy_v1_independent.py"
)
SAGE_PATH = (
    ROOT
    / "experimental/scripts/"
    "verify_m31_rank7_source_basis_private_root_overlap_dichotomy_v1.sage"
)
NOTE_PATH = (
    ROOT
    / "experimental/notes/thresholds/"
    "m31_rank7_source_basis_private_root_overlap_dichotomy_v1.md"
)
README_PATH = (
    ROOT
    / "experimental/data/certificates/"
    "m31-rank7-source-basis-private-root-overlap-dichotomy-v1/README.md"
)
DEFAULT_MANIFEST = README_PATH.with_name("manifest.json")
PARENT_MANIFEST = (
    ROOT
    / "experimental/data/certificates/"
    "m31-rank7-combined-domain-fixed-mismatch-recurrence-v1/manifest.json"
)
PARENT_PAYLOAD = (
    "7ba77dfa1f9e75c69e6e58ea8b084e10599252979425ad83bee97ee4a8961a00"
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


def payload_sha256(value: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(value)
    unsigned.pop("payload_sha256", None)
    return hashlib.sha256(canonical_bytes(unsigned)).hexdigest()


def seal(value: dict[str, Any]) -> dict[str, Any]:
    output = copy.deepcopy(value)
    output.pop("payload_sha256", None)
    output["payload_sha256"] = payload_sha256(output)
    return output


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
        output: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in output, f"duplicate JSON key: {key}")
            output[key] = value
        return output

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


def direct_cap(
    rank: int,
    dimension: int,
    excess: int,
) -> int:
    inner = (
        comb(K + rank - 1, rank - 1)
        // comb(excess + rank - 1, rank - 1)
    )
    cap = (K + dimension) * inner // (excess + dimension)
    denominator = (
        (excess + dimension) ** 2
        - (K + dimension) * (dimension - 1)
    )
    if denominator > 0:
        cap = min(
            cap,
            (K + dimension) * (excess + 1) // denominator,
        )
    return cap


def recurrence_arrays(
    maximum_dimension: int,
    excess: int,
) -> dict[int, list[int]]:
    """Replay the projective-line recurrence with a monotone window."""

    arrays: dict[int, list[int]] = {}
    rank_one = [0] * (maximum_dimension + 1)
    for dimension in range(1, maximum_dimension + 1):
        rank_one[dimension] = (K + dimension) // (excess + dimension)
    arrays[1] = rank_one

    for rank in range(2, DIRECTION_RANK + 1):
        child = arrays[rank - 1]
        current = child.copy()
        prefix_cap = -1
        window: deque[int] = deque()
        for dimension in range(rank, maximum_dimension + 1):
            added = dimension - 1
            prefix_cap = max(prefix_cap, child[added])
            while window and child[window[-1]] <= child[added]:
                window.pop()
            window.append(added)
            lower = dimension - (dimension - 1) // (rank - 1)
            while window and window[0] < lower:
                window.popleft()
            require(bool(window), "nonempty recurrence window")
            recurrence = (
                (dimension - 1) * prefix_cap
                + (K + 1) * child[window[0]]
            ) // (excess + dimension)
            current[dimension] = max(
                child[dimension],
                min(recurrence, direct_cap(rank, dimension, excess)),
            )
        arrays[rank] = current
    return arrays


def line_deficits(rank_five: list[int]) -> list[dict[str, int]]:
    baseline = rank_five[RESIDUAL_DIMENSION - 1]
    return [
        {
            "line_size": size,
            "child_dimension": RESIDUAL_DIMENSION - size,
            "child_cap": rank_five[RESIDUAL_DIMENSION - size],
            "numerator_deficit":
                size
                * (
                    baseline
                    - rank_five[RESIDUAL_DIMENSION - size]
                ),
        }
        for size in range(1, 12)
    ]


def unclosed_histograms(
    losses: dict[int, int],
) -> list[dict[str, Any]]:
    """Enumerate every non-singleton histogram below the closing deficit."""

    output: list[dict[str, Any]] = []
    for count_two in range(MAX_UNCLOSED_DEFICIT // losses[2] + 1):
        for count_three in range(
            MAX_UNCLOSED_DEFICIT // losses[3] + 1
        ):
            for count_four in range(
                MAX_UNCLOSED_DEFICIT // losses[4] + 1
            ):
                deficit = (
                    count_two * losses[2]
                    + count_three * losses[3]
                    + count_four * losses[4]
                )
                if deficit <= MAX_UNCLOSED_DEFICIT:
                    parts = (
                        [2] * count_two
                        + [3] * count_three
                        + [4] * count_four
                    )
                    numerator = (
                        RESIDUAL_DOMAIN * CURRENT_CHILD_CAP - deficit
                    )
                    output.append(
                        {
                            "non_singleton_line_sizes": sorted(
                                parts,
                                reverse=True,
                            ),
                            "singleton_line_count":
                                RESIDUAL_DOMAIN - sum(parts),
                            "numerator_deficit": deficit,
                            "additional_deficit_needed":
                                REQUIRED_NUMERATOR_DEFICIT - deficit,
                            "recurrence_cap":
                                numerator // RESIDUAL_AGREEMENT,
                            "recurrence_remainder":
                                numerator % RESIDUAL_AGREEMENT,
                        }
                    )
    return sorted(
        output,
        key=lambda item: (
            item["numerator_deficit"],
            item["non_singleton_line_sizes"],
        ),
    )


def build_template() -> dict[str, Any]:
    parent = strict_json(PARENT_MANIFEST)
    require(parent["payload_sha256"] == PARENT_PAYLOAD, "parent payload pin")
    require(payload_sha256(parent) == PARENT_PAYLOAD, "parent payload seal")

    zero_arrays = recurrence_arrays(RESIDUAL_DIMENSION, W)
    one_arrays = recurrence_arrays(RESIDUAL_DIMENSION - 1, W + 1)
    current_child = zero_arrays[5][RESIDUAL_DIMENSION - 1]
    current_numerator = RESIDUAL_DOMAIN * current_child
    current_denominator = RESIDUAL_AGREEMENT
    one_zero_cap = one_arrays[6][RESIDUAL_DIMENSION - 1]
    positive_zero_caps = [
        (
            direct_cap(
                DIRECTION_RANK,
                RESIDUAL_DIMENSION - zero_count,
                W + zero_count,
            ),
            zero_count,
        )
        for zero_count in range(
            1,
            RESIDUAL_DIMENSION - DIRECTION_RANK + 1,
        )
    ]
    maximum_positive_zero_cap, maximum_positive_zero_arg = max(
        positive_zero_caps
    )
    deficits = line_deficits(zero_arrays[5])
    loss_map = {
        item["line_size"]: item["numerator_deficit"]
        for item in deficits
    }
    histograms = unclosed_histograms(loss_map)
    large_line_losses = [
        (
            size
            * (
                current_child
                - zero_arrays[5][RESIDUAL_DIMENSION - size]
            ),
            size,
        )
        for size in range(
            5,
            RESIDUAL_DIMENSION - 5 + 1,
        )
    ]
    minimum_large_line_deficit, minimum_large_line_size = min(
        large_line_losses
    )

    minimum_degree_sum = (
        2 * G - MAX_UNCLOSED_PRIVATE_ROOTS
    )
    minimum_total_pair_overlap = minimum_degree_sum - G
    forced_pair_overlap = ceil(
        minimum_total_pair_overlap / PAIR_COUNT
    )

    require(current_child == CURRENT_CHILD_CAP, "rank-five child cap")
    require(
        current_numerator == 710_260_719_335,
        "current recurrence numerator",
    )
    require(current_denominator == 72_428, "current denominator")
    require(
        current_numerator // current_denominator == CURRENT_PARENT_CAP,
        "current parent cap",
    )
    require(
        current_numerator % current_denominator == 27_871,
        "current recurrence remainder",
    )
    require(one_zero_cap == 444_522, "one-zero recurrence cap")
    require(
        (maximum_positive_zero_cap, maximum_positive_zero_arg)
        == (444_522, 1),
        "all positive-zero direct caps",
    )
    require(loss_map[5] == 3_273_960, "five-line deficit")
    require(
        (minimum_large_line_deficit, minimum_large_line_size)
        == (3_273_960, 5),
        "all large-line deficits",
    )
    require(loss_map[5] >= REQUIRED_NUMERATOR_DEFICIT, "five-line closes")
    require(
        [
            (
                item["non_singleton_line_sizes"],
                item["singleton_line_count"],
                item["numerator_deficit"],
                item["additional_deficit_needed"],
                item["recurrence_cap"],
                item["recurrence_remainder"],
            )
            for item in histograms
        ]
        == [
            ([], 1_053_557, 0, 3_214_704, 9_806_438, 27_871),
            ([2], 1_053_555, 1_195_278, 2_019_426, 9_806_421, 63_869),
            ([3], 1_053_554, 1_906_755, 1_307_949, 9_806_412, 4_244),
            ([2, 2], 1_053_553, 2_390_556, 824_148, 9_806_405, 27_439),
            ([4], 1_053_553, 2_593_488, 621_216, 9_806_402, 41_791),
            ([3, 2], 1_053_552, 3_102_033, 112_671, 9_806_395, 40_242),
        ],
        "complete unclosed histogram list",
    )
    require(minimum_degree_sum == 709_916, "minimum degree sum")
    require(
        minimum_total_pair_overlap == 354_944,
        "total pair overlap",
    )
    require(forced_pair_overlap == 16_903, "forced pair overlap")

    result = {
        "schema": SCHEMA_ID,
        "theorem_id": THEOREM_ID,
        "architecture_id": THEOREM_ID,
        "status": STATUS,
        "row_contract": {
            "row": "Mersenne-31 list at 2^-100",
            "object": "LIST",
            "unit": "DISTINCT_CODEWORDS_PER_RECEIVED_WORD",
            "p": P_FIELD,
            "n": N,
            "K": K,
            "agreement": AGREEMENT,
            "radius": RADIUS,
            "w": W,
            "g": G,
            "d": D,
            "source_rank": SOURCE_RANK,
            "direction_rank": DIRECTION_RANK,
            "first_open_Q": 147_595,
            "residual_dimension": RESIDUAL_DIMENSION,
            "current_class_cap": CURRENT_PARENT_CAP,
            "closing_class_cap": CLOSING_PARENT_CAP,
            "required_class_improvement": REQUIRED_PARENT_IMPROVEMENT,
            "required_numerator_deficit": REQUIRED_NUMERATOR_DEFICIT,
        },
        "fixed_mismatch_branch": {
            "common_direction_zero_count_parameter": "z",
            "delete_fixed_mismatches_without_padding": True,
            "transformed_dimension": "k-z",
            "transformed_excess": "w+z",
            "z0_cap": CURRENT_PARENT_CAP,
            "z1_cap": one_zero_cap,
            "positive_z_direct_cap_maximum": maximum_positive_zero_cap,
            "positive_z_direct_cap_arg": maximum_positive_zero_arg,
            "positive_z_scan_range": [
                1,
                RESIDUAL_DIMENSION - DIRECTION_RANK,
            ],
            "z_above_scan_forces_rank_drop": True,
            "z1_margin_below_closing_cap":
                CLOSING_PARENT_CAP - one_zero_cap,
            "z_positive_paid": True,
            "z_positive_paid_reason":
                "exact all-z direct-Johnson scan; larger z forces rank drop",
        },
        "projective_deficit_branch": {
            "baseline_rank_five_child_cap": current_child,
            "baseline_coordinate_count": RESIDUAL_DOMAIN,
            "baseline_numerator": current_numerator,
            "agreement_denominator": current_denominator,
            "baseline_quotient": current_numerator // current_denominator,
            "baseline_remainder": current_numerator % current_denominator,
            "required_numerator_deficit": REQUIRED_NUMERATOR_DEFICIT,
            "largest_unclosed_deficit": MAX_UNCLOSED_DEFICIT,
            "line_deficits": deficits,
            "large_line_scan_range": [
                5,
                RESIDUAL_DIMENSION - 5,
            ],
            "minimum_large_line_deficit": minimum_large_line_deficit,
            "minimum_large_line_deficit_arg": minimum_large_line_size,
            "size_five_numerator":
                current_numerator - loss_map[5],
            "size_five_cap":
                (current_numerator - loss_map[5]) // current_denominator,
            "size_five_remainder":
                (current_numerator - loss_map[5]) % current_denominator,
            "line_size_five_closes": True,
            "complete_unclosed_non_singleton_histograms": histograms,
        },
        "source_basis_dichotomy": {
            "basis_size": SOURCE_RANK,
            "basis_members_are_actual_source_members": True,
            "arbitrary_linear_combination_basis_forbidden": True,
            "basis_locators_cover_master_denominator": True,
            "coverage_reason":
                "otherwise the full source span has a common zero on Z(P)",
            "private_root_evaluation":
                "scalar_multiple_of_coordinate_functional_e_i_star",
            "private_root_restriction_dichotomy":
                "common_direction_zero_or_nonzero_projective_axis_line",
            "z0_private_roots_form_axis_lines": True,
            "private_root_closing_threshold":
                PRIVATE_ROOT_CLOSING_THRESHOLD,
            "private_root_pigeonhole_denominator": SOURCE_RANK,
            "maximum_unclosed_private_roots":
                MAX_UNCLOSED_PRIVATE_ROOTS,
            "minimum_sum_basis_locator_degrees": minimum_degree_sum,
            "minimum_total_pairwise_locator_overlap":
                minimum_total_pair_overlap,
            "basis_locator_pair_count": PAIR_COUNT,
            "forced_pairwise_gcd_degree": forced_pair_overlap,
            "squarefree_split_locators_required": True,
            "individual_gcd_bi_Gi_required": True,
        },
        "remaining_terminal": {
            "name": "HIGH_PAIRWISE_MASTER_LOCATOR_OVERLAP",
            "condition": "exists i<j with deg gcd(G_i,G_j)>=16903",
            "paid_owner": None,
            "Q147595_closed": False,
            "next_exact_theorem":
                "route or eliminate the source-compatible high-overlap pair using cross-H/cross-cofactor equations",
        },
        "ledger_state": {
            "local_branch_reduction": True,
            "ledger_movement": 0,
            "official_endpoint_movement": 0,
            "U_paid": 3_730,
            "U_Q": None,
            "U_list_int": None,
            "U_ext": None,
            "U_new": None,
            "signed_Xi46_paid": False,
            "row_closed": False,
        },
        "nonclaims": {
            "Q147595_paid": False,
            "high_overlap_component_paid": False,
            "global_rank7_closed": False,
            "rank_at_least_8_treated": False,
            "v4_atom_paid": False,
            "row_upper_bound_proved": False,
            "recurrence_extremizer_realized": False,
            "stable_paper_modified": False,
            "lean_used": False,
        },
        "source_bindings": [
            source_binding("packet_schema", SCHEMA_PATH, "Closed schema."),
            source_binding("packet_verifier", VERIFIER_PATH, "Primary verifier."),
            source_binding(
                "independent_replay",
                INDEPENDENT_PATH,
                "Independent heap and combinatorial replay.",
            ),
            source_binding(
                "sage_replay",
                SAGE_PATH,
                "Sage exact arithmetic and finite-field source control.",
            ),
            source_binding("theorem_note", NOTE_PATH, "Proof and audit."),
            source_binding("packet_readme", README_PATH, "Replay contract."),
            source_binding(
                "fixed_mismatch_parent",
                PARENT_MANIFEST,
                "Sealed Q=147594 parent and Q=147595 residual.",
                PARENT_PAYLOAD,
            ),
        ],
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
            require(source["payload_sha256"] == internal, "internal payload")
            require(payload_sha256(source) == internal, "internal seal")


def validate_semantics(data: dict[str, Any]) -> None:
    fixed = data["fixed_mismatch_branch"]
    projective = data["projective_deficit_branch"]
    basis = data["source_basis_dichotomy"]
    terminal = data["remaining_terminal"]
    ledger = data["ledger_state"]
    require(fixed["z_positive_paid"] is True, "positive-z branch paid")
    require(
        fixed["z1_cap"] < data["row_contract"]["closing_class_cap"],
        "positive-z cap closes",
    )
    require(projective["line_size_five_closes"] is True, "five-line closes")
    require(
        len(projective["complete_unclosed_non_singleton_histograms"]) == 6,
        "six residual histograms including singleton extremizer",
    )
    require(
        basis["basis_members_are_actual_source_members"] is True,
        "actual source basis",
    )
    require(
        basis["arbitrary_linear_combination_basis_forbidden"] is True,
        "arbitrary basis forbidden",
    )
    require(
        basis["forced_pairwise_gcd_degree"] == 16_903,
        "forced high overlap",
    )
    require(terminal["paid_owner"] is None, "high overlap unpaid")
    require(terminal["Q147595_closed"] is False, "Q147595 open")
    require(ledger["ledger_movement"] == 0, "zero ledger movement")
    require(ledger["row_closed"] is False, "row open")
    require(
        all(value is False for value in data["nonclaims"].values()),
        "all nonclaims false",
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
    output = copy.deepcopy(data)
    cursor: Any = output
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value
    return seal(output)


def expect_rejected(label: str, candidate: dict[str, Any]) -> None:
    try:
        validate(candidate)
    except VerificationError:
        return
    raise VerificationError(f"mutation accepted: {label}")


def tamper_selftest(template: dict[str, Any]) -> None:
    mutations = [
        (
            "padding restored",
            mutate(
                template,
                ("fixed_mismatch_branch", "delete_fixed_mismatches_without_padding"),
                False,
            ),
        ),
        (
            "wrong one-zero cap",
            mutate(template, ("fixed_mismatch_branch", "z1_cap"), 444_523),
        ),
        (
            "wrong five-line deficit",
            mutate(
                template,
                (
                    "projective_deficit_branch",
                    "line_deficits",
                    4,
                    "numerator_deficit",
                ),
                3_273_959,
            ),
        ),
        (
            "missing histogram",
            mutate(
                template,
                (
                    "projective_deficit_branch",
                    "complete_unclosed_non_singleton_histograms",
                ),
                template["projective_deficit_branch"][
                    "complete_unclosed_non_singleton_histograms"
                ][:-1],
            ),
        ),
        (
            "arbitrary basis admitted",
            mutate(
                template,
                (
                    "source_basis_dichotomy",
                    "arbitrary_linear_combination_basis_forbidden",
                ),
                False,
            ),
        ),
        (
            "basis coverage erased",
            mutate(
                template,
                ("source_basis_dichotomy", "basis_locators_cover_master_denominator"),
                False,
            ),
        ),
        (
            "private root threshold",
            mutate(
                template,
                ("source_basis_dichotomy", "private_root_closing_threshold"),
                28,
            ),
        ),
        (
            "degree sum",
            mutate(
                template,
                ("source_basis_dichotomy", "minimum_sum_basis_locator_degrees"),
                709_915,
            ),
        ),
        (
            "pair overlap",
            mutate(
                template,
                ("source_basis_dichotomy", "forced_pairwise_gcd_degree"),
                16_902,
            ),
        ),
        (
            "force owner",
            mutate(
                template,
                ("remaining_terminal", "paid_owner"),
                "UNJUSTIFIED_OWNER",
            ),
        ),
        (
            "false Q closure",
            mutate(
                template,
                ("remaining_terminal", "Q147595_closed"),
                True,
            ),
        ),
        (
            "ledger movement",
            mutate(template, ("ledger_state", "ledger_movement"), 1),
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
            "payload hash",
            {**template, "payload_sha256": "0" * 64},
        ),
    ]
    for label, candidate in mutations:
        expect_rejected(label, candidate)
    print(
        "M31 rank7 source-basis overlap hostile controls: "
        f"PASS ({len(mutations)} mutations)"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--print-template", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        template = build_template()
        if args.write:
            args.manifest.parent.mkdir(parents=True, exist_ok=True)
            args.manifest.write_bytes(canonical_bytes(template))
            print(f"wrote {args.manifest}")
        if args.print_template:
            sys.stdout.buffer.write(canonical_bytes(template))
        if args.check:
            validate(strict_json(args.manifest))
            print(
                "M31 rank7 source-basis overlap dichotomy: "
                f"PASS ({CHECKS} checks)"
            )
        if args.tamper_selftest:
            tamper_selftest(template)
        if not (
            args.write
            or args.print_template
            or args.check
            or args.tamper_selftest
        ):
            validate(strict_json(args.manifest))
            print(
                "M31 rank7 source-basis overlap dichotomy: "
                f"PASS ({CHECKS} checks)"
            )
    except (OSError, KeyError, TypeError, ValueError, VerificationError) as exc:
        print(
            f"M31 rank7 source-basis overlap dichotomy: FAIL: {exc}",
            file=sys.stderr,
        )
        raise SystemExit(1)


if __name__ == "__main__":
    main()
