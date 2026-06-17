# Quotient-Profile Dimension-Dither Scanner

**Status:** AUDIT / EXPERIMENTAL.

This note accompanies `experimental/quotient_profile.py`.  It implements the
finite-length divisor scan requested by the L3 target in `agents.md`: compare
exact-rate dimensions `k0=rho*n` against dithered dimensions `k=k0-r` on dyadic
domains `n=2^m`.

The theorem-backed quantity is the exact-divisibility profile from
`tex/snarks_v4.tex`:

```text
Qprof_H(a,k)
  = max log2 binom(n/M - 1, k/M)
```

where the maximum ranges over divisors `M | gcd(n,k)` with `M>1`, `a-k<M`, and
`k/M <= n/M - 1`.  The script sets `a=k+sigma`, with
`sigma=ceil(eta*n)`, and reports the active quotient scales.

The script also reports a separate remainder diagnostic from the quotient
hygiene discussion.  For a quotient scale `M`, write

```text
k = M floor(k/M) + rem.
```

The remainder variant can reach target slack `sigma` by using a support of size
`sigma+rem` inside one `M`-coset, so it remains potentially active when
`sigma+rem<M`.  This diagnostic is useful for checking that one-step dithering
`k=rho*n-1` not only empties the exact profile on dyadic domains, but also gives
maximal remainders at the quotient scales that divided the original deployed
dimension.

Example commands:

```bash
python3 experimental/quotient_profile.py --m-min 8 --m-max 12
python3 experimental/quotient_profile.py --m-min 8 --m-max 12 --format json
python3 experimental/quotient_profile.py --rates 1/2 --etas 1/64 --max-dither 16
```

The default scan covers `m=8..20`, rates `1/2,1/4,1/8,1/16`, reserves
`1/64,1/32,1/16`, and dithers `0..16`.  The output is deterministic and uses no
random seed.

This is not a proof of the corrected local-limit conjecture.  Passing this scan
means only that the explicit quotient-core obstructions represented by the
printed profile are absent or budgeted at the scanned finite parameters.
