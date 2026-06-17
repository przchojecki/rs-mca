# F1 Extension-Line Slope Sweep

**Status:** EXPERIMENTAL / AUDIT.

This note accompanies `experimental/f1_extension_slope_sweep.py`.  It records a
small exact experiment for the F1 problem in `agents.md`: whether extension
valued residue denominators can create bad slopes that are invisible to a
base-field-only MCA search.

The sweep works over `B = F_p` and `F = F_p[u]/(u^2-d)`, with `d` the least
nonsquare modulo `p`.  It uses a multiplicative subgroup `H <= B^*` of size
`n`, the Reed-Solomon dimension parameter `k`, and the denominator family

```text
f_beta(x) = 1 / (x - beta),    beta in F \ B,
g(x) = x^k.
```

For each support `S subset H` of size `k+1`, let `L_S(f_beta)` be the leading
coefficient of the degree `<= k` interpolant through `f_beta` on `S`.  Since
the leading coefficient of the interpolant of `g=x^k` is `1`, exactly one slope

```text
z = -L_S(f_beta)
```

makes `f_beta + z g` agree with a degree `< k` word on that support.  The
script counts the unique slopes obtained from all such supports and separates
`z in B` from genuinely extension-valued `z in F \ B`.

The default cases are intentionally small and exact:

```text
p=5,  n=4, k=2
p=7,  n=6, k=3
p=17, n=8, k=4
```

These are not full reserve-size MCA counterexamples.  They isolate one residue
denominator mechanism and show, in a reproducible finite-field window, that
extension denominators produce many same-support bad slopes outside the base
field.  The `p=17,n=8,k=4` case is especially relevant to the quadratic
extension toy window in the F1 guidance.

Natural next steps are to sweep cubic extensions, vary the direction `g`, move
from minimal supports of size `k+1` to larger supports, and compare the resulting
slopes with residue-line normal forms in the corrected MCA framework.
