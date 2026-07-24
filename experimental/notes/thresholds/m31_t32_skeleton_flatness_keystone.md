---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: "On the pinned c=2048, (u,v)=(0,1) quotient profile, fix the canonical remainder obtained by deleting every complete intact T32 fiber from a 479-subset. For every fixed remainder and every depth-32 locator-prefix target, at most 3432 supports realize that target. This cap is sharp. Consequently an average-sized fiber needs at least 1054 canonical remainders, while a fiber exceeding B*=16777215 needs at least 4889."
architecture: DIRECT_PINNED_C2048_U0_V1_QUOTIENT_PROFILE
partition_digest: "N/A; fixed support-level quotient profile, no first-match ledger atom assigned"
atom_or_cell: Q / PINNED_QUOTIENT_PREFIX_FIBER / T32_SKELETON
quantifier: "Uniform over every fixed canonical T32 remainder, every selector size compatible with a 479-subset, and every depth-32 prefix target in the pinned punctured 1022-point quotient domain."
projection_and_unit: "479-subsets per first-32 monic quotient-locator coefficient target; no received-word, explanation, codeword, ray, or slope projection."
claimed_bound: "fixed-remainder fiber <=3432; equality attained; average threshold 1054 remainders; budget-breaking threshold 4889 remainders; 4888 remainders contribute at most 16775616."
status: PROVED / COMPUTED / ROUTE_CUT / OPEN_GAP
impact: ROUTE_CUT / LOCAL_ONLY
falsifier: "A thirty-block selector sum fiber of size at least 3433; a missing signed selector relation; one compressed pattern incident to two certified nontrivial relations; a nontrivial collision fiber above 482; or a failure of the exact threshold arithmetic."
replay: "python3 experimental/scripts/verify_m31_t32_skeleton_flatness_keystone.py --check; python3 experimental/scripts/verify_m31_t32_skeleton_flatness_keystone.py --tamper-selftest; source provenance is recorded but steering files are not hard-pinned."
---

# M31 flatness keystone: a sharp complete-`T_32` skeleton cap

## Status

```text
fixed canonical T_32 remainder, depth-32 fiber cap = 3,432
cap sharp                                      = yes
nonzero signed selector relations              = 18
relations up to sign                           = 9
compressed nontrivial collision graph          = matching
largest nontrivial collision fiber              = 482
exact full-domain average ceiling               = 3,614,120
remainders required by an average-sized fiber   >= 1,054
remainders required to exceed B*=16,777,215     >= 4,889
uniform bound from at most 4,888 remainders     = 16,775,616
row ledger movement                             = 0
```

The packet proves the strongest exact max-versus-average statement reached here:
complete `T_32`-block freedom is fully classified and contributes at most
`3,432` supports to any one depth-32 target after the partial-block remainder is
fixed.  The missing maximum-fiber input is therefore not more freedom inside one
complete-block skeleton.  It is control of how many different partial-block
remainders can coalesce on the same prefix.

The active source labels are `def:primitive-q`, `def:q-row-atom`,
`prop:q-exact-target`, and `lem:newton-equivalence` in
`experimental/grande_finale.tex`.  The integrated packets
`m31_quotient_band_swap_census_t16_mixing.md` and
`m31_quotient_t16_mixing_floor.md` are cited for their existing `T_64` and
`T_16` witnesses; they are not regenerated here.

## 1. Pinned quotient domain and intact `T_32` blocks

Put

\[
 p=2^{31}-1=2,147,483,647.
\]

The quotient construction has `1,024` distinct labels.  Removing the two labels
with representatives `1` and `3` leaves the pinned domain `Q'` of size `1,022`.
The map

\[
 q\longmapsto \sigma(q)=T_{32}(2q)
\]

has exactly `32` fibers of size `32`.  The two punctures lie in different
fibers, hence exactly `30` fibers remain intact.

For an intact fiber with value `sigma`, its monic locator is

\[
 P_\sigma(Y)=2^{-63}\bigl(T_{32}(2Y)-\sigma\bigr)
            =F(Y)-\lambda_\sigma .
\tag{1.1}
\]

Thus all intact block locators have one common monic nonconstant part `F` and
differ only in the constant `lambda_sigma`.

The `30` intact sigma values consist of `14` opposite pairs
`{s_i,-s_i}` and two singleton values

\[
 u=9,803,698,\qquad v=1,263,730,590,
 \qquad u+v=1,273,534,288\pmod p.
\tag{1.2}
\]

