# KoalaBear full-span hyperplane closure attempt v1 — unresolved

## Status

`YELLOW / NOT BANKED`.

This attempt tried to strengthen the exact equality-wall
ternary-secant/circuit countermodel to the full statement

\[
\min_{0\ne a\in\mathbf F_p^8}
\operatorname{wt}\langle a,u_\bullet\rangle
\ge 1{,}048{,}577.
\]

It did not produce a solver-independent certificate.  No full-span claim
may cite this file as proof.

## Exact facts retained

The sealed witness with SHA-256

```text
5fbaed397c3cf788d6805c7b203e4a94e95ea8a13bdd74e54c393220ddcdd788
```

has 225 coordinate types, 69 records, exact support 981,105 per record,
secant rank eight, and exact record-pair/circuit data.  Exhaustive
enumeration of all 3,280 projective directions in
\(\{-1,0,1\}^8/\{\pm1\}\) gives maximum zero mass 841,778, first attained
at

\[
(1,0,0,0,0,0,0,1),
\]

and hence ternary-secant distance 1,052,958.

These facts are replayed in the adjacent committed route-cut packet.  They
do not quantify over every coefficient in \(\mathbf F_p^8\).

## Unbanked searches

1. A weighted random search over 300,000 rank-seven flats took about 54
   seconds and found no zero mass larger than 841,778.  This is empirical
   evidence only.
2. A bounded-cofactor CP-SAT search used the valid Hadamard reduction
   \[
   |a_i|\le \lfloor 7^{7/2}\rfloor=907
   \]
   for primitive normals to support-generated rank-seven flats.  The first
   chart returned only `FEASIBLE` with objective 841,778 and a useless upper
   bound after 120 seconds.
3. An independent SCIP feasibility formulation processed about 245,104
   nodes on the first chart and timed out after 120 seconds without proving
   infeasibility.
4. A lazy weighted-matroid basis-cut formulation was effective as a
   counterexample finder on the rejected predecessor, but its relaxation
   closed too slowly to certify this witness.

Solver timeout or failure to find a counterexample is not proof.

## Exact route that remains

Aggregate equal projective normals with their integer weights.  Since every
ternary minor has determinant of absolute value at most
\(8^4=4096<p\), rational and \(\mathbf F_p\) ranks agree.  A future closure
must emit one of:

- an explicit coefficient normal with zero mass at least 846,160; or
- a replayable deletion/contraction proof tree showing every subset of
  normal weight at least 701,274 has rank eight.

The tree checker must recompute every basis determinant, branch cover, and
weight bound.  CP-SAT or SCIP status alone is not an acceptable terminal
certificate.
