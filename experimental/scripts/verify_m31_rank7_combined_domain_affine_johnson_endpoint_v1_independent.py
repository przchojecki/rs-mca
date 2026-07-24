#!/usr/bin/env python3
"""Independent replay of the M31 combined-domain rank-seven endpoint."""

from __future__ import annotations

import hashlib
import json
from collections import deque
from functools import lru_cache
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = (
    ROOT
    / "experimental/data/certificates/"
    "m31-rank7-combined-domain-affine-johnson-endpoint-v1/manifest.json"
)

K = 1_048_576
R = 981_129
W = 67_447
G = 354_972
D = 287_525
TARGET = 15_775_932


def need(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def digest(values: list[int]) -> str:
    raw = (
        json.dumps(values, sort_keys=True, separators=(",", ":")).encode("ascii")
        + b"\n"
    )
    return hashlib.sha256(raw).hexdigest()


def affine_or_johnson(
    rank: int,
    dimension: int,
    ambient: int,
    excess: int,
) -> int:
    span = (
        (ambient + dimension)
        * (
            comb(ambient + rank - 1, rank - 1)
            // comb(excess + rank - 1, rank - 1)
        )
        // (excess + dimension)
    )
    den = (excess + dimension) ** 2 - (
        ambient + dimension
    ) * (dimension - 1)
    if den > 0:
        span = min(
            span,
            (ambient + dimension) * (excess + 1) // den,
        )
    return span


@lru_cache(maxsize=None)
def e0_six(cutoff: int) -> tuple[int, ...]:
    ambient = R - D
    excess = W - cutoff
    rows: dict[int, list[int]] = {}
    first = [0] + [
        (ambient + k) // (excess + k)
        for k in range(1, D + 1)
    ]
    rows[1] = first
    for rank in range(2, 7):
        child = rows[rank - 1]
        current = child.copy()
        prefix_value = -1
        window: deque[int] = deque()
        for k in range(rank, D + 1):
            j = k - 1
            prefix_value = max(prefix_value, child[j])
            while window and child[window[-1]] <= child[j]:
                window.pop()
            window.append(j)
            lower = k - (k - 1) // (rank - 1)
            while window[0] < lower:
                window.popleft()
            projective = (
                (k - 1) * prefix_value
                + (ambient + 1) * child[window[0]]
            ) // (excess + k)
            exact = min(
                projective,
                affine_or_johnson(rank, k, ambient, excess),
            )
            current[k] = max(child[k], exact)
        rows[rank] = current
    return tuple(rows[6])


def direct_cap(k: int, affine_cap: int) -> int:
    den = (k + W) ** 2 - (K + k) * (k - 1)
    if den > 0:
        return min(affine_cap, (K + k) * (W + 1) // den)
    return affine_cap


def scan(
    cutoff: int,
    affine_cap: int,
    override_dimensions: frozenset[int] | None = None,
) -> dict[str, object]:
    e0 = list(e0_six(cutoff))
    largest = D - 6
    generic = 14_115_528
    direct = [0]
    for k in range(1, D + 1):
        cap = (
            affine_cap
            if override_dimensions is None or k in override_dimensions
            else generic
        )
        direct.append(direct_cap(k, cap))
    classes = [0] * (largest + 1)
    for size in range(1, largest + 1):
        k = D - size
        classes[size] = min(e0[k], direct[k])

    prefix = [0] * (largest + 1)
    arg = [0] * (largest + 1)
    for size in range(1, largest + 1):
        if classes[size] > prefix[size - 1]:
            prefix[size] = classes[size]
            arg[size] = size
        else:
            prefix[size] = prefix[size - 1]
            arg[size] = arg[size - 1]

    agreement = G - cutoff
    best_num = -1
    best: dict[str, int] = {}
    survivors: list[int] = []
    for size in range(1, largest + 1):
        remaining = D - 1 - size
        upper = min(size, remaining - 4)
        tail_upper = min(size, remaining // 5)
        if upper < 1 or tail_upper < 1:
            continue
        num = (
            size * classes[size]
            + remaining * prefix[upper]
            + (R - D + 1) * prefix[tail_upper]
        )
        if num // agreement > TARGET:
            survivors.append(size)
        if num > best_num:
            best_num = num
            best = {
                "largest_class_size": size,
                "largest_residual_dimension": D - size,
                "largest_class_cap": classes[size],
                "other_top_cap": prefix[upper],
                "other_top_cap_arg_size": arg[upper],
                "tail_cap": prefix[tail_upper],
                "tail_cap_arg_size": arg[tail_upper],
            }
    return {
        "head": best_num // agreement,
        "numerator": best_num,
        "remainder": best_num % agreement,
        "survivors": survivors,
        "hashes": {
            "E0_at_most_rank_six_sha256": digest(e0),
            "combined_direct_cap_sha256": digest(direct),
            "hybrid_class_cap_sha256": digest(classes),
            "prefix_cap_sha256": digest(prefix),
            "prefix_arg_sha256": digest(arg),
        },
        **best,
    }


def threshold(cutoff: int, generic: int) -> tuple[int, int, int]:
    residual_dimensions = frozenset(range(4_981, 4_987))
    low = 0
    high = generic
    while low < high:
        middle = (low + high + 1) // 2
        if int(
            scan(cutoff, middle, residual_dimensions)["head"]
        ) <= TARGET:
            low = middle
        else:
            high = middle - 1
    return (
        low,
        int(scan(cutoff, low, residual_dimensions)["head"]),
        int(scan(cutoff, low + 1, residual_dimensions)["head"]),
    )


def compare_scan(
    calculated: dict[str, object],
    certified: dict[str, object],
    label: str,
) -> None:
    need(calculated["head"] == certified["head_cap"], f"{label} head")
    need(
        calculated["numerator"] == certified["objective_numerator"],
        f"{label} numerator",
    )
    need(
        calculated["remainder"] == certified["objective_remainder"],
        f"{label} remainder",
    )
    for key, value in calculated["hashes"].items():
        need(value == certified["array_hashes"][key], f"{label} {key}")
    for key in (
        "largest_class_size",
        "largest_residual_dimension",
        "largest_class_cap",
        "other_top_cap",
        "other_top_cap_arg_size",
        "tail_cap",
        "tail_cap_arg_size",
    ):
        need(calculated[key] == certified[key], f"{label} {key}")


def main() -> None:
    packet = json.loads(MANIFEST.read_text(encoding="ascii"))
    affine = [
        comb(K + r, r) // comb(W + r, r)
        for r in range(7)
    ]
    need(
        affine == [1, 15, 241, 3_757, 58_410, 908_021, 14_115_528],
        "rank caps",
    )
    need(
        (4_550_146_385 - 913_681 * 4_980) == 15_005,
        "last Johnson denominator",
    )
    need(
        (4_550_146_385 - 913_681 * 4_981) == -898_676,
        "first inactive Johnson denominator",
    )

    q26194 = scan(26_194, affine[6])
    q29554 = scan(29_554, affine[6])
    q29555 = scan(29_555, affine[6])
    need(q26194["head"] == 14_302_721, "Q26194")
    need(q29554["head"] == 15_775_891, "Q29554")
    need(q29555["head"] == 15_776_139, "Q29555")
    need(q29555["survivors"] == list(range(282_539, 282_545)), "survivors")

    compare_scan(q26194, packet["exact_endpoint"]["Q26194"], "manifest Q26194")
    compare_scan(q29554, packet["exact_endpoint"]["Q29554"], "manifest Q29554")
    compare_scan(
        q29555,
        packet["first_unresolved_head"]["compiled"],
        "manifest Q29555",
    )

    cap, at_cap, after_cap = threshold(29_555, affine[6])
    need((cap, at_cap, after_cap) == (14_115_290, TARGET, TARGET + 1), "threshold")
    certified = packet["first_unresolved_head"][
        "uniform_combined_cap_threshold"
    ]
    need(
        certified["largest_uniform_cap_closing_head"] == cap,
        "manifest threshold",
    )
    need(
        certified["improvement_from_generic_affine_cap"] == 238,
        "manifest improvement",
    )
    print("independent M31 rank7 combined-domain endpoint: PASS")


if __name__ == "__main__":
    main()
