# A0 Crites-Stewart Import Audit

**Status:** AUDIT.

This note audits the local use of the Crites-Stewart list-to-agreement
conversion in `tex/cs25_cap_v4.tex` and `tex/slackMCA_v3.tex`.  It does not
certify that the external theorem matches the local restatement.  The primary
source must still be checked manually against Crites--Stewart, ePrint 2025/2046,
and the ABF restatement cited by the manuscripts.

## Local Import Sites

Paper D states the imported theorem as:

```text
C = RS[F,D,k], C+ = RS[F,D,k+1], delta in (0,dmin(C)), eta in [0,1).
If eca(C,delta) <= eta * (1/k - n/(k|F|)),
then Lst(C+,delta) <= ceil(|F| * eca(C,delta) / (1-eta)).
```

Paper B keeps an older, looser version:

```text
C = RS[F_q,D,k], delta in (0,1-rho].
If eca(C,delta) <= eta * (1/k - n/(kq)),
then the relevant augmented code C+ has
Lst(C+,delta) <= ceil(q * eca(C,delta) / (1-eta)).
```

The Paper D version is the more precise local interface: it names
`C+=RS[F,D,k+1]` and uses the admissible range `delta in (0,dmin(C))`.

## Internal Checks

The eta-`1/2` contrapositive used in Paper D is algebraically consistent with
the displayed imported inequality.  If

```text
eca(C,delta) <= (1/(2k)) * (1 - n/q),
```

then applying the imported theorem with conversion parameter `eta=1/2` gives

```text
Lst(C+,delta) <= ceil(2q * eca(C,delta))
               <= ceil((q-n)/k)
               < q/k + 1.
```

Therefore any lower bound `Lst(C+,delta) >= q/k + 1` contradicts the small-CA
hypothesis and yields

```text
eca(C,delta) > (1/(2k)) * (1 - n/q).
```

The Paper D slack-two fiber construction is shaped to produce codewords inside
`C+=RS[F,D,k+1]`, so it does not rely only on the subcode monotonicity
`Lst(C,delta) <= Lst(C+,delta)`.  Paper B's older quotient-core cap does rely
on that monotonicity, which is valid once `C subset C+` is the intended
augmentation.

The local chain from CA to MCA is also internally explicit:

```text
eca(C,delta) <= emca(C,delta).
```

Thus the cap proof only needs the imported displayed implication plus this
local CA-to-MCA fact.

## Deep-Point MCA Cap Split

The original Paper D proof route above remains conditional on the imported
CS25/ABF implication.  However, the X1 deep-point route gives a separate local
proof of the same headline MCA cap constant.  The dependency-split note now
spells out the elementary `lem:fiber(ii)` lower bound, the simple-pole transfer,
deep-point averaging, and the scalar algebra.

The local algebra is:

```text
L >= q/k + 1,
M >= L/(1+k(L-1)/(q-n))
  ==>  M/q > (1/(2k))(1-n/q).
```

Indeed, after cancelling `(q-n)/q`, the strict comparison is equivalent to

```text
kL - q + n + k > 0,
```

which follows from `kL >= q+k`.  Thus the elementary fiber lower bound plus the
simple-pole transfer and deep-point averaging can produce the same `emca` lower
bound without invoking CS25.
See `experimental/notes/audits/a0_deep_point_cap_dependency_split.md` and
`experimental/scripts/verify_a0_deep_point_cap_algebra.py`; the finite fiber
model is checked by `experimental/scripts/verify_x1_lem_fiber.py`.

## Unresolved External Checks

The following items remain open until the external theorem is checked directly:

- **Radius range:** Paper D needs `delta in (0,dmin(C))` for all cap uses.
  Confirm CS25/ABF allows this exact range, or record any endpoint or
  proximity-loss correction.
- **Augmented code:** Paper D uses `C+=RS[F,D,k+1]`.  Confirm the external
  `C+` is exactly this degree-rung augmentation.
- **CA normalization:** Local `eca` is a probability over uniform `gamma in F`.
  Confirm the external theorem uses the same normalization and no extra scaling.
- **Sampling field:** Local denominator is `|F|=q`, the line field.  Confirm
  the external theorem samples the agreement parameter from this same field.
- **Conversion parameter:** Local proofs set the import parameter to
  `eta=1/2`.  Confirm the theorem permits `eta=1/2` and has the factor
  `1/(1-eta)` exactly.
- **List object:** Local conclusion is worst-case list size at radius `delta`.
  Confirm whether the external list is for `C+`, `C`, or an augmented/extended
  presentation with additional hypotheses.

## Recommended Local Cleanup

1. Prefer the Paper D restatement when citing the import inside this repository.
2. Rename the import's parameter from `eta` to `theta` in future notes or
   scripts, to avoid confusing it with the reserve `eta=1-rho-delta`.
3. Treat the original CS25-based cap proof and any direct use of the imported
   theorem as conditional until the six unresolved checks above are discharged.
   For the headline MCA cap, cite the deep-point dependency split separately.
4. If the external theorem only gives a constant-factor variant, the cap still
   survives qualitatively, but the displayed error constant should be recomputed
   rather than quoted from the CS25 route as `1/(2k) * (1-n/q)`.

## Audit Outcome

The internal algebra of the Paper D CS25 composition is coherent conditional
on the displayed imported theorem.  The import does **not** yet match exactly
from the evidence in this repository alone: the exact external radius range,
augmented code definition, CA normalization, sampling field, and constants
still require direct source verification.

The headline MCA cap now has a separate local dependency path through the
deep-point line.  That path does not source-certify CS25; it narrows what A0
still needs to audit by separating the original imported proof from the local
deep-point proof.
