# Quotient-Profile Dimension-Dither Scanner

**Status:** AUDIT / EXPERIMENTAL.

This note accompanies `experimental/scripts/quotient_profile_dither.py`.  It
implements the finite-length divisor scan requested by the L3 target in
`agents.md`: compare exact-rate dimensions `k0=rho*n` against dithered
dimensions `k=k0-r` on dyadic domains `n=2^m`.

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
python3 experimental/scripts/quotient_profile_dither.py --m-min 8 --m-max 12
python3 experimental/scripts/quotient_profile_dither.py --m-min 8 --m-max 12 --format json
python3 experimental/scripts/quotient_profile_dither.py --rates 1/2 --etas 1/64 --max-dither 16
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
python3 experimental/scripts/quotient_profile_dither.py \
  --rates 1/2 --etas 1/64 --m-min 8 --m-max 12 \
  --max-dither 16 --slack-window 1:16
```

For each fixed dimension dither `r` and dyadic quotient scale `M`, this mode
reports the first-exchange whole-fiber quotient ledger proved in
`experimental/notes/m1/m1_quotient_periodic_overlap_profile.md`:

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

The M1 note also proves a general quotient-fiber occupancy formula. For any
histogram `h=(h_0,...,h_M)` of fiber occupancies, the strict exchange ledger is
the coefficient of a finite product of one-fiber transition polynomials. The
current scanner reports the whole-fiber and one-remainder classes explicitly;
`experimental/scripts/m1_occupancy_profile_scan.py` gives the theorem-backed
complete histogram scanner for small quotient partitions, including the exact
cross-histogram union ledger. This accounts for quotient-fiber content classes
and their cross-content transitions before any remaining obstruction is treated
as aperiodic.

The JSON output also includes a theorem-backed `fixed_window_minimax` block.
For a window `W={t_-,...,t_+}` of length `L_W`, it records the two elementary
minimax radii

```text
min_{r in Z} max_{t in W} |t-r| = floor(L_W/2),
min_{r notin W} max_{t in W} |t-r| = L_W.
```

The first number is the center-dither radius, but any center dither has an
exact-`k0` slack inside the window. The second number is the unavoidable
endpoint gap if the fixed dither avoids such an exact-support slack. When that
endpoint is stable-eligible, the M1 note turns the gap into a binomial
large-scale one-remainder tail of degree `L_W`. The scanner also reports the
best radii among the actually scanned dithers `0 <= r <= max_dither`.

If a target stable gap is supplied, the same mode reports the finite-menu
covering bound:

```bash
python3 experimental/scripts/quotient_profile_dither.py \
  --rates 1/2 --etas 1/64 --m-min 8 --m-max 12 \
  --max-dither 16 --slack-window 1:16 --target-stable-gap 2
```

For `D=target_stable_gap`, the exact safe covering capacity of a `C`-value
dither menu is

```text
Cap(C,D) = floor(C/2)(3D+1) + (C mod 2)D.
```

This accounts for the forbidden exact-support point `t=r`: a pair of dithers
can safely cover `3D+1` consecutive slacks, while a leftover single dither can
cover `D`. The scanner reports the exact minimum menu size needed for
`Cap(C,D) >= |W|`, plus an explicit capacity-achieving construction.

Equivalently, for a target gap `D`, the exact minimum menu size is

```text
min(
  2 ceil(|W|/(3D+1)),
  2 ceil(max(0,|W|-D)/(3D+1)) + 1
).
```

For a fixed menu size `C`, with `p=floor(C/2)` and `eps=C mod 2`, the exact
forced safe gap is

```text
max(1, ceil((|W|-p)/(3p+eps))).
```

The same summary also reports the exact menu size needed for asymptotic
adaptive competitiveness over an unbounded dyadic quotient hierarchy. This is
the gap-one inverse `exact_min_menu_size_for_asymptotic_adaptive_competitiveness`.
For a length-`|W|` window, it is the minimum `C` with `Cap(C,1) >= |W|`. A
queried menu has `queried_menu_asymptotically_adaptive_competitive=true`
exactly when its forced safe gap is one; otherwise a forced gap at least two
eventually creates a finite-menu tail above the adaptive maximal-dither
baseline. The field `adaptive_competitive_construction_dithers` gives an
explicit gap-one menu attaining this threshold.
For a queried menu, `large_scale_menu_regime` records the dichotomy:
`finite_prefix_linear` means all nonlinear large-scale dyadic tails are
confined to `M <= slack_window.end`, while `forced_superlinear_tail` means the
forced gap is at least two and a super-linear stable tail appears at large
dyadic scales. The field `forced_tail_binomial_degree` records that forced
stable-tail degree.

Adding a menu size turns this into a per-parameter stable-tail lower-bound
certificate:

```bash
python3 experimental/scripts/quotient_profile_dither.py \
  --rates 1/2 --etas 1/64 --m-min 8 --m-max 12 \
  --max-dither 16 --slack-window 5:12 \
  --target-stable-gap 3 --dither-menu-size 2
