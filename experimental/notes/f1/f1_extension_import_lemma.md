# F1: extension-import lemma

- **Status:** PROVED arithmetic lemma + verifier.
- **Agent/model:** Codex, acting autonomously for AllenGrahamHart.
- **Date:** 2026-07-02.
- **DAG target:** `ext_import`.
- **Verifier:** `experimental/scripts/verify_f1_extension_import_lemma.py`.
- **Artifact:** `experimental/data/certificates/f1-extension-import/f1_extension_import_certificate.json`.

## Statement

Let `B <= F` be fields.  There are two separate extension-line facts that must
not be conflated.

### 1. Base-rational pencils have only base-field isolated slopes

Let `a_i,b_i in B`.  Consider the affine linear conditions

```text
a_i + z b_i = 0,        z in F.
```

If the solution set is a singleton, then the solution lies in `B`.  Indeed, for
some `b_i != 0`,

```text
z = -a_i / b_i in B.
```

If no such `b_i` exists, the solution set is either empty or all of `F`,
depending on whether every `a_i` is zero.  Therefore a genuinely `F \ B` bad
slope cannot be produced by an otherwise `B`-rational nondegenerate pencil just
by enlarging the slope field.

### 2. Extension-pole numerators have an exact threshold

For a proper extension sampling field with

```text
q = |F|,        b = |B|,        X = q-b,
```

Paper D's extension-pole conversion gives the numerator

```text
N_ext(L) = ceil( L X / (X + k L) )
```

from a base list of size `L`.  Against a denominator budget

```text
B* = floor(q / 2^lambda),
```

the exact crossing threshold is:

```text
if X - B* k <= 0:
    no L crosses the budget, since N_ext(L) <= floor(X/k) <= B*
else:
    min { L : N_ext(L) > B* }
      =
    floor( B* X / (X - B* k) ) + 1.
```

This is the safe way to import list-side lower floors into an extension-line
MCA ledger: the extension denominator is printed, and the threshold is computed
from the actual `(q,b,k,L)` rather than by replacing a generated-field ledger
with the largest available field.

## Consequence

The F1 extension lane has a clean split:

```text
B-rational pencil data  -> isolated slopes stay in B;
extension-pole data     -> counted by N_ext(L) with q_line=|F|;
general F-valued data   -> still needs the F1 safe-side classification.
```

The lemma does not prove that every `F`-valued bad slope is extension-pole or
subfield-confined.  It only proves the denominator accounting and the trivial
base-rational confinement needed before an extension-valued packet can be used
in a prize-facing ledger.

## Reproduce

```bash
python3 experimental/scripts/verify_f1_extension_import_lemma.py --emit
python3 experimental/scripts/verify_f1_extension_import_lemma.py
```
