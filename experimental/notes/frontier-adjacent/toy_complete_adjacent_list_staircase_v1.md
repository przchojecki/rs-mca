# Toy complete adjacent LIST staircase certificate (enumerable row)

Status: **PROVED / COMPLETE / NO RESIDUAL** (toy scale, list route). EXPERIMENTAL.

This note ships one fully-worked instance of the prize's core object,
`def:staircase` (`experimental/grande_finale.tex` L120), on the **list route** at
a row small enough that *both* sides of the adjacent inequality are settled by
exact finite certificates that hold for the worst case, with **zero residual or
conditional cells**. It is the first in-repo instantiation of the certificate
condition of the *list-row branch* of `thm:finite` (the adjacent-criterion
compiler, `grande_finale.tex` L1917; stated there for the four deployed rows,
its proof is row-generic via `def:staircase` + `lem:integer-budget`).

Companion artifacts:

```text
experimental/data/certificates/frontier-adjacent/toy_complete_adjacent_list_staircase_v1.json
experimental/scripts/verify_toy_complete_adjacent_list_staircase.py
```

The verifier is zero-arg, stdlib `python3`, runs in < 1 s, and exits 0 only if it
recomputes every number in the packet from scratch (including a full
`C(16,10)=8008`-subset enumeration and a 32-codeword witness reconstruction),
cross-checks the shipped JSON field-by-field, and catches four planted tampers.

## Claim and scope of the "first"

**Claim (EXPERIMENTAL).** This is the repo's first **complete two-sided adjacent
staircase certificate on the list route**: the unsafe side is a *fully enumerated
exact worst-received-word max prefix-fiber* with its entire maximal codeword list
reconstructed and verified (`prop:prefix-witness` realized end-to-end), the safe
side is an *unconditional all-received-words* Johnson packing cell, and there is
no `CONDITIONAL_ON_NAMED_INPUT` branch. Equivalently, it is the first
instantiation of the certificate condition of the **list-row branch** of
`thm:finite`.

**Not claimed (label hygiene against overclaiming).**

- NOT "the first complete adjacent certificate" unqualified. The repo already has
  complete two-sided adjacent staircase certificates on the **LD_sw /
  support-wise-MCA (line-decoding) route**, paid by closed-form or structural
  theorems, at toy through prize scale:
  - `experimental/data/certificates/adjacent-threshold-pins-multirate/adjacent_threshold_pins.json`
    (safe side = exact tangent theorem `LD_sw = n-A+1` at `r=R3=floor((n-k)/3)`;
    64 rows, `n = 2^9 .. 2^21` plus prize scale);
  - `experimental/data/certificates/a426-two-core-exact-threshold-v26/`
    (two-core closure theorem, `r=R3+1`, deployed prime field);
  - `experimental/data/certificates/m1-a407-a408-residual-design-threshold-v1/`
    (exact-support reduction, deployed prime field, status
    `PROVED_ADJACENT_THRESHOLD_ROW`).
  These already instantiate the corresponding condition on the **MCA/LD_sw
  side**. The present packet instantiates the **list branch**, which no prior
  artifact does.
- NOT a closure of any deployed dense-frontier row. Those remain open at
  `prop:q-exact-target` / `prob:row-sharp-q` (see Honest gap).

**Prior list-route status (why the list branch was open).** Every prior
list-route two-sided-shaped packet leaves the safe side OPEN/conditional
(`cap25-v13-identity-frontier`, `frontier-adjacent/{kb,m31}_{list,mca}_v1.packet.json`,
`list-planted-arithmetic`) or is lower-bound / closed-form-count only; none
enumerates the worst received word and reconstructs its codeword list. The only
prior list enumeration-and-dedup artifact,
`experimental/data/certificates/l1-petal-fixed-excess/e15_worst_word_challenge.json`,
is a toy tightness probe explicitly *not* a safe-side proof and *not* framed as an
adjacent budget crossing.

## The row

```text
route         list (base-code list size; K_list = k, no MCA conversion)
F = B         F_17           (beta = log2 17 = 4.087 bits)
D             mu_16 = F_17^x (the full multiplicative group; n = p-1)
n, k, rho     16, 8, 1/2     (K_list = k = 8)
min distance  d = n-k+1 = 9  (unique-decoding agreement threshold 12)
Q_list        p^k = 17^8 = 6 975 757 441   (toy sampler denominator = #codewords)
eps*          2^-29
B*            floor(eps* * Q_list) = floor(17^8 >> 29) = 12
endpoint      closed ball, agreement threshold ">= a" (equality positions counted)
```

