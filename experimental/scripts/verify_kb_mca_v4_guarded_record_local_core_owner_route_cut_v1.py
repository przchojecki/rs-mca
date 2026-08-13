#!/usr/bin/env python3
"""Verify the guarded actual-record common-core owner route cut."""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import subprocess
from math import comb
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-v4-guarded-record-local-core-owner-route-cut-v1/manifest.json"
BASE_HEAD = "e26c15b2d2c2f98ae12dda17b97c40981f76e1ff"
P = 11
DOMAIN = tuple(range(1, 11))
K = 5
M = 7
W = M - K


class Reject(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in out, f"duplicate JSON key: {key}")
        out[key] = value
    return out


def strict_load(path: Path) -> Any:
    return json.loads(
        path.read_text(),
        object_pairs_hook=strict_pairs,
        parse_float=lambda value: (_ for _ in ()).throw(Reject(f"float {value}")),
        parse_constant=lambda value: (_ for _ in ()).throw(Reject(f"constant {value}")),
    )


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def payload_hash(value: dict[str, Any]) -> str:
    copy_value = copy.deepcopy(value)
    copy_value.pop("payload_sha256", None)
    return sha256(canonical_bytes(copy_value))


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def trim(poly: list[int] | tuple[int, ...]) -> tuple[int, ...]:
    out = [x % P for x in poly]
    while out and out[-1] == 0:
        out.pop()
    return tuple(out)


def degree(poly: tuple[int, ...]) -> int:
    return len(poly) - 1


def evaluate(poly: tuple[int, ...], x: int) -> int:
    value = 0
    for coefficient in reversed(poly):
        value = (value * x + coefficient) % P
    return value


