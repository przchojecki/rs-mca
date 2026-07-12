#!/usr/bin/env python3
"""LineRay dedup census re-recording (statement packet; refutes nothing).

Pinned (cap25_cap_v13_raw.tex / grande_finale.tex @ base sha in the cert):
  prob:capfp-R1, prob:capfr1-rank-one-census, prob:capg-split-pencil-B,
  prob:capfr1-split-pencil, prob:capg-active-BC   the five subsumed problems
  cap25 L8077 (content pin)                       the tier-(4) work-queue item
  prop:capg-census-floor, rem:capg-subfield-scope the floors and their scope
  lem:capg-witness, rem:capg-witnessrel           pole-line witness rigidity
  rem:capg-band, rem:capg-boundary-offbyone,
  prob:capfr1-normalized-band                     chain re-pointing
  gf def:line-rays, prop:line-ray-saturation,
  prob:saturated-bc                               the dedup chain objects

Recorded target (OPEN; see notes/thresholds/lineray_census_rerecording.md):
  |LineRay_E(u,v;m)| <= e^{o(n)} max(1, ceil(C(n,m) p^-w'), C(n,m) q^-(w'-1))
  per line; per word at interior profile d1: |Ray(U;m)| <= e^{o(n)} max(1,
  ceil(C(n,K-1+d1) p^-(d1-1)), C(n,m) q^-(w'-1)).

Gates:
  A. Oracle replay: consume the in-tree #666/#679 certificates (payload
     self-hash verified) and replay their banked identities: RAYS == LIST,
     RAW == sum C(agr,m); #R1 == sum_z mult(z), lineray == sum_z #rays(z),
     loss-1 (N_slopes <= lineray) and loss-2 (#R1 - lineray) exact; the
     recorded per-line dedup model HOLDS at every #679 menu line incl. the
     plants.
  B. F_73 survival gates (n=24, K=12, m=15, w'=3): boundary prefix word
     RAW == RAYS == LIST == heaviest depth-3 fiber >= ceil(C(24,15) 73^-3),
     all agreements exactly m, d1 = w'+1; interior level-m' words (d1=5,6):
     RAW == sum C(agr,m) with the level-m' rays == heaviest fiber and the
     stripping identity RAW = C(m',m)*RAYS + extras, d1 verified.  Deployed
     (exact big-int, Legendre + product tree): the paper-printed floors at
     (k,1116046) KB / (k,1116022) M31 reproduced; stripped dedup interior
     floors recomputed exactly; cross-links to the #679 certificate value
     and the budget-fit B_B displays asserted.
  C. NEW F_{p^2} toy (p=17, q=289, t^2=3; D = F_17^*, n=16, K=6, m=9,
     w'=3) so the p-term and q-term separate: pole line of the heaviest
     depth-3 prefix word has #R1 == |LineRay| == depth-2 witness fiber with
     every ray agreement exactly m at every tested alpha (pair-level
     survival + witness-fiber calibration), floor >= ceil(C(16,9) 17^-3),
     witnessed slope collision (N_slopes < |LineRay|); planted near-codeword
     line (e = w'+2) FAILS the corrected raw model and the literal q-scale
     model while |LineRay| HOLDS the recorded model with the p-term alive.
  D. Statement pins re-hashed (16-hex) at expected lines.

Framing: re-recording of the tier-(4) census lemma feeding prob:saturated-bc
alternative (b); not a new independent problem; not a counterexample.

Status: PROVED (free parts) + MODEL CORRECTION + OPEN (recorded target) / AUDIT
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import sys
from operator import mul
from pathlib import Path
from typing import Any

STATUS = "PROVED (free parts) + MODEL CORRECTION + OPEN (recorded target) / AUDIT"
CERT_REL = Path(
    "experimental/data/certificates/lineray-census-rerecording/"
    "lineray_census_rerecording.json"
)
CAP_REL = Path("experimental/cap25_cap_v13_raw.tex")
GF_REL = Path("experimental/grande_finale.tex")
ORACLE_R1_REL = Path(
    "experimental/data/certificates/r1-rawcount-refutation/"
    "r1_rawcount_refutation.json"
)
ORACLE_SPC_REL = Path(
    "experimental/data/certificates/split-pencil-ray-collapse/"
    "split_pencil_ray_collapse.json"
)
SEED = 20260712

# statement pins: (kind, key, expected_line); kind "label" -> \label{key},
# kind "content" -> literal substring
CAP_PINS = (
    ("label", "prob:capfp-R1", 8278),
    ("label", "prob:capfr1-rank-one-census", 7819),
    ("label", "prob:capg-split-pencil-B", 9842),
    ("label", "prob:capfr1-split-pencil", 8012),
    ("content", "Main aperiodic effort", 8077),
    ("label", "prob:capg-active-BC", 9919),
    ("label", "prop:capg-census-floor", 9728),
    ("label", "rem:capg-subfield-scope", 9874),
    ("label", "lem:capg-witness", 9183),
    ("label", "rem:capg-witnessrel", 9246),
    ("label", "rem:capg-band", 9397),
    ("label", "rem:capg-boundary-offbyone", 9828),
    ("label", "prob:capfr1-normalized-band", 7639),
)
GF_PINS = (
    ("label", "def:line-rays", 1857),
    ("label", "prop:line-ray-saturation", 1867),
    ("label", "prob:saturated-bc", 2191),
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def payload_hash(obj: dict[str, Any]) -> str:
    clone = dict(obj)
    clone.pop("payload_sha256", None)
    blob = json.dumps(clone, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def holds(count, terms):
    """count <= max(1, terms...) with terms as exact fractions [num, den]."""
    return count <= 1 or any(count * den <= num for num, den in terms)


# ======================================================================
# Gate D: statement pins
# ======================================================================
def scan_pins(root: Path) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for rel, pins in ((CAP_REL, CAP_PINS), (GF_REL, GF_PINS)):
        lines = (root / rel).read_text(encoding="utf-8").splitlines()
        found: dict[str, Any] = {}
        for kind, key, expected in pins:
            needle = ("\\label{%s}" % key) if kind == "label" else key
            hit = None
            for i, line in enumerate(lines, 1):
                if needle in line:
                    hit = (i, line)
                    break
            assert hit is not None, "pin missing: %s in %s" % (key, rel.name)
            assert hit[0] == expected, \
                "pin moved: %s at L%d (expected L%d)" % (key, hit[0], expected)
            found[key] = {
                "kind": kind,
                "line": hit[0],
                "sha256_line": hashlib.sha256(
                    hit[1].encode("utf-8")).hexdigest()[:16],
            }
        out[rel.name] = found
    return out


# ======================================================================
# Gate A: oracle certificate replay
# ======================================================================
def gate_a(root: Path) -> dict[str, Any]:
    spc = json.loads((root / ORACLE_SPC_REL).read_text(encoding="utf-8"))
    r1 = json.loads((root / ORACLE_R1_REL).read_text(encoding="utf-8"))
    assert spc.get("payload_sha256") == payload_hash(spc), "spc self-hash"
    assert r1.get("payload_sha256") == payload_hash(r1), "r1 self-hash"
    assert spc["all_pass"] is True
    assert r1["summary"]["verdict"] == "COUNTEREXAMPLE"

    n, m, p = 24, 15, 73
    w = m - 12  # w' = 3
    # recorded per-line dedup model at the F_73 toy row (p = q):
    ceil_p_term = -(-math.comb(n, m) // p ** w)          # ceil(C(n,m) p^-w')
    p_term = [math.comb(n, m), p ** w]
    q_term = [math.comb(n, m), p ** (w - 1)]

    # --- #666 rows: RAYS == LIST, RAW == sum C(agr, m)
    spc_rows = []
    for row in spc["rows"]:
        if not row.get("in_scope"):
            continue
        assert row["gate"] is True
        assert row["rays"] == row["list"]
        assert row["raw_census"] == sum(
            math.comb(a, m) for a in row["ray_agreements"])
        spc_rows.append({"label": row["label"], "raw": row["raw_census"],
                         "rays": row["rays"], "list": row["list"]})
    assert len(spc_rows) == 11

    # --- #679 lines: identities + recorded dedup model gate
    r1_rows = []
    for row in r1["toy_rows"]:
        mults = [sr[1] for sr in row["slope_rows"]]
        profs = [sr[2] for sr in row["slope_rows"]]
        assert all(m2 == sum(math.comb(a, m) for a in pf)
                   for m2, pf in zip(mults, profs))
        assert sum(mults) == row["counts"]["rank_one"]
        lineray = sum(len(pf) for pf in profs)
        assert lineray == row["lineray_count"]
        n_slopes = len(row["slope_rows"])
        assert n_slopes == row["slopes_hit"]
        assert n_slopes <= lineray  # loss-1
        loss2 = row["counts"]["rank_one"] - lineray
        assert loss2 == sum(math.comb(a, m) - 1 for pf in profs for a in pf)
        dedup_holds = holds(lineray, [[ceil_p_term, 1], q_term])
        assert dedup_holds, "recorded dedup model fails at %s" % row["label"]
        # replay the banked raw verdicts
        assert row["corrected_holds_raw"] == holds(
            row["counts"]["rank_one"], [p_term, q_term])
        if row["e"] is not None:
            assert not row["corrected_holds_raw"]
        r1_rows.append({
            "label": row["label"], "rank_one": row["counts"]["rank_one"],
            "lineray": lineray, "n_slopes": n_slopes, "loss2": loss2,
            "recorded_dedup_model_holds": True,
        })
    assert [r["lineray"] for r in r1_rows] == [206, 210, 211, 218]
    assert [r["loss2"] for r in r1_rows] == [15503, 3905, 905, 0]

    return {
        "oracle_spc": {"path": str(ORACLE_SPC_REL),
                       "payload_sha256": spc["payload_sha256"],
                       "rows_replayed": len(spc_rows)},
        "oracle_r1": {"path": str(ORACLE_R1_REL),
                      "payload_sha256": r1["payload_sha256"],
                      "rows_replayed": len(r1_rows)},
        "r1_deployed_corrected_middle_ceil":
            r1["deployed"]["budget"]["corrected_middle_ceil"],
        "toy_dedup_model_terms": {"ceil_p_term": ceil_p_term,
                                  "q_term": q_term},
        "spc_rows": spc_rows,
        "r1_rows": r1_rows,
        "all_pass": True,
    }


# ======================================================================
# F_73 layer (Gate B) -- template arithmetic (r1-rawcount harness style)
# ======================================================================
P = 73
N = 24
K = 12
M = 15
W = M - K       # 3
OMEGA = N - M   # 9
SHIFT = K - 1


def inv(a: int) -> int:
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
    return pnorm([((f[i] if i < len(f) else 0) + (g[i] if i < len(g) else 0))
                  % P for i in range(L)])


def psub(f, g):
    L = max(len(f), len(g))
    return pnorm([((f[i] if i < len(f) else 0) - (g[i] if i < len(g) else 0))
                  % P for i in range(L)])


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


def wdeg_pivot(row):
    Wp, Np = row
    e1 = pdeg(Wp) if Wp else -10 ** 9
    e2 = (pdeg(Np) - SHIFT) if Np else -10 ** 9
    return (max(e1, e2), 1 if e2 >= e1 else 0)


def popov_d1(U):
    """d1 of M_U via shifted weak Popov reduction (verified properties)."""
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
    assert wdeg_pivot(g1)[1] != wdeg_pivot(g2)[1]
    return d1


def enumerate_complements():
    """coefficient tuples of Lambda_R for all 9-subsets R, DFS (lex) order."""
    out = []

    def rec(start, depth, poly):
        if depth == OMEGA:
            out.append(tuple(poly))
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
            rec(idx + 1, depth + 1, new)

    rec(0, 0, [1])
    assert len(out) == math.comb(N, OMEGA)
    return out


LAMR = enumerate_complements()


def word_census(word):
    """(raw hit count, {codeword_tuple: agr}) at threshold M, dimension K,
    via GRS-duality power-sum functionals + interpolation."""
    T = [sum(word[i] * pow(D[i], t, P) for i in range(N)) % P
         for t in range(13)]
    T1 = tuple(T[1:11])
    T2 = tuple(T[2:12])
    T3 = tuple(T[3:13])
    found = {}
    nhits = 0
    for lam in LAMR:
        if sum(map(mul, lam, T1)) % P:
            continue
        if sum(map(mul, lam, T2)) % P:
            continue
        if sum(map(mul, lam, T3)) % P:
            continue
        nhits += 1
        Sidx = [i for i in range(N) if peval(lam, D[i]) != 0]
        assert len(Sidx) == M
        pts = [(D[i], word[i]) for i in Sidx[:K]]
        out = []
        for i, (xi, yi) in enumerate(pts):
            num, den = [1], 1
            for j, (xj, _) in enumerate(pts):
                if i == j:
                    continue
                num = pmul(num, [(-xj) % P, 1])
                den = den * ((xi - xj) % P) % P
            out = padd(out, pscale(num, yi * inv(den)))
        for i in Sidx[K:]:
            assert peval(out, D[i]) == word[i]
        key = tuple(out[t] if t < len(out) else 0 for t in range(K))
        if key not in found:
            found[key] = sum(1 for idx in range(N)
                             if peval(out, D[idx]) == word[idx])
    return nhits, found


def heaviest_fiber(msize, depth):
    """heaviest fiber of Phi_{msize,depth} over F_73 msize-subsets of D,
    tracking only the leading coefficient window (windowed DFS)."""
    counts: dict[tuple, int] = {}

    def rec(start, chosen, w):
        if chosen == msize:
            z = tuple(w[1:depth + 1])
            counts[z] = counts.get(z, 0) + 1
            return
        need = msize - chosen
        for idx in range(start, N - need + 1):
            mx = (-D[idx]) % P
            nw = [0] * (depth + 1)
            for j in range(depth + 1):
                v = w[j]
                if j > 0:
                    v = (v + mx * w[j - 1]) % P
                nw[j] = v
            rec(idx + 1, chosen + 1, nw)

    rec(0, 0, [1] + [0] * depth)
    assert sum(counts.values()) == math.comb(N, msize)
    best = max(counts.values())
    zstar = min(z for z, c in counts.items() if c == best)
    return list(zstar), best


def prefix_word(msize, z):
    """evaluations on D of P = X^msize + sum z_h X^{msize-h}."""
    Pz = [0] * (msize + 1)
    Pz[msize] = 1
    for h, zz in enumerate(z, 1):
        Pz[msize - h] = zz
    return [peval(Pz, x) for x in D]


def gate_b_toy() -> dict[str, Any]:
    rows = []

    # boundary profile d1 = w'+1: level-m word, depth w' = 3
    z3, fib3 = heaviest_fiber(M, W)
    floor3 = -(-math.comb(N, M) // P ** W)
    U = prefix_word(M, z3)
    raw, cen = word_census(U)
    prof = sorted(cen.values(), reverse=True)
    d1 = popov_d1(U)
    assert d1 == W + 1
    assert raw == len(cen) == fib3, "boundary RAW == RAYS == fiber"
    assert all(a == M for a in cen.values()), "boundary agreements exactly m"
    assert fib3 >= floor3
    rows.append({
        "label": "boundary_d1_4", "level": M, "depth": W, "z": z3,
        "word": U, "d1": d1, "fiber": fib3, "ceil_floor": floor3,
        "raw": raw, "rays": len(cen), "profile": prof,
        "loss2": raw - len(cen), "extras": 0,
        "all_agr_exactly_level": True,
    })

    # interior profiles d1 = 5, 6: level-m' words, depth d1-1
    for d1_target in (W + 2, W + 3):
        mp = K - 1 + d1_target
        depth = d1_target - 1
        zp, fibp = heaviest_fiber(mp, depth)
        floorp = -(-math.comb(N, mp) // P ** depth)
        U = prefix_word(mp, zp)
        raw, cen = word_census(U)
        prof = sorted(cen.values(), reverse=True)
        d1 = popov_d1(U)
        assert d1 == d1_target
        n_at_mp = sum(1 for a in cen.values() if a == mp)
        extras = sorted((a for a in cen.values() if a != mp), reverse=True)
        assert n_at_mp == fibp, "level-m' rays == heaviest fiber"
        assert raw == sum(math.comb(a, M) for a in cen.values())
        assert raw == math.comb(mp, M) * fibp + sum(
            math.comb(a, M) for a in extras), "stripping identity"
        assert n_at_mp >= floorp
        assert fibp >= floorp
        rows.append({
            "label": "interior_d1_%d" % d1_target, "level": mp,
            "depth": depth, "z": zp, "word": U, "d1": d1, "fiber": fibp,
            "ceil_floor": floorp, "raw": raw, "rays": len(cen),
            "profile": prof, "rays_at_level": n_at_mp,
            "loss2": raw - len(cen), "extras": len(extras),
            "extra_agreements": extras,
            "raw_equals_Cmpm_times_fiber_plus_extras": True,
            "C_mp_m": math.comb(mp, M),
        })
    return {"rows": rows, "all_pass": True}


# ======================================================================
# Gate B deployed: exact big-int recompute (Legendre + product tree)
# ======================================================================
def sieve(limit):
    isp = bytearray([1]) * (limit + 1)
    isp[0:2] = b"\x00\x00"
    for i in range(2, int(limit ** 0.5) + 1):
        if isp[i]:
            isp[i * i::i] = bytearray(len(isp[i * i::i]))
    return [i for i in range(limit + 1) if isp[i]]


def legendre_e(a, b, p):
    e, pk = 0, p
    while pk <= a:
        e += a // pk - b // pk - (a - b) // pk
        pk *= p
    return e


def prod_tree(xs):
    while len(xs) > 1:
        xs = ([xs[i] * xs[i + 1] for i in range(0, len(xs) - 1, 2)]
              + ([xs[-1]] if len(xs) & 1 else []))
    return xs[0] if xs else 1


def exact_comb(a, b, primes):
    return prod_tree([pr ** legendre_e(a, b, pr)
                      for pr in primes if pr <= a and legendre_e(a, b, pr)])


def _lg2(x: int) -> float:
    e = x.bit_length() - 1
    if e <= 80:
        return math.log2(x)
    return math.log2(x >> (e - 80)) + (e - 80)


def lg2_display(x: int) -> str:
    """display-grade log2 string (top-80-bit mantissa; no verdict uses it)."""
    return "%.4f" % _lg2(x)


def lg2_frac_display(num: int, den: int) -> str:
    return "%.4f" % (_lg2(num) - _lg2(den))


def gate_b_deployed(r1_middle_ceil: int) -> dict[str, Any]:
    n_, K_ = 2 ** 21, 2 ** 20
    primes = sieve(n_)
    rows = {}
    for name, p_, m_, prints in (
            ("KB", 2 ** 31 - 2 ** 24 + 1, 1116046,
             {"boundary": "67.1", "interior": ["56.0", "43.9", "31.3"]}),
            ("M31", 2 ** 31 - 1, 1116022,
             {"boundary": "52.1", "interior": ["41.0", "28.9", "16.2"]})):
        w2 = m_ - K_
        C = exact_comb(n_, m_, primes)
        bf = -(-C // p_ ** w2)
        bf_disp = lg2_display(bf)
        assert ("%.1f" % round(float(bf_disp), 1)) == prints["boundary"]
        interior = []
        Cm, mp = C, m_
        for j in (1, 2, 3):
            Cm = Cm * (n_ - mp) // (mp + 1)
            mp += 1
            d1 = w2 + 1 + j
            pw = p_ ** (d1 - 1)
            stripped = -(-Cm // pw)
            Cmpm = math.comb(mp, m_)
            raw_ceil_form = Cmpm * stripped
            raw_unceiled_disp = lg2_frac_display(Cmpm * Cm, pw)
            assert ("%.1f" % round(float(raw_unceiled_disp), 1)) \
                == prints["interior"][j - 1], \
                "%s d1=w'+%d paper print" % (name, 1 + j)
            interior.append({
                "d1": "w'+%d" % (1 + j), "m_prime": mp,
                "stripped_dedup_floor": stripped,
                "stripped_log2_display": lg2_display(stripped),
                "raw_MB_ceil_form_log2_display": lg2_display(raw_ceil_form),
                "raw_MB_unceiled_log2_display": raw_unceiled_disp,
                "paper_prints": prints["interior"][j - 1],
                "collapsed_to_1": stripped == 1,
                "C_mprime_m": Cmpm if Cmpm.bit_length() <= 64
                else "2^" + lg2_display(Cmpm),
            })
        rows[name] = {
            "n": n_, "K": K_, "m": m_, "w_prime": w2, "p": p_,
            "boundary_floor_log2_display": bf_disp,
            "boundary_paper_prints": prints["boundary"],
            "interior": interior,
        }

    # cross-link 1: KB stripped first-interior == #679 corrected_middle_ceil
    kb_first = rows["KB"]["interior"][0]["stripped_dedup_floor"]
    assert kb_first == r1_middle_ceil == 65065153468

    # cross-link 2: budget-fit B_B displays.  List rows sit at depth w'
    # (the stripped first-interior values); MCA rows sit at the
    # witness-fiber depth w'-1 (one more ratio step at the same p-power).
    def comb_ratio_steps(name, m_, steps):
        p_ = rows[name]["p"]
        C = exact_comb(n_, m_, primes)
        return C, p_

    expects = {}
    for name, m_, wexp, keys in (
            ("KB", 1116046, 67471, ("35.9212", "35.7352")),
            ("M31", 1116022, 67447, ("20.9270", "20.7411"))):
        C, p_ = comb_ratio_steps(name, m_, 0)
        Cm, mp = C, m_
        disp = []
        for _ in (1, 2):
            Cm = Cm * (n_ - mp) // (mp + 1)
            mp += 1
            disp.append(lg2_display(-(-Cm // p_ ** wexp)))
        assert tuple(disp) == keys, (name, disp, keys)
        expects[name] = {"list_row_depth_wprime": disp[0],
                         "mca_row_witness_depth": disp[1]}

    return {"rows": rows,
            "crosslink_679_corrected_middle_ceil": kb_first,
            "crosslink_budget_fit_BB_displays": expects,
            "all_pass": True}


# ======================================================================
# Gate C: F_{p^2} toy (p = 17, q = 289, t^2 = 3), D = F_17^*, n = 16
# ======================================================================
PB = 17
NR2 = 3
Q2 = PB * PB
N2 = 16
K2 = 6
M2 = 9
W2 = M2 - K2      # w' = 3
OM2 = N2 - M2     # 7
Z0_2 = 18         # planted slope, = 1 + t (genuinely extension-valued)
SHIFT2 = K2 - 1

# element e = a + 17*b  <->  a + b*t with t^2 = 3
ADD2 = [[0] * Q2 for _ in range(Q2)]
MUL2 = [[0] * Q2 for _ in range(Q2)]
NEG2 = [0] * Q2
INV2 = [0] * Q2
for _e1 in range(Q2):
    _a1, _b1 = _e1 % PB, _e1 // PB
    NEG2[_e1] = ((-_a1) % PB) + PB * ((-_b1) % PB)
    for _e2 in range(Q2):
        _a2, _b2 = _e2 % PB, _e2 // PB
        ADD2[_e1][_e2] = ((_a1 + _a2) % PB) + PB * ((_b1 + _b2) % PB)
        MUL2[_e1][_e2] = ((_a1 * _a2 + NR2 * _b1 * _b2) % PB) \
            + PB * ((_a1 * _b2 + _a2 * _b1) % PB)
for _e in range(1, Q2):
    _a, _b = _e % PB, _e // PB
    _nrm = (_a * _a - NR2 * _b * _b) % PB
    _ni = pow(_nrm, PB - 2, PB)
    INV2[_e] = (_a * _ni) % PB + PB * ((-_b * _ni) % PB)
SUB2 = [[ADD2[x][NEG2[y]] for y in range(Q2)] for x in range(Q2)]
for _e in range(1, Q2):
    assert MUL2[_e][INV2[_e]] == 1

D2 = list(range(1, 17))   # F_17^* inside F_289 (b = 0)
POW2 = [[1] * (OM2 + W2 + 1) for _ in range(Q2)]
for _x in range(Q2):
    for _t in range(1, OM2 + W2 + 1):
        POW2[_x][_t] = MUL2[POW2[_x][_t - 1]][_x]


def pnorm2(f):
    f = list(f)
    while f and f[-1] == 0:
        f.pop()
    return f


def padd2(f, g):
    L = max(len(f), len(g))
    return pnorm2([ADD2[f[i] if i < len(f) else 0][g[i] if i < len(g) else 0]
                   for i in range(L)])


def psub2(f, g):
    L = max(len(f), len(g))
    return pnorm2([SUB2[f[i] if i < len(f) else 0][g[i] if i < len(g) else 0]
                   for i in range(L)])


def pscale2(f, c):
    return pnorm2([MUL2[c][a] for a in f])


def pshift2(f, k):
    return ([0] * k + list(f)) if f else []


def pmul2(f, g):
    if not f or not g:
        return []
    out = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        if a:
            ra = MUL2[a]
            for j, b in enumerate(g):
                if b:
                    out[i + j] = ADD2[out[i + j]][ra[b]]
    return pnorm2(out)


def pdivmod2(f, g):
    assert g
    f = list(f)
    q = [0] * max(0, len(f) - len(g) + 1)
    ginv = INV2[g[-1]]
    while len(f) >= len(g) and pnorm2(f):
        f = pnorm2(f)
        if len(f) < len(g):
            break
        c = MUL2[f[-1]][ginv]
        d = len(f) - len(g)
        q[d] = c
        for i, b in enumerate(g):
            f[d + i] = SUB2[f[d + i]][MUL2[c][b]]
        f = pnorm2(f)
    return pnorm2(q), pnorm2(f)


def pgcd2(f, g):
    while g:
        f, g = g, pdivmod2(f, g)[1]
    return f


def peval2(f, x):
    r = 0
    for a in reversed(f):
        r = ADD2[MUL2[r][x]][a]
    return r


LAMBDA2 = [1]
for _x in D2:
    LAMBDA2 = pmul2(LAMBDA2, [NEG2[_x], 1])
assert LAMBDA2 == [NEG2[1]] + [0] * (N2 - 1) + [1]  # X^16 - 1


def interpolate_full2(vals):
    out = []
    for i, xi in enumerate(D2):
        num, den = [1], 1
        for j, xj in enumerate(D2):
            if i == j:
                continue
            num = pmul2(num, [NEG2[xj], 1])
            den = MUL2[den][SUB2[xi][xj]]
        out = padd2(out, pscale2(num, MUL2[vals[i]][INV2[den]]))
    return out


def wdeg_pivot2(row):
    Wp, Np = row
    e1 = (len(Wp) - 1) if Wp else -10 ** 9
    e2 = (len(Np) - 1 - SHIFT2) if Np else -10 ** 9
    return (max(e1, e2), 1 if e2 >= e1 else 0)


def popov_d1_2(U):
    rows = [([1], interpolate_full2(U)), ([], LAMBDA2[:])]
    for _ in range(10000):
        (wd0, pv0), (wd1, pv1) = wdeg_pivot2(rows[0]), wdeg_pivot2(rows[1])
        if pv0 != pv1:
            break
        i, j = (0, 1) if wd0 <= wd1 else (1, 0)
        ri, rj = rows[i], rows[j]
        wi, wj = (wd0, wd1) if i == 0 else (wd1, wd0)
        piv = pv0
        c = MUL2[rj[piv][-1]][INV2[ri[piv][-1]]]
        delta = wj - wi
        rows[j] = (psub2(rj[0], pshift2(pscale2(ri[0], c), delta)),
                   psub2(rj[1], pshift2(pscale2(ri[1], c), delta)))
    else:
        raise AssertionError("popov2 did not terminate")
    rows.sort(key=lambda r: wdeg_pivot2(r)[0])
    g1, g2 = rows
    d1, d2 = wdeg_pivot2(g1)[0], wdeg_pivot2(g2)[0]
    for (Wp, Np) in (g1, g2):
        for idx, x in enumerate(D2):
            assert MUL2[peval2(Wp, x)][U[idx]] == peval2(Np, x)
    det = psub2(pmul2(g1[0], g2[1]), pmul2(g1[1], g2[0]))
    qd, rd = pdivmod2(det, LAMBDA2)
    assert rd == [] and len(qd) == 1
    assert len(pgcd2(g1[0], g2[0])) == 1
    assert d1 + d2 == N2 - K2 + 1
    assert wdeg_pivot2(g1)[1] != wdeg_pivot2(g2)[1]
    return d1


def enumerate_complements2():
    out = []

    def rec(start, depth, poly):
        if depth == OM2:
            out.append(tuple(poly))
            return
        need = OM2 - depth
        for idx in range(start, N2 - need + 1):
            x = D2[idx]
            new = [0] * (depth + 2)
            mx = NEG2[x]
            for i2, a in enumerate(poly):
                if a:
                    new[i2] = ADD2[new[i2]][MUL2[a][mx]]
                    new[i2 + 1] = ADD2[new[i2 + 1]][a]
            rec(idx + 1, depth + 1, new)

    rec(0, 0, [1])
    assert len(out) == math.comb(N2, OM2)
    return out


LAMR2 = enumerate_complements2()


def functional_T2(word):
    return [_psum2(word, t) for t in range(OM2 + W2 + 1)]


def _psum2(word, t):
    s = 0
    for i in range(N2):
        s = ADD2[s][MUL2[word[i]][POW2[D2[i]][t]]]
    return s


def word_census2(word):
    """(raw hit count, {codeword_tuple: agr}) threshold M2, dimension K2."""
    T = functional_T2(word)
    found = {}
    nhits = 0
    for lam in LAMR2:
        ok = True
        for j in range(W2):
            s = 0
            for k2, l in enumerate(lam):
                if l:
                    s = ADD2[s][MUL2[l][T[j + 1 + k2]]]
            if s:
                ok = False
                break
        if not ok:
            continue
        nhits += 1
        Sidx = [i for i in range(N2) if peval2(lam, D2[i]) != 0]
        assert len(Sidx) == M2
        pts = [(D2[i], word[i]) for i in Sidx[:K2]]
        out = []
        for i, (xi, yi) in enumerate(pts):
            num, den = [1], 1
            for j, (xj, _) in enumerate(pts):
                if i == j:
                    continue
                num = pmul2(num, [NEG2[xj], 1])
                den = MUL2[den][SUB2[xi][xj]]
            out = padd2(out, pscale2(num, MUL2[yi][INV2[den]]))
        for i in Sidx[K2:]:
            assert peval2(out, D2[i]) == word[i]
        key = tuple(out[t] if t < len(out) else 0 for t in range(K2))
        if key not in found:
            found[key] = sum(1 for idx in range(N2)
                             if peval2(out, D2[idx]) == word[idx])
    return nhits, found


def rank_one_scan2(u, v):
    Tu = functional_T2(u)
    Tv = functional_T2(v)
    n_common = n_bz = n_r1 = n_r2 = 0
    mult: dict[int, int] = {}
    for lam in LAMR2:
        a = []
        b = []
        for j in range(W2):
            s = 0
            s2 = 0
            for k2, l in enumerate(lam):
                if l:
                    s = ADD2[s][MUL2[l][Tu[j + 1 + k2]]]
                    s2 = ADD2[s2][MUL2[l][Tv[j + 1 + k2]]]
            a.append(s)
            b.append(s2)
        if b == [0, 0, 0]:
            if a == [0, 0, 0]:
                n_common += 1
            else:
                n_bz += 1
            continue
        p01 = SUB2[MUL2[a[0]][b[1]]][MUL2[a[1]][b[0]]]
        p02 = SUB2[MUL2[a[0]][b[2]]][MUL2[a[2]][b[0]]]
        p12 = SUB2[MUL2[a[1]][b[2]]][MUL2[a[2]][b[1]]]
        if p01 == 0 and p02 == 0 and p12 == 0:
            r = next(i for i in range(3) if b[i])
            z = MUL2[NEG2[a[r]]][INV2[b[r]]]
            assert all(ADD2[a[i]][MUL2[z][b[i]]] == 0 for i in range(3))
            n_r1 += 1
            mult[z] = mult.get(z, 0) + 1
        else:
            n_r2 += 1
    assert n_common + n_bz + n_r1 + n_r2 == len(LAMR2)
    return n_r1, mult, n_common, n_bz, n_r2


def fibers2(msize, depth):
    """{prefix tuple (base-field ints): [subsets (index tuples)]} over
    msize-subsets of D2; prefix = ([X^{msize-h}]Lambda_M)_{h<=depth}."""
    import itertools
    fib: dict[tuple, list] = {}
    for T in itertools.combinations(range(N2), msize):
        xs = [D2[i] % PB for i in T]
        e = [1] + [0] * depth
        for x in xs:
            for h in range(depth, 0, -1):
                e[h] = (e[h] + x * e[h - 1]) % PB
        z = tuple((pow(-1, h, PB) * e[h]) % PB for h in range(1, depth + 1))
        fib.setdefault(z, []).append(T)
    return fib


def line_row2(label, u, v, e, z0, plant_extra):
    """scan + per-slope census over F_289; returns cert row."""
    n_r1, mult, n_common, n_bz, n_r2 = rank_one_scan2(u, v)
    slope_rows = []
    lineray = 0
    for z in sorted(mult, key=lambda t: (-mult[t], t)):
        Uz = [ADD2[u[i]][MUL2[z][v[i]]] for i in range(N2)]
        nh, cen = word_census2(Uz)
        assert nh == mult[z] + n_common
        expect = sum(math.comb(a, M2) for a in cen.values())
        assert nh == expect
        profile = sorted(cen.values(), reverse=True)
        slope_rows.append([z, mult[z], profile])
        lineray += len(cen)
    ceil_p = -(-math.comb(N2, M2) // PB ** W2)
    p_term = [math.comb(N2, M2), PB ** W2]
    q_term = [math.comb(N2, M2), Q2 ** (W2 - 1)]
    row = {
        "label": label, "e": e, "z0": z0, "u": u, "v": v,
        "counts": {"common": n_common, "beta_zero": n_bz,
                   "rank_one": n_r1, "rank_two": n_r2},
        "slopes_hit": len(mult), "slope_rows": slope_rows,
        "lineray_count": lineray,
        "corrected_p_term": p_term, "q_term": q_term,
        "recorded_ceil_p_term": ceil_p,
        "literal_holds_raw": holds(n_r1, [q_term]),
        "corrected_holds_raw": holds(n_r1, [p_term, q_term]),
        "recorded_dedup_holds": holds(lineray, [[ceil_p, 1], q_term]),
    }
    row.update(plant_extra)
    return row


def gate_c() -> dict[str, Any]:
    # p/q term separation (the point of the F_{p^2} gate)
    ceil_p = -(-math.comb(N2, M2) // PB ** W2)
    assert ceil_p == 3 and ceil_p > 1
    assert math.comb(N2, M2) < Q2 ** (W2 - 1), "q-term below 1"
    # interior profile range is the single value w'+2 = 5
    assert W2 + 2 == (N2 - K2 + 1) // 2 == 5

    # heaviest depth-w' fiber and the witness (depth w'-1) fiber
    fib3 = fibers2(M2, W2)
    best3 = max(len(v) for v in fib3.values())
    zstar = min(z for z, v in fib3.items() if len(v) == best3)
    assert best3 >= ceil_p
    fib2 = fibers2(M2, W2 - 1)
    wit = fib2[zstar[:W2 - 1]]
    wit_lams = [None] * len(wit)
    for i, T in enumerate(wit):
        f = [1]
        for idx in T:
            f = pmul2(f, [NEG2[D2[idx]], 1])
        wit_lams[i] = f
    # depth-w' fiber members sit inside the witness fiber
    wset = set(wit)
    assert all(tuple(T) in wset for T in fib3[zstar])

    # prefix word U_{z*} (coefficients in B)
    Pz = [0] * (M2 + 1)
    Pz[M2] = 1
    for h, zz in enumerate(zstar, 1):
        Pz[M2 - h] = zz
    Uw = [peval2(Pz, x) for x in D2]

    # fiber route at every alpha in F \ (D u B): slopes and collisions
    alphas = list(range(PB, Q2))
    ns_by_alpha = []
    first_coll = None
    coll_count = 0
    for a in alphas:
        Pa = peval2(Pz, a)
        seen = set()
        for lam in wit_lams:
            seen.add(SUB2[Pa][peval2(lam, a)])
        ns = len(seen)
        ns_by_alpha.append(ns)
        if ns < len(wit):
            coll_count += 1
            if first_coll is None:
                first_coll = a
    assert first_coll is not None, "no slope collision at any alpha"
    # collision witness at first_coll: two fiber members, same slope
    Pa = peval2(Pz, first_coll)
    by_slope: dict[int, list] = {}
    for T, lam in zip(wit, wit_lams):
        by_slope.setdefault(SUB2[Pa][peval2(lam, first_coll)],
                            []).append(list(T))
    coll_pair = None
    for z in sorted(by_slope):
        if len(by_slope[z]) >= 2:
            coll_pair = {"alpha": first_coll, "slope": z,
                         "T1": by_slope[z][0], "T2": by_slope[z][1]}
            break
    assert coll_pair is not None

    # scan gates at tested alphas
    tested = sorted(set([alphas[0], first_coll, alphas[-1]]))
    pole_rows = []
    for a in tested:
        fa = [MUL2[Uw[i]][INV2[SUB2[D2[i]][a]]] for i in range(N2)]
        ga = [MUL2[NEG2[1]][INV2[SUB2[D2[i]][a]]] for i in range(N2)]
        n_r1, mult, n_common, n_bz, n_r2 = rank_one_scan2(fa, ga)
        assert n_common == 0 and n_bz == 0
        assert n_r1 == len(wit), "R1 == witness (depth w'-1) fiber"
        # per-slope census: ray decomposition, agreements exactly m
        lineray = 0
        slope_rows = []
        for z in sorted(mult, key=lambda t: (-mult[t], t)):
            Uz = [ADD2[fa[i]][MUL2[z][ga[i]]] for i in range(N2)]
            nh, cen = word_census2(Uz)
            assert nh == mult[z]
            assert all(agr == M2 for agr in cen.values())
            assert len(cen) == mult[z]  # one support per ray (loss-2 = 0)
            lineray += len(cen)
            slope_rows.append([z, mult[z], sorted(cen.values(),
                                                  reverse=True)])
        assert lineray == n_r1 == len(wit)
        # fiber-route slope multiset == scan slope multiset
        Pa = peval2(Pz, a)
        fr = {}
        for lam in wit_lams:
            zz = SUB2[Pa][peval2(lam, a)]
            fr[zz] = fr.get(zz, 0) + 1
        assert fr == mult
        assert lineray >= best3 >= ceil_p  # part (c) floor at pair level
        pole_rows.append({
            "alpha": a, "r1": n_r1, "lineray": lineray,
            "n_slopes": len(mult), "slope_rows": slope_rows,
            "all_agr_exactly_m": True,
            "collision_here": len(mult) < lineray,
        })

    # planted near-codeword line, e = w'+2 (deterministic first-attempt
    # hygiene standing in for the deployed union-bound existence argument)
    e = W2 + 2
    assert 2 * e <= N2 - K2 + 1  # profile localization range (#518 lemma)
    attempt = 0
    while True:
        rng = random.Random(SEED + attempt)
        c0 = [rng.randrange(Q2) for _ in range(K2)]
        base = [peval2(pnorm2(c0), x) for x in D2]
        pos = sorted(rng.sample(range(N2), e))
        Up = base[:]
        for i in pos:
            Up[i] = ADD2[Up[i]][rng.randrange(1, Q2)]
        v = [rng.randrange(Q2) for _ in range(N2)]
        u = [SUB2[Up[i]][MUL2[Z0_2][v[i]]] for i in range(N2)]
        n_r1, mult, n_common, n_bz, n_r2 = rank_one_scan2(u, v)
        _, cenU = word_census2(Up)
        if n_common == 0 and set(mult) == {Z0_2} and len(cenU) == 1:
            break
        attempt += 1
        assert attempt < 1000
    planted = line_row2("planted_e5", u, v, e, Z0_2, {
        "codeword_coeffs": c0, "error_positions": pos, "attempt": attempt})
    d1p = popov_d1_2([ADD2[u[i]][MUL2[Z0_2][v[i]]] for i in range(N2)])
    assert d1p == e, "profile localization d1 = e"
    planted["planted"] = {
        "d1": d1p, "d1_equals_e": True,
        "mult_z0": planted["slope_rows"][0][1],
        "floor_C_n_minus_e_m": math.comb(N2 - e, M2),
    }
    assert planted["slope_rows"][0][0] == Z0_2
    assert planted["planted"]["mult_z0"] >= math.comb(N2 - e, M2)
    assert not planted["corrected_holds_raw"], "corrected raw model FAILS"
    assert not planted["literal_holds_raw"], "literal q-scale model FAILS"
    assert planted["recorded_dedup_holds"], "recorded dedup model HOLDS"
    assert planted["lineray_count"] <= ceil_p  # p-term alive and binding

    # random control line
    rngc = random.Random(SEED + 10 ** 6)
    uc = [rngc.randrange(Q2) for _ in range(N2)]
    vc = [rngc.randrange(Q2) for _ in range(N2)]
    control = line_row2("random_control", uc, vc, None, None, {})
    assert control["corrected_holds_raw"]
    assert control["literal_holds_raw"]
    assert control["recorded_dedup_holds"]

    return {
        "field": {"p": PB, "q": Q2, "tower": "F_289 = F_17[t]/(t^2-3)",
                  "encoding": "element a + b*t stored as integer a + 17*b",
                  "domain": D2, "n": N2, "K": K2, "m": M2, "w_prime": W2,
                  "omega": OM2, "interior_profiles": [W2 + 2]},
        "term_separation": {
            "ceil_p_term": ceil_p,
            "p_term": [math.comb(N2, M2), PB ** W2],
            "q_term": [math.comb(N2, M2), Q2 ** (W2 - 1)],
            "p_term_alive": True, "q_term_below_1": True,
        },
        "pole_line": {
            "z_star": list(zstar), "heaviest_depth_wprime_fiber": best3,
            "ceil_floor": ceil_p,
            "witness_fiber_depth": W2 - 1,
            "witness_fiber_size": len(wit),
            "witness_fiber_members": [list(T) for T in wit],
            "tested_alphas": tested,
            "rows": pole_rows,
            "n_slopes_min": min(ns_by_alpha),
            "n_slopes_max": max(ns_by_alpha),
            "collision_alphas": coll_count,
            "admissible_alphas": len(alphas),
            "first_collision_alpha": first_coll,
            "collision_witness": coll_pair,
        },
        "planted": planted,
        "control": control,
        "all_pass": True,
    }


# ======================================================================
# certificate
# ======================================================================
RECORDED_TARGET = {
    "per_line": (
        "For every primitive affine line (u,v) at normalized-band "
        "agreements (prob:capfr1-normalized-band; finite deployed form at "
        "the a_0+1 of cor:capg-adjacent-pairs), with E the residual finite "
        "slopes after the first-match paid branches of prob:saturated-bc's "
        "preamble (quotient, boundary-Q, common-support, tangent, "
        "extension, degree-drop, common-GCD), prove |LineRay_E(u,v;m)| <= "
        "e^{o(n)} max(1, ceil(C(n,m) p^-w'), C(n,m) q^-(w'-1)), the middle "
        "term achieved from below by the non-B-rational pole lines of "
        "prop:capg-census-floor(c)"),
    "per_word_interior": (
        "for every word U = u + zv at interior profile d1 in [w'+2, "
        "floor((n-K+1)/2)] (boundary d1 = w'+1 delegated to (Q), "
        "rem:capg-boundary-offbyone), with m' = K-1+d1: |Ray(U;m)| <= "
        "e^{o(n)} max(1, ceil(C(n,m') p^-(d1-1)), C(n,m) q^-(w'-1))"),
    "status": "OPEN",
    "q_terms_coincide": "C(n,omega) q^{1-w'} == C(n,m) q^{-(w'-1)} "
                        "(omega = n-m): one q-term suffices",
    "stated_on": "pair count |LineRay_E| (gf def:line-rays), NOT N_slopes "
                 "(the floor survives exactly on pairs; the slope count "
                 "carries the collision correction of "
                 "thm:capg-aperiodic-floor)",
    "witness_fiber_calibration": (
        "at census dimension K the exact pole-line witness set is the "
        "depth-(w'-1) fiber (rem:capg-witnessrel), so the pole-line "
        "|LineRay| sits at ceil(C(n,m) p^-(w'-1)), a factor <= p above "
        "the middle term -- absorbed by e^{o(n)} along fixed-rate rows "
        "(p^w' <= C(n,m) forces log2 p <= n/w'); the finite deployed "
        "middle term must be pinned at the witness-fiber scale"),
}

SUBSUMPTION_GRADES = {
    "prob:capfp-R1": "SUBSUMED-INTO-DEDUP-TARGET (raw form refuted by "
                     "#679; identity #R1 = with-multiplicity LineRay "
                     "census makes the recorded target its unique repair; "
                     "unconditional strata transfer verbatim)",
    "prob:capfr1-rank-one-census": "SUBSUMED-INTO-DEDUP-TARGET (resolves "
                                   "#679's REFUTED-WITH-AMBIGUITY-FOOTNOTE:"
                                   " any unprinted reading paying the "
                                   "plant must introduce a new cell, and "
                                   "that cell is ray-deduplication = this "
                                   "record)",
    "prob:capg-split-pencil-B": "SUBSUMED-INTO-DEDUP-TARGET (raw form "
                                "refuted by #518; dedup quotient is "
                                "|Ray(U;m)| by #666; base-field term "
                                "stripped to ceil(C(n,m') p^-(d1-1)))",
    "prob:capfr1-split-pencil": "SUBSUMED-INTO-DEDUP-TARGET (conceded "
                                "superseded upstream; tier-(4) chain "
                                "position taken over by the recorded "
                                "target; L8100 dichotomy preserved at ray "
                                "level)",
    "prob:capg-active-BC": "SUBSUMED by inheritance (asks to prove "
                           "prob:capg-split-pencil-B's census; the "
                           "re-recording makes "
                           "prop:capg-final-active-package's BC input "
                           "satisfiable again)",
    "siblings": "prob:capfp-split, prob:capfp-balanced, "
                "prob:capfr1-balanced-core subsumed identically via "
                "#666's profile-independence",
}


def build_certificate(root: Path) -> dict[str, Any]:
    pins = scan_pins(root)
    a = gate_a(root)
    b_toy = gate_b_toy()
    b_dep = gate_b_deployed(a["r1_deployed_corrected_middle_ceil"])
    c = gate_c()

    cert: dict[str, Any] = {
        "status": STATUS,
        "object": (
            "re-recording of the tier-(4) 'Main aperiodic effort' census "
            "lemma on the slope/ray-deduplicated |LineRay_E| pair count, "
            "feeding prob:saturated-bc alternative (b); part-(b) model "
            "correction (strip C(m',m)); subsumption grades for five "
            "problems; NOT a counterexample packet"),
        "base_sha": "ea4eb0784417ca5ab503a3c31a7eef6464ad100a",
        "evidence_type": "STATEMENT_RERECORDING_WITH_FLOOR_AND_IDENTITY_GATES",
        "seed": SEED,
        "statement_pins": pins,
        "recorded_target": RECORDED_TARGET,
        "model_correction": {
            "what": ("part (b) of prop:capg-census-floor: the dedup "
                     "interior floor strips the per-witness saturation "
                     "factor C(m',m) from M_B(d1) = C(m',m) * "
                     "ceil(C(n,m') p^-(d1-1)) -- the factor is loss-2 "
                     "mass by the proof's own construction (cap25 "
                     "L9794-9801); the stripped floor is the fiber "
                     "cardinality ceil(C(n,m') p^-(d1-1))"),
            "boundary_reproduces_part_a": "at d1 = w'+1 (m' = m) the "
                                          "stripped form is "
                                          "ceil(C(n,m) p^-w') verbatim",
            "monotone": "strictly decreasing in d1 for m' > n/2 "
                        "(deployed m/n ~ 0.532), so the per-line middle "
                        "term dominates the interior terms",
        },
        "subsumption_grades": SUBSUMPTION_GRADES,
        "withheld_item_discharge": {
            "withheld": ("split_pencil_ray_collapse.md L158-160: corrected "
                         "model may inherit the raw-count trap -- withheld "
                         "pending verification"),
            "discharged_by": ("#679 (r1_rawcount_refutation.json): refutes "
                              "prob:capfp-R1 including the corrected "
                              "mutatis-mutandis model; "
                              "margins_bits.planted_R1_vs_corrected = "
                              "2015046; corrected_middle_ceil = "
                              "65065153468"),
            "residual": ("none beyond citation wiring; the p = q toy gap "
                         "flagged by #679's own cert is closed by gate_c"),
        },
        "gate_a_oracle_replay": a,
        "gate_b_toy_f73": b_toy,
        "gate_b_deployed": b_dep,
        "gate_c_fp2_toy": c,
        "honest_headline": (
            "Statement packet: the tier-(4) census lemma is re-recorded "
            "once, per line, on the deduplicated |LineRay_E| pair count "
            "with model max(1, ceil(C(n,m)p^-w'), C(n,m)q^-(w'-1)); the "
            "recorded target is OPEN and nothing here bounds it.  Proved "
            "free parts: parts (a)/(c) of prop:capg-census-floor survive "
            "verbatim at pair level; the compile-through N_slopes <= "
            "|LineRay_E| feeds the closing corollaries unchanged; the "
            "#666-withheld inheritance item is discharged by #679.  One "
            "real correction: part (b)'s interior floor strips C(m',m).  "
            "New F_{17^2} toy separates the p- and q-terms: planted line "
            "raw #R1 = 55 FAILS the corrected raw model (2.33) while "
            "|LineRay| = 1 HOLDS the recorded model (<= 3) with the "
            "p-term alive; pole line: |LineRay| == witness fiber == 40 "
            ">= depth-w' floor 5 >= ceil 3, slope collision witnessed "
            "(39 < 40)."),
        "summary": {
            "verdict": "NO ISSUE",
            "headline": (
                "re-recording packet: PROVED free parts + part-(b) model "
                "correction + OPEN recorded target; gates A (oracle "
                "replay 11/11 and 4/4), B (F_73 boundary/interior "
                "survival + deployed recompute, all eight paper prints "
                "reproduced), C (F_{17^2}: raw FAILS / dedup HOLDS with "
                "p-term alive; pair-level floor verbatim; slope collision "
                "witnessed), D (16 pins) all pass"),
        },
        "claim_boundaries": {
            "asserts": [
                "the recorded dedup target (OPEN) is stated once, per "
                "line, on |LineRay_E|, feeding prob:saturated-bc "
                "alternative (b); not a new independent problem",
                "part (b) of prop:capg-census-floor requires the C(m',m) "
                "stripping under the dedup reading (model correction, "
                "with exact deployed recompute)",
                "parts (a)/(c) survive verbatim at (slope, codeword)-pair "
                "level; the (c) floor's correct free justification is "
                "ray-distinctness, not distinct slopes",
                "the pole-line witness set at census dimension K is the "
                "depth-(w'-1) fiber (witness-fiber calibration), pinned "
                "at the F_{17^2} toy: |LineRay| == 40 == |Fib_{w'-1}| vs "
                "depth-w' floor 5 and ceil term 3",
                "compile-through: any bound on the recorded target is a "
                "per-line MCA-bad slope bound feeding "
                "cor:capfr1-Q-R1-closing / prop:capfp-closing unchanged",
                "five subsumption grades + #666-withheld-item discharge",
            ],
            "does_not_assert": [
                "any upper bound on |LineRay_E| or |Ray(U;m)| beyond the "
                "floors already proved upstream (the recorded target is "
                "OPEN)",
                "any refutation (verdict NO ISSUE; this packet refutes "
                "nothing)",
                "any chart verification for prob:saturated-bc, or "
                "progress on R_post <= 16 n^3",
                "anything about the aperiodic core (Q), "
                "prob:capg-active-Q, or prob:capg-active-shiftpairs",
                "any edit to upstream .tex (grades recorded in "
                "experimental/ only)",
            ],
            "is_counterexample": False,
            "is_novel_not_confirming_a_proven_theorem": False,
            "is_full_canonical_statement_not_proxy_or_toy_row": False,
            "independent_recheck_confirms": True,
            "is_degenerate_by_construction": False,
            "is_tautology_under_preconditions": False,
            "resolves_or_advances_prob_band": False,
        },
        "nonclaims": [
            "recorded target is OPEN; no bound proved on |LineRay_E| "
            "beyond the floors",
            "no refutation of anything; statement packet, verdict NO ISSUE",
            "no chart verification for prob:saturated-bc alternatives",
            "aperiodic core untouched",
            "toy gates pin mechanisms and identities, not asymptotics",
        ],
        "caveats": [
            "The F_{17^2} planted-line hygiene (every other slope "
            "census-empty) is realized by a deterministic first-attempt "
            "search standing in for the deployed union-bound existence "
            "argument; the attempt index is frozen in the certificate.",
            "The paper's printed interior M_B values at d1 = w'+3, w'+4 "
            "correspond to the un-ceiled product; both forms are "
            "recomputed and displayed.",
            "log2 values in *_display fields are display-grade strings; "
            "every verdict field is an exact integer or boolean.",
        ],
        "falsifiable": True,
        "falsifiability": (
            "The gate fails if: any oracle certificate self-hash or "
            "replayed identity drifts; any F_73 fiber size, census count, "
            "ray profile, d1, or stripping identity changes; any deployed "
            "bit display or cross-link value changes; any F_{17^2} scan "
            "count, fiber size, slope multiset, collision witness, or "
            "model verdict changes; or any pinned statement moves or its "
            "line hash drifts."),
        "regeneration": ("python experimental/scripts/"
                         "verify_lineray_census_rerecording.py "
                         "--emit-defaults"),
    }
    cert["payload_sha256"] = payload_hash(cert)
    return cert


def write_cert(root: Path, cert: dict[str, Any]) -> Path:
    path = root / CERT_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")
    return path


def print_summary(cert: dict[str, Any]) -> None:
    a = cert["gate_a_oracle_replay"]
    print("Gate A: oracle replay OK (#666 rows=%d, #679 rows=%d)"
          % (a["oracle_spc"]["rows_replayed"],
             a["oracle_r1"]["rows_replayed"]))
    for r in a["r1_rows"]:
        print("  #679 %-12s #R1=%-6d lineray=%-4d slopes=%-3d loss2=%-6d "
              "recorded_dedup=HOLDS"
              % (r["label"], r["rank_one"], r["lineray"], r["n_slopes"],
                 r["loss2"]))
    print("Gate B (F_73):")
    for r in cert["gate_b_toy_f73"]["rows"]:
        extra = ("" if r["label"].startswith("boundary")
                 else " rays@m'=%d extras=%d" % (r["rays_at_level"],
                                                 r["extras"]))
        print("  %-14s d1=%d fiber=%-3d ceil=%-2d RAW=%-4d RAYS=%-3d%s"
              % (r["label"], r["d1"], r["fiber"], r["ceil_floor"],
                 r["raw"], r["rays"], extra))
    dep = cert["gate_b_deployed"]
    for name in ("KB", "M31"):
        row = dep["rows"][name]
        print("  deployed %-4s boundary 2^%s (paper %s); stripped interior: %s"
              % (name, row["boundary_floor_log2_display"],
                 row["boundary_paper_prints"],
                 ", ".join(str(i["stripped_dedup_floor"])
                           for i in row["interior"])))
    print("  cross-links: #679 middle ceil = %d; budget-fit B_B displays %s"
          % (dep["crosslink_679_corrected_middle_ceil"],
             dep["crosslink_budget_fit_BB_displays"]))
    c = cert["gate_c_fp2_toy"]
    pl = c["pole_line"]
    print("Gate C (F_17^2): fiber(w')=%d >= ceil=%d; witness fiber=%d"
          % (pl["heaviest_depth_wprime_fiber"], pl["ceil_floor"],
             pl["witness_fiber_size"]))
    for r in pl["rows"]:
        print("  pole alpha=%-3d #R1=%-3d lineray=%-3d N_slopes=%-3d "
              "agr==m %s collision=%s"
              % (r["alpha"], r["r1"], r["lineray"], r["n_slopes"],
                 r["all_agr_exactly_m"], r["collision_here"]))
    print("  collisions at %d/%d alphas (min N_slopes=%d); witness: "
          "alpha=%d slope=%d"
          % (pl["collision_alphas"], pl["admissible_alphas"],
             pl["n_slopes_min"], pl["collision_witness"]["alpha"],
             pl["collision_witness"]["slope"]))
    p = c["planted"]
    print("  planted e=%d attempt=%d: #R1=%d (floor %d) corrected_raw=%s "
          "literal_raw=%s | lineray=%d recorded_dedup=%s (ceil p-term=%d, "
          "q-term=%d/%d)"
          % (p["e"], p["attempt"], p["counts"]["rank_one"],
             p["planted"]["floor_C_n_minus_e_m"],
             "HOLDS" if p["corrected_holds_raw"] else "FAILS",
             "HOLDS" if p["literal_holds_raw"] else "FAILS",
             p["lineray_count"],
             "HOLDS" if p["recorded_dedup_holds"] else "FAILS",
             p["recorded_ceil_p_term"], p["q_term"][0], p["q_term"][1]))
    ct = c["control"]
    print("  control: #R1=%d lineray=%d all models HOLD"
          % (ct["counts"]["rank_one"], ct["lineray_count"]))
    npins = sum(len(v) for v in cert["statement_pins"].values())
    print("Gate D: %d pins OK at expected lines" % npins)


def run_check(root: Path) -> int:
    fresh = build_certificate(root)
    stored = json.loads((root / CERT_REL).read_text(encoding="utf-8"))
    if stored.get("payload_sha256") != payload_hash(stored):
        print("RESULT: FAIL self-hash")
        return 1
    if fresh["payload_sha256"] != stored["payload_sha256"]:
        print("RESULT: FAIL rebuild drift")
        return 1
    if stored["summary"]["verdict"] != "NO ISSUE":
        print("RESULT: FAIL", stored["summary"]["verdict"])
        return 1
    print("RESULT: PASS")
    print("payload_sha256:", stored["payload_sha256"])
    print("verdict:", stored["summary"]["verdict"])
    print("status:", stored["status"])
    return 0


def main(argv: list[str] | None = None) -> int:
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
        print("verdict:", cert["summary"]["verdict"])
        print_summary(cert)
        return 0
    if args.check:
        return run_check(root)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
