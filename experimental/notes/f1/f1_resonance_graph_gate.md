# F1 Resonance Graph-Gate Certificate

## Status

EXPERIMENTAL / AUDIT.

This note adds a finite verifier for the restricted F1 arbitrary-anchor
balanced-denominator wall

```text
B = F_p,       F = F_{p^2},       D = F_p,
t = sigma = 2,       j = n-a = 3,
```

off the degenerate locus

```text
R0 = { wedge([W]_E,[Bnum]_E) = 0 }.
```

It does not prove F1, MCA, CA, list decoding, line decoding, or a protocol
statement. Its purpose is narrower: make the Cycle 18 graph-gate reduction
machine-checkable using the same Fable-loop arithmetic, with quick random
off-`R0` samples for the graph branch and tiny forced-resonance samples for
the exact gates.

## Verified Gate

Let `Delta(tau1,tau2,tau3)` be the Cycle 12 landing determinant for split
co-support triples `T subset D`, written as an `F`-valued quadratic in the
elementary symmetric coordinates of `T`.

On `R0^c`, normalize by

```text
r0 = wedge([W]_E,[Bnum]_E).
```

The verifier checks that the normalized polynomial has the Cycle 18 shape

```text
Delta = Delta0 + alpha Delta1,
Delta0 = tau3^2 + A(tau1,tau2) tau3 + B(tau1,tau2),
Delta1 = s(tau1,tau2) tau3 + h(tau1,tau2).
```

Consequently, outside the branch `Delta1 == 0`, every common zero of
`Delta0=Delta1=0` with `s != 0` lies on the graph

```text
tau3 = -h/s.
```

After clearing denominators, the graph branch must satisfy

```text
G = h^2 - A h s + B s^2 = 0.
```

The point of this polynomial is exact. It is the cleared remainder in the
identity

```text
s^2 Delta0 = Delta1 * (s tau3 + A s - h) + G.
```

Equivalently, on the open locus `s != 0`, `G=s^2 Delta0(-h/s)`. Thus `G`
is the resultant/divisibility gate for the graph branch: once `Delta1=0`
forces `tau3=-h/s`, common zeros of `Delta0` can persist in dimension two
only if this cleared remainder vanishes identically.

Since `deg G <= 4`, a nonzero `G` leaves only `O(p)` base pairs
`(tau1,tau2)` on the graph branch and therefore cannot by itself produce a
two-dimensional `Theta(p^2)` slope image. A large split-cubic counterpacket
must pass through one of the exact gates

```text
Delta1 == 0        or        G == 0.
```

More explicitly, if `Delta1` is not the zero polynomial and `G` is not the
zero polynomial, then the common-zero locus

```text
Delta0 = Delta1 = 0
```

inside `B^3` has `O(p)` points. A crude uniform bound is `<= 6p` when
`s` is nonzero, because the graph part has at most `deg(G) p <= 4p`
base pairs by Schwartz-Zippel and the exceptional locus `s=h=0` lies over at
most one base line, with at most two `tau3` values from the monic quadratic
`Delta0`. If `s` is identically zero, then `h` is a nonzero polynomial of
degree at most `2`; the exceptional branch contributes at most `4p` points.
Since the distinct slope count is bounded by the number of landing triples,
the nonzero-gate branch is curve-sized before any slope-fiber collapse is
used.

## Gate Partition

The verifier now records the exact gate into which each landing triple falls.
In the normalized notation above, every split-triple landing belongs to one
of the following disjoint branches:

```text
base-valued gate:       Delta1 is the zero polynomial;
graph gate:             Delta1 is nonzero and s(tau1,tau2) != 0,
                         hence tau3=-h/s and G(tau1,tau2)=0;
exceptional locus:      Delta1 is nonzero and s(tau1,tau2)=h(tau1,tau2)=0.
```

