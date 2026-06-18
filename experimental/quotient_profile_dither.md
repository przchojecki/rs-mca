# Quotient-Profile Dimension-Dither Scanner

**Status:** AUDIT / EXPERIMENTAL.

This note accompanies `experimental/quotient_profile_dither.py`.  It implements the
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
python3 experimental/quotient_profile_dither.py --m-min 8 --m-max 12
python3 experimental/quotient_profile_dither.py --m-min 8 --m-max 12 --format json
python3 experimental/quotient_profile_dither.py --rates 1/2 --etas 1/64 --max-dither 16
```

The default scan covers `m=8..20`, rates `1/2,1/4,1/8,1/16`, reserves
`1/64,1/32,1/16`, and dithers `0..16`.  The output is deterministic and uses no
random seed.

This is not a proof of the corrected local-limit conjecture.  Passing this scan
means only that the explicit quotient-core obstructions represented by the
printed profile are absent or budgeted at the scanned finite parameters.

## Slack-Window Ledger Mode

The script also has a theorem-backed window mode:

```bash
python3 experimental/quotient_profile_dither.py \
  --rates 1/2 --etas 1/64 --m-min 8 --m-max 12 \
  --max-dither 16 --slack-window 1:16
```

For each fixed dimension dither `r` and dyadic quotient scale `M`, this mode
reports the first-exchange whole-fiber quotient ledger proved in
`experimental/m1_quotient_periodic_overlap_profile.md`:

```text
L_win(r) = {
  (t,M) : t in W, M | k0, M > 1,
          t >= M+1, M <= k0+t-r <= n-M, t == r mod M
}.
```

The entry `(t,M)` contributes first-exchange codegree

```text
((k0+t-r)/M)(n/M - (k0+t-r)/M)
```

to the quotient-periodic support ledger.  The text output reports the best
fixed dither by the maximum active first-exchange codegree in the requested
window; JSON output includes the retained active entries under
`slack_window_ledger`.

The same mode also reports a one-remainder ledger.  For a fixed dither, slack,
and dyadic scale, put

```text
s = k0+t-r,        b = s mod M.
```

If `b != 0`, the script evaluates the proved one-remainder enumerator
`H_REM(y)` and sums exactly the strict coefficients

```text
sum_{1 <= j < t} [y^j] H_REM(y).
```

This is reported as `remainder_window_ledger`.  In the large-fiber range
`t <= M`, it is the closed three-term truncation from the M1 quotient-profile
note; for small scales, the script still uses the exact `H_REM` formula but
only iterates terms whose exponent can lie below `t`.

This distinction matters when comparing fixed dithers across a slack window:
an odd dither can remove whole-fiber dyadic scales at one slack, while the
nonzero one-remainder packet may still carry a much larger strict codegree mass
at nearby slacks.
