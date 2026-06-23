# X1: Interleaved Deep-Point Bridge (list -> interleaved CA/MCA, forward direction)

- **Status:** AUDIT (base identity, independently reproduced) / CONJECTURAL->TARGET
  (interleaved extension, stated here, proved+verified in later commits).
- **Agent/model:** Claude Opus 4.8 (L2 loop, branch `allen/l2-x1-interleaved-mca`).
- **Date:** 2026-06-23.
- **Scope:** Problem X1 (list <-> CA/MCA without square-root loss) and L2
  (interleaved-list constants), `agents.md`. Builds on
  `notes/f1/f1_deep_point_list_to_ca_mca.md` (avdeevvadim, Theorem 1.1/2.2) and
  `notes/l2/l2_interleaved_dilation_constants.md` (our L2 sharp-constant target).
  Does not edit Papers A--D.

## Lane / non-overlap statement

This note is the **forward, interleaved** half of the deep-point program:
turning interleaved *list upper bounds* (L2) into interleaved/curve **MCA**
bad-slope counts for `RS[F,D,k]`. It deliberately does **not** touch the
base-code *cap* / counterexample-arithmetic direction (consume a list *lower*
bound to cap `delta*`), which is the subject of the active M1 audit PR #100
(`codex/m1-cycle120-gate-audit`, the `n=512,k=256,delta=125/256` row). Files
here live under `notes/x1/`, `notes/l2/`, and `scripts/verify_x1_*` /
`scripts/verify_l2_*`; they do not collide with `notes/m1/` or `verify_m1_*`.

## 1. Base identity, independently audited

Theorem 1.1 of the deep-point note states, for `U : D -> F`, a deep point
`alpha in F \ D`, the simple-pole line

```text
f_alpha(x) = U(x)/(x-alpha),   g_alpha(x) = -1/(x-alpha),
```

and `k < a <= n`, `delta_a = 1 - a/n`:

```text
Bad_CA(f_alpha,g_alpha; delta_a)
  = Bad_MCA(f_alpha,g_alpha; delta_a)
  = Deep_alpha(U,a)
  = { P(alpha) : P in F[X]_{<k+1}, |{x in D : P(x)=U(x)}| >= a }.
```

The proof (note §1) is clean: forward, `Q(X)=(P(X)-P(alpha))/(X-alpha)` has
degree `< k` and explains `f_alpha + P(alpha) g_alpha` on the agreement support;
the global far condition is that `g_alpha` has no degree-`<k` explanation on any
support of size `> k` (else `H(X)=(X-alpha)G(X)+1` would vanish at `> k` points
yet `H(alpha)=1`). Reverse: multiply the support identity by `(x-alpha)`.

**Independent reproduction.** `scripts/verify_x1_deep_point_identity.py`
re-derives the three sets from scratch in a model independent of the existing
`f1_deep_point_list_to_ca_mca_sanity.py`:

- prime field `F_p` only, so the deep point `alpha` ranges over **all** of
  `F_p \ D` (prime-field deep points, not only an extension-valued `alpha=t`);
- many received words per configuration (monomial-prefix, degree-`k`, and
  several deterministic pseudo-random words), not one hand-picked word;
- `Bad_CA`, `Bad_MCA`, `Deep_alpha` each computed by a separate brute force and
  asserted mutually equal.

Result: PASS over `(p,n,k,a) in {(17,8,3,5),(17,8,4,6),(17,16,8,12),(41,8,3,5)}`,
**312 identity checks** (e.g. `p=41,n=8`: 33 deep points x 6 words). The global
far condition holds at every prime-field deep point in every configuration. This
upgrades the base identity from "one extension-field example" to "all
prime-field deep points x many words across four fields", with no exception.

## 2. Interleaved deep-point bridge (the new target)

Let `U=(U_1,...,U_mu) : D -> F^mu` be a `mu`-row received word and let `Int(C,mu)`
be the `mu`-fold interleaving of `C=RS[F,D,k]` with **column distance**
(common agreement support). Fix a deep point `alpha in F \ D` and form the
*shared-pole* curve

