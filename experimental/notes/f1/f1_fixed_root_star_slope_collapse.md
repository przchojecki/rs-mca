# F1 Fixed-Root Star Slope Collapse

Status: PROVED sharpening of an existing branch lemma / AUDIT verifier / NOT an
F1 theorem and NOT progress on F1.

This note sharpens one entry of the branch ledger in
[`f1_syndrome_pencil_normal_form.md`](f1_syndrome_pencil_normal_form.md),
namely the global monic-rank-one (fixed-root-star) branch of Corollaries 13, 15,
and 16. It does not advance F1: that branch had already been moved to the
polynomial, non-aperiodic side of the ledger. The open obstruction -- the
aperiodic non-global determinant-incidence branch -- is untouched.

## What the host note already proves

Keep the `t=2` set-up of the host note: `RS[F,D,k]`, `r=n-k`, slack `t=r-j`, a
size-`j` complement `T` with monic locator `L_T(X)=ell_0+...+ell_j X^j`
(`ell_j=1`), syndromes `u=Syn(f)`, `v=Syn(g)`, Hankel rows

```text
a_T = H_{2,j}(u) ell_T = (a_0,a_1),    b_T = H_{2,j}(v) ell_T = (b_0,b_1),
a_m = sum_{l=0}^{j} ell_l u_{m+l},     b_m = sum_{l=0}^{j} ell_l v_{m+l}.
```

By Corollary 4, `T` contributes a noncontained bad slope iff `b_T != 0` and
`a_0 b_1 - a_1 b_0 = 0`; the slope is then `z_T = -a_1/b_1 = -a_0/b_0`.

Corollary 15 isolates the **global monic-rank-one branch** (`rank A_z <= 1` for
every slope `z`): the first `j+1` syndrome entries are a fixed rational-normal
point,

```text
(u_0,...,u_j) = a (1,alpha,...,alpha^j),
(v_0,...,v_j) = b (1,alpha,...,alpha^j),
```

with `u_{j+1}, v_{j+1}` free. If `alpha in D` this is the fixed-root star
`T = {alpha} u U`, `|U| = j-1`. Corollaries 13/15/16 bound the number of
distinct noncontained bad slopes of this branch by

```text
1 + binom(|D|-1, j-1).
```

That bound assigns each of the `binom(|D|-1,j-1)` star landing complements its
own potential slope. For `j ~ |D|/2` it is **exponential in `|D|`**.

## The sharpening: the star carries a single slope

**Star-constancy lemma.** With the global rank-one pencil above, for every star
complement `T = {alpha} u U`:

```text
a_0 = a*L_T(alpha) = 0,                 b_0 = b*L_T(alpha) = 0,
a_1 = u_{j+1} - a*alpha^{j+1},          b_1 = v_{j+1} - b*alpha^{j+1},
```

and `a_1, b_1` do **not** depend on `U`.

*Proof.* `alpha` is a root of `L_T`, so `a_0 = sum_l ell_l (a alpha^l) =
a L_T(alpha) = 0`, and `b_0 = 0` likewise. For the second row, `a_1 = sum_{l=0}^j
ell_l u_{1+l} = a sum_{l=0}^{j-1} ell_l alpha^{1+l} + ell_j u_{j+1}`. Since
`ell_j = 1` and `sum_{l=0}^{j} ell_l alpha^{1+l} = alpha L_T(alpha) = 0`, the
inner sum equals `-alpha^{j+1}`, so `a_1 = u_{j+1} - a alpha^{j+1}`; the same
computation gives `b_1 = v_{j+1} - b alpha^{j+1}`. Neither depends on `U`. ∎

**Corollary (sharpened slope count).** In the global monic-rank-one branch the
whole fixed-root star contributes **exactly one** noncontained slope -- namely
`z = -a_1/b_1`, present iff `b_1 = v_{j+1} - b alpha^{j+1} != 0` -- and the whole
branch contributes **at most two** distinct noncontained bad slopes: that one
star slope and, at most, the note's scalar-zero slope `a + z b = 0`. This
replaces the `1 + binom(|D|-1, j-1)` bound of Corollaries 13/15/16 by `2`.

*Proof.* By the star-constancy lemma `a_0 = b_0 = 0`, so every star complement
automatically lies on the determinant quadric (`a_0 b_1 - a_1 b_0 = 0`), is
noncontained iff `b_1 != 0`, and -- since `a_1, b_1` are constant in `U` -- has
the one slope `-a_1/b_1`. By Corollary 15 the only landing complements away from
the scalar-zero slope are star complements, so the branch's noncontained slopes
are this single star slope together with at most the scalar-zero slope. ∎

If `alpha notin D`, or in the infinity (`s=0`) branch, Corollary 15 already
leaves at most the scalar-zero slope, so the bound is `1`.

## Scope: this does not touch the open obstruction

This is a sharpening, not progress on F1. The host note's "Why This Helps F1"
already disposes of the fixed-root-star branch as polynomial and *"no longer part
of the aperiodic obstruction"*; the sharpening only replaces an exponential
constant by `O(1)` inside that already-disposed branch. The `2` holds **only** in
the degenerate global monic-rank-one pencil (a rank identity on the first `j+1`
syndromes), not generically. The open F1 obstruction is the aperiodic non-global
determinant-incidence branch (Cor 16 case 2, Cor 18-22), where the number of
distinct bad slopes is unbounded by the note: independent generic-`(u,v)` scans
still produce on the order of `|D|` distinct slopes. Nothing here changes that.

## Verification

The verifier

```text
experimental/scripts/verify_f1_fixed_root_star_slope_collapse.py
```

re-implements `GF(p)`, `GF(p^2)`, `GF(p^3)`, the locator and the Corollary 4 gate
from scratch (no shared code with the host verifier) and checks, exhaustively
over small fields (`p` up to `13`, `|D|` up to `12`, `j` up to `6`):

- `a_0 = b_0 = 0` and `a_1, b_1` constant across every star complement;
- the star contributes exactly one noncontained slope iff `b_1 != 0`;
- the whole global monic-rank-one branch has at most two distinct noncontained
  slopes (the star part at most one), including the `alpha notin D` and infinity
  branches;
- the looseness witnesses: e.g. for `|D|=12, j=6`, `462` star landing
  complements collapse onto a **single** slope (host bound was `1+462`);
- a gate-versus-direct-interpolation cross-check on non-structured `(u,v)`,
  validating Corollary 4 itself.

It reports `96376` structured checks with `0` violations, observed maximum star
slopes `1` and branch slopes `2` (so the `2` is attained), and supports
`--certificate` / `--check` for a deterministic certificate.
