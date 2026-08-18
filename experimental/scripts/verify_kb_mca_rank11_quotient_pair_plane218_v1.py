#!/usr/bin/env python3
"""Verify the KoalaBear quotient-pair affine-plane cap and endpoint bank."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from math import comb, gcd
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / "experimental/data/certificates/kb-mca-rank11-quotient-pair-plane218-v1"
CONTRACT = CERT / "contract.json"
MANIFEST = CERT / "manifest.json"
CONTRACT_SHA256 = "86febeab22df67fdd0c55d92b4ac1503f8f33104f0e1615c8c84753bdcb81c6b"
SOURCE_FILES = {
    "background/nodes/rate_half_mca_rank11_pair_pencil_affine_plane_cap_218_sharpening/statement.md":
        "f17a18c39f68994c689f484a0d50f4b800f3187b615f4f09b5b4b27751cd52bf",
    "background/nodes/rate_half_mca_rank11_pair_pencil_affine_plane_cap_218_sharpening/proof.md":
        "d8a22ea247fa7e13dfba7c3bd2faa4f8dd537bcf340b2628599f8454777c7984",
    "background/nodes/rate_half_mca_rank11_pair_pencil_plane218_projective_direction_bank/statement.md":
        "aa62abc6626c36f03e81aa0e4a5497d7e19a08ebff079d7f4c4d02b4f7aef020",
    "background/nodes/rate_half_mca_rank11_pair_pencil_plane218_projective_direction_bank/proof.md":
        "44fc736822cdb6077c86a47f67a762840d211e2e05d643a969626aece784af90",
}
PURE_POWER_SOURCE_COMMIT = "b5e3a90d8415ea7de6c144d1fcd56c0e5c50b7d2"
PURE_POWER_SOURCE_FILES = {
    "background/nodes/rate_half_mca_rank11_pair_pencil_plane218_pure_power_router/statement.md":
        "4a35eb89713755612d897b8217941a6edb71029a2e92b5d14dd5d8bd978cef31",
    "background/nodes/rate_half_mca_rank11_pair_pencil_plane218_pure_power_router/proof.md":
        "5985806e56c45b0730998d0a8703e238788b1de05ffbb7297270bb926d146a85",
}
RICH_PLANE_SOURCE_COMMIT = "d79701f94add274e6c7fbf2f4744980d77817f4b"
RICH_PLANE_SOURCE_FILES = {
    "background/nodes/rate_half_mca_rank11_pair_pencil_dimension_three_rich_plane_recurrence_sharpening/statement.md":
        "58f549e620b401d1fedcd64c3c14a85dfcd1829657016c8080e14517cc2204a4",
    "background/nodes/rate_half_mca_rank11_pair_pencil_dimension_three_rich_plane_recurrence_sharpening/proof.md":
        "aa783aad6da1ff43f013d0bdedc3ea8c2259f50da18109309d92559f3c393a35",
}
PAIR_MOMENT_SOURCE_COMMIT = "473f41afc6b76d747e534cb8e509a0353dcde3aa"
PAIR_MOMENT_SOURCE_FILES = {
    "background/nodes/rate_half_mca_rank11_pair_pencil_dimension_three_pair_overlap_moment_floor/statement.md":
        "0e7fbd7184ade032eab32ffd96e803ca56195b827d26bcb1cfd61e161b6461f5",
    "background/nodes/rate_half_mca_rank11_pair_pencil_dimension_three_pair_overlap_moment_floor/proof.md":
        "171af5028580e011cfa7c30b6900fed5b30f3f2d6ebb2ea90ba276a74d7fcf7b",
}
TYPE_POPULATION_SOURCE_COMMIT = "1d52ff3013b6ab4e94f39cf9d6627f7562d65cf8"
TYPE_POPULATION_SOURCE_FILES = {
    "background/nodes/rate_half_mca_rank11_pair_pencil_dimension_three_type_population_ceiling/statement.md":
        "41cb9d67473a9e7cab38d75db9cee8dc55f01fb4e227ef177fb7c6ff0a0e5dac",
    "background/nodes/rate_half_mca_rank11_pair_pencil_dimension_three_type_population_ceiling/proof.md":
        "ab41ece43cb0df6023f87b516e02900f58229289b62bcbd67fff7e00925805bf",
}
ENDPOINT_PLANE_LINE_SOURCE_COMMIT = "f0a13cc6e33399aa8192bf4879b9a9e7941371e3"
ENDPOINT_PLANE_LINE_SOURCE_FILES = {
    "background/nodes/rate_half_mca_rank11_pair_pencil_dimension_three_population_endpoint_plane_line_design/statement.md":
        "262f4c39199716ca7123deefe25bc2f60c172babcb58987d80e2141701e78bf8",
    "background/nodes/rate_half_mca_rank11_pair_pencil_dimension_three_population_endpoint_plane_line_design/proof.md":
        "593886671c0aafebd34b3a0b84ef2e467a75181fde81a4d579a01df7df508db1",
}
ENDPOINT_DIRECTION_SOURCE_COMMIT = "1db90bbbef8c8e31b881de04dc9cedb387728c0f"
ENDPOINT_DIRECTION_SOURCE_FILES = {
    "background/nodes/rate_half_mca_rank11_pair_pencil_dimension_three_population_endpoint_direction_saturation/statement.md":
        "8bdec6b57c712da9f595f233bdf9ce2b06a09cf406fe86641d05da463ea59e3e",
    "background/nodes/rate_half_mca_rank11_pair_pencil_dimension_three_population_endpoint_direction_saturation/proof.md":
        "65d46ff0e58d738c988d88fd3369272425deeb49e2b2db87a38d3f142e182805",
}
PROJECTIVE_IMAGE_SOURCE_COMMIT = "121e75fa14d2b58968ca398f352437e1357b16fb"
PROJECTIVE_IMAGE_SOURCE_FILES = {
    "background/nodes/rate_half_mca_rank11_pair_pencil_dimension_three_projective_image_degree_router/statement.md":
        "be0921587aac16e2342dd1bdbce9edcb027733744426531e8bb5dad180e4fc01",
    "background/nodes/rate_half_mca_rank11_pair_pencil_dimension_three_projective_image_degree_router/proof.md":
        "8e3a9c40daea14f95ca8f7254c89ee673a53f7794fd718fe0adf5b77aced9cb0",
}


class Reject(ValueError):
    """A contract or provenance check failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def ceil_div(a: int, b: int) -> int:
    return -(-a // b)


def choose2(x: int) -> int:
    return x * (x - 1) // 2


def check_manifest() -> None:
    manifest = json.loads(MANIFEST.read_text())
    require(manifest.get("schema") == "kb-mca-rank11-quotient-pair-plane218-manifest-v1",
            "manifest schema")
    hashes = manifest.get("packet_file_sha256")
    require(isinstance(hashes, dict), "manifest hashes")
    for relative, expected in hashes.items():
        path = ROOT / relative
        require(path.is_file(), f"packet file {relative}")
        require(hashlib.sha256(path.read_bytes()).hexdigest() == expected,
                f"packet hash {relative}")


def check_source(source_root: Path, data: dict[str, Any]) -> None:
    source_root = source_root.resolve()
    provenance = data["provenance"]
    commit = provenance["commit"]
    head = subprocess.run(
        ["git", "rev-parse", commit],
        cwd=source_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    require(head == commit, "source commit")
    for path, expected in SOURCE_FILES.items():
        payload = subprocess.run(
            ["git", "show", f"{commit}:{path}"],
            cwd=source_root,
            check=True,
            capture_output=True,
        ).stdout
        require(hashlib.sha256(payload).hexdigest() == expected, f"source hash {path}")
    trees = {
        "plane_cap_node_tree":
            "background/nodes/rate_half_mca_rank11_pair_pencil_affine_plane_cap_218_sharpening",
        "direction_bank_node_tree":
            "background/nodes/rate_half_mca_rank11_pair_pencil_plane218_projective_direction_bank",
    }
    for key, path in trees.items():
        tree = subprocess.run(
            ["git", "rev-parse", f"{commit}:{path}"],
            cwd=source_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        require(tree == provenance[key], f"source tree {key}")

    extension_commit = provenance["pure_power_router_commit"]
    require(extension_commit == PURE_POWER_SOURCE_COMMIT, "extension source commit")
    extension_head = subprocess.run(
        ["git", "rev-parse", extension_commit],
        cwd=source_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    require(extension_head == extension_commit, "extension source commit resolution")
    for path, expected in PURE_POWER_SOURCE_FILES.items():
        payload = subprocess.run(
            ["git", "show", f"{extension_commit}:{path}"],
            cwd=source_root,
            check=True,
            capture_output=True,
        ).stdout
        require(hashlib.sha256(payload).hexdigest() == expected,
                f"extension source hash {path}")
    extension_tree = subprocess.run(
        ["git", "rev-parse",
         f"{extension_commit}:background/nodes/rate_half_mca_rank11_pair_pencil_plane218_pure_power_router"],
        cwd=source_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    require(extension_tree == provenance["pure_power_router_node_tree"],
            "extension source tree")

    rich_commit = provenance["dimension_three_rich_plane_commit"]
    require(rich_commit == RICH_PLANE_SOURCE_COMMIT, "rich-plane source commit")
    rich_head = subprocess.run(
        ["git", "rev-parse", rich_commit],
        cwd=source_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    require(rich_head == rich_commit, "rich-plane source commit resolution")
    for path, expected in RICH_PLANE_SOURCE_FILES.items():
        payload = subprocess.run(
            ["git", "show", f"{rich_commit}:{path}"],
            cwd=source_root,
            check=True,
            capture_output=True,
        ).stdout
        require(hashlib.sha256(payload).hexdigest() == expected,
                f"rich-plane source hash {path}")
    rich_tree = subprocess.run(
        ["git", "rev-parse",
         f"{rich_commit}:background/nodes/rate_half_mca_rank11_pair_pencil_dimension_three_rich_plane_recurrence_sharpening"],
        cwd=source_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    require(rich_tree == provenance["dimension_three_rich_plane_node_tree"],
            "rich-plane source tree")

    moment_commit = provenance["dimension_three_pair_moment_commit"]
    require(moment_commit == PAIR_MOMENT_SOURCE_COMMIT, "pair-moment source commit")
    moment_head = subprocess.run(
        ["git", "rev-parse", moment_commit],
        cwd=source_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    require(moment_head == moment_commit, "pair-moment source commit resolution")
    for path, expected in PAIR_MOMENT_SOURCE_FILES.items():
        payload = subprocess.run(
            ["git", "show", f"{moment_commit}:{path}"],
            cwd=source_root,
            check=True,
            capture_output=True,
        ).stdout
        require(hashlib.sha256(payload).hexdigest() == expected,
                f"pair-moment source hash {path}")
    moment_tree = subprocess.run(
        ["git", "rev-parse",
         f"{moment_commit}:background/nodes/rate_half_mca_rank11_pair_pencil_dimension_three_pair_overlap_moment_floor"],
        cwd=source_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    require(moment_tree == provenance["dimension_three_pair_moment_node_tree"],
            "pair-moment source tree")

    population_commit = provenance["dimension_three_type_population_commit"]
    require(population_commit == TYPE_POPULATION_SOURCE_COMMIT,
            "type-population source commit")
    population_head = subprocess.run(
        ["git", "rev-parse", population_commit],
        cwd=source_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    require(population_head == population_commit,
            "type-population source commit resolution")
    for path, expected in TYPE_POPULATION_SOURCE_FILES.items():
        payload = subprocess.run(
            ["git", "show", f"{population_commit}:{path}"],
            cwd=source_root,
            check=True,
            capture_output=True,
        ).stdout
        require(hashlib.sha256(payload).hexdigest() == expected,
                f"type-population source hash {path}")
    population_tree = subprocess.run(
        ["git", "rev-parse",
         f"{population_commit}:background/nodes/rate_half_mca_rank11_pair_pencil_dimension_three_type_population_ceiling"],
        cwd=source_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    require(population_tree == provenance["dimension_three_type_population_node_tree"],
            "type-population source tree")

    endpoint_sources = (
        ("dimension_three_endpoint_plane_line_commit",
         "dimension_three_endpoint_plane_line_node_tree",
         ENDPOINT_PLANE_LINE_SOURCE_COMMIT,
         ENDPOINT_PLANE_LINE_SOURCE_FILES,
         "background/nodes/rate_half_mca_rank11_pair_pencil_dimension_three_population_endpoint_plane_line_design",
         "endpoint-plane-line"),
        ("dimension_three_endpoint_direction_commit",
         "dimension_three_endpoint_direction_node_tree",
         ENDPOINT_DIRECTION_SOURCE_COMMIT,
         ENDPOINT_DIRECTION_SOURCE_FILES,
         "background/nodes/rate_half_mca_rank11_pair_pencil_dimension_three_population_endpoint_direction_saturation",
         "endpoint-direction"),
        ("dimension_three_projective_image_commit",
         "dimension_three_projective_image_node_tree",
         PROJECTIVE_IMAGE_SOURCE_COMMIT,
         PROJECTIVE_IMAGE_SOURCE_FILES,
         "background/nodes/rate_half_mca_rank11_pair_pencil_dimension_three_projective_image_degree_router",
         "projective-image"),
    )
    for commit_key, tree_key, expected_commit, files, directory, label in endpoint_sources:
        commit = provenance[commit_key]
        require(commit == expected_commit, f"{label} source commit")
        resolved = subprocess.run(
            ["git", "rev-parse", commit], cwd=source_root, check=True,
            capture_output=True, text=True,
        ).stdout.strip()
        require(resolved == commit, f"{label} source commit resolution")
        for path, expected in files.items():
            payload = subprocess.run(
                ["git", "show", f"{commit}:{path}"], cwd=source_root,
                check=True, capture_output=True,
            ).stdout
            require(hashlib.sha256(payload).hexdigest() == expected,
                    f"{label} source hash {path}")
        tree = subprocess.run(
            ["git", "rev-parse", f"{commit}:{directory}"], cwd=source_root,
            check=True, capture_output=True, text=True,
        ).stdout.strip()
        require(tree == provenance[tree_key], f"{label} source tree")


def validate(raw: object) -> dict[str, int]:
    require(isinstance(raw, dict), "contract object")
    data: dict[str, Any] = raw
    require(data.get("schema") == "kb-mca-rank11-quotient-pair-plane218-v1", "schema")

    row = data.get("row")
    source = data.get("source_interface")
    cap = data.get("plane_cap")
    router = data.get("dimension_router")
    moment = data.get("pair_overlap_moment")
    population = data.get("type_population_router")
    endpoint = data.get("population_endpoint_design")
    image = data.get("projective_image_router")
    bank = data.get("endpoint_bank")
    power = data.get("pure_power_router")
    claims = data.get("claims")
    require(all(isinstance(x, dict) for x in
                (row, source, cap, router, moment, population, endpoint, image,
                 bank, power, claims)),
            "sections")

    n, K, m, s = row["n"], row["K"], row["m"], row["pair_core_size"]
    q, line = source["selected_types"], source["affine_line_cap"]
    require((row["p"], row["extension_degree"], n, K, m, s) ==
            (2130706433, 6, 2097152, 1048576, 1116048, m - 2), "row pins")
    require((q, source["scalar_span_dimension_ceiling"], line,
             source["selected_type_record_floor"], source["coprime_direction_normal_form"]) ==
            (520, 4, 15, 29, True), "source pins")

    excluded = cap["excluded_occupancy"]
    core = ceil_div(excluded * s - line * n, excluded - line)
    require((excluded, core, cap["common_core_floor"]) == (219, 1043906, 1043906), "cap core")
    kmax = K - core
    require(cap["shortened_K_ceiling"] == kmax == 4670, "cap K")
    f0, f1 = cap["full_coordinate_floor_constant"], cap["full_coordinate_floor_slope"]
    require((f0, f1) == (95866, 205), "cap full floor")
    line_ceiling = excluded * ((excluded - 1) // (line - 1)) // line
    require(cap["full_line_ceiling"] == line_ceiling == 219, "cap lines")
    margin = f0 + f1 * kmax - line_ceiling * (kmax - 1)
    require(cap["contradiction_margin_floor"] == margin == 30705, "cap margin")
    plane = excluded - 1
    require(cap["proved_occupancy_ceiling"] == plane == 218, "plane cap")

    common = ceil_div(q * s - plane * n, q - plane)
    require(router["dimension_three_core_floor"] == common == 407831, "dimension-three core")
    shortened = (n - common, K - common, m - common, s - common)
    require(shortened == (router["shortened_n"], router["shortened_K"],
                          router["shortened_m"], router["shortened_pair_core"]) ==
            (1689321, 640745, 708217, 708215), "dimension-three shortening")
    slack = plane * shortened[0] - q * shortened[3]
    require(router["incidence_slack"] == slack == 178, "dimension-three slack")
    rich_threshold = router["rich_plane_threshold"]
    require(rich_threshold == 189, "rich-plane threshold")
    require(3 * rich_threshold - 3 * line > q, "rich-plane obstruction")
    require(3 * (rich_threshold - 1) - 3 * line <= q,
            "rich-plane threshold adjacency")
    require(router["rich_plane_count_ceiling"] == 2, "rich-plane count")
    recurrence_offset = router["rich_plane_recurrence_offset"]
    require(recurrence_offset == 2, "rich-plane recurrence")
    low = rich_threshold - 1
    excess = plane - low
    n0, s0 = n - K, s - K
    rich_coefficient = excess * router["rich_plane_count_ceiling"]
    denominator = q - low - rich_coefficient
    numerator = low * n0 - q * s0 - rich_coefficient * recurrence_offset
    sharp_kmax, sharp_slack = divmod(numerator, denominator)
    require((denominator, numerator, sharp_kmax, sharp_slack) ==
            (272, 162047768, 595763, 232), "rich-plane ledger")
    sharp_common = K - sharp_kmax
    require(router["sharpened_dimension_three_core_floor"] ==
            sharp_common == 452813, "sharpened core")
    sharp_shortened = (n - sharp_common, K - sharp_common,
                       m - sharp_common, s - sharp_common)
    require(sharp_shortened ==
            (router["sharpened_shortened_n"], router["sharpened_shortened_K"],
             router["sharpened_shortened_m"],
             router["sharpened_shortened_pair_core"]) ==
            (1644339, 595763, 663235, 663233), "sharpened shortening")
    require(router["sharpened_incidence_slack"] == sharp_slack,
            "sharpened slack")
    require(router["adjacent_incidence_deficit"] ==
            denominator - sharp_slack == 40, "sharpened adjacency")
    require(router["dimension_four_heavy_type_floor"] == plane + 1 == 219, "heavy types")
    heavy_records = (plane + 1) * source["selected_type_record_floor"]
    require(router["dimension_four_heavy_record_floor"] == heavy_records == 6351, "heavy records")

    require((moment["residual_length_offset"], moment["residual_core_offset"],
             moment["pair_overlap_offset"]) == (1048576, 67470, 1),
            "pair-moment offsets")

    def pair_moment_gap(kprime: int) -> tuple[int, int]:
        residual_n = moment["residual_length_offset"] + kprime
        incidence = q * (moment["residual_core_offset"] + kprime)
        average, _ = divmod(incidence, residual_n)
        minimum = average * incidence - comb(average + 1, 2) * residual_n
        capacity = comb(q, 2) * (kprime - moment["pair_overlap_offset"])
        return capacity - minimum, average

    intervals = moment["average_floor_intervals"]
    require(intervals == [[3, 1167, 33], [1168, 3331, 34],
                          [3332, 4835, 35]], "pair-moment intervals")
    excluded_rows = 0
    for start, stop, expected_average in intervals:
        for kprime in range(start, stop + 1):
            gap, average = pair_moment_gap(kprime)
            require(average == expected_average, f"pair-moment average {kprime}")
            require(gap < 0, f"pair-moment excluded row {kprime}")
            excluded_rows += 1
    last = moment["last_excluded_residual_dimension"]
    first = moment["first_feasible_residual_dimension"]
    require((last, first, excluded_rows) == (4835, 4836, 4833),
            "pair-moment adjacent rows")
    last_gap, _ = pair_moment_gap(last)
    first_gap, _ = pair_moment_gap(first)
    require(last_gap == -moment["last_excluded_deficit"] == -2110,
            "pair-moment endpoint deficit")
    require(first_gap == moment["first_feasible_slack"] == 115260,
            "pair-moment adjacent slack")
    require(moment["residual_dimension_ceiling"] == sharp_kmax == 595763,
            "pair-moment ceiling")
    require(moment["common_core_floor"] == sharp_common == 452813,
            "pair-moment core floor")
    require(moment["common_core_ceiling"] == K - first == 1043740,
            "pair-moment core ceiling")
    payment_max = moment["shared_payment_residual_ceiling"]
    require(payment_max == 4922, "pair-moment payment threshold")
    require(moment["shared_payment_overlap_row_count"] ==
            payment_max - first + 1 == 87, "pair-moment payment overlap")
    require(moment["shared_payment_transport_proved"] is False,
            "pair-moment transport nonclaim")

    require(population["additional_hypothesis"] ==
            "COMPLETE_RETAINED_QUOTIENT_TYPE_FAMILY", "population hypothesis")
    require((population["retained_record_mass"], population["population_floor"],
             population["population_ceiling"]) == (255011043, 520, 3170),
            "population pins")

    def population_terms(types: int) -> tuple[int, int, int]:
        pair_cap = comb(plane, 2)
        coefficient = comb(types, 2) - (plane - 1) * types + pair_cap
        lower = ((plane - 1) * types * 67470 - pair_cap * 1048576
                 + comb(types, 2))
        upper = plane * 1048576 - types * 67470
        return coefficient, lower, upper

    def population_cross(types: int) -> int:
        coefficient, lower, upper = population_terms(types)
        return 2 * (coefficient * upper - lower * (types - plane))

    for types in range(520, 3388):
        factored = (-population["factor_constant"] * types * (types - plane)
                    * (population["factor_slope"] * types
                       - population["factor_intercept"]))
        require(population_cross(types) == factored,
                f"population factor {types}")
    require((population["factor_constant"], population["factor_slope"],
             population["factor_intercept"]) == (109, 619, 1962831),
            "population factor pins")
    qmax = population["population_ceiling"]
    last_cross = population_cross(qmax)
    first_cross = population_cross(qmax + 1)
    require(last_cross == population["last_feasible_cross_product_twice"] ==
            613022740560, "population last cross")
    require(first_cross == -population["first_excluded_cross_product_deficit_twice"] ==
            -18372095406, "population first cross")
    coefficient, lower, upper = population_terms(qmax)
    low_q, low_r = divmod(lower, coefficient)
    high_q, high_r = divmod(upper, qmax - plane)
    require((low_q, low_r, high_q, high_r) == (4959, 556785, 4982, 2804),
            "population endpoint divisions")
    require(population["endpoint_residual_dimension_floor"] == low_q + 1 == 4960,
            "population residual floor")
    require(population["endpoint_residual_dimension_ceiling"] == high_q == 4982,
            "population residual ceiling")
    full_floor = 1048576 + 4960 - (upper - (qmax - plane) * 4960)
    full_upper = 1048576 + 4982 - (upper - (qmax - plane) * 4982)
    require(population["endpoint_full_owner_coordinate_floor"] ==
            full_floor == 985788, "population full-owner floor")
    require(population["endpoint_upper_row_full_owner_coordinate_floor"] ==
            full_upper == 1050754, "population full-owner upper")
    dense = ceil_div(population["retained_record_mass"], qmax)
    require(population["dense_type_record_floor"] == dense == 80446,
            "population dense type")
    require(population["dense_type_paid"] is False, "population payment nonclaim")

    require((endpoint["type_population"], endpoint["residual_dimension_floor"],
             endpoint["residual_dimension_ceiling"],
             endpoint["full_owner_floor_constant"],
             endpoint["full_owner_floor_slope"],
             endpoint["plane_local_residual_dimension_floor"]) ==
            (3170, 4960, 4982, -13661092, 2953, 2044),
            "endpoint-design pins")
    endpoint_rows = []
    for kprime in range(4960, 4983):
        full = -13661092 + 2953 * kprime
        planes = ceil_div(full, kprime - 2044)
        marks = 218 * planes
        average = marks // 3170
        required_pairs = average * marks - comb(average + 1, 2) * 3170
        plane_gap = 15 * comb(planes, 2) - required_pairs
        saturated_pairs = comb(planes, 2) - plane_gap
        direction_roots = 210 * full
        direction_floor = ceil_div(direction_roots, kprime - 1)
        endpoint_rows.append((planes, saturated_pairs, direction_floor,
                              47836 * (kprime - 1) - direction_roots))
    require(min(item[0] for item in endpoint_rows) ==
            endpoint["distinct_plane_floor"] == 339, "endpoint plane floor")
    require(max(item[0] for item in endpoint_rows) ==
            endpoint["distinct_plane_ceiling_on_rows"] == 358,
            "endpoint plane ceiling")
    require(min(item[1] for item in endpoint_rows) ==
            endpoint["minimum_saturated_plane_pairs"] == 22752,
            "endpoint saturated pairs")
    require(endpoint["distinct_saturated_line_floor"] ==
            ceil_div(22752, comb(15, 2)) == 217, "endpoint saturated lines")
    require(endpoint["saturated_line_local_dimension_ceiling"] == 2609,
            "endpoint line local dimension")
    require(endpoint["saturated_line_residual_recurrence_floor"] ==
            4960 - 2609 == 2351, "endpoint line recurrence")
    require(endpoint["directions_per_full_plane_floor"] == 210,
            "endpoint internal directions")
    require(endpoint_rows[0][2] == endpoint["direction_population_floor"] == 41746,
            "endpoint direction floor")
    require(endpoint_rows[-1][2] ==
            endpoint["direction_population_upper_row_floor"] == 44301,
            "endpoint direction upper row")
    direction_ceiling = comb(3170, 2) // comb(15, 2)
    require(endpoint["direction_population_ceiling"] == direction_ceiling == 47836,
            "endpoint direction ceiling")
    require(max(item[3] for item in endpoint_rows) ==
            endpoint["aggregate_direction_degree_deficit_ceiling"] == 30203244,
            "endpoint direction deficit")
    saturation_num = 210 * 985788
    saturation_den = direction_ceiling * 4959
    saturation_gcd = gcd(saturation_num, saturation_den)
    require((endpoint["aggregate_saturation_numerator"],
             endpoint["aggregate_saturation_denominator"]) ==
            (saturation_num // saturation_gcd, saturation_den // saturation_gcd) ==
            (5750430, 6589409), "endpoint saturation")
    require(endpoint["endpoint_paid"] is False, "endpoint payment nonclaim")

    require((image["residual_dimension_floor"],
             image["residual_dimension_ceiling"],
             image["full_owner_floor_constant"],
             image["full_owner_floor_slope"],
             image["owner_multiplicity_ceiling"],
             image["occupancy_deficit_constant"],
             image["occupancy_deficit_slope"],
             image["raw_direction_root_offset"]) ==
            (4960, 4982, -13661092, 2953, 218, 14709668, -2952, 2609),
            "projective-image pins")
    image_rows = []
    for kprime in range(4960, 4983):
        full = -13661092 + 2953 * kprime
        occupancy_deficit = 14709668 - 2952 * kprime
        gcd_roots = occupancy_deficit // 218
        primitive_roots = kprime - 2609 - gcd_roots
        conic_e_max = (kprime - 1) // 2
        higher_e_max = (kprime - 1) // 3
        image_rows.append((gcd_roots, primitive_roots,
                           ceil_div(primitive_roots, 2),
                           ceil_div(full, conic_e_max),
                           higher_e_max,
                           ceil_div(full, higher_e_max)))
    require(image_rows[0] == (310, 2041, 1021, 398, 1653, 597),
            "projective-image first row")
    require(image_rows[-1] == (12, 2361, 1181, 422, 1660, 633),
            "projective-image last row")
    require((image["common_gcd_domain_root_ceiling_first_row"],
             image["common_gcd_domain_root_ceiling_last_row"],
             image["primitive_direction_root_floor_first_row"],
             image["primitive_direction_root_floor_last_row"]) ==
            (310, 12, 2041, 2361), "projective-image gcd/root rows")
    require((image["projective_image_degree_floor"],
             image["conic_map_degree_floor"],
             image["conic_map_degree_ceiling"],
             image["conic_normal_floor_first_row"],
             image["conic_normal_floor_last_row"]) ==
            (2, 1021, 2490, 398, 422), "projective-image conic branch")
    require((image["higher_image_degree_floor"],
             image["higher_image_map_degree_ceiling"],
             image["higher_image_normal_floor_first_row"],
             image["higher_image_normal_floor_last_row"]) ==
            (3, 1660, 597, 633), "projective-image higher branch")
    require(image["branches_paid"] is False, "projective-image payment nonclaim")

    endpoint = bank["plane_occupancy"]
    endpoint_core = ceil_div(endpoint * s - line * n, endpoint - line)
    require((endpoint, endpoint_core, bank["common_core_floor"]) == (218, 1043551, 1043551), "bank core")
    bank_kmax = K - endpoint_core
    require(bank["shortened_K_ceiling"] == bank_kmax == 5025, "bank K max")
    b0, b1 = bank["full_coordinate_floor_constant"], bank["full_coordinate_floor_slope"]
    require((b0, b1) == (28396, 204), "bank full floor")
    bank_lines = endpoint * ((endpoint - 1) // (line - 1)) // line
    require(bank["full_line_ceiling"] == bank_lines == 218, "bank lines")
    bank_kmin = ceil_div(b0 + bank_lines, bank_lines - b1)
    require(bank["shortened_K_floor"] == bank_kmin == 2044, "bank K min")
    require(bank["common_core_ceiling"] == K - bank_kmin == 1046532, "bank core max")

    max_deficit = 0
    min_directions = bank_lines
    for kprime in range(bank_kmin, bank_kmax + 1):
        full = b0 + b1 * kprime
        require(full <= bank_lines * (kprime - 1), f"endpoint feasibility {kprime}")
        directions = ceil_div(full, kprime - 1)
        require(directions >= 210, f"direction floor {kprime}")
        min_directions = min(min_directions, directions)
        max_deficit = max(max_deficit, bank_lines * (kprime - 1) - full)
    require(bank["projective_direction_floor"] == min_directions == 210, "direction floor")
    require(bank["aggregate_degree_deficit_ceiling"] == max_deficit == 41736, "degree deficit")

    full = b0 + b1 * bank_kmax
    total = bank_lines * (bank_kmax - 1)
    divisor = gcd(full, total)
    require((bank["saturation_numerator"], bank["saturation_denominator"]) ==
            (full // divisor, total // divisor) == (131687, 136904), "saturation")
    remaining_pairs = choose2(endpoint) - bank["dual_rich_point_floor"] * choose2(line)
    require(bank["dual_rich_point_floor"] == 210, "dual rich points")
    require(bank["dual_remaining_pair_ceiling"] == remaining_pairs == 1603, "dual pair budget")

    require(power["hypothesis"] == "PROJECTIVELY_EQUIVALENT_TO_XE_1", "power hypothesis")
    require(power["domain_order"] == n, "power domain")
    feasible: dict[int, list[int]] = {}
    for exponent in range(22):
        e = 1 << exponent
        rows = [
            kprime for kprime in range(bank_kmin, bank_kmax + 1)
            if e <= kprime - 1 and b0 + b1 * kprime <= bank_lines * e
        ]
        if rows:
            feasible[e] = rows
    require(list(feasible) == power["surviving_degrees"] == [2048, 4096],
            "power degrees")
    cases = power["cases"]
    require((min(feasible[2048]), max(feasible[2048]), len(feasible[2048])) ==
            (2049, 2049, 1), "power 2048 rows")
    full_2048 = b0 + b1 * 2049
    require(cases["2048"] == {
        "shortened_K_floor": 2049,
        "shortened_K_ceiling": 2049,
        "projective_direction_floor": 218,
        "full_line_count": 218,
        "missing_slot_ceiling": 72,
    }, "power 2048 case")
    require((ceil_div(full_2048, 2048), bank_lines * 2048 - full_2048) ==
            (218, 72), "power 2048 arithmetic")
    require((min(feasible[4096]), max(feasible[4096]), len(feasible[4096])) ==
            (4097, 4237, 141), "power 4096 rows")
    direction_4096 = min(ceil_div(b0 + b1 * kprime, 4096)
                         for kprime in feasible[4096])
    missing_4096 = max(bank_lines * 4096 - (b0 + b1 * kprime)
                       for kprime in feasible[4096])
    require(cases["4096"] == {
        "shortened_K_floor": 4097,
        "shortened_K_ceiling": 4237,
        "projective_direction_floor": 211,
        "duplicate_line_ceiling": 7,
        "missing_slot_ceiling": 28744,
    }, "power 4096 case")
    require((direction_4096, bank_lines - direction_4096, missing_4096) ==
            (211, 7, 28744), "power 4096 arithmetic")

    require(claims["source_interface_proved_here"] is False, "source nonclaim")
    require(claims["endpoint_excluded"] is False, "endpoint nonclaim")
    require(claims["endpoint_pure_power_proved"] is False, "power-form nonclaim")
    require(claims["pure_power_survivors_paid"] is False, "power-payment nonclaim")
    require(claims["shared_pair_core_payment_transported"] is False,
            "shared-core transport nonclaim")
    require(claims["dense_quotient_type_paid"] is False,
            "dense-type payment nonclaim")
    require(claims["population_endpoint_paid"] is False,
            "population-endpoint payment nonclaim")
    require(claims["projective_image_branches_paid"] is False,
            "projective-image payment nonclaim")
    require(claims["rank11_paid"] is False, "rank11 nonclaim")
    require(claims["active_v4_ledger_movement"] == 0, "ledger nonclaim")
    require(claims["KoalaBear_closed"] is False, "row nonclaim")
    return {"plane": plane, "core": sharp_common, "margin": margin,
            "directions": min_directions, "deficit": max_deficit,
            "power_degrees": len(feasible), "moment_first": first,
            "moment_rows": excluded_rows, "population_max": qmax,
            "dense": dense, "endpoint_directions": endpoint_rows[0][2],
            "primitive_roots": image_rows[0][1],
            "higher_normals": image_rows[0][5]}


def tamper_selftest(data: dict[str, Any]) -> int:
    mutations = (
        lambda x: x["row"].__setitem__("pair_core_size", 1116045),
        lambda x: x["source_interface"].__setitem__("affine_line_cap", 16),
        lambda x: x["plane_cap"].__setitem__("common_core_floor", 1043905),
        lambda x: x["plane_cap"].__setitem__("full_line_ceiling", 220),
        lambda x: x["plane_cap"].__setitem__("contradiction_margin_floor", 30704),
        lambda x: x["dimension_router"].__setitem__("dimension_three_core_floor", 407830),
        lambda x: x["dimension_router"].__setitem__("rich_plane_threshold", 188),
        lambda x: x["dimension_router"].__setitem__("rich_plane_count_ceiling", 3),
        lambda x: x["dimension_router"].__setitem__("sharpened_dimension_three_core_floor", 452812),
        lambda x: x["dimension_router"].__setitem__("adjacent_incidence_deficit", 39),
        lambda x: x["dimension_router"].__setitem__("dimension_four_heavy_record_floor", 6350),
        lambda x: x["pair_overlap_moment"].__setitem__("last_excluded_deficit", 2109),
        lambda x: x["pair_overlap_moment"].__setitem__("first_feasible_residual_dimension", 4835),
        lambda x: x["pair_overlap_moment"].__setitem__("average_floor_intervals", [[3, 1167, 33]]),
        lambda x: x["pair_overlap_moment"].__setitem__("common_core_ceiling", 1043739),
        lambda x: x["pair_overlap_moment"].__setitem__("shared_payment_overlap_row_count", 86),
        lambda x: x["pair_overlap_moment"].__setitem__("shared_payment_transport_proved", True),
        lambda x: x["type_population_router"].__setitem__("population_ceiling", 3171),
        lambda x: x["type_population_router"].__setitem__("dense_type_record_floor", 80445),
        lambda x: x["type_population_router"].__setitem__("endpoint_residual_dimension_floor", 4959),
        lambda x: x["type_population_router"].__setitem__("endpoint_full_owner_coordinate_floor", 985787),
        lambda x: x["type_population_router"].__setitem__("first_excluded_cross_product_deficit_twice", 18372095405),
        lambda x: x["type_population_router"].__setitem__("dense_type_paid", True),
        lambda x: x["population_endpoint_design"].__setitem__("distinct_plane_floor", 338),
        lambda x: x["population_endpoint_design"].__setitem__("minimum_saturated_plane_pairs", 22751),
        lambda x: x["population_endpoint_design"].__setitem__("distinct_saturated_line_floor", 216),
        lambda x: x["population_endpoint_design"].__setitem__("saturated_line_residual_recurrence_floor", 2350),
        lambda x: x["population_endpoint_design"].__setitem__("direction_population_floor", 41745),
        lambda x: x["population_endpoint_design"].__setitem__("direction_population_ceiling", 47837),
        lambda x: x["population_endpoint_design"].__setitem__("aggregate_direction_degree_deficit_ceiling", 30203243),
        lambda x: x["population_endpoint_design"].__setitem__("endpoint_paid", True),
        lambda x: x["projective_image_router"].__setitem__("owner_multiplicity_ceiling", 217),
        lambda x: x["projective_image_router"].__setitem__("occupancy_deficit_constant", 14709667),
        lambda x: x["projective_image_router"].__setitem__("common_gcd_domain_root_ceiling_first_row", 309),
        lambda x: x["projective_image_router"].__setitem__("primitive_direction_root_floor_first_row", 2040),
        lambda x: x["projective_image_router"].__setitem__("conic_map_degree_floor", 1020),
        lambda x: x["projective_image_router"].__setitem__("higher_image_normal_floor_first_row", 596),
        lambda x: x["projective_image_router"].__setitem__("branches_paid", True),
        lambda x: x["endpoint_bank"].__setitem__("shortened_K_floor", 2043),
        lambda x: x["endpoint_bank"].__setitem__("projective_direction_floor", 209),
        lambda x: x["endpoint_bank"].__setitem__("aggregate_degree_deficit_ceiling", 41735),
        lambda x: x["endpoint_bank"].__setitem__("dual_remaining_pair_ceiling", 1604),
        lambda x: x["pure_power_router"].__setitem__("surviving_degrees", [1024, 2048, 4096]),
        lambda x: x["pure_power_router"]["cases"]["2048"].__setitem__("missing_slot_ceiling", 73),
        lambda x: x["pure_power_router"]["cases"]["4096"].__setitem__("shortened_K_ceiling", 4238),
        lambda x: x["pure_power_router"]["cases"]["4096"].__setitem__("missing_slot_ceiling", 28743),
        lambda x: x["claims"].__setitem__("rank11_paid", True),
    )
    caught = 0
    for mutate in mutations:
        altered = copy.deepcopy(data)
        mutate(altered)
        try:
            validate(altered)
        except (Reject, KeyError, TypeError, ValueError):
            caught += 1
    require(caught == len(mutations), "hostile mutations")
    return caught


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--source-root", type=Path)
    args = parser.parse_args()
    payload = CONTRACT.read_bytes()
    require(hashlib.sha256(payload).hexdigest() == CONTRACT_SHA256, "contract hash")
    check_manifest()
    data = json.loads(payload)
    result = validate(data)
    if args.source_root is not None:
        check_source(args.source_root, data)
    if args.tamper_selftest:
        print(f"KB_RANK11_QUOTIENT_PAIR_PLANE218_TAMPER_PASS mutations={tamper_selftest(data)}/47")
        return
    source = " checked" if args.source_root is not None else " skipped"
    print(
        "KB_RANK11_QUOTIENT_PAIR_PLANE218_PASS "
        f"cap={result['plane']} core={result['core']} margin={result['margin']} "
        f"directions={result['directions']} deficit={result['deficit']} "
        f"moment_first={result['moment_first']} moment_rows={result['moment_rows']} "
        f"qmax={result['population_max']} dense={result['dense']} "
        f"endpoint_directions={result['endpoint_directions']} "
        f"primitive_roots={result['primitive_roots']} "
        f"higher_normals={result['higher_normals']} "
        f"power_degrees={result['power_degrees']} source={source.strip()}"
    )


if __name__ == "__main__":
    main()
