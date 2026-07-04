# E33: deep-link staircase toy census

DAG node: `deep_link_staircase`.

Status: EVIDENCE / finite toy census.  This does not prove the staircase
lemma; it prices the falsifier requested in Wave 5.

## Setup

The census fixes an aligned anchor `(u,v,T0,z0)` and counts aligned partner
supports `T` at slopes `z != z0` with

```text
k/2 < |T cap T0| < k.
```

Both rows use `n=16`, `k=8`, `A=11`, hence `t=A-k=3`.  The strict near-k
overlap range is nominally `5,6,7`, but `r=5` is impossible because
`n-A=5` and a second size-11 support cannot take six points outside `T0`.
Thus the checked bands are

```text
r = 6, 7.
```

The expected count uses the qx13 plateau: for `r<k`, a distinct-slope partner
has fresh codimension `t`.  For each anchor,

```text
E_r = (q-1) * C(A,r) * C(n-A,A-r) / q^t.
```

The verifier samples anchors deterministically and counts all partner supports
by the same syndrome-pencil method used in E27.

## Results

`F_97`, the E27 corridor row:

```text
samples: 4096
expected events: 909.934
observed events: 870
by overlap: r=6 -> 186, r=7 -> 684
max partner events for one anchor: 13
max distinct partner slopes for one anchor: 3
max partner events through one fixed subcore: 5
```

`F_17`, a denser stress row:

```text
samples: 512
expected events: 3521.576
observed events: 3734
by overlap: r=6 -> 852, r=7 -> 2882
max partner events for one anchor: 72
max distinct partner slopes for one anchor: 10
max partner events through one fixed subcore: 5
```

No all-slope support code appears in the near-k band on either row.

## Interpretation

The falsifier was a toy pair/support with super-linear many near-k aligned
partners.  It was not found.

The `F_97` row is strongly staircase-linear: the maximum anchor has 13 partner
events, below `n=16`.  The denser `F_17` stress row raises the constant to
`72 = 4.5n`, but the shape is still linear and the link through any single
subcore stays tiny (maximum 5).  This points toward a link-population cap as
the first proof route; the derived-pencil recursion remains a transport tool,
not something forced by a visible super-linear toy growth pattern.

## Verifier

Run:

```bash
python3 experimental/scripts/verify_e33_deep_link_staircase.py
```

The recomputed summary is pinned in
`experimental/data/certificates/e33-deep-link-staircase/e33_deep_link_staircase.json`.
