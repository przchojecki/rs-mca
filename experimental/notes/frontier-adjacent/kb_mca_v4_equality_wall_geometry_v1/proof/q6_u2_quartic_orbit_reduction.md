# Pole-Graph Orbit Reduction for the \(u=2\) Star Quartic

## 1. Status

This note performs the exact combinatorial symmetry reduction for
the simple-vertex birational-quartic branch of:

```text
proof/q6_u2_plane_map_reduction.md
target/q6_u2_star_quartic_elimination_target.md
```

It reduces the \(11{,}130\) raw graph/free-edge cases to at most
\(985\) pole-graph automorphism orbits, depending on the pole-cycle
partition. It does not perform the remaining symbolic quartic
elimination and books no payment.

The exact classifier and certificate are:

```text
experiments/classify_q6_u2_quartic_graph_orbits.py
experiments/q6_u2_quartic_graph_orbits.json
```

## 2. Case object

Fix one of the four two-regular bipartite pole-graph types:

\[
6,\qquad4+2,\qquad3+3,\qquad2+2+2,
\tag{2.1}
\]

where the parts are cycle half-lengths.

A simple-vertex quartic case consists of:

1. four selected free pole edges \(E\) among the twelve pole-graph
   edges;
2. a five-edge complement graph
   \(\overline G\subset K_6\) on the six noninvariant source rows;
3. the exact degree law
   \[
   \deg_{\overline G}(j)=1+e_j,
   \qquad
   e_j=\deg_E(j)\in\{0,1,2\}.
   \tag{2.2}
   \]

There are \(11{,}130\) such labeled pairs
\((E,\overline G)\): \(8{,}730\) with
\(\overline G\) a tree and \(2{,}400\) with it disconnected and
cyclic.

## 3. Correct symmetry group

The valid relabelings are the bipartition-preserving automorphisms
of the actual pole graph. A full independent \(S_6\) action on the
left rows would forget which free root belongs to which right
vertex and is not valid.

For the four pole-cycle partitions, the exact automorphism-group
orders are:

\[
\boxed{12,\qquad32,\qquad72,\qquad384.}
\tag{3.1}
\]

The action is applied simultaneously to:

* the four selected bipartite pole edges;
* the six left source rows;
* the five edges of \(\overline G\).

Relabeling is valid even though the actual source values are
symbolic: it renames the corresponding source and pole variables
together and preserves every incidence and interpolation equation.

## 4. Exact orbit census

\[
\boxed{
\begin{array}{c|r|r|r|r|r}
\text{pole cycles}&|\operatorname{Aut}|&
\text{all orbits}&\text{tree}&\text{cyclic}&
\text{noncycle open}\\ \hline
6&12&985&768&217&985\\
4+2&32&490&359&131&488\\
3+3&72&188&138&50&188\\
2+2+2&384&79&53&26&77
\end{array}}
\tag{4.1}
\]

The raw case count remains \(11{,}130\) in every row.

The complete pole-cycle conclusion can already hold for a
degree-two component only when the pole graph has a four-cycle.
Exactly:

\[
\begin{array}{c|r|r}
\text{pole cycles}&\text{paid raw cases}&\text{paid orbits}\\ \hline
6&0&0\\
4+2&6&2\\
3+3&0&0\\
2+2+2&18&2
\end{array}
\tag{4.2}
\]

All other orbits require contradiction or owner emission.

## 5. Remaining symbolic check per orbit

For one representative:

1. construct the six source lines
   \(\mathscr L_j\);
2. construct the line sections \(R_j\) from the ten selected star
   vertices and four selected free roots;
3. impose
   \[
   c_jR_j(v_{jk})=c_kR_k(v_{jk})
   \]
   on the five complement edges;
4. for a cyclic complement, apply every exact cycle-product gate;
5. interpolate the unique quartic for each projective scalar
   solution;
6. test irreducibility and geometric genus zero;
7. test the exact pullback divisor and actual endpoint minors.

The tree rows have one scalar solution up to scale. Cyclic rows may
have no solution after the product gates; if they do, the number of
projective scalar parameters is the number of connected components
minus one.

The important reduction is quantitative:

> The largest simple-vertex symbolic elimination now has \(985\)
> orbit representatives, not \(11{,}130\) labeled cases.

The classifier certificate prints every open canonical
representative, including the four free pole edges, the five
complement-graph edges, its tree/cyclic branch, and its exact orbit
size:

```text
experiments/classify_q6_u2_quartic_graph_orbits.py
experiments/q6_u2_quartic_graph_orbits.json
```

The symbolic gluing calculation can therefore consume the
certificate directly.

## 6. Guardrails

The orbit census does not:

* substitute convenient numerical source values;
* handle repeated star vertices;
* handle ramification in \(\psi^*\mathcal K\);
* prove that any open representative is impossible;
* book a same-record owner payment.

The symbolic source and pole variables, and their exact
source-facet relations, remain load-bearing in the next eliminant.
