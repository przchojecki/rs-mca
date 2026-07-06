#!/usr/bin/env python3
"""verify_l1_e3_dim_syz_crux.py

Zero-arg, stdlib-only, deterministic verifier for
`experimental/notes/l1/l1_e3_dim_syz_crux_refuted.md`, which shows the L1 E3
proof-program's named-open crux

    dim Syz <= K   (K = #{mu_k >= 3} >= 3)      <=>      E_3 <= ell - 2

(`experimental/l1_e3_obligation_v2.md`) is already DECIDED -- FALSE -- by
witnesses co-integrated on the same branch
(`experimental/notes/l1/l1_prime_ell_key_lemma_refuted.md`,
`l1_e3_law_refuted.md`): building the proof-program's own `Syz` module
verbatim on those witnesses gives `dim Syz > K` on all thirteen (margins
+1..+4), while the proof-program's own PROVED "upper half"
(`dim(sum V_k) <= ell-2`) and the sigma-calculus master identity
(`l1_sigma_calculus.md`) hold on every one of them.

Ground rule: self-contained. Does NOT import from, edit, or depend on any
other script's claims being true; every object below is reconstructed here
from its raw `gamma` alone by exact F_p linear algebra (a fresh port of
`laneF_compute.py`'s conventions, themselves pinned to the exact definitions
of `experimental/l1_e3_obligation_v2.md`).

Four gate classes; exit 0 iff ALL pass, nonzero on ANY failure:

  (i)   per-object recompute: spectrum, E_3, K_3 = #{mu_k>=3}, dim Syz (the
        proof-program's own mu_k>=3 convention), and
        margin = dim Syz - K_3 = E_3 - (ell-2), exactly, on the 13 witnesses
        PLUS the 2 E_3=ell-2 saturator controls (margin 0).
  (ii)  transport identity: dim(sum V_k) attained at ell-2 (recomputed, not
        assumed) and dim Syz - K_3 == E_3 - dim(sum V_k), on all 15.
  (iii) convention dictionary: recompute sigma (mu_k>=2 convention), K_2,
        dimU; check the master identity sigma == E_3 + K_2 - ell + dimU,
        and the K_3/K_2 translation (sigma - K_2) == (dim Syz - K_3) (the
        margin is convention-invariant), on all 15.
  (iv)  in-scope checks per object: ell odd prime, ell | p-1, Gamma
        constant-free (deg <= ell-1 by construction) and mixed (>=2 nonzero
        coefficients), K_3 >= 3.

Hidden self-test: python3 verify_l1_e3_dim_syz_crux.py --tamper-selftest
    flips one datum guarded by each gate and asserts that gate then FAILS
    (proves every gate has teeth). The shipped default is zero-arg.

All arithmetic exact over F_p, stdlib only. No network; no files read at
runtime (the companion certificate
`experimental/data/certificates/l1-e3-law/l1_dim_syz_crux_table.json` is a
ported human-readable copy of the same data, not a dependency of this
script). Runtime target < 30s (actual: well under 1s).
"""
import sys
import time

# ============================================================================
# exact F_p polynomial + linear-algebra arithmetic (fresh port of
# laneF_compute.py's conventions; self-contained, not an import)
# ============================================================================
def inv(a, p):
    return pow(a % p, p - 2, p)


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


def trim(c):
    out = list(c)
    while out and out[-1] == 0:
        out.pop()
    return out


def pmul(a, b, p):
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        ai %= p
        if ai:
            for j, bj in enumerate(b):
                out[i + j] = (out[i + j] + ai * bj) % p
    return trim(out)


def poly_from_roots(rs, p):
    out = [1]
    for r in rs:
        out = pmul(out, [(-r) % p, 1], p)
    return out


def poly_div_exact(num, den, p):
    """Exact quotient num/den over F_p; raises if the remainder is nonzero."""
    num = trim(list(num))
    den = trim(list(den))
    if not den:
        raise ZeroDivisionError
    if len(num) < len(den):
        if not num:
            return []
        raise ValueError("does not divide (deg num < deg den)")
    rem = num[:]
    dlead_inv = inv(den[-1], p)
    q = [0] * (len(rem) - len(den) + 1)
    for i in range(len(q) - 1, -1, -1):
        coeff = rem[i + len(den) - 1] * dlead_inv % p
        q[i] = coeff
        if coeff:
            for j, dj in enumerate(den):
                rem[i + j] = (rem[i + j] - coeff * dj) % p
    rem = trim(rem)
    if rem:
        raise ValueError("does not divide exactly, nonzero remainder %r" % (rem,))
    return q


