# List Planted Arithmetic Compiler

## Status

PROVED-ARITHMETIC-COMPILER, conditional only on the already-proved quotient-core
list obstruction in Paper B (`tex/slackMCA_v4.tex`, Theorem `thm:qcore`).

This note discharges the roadmap node `list_planted_arithmetic` in the
conservative sense used here: it compiles the exact quotient-core planted lower
counts and the `2^-128` budget-window arithmetic. It does **not** prove the
matching safe-side `ImgFib` upper bound, and it does not bound non-planted
sunflower or petal extras.

## Object

Let `C = RS[F_q,H,k]` with `|H| = n`, let `rho = k/n`, and write the list
agreement as

```text
s = k + sigma.
```

The list radius is `1 - rho - sigma/n`. The challenge budget used by this
compiler is

```text
B*(q_list) = floor(q_list / 2^128).
```

The exact list object is the image fiber `ImgFib_U(s)` from Paper B:

```text
|List(y,1-s/n)| = |ImgFib_U(s)|.
```

The compiler below is a lower-bound certificate: it exhibits a planted received
word and codewords, then compares the planted count to `B*(q_list)`.

## Theorem

For every divisor `M | gcd(n,k)` satisfying

```text
1 <= sigma < M,        k/M <= n/M - 1,
```

there is a received word with at least

```text
P_M(n,k) = binom(n/M - 1, k/M)
```

codewords agreeing on `k+sigma` positions. Consequently

```text
Lst(C,1-rho-sigma/n)
  >= max_{M | gcd(n,k), sigma < M, k/M <= n/M - 1}
       binom(n/M - 1, k/M).
```

In particular, the planted quotient-core certificate proves the list row unsafe
whenever

```text
max_M binom(n/M - 1, k/M) > floor(q_list / 2^128).
```

## Proof

The first displayed lower bound is exactly Paper B Theorem `thm:qcore`: choose
a subgroup `K <= H` of order `M`, one `K`-coset `C_0`, and a set
`T subset C_0` of size `sigma`. For every `k/M`-subset of the quotient
`H/K \ {C_0}`, the quotient-core construction gives a distinct degree-`<k`
codeword agreeing with the planted received word on `k+sigma` coordinates. This
gives `binom(n/M - 1,k/M)` distinct codewords.

Taking the maximum over active quotient-core scales gives the compiled lower
bound. The unsafe test is just the integer comparison with
`floor(q_list/2^128)`.

## Dyadic Deployed Rates

For `n = 2^m` and the official rates `rho in {1/2,1/4,1/8,1/16}`, the active
scales can be indexed by the quotient order `N = n/M`. At rate `rho`, scale
`N` contributes

```text
binom(N - 1, rho N)
```

when `sigma < n/N`. The verifier computes the exact first dyadic quotient
order whose planted count beats each budget.

For budget `2^128-1`, the first unsafe quotient orders are:

```text
rho = 1/2:   N = 256
rho = 1/4:   N = 256
rho = 1/8:   N = 256
rho = 1/16:  N = 512
```

Thus, for example, at rates `1/2`, `1/4`, and `1/8`, the planted lower
certificate is already over the `2^-128` budget whenever `sigma < n/256`; at
rate `1/16`, the corresponding dyadic lower certificate starts at
`sigma < n/512`.

These are lower-side certificates only. Above the displayed boundary the
quotient-core plant at that dyadic order deactivates; proving safety requires
the repaired `ImgFib` theorem and the non-planted extras ledger.

## Diophantine Budget Windows

For exact planted counts `L < P`, the budget window

```text
floor(q_list / 2^128) in [L, P)
```

is exactly the field-size interval

```text
L*2^128 <= q_list <= P*2^128 - 1.
```

The verifier records these intervals for the adjacent dyadic planted counts at
each official rate and budget size. No finite-field residue or zone-b value-set
test appears on the list side: once the planted word is constructed, the
certificate is exact integer arithmetic.

## Reproducibility

Regenerate the certificate:

```bash
python3 experimental/scripts/verify_list_planted_arithmetic_compiler.py --emit
```

Replay it:

```bash
python3 experimental/scripts/verify_list_planted_arithmetic_compiler.py \
  --check experimental/data/certificates/list-planted-arithmetic/list_planted_arithmetic_compiler.json
```

The script is stdlib-only and uses exact integer arithmetic throughout.

