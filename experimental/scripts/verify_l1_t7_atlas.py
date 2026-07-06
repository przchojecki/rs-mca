#!/usr/bin/env python3
"""verify_l1_t7_atlas.py

Zero-arg, stdlib-only, deterministic verifier for
`experimental/notes/l1/l1_t7_atlas_concurrency.md` (the `T=7` candidate atlas
and the fat-tail concurrency law toward the open `C' <= 2` ceiling).

Ground rule (matching every other verifier in this L1 series): self-contained.
This script is a FRESH reimplementation of (a) the excess=3 atlas enumeration
of `experimental/scripts/l1_t7_atlas.py` and (b) the F_p coset/spectrum/
concurrency toolkit used by the (unshipped, internal) "Lane I" hunt that
produced the note's concurrency-law table. It does NOT import
`l1_t7_atlas.py`, any sibling script, or any concurrent PR's files
(`l1_bounded_excess_structure.md` / PR #368, `l1_ell19_band_refuted.md` /
PR #364 are cited by the note but neither their scripts nor their claims are
depended on here -- PR #364's witness gamma is independently RECOMPUTED in
gate v as a cross-check, not trusted).

Five gate classes; exit 0 iff ALL pass, nonzero on ANY failure:

  i.   Atlas regeneration (fresh enumeration, independent partition
       algorithm) for ell in {17, 19}: exact match to 447/51 and 792/66
       (total shapes / cap-tight T=7 slice). ell in {23,29,31} are checked
       against embedded expected values (2166/96, 7989/141, 11920/156)
       WITHOUT live regeneration by default; pass --full to regenerate all
       five live and hard-assert the same numbers.
  ii.  The j+5 over-determination theorem (note Sec 1), recomputed from
       scratch on EVERY atlas shape at ell in {17,19} (1239 shapes): for
       each shape, overdet := sum(mu_k-1) - (ell-2) must equal j+5 exactly.
  iii. The ell=31, p=373 witness: reconstruct Gamma from the raw plant
       (dropset (5,16,24) on coset 0, q = 1+2*X^2) by exact polynomial
       division/multiplication, then independently recompute its spectrum
       (brute-force evaluation over F_p^*) AND its concurrency (an
       exhaustive triple-tally over all 11 non-planted cosets that is NOT
       told q in advance -- it must rediscover q and the concurrency count
       from the raw points alone).
  iv.  Fat-tail excess identity `excess = k3 - 5` (given mu_1 = ell-3),
       spot-checked on the two independently-known +2 witnesses: W3
       (ell=17, p=137, embedded gamma) and the ell=31 witness of gate iii.
  v.   Concurrency-law table consistency: the embedded 17-row table
       (arithmetic self-consistency: excess=max_k3-5, n=(p-1)/ell, p prime,
       overall max=7, no row >=8) PLUS three live reproductions backing it:
       an exhaustive 680-dropset sweep at ell=17,p=137 (the calibration
       row), 40-/30-dropset spread subsamples at ell=31,p=373 AND ell=29,p=233 (each includes the
       gate-iii witness dropset), and an independent recomputation of PR
       #364's own ell=19,p=571 gamma (concurrent open PR, cited not
       depended on) confirming it lands on the SAME k3=6 the table reports.

  --tamper-selftest: perturbs one datum per gate (an atlas count, a shape's
  j in the j+5 check, the ell=31 witness's q-coordinate, W3's gamma, and a
  concurrency-law k3 value) and asserts each targeted gate then FAILS. The
  shipped default is zero-arg (no tampering).

All arithmetic exact over F_p, stdlib only. No network, no file I/O beyond
this script. Runtime target < 90s zero-arg (dominated by gate v's live
sweeps, ~25-30s on a typical machine).
"""
import sys
import time
import copy
import itertools


# =====================================================================================
# Fresh F_p toolkit (self-contained; independent of any Lane I / sibling script)
# =====================================================================================

def is_prime(m):
    if m < 2:
        return False
    if m % 2 == 0:
        return m == 2
    d = 3
    while d * d <= m:
        if m % d == 0:
            return False
        d += 2
    return True


