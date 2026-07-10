# Deep-regime exactness: cyclotomic rigidity and the measured phase
# transition of the t-null census

- **Status:** PROVED (theorem + Lam-Leung descent note at full
  rigor) + measured (exhaustive transitions).
- **Track:** the FINITE prize. Safe to park until the finite pivot.
- **Source:** the fork's finite-track campaign (satellite 29 + the
  phase-transition scans); https://github.com/AllenGrahamHart/rs-mca-prize-dag
- **Verifier:** `python3 experimental/scripts/verify_finite_deep_regime_exactness.py`

## Theorem (deep-regime exactness)

Fix N = 2^s and j (2-power thresholds below; j <= 3 shown here,
general j identical with M_j = least 2-power > j). The moment
vectors of a subset T of mu_N(F_q) are the reductions mod the
prime above q of FIXED cyclotomic integers M_i(T) in Z[zeta_N].
If T is not a union of mu_{M_j}-cosets then some M_i(T) != 0
(the LAM-LEUNG DESCENT: M_1 = 0 forces antipodal pairs; M_2 = 0
forces the pairs antipodal in the quotient — mu_4-coset unions;
each further 2-power threshold in j adds one descent; and p_3
vanishes automatically on mu_4-unions since 3 is coprime to 4 —
which also PROVES struct(j=2) = struct(j=3)). A nonzero M_i(T)
has norm a nonzero integer of size <= N^{phi(N)}, so T can be
j-null for at most phi(N) log_2 N-scale many primes. Union over
the 2^N subsets: for almost every prime q = 1 mod N beyond
2^{(1+eps)N}, the census is EXACTLY the coset-union struct —
ZERO extras, no tolerance needed.

## The measured phase diagram (exact, replayed here at small scale)

Extras exist only in the shallow flat-dominated band; the census
becomes EXACTLY struct far earlier than the theorem's guaranteed
corner (occupancy ~4 in the fork's full scans: 70/70 primes exact
at (N=32, j=3) from q ~ 1000 to 300000; 1247/1247 exact at N=8
through 50000). The verifier replays: (a) an N=8 prime sweep;
(b) the j=4 struct census = 2^{N/8} exactly (the level-dependent
struct — the mu_8-coset unions — at a deep prime); (c) a mini
N=32 meet-in-the-middle transition scan.

## Why this matters for the finite prize

(1) It is the first unconditional EXACT-dichotomy regime for the
t-null census. (2) The mechanism (extras exist mod q only where q
divides finitely many fixed cyclotomic norms) is the cleanest
known explanation of extras scarcity at every measured scale.
(3) It calibrates falsifiers: deep-regime extras would contradict
a THEOREM. (4) The level-dependent struct census (M_j = least
2-power > j) is load-bearing — mis-stating it as 2^{N/4} at
j >= 4 makes census conjectures false (see the necessary-
hypotheses packet).
