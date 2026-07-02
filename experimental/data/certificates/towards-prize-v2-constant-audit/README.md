# Towards-Prize v2 Constant Audit

This packet records the constants used by the promoted `tex/towards-prize.tex`
v2 ordinary-locator and quadratic-envelope checks.

Replay:

```bash
python3 experimental/scripts/verify_towards_prize_v2_constants.py
```

The verifier uses exact integer arithmetic for the cap-criterion inequalities
at `n=2^15`, `q=2^256-1`, and checks the rational side conditions such as
`alpha_rho > g_rho`.
