#!/usr/bin/env python3
"""l1_ell19_bigfiber_v2.py

Companion CONSTRUCTOR/engine for `experimental/notes/l1/l1_ell19_attainment.md`.
Adapted from the session's discovery script (`ell19_bigfiber_hunt_v2.py`): a
plant-big-fibers-then-exact-solve constructor at `ell = 19` -- per trial, it
greedily plants big fibers (sizes cycling high-to-low) on distinct cosets
while the exact coincidence-rank stays `<= ell-2 = 17` (the realizability
cap), then reads a `gamma` off the solved nullspace and evaluates its
spectrum / `E_3`.

Default mode is a DETERMINISTIC, SEEDED RE-DERIVATION, not a replay of stored
coefficients: it reruns the exact `seed_base = 314159265` trial sequence
(trials `1..2240`) at `p = 647` that this session used to discover the
`E_3 = 18` witness, using only the seed formula and the construction
algorithm (never reading the shipped `gamma` from disk), and asserts that
this from-scratch rerun (a) reaches `best_E3 == 18` and (b) the gamma
achieving it is IDENTICAL to the one shipped in
`experimental/notes/l1/l1_ell19_attainment.md` sec 1. Each trial reseeds its
own `random.Random` independently from `(seed_base, ell, p, trial)`, so a
fixed trial COUNT (not a wall-clock time budget) reproduces the discovery
bit-for-bit regardless of machine speed -- this is what makes the default
run deterministic.

`--fresh-seed N`: hunts `p = 647` with a NEW `seed_base = N` for a bounded
number of trials, printing progress and the best `E_3` found; NOT expected to
reliably hit `E_3 = 18` (observed rate ~1/3000 per tested gamma at `p=647`,
see the note's sec 0 item 3 histogram), so no hit is asserted for this mode.

Stdlib only (`random`, `time`, `sys`); no imports of any sibling verifier
module (self-contained, matching the note's "companion engine" contract).
"""
import sys
import time
import random

ELL = 19
M = (ELL + 1) // 2                    # 10
TARGET_TOPM = 2 * ELL                 # 38
DEFAULT_P = 647
DEFAULT_SEED_BASE = 314159265
DEFAULT_NUM_TRIALS = 2240             # matches the shipped discovery's trial count exactly
BIGSIZES = (16, 15, 14, 13, 11, 10, 9, 12, 8)

SHIPPED_GAMMA = [298, 638, 143, 294, 14, 111, 237, 78, 464, 166, 355, 385, 207, 68, 465, 369, 316, 1]
SHIPPED_E3 = 18
SHIPPED_TRIAL = 2240

# =====================================================================================
# exact F_p arithmetic -- fresh, self-contained
# =====================================================================================
def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True

def inv(a, p):
    return pow(a % p, p - 2, p)

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

def spectrum_A(gamma, p, ell):
    """generator-power cosets g^i H, ascending power-sum evaluation."""
    g = find_gen(p)
    n = (p - 1) // ell
    zeta = pow(g, n, p)
    H = [pow(zeta, j, p) for j in range(ell)]
    out = []
    for i in range(n):
        b = pow(g, i, p)
        cnt = {}
        for h in H:
            x = b * h % p
            v = 0
            xr = 1
            for r in range(1, ell):
                xr = xr * x % p
                if gamma[r - 1]:
                    v = (v + gamma[r - 1] * xr) % p
            cnt[v] = cnt.get(v, 0) + 1
        out.append(max(cnt.values()))
    out.sort(reverse=True)
    return out

def spectrum_B(gamma, p, ell):
    """independent: label cosets by x^ell mod p (no generator), Horner evaluation."""
    groups = {}
    for x in range(1, p):
        a = pow(x, ell, p)
        v = 0
        for c in reversed(gamma):
            v = (v * x + c) % p
        v = v * x % p  # Gamma has no constant term
        d = groups.setdefault(a, {})
        d[v] = d.get(v, 0) + 1
    out = [max(d.values()) for d in groups.values()]
    out.sort(reverse=True)
    return out

def E3(spec):
    return sum(mu - 2 for mu in spec if mu >= 3)

def topk(spec, k):
    return sum(spec[:k])