def rank_Fp(rows, ncols, p):
    """Rank (mod p) of a matrix given as a list of row-lists (Gaussian elim)."""
    if not rows:
        return 0
    A = [[v % p for v in r] for r in rows]
    m = len(A)
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, m):
            if A[i][c] % p:
                piv = i
                break
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
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


# ============================================================================
# config reconstruction from a raw gamma (constant-free: gamma[r-1] = coeff
# of X^r, r=1..ell-1), exactly per experimental/l1_e3_obligation_v2.md
# ============================================================================
def eval_gamma(gamma, x, p):
    v = 0
    xr = 1
    for r in range(1, len(gamma) + 1):
        xr = xr * x % p
        v = (v + gamma[r - 1] * xr) % p
    return v


def build_fibers(gamma, p, ell):
    """Group F_p^* by x^ell; per coset, take the max level-set (mu >= 1).
    Returns only the mu>=2 fibers (mu=1 cosets carry no E_3/K contribution
    and are dropped, matching the spectrum convention), largest-first, each
    carrying its co-fiber locator h_k = (X^ell - w_k)/g_k."""
    cosets = {}
    for x in range(1, p):
        w = pow(x, ell, p)
        cosets.setdefault(w, []).append(x)
    fibers = []
    for w, xs in cosets.items():
        byval = {}
        for x in xs:
            byval.setdefault(eval_gamma(gamma, x, p), []).append(x)
        best_c = max(sorted(byval), key=lambda c: len(byval[c]))
        F = sorted(byval[best_c])
        if len(F) >= 2:
            g = poly_from_roots(F, p)
            xell_minus_w = [0] * ell + [1]
            xell_minus_w[0] = (-w) % p
            h = poly_div_exact(xell_minus_w, g, p)
            assert pmul(g, h, p) == trim(xell_minus_w), "g_k h_k != X^ell - w_k"
            fibers.append(dict(w=w, F=F, mu=len(F), h=h))
    fibers.sort(key=lambda f: -f["mu"])
    return fibers


def syz_and_vsum(fibers_sel, p, ell):
    """Columns: X^d h_k for d=0..mu_k-2, over the selected fiber subset.
    Rows: degrees 0..ell-2. dim(sum V_k) = rank; dim Syz = ncols - rank."""
    cols = []
    for f in fibers_sel:
        h = f["h"]
        for d in range(f["mu"] - 1):
            col = [0] * (ell - 1)
            for i, c in enumerate(h):
                if c % p:
                    col[i + d] = c % p
            cols.append(col)
    rk = rank_Fp(cols, ell - 1, p) if cols else 0
    return dict(ncols=len(cols), dimVsum=rk, dimSyz=len(cols) - rk)


def dimU(fibers_mu_ge_2, p, ell):
    """dim{A: deg<=ell-1, A constant on each max-fiber}, via ell minus the
    rank of the per-fiber coincidence rows (constraints A(x)=A(x0), x0 the
    fiber anchor), over every fiber with mu>=2."""
    rows = []
    for f in fibers_mu_ge_2:
        F = f["F"]
        x0 = F[0]
        pow0 = [pow(x0, e, p) for e in range(ell)]
        for x in F[1:]:
            rows.append([(pow(x, e, p) - pow0[e]) % p for e in range(ell)])
    rk = rank_Fp(rows, ell, p) if rows else 0
    return ell - rk