`Q_list = p^k` here is a **toy list-denominator convention** (the number of
deg-`<k` codewords); the deployed list rows denominate by the shared
`Q = q_line = |field|^ext` of `prop:q-exact-target`, not by `p^k`.

## The certificate

```text
a0 = 10 (unsafe)              a0 + 1 = 11 (safe)
L(10) = 32  >  B* = 12  >=  U(11) = 7

margins:  unsafe log2(32/12) = 1.415 b
          safe   log2(12/7)  = 0.778 b
          total  log2(32/7)  = 2.193 b
```

**Endpoint radii** (`rem:endpoint`, `grande_finale.tex` L1929):

```text
first proved unsafe closed-grid radius    (n-a0)/n   = 6/16 = 3/8
largest attained safe closed-grid radius  (n-a0-1)/n = 5/16
real-supremum convention: recorded as a real sup over closed integer balls,
  the safe-radius threshold sits at the UPPER EDGE (3/8), not attained at the
  unsafe endpoint; the convention must be printed with the proof.
```

**`thm:finite` instance.** `thm:finite` (L1917) says: if the unsafe inequality at
`a0` is the banked identity-prefix theorem and a proved upper bound gives
`B(a0+1) <= U(a0+1) <= B*`, then the first safe integer agreement is `a0+1` and
`delta*_C(eps*)` is pinned to one integer step under the closed-ball convention.
It is stated there for the four deployed rows; its proof is row-generic via
`def:staircase` + `lem:integer-budget`. This row instantiates the certificate
condition on the list object (both halves proved):
`L(10)=32 > B*=12` (enumerated `prop:prefix-witness` fiber) and
`U(11)=7 <= B*=12` (Johnson packing). Here `U` is a single unconditional cell,
not the deployed first-match ledger of `lem:first-match-ledger`.

## Why each cell is paid

### Unsafe cell -- `L(a0) = 32` -- `PAID_BY_EXACT_CERTIFICATE`

By `prop:prefix-witness` (`grande_finale.tex` L563), for the received word
`U_z(X) = X^a + z_1 X^{a-1} + ... + z_w X^{a-w}` (`w = a-k`), the degree-`<k`
codewords agreeing with `U_z` on `>= a` points are **exactly**
`{U_z - ell_M : M in Fib_w(z)}`, and none agrees on more than `a` points. So the
list-(`>=a`) count for `U_z` equals the prefix-fiber size `|Fib_w(z)|` exactly.

The verifier enumerates all `C(16,10) = 8008` ten-subsets of `D`, buckets them by
their depth-2 signed elementary-symmetric prefix `(e_1, e_2) mod 17` (289
buckets), and takes the heaviest. The maximum fiber is **32**, attained at the
**null prefix** `z* = (0,0)`, i.e. the received word `y = X^10` on `D`. All 32
codewords `c_M = X^10 - ell_M` are reconstructed and checked: each has `deg < 8`
(the shared top three coefficients cancel), each agrees with `y` on **exactly**
10 positions (namely `M`), and all 32 are pairwise **distinct**. Hence
`B_list(10) >= 32`. This is an exact worst-word lower bound, not an average.

### Safe cell -- `U(a0+1) = 7` -- `PAID_BY_EXACT_CERTIFICATE` (all words)

Two distinct degree-`<8` codewords agree on at most `k-1 = 7` points (their
difference is a nonzero polynomial of degree `< 8`). A list of `L` codewords each
agreeing with a received word on `>= 11` points has agreement sets `S_i` with
`|S_i| >= 11` and pairwise `|S_i cap S_j| <= 7`. The Johnson/Cauchy--Schwarz
incidence count gives

```text
L <= n(a-t)/(a^2 - n t) = 16*4/(121 - 112) = 64/9,   so   L <= 7.
```

This is a finite combinatorial theorem valid for **every** received word -- no
fiber, no prefix, no genericity. It is valid because `a0+1 = 11` is **above the
Johnson radius** `sqrt(n(k-1)) = sqrt(112) ~= 10.58` (`a^2 = 121 > n t = 112`);
at `a = 10` the bound is vacuous (`100 < 112`). The unique-decoding cell
(`2a-n > k-1`) is inactive at `a=11` (`2*11-16 = 6 <= 7`); it activates only at
`a >= 12`, where it gives `U = 1`.

Because the entire upper ledger at `a0+1` is this single unconditional
all-words cell, **there is no residual cell**. `residual_cells: []`.

### Dedup