```text
f_alpha^{(i)}(x) = U_i(x)/(x-alpha),    g_alpha(x) = -1/(x-alpha),   i=1..mu,
```

i.e. the same denominator `(x-alpha)` in every row. A slope **vector**
`z=(z_1,...,z_mu) in F^mu` is *interleaved-MCA-bad* at radius `delta_a` if there
is a common support `S`, `|S| >= a`, on which every row
`f_alpha^{(i)} + z_i g_alpha` is explained by `C`, while the curve is not
simultaneously explained on any support of size `> k`.

**Target Theorem (interleaved deep-point identity).** Define the
*interleaved deep image*

```text
Deep_alpha^{mu}(U,a)
  = { (P_1(alpha),...,P_mu(alpha)) :
      P_i in F[X]_{<k+1},
      |{x in D : P_i(x)=U_i(x)  for all i}| >= a }.
```

Then the interleaved-MCA-bad slope vectors of the shared-pole curve at
`delta_a` equal `Deep_alpha^{mu}(U,a)`; in particular

```text
|Bad_MCA^{int}(alpha; delta_a)| = |Deep_alpha^{mu}(U,a)| <= |Lambda(Int(C_+,mu), delta_a, U)|,
```

the interleaved (column-distance) list of `C_+ = RS[F,D,k+1]` at radius
`delta_a`. The forward inclusion is the per-row computation of §1 applied on the
**common** support `S` (the same `Q_i(X)=(P_i(X)-P_i(alpha))/(X-alpha)` has
degree `< k`); the reverse multiplies each row identity by `(x-alpha)` and uses
that the shared far condition for `g_alpha` is exactly the §1 far condition,
independent of `mu`.

**Why this is the L2 payoff (mu-independent transfer).** For the averaging
(Lemma 2.1 analogue), two *distinct* interleaved tuples `(P_i^{(s)})` and
`(P_i^{(t)})` differ in some row `i0`, and `{alpha : P_{i0}^{(s)}(alpha) =
P_{i0}^{(t)}(alpha)} <= k`. Hence the simultaneous-collision set has size `<= k`
**regardless of `mu`**, so the deep-point evaluation expansion gives the *same*

```text
M >= L / (1 + k(L-1)/|Omega|)
```

bound for the interleaved tuple list as for a single row. Combined with the L2
result that the interleaved list numerator does not pay the Cartesian exponent
(`l2_interleaved_dilation_constants.md` §2-§5: `binom(n,a) q^{-mu(a-k)} +
Quot_mu`), this says: **interleaving multiplies neither the transfer constant nor
the list numerator** -- the forward list->MCA conversion is `mu`-clean. This is
the positive/forward counterpart of the negative cap direction, and the exact
statement Paper C needs to consume interleaved lists as interleaved MCA.

## 3. Plan (incremental commits on this PR)

1. (done) Independent audit + broadened verifier of the base identity (§1).
2. Interleaved identity (§2): proof + `scripts/verify_x1_interleaved_deep_point.py`
   checking `Bad_MCA^{int} = Deep_alpha^{mu}` and the `mu`-independent collision
   bound over `F_17`, `mu=2,3`.
3. Forward X1 statement: combine §2 with the L2 numerator to print an explicit
   interleaved-MCA bad-slope-vector count vs. the L2 list bound; verifier.
4. (stretch) push the aperiodic `mu`-fold remainder of the L2 conjecture, now
   carrying MCA meaning through §2.

## Ledger impact

- **X1 (forward, new):** a square-root-loss-free list->MCA transfer in the
  interleaved setting, with a `mu`-independent transfer constant.
- **L2 (sharpened):** the interleaved-list bound becomes an interleaved-MCA
  statement, not merely a list statement.
- **Field ledger:** all objects stay over the same `F`; no `q_gen`/`q_chal`
  swap. The deep point `alpha` is in `F \ D`; the list is the `C_+ = RS[F,D,k+1]`
  list at the *same* radius `delta_a`.

## Reproducibility

```bash
python3 experimental/scripts/verify_x1_deep_point_identity.py
python3 experimental/scripts/verify_x1_deep_point_identity.py --json
```
