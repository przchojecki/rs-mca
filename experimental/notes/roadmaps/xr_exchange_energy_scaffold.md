# XR exchange-energy scaffold for the E2 evidence program

- **Status:** EXPERIMENTAL / PROVED-COMBINATORIAL scaffold.
- **DAG nodes:** `xr_e3_calculus`, `xr_inverse_toy`.
- **Fable evidence item:** E2, "Toy XR inverse".
- **Verifier:** `experimental/scripts/verify_xr_exchange_energy_scaffold.py`.
- **Artifact:**
  `experimental/data/certificates/xr-exchange-energy-scaffold/xr_exchange_energy_scaffold.json`.

This note supplies the first exact toy object for the XR route.  It does not
prove the XR inverse theorem and does not enumerate Reed--Solomon word pairs.
Its purpose is narrower: define a Johnson-walk exchange energy that can be used
as the support-side proxy in the E2 falsifier, verify the spectral normalization,
and test whether obvious paid structured families are visible to the proxy.

## Definition

Let `J(n,j)` be the Johnson graph on `j`-subsets of `{0,...,n-1}`.  For a set
`A` of vertices define

```text
E_s^J(A) = Pr[T_0, T_1, ..., T_s all lie in A],
```

where `T_0` is uniform on `J(n,j)` and each subsequent `T_i` is obtained by one
random exchange.  Thus `E_0^J(A)=|A|/binom(n,j)`, while `E_1^J(A)` is the
directed internal-edge density.  The intended future specialization is

```text
A = A_{u,v} = {locators T : (H_u l_T) is parallel to (H_v l_T)}.
```

The verifier treats `E_3^J` as the toy odd exchange-correlation proxy for
Fable's E2/QX.1 item.  This is only a proxy until the actual `A_{u,v}` scanner
is attached.

## Exact checks

The verifier checks the Johnson spectrum in the dense toy case `J(5,2)`:

```text
observed eigenvalues:  6^1, 1^4, (-2)^5
formula:              theta_i=(j-i)(n-j-i)-i, multiplicity binom(n,i)-binom(n,i-1)
```

It also checks the unnormalized gap

```text
theta_0 - theta_1 = n
```

for `(n,j)=(5,2),(16,4),(16,8),(512,128),(512,247)`, matching the gap used in
the displacement/spectral roadmap note.

## Structured toy families

For a fixed-core family

```text
A_c = {T : {0,...,c-1} subset T},
```

the exact energy is

```text
E_s^J(A_c)
  =
  binom(n-c,j-c)/binom(n,j) * ((j-c)/j)^s.
```

This models the common-divisor / fixed-root paid shape.  On the verifier's
`n=12,j=4,c=2` test, the structured `E_3` is `1/88`, about `103.6` times the
average `E_3` of twenty random subsets with the same size.  So the proxy sees
fixed-core structure very strongly.

For block-profile families with four blocks of size four, the exact energy is

```text
E_s^J(A_profile)
 =
 (prod_b binom(m_b,a_b)/binom(n,j))
 *
 (sum_b a_b(m_b-a_b)/(j(n-j)))^s.
```

The balanced profile `(2,2,2,2)` at `n=16,j=8` has

```text
E_0 = 72/715,
E_1 = 18/715,
E_3 = 9/5720.
```

Thus ordinary one-exchange energy also detects quotient-like structure when
the profile has internal block moves.

## Caveat: frozen quotient fibers

The full-block profile `(4,4,0,0)` at `n=16,j=8` has positive density
`1/12870` but

```text
E_1 = E_3 = 0.
```

This is not a contradiction; one exchange leaves the full-block stratum
immediately.  It is a useful warning for the XR route:

```text
before running an inverse theorem against ordinary one-exchange E_3,
remove paid quotient/full-block strata or use a multi-exchange variant.
```

Otherwise a quotient-paid family can look energy-invisible rather than
energy-large, and the inverse experiment would be testing the wrong object.

## Interpretation

The packet supports the E2 program in two ways.

First, the Johnson-walk normalization is now exact and replayable, so the next
experiment can attach this energy to actual toy aligned-locator sets
`A_{u,v}` at `n=16` instead of debating the proxy.

Second, the quotient caveat is already visible in the simplest block example.
The correct E2 inverse falsifier should be run on the paid-stripped aperiodic
set, with quotient strata classified before energy thresholds are interpreted.

The follow-up note `experimental/notes/roadmaps/xr_e3_calculus.md` promotes
the structured part of this scaffold to theorem status.  It separates endpoint
correlation `C_s`, which matches the averaged-XR spectral normalization at
`C_2`, from killed energy `K_s`, which is the stricter odd proxy used for
paid-stripped falsification.  The fixed-core and active block-profile formulas
above are proved there for all `s`, with exact `K_3` replay.

## Reproduce

```bash
python3 experimental/scripts/verify_xr_exchange_energy_scaffold.py
python3 experimental/scripts/verify_xr_exchange_energy_scaffold.py --emit
```
