# X1: explicit non-B-rational MCA-bad lines for Paper D `prob:explicit`

- **Status:** PROVED (density bound, composing `lem:fiber` + deep-point identity +
  averaging) / AUDIT. Construction is an explicit family with a rigorous
  generic-`alpha` density; not a single brute-certified line (infeasible over `F_{p^6}`).
- **Agent/model:** Claude Opus 4.8 (L2/X1 lane, branch `allen/l2-x1-interleaved-mca`).
- **Date:** 2026-06-24.
- **Scope:** Paper D (`tex/cs25_cap_v12.tex`) `cor:Fvalued`, `prob:explicit`,
  `cor:deployed`, `thm:main`/`cor:grand` (universal cap), `lem:fiber`; the deep-point bridge of `notes/x1` §1 /
  `notes/f1/f1_deep_point_list_to_ca_mca.md`. Does not edit Papers A--D.

## The open problem

`cor:Fvalued` proves that at the deployed parameters the MCA-bad lines certifying
`cor:deployed` are **necessarily not `B`-rational** -- "fiber-borne and currently
non-constructive." `prob:explicit` then asks to **exhibit** such lines, naming
"residue-line normal forms with denominator `E in F[X]` not defined over `B`" as
the natural candidate.

## The explicit construction

Take Paper D's own heavy word (`lem:fiber`(ii)),
`u_z = (x^{k+2a_q} + z\,x^{k+a_q})_{x in D}`, whose `C_+=RS[F,D,k+1]` list at radius
`1-rho-2/N` has size `L >= binom(N,ell_2)/|B|`. Form the **simple-pole deep-point
line**
```text
f(x) = u_z(x)/(x-alpha),    g(x) = -1/(x-alpha),    alpha a deep point in F\D,
```
with denominator `E = X-alpha in F[X] \ B[X]` -- exactly the named candidate. By
the deep-point identity (`notes/x1` §1), its support-wise MCA-bad slopes for
`C=RS[F,D,k]` at agreement `k+2a_q` are exactly the deep image
`{P(alpha) : P in the list}`, of size `M`.

**When are the slopes genuinely `F`-valued?** The heavy word is `X^{a_q}`-periodic,
so the listed codewords are functions of `X^{a_q}` and `P(alpha)=G(alpha^{a_q})`.
Hence the bad slopes are `F`-valued **iff `alpha^{a_q} notin B`** -- a finer,
quotient-periodic confinement that *extends* `lem:confine` (which confines lines
with `B`-valued words; here the words are `F`-valued but the slopes still confine
when `alpha^{a_q} in B`). The deep-point bridge thus **unifies** `lem:confine`
(`alpha^{a_q} in B` -> slopes in `B`) and `cor:Fvalued` (`alpha^{a_q} notin B` ->
genuinely `F`-valued). [Validated over `F_{17^2}`:
`verify_x1_prob_explicit_mechanism.py` confirms the identity and the exact
characterization `F`-valued <=> `alpha^{a_q} notin B` over all deep points.]

## Density at the deployed parameters

`cor:deployed`: `p=2^31-2^24+1`, `F=F_{p^6}` (`q~2^185.93`), `n=2^21`, `k=2^20`,
`rho=1/2`, gap `2^-7`. Then `N=256`, `a_q=2^13`, `ell_2=130`, and
`L = binom(256,130)/p ~ 2^220.6`. The averaging expansion (Lemma 2.1) gives, with
`|Omega|=q-n ~ 2^185.93`,
```text
best alpha:        M >= L/(1 + k(L-1)/|Omega|)   ~ |Omega|/k ~ 2^165.93,  density ~ 2^-20,
>= half of alpha:  M >= L/(1 + 2k(L-1)/|Omega|)               ~ 2^164.93,  density ~ 2^-21,
```
the second by Markov on the collision count (`sum_alpha C_alpha <= k binom(L,2)`).
Both clear the `prob:explicit` target `2^-22`. Since `v_2(q-1)=25 >= 13`, a
generator `alpha` of `F_{p^6}^*` has `alpha^{a_q}` of full degree `6`, so a
generic (in fact `>= 1/2`) set of deep points gives genuinely `F`-valued slopes
filling a `2^-21` fraction of `F`. [`verify_x1_prob_explicit_deployed.py`.]

## Also covers the CA (`eca`) half, and the periodicity is harmless

- **CA as well as MCA.** The deep-point identity is `Bad_CA = Bad_MCA =
  Deep_alpha(U,a)` (Thm 1.1), so the *same* explicit line gives the no-loss
  `eca` lower bound too, on `cor:deployed`'s CS-admissible subinterval
  `[1/2-2^-7, 1/2-2^-21)` (via the persistence statement of Thm 1.1). So the
  construction covers the *full* `cor:deployed` claim, not just the `emca` half.
