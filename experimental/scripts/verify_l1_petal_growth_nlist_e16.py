#!/usr/bin/env python3
"""verify_l1_petal_growth_nlist_e16.py

Zero-arg, stdlib-only verifier for the E16 petal-growth `N_list(7,p)` packet.

Repo target for the companion note: experimental/notes/l1/l1_petal_growth_nlist_e16.md
Repo target for this verifier:      experimental/scripts/verify_l1_petal_growth_nlist_e16.py

WHAT THIS CHECKS (eight gate classes, run in this order):

  0. TAMPER SELF-TEST (negative AND positive controls). Before trusting any
     gate below, each gate's comparison logic is first exercised against a
     DELIBERATELY corrupted copy of its own reference data (must FAIL) or,
     for gate 4 / the monomial-scan and capture-rate detectors (whose real
     run is expected to find nothing), against a DELIBERATELY planted known
     hit fed through the real detector function (must FIND it). This proves
     the gates actually discriminate rather than being vacuously true in
     either direction. If any control does not behave as required, the whole
     script exits nonzero.

  1. FIT GATE. Recomputes the log-log least-squares exponent of
     `N_list(7,p)` vs `p` from the embedded 6-prime reference table (the
     table itself is NOT recomputed here, only the arithmetic of the fit --
     see gate 2 for the expensive from-scratch recomputation and gate 5 for
     a cheap tight-tolerance cross-check that covers all 6 stored entries),
     and checks it reproduces the two headline exponents recorded in
     `D_nlist_note.md` / `D_nlist.json`: slope=+0.768 (all 6 points) and
     slope=-0.071 (excluding p=71, the small-n boundary point). NOTE: at its
     documented 5e-3 slope tolerance this gate alone provides near-zero
     protection against a small per-entry drift (e.g. a table value off by
     +1..+8) on any ONE of the 6 stored entries -- do not treat "fit gate
     passes" as validating individual table entries; gates 2 and 5 do that.

  2. RECOMPUTE GATE (the expensive one). Recomputes `N_list(7,p)` FROM
     SCRATCH, by the same "2-seed, let the top-5 emerge" construction +
     exact orbit correction as `D_lib3.two_seed_census` (ported below,
     self-contained -- no import from the wave_t1 scratch tree), at THREE
     primes chosen for CI speed: p=71 (n=10 cosets, full/uncapped sweep,
     ~2s), p=113 (n=16 cosets, full/uncapped sweep, ~8s), and p=127 (n=18
     cosets, full/uncapped sweep, ~11s). All three are run FULL (no capping
     of the documented gap-range / pattern-pair scope -- capping was not
     needed to hit the <120s target; see timing printed at the end). Gates
     the recomputed value against the stored table to floating-point
     tolerance. CAVEAT: this recomputation is a port of the same
     `D_lib3.two_seed_census` algorithm the original wave_t1 measurement
     used (see the Section-0 docstring below), not an independently
     designed method -- it reliably catches transcription/copy-paste drift
     between the stored table and its source, but cannot catch a bug present
     identically in both (no CAS is available in this stdlib-only
     environment for a truly independent recomputation).

  3. ORBIT-CORRECTION LEMMA GATE. Independently re-derives (does not just
     re-assert) the orbit-correction lemma on TWO concrete witnesses pulled
     from the gate-2 recomputation at p=71: one on a "periodic" config
     (gaps all equal to n/5 -- the case the note flags as needing the
     rare-exception language) and one on a generic (non-periodic) config.
     For each, it explicitly constructs all n shift-images
     `gamma_r -> gamma_r * g^{kr}` (k=0..n-1), recomputes each image's own
     HONEST full n-coset spectrum from scratch, and checks by direct count
     that (a) the true (config,gamma)-pair orbit has exactly n distinct
     members (not n/5, even on the periodic-config instance -- see note sec
     2.3 "audit finding") and (b) exactly `c` of the n images have coset 0
     landing on one of that image's own fiber>=3 cosets, where `c` is the
     recorded c_elevated value. This is a from-scratch reconstruction of the
     lemma's counting claim, not a re-statement of the formula.

  4. CAPTURE-RATE GATE (reduced, documented, seeded replica). Reproduces the
     qualitative capture-rate finding (random/unplanted 2-dim slices of
     gamma-space find ~0 threshold-crossing witnesses) at REDUCED scope vs
     the original D_capture_rate.py run (3 hit configs + 2 non-hit configs x
     60 random slices each = 300 slices x 72 points/slice = 21,600 points,
     vs the original's 14 configs x 200 slices = 201,600 points) -- fully
     documented as a reduced-scope CI-speed replica, seeded for
     reproducibility (random.seed(20260704)).

  5. HISTOGRAM-CONSISTENCY GATE (cheap, covers ALL 6 stored entries, tight
     tolerance). The note's own Data table (sec 4) records, for every prime,
     both `N_list` AND the underlying `c`-histogram (how many raw witnesses
     have c_elevated=3 vs 4) the orbit-correction sum was built from. This
     gate independently re-derives `N_list = n * sum_c hist[c]/c` from that
     SECOND, already-published piece of the same census and checks it
     against the stored `N_list` at 1e-6 tolerance for all 6 primes -- not
     just the 2-3 gate-2 recomputes. This closes the gap gate 1 leaves open:
     a single-entry drift on ANY of the 6 stored values (e.g. p=197, 211, or
     337, none of which gate 2 recomputes) is now caught unless the
     histogram was tampered in lockstep with it.

  6. MONOMIAL-SCAN GATE (extends the sec 7 "0/1092" audit). Scans every raw
     witness gamma_norm produced by gate 2's from-scratch recomputation
     (all primes gate 2 actually recomputes: p=71,113,127, i.e. 673 of the
     note's 1092 census witnesses) for the monomial exception the sec 7
     exact-orbit-size lemma excludes. Reproduces (does not just re-assert)
     the "0 monomial gamma found" claim for this reproducible subset; the
     remaining primes (197,211,337, 419 more witnesses) are NOT re-scanned
     here (too expensive to recompute from scratch in this verifier's time
     budget) and the note/pr_body flag this scope explicitly.

  7. HEADLINE-NUMBERS GATE (re-derives narrative NUMERIC figures). Directly
     recomputes, from the same embedded 6-prime table gate 1 uses, three
     plain-arithmetic figures the note's prose quotes (337**14 and how many
     orders of magnitude it is above the stored p=337 entry; the max/min
     prime-range ratio among the 5 non-p71 points; the first
     consecutive-pair log-log exponent 71->113) and checks them against the
     corrected values. These are cheap sanity checks added after a packet
     audit found the previous prose had drifted from the table on all three
     (a copy/rounding-type error, not a data error).

Overall: exit 0 and print a summary iff every gate (0-7) passes. Exit 1 (and
print which gate failed) on ANY failure. No CLI arguments are read or
required; no network access; no third-party imports (stdlib only:
sys/time/random/itertools/math).
"""
import sys
import time
import math
import random
import itertools

