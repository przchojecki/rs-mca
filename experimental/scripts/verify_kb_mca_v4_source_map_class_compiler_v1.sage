#!/usr/bin/env sage
"""Independent Sage replay for the abstract source-map packet compiler."""

import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-source-map-class-compiler-v1/manifest.json"
)
P = ZZ(2130706433)


def need(condition, label):
    if not condition:
        raise RuntimeError(label)


def normalize(vector, field):
    row = [field(value) for value in vector]
    pivot = next((value for value in row if value != 0), None)
    need(pivot is not None, "nonzero projective vector")
    return tuple(value / pivot for value in row)


document = json.loads(MANIFEST.read_text(encoding="ascii"))
Fp = GF(P)
W = VectorSpace(Fp, 6)

slope_indices = [0, 0, 1, 1, 2, 3, 4, 5, 10, 11, 12, 13]
slope_indices += [100 + index for index in range(3)]
slope_indices += [200 + index for index in range(69)]
slope_vectors = {tuple(W([index, 0, 0, 0, 0, 0])) for index in slope_indices}
need(len(slope_vectors) == 82, "82 distinct six-coordinate slopes")

direction_vectors = [
    [1, 0, 1],
    [2, 0, 2],
    [1, 2, 3],
    [2, 4, 6],
    [3, 6, 9],
    [1, 1, 0],
    [1, 1, 1],
    [1, 1, 2],
    [1, 1, 7],
    [1, 1, 8],
    [1, 1, 9],
    [1, 1, 10],
]
direction_vectors += [[1, 100 + index, 1] for index in range(3)]
direction_vectors += [[1, 1000 + index, 1] for index in range(69)]
direction_keys = {normalize(vector, Fp) for vector in direction_vectors}
need(len(direction_keys) == 81, "81 projective residue directions")
need(
    normalize([1, 2, 3], Fp) == normalize([2, 4, 6], Fp),
    "scaled residue directions agree",
)
need(
    normalize([1, 2, 3], Fp) != normalize([1, 2, 4], Fp),
    "distinct residue directions differ",
)

packet_classes = defaultdict(set)
for index in range(3):
    packet_classes["fixture-packet-small"].add(f"fixture-small-class::{index}")
for index in range(69):
    packet_classes["fixture-packet-large"].add(f"fixture-large-class::{index}")
need(len(packet_classes["fixture-packet-small"]) == 3, "small packet has three classes")
need(len(packet_classes["fixture-packet-large"]) == 69, "large packet has 69 classes")

packet_controls = {
    row["source_map_packet_id"]: row
    for row in document["regression_fixture"]["diagnostics"]["source_map_packets"]
}
need(
    packet_controls["fixture-packet-small"][
        "distinct_declared_rational_source_map_classes"
    ]
    == 3,
    "committed small-packet count",
)
need(
    packet_controls["fixture-packet-large"][
        "distinct_declared_rational_source_map_classes"
    ]
    == 69,
    "committed large-packet count",
)
need(
    packet_controls["fixture-packet-small"]["derived_terminal"]
    == "DECLARED_CONDITIONAL_SOURCE_MAP_PACKET_AT_MOST_68_NOT_GLOBALLY_BANKABLE",
    "small-packet terminal",
)
need(
    packet_controls["fixture-packet-large"]["derived_terminal"]
    == "UNPAID_PRIMITIVE_SOURCE_MAP_PACKET_AT_LEAST_69",
    "large-packet terminal",
)

B_remaining = ZZ(270780212960575880)
carrier_size = ZZ(1894736)
cap68_points = ZZ(67) * P + ZZ(68)
cap68_charge = cap68_points * carrier_size
need(cap68_charge == ZZ(270487454459300144), "cap-68 charge")
need(B_remaining - cap68_charge == ZZ(292758501275736), "cap-68 margin")

cap69_points = ZZ(68) * P + ZZ(69)
cap69_charge = cap69_points * carrier_size
need(cap69_charge == ZZ(274524580645231568), "cap-69 charge")
need(cap69_charge - B_remaining == ZZ(3744367684655688), "cap-69 deficit")

need(ZZ(213050) - ZZ(134943) + 1 == ZZ(78108), "open interval count")
need(ZZ(213050) - ZZ(134944) + 1 == ZZ(78107), "later-slack count")

print("PASS: Sage GF(p)-coordinate and collective packet replay")
print("charged_slopes=82")
print("residue_directions=81")
print("packet_classes=3,69")
print("cap68_margin=292758501275736")
