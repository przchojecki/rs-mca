# L1 Prefix Fibers as Divisor-Coefficient Counts, with an Exact Quotient-Core Floor

- **Status:** PROVED (quotient-core theory) / CONDITIONAL (Fourier bound) /
  EXPERIMENTAL (scans) / AUDIT (cross-checks). `conj:prefix-local` itself: OPEN,
  reduced.
- **Agent/model:** Claude Opus 4.8.
- **Date:** 2026-06-18 / 2026-06-19.
- **Scope:** Paper B `conj:prefix-local`, `conj:arbitrary-local`,
  `thm:conditional-list` (`tex/slackMCA_v3.tex`) and the L1 target in
  `agents.md`. This note does not edit Papers A--D and does not assert
  Reed--Solomon list decoding, MCA, or protocol safety. It is the list/locator
  side of the program; it does not touch the M1 residue-line work.

## Claim and results ledger

The object is the Paper B monomial-prefix fiber `Phi_sigma^{-1}(c)`
(`def:locator-fiber`, `prop:monomial-fiber`), recast through the
complement-locator bijection of `l1_aperiodic_prefix_collision.md` as a count of
monic degree-`m` divisors of `X^n-1` over `F_q` with prescribed top `sigma`
coefficients. The note builds a complete theory of the **quotient-core
(structured) part** of this count and reduces the remaining **aperiodic** part to
a subgroup exponential-sum estimate.

| § | Result | Status | Supports |
|---|--------|--------|----------|
| 1 | Prefix fiber = prescribed-top-coefficient divisor count of `X^n-1` | PROVED | recasts `conj:prefix-local` |
| 2 | `K_d`-coset-union locator lemma; quotient-core floor `max_c |fiber| >= binom(n/d,m/d)` | PROVED | `conj:prefix-local` `Quot` term (lower bd) |
| 5 | Exact structured count = subgroup-lattice Möbius sum; dyadic collapse `binom(n/d*,m/d*)` | PROVED | `conj:prefix-local` `Quot` term (exact) |
| 6 | Dilation equivariance `Phi_sigma(h.A)=h*Phi_sigma(A)`; `Stab_H(A)=K_{per(A)}` | PROVED | worst-case reduction |
| 7 | Prefix-space localization `per(A) | g_c`: generic fibers (`c_1!=0`) purely aperiodic | PROVED | `conj:prefix-local` quotient/aperiodic split |
| 8 | Non-enumerative DP counter; first entropy-cleared **sub-Johnson** data (`F_257,n=32`) | EXPERIMENTAL | evidence for `conj:prefix-local` beyond Johnson |
| 9 | Arbitrary-word lift to `ImgFib_U`: dilation symmetry + folding source `W|->W(X^d)` | PROVED | `conj:arbitrary-local`, `thm:conditional-list` |
| 10 | Fourier reduction: `S(r)=e_m({e_p(g_r(a))})`, power sums = subgroup Weil sums `T(lr)` | PROVED (identity) / CONDITIONAL (bound) | reduces `conj:prefix-local` to exp-sums |
| 11 | Structured/generic `r` split: classified + measured; necessary but NOT sufficient (needs phase cancellation) | PROVED (classification) / EXPERIMENTAL / route-refinement | sharpens the §10 open step |

**What is proved.** The structured (quotient-periodic) contribution to the list
is *completely characterized*: it is an exact, field-independent count
(`binom(n/d*, m/d*)` at dyadic rates, Möbius in general), it is localized
identically in divisor space (§2,§5), prefix space (§7), arbitrary-word/list
space (§9), and Fourier space (§10, the large coefficients), and it is removed by
the dimension dither `gcd(n, k+sigma) <= sigma`.

**What remains open.** The upper bound on the *aperiodic* (generic, `g_c=1`,
trivial-stabilizer) list above the corrected reserve --- the genuine content of
`conj:prefix-local`. §10 reduces it to a uniform-in-`l` subgroup
exponential-sum estimate; §11 then shows the natural structured/generic-`r` split
is *necessary but not sufficient* (the generic bulk dominates the `L1` bound,
which itself overestimates the truth by `4-10x` due to phase cancellation). So
the essential difficulty is pinned to *cancellation across `r`* --- the
second-moment `sec:pairwise` barrier of Paper B, in Fourier form.

All PROVED/EXPERIMENTAL claims are machine-verified:
`verify_l1_prefix_divisor_count.py` (§§1-8, reproduces the `F_17` certificate),
`verify_l1_arbitrary_word_lift.py` (§9), `verify_l1_fourier_reduction.py` (§10).

## Parameters

`q`, `q_gen = q` (split case `n \mid q-1`), `n = 2^m_0`, `k`, `rho = k/n`,
`sigma`, `s = k+sigma`, `m = n-s`. Toy cases: `q=17, n=16` (this note);
`q=257, n=256` and dyadic `n` flagged for the optimized non-enumerative path.

## Existing paper dependency

- `def:locator-fiber`, `prop:monomial-fiber`, `prop:arb-fiber`,
  `conj:prefix-local`, `conj:arbitrary-local` in `tex/slackMCA_v3.tex`.
