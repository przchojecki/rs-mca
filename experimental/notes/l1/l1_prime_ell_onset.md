# L1 Prime-`ell` Onset: Pair-Counting Kills the `t=3` Mixed Kernel Set

## Setting

Background-free coset sunflower over `F_p`, `H = mu_ell` (order `ell | p-1`).
Petals `T_i = a_i H` (`i=1..t`, `alpha_i = a_i^ell`), core `C = union_{j=1..m} b_j H`
(`beta_j = b_j^ell`, all `alpha_i, beta_j` distinct), `phi(Y) = prod_i (Y-alpha_i)`,
`Lambda(Y) = prod_j (Y-beta_j)`, `L_C = Lambda(X^ell)`. Distinct nonzero scalars
`c_i`; received word `U = c_i L_C` on `T_i`, `0` on `C`. `k = m*ell+1`,
`s = (m+1)*ell`. By the PR #219 bijection (`l1_general_reconstruction_collapse.md`)
listed full-petal codewords biject with divisibility-minimal kernel sets `E`
(`ell <= |E| <= (t-1)ell`, `deg W_E <= |E|`), `E` = exact missed core; `E` is MIXED
if not a union of full `H`-cosets. Companion: `l1_coset_mixed_vacancy_threshold.md`
(Theorem A: `m <= t` => total mixed vacancy; the composite-`ell` refutation).