# =====================================================================================
# rank-formula machinery -- exact F_p linear algebra (needed by the constructor)
# =====================================================================================
def rref(rows, ncols, p):
    A = [[v % p for v in r] for r in rows]
    m = len(A)
    piv = []
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
        iv = inv(A[r][c], p)
        A[r] = [(v * iv) % p for v in A[r]]
        for i in range(m):
            if i != r and A[i][c] % p:
                f = A[i][c]
                A[i] = [(A[i][j] - f * A[r][j]) % p for j in range(ncols)]
        piv.append(c)
        r += 1
        if r == m:
            break
    return r, A, piv

def rank_Fp(rows, ncols, p):
    if not rows:
        return 0
    return rref(rows, ncols, p)[0]

def vpow(x, ell, p):
    return [pow(x, r, p) for r in range(1, ell)]

def fiber_rows(points, ell, p):
    if len(points) < 2:
        return []
    v0 = vpow(points[0], ell, p)
    rows = []
    for x in points[1:]:
        vx = vpow(x, ell, p)
        rows.append([(v0[r] - vx[r]) % p for r in range(ell - 1)])
    return rows

def basis_from_rows(rows, ell, p):
    r, A, piv = rref(rows, ell - 1, p)
    pivset = set(piv)
    basis = []
    for free in range(ell - 1):
        if free in pivset:
            continue
        v = [0] * (ell - 1)
        v[free] = 1
        for i, c in enumerate(piv):
            v[c] = (-A[i][free]) % p
        basis.append(v)
    return basis

# =====================================================================================
# the plant-big-fibers-then-exact-solve constructor (faithful port of
# ell19_bigfiber_hunt_v2.py construct_one / hunt_prime)
# =====================================================================================
def construct_one(ell, p, rnd, bigsize, n, g, H, cosets, rank_cap, subset_tries=6):
    order = list(range(n))
    rnd.shuffle(order)
    rows = []
    fibers = []
    stall = 0
    for ci in order:
        cur_rank = rank_Fp(rows, ell - 1, p) if rows else 0
        if cur_rank >= rank_cap:
            stall += 1
            if stall > 3:
                break
            continue
        lo = max(3, bigsize - 4)
        start = rnd.randint(lo, bigsize)
        for sz in range(min(start, ell - 1), 2, -1):
            placed = False
            for _ in range(subset_tries):
                exps = rnd.sample(range(ell), sz)
                pts = [cosets[ci][e] for e in exps]
                nr = fiber_rows(pts, ell, p)
                if rank_Fp(rows + nr, ell - 1, p) <= rank_cap:
                    rows += nr
                    fibers.append(pts)
                    placed = True
                    stall = 0
                    break
            if placed:
                break
    return rows, fibers

