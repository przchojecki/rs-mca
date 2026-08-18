#!/usr/bin/env python3
"""Independent integer replay for the quotient-pair plane-218 packet."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "experimental/data/certificates/kb-mca-rank11-quotient-pair-plane218-v1/contract.json"
CONTRACT_SHA256 = "6f667f2e0dee061cea4a166fdca08b908f3f7e291adc5367c43c4e48bc28a525"


def check(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


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
    print(
        "KB_RANK11_QUOTIENT_PAIR_PLANE218_INDEPENDENT_PASS "
        f"states={scanned} core=452813 directions={direction_minimum} "
        f"pairs=1603 moment_rows={moment_rows} moment_first=4836 power=2048,4096"
    )


if __name__ == "__main__":
    main()