Reduction (PR #219): NO mixed minimal kernel set `<=>` every mixed full-petal
codeword is UNLISTED, i.e. its retained core `R := sum_j rho_j < (m-t+1)ell`, where
`rho_j = #{x in b_j H : P(x)=0}`.

## Theorem R (odd prime `ell`, `t=3`, `m=4`) — PROVED-LOCAL

For `ell` an ODD prime (`ell > 2`), `t=3`, `m=t+1=4`, every `p` and every
distinct-nonzero scalar vector: there is NO mixed minimal kernel set. Equivalently
every mixed full-petal codeword has `R <= 2ell-1 < 2ell = (m-t+1)ell`. (`ell = 2`
is excluded: the closing strict inequality degenerates there; in any case `m=4 <
ell` fails at `ell=2`, so the cell is outside the `m < ell` frontier.)

**Graded form (`m=t+1`).** Full-petal codewords are `P(X) = w(X^ell)+phi(X^ell)g(X)`,
`g(X)=sum_{r=0}^{ell-1} X^r g_r(X^ell)`, `deg g_0 <= m-t`, `deg g_r <= m-t-1` (`r>=1`),
`deg w <= t-1` (`w` fixed by the scalars). At `m=t+1` the bound `deg g_r <= 0`
(`r>=1`) makes each `g_r=gamma_r` a CONSTANT, so
`Gamma(X) := sum_{r=1}^{ell-1} gamma_r X^r` is a single FIXED sector polynomial,
independent of the coset, and the word is mixed iff `Gamma != 0`. On core coset `j`,
`P(b_j h) = P_0(beta_j) + phi(beta_j) Gamma(b_j h)`, so a point is retained iff
`Gamma(b_j h) = lambda_j := -P_0(beta_j)/phi(beta_j)` (`phi(beta_j) != 0`). Thus the
retained set on coset `j` is a single LEVEL SET of the fixed `Gamma`; and since
`P_0 = w + phi g_0` ranges over all polynomials of degree `<= m` as the scalars and
`g_0` vary, the `lambda_j` are FREE. Also `rho_j <= ell-1` (a full coset would force
the degree-`<ell` polynomial `Gamma - lambda_j` to vanish on all `ell` points of
`b_j H`, i.e. `Gamma` constant `= 0`, not mixed).

**Lemma R (pair-count) — PROVED, holds for every `m=t+1`, any `t`.** Every mixed
`m=t+1` codeword satisfies `sum_j rho_j(rho_j-1) <= (ell-1)(ell-2)`.

*Proof.* For `omega in mu_ell\{1}` put `Q_omega(X) = Gamma(X)-Gamma(omega X) =
sum_{r=1}^{ell-1} gamma_r(1-omega^r) X^r`. Since `ell` is PRIME and `1 <= r <= ell-1`,
`omega^r != 1`, so `gamma_r(1-omega^r) != 0` exactly when `gamma_r != 0`; as
`Gamma != 0`, `Q_omega != 0`. Also `Q_omega(0)=0`, so `Q_omega(X)=X*Qtil(X)` with
`deg Qtil <= ell-2`, whence

    #{ x in F_p^* : Gamma(x)=Gamma(omega x) } = #{nonzero roots of Q_omega} <= ell-2.   (*)

The `rho_j` retained points on coset `j` all carry the same value `lambda_j`, so each
ordered pair `(x, x'=omega x)` of distinct retained points (`omega = x'/x in mu_ell\{1}`)
contributes `x` to `(*)` for that `omega`; distinct pairs give distinct `(x,omega)`.
Hence `sum_j rho_j(rho_j-1) <= sum_{omega != 1} #{x in C : Gamma(x)=Gamma(omega x)}
<= (ell-1)(ell-2)`. QED

**Closing (`t=3`, i.e. `m=4` cosets).** Suppose `R = sum_j rho_j >= 2ell`.
Cauchy-Schwarz over the 4 cosets gives `sum_j rho_j^2 >= R^2/4`, so
`sum_j rho_j(rho_j-1) = sum rho_j^2 - R >= R^2/4 - R`. The map `R -> R^2/4 - R` is
increasing for `R > 2`, and `R >= 2ell > 2`, so `sum_j rho_j(rho_j-1) >=
(2ell)^2/4 - 2ell = ell(ell-2)`. But Lemma R gives `<= (ell-1)(ell-2) =
ell(ell-2) - (ell-2) < ell(ell-2)` (`ell > 2`). Contradiction. Hence `R <= 2ell-1`,
the codeword is unlisted, and by the reduction there is no mixed minimal kernel set.
QED

## Corollary — `ell = 5` resolved (one `t=2` cell experimental)

With companion Theorem A (`m <= t` => total mixed vacancy): for `t=3`, odd prime
`ell`, `m <= 4`, the coset full-petal contribution to the primitive count `Q_1^list`
is ZERO unconditionally. For the `m < ell` frontier at `ell=5` the in-range cells
`t < m < 5` are `(3,4)`, `(2,3)`, `(2,4)`: `(3,4)` is Theorem R; `(2,3)` follows by
the SAME proof run over its `m=3` cosets (Lemma R is `t`-independent; Cauchy-Schwarz
over 3 cosets needs `(2ell)^2/3 - 2ell > (ell-1)(ell-2)`, i.e. `ell^2/3 + ell - 2 >
0`, true for all `ell >= 2`); `(2,4)` (`m = t+2`, outside every stated theorem) is
EXPERIMENTAL: exhaustive all-distinct-scalar checks (verifier gate (v), `p in
{31,41}`, using the scalar-scaling reduction to `c=(1,x)`; additionally confirmed
at `p in {61,71}` during panel review) find only full-coset kernel sets, zero
mixed. So the `m < ell` mixed-vacancy at `ell=5`
is proved for all `t >= 3` and `(2,3)`, and verified (not proved) at `(2,4)`.

## Tightness — CERTIFICATE

The bound is razor-tight: exhaustive projective enumeration of `Gamma` at
`(t=3, ell=5, m=4)` gives `max_Gamma sum_j maxfiber_j = 9 = 2ell-1` at `p=41` and
`p=61` (retained profile `[3,2,2,2]`, `sum_j rho_j(rho_j-1) = 12 = (ell-1)(ell-2)`
achieved WITH EQUALITY, so Lemma R has no slack). The `lambda_j` being free, this is
realized by an ACTUAL mixed codeword over distinct nonzero scalars: at `p=41`,
`c=(27,1,16)`, with cosets labelled by increasing least element (petals = the
`mu_5`-cosets of `1, 2, 3`; core = those of `4, 5, 6, 11` — this labelling, NOT
primitive-root power order, is the one under which these scalars attain the max;
exact point sets and the codeword are embedded in verifier gate (iii)), an explicit
degree-`19 (<= m*ell=20)` codeword agrees with `U` on all `15` petal points, has
exactly `9` retained core points, and a MIXED missed core of size `|M| = 11`. So the corrected mechanism margin is `min |M| = (t-1)ell+1 = 11`
(retained `2ell-1`), one point short of listed — NOT the loose `16` from an earlier
sampled scan. Any argument with slack would fail; the proof's strict step
`(ell-1)(ell-2) < ell(ell-2)` is exactly what supplies the "`-1`".

## Lemma Psi_1 — first rung of the general-`m` rigidity hierarchy (PROVED)

For general `m` a coset with `n_j := ell - rho_j = 1` forces `P_r(beta_j) = e_j theta_j^r`
(single geometric ratio), `theta_j^ell = beta_j^{-1}`; for consecutive live sectors
`beta_j` is then a root of `Psi_r(Y) = Y g_{r+1}(Y)^ell - g_r(Y)^ell` (degree
`<= 1 + ell(m-t-1)`, nonzero because its two leading terms sit in different residues
mod `ell`). Hence `#{ j : n_j = 1 } <= 1 + ell(m-t-1)`. At `m=t+1` (`D=0`) this reads
`<= 1`. This is the `nu=1` rung of a resultant-elimination hierarchy for
`#{ j : n_j <= nu }`; assembling all rungs against the listedness budget is the
identified route to general `m`.

## Scope — honest

- Pair-counting closes EXACTLY `t=3` (PROVED limitation). The closing step needs the
  integer program `max sum_j rho_j` subject to `sum rho_j(rho_j-1) <= (ell-1)(ell-2)`,
  `0 <= rho_j <= ell-1`, over `m=t+1` cosets, to stay below `2ell`. For `t=3` the IP-max
  is `2ell-1` at every `ell`; for `t>=4` the IP-max is `>= 2ell` (e.g. `t=4,ell=7`: `15`;
  `t=4,ell=11`: `23`), so the pair-count budget ALONE cannot exclude `R=2ell`. The
  theorem is still TRUE for `t>=4` (aggressive codeword-space search never reaches `2ell`;
  smallest gap `1`, only at `(5,3,4)`) but OPEN — closing it needs the realizability
  constraint the pair-count misses (a single `deg <= ell-1` `Gamma` cannot have medium
  fibers on many cosets at once).
- General `m > t+1` (`D >= 1`): the `g_r` become non-constant, there is no single fixed
  `Gamma`, the pair-count breaks; numerically vacant throughout `m < ell` but OPEN.
- Prime vs composite: `(*)` uses `omega^r != 1` for `1 <= r <= ell-1`, which holds iff
  `ell` is PRIME. For composite `ell` it fails and the onset is genuinely earlier —
  consistent with the `ell=6` mixed witnesses at `m=t+1` in the companion note.

## Status

PROVED-LOCAL: Theorem R (`odd prime ell, t=3, m=4`), Lemma R (all `m=t+1`), the `ell=5`
corollary (with companion Theorem A), Lemma Psi_1. CERTIFICATE: the razor-tight
retained-`9` witness at `(5,3,4)`. PROVED limitation: pair-counting closes only `t=3`.
OPEN: `t>=4` and general `m` (numerically vacant, no primitive mixed set observed at
`m<ell`). Sharpens the counting consequence of Lemma 8 of
`l1_full_list_quotient_proof_program.md`; no paper-text change, material in
`experimental/`.

## Parameters

Theorem/lemma: `ell in {5,7,11,13}`, `t=3`, `m=4`. Exhaustive (`Gamma`-projective and
kernel-set lattice): `ell=5`, `p in {41,61}`. IP closing step: `ell in {5,7,11,13}`
(and the `t>=4` failure). Tightness witness embedded at `p=41`. All scalars distinct
nonzero; petals/core genuine `mu_ell` cosets.

## Reproducibility

`experimental/scripts/verify_l1_prime_ell_onset.py` (stdlib-only, offline,
deterministic; exit 0 iff all gates pass): (i) Lemma R and the `(*)` root bound,
EXHAUSTIVE over projective `Gamma` at `ell=5` (`p in {41,61}`) and sampled at
`ell in {7,11,13}`, zero violations, equality `(ell-1)(ell-2)` attained; (ii) mixed
vacancy at `(t=3,m=4)`: EXHAUSTIVE `Gamma`-projective max retained `= 2ell-1` plus
direct minimal-kernel-set lattice enumeration `= 0` mixed at `ell=5`; exact IP-max
`= 2ell-1 < 2ell` with the kernel-range exclusion at `ell=7` (`p in {71,113}`);
(iii) the embedded retained-`9` witness re-verified from scratch (`|M|=11`, mixed,
unlisted); (iv) Psi_1 spot check `#{n_j=1} <= 1 + ell(m-t-1)`; (v) the `(t=2,m=4,
ell=5)` exhaustive all-scalar vacancy (`p in {31,41}`).
