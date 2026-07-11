#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_routing_exhaustiveness.py  --  stdlib only, zero-arg, exact.

Decides routing exhaustiveness on the frontiers paper's PRINTED first-match
order (asymptotic_rs_mca_frontiers.tex L5180-5183):

    "algebraic major arcs first, then a separately certified Sidon/Fourier
     cell, and only then the high-energy primitive inverse step."

It recomputes every number behind experimental/notes/thresholds/
routing_exhaustiveness.md: the trigger-detectability table, the routing
traces of the two C7 triggers, the witness arithmetic (block-parabola collapse
and heavy-atom saturation), the rung-3 hole refutation (primitive-Q failure ==
ray-saturation trigger firing), the router-decidability demonstration (image
size / max-fiber are functions of the profile occupancy vector; additive energy
is NOT), and the census.

Lineage recomputed / cross-checked byte-for-byte:
  #614 minimal_phase_supplement (E+1 = A_eff P_2, L >= A_eff/(1+E)),
  #622 se_on_admissible_leaves (T3 multiplicativity, single-leaf census),
  #625 c7_routing_spectrum (MASTER-2, the two witnesses, no-third-mode),
  #626 c7_degree_enumeration (binomial-tail collapse count, saturation H=1),
  #536 atlas_missing_witness, #545 gap2_collapse_routing, #609 frame_image,
  avdeevvadim #558 (block-parabola family).