```

For a menu of size `C`, the forced safe gap is
`E=min{D': |W| <= Cap(C,D')}`. When `D<t_-`, every dyadic scale
`M >= t_+ + D` has a theorem-backed lower bound

```text
min(k0/M,(n-k0)/M) binom(M,E) - 1
```

for some slack served by the menu. JSON output stores this as
`dither_menu_tail_lower_bound` on each scanned case. If `--line-field-size q`
is also supplied, the scanner multiplies the mass floor by `q^(t_- - D)` and
reports `stable_tail_weighted_lower_bound`; this is the conservative
random-line variance numerator forced by the finite menu.

For comparison, each slack-window case also reports
`adaptive_maximal_window_baseline`. This is the per-slack rule `r(t)=t-1`.
At every dyadic scale `M>t_+`, it gives the uniform large-scale profile

```text
H_REM^{<t}(y) = (n-k0-1)y,
R_REM(t,q) = (n-k0-1)q^(t-1),
```

so the maximum weighted correction across the window is
`(n-k0-1)q^(t_+-1)`. This baseline is the reference point for comparing a
bounded dither menu against genuinely adaptive dimension choices.
The menu-tail entries also include `log2_mass_over_adaptive_linear`; positive
values identify stable scales where the finite-menu floor is already larger
than the adaptive linear mass. With `--line-field-size q`, the
`log2_same_slack_weighted_over_adaptive` field gives the conservative
same-slack weighted comparison.
The summary fields `min_scale_mass_dominates_adaptive_linear` and
`min_scale_same_slack_weighted_dominates_adaptive` report the first stable
dyadic quotient scale where these comparisons become positive.
The field `log2_window_weighted_over_adaptive` uses the more conservative
comparison against the maximum adaptive weighted correction over the whole
slack window, and `min_scale_window_weighted_dominates_adaptive` reports the
first scale where that window-level comparison becomes positive.

Entries marked `stable_large_scale_formula` lie in the range

```text
d = t-r,        1 <= d < t,        M >= t+d.
```

There the scanner is using the closed mass

```text
((n-k0)/M) binom(M,d) - 1.
```

In particular, if a fixed dither is maximal at slack `t0`, then at the adjacent
slack `t0+1` one has `d=2`, and every dyadic scale `M >= t0+3` has stable mass

```text
(n-k0)(M-1)/2 - 1.
```

This is the executable form of the fixed-window remainder obstruction: a
single fixed dither cannot keep all adjacent large-scale remainder packets in
the linear maximal-dither regime.

If a line-field size is supplied, the scanner also evaluates the stable
large-scale random-line correction from the M1 note:

```bash
python3 experimental/scripts/quotient_profile_dither.py \
  --rates 1/2 --etas 1/64 --m-min 8 --m-max 12 \
  --max-dither 16 --slack-window 1:16 --line-field-size 17
```

For stable one-remainder entries with `d=t-r`, `e=|d|`, and `M>=t+e`, the
reported weighted term is

```text
sum_{ell=1}^e binom(e,ell) binom(M-e,ell) q_line^(t-ell)
  + C_side binom(M,e) q_line^(t-e),
```

with `C_side=(n-k0)/M-1` above the dither and `C_side=k0/M-1` below it.  The
JSON field `max_log2_stable_weighted_correction` lets fixed dither choices be
ranked by the actual random-line variance numerator, not only by unweighted
remainder mass.
