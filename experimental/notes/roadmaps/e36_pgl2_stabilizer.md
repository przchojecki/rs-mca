# E36: PGL2 stabilizers of 2-power toy domains

Node: `f_dih_subgroup_completeness`.

Status: finite check / evidence packet.  This does not promote the full
group-theoretic node to `PROVED`; it discharges the requested toy stabilizer
casework and leaves the general algebraic lemma as the remaining route.

## Method

For each field `F_q` in `{F_17, F_97}` and each 2-power `n | q-1`, the verifier
tests every distinct coset domain

```text
D = alpha * mu_n.
```

For `D = alpha * mu_n`, the expected dihedral stabilizer is

```text
x -> zeta x,
x -> alpha^2 zeta / x,
```

with `zeta in mu_n`.

The stabilizer enumeration is exact but avoids a large full-group sweep.  Fix
three distinct source points of `D`.  Every `PGL_2(F_q)` set-stabilizer sends
that triple to an ordered triple of distinct points of `D`, and the Mobius map
is uniquely determined by those three images.  The verifier solves the
resulting linear equations

```text
a x_i + b = y_i(c x_i + d),  i = 1,2,3,
```

then tests whether the resulting map sends all of `D` to `D`.

## Result

The pinned certificate
`experimental/data/certificates/e36-pgl2-stabilizer/e36_pgl2_stabilizer.json`
has 52 row checks and no exceptions:

```text
F_17: n=4 all 4 cosets, n=8 all 2 cosets, n=16 all 1 coset.
F_97: n=4 all 24 cosets, n=8 all 12 cosets,
      n=16 all 6 cosets, n=32 all 3 cosets.
```

For every row, the computed set-stabilizer has size `2n` and equals the
explicit dihedral set above.  No exotic Mobius stabilizer appears in these toy
prize-class domains.

## Consequence

At the checked toy rows, the quotient-sector taxonomy has no sixth
PGL2-symmetry mechanism: the only finite stabilizer mechanisms visible are the
cyclic/multiplicative and dihedral/Chebyshev ones.  The remaining obligation in
`f_dih_subgroup_completeness` is the general group-theoretic argument excluding
special overgroups beyond this finite toy scope.
