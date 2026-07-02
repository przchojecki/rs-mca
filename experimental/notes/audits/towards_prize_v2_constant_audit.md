# Towards-Prize v2 Constant Audit

- **Status:** AUDIT / exact integer replay.
- **Source:** `tex/towards-prize.tex` v2.
- **Packet:** `experimental/data/certificates/towards-prize-v2-constant-audit/towards_prize_v2_constants.json`.
- **Verifier:** `experimental/scripts/verify_towards_prize_v2_constants.py`.

This audit checks the promoted `towards-prize.tex` v2 constants that determine
the new plain-CA unsafe slice:

```text
alpha_{1/2}=1/300, alpha_{1/4}=3/1000,
alpha_{1/8}=41/20000, alpha_{1/16}=3/2500.
```

For each challenge rate, the verifier checks:

1. `alpha_rho > g_rho`, so the ordinary-locator slice is genuinely stronger
   than the older quadratic-envelope gap;
2. `rho + alpha_rho + 2^-15 < 1`, the side condition used in the proof;
3. the exact ordinary-locator cap criterion at `n=2^15`, `q=2^256-1`;
4. the exact quadratic-envelope cap criterion at the same endpoint, matching
   the parenthetical claim in the proof of `cor:envelope`;
5. the worst-case endpoint arithmetic behind
   `(1/(2k))*(1-n/q)>2^-128` for `k<=2^40`, `n<=16k`, `q>=2^128`.

The cap criteria are replayed by integer cross-multiplication.  For instance,

```text
binom(n,k+s) > q^(s-1)(q/k+1)
```

is checked as

```text
binom(n,k+s)*k > q^(s-1)(q+k).
```

## Result

The current packet reports:

```text
implemented PASS: 9   FAIL: 0
```

No arithmetic discrepancy was found.  This audit covers the numerical constants;
it does not by itself audit the residual shortening-image proof or the
doubled-radius pair-list proof.
