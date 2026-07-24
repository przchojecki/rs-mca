#!/usr/bin/env sage
"""Independent Sage replay for the M31 combined-domain endpoint."""

from collections import deque
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = (
    ROOT
    / "experimental/data/certificates/"
    "m31-rank7-combined-domain-affine-johnson-endpoint-v1/manifest.json"
)

K = ZZ(1_048_576)
RADIUS = ZZ(981_129)
W = ZZ(67_447)
G = ZZ(354_972)
D = ZZ(287_525)
TARGET = ZZ(15_775_932)


def need(condition, label):
    if not condition:
        raise RuntimeError(label)


def local_cap(rank, k, ambient, excess):
    span = (
        (ambient + k)
        * (
            binomial(ambient + rank - 1, rank - 1)
            // binomial(excess + rank - 1, rank - 1)
        )
        // (excess + k)
    )
    denominator = (excess + k)^2 - (ambient + k) * (k - 1)
    if denominator > 0:
        span = min(
            span,
            (ambient + k) * (excess + 1) // denominator,
        )
    return ZZ(span)


def e0_six(cutoff):
    ambient = RADIUS - D
    excess = W - cutoff
    rows = {}
    base = [ZZ(0)] * (int(D) + 1)
    for k in range(1, int(D) + 1):
        base[k] = (ambient + k) // (excess + k)
    rows[1] = base
    for rank in range(2, 7):
        child = rows[rank - 1]
        current = list(child)
        prefix = ZZ(-1)
        window = deque()
        for k in range(rank, int(D) + 1):
            j = k - 1
            prefix = max(prefix, child[j])
            while window and child[window[-1]] <= child[j]:
                window.pop()
            window.append(j)
            lower = k - (k - 1) // (rank - 1)
            while window[0] < lower:
                window.popleft()
            projective = (
                (k - 1) * prefix
                + (ambient + 1) * child[window[0]]
            ) // (excess + k)
            exact = min(
                projective,
                local_cap(rank, ZZ(k), ambient, excess),
            )
            current[k] = max(child[k], exact)
        rows[rank] = current
    return rows[6]


def joined_cap(k, affine):
    denominator = (k + W)^2 - (K + k) * (k - 1)
    if denominator > 0:
        return min(
            affine,
            (K + k) * (W + 1) // denominator,
        )
    return affine


def endpoint(cutoff, affine, override_dimensions=None):
    e0 = e0_six(ZZ(cutoff))
    largest = int(D - 6)
    classes = [ZZ(0)] * (largest + 1)
    for size in range(1, largest + 1):
        k = D - size
        local_affine = (
            affine
            if override_dimensions is None or int(k) in override_dimensions
            else ZZ(14_115_528)
        )
        classes[size] = min(e0[int(k)], joined_cap(k, local_affine))

    prefix = [ZZ(0)] * (largest + 1)
    arg = [0] * (largest + 1)
    for size in range(1, largest + 1):
        if classes[size] > prefix[size - 1]:
            prefix[size] = classes[size]
            arg[size] = size
        else:
            prefix[size] = prefix[size - 1]
            arg[size] = arg[size - 1]

    agreement = G - cutoff
    best_num = ZZ(-1)
    best = None
    survivors = []
    for size in range(1, largest + 1):
        other = int(D - 1) - size
        upper = min(size, other - 4)
        tail_upper = min(size, other // 5)
        if upper < 1 or tail_upper < 1:
            continue
        numerator = (
            size * classes[size]
            + other * prefix[upper]
            + (RADIUS - D + 1) * prefix[tail_upper]
        )
        if numerator // agreement > TARGET:
            survivors.append(size)
        if numerator > best_num:
            best_num = numerator
            best = {
                "size": size,
                "k": int(D) - size,
                "cap": int(classes[size]),
                "other_cap": int(prefix[upper]),
                "other_arg": arg[upper],
                "tail_cap": int(prefix[tail_upper]),
                "tail_arg": arg[tail_upper],
            }
    return {
        "head": int(best_num // agreement),
        "numerator": int(best_num),
        "remainder": int(best_num % agreement),
        "survivors": survivors,
        **best,
    }


# Symbolic bridge identities.  The first difference is s_i+sigma-c, which is
# nonnegative under the declared source inequalities.
S.<gg,qq,si,cc,sigma,ww,rr> = PolynomialRing(QQ)
agreement_difference = (
    (gg - (qq - si) - cc + qq)
    - ((gg - ww - sigma) + ww)
)
domain_difference = (
    ((rr - sigma) + gg)
    - ((rr + ww) + (gg - ww - sigma))
)
need(agreement_difference == si + sigma - cc, "symbolic agreement identity")
need(domain_difference == 0, "symbolic domain identity")

affine_by_rank = [
    ZZ(binomial(K + rank, rank) // binomial(W + rank, rank))
    for rank in range(7)
]
need(
    affine_by_rank
    == [1, 15, 241, 3_757, 58_410, 908_021, 14_115_528],
    "affine caps",
)
affine = affine_by_rank[6]

q26194 = endpoint(26_194, affine)
q29554 = endpoint(29_554, affine)
q29555 = endpoint(29_555, affine)
need(q26194["head"] == 14_302_721, "Q26194 head")
need(q29554["head"] == 15_775_891, "Q29554 head")
need(q29554["numerator"] == 5_133_759_040_567, "Q29554 numerator")
need(q29555["head"] == 15_776_139, "Q29555 head")
need(q29555["numerator"] == 5_133_824_008_972, "Q29555 numerator")
need(q29555["survivors"] == list(range(282_539, 282_545)), "Q29555 survivors")

residual_dimensions = set(range(4_981, 4_987))
at_threshold = endpoint(29_555, ZZ(14_115_290), residual_dimensions)
after_threshold = endpoint(29_555, ZZ(14_115_291), residual_dimensions)
need(at_threshold["head"] == TARGET, "threshold closes")
need(after_threshold["head"] == TARGET + 1, "threshold sharp")

packet = json.loads(MANIFEST.read_text(encoding="ascii"))
need(
    packet["exact_endpoint"]["Q29554"]["head_cap"] == q29554["head"],
    "manifest endpoint",
)
need(
    packet["first_unresolved_head"]["compiled"]["head_cap"] == q29555["head"],
    "manifest residual",
)
need(
    packet["first_unresolved_head"]["uniform_combined_cap_threshold"][
        "largest_uniform_cap_closing_head"
    ]
    == 14_115_290,
    "manifest threshold",
)

print("Sage M31 rank7 combined-domain endpoint: PASS")