# ============================================================================
# the 13 witnesses (7 key_lemma_refuted Sec1 + 6 e3_law_refuted) + 2
# sigma_calculus saturator controls (E_3 = ell-2, dim Syz = K exactly).
# All gammas verbatim from the integrated notes (ported via laneF_compute.py
# / l1_e3_law_refutation.json); "expect" = laneF_output.json, independently
# recomputed here from the raw gamma alone, not trusted.
# ============================================================================
WITNESSES = [
    {"id": "KL_ell11_p67", "source": "key_lemma_refuted Sec1", "ell": 11, "p": 67,
     "gamma": [43, 44, 38, 44, 17, 18, 42, 44, 65, 1],
     "expect": {"spectrum": [8, 3, 3, 3, 3, 2], "E3": 10, "K3": 5, "dimSyz": 6, "margin": 1, "K2": 6, "sigma": 7}},
    {"id": "KL_ell11_p199", "source": "key_lemma_refuted Sec1", "ell": 11, "p": 199,
     "gamma": [21, 144, 71, 171, 42, 10, 12, 115, 173, 1],
     "expect": {"spectrum": [7, 4, 3, 3, 3], "E3": 10, "K3": 5, "dimSyz": 6, "margin": 1, "K2": 5, "sigma": 6}},
    {"id": "KL_ell13_p79", "source": "key_lemma_refuted Sec1", "ell": 13, "p": 79,
     "gamma": [23, 71, 3, 40, 40, 2, 46, 40, 67, 69, 71, 1],
     "expect": {"spectrum": [6, 6, 6, 2, 2], "E3": 12, "K3": 3, "dimSyz": 4, "margin": 1, "K2": 5, "sigma": 6}},
    {"id": "KL_ell13_p313", "source": "key_lemma_refuted Sec1", "ell": 13, "p": 313,
     "gamma": [185, 42, 295, 307, 71, 257, 218, 32, 90, 290, 279, 1],
     "expect": {"spectrum": [8, 5, 3, 3, 3, 2, 2, 2, 2, 2], "E3": 12, "K3": 5, "dimSyz": 6, "margin": 1, "K2": 10, "sigma": 11}},
    {"id": "KL_ell17_p103", "source": "key_lemma_refuted Sec1", "ell": 17, "p": 103,
     "gamma": [27, 7, 1, 74, 35, 11, 86, 96, 66, 44, 7, 96, 5, 48, 72, 1],
     "expect": {"spectrum": [10, 7, 3, 3, 3, 2], "E3": 16, "K3": 5, "dimSyz": 6, "margin": 1, "K2": 6, "sigma": 7}},
    {"id": "KL_ell19_p191", "source": "key_lemma_refuted Sec1", "ell": 19, "p": 191,
     "gamma": [16, 44, 177, 106, 79, 157, 14, 155, 11, 181, 151, 28, 126, 22, 142, 23, 1, 1],
     "expect": {"spectrum": [11, 8, 4, 3, 2, 2], "E3": 18, "K3": 4, "dimSyz": 5, "margin": 1, "K2": 6, "sigma": 7}},
    {"id": "KL_ell23_p139", "source": "key_lemma_refuted Sec1", "ell": 23, "p": 139,
     "gamma": [60, 80, 118, 60, 48, 137, 123, 101, 89, 94, 15, 23, 21, 88, 134, 5, 48, 8, 124, 42, 77, 1],
     "expect": {"spectrum": [13, 10, 4, 3, 3, 2], "E3": 23, "K3": 5, "dimSyz": 7, "margin": 2, "K2": 6, "sigma": 8}},
    {"id": "LAW_W1", "source": "e3_law_refuted W1", "ell": 29, "p": 233,
     "gamma": [126, 24, 50, 214, 172, 207, 131, 212, 64, 48, 179, 143, 189, 59,
               86, 107, 196, 67, 125, 47, 63, 162, 110, 189, 69, 218, 156, 1],
     "expect": {"spectrum": [15, 14, 4, 3, 3, 3, 2, 2], "E3": 30, "K3": 6, "dimSyz": 9, "margin": 3, "K2": 8, "sigma": 11}},
    {"id": "LAW_W2", "source": "e3_law_refuted W2", "ell": 23, "p": 139,
     "gamma": [91, 120, 12, 78, 12, 136, 48, 11, 118, 111, 69, 66, 43, 110, 6,
               14, 54, 38, 104, 2, 76, 1],
     "expect": {"spectrum": [14, 9, 4, 4, 3, 2], "E3": 24, "K3": 5, "dimSyz": 8, "margin": 3, "K2": 6, "sigma": 9}},
    {"id": "LAW_W3", "source": "e3_law_refuted W3", "ell": 17, "p": 137,
     "gamma": [95, 83, 94, 43, 16, 101, 72, 52, 93, 129, 47, 76, 80, 45, 64, 1],
     "expect": {"spectrum": [14, 3, 3, 3, 3, 3, 3, 3], "E3": 19, "K3": 8, "dimSyz": 12, "margin": 4, "K2": 8, "sigma": 12}},
    {"id": "LAW_EXTRA1", "source": "e3_law_refuted EXTRA1", "ell": 29, "p": 233,
     "gamma": [17, 195, 160, 138, 183, 48, 208, 127, 215, 127, 165, 216, 5, 154,
               15, 168, 221, 41, 15, 96, 205, 78, 67, 200, 8, 208, 182, 1],
     "expect": {"spectrum": [20, 9, 4, 3, 3, 3, 2, 2], "E3": 30, "K3": 6, "dimSyz": 9, "margin": 3, "K2": 8, "sigma": 11}},
    {"id": "LAW_EXTRA2", "source": "e3_law_refuted EXTRA2", "ell": 29, "p": 233,
     "gamma": [83, 0, 6, 232, 143, 192, 212, 48, 86, 182, 127, 17, 104, 134,
               194, 213, 17, 205, 118, 19, 45, 203, 39, 182, 145, 212, 102, 1],
     "expect": {"spectrum": [16, 13, 4, 3, 3, 3, 2, 2], "E3": 30, "K3": 6, "dimSyz": 9, "margin": 3, "K2": 8, "sigma": 11}},
    {"id": "LAW_EXTRA3", "source": "e3_law_refuted EXTRA3", "ell": 17, "p": 103,
     "gamma": [1, 30, 67, 2, 86, 41, 28, 85, 62, 87, 80, 84, 36, 89, 76, 1],
     "expect": {"spectrum": [11, 5, 5, 4, 3, 2], "E3": 18, "K3": 5, "dimSyz": 8, "margin": 3, "K2": 6, "sigma": 9}},
]

