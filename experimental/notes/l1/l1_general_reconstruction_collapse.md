# L1 General Reconstruction Collapse: Full-Petal Codewords = Minimal Kernel Sets

## Claim

For EVERY background-free sunflower received word (petals `T_1..T_t`
disjoint size-`ell` subsets of `F_q^*`, scalars `c_i`, core `C`, word
`U = c_i L_C` on petal `i` and `0` on `C`; `k = |C|+1`, `s = k+ell-1`) with
not-all-equal scalars, the listed codewords touching all `t` petals fully
are in explicit BIJECTION with the divisibility-minimal kernel sets:

Call `E subset C` a KERNEL SET if `ell <= |E| <= (t-1)ell` and the unique
degree-`< t*ell` CRT representative `W_E` of `(c_i L_E mod L_{T_i})_i`
has `deg W_E <= |E|` (equivalently `L_E in K_{I,|E|}`, Lemma 8's kernel);
MINIMAL if no proper nonempty subset is a kernel set. Then:

1. **(Collapse)** If `D` and `E subset D` are kernel sets then the Lemma 7
   reconstructions coincide: `W_D = L_{D\E} * W_E` (CRT uniqueness, using
   `|D| <= (t-1)ell < t*ell`) and hence `P_D := W_D L_{C\D} = W_E L_{C\E}
   =: P_E`.
2. **(Agreement formula)** For every kernel set `E`, `P_E` agrees with `U`
   exactly on (all petals) `u (C\E) u {x in E : W_E(x) = 0}`; its exact
   missed core is `M(E) = E \ Z(W_E)`, and `P_E` is listed iff
   `|M(E)| <= (t-1)ell` (automatic for kernel sets).
3. **(Rigidity)** If `E` is minimal and `M(E)` nonempty then `M(E) = E`
   (else Lemma 7 applied to `P_E` would produce a proper kernel subset).
4. **(Bijection)** `E -> P_E` is a bijection from the minimal kernel sets
   (`M(E) = emptyset` occurs only when `U` is itself a codeword, i.e.
   never for not-all-equal scalars by item 6) onto the listed codewords
   touching all `t` petals fully. Injectivity: distinct minimal sets are
   the exact missed cores of their images. Surjectivity: the exact missed
   core `M` of any such codeword is a kernel set (Lemma 7) and is minimal
   (a proper kernel subset would force, via items 1-2, exact missed core
   strictly inside `M`).
5. **(Range necessity — route-cut)** The size cap `|E| <= (t-1)ell` is
   ESSENTIAL: `deg W_E < t*ell` always holds, so every `E` with
   `|E| >= t*ell-1` satisfies the degree inequality vacuously, and generic
   such sets are subset-minimal with `M(E) = E` yet reconstruct to
   NON-listed polynomials (agreement `< s`). Explicit counterexample:
   `p=17`, petals `[[1,2],[3,4],[5,6]]`, `c=(3,10,5)`, `C={8,..,12}`,
   `E = C` (size 5 > 4): "minimal, M(E)=E", agreement `6 < s=7`. Without
   the cap the collapse step itself also fails (`h W_E` overflows the CRT
   window once `|D| >= t*ell`). Do not restate the lemma without the cap.
6. **(Sub-`ell` floor)** A nonempty `E` with `|E| < ell` and
   `deg W_E <= |E|` exists iff `c_1 = ... = c_t` (then `W_E = c L_E`
   identically and `U` IS the codeword `c L_C`): if `|E| < ell` then
   `W_E - c_i L_E` has degree `< ell` yet is divisible by the degree-`ell`
   petal locator, hence zero, for every `i` simultaneously. So for
   distinct scalars the abstract kernel floor equals Lemma 7's defect
   floor `ell` exactly, and minimality needs no sub-`ell` blockers.

CONSEQUENCE: Lemma 8's counting bound `q^{d+1-r_{I,d}}` and any bound via
raw split-locator concentration in `K_{I,d}` are superseded by
`#minimal kernel sets` — a strictly smaller, structured quantity. A
super-polynomial primitive full-petal family requires super-polynomially
many MINIMAL kernel sets; abundance of non-minimal split kernel locators
(e.g. the resonant coset families of `l1_coset_petal_rank_collapse.md`)
produces NO additional codewords.

## Status

PROVED-LOCAL (items 1-6; elementary, self-contained proofs above at the
level of detail of the proof program's Lemma 7/8, plus exhaustive finite
verification: four independent implementations, ~2,600 instances total,
including full brute-force list decoding; the shipped verifier gates the
bijection, the agreement formula, the sub-`ell` iff, the range-necessity
counterexamples, and the coset corollary). The growth question for
`#minimal kernel sets` in the asymptotic regime remains OPEN
(EXPERIMENTAL findings below).

## Parameters

Verified: `p in {17,19,23,29,31,37,41,43,61,73,97}`, `ell in {2,3}`
(spot `4,5`), `t in {2,3,4,5}`, petal shapes consecutive-block / random /
subgroup-coset, cores to `|C| = 12` (lattice) and `n <= 22` (decode),
scalar modes generic / repeated-pair / all-equal / engineered moments.

## Existing paper dependency

Sharpens the counting consequence of Lemma 8 of
`l1_full_list_quotient_proof_program.md` (uses Lemma 7 verbatim for the
forward direction; no change to either lemma). Companion to
`l1_coset_petal_rank_collapse.md` (PR #218), whose t=3 Theorem 4 becomes
the corollary "minimal kernel sets = {beta-coset} iff resonant, else
empty" and whose t>=5 EXPERIMENTAL equality
(#codewords = #divisibility-minimal generators) is upgraded to a THEOREM
by item 4 — the decoder-verified counts 27/5/19 at `p in {23,41}`, t=5
were independently reproduced bit-exactly and matched to minimal-set
enumerations at set level.

## Proof idea or experiment

All proofs are short consequences of CRT-representative uniqueness below
degree `t*ell` plus Lemma 7: see items 1-6 (each stated with its proof
mechanism). The verification suite additionally exercises the exact
counterexamples that make the stated hypotheses necessary. Verifier:
`experimental/scripts/verify_l1_general_reconstruction_collapse.py`
(stdlib-only, offline, deterministic, exit 0 iff all five check groups
pass).

## Ledger impact

Mixed-petal residual machinery (Lane B / Conjecture 1): the full-petal
counting object improves from `q^{kernel-dim}` to `#minimal kernel sets`
for every sunflower family. EXPERIMENTAL map from a 611-case growth study
(not verifier-gated): (i) no dimension/VC-type route bounds
`#minimal kernel sets` polynomially — a polynomial bound must be
arithmetic; (ii) subgroup-coset petals are the extremal configuration
(random and engineered non-coset families gave O(1)); (iii) the coset
count concentrates at top defect `d = (t-1)ell` and splits as
`C(m, t-1)` coset-unions (`m` = number of core cosets) — ALL
quotient-charged (agreement stabilizer contains `H`) — plus a MIXED part
which is exactly the stabilizer-primitive contribution; (iv) in the prize
regime `m = O(log n) < ell` and NO mixed (primitive) minimal set was ever
observed with `m < ell`. Named next target: prove the `m < ell`
mixed-vacancy, which would zero the primitive full-petal contribution of
coset configurations in the regime. No paper text changes; everything
stays in `experimental/`.

## Constants

Explicit throughout: kernel-set range `[ell, (t-1)ell]`; listedness
threshold `|M(E)| <= (t-1)ell`; counterexample instances printed in the
verifier; measured coset top-defect counts `C(m,t-1) + mixed` with
decoder-matched values 27 (`p=23, t=5, m=6`), 5 (`p=41, t=5, m=5`),
19 (`p=41, t=5, m=6`).

## Reproducibility

`experimental/scripts/verify_l1_general_reconstruction_collapse.py`:
(1) sub-`ell` iff-degenerate over 320 instance-classes (both directions);
(2) agreement formula on EVERY kernel set + bijection vs full decode on
120 deterministic instances (consecutive/random/coset petals, t=2..4,
25 with nonzero counts); (3) t=3 coset corollary over 200 scalar vectors
(38 resonant / 162 non-resonant, PR #218's dichotomy re-derived);
(5) range-necessity: both counterexamples of item 5 reproduced exactly.
Deterministic (fixed LCG seeds), fully offline, stdlib-only.
