# Lane L fixed-G adjacent-interior Hahn package

This stdlib-only Lean package is the replay layer for

```text
experimental/notes/thresholds/l_fixedg_adjacent_hahn_stop_v1.md
```

It freezes the first undecided symmetric pair

```text
(d,m) = (5413,72860) / (840822,908269)
N = 981129
w = 67447
D = 67448
B* - 1 = 16777214
```

and checks the arithmetic shadow of the complete Johnson-scheme
Hahn/Delsarte route stop:

- exact finite-`p`, target-list Johnson boundaries and post-Johnson gaps;
- the three active distances and exact positive primal weights;
- the exact positive degree-three dual coefficients and objective;
- the dual factorization/sign on all 5,413 allowed intersections;
- the matching Hahn primal constraints through degree three;
- the recurrence and all 487 exact prefix slacks in degrees 4 through 490;
- the elementary mode, step-ratio, multiplicity, and tail-start integer gates;
- the all-degree LP floor `20,737,821`, its `3,960,607` target excess, and the
  one-hypothesis quarter-gap conditional cap `16,032,481`.

The coding-theory and association-scheme proof is in the note. This package
does not axiomatize or claim a kernel proof of the polynomial root bound,
Delsarte positivity, Hahn orthogonality, weighted Cauchy, or weak duality.

## Trust boundary

- Lean stdlib only; no Mathlib.
- No `sorry` and no custom axioms.
- `native_decide` is used for closed natural-, integer-, rational-, and
  finite-list propositions, including the finite scans.
- Two variable floor implications use the stdlib `omega` tactic.
- Every theorem has a `#print axioms` census.
- There is no Python verifier in the packet.

## Build target

```text
lake build LFixedGAdjacentHahnStop
```
