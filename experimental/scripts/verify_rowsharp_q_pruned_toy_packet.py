#!/usr/bin/env python3
"""Pruned-Q toy packet: exact raw + first-match-pruned prefix-fiber censuses.

Tests `prob:row-sharp-q` (experimental/grande_finale.tex L3574-3580) at rows
where the full fiber distribution can be enumerated (agents.md Good-first-PR #1).

Object: depth-w power-sum prefix map on m-subsets of the order-N subgroup D of
F_p^* (his census convention, experimental/scripts/qsp_fiber_census.py).
Raw side reproduces his committed exact anchors digit-exact
(experimental/data/rowsharp_q_external_calibration.json and the printed
max-to-mean table of rem:capff1-collision-gap, cs25_cap_v13_2.tex L6334).
Pruned side removes, in first-match order, HIS in-tree toy quotient-pullback
classifier cells (experimental/scripts/qsp_modeatnull_structure.py L20-23):

    C1 "coset-union"     : S = -S (union of antipodal mu_2-pairs)
    C2 "dilation-stable" : gS = S for some g in D, g != 1

and reports the residual distribution P_Q(z) (trivial-stabilizer subsets),
its max, null, exact residual mass tau (the quantity prop:q-moment-order-floor
requires), and the def:q-row-atom ratio R = p^w * max / C(N,m) against the
binding deployed full-budget allowance 8.4152 (prop:q-exact-target,
Mersenne-31 list row).  The remaining deployed-row cells (tangent,
common-support, planted, field-drop, extension, rank) have no in-tree
toy-scale instantiation and are NOT modeled (stated, not silently assumed
empty).  Calibration only; enters no proof.

Exactness: python big ints and Fractions in every decision; floats only in
display strings.  Stdlib only, zero arguments, fail-closed: any check failure,
anchor mismatch, or uncaught mutation control => RESULT: FAIL, exit 1.

Rows (all from his FIBER_DEFAULT): (17,16,8) w=1,2,3 and (41,20,10) w=1,2,3 by
direct enumeration; (101,50,25) w=2 and (257,64,34) w=1 by exact big-int DP.
(257,64,34,2) is excluded by compute budget (row shrunk, not budget raised).

Mutation controls (each must be caught): M1 wrong pruning-cell membership,
M2 off-by-one depth, M3 wrong bound constant, M4 wrong domain.
"""
import json
import math
import os
import sys
from fractions import Fraction
from itertools import combinations

# --- his committed exact anchors (rowsharp_q_external_calibration.json) -----
ANCHORS = {  # (p,N,m,w) -> (max, null, sum_z N^2)
    (17, 16, 8, 1): (758, 758, 9743348),
    (17, 16, 8, 2): (54, 54, 574020),
    (17, 16, 8, 3): (7, 6, 38356),
    (41, 20, 10, 1): (4516, 4516, 832556056),
    (41, 20, 10, 2): (133, 66, 20390226),
    (41, 20, 10, 3): (11, 6, 744166),
    (101, 50, 25, 2): (12392018052, 12392018052, 1566477935492737080014204),
    (257, 64, 34, 1): (6304622609083424, 6304622609083424,
                       10215304424390627411534790353735040),
}
# printed max-to-mean ratios (calibration note L26-30 / v13.2 L6334, 4 decimals)
PRINTED_RATIO = {
    (17, 16, 8, 1): "1.0012", (17, 16, 8, 2): "1.2126", (17, 16, 8, 3): "2.6722",
    (41, 20, 10, 1): "1.0022", (41, 20, 10, 2): "1.2101",
    (41, 20, 10, 3): "4.1034",
}
# hand-derived pruning-cell totals (pq_design.md section 3)
CELL_TOTALS = {  # (p,N,m) -> (|C1|, |C2 \ C1|)
    (17, 16, 8): (70, 0),
    (41, 20, 10): (252, 4),
    (101, 50, 25): (0, 252),
    (257, 64, 34): (565722720, 0),
}
ALLOWANCE = Fraction(84152, 10000)  # binding M31-list full-budget ceiling 8.4152

ROWS = [
    dict(p=17, N=16, m=8, depths=(1, 2, 3), method="enum"),
    dict(p=41, N=20, m=10, depths=(1, 2, 3), method="enum"),
    dict(p=101, N=50, m=25, depths=(2,), method="dp"),
    dict(p=257, N=64, m=34, depths=(1,), method="dp"),
]
MUT_ROWS = [0, 3]  # mutation-control runs use (17,16,8) enum + (257,64,34) dp