- **Periodicity is harmless.** The heavy word is `X^{a_q}`-periodic, so codewords
  are `P=G(X^{a_q})` with `deg G <= m=k/a_q=128`, and slopes are `G(alpha^{a_q})`.
  The averaging over `beta=alpha^{a_q}` (range size `~(q-1)/a_q ~ 2^173`) uses
  `deg G <= m`: `m/|B_set| = 2^7/2^173 = 2^-166 = k/|Omega|`, giving the same
  `M >= 2^165.93`. The `1/k` density is unchanged; the slopes fill `F_{p^6}`
  exactly when `alpha^{a_q}` has full degree 6 (generator `alpha`, as above).

## Generalization: the explicit line is the constructive form of the *whole* cap

The cor:deployed instance is not special. `thm:main` (universal cap) has
hypothesis (eq:hyp) `binom(N,rho N+2) >= |B|(q/k+1)`, i.e. exactly
`L >= q/k + 1` -- **the averaging-saturation condition**. Its conclusion is
`emca(C,delta) > (1/(2k))(1-n/q)` on `[1-rho-2/N, 1-rho)`. The explicit
deep-point line recovers this **exactly**:

- at the saturation boundary `L ~ q/k`, the best-`alpha` deep-image density is
  `(q/k)/(1+1)/q = 1/(2k)` -- precisely `thm:main`'s bound; for `L >> q/k`
  (e.g. cor:deployed) it improves to `1/k`. So `dens_best >= (1/(2k))(1-n/q)`
  wherever (eq:hyp) holds.
- `verify_x1_prob_explicit_universal.py` checks four cap-regime points
  (cor:deployed `e=6`; an `e=2`, `rho=1/4` extension; a subgroup `B=F`,
  `q~2^64`; a large `k=2^40`, `e=2` point): all satisfy (eq:hyp), all have
  `dens_best >= thm:main bound`, and all clear `2^-128` (since `1/(2k) >= 2^-41`
  for `k <= 2^40`).

So the deep-point bridge is the **explicit/constructive form of `thm:main`**:
same hypothesis (saturation = eq:hyp), same bound `(1/(2k))(1-n/q)`, replacing
the non-constructive CS25 augmented-code conversion by an explicit line. This
makes the **entire universal cap constructive**, not just `cor:deployed`.

**Non-`B`-rational regime (the `prob:explicit`/`cor:Fvalued` part).** The slopes
are `G(alpha^{a_q})`, so they are genuinely `F`-valued exactly when `alpha^{a_q}`
has full degree `e=[F:B]` -- which for a generator `alpha` needs the 2-power
condition `v_2(q-1) >= v_2(a_q)` (and `e>=2`). The two extension points above
satisfy it (`v_2=25 >= 13`); the subgroup case (`e=1`) is, of course, not
non-`B`-rational (there is nothing to confine); and the large-`k` `e=2` point
*fails* it (`a_q=2^31`, `v_2(q-1)=25<31`), so there the line recovers the cap
bound but its slopes may confine to `B`. Thus: the explicit construction gives
`thm:main`'s bound throughout the cap, and is additionally a `prob:explicit`-type
non-`B`-rational witness in the extension regime with `v_2(q-1) >= v_2(a_q)`.

## What this resolves, honestly

- **Constructive vs. existence.** This is the **explicit, `B`-free counterpart of
  `cor:deployed`'s `1/k` bound**: Paper D obtains `emca ~ 1/k` non-constructively
  through the CS25 augmented-code conversion (`thm:A`, used contrapositively);
  the deep-point line obtains the *same* `1/k` density through an **explicit
  line**, with the `1/k` arising as the averaging saturation `M ~ |Omega|/k`. No
  `eta`, no augmented code, no CS25 import.
- **`prob:explicit`.** This exhibits an explicit family `{(f,g)_alpha}` (heavy
  word explicit; `alpha` a generator with `alpha^{a_q} notin B`) in which a
  provable `>= 1/2` fraction have MCA-bad-slope density `>= 2^-21 > 2^-22`, all
  genuinely `F`-valued with denominator `X-alpha notin B[X]`. This is the
  residue-line normal form `prob:explicit` predicts, made explicit.
- **Caveat (scope).** The averaging gives the density for a positive fraction of
  `alpha`, not a single pinned `alpha` certified by direct computation (a brute
  density check over `F_{p^6}` is infeasible). So this is an explicit *family*
  with a proven generic-`alpha` density, which is the operative meaning of
  "exhibit explicit pairs" here -- a strong constructive advance on the stated
  problem, not a single machine-certified witness.

## Ledger impact

- **Paper D `prob:explicit` (advanced):** explicit non-`B`-rational lines with
  proven `> 2^-22` density at the deployed parameters.
- **`cor:Fvalued`/`lem:confine` (unified + refined):** both are the deep-point
  dichotomy `alpha^{a_q} in/notin B`; confinement is quotient-periodic.

## Reproducibility
```bash
python3 experimental/scripts/verify_x1_prob_explicit_mechanism.py   # mechanism (F_{17^2})
python3 experimental/scripts/verify_x1_prob_explicit_deployed.py    # deployed-scale density
```
