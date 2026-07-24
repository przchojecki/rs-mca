#!/usr/bin/env python3
"""census_aligned.py -- standalone exhaustive T16-aligned depth-32 collision
census rooted at the band anchor (packet: m31_aligned_collision_census_v1).

This is the pure-Python reference enumerator for the fiber-aligned slice: since
a deficiency e <= 65 uses at most four T16 fibers per side, enumerating all
a-subsets of the 28 anchor-side and 31 complement-side intact T16 classes is
exhaustive.  A union of `a` T16 classes collides at depth 32 iff its 32-power-sum
vector equals that of the complement union (power sums are additive over disjoint
fibers).  Each collision is classified as a whole-T64-block swap (both sides a
complete T64 block, i.e. all four of its T16 subclasses) or a non-block collision.

For a in {1,2,3,4} (deficiency e = 16a in {16,32,48,64}) the result is:
0 collisions for e in {16,32,48}; at e=64 exactly 49 collisions, every one a
whole-T64-block swap (7 anchor x 7 complement) and 0 non-block collisions.

Usage : python3 experimental/scripts/census_aligned.py
Stdlib only; self-contained; runs in well under a minute.
"""
from itertools import combinations

P = 2**31 - 1
SCALE = pow(2, -2047, P)                  # 1073741824 = 2^30 (mod p)
GENERATOR = (1717986917, 1288490189)      # norm 1, order 2^31 in F_p[i]
DEPTH = 32


def mul2(u, v):
    return ((u[0] * v[0] - u[1] * v[1]) % P, (u[0] * v[1] + u[1] * v[0]) % P)


def pow2(u, exponent):
    acc, base = (1, 0), u
    while exponent:
        if exponent & 1:
            acc = mul2(acc, base)
        base = mul2(base, base)
        exponent >>= 1
    return acc


def quotient_labels():
    base = pow2(GENERATOR, 2**19)
    step = mul2(base, base)
    current = base
    out = {}
    for j in range(1024):
        out[2 * j + 1] = (SCALE * current[0]) % P
        current = mul2(current, step)
    return out


def block_reps64(a):
    return [r for r in range(1, 2048, 2) if r % 64 in {a, 64 - a}]


def t16_reps(a):
    return [r for r in range(1, 2048, 2) if r % 256 in {a, 256 - a}]


def power_sums(reps, labels):
    out = [0] * DEPTH
    for r in reps:
        q = labels[r]
        cur = q
        for k in range(DEPTH):
            out[k] = (out[k] + cur) % P
            cur = (cur * q) % P
    return tuple(out)


def main():
    labels = quotient_labels()
    qprime = [r for r in range(1, 2048, 2) if r not in {1, 3}]
    dset = set(qprime)

    core31 = [
        63, 65, 127, 129, 191, 193, 255, 257,
        319, 321, 383, 385, 447, 449, 511, 513,
        575, 577, 639, 641, 703, 705, 767, 769,
        831, 833, 895, 897, 959, 961, 1023,
    ]
    anchor_classes = [5, 7, 9, 11, 13, 15, 17]
    comp_classes = [a for a in range(5, 32, 2) if a not in anchor_classes]
    anchor = set(core31)
    for a in anchor_classes:
        anchor.update(block_reps64(a))
    compset = dset - anchor

    intact_t16 = []
    for a in range(1, 128, 2):
        cls = frozenset(t16_reps(a))
        if len(cls) == 16 and cls <= dset:
            intact_t16.append(cls)
    anchor_side = [c for c in intact_t16 if c <= anchor]
    comp_side = [c for c in intact_t16 if c <= compset]
    print(f"intact T16 classes: {len(intact_t16)}  "
          f"anchor-side: {len(anchor_side)}  complement-side: {len(comp_side)}")

    anchor_mom = [power_sums(sorted(c), labels) for c in anchor_side]
    comp_mom = [power_sums(sorted(c), labels) for c in comp_side]

    def subset_moment(moms, idx):
        acc = [0] * DEPTH
        for i in idx:
            row = moms[i]
            for k in range(DEPTH):
                acc[k] = (acc[k] + row[k]) % P
        return tuple(acc)

    def block_sets(side_classes, classes):
        sets = set()
        for a in classes:
            block = set(block_reps64(a))
            members = frozenset(i for i, c in enumerate(side_classes)
                                if c <= block)
            if len(members) == 4:
                sets.add(members)
        return sets

    anchor_blocks = block_sets(anchor_side, anchor_classes)
    comp_blocks = block_sets(comp_side, comp_classes)

    print()
    for a in range(1, 5):
        e = 16 * a
        left = {}
        for idx in combinations(range(len(anchor_side)), a):
            left.setdefault(subset_moment(anchor_mom, idx), []).append(idx)
        collisions = whole_block = nonblock = 0
        for idx in combinations(range(len(comp_side)), a):
            matches = left.get(subset_moment(comp_mom, idx))
            if not matches:
                continue
            comp_is_block = (a == 4 and frozenset(idx) in comp_blocks)
            for lidx in matches:
                collisions += 1
                anchor_is_block = (a == 4 and frozenset(lidx) in anchor_blocks)
                if anchor_is_block and comp_is_block:
                    whole_block += 1
                else:
                    nonblock += 1
        tag = " in[34,65]" if 34 <= e <= 65 else ""
        print(f"e={e:>3}{tag}: collisions={collisions:>3}  "
              f"whole-T64-block={whole_block:>3}  non-block={nonblock:>3}")

    print("\nNo non-block T16-aligned collision in [34,65]; "
          "the 49 at e=64 are exactly the whole-T64-block swaps (7 x 7).")


if __name__ == "__main__":
    main()
