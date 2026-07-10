# Extension-pole conversion identity (rem:capf-extension-main)

**Status:** EXPERIMENTAL / AUDIT  
**Verdict:** `NO ISSUE`  
**Object:** `prop:capf-extension` ExtPole formula + evaluation conversion kappa  
**Evidence type:** `ORACLE_GATED_VS_COMMITTED_VALUE`

## Primary finding

The sharp conversion numerator

```text
ExtPole(L, m, kappa) = ceil( L * m / (m + kappa*(L-1)) )
```

with `m = q_line − q_gen` matches the integer menu; it is always at least the weak
`ceil(L m / (m + kappa L))` fallback. Distinct degree-`<k` polynomials over prime
fields agree in at most `k−1` points (kappa bound for ordinary RS lists). Oracle
`L=2,m=3,kappa=1 → 2` holds. This confirms the arithmetic of the conversion
certificate; it does not re-prove the extension-pole floor theorem.

## Non-claims

Not a full extension-field MCA witness construction; not a deployed-row payment.
