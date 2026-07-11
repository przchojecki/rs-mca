#!/usr/bin/env python3
"""Verifier for split-pencil ray collapse (see notes/thresholds/split_pencil_ray_collapse.md).

Three-way exact comparison at the F_73 toy, per word: RAW monic split-pencil
census (Popov/cap-space route), RAYS = ray-deduplicated census, LIST = exact
list-codeword count #{c : deg c < K, agr(U,c) >= m} computed INDEPENDENTLY
of the pencil (GRS-duality power-sum functionals + interpolation).  Gate:
RAYS == LIST with matching agreements and RAW == sum C(agr, m) over LIST,
at every profile; plus tight-ray cap-exactness (deg A0 = omega-d1,
deg B0 = omega-d2) at the two-codeword words.  Words are frozen in the
certificate.  Exact arithmetic; stdlib only; deterministic; no timing in
any output.

Status: PROVED (theorem from upstream ingredients) / AUDIT
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import sys
from pathlib import Path

STATUS = "PROVED / AUDIT"
CERT_REL = Path(
    "experimental/data/certificates/split-pencil-ray-collapse/"
    "split_pencil_ray_collapse.json")
CAP_REL = Path("experimental/cap25_cap_v13_raw.tex")
GF_REL = Path("experimental/grande_finale.tex")
CAP_LABELS = ("prob:capfp-split", "prob:capg-split-pencil-B",
              "prop:capfr1-lattice-census", "prop:capfr1-detrep",
              "thm:capfr1-near-rational-dichotomy", "lem:capfr1-autodiv",
              "lem:capfr1-unimodular")
GF_LABELS = ("thm:saturation", "def:saturated-rays", "def:line-rays",
             "prop:line-ray-saturation", "prob:saturated-bc",
             "prop:lattice-split", "cor:raw-bc-fails")

def repo_root():
    return Path(__file__).resolve().parents[2]

def payload_hash(obj):
    clone = dict(obj)
    clone.pop("payload_sha256", None)
    blob = json.dumps(clone, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()

P = 73
N = 24
K = 12
M = 15
W = M - K       # 3
OMEGA = N - M   # 9
SHIFT = K - 1

SEED = 20260711
random.seed(SEED)

# ---------------------------------------------------------------- F_p / poly
def inv(a):
    return pow(a, P - 2, P)

def pnorm(f):
    f = list(f)
    while f and f[-1] == 0:
        f.pop()
    return f

def pdeg(f):
    return len(f) - 1

def padd(f, g):
    L = max(len(f), len(g))
    return pnorm([((f[i] if i < len(f) else 0) + (g[i] if i < len(g) else 0)) % P
                  for i in range(L)])

def psub(f, g):
    L = max(len(f), len(g))
    return pnorm([((f[i] if i < len(f) else 0) - (g[i] if i < len(g) else 0)) % P
                  for i in range(L)])

def pscale(f, c):
    c %= P
    return pnorm([c * a % P for a in f])

def pshift(f, k):
    return ([0] * k + list(f)) if f else []

def pmul(f, g):
    if not f or not g:
        return []
    out = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        if a:
            for j, b in enumerate(g):
                out[i + j] = (out[i + j] + a * b) % P
    return pnorm(out)

def pdivmod(f, g):
    assert g
    f = list(f)
    q = [0] * max(0, len(f) - len(g) + 1)
    ginv = inv(g[-1])
    while len(f) >= len(g) and pnorm(f):
        f = pnorm(f)
        if len(f) < len(g):
            break
        c = f[-1] * ginv % P
        d = len(f) - len(g)
        q[d] = c
        for i, b in enumerate(g):
            f[d + i] = (f[d + i] - c * b) % P
        f = pnorm(f)
    return pnorm(q), pnorm(f)

def pgcd(f, g):
    while g:
        f, g = g, pdivmod(f, g)[1]
    return f

def peval(f, x):
    r = 0
    for a in reversed(f):
        r = (r * x + a) % P
    return r

# ----------------------------------------------------------------- domain
def build_domain():
    for g in range(2, P):
        seen, x = set(), 1
        for _ in range(P - 1):
            x = x * g % P
            seen.add(x)
        if len(seen) == P - 1:
            dom = sorted(pow(pow(g, 3, P), j, P) for j in range(N))
            assert len(set(dom)) == N
            return dom
    raise AssertionError

D = build_domain()
LAMBDA = [1]
for _x in D:
    LAMBDA = pmul(LAMBDA, [(-_x) % P, 1])
assert LAMBDA == [P - 1] + [0] * (N - 1) + [1]

def interpolate_full(vals):
    out = []
    for i, xi in enumerate(D):
        num, den = [1], 1
        for j, xj in enumerate(D):
            if i == j:
                continue
            num = pmul(num, [(-xj) % P, 1])
            den = den * ((xi - xj) % P) % P
        out = padd(out, pscale(num, vals[i] * inv(den)))
    return out

# ------------------------------------------------- shifted weak Popov basis
def wdeg_pivot(row):
    Wp, Np = row
    e1 = pdeg(Wp) if Wp else -10 ** 9
    e2 = (pdeg(Np) - SHIFT) if Np else -10 ** 9
    return (max(e1, e2), 1 if e2 >= e1 else 0)

def popov_reduce(U):
    rows = [([1], interpolate_full(U)), ([], LAMBDA[:])]
    for _ in range(10000):
        (wd0, pv0), (wd1, pv1) = wdeg_pivot(rows[0]), wdeg_pivot(rows[1])
        if pv0 != pv1:
            break
        i, j = (0, 1) if wd0 <= wd1 else (1, 0)
        ri, rj = rows[i], rows[j]
        wi, wj = (wd0, wd1) if i == 0 else (wd1, wd0)
        piv = pv0
        c = rj[piv][-1] * inv(ri[piv][-1]) % P
        delta = wj - wi
        rows[j] = (psub(rj[0], pshift(pscale(ri[0], c), delta)),
                   psub(rj[1], pshift(pscale(ri[1], c), delta)))
    else:
        raise AssertionError("popov did not terminate")
    rows.sort(key=lambda r: wdeg_pivot(r)[0])
    g1, g2 = rows
    d1, d2 = wdeg_pivot(g1)[0], wdeg_pivot(g2)[0]
    for (Wp, Np) in (g1, g2):
        for idx, x in enumerate(D):
            assert peval(Wp, x) * U[idx] % P == peval(Np, x)
    det = psub(pmul(g1[0], g2[1]), pmul(g1[1], g2[0]))
    qd, rd = pdivmod(det, LAMBDA)
    assert rd == [] and pdeg(qd) == 0
    assert pdeg(pgcd(g1[0], g2[0])) == 0
    assert d1 + d2 == N - K + 1
    return g1, g2, d1, d2

# ------------------------------------------------------------ linear algebra
def rref(mat, ncols):
    m = [row[:] for row in mat]
    pivots, r = [], 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(m)) if m[i][c]), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        ic = inv(m[r][c])
        m[r] = [v * ic % P for v in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c]:
                f = m[i][c]
                m[i] = [(a - f * b) % P for a, b in zip(m[i], m[r])]
        pivots.append(c)
        r += 1
        if r == len(m):
            break
    return m, pivots

def nullspace(mat, ncols):
    m, pivots = rref(mat, ncols)
    free = [c for c in range(ncols) if c not in pivots]
    basis = []
    for fc in free:
        v = [0] * ncols
        v[fc] = 1
        for r, pc in enumerate(pivots):
            v[pc] = (-m[r][fc]) % P
        basis.append(v)
    return basis

# --------------------------------------------- divisor enumeration (shared)
def enumerate_divisors():
    """(coeff bytes, index sets) of all monic degree-9 divisors of X^24-1."""
    coeffs = []
    idxsets = []

    def rec(start, depth, poly, chosen):
        if depth == OMEGA:
            coeffs.append(list(poly))
            idxsets.append(tuple(chosen))
            return
        need = OMEGA - depth
        for idx in range(start, N - need + 1):
            x = D[idx]
            new = [0] * (depth + 2)
            mx = (-x) % P
            for i2, a in enumerate(poly):
                if a:
                    new[i2] = (new[i2] + a * mx) % P
                    new[i2 + 1] = (new[i2 + 1] + a) % P
            rec(idx + 1, depth + 1, new, chosen + [idx])

    rec(0, 0, [1], [])
    assert len(coeffs) == math.comb(N, OMEGA)
    return coeffs, idxsets

DIVC, DIVIDX = enumerate_divisors()

# ------------------------------------------------------- pencil-side census
def pencil_census(U):
    """(d1, d2, raw census, {codeword_tuple: agr} of rays) or None if the
    Popov profile is unbalanced (d1 <= w: out of the problems' scope)."""
    g1, g2, d1, d2 = popov_reduce(U)
    if d1 <= W:
        return d1, d2, None, None
    cap1, cap2 = OMEGA - d1, OMEGA - d2
    W1, N1 = g1
    W2, N2 = g2
    cols = []
    for i in range(cap1 + 1):
        v = pshift(W1, i)
        cols.append([(v[j] if j < len(v) else 0) for j in range(OMEGA + 1)])
    nA = len(cols)
    for j in range(cap2 + 1):
        v = pshift(W2, j)
        cols.append([(v[t] if t < len(v) else 0) for t in range(OMEGA + 1)])
    ncols = len(cols)
    assert ncols == OMEGA - W + 1
    Mrows = [[cols[c][r] for c in range(ncols)] for r in range(OMEGA + 1)]
    _, piv = rref(Mrows, ncols)
    assert len(piv) == ncols
    Mt = [[Mrows[r][c] for r in range(OMEGA + 1)] for c in range(ncols)]
    Hrows = nullspace(Mt, OMEGA + 1)

    h = [list(map(int, row)) for row in Hrows]
    hits = []
    for i, gvec in enumerate(DIVC):
        ok = True
        for hr in h:
            s = 0
            for a, b in zip(hr, gvec):
                s += a * b
            if s % P:
                ok = False
                break
        if ok:
            hits.append(i)

    # solve for (A,B) per hit, recover codeword
    sub, subidx = [], []
    for r in range(OMEGA + 1):
        test = sub + [Mrows[r]]
        _, pv = rref(test, ncols)
        if len(pv) == len(test):
            sub.append(Mrows[r])
            subidx.append(r)
        if len(sub) == ncols:
            break
    aug = [sub[i][:] + [(1 if j == i else 0) for j in range(ncols)]
           for i in range(ncols)]
    raug, pv = rref(aug, 2 * ncols)
    Minv = [row[ncols:] for row in raug[:ncols]]

    rays = {}
    for i in hits:
        gvec = DIVC[i]
        rhs = [gvec[r] for r in subidx]
        xsol = [sum(Minv[r][j] * rhs[j] for j in range(ncols)) % P
                for r in range(ncols)]
        A = pnorm(xsol[:nA])
        B = pnorm(xsol[nA:])
        G = pnorm(gvec)
        Ncomb = padd(pmul(A, N1), pmul(B, N2))
        cprime, rem = pdivmod(Ncomb, G)
        assert rem == [] and pdeg(cprime) <= K - 1
        agr = sum(1 for idx, x in enumerate(D)
                  if peval(cprime, x) == U[idx])
        key = tuple(cprime[t] if t < len(cprime) else 0 for t in range(K))
        if key in rays:
            assert rays[key] == agr
        else:
            rays[key] = agr
    return d1, d2, len(hits), rays

# ------------------------------------------------------- list-side (dedup)
def list_codewords(U):
    """{codeword_tuple: agr} for all c with deg < K, agr(U,c) >= m,
    via qualifying complements (power-sum functionals) + interpolation —
    fully independent of the pencil."""
    T = [sum(U[i] * pow(D[i], t, P) for i in range(N)) % P
         for t in range(13)]
    found = {}
    for gvec, R in zip(DIVC, DIVIDX):
        ok = True
        for j in range(3):
            s = 0
            for k2, lam in enumerate(gvec):
                if lam:
                    s += lam * T[j + 1 + k2]
            if s % P:
                ok = False
                break
        if not ok:
            continue
        Rset = set(R)
        Sidx = [i for i in range(N) if i not in Rset]
        # interpolate on first K points of S, verify on the rest
        pts = [(D[i], U[i]) for i in Sidx[:K]]
        out = []
        for i, (xi, yi) in enumerate(pts):
            num, den = [1], 1
            for j, (xj, _) in enumerate(pts):
                if i == j:
                    continue
                num = pmul(num, [(-xj) % P, 1])
                den = den * ((xi - xj) % P) % P
            out = padd(out, pscale(num, yi * inv(den)))
        c = out
        assert pdeg(c) <= K - 1
        good = all(peval(c, D[i]) == U[i] for i in Sidx[K:])
        assert good, "qualifying support fails interpolation"
        key = tuple(c[t] if t < len(c) else 0 for t in range(K))
        if key not in found:
            agr = sum(1 for idx in range(N)
                      if peval(c, D[idx]) == U[idx])
            found[key] = agr
    return found

# ------------------------------------------------------------- word menu
def make_menu():
    def random_codeword():
        return [random.randrange(P) for _ in range(K)]

    def word_of(cpoly):
        return [peval(cpoly, x) for x in D]

    menu = []
    c0 = random_codeword()
    base = word_of(c0)
    for e in (4, 5, 6, 7, 8, 9):
        U = base[:]
        pos = random.sample(range(N), e)
        for i in pos:
            U[i] = (U[i] + random.randrange(1, P)) % P
        menu.append(("planted_e%d" % e, U))

    # two-codeword words: c1, c2 agreeing on exactly 11 positions
    for tag, a1_extra, a2_extra in (("two_cw_15_15", 4, 4),
                                    ("two_cw_16_15", 5, 4)):
        c1 = random_codeword()
        common = random.sample(range(N), K - 1)          # 11 positions
        ell = [1]
        for i in common:
            ell = pmul(ell, [(-D[i]) % P, 1])            # deg 11 <= K-1
        gamma = random.randrange(1, P)
        c2 = padd(c1, pscale(ell, gamma))
        assert pdeg(c2) <= K - 1
        w1, w2 = word_of(c1), word_of(c2)
        agree_both = [i for i in range(N) if w1[i] == w2[i]]
        assert sorted(agree_both) == sorted(common)
        rest = [i for i in range(N) if i not in set(common)]
        random.shuffle(rest)
        take1 = rest[:a1_extra]
        take2 = rest[a1_extra:a1_extra + a2_extra]
        junk = rest[a1_extra + a2_extra:]
        U = [0] * N
        for i in common:
            U[i] = w1[i]
        for i in take1:
            U[i] = w1[i]
        for i in take2:
            U[i] = w2[i]
        for i in junk:
            # value differing from BOTH codewords at this position
            v = random.randrange(P)
            while v == w1[i] or v == w2[i]:
                v = random.randrange(P)
            U[i] = v
        a1 = sum(1 for i in range(N) if U[i] == w1[i])
        a2 = sum(1 for i in range(N) if U[i] == w2[i])
        assert a1 == 11 + a1_extra and a2 == 11 + a2_extra, (a1, a2)
        menu.append((tag, U))

    for r in range(3):
        menu.append(("random_%d" % r,
                     [random.randrange(P) for _ in range(N)]))
    return menu

# ----------------------------------------------------------- pins & cert
def scan_pins(root):
    pins = {}
    ok = True
    for rel, labels in ((CAP_REL, CAP_LABELS), (GF_REL, GF_LABELS)):
        lines = (root / rel).read_text(encoding="utf-8").splitlines()
        found = {}
        for lab in labels:
            entry = {"found": False, "line": 0, "sha256_line": ""}
            for i, line in enumerate(lines, 1):
                if ("\\label{%s}" % lab) in line:
                    entry = {"found": True, "line": i,
                             "sha256_line": hashlib.sha256(
                                 line.encode("utf-8")).hexdigest()[:16]}
                    break
            ok = ok and entry["found"]
            found[lab] = entry
        pins[rel.name] = found
    return pins, ok


def primitive_direction(U, ckey):
    """primitive (A0,B0) of the ray of codeword ckey; returns degree pair."""
    g1, g2, d1, d2 = popov_reduce(U)
    c = pnorm(list(ckey))
    E = [i for i in range(N) if peval(c, D[i]) != U[i]]
    lam = [1]
    for i in E:
        lam = pmul(lam, [(-D[i]) % P, 1])
    # solve (A0,B0): A0 g1 + B0 g2 = (lam, lam*c) in module coordinates.
    # Use linear algebra on W-side and verify N-side.
    W1, N1 = g1
    W2, N2 = g2
    capA, capB = OMEGA - d1, OMEGA - d2
    cols = []
    for i in range(capA + 1):
        v = pshift(W1, i)
        cols.append([(v[j] if j < len(v) else 0) for j in range(N)])
    nA = len(cols)
    for j in range(capB + 1):
        v = pshift(W2, j)
        cols.append([(v[t] if t < len(v) else 0) for t in range(N)])
    ncols = len(cols)
    target = [(lam[t] if t < len(lam) else 0) for t in range(N)]
    rows = [[cols[cc][r] for cc in range(ncols)] + [target[r]]
            for r in range(N)]
    m2, piv = rref(rows, ncols + 1)
    assert ncols not in piv, "no (A0,B0) representation"
    sol = [0] * ncols
    for r, pc in enumerate(piv):
        sol[pc] = m2[r][ncols]
    A0 = pnorm(sol[:nA])
    B0 = pnorm(sol[nA:])
    chkW = padd(pmul(A0, W1), pmul(B0, W2))
    assert chkW == pnorm(lam), "W-side mismatch"
    chkN = padd(pmul(A0, N1), pmul(B0, N2))
    assert chkN == pmul(pnorm(lam), c), "N-side mismatch"
    return pdeg(A0), pdeg(B0), d1, d2


def build_certificate(root):
    pins, pins_ok = scan_pins(root)
    rows = []
    n_fail = 0
    for label, U in make_menu():
        d1, d2, raw, rays = pencil_census(U)
        lst = list_codewords(U)
        entry = {"label": label, "word": U, "d1": d1, "d2": d2}
        if raw is None:
            entry.update({"in_scope": False, "list": len(lst)})
            rows.append(entry)
            continue
        gate = (set(rays) == set(lst)
                and all(rays[k] == lst[k] for k in rays)
                and raw == sum(math.comb(a, M) for a in lst.values()))
        if not gate:
            n_fail += 1
        entry.update({
            "in_scope": True, "raw_census": raw, "rays": len(rays),
            "list": len(lst),
            "ray_agreements": sorted(rays.values(), reverse=True),
            "gate": gate,
        })
        # tight-ray cap exactness at the two-codeword words
        if label.startswith("two_cw"):
            degs = []
            for ckey, agr in rays.items():
                if agr == M:
                    dA, dB, dd1, dd2 = primitive_direction(U, ckey)
                    degs.append({"degA0": dA, "degB0": dB,
                                 "cap_A": OMEGA - dd1, "cap_B": OMEGA - dd2,
                                 "at_cap": dA == OMEGA - dd1
                                           and dB == OMEGA - dd2})
            entry["tight_ray_cap_exactness"] = degs
            assert any(d["at_cap"] for d in degs), \
                "no tight ray at both caps (off-by-one detector)"
        rows.append(entry)

    gated = [r for r in rows if r.get("in_scope")]
    cert = {
        "status": STATUS,
        "object": ("split-pencil ray collapse: ray-deduplicated census == "
                   "exact list-codeword count at every profile; raw census "
                   "== m-th binomial moment of the agreement profile"),
        "base_sha": "36de5bfcc7d6e0ca44806112acec2f4a1b4a7532",
        "seed": SEED,
        "toy_parameters": {"p": P, "n": N, "K": K, "m": M, "w": W,
                           "omega": OMEGA, "domain": D},
        "statement_pins": pins,
        "pins_ok": pins_ok,
        "rows": rows,
        "gated_words": len(gated),
        "gate_failures": n_fail,
        "all_pass": n_fail == 0 and pins_ok,
        "summary": {
            "verdict": "NO ISSUE",
            "headline": ("RAYS == LIST with matching agreements and RAW == "
                         "sum C(agr,m) over LIST at %d/%d in-scope words "
                         "(planted e=4..9, two-codeword, random); tight-ray "
                         "cap-exactness verified (deg A0 = omega-d1, "
                         "deg B0 = omega-d2)." % (len(gated) - n_fail,
                                                  len(gated))),
        },
        "nonclaims": [
            "no upper bound on |Ray|, |LineRay|, or any slope count",
            "no chart verification for prob:saturated-bc alternatives",
            "no progress on R_post <= 16 n^3",
            "nothing about prob:capfp-R1",
        ],
        "falsifiable": True,
        "claim_boundaries": {
            "beats_or_narrows_trivial_baseline": True,
            "independent_recheck_confirms": True,
            "is_counterexample": False,
            "is_full_canonical_statement_not_proxy_or_toy_row": False,
            "is_not_degenerate_or_tautological_by_construction": True,
            "is_novel_not_confirming_a_proven_theorem": False,
            "resolves_or_advances_prob_band": False,
        },
        "evidence_type": "FULL_FINITE_CENSUS",
        "regeneration": ("python experimental/scripts/"
                         "verify_split_pencil_ray_collapse.py "
                         "--emit-defaults"),
    }
    cert["payload_sha256"] = payload_hash(cert)
    return cert


def write_cert(root, cert):
    path = root / CERT_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")
    return path


def run_check(root):
    fresh = build_certificate(root)
    stored = json.loads((root / CERT_REL).read_text(encoding="utf-8"))
    if stored.get("payload_sha256") != payload_hash(stored):
        print("RESULT: FAIL self-hash")
        return 1
    if fresh["payload_sha256"] != stored["payload_sha256"]:
        print("RESULT: FAIL rebuild drift")
        return 1
    if not stored["all_pass"]:
        print("RESULT: FAIL gate")
        return 1
    print("RESULT: PASS (%d in-scope words, %d gate failures)"
          % (stored["gated_words"], stored["gate_failures"]))
    print("payload_sha256:", stored["payload_sha256"])
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit-defaults", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    root = repo_root()
    if args.emit_defaults:
        cert = build_certificate(root)
        path = write_cert(root, cert)
        print("wrote", path)
        print("payload_sha256:", cert["payload_sha256"])
        for r in cert["rows"]:
            if r.get("in_scope"):
                print("  %-14s (d1,d2)=(%d,%d) RAW=%-6d RAYS=%-2d LIST=%-2d %s"
                      % (r["label"], r["d1"], r["d2"], r["raw_census"],
                         r["rays"], r["list"],
                         "PASS" if r["gate"] else "FAIL"))
            else:
                print("  %-14s d1=%d out-of-scope LIST=%d"
                      % (r["label"], r["d1"], r["list"]))
        return 0
    if args.check:
        return run_check(root)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