CONTROLS = [
    {"id": "CTRL_ell11_p331", "source": "sigma_calculus witness (E3=ell-2 saturator)", "ell": 11, "p": 331,
     "gamma": [97, 29, 97, 239, 171, 92, 143, 155, 270, 1],
     "expect": {"spectrum": [5, 5, 4, 3, 2, 2, 2], "E3": 9, "K3": 4, "dimSyz": 4, "margin": 0, "K2": 7, "sigma": 7}},
    {"id": "CTRL_ell23_p139_D3", "source": "sigma_calculus D3 witness (E3=ell-2 saturator)", "ell": 23, "p": 139,
     "gamma": [12, 79, 132, 135, 100, 118, 97, 22, 50, 20, 86, 134, 91, 89, 92, 110, 11, 56, 39, 17, 0, 1],
     "expect": {"spectrum": [8, 8, 6, 4, 4, 3], "E3": 21, "K3": 6, "dimSyz": 6, "margin": 0, "K2": 6, "sigma": 6}},
]

ALL_OBJECTS = WITNESSES + CONTROLS


def make_fibers(obj, tamper_gamma=False):
    gamma = list(obj["gamma"])
    if tamper_gamma:
        gamma[0] = (gamma[0] + 1) % obj["p"]
    return build_fibers(gamma, obj["p"], obj["ell"])


# ============================================================================
# GATES (each returns (ok: bool, summary: str))
# ============================================================================
def gate_i_margin(tamper=False):
    ok = True
    lines = []
    for oi, obj in enumerate(ALL_OBJECTS):
        fibers = make_fibers(obj, tamper_gamma=(tamper and oi == 0))
        exp = obj["expect"]
        spectrum = [f["mu"] for f in fibers]
        E3 = sum(m - 2 for m in spectrum if m >= 3)
        mu3 = [f for f in fibers if f["mu"] >= 3]
        K3 = len(mu3)
        r3 = syz_and_vsum(mu3, obj["p"], obj["ell"])
        dimSyz = r3["dimSyz"]
        margin = dimSyz - K3
        good = (spectrum == exp["spectrum"] and E3 == exp["E3"] and K3 == exp["K3"]
                and dimSyz == exp["dimSyz"] and margin == exp["margin"]
                and margin == E3 - (obj["ell"] - 2))
        ok = ok and good
        lines.append("%s: spectrum=%s E3=%d K3=%d dimSyz=%d margin=%+d(exp %+d):%s"
                      % (obj["id"], spectrum, E3, K3, dimSyz, margin, exp["margin"], good))
    return ok, " | ".join(lines)


def gate_ii_transport(tamper=False):
    ok = True
    lines = []
    for oi, obj in enumerate(ALL_OBJECTS):
        fibers = make_fibers(obj)
        mu3 = [f for f in fibers if f["mu"] >= 3]
        K3 = len(mu3)
        E3 = sum(f["mu"] - 2 for f in fibers if f["mu"] >= 3)
        r3 = syz_and_vsum(mu3, obj["p"], obj["ell"])
        dimVsum = r3["dimVsum"] + (1 if (tamper and oi == 0) else 0)
        attained = (dimVsum == obj["ell"] - 2)
        transport = (r3["dimSyz"] - K3 == E3 - dimVsum)
        good = attained and transport
        ok = ok and good
        lines.append("%s: dim(sumVk)=%d(ell-2=%d attained=%s) dimSyz-K3=%d E3-dimVsum=%d transport:%s"
                      % (obj["id"], dimVsum, obj["ell"] - 2, attained, r3["dimSyz"] - K3, E3 - dimVsum, transport))
    return ok, " | ".join(lines)


