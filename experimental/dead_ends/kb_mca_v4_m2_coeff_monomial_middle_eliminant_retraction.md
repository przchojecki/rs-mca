# Retracted m2 middle-coefficient elimination: the `coeff_monomial` trap

## Status

```text
RETRACTED_INVALID_ELIMINATION_CAUGHT_BEFORE_PUBLICATION
```

This records, in the shared dead-end registry, a computer-algebra error made
and caught inside the KoalaBear `m=2` q-slice campaign on 2026-07-30. The
invalid outputs were retracted the same day, before any DAG status, exported
certificate, or upstream artifact depended on them. It is filed here because
the trap is generic to every sympy-based elimination helper in this program,
including the parallel K3 stacks.

## The trap

`sympy.Poly(expr, b, c, d).coeff_monomial(b)` returns the coefficient of the
**exact monomial** `b*c^0*d^0` — not the full coefficient of `b` as a
polynomial in the remaining variables. Three-line reproduction:

```python
import sympy
b, c = sympy.symbols("b c")
P = sympy.Poly(b*c + 3*b + 5*c + 7, b, c)
P.coeff_monomial(b)          # -> 3          (silently wrong for this use)
sympy.diff(P.as_expr(), b)   # -> c + 3      (the intended object)
```

No exception is raised and the result is a perfectly plausible constant,
which is what makes the failure quiet.

## What it produced, and what was retracted

In the near q-slice elimination the helper used `coeff_monomial(b)` for the
full coefficient of `b` on a selected endpoint line, and therefore
substituted the spurious constants `b=3` and `b=-1` in place of the rational
function `b(c,d)` determined by that line. The formerly printed lex
eliminants and survivor bases derived from those substitutions were
retracted, together with their replay timings, none of which is evidence for
chart deletion. What SURVIVED the retraction, because it predated the
substitution: the endpoint-resultant factors `c=1`, `cd=1`, and
`5cd-4c-4d+5=0`.

## The corrected form

The repaired helper extracts the full coefficient by differentiating in `b`
and re-derives the chart from scratch; its SHA-256 is

```text
830d49882c8183a94442f62862ec9d4a0f5d483466ecb2f1abe4072b04f98860
```

and every subsequently published q-slice exclusion (including the exported
saturated-112 packet) binds this corrected helper or fresh post-retraction
scripts. A repository-wide search confirms `coeff_monomial` appears in no
exported script.

## Suggested guard for elimination helpers

When the full coefficient is intended, use `sympy.diff(P.as_expr(), v)` (for
degree-one `v`) or `sympy.Poly(expr, v).all_coeffs()`, and assert the
extracted coefficient's free symbols are a superset of what the geometry
demands — the spurious constants here would have failed a one-line
`assert extracted.free_symbols >= {c, d}` check.

## Scope

This note deletes nothing, closes nothing, and charges no ledger. It exists
so the next elimination helper in any lane does not re-learn this quietly.
