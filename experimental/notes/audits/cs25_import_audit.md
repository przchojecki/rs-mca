# CS25 Import Audit Checklist for Paper D

- **Status:** AUDIT
- **Agent/model:** Codex acting autonomously through AllenGrahamHart
- **Date:** 2026-06-17
- **Scope:** Local import map and due-diligence checklist for the Crites--Stewart
  conversion used by Paper D. This is not an independent proof of CS25.

## Summary

Paper D (`tex/cs25_cap_v4.tex`) proves its universal cap by composing a
locator-fiber list lower bound with an imported correlated-agreement-to-list
decoding implication attributed to Crites--Stewart, as restated in ABF26. The
same import also appears in the companion slack/MCA paper.

This audit records the exact local dependency surface and the external checks
that must be closed before the CS25-based route is cited as unconditional. The
repo already marks the import as recent and conditional; this file makes the
checklist explicit for later human or agent review.  For the separate local
deep-point route to the headline MCA cap, see
`experimental/notes/audits/a0_deep_point_cap_dependency_split.md`.

## Local Import Surface

| Local label | File | Role |
| --- | --- | --- |
| `thm:A` | `tex/cs25_cap_v4.tex` | CS25 Theorem 2 as restated in ABF26 Theorem 5.3. |
| `thm:B` | `tex/cs25_cap_v4.tex` | BCHKS25 Theorem 1.9 as restated in ABF26 Theorem 5.2. |
| `rem:import` | `tex/cs25_cap_v4.tex` | Paper D's explicit import warning and checklist. |
| `lem:fiber` | `tex/cs25_cap_v4.tex` | Produces the list lower bound fed into `thm:A`. |
| `thm:main` | `tex/cs25_cap_v4.tex` | Main contrapositive use of `thm:A` at `eta=1/2`. |
| `rem:eta` | `tex/cs25_cap_v4.tex` | Records constant-factor flexibility in `eta`. |
| `prop:slacked` | `tex/cs25_cap_v4.tex` | Independent fallback route through `thm:B`. |
| `lem:confine` | `tex/cs25_cap_v4.tex` | Separates base-rational lines from extension-field mass. |
| `cor:Fvalued` | `tex/cs25_cap_v4.tex` | Interprets deployed lines as genuinely `F`-valued. |
| `thm:capimport` | `tex/slackMCA_v3.tex` | Earlier local statement of the CS25 import. |
| `lem:capcontra` | `tex/slackMCA_v3.tex` | Earlier contrapositive at `eta=1/2`. |
| `thm:cap` | `tex/slackMCA_v3.tex` | Earlier conditional universal cap. |
| `cor:captiers` | `tex/slackMCA_v3.tex` | Challenge-parameter tiering under the import. |
| `rem:diligence` | `tex/slackMCA_v3.tex` | Companion due-diligence checklist. |

## Load-Bearing Implications

1. `thm:A` is used only through the displayed implication
   `eca(C,delta) <= eta(1/k - n/(kq)) => Lst(C+,delta) <= ceil(q eca/(1-eta))`.
2. In `thm:main`, Paper D applies `thm:A` with `eta=1/2`, deriving
   `Lst(C+,delta) < q/k + 1` from the assumption
   `eca(C,delta) <= (1/(2k))(1 - n/q)`.
3. `lem:fiber` gives a word in `C+` with at least
   `binom(N,rho N+2)/|B|` codewords at radius `1-rho-2/N`.
4. The contradiction needs the local numerical hypothesis
   `binom(N,rho N+2) >= |B|(q/k + 1)`.
5. `prop:slacked` is independent of `thm:A` and uses `thm:B` instead, but still
   depends on the ABF26 restatement of the BCHKS25 theorem.

## External Checks To Close

- **E1: CS25 delta range.** Verify the exact admissible range of `delta` in
  CS25 Theorem 2. Paper D applies the import for every `delta` in
  `[1-rho-2/N, dmin(C))`. Current status: open.
- **E2: Augmented code.** Verify the augmented-code definition
  `C+ = RS[F,D,k+1]`. The heavy list from `lem:fiber(ii)` is placed in `C+`.
  Current status: open.
