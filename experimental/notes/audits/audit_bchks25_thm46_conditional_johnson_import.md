# BCHKS25 Theorem 4.6 Conditional Johnson-Regime MCA Import

- **Status:** AUDIT / CONDITIONAL IMPORT PROPOSAL.
- **Date:** 2026-07-04.
- **Agent/model:** Claude Fable 5 acting for latifkasuli.
- **Sources:** BCHKS25 = Ben-Sasson--Carmon--Haböck--Kopparty--Saraf, *On
  Proximity Gaps for Reed--Solomon Codes*, ePrint 2025/2055 (§4.3, Thm 4.6,
  pp. 27--29; two byte-distinct copies of the same version cross-checked);
  `tex/cs25_cap_v12.tex` (`def:mca` line ~139, `thm:mca-from-ca` ~4939,
  `cor:conditional-half` ~5054); `tex/towards-prize.tex` (`sigma_C` ~217,
  `prop:p2-half-sharp` ~522, `thm:sparsify` ~661, `thm:transfer` ~780);
  `open-proximity.tex` (table `tab:mca` ~163, Thm 4.6 rendering ~691,
  bibliography ~1451); `experimental/notes/audits/m0_prize_mca_definition_freeze.md`.
- **External audit trail:** full primary-source audit at
  `github.com/latifkasuli/mca`, `docs/bchks25-thm46-import-audit.md`, repo tip
  commit `e16dd12` (exact-rational arithmetic, verbatim quotations, page
  references). This note is the upstream-facing packet of that audit,
  reconciled against `origin/main = c87675e`.

## Summary

BCHKS25 Theorem 4.6 states list (mutual) correlated agreement for Reed--Solomon
codes up to the Johnson radius. The statement bridges **exactly** to `def:mca`
(support-wise witness, same-support noncontainment, finite affine sampler,
count/q normalization) after one dimension reindex `k_B = k-1`. Instantiated on
the KoalaBear sextic row it would move the certified safe frontier from
`delta = 1/4` to the exact integer edge `r = 604,085` (`delta ~= 0.2880502`,
88.7% of the way to Johnson), sharp to 0.006 bits at `r+1`.

**The import is CONDITIONAL and must not be presented otherwise.** The theorem
is not proved in BCHKS25: it carries a one-paragraph sketch and attributes the
proof to [Hab25], which BCHKS25's own bibliography prints as "Personal
communication". Per the M0 freeze use rule ("If any row cannot be filled
without importing a theorem, mark it as a residual or conditional dependency
instead of silently merging ledgers"), the drafted corollary below is tagged as
a conditional dependency on [Hab25].

**Repositioning against in-repo prior work (important).** This repository
already discusses the Johnson-regime mutual bound: `open-proximity.tex`
(landed 2026-06-26, commit `b80ae72`) tabulates the row
`delta = J(dmin) - eta => epsmca <= n*poly(1/eta)/|F|` citing
{BCHKS25, Hab25, BCGM25, BCIKS20} (line ~163), states a rendering of Thm 4.6 as
a survey theorem (line ~691), and — critically — its bibliography records
[Hab25] as **Cryptology ePrint Archive, Paper 2025/2110** ("A note on mutual
correlated agreement for Reed-Solomon codes", line ~1451), i.e. as a *public*
ePrint, superseding BCHKS25's "personal communication" printing that the
external audit relied on. `tex/snarks_v5.tex` also cites Hab25 (line ~282).
What this note adds beyond the survey layer: the verbatim statement-level
bridge audit to `def:mca`, the exact-integer deployed-row instantiation and its
sharpness, the conditionality classification and packaging, the consistency
analysis against the repository's own sharpness/limit results, and two
discrepancy flags on the survey's rendering (below). The proof-status
condition is *changed in kind* by the ePrint discovery — and has now been
resolved one level further: ePrint 2025/2110 was **independently proof-audited
on 2026-07-04** (line-by-line, all deferrals checked against BCIKS20 ECCC
TR20-083; full audit in the external repository, `docs/
bchks25-thm46-import-audit.md`, section "Hab25 proof audit"). Outcome:

- **The Johnson-radius mutual MECHANISM is PROVED.** Hab25 Theorem 2
  establishes exactly the `def:mca` event (same-support quantifier, `M = 1`
  line) up to `1 - sqrt(rho_B)`, with error `(l^7/3)(rho_B n)^2`,
  `l = (m + 1/2)/sqrt(rho_B)` — quadratic in `n`. The same-support crux
  (per-class collapse to a unique affine proximate + a fully-written AHIV17
  count) is rigorous; three bookkeeping gaps were closed in the audit, and
  the note's `[BCI+20, Claim 5.7]` should read Claim 5.6/(5.10) in the ECCC
  version.
- **The printed LINEAR-in-n bound of BCHKS25 Thm 4.6 is NOT yet proved**: it
  exists only as the BCHKS25 p. 29 sketch, with the verbose update announced
  in Hab25's own remark. This is the sole remaining condition (`M > 1`
  batching is likewise asserted-only but irrelevant to `def:mca`).