def hunt_fixed_trials(p, ell, m, num_trials, seed_base, bigsizes=BIGSIZES, log=print,
                       progress_every=200):
    """Deterministic variant of hunt_prime: runs EXACTLY `num_trials` trials
    (trial = 1..num_trials), each with its OWN independently-seeded
    random.Random(seed_base + ell*1000003 + p*trial97... ) -- i.e. the same
    per-trial seed formula as the discovery session. Because each trial's
    randomness is self-contained, a fixed trial count reproduces the exact
    same sequence of planted fibers / candidate gammas regardless of
    wall-clock speed (no time-budget cutoff, hence fully deterministic)."""
    assert is_prime(p) and (p - 1) % ell == 0
    n = (p - 1) // ell
    g = find_gen(p)
    zeta = pow(g, n, p)
    H = [pow(zeta, j, p) for j in range(ell)]
    cosets = [[pow(g, i, p) * h % p for h in H] for i in range(n)]
    can_list = (n >= 2 * m - 1)

    t0 = time.time()
    best_E3 = -1
    best_record = None
    e3_hist = {}
    tested_gammas = 0
    for trial in range(1, num_trials + 1):
        bigsize = bigsizes[(trial - 1) % len(bigsizes)]
        rnd = random.Random(seed_base + ell * 1000003 + p * 97 + trial)
        rows, fibers = construct_one(ell, p, rnd, bigsize, n, g, H, cosets, rank_cap=ell - 2)
        if rows:
            basis = basis_from_rows(rows, ell, p)
            cand_vecs = [v[:] for v in basis if any(v)]
            if len(basis) >= 2:
                for _ in range(4):
                    coeffs = [rnd.randint(0, p - 1) for _ in basis]
                    if not any(coeffs):
                        continue
                    comb = [0] * (ell - 1)
                    for cf, bv in zip(coeffs, basis):
                        if cf:
                            for i in range(ell - 1):
                                comb[i] = (comb[i] + cf * bv[i]) % p
                    if any(comb):
                        cand_vecs.append(comb)
            for gm in cand_vecs:
                tested_gammas += 1
                specA = spectrum_A(gm, p, ell)
                e3 = E3(specA)
                e3_hist[e3] = e3_hist.get(e3, 0) + 1
                if e3 > best_E3:
                    specB = spectrum_B(gm, p, ell)
                    tm = topk(specA, m) if can_list else None
                    best_E3 = e3
                    best_record = {
                        "gamma": gm[:], "spectrum": specA[:], "spectra_agree": (specA == specB),
                        "E3": e3, "top_m": tm, "trial": trial, "bigsize": bigsize,
                        "n_planted_fibers": len(fibers),
                        "planted_sizes": sorted((len(f) for f in fibers), reverse=True),
                    }
                    log("  [p=%d n=%d] new best E3=%d trial=%d/%d bigsize=%d planted=%s t=%.1fs"
                        % (p, n, e3, trial, num_trials, bigsize, best_record["planted_sizes"], time.time() - t0))
        if progress_every and trial % progress_every == 0:
            log("  ... trial %d/%d done (best_E3 so far=%d, tested_gammas=%d, t=%.1fs)"
                % (trial, num_trials, best_E3, tested_gammas, time.time() - t0))
    elapsed = time.time() - t0
    return {
        "p": p, "ell": ell, "n_cosets": n, "can_list_m10": can_list,
        "elapsed_s": round(elapsed, 2), "trials": num_trials, "tested_gammas": tested_gammas,
        "best_E3": best_E3, "best_record": best_record,
        "e3_histogram": {str(k): v for k, v in sorted(e3_hist.items())},
        "seed_base": seed_base, "bigsizes_used": list(bigsizes),
    }

def hunt_time_budget(p, ell, m, time_budget, seed_base, bigsizes=BIGSIZES, log=print):
    """--fresh-seed mode: bounded by wall-clock time budget (not a fixed trial
    count), since a new seed is not expected to reliably hit E_3=18 quickly and
    we don't want an unbounded run."""
    assert is_prime(p) and (p - 1) % ell == 0
    n = (p - 1) // ell
    g = find_gen(p)
    zeta = pow(g, n, p)
    H = [pow(zeta, j, p) for j in range(ell)]
    cosets = [[pow(g, i, p) * h % p for h in H] for i in range(n)]
    can_list = (n >= 2 * m - 1)

    t0 = time.time()
    best_E3 = -1
    best_record = None
    e3_hist = {}
    trial = 0
    tested_gammas = 0
    while time.time() - t0 < time_budget:
        trial += 1
        bigsize = bigsizes[(trial - 1) % len(bigsizes)]
        rnd = random.Random(seed_base + ell * 1000003 + p * 97 + trial)
        rows, fibers = construct_one(ell, p, rnd, bigsize, n, g, H, cosets, rank_cap=ell - 2)
        if not rows:
            continue
        basis = basis_from_rows(rows, ell, p)
        cand_vecs = [v[:] for v in basis if any(v)]
        if len(basis) >= 2:
            for _ in range(4):
                coeffs = [rnd.randint(0, p - 1) for _ in basis]
                if not any(coeffs):
                    continue
                comb = [0] * (ell - 1)
                for cf, bv in zip(coeffs, basis):
                    if cf:
                        for i in range(ell - 1):
                            comb[i] = (comb[i] + cf * bv[i]) % p
                if any(comb):
                    cand_vecs.append(comb)
        for gm in cand_vecs:
            tested_gammas += 1
            specA = spectrum_A(gm, p, ell)
            e3 = E3(specA)
            e3_hist[e3] = e3_hist.get(e3, 0) + 1
            if e3 > best_E3:
                specB = spectrum_B(gm, p, ell)
                tm = topk(specA, m) if can_list else None
                best_E3 = e3
                best_record = {
                    "gamma": gm[:], "spectrum": specA[:], "spectra_agree": (specA == specB),
                    "E3": e3, "top_m": tm, "trial": trial, "bigsize": bigsize,
                    "n_planted_fibers": len(fibers),
                    "planted_sizes": sorted((len(f) for f in fibers), reverse=True),
                }
                log("  [p=%d n=%d, seed_base=%d] new best E3=%d trial=%d bigsize=%d t=%.1fs"
                    % (p, n, seed_base, e3, trial, bigsize, time.time() - t0))
    elapsed = time.time() - t0
    return {
        "p": p, "ell": ell, "n_cosets": n, "can_list_m10": can_list,
        "elapsed_s": round(elapsed, 2), "trials": trial, "tested_gammas": tested_gammas,
        "best_E3": best_E3, "best_record": best_record,
        "e3_histogram": {str(k): v for k, v in sorted(e3_hist.items())},
        "seed_base": seed_base, "bigsizes_used": list(bigsizes),
    }

