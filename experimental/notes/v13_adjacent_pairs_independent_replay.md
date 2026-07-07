# Independent exact replay of the four v13 adjacent pairs

- **Status:** AUDIT / EXPERIMENTAL (supports, does not perform, v13
  promotion).
- **Script:** `experimental/scripts/verify_v13_adjacent_pairs_independent.py`
  (~1 minute, Python integers only).
- **Data:** `experimental/data/v13_adjacent_pairs_independent_replay.json`.

## What is verified

A from-scratch implementation (no shared code with this repo's scripts;
independent bit-length integer arithmetic) of the exact comparisons of
`prop:capg-moved-frontier` / `cor:capg-adjacent-pairs`
(experimental/cap25_cap_v13_raw.tex):

    list row : unsafe(m)  <=>  C(n,m) > p^(m-K)   * floor(q * eps*)
    MCA row  : unsafe(m)  <=>  C(n,m) > p^(m-K-1) * floor(q * eps*)

with n = 2^21, k = 2^20; KoalaBear p = 2^31−2^24+1, q = p^6,
eps* = 2^−128; Mersenne-31 p′ = 2^31−1, q = p′^4, eps* = 2^−100. All ten
integer comparisons reproduce (four passes at a0, four failures at a0+1,
two admissibility inequalities, checked in both the q−n and q−|B| forms):

    row              a0        unsafe@a0   fail@a0+1   (AGENTS.md margins)
    KoalaBear MCA    1116047   +8.978      −22.197     22.1969  OK
    KoalaBear list   1116046   +9.164      −22.011     22.0109  OK
    Mersenne-31 MCA  1116023   +27.927     −3.259      3.2589   OK
    Mersenne-31 list 1116022   +28.113     −3.073      3.0730   OK

Margins match the AGENTS.md / cor:capg-adjacent-pairs table to every
printed decimal. The MCA/list convention was re-derived independently
before matching (the identity witness at K = k+1 supplies the one-factor-
of-p pencil shift; the M31 rows pin q = p′^4 and eps* = 2^−100).

## Why this is useful

The Paper-D promotion rule requires the v13 rows be "printed, replayed,
audited" before citation as theorem rows. This packet is a third-party
replay of the unsafe certificates and the pair locations from an
independent code path: same integers, same margins, conventions re-derived
rather than copied. It does NOT audit the (conjectural) safe side at
a0 + 1 — the pair verdicts here verify the unsafe pass and the displayed
comparison failure, exactly as stated in the source.

One external observation worth recording with the audit: the list-row
unsafe test is the statement "the base tangent-column mean
C(n,m)·p^(K−m) crosses the row gate floor(q·eps*)" — the pigeonhole floor
sits at the first-moment mean, which is why the pair locations are
first-moment-predictable. (In our own program's ledger dictionary this is
the tangent-column mean; the identity m′ = K−1+d1 ⇒ p^−(d1−1) = p^(K−m′)
makes prop:capg-census-floor's M_B(d1) equal to
C(m′,m)·ceil(tangent mean) exactly.)

## What to do next

Fold into whatever replay matrix gates the v13 → Paper D promotion; the
script is deterministic and CI-friendly (exits nonzero on any mismatch).
