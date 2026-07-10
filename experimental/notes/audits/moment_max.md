# moment-max second-opinion (lem:moment-max)

**Status:** EXPERIMENTAL / AUDIT. **Verdict:** NO ISSUE.

Second opinion vs #435 on the moment-max sandwich. Rebased W29 onto frontiers draft base; label pin is L375 (was L165 pre-tex growth).

- generator route: direct Gord average of ratios^q + max sandwich
- checker route: genuine log-sum-exp Gord=exp(logsumexp(q*log r)-log L); sandwich recheck
- payload_sha256: b4f11bf17b1aa8e33f28322a7ce746d11085b483e203af526d16f32977715b48
- n_rows: 16; all_pass after line-pin refresh

## Reproducibility
```
py -3.13 experimental/scripts/verify_moment_max.py --emit-defaults --check
py -3.13 experimental/scripts/verify_moment_max_check.py --check
```