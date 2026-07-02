# E1 Cluster Certificates

- **Status:** PROVED / verifier-backed.
- **Agent:** Codex acting autonomously for Allen Graham Hart.
- **Roadmap link:** Fable execution queue `QA.14 [cluster_certificates]`.
- **Verifier:** `experimental/scripts/verify_row_c_e1_collision_norm_criterion.py`.
- **Artifact:** `experimental/data/certificates/row-c-e1-sampling/row_c_e1_collision_norm_criterion.json`.

This note records the small certificate-compression lemmas that sit immediately
after the graded collision-radius result.  It does **not** solve the later
generator-economy design problem: constructing large structured families whose
differences all factor through a small generator set remains separate.

## 1. Free Cliques From The Graded Radius

Fix a cyclotomic order `N`, a prime `p == 1 mod N`, and use the dyadic
antipodal class normal form from the E1 collision-norm note.  Suppose a class
set `F` has pairwise coefficient half-`l_1` distance at most `d`, and

```text
(2d)^phi(N) < p.
```

Then every pair of distinct characteristic-zero classes in `F` remains distinct
after reduction modulo the chosen embedding into `F_p`.

**Proof.**  For a pair difference `Delta`, every conjugate has absolute value
at most `2d`, so `|Norm(Delta)| <= (2d)^phi(N) < p`.  Since `Delta` is nonzero,
its norm is a nonzero integer of absolute value below `p`; hence `p` cannot
divide it.  The collision-norm criterion then forbids a modular collision.

For Row-C, the existing graded-radius table gives:

| `N'` | certified half-`l_1` radius `d` | consequence |
|---:|---:|---|
| 64 | 112 | the whole Row-C class is a free clique |
| 128 | 7 | every diameter-7 subcluster is certified |
| 256 | 1 | every diameter-1 subcluster is certified |

## 2. One-Check Cross-Cluster Pairing

Let `Delta in Z[zeta_N]` be a common center-difference factor.  Suppose every
cross-cluster difference factors as

```text
D_xy = Delta * Q_xy
```

where `Q_xy` is a nonzero algebraic integer.  If

```text
p does not divide Norm(Delta),
0 < |Norm(Q_xy)| < p       for every x,y,
```

then one precomputed check of `Norm(Delta)` certifies all cross-pairs.

**Proof.**  Norms multiply:

```text
Norm(D_xy) = Norm(Delta) Norm(Q_xy).
```

The first factor is nonzero modulo `p`; the second is a nonzero integer of
absolute value below `p`, hence is also nonzero modulo `p`.  Therefore `p` does
not divide `Norm(D_xy)`, and the collision-norm criterion rules out a modular
collision for that pair.

The common "everywhere-big" analytic sufficient condition is a way to certify
the quotient factor: if `D_xy = Delta + eta_xy`, the quotient
`Q_xy = 1 + Delta^{-1} eta_xy` is known to be a nonzero algebraic integer, and
every conjugate satisfies

```text
|eta_xy^tau| <= (R-1)|Delta^tau|,
R^phi(N) < p,
```

then every conjugate of `Q_xy` has absolute value at most `R`, so
`|Norm(Q_xy)| < p`.  The algebraic-integrality/factorization hypothesis is
essential; without it this is only an archimedean estimate, not a certificate.

## 3. Integer-Factor Freebie

If `Delta` is certified and `0 < m < p`, then `m Delta` is certified.  Indeed,

```text
Norm(m Delta) = m^phi(N) Norm(Delta),
```

and neither factor is divisible by `p`.

This is useful in generator-economy searches: integer scalar multiples of a
certified generator do not require new norm-factorization work.

## Verification

Replay:

```bash
python3 experimental/scripts/verify_row_c_e1_collision_norm_criterion.py
python3 experimental/scripts/verify_row_c_e1_collision_norm_criterion.py --emit
python3 -m py_compile experimental/scripts/verify_row_c_e1_collision_norm_criterion.py
```

The verifier records:

- the Row-C free-clique consequences of the graded-radius table;
- the exact root budgets `R` with `R^phi(N) < p`;
- a toy one-check cross-cluster replay in `Z[zeta_8]`, `p=17`;
- the integer-factor freebie on the same toy ring.
