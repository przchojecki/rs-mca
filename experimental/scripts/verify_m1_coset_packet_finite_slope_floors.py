#!/usr/bin/env python3
"""Verify the M1 coset-packet finite-slope floor certificate."""

from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path
from typing import Any


N = 512
K = 256
Q = 17**32
H_SIZE = 512
DATA_PATH = Path("experimental/data/m1_coset_packet_finite_slope_floors.json")


def packet_count(agreement: int, coset_size: int) -> dict[str, int]:
    prefix_depth = agreement - K - 1
    if prefix_depth < 0:
        raise AssertionError((agreement, prefix_depth))
    if prefix_depth >= coset_size:
        raise AssertionError((agreement, prefix_depth, coset_size))
    if N % coset_size:
        raise AssertionError((N, coset_size))

    coset_count = N // coset_size
    base_size = agreement % coset_size
    full_cosets = (agreement - base_size) // coset_size

    if base_size == 0:
        available = coset_count
        reserved = 0
    else:
        available = coset_count - 1
        reserved = 1

    if not 0 <= full_cosets <= available:
        raise AssertionError((agreement, coset_size, full_cosets, available))

    lower = comb(available, full_cosets)
    return {
        "agreement": agreement,
        "prefix_depth": prefix_depth,
        "coset_size": coset_size,
        "coset_count": coset_count,
        "reserved_partial_cosets": reserved,
        "base_size": base_size,
        "full_cosets_chosen": full_cosets,
        "available_full_cosets": available,
        "lower": lower,
    }


def selected_coset_size(agreement: int) -> int:
    if 261 <= agreement <= 264:
        return 8
    if 265 <= agreement <= 272:
        return 16
    if 273 <= agreement <= 288:
        return 32
    raise AssertionError(agreement)


def expanded_rows() -> list[dict[str, int]]:
    return [
        packet_count(agreement, selected_coset_size(agreement))
        for agreement in range(261, 289)
    ]


def grouped_records() -> list[dict[str, Any]]:
    groups = [
        (261, 263, 8),
        (264, 264, 8),
        (265, 271, 16),
        (272, 272, 16),
        (273, 287, 32),
        (288, 288, 32),
    ]
    records: list[dict[str, Any]] = []
    for start, end, coset_size in groups:
        rows = [packet_count(agreement, coset_size) for agreement in range(start, end + 1)]
        lowers = {row["lower"] for row in rows}
        full_cosets = {row["full_cosets_chosen"] for row in rows}
        available = {row["available_full_cosets"] for row in rows}
        reserved = {row["reserved_partial_cosets"] for row in rows}
        coset_count = {row["coset_count"] for row in rows}
        if len(lowers) != 1 or len(full_cosets) != 1 or len(available) != 1:
            raise AssertionError((start, end, rows))
        if len(reserved) != 1 or len(coset_count) != 1:
            raise AssertionError((start, end, rows))
        lower = lowers.pop()
        chosen = full_cosets.pop()
        avail = available.pop()
        reserved_value = reserved.pop()
        count = coset_count.pop()
        if reserved_value:
            base_size = f"a mod {coset_size}"
        else:
            base_size = "0"
        records.append(
            {
                "agreementStart": start,
                "agreementEnd": end,
                "prefixDepthStart": start - K - 1,
                "prefixDepthEnd": end - K - 1,
                "cosetSize": coset_size,
                "cosetCount": count,
                "reservedPartialCosets": reserved_value,
                "baseSize": base_size,
                "fullCosetsChosen": chosen,
                "availableFullCosets": avail,
                "badSlopesLower": str(lower),
                "badSlopesLowerFormula": f"binom({avail},{chosen})",
                "beatsMovingRootTangentFloor": True,
                "anchorSeparationChecked": True,
            }
        )
    return records


def certificate() -> dict[str, Any]:
    return {
        "status": "PROVED / FINITE-SLOPE LOWER-BOUND / AUDIT",
        "row": "RS[F_17^32,H,256]",
        "field": "F_17[z]/(z^32 - 3)",
        "predicate": "finite-slope support-wise LD/MCA",
        "q": "17^32",
        "qExact": str(Q),
        "n": N,
        "k": K,
        "baseCodeDegree": "deg Q < 256",
        "numeratorDegree": "deg P <= 256",
        "construction": "full dyadic coset packets plus optional fixed partial coset",
        "records": grouped_records(),
        "nonclaims": [
            "not a safe-side bound",
            "not ordinary list decoding",
            "not interleaved list size",
            "not protocol soundness",
            "finite slopes only",
            "separate existence statements by agreement",
            "not one received line realizing all agreement rows simultaneously",
            "a=257..260 intentionally outside this coset-packet row set",
            "not an exact Bad_fin classification",
        ],
    }


def best_packet_floor(agreement: int) -> tuple[int, int]:
    best_lower = -1
    best_m = -1
    for coset_size in (2, 4, 8, 16, 32, 64, 128, 256, 512):
        try:
            row = packet_count(agreement, coset_size)
        except AssertionError:
            continue
        if row["lower"] > best_lower:
            best_lower = row["lower"]
            best_m = coset_size
    return best_lower, best_m


def validate_math() -> None:
    assert Q == 2367911594760467245844106297320951247361
    assert Q // (2**128) == 6

    rows = expanded_rows()
    assert len(rows) == 28
    for row in rows:
        agreement = row["agreement"]
        lower = row["lower"]
        tangent_floor = N - agreement + 1
        assert lower > tangent_floor, (agreement, lower, tangent_floor)
        assert Q - H_SIZE > K * comb(lower, 2), agreement
        assert row["prefix_depth"] < row["coset_size"], row

    assert comb(63, 32) == 916312070471295267
    assert comb(64, 33) == 1777090076065542336
    assert comb(31, 16) == 300540195
    assert comb(32, 17) == 565722720
    assert comb(15, 8) == 6435
    assert comb(16, 9) == 11440

    # Scope check for the displayed packet method after the entropy rows.
    # The packet method also produces large rows at a=257..260, but those are
    # intentionally left to the random simple-pole entropy PR. Starting at
    # a=261, the displayed coset-packet method beats the moving-root tangent
    # floor exactly through a=288. This is not a global impossibility claim for
    # other constructions.
    beat_rows = []
    for agreement in range(261, 513):
        lower, _ = best_packet_floor(agreement)
        if lower > N - agreement + 1:
            beat_rows.append(agreement)
    assert beat_rows == list(range(261, 289))


def validate_json(path: Path) -> None:
    expected = certificate()
    actual = json.loads(path.read_text(encoding="utf-8"))
    if actual != expected:
        raise AssertionError("JSON certificate does not match verifier output")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="print computed certificate JSON")
    parser.add_argument("--check", type=Path, default=DATA_PATH, help="certificate path")
    args = parser.parse_args()

    validate_math()
    if args.json:
        print(json.dumps(certificate(), indent=2))
        return
    validate_json(args.check)

    print("q =", Q)
    for record in grouped_records():
        start = record["agreementStart"]
        end = record["agreementEnd"]
        lower = record["badSlopesLower"]
        formula = record["badSlopesLowerFormula"]
        label = f"a={start}" if start == end else f"a={start}..{end}"
        print(f"{label}: lower={lower} ({formula})")
    print("floor(q/2^128) =", Q // (2**128))
    print("coset-packet finite-slope floor checks passed")


if __name__ == "__main__":
    main()
