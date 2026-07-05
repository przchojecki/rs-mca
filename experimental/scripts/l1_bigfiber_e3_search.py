#!/usr/bin/env python3
"""l1_bigfiber_e3_search.py

Plant-big-fibers-then-exact-solve CONSTRUCTOR for counterexamples to the L1
prime-`ell` KEY LEMMA `E_3 <= ell-2` of
`experimental/notes/l1/l1_prime_ell_frontier_corrected.md` sec 3, documented
as REFUTED in `experimental/notes/l1/l1_prime_ell_key_lemma_refuted.md`
(verified by the companion `experimental/scripts/verify_l1_key_lemma_refuted.py`).

Stdlib only. No imports from any other script in this repo (independent,
from-scratch reimplementation of the method described in the refutation's
input material; the algebra necessarily resembles the sibling verifier's
exact-`F_p` machinery because it is the same underlying mathematics, but no
code is shared or imported).

--------------------------------------------------------------------------
WHY A NEW SEARCH METHOD WAS NEEDED (root cause, see the refutation note sec 3)
--------------------------------------------------------------------------
The integrated note's KEY LEMMA was backed only by a search that plants a
FEW small (`K <= 3`, size-3) fibers and never finds `E_3 > ell-2`.  That
search under-samples: it never plants the *big* fibers that carry the
excess.  This script instead plants ONE large fiber per coset -- sizes in
the neighborhood of `(ell+1)/2`, kept mutually legal via the PROVED pairwise
cap `mu_i + mu_j <= ell` -- and keeps stacking fibers, one coset at a time,
for as long as the *exact* coincidence rank (over `F_p`, in the
constant-free `(ell-1)`-dim coefficient space) stays realizable, i.e.
`<= ell-2` (the note's PROVED rank formula, sec 2.2: a nonzero constant-free
`Gamma` of degree `<= ell-1` realizing a set of fibers exists iff the rank
of their coincidence rows is `<= ell-2`).  Once no more cosets admit a legal
fiber, the actual `Gamma` is read off by solving the exact nullspace of the
stacked rows (never merely assumed) and then the TRUE realized spectrum is
recomputed by evaluating that `Gamma` on *every* coset of `F_p^*` -- because
incidental coincidences beyond the ones planted are common, and are exactly
what can push the realized `E_3` at or above `ell-1`.

--------------------------------------------------------------------------
ALGORITHM
--------------------------------------------------------------------------
Given `ell` (odd prime), `p` (prime, `ell | p-1`), a seed:
  1. `n = (p-1)/ell` cosets `bH` partition `F_p^*` (`H` = the `ell`-th roots
     of unity).  Visit the `n` cosets in a seeded pseudo-random order.
  2. For each coset in turn, try to plant ONE new fiber (points forced to a
     shared `Gamma`-value) of size `s`, `s` drawn near `(ell+1)/2` (seeded
     random target, re-capped every coset by the PROVED pairwise rule
     `s <= ell - max(sizes already planted)`), trying up to `subset_tries`
     random point-subsets of that coset at that size before shrinking `s`;
     accept the first subset whose ADDED rows keep the combined exact rank
     (all rows accepted so far) `<= ell-2`.  Skip the coset if no legal
     `s >= 3` subset is found (fibers of size `<=2` cannot raise `E_3`).
  3. After all cosets are visited, solve the nullspace of the final row set
     in the `(ell-1)`-dim coefficient space: any nonzero element is a valid
     constant-free mixed `Gamma` realizing every accepted coincidence
     (nullity `>= 1` is an invariant of step 2's acceptance rule).
  4. Recompute the TRUE spectrum of that `Gamma` by direct evaluation over
     every coset of `F_p^*`, and report the true `E_3`.

Because the target configurations are rare (the refutation note: naive
sampling of `Gamma`-space found "0 of 201600" crossings), this remains a
SEEDED SEARCH, not a closed-form construction: a given `(ell, p)` is tried
across a bounded, deterministic sweep of seeds (`--seed` sets the sweep's
start; `--max-tries` bounds its length) until a violation `E_3 > ell-2` is
found or the budget is exhausted.  The two default targets below are tuned
to be found FAST (well under a second to a few seconds each); other primes
are demonstrably harder for this generic greedy method (some of the
shipped counterexamples are tied to much more special, high-`K`
coincidences, e.g. `ell=13, p=313` has `K=10` simultaneous fibers) and are
only attempted, best-effort, under `--all`.

--------------------------------------------------------------------------
USAGE
--------------------------------------------------------------------------
    python3 experimental/scripts/l1_bigfiber_e3_search.py
        -> default: constructs fresh (independently re-discovered, NOT
           replayed from stored coefficients) violations at (ell=11,p=67)
           and (ell=13,p=79), the two counterexamples this script is
           required to reproduce.  Exit 0 iff both are found within budget.
           Typical run time: a few seconds.

    python3 experimental/scripts/l1_bigfiber_e3_search.py --ell 17 --p 103 --seed 0 --max-tries 2000
        -> run the constructor at an arbitrary (ell,p), sweeping seeds from
           --seed.  Exit 0 iff a violation is found within --max-tries.

    python3 experimental/scripts/l1_bigfiber_e3_search.py --all
        -> ALSO best-effort attempts (ell=11,p=199), (ell=17,p=103),
           (ell=23,p=139), (ell=13,p=313) (the harder shipped
           counterexamples); does not affect the exit code (informational
           only -- these are not required to succeed by this constructor).
"""
import sys
import time
import argparse

