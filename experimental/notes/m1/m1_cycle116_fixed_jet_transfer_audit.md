# M1 Cycle116 Fixed-Jet Transfer Audit

Status: CONDITIONAL / AUDIT / FIXED-JET-TRANSFER-ALGEBRA.

Date: 2026-06-24.

This note isolates the native Cycle116 algebra that turns fixed-jet locators
into distinct support-wise bad line parameters.

The slot-block bridge proves, for each Cycle84 tuple `T`,

```text
P_T(X)=X^113-X^112+O(X^107),
P_T(beta)=4(beta-1)Phi(T),
beta=X+2.
```

The abstract transfer uses the complement `S_T=D0\J_T`, where `D0=<eta>` has
order `256`. Since

```text
V_D(X)=prod_{x in D0}(X-x)=X^256-1,
L_T(X)=prod_{x in S_T}(X-x)=V_D(X)/P_T(X),
```

the top six coefficients of `P_T` force the top six coefficients of `L_T`.
Writing

```text
P_T(X)=X^113-X^112+O(X^107),
```

the quotient recurrence gives

```text
L_T(X)=X^143+X^142+X^141+X^140+X^139+X^138+O(X^137).
```

Thus the common truncation is

```text
W(X)=X^143+X^142+X^141+X^140+X^139+X^138,
```

and

```text
Q_T(X)=W(X)-L_T(X)
```

has degree at most `137`, the native code dimension.

The bad line parameter is

```text
z_T = Q_T(beta)
    = W(beta)-L_T(beta)
    = W(beta)-V_D(beta)/P_T(beta).
```

Because `beta` is outside `D0`, `V_D(beta)!=0`. Since `4(beta-1)!=0`,

```text
P_T(beta)=4(beta-1)Phi(T)
```

shows that distinct nonzero `Phi(T)` values give distinct `z_T` values through
the injective map

```text
Phi -> W(beta)-V_D(beta)/(4(beta-1)Phi).
```

This is the precise algebraic bridge from the Cycle84 product occupancy count
to the number of bad native line parameters.

## Verifier

Run:

```sh
python3 experimental/scripts/verify_m1_cycle116_fixed_jet_transfer.py
python3 experimental/scripts/verify_m1_cycle116_fixed_jet_transfer.py --json
```

The verifier checks:

```text
the quotient recurrence gives the common complement truncation W;
for a representative seven-slot tuple, P_T * L_T = X^256-1;
W-L_T has degree at most 137;
beta is outside D0 and V_D(beta) is nonzero;
4(beta-1) is nonzero;
P_T(beta)=4(beta-1)Phi(T) on the representative tuple;
Q_T(beta)=W(beta)-V_D(beta)/P_T(beta);
the noncontainment degree inequality is 143 > 137.
```

The representative tuple check is not a substitute for the 336 slot-identity
replay; it is a concrete sanity check that the formal transfer formula is being
applied with the same field model and locator conventions.

## Remaining Dependencies

This audit still depends on:

```text
the slot-identity replay for P_T(X)=X^113-X^112+O(X^107) and
  P_T(beta)=4(beta-1)Phi(T);
the Cycle84 exact occupancy theorem for the number of distinct Phi(T) values;
the official ABF source gate if the result is promoted as prize-facing.
```