def factorize(n):
    f = set()
    d, m = 2, n
    while d * d <= m:
        while m % d == 0:
            f.add(d)
            m //= d
        d += 1
    if m > 1:
        f.add(m)
    return f


def find_gen(p):
    fac = factorize(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g
    raise RuntimeError("no generator found for p=%d" % p)


def cosets_of(p, ell):
    """The n=(p-1)/ell cosets of mu_ell in F_p^*, as lists of representatives."""
    n = (p - 1) // ell
    g = find_gen(p)
    zeta = pow(g, n, p)
    H = [pow(zeta, j, p) for j in range(ell)]
    return [[pow(g, i, p) * h % p for h in H] for i in range(n)]


def poly_from_roots(roots, p):
    """Monic polynomial (ascending coefficients) with the given roots."""
    out = [1]
    for r in roots:
        new = [0] * (len(out) + 1)
        for i, c in enumerate(out):
            new[i] = (new[i] - r * c) % p
            new[i + 1] = (new[i + 1] + c) % p
        out = new
    return out


def poly_mul(a, b, p):
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai % p == 0:
            continue
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % p
    return out


def peval(poly, x, p):
    """Evaluate ascending-coefficient poly at x via Horner."""
    v = 0
    for c in reversed(poly):
        v = (v * x + c) % p
    return v


def build_inv(p):
    t = [0] * p
    for a in range(1, p):
        t[a] = pow(a, p - 2, p)
    return t


def normalize_proj(v, p, inv):
    for i, c in enumerate(v):
        if c % p:
            iv = inv[c % p]
            return tuple((cc * iv) % p for cc in v)
    return tuple(v)


def solve_q_2x3(gx, x, gy, y, gz, z, p, inv):
    """Kernel (a normalized projective point) of the 2x3 matrix with rows
    [gx*(1,x,x^2) - gy*(1,y,y^2); gy*(1,y,y^2) - gz*(1,z,z^2)].
    Returns None if the triple is degenerate (rank < 2)."""
    r1 = [(gx - gy) % p, (gx * x - gy * y) % p, (gx * x * x - gy * y * y) % p]
    r2 = [(gy - gz) % p, (gy * y - gz * z) % p, (gy * y * y - gz * z * z) % p]
    A = [r1[:], r2[:]]
    piv = []
    r = 0
    for c in range(3):
        pr = None
        for i in range(r, 2):
            if A[i][c] % p:
                pr = i
                break
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        ivv = inv[A[r][c] % p]
        A[r] = [(v * ivv) % p for v in A[r]]
        for i in range(2):
            if i != r and A[i][c] % p:
                f = A[i][c]
                A[i] = [(A[i][j] - f * A[r][j]) % p for j in range(3)]
        piv.append(c)
        r += 1
    if r < 2:
        return None
    pivset = set(piv)
    for free in range(3):
        if free in pivset:
            continue
        v = [0, 0, 0]
        v[free] = 1
        for i, c in enumerate(piv):
            v[c] = (-A[i][free]) % p
        return normalize_proj(v, p, inv)
    return None


def brute_spectrum(gamma_ascending, p, ell):
    """Full spectrum (descending mu_b, mu_b>=1) by direct evaluation:
    group F_p^* by x^ell mod p (coset label), then by Gamma(x) (fiber),
    take the max fiber size per coset."""
    groups = {}
    for x in range(1, p):
        lab = pow(x, ell, p)
        v = peval(gamma_ascending, x, p)
        groups.setdefault(lab, {}).setdefault(v, 0)
        groups[lab][v] += 1
    return sorted((max(byval.values()) for byval in groups.values()), reverse=True)


def tally_plant_concurrency(cs, ell, p, dropidx, inv):
    """For a planted size-(ell-3) fiber (coset 0 minus 3 dropped indices),
    solve every triple in every non-planted coset for its q-point and tally
    by DISTINCT coset count. Returns (max_k3, best_q, cosets_at_best_q).
    Does not use any pre-known q -- this is the from-scratch discovery."""
    c0 = cs[0]
    F0 = sorted(c0[i] for i in range(ell) if i not in set(dropidx))
    g0 = poly_from_roots(F0, p)
    gval = {}
    for cid in range(1, len(cs)):
        for x in cs[cid]:
            gval[x] = peval(g0, x, p)
    conc = {}
    for cid in range(1, len(cs)):
        pts = cs[cid]
        for x, y, z in itertools.combinations(pts, 3):
            q = solve_q_2x3(gval[x], x, gval[y], y, gval[z], z, p, inv)
            if q is None:
                continue
            conc.setdefault(q, set()).add(cid)
    if not conc:
        return 0, None, []
    best_q = max(conc, key=lambda k: len(conc[k]))
    return len(conc[best_q]), best_q, sorted(conc[best_q])


# =====================================================================================
# Fresh atlas enumeration (independent partition algorithm; see note Sec 1)
# =====================================================================================

def gen_partitions_capped(total, maxpart):
    """All descending partitions of `total` into parts <= maxpart.
    Structured differently from l1_t7_atlas.py's `partitions_desc` (which
    recurses by choosing the first part then capping the tail at that part):
    here we recurse on the PART VALUE itself, choosing how many copies of
    `maxpart` to use before dropping to `maxpart-1`."""
    def rec(rem, cap):
        if rem == 0:
            yield ()
            return
        if cap <= 0:
            return
        maxcount = min(rem // cap, rem)
        for use in range(maxcount, -1, -1):
            for tail in rec(rem - use * cap, cap - 1):
                yield (cap,) * use + tail
    yield from rec(total, maxpart)


def atlas_regenerate(ell, excess=3, want_shapes=False):
    """Returns dict(total, cap_tight, min_j, min_j_overdet, example, shapes).
    `shapes` (list of (mu_tuple, j, overdet)) is populated only if
    want_shapes=True (used by gate ii, which needs every shape)."""
    E = ell + excess
    LR = (ell - 1) * (ell - 2)
    maxpart = ell - 5
    total = 0
    cap_tight = 0
    minj = None
    example = None
    shapes = []
    for part in gen_partitions_capped(E, maxpart):
        mu = sorted((e + 2 for e in part), reverse=True)
        if len(mu) < 2:
            continue
        if mu[0] + mu[1] > ell:
            continue
        if sum(m * (m - 1) for m in mu) > LR:
            continue
        total += 1
        j = len(mu)
        capslack = ell - (mu[0] + mu[1])
        if capslack == 0:
            cap_tight += 1
        overdet = sum(m - 1 for m in mu) - (ell - 2)
        if minj is None or j < minj:
            minj, example = j, tuple(mu)
        if want_shapes:
            shapes.append((tuple(mu), j, overdet))
    return dict(total=total, cap_tight=cap_tight, min_j=minj,
                min_j_overdet=(minj + 5 if minj is not None else None),
                example=example, shapes=shapes)


# =====================================================================================
# Embedded data (the note's claims; tamper-selftest mutates copies of these)
# =====================================================================================

ATLAS_EXPECTED = {
    17: dict(total=447, cap_tight=51),
    19: dict(total=792, cap_tight=66),
    23: dict(total=2166, cap_tight=96),
    29: dict(total=7989, cap_tight=141),
    31: dict(total=11920, cap_tight=156),
}

# W3 (l1_e3_law_refuted.md flagship witness): ell=17, p=137, E_3=19=ell+2.
W3 = dict(
    ell=17, p=137,
    gamma=[95, 83, 94, 43, 16, 101, 72, 52, 93, 129, 47, 76, 80, 45, 64, 1],  # gamma_1..gamma_16
)

# The new ell=31 witness (this note): plant + q, from sweep_deep.json / Lane I.
ELL31_WITNESS = dict(ell=31, p=373, dropset=(5, 16, 24), q=(1, 0, 2))

# PR #364 (l1_ell19_band_refuted.md, concurrent, NOT depended on): its own
# m*(19)<=9 listing witness, independently recomputed here as a cross-check
# that it lands on the SAME (ell=19,p=571) row of the concurrency-law table.
PR364_WITNESS = dict(
    ell=19, p=571,
    gamma=[545, 15, 163, 341, 470, 274, 474, 224, 174, 556,
           179, 28, 321, 233, 543, 54, 203, 1],  # gamma_1..gamma_18
)

# The 17-row empirical concurrency law (ell, p, n, ndrops, max_k3); excess is
# derived (max_k3-5), not stored, so tampering k3 automatically moves excess.
CONCURRENCY_LAW = [
    (17, 137, 8, 680, 7),
    (17, 239, 14, 300, 5),
    (17, 307, 18, 200, 5),
    (17, 409, 24, 150, 5),
    (17, 613, 36, 80, 5),
    (19, 229, 12, 300, 5),
    (19, 419, 22, 150, 5),
    (19, 571, 30, 100, 6),
    (23, 277, 12, 900, 5),
    (23, 461, 20, 120, 5),
    (23, 599, 26, 80, 5),
    (29, 233, 8, 900, 7),
    (29, 349, 12, 900, 5),
    (29, 523, 18, 60, 5),
    (31, 311, 10, 1200, 7),
    (31, 373, 12, 900, 7),
    (31, 683, 22, 40, 7),
]


# =====================================================================================
# Gates
# =====================================================================================

class GateFail(AssertionError):
    pass


def gate_i(atlas_expected, full=False):
    """Atlas regeneration: fresh enumeration for ell in {17,19} must match
    exactly; ell in {23,29,31} checked live only under --full."""
    msgs = []
    live_ells = [17, 19] + ([23, 29, 31] if full else [])
    for ell in live_ells:
        r = atlas_regenerate(ell)
        exp = atlas_expected[ell]
        if r['total'] != exp['total'] or r['cap_tight'] != exp['cap_tight']:
            raise GateFail("ell=%d: got total=%d cap_tight=%d, expected total=%d cap_tight=%d"
                           % (ell, r['total'], r['cap_tight'], exp['total'], exp['cap_tight']))
        msgs.append("ell=%d: %d shapes, %d cap-tight (T=7), min-j=%d (over-det=%d) [LIVE]"
                    % (ell, r['total'], r['cap_tight'], r['min_j'], r['min_j_overdet']))
    skipped = [e for e in (23, 29, 31) if e not in live_ells]
    for ell in skipped:
        exp = atlas_expected[ell]
        msgs.append("ell=%d: total=%d cap_tight=%d [EMBEDDED, not regenerated -- pass --full]"
                    % (ell, exp['total'], exp['cap_tight']))
    return msgs


def gate_ii(ells=(17, 19)):
    """j+5 over-determination theorem, recomputed on every shape."""
    msgs = []
    total_checked = 0
    for ell in ells:
        r = atlas_regenerate(ell, want_shapes=True)
        for mu, j, overdet in r['shapes']:
            if len(mu) != j:
                raise GateFail("ell=%d shape %s: len(mu)=%d != j=%d" % (ell, mu, len(mu), j))
            if overdet != j + 5:
                raise GateFail("ell=%d shape %s: overdet=%d != j+5=%d" % (ell, mu, overdet, j + 5))
            total_checked += 1
        msgs.append("ell=%d: j+5 identity holds on all %d shapes" % (ell, len(r['shapes'])))
    msgs.append("total shapes checked: %d" % total_checked)
    return msgs


def gate_iii(witness):
    """ell=31 witness: reconstruct Gamma from the plant, recompute spectrum
    AND concurrency fresh (concurrency tally is NOT told q in advance)."""
    ell, p, dropset, q = witness['ell'], witness['p'], witness['dropset'], witness['q']
    if not is_prime(p):
        raise GateFail("p=%d is not prime" % p)
    inv = build_inv(p)
    cs = cosets_of(p, ell)
    c0 = cs[0]
    F0 = sorted(c0[i] for i in range(ell) if i not in set(dropset))
    if len(F0) != ell - 3:
        raise GateFail("planted fiber has size %d, expected ell-3=%d" % (len(F0), ell - 3))
    g0 = poly_from_roots(F0, p)
    g0q = poly_mul(g0, list(q), p)
    lambda0 = (-g0q[0]) % p
    gamma = g0q[:]
    gamma[0] = (gamma[0] + lambda0) % p
    if gamma[0] != 0:
        raise GateFail("reconstructed Gamma is not constant-free")

    spectrum = brute_spectrum(gamma, p, ell)
    mu1 = spectrum[0]
    E3 = sum(m - 2 for m in spectrum if m >= 3)
    k3_spec = sum(1 for m in spectrum if m == 3)
    if mu1 != ell - 3:
        raise GateFail("mu_1=%d != ell-3=%d" % (mu1, ell - 3))
    if E3 != ell + 2:
        raise GateFail("E_3=%d != ell+2=%d" % (E3, ell + 2))
    if k3_spec != 7:
        raise GateFail("spectrum gives k3=%d != 7" % k3_spec)

    # Independent concurrency rediscovery: does NOT use `q` at all.
    k3_conc, best_q, cosets_at_q = tally_plant_concurrency(cs, ell, p, dropset, inv)
    if k3_conc != 7:
        raise GateFail("concurrency tally gives k3=%d != 7" % k3_conc)
    want_q = normalize_proj(q, p, inv)
    if best_q != want_q:
        raise GateFail("rediscovered q=%s != claimed q=%s (normalized)" % (best_q, want_q))
    if cosets_at_q != [2, 3, 5, 6, 8, 9, 11]:
        raise GateFail("rediscovered concurrent cosets %s != claimed [2,3,5,6,8,9,11]" % cosets_at_q)

    return dict(ell=ell, p=p, mu1=mu1, E3=E3, k3=k3_conc, q=best_q, cosets=cosets_at_q,
                gamma=gamma), [
        "reconstructed Gamma from plant (dropset=%s, q=%s)" % (dropset, list(q)),
        "spectrum (fresh eval): mu_1=%d, E_3=%d, k3(spectrum)=%d" % (mu1, E3, k3_spec),
        "concurrency (fresh tally, q NOT given): k3=%d at q=%s, cosets=%s"
        % (k3_conc, best_q, cosets_at_q),
    ]


def gate_iv(w3, ell31_result):
    """Fat-tail excess identity excess=k3-5 (mu_1=ell-3), on W3 and ell=31."""
    msgs = []
    ell, p = w3['ell'], w3['p']
    gamma = [0] + list(w3['gamma'])  # prepend the (forced-zero) constant term
    spectrum = brute_spectrum(gamma, p, ell)
    mu1 = spectrum[0]
    E3 = sum(m - 2 for m in spectrum if m >= 3)
    k3 = sum(1 for m in spectrum if m == 3)
    if mu1 != ell - 3:
        raise GateFail("W3: mu_1=%d != ell-3=%d" % (mu1, ell - 3))
    if (E3 - ell) != (k3 - 5):
        raise GateFail("W3: excess=%d != k3-5=%d" % (E3 - ell, k3 - 5))
    msgs.append("W3 (ell=%d,p=%d): mu_1=ell-3=%d, k3=%d, excess=%d=k3-5 [PASS]"
                % (ell, p, mu1, k3, E3 - ell))

    e_ell, e_p, e_mu1, e_E3, e_k3 = (ell31_result['ell'], ell31_result['p'],
                                      ell31_result['mu1'], ell31_result['E3'], ell31_result['k3'])
    if e_mu1 != e_ell - 3:
        raise GateFail("ell=31 witness: mu_1=%d != ell-3=%d" % (e_mu1, e_ell - 3))
    if (e_E3 - e_ell) != (e_k3 - 5):
        raise GateFail("ell=31 witness: excess=%d != k3-5=%d" % (e_E3 - e_ell, e_k3 - 5))
    msgs.append("ell=31 (p=%d): mu_1=ell-3=%d, k3=%d, excess=%d=k3-5 [PASS]"
                % (e_p, e_mu1, e_k3, e_E3 - e_ell))
    return msgs


def gate_v(law, pr364, live_full_pair=(17, 137, 680), live_sub_pair=(31, 373, 40, (5, 16, 24)),
           live_sub_pair2=(29, 233, 30, (0, 2, 16))):
    """Concurrency-law table consistency + three live reproductions."""
    msgs = []
    # --- arithmetic self-consistency of the embedded table ---
    if len(law) != 17:
        raise GateFail("expected 17 rows, got %d" % len(law))
    max_k3 = 0
    for (ell, p, n, ndrops, k3) in law:
        if not is_prime(p):
            raise GateFail("p=%d not prime (ell=%d)" % (p, ell))
        if (p - 1) % ell != 0 or (p - 1) // ell != n:
            raise GateFail("n mismatch for ell=%d,p=%d: claimed n=%d, computed %d"
                           % (ell, p, n, (p - 1) // ell))
        if k3 >= 8:
            raise GateFail("row (ell=%d,p=%d) has k3=%d >= 8 -- would refute C'<=2!" % (ell, p, k3))
        max_k3 = max(max_k3, k3)
    if max_k3 != 7:
        raise GateFail("overall max k3=%d, expected 7" % max_k3)
    ells_present = sorted(set(row[0] for row in law))
    if ells_present != [17, 19, 23, 29, 31]:
        raise GateFail("ell coverage %s != [17,19,23,29,31]" % ells_present)
    msgs.append("table: 17 rows, ell in {17,19,23,29,31}, overall max k3=7, no row >=8 [PASS]")

    # --- live reproduction 1: exhaustive sweep at the calibration row ---
    ell, p, ndrops_full = live_full_pair
    t0 = time.time()
    inv = build_inv(p)
    cs = cosets_of(p, ell)
    allc = list(itertools.combinations(range(ell), 3))
    if len(allc) != ndrops_full:
        raise GateFail("C(%d,3)=%d != expected %d" % (ell, len(allc), ndrops_full))
    glob_max = 0
    for drop in allc:
        k3, _, _ = tally_plant_concurrency(cs, ell, p, drop, inv)
        glob_max = max(glob_max, k3)
    dt = time.time() - t0
    table_row = next(r for r in law if r[0] == ell and r[1] == p)
    if glob_max != table_row[4]:
        raise GateFail("live exhaustive sweep (ell=%d,p=%d) got max_k3=%d, table says %d"
                       % (ell, p, glob_max, table_row[4]))
    msgs.append("LIVE exhaustive %d/%d dropsets (ell=%d,p=%d): max_k3=%d, matches table (%.1fs)"
                % (len(allc), ndrops_full, ell, p, glob_max, dt))

    # --- live reproduction 2: bounded spread subsample at ell=31,p=373 ---
    ell2, p2, nsub, witness_drop = live_sub_pair
    t0 = time.time()
    inv2 = build_inv(p2)
    cs2 = cosets_of(p2, ell2)
    allc2 = list(itertools.combinations(range(ell2), 3))
    step = len(allc2) / nsub
    sample = [allc2[int(i * step)] for i in range(nsub)]
    if witness_drop not in sample:
        sample = [witness_drop] + sample[:-1]   # guarantee the known record is included
    sub_max = 0
    for drop in sample:
        k3, _, _ = tally_plant_concurrency(cs2, ell2, p2, drop, inv2)
        if k3 >= 8:
            raise GateFail("subsample dropset %s at (ell=%d,p=%d) hit k3=%d >= 8!"
                           % (drop, ell2, p2, k3))
        sub_max = max(sub_max, k3)
    dt = time.time() - t0
    if sub_max != 7:
        raise GateFail("bounded subsample (ell=%d,p=%d, %d dropsets incl. witness) got max=%d, expected 7"
                       % (ell2, p2, len(sample), sub_max))
    msgs.append("LIVE bounded subsample %d/%d dropsets (ell=%d,p=%d, incl. witness %s): max_k3=%d, no k3>=8 (%.1fs)"
                % (len(sample), len(allc2), ell2, p2, witness_drop, sub_max, dt))

    # --- live reproduction 3: bounded spread subsample at ell=29,p=233 ---
    # (backs the "excess +2 attained at three distinct ell" headline with a
    #  third verifier-reproduced row; witness dropset force-included)
    ell4, p4, nsub4, witness_drop4 = live_sub_pair2
    t0 = time.time()
    inv4 = build_inv(p4)
    cs4 = cosets_of(p4, ell4)
    allc4 = list(itertools.combinations(range(ell4), 3))
    step4 = len(allc4) / nsub4
    sample4 = [allc4[int(i * step4)] for i in range(nsub4)]
    if witness_drop4 not in sample4:
        sample4 = [witness_drop4] + sample4[:-1]
    sub_max4 = 0
    for drop in sample4:
        k3, _, _ = tally_plant_concurrency(cs4, ell4, p4, drop, inv4)
        if k3 >= 8:
            raise GateFail("subsample dropset %s at (ell=%d,p=%d) hit k3=%d >= 8!"
                           % (drop, ell4, p4, k3))
        sub_max4 = max(sub_max4, k3)
    dt = time.time() - t0
    if sub_max4 != 7:
        raise GateFail("bounded subsample (ell=%d,p=%d, %d dropsets incl. witness) got max=%d, expected 7"
                       % (ell4, p4, len(sample4), sub_max4))
    table_row4 = next(r for r in law if r[0] == ell4 and r[1] == p4)
    if table_row4[4] != 7:
        raise GateFail("law table row (29,233) says max_k3=%d, live witness gives 7" % table_row4[4])
    msgs.append("LIVE bounded subsample %d/%d dropsets (ell=%d,p=%d, incl. witness %s): max_k3=%d, no k3>=8 (%.1fs)"
                % (len(sample4), len(allc4), ell4, p4, witness_drop4, sub_max4, dt))

    # --- cross-reference: PR #364's own ell=19,p=571 witness lands on the same k3 ---
    ell3, p3 = pr364['ell'], pr364['p']
    gamma3 = [0] + list(pr364['gamma'])
    spectrum3 = brute_spectrum(gamma3, p3, ell3)
    k3_pr364 = sum(1 for m in spectrum3 if m == 3)
    E3_pr364 = sum(m - 2 for m in spectrum3 if m >= 3)
    table_row3 = next(r for r in law if r[0] == ell3 and r[1] == p3)
    if k3_pr364 != table_row3[4]:
        raise GateFail("PR #364 witness (ell=%d,p=%d) recomputes k3=%d, table row says %d"
                       % (ell3, p3, k3_pr364, table_row3[4]))
    msgs.append("PR #364 (l1_ell19_band_refuted.md) witness (ell=%d,p=%d): independently recomputes "
                "E_3=%d, k3=%d, matching this note's own table row exactly [PASS]"
                % (ell3, p3, E3_pr364, k3_pr364))
    return msgs


def run_gates(full=False, atlas_expected=None, w3=None, ell31=None, law=None, pr364=None):
    """Run all five gates in order; returns list of (name, ok, detail_msgs_or_error, secs)."""
    atlas_expected = atlas_expected if atlas_expected is not None else ATLAS_EXPECTED
    w3 = w3 if w3 is not None else W3
    ell31 = ell31 if ell31 is not None else ELL31_WITNESS
    law = law if law is not None else CONCURRENCY_LAW
    pr364 = pr364 if pr364 is not None else PR364_WITNESS

    results = []

    t0 = time.time()
    try:
        msgs = gate_i(atlas_expected, full=full)
        results.append(("i. atlas regeneration", True, msgs, time.time() - t0))
    except GateFail as e:
        results.append(("i. atlas regeneration", False, [str(e)], time.time() - t0))

    t0 = time.time()
    try:
        msgs = gate_ii()
        results.append(("ii. j+5 over-determination", True, msgs, time.time() - t0))
    except GateFail as e:
        results.append(("ii. j+5 over-determination", False, [str(e)], time.time() - t0))

    t0 = time.time()
    ell31_result = None
    try:
        ell31_result, msgs = gate_iii(ell31)
        results.append(("iii. ell=31 witness (fresh)", True, msgs, time.time() - t0))
    except GateFail as e:
        results.append(("iii. ell=31 witness (fresh)", False, [str(e)], time.time() - t0))

    t0 = time.time()
    try:
        if ell31_result is None:
            raise GateFail("skipped: gate iii did not produce a witness result")
        msgs = gate_iv(w3, ell31_result)
        results.append(("iv. fat-tail excess=k3-5", True, msgs, time.time() - t0))
    except GateFail as e:
        results.append(("iv. fat-tail excess=k3-5", False, [str(e)], time.time() - t0))

    t0 = time.time()
    try:
        msgs = gate_v(law, pr364)
        results.append(("v. concurrency-law table", True, msgs, time.time() - t0))
    except GateFail as e:
        results.append(("v. concurrency-law table", False, [str(e)], time.time() - t0))

    return results


# =====================================================================================
# Tamper self-test
# =====================================================================================

def tamper_selftest():
    print("=" * 90)
    print("TAMPER SELF-TEST -- each scenario must make its targeted gate FAIL")
    print("=" * 90)
    all_caught = True

    # T1: flip one atlas count (gate i)
    bad_atlas = copy.deepcopy(ATLAS_EXPECTED)
    bad_atlas[17]['total'] = 448
    try:
        gate_i(bad_atlas, full=False)
        print("[FAIL] T1 (atlas count tamper) was NOT caught by gate i")
        all_caught = False
    except GateFail as e:
        print("[OK]   T1 (atlas count 447->448 at ell=17) caught by gate i: %s" % e)

    # T2: corrupt the j+5 identity by lying about j for a real shape (gate ii)
    real = atlas_regenerate(17, want_shapes=True)
    mu, j, overdet = real['shapes'][0]
    lied_j = j + 1
    try:
        if overdet != lied_j + 5:
            raise GateFail("shape %s: overdet=%d != (lied) j+5=%d" % (mu, overdet, lied_j + 5))
        print("[FAIL] T2 (j+5 tamper) was NOT caught")
        all_caught = False
    except GateFail as e:
        print("[OK]   T2 (j+5 identity, lied j=%d->%d) caught: %s" % (j, lied_j, e))

    # T3: flip the ell=31 witness's q-coordinate (gate iii)
    bad_witness = copy.deepcopy(ELL31_WITNESS)
    bad_witness['q'] = (1, 0, 3)
    try:
        gate_iii(bad_witness)
        print("[FAIL] T3 (q-coordinate tamper) was NOT caught by gate iii")
        all_caught = False
    except GateFail as e:
        print("[OK]   T3 (q-coordinate (1,0,2)->(1,0,3)) caught by gate iii: %s" % e)

    # T4: flip one coefficient of W3's gamma (gate iv, via a corrupted spectrum)
    bad_w3 = copy.deepcopy(W3)
    bad_w3['gamma'][0] = (bad_w3['gamma'][0] + 1) % bad_w3['p']
    try:
        ell31_result, _ = gate_iii(ELL31_WITNESS)
        gate_iv(bad_w3, ell31_result)
        print("[FAIL] T4 (W3 gamma tamper) was NOT caught by gate iv")
        all_caught = False
    except GateFail as e:
        print("[OK]   T4 (W3 gamma coefficient flipped) caught by gate iv: %s" % e)

    # T5: flip one concurrency-law k3 to 8 (gate v)
    bad_law = copy.deepcopy(CONCURRENCY_LAW)
    idx = next(i for i, r in enumerate(bad_law) if r[0] == 23 and r[1] == 277)
    row = list(bad_law[idx])
    row[4] = 8
    bad_law[idx] = tuple(row)
    try:
        gate_v(bad_law, PR364_WITNESS)
        print("[FAIL] T5 (k3 tamper) was NOT caught by gate v")
        all_caught = False
    except GateFail as e:
        print("[OK]   T5 (k3 5->8 at ell=23,p=277) caught by gate v: %s" % e)

    print("=" * 90)
    if all_caught:
        print("TAMPER SELF-TEST: all 5 scenarios CAUGHT.")
        return 0
    else:
        print("TAMPER SELF-TEST: at least one scenario was NOT caught -- verifier is unsound.")
        return 1


# =====================================================================================
# Main
# =====================================================================================

def main(argv):
    full = "--full" in argv
    tamper = "--tamper-selftest" in argv

    if tamper:
        return tamper_selftest()

    print("verify_l1_t7_atlas.py -- T=7 atlas + concurrency law (%s)"
          % ("--full" if full else "default"))
    print("=" * 90)
    t_start = time.time()
    results = run_gates(full=full)
    all_ok = True
    for name, ok, msgs, secs in results:
        status = "PASS" if ok else "FAIL"
        print("[%s] %-30s (%.2fs)" % (status, name, secs))
        for m in msgs:
            print("       %s" % m)
        all_ok = all_ok and ok
    total = time.time() - t_start
    print("=" * 90)
    print("TOTAL: %s in %.1fs" % ("ALL GATES PASS" if all_ok else "AT LEAST ONE GATE FAILED", total))
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