- **Deployed-row consequence, exact integers:** under the PROVED quadratic
  bound the certified safe radius is only `r = 428,878`
  (`delta ~ 0.20450`) — *below* the existing `1/4` edge, hence currently
  dominated by `cor:conditional-half` (it becomes the correct citation for
  rows with `q >~ 2^220` or laxer budgets). The full imported band
  `delta in (1/4, 604085/2^21]` therefore rests exactly on the unproved
  linear bound and **remains conditional** — retagged from "proof
  unavailable" to "mechanism proof-audited; printed constant pending
  Haböck's announced update or a revised BCHKS25 §4.3", which is also the
  re-audit trigger that would let the band shed the conditional tag.

## Item 1 — Statement match: Thm 4.6 vs `def:mca` (MATCH, with a k-reindex)

BCHKS25 Thm 4.6 (p. 28, verbatim): "Let C = RS_k[F_q, D, k] be the Reed--Solomon
code over F_q with domain of definition D of size |D| = n, and dimension k + 1.
Denote rho = k/n, the slightly reduced rate of the code. Then for any
u_0, ..., u_M : D -> F_q, and gamma in (0, 1 - sqrt(rho)), the size of

```text
E = { z in F_q : exists A subset D, |A| >= (1-gamma)*n, s.t.
      (u_0 + z*u_1 + ... + z^M u_M)|_A in C|_A,
      but [u_0, ..., u_M]|_A not in C^{M+1}|_A }
```

is bounded as |E| <= M * ( (2(m+1/2)^5 + 3(m+1/2)*gamma*rho) / (3*rho^{3/2}) * n
+ (m+1/2)/sqrt(rho) ), where m = max(ceil(sqrt(rho)/(1-sqrt(rho)-gamma)), 3)."

Point-by-point against `def:mca` (`tex/cs25_cap_v12.tex` ~139):

| aspect | BCHKS25 Thm 4.6 (M=1) | `def:mca` | verdict |
|---|---|---|---|
| quantifier shape | exists A per z, `\|A\| >= (1-gamma)n`, point in `C\|_A`, tuple not in `C^{M+1}\|_A` on the same A | exists S per gamma, `\|S\| >= (1-delta)n`, `dist_S(f1+gamma f2, C) = 0`, pair not in `C^{==2}\|_S` on the same S | exact match (support-wise, same-support noncontainment) |
| batching | degree-M curve; at M=1 the affine line `u0 + z*u1` | affine line `f1 + gamma f2` | match at M=1; BCHKS additionally covers curve samplers M>1 |
| radius convention | closed agreement, range open at Johnson | closed integer ball, supremum open at first unsafe endpoint (M0 freeze) | match; Johnson endpoint excluded on both sides |
| challenge sampler | `z in F_q`, whole field | `Pr_{gamma <- F}` uniform = M0 finite affine slope sampler | match; M0 projective variant: numerator +1, denominator q+1 (immaterial at 2^-128) |
| normalization | count `\|E\|` | probability = count/q | match after dividing by q: `epsmca(C, delta) <= \|E\|_max / q` |
| code convention | `RS_k[F_q, D, k_B]` = deg <= k_B, dim k_B+1, rho_B = k_B/n | `RS[F, D, k]` = deg < k, dim k, rho = k/n | off-by-one: import at `k_B := k-1`, `rho_B = rho - 1/n`; Johnson `1 - sqrt(rho_B)` slightly larger — favorable direction |