def gate_iii_dictionary(tamper=False):
    ok = True
    lines = []
    for oi, obj in enumerate(ALL_OBJECTS):
        fibers = make_fibers(obj)
        mu2 = [f for f in fibers if f["mu"] >= 2]
        mu3 = [f for f in fibers if f["mu"] >= 3]
        K2, K3 = len(mu2), len(mu3)
        E3 = sum(f["mu"] - 2 for f in fibers if f["mu"] >= 3)
        r2 = syz_and_vsum(mu2, obj["p"], obj["ell"])
        r3 = syz_and_vsum(mu3, obj["p"], obj["ell"])
        sigma = r2["dimSyz"] + (1 if (tamper and oi == 0) else 0)
        dU = dimU(mu2, obj["p"], obj["ell"])
        exp = obj["expect"]
        sigma_ok = (sigma == exp["sigma"])
        k2_ok = (K2 == exp["K2"])
        dimU_ok = (dU == 2)
        master = (sigma == E3 + K2 - obj["ell"] + dU)
        translation = ((sigma - K2) == (r3["dimSyz"] - K3))
        good = sigma_ok and k2_ok and dimU_ok and master and translation
        ok = ok and good
        lines.append("%s: sigma=%d(exp %d) K2=%d(exp %d) dimU=%d master(sigma==E3+K2-ell+dimU):%s translation(sigma-K2==dimSyz-K3):%s"
                      % (obj["id"], sigma, exp["sigma"], K2, exp["K2"], dU, master, translation))
    return ok, " | ".join(lines)


def gate_iv_in_scope(tamper=False):
    ok = True
    lines = []
    for oi, obj in enumerate(ALL_OBJECTS):
        ell, p, gamma = obj["ell"], obj["p"], obj["gamma"]
        ell_prime = is_prime(ell)
        ell_odd = (ell % 2 == 0) if (tamper and oi == 0) else (ell % 2 == 1)
        ell_dvd = ((p - 1) % ell == 0)
        deg_ok = (len(gamma) == ell - 1)  # constant-free, deg <= ell-1 by construction
        mixed_ok = sum(1 for c in gamma if c % p) >= 2
        fibers = make_fibers(obj)
        K3 = sum(1 for f in fibers if f["mu"] >= 3)
        k3_ok = (K3 >= 3)
        good = ell_prime and ell_odd and ell_dvd and deg_ok and mixed_ok and k3_ok
        ok = ok and good
        lines.append("%s: ell_prime:%s ell_odd:%s ell|p-1:%s deg<=ell-1:%s mixed:%s K3=%d>=3:%s"
                      % (obj["id"], ell_prime, ell_odd, ell_dvd, deg_ok, mixed_ok, K3, k3_ok))
    return ok, " | ".join(lines)


GATES = [
    ("(i)   per-object margin recompute           ", gate_i_margin),
    ("(ii)  transport identity (dim(sumVk)=ell-2)  ", gate_ii_transport),
    ("(iii) convention dictionary + master identity", gate_iii_dictionary),
    ("(iv)  in-scope checks                        ", gate_iv_in_scope),
]


def main():
    assert len(WITNESSES) == 13, "expected 13 witnesses"
    assert len(CONTROLS) == 2, "expected 2 controls"
    t0 = time.time()
    selftest = "--tamper-selftest" in sys.argv
    print("=" * 96)
    if selftest:
        print(" TAMPER SELF-TEST: each gate must FAIL when its guarded datum/claim is corrupted")
    else:
        print(" verify_l1_e3_dim_syz_crux  (zero-arg)   dim Syz<=K (K>=3) REFUTED on 13 co-integrated witnesses")
        print(" (experimental/notes/l1/l1_e3_dim_syz_crux_refuted.md)")
    print("=" * 96)
    all_good = True
    for name, fn in GATES:
        if selftest:
            ok, summ = fn(tamper=True)
            caught = not ok
            all_good = all_good and caught
            print("  %s  TAMPER %s" % (name, "CAUGHT " if caught else "MISSED!"))
            print("        %s" % summ)
        else:
            ok, summ = fn(tamper=False)
            all_good = all_good and ok
            print("  %s  %s" % (name, "PASS" if ok else "FAIL"))
            print("        %s" % summ)
    print("=" * 96)
    if selftest:
        print(" SELF-TEST RESULT: %s   (%.1fs)"
              % ("all tampers CAUGHT" if all_good else "A TAMPER WAS MISSED", time.time() - t0))
    else:
        print(" RESULT: %s   (%.1fs)" % ("ALL GATES PASS" if all_good else "FAILURE", time.time() - t0))
    sys.exit(0 if all_good else 1)


if __name__ == "__main__":
    main()