def add(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return trim([
        (left[i] if i < len(left) else 0) + (right[i] if i < len(right) else 0)
        for i in range(max(len(left), len(right)))
    ])


def scale(poly: tuple[int, ...], scalar: int) -> tuple[int, ...]:
    return trim([scalar * x for x in poly])


def multiply(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    if not left or not right:
        return ()
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] = (out[i + j] + a * b) % P
    return trim(out)


def interpolate(points: tuple[int, ...], values: tuple[int, ...]) -> tuple[int, ...]:
    result: tuple[int, ...] = ()
    for i, (x_i, y_i) in enumerate(zip(points, values)):
        basis = (1,)
        denominator = 1
        for j, x_j in enumerate(points):
            if i == j:
                continue
            basis = multiply(basis, ((-x_j) % P, 1))
            denominator = denominator * (x_i - x_j) % P
        result = add(result, scale(basis, y_i * pow(denominator, -1, P)))
    return result


def locator(points: tuple[int, ...]) -> tuple[int, ...]:
    result = (1,)
    for point in points:
        result = multiply(result, ((-point) % P, 1))
    return result


def rank(matrix: list[list[int]]) -> int:
    a = [[x % P for x in row] for row in matrix]
    row = 0
    for column in range(len(a[0]) if a else 0):
        pivot = next((i for i in range(row, len(a)) if a[i][column]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        inverse = pow(a[row][column], -1, P)
        a[row] = [(inverse * x) % P for x in a[row]]
        for i in range(len(a)):
            if i != row and a[i][column]:
                factor = a[i][column]
                a[i] = [(x - factor * y) % P for x, y in zip(a[i], a[row])]
        row += 1
        if row == len(a):
            break
    return row


def shifted_minimum(word: tuple[int, ...]) -> int:
    for s in range(0, 6):
        columns = 2 * s + K + 1
        matrix = [
            [value * pow(x, j, P) % P for j in range(s + 1)]
            + [(-pow(x, j, P)) % P for j in range(s + K)]
            for x, value in zip(DOMAIN, word)
        ]
        if rank(matrix) < columns:
            return s
    raise Reject("shifted minimum not found")


FIXTURE = {
    "field": 11,
    "domain": list(DOMAIN),
    "k": 5,
    "m": 7,
    "w": 2,
    "critical_order": 6,
    "received_line": {
        "u": [0, 1, 4, 10, 9, 6, 9, 4, 3, 0],
        "v": [7, 2, 10, 7, 9, 5, 2, 2, 9, 3],
    },
    "explanations": [
        {"slope": 0, "coefficients": [4, 6, 8, 8, 2], "maximal_support": [2, 5, 6, 7, 8, 9, 10]},
        {"slope": 2, "coefficients": [10, 6, 10, 9, 1], "maximal_support": [1, 3, 5, 6, 7, 8, 10]},
        {"slope": 3, "coefficients": [7, 9, 1, 8, 7], "maximal_support": [1, 2, 3, 4, 8, 9, 10]},
        {"slope": 5, "coefficients": [0, 10, 2, 0, 1], "maximal_support": [1, 2, 5, 6, 8, 9, 10]},
        {"slope": 6, "coefficients": [8, 2, 3, 5, 3], "maximal_support": [2, 4, 5, 6, 8, 9, 10]},
        {"slope": 8, "coefficients": [10, 2, 2, 3, 6], "maximal_support": [1, 3, 5, 7, 8, 9, 10]},
        {"slope": 9, "coefficients": [4, 8, 0, 10, 8], "maximal_support": [1, 2, 4, 5, 6, 7, 10]},
    ],
}


PACKET_FILES = [
    "experimental/notes/thresholds/kb_mca_v4_guarded_record_local_core_owner_route_cut_v1.md",
    "experimental/data/certificates/kb-mca-v4-guarded-record-local-core-owner-route-cut-v1/README.md",
    "experimental/scripts/verify_kb_mca_v4_guarded_record_local_core_owner_route_cut_v1.py",
    "experimental/scripts/verify_kb_mca_v4_guarded_record_local_core_owner_route_cut_v1.sage",
    "experimental/scripts/verify_kb_mca_v4_guarded_record_local_core_owner_route_cut_v1_flint.py",
    "experimental/scripts/verify_kb_mca_v4_guarded_record_local_core_owner_route_cut_v1.wl",
]


def source_binding(identifier: str, path: str, blob: str, digest: str, role: str) -> dict[str, Any]:
    return {"id": identifier, "path": path, "git_blob_sha1": blob, "sha256": digest, "role": role}


def build_manifest() -> dict[str, Any]:
    manifest: dict[str, Any] = {
        "schema": "rs-mca-kb-v4-guarded-record-local-core-owner-route-cut-v1",
        "artifact_kind": "ACTUAL_GUARDED_RECORD_COLLISION_AND_ROUTE_CUT",
        "base": {"repository": "przchojecki/rs-mca", "exact_pr1163_head": BASE_HEAD, "upstream_main_at_refresh": "93fba1be3f3299b0ba4708d88715377bbb656e45"},
        "source_bindings": [
            source_binding("ACTIVE_V4", "experimental/grande_finale.tex", "5e0cb1bad6b40c4db39f6b4cb3e5316aebeafe2f", "03b8806c5e71ebd41a97012fbdcc6442dabd4c8bf9383b7d832a48b0c55ce5ab", "S_A_E_CHRONOLOGY"),
            source_binding("PR1163_STAIRCASE", "experimental/notes/thresholds/kb_mca_v4_common_core_shortening_staircase_route_cut_v1.md", "65a308ac97912de3dfe637d8a10a2f84e3a19c47", "d04dbe2dda570e3caf7b3380885d89e597762aa99c190bd305884bfc0fcd3cb6", "FIXED_CORE_ADAPTER_AND_WALLS"),
            source_binding("PR1160_TWO_ANCHOR", "experimental/notes/thresholds/kb_mca_supportwise_near_rational_two_anchor_repair_v1.md", "12bc4a0f06189829a9490928e4855d1aa958f940", "7e75d67420f4ed37add3b4f6ea3aa45e043a782a6396f328b1e34ce659938989", "SEPARATE_2W_OWNER"),
            source_binding("ALL_LINERAY_AFFINE_CORE", "experimental/notes/thresholds/all_lineray_affine_core_set_pair.md", "aa9674f669e411c1c48ad3879365947b9de77888", "b69eaeebff0e535936f145dbea0f2ef00dd8a5a3171d46a7f5dbb7cd2d77d60a", "SELECTOR_FREE_LOW_AFFINE_RANK_PAYMENT"),
        ],
        "external_provenance_not_imported": [
            {"commit": "83eefd94fd25fbe64f5fd1dc8d6766ccdcd7b41f", "role": "ORIGINAL_TWO_RECORD_FIXTURE_PROVENANCE_ONLY"},
            {"commit": "be4efd23a0eb226720b53fddadf4973f37441602", "role": "WHOLE_LINE_GLOBAL_CORE_ROUTER_PRIOR_PROVENANCE_ONLY"},
            {"commit": "d797d8ffd", "role": "NEGATIVE_BC_REGRESSION_PROVENANCE_ONLY"},
            {"commit": "fc74e16cd3f3acfa1030317e8d1636f492aca11f", "role": "STRONGER_NONEMPTY_CORE_COMPOSITION_PROVENANCE_ONLY"},
            {"commit": "67d17fff81130aed694ec2d1e7b8f6103e96a907", "role": "PR1156_LARGE_CLONE_CONTINUATION_OUT_OF_SCOPE"},
        ],
        "fixture": FIXTURE,
        "exact_results": {
            "displayed_slopes": 7,
            "critical_records": 7,
            "critical_core_histogram": [{"core": [8, 10], "records": 1}, {"core": [10], "records": 5}, {"core": [5, 10], "records": 1}],
            "global_core": [10],
            "shifted_minima": [3, 3, 3, 3, 3, 3, 3],
            "near_rational_threshold": 2,
            "all_outside_near_rational": True,
            "all_actual_degree_guarded": True,
            "global_affine": False,
            "record_local_core_is_slope_invariant": False,
            "lexicographic_complete_record_selector_total": True,
            "aggregate_selector_payment_proved": False,
        },
        "global_core_first_compiler": {
            "input": "ALREADY_DECLARED_FIRST_MATCH_SLOPE_SET_OF_SIZE_AT_LEAST_32_WITH_ONE_CANONICAL_COMPLETE_ACTUAL_RECORD_PER_SLOPE",
            "global_affine_terminal": "GLOBAL_AFFINE_PAID",
            "nonempty_global_core_uses_pr1163_once": True,
            "fixed_core_terminals": [
                "FIXED_CORE_GENERIC_PAID_s_LE_2",
                "DIRECTION_SEPARATED_PAID_3_LE_s_LE_13",
                "DIRECTION_LIST_SHORTENED_s",
                "COMMON_CORE_SHORTENED_s_GE_14",
            ],
            "empty_global_core_terminal": "EMPTY_GLOBAL_CORE_WITH_LOCAL_CRITICAL_CORES",
            "sums_over_record_local_cores": False,
            "fixture_s": 4,
            "fixture_terminal_without_direction_separation": "DIRECTION_LIST_SHORTENED_4",
            "aggregate_payment_for_all_terminals_proved": False,
        },
        "coherent_degree31_empty_core_fence": {
            "common_source_degree_Z_at_most": 31,
            "local_intersection_order": 32,
            "minimal_empty_cover_lower_bound": 33,
            "private_point_root_lower_bound": 32,
            "coherent_empty_global_core_possible": False,
            "empty_core_terminals": [
                "LOCAL_EMPTY_ORDER_32_CORE",
                "NONCOHERENT_DEGREE_31_SOURCE_FOREST",
            ],
            "line_global_source_coherence_proved_by_active_source": False,
            "sharp_control": {
                "field": 5,
                "source_degree": 3,
                "supports": 4,
                "local_intersection_order": 3,
            },
        },
        "overlap_source_change_ray_compiler": {
            "shared_slopes": 31,
            "source_degree_Z_at_most": 31,
            "difference_form": "H_PRIME_MINUS_H_EQUALS_P_X_TIMES_PRODUCT_OVER_SHARED_SLOPES",
            "quotient_independent_of_Z": True,
            "new_slope_scalar_nonzero": True,
            "same_actual_record_preserved": True,
            "printed_primitive_no_common_ray_bound": 1963173,
            "printed_bound_not_imported_for_local_common_core": True,
            "automatic_core": "P_X_ZERO_AND_E_X_Z_IDENTICALLY_ZERO",
            "one_canonical_rich_point_per_slope_before_cancellation": True,
            "automatic_core_may_be_strict_subset_of_maximal_support_intersection": True,
            "common_subset_cancellation_proved_directly": True,
            "does_not_invoke_pr1163_exact_core_statement": True,
            "shortened_dimension_q_le_2_terminal": "FIXED_CORE_GENERIC_PAID_s_LE_2",
            "guarded_shortened_ray_q_range": [3, 1048576],
            "guarded_shortened_ray_max_q": 3,
            "guarded_shortened_ray_max": 342921713716,
            "guarded_shortened_ray_slack": 274980385189681371,
            "guarded_shortened_ray_formula": "FLOOR((R+q)/q)*(t+1)+FLOOR(31*C(R+q,2)/XI(d+q,q-1))",
            "aggregate_direction_payment_proved": False,
            "residual": "MULTIPLE_NONCOHERENT_CORRECTION_RAY_DIRECTIONS",
        },
        "all_lineray_low_rank_gate": {
            "objects_counted": "DISTINCT_ACTUAL_SLOPE_EXPLANATION_PAIRS",
            "one_complete_record_per_slope": True,
            "transversality_from_same_support_noncontainment": True,
            "residual_weight_t": 981104,
            "rank_caps": [
                {"affine_rank": 0, "cap": 1},
                {"affine_rank": 1, "cap": 981105},
                {"affine_rank": 2, "cap": 481284001065},
                {"affine_rank": 3, "cap": 157397034144292985},
            ],
            "largest_budget_fitting_rank": 3,
            "first_unpaid_rank": 4,
            "first_unpaid_cap": 38605872343809750481845,
            "earlier_disjoint_addback": 134975,
            "rank3_slack_after_addback": 117583693966967127,
            "residual": "HIGH_ALL_RAY_AFFINE_DIMENSION_AT_LEAST_4",
            "active_v4_ledger_movement": 0,
            "promotion_requires_source_and_independent_math_review": True,
        },
        "deployed_guard": {
            "B_star": 274980728111395087,
            "w": 67472,
            "near_rational_2w": 134944,
            "exception_reserve": 31,
            "charges_are_disjoint": True,
            "joint_charge": 134975,
            "remaining_after_both": 274980728111260112,
            "pr1160_d1_upper": 67471,
            "balanced_guard": 67472,
            "pr1160_terminal": "NEAR_RATIONAL_2W",
            "pr1160_enters_common_core_forest": False,
        },
        "terminal": {
            "label": "SEMANTIC_ROUTE_CUT_RECORD_LOCAL_CORE_OWNER_NONINVARIANCE",
            "weakest_repair": "DEGREE31_SOURCE_COHERENCE_ACROSS_31_OVERLAPS_OR_EXACT_OWNER_FOR_FIRST_PASSPORT_CHANGE",
            "U_S_movement": 0,
            "U_A_movement": 0,
            "U_E_movement": 0,
            "global_ledger_movement": 0,
            "KoalaBear_closed": False,
        },
        "packet_files": PACKET_FILES,
        "packet_file_sha256": {path: sha256((ROOT / path).read_bytes()) for path in PACKET_FILES},
    }
    manifest["payload_sha256"] = payload_hash(manifest)
    return manifest


def verify_sources(manifest: dict[str, Any]) -> None:
    for item in manifest["source_bindings"]:
        data = (ROOT / item["path"]).read_bytes()
        require(git_blob(data) == item["git_blob_sha1"], f"blob pin {item['id']}")
        require(sha256(data) == item["sha256"], f"sha pin {item['id']}")
        proc = subprocess.run(["git", "-C", str(ROOT), "show", f"{BASE_HEAD}:{item['path']}"], capture_output=True)
        require(proc.returncode == 0 and proc.stdout == data, f"exact head pin {item['id']}")


def verify_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    require(fixture == FIXTURE, "exact fixture")
    u = tuple(fixture["received_line"]["u"])
    v = tuple(fixture["received_line"]["v"])
    supports: dict[int, set[int]] = {}
    polynomials: dict[int, tuple[int, ...]] = {}
    minima = []
    seed_checks = 0
    for item in fixture["explanations"]:
        slope = item["slope"]
        poly = trim(item["coefficients"])
        word = tuple((a + slope * b) % P for a, b in zip(u, v))
        support = {x for x, value in zip(DOMAIN, word) if evaluate(poly, x) == value}
        require(support == set(item["maximal_support"]), f"maximal support {slope}")
        found: set[tuple[int, ...]] = set()
        for seed in itertools.combinations(DOMAIN, K):
            candidate = interpolate(seed, tuple(word[x - 1] for x in seed))
            if sum(evaluate(candidate, x) == value for x, value in zip(DOMAIN, word)) >= M:
                found.add(candidate)
            seed_checks += 1
        require(found == {poly}, f"unique explanation {slope}")
        ordered = tuple(sorted(support))
        u_poly = interpolate(ordered, tuple(u[x - 1] for x in ordered))
        v_poly = interpolate(ordered, tuple(v[x - 1] for x in ordered))
        require(degree(u_poly) >= K or degree(v_poly) >= K, f"same-support bad {slope}")
        d1 = shifted_minimum(word)
        require(d1 == W + 1, f"balanced d1 {slope}")
        complement = tuple(x for x in DOMAIN if x not in support)
        locator_poly = locator(complement)
        numerator = multiply(locator_poly, poly)
        s_k = max(degree(locator_poly), degree(numerator) - (K - 1))
        s_k1 = max(degree(locator_poly), degree(numerator) - K)
        require(s_k <= len(complement) and s_k1 <= s_k, f"degree guard {slope}")
        supports[slope] = support
        polynomials[slope] = tuple(item["coefficients"])
        minima.append(d1)

    slopes = tuple(sorted(supports))
    records = []
    core_counts: dict[tuple[int, ...], int] = {}
    memberships: dict[int, set[tuple[int, ...]]] = {slope: set() for slope in slopes}
    for record in itertools.combinations(slopes, fixture["critical_order"]):
        core = set(DOMAIN)
        for slope in record:
            core &= supports[slope]
        require(core, f"critical core {record}")
        core_tuple = tuple(sorted(core))
        core_counts[core_tuple] = core_counts.get(core_tuple, 0) + 1
        for slope in record:
            memberships[slope].add(core_tuple)
        records.append((record, core_tuple))
    require(core_counts == {(8, 10): 1, (10,): 5, (5, 10): 1}, "core histogram")
    require(all(len(values) >= 2 for values in memberships.values()), "every slope collides")
    require(sum(len(values) == 3 for values in memberships.values()) == 5, "five three-core slopes")
    global_core = set(DOMAIN)
    for support in supports.values():
        global_core &= support
    require(global_core == {10}, "global core")

    first, second = slopes[0], slopes[1]
    inverse = pow(second - first, -1, P)
    affine_direction = tuple((b - a) * inverse % P for a, b in zip(polynomials[first], polynomials[second]))
    affine = all(tuple((a + (slope - first) * d) % P for a, d in zip(polynomials[first], affine_direction)) == polynomials[slope] for slope in slopes)
    require(not affine, "non-global-affine")

    selected: dict[int, tuple[int, ...]] = {}
    for slope in slopes:
        selected_record = next(item for item in records if slope in item[0])
        selected[slope] = selected_record[1]
    require(set(selected) == set(slopes), "selector total")
    require(len(selected) == len(slopes), "selector no duplicate slope")
    return {"seed_checks": seed_checks, "records": len(records), "minima": minima}


def global_core_terminal(
    supports: list[set[int]], k: int, globally_affine: bool,
    direction_separated: bool,
) -> tuple[str, set[int], int | None]:
    require(bool(supports), "nonempty slope set")
    core = set.intersection(*supports)
    if globally_affine:
        return "GLOBAL_AFFINE_PAID", core, None
    if not core:
        return "EMPTY_GLOBAL_CORE_WITH_LOCAL_CRITICAL_CORES", core, None
    require(len(core) < k, "non-affine global core below k")
    s = k - len(core)
    if s <= 2:
        return "FIXED_CORE_GENERIC_PAID_s_LE_2", core, s
    if s <= 13 and direction_separated:
        return "DIRECTION_SEPARATED_PAID_3_LE_s_LE_13", core, s
    if s <= 13:
        return f"DIRECTION_LIST_SHORTENED_{s}", core, s
    return "COMMON_CORE_SHORTENED_s_GE_14", core, s


def verify_global_core_compiler(manifest: dict[str, Any]) -> None:
    supports = [set(item["maximal_support"]) for item in manifest["fixture"]["explanations"]]
    terminal, core, s = global_core_terminal(supports, K, False, False)
    require((terminal, core, s) == ("DIRECTION_LIST_SHORTENED_4", {10}, 4), "fixture global compiler")
    require(global_core_terminal([{1, 2, 3, 4}, {1, 2, 3, 5}], 4, False, False)[0] == "FIXED_CORE_GENERIC_PAID_s_LE_2", "generic paid control")
    require(global_core_terminal([{1, 2}, {1, 3}], 6, False, True)[0] == "DIRECTION_SEPARATED_PAID_3_LE_s_LE_13", "direction paid control")
    require(global_core_terminal([{1, 2}, {2, 3}], 20, False, False)[0] == "COMMON_CORE_SHORTENED_s_GE_14", "large-s residual control")
    require(global_core_terminal([{1}, {2}], 5, False, False)[0] == "EMPTY_GLOBAL_CORE_WITH_LOCAL_CRITICAL_CORES", "empty-core residual control")
    require(global_core_terminal([{1}, {2}], 5, True, False)[0] == "GLOBAL_AFFINE_PAID", "affine priority control")


def eval_poly(coefficients: list[int], value: int, p: int) -> int:
    total = 0
    for coefficient in reversed(coefficients):
        total = (total * value + coefficient) % p
    return total


def multiply_linear(coefficients: list[int], root: int, p: int) -> list[int]:
    result = [0] * (len(coefficients) + 1)
    for index, coefficient in enumerate(coefficients):
        result[index] = (result[index] - root * coefficient) % p
        result[index + 1] = (result[index + 1] + coefficient) % p
    return result


def verify_coherent_empty_core_fence(manifest: dict[str, Any]) -> None:
    fence = manifest["coherent_degree31_empty_core_fence"]
    degree = fence["common_source_degree_Z_at_most"]
    local_order = fence["local_intersection_order"]
    require(local_order == degree + 1, "degree/local-order boundary")
    require(fence["minimal_empty_cover_lower_bound"] == local_order + 1, "minimal-cover lower bound")
    require(fence["private_point_root_lower_bound"] == local_order, "private-point roots")
    require(fence["private_point_root_lower_bound"] > degree, "root contradiction")
    require(fence["coherent_empty_global_core_possible"] is False, "coherent empty core excluded")
    require(fence["empty_core_terminals"] == ["LOCAL_EMPTY_ORDER_32_CORE", "NONCOHERENT_DEGREE_31_SOURCE_FOREST"], "empty-core fence")

    # Sharp degree-three boundary control: four complements of singletons are
    # 3-wise intersecting with empty total intersection.  The private-point
    # error polynomial has the three off-diagonal labels as its exact roots.
    p = 5
    labels = list(range(4))
    universe = set(labels)
    supports = [universe - {index} for index in labels]
    require(not set.intersection(*supports), "sharp control empty global core")
    for chosen in itertools.combinations(supports, 3):
        require(bool(set.intersection(*chosen)), "sharp control 3-wise core")
    for index in labels:
        polynomial = [1]
        for other in labels:
            if other != index:
                polynomial = multiply_linear(polynomial, other, p)
        require(len(polynomial) - 1 == 3, "sharp control degree")
        for other in labels:
            expected_zero = other != index
            require((eval_poly(polynomial, other, p) == 0) == expected_zero, "sharp control roots")


def verify_overlap_ray_compiler(manifest: dict[str, Any]) -> None:
    compiler = manifest["overlap_source_change_ray_compiler"]
    require(compiler["shared_slopes"] == compiler["source_degree_Z_at_most"], "31-overlap degree")
    require(compiler["quotient_independent_of_Z"] is True, "constant quotient")
    require(compiler["new_slope_scalar_nonzero"] is True, "new-slope scalar")
    require(compiler["same_actual_record_preserved"] is True, "same record")
    require(compiler["printed_primitive_no_common_ray_bound"] == 1963173, "primitive ray bound")
    require(compiler["printed_bound_not_imported_for_local_common_core"] is True, "primitive hypothesis fence")
    require(compiler["one_canonical_rich_point_per_slope_before_cancellation"] is True, "distinct-slope selector")
    require(compiler["automatic_core_may_be_strict_subset_of_maximal_support_intersection"] is True, "automatic-core subset fence")
    require(compiler["common_subset_cancellation_proved_directly"] is True, "common-subset cancellation")
    require(compiler["does_not_invoke_pr1163_exact_core_statement"] is True, "#1163 interface fence")
    require(compiler["shortened_dimension_q_le_2_terminal"] == "FIXED_CORE_GENERIC_PAID_s_LE_2", "small-q terminal")
    require(compiler["aggregate_direction_payment_proved"] is False, "no aggregate promotion")

    # Degree-three analogue of the coefficientwise divisibility identity.
    # P has two X-coefficients; each coefficient difference is P_a L_J.
    p = 7
    shared = [0, 1, 2]
    new_slope = 3
    locator = [1]
    for label in shared:
        locator = multiply_linear(locator, label, p)
    direction = [2, 5]
    base = [[1, 4, 0, 2], [3, 1, 6, 0]]
    changed = [
        [(coefficient + direction[row] * locator[column]) % p for column, coefficient in enumerate(base[row])]
        for row in range(2)
    ]
    for label in shared:
        require(all(eval_poly(changed[row], label, p) == eval_poly(base[row], label, p) for row in range(2)), "overlap identity")
    scalar = eval_poly(locator, new_slope, p)
    require(scalar != 0, "new label outside overlap")
    require(all((eval_poly(changed[row], new_slope, p) - eval_poly(base[row], new_slope, p)) % p == scalar * direction[row] % p for row in range(2)), "ray image")

    R = 1048576
    d = 67472
    t = 981104
    best: tuple[int, int] = (-1, -1)
    for q in range(3, 1048577):
        n_short = R + q
        m_short = d + q
        part_cap = q - 1
        quotient, remainder = divmod(m_short, part_cap)
        heterogeneous_pairs = comb(m_short, 2) - quotient * comb(part_cap, 2) - comb(remainder, 2)
        require(heterogeneous_pairs > 0, "positive heterogeneous-pair denominator")
        ray_bound = (n_short // q) * (t + 1) + 31 * comb(n_short, 2) // heterogeneous_pairs
        if ray_bound > best[0]:
            best = (ray_bound, q)
    require(best == (342921713716, 3), "guarded shortened-ray maximum")
    require(compiler["guarded_shortened_ray_q_range"] == [3, 1048576], "guarded q range")
    require(compiler["guarded_shortened_ray_max_q"] == best[1], "guarded max q")
    require(compiler["guarded_shortened_ray_max"] == best[0], "guarded ray maximum")
    require(compiler["guarded_shortened_ray_slack"] == 274980728111395087 - best[0], "guarded ray slack")


def verify_all_lineray_gate(manifest: dict[str, Any]) -> None:
    gate = manifest["all_lineray_low_rank_gate"]
    t = gate["residual_weight_t"]
    expected = [{"affine_rank": rank, "cap": comb(t + rank, rank)} for rank in range(4)]
    require(gate["rank_caps"] == expected, "all-LineRay rank caps")
    require(gate["largest_budget_fitting_rank"] == 3, "all-LineRay last paid rank")
    require(gate["first_unpaid_rank"] == 4, "all-LineRay first unpaid rank")
    require(gate["first_unpaid_cap"] == comb(t + 4, 4), "all-LineRay first unpaid cap")
    require(gate["earlier_disjoint_addback"] == 134975, "all-LineRay earlier add-back")
    require(gate["rank3_slack_after_addback"] == 274980728111395087 - 134975 - comb(t + 3, 3), "all-LineRay rank3 slack")
    require(gate["rank_caps"][-1]["cap"] + gate["earlier_disjoint_addback"] <= 274980728111395087 < gate["first_unpaid_cap"] + gate["earlier_disjoint_addback"], "all-LineRay budget wall")
    require(gate["active_v4_ledger_movement"] == 0, "no unreviewed owner promotion")


def verify_manifest(manifest: dict[str, Any], check_hashes: bool = True) -> dict[str, Any]:
    expected = build_manifest()
    require(manifest == expected, "canonical manifest")
    require(manifest["payload_sha256"] == payload_hash(manifest), "payload hash")
    verify_sources(manifest)
    result = verify_fixture(manifest["fixture"])
    verify_global_core_compiler(manifest)
    verify_coherent_empty_core_fence(manifest)
    verify_overlap_ray_compiler(manifest)
    verify_all_lineray_gate(manifest)
    guard = manifest["deployed_guard"]
    require(guard["near_rational_2w"] == 2 * guard["w"], "2w")
    require(guard["joint_charge"] == guard["near_rational_2w"] + guard["exception_reserve"], "separate reserve")
    require(guard["remaining_after_both"] == guard["B_star"] - guard["joint_charge"], "reserve arithmetic")
    require(guard["pr1160_d1_upper"] < guard["balanced_guard"], "#1160 negative BC guard")
    require(manifest["terminal"]["global_ledger_movement"] == 0, "zero movement")
    if check_hashes:
        for path, digest in manifest["packet_file_sha256"].items():
            require(sha256((ROOT / path).read_bytes()) == digest, f"packet hash {path}")
    return result


def mutations() -> list[Callable[[dict[str, Any]], None]]:
    return [
        lambda d: d["fixture"]["received_line"]["u"].__setitem__(0, 1),
        lambda d: d["fixture"]["explanations"][0]["coefficients"].__setitem__(0, 5),
        lambda d: d["fixture"]["explanations"][0]["maximal_support"].__setitem__(0, 1),
        lambda d: d["exact_results"].__setitem__("global_core", []),
        lambda d: d["exact_results"].__setitem__("near_rational_threshold", 3),
        lambda d: d["exact_results"].__setitem__("aggregate_selector_payment_proved", True),
        lambda d: d["global_core_first_compiler"].__setitem__("sums_over_record_local_cores", True),
        lambda d: d["global_core_first_compiler"].__setitem__("fixture_s", 3),
        lambda d: d["global_core_first_compiler"].__setitem__("aggregate_payment_for_all_terminals_proved", True),
        lambda d: d["coherent_degree31_empty_core_fence"].__setitem__("common_source_degree_Z_at_most", 32),
        lambda d: d["coherent_degree31_empty_core_fence"].__setitem__("coherent_empty_global_core_possible", True),
        lambda d: d["coherent_degree31_empty_core_fence"]["empty_core_terminals"].__setitem__(1, "PAID"),
        lambda d: d["overlap_source_change_ray_compiler"].__setitem__("new_slope_scalar_nonzero", False),
        lambda d: d["overlap_source_change_ray_compiler"].__setitem__("printed_bound_not_imported_for_local_common_core", False),
        lambda d: d["overlap_source_change_ray_compiler"].__setitem__("one_canonical_rich_point_per_slope_before_cancellation", False),
        lambda d: d["overlap_source_change_ray_compiler"].__setitem__("automatic_core_may_be_strict_subset_of_maximal_support_intersection", False),
        lambda d: d["overlap_source_change_ray_compiler"].__setitem__("does_not_invoke_pr1163_exact_core_statement", False),
        lambda d: d["overlap_source_change_ray_compiler"].__setitem__("guarded_shortened_ray_max", 1963173),
        lambda d: d["overlap_source_change_ray_compiler"].__setitem__("aggregate_direction_payment_proved", True),
        lambda d: d["all_lineray_low_rank_gate"].__setitem__("largest_budget_fitting_rank", 4),
        lambda d: d["all_lineray_low_rank_gate"]["rank_caps"][3].__setitem__("cap", 1),
        lambda d: d["all_lineray_low_rank_gate"].__setitem__("active_v4_ledger_movement", 1),
        lambda d: d["deployed_guard"].__setitem__("near_rational_2w", 1),
        lambda d: d["deployed_guard"].__setitem__("charges_are_disjoint", False),
        lambda d: d["deployed_guard"].__setitem__("pr1160_enters_common_core_forest", True),
        lambda d: d["terminal"].__setitem__("global_ledger_movement", 7),
        lambda d: d["terminal"].__setitem__("KoalaBear_closed", True),
        lambda d: d["external_provenance_not_imported"][0].__setitem__("role", "IMPORTED_DEPENDENCY"),
    ]


def tamper_selftest(manifest: dict[str, Any]) -> int:
    caught = 0
    for mutation in mutations():
        changed = copy.deepcopy(manifest)
        mutation(changed)
        changed["payload_sha256"] = payload_hash(changed)
        try:
            verify_manifest(changed, check_hashes=False)
        except (Reject, KeyError, TypeError, ValueError):
            caught += 1
    require(caught == len(mutations()), "all mutations rejected")
    duplicate = MANIFEST.read_text().replace('"schema":', '"schema":"duplicate",\n  "schema":', 1)
    try:
        json.loads(duplicate, object_pairs_hook=strict_pairs)
    except Reject:
        caught += 1
    require(caught == len(mutations()) + 1, "duplicate key rejected")
    return caught


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if args.write:
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST.write_text(json.dumps(build_manifest(), indent=2) + "\n")
        print(f"WROTE {MANIFEST}")
        return
    manifest = strict_load(MANIFEST)
    result = verify_manifest(manifest)
    if args.tamper_selftest:
        caught = tamper_selftest(manifest)
        print(f"KB_MCA_V4_GUARDED_CORE_OWNER_TAMPER_PASS mutations={caught}/{caught}")
    else:
        print("KB_MCA_V4_GUARDED_CORE_OWNER_ROUTE_CUT_PASS "
              f"slopes=7 critical_records={result['records']} seed_checks={result['seed_checks']} "
              f"d1={result['minima']} ledger_movement=0")


if __name__ == "__main__":
    main()
