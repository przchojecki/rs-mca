# F17^32 M3 Line-Value Lift

This directory contains an explicit line-value lift of the fixed top-window
synthetic M3 packet for

```text
RS[F_17^32,H,256], |H|=512, 421 <= A <= 426.
```

The regular-minor extractor consumes syndrome pencils.  This certificate
records actual values `f,g:H -> F_17^32` whose weighted Reed-Solomon syndromes
are exactly the fixed top-window input.  For the order-512 subgroup,
`lambda_x = x/512`, so the verifier uses the inverse Fourier section
`y(x)=sum_m s_m x^(-m-1)` and checks `Syn(y)=s`.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_line_value_lift.py \
  --check experimental/data/certificates/hankel-f17-32-m3-line-value-lift/f17_32_n512_k256_a421_426_fixed_prefix92_line_values.json
```

Non-claims: this is a line-value lift of a synthetic packet, not a worst-case
MCA bound, not a quotient/tangent subtraction table, and not a singular-pivot
packet.