def prime_factors(x):
    out, d = [], 2
    while d * d <= x:
        while x % d == 0:
            out.append(d)
            x //= d
        d += 1
    if x > 1:
        out.append(x)
    return sorted(set(out))


def domain(p, N, mut):
    """Order-N subgroup of F_p^*, exponent order d[i] = h^i (multiplication by
    h^s = index rotation by s).  His script sorts D; the census is
    order-invariant.  M4 mutation: not a subgroup at all."""
    if mut == "M4_domain":
        return list(range(1, N + 1))
    g = next(c for c in range(2, p)
             if all(pow(c, (p - 1) // r, p) != 1 for r in prime_factors(p - 1)))
    h = pow(g, (p - 1) // N, p)
    return [pow(h, i, p) for i in range(N)]


def key_from_sums(sums, w, mut):
    """Depth-w prefix key from the full power-sum vector.  M2 mutation:
    off-by-one depth (top power sum dropped, padded with 0)."""
    if mut == "M2_depth":
        return tuple(sums[:w - 1]) + (0,)
    return tuple(sums[:w])


def ie_terms(N, m):
    """Subgroup-lattice inclusion-exclusion for {S : Stab_D(S) != 1}:
    sum over nonempty subsets Q of primes(N) of (-1)^(|Q|+1) A_prod(Q),
    A_d = unions of m/d distinct mu_d-cosets (empty unless d | m)."""
    primes = prime_factors(N)
    terms = []
    for bits in range(1, 1 << len(primes)):
        d, k = 1, 0
        for i, q in enumerate(primes):
            if bits >> i & 1:
                d *= q
                k += 1
        if m % d == 0:
            terms.append((d, 1 if k % 2 == 1 else -1))
    return terms


def coset_dp(p, D, dsub, m, wmax):
    """Exact census of unions of m/dsub distinct mu_dsub-cosets of D:
    dict (depth-wmax power-sum vector) -> count.  None if dsub does not
    divide m (no such unions)."""
    N = len(D)
    if m % dsub:
        return None
    k, ncos = m // dsub, N // dsub
    vecs = []
    for i in range(ncos):
        elems = [D[(i + t * ncos) % N] for t in range(dsub)]
        vecs.append(tuple(sum(pow(e, j, p) for e in elems) % p
                          for j in range(1, wmax + 1)))
    dp = [dict() for _ in range(k + 1)]
    dp[0][(0,) * wmax] = 1
    for v in vecs:
        for c in range(k - 1, -1, -1):
            for z, cnt in dp[c].items():
                nz = tuple((z[j] + v[j]) % p for j in range(wmax))
                dp[c + 1][nz] = dp[c + 1].get(nz, 0) + cnt
    assert sum(dp[k].values()) == math.comb(ncos, k)
    return dp[k]


def cells_by_fiber(p, D, N, m, w, mut):
    """Per-fiber counts of stab-nontrivial subsets via inclusion-exclusion of
    coset-DPs: (c1[z], c2only[z]) dicts.  C1 = A_2 (S=-S); C2only = IE - A_2."""
    ie = {}
    a2 = {}
    for d, sign in ie_terms(N, m):
        hist = coset_dp(p, D, d, m, w if mut != "M2_depth" else max(w - 1, 0))
        if hist is None:
            continue
        red = {}
        for z, cnt in hist.items():
            kz = key_from_sums(list(z) + [0] * w, w, mut) if mut == "M2_depth" \
                else tuple(z[:w])
            red[kz] = red.get(kz, 0) + cnt
        for kz, cnt in red.items():
            ie[kz] = ie.get(kz, 0) + sign * cnt
        if d == 2:
            a2 = red
    c1 = dict(a2)
    c2only = {}
    for kz, cnt in ie.items():
        rest = cnt - c1.get(kz, 0)
        c2only[kz] = rest
    return c1, c2only


def census_enum(p, N, m, depths, mut):
    """Direct enumeration.  Returns per-depth histograms {z: [raw, c1, c2only]}
    plus global classification totals (c1_total, c2only_total)."""
    D = domain(p, N, mut)
    X1 = [x % p for x in D]
    X2 = [x * x % p for x in D]
    X3 = [x * x * x % p for x in D]
    bits = [1 << i for i in range(N)]
    full = (1 << N) - 1
    half = N // 2
    shifts = [N // q for q in prime_factors(N)]
    hist = {w: {} for w in depths}
    c1_total = c2_total = 0
    Dset = None
    if mut == "M1_wrong_cell":
        Dset = list(D)
    for combo in combinations(range(N), m):
        a = b = c = 0
        mask = 0
        for i in combo:
            a += X1[i]
            b += X2[i]
            c += X3[i]
            mask |= bits[i]
        sums = (a % p, b % p, c % p)
        if mut == "M1_wrong_cell":
            S = frozenset(D[i] for i in combo)
            c1f = all((p - x + 1) % p in S for x in S)
            stab = any(all((g * x) % p in S for x in S)
                       for g in Dset if g != 1)
        else:
            c1f = ((mask << half) | (mask >> (N - half))) & full == mask
            stab = c1f or any(
                ((mask << s) | (mask >> (N - s))) & full == mask
                for s in shifts if s != half)
        c2f = stab and not c1f
        c1_total += c1f
        c2_total += c2f
        for w in depths:
            kz = key_from_sums(sums, w, mut)
            cell = hist[w].get(kz)
            if cell is None:
                cell = hist[w][kz] = [0, 0, 0]
            cell[0] += 1
            if c1f:
                cell[1] += 1
            elif c2f:
                cell[2] += 1
    return hist, c1_total, c2_total, D


def census_dp(p, N, m, w, mut):
    """Exact big-int DP over the p^w prefix cells (his qsp_fiber_census.py
    recurrence, stdlib ints).  Returns histogram {z: raw}."""
    D = domain(p, N, mut)
    weff = (w - 1) if mut == "M2_depth" else w
    size = p ** weff
    dp = [[0] * size for _ in range(m + 1)]
    dp[0][0] = 1
    for x in D:
        v = [pow(x, j, p) for j in range(1, weff + 1)]
        if weff == 2:
            r0 = [((u - v[0]) % p) * p for u in range(p)]
            r1 = [(t - v[1]) % p for t in range(p)]
            perm = [base + off for base in r0 for off in r1]
        elif weff == 1:
            perm = [(u - v[0]) % p for u in range(p)]
        else:
            perm = [0]
        for c in range(m - 1, -1, -1):
            src = dp[c]
            dp[c + 1] = [acc + src[j] for acc, j in zip(dp[c + 1], perm)]
    flat = dp[m]
    hist = {}
    for i, cnt in enumerate(flat):
        if cnt:
            if weff == 2:
                z = (i // p, i % p)
            elif weff == 1:
                z = (i,)
            else:
                z = ()
            hist[key_from_sums(list(z) + [0] * w, w, mut)
                 if mut == "M2_depth" else z] = cnt
    return hist, D


def fmt_frac(fr, digits=6):
    return f"{float(fr):.{digits}f}"


def run(rows_idx, mut=None):
    """Run the packet on the given rows.  Returns (checks, lines, results):
    checks = [(name, ok, detail)], lines = printable report, results = data."""
    checks, lines, results = [], [], []

    def ck(name, ok, detail=""):
        checks.append((name, bool(ok), detail))
        if not ok:
            lines.append(f"    CHECK FAIL: {name} {detail}")
        return bool(ok)

    allowance = Fraction(1) if mut == "M3_bound" else ALLOWANCE
    for ri in rows_idx:
        row = ROWS[ri]
        p, N, m, depths, method = (row["p"], row["N"], row["m"],
                                   row["depths"], row["method"])
        Cnm = math.comb(N, m)
        exp_c1, exp_c2 = CELL_TOTALS[(p, N, m)]
        if method == "enum":
            hist, c1_tot, c2_tot, D = census_enum(p, N, m, depths, mut)
        else:
            hist = {}
            for w in depths:
                hist[w], D = census_dp(p, N, m, w, mut)
            c1_tot = c2_tot = None  # from coset-DP below
        # per-fiber cell counts via subgroup-lattice inclusion-exclusion
        cells_ie = {w: cells_by_fiber(p, D, N, m, w, mut) for w in depths}
        if method == "dp":
            c1_tot = sum(cells_ie[depths[0]][0].values())
            c2_tot = sum(cells_ie[depths[0]][1].values())
        ck(f"({p},{N},{m}) cell totals C1={exp_c1} C2only={exp_c2}",
           (c1_tot, c2_tot) == (exp_c1, exp_c2),
           f"got ({c1_tot},{c2_tot})")
        lines.append(f"row ({p},{N},{m}) |D|={N}: pruning cells "
                     f"C1 coset-union = {c1_tot}, "
                     f"C2 dilation-stable-only = {c2_tot} "
                     f"[his classifiers, qsp_modeatnull_structure.py L20-23]")
        for w in depths:
            key = (p, N, m, w)
            h = hist[w]
            if method == "enum":
                raw = {z: v[0] for z, v in h.items()}
                c1_z = {z: v[1] for z, v in h.items() if v[1]}
                c2_z = {z: v[2] for z, v in h.items() if v[2]}
                # cross-check classification vs inclusion-exclusion, per fiber
                ie1, ie2 = cells_ie[w]
                ok_ie = (all(c1_z.get(z, 0) == ie1.get(z, 0)
                             for z in set(c1_z) | set(ie1)) and
                         all(c2_z.get(z, 0) == ie2.get(z, 0)
                             for z in set(c2_z) | set(ie2)))
                ck(f"{key} classification == coset-DP inclusion-exclusion "
                   f"(per fiber)", ok_ie)
            else:
                raw = h
                c1_z, c2_z = cells_ie[w]
                ck(f"{key} cell counts nonneg per fiber",
                   all(v >= 0 for v in c1_z.values()) and
                   all(v >= 0 for v in c2_z.values()))
                onull = all(z == (0,) * w
                            for z, v in list(c1_z.items()) + list(c2_z.items())
                            if v)
                ck(f"{key} all cell mass at null fiber (derived)", onull)
            total = sum(raw.values())
            second = sum(v * v for v in raw.values())
            mx = max(raw.values())
            nullf = raw.get((0,) * w, 0)
            mean = Cnm / p ** w
            ck(f"{key} checksum sum_z N_w(z) == C({N},{m})", total == Cnm,
               f"{total} != {Cnm}")
            amax, anull, asec = ANCHORS[key]
            ck(f"{key} anchor max == {amax}", mx == amax, f"got {mx}")
            ck(f"{key} anchor null == {anull}", nullf == anull, f"got {nullf}")
            ck(f"{key} anchor sum N^2 == {asec}", second == asec,
               f"got {second}")
            ck(f"{key} SP mass = sumN2 - C(N,m) >= 0", second - Cnm >= 0)
            if key in PRINTED_RATIO:
                got = f"{mx / mean:.4f}"
                ck(f"{key} printed max/mean ratio {PRINTED_RATIO[key]}",
                   got == PRINTED_RATIO[key], f"got {got}")
            # ---- pruned distribution (first match: C1 then C2) ----
            pruned = {}
            rm1 = rm2 = 0
            okmono = True
            for z, v in raw.items():
                d1, d2 = c1_z.get(z, 0), c2_z.get(z, 0)
                pv = v - d1 - d2
                rm1 += d1
                rm2 += d2
                if pv < 0 or pv > v:
                    okmono = False
                pruned[z] = pv
            ck(f"{key} monotonicity 0 <= pruned(z) <= raw(z)", okmono)
            pmass = sum(pruned.values())
            ck(f"{key} mass identity sum pruned == C(N,m) - |C1 u C2|",
               pmass == Cnm - (c1_tot + c2_tot),
               f"{pmass} != {Cnm}-({c1_tot}+{c2_tot})")
            pmx = max(pruned.values())
            pnull = pruned.get((0,) * w, 0)
            tau = Fraction(pmass, Cnm)
            r_raw = Fraction(p ** w * mx, Cnm)
            r_pr = Fraction(p ** w * pmx, Cnm)
            ck(f"{key} G2 R_pruned <= R_raw", r_pr <= r_raw)
            ck(f"{key} G2 R_pruned < allowance {float(allowance)}",
               r_pr < allowance, f"R_pruned = {float(r_pr):.6f}")
            cells_at_null = c1_z.get((0,) * w, 0) + c2_z.get((0,) * w, 0)
            if cells_at_null:
                ck(f"{key} G3 pruned null < raw null", pnull < nullf)
            argmax_moved = pruned.get(max(raw, key=raw.get), 0) != pmx
            poisson = " [Poisson-boundary row: mean < 10]" if mean < 10 else ""
            lines.append(
                f"fiber ({p},{N},{m},{w}) EXACT: "
                f"max/mean-1 = {mx / mean - 1.0:.4e}, "
                f"null/mean-1 = {nullf / mean - 1.0:.4e}, "
                f"max = {mx}, null = {nullf}")
            lines.append(
                f"pruned({p},{N},{m},{w}): max = {pmx}, null = {pnull}, "
                f"removed C1 = {rm1}, C2 = {rm2} "
                f"(at null: {cells_at_null}); "
                f"tau = {pmass}/{Cnm} = {fmt_frac(tau)}")
            lines.append(
                f"    R_raw = {fmt_frac(r_raw)}, R_pruned = {fmt_frac(r_pr)}, "
                f"allowance = {float(allowance)}, "
                f"verdict: {'OK' if r_pr < allowance else 'EXCEEDED'}; "
                f"max {'moved off' if argmax_moved else 'stays at'} "
                f"raw argmax{poisson}")
            results.append(dict(
                p=p, N=N, m=m, w=w, method=method,
                raw_max=str(mx), raw_null=str(nullf), sum_N2=str(second),
                pruned_max=str(pmx), pruned_null=str(pnull),
                removed_C1=str(rm1), removed_C2only=str(rm2),
                cells_at_null=str(cells_at_null),
                tau=f"{pmass}/{Cnm}",
                R_raw=f"{p ** w * mx}/{Cnm}", R_pruned=f"{p ** w * pmx}/{Cnm}",
                R_raw_f=float(r_raw), R_pruned_f=float(r_pr),
                verdict_below_allowance=bool(r_pr < allowance)))
            # ---- mode-at-null datum replay (his qsp_modeatnull_structure.py)
            if key == (41, 20, 10, 2) and mut is None:
                zs = (11, 0)
                ck("(41,20,10,2) mode-at-null: max fiber at (11,0)",
                   raw.get(zs, 0) == 133 == mx)
                ck("(41,20,10,2) mode-at-null: null = 66 (suppressed)",
                   nullf == 66)
                ck("(41,20,10,2) orbit line (mu_20*11, 0) uniform 133",
                   all(raw.get(((g * 11) % p, 0), 0) == 133 for g in D))
                ck("(41,20,10,2) argmax fiber classifier counts (0,0)",
                   c1_z.get(zs, 0) == 0 and c2_z.get(zs, 0) == 0)
                lines.append(
                    "    mode-at-null replay: null 66 -> pruned null "
                    f"{pnull} (his open item: what rung-charging does to "
                    "the (.,0) line)")
    return checks, lines, results


def main():
    all_idx = list(range(len(ROWS)))
    checks, lines, results = run(all_idx, mut=None)
    print("== pruned-Q toy packet: raw anchors + first-match pruned "
          "distributions ==")
    print("pruning ledger: C1 coset-union, then C2 dilation-stable (his toy "
          "quotient-pullback classifiers); residual = trivial-stabilizer "
          "subsets.")
    print("NOT modeled (no in-tree toy instantiation): tangent, "
          "common-support, planted, field-drop, extension, rank cells "
          "(grande_finale.tex L3561).")
    for ln in lines:
        print(ln)
    n_ok = sum(1 for _, ok, _ in checks if ok)
    main_ok = n_ok == len(checks)

    muts = ["M1_wrong_cell", "M2_depth", "M3_bound", "M4_domain"]
    caught = {}
    for mm in muts:
        try:
            mc, _, _ = run(MUT_ROWS, mut=mm)
            bad = [nm for nm, ok, _ in mc if not ok]
            caught[mm] = (len(bad) > 0,
                          f"{len(bad)} checks flipped, first: "
                          f"{bad[0] if bad else '-'}")
        except Exception as e:  # a crash is also a catch (verifier cannot PASS)
            caught[mm] = (True, f"exception: {e!r}")
    print("-- mutation controls --")
    for mm in muts:
        got, why = caught[mm]
        print(f"    {mm}: {'CAUGHT' if got else 'NOT CAUGHT'} ({why})")
    all_caught = all(v[0] for v in caught.values())

    here = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(here, "..", "data", "rowsharp_q_pruned_toy_packet.json")
    payload = dict(rows=results,
                   checks=[dict(name=n, ok=o) for n, o, _ in checks],
                   mutations={k: v[0] for k, v in caught.items()})
    if os.path.exists(data_path):
        with open(data_path) as f:
            committed = json.load(f)
        assert committed == payload, "committed data file does not match recomputation"
        print(f"committed data file MATCHES recomputation: {os.path.normpath(data_path)}")
    else:
        with open(data_path, "w") as f:
            json.dump(payload, f, indent=1)
        print(f"wrote {os.path.normpath(data_path)}")

    verdict = main_ok and all_caught
    print(f"RESULT: {'PASS' if verdict else 'FAIL'} "
          f"({n_ok}/{len(checks)} checks; "
          f"{sum(1 for v in caught.values() if v[0])}/{len(muts)} "
          f"mutation controls caught)")
    sys.exit(0 if verdict else 1)


if __name__ == "__main__":
    main()
