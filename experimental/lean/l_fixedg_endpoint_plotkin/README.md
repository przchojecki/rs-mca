# Lane L fixed-G ordinary endpoint package

This stdlib-only Lean package is the arithmetic shadow of

```text
experimental/notes/thresholds/m31_fixed_g_boundary_endpoint_plotkin_v1.md
```

It freezes the two ordinary Reed--Solomon boundary rows
`(d,m)=(5412,72859)` and `(840823,908270)` at
`R=981129`, `w=67447`, and proves the exact arithmetic needed by the
one-coordinate Plotkin argument:

- exact finite-`p`, target-list Johnson grid boundaries and post-Johnson gaps;
- the shortened constant-weight Plotkin numerator, positive denominator,
  quotient, and remainder;
- arithmetic implications from the cross-multiplied Plotkin and incidence
  inequalities to ordinary list size at most `2310492`;
- the `B* - 1` safety margin and fixed-`G` zero-anchor add-back;
- the adjacent-shell failure of one shortening and the exact two-shortening
  route-stop cap.

The coding-theory proof is in the note.  This package does not axiomatize or
claim a kernel proof of the polynomial root bound, incidence averaging, or the
constant-weight double count.

## Trust boundary

- Lean stdlib only; no Mathlib.
- No `sorry` and no custom axioms.
- `native_decide` is used only for closed natural-number propositions.
- The two variable arithmetic implications use the stdlib `omega` tactic.
- Every theorem has a `#print axioms` census.

## Build target

```text
lake build LFixedGEndpointPlotkin
```