The opposite pairs have minimum-representative pairs

```text
(5,59) (7,57) (9,55) (11,53) (13,51) (15,49) (17,47)
(19,45) (21,43) (23,41) (25,39) (27,37) (29,35) (31,33)
```

and the singleton fibers have minimum representatives `61` and `63`.
All of these field values, fibers, locator normalizations, and pairings are
reconstructed independently by the verifier.

## 2. Canonical remainder and the depth-32 selector equation

For a support `E` in `binom(Q',479)`, remove every complete intact `T_32`
fiber contained in `E`.  The points left behind form its **canonical `T_32`
remainder** `R`.  Once `R` is fixed, every support with that remainder has the
form

\[
 E=R\sqcup\bigsqcup_{\sigma\in S}\mathcal D_\sigma,
\tag{2.1}
\]

where `S` is a subset of the intact blocks disjoint from `R`.  Because every
block has size `32`, fixing `R` and the support size fixes `m=|S|`.

The locator is

\[
 V_E(Y)=V_R(Y)\prod_{\sigma\in S}(F(Y)-\lambda_\sigma).
\tag{2.2}
\]

For two selectors `S,T` of the same size, the `F^m` terms cancel.  The first
possibly different term is

\[
 -\biggl(\sum_{\sigma\in S}\lambda_\sigma
          -\sum_{\tau\in T}\lambda_\tau\biggr)
   V_R F^{m-1},
\tag{2.3}
\]

whose degree is `479-32=447`.  Every later term has degree at most
`479-64=415`.  Therefore the first `31` nonleading locator coefficients agree
automatically, and the thirty-second agrees exactly when

\[
 \sum_{\sigma\in S}\sigma
 =\sum_{\tau\in T}\sigma\pmod p.
\tag{2.4}
\]

This is an exact equivalence, not a moment estimate.  If only a subset of the
`30` intact blocks is available for a given remainder, its selector fiber is a
subset of the full thirty-block selector fiber, so a cap for all `30` blocks is
uniform for every remainder.

## 3. Exhaustive selector-relation atlas

For each opposite pair, encode a selector by

```text
-1 = choose the -s_i block only
 0 = choose neither block or both blocks
+1 = choose the +s_i block only.
```

The two singleton coordinates lie in `{0,1}`.  The difference of two compressed
selectors therefore lies in

\[
 [-2,2]^{14}\times[-1,1]^2.
\tag{3.1}
\]

The verifier splits the `14` pair coordinates into two groups of `7`, attaching
one singleton to each half.  Each half has exactly

\[
 5^7\cdot3=234,375
\tag{3.2}
\]

coefficient vectors.  Both half-sum maps into `F_p` are injective.  Their exact
meet-in-the-middle intersection consists of the zero vector and `18` nonzero
signed relations, or `9` relations up to sign.  The certificate prints all
`9` vectors and binds their digest.

For those `9` relations, the numbers of valid compressed-pattern realizations
are

```text
3,888; 1,944; 4,608; 6,912; 1,024; 46,656; 1,728; 192; 1,944.
```

Their sum is `68,896`.  The resulting `137,792` endpoints are all distinct, so
the nontrivial compressed collision graph is a matching: every compressed
selector pattern has either no nontrivial partner or exactly one.

The largest actual fixed-size selector fiber on a nontrivial matching edge is

\[
 20+462=482
\tag{3.3}
\]

at selector size `15`.  This is strictly below the largest multiplicity of a
single compressed pattern.

The Lean module kernel-checks the finite half-sum injectivity/intersection
summary, all `9` relation residues, the realization counts, endpoint
uniqueness, the collision maximum, and the deployed arithmetic.  It uses
`native_decide`, disclosed here and in `CORRESPONDENCE.md`.

## 4. Sharp fixed-remainder cap

For a compressed pattern with `z` zero opposite-pair coordinates, fixing the
selector size determines how many of those `z` pairs are chosen twice.  Its
multiplicity is therefore one binomial coefficient `binom(z,j)`, with
`0<=z<=14`.  Hence

\[
 \max_{0\le j\le z\le14}\binom zj
 =\binom{14}{7}=3,432.
\tag{4.1}
\]

The matching atlas shows that a nontrivial two-pattern collision contributes at
most `482`, so it cannot beat (4.1).  Therefore:

