# S6: the extension lift — F-valued slopes, and how the list threshold enters MCA

- **Status:** PROVED-cited floor + verified arithmetic + classification
  CONJECTURE. NOT rigorous as a whole.
- **Parent:** `prize_proof_sketch_spine.md` S6. Numerics machine-checked.

## 1. The trivial half of the lift [elementary]

Let `B = F_p(D)` be the generated field, `F ⊇ B` the ambient/sampling field.
The alignment pencil is linear with coefficients `a(l), b(l)` built from the
pair's syndromes: if the PAIR (and hence its syndromes) is `B`-rational,
then every aligned slope `Z = -a_r/b_r` lies in `B` automatically. So
`B`-rational data cannot produce genuinely `F`-valued bad slopes — those
require either `F`-valued words or the pole mechanism below. This is the
sense in which the lift is "free" for generating rows and the reason the
classification (§4) is a Galois-descent question about the pencil data.

## 2. The pole mechanism imports the LIST threshold into MCA [verified]

Paper D v10's extension-pole floor converts a base list of size `L` into
genuinely `F`-valued witness lines with numerator
`N(L) = ceil(L(|F|-|B|)/(|F|-|B|+kL))`. Verified behavior:

```text
N(L) ~ L below the saturation cap X/k ~ 2^216 (X = |F|-|B|, k = 2^40),
essentially independent of |B|; gate crossing N > |F| 2^-128 = 2^128
happens exactly when the BASE LIST crosses L ~ 2^128.
```

Consequence (the node's headline): **B_ext crosses the MCA gate precisely
at the list-side crossing window of S7** (`slack in [H/256, H/128]` of the
base row). The extension mechanism is the channel through which grand
challenge 2's threshold enters grand challenge 1's ledger. Since the S7
window sits farther from capacity than the MCA quotient corridor (S2), for
rows where the mechanism is live it BINDS:

```text
delta*_MCA(row) = min( MCA corridor (S2),  imported list window (S7) )
                = the imported list window,   when F \ B is nonempty.
```

## 3. When is the mechanism live? Generating rows escape it [verified]

The pole needs `F \ B` nonempty, i.e. a NON-generating row (`q_gen <
q_line`). Admissibility forces such rows to be tiny at the base: `q_line =
q_gen^m` with `m >= 2` and `q_line < 2^256` give

```text
q_gen < 2^128   =>   base gate B*_gen = floor(q_gen/2^128) <= 1,
                     base reserve tau*(rho, q_gen) >= H(rho)/128 (doubled).
```

For PRIME fields the question vanishes (no proper subfields); for extension
rows the minimal field containing `mu_n` is `F_p^ord` and the pinned row is
exactly the generating case (`ord(17 mod 512) = 32`, turn 7). So:

```text
generating rows  (q_gen = q_line):  B_ext degenerate; S2 corridor stands.
non-generating rows:                the imported S7 window binds, and it is
                                    WIDE (base reserve doubled).
```

Submission guidance falling out of the sketch: prize rows should be chosen
GENERATING; "domain generates F" joins the S5 hypothesis table as the
favorable hypothesis, and WP-0.2 should check whether the official family
even admits non-generating rows.

## 4. Safe-side classification [CONJECTURE — the remaining F1 content]

```text
Claim: every F-valued bad slope above the corrected reserve is
 (i)   B-pencil-rational (Z in B; paid by the base ledgers), or
 (ii)  extension-pole type (paid by B_ext = the imported list term), or
 (iii) subfield-confined to some intermediate B <= K <= F (priced per K by
       the same two mechanisms one level up — the tower recursion).
```

Route: the confinement theorem generalizes fieldwise (pencil rational over
`K` => slopes in `K`); the classification is "which `K` the pair's pencil
data generates" — a Galois-descent stratification of pairs, consuming the
X1 bridge-loss table (WP-6.3). The e-fold structure is already reduced:
my x1 §2.9-2.10 (on main) writes an F-line as an `M_z`-coupled slice of the
e-fold interleaved base object, realized explicitly over `F_17^2` — so
case (ii) is list-controlled by S7's interleaved machinery with `mu = e`.

**Calibration [PROVED-cited, my #103 audit]:** the sigma=1 counterexample
over `F_p^2` gives `emca >= C(p-a+1, 2)/p^2` (0.298 and 0.266 at the two
audited toys) — the mechanism is real, at exactly the e=2 pairs-of-poles
shape the slicing predicts. The Lean F1 extension ledger (on main) is
formalization support for precisely the case split above.

## 5. Forks

```text
F1: a genuinely-F obstruction NOT of pole/confined type -> new ledger
    column (S9); the Lean-ledger case split is the honest place it would
    first fail to typecheck.
F2: the official family admits non-generating rows -> the dossier's
    per-rate tables must carry the imported window as the binding column;
    if it does NOT, S6 reduces to the generating case and this node's
    content is a guard, not a term. (WP-0.2 decides.)
F3: the tower case (iii) at depth: intermediate fields between B and F
    exist only for composite m; each level multiplies bookkeeping but the
    mechanism is the same two-case split — no new mathematics expected,
    but the checker must enforce per-level denominators (q_K printed).
F4: saturation regime (kL >> |F|): N caps at ~2^216 >> 2^128 — saturation
    never rescues safety at the gate; recorded to preempt a false hope.
```