List route: codewords indexed by distinct `m`-subsets `M in Fib_w(z)` are
automatically distinct, since `ell_M = U_z - c_M` recovers `M` as its root set;
the verifier checks `len(set(codewords)) = 32`. No first-match slope collapse is
needed -- that is an MCA-route device.

## Honest gap (labeled claims, not an essay)

- **`no-hard-Q-cell` (SCOPE).** The safe side here is a *word-independent* packing
  cell that exists **only above the Johnson radius**. The four deployed rows sit
  far **below** their Johnson radius, where no universal packing cell exists and
  the safe side genuinely requires `prob:row-sharp-q`. Per `prop:q-exact-target`
  (`grande_finale.tex` L1956), that open cell is a prefix-boundary max-fiber at
  `w = a+ - K = 67471` (KoalaBear) / `67447` (Mersenne-31) whose exact constants
  must fit the printed row margins (`22.20 / 22.01 / 3.26 / 3.07` bits). This toy
  validates the certificate **grammar** end-to-end; it does **not** exercise that
  hard cell.
- **`toy-epsilon` (SCOPE).** `eps* = 2^-29` is non-cryptographic at toy scale
  (`F_17` is far too small for `eps*` to mean protocol soundness). Only the
  integer staircase `L > B* >= U` transfers; the probabilistic reading does not.
  Deployed rows use `eps* in {2^-128, 2^-100}`.
- **`floor-is-not-truth` (DATUM).** The identity-prefix average floor
  `ceil(C(n,a)/p^w) = ceil(8008/289) = 28` is loose; the exact worst-word fiber is
  `32` (`+4` null-prefix excess). The certificate uses the exact enumerated `32`,
  confirming the deployed `L(a) = ceil(C(n,a)/p^w)` staircase is a *floor*, not
  the true `B_list`.

## Companion pair (recorded, non-headline)

The same row yields a second adjacent pair whose safe side is the
**unique-decoding** cell rather than Johnson:

```text
a0 = 11 (unsafe), a0+1 = 12 (safe):  L(11) = 3 > B* in {1,2} >= U(12) = 1,
U(12) via 2*12-16 = 8 > 7 (unique decoding, all words).  total sep 1.585 b.
```

`L(11)=3` is by full `C(16,11)=4368` enumeration. Its budget window `{1,2}` needs
a smaller `eps*` than the headline `B*=12`; tighter margins, trivial safe cell.
Recorded in the packet JSON, not the headline.

## Positioning

This gives the program its first fully-worked **template** instance of the object
every deployed row must eventually instantiate on the list route: an adjacent
staircase whose two sides are both proved, with the ledger, dedup rule, endpoint
convention, and row-packet schema exercised end-to-end. The floor-vs-truth datum
(`28` vs `32`) is a small independent measurement. No prize-metric movement is
claimed.

## Contribution template

- **Claim.** First complete two-sided adjacent staircase certificate on the list
  route; first list-route instantiation of the certificate condition of
  `thm:finite`.
- **Status.** EXPERIMENTAL (toy scale); the two cells are PROVED under their
  stated hypotheses.
- **Parameters.** `p=17`, `n=16`, `k=8`, `rho=1/2`, list route, `eps*=2^-29`,
  `B*=12`.
- **Existing paper dependency.** `def:staircase`, `thm:finite`,
  `lem:integer-budget`, `lem:first-match-ledger`, `prop:prefix-witness`,
  `rem:endpoint`, `prop:q-exact-target`, `prob:row-sharp-q`
  (all `experimental/grande_finale.tex`); convention layer
  `experimental/notes/thresholds/adjacency_staircase_localization.md` and
  `experimental/notes/thresholds/paid_ledger_functions.md`.
- **Proof idea / experiment.** Enumerate `C(16,10)` prefix fibers (unsafe) +
  Johnson packing (safe); see the verifier.
- **Ledger impact.** Adds a complete list-route adjacent example; no change to any
  deployed row's status.
- **Constants.** All integer and printed above.
- **Reproducibility.**
  `python3 experimental/scripts/verify_toy_complete_adjacent_list_staircase.py`
  (zero-arg, exit 0 = PASS).

## Label hygiene

All TeX citations are to the **promoted** `experimental/grande_finale.tex` labels.
The working drafts under `experimental/grande_finale_work/*.tex` use different
label names (e.g. `thm:finite-next-compiler`, `prop:finite-packet-unsafe`) that
are already absorbed into the promoted tex under the labels cited here; those
draft labels are deliberately not cited.