Bridge lemma (four bookkeeping clauses, no mathematical content): (i) at M=1 the
event is the `def:mca` event verbatim after renaming; (ii)
`epsmca(C, delta) <= |E|_max / q`; (iii) reindex `k_B = k-1`; (iv) projective
sampler: numerator +1, denominator q+1. The support-wise/same-support
quantifier — historically the layer most likely to silently mismatch (cf.
`audit_step1_sampler_reconciliation.md`) — is verbatim-identical.

Cosmetic flags in the source: theorem title reads "up to Johson bound" (typo);
witness set written `A ⊂ D` (read as `⊆`; strictness immaterial, one witness
suffices and `A = D` qualifies).

### Discrepancy flags on the `open-proximity.tex` rendering (survey-level)

The survey theorem at `open-proximity.tex` ~691 instantiates with
`rho_+ := rho + 1/n`, `m := max(ceil(sqrt(rho_+)/(2*eta)), 3)`, for
`delta < 1 - sqrt(rho_+) - eta`. Two observations, flagged for the survey
author (neither affects any certificate):

1. **Rate direction.** The exact-dimension bridge to `RS[F, L, k]` (deg < k,
   dim k) is `k_B = k-1`, i.e. `rho_B = rho - 1/n`. The survey's
   `rho_+ = rho + 1/n` is the conservative direction (smaller Johnson window,
   larger bound) but concedes `2/n` of rate relative to the exact match.
2. **The m parameter as printed appears unsound by up to 2x.** BCHKS25
   prescribes `m = max(ceil(sqrt(rho)/(1 - sqrt(rho) - gamma)), 3)` and the
   bound is increasing in m. Under the survey's hypothesis
   `delta < 1 - sqrt(rho_+) - eta` one only gets
   `m <= ceil(sqrt(rho_+)/eta)`; when `eta < 1 - sqrt(rho_+) - delta < 2*eta`
   the true m exceeds the printed `ceil(sqrt(rho_+)/(2*eta))`, so the printed
   constant undershoots (by up to `~2^5 = 32` in the leading `m^5` term). The
   asymptotic `O_rho(n / (eta^5 |F|))` is unaffected. The corollary drafted
   below instantiates BCHKS25's own m directly and avoids the issue.

## Item 2 — Exact KoalaBear instantiation (M=1, k_B = 2^20 - 1)

Method (external audit, commit `e16dd12`): all inequalities in exact rationals;
`sqrt(rho_B)` sandwiched by integer-sqrt bounds at denominator `n * 10^50` with
every occurrence replaced by the adverse endpoint; the budget condition
`B(delta) * 2^128 <= q` as an exact integer comparison; binary search over the
integer radius r (`B(r/n)` nondecreasing in r). Row: `n = 2^21`, `k = 2^20`,
`q = p^6`, `p = 2^31 - 2^24 + 1`, `log2 q = 185.9321`.

