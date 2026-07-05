# E1 Pocklington 250-bit Exhibit Field

Status: PROVED.

Source DAG node: `e1_pocklington_250bit_exhibit_field`.

## Statement

The integer

```text
p = 904625697166646869347790708689937759412227977745095982970820953353127723009
  = 562949953421383 * 2^200 + 1
```

is prime, has bit length `250`, satisfies `p < 2^256`, and satisfies
`p = 1 mod 256`.

Consequently `F_p` is a valid named E1 exhibit field for the open folded
certificate cells `N'=128` and `N'=256`.  With base `3`,

```text
rho_128 = 3^((p-1)/128) mod p
        = 440266185830122294862552098878717819794821358702875176198798016633729926114

rho_256 = 3^((p-1)/256) mod p
        = 368095729527972287347366462180303065908636718991804826343652948937354262881
```

have exact orders `128` and `256`, respectively.

## Proof

Let

```text
c = 562949953421383
F = 2^200
p = cF + 1.
```

The verifier checks the displayed decimal value of `p`, `p < 2^256`,
`p mod 256 = 1`, and `F^2 > p`.

Use Pocklington's theorem with the known factor `F = 2^200` of `p-1`.  The only
prime divisor of `F` is `2`.  For base `a = 3`, the verifier checks

```text
3^(p-1) = 1 mod p
gcd(3^((p-1)/2) - 1, p) = 1.
```

Since `F > sqrt(p)`, these checks satisfy Pocklington's criterion, so `p` is
prime.

Because `p-1` is divisible by `256`, the multiplicative group `F_p^*` contains
elements of orders `128` and `256`.  The verifier checks the displayed
`rho_128` and `rho_256` by testing

```text
rho_N^N = 1 mod p
rho_N^(N/2) != 1 mod p
```

for `N in {128,256}`.

## Non-Claims

This packet only certifies the named field and primitive roots.  It does not
prove a folded no-vector certificate for either open E1 cell.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_e1_pocklington_250bit_exhibit_field.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_e1_pocklington_250bit_exhibit_field.py \
  --check experimental/data/certificates/e1-pocklington-250bit-exhibit-field/e1_pocklington_250bit_exhibit_field.json
```
