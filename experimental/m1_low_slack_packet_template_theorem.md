# M1 Low-Slack Packet-Template Theorem

**Status:** PROVED / AUDIT.

This note packages the exact residual-packet bookkeeping used by the M1
low-slack templates. It is the common template behind the slack-two depth-two
window theorem, the slack-three first-superboundary theorem, and the
residual-depth frontier shift.

## Packet Formula

Let `D subset F_p^*` be a multiplicative subgroup with a quotient
decomposition into `N` fibers of size `m`. Fix slack `T` and residual depth
`d`, with `T+d<m`. A normalized residual packet has size `T+d`:

```text
P = {1,u_1,...,u_(T+d-1)}.
```

The depth-`d` canonical residual catalog is

```text
C_T^(d)(D) = { P :
  e_1(P)=...=e_(T-1)(P)=0,
  |P|=T+d, all elements distinct }.
```

For `P in C_T^(d)(D)`, put

```text
c_T,d(P)=(-1)^T e_T(P),
tau(P)=#{quotient fibers touched by P}.
```

At exact support size `s=Lm+T+d`, the residual-packet slope multiset is

```text
M_T^(d)(z) = (1/(T+d)!) sum_{P in C_T^(d)(D)}
             binom(N-tau(P), L) * #{x in D : x^T c_T,d(P)=z}.
```

Thus every nonzero frontier image is a union of power cosets, and the
quotient-lift contribution is completely separated as a binomial weight.

## Frontier Organization

The residual catalog has a disjoint first-nonzero frontier partition. For
`0<=j<d`,

```text
F_{T,d}^{(j)} = { P : |P|=T+d,
                  e_1(P)=...=e_(T+j-1)(P)=0,
                  e_(T+j)(P) != 0 },
```

and the terminal stratum has `e_1(P)=...=e_(T+d-1)(P)=0`. On
`F_{T,d}^{(j)}`, after `j` residual-depth shifts, the first nonzero slope is

```text
z_j(P)=(-1)^(T+j)e_(T+j)(P),
```

and scaling by `D` gives a union of `D^(T+j)` cosets. Terminal pure-zero
packets are exactly power-cosets: if `h=T+d`, they exist precisely when `h|n`,
in which case they are the `n/h` cosets of the subgroup of size `h`.

Consequently, low-slack M1 packet work can be organized as:

1. remove inactive quotient-lift gates;
2. close terminal pure-zero power-cosets explicitly;
3. shift inherited zero frontiers to the next slack;
4. prove coset-image estimates only on the genuinely first-nonzero frontiers.

The weighted ladder identity in
`experimental/m1_residual_depth_frontier_shift.md` makes item 3 exact: the
zero-frontier catalog at slack `T` is the next-slack catalog at `T+1` with the
same binomial quotient-lift weight.  Thus the template exposes one genuinely
new frontier per rung rather than multiplying the inherited packet weight
through the ladder.  The additive criterion there shows that any subadditive
certificate with a depth-uniform `K sqrt(p)` bound on each new frontier pays
`K sqrt(p)` once per rung, plus the explicit terminal power-coset ledger.

## Dither Gate

At the canonical exact layer `s=k+T`, a residual packet of depth `d` can lift
only if

```text
m | k-d.
```

If `k=k_0-r` with `m|k_0`, then depth `d` survives only when `m | r+d`.
In particular, when `0 < (k+T mod m) < T`, the small-residual catalog below
one quotient fiber is cleared at that quotient scale before any character-sum
or shape-count estimate is needed.

## Verification

The verifier

```bash
python3 experimental/verify_m1_low_slack_packet_template.py
```

checks representative tiny canonical scans. It verifies the packet-lift
formula, residual slope consistency, terminal pure-zero counts, first-nonzero
frontier partition, active-depth gate, and positive-dither clearance.
