---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
atom_or_cell: K3_M2_DIAGONAL_112_NEAR_NEGATIVE_QSLICE
quantifier: every saturated source-line (a,b,c)=(1,1,2) near-aligned negative reconstruction retained by the parent factor census
projection_and_unit: exact source-facet necessary q-slice; not a carrier, received-line theorem, slope owner, or payment
claimed_bound: the near-aligned negative sign is empty
status: PROVED_NEAR_ALIGNED_NEGATIVE_QSLICE_EMPTY_ROW_112_OPEN_K3_OPEN
impact: removes one of the three signs left by the parent saturated source-line census
falsifier: an admissible retained negative reconstruction satisfying the target q-slice without forcing xi=tau(ell) in K
replay: python3 experimental/scripts/verify_kb_mca_v4_m2_diagonal_112_near_negative_qslice_v1.py --check --tamper-selftest
---

# KoalaBear diagonal `(1,1,2)` near-negative q-slice deletion

## 0. Verdict

The saturated source-line `(a,b,c)=(1,1,2)` near-aligned negative sign is
empty.

The parent census reduces every negative candidate to three retained
rank-drop loci. Exact reconstruction shows that all three loci have the same
monic residual quartic. The required root `tau(ell)` forces one polynomial
factor to vanish, after which the residual roots are
`{tau(ell),ell}`. Matching the actual near-aligned target then forces
`tau(xi)=ell`, equivalently `xi=tau(ell) in K`, contradicting
`xi in I minus K`.

This removes only the near-aligned negative sign. The aligned positive and
near-aligned positive signs remain open, so the full `(1,1,2)` row, K3, and
the KoalaBear row remain open. No owner or charge is booked.

## 1. Imported interface

Use the notation and hypotheses of the universal degree-two source-facet
census at parent commit
`c2edcfa5cbfb8a41e7dea04ae1b34325c90ed5dc`, especially equations
(9.17)--(9.26).

Normalize the fixed-point-free deck involution as

```text
tau(x)=1/x,
J_0={2,1/2,b,1/b},
J_1={eta,ell}={c,d},
w=tau(eta)=1/c.
```

The six-set and its common five-set are

```text
I={tau(eta),tau(ell),tau(xi),xi,z,tau(z)},
K=I minus {xi}.
```

In the near-aligned branch, equation (9.24) therefore requires the residual
quartic to have the double-root pair

```text
{tau(ell),tau(xi)}={1/d,tau(xi)}.                 (1.1)
```

The parent negative determinant factorization (9.25), including the
fixed-label exclusion of `A=0`, retains exactly

```text
fixed-moving:B,   moving-moving:B,   moving-moving:C.          (1.2)
```

Put

```text
P=cd-2c-2d+1,       Q=2cd-c-d+2.
```

The two `B` charts have `b=-Q/P`; the `C` chart has `b=-P/Q`.
The corresponding `P` or `Q` is nonzero. For example, on `B=0`, `P=0`
would also force `Q=0`, hence `c+d=0` and `c^2=1`, contrary to the
fixed-point-free distinct-label hypotheses. The `C` case is symmetric.
All other incidence and reconstruction denominators are the nonzero chart
units already declared in parent equations (9.25)--(9.26).

## 2. Common reconstructed residual

Write `R(W)` for the product of the two residual quadratics obtained after
dividing the two `J_1` norm slices by `(W-w)^2`, made monic.

The exact Sage replay reconstructs the source form independently on each
chart in (1.2), verifies its fifth compatibility equation, performs both
exact divisions, and proves that all three monic quartics are identical.
The independent Wolfram Engine replay rebuilds the same linear systems and
checks the same common-residual assertion.

Define

```text
Lambda=4c^2d-2c^2-cd-c-2d+4.
```

If `E` is the parent incidence denominator in (9.25), substitution of
`w=1/c` gives the exact identity

```text
Lambda=cE.                                          (2.1)
```

Thus `Lambda` is nonzero on every parent chart. The unnormalized residual
leading coefficient is, on each of the three loci,

```text
(c-1)^2(d-1)^2(d+1)^2(cd-1)^4 Lambda^4
---------------------------------------------------. (2.2)
              (c+1)^2 A^4
```