> **Theorem 4.1 (sharp complete-`T_32` skeleton cap; PROVED/COMPUTED).**  For
> every fixed canonical `T_32` remainder, every compatible selector size, and
> every depth-32 prefix target, at most `3,432` supports realize that target.

The cap is attained in exactly the following four selector-size/sum cases:

```text
size 14, sum 0
size 15, sum 9,803,698
size 15, sum 1,263,730,590
size 16, sum 1,273,534,288
```

In each case, choose both members of exactly `7` of the `14` opposite pairs and
neither member of the others, together with the indicated singleton subset.
There are `binom(14,7)=3,432` choices.  The size-`14`, sum-zero equality case is
exactly the complete-`T_64` family already integrated in the census packet, so
the new upper bound is sharp on the deployed quotient instance.

## 5. Maximum versus average

The full support count is

\[
 M=\binom{1,022}{479},
\]

and the exact depth-32 average arithmetic is

\[
 \left\lfloor\frac{M}{p^{32}}\right\rfloor=3,614,119,
 \qquad
 \left\lceil\frac{M}{p^{32}}\right\rceil=3,614,120.
\tag{5.1}
\]

If a target prefix receives `r` distinct canonical remainders, Theorem 4.1 gives

\[
 N(\eta)\le3,432\,r.
\tag{5.2}
\]

Thus an average-sized fiber requires at least `1,054` remainders, because

```text
3,432 * 1,053 = 3,613,896  (short by 224)
3,432 * 1,054 = 3,617,328.
```

A fiber exceeds the row budget `16,777,215` only if it has at least `4,889`
remainders, because

```text
3,432 * 4,888 = 16,775,616  (budget margin 1,599)
3,432 * 4,889 = 16,779,048  (budget excess 1,833).
```

Consequently the exact missing keystone for this pinned quotient profile can be
stated without asymptotic loss:

> A uniform bound of at most `4,888` canonical `T_32` remainders per depth-32
> target would imply the quotient-prefix maximum is at most `16,775,616`, hence
> below `B*=16,777,215`.

This is a conditional transport statement, not the missing remainder theorem.

## 6. Relation to the integrated floors

The integrated complete-`T_64` family contributes `3,432` supports to one
prefix.  The later integrated `T_16` packet supplies `8` further same-prefix
supports outside that family.  Hence the cited packets already imply the exact
arithmetic lower floor

\[
 N(\eta)\ge3,432+8=3,440,
\tag{6.1}
\]

and those supports occupy at least `2` canonical `T_32` remainders.  This packet
does not regenerate either witness and does not claim that `3,440` is the true
maximum.

## 7. Failed route and the input that would revive it

The attempted route was to prove the deployed maximum-vs-average inequality by
classifying complete Chebyshev block freedom alone.  The exact atlas shows why
that route fails: its sharp maximum is only `3,432`, already below the average
ceiling `3,614,120`.  Complete-block flatness therefore cannot control the
maximum without a theorem coupling different partial-block remainders.

The route would revive with either of the following equivalent-strength inputs
on this pinned profile:

- a direct uniform cap of `4,888` canonical remainders per prefix; or
- a weighted cross-remainder theorem whose total contribution is at most
  `16,777,215` after applying the sharp per-remainder cap.

Second moments, collision ledgers, and low moments are not used: they cannot
supply this pointwise cross-remainder control within the available multiplicative room.

## 8. Validation and limits

The deterministic verifier supports

```text
python3 experimental/scripts/verify_m31_t32_skeleton_flatness_keystone.py --check
python3 experimental/scripts/verify_m31_t32_skeleton_flatness_keystone.py --tamper-selftest
```

It independently reconstructs the quotient labels by exponentiation and by an
order recurrence; rebuilds all `T_32` fibers and locator templates; performs the
full meet-in-the-middle relation atlas; checks every collision endpoint and all
stated integer arithmetic; and hash-binds the packet.  Source provenance is
recorded, while `agents.md` and other steering files are deliberately not
hard-pinned.  Neither command requires `PR_BODY.md` or an agents-log fragment.

Explicit nonclaims:

- no upper bound on the number of canonical remainders in one prefix fiber;
- no maximum-fiber bound for all `479`-subsets beyond (5.2);
- no received-word realization, ordinary-list upper bound, or row closure;
- no first-match survival, projection, add-back, or deployed `U_Q` integer;
- no claim that the global maximum is close to the average.

# OPEN GAP