| quantity | value |
|---|---|
| max safe integer radius | `r = 604,085` |
| safe edge delta | `604085 / 2^21 ~= 0.2880502` |
| safe-edge agreement | `a = n - r = 1,493,067` (`a/n ~= 0.7119498`) |
| band at the edge | `m = 146` (`eta ~= 0.0048434 >= sqrt(rho_B)/146`) |
| bound at the edge | `B ~= 2^57.8888`, so `epsmca <= 2^-128.043 < 2^-128` (~3% headroom) |
| sharpness at `r+1 = 604,086` | band jumps to `m = 147`, `B ~= 2^57.9379 > q * 2^-128 ~= 2^57.9321` — fails by 0.006 bits |
| certified frontier shape | exactly the `m <= 146` band edge, `delta <= 1 - sqrt(rho_B) * (147/146)` |
| robustness to dimension reading | pessimistic `rho = 1/2` exactly gives `r = 604,084` (one coordinate less) |
| context | Johnson `1 - sqrt(rho_B) in [0.29289355, 0.29289356]`; edge covers 88.7% of the gap from 1/4; gain +79,797 radius steps over `r = 2^19` |
| division of labor | at `delta <= 1/4`, `cor:conditional-half` stays tighter (`n/q < 2^-164.9` vs `~2^-143.4`); the import only improves the band `delta in (1/4, 604085/2^21]` |

## Item 3 — Conditionality and provenance (the load-bearing caveat)

- BCHKS25 does **not** prove Thm 4.6. It gives a one-paragraph sketch (p. 29)
  grounded in the paper's fully-proved §3 machinery, and attributes the proof:
  "a proof of it, which generalizes the decoder analysis from [BCI+20] is
  discussed in [Hab25]" (p. 28). BCHKS25's bibliography (p. 48): "[Hab25]
  Ulrich Haböck. A note on mutual correlated agreement. 2025. (Personal
  communication)."
- `open-proximity.tex` ~1451 records the same note as **ePrint 2025/2110** —
  evidently public after BCHKS25's version was fixed. This answers the external
  audit's open question ("ask whether [Hab25] has or will get an ePrint
  number") but does not discharge the condition: the proof has not been
  audited against `def:mca` in this repository or in the external audit.
- Classification: claimed-with-sketch in BCHKS25 on the authority of [Hab25].
  Contrast: BCHKS25 Thms 1.3/1.5/4.1/4.2 (plain CA) and Thm 1.9 are proved in
  the paper. Note the §4.2--4.3 layer also leans on a second non-public source
  ("[Sta25] StarkWare Team. S-two whitepaper. 2025. (Personal communication)").
- Statement-level conditions: none beyond `gamma in (0, 1 - sqrt(rho_B))` — no
  field-size, characteristic, or domain-structure hypotheses; q enters only
  through the budget comparison.
- Per the M0 freeze use rule, the corollary below is marked a **conditional
  dependency on [Hab25]**. Nothing in this packet is presented as
  unconditional, and no leaderboard row or paper theorem is promoted.

## Item 4 — Unconditional fallback landscape (no help at rho = 1/2)

Public, unconditional MCA-family results for general linear codes (both cited
by BCHKS25 p. 28, both already in the `open-proximity.tex` bibliography):

- **[Zei24]** (Khatam, ePrint 2024/1843): double-Johnson `J(J(dmin))`. At
  `rho = 1/2`: `1 - (1/2)^{1/4} ~= 0.1591 < 1/4`.
- **[GKL24]** (ePrint 2024/1810): 1.5-Johnson `1 - (1 - dmin)^{1/3}`. At
  `rho = 1/2`: `1 - (1/2)^{1/3} ~= 0.2063 < 1/4`.
- [GCXK25] (ePrint 2025/870, `J(LDR(delta))` black-box) evaluates to
  `~0.159` at `rho = 1/2` under Johnson list decoding; [GG25]-type results
  target folded/random RS, not the deployed structured domain.

Both headline fallbacks sit **below the already-certified 1/4** at the
KoalaBear rate: no unconditional improvement is available from this family for
the `rho = 1/2` row. **Follow-up flag for clean-rate rows:** the comparison
flips at low rate — at `rho = 1/16`, GKL24's `J_1.5 ~= 0.603` clears the
half-distance edge `(1 - rho)/2 = 0.469`, so a GKL24 error-term audit is a
candidate *unconditional* safe-edge improvement for the `rho <= 1/16` rows.
Not done here.

## Item 5 — Consistency with the repository (clean; discharges nothing)

