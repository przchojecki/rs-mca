# L1 Coset-Chart Residue-Line Bridge

## Claim

Status: `PROVED-LOCAL / NORMAL-FORM`.

This note consumes the L1 coset-petal and reconstruction-collapse framework now
recorded on `main`:

1. `experimental/notes/l1/l1_coset_petal_rank_collapse.md`.
2. `experimental/notes/l1/l1_general_reconstruction_collapse.md`.

The result is a local bridge, not a primitive-vacancy theorem.  In a full-petal
coset chart, every capped kernel set is either quotient-coset structured or
emits a low-degree projective residue pair.  After cancelling simultaneous
active quotient-label basepoints, that pair becomes ordinary residue-line data
on the surviving quotient labels.

This is compatible with
`experimental/notes/l1/l1_prime_ell_pv_refutation.md`: the primitive mixed
minimal examples recorded there are not declared paid or absent here.  They are
classified by the residue-line data produced below.

Assume:

```text
H <= F_q^* has order ell,
ell | (q-1),
t >= 2,
T_i = g_i H are distinct active full petals,
a_i = g_i^ell are their distinct quotient labels,
C is a disjoint union of H-cosets,
c_i in F_q^*.
```

For `E subset C`, put

```text
F_E(X) = L_E(X) = product_{x in E} (X-x).
```

Let `W_E` be the unique degree-`< t*ell` CRT representative satisfying

```text
W_E == c_i F_E   mod X^ell-a_i        for i=1,...,t.
```

Call `E` a capped kernel set if

```text
ell <= |E| = d <= (t-1)ell,
deg W_E <= d.
```

Then every capped kernel set is one of two types.

1. **Quotient-coset.** `F_E in F_q[X^ell]`, equivalently `E` is a union of
   full `H`-cosets.
2. **Residue-line bridge.** There is a residue `1 <= r < ell` and a nonzero
   projective pair `(G,Hh)` with

   ```text
   deg G, deg Hh <= t-2,
   Hh(a_i) = c_i G(a_i)        for i=1,...,t,
   G does not vanish on all active labels.
   ```

   Let

   ```text
   Z = { i : G(a_i)=Hh(a_i)=0 },
   S_Z(Y) = product_{i in Z} (Y-a_i),
   G0 = G/S_Z,
   H0 = Hh/S_Z.
   ```

   Then on the surviving active labels `A0={a_i:i notin Z}`,

   ```text
   H0(a_i) = c_i G0(a_i),
   G0(a_i) != 0,
   deg G0, deg H0 <= |A0|-2,
   |A0| >= 2.
   ```

   Thus `(G0,H0)` is ordinary residue-line data on the quotient subchart.  The
   cancelled divisor `S_Z` is an active-basepoint boundary term that must still
   be handled by the appropriate residue/tangent ledger.

Consequently, the local coset-chart search has no third class after applying
the quotient-or-residue-line normal form:

```text
K_capped subset K_quot union K_residue_bridge.
```

The statement remains true after restricting to divisibility-minimal kernel
sets via the reconstruction-collapse note.  It does not say that
`K_residue_bridge` is paid, small, or non-primitive under the current
stabilizer-primitive ledger.

## Proof

Write `Y=X^ell`.  Since the petals are `H`-cosets, their locators are

```text
L_{T_i}(X) = X^ell - a_i.
```

The coset-petal graded block decomposition says that reduction modulo
`X^ell-a_i` respects degree residue modulo `ell`.

Decompose the missed-core locator and its CRT representative by residue class:

```text
F_E(X) = sum_{r=0}^{ell-1} X^r f_r(Y),
W_E(X) = sum_{r=0}^{ell-1} X^r w_r(Y).
```

Modulo `X^ell-a_i`,

```text
X^r f_r(X^ell) -> X^r f_r(a_i),
```

so CRT uniqueness gives, for every residue `r`,

```text
w_r(a_i) = c_i f_r(a_i)        for i=1,...,t.
```

Now use the kernel inequality `deg W_E <= d=|E|`.  For every nonzero `w_r`,

```text
deg w_r <= floor((d-r)/ell).
```

Also `deg f_r <= floor((d-r)/ell)`, because `F_E` itself has degree `d`.
For `r>0` and `d <= (t-1)ell`,

