# XR scattered-syzygy flat transport (2c-gamma-a)

DAG node: `xr_syzygy_flat_transport`.

Status: PROVED as a dictionary/reduction.

## Statement

The diffuse part of rung 2c produces syzygy members that are constrained-
support dual words.  The transport dictionary sends each such member to the
same sparse-dual/closed-set object used by the Conjecture F support-lattice
machinery.

Concretely, let `(P,E)` be an evaluation flat in the QF.12/E30 sense, and let

```text
Ann(P,E) = { u in F^E : sum_{x in E} u_x f(x) = 0 for every f in P }.
```

For a nonzero syzygy member `u in Ann(P,E)`, define

```text
S(u)  = supp(u),
cl(S) = { x in E : ev_x(P) lies in span(ev_y(P) : y in S) }.
```

Then:

1. `S(u)` is a sparse dual support of the evaluation code of `P`.
2. `cl(S(u))` is a closed set in the trace matroid of `P`.
3. The coefficient choices on `S` have dimension
   `|S| - rank(ev_S(P))`, exactly the local nullity counted by sparse-dual
   enumeration.
4. Unions of transported supports are handled by the same closure operation
   used in the QF.12 support-lattice accounting identity.

Therefore counting diffuse stagnation patterns with scattered syzygy supports
is not a new object: after this transport, it is precisely sparse dual words
and their generated closed sets over an evaluation flat.  The polynomial
closed-set bound remains the downstream `f_support_lattice` /
`f_many_sparse_structure` problem; this packet only proves the dictionary.

## Proof

For an evaluation flat `(P,E)`, the trace matroid has one column
`ev_x(P)` for each `x in E`.  A vector `u` supported on `S subset E` lies in
`Ann(P,E)` exactly when

```text
sum_{x in S} u_x ev_x(P) = 0.
```

Thus `S` is a dependent support in the trace matroid, and the space of
coefficient choices on that fixed support is the kernel of the column matrix
on `S`, with dimension `|S| - rank(ev_S(P))`.

The closure formula is the standard matroid closure: `x in cl(S)` exactly when
adding `ev_x(P)` does not raise the rank of the columns indexed by `S`.  Hence
`cl(S)` is closed, contains `S`, and is determined entirely by the evaluation
flat.  Taking several syzygy members and replacing their supports by closures
or by closures of unions is exactly the support-lattice operation in QF.12.

For the 2c-gamma application, alpha's support-cancellation step supplies the
input syzygy members: each member is supported on the scattered pieces cut out
by the intersection pattern.  Transporting those supports via `S -> cl(S)`
places the diffuse stagnation count into the F-lattice language with the same
piece sizes and coefficient nullities.  No additional algebraic structure is
introduced by the transport.

## Verifier

`experimental/scripts/verify_xr_syzygy_flat_transport.py` checks the dictionary
over three explicit `F_17` flats on `H = F_17^*`:

```text
mds_deg3       span(1, X, X^2, X^3)
common_root    (X-1) * span(1, X, X^2, X^3)
even_pullback  span(1, X^2, X^4, X^6)
```

For every support of size at most 4 it detects sparse annihilator supports,
computes their trace-matroid closures, checks closure idempotence and support
containment, verifies the coefficient nullity formula, and samples closure of
unions of transported supports.  The rows exercise the three relevant cases:
trivial MDS lattice, loop/common-root support, and pullback/twin-pair supports.

The recomputed summary is pinned in
`experimental/data/certificates/xr-syzygy-flat-transport/toy_flat_transport.json`.