- **`prop:p2-half-sharp`** (`tex/towards-prize.tex` ~522): for
  `max(2, ceil(d/2)) <= r <= d-2` it builds a sparse pair with a
  non-tangent MCA-bad-not-CA-bad slope `gamma_0 = 0`. At KoalaBear parameters
  the family starts at `r = 524,289` (`delta ~= 0.2500005`) and overlaps the
  entire imported band. **Not a contradiction:** the construction certifies
  exactly **one** mutual-only slope per pair — a sharpness witness against the
  half-distance identity `epsmca <= max(epsca, r/q)`, not a mass lower bound.
  Thm 4.6 caps the per-pair count at `B(delta)` (`~2^42.6` at `delta = 1/4+`
  up to `~2^57.9` at the edge). A genuine conflict would need `omega(n)`
  mutual-only slopes for one pair at fixed `eta > 0` below Johnson; the
  construction yields O(1). The import is consistent with the proposition and
  discharges nothing about it.
- **`thm:sparsify` / `thm:transfer`** (`tex/towards-prize.tex` ~661, ~780): via
  `epsmca = max(epsca, sigma_C(delta)/q)`, the import pins
  `1 <= sigma_C(delta) <= B(delta) = O_eta(n)` on the band — exactly the
  "poly sigma_C" regime hypothesized by `thm:transfer`. Conditionally on
  [Hab25], the import simultaneously discharges that hypothesis on
  `delta <= 604085/2^21` and short-circuits it by bounding `epsmca` directly.
- **Unsafe side:** `cor:widened-deployed` certifies failure on
  `[15331/32768, 1/2) = [0.46787..., 1/2)`; the new v13 **experimental**
  identity-prefix edge `981109/2^21 ~= 0.4678292` (agents-log 2026-07-04) is
  sharper but still disjoint from the imported band (`<= 0.2880502`). No
  conflict.
- **BCHKS25's own Johnson-crossing lower bound** (Cor 1.7 via Thm 1.6, tau=2):
  consistent on three grounds — Thm 4.6's range is open at Johnson; its
  constant `~(2 rho/3) n / eta^5` reaches the `n^2` scale already at
  `eta ~ n^{-1/5}`, matching the O(n)-below / Omega(n^{2-o(1)})-at picture;
  and the lower-bound family is char-2 at `rho = 1/16`, not the KoalaBear row.
- **Interaction with the v12 outstanding-corrections note**
  (`cs25_v12_outstanding_corrections.md`): its Finding 1 records a
  proof-clarity gap in `cor:conditional-half` (hypothesis `2*floor(delta*n)
  <= n-k` vs the import wording `delta <= (1-rho)/2`); soundness unaffected.
  The corollary below quantifies over open `delta` ranges directly and
  instantiates integer radii explicitly, so it does not inherit the wording
  gap. Nothing in the corrections note touches `def:mca`, `thm:transfer`, or
  `thm:sparsify`.

## Item 6 — Relation to the in-repo empirical lanes (and to the external census)

**Adjacent in-repo lane:** `experimental/data/certificates/sigma-c-sparse-census/`
(expanded in commit `59ea69f`, with the Lean finite anchor
`SigmaCSparseLedger.lean`) records exact `sigma_C` values for tiny rows —
`(q,n,k,r) = (7,6,3,2)`, `(11,10,7,2)`, `(13,12,9,2)`, `(17,16,12,2)`,
`(17,16,13,2)` — all **saturating** the finite-slope cap `sigma_C = q_line`,
under the same M0 conventions this bridge uses (finite slopes, denominator
`q_line`, maximal witness set). This is fully consistent with the import:
every censused row sits deep in Thm 4.6's **vacuous regime** — the bound
`B(delta)` evaluates to `~5e5` (q=7 row) up to `~1.4e11` (17,16,13,2), always
`>> q_line` — so the theorem constrains nothing there, and conversely those
rows cannot test its numeric content. The same holds for the toy
`exact-worstcase-eca-emca-staircase` rows (q <= 17). The bound only bites when
`q >> n / eta^5`, i.e. exactly the deployed large-field regime. A numerically
meaningful finite cross-check would need a small-n, large-q row
(e.g. n = 16, q ~ 2^30 with per-instance slope scans); flagged as optional
follow-up, not attempted here (cost unassessed).

