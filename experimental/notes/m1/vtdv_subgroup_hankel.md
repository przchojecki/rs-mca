# Subgroup Hankel VTDV Packet

- **Status:** PROVED / linear-algebra identity.
- **DAG node:** `vtdv`.
- **Certificate:** `experimental/data/certificates/vtdv/vtdv.json`.
- **Verifier:** `python3 experimental/scripts/verify_vtdv_packet.py --check experimental/data/certificates/vtdv/vtdv.json`.

This packet records the Hankel moment factorization used throughout the v10
Hankel safe-side program.

## Claim

Let `H` be an evaluation subgroup or any distinct evaluation set in a field
`F`. Let `lambda_x` be the dual/parity-check weight at `x`, and let `u_x` be
the received-word value. Define weighted moments

```text
S_m = sum_{x in H} lambda_x u_x x^m.
```

For row powers `i=0..t-1` and column powers `c=0..j`, the Hankel block

```text
M_u[i,c] = S_{i+c}
```

factors as

```text
M_u = V_t^T D_u V_{j+1},
```

where

```text
V_t[x,i] = x^i,
V_{j+1}[x,c] = x^c,
D_u[x,x] = lambda_x u_x.
```

Indeed, the `(i,c)` entry of the right hand side is

```text
sum_{x in H} x^i (lambda_x u_x) x^c = S_{i+c}.
```

The identity is field-generic and therefore applies over prime fields and
extension fields. The subgroup assumption matters for later quotient and
displacement structure, not for this matrix multiplication identity.

## DAG Use

This packet is a required input for `fm1`, `counting_frame`, and the
displacement/F1/U1 lanes. It is the common bridge from received-word moments to
Hankel pencils.

## Non-Claims

- This packet does not classify bad slopes.
- This packet does not count locator fibers.
- This packet does not prove displacement-uniformity by itself.
- This packet does not edit Papers A-D.
