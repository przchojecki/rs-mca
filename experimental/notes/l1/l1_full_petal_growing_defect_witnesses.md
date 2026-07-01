# L1 Full-Petal Growing-Defect Witnesses

## Claim

For background-free Reed--Solomon sunflower received words with `t>=3`
petals of size `ell` each (notation of
`l1_full_list_quotient_proof_program.md` Lemma 2/7/8), there exist
non-planted listed codewords that touch **all** `t` petals in full at
core-defect `d` strictly above `ell`, i.e. with strictly positive
"cofactor excess" `d-ell`. Two explicit witnesses are exhibited, at
`d-ell=2` (`t=3`) and `d-ell=5` (`t=5`).

This shows the full-petal branch of the "cofactor excess `d-ell ->
infinity`" escape route left open by Theorem 21 / Theorem B11 (the
proof program's current stopping point) is genuinely populated beyond
the single `d=ell` layer that Lemma 9 already proves is nonempty. It is
an existence result only: it does not establish a growth rate, and does
not prove or disprove Conjecture 1 (the full-list quotient-budgeted
bound) or the "Mixed-petal sunflower amplification" target that closes
`l1_full_list_quotient_proof_program.md`.

A secondary, negative finding (route-cut) is also recorded: the natural
attempt to strengthen Lemma 13's rank floor `r_{I,d} >= ell` into an
exact closed form `r_{I,d} = min(d+1, t*ell-d-1)` -- which would have
implied the full-petal kernel is *trivial* (zero extras, not merely
polynomially bounded) for `d` up to about half of `t*ell` -- is **false
in general**. Do not re-attempt this exact formula; see "Proof idea or
experiment" below for the two failure modes found.

## Status

COUNTEREXAMPLE-STYLE (existence witnesses) for the informal hope that
the full-petal, `t>=3` case might contribute nothing; ROUTE-CUT for the
exact-rank-formula sub-attempt. EXPERIMENTAL tier: does not change the
status of Conjecture 1 itself, which remains CONJECTURAL.

## Parameters

Both witnesses use `p=1009`. Notation matches the proof program:
`ell` = petal size, `t` = touched petals, `d` = core defect (missed core
size), `s = k+ell-1` (agreement threshold for the sunflower's `sigma =
ell-1`).

- **Witness A:** `ell=3`, `t=3`, petals `{0,1,2},{3,4,5},{6,7,8}`,
  scalars `c=(1,2,3)`, core size `k-1=10` (retained core `C_P` size 5,
  missed core `D={558,784,852,874,900}` size `d=5`), so `d-ell=2`. Here
  `n=19`, `k=11`, `s=13`. The extra codeword's agreement set is the 5
  retained core points union all 3 petals (size 14).
- **Witness B:** `ell=3`, `t=5`, petals `{0,1,2},...,{12,13,14}`,
  scalars `c=(1,2,3,4,5)`, core size `k-1=8` **equal** to the missed
  core `D={69,453,512,670,682,855,864,917}` (retained core `C_P` is
  empty), so `d=8`, `d-ell=5`. Here `n=23`, `k=9`, `s=11`. The extra
  codeword's agreement set is exactly the union of all 5 petals (size
  15), with zero core agreement.

## Existing paper dependency

Builds directly on `experimental/notes/l1/l1_full_list_quotient_proof_program.md`:
Lemma 2 (sunflower core-defect reduction), Lemma 7/8 (full-petal CRT
compression and rank certificate), Lemma 9/13/14/15/16 (existing
defect-layer bounds for the full-petal case), and Theorem 21/B11 (the
residual frontier that isolates "`d-ell -> infinity`" as the open
escape route). Also extends
`experimental/notes/l1/l1_full_list_quotient_falsification.md`'s
sunflower attack, whose exhibited extras were all *partial*-petal
(mixing petals without fully covering any beyond the planted ones) --
no full-petal (`t>=3`, all touched petals complete), growing-defect
witness previously appears in either note.

## Proof idea or experiment

1. Lemma 8 shows full-petal extras with exact touched-set `I` (`|I|=t`)
   and exact defect `d` inject into `{L_D : D subset C, |D|=d}` (split
   monic degree-`d` locators with roots in the core) intersected with
   `K_{I,d} = ker(pi_{>d} R_{I,d})`, the kernel of the CRT
   top-coefficient map. Lemma 13 proves only `dim K_{I,d} <= d-ell+1`.
2. Numerically, across an initial sweep of consecutive-block petals and
   sequential scalars, `rank(pi_{>d} R_{I,d})` matched the exact closed
   form `min(d+1, t*ell-d-1)` with zero exceptions -- strictly sharper
   than Lemma 13, and implying `K_{I,d}={0}` (zero extras, not just
   polynomially bounded) for `d` up to about `t*ell/2`.
3. Adversarial search **refuted** this exact formula in general, via two
   distinct failure modes, both independently reproduced against the
   repo's own unmodified `interpolate_polynomial`/`matrix_rref`: (a)
   isolated prime-specific coincidences even for plain consecutive-block
   petals (e.g. `p=101, ell=6, t=6, d=17`, which does not reproduce at
   ~35 other tested primes); (b) a robust **structural** family --
   round-robin cosets of the order-`ell` subgroup as petals, with `t`
   odd -- where the rank drops below the formula for *every* tested
   scalar choice (verified independently above for `p=19, ell=3, t=3`).
   Lemma 13's original floor `r_{I,d}>=ell` is never violated by any of
   these; only the strictly stronger exact-formula conjecture fails.
4. Separately, and regardless of the abstract rank, realizability
   (whether the kernel actually contains a *split* locator with roots in
   the fixed core, as opposed to an arbitrary kernel element) was tested
   directly via exact CRT-degree checks over candidate missed-core sets.
   This produced Witnesses A and B above. Each was independently
   re-confirmed a second way: reconstructing the actual received word
   `U` explicitly and running a from-scratch brute-force exact
   support-subset RS list decode, confirming that the predicted extra
   codeword's exact agreement set genuinely appears in the real list
   (alongside the expected planted codewords and, in Witness A's
   underlying search, occasional unrelated partial-petal extras of the
   kind already catalogued by the falsification note).

## Ledger impact

No Paper A/B/C/D ledger changes. Sharpens the open status of the
"Mixed-petal sunflower amplification" CONJECTURAL target at the end of
`l1_full_list_quotient_proof_program.md`: a future proof of Conjecture 1
must actually bound the full-petal growing-defect family (it is
non-empty), and a future counterexample search aiming to falsify
Conjecture 1 should look here -- specifically at families with `t`
growing and `d-ell` growing together -- rather than assume this corner
is vacuous.

## Constants

Explicit witnesses only (see Parameters); no asymptotic count or
growth-rate claim is made. In particular this note does **not** claim
the number of such extras grows polynomially, super-polynomially, or is
bounded -- that question is exactly what remains open.

## Reproducibility

`experimental/scripts/verify_l1_full_petal_growing_defect_witnesses.py`.
Deterministic, stdlib-only, fully offline (reuses
`experimental/scripts/scan_l1_full_list_quotient_conjecture.py`'s
modular-arithmetic helpers). Reconstructs both received words explicitly
from the parameters above and runs a brute-force exact support-subset RS
list decode, reporting and tagging every codeword found (planted /
predicted-extra / other) rather than checking only the predicted one, so
a reviewer sees the complete list. Also independently re-derives the
Witness-A-style rank counterexample for the round-robin-coset family
(`p=19, ell=3, t=3`) across several scalar choices.
