# XR E3 Calculus

- **Status:** PROVED / COMBINATORIAL / STRUCTURED LOWER-BOUND DIRECTION.
- **DAG node:** `xr_e3_calculus`.
- **Verifier:** `experimental/scripts/verify_xr_e3_calculus.py`.
- **Artifact:** `experimental/data/certificates/xr-e3-calculus/xr_e3_calculus.json`.

This note upgrades the exchange-energy scaffold from a toy proxy to a precise
calculus for the two support-side quantities used in the XR route.

```text
endpoint correlation C_s(A) = Pr[T_0 in A and T_s in A],
killed energy        K_s(A) = Pr[T_0,...,T_s all lie in A],
```

where `T_i` is the simple random walk on the Johnson graph `J(n,j)`.  The
endpoint quantity is the one governed by the averaged-XR spectral inequality.
The killed quantity is the stricter odd exchange proxy used by the E2
falsifier after paid quotient strata are stripped.

## Convention Block

```text
object:              Johnson locator graph J(n,j)
vertices:            j-subsets of an n-point domain
exchange step:       remove one selected point and add one missing point
XR role:             support-side proxy for aligned-locator sets A_{u,v}
sampler:             not an MCA/list slope sampler
denominator role:    none; consumers must print q_line/q_chal separately
```

## Theorem 1: Endpoint E2 Consistency

Let `A_x` be the point-dictator family

```text
A_x = {T : x in T}.
```

Write

```text
delta = j/n,
lambda = 1 - n/(j(n-j)).
```

Then for every `s >= 0`,

```text
C_s(A_x) = delta^2 + lambda^s delta(1-delta).
```

In particular,

```text
C_2(A_x)-delta^2 = lambda^2 delta(1-delta),
```

which is exactly the endpoint second-moment form used by averaged-XR.  Thus
the E2 endpoint normalization agrees with the Johnson-scheme variance
normalization in the displacement/XR packet.

Proof.  The indicator `1_{x in T}` spans the constant function plus the first
nontrivial Johnson eigenspace.  The normalized simple-exchange walk has
eigenvalue `lambda` on this first eigenspace.  Starting from stationarity,

```text
C_s(A_x)-delta^2 = <1_A-delta, P^s(1_A-delta)>
                 = lambda^s ||1_A-delta||_2^2
                 = lambda^s delta(1-delta).
```

The verifier checks this identity directly by exact rational random-walk
computation for several `(n,j,s)`.

## Theorem 2: Fixed-Core Killed E3

Let `A_C` be the fixed-core family

```text
A_C = {T : C subset T},      |C|=c.
```

Then

```text
K_s(A_C)
  = binom(n-c,j-c)/binom(n,j) * ((j-c)/j)^s.
```

In particular,

```text
K_3(A_C) = delta_C * ((j-c)/j)^3.
```

Proof.  The initial probability of containing `C` is
`delta_C=binom(n-c,j-c)/binom(n,j)`.  Conditional on a current vertex
containing `C`, a single exchange remains inside `A_C` exactly when the
removed element is not in `C`, which has probability `(j-c)/j`.  Iterating
gives the formula.

This is the structured lower-bound direction for tangent/common-root families:
paid fixed-root structure has visibly large odd exchange energy until the core
nearly fills the locator.

## Theorem 3: Active Block-Profile Killed E3

Partition the domain into blocks `B_b` of sizes `m_b`, and fix a profile
`a_b` with `sum_b a_b=j`.  Let

```text
A_a = {T : |T cap B_b| = a_b for every b}.
```

Put

```text
delta_a = prod_b binom(m_b,a_b) / binom(n,j),
gamma_a = (sum_b a_b(m_b-a_b)) / (j(n-j)).
```

Then

```text
K_s(A_a) = delta_a * gamma_a^s.
```

The profile is active exactly when `gamma_a>0`, i.e. some block has both a
selected and an unselected point.  Active folded/equivariant support profiles
therefore have explicit positive `K_3`; frozen full-block quotient profiles
have `gamma_a=0` and are energy-invisible to one-exchange `K_3`.

Proof.  The initial density is `delta_a`.  From a vertex with profile `a`, an
exchange preserves the profile exactly when it removes and adds inside the
same block.  The number of such directed exchanges is
`sum_b a_b(m_b-a_b)` out of `j(n-j)` total directed exchanges.  This
probability is constant across the stratum, so iteration gives the formula.

## Consequence For The E2 Falsifier

This proves the easy direction of the XR inverse program:

- common-root/tangent model families have explicit large `K_3`;
- active folded/equivariant profile families have explicit positive `K_3`;
- frozen quotient/full-block families can have `K_3=0`, so paid quotient
  strata must be removed before interpreting low energy as aperiodic.

Non-claims:

- no inverse theorem is proved;
- no Reed-Solomon word-pair set `A_{u,v}` is enumerated here;
- no M1 safe-side threshold or list threshold follows from this note alone.