def main():
    args = sys.argv[1:]
    print("=" * 92)
    if args and args[0] == "--fresh-seed":
        if len(args) < 2:
            print("usage: l1_ell19_bigfiber_v2.py --fresh-seed N [time_budget_s]")
            sys.exit(2)
        seed = int(args[1])
        time_budget = float(args[2]) if len(args) > 2 else 120.0
        print(" FRESH-SEED HUNT   ell=%d p=%d seed_base=%d time_budget=%.0fs" % (ELL, DEFAULT_P, seed, time_budget))
        print(" (a new seed is NOT expected to reliably hit E_3=18; ~1/3000 hit rate per tested gamma)")
        print("=" * 92)
        res = hunt_time_budget(DEFAULT_P, ELL, M, time_budget, seed_base=seed)
        print("-" * 92)
        print("DONE: trials=%d tested_gammas=%d best_E3=%d elapsed=%.1fs" % (
            res["trials"], res["tested_gammas"], res["best_E3"], res["elapsed_s"]))
        if res["best_record"]:
            print("best gamma: %s" % res["best_record"]["gamma"])
            print("E3 histogram: %s" % res["e3_histogram"])
        print("=" * 92)
        sys.exit(0)

    # default mode: deterministic seeded re-derivation of the shipped p=647 discovery
    print(" DETERMINISTIC RE-DERIVATION   ell=%d p=%d seed_base=%d trials=1..%d (matches shipped discovery)"
          % (ELL, DEFAULT_P, DEFAULT_SEED_BASE, DEFAULT_NUM_TRIALS))
    print(" (re-derives from scratch via the plant-big-fibers-then-exact-solve constructor;")
    print("  does NOT read the shipped gamma from disk -- only the seed formula and trial count)")
    print("=" * 92)
    res = hunt_fixed_trials(DEFAULT_P, ELL, M, DEFAULT_NUM_TRIALS, seed_base=DEFAULT_SEED_BASE)
    print("-" * 92)
    print("DONE: trials=%d tested_gammas=%d best_E3=%d elapsed=%.1fs"
          % (res["trials"], res["tested_gammas"], res["best_E3"], res["elapsed_s"]))
    print("E3 histogram over %d exact-solved plants: %s" % (res["tested_gammas"], res["e3_histogram"]))
    br = res["best_record"]
    print("best gamma (trial=%d, bigsize=%d, planted=%s): %s"
          % (br["trial"], br["bigsize"], br["planted_sizes"], br["gamma"]))
    print("=" * 92)

    ok_e3 = (res["best_E3"] == SHIPPED_E3)
    ok_gamma = (br["gamma"] == SHIPPED_GAMMA)
    ok_trial = (br["trial"] == SHIPPED_TRIAL)
    print("ASSERT best_E3 == %d (shipped): %s" % (SHIPPED_E3, ok_e3))
    print("ASSERT gamma == shipped gamma (exact match, not read from disk): %s" % ok_gamma)
    print("ASSERT hit occurred at trial == %d (matches shipped provenance): %s" % (SHIPPED_TRIAL, ok_trial))
    print("=" * 92)
    if ok_e3 and ok_gamma and ok_trial:
        print(" RESULT: RE-DERIVATION MATCHES THE SHIPPED WITNESS EXACTLY   (%.1fs)" % res["elapsed_s"])
        sys.exit(0)
    else:
        print(" RESULT: RE-DERIVATION DID NOT REPRODUCE THE SHIPPED WITNESS -- investigate")
        sys.exit(1)

if __name__ == "__main__":
    main()