Here every displayed factor is a parent unit: `A!=0` was proved in (9.26),
and the remaining factors are nonzero by distinctness and
fixed-point-freeness. Hence monic normalization loses no candidate.

The explicit polynomials `Phi,Psi in Z[c,d]` are fixed by their hashes in
the certificate and printed in both exact replays. They satisfy

```text
R(1/d)=Phi^2/(d^4 Lambda^4),                       (2.3)
```

and

```text
R(W)-((W-1/d)(W-d))^2
 = 2 Phi/(d Lambda^2)(W+W^3)
   - Phi Psi/(d^2 Lambda^4) W^2.                  (2.4)
```

The actual chart has `d Lambda != 0`: `d` is a nonzero label and (2.1)
proves the second factor is a parent unit. The q-slice target (1.1)
has root `1/d`, so (2.3) gives `Phi=0`. Equation (2.4) then gives

```text
R(W)=((W-1/d)(W-d))^2.                             (2.5)
```

Both sides of (2.3)--(2.4), after clearing the displayed and inherited chart
denominators, are integer polynomial identities. The symbolic proof over
`QQ(b,c,d)` therefore reduces to every admissible specialization in
characteristic `2130706433`, and hence to its degree-six challenge-field
extension. The deployed prime avoids characteristics `2,3,5`.

The default symbolic solver minor contains a removable `c+d` factor. On the
divisor `d=-c`, rows `(0,1,2,4)` of the same five-row system have determinant

```text
15(c-2)(c-1)^2(c+1)^6(c+2)(2c-1)(2c+1)(c^2+1)
--------------------------------------------------------------.
                 c^4(4c^2+5c+4)^4
```

Every factor is nonzero by the parent label conditions, (2.1), and
invertibility of `15`. The exact Sage and Wolfram replays check this
alternate minor, so the cleared identities cover `c+d=0` as well.

## 3. Terminal collision

The required target quartic is

```text
((W-1/d)(W-tau(xi)))^2.
```

Comparing with (2.5), cancelling the nonzero polynomial `(W-1/d)^2`, and
using monicity in odd characteristic gives

```text
tau(xi)=d=ell.
```

Applying `tau` gives

```text
xi=tau(ell).
```

But `tau(ell)` is one of the five declared labels of `K`, whereas
`xi in I minus K`. This is the forbidden collision. Thus every retained
near-aligned negative chart is empty.

## 4. Positive route cut

The exact Python verifier also replays one `GF(43)` fixed-moving positive
packet. Its twelve labels are nonzero and distinct, its `I,J,K` interface is
correct, and its two residual quadratics obey the required q-slice
factorization. Nevertheless the full product over `J` has a nonzero odd
coefficient and therefore fails the even quadratic-pullback condition
needed for the full quotient identities (9.17)--(9.18).

This packet is a toy-field q-slice control, not a deployed component. Its
role is negative: a q-slice survivor does not justify deletion or
realization of the positive sign. The next maximal gate is the full
quotient system for the positive reconstructions, not another q-slice
search.

## 5. Replay and scope

Run:

```bash
python3 experimental/scripts/verify_kb_mca_v4_m2_diagonal_112_near_negative_qslice_v1.py --check --tamper-selftest
/usr/local/bin/sage experimental/scripts/verify_kb_mca_v4_m2_diagonal_112_near_negative_qslice_v1.sage
"/Users/scott/Applications/Wolfram Engine.app/Contents/MacOS/WolframKernel" \
  -script experimental/scripts/verify_kb_mca_v4_m2_diagonal_112_near_negative_qslice_v1.wl
```

The Python verifier binds the exact parent note, certificate, and verifier
blobs, rejects duplicate JSON keys, checks the Sage and Wolfram script
hashes, replays the positive control, and runs semantic mutations.

Not proved:

- the aligned positive sign;
- the near-aligned positive sign;
- deletion of the complete `(1,1,2)` row;
- any statement about the exceptional unsaturated orbit (9.10) or the
  biquadratic source-cover branch;
- an active first-match owner, distinct-slope payment, K3 value, or
  KoalaBear row bound.