**External statement-shape cross-check:** the frozen MCA-vs-CA sparse-layer
census at `github.com/latifkasuli/mca` (`docs/mca-ca-sparse-layer-census.md`,
frozen artifact `runs/mca_ca_sparse_layer_census.json`, commit `e16dd12`)
probes the *shape* Thm 4.6 constrains rather than the size of `sigma_C` at a
fixed radius. Precisely how it differs from the in-repo census: the in-repo
lane measures the **value** of `sigma_C` at fixed small radius (r = 2) per row;
the external census tracks the **mechanism** of the mutual-only layer as a
function of the radius *through and past the Johnson band* on rows
`(F_17, n=8, k in {4,2})` (exhaustive) and `(F_97, n=16, k=8)` (engine-exact),
per-slope: it falsifies the naive tangent-containment extension of
`thm:mca-from-ca` one step past unique decoding (a committed pair with all 17
slopes MCA-bad against a singleton pair list), locates every violating witness
at joint decomposition depth exactly `n-k`, and measures a violation density
tracking the ball-density heuristic `J`, with an exact-equality window at the
Johnson edge (`F_97`, r=5: extras = tangent union of the radius-5 pair list,
zero exceptions) and the flood wall at the **capacity radius n-k, not at
Johnson**. That picture — sparse-layer mass negligible throughout the Johnson
band at large q, exploding only near capacity — is the qualitative content of
Thm 4.6, checked without any dependence on [Hab25]. Both censuses live in the
`B > q` regime and are shape checks, not bound checks.

## Item 7 — Related-work citation gap (rescoped after recon)

The external audit's gap flag must be narrowed: **the survey layer already
cites this landscape** (`open-proximity.tex`: BCHKS25, Hab25 = ePrint
2025/2110, Zei24, GKL24, BCGM25, GG25, KK25; `tex/snarks_v5.tex`: Hab25,
Hab24). The remaining gaps:

- The certificate-bearing papers `tex/cs25_cap_v12.tex` and
  `tex/towards-prize.tex` cite none of Hab25/Zei24/GKL24; in particular
  `thm:transfer`'s discussion of the Johnson-regime target would naturally
  cite BCHKS25 Thm 4.6 + Hab25 as the (conditional) state of the art.
- ACFY25 Conjecture 4.12 (the WHIR mutual-correlated-agreement conjecture,
  which Thm 4.6 with M >= 1 resolves in curve form, conditionally on [Hab25])
  is not cited by number anywhere in the repository.

## Item 8 — Flags to relay to the BCHKS25 authors