# =====================================================================================
# exact F_p arithmetic (self-contained, independent implementation)
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
    raise RuntimeError("no generator found")

def inv(a, p):
    return pow(a % p, p - 2, p)

class LCG:
    """Deterministic, version-independent PRNG (never used to assert existence
    of anything -- only to pick seeded search choices)."""
    def __init__(self, seed):
        self.s = seed & ((1 << 64) - 1)

    def nxt(self):
        self.s = (self.s * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)
        return self.s >> 17

    def randint(self, lo, hi):  # inclusive
        return lo + self.nxt() % (hi - lo + 1)

    def shuffle(self, seq):
        a = list(seq)
        for i in range(len(a) - 1, 0, -1):
            j = self.randint(0, i)
            a[i], a[j] = a[j], a[i]
        return a

# =====================================================================================
# exact-rank / nullspace linear algebra over F_p (own implementation)
# =====================================================================================
def rank_Fp(rows, ncols, p):
    if not rows:
        return 0
    A = [r[:] for r in rows]
    m = len(A)
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
        r += 1
        if r == m:
            break
    return r

def nullspace_basis(rows, ncols, p):
    """Basis of {v in F_p^ncols : row . v = 0 for every row}."""
    if not rows:
        return [[1 if i == j else 0 for i in range(ncols)] for j in range(ncols)]
    A = [r[:] for r in rows]
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
    pivset = set(piv)
    basis = []
    for free in range(ncols):
        if free in pivset:
            continue
        v = [0] * ncols
        v[free] = 1
        for i, c in enumerate(piv):
            v[c] = (-A[i][free]) % p
        basis.append(v)
    return basis

def vpow(x, ell, p):
    """(x^1, x^2, ..., x^(ell-1)) mod p -- the constant-free coordinate row."""
    return [pow(x, r, p) for r in range(1, ell)]

def fiber_rows(points, ell, p):
    """Coincidence rows for one fiber: v(x_i) - v(x_0), i = 1..len-1."""
    if len(points) < 2:
        return []
    v0 = vpow(points[0], ell, p)
    rows = []
    for x in points[1:]:
        vx = vpow(x, ell, p)
        rows.append([(v0[r] - vx[r]) % p for r in range(ell - 1)])
    return rows

