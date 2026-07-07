#!/usr/bin/env python3
"""Independent exact-integer replay of the four v13 adjacent pairs.

Verifies, from a fresh implementation (Python integers only, no shared code
with the repo's scripts), the exact comparisons displayed in
experimental/cap25_cap_v13_raw.tex prop:capg-moved-frontier and the pair
table of cor:capg-adjacent-pairs / AGENTS.md:

  list row : unsafe(m)  <=>  C(n,m) > p^(m-K)   * floor(q * eps)
  MCA row  : unsafe(m)  <=>  C(n,m) > p^(m-K-1) * floor(q * eps)
             (identity witness at K = k+1 -- the pencil degree of freedom;
              "at equal m the MCA comparison is exactly one factor of p
              easier", cor:capg-adjacent-pairs remark)

Rows: n = 2^21, k = 2^20; KoalaBear p = 2^31 - 2^24 + 1, q = p^6,
eps* = 2^-128 (official-shaped); Mersenne-31 p' = 2^31 - 1, q = p'^4,
eps* = 2^-100 (circle line-round). For each row the script checks the pass
at a0, the failure at a0 + 1 (with w -> w + 1), the auxiliary admissibility
C(floor(eps* q) + 1, 2) * k < q - n, and prints bit margins.

Expected output (matches the printed table to every decimal):

  KoalaBear MCA   a0 = 1116047  +8.978 / -22.197   PAIR OK
  KoalaBear list  a0 = 1116046  +9.164 / -22.011   PAIR OK
  M31 MCA         a0 = 1116023  +27.927 / -3.259   PAIR OK
  M31 list        a0 = 1116022  +28.113 / -3.073   PAIR OK

Runtime ~1 minute (eight C(2^21, ~1.116M) evaluations). Writes
experimental/data/v13_adjacent_pairs_independent_replay.json.
"""
import json
import math
import os


def log2_int(x):
    """log2 of a positive integer, accurate to ~1e-12."""
    b = x.bit_length()
    if b <= 64:
        return math.log2(x)
    return (b - 64) + math.log2(x >> (b - 64))


def check_row(name, p, ext_deg, eps_bits, pencil, a0, n, k):
    q = p ** ext_deg
    gate = q >> eps_bits                      # floor(q * 2^-eps_bits)
    out = {"row": name, "p": p, "ext_deg": ext_deg, "eps_bits": eps_bits,
           "pencil_shift": pencil, "a0": a0, "n": n, "k": k}
    K = k + pencil                            # MCA witness at K = k+1
    for tag, m in (("at_a0", a0), ("at_a0_plus_1", a0 + 1)):
        lhs = math.comb(n, m)
        w = m - K                             # depth m-K-pencil relative to k
        rhs = pow(p, w) * gate
        out[tag] = {"m": m, "depth_w": w, "unsafe": lhs > rhs,
                    "margin_bits": round(log2_int(lhs) - log2_int(rhs), 4)}
    # auxiliary admissibility: C(floor(eps q)+1, 2) * k < q - n  (and q - p)
    L0 = gate + 1
    out["admissibility_q_minus_n"] = (L0 * (L0 - 1) // 2) * k < q - n
    out["admissibility_q_minus_B"] = (L0 * (L0 - 1) // 2) * k < q - p
    out["pair_ok"] = out["at_a0"]["unsafe"] and not out["at_a0_plus_1"]["unsafe"] \
        and out["admissibility_q_minus_n"]
    return out


def main():
    N, k = 1 << 21, 1 << 20
    KB = 2**31 - 2**24 + 1
    M31 = 2**31 - 1
    rows = [
        ("KoalaBear MCA",  KB,  6, 128, 1, 1116047),
        ("KoalaBear list", KB,  6, 128, 0, 1116046),
        ("Mersenne-31 MCA",  M31, 4, 100, 1, 1116023),
        ("Mersenne-31 list", M31, 4, 100, 0, 1116022),
    ]
    results = []
    print(f"{'row':>16} {'a0':>8} {'unsafe@a0':>10} {'safe@a0+1':>10} {'admiss.':>8} {'verdict':>8}")
    for row in rows:
        r = check_row(*row, N, k)
        results.append(r)
        print(f"{r['row']:>16} {r['a0']:>8} "
              f"{'%+.3f' % r['at_a0']['margin_bits']:>10} "
              f"{'%.3f' % r['at_a0_plus_1']['margin_bits']:>10} "
              f"{str(r['admissibility_q_minus_n']):>8} "
              f"{'PAIR OK' if r['pair_ok'] else 'MISMATCH':>8}")
    here = os.path.dirname(os.path.abspath(__file__))
    dst = os.path.join(here, "..", "data",
                       "v13_adjacent_pairs_independent_replay.json")
    with open(dst, "w") as f:
        json.dump(results, f, indent=1)
    print(f"\nwrote {os.path.normpath(dst)}")
    assert all(r["pair_ok"] for r in results), "INDEPENDENT REPLAY FAILED"
    print("ALL FOUR PAIRS INDEPENDENTLY VERIFIED")


if __name__ == "__main__":
    main()
