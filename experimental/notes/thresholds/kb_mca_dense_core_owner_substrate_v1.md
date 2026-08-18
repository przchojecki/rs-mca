# KoalaBear dense-core owner substrate and reserve repricing

Status: **PROVED INTERFACE PACKET / ZERO DEPLOYED LEDGER MOVEMENT**

Exact parent: PR #1168 head
`6a5dcdae1591fc7f044eda6a942bfe178521a48c`.

This packet supplies three guarded inputs for the owner route left open by
the rank-eleven pair-core cut. It does not construct that owner. Its purpose
is to make the next theorem type-correct and honestly priced before any
dense pair-core group is charged to the existing S/A/E chronology.

The #1168 terminal that the interface must handle is an actual fixed
minimizing pair with core deficiency at most `4` owning at least `200632`
distinct finite slopes. The fixed-pair multiplicity is genuinely parallel;
it is not a distinct-neighbor degree.

## 1. Separate two-anchor reserve

Let `N` be the proved near-rational first-match set and `E` the residual
order-32 exception set. The available bounds are

```text
|N| <= 2w,    |E| <= 31.
```

They cannot be identified: `2w=134944` on KoalaBear and `2w=134896` on the
Mersenne-31 stress row. If a chronology-correct dense-core owner reuses the
active large rational-owner assembly, then for owner size `g>2m-K` its
contained-slope target must therefore be

```text
B_owner^(2w)(g) <= B*-(2w+31)-(n-g).                 (R1)
```

The four charges then close by the exact identity

```text
2w + 31 + (n-g) + [B*-(2w+31)-(n-g)] = B*.
```

The endpoint ledger is:

| row | `2w+31` | target at `g_min=2m-K+1` | target at `g=n` |
|---|---:|---:|---:|
| KoalaBear | 134975 | 274980728110346481 | 274980728111260112 |
| Mersenne-31 stress | 134927 | 15728609 | 16642288 |

The exact full-owner average ceilings leave integer factors `4807520` and
`9`, respectively. This proves arithmetic viability only. It does not prove
the stricter large-owner maximum-fiber theorem required by (R1).

## 2. The silent `k -> k+1` transport is false

On the deployed KoalaBear domain `D=<zeta>` of order `n=2^21`, let

```text
e=67473,
E={zeta^i: 0<=i<e},
S={zeta^i: e<=i<e+m},
u=1_E,  v=X^k,  gamma=0.
```

The zero polynomial explains `u` on `S`. No polynomial of degree below `k`
agrees with `X^k` on `m>k` points, so the pair is not simultaneously
explained there and the record is support-wise MCA-bad for `RS[F,D,k]`.
For `RS[F,D,k+1]`, `(0,X^k)` explains the pair on the identical support.
Thus neither badness nor first-owner semantics is invariant under a silent
dimension substitution.

This is a hostile regression against unguarded transport, not an obstruction
to a guarded adapter.

## 3. Exact guarded shifted-lattice adapter

For a word `U` define

```text
M_U={(W,N): W(x)U(x)=N(x) for every x in D}
```

and the two shifts

```text
s_k(W,N)   = max(deg W, deg N-(k-1)),
s_k+1(W,N) = max(deg W, deg N-k).
```

Every nonzero vector satisfies

```text
s_k+1 <= s_k <= s_k+1+1,
```

and the minima satisfy the same one-step comparison. Put `omega=n-m`. If
`W` is the monic split squarefree locator of `D\T`, has degree `omega`, and
`N=Wc`, then the effective envelope permits `deg c<=k`. It represents an
actual degree-below-`k` explanation on the same size-`m` support exactly
when any of the equivalent guards holds:

```text
deg c<k,
deg N<=omega+k-1,
s_k(W,N)<=omega.                                    (G1)
```

Conversely every degree-below-`k` explanation on an exact size-`m` support
has one unique guarded `(W,N)` representation.

Pair noncontainment is executable on the same support. Interpolate `u|T`
and `v|T` to their unique polynomials of degree below `m`. The pair is
simultaneously code-explained on `T` if and only if both interpolants have
degree below `k`. A guarded explanation of `u+gamma v` together with failure
of this pair test is therefore an actual support-wise MCA-bad witness.

This theorem reconstructs a witness. It does not transport or assign an
owner.

## 4. Typed deployed boundary witness

The upstream #1159 record `KB_SPARSE_BOUNDARY_ACTUAL_RECORD_V1` realizes the
guard on the deployed row. In
`F_p[alpha]/(alpha^6+alpha+6)`, with the same prefix `E` and following
support `S`, set

```text
v(x)=-1/(x-alpha),
u(x)=1_E(x)+alpha/(x-alpha),
gamma=alpha.
```

Then `u+gamma v=1_E`, so zero explains the slope word on `S`. If a
polynomial `g` of degree below `k+1` agreed with `v` there, then
`(X-alpha)g+1` would have `m>k+1` roots and degree at most `k+1`, a
contradiction. The pair is therefore noncontained even for the enlarged
dimension. The complement locator with numerator zero satisfies (G1) and
reconstructs the identical support and explanation.

The shifted lattice minimum is exactly `67473` under both shifts. The owner
fields remain deliberately unassigned:

```text
Q owner:      UNASSIGNED
BC owner:     UNASSIGNED
U_new owner:  UNASSIGNED
```

## 5. Interface for the #1168 dense-core terminal

Any chronology-correct owner theorem proposed for the `delta<=4`,
`200632`-slope terminal may use this packet as the following acceptance
contract.

1. If it reuses the active large-owner assembly, it must prove the contained
   owner bound at the repriced target (R1), with the `2w` and `31` sets
   charged separately in first-match order.
2. If its certificate is computed in the effective `K=k+1` lattice
   envelope, it must enforce (G1) and the exact-support pair-noncontainment
   test before counting an actual `RS[...,k]` bad slope.
3. It must preserve the actual line, finite slope, support, and chronology;
   numerical profile equality alone is not an owner assignment.
4. It must accept or explicitly route the typed pole-line witness and reject
   the unguarded `(1_E,X^k)` transport mutation.

The packet proves that these checks are sufficient for witness soundness and
that the repriced arithmetic is internally consistent. It does **not** prove
that every dense pair-core group has such an owner, that Q or BC is total,
or that the resulting owner bound meets (R1). Those are the missing
same-line coupling/chronology statements identified by #1168.

## 6. Provenance

The four source nodes are public, commit- and tree-pinned in
`experimental/data/certificates/kb-mca-dense-core-owner-substrate-v1/manifest.json`:

- two-anchor reserve repricing;
- the `k -> k+1` badness-transport counterexample;
- the degree-guarded shifted-lattice witness adapter;
- the typed deployed pole-line witness certificate.

The source nodes in turn pin the exact #1159, #1160, and #1163 manuscript,
manifest, and verifier blobs. No external theorem is imported beyond those
recorded dependencies.

## 7. Replay and scope

```text
python3 experimental/scripts/verify_kb_mca_dense_core_owner_substrate_v1.py
python3 experimental/scripts/verify_kb_mca_dense_core_owner_substrate_v1.py --tamper-selftest
python3 experimental/scripts/verify_kb_mca_dense_core_owner_substrate_v1_independent.py
```

This packet moves no active-v4 atom, does not pay error rank eleven, and does
not close KoalaBear or either prize problem.