- The complement-locator compression (`E_S(Z) E_A(Z) = 1-(-Z)^n`) and the
  divisor-gap picture of `experimental/l1_aperiodic_prefix_collision.md`.
- The honest-list repair (`ImgFib`) of `experimental/l1_arbitrary_fiber_repair.md`:
  the raw `Fib_U` overcounts; the prefix fiber `Phi_sigma^{-1}(c)` is exact only
  for monomial-prefix data, which is the regime treated here.

## 1. Divisor-coefficient reframing

Let `H = mu_n <= F_q^*` (so `n \mid q-1`, `X^n - 1 = prod_{h in H}(X-h)`).
For `S in binom(H, s)` let `A = H \ S`, `|A| = m`. The locator
`L_A(X) = prod_{a in A}(X-a)` is a **monic degree-`m` divisor of `X^n-1`**, and
every such divisor arises this way (its roots are distinct elements of `H`).
The complement-prefix lemma gives, for equal-size supports `S,T`,
```text
Phi_sigma(S) = Phi_sigma(T)
  iff  (e_1(A),...,e_sigma(A)) = (e_1(B),...,e_sigma(B))
  iff  L_A and L_B share their top sigma coefficients,
```
where `B = H \ T`. Writing the prescribed top-`sigma` coefficient vector as the
fiber key, we obtain the canonical bijection
```text
Phi_sigma^{-1}(c)  <->  { monic degree-m D | X^n-1 : top sigma coeffs of D fixed }.
```
Thus the prefix-fiber histogram of `conj:prefix-local` is the histogram of
degree-`m` divisors of `X^n-1` bucketed by their top `sigma` coefficients. This
is the object the scanner computes directly (no codewords, no field-size
enumeration), and it reproduces the `F_17, k=6, sigma=4` certificate exactly
(8008 divisors, 7968 distinct keys, 40 two-point fibers, max fiber 2).

## 2. The quotient-periodic locator lemma

For `d \mid n`, let `K_d <= H` be the unique subgroup of order `d`
(`K_d = mu_d`). Call `A <= H` a **`K_d`-coset-union** if `A K_d = A`.

**Lemma (coset-union locators are `X^d`-polynomials).**
Let `A` be a `K_d`-coset-union with `|A| = m` (so `d \mid m`). Write the cosets
comprising `A` as `zeta_1 K_d, ..., zeta_{m/d} K_d`. Then
```text
L_A(X) = prod_{j=1}^{m/d} (X^d - beta_j),   beta_j := zeta_j^d,
```
a polynomial `G(X^d)` with `G(Y) = prod_j (Y - beta_j)` monic of degree `m/d`.
The `beta_j` are distinct `(n/d)`-th roots of unity, so `G` is a monic
degree-`m/d` divisor of `Y^{n/d}-1`. The map `A \mapsto G` is a bijection from
`K_d`-coset-union divisors of degree `m` onto `(m/d)`-subsets of `mu_{n/d}`; in
particular there are exactly `binom(n/d, m/d)` of them.

*Proof.* For a single coset, `prod_{kappa in K_d}(X - zeta kappa)
= prod_{kappa in mu_d}(X - zeta kappa) = X^d - zeta^d`, because the left side is
monic of degree `d`, vanishes exactly at `zeta mu_d`, and `X^d - zeta^d` has the
same roots. Multiplying over the `m/d` chosen cosets gives the displayed product,
which is a polynomial in `X^d`. Each `beta_j = zeta_j^d` satisfies
`beta_j^{n/d} = zeta_j^n = 1`; distinct cosets give distinct `beta_j` (the `d`-th
power map `mu_n -> mu_{n/d}` has kernel `K_d`, so it is injective on coset
representatives). Conversely any `(m/d)`-subset of `mu_{n/d}` lifts to a unique
`K_d`-coset-union via the surjection `mu_n -> mu_{n/d}`. ∎

**Coefficient corollary.** Since `L_A = G(X^d)` has nonzero coefficients only at
degrees divisible by `d`, and `d \mid m`, the coefficient of `X^{m-i}` vanishes
unless `d \mid i`. Hence the top `sigma` coefficients of `L_A` are:
- forced zeros at all positions `i in {1,...,sigma}` with `d \nmid i`, and
- the top `floor(sigma/d)` coefficients of `G` at positions `i in {d,2d,...}`.

So `Phi_sigma` restricted to `K_d`-coset-unions factors through
`Phi_{floor(sigma/d)}` of the *smaller* divisor problem on `mu_{n/d}`.

**Corollary (quotient-core floor).** If `d > sigma` then `floor(sigma/d) = 0`:
every `K_d`-coset-union of degree `m` has the all-zero top-`sigma` key, so they
all share one fiber. Therefore, for every `d \mid gcd(n, s)` with `d > sigma`,
```text
max_c |Phi_sigma^{-1}(c)|  >=  #{K_d-coset-union divisors of degree m}
                            =  binom(n/d, m/d).
```
(`d \mid m = n-s` and `d \mid n` together are equivalent to `d \mid gcd(n,s)`.)

### Consequences

- **Field-independence.** The floor `binom(n/d, m/d)` does not involve `q`. No
  generated-field entropy reserve can suppress it; this is exactly why the
  arbitrary-word raw conjecture needs the quotient-core carve-out of
  `conj:prefix-local`, on the list side as well as the MCA side.
