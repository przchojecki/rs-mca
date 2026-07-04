# Prize Rules Parameter Pinning

## Claim

The commonly used parameter caps `k <= 2^40` and `|F| < 2^256` are present in
the companion ePrint/paper text, but not printed on the live Proximity Prize
landing page checked in this audit.

## Status

AUDIT.

## Parameters

- Access date: 2026-07-02 America/Denver / 2026-07-03 UTC
- Live page: https://proximityprize.org/
- Companion paper: ePrint 2026/680, reconstructed locally as `open-proximity.tex`
- Local source line: `open-proximity.tex:153`

## Existing Paper Dependency

`tex/towards-prize.tex` uses the ePrint parameter box in its prize-facing
framing, notably at lines 61, 68, and 81 in this checkout.

## Proof Idea Or Experiment

Compare the live prize page against the companion paper text and the repository
framing. The live page was checked for the strings `2^40`, `2^{40}`, `2^256`,
and `2^{256}`; these caps were not present there. The local ePrint
reconstruction contains both caps.

## Results

The live page states the challenge in terms of the grand MCA/list thresholds and
assumes the field is sufficiently large. It does not print the caps `k <= 2^40`
or `|F| < 2^256` in the fetched page text.

The companion paper text does print the parameter box. In the local
reconstruction:

```text
open-proximity.tex:153
... smooth domain, k <= 2^{40}, and |F| < 2^{256}.
```

`tex/towards-prize.tex` quotes the same parameter box:

```text
tex/towards-prize.tex:68
... smooth domain, k <= 2^{40}, and |F| < 2^{256}.
```

PR #174 historically flagged this provenance question as unresolved planning
context; it is now closed as of the 2026-07-03 upstream refresh. This local
check settles the rules-audit point as "ePrint-present, live-page-absent." The
same refresh shows PR #198 is now closed without merge, and the current open
PR set checked on 2026-07-03 is #209--#222; none of those open PRs overlaps this rules-provenance
note.

## Ledger Impact

Downstream notes should not say that the live prize page itself states the
`k <= 2^40` and `|F| < 2^256` caps. Safer wording:

```text
The companion ePrint paper linked from the Proximity Prize page singles out the
smooth-domain parameter box k <= 2^40 and |F| < 2^256.
```

Because the live page labels the statements preliminary, this provenance should
be rechecked before public submission text is finalized.

## Constants

No mathematical constant is changed. The audit only pins where the constants are
stated.

## Reproducibility

```sh
rg -n "2\\^\\{40\\}|2\\^40|2\\^\\{256\\}|2\\^256" open-proximity.tex tex/towards-prize.tex
```

For live-page verification, fetch https://proximityprize.org/ and search the
returned page text for the same strings.

## Non-Claims

- This note does not decide which parameter box the prize administrators will
  enforce.
- This note does not edit `tex/towards-prize.tex`.
- No public comment or PR was posted.