# =====================================================================================
# the constructor
# =====================================================================================
def construct(ell, p, seed=0, subset_tries=10, verbose=False):
    """One deterministic attempt (given ell, p, seed) at the plant-big-fibers-
    then-exact-solve search.  Returns (gamma, planted_sizes) or (None, [])
    if the rank budget was already saturated before any fiber could be
    placed (rare; the caller should just try the next seed)."""
    if not (is_prime(p) and is_prime(ell) and (p - 1) % ell == 0):
        raise ValueError("need ell, p prime with ell | (p-1); got ell=%r p=%r" % (ell, p))
    n = (p - 1) // ell
    g = find_gen(p)
    zeta = pow(g, n, p)
    H = [pow(zeta, j, p) for j in range(ell)]
    cosets = [[pow(g, i, p) * h % p for h in H] for i in range(n)]

    rng = LCG(seed)
    order = rng.shuffle(range(n))

    rows = []
    fiber_sizes = []
    lo_target = max(3, (ell - 1) // 2 - 1)
    hi_target = (ell + 1) // 2 + 2

    for ci in order:
        coset_pts = cosets[ci]
        cap = (ell - max(fiber_sizes)) if fiber_sizes else (ell - 1)
        target = rng.randint(lo_target, hi_target)
        size = min(target, cap, ell - 1)
        placed = False
        while size >= 3:
            accepted = None
            for _ in range(subset_tries):
                idxs = rng.shuffle(range(ell))[:size]
                pts = [coset_pts[j] for j in idxs]
                new_rows = fiber_rows(pts, ell, p)
                trial = rows + new_rows
                if rank_Fp(trial, ell - 1, p) <= ell - 2:
                    accepted = trial
                    break
            if accepted is not None:
                rows = accepted
                fiber_sizes.append(size)
                placed = True
                if verbose:
                    print("    coset %d: planted fiber size %d (rank now %d)"
                          % (ci, size, rank_Fp(rows, ell - 1, p)))
                break
            size -= 1
        if verbose and not placed:
            print("    coset %d: no legal fiber size >= 3 (cap was %d)" % (ci, cap))

    basis = nullspace_basis(rows, ell - 1, p)
    if not basis:
        return None, fiber_sizes
    gm = basis[0]
    nz = [i for i, c in enumerate(gm) if c % p]
    if not nz:
        return None, fiber_sizes
    top = max(nz)
    s = inv(gm[top], p)
    gamma = [(c * s) % p for c in gm]
    return gamma, fiber_sizes

def true_spectrum(gamma, p, ell):
    """Re-evaluate Gamma on EVERY coset of F_p^* (grouping by x^ell, Horner
    evaluation) to read the actual realized spectrum -- never assumed from
    the planted structure."""
    grp = {}
    for x in range(1, p):
        lab = pow(x, ell, p)
        v = 0
        xr = 1
        for r in range(1, ell):
            xr = xr * x % p
            if gamma[r - 1]:
                v = (v + gamma[r - 1] * xr) % p
        d = grp.setdefault(lab, {})
        d[v] = d.get(v, 0) + 1
    return sorted((max(d.values()) for d in grp.values()), reverse=True)

def E3(spec):
    return sum(mu - 2 for mu in spec if mu >= 3)

def search(ell, p, seed0=0, max_tries=1000, subset_tries=10, verbose=False):
    """Sweep seeds seed0, seed0+1, ... (deterministic) until E_3 > ell-2 is
    found or max_tries is exhausted.  Returns a result dict or None."""
    for k in range(max_tries):
        seed = seed0 + k
        gamma, sizes = construct(ell, p, seed=seed, subset_tries=subset_tries, verbose=False)
        if gamma is None:
            continue
        spec = true_spectrum(gamma, p, ell)
        e3 = E3(spec)
        if e3 > ell - 2:
            return {"ell": ell, "p": p, "seed": seed, "planted_sizes": sizes,
                    "gamma": gamma, "spectrum_head": spec[:10], "E3": e3, "tries": k + 1}
    return None

# =====================================================================================
# CLI
# =====================================================================================
REQUIRED_DEFAULT_TARGETS = [(11, 67), (13, 79)]
BEST_EFFORT_TARGETS = [(11, 199), (17, 103), (23, 139), (13, 313)]

def report(res, ell, p):
    if res is None:
        print("  ell=%2d p=%4d : NOT FOUND within budget" % (ell, p))
        return False
    print("  ell=%2d p=%4d : FOUND at seed=%d (%d tries)  planted_sizes=%s"
          % (ell, p, res["seed"], res["tries"], res["planted_sizes"]))
    print("      gamma (X^1..X^%d) = %s" % (ell - 1, res["gamma"]))
    print("      TRUE spectrum head = %s   E_3 = %d   (ell-2 = %d)   E_3 > ell-2: %s"
          % (res["spectrum_head"], res["E3"], ell - 2, res["E3"] > ell - 2))
    return res["E3"] > ell - 2

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ell", type=int, default=None, help="prime ell (needs --p too)")
    ap.add_argument("--p", type=int, default=None, help="prime p, ell | p-1 (needs --ell too)")
    ap.add_argument("--seed", type=int, default=0, help="deterministic sweep start seed (default 0)")
    ap.add_argument("--max-tries", type=int, default=1000, help="seed-sweep budget per target (default 1000)")
    ap.add_argument("--subset-tries", type=int, default=10, help="random point-subsets tried per fiber size (default 10)")
    ap.add_argument("--all", action="store_true", help="also best-effort attempt the harder shipped counterexample primes")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    t0 = time.time()
    print("=" * 90)
    print(" l1_bigfiber_e3_search: plant-big-fibers-then-exact-solve KEY LEMMA counterexample search")
    print("=" * 90)

    if args.ell is not None or args.p is not None:
        if args.ell is None or args.p is None:
            print("error: --ell and --p must be given together", file=sys.stderr)
            sys.exit(2)
        print("Custom target ell=%d p=%d, seed sweep from %d (max %d tries):"
              % (args.ell, args.p, args.seed, args.max_tries))
        res = search(args.ell, args.p, seed0=args.seed, max_tries=args.max_tries,
                     subset_tries=args.subset_tries, verbose=args.verbose)
        ok = report(res, args.ell, args.p)
        print("=" * 90)
        print(" RESULT: %s   (%.1fs)" % ("VIOLATION CONSTRUCTED (E_3 > ell-2)" if ok else "NOT FOUND", time.time() - t0))
        sys.exit(0 if ok else 1)

    print("Default targets (required, must both succeed): %s" % REQUIRED_DEFAULT_TARGETS)
    all_ok = True
    for ell, p in REQUIRED_DEFAULT_TARGETS:
        res = search(ell, p, seed0=args.seed, max_tries=args.max_tries,
                     subset_tries=args.subset_tries, verbose=args.verbose)
        ok = report(res, ell, p)
        all_ok = all_ok and ok

    if args.all:
        print("-" * 90)
        print("Best-effort targets (--all; not required to succeed):")
        for ell, p in BEST_EFFORT_TARGETS:
            res = search(ell, p, seed0=args.seed, max_tries=args.max_tries,
                         subset_tries=args.subset_tries, verbose=args.verbose)
            report(res, ell, p)

    print("=" * 90)
    print(" RESULT: %s   (%.1fs)" % ("ALL REQUIRED DEFAULT TARGETS CONSTRUCTED" if all_ok else "FAILURE", time.time() - t0))
    sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    main()
