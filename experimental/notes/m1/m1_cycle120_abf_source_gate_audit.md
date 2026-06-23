# M1 Cycle120 ABF Source Gate Audit

Status: AUDIT / SOURCE-PARTIAL / PDF-EXTRACT-DEPENDENT.

Date: 2026-06-23.

This note records the source status for the Cycle120 ABF-facing M1 candidate.
It is deliberately narrower than a theorem note: it checks which source gates
are already supported by independently reachable public material, which gates
are supported only by the PR #96 ABF PDF extract, and which questions remain
fatal if the official PDF later differs.

It does not import the copied ABF PDF, rendered pages, HTML snapshots, raw model
returns, or generated packet from PR #96.

## Source Tiers

### Tier 1: independently reachable public sources

The public Proximity Prize page was reachable on 2026-06-23:

```text
https://proximityprize.org/
```

It confirms the prize-facing grand MCA envelope:

```text
C = RS[F,L,k] over a smooth evaluation domain L subset F,
rate in {1/2, 1/4, 1/8, 1/16},
epsilon* example 2^-128,
determine the largest delta*_C with epsilon_mca(C,delta*_C) <= epsilon*.
```

It also labels the page and accompanying paper as preliminary, invites
feedback, and says partial progress may be considered. This is useful for
scope, but it does not define `smooth` or `epsilon_mca`.

Giacomo Fenzi's public author page was also reachable:

```text
https://gfenzi.io/
```

It identifies the paper

```text
Open Problems in List Decoding and Correlated Agreement
Gal Arnon, Dan Boneh, Giacomo Fenzi
IACR ePrint 2026/680
```

The direct ePrint endpoint was not reachable from this environment. A direct
header fetch of

```text
https://eprint.iacr.org/2026/680.pdf
```

returned an HTTP 403 Cloudflare challenge on 2026-06-23. The same obstacle is
already recorded in
`experimental/notes/audits/a0_external_import_source_check_20260618.md`.

### Tier 2: repository-local ABF-aligned definitions

The local Paper D definitions in `tex/cs25_cap_v4.tex` align the repository's
notation with ABF Definition 4.3. In particular, `def:mca` defines
`emca(C,delta)` as a maximum over `f1,f2`, with probability over
`gamma <- F`, of a same-support event:

```text
exists S subset D, |S| >= (1-delta)n,
f1 + gamma f2 is code-explained on S,
(f1,f2) is not simultaneously explained on that same S.
```

This is repository-authoritative for the local theorem chain, but it is not an
independent external-source check.

The local blueprint file `tex/proximity_blueprint_v3.tex` restates the survey
envelope as smooth-domain RS with rates
`{1/2,1/4,1/8,1/16}`, target `2^-128`, `k <= 2^40`, and `|F| < 2^256`.
Again, this is useful local alignment, not a replacement for the official PDF.

### Tier 3: PR #96 ABF PDF extract

The closed PR #96 branch contains a copied ABF PDF and text extracts under:

```text
experimental/notes/m1/cycle119_official_source_audit/abf_pdf_extract/
```

The copied PDF hash on the fetched PR ref is:

```text
e543ec6a4f3312b4383000e72e5aa23862e79cc9770ce21db2c48db679581de3
```

The extracted text records the source pages used by the raw Cycle120 audit:

```text
page 5: grand MCA challenge,
page 9: Definitions 2.11 and 2.12,
page 17: Definition 4.3.
```

Because the PDF was obtained from a closed PR branch rather than independently
downloaded from ePrint in this session, this tier should be treated as
PDF-extract evidence, not final source closure.

## Gate Matrix

| Gate | Best current evidence | Cycle120 status |
| --- | --- | --- |
| Paper identity | public Proximity Prize page and Fenzi author page | PASS |
| Grand MCA row shape | public Proximity Prize page | PASS |
| Rate `1/2` allowed | public Proximity Prize page | PASS |
| Target `2^-128` | public Proximity Prize page | PASS |
| RS over arbitrary finite field | PR #96 ABF extract, Definition 2.11 | PDF-EXTRACT PASS |
| Smooth domain definition | PR #96 ABF extract, Definition 2.12 | PDF-EXTRACT PASS |
| Uniform `gamma <- F` sampler | PR #96 ABF extract, Definition 4.3; local Paper D `def:mca` | PDF-EXTRACT PASS / LOCAL PASS |
| Same-support noncontainment | PR #96 ABF extract, Definition 4.3; local Paper D `def:mca` | PDF-EXTRACT PASS / LOCAL PASS |
| Closed threshold `|S| >= (1-delta)n` | PR #96 ABF extract, Definition 4.3; local Paper D `def:mca` | PDF-EXTRACT PASS / LOCAL PASS |
| No `q_chal` or quotient/event filter in `epsilon_mca` | absence from audited Definition 4.3 and public challenge wording | PASS FOR AUDITED GRAND MCA TEXT |

The last row is intentionally phrased narrowly. Protocol sections may add
protocol-specific checks, but the audited grand MCA quantity is stated directly
in terms of `epsilon_mca(C,delta)`.

## Row Consequence Under The Audited Gates

Assume the PR #96 ABF extract is faithful to ePrint 2026/680.

Then the row

```text
K = F_17^32,
H = <theta> <= K^*,
|H| = 512,
C = RS[K,H,256]
```

passes the ABF source gates:

```text
finite field:       K = F_17^32,
smooth domain:      H is the subgroup case of a power-of-two smooth domain,
rate:               256/512 = 1/2,
degree envelope:    256 <= 2^40,
field envelope:     17^32 < 2^256,
sampler:            gamma is sampled from K,
predicate:          support-wise same-support MCA noncontainment.
```

At `delta=125/256` and `n=512`, the printed closed support threshold is

```text
(1-delta)n = 262.
```

So the Cycle116 agreement-262 theorem is already the ABF-critical input. The
Cycle119 agreement-263 theorem is a one-symbol strict-ball strengthening, not a
necessary ABF threshold repair.

## Source-Conditioned Claim

The strongest claim supported by this audit is source-conditioned:

```text
If the PR #96 ABF PDF extract is faithful to the official ABF ePrint source,
and if the Cycle84 finite count plus Cycle116 fixed-jet transfer are correct,
then

epsilon_mca(RS[F_17^32,H,256],125/256)
  >= 52,747,567,092 / 17^32
  > 2^-128.
```

This is a negative certificate at one radius for one ABF-admissible row. It is
not an exact determination of `delta*_C`, an ordinary list-decoding theorem, a
protocol soundness failure, a prime-field/deployed-row result, or an accepted
prize submission.

## Fatal Checks Still Open

Before promotion, a human reviewer should still discharge:

1. Independently fetch the official ABF PDF or source from ePrint and verify
   Definitions 2.11, 2.12, and 4.3 with page references.
2. Confirm that no later official revision changes the row envelope, smoothness
   definition, sampler field, or support-wise predicate.
3. Tie the finite `H=<theta>` assertion to the Cycle84/Cycle116 certificate:
   `H` must be the intended order-512 subgroup of `K^*`, where
   `K = F_17^32`.
4. Review the Cycle84 finite numerator and the Cycle116 fixed-jet transfer
   independently from generated proof text.

If any of these checks fails, the Cycle120 contract should be revised before
public use.

## Next Review Target

The next useful PR increment is not another gate note. It is a compact
Cycle84/Cycle116 finite-chain review:

```text
Cycle84 count N = 52,747,567,092
  -> fixed-jet transfer
  -> smooth row RS[F_17^32,H,256]
  -> support-wise agreement 262 and noncontainment.
```

That is now the main mathematical bottleneck after the source-gate audit.
