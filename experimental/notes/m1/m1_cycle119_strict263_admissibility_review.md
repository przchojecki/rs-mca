# M1 Cycle119 Strict-263 Admissibility Review

Status: CONDITIONAL / AUDIT / STRICT-BALL-THEOREM-CHECKED.

Date: 2026-06-23.

Source PR: `#96`, DannyExperiments, new commits through `2965689`.

## Executive Read

Cycle119 is potentially important, but the branch is not integrable as-is. The
PR adds another large generated archive: 678 files and about 201k inserted
lines, including raw model returns, zips, generated checkers, and generated
review folders. None of that should be merged into the streamlined
`experimental/` tree.

The useful mathematical claim is compact:

```text
K = F_17^32
H = <theta> <= K^*, |H| = 512
C = RS[K,H,256]

LD_sw(C,263) >= 52,747,567,092.
```

The claimed upgrade over Cycle116 is agreement `263` instead of `262`, so the
Hamming distance is at most:

```text
512 - 263 = 249 < 250 = (125/256) * 512.
```

This closes the external strict-ball objection if the two-ended locator proof
is correct.

## What Was Double-Checked

This review did not run PR code. It inspected PR text, local paper definitions,
and public prize wording.

Arithmetic:

```text
17^32 = 2367911594760467245844106297320951247361
floor(17^32 / 2^128) = 6
52,747,567,092 > 6
```

Thus the proposed numerator would indeed imply:

```text
52,747,567,092 / 17^32 > 2^-128.
```

Numerically this density is about `2^-95.18`, so the denominator threshold is
not the tight part of the claim.

Local definition alignment:

- `tex/cs25_cap_v4.tex` defines `emca(C,delta)` as a maximum over `f1,f2` of
  `Pr_{gamma <- F}` of the same-support noncontainment event.
- `tex/slackMCA_v3.tex` uses the same support-wise bad-slope denominator
  `#bad slopes / |F|`.
- `tex/RS_disproof_v3.tex` uses the same support-wise line-MCA notion.

Public Proximity Prize page:

- The grand MCA challenge uses `C = RS[F,L,k]` over a smooth domain
  `L subset F`.
- The allowed rates include `1/2`.
- The target is `epsilon_mca(C,delta) <= 2^-128`.
- The page is explicitly preliminary.

PR-supplied ABF PDF extraction says:

- `RS[F,L,k]` is over an arbitrary finite field `F`.
- Smooth means a multiplicative coset of a subgroup of `F^*` of power-of-two
  order.
- Definition 4.3 samples `gamma <- F`.
- Definition 4.3 uses the same-support event with
  `|S| >= (1-delta)n`.

I could not independently download the ABF PDF inside this session because the
ePrint PDF endpoint was inaccessible. The PR-supplied extraction matches our
local TeX definitions, but it should be independently checked from the official
PDF before any public claim.

## Admissibility Assessment

If the ABF text extracted in PR #96 is faithful, then the row appears
admissible for the grand MCA formulation:

```text
RS[F_17^32,H,256]
rate = 1/2
H is a power-of-two multiplicative subgroup
gamma is sampled uniformly from F_17^32
the predicate is support-wise same-support noncontainment
```

Under that reading, no independent `q_chal`, endpoint filter, quotient filter,
duplicate-slope charge, or retained-event rule appears in the grand MCA
definition. Those may matter for protocol variants, but not for the grand MCA
quantity as stated.

The later Cycle120 direct ABF admissibility audit in PR #96 makes the stronger
internal claim that, under ABF Definition 4.3 and the printed grand MCA
formulation, the row, support-wise predicate, uniform sampler, and absence of
extra filters pass. This review treats that as a useful workbench audit, not as
a prize ruling.

Important nuance: under the printed same-support threshold

```text
|S| >= (1-delta)n
```

at `delta=125/256`, `n=512`, the agreement threshold is exactly `262`. So
Cycle116's agreement-262 statement would already match the closed ABF
threshold. Cycle119's agreement-263 statement is stronger and addresses stricter
external conventions, but the ABF closed threshold does not appear to require
it.

## Proof/Computation Status

Do not promote this to a main-paper theorem yet.

The Cycle119 claim depends on two nontrivial components:

1. the Cycle84 finite computation giving the `52,747,567,092` numerator;
2. the Cycle119 two-ended locator transfer proof.

The two-ended idea is now isolated as a local theorem and verifier:

```text
experimental/notes/m1/m1_two_ended_fixed_jet_ldsw_theorem.md
python3 experimental/scripts/verify_m1_two_ended_fixed_jet_ldsw_theorem.py
```

That theorem avoids the invalid naive padding multiplication and constructs
the final `[512,256]` line in parity-check space using a common nonzero
constant coefficient plus the common selected high coefficients. The result
remains conditional on the Cycle84 finite computation and official-source
gates, but the two-ended proof-logic import is no longer only a prose request.

## Recommended External Wording

Use cautious, definition-pinned language:

```text
Under the printed ABF grand MCA formulation, the row
C = RS[F_17^32,H,256], |H|=512, appears admissible: H is a smooth
power-of-two multiplicative subgroup, the rate is 1/2, the predicate is ABF
support-wise epsilon_mca, and gamma is sampled uniformly from the code field.
Cycle119 gives the finite/source-scoped bound

LD_sw(C,263) >= 52,747,567,092.

Assuming the finite computation and the two-ended locator transfer are correct,
this gives

epsilon_mca(C,125/256) >= 52,747,567,092 / 17^32 > 2^-128.

This is a prize-facing negative counterexample candidate for that row under the
printed ABF formulation. It is not a complete determination of delta_C^* and it
is not an accepted prize solution.
```

## Cycle120 Integration Update

The later Cycle120 packet makes the same point more sharply: under the printed
ABF closed support threshold, Cycle116 agreement `262` is already enough at
`delta=125/256`, while Cycle119 agreement `263` is the strict-ball addendum.

The cleaned integration note is:

```text
experimental/notes/m1/m1_cycle120_abf_counterexample_candidate.md
```

That note records the direct two-ended algebra audit and keeps the result
conditional on independent review of the Cycle84/Cycle116 finite inputs and
independent retrieval of the ABF PDF.

The direct theorem/proof note is:

```text
experimental/notes/m1/m1_two_ended_fixed_jet_ldsw_theorem.md
```

## Integration Decision

Do not merge PR #96 as-is.

Keep only this compact audit. Do not import:

```text
new generated proof-record folders
cycle115--cycle120 prompt packets
raw returns
zips
generated checker folders
GitHub Actions or shell replay machinery
```

Also avoid marketing language. The project should classify this as one of:

```text
PROOF, once independently written and reviewed;
COMPUTATION, for the Cycle84 finite count;
HEURISTIC/AUDIT, for unreviewed generated proof sketches.
```

## Question To Send Back

The main remaining request to Danny is a clean finite-computation/source packet,
not another generated archive:

```text
Please provide:

1. Independent review material for the Cycle84 finite computation.
2. Exact ABF PDF/source references with page numbers.
3. A minimal nonmutating packet tying the finite count to the stated row.
4. No generated-checker or archive language; classify inputs as proof,
   computation, audit, or heuristic.
```