- **Dithering kills it (link to L3).** If `k` is chosen so that
  `gcd(n, k+sigma) <= sigma`, then no order `d > sigma` divides `gcd(n,s)`, and
  this coset-union floor is empty. This is the locator-side statement of the
  `k = rho n - r` dimension dithering studied in `quotient_profile_dither.md`:
  the dither target is to make `gcd(n, k+sigma) <= sigma`.
- **Aperiodic remainder is the real target.** After removing coset-union
  divisors for all active `d > sigma`, the *aperiodic* prefix count is what
  `conj:prefix-local` predicts to be `binom(n,s)/q^sigma + O(n^B)`. The scan
  isolates and counts this remainder; bounding it is the open analytic step
  (and the direct list-side analogue of Codex's M1 aperiodic residue-line wall).

## 3. Numerical experiment (`F_17`, `n=16`)

Exact full enumeration of all `binom(16,m)` divisors, bucketed by top-`sigma`
coefficients. The coset-union count matches `binom(n/d, m/d)` and the floor is
respected in all 35 `(k,sigma)` cases swept by the verifier. Selected rows:

| rho   | k | sigma | m | entropy margin (bits) | max fiber | quot. floor (d>sigma) | nonsingleton aperiodic |
|-------|---|-------|---|----------------------:|----------:|----------------------:|-----------------------:|
| 6/16  | 6 | 4     | 6 | +3.383                |        2  | 0 (none divides gcd=2)|  80 / 80               |
| 4/16  | 4 | 4     | 8 | +2.698                |        2  | 2  (d=8)              | 480 / 482              |
| 6/16  | 6 | 2     | 8 | -5.477                |       54  | 6  (d=4)              | 12864 / 12870          |
| 7/16  | 7 | 1     | 8 | -9.564                |      758  | 70 (d=2)              | 12800 / 12870          |

Reading: where the generated-field entropy margin is positive (rows 1--2), the
aperiodic prefix fibers are already polynomial (max size 2) and the only
non-aperiodic members are the coset-union divisors flagged by the lemma. Where
the margin is negative (rows 3--4) the random codimension-`sigma` law dominates
and fibers sit near `binom(16,m)/17^sigma`; the coset-union floor is still
present but submerged. `F_17, n=16` is too small to realize a large quotient
floor *and* a cleared entropy margin simultaneously; that separation needs
`n in {32,64}` (next iteration, optimized path).

## 4. Audit cross-check

`verify_l1_prefix_divisor_count.py --self-check` confirms, against
`l1_aperiodic_prefix_collision.md`:

- `total_divisors = 8008`, `distinct_prefix_values = 7968`, `max_fiber = 2`,
  `two_point_fibers = 40`;
- all 40 nonsingleton fibers are aperiodic for the active orders `{8,16}`
  (matching the note's `M=8`/`M=16` coset-union exclusion);
- the `X^d -> Y` injection of the Lemma holds for every order `d in {2,4,8,16}`;
- the coset-union identity `binom(n/d,m/d)` and the quotient-core floor hold
  across a 35-case `(k,sigma)` sweep.

No discrepancy with the existing certificate.

## 5. Exact structured count via subgroup-lattice Möbius

The per-`d` floor of §2 is a lower bound from one subgroup. The *exact* number
of structured (quotient-periodic) divisors --- those that are `K_d`-coset-union
for at least one active order `d > sigma` --- follows from a lattice identity.

**Lemma (lcm closure).** For `d, e \mid n`, a set `A <= H` is simultaneously a
`K_d`- and `K_e`-coset-union iff it is a `K_{lcm(d,e)}`-coset-union.

*Proof.* `K_d` and `K_e` are the order-`d`, order-`e` subgroups of the cyclic
group `H`, so `K_d, K_e <= K_{lcm(d,e)}` and `K_d K_e = K_{lcm(d,e)}` (in an
abelian group `|K_d K_e| = |K_d||K_e|/|K_d \cap K_e| = de/\gcd(d,e) = lcm(d,e)`,
and `K_d K_e` is a subgroup of the cyclic group `H`, hence the unique one of that
order). If `A K_d = A` and `A K_e = A` then `A K_{lcm} = A (K_d K_e) = A`;
conversely `A K_{lcm} = A` forces closure under the subgroups `K_d, K_e`. ∎

Write `CU_d` for the set of `K_d`-coset-union degree-`m` divisors, so
`|CU_d| = binom(n/d, m/d)` (§2) and, by the Lemma,
`CU_d \cap CU_e = CU_{lcm(d,e)}`. Let `S = \{ d \mid \gcd(n,m) : d > sigma \}` be
the active orders.

**Theorem (exact quotient-core count).**
```text
#{structured divisors}  =  | union_{d in S} CU_d |
                        =  sum_{∅ != T ⊆ S} (-1)^{|T|+1} binom(n/L_T, m/L_T),
                           where L_T = lcm(T).
```
Consequently the *aperiodic* divisor count is exactly
`binom(n,m) - #{structured divisors}`, and `conj:prefix-local` predicts the
maximal aperiodic prefix fiber to be `binom(n,s)/q^sigma + O(n^B)`.

*Proof.* Inclusion-exclusion on the union, with
`CU_{d_1} \cap ... \cap CU_{d_t} = CU_{lcm(d_1,...,d_t)}` by iterating the Lemma,
and `|CU_e| = binom(n/e, m/e)` from §2 (`e = L_T \mid \gcd(n,m)`, so `e \mid m`
and `e \mid n`). ∎

**Corollary (dyadic collapse).** If `n = 2^{m_0}` then `\gcd(n,m)` is a power of
two, so `S` is a chain under divisibility with least element `d_* = ` smallest
power of two `> sigma` dividing `\gcd(n,m)`. Every `CU_d` (`d \in S`) satisfies
`CU_d \subseteq CU_{d_*}` (as `d_* \mid d`), so the union collapses:
```text
#{structured divisors} = binom(n/d_*, m/d_*)        (n dyadic).
```
This is the exact field-independent quotient-core mass at dyadic rates --- the
prize regime --- and it vanishes precisely when `\gcd(n, k+sigma) <= sigma`.

Both the inclusion-exclusion total and the dyadic collapse are verified by
`verify_l1_prefix_divisor_count.py` (fields `structured_count_direct`,
`structured_count_incl_excl`, `dyadic_collapse_ok`) against direct enumeration
across the 35-case sweep. For `F_17, n=16`: at `k=4, sigma=4` the structured
count is exactly `2 = binom(2,1)` (`d_*=8`), the `12868` aperiodic divisors have
maximal aperiodic fiber `2`, and the random baseline `binom(16,8)/17^4 = 0.154`
--- i.e. the aperiodic remainder is already at the predicted scale.

## 6. Dilation equivariance and the period stabilizer

The group `H` acts on divisors by dilation `h \cdot A = \{ha : a \in A\}`
(`h \in H`), which permutes the degree-`m` divisors of `X^n-1`. Since a
`j`-subset product scales by `h^j`,
```text
e_j(h \cdot A) = h^j e_j(A),    so    L_{h\cdot A}(X) = h^m L_A(X/h).
```
Hence the top-`sigma` key transforms by the **star-action**
```text
h \star (c_1, ..., c_sigma) = (h c_1, h^2 c_2, ..., h^sigma c_sigma).
```

**Lemma (dilation equivariance).** `Phi_sigma(h \cdot A) = h \star Phi_sigma(A)`.
Dilation by `h` is therefore a bijection
`Phi_sigma^{-1}(c) -> Phi_sigma^{-1}(h \star c)`, so the prefix-fiber size is
constant on each `H`-orbit of the star-action on `F_q^sigma`:
```text
|Phi_sigma^{-1}(c)| = |Phi_sigma^{-1}(h \star c)|   for all h in H.
```
*Proof.* `e_j(h\cdot A) = sum_{T in binom(A,j)} prod_{a in T} (ha)
= h^j e_j(A)`; the key is `((-1)^{j+1} e_{j+1}(A))_j`, which scales coordinatewise
by `h^{j+1}`. Dilation is invertible, giving the bijection. ∎

**Consequence (worst-case reduction).** The worst-case prefix fiber is attained
on a set of star-orbit representatives:
```text
max_c |Phi_sigma^{-1}(c)| = max over star-orbit representatives,
```
cutting the worst-case search by up to a factor `n`, and the number of distinct
fiber sizes is at most the number of star-orbits.

**Proposition (period = stabilizer).** For a divisor `A`, the dilation
stabilizer `Stab_H(A) = \{h in H : h \cdot A = A\}` is the unique subgroup
`K_d <= H` of largest order `d` for which `A` is a `K_d`-coset-union. Writing
`per(A) := |Stab_H(A)|`,
```text
A is quotient-periodic (coset-union for some active d > sigma)
   <=>  per(A) > sigma.
```
*Proof.* `Stab_H(A)` is a subgroup of the cyclic group `H`, hence equals `K_d`
for `d = per(A)`. `h \cdot A = A` for all `h in K_d` says exactly that `A` is a
union of `K_d`-cosets; maximality of `d` is maximality of the stabilizer. ∎

This unifies the symmetry with §2--§5: the structured (quotient-core) mass of §5
is *precisely* the divisors with super-`sigma` dilation stabilizer, and the
aperiodic remainder is `\{A : per(A) <= sigma\}` --- divisors with small
stabilizer, hence dilation orbits of size `n/per(A) >= n/sigma`. So the aperiodic
family is forced to spread into large dilation orbits, a structural handle the
purely pairwise (Johnson) bound does not see. All three statements are verified
by the scanner (`dilation_equivariant`, `stab_equals_period`,
`fiber_const_on_dilation_orbits`) across the 35-case sweep, and they explain the
dilation-orbit structure of the `F_17` collisions reported in
`l1_aperiodic_prefix_collision.md` (its three "dilation orbits" are exactly
star-orbits under this action).

## 7. Prefix-space localization of the quotient core

The star-action of §6 has stabilizers. For a prefix `c`, set
`H_c = Stab_star(c) = \{h in H : h \star c = c\}`. Since `h \star c = c` means
`h^j c_j = c_j` for each `j`, i.e. `h^j = 1` whenever `c_j != 0`,
```text
H_c = K_{g_c},     g_c = gcd(n, \{ j : c_j != 0 \})      (g_c = n if c = 0).
```
By §6, `H_c` acts on the fiber `Phi_sigma^{-1}(c)` by dilation.

**Theorem (the quotient core lives only in symmetric prefixes).** For every
divisor `A in Phi_sigma^{-1}(c)`,
```text
Stab_H(A) ⊆ H_c,    equivalently    per(A) \mid g_c.
```
Consequently:

(i) **Generic fibers are purely aperiodic.** If `g_c = 1` --- in particular
whenever `c_1 != 0` --- then `per(A) = 1` for every `A` in the fiber: the fiber
contains no quotient-periodic divisor at all.

(ii) **Period-`d` mass sits in a thin prefix slice.** A divisor of period
`d` (`K_d`-coset-union) occurs only in fibers with `d \mid g_c`, i.e. with
`c_j = 0` for every index `j` not divisible by `d`. For dyadic `n` and `d=2`
this means all odd-index prefix coordinates vanish --- a fraction
`q^{-\lceil sigma/2 \rceil}` of prefix space.

(iii) **Orbit decomposition.** The `K_{g_c}`-orbit of `A` inside the fiber has
size `g_c / \gcd(g_c, per(A))`; in particular the number of fully aperiodic
(`per = 1`) divisors in any fiber is divisible by `g_c`.

*Proof.* If `h in Stab_H(A)` then `hA = A`, so by the §6 Lemma
`c = Phi_sigma(A) = Phi_sigma(hA) = h \star c`, i.e. `h in H_c`. Thus
`K_{per(A)} = Stab_H(A) ⊆ K_{g_c} = H_c`, giving `per(A) \mid g_c`. (i) is the
case `g_c = 1`. (ii): `per(A) = d \mid g_c = \gcd(n, \{j : c_j != 0\})` forces
`d \mid j` for every `j` with `c_j != 0`, i.e. `c_j = 0` when `d \nmid j`.
(iii): `Stab_{H_c}(A) = H_c \cap Stab_H(A) = K_{\gcd(g_c, per(A))}`, so
orbit-stabilizer gives the orbit size; for `per(A) = 1` each orbit has size
`g_c`. ∎

**Significance.** Together with §5 (quotient core localized in *divisor* space as
coset-unions) this pins the quotient core in *prefix* space as well: it can
inflate only the vanishing-fraction slice of *symmetric* prefixes
(`g_c > 1`). Over the generic prefix (`c_1 != 0`) the fiber is a purely aperiodic
list, so `conj:prefix-local`'s prediction `binom(n,s)/q^sigma + O(n^B)` must hold
there with **no** quotient correction --- isolating the remaining open step (the
aperiodic upper bound) to exactly the generic, quotient-free fibers. All three
parts are verified by the scanner (`per_divides_gc`, `gc1_fibers_all_aperiodic`,
`prefix_orbit_size_ok`) across the 35-case sweep.

## 8. Non-enumerative counter and the first sub-Johnson evidence

`F_17, n=16` cannot host the regime that matters: entropy-cleared *and*
sub-Johnson cannot coexist at `n=16` (Johnson needs `a^2 > n(k-1)`, which at
fixed rate forces `a` near `n`). To probe further we count without enumerating
the `binom(n,m)` divisors.

**DP counter.** Process the elements of `H` one at a time, carrying the state
`(chosen size, e_1, ..., e_eff mod q)` with `eff = min(sigma, m)`, using the
elementary-symmetric recurrence `e'_i = e_i + h e_{i-1}` on inclusion. The
prefix-fiber histogram is read off at `size = m`. State space is
`(m+1) q^{eff}`, so for small `sigma` this reaches `n` far beyond brute force.
Verified (`--self-check`) to reproduce the brute-force size distribution at
`n=16` and to sum to `binom(n,m)`; the closed-form structured count of §5 is
checked against the enumerated one across the 35-case sweep.

**First sub-Johnson data point.** Over the Fermat prime `F_257` (which carries
all dyadic `n <= 256`), take `n=32, k=2, sigma=2` (`rho=1/16`). Here `a=4`, so
`a^2 = 16 < n(k-1) = 32` (**sub-Johnson**, where the Johnson anchor is silent),
while the entropy margin is `+0.88` bits (**cleared**):

| field | n | k | sigma | entropy (bits) | Johnson? | global max fiber | quotient floor | max aperiodic (g_c=1) | random baseline |
|---|---|---|---|---:|---|---:|---:|---:|---:|
| F_257 | 32 | 2 | 2 | +0.88 | sub-Johnson | 8 | 8 = binom(8,7) | **5** | 0.54 |
| F_97  | 32 | 8 | 2 | -12.74 | --- | 7344 | 0 | 7190 | 6856 |

Reading: in the cleared, sub-Johnson row the global maximum fiber is exactly the
**quotient-core floor** `binom(n/4, m/4) = binom(8,7) = 8` (pure period-4
coset-unions, §5/§7), and once the quotient core is removed the largest
**aperiodic** fiber is only `5` --- polynomially small, near the random baseline,
in a regime where Johnson gives nothing. This is the first direct evidence that
`conj:prefix-local` holds beyond the Johnson radius with the quotient core as the
*sole* source of large fibers. The second row is the control: with the entropy
margin negative, fibers sit at the random scale `binom(n,m)/q^sigma`.

**Honest reach.** The DP scales in `q^{sigma}`, so it cannot reach the asymptotic
target `sigma = Theta(n/log n)`; that regime stays out of all exact computation
and requires the analytic aperiodic bound. The DP's role is to validate the
structural theory (§2--§7) at parameters brute force cannot touch and to confirm
the quotient-core/aperiodic split survives into the sub-Johnson window.

## 9. Lift to arbitrary words: dilation symmetry and the folding source

§§2--8 treat the monomial-prefix fiber, which `prop:monomial-fiber` identifies
with the list exactly. For an *arbitrary* received word `U : H -> F_q` the honest
object is `ImgFib_U(s) = \{ P in F_{<k}[X] : |\{x : U(x)=P(x)\}| >= s \}`
(`l1_arbitrary_fiber_repair.md`) --- the list at radius `1 - s/n`. The symmetry
and quotient-core structure transfer.

**Theorem (dilation symmetry of the list).** For `h in H` define
`U^h(x) = U(h^{-1}x)` and `P^h(x) = P(h^{-1}x)`. Then `deg P^h = deg P`,
`A_{P^h}(U^h) = h \cdot A_P(U)`, and `P |-> P^h` is a bijection
`ImgFib_U(s) -> ImgFib_{U^h}(s)`. Hence
```text
|ImgFib_{U^h}(s)| = |ImgFib_U(s)|,
```
so the worst-case list `Lst(RS[F_q,H,k], 1-s/n)` is attained on dilation-orbit
representatives of received words (search reduced by up to a factor `n`). If
`h in Stab_H(U)` the map permutes `ImgFib_U(s)`, so the number of fully aperiodic
codewords in the list is divisible by `per(U) := |Stab_H(U)|`.

*Proof.* `P^h(h x) = P(x)`, so `U^h(hx) = U(x) = P(x) = P^h(hx)` exactly on
`h \cdot A_P(U)`; dilation by `h` is invertible on `F_{<k}`. ∎

**Theorem (folding is the arbitrary-word quotient-core source).** Suppose
`U = V(X^d)` with `d \mid n`, `d \mid k`, `d \mid s`. Then
```text
W |-> W(X^d)   injects   ImgFib_V(s/d)  over RS[F_q, mu_{n/d}, k/d]
                          into ImgFib_U(s)  over RS[F_q, mu_n, k].
```
Thus a `d`-periodic received word inherits the entire folded list.

*Proof.* `deg W(X^d) = d \deg W < d (k/d) = k`, so `P = W(X^d)` is a codeword of
`RS[F_q, H, k]`. The `d`-power map `x \mapsto x^d` is `d`-to-`1` from `mu_n` onto
`mu_{n/d}`, and `P(x) = U(x) \iff W(x^d) = V(x^d)`. So each agreement point
`y in mu_{n/d}` of `(W,V)` lifts to `d` agreement points of `(P,U)`, giving
`|A_P(U)| = d\,|A_W(V)| >= d (s/d) = s`. Injectivity of `W \mapsto W(X^d)` is
clear. ∎

**Significance.** This is the arbitrary-word analogue of §§5--7: the
field-independent quotient-core floor on the list comes from *periodic* received
words `U = V(X^d)` inheriting folded lists (the §5 coset-union floor was the
prefix shadow of this), the dilation symmetry organizes the worst case (§6), and
the open target is again the *aperiodic* (trivial `Stab_H(U)`) regime. One
caveat distinguishes it from the prefix case: arbitrary listed codewords need not
be `d`-periodic, so the list can exceed the folded floor --- the folded copy is a
lower bound, not the whole list. Verified by
`verify_l1_arbitrary_word_lift.py`: dilation list-size invariance at
`F_17, n=16, k=6, s=8`, and the folding lift for `d = 2, 4`.

## 10. Fourier reduction to subgroup exponential sums

This section recasts the *open* aperiodic bound as an exponential-sum problem. It
proves an exact identity and a conditional bound, and states honestly where the
barrier of `sec:pairwise` reappears. (List/locator side; the exponential sums
here are over the base code and are a different object from the M1 residue-line
Weil sums.)

**Power-sum coordinates.** For `p > sigma`, Newton's identities make
`(e_1,...,e_sigma)` and the power sums `(p_1,...,p_sigma)`,
`p_j(A) = sum_{a in A} a^j`, a polynomial bijection; the fiber count is the same
in either coordinate. Power sums are *additive over* `A`, which is the whole
point: with `g_r(w) = sum_{j=1}^sigma r_j w^j`,
```text
<r, p(A)> = sum_{a in A} g_r(a).
```

**Exact Fourier identity (PROVED).** With `e_p(x) = exp(2 pi i x / p)`,
```text
|{A : |A|=m, p(A)=c}|
   = (1/p^sigma) sum_{r in F_p^sigma} e_p(-<r,c>) S(r),
S(r) := sum_{|A|=m} e_p(<r,p(A)>)
      = sum_{|A|=m} prod_{a in A} e_p(g_r(a))
      = e_m( { e_p(g_r(a)) : a in mu_n } ),
```
with main term `S(0) = binom(n,m)`, so the fiber equals
`binom(n,m)/p^sigma` plus `(1/p^sigma) sum_{r != 0} e_p(-<r,c>) S(r)`. The factor
`binom(n,m) = binom(n,s)` is exactly the `conj:prefix-local` main term.

**Weil-sum structure (PROVED).** The values `w_a = e_p(g_r(a))` have power sums
```text
P_l(r) = sum_{a in mu_n} w_a^l = sum_{a in mu_n} e_p(l g_r(a)) = T(l r),
```
the **subgroup exponential (Weil) sums** of the degree-`<= sigma` polynomials
`l g_r` over `mu_n`. By Newton's identities `S(r) = e_m` is a fixed polynomial in
`{T(l r) : 1 <= l <= m}`. So the entire prefix count is governed by subgroup
exponential sums.

**Conditional bound (PROVED, conditional).** If `|T(l r)| <= tau` for
`1 <= l <= m`, the Newton recurrence `m e_m = sum_l (-1)^{l-1} P_l e_{m-l}` gives
```text
|S(r)| <= prod_{j=1}^m (1 + tau/j)   (<= (1+m)^tau).
```
Hence `|fiber(c) - binom(n,m)/p^sigma| <= max_{r != 0} prod_j (1 + tau_r/j)`.

**Honest assessment of the barrier.** A worst-case subgroup sum has
`tau ~ sqrt(n)` (or larger), and then `(1+m)^tau` is super-polynomial: the
worst-`r` bound does *not* reach `n^B`. The saving must come from *averaging*
`|S(r)|` over `r`, but `sum_r |S(r)|^2 = p^sigma sum_c |fiber(c)|^2` (Parseval) is
exactly the second moment --- the `sec:pairwise` wall in Fourier dress. So this
reduction does **not** resolve `conj:prefix-local`; its value is to pin the open
problem to a precise, standard object (uniform-in-`l` subgroup exponential-sum
control) and to expose the structure of the large coefficients.

**The promising link to §7.** `T(l r) = sum_{a in mu_n} e_p(l g_r(a))` is large
exactly when `g_r` is close to constant on cosets of some `K_d` --- i.e. when `r`
is *structured* (supported on indices with a common factor `d`). That is the same
`g_c`-localization that §7 proved on the prefix side: the large Fourier
coefficients come from the quotient-core prefixes. This suggests the workable
split --- bound the structured `r` by the §5/§7 quotient-core count, and the
generic `r` (full-degree `g_r`) by a Weil/Deligne subgroup-sum estimate --- as
the concrete route past the barrier, recorded here as the next target.

**Status.** Exact identity and Weil-sum structure: PROVED. Newton bound:
PROVED-conditional. `conj:prefix-local`: still OPEN; reduced, not resolved.
Verified by `verify_l1_fourier_reduction.py` over `F_17, n=16` (`sigma=2,3`):
`S(r)` enumeration equals the product formula, the Fourier inversion reconstructs
the brute histogram to `< 1e-12`, and the conditional Newton bound holds for
every `r`.

## 11. The structured/generic split: necessary but not sufficient

§10 proposed splitting the Fourier sum into *structured* and *generic* `r`. This
section proves the classification and measures the split --- and finds, honestly,
that the split alone does **not** give the bound.

**Classification (PROVED).** Call `r` *structured at level `e`* if
`e = gcd\{j : r_j != 0\} > 1`; then `g_r(w) = h(w^e)` is a polynomial in `w^e`,
the `e`-power map folds `mu_n` onto `mu_{n/e}` (`e`-to-`1`), and
```text
{ e_p(g_r(a)) : a in mu_n } = e copies of { e_p(h(y)) : y in mu_{n/e} },
```
so `S(r)` is the elementary symmetric of an `e`-fold repeated multiset --- the
folded object of §9, and the source of the large Weil sums `|T(l r)|` (a factor
`e` from the fold). The structured set is `union_{prime d <= sigma} L_d` with
`L_d = \{ r : r_j = 0 unless d | j \}`, `|L_d| = p^{floor(sigma/d)}`, so the
structured `r` are a `p^{-ceil(sigma/2)}` fraction of `F_p^sigma` --- the same
thin slice as the §7 `g_c`-localization. Generic `r` (`e = 1`) have `g_r` of full
degree and, by Weil over the (generated) field, small sums `|T(l r)| <= sigma
sqrt(p)`.

**Measurement (EXPERIMENTAL, `F_17, n=16`,
`verify_l1_fourier_reduction.py`).**

| case | struct `r` (frac) | gen `r` | L1 mass struct | L1 mass gen | max gen `|T|` vs `sigma√p` | actual max dev |
|---|---|---|---|---|---|---|
| `k=8, sigma=2` | 16 (0.056) | 272 | 3.54 | **15.82** | 5.1 vs 8.2 | 4.29 |
| `k=4, sigma=3` | 32 (0.0065) | 4880 | 0.26 | **27.77** | 8.3 vs 12.4 | 2.67 |

Three honest readings:
1. Generic Weil sums are indeed small (`max|T| <= sigma sqrt(p)`), confirming the
   Weil heuristic for the generic part.
2. **The structured `r` are not the L1 bottleneck.** They carry the largest
   *individual* coefficients (`max|S|` struct `124` vs generic `36` at
   `sigma=2`), but there are too few of them; the `L1` error mass
   `sum_r |S(r)| / p^sigma` is dominated by the *generic bulk*.
3. **The `L1` bound is far from the truth.** It overestimates the actual maximal
   fiber deviation by `4-10x` (e.g. `19` vs `4.3`). The gap is exactly the phase
   cancellation in `sum_r e_p(-<r,c>) S(r)` that the triangle inequality discards.

**Conclusion (route refinement, not a resolution).** The structured/generic split
is *necessary* --- it isolates the few genuinely large coefficients as the §5/§7
quotient core --- but it is *not sufficient*: bounding the generic bulk by `|S(r)|`
termwise (even with sharp Weil input) loses to the trivial count, because the
crude Newton bound from `tau ~ sqrt(n)` is loose and the generic coefficients are
many. A polynomial list bound must exploit the **phase cancellation** across `r`,
which is the second-moment / `sec:pairwise` barrier of Paper B in Fourier form.
So this records, with explicit constants, *why* the natural split does not by
itself crack `conj:prefix-local`, and pins the essential difficulty to cancellation
rather than to the size of any individual exponential sum.

## Ledger impact

- **Quotient (worsens, now explicit):** gives an exact, field-independent
  lower-bound floor `binom(n/d,m/d)` on the worst-case prefix list, on the
  locator side. Quantifies the `Quot_{sigma,c}` term of `conj:prefix-local`.
- **Entropy (clarified):** the floor cannot be paid by `q_gen`; entropy controls
  only the aperiodic remainder.
- **Dimension dithering (improves):** identifies the exact dither target
  `gcd(n, k+sigma) <= sigma` that empties the coset-union floor.

## Constants

Floor `= binom(n/d, m/d)` for each `d \mid gcd(n,k+sigma)`, `d > sigma`.
The dominant floor is at the smallest such `d`. For dyadic `n=2^{m_0}` the active
`d` are powers of two; the largest dither-resistant floor at fixed `(rho,sigma)`
is `binom(n/d*, m/d*)` with `d* = ` smallest power of two `> sigma` dividing
`gcd(n,s)`.

## Reproducibility

```bash
python3 experimental/verify_l1_prefix_divisor_count.py --self-check
python3 experimental/verify_l1_prefix_divisor_count.py --p 17 --n 16 --k 4 --sigma 4
python3 experimental/verify_l1_prefix_divisor_count.py --p 17 --n 16 --k 4 --sigma 4 --format json
# non-enumerative DP, beyond brute force (§8):
python3 experimental/verify_l1_prefix_divisor_count.py --dp-summary --p 257 --n 32 --k 2 --sigma 2
```

## What to do next

1. **Aperiodic remainder bound.** Prove `binom(n,s)/q^sigma + O(n^B)` for the
   *aperiodic* count beyond the Johnson anchor. §10 reduces this to subgroup
   exponential sums; the concrete route is to split the Fourier sum into
   *structured* `r` (bounded by the §5/§7 quotient-core count) and *generic*
   `r` (full-degree `g_r`, bounded by a Weil/Deligne subgroup-sum estimate),
   avoiding the worst-case `(1+m)^tau` blow-up.
2. **Scale up.** DONE (§8): a DP counter `(size, e_1..e_eff)` reaches `n=32` over
   `F_257`/`F_97` (and `n=64` for `sigma <= 2`), giving the first sub-Johnson,
   entropy-cleared data point. Extend with a coset-folded DP (quotient `Y=X^d`)
   to push `sigma` higher, or a character-sum evaluation for the per-`c` count.
3. **Inclusion-exclusion over orders.** DONE (§5): exact structured count via
   subgroup-lattice Möbius, with the dyadic collapse `binom(n/d_*, m/d_*)`.
4. **Lift to arbitrary words.** DONE (§9): dilation symmetry of `ImgFib_U` and
   the folding source `W |-> W(X^d)` for periodic `U=V(X^d)`. Remaining: bound
   the *aperiodic* (trivial-stabilizer) arbitrary-word list above the reserve.
5. **Aperiodic second moment.** The scan shows the aperiodic remainder sits at
   the random scale `binom(n,s)/q^sigma`; target a worst-case second-moment /
   Plotkin bound on the *aperiodic* sub-family that beats the generic Johnson
   anchor by using that coset-union mass has been removed.
6. **Exploit the dilation symmetry (§6, §7).** DONE in part: §7 localizes the
   quotient core to symmetric prefixes (`g_c > 1`), so the remaining open step
   is now isolated to the *generic, purely aperiodic* fiber (`c_1 != 0`). Target:
   a `binom(n,s)/q^sigma + O(n^B)` upper bound there. The orbit-divisibility of
   §7(iii) and the large-orbit structure of §6 are the non-pairwise handles to
   try first against the `sec:pairwise` barrier.