The exceptional locus is already lower-dimensional, independently of whether
`G` vanishes. If `s` is a nonzero affine form, `s=0` lies over a line and the
monic quadratic `Delta0` gives at most two `tau3` values, so this branch has
`<=2p` ambient points over `B=F_p`. If `s` is identically zero, then `h` is a
nonzero degree-`<=2` polynomial and the same quadratic-in-`tau3` argument gives
`<=4p` ambient points. Thus the exceptional branch is always curve-sized once
`Delta1` is not identically zero.

Consequently, the only branches that can plausibly support a `Theta(p^2)`
split-cubic slope image across growing primes are:

```text
Delta1 == 0                     (base-valued gate),
s != 0 and G == 0               (open graph-divisibility gate).
```

This is the operational form of the remaining search target. A future
counterpacket must report which exact gate it occupies; a future positive
proof must collapse the slope image on those exact gates.

## Slope Map

On the non-base graph side, the remaining problem is not just the zero set of
`G`; it is the image size of the slope map on that zero set. The landing
equation has coordinates

```text
p1 - tau3 = z q1,
p2        = z(q2 - tau3).
```

Eliminating `tau3` gives the exact quadratic normal form

```text
q1 z^2 - (p1 - q2) z - p2 = 0.
```

Thus, away from denominator degeneracies, the graph-gate slope image is
controlled by the projective coefficient map

```text
(tau1,tau2) |-> [q1 : (p1-q2) : p2].
```

The symbolic checker verifies this elimination identity. This is the algebraic
form of the remaining graph-collapse question: on source-valid pieces of
`G==0`, does this projective map have one-dimensional image, or can it have
two-dimensional image and therefore `Theta(p^2)` distinct slopes?

## Verifier

Run from the repository root:

```sh
python3 experimental/scripts/verify_f1_resonance_graph_gate.py
```

The script imports the existing Cycle 11/12/15 local arithmetic, normalizes
each off-`R0` landing polynomial, and verifies:

- direct determinant values agree with the interpolated quadratic `Delta`;
- the normalized `tau3^2` coefficient is exactly `1`;
- the `alpha` component has no `tau3^2` term;
- the cleared-remainder identity
  `s^2 Delta0 = Delta1*(s tau3 + A s - h) + G` holds coefficientwise;
- `Delta1 = s tau3 + h` recovers every graph value `tau3=-h/s`;
- every graph-branch common zero passes through `G=0`;
- every landing is classified by the gate partition above;
- the exceptional branch is bounded by the explicit `<=2p` or `<=4p`
  lower-dimensional estimate whenever `Delta1` is nonzero;
- whenever `G` is nonzero, the observed graph branch is bounded by the
  finite `G`-zero pair count;
- whenever both exact gates are inactive, the observed split-triple landings
  are bounded by the explicit nonzero-gate finite bound.

The final `CERT` line records the best sampled branch in a machine-readable
form with fields such as `p`, `q_gen`, `q_line`, `Delta1_zero`, `G_zero`,
`G_degree`, `G_zero_pairs`, `nonzero_gate_bound`, `exceptional_bound`,
`remainder_identity`, `gate_status`, `base_gate_C2`, `graph_C2`,
`exceptional_C2`, and split-triple counts.

The companion symbolic checker

```sh
python3 experimental/scripts/fable_loop/local_checks/20260618_cycle18_resonance_slope_symbolic.py
```

also verifies the cleared-remainder identity and the slope-quadratic
elimination identity with formal coefficients, before any finite sampling or
source-validity filtering enters.

The default run mixes quick random off-`R0` samples, which exercise the
nonzero graph gate, with a tiny forced-`Ra` nullspace sample, which exercises
the exact resonance gates. Larger forced scans should be run explicitly when
searching for a persistent counterpacket.

## Ledger Impact

This makes the F1 rank/determinant resonance branch more falsifiable. The
previous notes isolated `Q==0` and then the Cycle 18 graph map as the live
wall. The new verifier turns that into a concrete counterexample-first test:
look for source-valid forced-resonance families where the exact gates
`Delta1==0` or `G==0` persist and the distinct slope count grows like
`Theta(p^2)`.

No such family is claimed here. The contribution is the checked reduction and
certificate format needed to search for one without confusing finite evidence
with a corrected-reserve theorem.
