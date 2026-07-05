# E1 Pocklington 250-bit Exhibit Field

- **Status:** PROVED / exact integer certificate.
- **DAG node:** `e1_pocklington_250bit_exhibit_field`.
- **Certificate:** `experimental/data/certificates/e1-pocklington-250bit-exhibit-field/e1_pocklington_250bit_exhibit_field.json`.
- **Verifier:** `python3 experimental/scripts/verify_e1_pocklington_250bit_exhibit_field.py --check experimental/data/certificates/e1-pocklington-250bit-exhibit-field/e1_pocklington_250bit_exhibit_field.json`.

This packet records a named exhibit field for the E1 folded certificate cells.
It is intentionally local: it supplies one exact field and two exact roots of
unity, not a uniform-in-field theorem.

## Statement

Let

```text
c = 562949953421383
F = 2^200
p = c F + 1
  = 904625697166646869347790708689937759412227977745095982970820953353127723009.
```

Then `p` is prime, has bit length `250`, satisfies `p < 2^256`, and satisfies
`p = 1 mod 256`.  Therefore `F_p` is an admissible named exhibit field for the
E1 folded cells at `N' = 128` and `N' = 256`.

With base `3`, the elements

```text
rho_128 = 3^((p-1)/128) mod p
        = 440266185830122294862552098878717819794821358702875176198798016633729926114

rho_256 = 3^((p-1)/256) mod p
        = 368095729527972287347366462180303065908636718991804826343652948937354262881
```

have exact multiplicative orders `128` and `256`, respectively.

## Certificate Check

Pocklington's theorem applies with known factor `F = 2^200` of `p-1`.  The
verifier checks:

```text
p = c 2^200 + 1
p < 2^256
p mod 256 = 1
F^2 > p
3^(p-1) = 1 mod p
gcd(3^((p-1)/2) - 1, p) = 1
```

Since the only prime divisor of `F` is `2`, these congruences satisfy
Pocklington's criterion and prove that `p` is prime.  The same verifier then
checks, for `N in {128, 256}`,

```text
rho_N = 3^((p-1)/N) mod p
rho_N^N = 1 mod p
rho_N^(N/2) != 1 mod p
```

Because each `N` is a power of two, this proves exact order `N`.

## Role

This discharges the exhibit-field part of the E1 folded-certificate branch:

```text
e1_pocklington_250bit_exhibit_field [PROVED]
    -> e1_folded_certificate_cell_128_payload [CONDITIONAL]
    -> e1_folded_certificate_cell_256_payload [CONDITIONAL]
```

Downstream packets can cite the field and roots without redoing primality or
root-order arithmetic.

## Non-Claims

- This packet does not prove a uniform statement over all admissible fields.
- This packet does not by itself close the two E1 folded no-vector payloads.
- This packet does not assert that there is a fixed list of official row
  primes; it is an exhibit-specific certificate.
