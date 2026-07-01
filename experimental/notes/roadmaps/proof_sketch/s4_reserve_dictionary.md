# S4: the reserve dictionary — one entropy budget, four coordinate systems

- **Status:** the core identity is VERIFIED-DICTIONARY (same defining
  equation, matched numerically to 6 digits); textual correspondences quoted
  from `tex/slackMCA_v4.tex`; residual breadth questions labelled GAP.
- **Parent:** `prize_proof_sketch_spine.md` S4 (upgraded from CONJECTURE).

## 1. The identity: FM crossover = tau* [VERIFIED]

Paper B's entropy gap (`def:taustar`): `tau*(rho, q)` is the unique
`tau in (0, 1-rho)` with

```text
tau log2 q = H(rho + tau),        tau* = (H(rho)+o(1))/log2 q.
```

My FM crossover (spine SS3) solves `n H(delta) = t log2 q - 128` with
`t = n(1-delta-rho)`; writing `tau = 1-rho-delta` and using the symmetry
`H(1-rho-tau) = H(rho+tau)`, this is THE SAME EQUATION up to the `128/n`
term. Machine-checked at `log2 q = 256`:

```text
rate    tau*        1-rho-tau*    turn-1 FM d_fm     match
1/2     0.003906    0.496094      0.496094           exact
1/4     0.003189    0.746811      0.746811           exact
1/8     0.002147    0.872853      0.872853           exact
1/16    0.001338    0.936162      0.936162           exact
```

So the list-side pigeonhole scale (`thm:pigeonhole` / `cor:entropy-lower`,
PROVED-cited) and the MCA-side alignment first moment (Lemma FM1, exact)
are ONE entropy budget seen from two sides. Spine node S4's "reserve
unification" is not an analogy — it is a definitional identity.

## 2. The quantifier dictionary [textually grounded]

**`thm:normalform` (quoted, PROVED-cited):**
`emca(C, delta) = (1/q) max_{1<=t<=r} Lambda^NC_{t,delta}(D,k)` — exact,
both directions constructive. So "max over residue-line data of noncontained
slope counts" IS "max over lines of bad-slope counts": packing numbers and
per-pair counts are the same object after the max. My per-pair `B_C(A)` at
EXACT agreement refines the `|S_z| >= s_delta` (cumulative) convention;
summing exact-agreement buckets recovers it.

**Three different t's — disambiguation table:**

```text
t_denom   denominator degree in def:residue (1 <= t <= r); the datum's t
T_slack   monomial exponent in x^{k+T} + z x^k (rem:strata stratum)
t_win     my syndrome window t = A - k (exact-agreement bucket)
relations: monomial stratum has E = X^r (t_denom = r, maximal);
           t_win is a bucket parameter, orthogonal to the datum's t_denom.
```

**Noncontainment matches:** def:residue's "no `A, G` of degree `<k` with
`A = w/E`, `G = -B/E` on `S_z`" is exactly the degenerate-pencil exclusion
(`a = b = 0` stratum) of spine SS2 — the pair explained on the same support.

**Sharpness:** rem:strata notes the tangent floor saturates the
`n^{1+o(1)}` in conj:B — the poly term in the operative R2 is not slack to
be optimized away; it is achieved.

## 3. GAP-2 resolved at sketch level [derivation]

rem:aper strips lines whose denominator is a pullback `E = g(X^M)`,
`M | gcd(n,k)`. A pullback denominator forces `M | t_denom`; with
`M | gcd(n,k)` we get `M | r = n-k`, hence `M | j <=> M | t_win` — the
line-side strip coincides with the RATE-PRESERVING support-side strip
(`k/M` integral: exactly my proved `Q_M = Q_1(H_{n/M})` recursion's
hypothesis). The residual seam — strata with `M | gcd(n,j)` but `M !| k` —
are non-rate-preserving folds: the syndrome conditions do not descend to a
valid quotient row, so no alignment boost is expected [SKETCH]; they stay
on the aperiodic side, and the checker convention is rem:aper's.
GAP-2 of `s3b_ii` is closed at sketch level (source-checked normal form).

## 4. Where the 128 bits sit [verified arithmetic]

The transition is extremely sharp: `d log2(count)/d delta ~ n(log2 q +
H'(delta)) ~ 2^41 * 256 = 2^49` bits per unit `delta` at prize scale, so
the 2^128 factor between "count ~ B*" and "count ~ q" moves the crossover by

```text
Delta delta ~ 128 / 2^49 = 2^-42       (invisible at the 2^-9 corridor).
```

Per-lane placement of the bits:

```text
MCA lane:    B* = q_line * 2^-128 (the gate); FM budget check: poly slack
             n^B costs 41B bits, B <= 3 (turn 2).
list lane:   |interleaved list| <= 2^-128 * |F_chal| — bits on the
             challenge-field denominator, NOT in the L1 reserve.
L1 lane:     reserve is bit-free: sigma log2 q_D >= (1+eps) log2 C(n,a),
             i.e. eta >= (1+eps) tau*(rho, q_D) — a poly-list statement;
             the 128 bits re-enter only at assembly (S8).
```

**Field-argument column (the one real asymmetry):** conj:B and the L1
reserve use `tau*(rho, q_D)` (GENERATED field); my corridor used `q_line`.
For the pinned row they coincide: `ord(17 mod 512) = 32` (verified), so
`mu_512` generates `F_17^32` and `q_gen = q_line`. Rows whose domain
generates a proper subfield split the two reserves — an S5 hypothesis line
("domain generates F", or track both reserves) and a WP-0.2 check against
the official family.

## 5. Consequences and forks

Below `(1+eps) tau*`: pigeonhole gives exponential lists (PROVED) and FM
gives super-B* alignment mean — the negative sides cohere across lanes.
Above: both positive halves are the same wall in two coordinates (the
per-fiber collision family, turns 4-5). The dictionary makes cross-lane
bookkeeping mechanical; nothing about it removes the wall.

```text
F1 (breadth): thm:normalform reduces every line to a t_denom = r datum, and
    rem:strata says the proved positive machinery lives on the MONOMIAL
    stratum; the reduction of arbitrary (E, B, w) data to monomial-type
    analysis is the old T4 arbitrary-word question — a named GAP consumed
    by the mechanisms (their statements quantify over all pairs, so no new
    wall, but stratum-specific shortcuts do not transfer automatically).
F2 (fields): official rows with q_gen < q_line make conj:B's reserve the
    binding one; the S5 per-rate tables must carry both tau* columns.
F3 (sharp constants): the o(1) in tau* and in Acl matter at corridor scale;
    any numeric delta* quoted to the community must carry second-order
    error bars — flag to WP-1.1/WP-7.4 wording.
```