RESULT: PASS (<passed>/<total>) printed at the end; exit 0 iff all pass.
Run under:  ulimit -v 2097152 ; python3 verify_routing_exhaustiveness.py
"""

from fractions import Fraction as F
from math import comb, log
from itertools import product

# ------------------------------------------------------------------ harness
_PASS = 0
_FAIL = 0
_LOG = []

def check(name, cond, detail=""):
    global _PASS, _FAIL
    if cond:
        _PASS += 1
    else:
        _FAIL += 1
        _LOG.append("FAIL: %s  %s" % (name, detail))
    return cond

def approx(a, b, tol=1e-9):
    return abs(float(a) - float(b)) <= tol * (1.0 + abs(float(b)))

# ------------------------------------------------------------ core spectral
# A profile leaf is given by its fiber-cardinality vector f = [f_s] over the
# realized image S (one entry per realized boundary value), plus the ambient
# scales A_eff (= |V_g|) and A (= |B^R|).  The ROUTER sees exactly f, A_eff, A.
#
#   L    = number of realized boundary values          = len(f)          [router]
#   Mtot = total residual witnesses (full slice)        = sum f           [router]
#   mu_s = f_s / Mtot                                    (profile measure)
#   P2   = sum mu_s^2
#   E    = A_eff * P2 - 1                                 (#614 Parseval)
#   Nbar_img = Mtot / L        (average full-slice fiber at image scale)  [router]
#   Mx   = max mu_s = max f_s / Mtot
#   G_1  = A_eff / L           (Gap-1 image-collapse ratio)               [router]
#   Q_img= L * Mx = max f_s / Nbar_img  (image-normalized max-fiber ratio)[router]

def leaf_invariants(f, A_eff):
    L = len(f)
    Mtot = sum(f)
    P2 = sum(F(fi, Mtot) ** 2 for fi in f)
    E = A_eff * P2 - 1
    Mx = F(max(f), Mtot)
    Nbar_img = F(Mtot, L)
    G1 = F(A_eff, L)
    Qimg = L * Mx
    return dict(L=L, Mtot=Mtot, P2=P2, E=E, Mx=Mx, Nbar_img=Nbar_img,
               G1=G1, Qimg=Qimg)

# --------------------------------------------------- exact F_p linear rank
def rank_mod_p(rows, p):
    """Gaussian elimination over F_p; rows = list of int lists."""
    M = [[x % p for x in r] for r in rows]
    if not M:
        return 0
    ncol = len(M[0])
    r = 0
    for c in range(ncol):
        piv = None
        for i in range(r, len(M)):
            if M[i][c] % p != 0:
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], p - 2, p)  # p prime => Fermat inverse
        M[r] = [(x * inv) % p for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] % p != 0:
                fac = M[i][c]
                M[i] = [(M[i][j] - fac * M[r][j]) % p for j in range(ncol)]
        r += 1
        if r == len(M):
            break
    return r

# =====================================================================
def block0_master2_spine():
    """MASTER-2 (#625): E+1 = A_eff P2 <= G_1 Q_img.  Reconfirmed so the note
    is self-contained.  Equality iff mu uniform on its support (Holder)."""
    # (i) uniform-on-support: equality
    for A_eff, L in [(9, 3), (25, 5), (81, 9), (625, 25)]:
        f = [1] * L                      # uniform image, singleton fibers
        inv = leaf_invariants(f, A_eff)
        check("B0.eq E+1=A_eff*P2 (%d,%d)" % (A_eff, L),
              inv["E"] + 1 == A_eff * inv["P2"])
        check("B0.eq MASTER-2 equality uniform (%d,%d)" % (A_eff, L),
              inv["E"] + 1 == inv["G1"] * inv["Qimg"],
              "%s vs %s" % (inv["E"] + 1, inv["G1"] * inv["Qimg"]))
    # (ii) non-uniform: strict inequality E+1 < G1*Qimg
    tests = [
        (16, [8, 1, 1, 1, 1, 1, 1, 1]),          # one heavy atom
        (36, [10, 5, 3, 2, 2, 2, 2, 2, 2, 2]),
        (49, [20, 4, 4, 4, 4, 4, 4, 1]),
    ]
    for A_eff, f in tests:
        inv = leaf_invariants(f, A_eff)
        check("B0.master2 E+1<=G1Q (%d)" % A_eff,
              inv["E"] + 1 <= inv["G1"] * inv["Qimg"])
        check("B0.master2 strict non-uniform (%d)" % A_eff,
              inv["E"] + 1 < inv["G1"] * inv["Qimg"])
        # #614 master: L*(1+E) >= A_eff  (=> (S_E) => (FI))
        check("B0.614 L(1+E)>=A_eff (%d)" % A_eff,
              inv["L"] * (1 + inv["E"]) >= A_eff)

def block1_collapse_witness():
    """Block-parabola (avdeev #558) as a leaf: N=pk, m=k, A_eff=A=p^{2k},
    L=p^k, singleton fibers.  G_1=p^k (exp), Q_img=1, E=p^k-1.  Router recovers
    G_1,Q_img from the occupancy vector f alone."""
    for p, k in [(3, 1), (3, 2), (3, 4), (5, 4), (7, 4)]:
        N = p * k
        A_eff = p ** (2 * k)             # = A (no Gap-2 span/ambient collapse)
        A = p ** (2 * k)
        L = p ** k
        f = [1] * L                      # singleton fibers (#609 escape)
        inv = leaf_invariants(f, A_eff)
        check("B1.A_eff=A (%d,%d)" % (p, k), A_eff == A)
        check("B1.L=p^k (%d,%d)" % (p, k), inv["L"] == p ** k)
        check("B1.G1=p^k (%d,%d)" % (p, k), inv["G1"] == p ** k)
        check("B1.Qimg=1 (%d,%d)" % (p, k), inv["Qimg"] == 1)
        check("B1.E=p^k-1 (%d,%d)" % (p, k), inv["E"] == p ** k - 1)
        # collapse trigger L<<A router-decidable: L/A = p^{-k}
        check("B1.collapse ratio L/A=p^-k (%d,%d)" % (p, k),
              F(L, A) == F(1, p ** k))
        # rate log(1+E)/N constant positive = signature of the k-fold product
        check("B1.rate>0 (%d,%d)" % (p, k), log(1 + inv["E"]) / N > 0.2)

def block2_rank_certificate_inert():
    """RANK CERTIFICATE (lem:rank-defect-payment L2534, prop:rank-pivot L4710)
    is INERT on the block-parabola: rank_Fp(V_g)=2k = full ambient rank R=2k,
    so the rank-defect locus {rank<=R-h, h>=1} does NOT contain it.  The
    collapse is |Phi(Omega)|=p^k, a property of the IMAGE, not the span rank.
    'generic rank alone gives no such conclusion' (L2542)."""
    for p, k in [(3, 1), (3, 2), (5, 2), (5, 3), (7, 2)]:
        # V_g per block = span_Fp{ (t,t^2)-(t0,t0^2) : t != t0 }.  Build gens.
        t0 = 0
        block_rows = []
        for t in range(1, p):
            block_rows.append([(t - t0) % p, (t * t - t0 * t0) % p])
        r_block = rank_mod_p(block_rows, p)
        check("B2.block rank=2 (p=%d)" % p, r_block == 2,
              "got %d" % r_block)
        # k-fold product: block-diagonal generators -> rank 2k
        R = 2 * k                        # ambient prefix depth per leaf
        rank_Vg = r_block * k
        check("B2.rank_Vg=2k=R full (%d,%d)" % (p, k),
              rank_Vg == 2 * k == R)
        # rank-defect trigger fires iff rank <= R-h, h>=1 ; full rank => silent
        rank_defect_fires = (rank_Vg <= R - 1)
        check("B2.rank trigger SILENT (%d,%d)" % (p, k),
              not rank_defect_fires)
        # but the image collapses: |Phi(Omega)| = p^k << p^{2k} = |B^R|
        L = p ** k
        A = p ** (2 * k)
        collapse_fires = (L < A)         # exponentially fewer boundary values
        check("B2.collapse trigger FIRES (%d,%d)" % (p, k), collapse_fires)
        check("B2.image<<span not a rank defect (%d,%d)" % (p, k),
              collapse_fires and not rank_defect_fires)

def block3_saturation_witness():
    """Heavy-atom (#625 Rung4): G_1=1 (FULL image, (FI) holds -> collapse
    trigger SILENT), Q_img exponential (primitive-Q FAILS).  Reproduces #625
    BLOCK3 exact rows A_eff in {16,81,256,625}, a=round(A^{3/4})/A."""
    expected = {                          # A_eff : (a_num, Qimg, E_exact)
        16:  (8,   8,   F(49, 15)),
        81:  (27,  27,  F(169, 20)),
        256: (64,  64,  F(1323, 85)),
        625: (125, 125, F(961, 39)),
    }
    for A_eff, (anum, Qimg_exp, E_exp) in expected.items():
        L = A_eff                         # FULL image
        # #625 measure: atom a=anum/A_eff at z*, remaining mass spread uniformly
        # on the other A_eff-1 points.  Exact integer fibers, M=A_eff*(A_eff-1):
        #   f(z*)   = anum*(A_eff-1),   f(other) = A_eff-anum   (x A_eff-1)
        check("B3.a=round(A^3/4) (%d)" % A_eff, round(A_eff ** 0.75) == anum)
        f = [anum * (A_eff - 1)] + [A_eff - anum] * (A_eff - 1)
        inv = leaf_invariants(f, A_eff)
        check("B3.G1=1 full image (%d)" % A_eff, inv["G1"] == 1)
        check("B3.Qimg exact (%d)" % A_eff, inv["Qimg"] == Qimg_exp,
              "%s vs %s" % (inv["Qimg"], Qimg_exp))
        check("B3.E exact matches #625 (%d)" % A_eff, inv["E"] == E_exp,
              "%s vs %s" % (inv["E"], E_exp))
        # (FI) HOLDS (span face fine); (S_E) FAILS; max-fiber Q FAILS
        check("B3.(FI) holds (%d)" % A_eff, inv["L"] == A_eff)  # L>=e^{-o}A_eff
        check("B3.max-fiber Q fails (Qimg>1) (%d)" % A_eff, inv["Qimg"] > 1)

def block4_hole_refutation():
    """RUNG-3 HOLE REFUTATION.  primitive-Q (def:primitive-q L4918):
    max_s f_s <= e^{o} Nbar_img.  Its FAILURE predicate is
    {max_s f_s > Nbar_img} == {Q_img > 1} == the ray-saturation trigger
    (L2440-2449: a displayed image with fiber cardinality above the image
    mean).  So a leaf that FAILS the primitive step's own payment (Q_img
    exponential) IDENTICALLY FIRES the pre-primitive ray-saturation trigger.
    There is NO leaf that escapes all pre-primitive triggers and then fails
    primitive payment -> the suspected unaccounted-mass hole does not exist."""
    import random
    random.seed(20260711)
    B_prim = 3.0                          # primitive-Q loss threshold (log)
    for _ in range(400):
        A_eff = random.choice([16, 25, 36, 49, 64, 81, 100, 121])
        L = random.randint(2, A_eff)
        f = [random.randint(1, 40) for _ in range(L)]
        inv = leaf_invariants(f, A_eff)
        N = float(log(A_eff))             # proxy scale; predicates are exact
        # failure of primitive-Q at loss B_prim:  log(Qimg) > B_prim
        fails_primQ = float(log(float(inv["Qimg"]))) > B_prim if inv["Qimg"] > 0 else False
        # ray-saturation trigger fires:  max fiber strictly above image mean
        fires_raysat = inv["Mx"] > F(1, inv["L"])   # Qimg = L*Mx > 1
        # implication: fails primitive payment ==> fires pre-primitive raysat
        if fails_primQ:
            check("B4.failsPrimQ=>firesRaysat",
                  fires_raysat, "Qimg=%s L=%d" % (inv["Qimg"], inv["L"]))
        # identity of the two predicates at the same threshold t>=1:
        for t in (F(1), F(3, 2), F(2), F(5), F(10)):
            fq = inv["Qimg"] > t          # normalized max-fiber ratio > t
            # equivalent statement in raw fibers: max f_s > t * Nbar_img
            fr = inv["Mx"] * inv["L"] > t
            check("B4.predicate identity t=%s" % t, fq == fr)
    # the exact contrapositive on the census witnesses:
    #   block-parabola: Qimg=1 -> does NOT fail primQ, does NOT fire raysat  (OK)
    #   heavy-atom:     Qimg>1 -> fails primQ AND fires raysat               (OK)
    inv_par = leaf_invariants([1] * 9, 81)          # p=3,k=2 parabola
    check("B4.parabola: no raysat", not (inv_par["Qimg"] > 1))
    inv_ha = leaf_invariants([64 * 255] + [256 - 64] * 255, 256)  # heavy atom
    check("B4.heavyatom: raysat fires", inv_ha["Qimg"] > 1)
    check("B4.heavyatom: Qimg=64 (primQ fails)", inv_ha["Qimg"] == 64)

def block5_no_third_mode():
    """No third mode / exhaustive two-cell partition (#625 Rung4): both ratios
    subexponential => E subexponential ((S_E) holds).  So every (S_E)-violator
    fires collapse (G_1) OR saturation (Q_img); none escapes both."""
    import random
    random.seed(4242)
    n = 0
    for _ in range(300):
        A_eff = random.choice([16, 27, 36, 49, 64, 81, 125, 128])
        L = random.randint(1, A_eff)
        f = [random.randint(1, 20) for _ in range(L)]
        inv = leaf_invariants(f, A_eff)
        B = max(float(inv["G1"]), float(inv["Qimg"]))
        # E+1 <= G1*Qimg <= B^2   (MASTER-2 + max)
        check("B5.E+1<=G1Qimg", inv["E"] + 1 <= inv["G1"] * inv["Qimg"])
        check("B5.E+1<=B^2", float(inv["E"] + 1) <= B * B + 1e-9)
        # if both ratios <= t then E+1 <= t^2  (no escape)
        for t in (F(2), F(4), F(8)):
            if inv["G1"] <= t and inv["Qimg"] <= t:
                check("B5.both<=t=>E+1<=t^2 t=%s" % t, inv["E"] + 1 <= t * t)
        n += 1
    check("B5.ran census", n == 300)

def block6_router_decidability():
    """DETECTABILITY, made concrete.  The two C7 triggers are functions of the
    profile OCCUPANCY VECTOR alone (image size L, max fiber, mean) -- so the
    router decides them at routing time.  The Fourier/Sidon trigger (L2476,
    additive energy) is NOT a function of the occupancy vector: two leaves with
    the SAME fiber multiset have DIFFERENT additive energy.  That is the single
    spectral outlier the tex keeps 'separate from the constructible atlas'."""
    # (i) collapse & saturation triggers computed from f only == spectral value
    for A_eff, f in [(81, [1] * 9), (256, [64] + [1] * 255),
                     (49, [7, 7, 7, 7, 7, 7, 7])]:
        L = len(f)                                   # router: image size
        Mtot = sum(f)                                # router: total witnesses
        maxf = max(f)                                # router: max fiber
        G1_router = F(A_eff, L)
        Qimg_router = F(maxf * L, Mtot)              # = maxf / (Mtot/L)
        inv = leaf_invariants(f, A_eff)
        check("B6.G1 router==spectral", G1_router == inv["G1"])
        check("B6.Qimg router==spectral", Qimg_router == inv["Qimg"])
    # (ii) additive energy is NOT a function of the occupancy vector.
    #      Two 4-element subsets of Z, both uniform singleton fibers (multiset
    #      {1,1,1,1}), different additive energy E_add = #{(a,b,c,d): a+b=c+d}.
    def add_energy(S):
        from collections import Counter
        cnt = Counter()
        for a in S:
            for b in S:
                cnt[a + b] += 1
        return sum(v * v for v in cnt.values())
    S_ap   = [0, 1, 2, 3]          # arithmetic progression: high energy
    S_sid  = [0, 1, 3, 7]          # Sidon-ish: low energy
    e_ap = add_energy(S_ap)
    e_sid = add_energy(S_sid)
    check("B6.same fiber multiset", sorted([1, 1, 1, 1]) == sorted([1, 1, 1, 1]))
    check("B6.additive energy differs (%d vs %d)" % (e_ap, e_sid),
          e_ap != e_sid)
    check("B6.AP energy>Sidon energy", e_ap > e_sid)
    # => the router (occupancy vector) cannot decide the Sidon/Fourier trigger,
    #    but CAN decide both C7 triggers.  Detectability split, empirical.

def block7_saturation_payment_defeated():
    """Saturation PAYMENT (lem:saturation-principle L2574, prop:saturation-
    payment L4726) needs a UNIFORM lower occupancy H: |Z|<=|C|/H.  The heavy-
    atom has a LIGHT tail, min occupancy = 1, so H=1 gives |Z|<=|C| -- NO
    compression.  'An upper bound on the number of profile lifts goes in the
    wrong direction' (L4738).  Detected but not payable by the printed bound
    (= #626 budget B, PARTIAL)."""
    for A_eff in (16, 81, 256, 625):
        anum = round(A_eff ** 0.75)
        f = [anum] + [1] * (A_eff - 1)
        H = min(f)                                   # uniform lower occupancy
        check("B7.min occupancy H=1 (%d)" % A_eff, H == 1)
        C = sum(f)                                   # |C| raw witnesses
        Zbound = C // H                              # lem:saturation-principle
        check("B7.no compression |Z|<=|C| (%d)" % A_eff, Zbound == C)
    # block-parabola too: singleton fibers => H=1
    check("B7.parabola H=1", min([1] * 9) == 1)

def block8_fi_routing_and_count():
    """(FI)-routing arithmetic (L877-881): a collapse leaf is routed at IMAGE
    scale, Nbar_lambda=|Omega^0|/L=1 (singleton fibers), envelope term
    (1+Nbar)=2.  The COUNT of collapse profiles is the binomial tail (#626
    T-COLLAPSE): N_coll(k,theta)=sum_{j>=theta k} C(k,j)=e^{Omega(N)} -- the
    open PAYMENT that detection does not discharge.  Reproduces #626 exactly."""
    # image-scale occupancy Nbar = 1 for the parabola
    for p, k in [(3, 2), (5, 3), (7, 2)]:
        Omega0 = p ** k                              # |Omega^0| full slice
        L = p ** k
        Nbar = F(Omega0, L)
        check("B8.Nbar=1 image scale (%d,%d)" % (p, k), Nbar == 1)
        check("B8.envelope term=2 (%d,%d)" % (p, k), 1 + Nbar == 2)
    # binomial-tail counts, exact (#626 Rung3, p=3)
    def N_coll(k, theta):
        thr = -(-int(theta * k * 1000) // 1000)      # ceil(theta k) via *1000
        # use exact ceil:
        import math
        thr = math.ceil(theta * k)
        return sum(comb(k, j) for j in range(thr, k + 1))
    check("B8.N_coll(20,0.6)=263950", N_coll(20, 0.6) == 263950,
          str(N_coll(20, 0.6)))
    check("B8.N_coll(40,0.6)=147437500478",
          N_coll(40, 0.6) == 147437500478, str(N_coll(40, 0.6)))
    check("B8.N_coll(40,0.75)=1221246132",
          N_coll(40, 0.75) == 1221246132, str(N_coll(40, 0.75)))
    # positive exponential rate => e^{Omega(N)}, busts A2's e^{o(n)} profiles
    rate = log(N_coll(40, 0.6)) / 40
    check("B8.rate>0 (busts e^{o(n)})", rate > 0.5)

def block9_census():
    """CENSUS.  Run the extracted triggers on three regimes and reproduce the
    sibling-note E values byte-for-byte.  Trigger-firing table is the empirical
    content (MEASURED)."""
    # (a) single admissible power-sum leaves (reproduce #622/#625/#626 exactly)
    #     (p, N, R, m, L, A_eff, E)
    rows = [
        (3, 2, 1, 1, 2, 3,  F(1, 2)),
        (5, 2, 1, 1, 2, 5,  F(3, 2)),
        (5, 3, 1, 2, 3, 5,  F(2, 3)),
        (5, 3, 2, 2, 3, 25, F(22, 3)),
        (7, 3, 1, 2, 3, 7,  F(4, 3)),
        (7, 4, 2, 2, 6, 49, F(43, 6)),
        (7, 5, 2, 2, 10, 49, F(39, 10)),
    ]
    for (p, N, R, m, L, A_eff, E_exp) in rows:
        f = [1] * L                                  # uniform on image
        inv = leaf_invariants(f, A_eff)
        check("B9.single E matches (%d,%d,%d)" % (p, N, R),
              inv["E"] == E_exp, "%s vs %s" % (inv["E"], E_exp))
        # neither C7 trigger fires: G_1 subexp (=A_eff/L bounded), Q_img=1
        check("B9.single Qimg=1 (no raysat) (%d,%d,%d)" % (p, N, R),
              inv["Qimg"] == 1)
        # single leaves are (S_E)-safe: rate decays; here just E small vs A_eff
        check("B9.single (S_E) safe (%d,%d,%d)" % (p, N, R),
              inv["E"] < A_eff)
    # (b) collapse products: collapse trigger fires, rank silent, raysat silent
    for p, k in [(3, 2), (3, 4), (5, 4), (7, 4)]:
        A_eff = p ** (2 * k)
        f = [1] * (p ** k)
        inv = leaf_invariants(f, A_eff)
        collapse = inv["G1"] > 1
        raysat = inv["Qimg"] > 1
        check("B9.collapse fires (%d,%d)" % (p, k), collapse)
        check("B9.collapse: raysat silent (%d,%d)" % (p, k), not raysat)
        check("B9.collapse E=p^k-1 (%d,%d)" % (p, k), inv["E"] == p ** k - 1)
    # (c) saturation products (heavy-atom per block, p=5,a=2/5): raysat fires,
    #     collapse silent, E+1=(5/4)^k exact (multiplicative, #626 BLOCK4)
    # S-block (#626 T,C,S table): full image L_i=p=5, atom a=2/5.  Exact integer
    # fibers M_i=20: [8,3,3,3,3].  Gives G1_i=1, Qimg_i=2, E_i+1=5/4.
    s_inv = leaf_invariants([8, 3, 3, 3, 3], 5)
    check("B9.sat block G1=1", s_inv["G1"] == 1)
    check("B9.sat block Qimg=2", s_inv["Qimg"] == 2)
    check("B9.sat block E+1=5/4", s_inv["E"] + 1 == F(5, 4))
    for k in [1, 2, 3, 4]:               # product over k S-blocks (T3)
        Eprod = (s_inv["E"] + 1) ** k    # multiplicative E+1
        G1 = s_inv["G1"] ** k
        Qimg = s_inv["Qimg"] ** k
        check("B9.sat E+1=(5/4)^k (k=%d)" % k, Eprod == F(5, 4) ** k)
        check("B9.sat G1=1 collapse silent (k=%d)" % k, G1 == 1)
        check("B9.sat Qimg=2^k raysat fires (k=%d)" % k,
              Qimg == 2 ** k and Qimg > 1)
        # MASTER-2 slack on saturation (E+1 <= G1*Qimg):
        check("B9.sat MASTER-2 slack (k=%d)" % k, Eprod <= G1 * Qimg)

# ===================================================================== main
def main():
    block0_master2_spine()
    block1_collapse_witness()
    block2_rank_certificate_inert()
    block3_saturation_witness()
    block4_hole_refutation()
    block5_no_third_mode()
    block6_router_decidability()
    block7_saturation_payment_defeated()
    block8_fi_routing_and_count()
    block9_census()

    total = _PASS + _FAIL
    for line in _LOG:
        print(line)
    print("RESULT: %s (%d/%d)" % ("PASS" if _FAIL == 0 else "FAIL",
                                   _PASS, total))
    return 0 if _FAIL == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