- **E3: List monotonicity.** Verify `Lst(C,delta) <= Lst(C+,delta)` under the
  same radius convention. The slack/MCA paper only needs this consequence.
  Current status: open.
- **E4: `eca` normalization.** Verify the normalization of `eca`. The cap
  needs density over the same challenge field used for slopes. Current status:
  open.
- **E5: Extension-field sampling.** Verify extension-field sampling in the
  CS25/ABF26 convention. Paper D's deployed corollary works over `F/B` with
  `D subset B`. Current status: open.
- **E6: Constants and ceiling.** Verify the constants in the displayed
  implication. The current cap uses the exact `eta=1/2` ceiling calculation.
  Current status: open.
- **E7: ABF26 Theorem 5.3.** Verify ABF26 Theorem 5.3 matches `thm:A`
  verbatim. Paper D cites the ABF26 restatement, not only CS25 directly.
  Current status: open.
- **E8: ABF26 Theorem 5.2.** Verify ABF26 Theorem 5.2 matches `thm:B`
  verbatim. The slacked fallback route depends on this restatement. Current
  status: open.

## Partial Source Notes

- CS25 appears in the repo bibliography as Crites--Stewart,
  "On Reed--Solomon Proximity Gaps Conjectures," IACR ePrint 2025/2046.
  The ePrint landing page is public, but a direct local PDF fetch returned HTTP
  403 during this audit, so the theorem text was not independently checked here.
- BCHKS25 appears in the repo bibliography as Ben-Sasson--Carmon--Habock--
  Kopparty--Saraf, "On Proximity Gaps for Reed--Solomon Codes." The ECCC
  report 2025/169 PDF was locally reachable during this audit. Text extraction
  found Theorem 1.9 with the expected `+2/n`, `-1/n`, and `q/(2n)` scale, but
  the ABF26 Theorem 5.2 translation still needs a direct check.

## Risk Register

- **Narrower CS25 range:** This would affect `thm:main`, `cor:grand`, and
  `cor:deployed`. Mitigation: `prop:slacked` gives a separate weaker route.
- **Different `C+` convention:** The list lower bound may land in the wrong
  code. Mitigation: `rem:import` already isolates this as due diligence.
- **Different `eca` normalization:** Extension-field corollaries could shift by
  `|B|/|F|`. Mitigation: `lem:confine` separates base-rational lines from
  `F`-valued mass.
- **Different ceiling or constant:** The certified error constant changes from
  about `1/(2k)`. Mitigation: `rem:eta` records robustness to constant-factor
  repairs.
- **Different BCHKS fallback restatement:** `prop:slacked` may need parameter
  edits. Mitigation: the fallback is isolated and weaker than the main cap.

## Suggested Verification Commands

These commands check that the local dependency labels still exist:

```sh
pat_d='\\label\{(thm:A|thm:B|rem:import|lem:fiber|thm:main'
pat_d="$pat_d"'|rem:eta|prop:slacked|lem:confine|cor:Fvalued)\}'
pat_b='\\label\{(thm:capimport|lem:capcontra|thm:cap'
pat_b="$pat_b"'|cor:captiers|rem:diligence)\}'
rg -n "$pat_d" tex/cs25_cap_v4.tex
rg -n "$pat_b" tex/slackMCA_v3.tex
```

When external PDFs are available, the next reviewer should also record:

```sh
pdftotext CS25.pdf -
pdftotext ABF26.pdf -
pdftotext BCHKS25.pdf -
```

and grep the extracted text for `Theorem 2`, `Theorem 5.3`,
`Theorem 5.2`, `C+`, `augmented`, `eta`, `epsilon`, `2/n`, and `1/(2n)`.

## Promotion Rule

Do not upgrade Paper D's CS25-based cap from conditional/imported to
unconditional until E1--E7 are closed. Do not upgrade the slacked fallback until
E8 is closed as well.  This rule concerns the imported CS25/ABF routes, not
the separate deep-point dependency split.
