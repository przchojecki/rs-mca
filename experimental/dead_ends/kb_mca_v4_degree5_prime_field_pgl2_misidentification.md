# Rejected degree-five prime-field \(\operatorname{PGL}_2\) argument

## Status

```text
REJECTED_VARIABLE_IDENTIFICATION
```

This argument was generated while building the degree-\(60\) decomposition
source-fiber adapter and was rejected by an independent audit before commit
or publication.

## The rejected argument

The first draft correctly observed that the inner-degree-five profile has
two totally ramified points, exhausts Riemann--Hurwitz, and is geometrically
conjugate to \(z\mapsto z^5\).  It then asserted that the sixty active roots
belong to the deployed prime-field evaluation domain

\[
D\subseteq\mathbf F_p^\times.
\]

From this it tried to place an order-five deck transformation in
\(\operatorname{PGL}_2(\mathbf F_p)\) and contradict
\(5\nmid p(p^2-1)\).

## Why it fails

The endpoint variable \(T\) in

\[
f(T)=V_{\rm act}(T)/A(T)^5
\]

is a parameter on the primitive transversal residue line.  The active roots
\(t_i\) and source values \(\alpha_j\) are parameter-line values in the
challenge field \(\mathbf F_{p^6}\), not carrier coordinates
\(x\in D\subseteq\mathbf F_p\).

The relevant source distinction is visible in:

- `regular_grs_mds_deficit_reduction.md`, where the \(t_i\) are regular
  selected parameters and the carrier locators are separate polynomials in
  the evaluation variable \(X\);
- `kb_mca_v4_equality_wall_fixed_domain_rank16_normalization_v1.md`, where
  the \(t_i\) parameterize the primitive transversal residue line.

Thus the three-point descent gives at most
\(\operatorname{PGL}_2(\mathbf F_{p^6})\).  Since

\[
p^6\equiv-1\pmod5,
\]

that group does admit order-five elements.  The proposed contradiction is
invalid.

The same error also invalidates any unconditional use of
\(m\mid|D|=2^{21}\) for the geometric endpoint map \(h\).  That divisibility
is only a necessary condition after a separate theorem identifies the
parameter-line decomposition with an \(m\)-fold map on the carrier domain.

## Correct replacement

The degree-five row can instead be deleted over the challenge field
\(K=\mathbf F_{p^6}\):

1. two reduced active \(h\)-fibers give a \(K\)-rational target transform of
   \(h\);
2. the two totally ramified source points are \(K\)-rational;
3. \(K\)-rational source and target normalizations put the map in the form
   \(cz^5\);
4. \(\gcd(5,|K^\times|)=1\), so \(z\mapsto z^5\) is a permutation of \(K\)
   and cannot have a reduced five-point \(K\)-rational active fiber.

That corrected proof is recorded in the live adapter note.  The geometric
inner-degree-thirty to inner-degree-six refinement was independent of the
rejected identification and remains valid.
