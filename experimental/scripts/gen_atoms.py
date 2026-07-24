#!/usr/bin/env python3
"""gen_atoms.py -- emit T_d fiber power-sum vectors for census_atoms.c
(packet: m31_aligned_collision_census_v1).

For fiber scale d (modulus M = 4096/d), each intact T_d fiber contained in the
punctured quotient domain Q' contributes one atom.  Atoms are split into
anchor-side (contained in the 479-point band anchor) and complement-side, and
each atom's first-32 power-sum vector (mod p = 2^31 - 1) is written little-endian
for the C fast-path enumerator.  Power sums are additive over disjoint fibers,
so a union of `a` atoms per side collides at depth 32 iff the two 32-vectors are
equal -- exactly what census_atoms.c checks.

Usage : python3 experimental/scripts/gen_atoms.py <d> [out.bin]
Example: python3 experimental/scripts/gen_atoms.py 8 atoms_d8.bin
Stdlib only; self-contained (no external engine module).
"""
import struct
import sys

P = 2**31 - 1
SCALE = pow(2, -2047, P)                 # 1073741824 = 2^30 (mod p)
GENERATOR = (1717986917, 1288490189)     # norm 1, order 2^31 in F_p[i]


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


def block_reps64(labels, a):
    return [r for r in range(1, 2048, 2) if r % 64 in {a, 64 - a}]


def power_sums(reps, labels, depth=32):
    out = [0] * depth
    for r in reps:
        q = labels[r]
        cur = q
        for k in range(depth):
            out[k] = (out[k] + cur) % P
            cur = (cur * q) % P
    return out


def main():
    d = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    outpath = sys.argv[2] if len(sys.argv) > 2 else f"atoms_d{d}.bin"

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
    anchor = set(core31)
    for a in anchor_classes:
        anchor.update(block_reps64(labels, a))
    compset = dset - anchor

    modulus = 4096 // d
    atoms = []
    for a in range(1, modulus // 2, 2):
        fiber = [r for r in range(1, 2048, 2) if r % modulus in {a, modulus - a}]
        if len(fiber) == d and len(set(fiber)) == d and set(fiber) <= dset:
            atoms.append(frozenset(fiber))

    anchor_atoms = [f for f in atoms if f <= anchor]
    comp_atoms = [f for f in atoms if f <= compset]
    split_atoms = [f for f in atoms
                   if not (f <= anchor) and not (f <= compset)]
    print(f"d={d} (fiber size {d}): intact atoms={len(atoms)}  "
          f"anchor-side={len(anchor_atoms)}  comp-side={len(comp_atoms)}  "
          f"split={len(split_atoms)}")

    with open(outpath, "wb") as handle:
        handle.write(struct.pack("<III", d, len(anchor_atoms), len(comp_atoms)))
        for atom in anchor_atoms:
            for value in power_sums(sorted(atom), labels):
                handle.write(struct.pack("<I", value))
        for atom in comp_atoms:
            for value in power_sums(sorted(atom), labels):
                handle.write(struct.pack("<I", value))
    with open(outpath + ".pts", "w") as handle:
        handle.write(f"{d} {len(anchor_atoms)} {len(comp_atoms)}\n")
        for atom in anchor_atoms:
            handle.write(" ".join(map(str, sorted(atom))) + "\n")
        for atom in comp_atoms:
            handle.write(" ".join(map(str, sorted(atom))) + "\n")
    print(f"wrote {outpath} and {outpath}.pts")


if __name__ == "__main__":
    main()