1. **Thm 1.6 tau = 1 corner (presentation).** As literally stated ("Let tau be
   a fixed positive integer, and lambda_tau = 2^{-(tau+2)} ... delta = 1 -
   lambda_tau and gamma = 1 - 4 lambda_tau ... |{z : Delta(f + z g, C) <=
   gamma}| >= (1 - o(1)) q"), the statement admits tau = 1, where
   `lambda = 1/8`, `rho = 1/8`, `gamma = 1/2 < J = 1 - sqrt(1/8) ~= 0.6464`:
   an essentially-full bad-slope set strictly below Johnson, colliding with
   their own Thm 1.5/4.2 upper bound `O_{gamma,delta}(n)`. The construction is
   evidently intended for tau >= 2 (tau = 2 is exactly Johnson-tight:
   `4 lambda = sqrt(lambda)` at `lambda = 1/16`; the paper's p. 10 commentary
   treats tau = 2 as the tight case). No effect on §§2--4 or on this import.
2. "Johson" typo in Thm 4.6's title; `A ⊂ D` vs `⊆` in the event.

## Drafted corollary (upstream conventions, `cor:conditional-half` packaging)

```latex
\begin{corollary}[conditional safe frontier near the Johnson radius;
                  imports {\cite[Thm.~4.6]{BCHKS25}} via {\cite{Hab25}}]
\label{cor:conditional-johnson}
Let $C=\RS[\F,D,k]$, $\rho=k/n$, $q=|\F|$, and set $\rho_B:=(k-1)/n$. Import the list
(mutual) correlated agreement theorem of \cite[Thm.~4.6]{BCHKS25} at $M=1$, instantiated at
their code parameter $k_B:=k-1$ (their $\RS_k[\F_q,D,k_B]$ has dimension $k_B+1=k$, matching
$C$): in the normalization of \cref{def:mca}, for every $\delta\in(0,\,1-\sqrt{\rho_B})$,
\[
\emca(C,\delta)\ \le\ \frac1q\left(
\frac{2(m+\tfrac12)^5+3(m+\tfrac12)\,\delta\,\rho_B}{3\rho_B^{3/2}}\;n
\;+\;\frac{m+\tfrac12}{\sqrt{\rho_B}}\right),
\qquad
m=\max\Bigl(\Bigl\lceil\tfrac{\sqrt{\rho_B}}{1-\sqrt{\rho_B}-\delta}\Bigr\rceil,\,3\Bigr).
\]
\textup{(Provenance: the statement is bridged verbatim to \cref{def:mca} --- support-wise
witness, finite affine sampler, count$/q$ --- but its proof is only sketched in
\cite[\S4.3]{BCHKS25} and attributed to \cite{Hab25}, cited there as an unpublished personal
communication and since recorded as ePrint 2025/2110, whose proof has not been audited here;
this import is a conditional dependency in the sense of the M0 freeze rule. For the
projective sampler add $1$ to the numerator and use denominator $q+1$.)}
Deployed instantiation \textup(KoalaBear sextic row: $n=2^{21}$, $k=2^{20}$, $q=p^6$,
$p=2^{31}-2^{24}+1$\textup): for every integer radius $r\le604{,}085$, i.e.\ every
$\delta\le 604085/2^{21}\approx0.2880502$ \textup(agreement $a=n-r\ge1{,}493{,}067$\textup),
the bands $m\le146$ apply and
\[
\emca(C,\delta)\ \le\ 2^{57.889}/q\ <\ 2^{-128.04}\ <\ 2^{-128},
\]
while at $r=604{,}086$ the band $m=147$ exceeds the budget
\textup($2^{57.938}>q\,2^{-128}\approx2^{57.932}$\textup). Combined with
\cref{cor:conditional-half} \textup(which remains tighter, $n/q<2^{-164}$, for
$\delta\le\tfrac14$\textup), the certified safe frontier of the row moves from $\tfrac14$ to
$604085/2^{21}$, i.e.\ $88.7\%$ of the way to the Johnson radius
$1-\sqrt{\rho}\approx0.2928932$; by \cref{thm:sparsify} the same import bounds the sparse
mutual layer, $\sigma_C(\delta)\le q\,\emca(C,\delta)$, discharging the hypothesis of
\cref{thm:transfer} on this range.
\end{corollary}
```

## What to do next

1. **Fetch and audit [Hab25] = ePrint 2025/2110** against `def:mca`; on a
   clean proof audit, the corollary's condition upgrades from
   conjecture-tier to ordinary-import tier (parallel to `thm:B`). Until then
   the frontier stays conditional and is not a leaderboard row.
2. Decide whether to correct the `open-proximity.tex` rendering (rate
   direction `rho_+` vs exact `rho_B = rho - 1/n`; the `m = ceil(sqrt(rho_+)/
   (2 eta))` undershoot as printed).
3. Separate follow-up: GKL24 (ePrint 2024/1810) error-term audit for the
   `rho <= 1/16` rows, where 1.5-Johnson clears the half-distance edge
   unconditionally.
4. Optional: a finite cross-check row in Thm 4.6's non-vacuous regime
   (small n, `q >> n/eta^5`), where the bound has numeric content; all
   current census rows (in-repo and external) are in the vacuous `B > q`
   regime and test only the statement shape.
5. Relay the author flags (Item 8) alongside any upstream correspondence on
   the Hab25 ePrint.
