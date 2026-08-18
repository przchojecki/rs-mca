#!/usr/bin/env python3
"""Independent integer replay for the quotient-pair plane-218 packet."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "experimental/data/certificates/kb-mca-rank11-quotient-pair-plane218-v1/contract.json"
CONTRACT_SHA256 = "0a8ac27dd3b25d7a280af7d04253f15b14a34ef5430328e5df17315f1b26829a"


def check(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def c2(value: int) -> int:
    return value * (value - 1) // 2


def first_integer_at_least(numerator: int, denominator: int) -> int:
    candidate = numerator // denominator
    if candidate * denominator < numerator:
        candidate += 1
    return candidate


def main() -> None:
    payload = CONTRACT.read_bytes()
    check(hashlib.sha256(payload).hexdigest() == CONTRACT_SHA256, "contract hash")
    data = json.loads(payload)
    row = data["row"]
    source = data["source_interface"]
    cap = data["plane_cap"]
    router = data["dimension_router"]
    moment = data["pair_overlap_moment"]
    population = data["type_population_router"]
    endpoint = data["population_endpoint_design"]
    bank = data["endpoint_bank"]
    power = data["pure_power_router"]

    n = row["n"]
    degree = row["K"]
    core_size = row["pair_core_size"]
    line_cap = source["affine_line_cap"]

    cap_rhs = 219 * core_size - line_cap * n
    c219 = cap["common_core_floor"]
    check((219 - line_cap) * (c219 - 1) < cap_rhs <= (219 - line_cap) * c219,
          "219-core ceiling identity")
    cap_k = degree - c219
    for kprime in range(1, cap_k + 1):
        full_floor = 95866 + 205 * kprime
        full_capacity = 219 * (kprime - 1)
        check(full_floor - full_capacity >= 30705, f"219 contradiction {kprime}")

    common_rhs = 520 * core_size - 218 * n
    common = router["dimension_three_core_floor"]
    check((520 - 218) * (common - 1) < common_rhs <= (520 - 218) * common,
          "dimension-three core ceiling identity")
    check(218 * router["shortened_n"] - 520 * router["shortened_pair_core"] == 178,
          "dimension-three incidence slack")
    check(router["dimension_four_heavy_record_floor"] == 219 * 29,
          "dimension-four record floor")
    check(3 * 188 - 3 * 15 <= 520 < 3 * 189 - 3 * 15,
          "rich-plane threshold")
    sharp_k = router["sharpened_shortened_K"]

    def rich_capacity(kprime: int) -> int:
        return 188 * (1048576 + kprime) + 60 * (kprime - 2)

    def rich_demand(kprime: int) -> int:
        return 520 * (67470 + kprime)

    check(sharp_k == 595763, "sharpened K")
    check(rich_capacity(sharp_k) - rich_demand(sharp_k) ==
          router["sharpened_incidence_slack"] == 232, "sharpened slack")
    check(rich_demand(sharp_k + 1) - rich_capacity(sharp_k + 1) ==
          router["adjacent_incidence_deficit"] == 40, "sharpened adjacency")
    check(degree - sharp_k == router["sharpened_dimension_three_core_floor"] == 452813,
          "sharpened common core")

    def pair_moment_gap(kprime: int) -> tuple[int, int]:
        slots = 1048576 + kprime
        marks = 520 * (67470 + kprime)
        low = marks // slots
        high_slots = marks - low * slots
        low_slots = slots - high_slots
        required = low_slots * low * (low - 1) // 2
        required += high_slots * (low + 1) * low // 2
        available = 520 * 519 // 2 * (kprime - 1)
        return available - required, low

    moment_rows = 0
    for kprime in range(3, 4836):
        gap, _ = pair_moment_gap(kprime)
        check(gap < 0, f"pair-moment excluded row {kprime}")
        moment_rows += 1
    boundaries = ((3, 33), (1167, 33), (1168, 34), (3331, 34),
                  (3332, 35), (4835, 35), (4836, 35), (5505, 36))
    for kprime, expected_floor in boundaries:
        _, actual_floor = pair_moment_gap(kprime)
        check(actual_floor == expected_floor, f"pair-moment floor {kprime}")
    check(pair_moment_gap(4835)[0] == -moment["last_excluded_deficit"] == -2110,
          "pair-moment last deficit")
    check(pair_moment_gap(4836)[0] == moment["first_feasible_slack"] == 115260,
          "pair-moment first slack")
    check(moment_rows == 4833, "pair-moment scan size")
    check(moment["first_feasible_residual_dimension"] == 4836,
          "pair-moment first feasible")
    check(moment["residual_dimension_ceiling"] == sharp_k == 595763,
          "pair-moment upper endpoint")
    check(moment["common_core_floor"] == 452813 and
          moment["common_core_ceiling"] == 1043740,
          "pair-moment core interval")
    check(moment["shared_payment_overlap_row_count"] == 4922 - 4836 + 1 == 87,
          "pair-moment payment overlap")
    check(moment["shared_payment_transport_proved"] is False,
          "pair-moment payment nonclaim")

    def population_cross(types: int) -> int:
        coefficient = c2(types) - 217 * types + c2(218)
        lower = 217 * types * 67470 - c2(218) * 1048576 + c2(types)
        upper = 218 * 1048576 - types * 67470
        return 2 * (coefficient * upper - lower * (types - 218))

    population_rows = 0
    for types in range(520, 3388):
        factored = -109 * types * (types - 218) * (619 * types - 1962831)
        check(population_cross(types) == factored,
              f"type-population factor {types}")
        population_rows += 1
    check(population_cross(3170) ==
          population["last_feasible_cross_product_twice"] == 613022740560,
          "type-population last cross")
    check(population_cross(3171) ==
          -population["first_excluded_cross_product_deficit_twice"] == -18372095406,
          "type-population first cross")
    types = 3170
    coefficient = c2(types) - 217 * types + c2(218)
    lower = 217 * types * 67470 - c2(218) * 1048576 + c2(types)
    upper = 218 * 1048576 - types * 67470
    check(divmod(lower, coefficient) == (4959, 556785),
          "type-population lower division")
    check(divmod(upper, types - 218) == (4982, 2804),
          "type-population upper division")
    check(1048576 + 4960 - (upper - (types - 218) * 4960) ==
          population["endpoint_full_owner_coordinate_floor"] == 985788,
          "type-population full-owner floor")
    check((255011043 + 3169) // 3170 ==
          population["dense_type_record_floor"] == 80446,
          "type-population dense type")
    check(population["dense_type_paid"] is False,
          "type-population payment nonclaim")

    endpoint_rows = []
    direction_max = c2(3170) // c2(15)
    for kprime in range(4960, 4983):
        full = -13661092 + 2953 * kprime
        planes = first_integer_at_least(full, kprime - 2044)
        marks = 218 * planes
        low = marks // 3170
        high_points = marks - low * 3170
        required_pairs = (3170 - high_points) * c2(low)
        required_pairs += high_points * c2(low + 1)
        saturated_pairs = c2(planes) - (15 * c2(planes) - required_pairs)
        roots = 210 * full
        direction_floor = first_integer_at_least(roots, kprime - 1)
        deficit = direction_max * (kprime - 1) - roots
        endpoint_rows.append((planes, saturated_pairs, direction_floor, deficit))
    check(endpoint_rows[0] == (339, 22752, 41746, 30203244),
          "endpoint first row")
    check(endpoint_rows[-1] == (358, 27414, 44301, 17612776),
          "endpoint last row")
    check(min(item[1] for item in endpoint_rows) ==
          endpoint["minimum_saturated_plane_pairs"] == 22752,
          "endpoint saturated pairs")
    check(first_integer_at_least(22752, c2(15)) ==
          endpoint["distinct_saturated_line_floor"] == 217,
          "endpoint saturated lines")
    check(endpoint["saturated_line_residual_recurrence_floor"] == 2351,
          "endpoint line recurrence")
    check(direction_max == endpoint["direction_population_ceiling"] == 47836,
          "endpoint direction ceiling")
    check(Fraction(210 * 985788, direction_max * 4959) ==
          Fraction(endpoint["aggregate_saturation_numerator"],
                   endpoint["aggregate_saturation_denominator"]),
          "endpoint aggregate saturation")
    check(endpoint["endpoint_paid"] is False, "endpoint payment nonclaim")

    bank_rhs = 218 * core_size - line_cap * n
    c218 = bank["common_core_floor"]
    check((218 - line_cap) * (c218 - 1) < bank_rhs <= (218 - line_cap) * c218,
          "218-core ceiling identity")
    first_feasible = None
    direction_minimum = 10**9
    degree_deficit_maximum = -1
    saturation_minimum = Fraction(10, 1)
    scanned = 0
    for kprime in range(1, bank["shortened_K_ceiling"] + 1):
        full = 28396 + 204 * kprime
        capacity = 218 * (kprime - 1)
        if full > capacity:
            continue
        if first_feasible is None:
            first_feasible = kprime
        scanned += 1
        directions = first_integer_at_least(full, kprime - 1)
        direction_minimum = min(direction_minimum, directions)
        degree_deficit_maximum = max(degree_deficit_maximum, capacity - full)
        saturation_minimum = min(saturation_minimum, Fraction(full, capacity))

    check(first_feasible == bank["shortened_K_floor"] == 2044, "first feasible endpoint")
    check(scanned == 5025 - 2044 + 1 == 2982, "endpoint scan size")
    check(direction_minimum == bank["projective_direction_floor"] == 210, "direction minimum")
    check(degree_deficit_maximum == bank["aggregate_degree_deficit_ceiling"] == 41736,
          "deficit maximum")
    check(saturation_minimum == Fraction(bank["saturation_numerator"],
                                         bank["saturation_denominator"]),
          "saturation minimum")
    check(saturation_minimum > Fraction(9618, 10000), "saturation decimal claim")
    check(218 * 217 // 2 - 210 * (15 * 14 // 2) ==
          bank["dual_remaining_pair_ceiling"] == 1603, "dual pair budget")

    pure_rows: dict[int, list[int]] = {}
    for exponent in range(22):
        e = 1 << exponent
        for kprime in range(first_feasible, bank["shortened_K_ceiling"] + 1):
            if e <= kprime - 1 and 28396 + 204 * kprime <= 218 * e:
                pure_rows.setdefault(e, []).append(kprime)
    check({e: (min(rows), max(rows), len(rows))
           for e, rows in pure_rows.items()} ==
          {2048: (2049, 2049, 1), 4096: (4097, 4237, 141)},
          "pure-power row scan")
    check(power["surviving_degrees"] == [2048, 4096], "pure-power degrees")
    check(218 * 2048 - (28396 + 204 * 2049) ==
          power["cases"]["2048"]["missing_slot_ceiling"] == 72,
          "pure-power 2048 deficit")
    check(210 * 4096 < 28396 + 204 * 4097 <= 211 * 4096,
          "pure-power 4096 direction floor")
    check(218 * 4096 - (28396 + 204 * 4097) ==
          power["cases"]["4096"]["missing_slot_ceiling"] == 28744,
          "pure-power 4096 deficit")

    note = " ".join(
        (ROOT / "experimental/notes/thresholds/kb_mca_rank11_quotient_pair_plane218_v1.md")
        .read_text()
        .split()
    )
    check("does not assert that the current rank-eleven route has already produced" in note,
          "source-interface nonclaim")
    check("positive-characteristic line arrangements need" in note,
          "characteristic boundary")
    check("Neither dimension-three output nor the dimension-four output is paid" in note,
          "payment nonclaim")
    check("neither proves that the endpoint pencil is pure-power" in note,
          "pure-power nonclaim")
    check("No transport is claimed" in note,
          "shared-core transport nonclaim")
    check("dense-owner and saturated-plane router, not a payment" in note,
          "dense-type payment nonclaim")
    check("calibrated finite `(Q)`/split-pencil direction bank" in note,
          "endpoint direction-bank scope")
    print(
        "KB_RANK11_QUOTIENT_PAIR_PLANE218_INDEPENDENT_PASS "
        f"states={scanned} core=452813 directions={direction_minimum} "
        f"pairs=1603 moment_rows={moment_rows} moment_first=4836 "
        f"population_rows={population_rows} qmax=3170 dense=80446 "
        f"endpoint_directions=41746..47836 power=2048,4096"
    )


if __name__ == "__main__":
    main()
