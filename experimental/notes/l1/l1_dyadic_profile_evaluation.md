# Dyadic Quotient-Profile Evaluation

- **Status:** PROVED / exact arithmetic verifier.
- **Agent:** Codex acting autonomously for Allen Graham Hart.
- **Roadmap/DAG node:** `dyadic_profile_evaluation`.
- **Verifier:** `experimental/scripts/verify_l1_dyadic_profile_evaluation.py`.
- **Artifact:** `experimental/data/certificates/l1-dyadic-profile-evaluation/l1_dyadic_profile_evaluation.json`.

This note isolates the finite divisor-count part of the list-side quotient
ledger.  It does not prove the L1 image-fiber local limit.  Its role is to
make the exact dyadic quotient profile computable, auditable, and independent
of asymptotic entropy estimates.

## Theorem

Let

```text
n = 2^nu,        R in {2,4,8,16},        k = n/R,
a = k + sigma,   sigma = eta n,
```

where `eta` is dyadic and `sigma` is integral.  For the exact-divisibility
quotient profile

```text
Q_H(a,k) = max log2 binom(n/M - 1, k/M)
```

over scales

```text
M | gcd(n,k),  M > 1,  sigma < M,  k/M <= n/M - 1,
```

put `N=n/M`.  Then the active dyadic quotient orders are exactly

```text
N = 2^v,        R <= N,        eta N < 1,
```

and

```text
Q_H(a,k) = max_{N} log2 binom(N-1, N/R),
```

with the empty maximum when no such `N` exists.

## Proof

Since `n` and `k=n/R` are powers of two up to the rate denominator, every
nontrivial divisor `M` of `gcd(n,k)` is dyadic.  Writing `N=n/M`, the condition
`M | k` is equivalent to `R | N`, hence, in the dyadic setting, to `N >= R`.
The strict quotient activity condition is

```text
sigma < M
  <=> eta n < n/N
  <=> eta N < 1.
```

Finally,

```text
k/M = N/R <= N-1
```

for all `R >= 2` and `N >= R`.  Substituting `M=n/N` into the profile formula
gives the displayed maximum.

## One-Step Dither Corollary

If `k0=n/R` and `k=k0-1`, then `k` is odd while `n` is a power of two.  Thus

```text
gcd(n,k)=1,
```

so there is no nontrivial dyadic scale in the exact-divisibility profile.  The
profile is empty for every slack `sigma`.  This is the exact quotient-core
part of the dyadic hygiene rule; it does not by itself rule out unrelated
aperiodic list mechanisms.

## 128-Bit Crossing Table

The verifier computes exact binomial integers.  For a `2^128` list numerator
budget, the first dyadic quotient orders whose exact quotient-core count
exceeds the budget are:

```text
rate 1/2:   N = 256,   unsafe iff eta < 1/256
rate 1/4:   N = 256,   unsafe iff eta < 1/256
rate 1/8:   N = 256,   unsafe iff eta < 1/256
rate 1/16:  N = 512,   unsafe iff eta < 1/512
```

At equality, the scale is not active because the profile condition is strict:
`sigma < M`, equivalently `eta N < 1`.

## Replay

```bash
python3 experimental/scripts/verify_l1_dyadic_profile_evaluation.py --emit
python3 experimental/scripts/verify_l1_dyadic_profile_evaluation.py \
  --check experimental/data/certificates/l1-dyadic-profile-evaluation/l1_dyadic_profile_evaluation.json
```

The certificate also direct-checks the formula against finite divisor scans at
`n=2^12`, `2^20`, and `2^40`, and checks that the one-step dither profile is
empty across the recorded dyadic reserve grid.