```text
floor((d-r)/ell) <= floor(((t-1)ell-r)/ell) = t-2.
```

Thus every nonzero residue block with `r>0` satisfies

```text
deg f_r, deg w_r <= t-2.
```

If all `f_r=0` for `r>0`, then `F_E=f_0(X^ell)`.  Therefore its root set is
stable under multiplication by `H`, so `E` is a union of full `H`-cosets.  This
is exactly the quotient-coset case.

Otherwise choose `r>0` with `f_r != 0`.  Put

```text
G = f_r,
Hh = w_r.
```

The displayed CRT relation gives

```text
Hh(a_i) = c_i G(a_i)        for every active label a_i.
```

Also `G` cannot vanish on all active labels: it is nonzero of degree `<= t-2`,
while the `a_i` are `t` distinct points.

It remains to put the projective pair into ordinary residue-line form.  Let

```text
Z = { i : G(a_i)=Hh(a_i)=0 }.
```

Because every scalar `c_i` is nonzero, the relation above implies
`G(a_i)=0` if and only if `Hh(a_i)=0` among the active labels.  Since the
labels are distinct, the polynomial

```text
S_Z(Y)=product_{i in Z}(Y-a_i)
```

divides both `G` and `Hh`.  Define

```text
G0=G/S_Z,
H0=Hh/S_Z.
```

For every survivor `i notin Z`, the divisor `S_Z(a_i)` is nonzero, so division
preserves the scalar relation:

```text
H0(a_i)=c_i G0(a_i).
```

Moreover `G0(a_i)` is nonzero on every surviving label.  If it vanished at a
survivor, then `G(a_i)` and hence `Hh(a_i)` would vanish there, contradicting
maximality of `Z`.

The degree bound sharpens after cancellation:

```text
deg G0, deg H0 <= (t-2)-|Z| = (t-|Z|)-2 = |A0|-2,
```

where `A0` is the surviving active label set.  Finally `|A0| >= 2`, because a
nonzero polynomial of degree `<= t-2` cannot vanish at `t-1` of the `t`
distinct active labels.  Hence `(G0,H0)` is ordinary residue-line data on
`A0`, with denominator nonzero on the surviving active quotient labels.

This proves the quotient-or-residue-line normal form for every capped kernel
set.  Restricting to the divisibility-minimal kernel sets of the
reconstruction-collapse note preserves the classification.

## Quotient Charge

For a quotient-coset set `E`, write

```text
E = union_{b in B_E} {x : x^ell=b},
|B_E| = j.
```

Then

```text
F_E(X) = f_E(X^ell),
f_E(Y) = product_{b in B_E} (Y-b),
|E| = j ell.
```

The CRT condition descends to the quotient labels:

```text
w_E(a_i)=c_i f_E(a_i),
deg w_E <= j.
```

So quotient-coset kernel sets are exactly the quotient-line objects in the
coset chart.

## Verification

The companion verifier exhaustively checks a finite sample grid and regenerates
the certificate/report:

```sh
python3 experimental/scripts/verify_l1_coset_chart_residue_bridge_v1.py --write
python3 experimental/scripts/verify_l1_coset_chart_residue_bridge_v1.py --check
python3 experimental/scripts/verify_l1_coset_chart_residue_bridge_v1.py --json
```

The checked grid contains:

```text
cases_checked = 8
subsets_checked = 76086
kernel_sets_checked = 187
minimal_kernel_sets_checked = 25
quotient_kernel_sets = 25
residue_bridge_kernel_sets = 162
minimal_quotient_kernel_sets = 23
minimal_residue_bridge_kernel_sets = 2
unclassified_after_quotient_or_residue_bridge = 0
```

The verifier also runs optimized CRT cross-checks against direct reconstruction
on small subcases and a synthetic active-basepoint cancellation example.

## Non-Claims

- Not a primitive-vacancy theorem under the current stabilizer-primitive ledger.
- Not a proof that residue-line data are paid, negligible, or globally packed.
- Not arbitrary non-coset petals.
- Not ordinary list decoding, interleaved-list safety, or protocol soundness.
- No Paper A-D or site-data edits are made.
