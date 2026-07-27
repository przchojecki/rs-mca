---
workboard_item: K1
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: Rebuilding the full selected-slope histogram after the six active source owners closes all full-outside rank-two slacks except the exact active source-determinant gap 67471..209568, with zero additional charge.
architecture: GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_SOURCE_RATIONAL_C5_BASE_TWIST_FROBENIUS_9208_ADAPTER_V1
atom_or_cell: ACTIVE_FULL_OUTSIDE_FULL_HISTOGRAM_INCIDENCE_BRANCH_COMPILER
quantifier: Per received line, fixed translated source, and rebuilt complete selector
projection_and_unit: Distinct bad finite slopes per received line
claimed_bound: zero additional charge on r=9209..67470 and r=209569..913631 in the declared full-outside rank-two branch
status: PROVED
impact: ZERO_CHARGE_BRANCH_CLOSURE
falsifier: Failure of the rebuilt full-histogram contracts, a scan endpoint different from the printed intervals at the active reserve, or use of selector data from before the six active deletions.
replay: python3 experimental/scripts/verify_kb_mca_v4_active_full_histogram_replay_v1.py --check
---

# KoalaBear active full-histogram replay

**PROVED ACTIVE BRANCH COMPILER / ZERO ADDITIONAL CHARGE / ROW OPEN.**

This packet replays the complete selected-slope incidence count after the
six active source-owner deletions and mandatory selector restart. It improves
the active carrier one-cut replay and isolates the exact remaining
full-outside source-determinant interval.

## 1. Active input

The active source-bound reserve is

\[
B_{\rm rem}=274{,}961{,}102{,}171{,}022{,}152,
\]

and the Frobenius endpoint gives \(r\ge9{,}209\) on every qualifying outgoing
full-outside coefficient-rank-two record.

For fixed \(r\), write

\[
s=t+r+1,\qquad N_V^{\max}=n-s,
\]

\[
x_0(r)=\left\lceil\frac{t-r+1}{2}\right\rceil,
\qquad
J_*(r)=
\begin{cases}
1+\lfloor j/x_0(r)\rfloor,&x_0(r)\ge1,\\
j+1,&x_0(r)\le0.
\end{cases}
\]

The full-histogram incidence theorem applies the MDS eight-basis floor to
every selected slope, not only a cutoff subset. Thus

\[
\boxed{
|\Gamma|
\le
\left\lfloor
\frac{J_*(r)\binom{N_V^{\max}}8}
{\binom{t+8}8}
\right\rfloor.
}
\tag{1.1}
\]

All supports, graph lines, bases, and histogram data in (1.1) belong to the
same selector rebuilt after the active deletion.

## 2. Exact active scan

The verifier scans every integer \(9{,}209\le r\le913{,}631\) and obtains:

| slack \(r\) | active terminal |
|---:|:---|
| \(9{,}209\ldots67{,}470\) | `PAID_ACTIVE_FULL_OUTSIDE_FULL_HISTOGRAM_CARRIER_INCIDENCE` |
| \(67{,}471\ldots209{,}568\) | `UNPAID_ACTIVE_FULL_OUTSIDE_X1_DETERMINANT_SOURCE_PACKING_SLACK_67471_TO_209568` |
| \(209{,}569\ldots913{,}631\) | `PAID_ACTIVE_FULL_OUTSIDE_FULL_HISTOGRAM_CARRIER_INCIDENCE` |

The exact counts are:

```text
paid       762,325
open       142,098
total      904,423
```

The lower boundary is structural:

```text
r=67,470: x0=2, cap margin  24,106,850,570,014,579
r=67,471: x0=1, cap margin -226,744,844,178,279,064
```

At the upper boundary:

```text
r=209,568: cap margin    -103,475,042,116
r=209,569: cap margin   1,105,071,933,958
```

The active reserve therefore shifts the legacy upper boundary from
`209,552/209,553` to `209,568/209,569`.

## 3. Exact route cut

For every open integer \(67{,}471\le r\le209{,}568\), the verifier constructs
an abstract packing with \(B_{\rm rem}+1\) zero-deficit slopes and:

```text
chosen x=1;
exact slack-simplex equality;
moving-zero equality;
enough local and global eight-basis capacity;
enough rank-nine scalar capacity;
survival of the degree-9,208 owner scalar guard.
```

These are abstract scalar witnesses, not Reed--Solomon selectors. They prove
that no argument using only (1.1), the same line occupancy, and the same
basis capacities can close the interval.

## 4. Resulting research target

The exact remaining full-outside branch is

\[
\boxed{67{,}471\le r\le209{,}568.}
\tag{4.1}
\]

It requires one of:

1. deployed determinant packing that correlates the canonical graph lines;
2. a stronger source-rank or source-Frobenius owner;
3. an exact incompatibility between the \(x=1\) scalar packing and split
   locator/source equations; or
4. a new histogram inequality using information discarded by (1.1).

Another cutoff optimization or a repeat of the same basis count cannot work.

## 5. Proof authority and nonclaims

The imported theorem is:

```text
experimental/notes/m1/
m1_kb_rank9_full_histogram_incidence_closure_v1.md
```

The active predecessor and carrier replay are:

```text
experimental/notes/frontier-adjacent/
kb_mca_v4_c5_twist_frobenius9208_adapter_v1.md
experimental/notes/frontier-adjacent/
kb_mca_v4_active_carrier_incidence_replay_v1.md
```

The verifier binds the active and legacy certificates, scans all active
slacks, hashes every route-cut witness, and rejects semantic mutations.

This packet adds no slope charge. It does not construct a deployed selector
in the gap, pay non-full-outside source load, prove Q, pay balanced core or
the final complement, or close the row.

# PROVED
