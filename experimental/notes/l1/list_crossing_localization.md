# List Crossing Localization

- **Status:** PROVED / toy endpoint replay.
- **Agent:** Codex acting autonomously for Allen Graham Hart.
- **Roadmap/DAG node:** `list_crossing_localization`.
- **Verifier:** `experimental/scripts/verify_list_crossing_localization.py`.
- **Artifact:** `experimental/data/certificates/list-crossing-localization/list_crossing_localization.json`.

This note records the elementary list-side analogue of the MCA staircase
localization.  It does not prove a safe-side image-fiber upper bound.  It says
that once a lower certificate and an upper certificate bracket the budget, the
integer list threshold is pinned by adjacent agreement levels.

## Statement

Let `C` be a finite code of length `n` over a finite alphabet, and fix the
usual closed agreement predicate.  For integer agreement `a`, define

```text
L_C(a) = sup_U #{c in C : agreement(c,U) >= a}.
```

For a budget `B >= 0`, the safe set

```text
Safe_B = {a : L_C(a) <= B}
```

is upward closed in `a`.  If both `Safe_B` and its complement are nonempty,
then

```text
a_* = min Safe_B
```

is well-defined, `a_*` is safe, and `a_*-1` is unsafe.  Equivalently, the
closed-radius staircase is pinned at the adjacent radii

```text
r_safe = n-a_*,
r_unsafe = n-a_*+1.
```

The same proof applies to interleaved list objects, extension-code list
objects, and any finite list object whose predicate is agreement at least `a`.

## Proof

If `a <= b`, then every codeword agreeing with `U` on at least `b` positions
also agrees with `U` on at least `a` positions.  Hence, for every received word
`U`,

```text
#{c : agreement(c,U) >= b} <= #{c : agreement(c,U) >= a}.
```

Taking the supremum over `U` gives

```text
L_C(b) <= L_C(a).
```

Thus `L_C(a)` is integer-valued and nonincreasing in `a`, so `Safe_B` is
upward closed.  If safe and unsafe levels both occur, the first safe level
`a_*` exists in the finite set `{0,...,n}`.  Minimality gives
`a_*-1` unsafe, while the definition gives `a_*` safe.

## Endpoint Replay

The verifier exhaustively enumerates the toy code

```text
C = RS[F_5, {0,1,2,3}, 2]
```

and all `5^4` received words.  With budget `B=1`, it computes the whole
staircase and checks that the first safe level and its predecessor form an
adjacent crossing.  This replay is included only to fix the endpoint convention
and to guard against off-by-one mistakes in certificate consumers.

Replay:

```bash
python3 experimental/scripts/verify_list_crossing_localization.py --emit
python3 experimental/scripts/verify_list_crossing_localization.py \
  --check experimental/data/certificates/list-crossing-localization/list_crossing_localization.json
```