# =============================================================================
# Section 0: ported library (self-contained port of D_s1_lib_copy.py's
# GenPowerCosets/rref_nullspace/all_fiber_patterns/fiber_rows and
# D_lib2.py's normalize_gamma/enumerate_and_check_dim2_fast and
# D_lib3.py's full_spectrum_dim2_fast/two_seed_census -- audited against the
# originals in wave_t1/D_audit.py before this port was written; ported here,
# rather than imported via sys.path, so this verifier has zero path
# dependency outside this one file).
# =============================================================================


def factorize(n):
    fac = set()
    d = 2
    m = n
    while d * d <= m:
        while m % d == 0:
            fac.add(d)
            m //= d
        d += 1
    if m > 1:
        fac.add(m)
    return fac


def find_generator(p):
    """Smallest primitive root mod p."""
    fac = factorize(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g
    raise RuntimeError(f"no generator found for p={p}")


class GenPowerCosets:
    """Cosets b_i*H, b_i = g^i, i=0..n-1, n=(p-1)/ell.  H = mu_ell."""

    def __init__(self, p, ell):
        assert (p - 1) % ell == 0
        self.p = p
        self.ell = ell
        self.dim = ell - 1
        self.g = find_generator(p)
        self.n = (p - 1) // ell
        self.zeta = pow(self.g, self.n, p)
        assert pow(self.zeta, ell, p) == 1 and self.zeta != 1
        self.reps = [pow(self.g, i, p) for i in range(self.n)]
        self.H = [pow(self.zeta, j, p) for j in range(ell)]
        Vpow = []
        for b in self.reps:
            row = []
            for h in self.H:
                x = b * h % p
                powers = []
                xr = 1
                for _r in range(1, ell):
                    xr = xr * x % p
                    powers.append(xr)
                row.append(tuple(powers))
            Vpow.append(row)
        self.Vpow = Vpow  # Vpow[i][j][r-1] = (b_i*H[j])^r


def rref_nullspace(rows, ncols, p):
    """Gaussian elimination over F_p; returns (rank, basis), basis vectors
    self-verified directly against A@v=0 mod p before being returned."""
    A = [list(r) for r in rows]
    m = len(A)
    piv_cols = []
    r = 0
    for c in range(ncols):
        pr = None
        for i in range(r, m):
            if A[i][c] % p:
                pr = i
                break
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [(v * inv) % p for v in A[r]]
        for i in range(m):
            if i != r and A[i][c] % p:
                f = A[i][c]
                A[i] = [(A[i][j] - f * A[r][j]) % p for j in range(ncols)]
        piv_cols.append(c)
        r += 1
        if r == m:
            break
    rank = r
    pivset = set(piv_cols)
    basis = []
    for free in range(ncols):
        if free in pivset:
            continue
        v = [0] * ncols
        v[free] = 1
        for i, c in enumerate(piv_cols):
            v[c] = (-A[i][free]) % p
        basis.append(v)
    for v in basis:
        for row in rows:
            s = sum((row[k] * v[k]) for k in range(ncols)) % p
            if s != 0:
                raise AssertionError("nullspace basis vector fails direct A@v=0 check")
    assert rank == ncols - len(basis)
    return rank, basis


def all_fiber_patterns(ell, nu):
    return [(0,) + combo for combo in itertools.combinations(range(1, ell), nu - 1)]


def fiber_rows(gpc, coset_index, pattern, p):
    dim = gpc.dim
    row0 = gpc.Vpow[coset_index][pattern[0]]
    rows = []
    for e in pattern[1:]:
        rowe = gpc.Vpow[coset_index][e]
        rows.append([(row0[r] - rowe[r]) % p for r in range(dim)])
    return rows


def normalize_gamma(gamma, p):
    """Projective normalization: scale so the first nonzero coordinate is 1."""
    for v in gamma:
        vv = v % p
        if vv:
            inv = pow(vv, p - 2, p)
            return tuple((c * inv) % p for c in gamma)
    return tuple(gamma)


def honest_full_spectrum(gamma, gpc):
    """Per-coset max-fiber array (length n), NOT sorted -- index i = coset i's
    own max fiber under this gamma.  O(n*ell) dot products."""
    n, dim, p = gpc.n, gpc.dim, gpc.p
    spec = []
    for i in range(n):
        counts = {}
        for powers in gpc.Vpow[i]:
            v = 0
            for r in range(dim):
                gr = gamma[r]
                if gr:
                    v += gr * powers[r]
            v %= p
            counts[v] = counts.get(v, 0) + 1
        spec.append(max(counts.values()))
    return spec


def top5_of_spectrum(spec):
    order = sorted(range(len(spec)), key=lambda i: (-spec[i], i))
    return tuple(sorted(order[:5]))


def full_spectrum_dim2_fast(v1, v2, gpc, p, threshold):
    """2-dim family spanned by v1,v2: exact full p+1-point projective-line
    scan, honest full n-coset spectrum via the precompute-(a,b)-then-affine-
    update speedup.  Yields (cand_gamma, top5_configs_tuple, top5_sum,
    c_elevated) for every member whose top-5 sum >= threshold."""
    n, dim = gpc.n, gpc.dim
    precomp = []
    for i in range(n):
        ab = []
        for powers in gpc.Vpow[i]:
            a = sum(x * y for x, y in zip(v1, powers)) % p
            b = sum(x * y for x, y in zip(v2, powers)) % p
            ab.append((a, b))
        precomp.append(ab)

    def eval_t(t, is_inf):
        per_coset = []
        for ab in precomp:
            counts = {}
            for a, b in ab:
                v = b if is_inf else (a + t * b) % p
                counts[v] = counts.get(v, 0) + 1
            per_coset.append(max(counts.values()))
        order = sorted(range(n), key=lambda i: (-per_coset[i], i))
        top5 = tuple(sorted(order[:5]))
        s = sum(per_coset[i] for i in top5)
        c_elev = sum(1 for i in top5 if per_coset[i] >= 3)
        return s, top5, c_elev

    for t in range(p):
        s, top5, c_elev = eval_t(t, False)
        if s >= threshold:
            cand = [(v1[k] + t * v2[k]) % p for k in range(dim)]
            yield cand, top5, s, c_elev
    s, top5, c_elev = eval_t(None, True)
    if s >= threshold:
        yield list(v2), top5, s, c_elev


def two_seed_census(gpc, p, ell, threshold):
    """Full 2-seed construction sweep, FULL/uncapped gap range (1..n-1) and
    ALL 15x15=225 pattern pairs -- identical scope to D_lib3.two_seed_census.
    Returns (witness_dict, stats); witness_dict maps
    (config_tuple, normalized_gamma_tuple) -> c_elevated."""
    n = gpc.n
    pat3 = all_fiber_patterns(ell, 3)
    pattern_pairs = [(p0, p1) for p0 in pat3 for p1 in pat3]
    witnesses = {}
    n_combos = 0
    dim_hist = {}
    off_path_seen = 0
    for gap in range(1, n):
        rows0_by_pat = {pt: fiber_rows(gpc, 0, pt, p) for pt in pat3}
        rowsg_by_pat = {pt: fiber_rows(gpc, gap, pt, p) for pt in pat3}
        for pat0, pat1 in pattern_pairs:
            n_combos += 1
            rows = rows0_by_pat[pat0] + rowsg_by_pat[pat1]
            rank, basis = rref_nullspace(rows, gpc.dim, p)
            if not basis:
                continue
            dim_hist[len(basis)] = dim_hist.get(len(basis), 0) + 1
            if len(basis) == 2:
                for cand, top5, s, c_elev in full_spectrum_dim2_fast(basis[0], basis[1], gpc, p, threshold):
                    key = (top5, normalize_gamma(cand, p))
                    if key not in witnesses:
                        witnesses[key] = c_elev
            else:
                # off-path (dim!=2): not exercised at ell=7 in the original
                # census (off_path_seen=0 at all 6 tested primes) -- counted
                # here defensively but not expected to fire.
                off_path_seen += 1
    stats = dict(n_combos=n_combos, dim_hist=dim_hist, off_path_seen=off_path_seen)
    return witnesses, stats


def shift_gamma(gamma, k, g, p, dim):
    """gamma_r -> gamma_r * (g^k)^r = gamma_r * g^{k*r}, r=1..dim (gamma[r-1]
    holds the exponent-r coefficient)."""
    return tuple((gamma[r] * pow(g, k * (r + 1), p)) % p for r in range(dim))


def enumerate_and_check_dim2_fast_random(v1, v2, gpc, config, p, threshold):
    """EXACT full projective-line scan (p+1 points) of the 2-dim family
    v1,v2, evaluated ONLY on the 5 cosets in `config` (cheap, honest).
    Returns the set of normalized gammas (within this family) reaching
    top-of-config-sum >= threshold on THIS SPECIFIC fixed config (used for
    the capture-rate replica: config is fixed, v1/v2 are random, not
    planted)."""
    dim = gpc.dim
    precomp = []
    for ci in config:
        ab = []
        for powers in gpc.Vpow[ci]:
            a = sum(x * y for x, y in zip(v1, powers)) % p
            b = sum(x * y for x, y in zip(v2, powers)) % p
            ab.append((a, b))
        precomp.append(ab)
    hits = set()
    for t in range(p):
        total = 0
        for ab in precomp:
            counts = {}
            for a, b in ab:
                v = (a + t * b) % p
                counts[v] = counts.get(v, 0) + 1
            total += max(counts.values())
        if total >= threshold:
            cand = [(v1[k] + t * v2[k]) % p for k in range(dim)]
            hits.add(normalize_gamma(cand, p))
    total = 0
    for ab in precomp:
        counts = {}
        for a, b in ab:
            counts[b] = counts.get(b, 0) + 1
        total += max(counts.values())
    if total >= threshold:
        hits.add(normalize_gamma(v2, p))
    return hits


def random_nonzero_vec(p, dim, rng):
    while True:
        v = [rng.randrange(p) for _ in range(dim)]
        if any(v):
            return v


# =============================================================================
# Section 1: reference data.
# Source: D_nlist_note.md Table 3.1 / D_nlist.json "summary" key (wave_t1
# scratch measurement this note packages). Embedded as literals (not loaded
# from an external file) so this verifier has no file-path dependency.
# =============================================================================

REFERENCE_TABLE = {
    71: 305.0,
    113: 1234.6666666666665,
    127: 1869.0,
    197: 1150.3333333333335,
    211: 1600.0,
    337: 1368.0,
}
FIT_ALL6_EXPECTED = 0.768
FIT_EXCL71_EXPECTED = -0.071
FIT_TOL = 5e-3
RECOMPUTE_TOL = 1e-6
# documented in D_nlist_note.md sec 3.4 / D_capture_rate.json:
CAPTURE_RATE_DOCUMENTED_HITS = 0
CAPTURE_RATE_DOCUMENTED_TRIALS = 201600

# =============================================================================
# Section 1b: c-histogram cross-check reference data (added post-audit to
# close a BLOCKER: gate 1's fit tolerance alone silently absorbs a several-
# unit drift on any ONE of the 3 stored entries (p=197,211,337) gate 2 does
# not recompute from scratch). Source: note sec 4 Data table's own "c-histogram" column
# (== D_nlist_note.md Table 3.1 / D_witnesses_p*.json c_elevated counts) --
# a SECOND, independently-recorded piece of the same census that lets every
# one of the 6 REFERENCE_TABLE entries be tightly cross-checked
# (N_list = n * sum_c hist[c]/c, n=(p-1)/7) without repeating the expensive
# combinatorial search.
# =============================================================================
CHIST_TABLE = {
    71:  {3: 63,  4: 38},
    113: {3: 206, 4: 34},
    127: {3: 250, 4: 82},
    197: {3: 70,  4: 71},
    211: {3: 88,  4: 96},
    337: {3: 60,  4: 34},
}

# Headline narrative-number constants (Section 2/4 of the note), re-derived
# directly from REFERENCE_TABLE below by gate 7 -- added post-audit after
# three of these prose figures were found to have drifted from the table.
HEADLINE_P = 337
HEADLINE_TRIVIAL_EXP = 14
HEADLINE_ORDERS_BELOW_EXPECTED = 32.25  # log10(337**14 / REFERENCE_TABLE[337])
HEADLINE_ORDERS_TOL = 0.1
PRANGE_EXCL71_EXPECTED = 2.9823  # max/min p among the 5 non-p71 points
PRANGE_TOL = 5e-3
PAIRWISE_71_113_EXPECTED = 3.009  # log(N_list(113)/N_list(71)) / log(113/71)
PAIRWISE_TOL = 5e-3


# =============================================================================
# Section 2: gate implementations
# =============================================================================

def fit_loglog(table):
    """Least-squares log(N_list) = slope*log(p) + intercept, stdlib-only
    (mirrors D_fit.py's method exactly)."""
    pts_all = [(math.log(p), math.log(v)) for p, v in sorted(table.items())]
    pts_excl71 = [(x, y) for (x, y), p in zip(pts_all, sorted(table)) if p != 71]

    def slope_of(pts):
        n = len(pts)
        mx = sum(x for x, y in pts) / n
        my = sum(y for x, y in pts) / n
        sxy = sum((x - mx) * (y - my) for x, y in pts)
        sxx = sum((x - mx) ** 2 for x, y in pts)
        return sxy / sxx

    return slope_of(pts_all), slope_of(pts_excl71)


def gate_fit(table):
    slope_all6, slope_excl71 = fit_loglog(table)
    ok = (abs(slope_all6 - FIT_ALL6_EXPECTED) < FIT_TOL and
          abs(slope_excl71 - FIT_EXCL71_EXPECTED) < FIT_TOL)
    detail = (f"slope_all6={slope_all6:+.4f} (expect {FIT_ALL6_EXPECTED:+.3f}), "
              f"slope_excl_p71={slope_excl71:+.4f} (expect {FIT_EXCL71_EXPECTED:+.3f})")
    return ok, detail


def gate_recompute(primes, reference_table):
    """Recompute N_list(7,p) from scratch at each prime in `primes`, full
    scope, and compare to reference_table.  Returns
    (ok, detail_str, elapsed_s, {p: (gpc, witnesses)})."""
    t0 = time.time()
    computed = {}
    per_prime_state = {}
    detail_lines = []
    ok = True
    for p in primes:
        tp0 = time.time()
        gpc = GenPowerCosets(p, 7)
        witnesses, stats = two_seed_census(gpc, p, 7, 14)
        n_list = sum(gpc.n / c for (cfg, g), c in witnesses.items())
        dtp = time.time() - tp0
        computed[p] = n_list
        per_prime_state[p] = (gpc, witnesses)
        expect = reference_table.get(p)
        match = expect is not None and abs(n_list - expect) < RECOMPUTE_TOL
        ok = ok and match
        detail_lines.append(
            f"p={p}: recomputed N_list={n_list:.4f} vs stored={expect} "
            f"({'MATCH' if match else 'MISMATCH'}, {dtp:.2f}s, "
            f"{len(witnesses)} raw witnesses, off_path_seen={stats['off_path_seen']})"
        )
    dt = time.time() - t0
    return ok, "; ".join(detail_lines), dt, per_prime_state


def orbit_correction_check(gpc, config, gamma_norm, c_recorded):
    """From-scratch reconstruction of the orbit-correction lemma's counting
    claim on ONE concrete (config, gamma_norm, c_recorded) witness: builds
    all n shift-images explicitly, recomputes each image's own HONEST full
    spectrum (not derived from the formula), and counts (a) the number of
    DISTINCT (top5, gamma_norm) images (claimed = n) and (b) how many of the
    n images have coset 0 in their own top-5 AND fiber>=3 there (claimed =
    c_recorded).  Returns (orbit_size, discoverable_count)."""
    n, dim, g, p = gpc.n, gpc.dim, gpc.g, gpc.p
    keys = set()
    discoverable = 0
    for k in range(n):
        gk = shift_gamma(gamma_norm, k, g, p, dim)
        spec = honest_full_spectrum(gk, gpc)
        top5 = top5_of_spectrum(spec)
        keys.add((top5, normalize_gamma(gk, p)))
        if 0 in top5 and spec[0] >= 3:
            discoverable += 1
    return len(keys), discoverable


def find_orbit_check_witnesses(gpc, witnesses):
    """From the recomputed p=71 witness set, pick ONE witness on the unique
    'periodic' config (gaps all = n/5, only possible since 5|10) -- the
    harder/adversarial case the note flags -- and ONE witness on a generic
    (non-periodic) config, for the orbit-correction gate."""
    n = gpc.n
    periodic_cfg = tuple(range(0, n, n // 5)) if n % 5 == 0 else None
    periodic_witness = None
    generic_witness = None
    for (cfg, gamma_norm), c in witnesses.items():
        if periodic_cfg is not None and cfg == periodic_cfg and periodic_witness is None:
            periodic_witness = (cfg, gamma_norm, c)
        elif cfg != periodic_cfg and generic_witness is None:
            generic_witness = (cfg, gamma_norm, c)
        if periodic_witness is not None and generic_witness is not None:
            break
    return periodic_witness, generic_witness


def gate_orbit_correction(gpc, witnesses):
    periodic_witness, generic_witness = find_orbit_check_witnesses(gpc, witnesses)
    ok = True
    details = []
    for label, w in (("periodic-config", periodic_witness), ("generic-config", generic_witness)):
        if w is None:
            details.append(f"{label}: NO WITNESS AVAILABLE TO TEST (skipped)")
            continue
        cfg, gamma_norm, c_recorded = w
        orbit_size, discoverable = orbit_correction_check(gpc, cfg, gamma_norm, c_recorded)
        match = (orbit_size == gpc.n) and (discoverable == c_recorded)
        ok = ok and match
        details.append(
            f"{label} config={cfg}: true_pair_orbit_size={orbit_size} (expect n={gpc.n}), "
            f"discoverable={discoverable} (expect recorded c={c_recorded}) "
            f"({'MATCH' if match else 'MISMATCH'})"
        )
    return ok, "; ".join(details)


def gate_capture_rate(gpc, witnesses, seed=20260704, n_hit_configs=3, n_nonhit_configs=2, n_slices=60):
    """Reduced, documented, seeded replica of D_capture_rate.py: draw
    n_slices independent random 2-dim slices of gamma-space on a sample of
    hit configs and non-hit configs, full exact projective-line scan on
    each, and confirm (as the original found at full scope, 0/201600) that
    random/unplanted slicing finds ~0 threshold-crossing witnesses."""
    rng = random.Random(seed)
    hit_configs = sorted(set(cfg for cfg, g in witnesses.keys()))[:n_hit_configs]
    all_5subsets_tried = 0
    non_hit_configs = []
    hit_set = set(cfg for cfg, g in witnesses.keys())
    start = list(range(gpc.n))
    for combo in itertools.combinations(start, 5):
        all_5subsets_tried += 1
        if combo not in hit_set:
            non_hit_configs.append(combo)
        if len(non_hit_configs) >= n_nonhit_configs or all_5subsets_tried > 500:
            break
    threshold = 14
    total_trials = 0
    total_hits = 0
    for label, cfgs in (("hit", hit_configs), ("non-hit", non_hit_configs)):
        for cfg in cfgs:
            for _trial in range(n_slices):
                v1 = random_nonzero_vec(gpc.p, gpc.dim, rng)
                v2 = random_nonzero_vec(gpc.p, gpc.dim, rng)
                found = enumerate_and_check_dim2_fast_random(v1, v2, gpc, cfg, gpc.p, threshold)
                total_trials += 1
                total_hits += len(found)
    ok = (total_hits == CAPTURE_RATE_DOCUMENTED_HITS)
    detail = (f"{total_hits} random-slice threshold-crossings found in {total_trials} trials "
              f"x {gpc.p + 1} points/trial = {total_trials * (gpc.p + 1)} points checked "
              f"(reduced scope vs documented full run's {CAPTURE_RATE_DOCUMENTED_HITS}/"
              f"{CAPTURE_RATE_DOCUMENTED_TRIALS} points; seed={seed})")
    return ok, detail


def n_list_from_histogram(p, ell, hist):
    """Independently re-derive N_list(p) from the (n, c-histogram) pair the
    note's own Data table already publishes, without touching the
    combinatorial search at all."""
    n = (p - 1) // ell
    return n * sum(cnt / c for c, cnt in hist.items())


def gate_hist_consistency(table, chist):
    """Cheap, tight-tolerance cross-check covering ALL 6 stored entries (not
    just the 2-3 gate-2 recomputes): recomputes N_list from the
    already-published c-histogram and compares to the stored REFERENCE_TABLE
    value. Added post-audit to close the BLOCKER that gate 1's wide fit
    tolerance alone leaves p=197/211/337 essentially unguarded."""
    ok = True
    lines = []
    for p in sorted(table):
        hist = chist.get(p)
        if hist is None:
            ok = False
            lines.append(f"p={p}: NO HISTOGRAM DATA (fail-closed)")
            continue
        derived = n_list_from_histogram(p, 7, hist)
        match = abs(derived - table[p]) < RECOMPUTE_TOL
        ok = ok and match
        lines.append(f"p={p}: hist-derived={derived:.4f} vs stored={table[p]} "
                     f"({'MATCH' if match else 'MISMATCH'})")
    return ok, "; ".join(lines)


def is_monomial_gamma(gamma_norm):
    """True iff exactly one coordinate is nonzero -- the excluded case in the
    sec 7 exact-orbit-size lemma, where the n/c weight can degrade to
    (n/5)/c."""
    return sum(1 for c in gamma_norm if c) == 1


def gate_monomial_scan(per_prime_state):
    """Scans every raw witness gamma_norm gate 2 actually recomputed from
    scratch (all primes in per_prime_state) for the monomial exception.
    Directly reproduces (not just re-asserts) the note sec 7 '0 monomial
    gamma found' claim for this reproducible subset of the 1092-witness
    census; primes gate 2 does not recompute are NOT covered here (too
    expensive) -- the note/pr_body flag this scope explicitly."""
    total = 0
    monomial_hits = []
    for p, (gpc, witnesses) in sorted(per_prime_state.items()):
        for (top5, gamma_norm) in witnesses:
            total += 1
            if is_monomial_gamma(gamma_norm):
                monomial_hits.append((p, top5, gamma_norm))
    ok = (len(monomial_hits) == 0)
    primes_str = ",".join(str(p) for p in sorted(per_prime_state))
    detail = (f"scanned {total} raw witnesses at p in {{{primes_str}}} for monomial "
              f"gamma_norm: {len(monomial_hits)} found (expect 0); this covers "
              f"{total}/1092 census witnesses (p=197,211,337 not re-scanned here -- "
              f"too expensive to recompute from scratch; see note sec 7/8 caveat)")
    return ok, detail


def gate_headline_numbers(table):
    """Re-derives three narrative NUMERIC figures the note's sec 2/4 prose
    quotes -- plain arithmetic on the already-verified 6-prime table -- and
    checks them against corrected constants. Added post-audit: the previous
    prose had silently drifted from the table on all three (a copy/rounding
    error, not a change in the underlying data)."""
    ok = True
    lines = []

    p337_pow = HEADLINE_P ** HEADLINE_TRIVIAL_EXP
    orders_below = math.log10(p337_pow / table[HEADLINE_P])
    m1 = abs(orders_below - HEADLINE_ORDERS_BELOW_EXPECTED) < HEADLINE_ORDERS_TOL
    ok = ok and m1
    lines.append(f"{HEADLINE_P}**{HEADLINE_TRIVIAL_EXP}={p337_pow} (~{p337_pow:.3e}), "
                 f"orders below stored N_list({HEADLINE_P})={orders_below:.2f} "
                 f"(expect ~{HEADLINE_ORDERS_BELOW_EXPECTED:.2f}) "
                 f"{'MATCH' if m1 else 'MISMATCH'}")

    non71 = [p for p in table if p != 71]
    prange = max(non71) / min(non71)
    m2 = abs(prange - PRANGE_EXCL71_EXPECTED) < PRANGE_TOL
    ok = ok and m2
    lines.append(f"p-range (excl. 71) max/min={prange:.4f} "
                 f"(expect {PRANGE_EXCL71_EXPECTED:.4f}) {'MATCH' if m2 else 'MISMATCH'}")

    p0, p1 = 71, 113
    exp01 = math.log(table[p1] / table[p0]) / math.log(p1 / p0)
    m3 = abs(exp01 - PAIRWISE_71_113_EXPECTED) < PAIRWISE_TOL
    ok = ok and m3
    lines.append(f"pairwise exponent {p0}->{p1}={exp01:+.4f} "
                 f"(expect {PAIRWISE_71_113_EXPECTED:+.4f}) {'MATCH' if m3 else 'MISMATCH'}")

    return ok, "; ".join(lines)


# =============================================================================
# Section 3: tamper self-test (negative control -- proves the gates above
# actually discriminate, rather than being vacuously true).
# =============================================================================

def run_tamper_selftest(gpc71, witnesses71):
    checks = []

    # (a) fit gate must FAIL against a corrupted table.
    tampered_table = dict(REFERENCE_TABLE)
    tampered_table[71] = tampered_table[71] * 5.0  # corrupt: 5x too high
    ok_tampered, _ = gate_fit(tampered_table)
    checks.append(("fit-gate catches corrupted table", ok_tampered is False))

    # (b) fit gate must still PASS on the untouched table (sanity: (a) isn't
    # just always failing).
    ok_clean, _ = gate_fit(REFERENCE_TABLE)
    checks.append(("fit-gate passes on the real table", ok_clean is True))

    # (c) recompute-gate comparison must FAIL if the stored reference is
    # tampered (reuse the already-recomputed p=71 value, compare against a
    # deliberately wrong stored figure -- no need to redo the expensive
    # recomputation just for this negative control).
    n_list_71 = sum(gpc71.n / c for (cfg, g), c in witnesses71.items())
    wrong_reference = {71: n_list_71 + 1.0}
    mismatch_detected = not (abs(n_list_71 - wrong_reference[71]) < RECOMPUTE_TOL)
    checks.append(("recompute-gate catches a 1.0-off stored value", mismatch_detected))

    # (d) orbit-correction gate must FAIL if fed a deliberately wrong
    # expected c_elevated.
    periodic_witness, generic_witness = find_orbit_check_witnesses(gpc71, witnesses71)
    w = generic_witness or periodic_witness
    assert w is not None, "tamper self-test needs at least one p=71 witness"
    cfg, gamma_norm, c_real = w
    orbit_size, discoverable = orbit_correction_check(gpc71, cfg, gamma_norm, c_real)
    wrong_c = c_real + 1
    tampered_match = (orbit_size == gpc71.n) and (discoverable == wrong_c)
    checks.append(("orbit-correction gate catches a wrong recorded c", tampered_match is False))

    # (e) orbit-correction gate must PASS against the real recorded c
    # (sanity companion to (d)).
    real_match = (orbit_size == gpc71.n) and (discoverable == c_real)
    checks.append(("orbit-correction gate passes on the real recorded c", real_match is True))

    # (f) capture-rate DETECTOR must actually detect a hit when one is
    # deliberately planted (a real positive control, not just re-checking a
    # fabricated boolean): build the 2-dim family v1=known-hit gamma_norm,
    # v2=arbitrary, on that witness's OWN config. At t=0 this family's member
    # is v1 itself (a KNOWN hit, taken straight from the gate-2
    # recomputation), so enumerate_and_check_dim2_fast_random -- the exact
    # function gate 4 uses -- MUST report >=1 hit on this input. If it ever
    # reported 0 here, gate 4's "0 hits" verdict on genuinely random slices
    # would be meaningless (the detector could just be broken/always-empty).
    plant_cfg, plant_gamma, _ = w
    v2_arbitrary = [(x + 1) % gpc71.p or 1 for x in plant_gamma]  # any nonzero vector != v1
    planted_hits = enumerate_and_check_dim2_fast_random(
        plant_gamma, v2_arbitrary, gpc71, plant_cfg, gpc71.p, 14)
    detector_works = normalize_gamma(plant_gamma, gpc71.p) in planted_hits
    checks.append(("capture-rate detector finds a deliberately planted known hit", detector_works is True))

    # (g) ... and, as a sanity companion, a family with NO seeded relationship
    # to any config (a fresh random pair, evaluated on a NON-hit config) is
    # not required to hit anything -- not asserted here (that's gate 4's own
    # real, non-tamper measurement), just confirming (f) isn't vacuously
    # matching on an unrelated/empty set.
    checks.append(("capture-rate detector's planted-hit set is non-empty", len(planted_hits) >= 1))

    # (h) histogram-consistency gate must FAIL if exactly one REFERENCE_TABLE
    # entry is tampered (+1) while its c-histogram is left untouched -- this
    # is the exact BLOCKER scenario a packet audit identified: gate 1's fit
    # tolerance alone silently absorbs a +1..+8 drift on p=337 (which gate 2
    # does not recompute from scratch).
    tampered_table_hist = dict(REFERENCE_TABLE)
    tampered_table_hist[337] = tampered_table_hist[337] + 1.0
    ok_hist_tampered, _ = gate_hist_consistency(tampered_table_hist, CHIST_TABLE)
    checks.append(("hist-consistency gate catches a +1-off p=337 entry (untouched by gate 2)",
                    ok_hist_tampered is False))

    # (i) ... and passes cleanly on the real table (sanity companion to (h)).
    ok_hist_clean, _ = gate_hist_consistency(REFERENCE_TABLE, CHIST_TABLE)
    checks.append(("hist-consistency gate passes on the real table", ok_hist_clean is True))

    # (j) monomial-scan gate must FAIL if fed a deliberately planted monomial
    # gamma_norm (positive control -- proves "0 found" isn't vacuous).
    monomial_vec = tuple([1] + [0] * (gpc71.dim - 1))
    any_key = next(iter(witnesses71))
    fake_witnesses = dict(witnesses71)
    fake_witnesses[(any_key[0], monomial_vec)] = witnesses71[any_key]
    ok_mono_tampered, _ = gate_monomial_scan({71: (gpc71, fake_witnesses)})
    checks.append(("monomial-scan gate catches a planted monomial gamma_norm",
                    ok_mono_tampered is False))

    # (k) ... and passes cleanly on the real (untampered) p=71 witness set.
    ok_mono_clean, _ = gate_monomial_scan({71: (gpc71, witnesses71)})
    checks.append(("monomial-scan gate passes on the real witness set", ok_mono_clean is True))

    # (l) headline-numbers gate must FAIL if p=337's stored value is
    # corrupted (the same BLOCKER scenario as (h), from the narrative-number
    # side: a drifted p=337 entry should break the "orders of magnitude"
    # figure too).
    tampered_table_hn = dict(REFERENCE_TABLE)
    tampered_table_hn[337] = tampered_table_hn[337] * 1.5
    ok_hn_tampered, _ = gate_headline_numbers(tampered_table_hn)
    checks.append(("headline-numbers gate catches a corrupted p=337 entry", ok_hn_tampered is False))

    # (m) ... and passes cleanly on the real table.
    ok_hn_clean, _ = gate_headline_numbers(REFERENCE_TABLE)
    checks.append(("headline-numbers gate passes on the real table", ok_hn_clean is True))

    failed = [name for name, passed in checks if not passed]
    if failed:
        raise AssertionError(f"TAMPER SELF-TEST FAILED (gates are vacuous for): {failed}")
    return checks


# =============================================================================
# Section 4: main
# =============================================================================

def main():
    t_start = time.time()
    print("=== verify_l1_petal_growth_nlist_e16.py ===")
    print("(E16 N_list(7,p) petal-growth packet: fit + recompute + orbit-correction + "
          "capture-rate + hist-consistency + monomial-scan + headline-numbers gates)\n")

    failures = []

    # Gate 2 (recompute) is run FIRST (even though numbered 2) because gates
    # 0's tamper self-test, gate 3 (orbit-correction), and gate 6
    # (monomial-scan) all need its output (the p=71,113,127 witness sets) to
    # run their own checks against real data -- this ordering avoids
    # recomputing them twice.
    print("--- Gate 2: recompute N_list(7,p) from scratch at p=71,113,127 ---")
    ok2, detail2, elapsed2, per_prime_state = gate_recompute((71, 113, 127), REFERENCE_TABLE)
    print(("[PASS] " if ok2 else "[FAIL] ") + detail2)
    print(f"  (recompute wall time: {elapsed2:.2f}s)\n")
    if not ok2:
        failures.append("gate 2 (recompute)")
    gpc71, witnesses71 = per_prime_state[71]

    print("--- Gate 0: tamper self-test (negative controls) ---")
    try:
        checks = run_tamper_selftest(gpc71, witnesses71)
        for name, passed in checks:
            print(f"  [PASS] {name}")
        print("[PASS] tamper self-test: all negative controls correctly discriminated\n")
    except AssertionError as e:
        print(f"[FAIL] tamper self-test: {e}\n")
        failures.append("gate 0 (tamper self-test)")

    print("--- Gate 1: log-log fit arithmetic (6-point stored table) ---")
    ok1, detail1 = gate_fit(REFERENCE_TABLE)
    print(("[PASS] " if ok1 else "[FAIL] ") + detail1 + "\n")
    if not ok1:
        failures.append("gate 1 (fit)")

    print("--- Gate 3: orbit-correction lemma, from-scratch reconstruction (p=71) ---")
    ok3, detail3 = gate_orbit_correction(gpc71, witnesses71)
    for line in detail3.split("; "):
        print(("  [PASS] " if ok3 else "  [FAIL] ") + line)
    if not ok3:
        failures.append("gate 3 (orbit-correction)")
    print()

    print("--- Gate 4: capture-rate reduced replica (p=71, seeded) ---")
    ok4, detail4 = gate_capture_rate(gpc71, witnesses71)
    print(("[PASS] " if ok4 else "[FAIL] ") + detail4 + "\n")
    if not ok4:
        failures.append("gate 4 (capture-rate)")

    print("--- Gate 5: c-histogram cross-check (all 6 stored entries) ---")
    ok5, detail5 = gate_hist_consistency(REFERENCE_TABLE, CHIST_TABLE)
    for line in detail5.split("; "):
        print(("  [PASS] " if ok5 else "  [FAIL] ") + line)
    if not ok5:
        failures.append("gate 5 (hist-consistency)")
    print()

    print("--- Gate 6: monomial-gamma scan (all gate-2-recomputed witnesses) ---")
    ok6, detail6 = gate_monomial_scan(per_prime_state)
    print(("[PASS] " if ok6 else "[FAIL] ") + detail6 + "\n")
    if not ok6:
        failures.append("gate 6 (monomial-scan)")

    print("--- Gate 7: headline narrative-number re-derivation ---")
    ok7, detail7 = gate_headline_numbers(REFERENCE_TABLE)
    for line in detail7.split("; "):
        print(("  [PASS] " if ok7 else "  [FAIL] ") + line)
    if not ok7:
        failures.append("gate 7 (headline-numbers)")
    print()

    total_elapsed = time.time() - t_start
    print(f"total runtime: {total_elapsed:.1f}s")

    if failures:
        print(f"\nRESULT: FAIL -- {len(failures)} gate(s) failed: {failures}")
        sys.exit(1)
    else:
        print("\nRESULT: ALL GATES PASSED (0 tamper-selftest + 1 fit + 2 recompute[p=71,113,127] "
              "+ 3 orbit-correction + 4 capture-rate + 5 hist-consistency + 6 monomial-scan "
              "+ 7 headline-numbers)")
        sys.exit(0)


if __name__ == "__main__":
    main()
