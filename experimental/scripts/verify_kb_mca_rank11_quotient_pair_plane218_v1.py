#!/usr/bin/env python3
"""Verify the KoalaBear quotient-pair affine-plane cap and endpoint bank."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from math import gcd
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / "experimental/data/certificates/kb-mca-rank11-quotient-pair-plane218-v1"
CONTRACT = CERT / "contract.json"
MANIFEST = CERT / "manifest.json"
CONTRACT_SHA256 = "29eb6fcd3368331b419b2fcbde05f18baef61162f1852300ff584cbe1f6348ea"
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


def validate(raw: object) -> dict[str, int]:
    require(isinstance(raw, dict), "contract object")
    data: dict[str, Any] = raw
    require(data.get("schema") == "kb-mca-rank11-quotient-pair-plane218-v1", "schema")

    row = data.get("row")
    source = data.get("source_interface")
    cap = data.get("plane_cap")
    router = data.get("dimension_router")
    bank = data.get("endpoint_bank")
    power = data.get("pure_power_router")
    claims = data.get("claims")
    require(all(isinstance(x, dict) for x in
                (row, source, cap, router, bank, power, claims)), "sections")

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
    require(claims["rank11_paid"] is False, "rank11 nonclaim")
    require(claims["active_v4_ledger_movement"] == 0, "ledger nonclaim")
    require(claims["KoalaBear_closed"] is False, "row nonclaim")
    return {"plane": plane, "core": sharp_common, "margin": margin,
            "directions": min_directions, "deficit": max_deficit,
            "power_degrees": len(feasible)}


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
        print(f"KB_RANK11_QUOTIENT_PAIR_PLANE218_TAMPER_PASS mutations={tamper_selftest(data)}/20")
        return
    source = " checked" if args.source_root is not None else " skipped"
    print(
        "KB_RANK11_QUOTIENT_PAIR_PLANE218_PASS "
        f"cap={result['plane']} core={result['core']} margin={result['margin']} "
        f"directions={result['directions']} deficit={result['deficit']} "
        f"power_degrees={result['power_degrees']} source={source.strip()}"
    )


if __name__ == "__main__":
    main()
