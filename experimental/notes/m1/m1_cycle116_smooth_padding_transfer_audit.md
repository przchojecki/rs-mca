# M1 Cycle116 Smooth Padding Transfer Audit

Status: CONDITIONAL / AUDIT / SMOOTH-PADDING-TRANSFER.

Date: 2026-06-24.

This note isolates the concrete smooth-padding step in the Cycle116 chain. The
native row gives

```text
LD_sw(RS[F0,D0,137],143) >= N.
```

The smooth row adjoins `theta` with `theta^2=eta` and uses

```text
H=<theta>=D0 disjoint_union theta D0.
```

The odd coset is partitioned as

```text
A={theta eta^i: 0<=i<=118},      |A|=119,
R={theta eta^i: 119<=i<=255},    |R|=137.
```

For a native witness support `S_T=D0\J_T`, define

```text
S_T^+ = S_T union A,
J_T^+ = J_T union R.
```

Then

```text
|S_T^+| = 143+119 = 262,
|J_T^+| = 113+137 = 250,
k^+ = 137+119 = 256.
```

The bad parameters are preserved. If a native codeword `c_z` of degree `<137`
explains `f+z g` on `S_T`, then

```text
L_A(X)c_z(X)
```

has degree at most `118+136<256` and explains the lifted line on `S_T union A`.
Conversely, if degree-`<256` codewords simultaneously explain the lifted pair on
`S_T union A`, they vanish on every point of `A`; dividing by `L_A` gives
degree-`<137` native codewords explaining the native pair on `S_T`, contradicting
native noncontainment.

For the fixed-jet view, multiplying the native co-support locator by the fixed
`R`-locator gives

```text
P_T^+(X)=P_R(X)P_T(X).
```

Since `deg(P_T-P_T')<=107` and `deg P_R=137`,

```text
deg(P_T^+-P_T'^+) <= 137+107 = 244 = 250-6.
```

Also `P_R(beta)!=0`, so

```text
P_T^+(beta)=P_R(beta)P_T(beta)
```

preserves the distinct product values counted by Cycle84.

## Verifier

Run:

```sh
python3 experimental/scripts/verify_m1_cycle116_smooth_padding_transfer.py
python3 experimental/scripts/verify_m1_cycle116_smooth_padding_transfer.py --json
```

The verifier checks:

```text
theta^2=eta and theta has order 512;
H partitions as D0 disjoint_union theta D0;
A and R partition the odd coset with sizes 119 and 137;
A is disjoint from D0, so L_A is nonzero on native supports;
beta is outside H and P_A(beta), P_R(beta) are nonzero;
the lifted agreement, dimension, and co-support sizes are 262, 256, and 250;
the fixed-jet loss remains sigma=6 after R-padding;
the division argument returns degree-<137 native codewords.
```

## Remaining Dependencies

This audit depends on the native Cycle116 transfer at agreement `143`, the
Cycle84 exact occupancy count for `N`, and the official ABF source gate if the
row is promoted as prize-facing. It does not rerun the Cycle84 product census.

The generic theorem behind the padding step is now isolated in:

```text
experimental/notes/m1/m1_smooth_padding_ldsw_transfer_theorem.md
python3 experimental/scripts/verify_m1_smooth_padding_ldsw_theorem.py
```

That theorem proves that multiplying the native line by the `A`-locator pads
agreement onto `A`, while any lifted simultaneous explanation must vanish on
`A` and divide back to a native explanation. This concrete audit supplies the
field/domain facts needed to instantiate that theorem for the `[512,256]` row.
