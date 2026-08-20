# Independent certificate and custody review

Date: 2026-08-13

Reviewer role: isolated certificate, provenance, build, mutation, and public-wording auditor

Artifact reviewed: payload
`ca624392d1842a69ca9212533af672e4325fa984dad11952443e247db80cb6c3`

Status: **GREEN**

## Scope

I reviewed the frozen KoalaBear rank-eleven pair/core route-cut packet as a
certificate and custody artifact.  I did not generate or edit its theorem,
note, release verifier, Sage verifier, campaign ledgers, or packet manifest.
This review file is deliberately excluded from `PACKET_FILES`.

The review covers exact file custody, canonical serialization, arithmetic
replay, hostile mutations, finite-field controls, dependency pins, units,
signs, result boundaries, public wording, parent diff, campaign hygiene, and
the full TeX build.  The separate mathematics review is the authority for the
informal proof joints; I independently checked that the certificate encodes
the reviewed theorem and does not strengthen its conclusion.

## Frozen payload and file custody

The manifest contains exactly 21 packet paths, and its path list agrees
exactly with the keys of `packet_file_sha256`.  I independently read every
file as bytes and recomputed every SHA-256.  All 21 hashes match.

I then removed only the top-level `payload_sha256`, serialized the remaining
object with sorted keys and compact separators, and independently obtained

```text
ca624392d1842a69ca9212533af672e4325fa984dad11952443e247db80cb6c3
```

which equals the sealed payload.  The manifest file itself has SHA-256

```text
f4b573b7a55474da707076d5b9ddd8d87304246ac0bfe0e57fba5d7fda30a509.
```

During the provisional review, one README clarification had been added after
the older `de47a1ce...` seal.  The old verifier correctly failed closed.  The
coordinator then froze and resealed the current bytes.  The final candidate
has no hash mismatch; the pre-freeze failure is evidence that the custody
gate detects drift, not a defect in the final packet.

## Provenance and parent boundary

The exact parent commit exists locally as a commit:

```text
491ccdf53d54846f5a013b808960645275c64ed3
```

and equals the locally tracked PR #1167 head.  Its ancestry contains the
restacked #1166 dependency `b67078c7c0254ce9e54e5748634de5133fae98ef`.
The recorded upstream-main refresh
`93fba1be3f3299b0ba4708d88715377bbb656e45` agrees with the local upstream
reference used for this packet.

The tracked parent diff is narrow and additive: `agents.md` changes by
`+2/-1`, `experimental/agents-log.md` by `+25`, and
`experimental/grande_finale.tex` by `+187`.  `git diff --check` passes.  No
parent theorem or prior result is deleted.  The new note, verifiers,
certificate, and campaign are separately added packet artifacts.

The README explicitly classifies
`scratch/scan_weighted_pair_core.py` as a superseded discovery artifact with
the weaker factor-two endpoint normalization.  It is excluded from the
packet.  The release verifier is unambiguously authoritative, so the
preserved scratch file cannot silently redefine the certified result.

## Exact verifier and hostile mutations

The release verifier passed in normal and optimized Python modes:

```text
KB_MCA_RANK11_PAIR_CORE_ROUTE_CUT_PASS
unconditional=813929118931913384
conditional=811958533186703629
conditional_over=536977805075308542
```

Its mutation mode rejected all `6/6` hostile changes, covering:

1. the unconditional total;
2. the resource-coupled total;
3. the fixed-pair deficiency wall;
4. false promotion of the abstract packing to RS realizability;
5. false rank-eleven payment; and
6. substitution of the base field for the deployed sextic field.

The campaign experiment independently reproduced both pair terminals and
both ceilings in normal and optimized modes, and rejected all `5/5` of its
own mutations.  An independently written exact optimizer also reproduced:

- fixed-pair weight `743449148` at cutoff `6486`;
- fixed-pair record load `200632` at cutoff `1795`;
- the unconditional core-deficiency minimum
  `813929118931913384` at `J=19737`; and
- signed excess `538948390820518297` over the budget.

These independent scripts were used only for review and are not imported by
the release packet.

## Finite-field controls

Both exact Sage controls pass:

```text
KB_MCA_RANK11_PAIR_CORE_ROUTE_CUT_SAGE_PASS
parallel_records=9 deficiency=1 sharp_capacity=9

KB_MCA_RANK11_GF7_PARALLEL_STAR_PASS
field=7 n=6 post_near=1 parallel=4 n_minus_A=4
```

They verify exact support, strict post-near behavior, same-support pair
noncontainment, common-pair core, parallel records, and the sharp local
multiplier.  The packet consistently says that neither toy realizes
KoalaBear affine error rank eleven.  They therefore falsify only the
distinct-neighbor or reduced one-pair-multiplier shortcut and do not
over-certify the official row.

## Units, normalization, guards, and signs

An independent standard-library reconstruction confirmed

```text
m = K+w = 1116048
2w = 134944
E = B_*-2w+1 = 274980728111260144
C_10 = 106618568137036225644
|F| = 2130706433^6
```

At the two official cutoffs it independently reproduced:

| cutoff | pair cap | forced pair weight | forced records |
|---:|---:|---:|---:|
| 6486 | 2255946383610 | 743449148 | 114624 |
| 1795 | 1075288922022 | 360132809 | 200632 |

The sub-square checks pass over the actual sextic line field and fail to
justify replacing it by the base prime; the field mutation is explicitly
tested.  Counts remain distinct finite affine slopes per actual received
line.  Supports, pair labels, minimizers, endpoint vertices, and graph
incidences are not substituted for slopes.

The signs are correct:

```text
B_* - 813929118931913384 = -538948390820518297
B_* - 811958533186703629 = -536977805075308542
```

Both method ceilings remain over budget.  The first is derived from the
printed threshold theorem plus cumulative pair/core bounds.  The second
uses the new nonuniform sum-of-margins theorem.  The manifest, note, source,
and reviews consistently preserve that dependency distinction.

The two optimized pair rows are separately quantified existentials; the
packet does not claim that one pair simultaneously attains both.  The direct
ordered-pair pigeonhole has no factor two.  Parallel owned slopes are not
called distinct neighbors.

## Campaign and build gates

The actionable campaign audit passes:

```text
ok=true
ideas=4
claims=3 (all candidate)
reviews=3
review_status_rows=15
dependencies=5
```

The multi-axis table correctly leaves public wording open until this custody
review; it does not use the campaign audit as proof of the theorem.

A fresh TeX Live build from a new output directory completed successfully:

```text
exitCode=0
pages=122
pdf size=1119632 bytes
```

The log has no undefined citations or references, multiply defined labels,
or overfull boxes.  The reported underfull boxes are pre-existing layout
warnings and do not affect the new theorem or cross-references.

## Public wording and result boundary

The workboard, agents log, theorem source, threshold note, README, campaign
contract, proof memo, and barrier audit consistently describe this as a
local route cut.  They expressly state:

- error rank eleven remains unpaid;
- active-v4 ledger movement is zero;
- KoalaBear is not closed;
- the abstract singleton packing is not asserted RS-realizable;
- the finite stars are local negative controls; and
- the missing result must couple different actual fixed pairs or provide a
  chronology-correct owner for dense parallel cores.

I found no wording that promotes the route cut to a deployed payment,
complete KoalaBear proof, universal four-rate result, or prize closure.

## Verdict

**GREEN.**  Exact payload
`ca624392d1842a69ca9212533af672e4325fa984dad11952443e247db80cb6c3`
passes certificate, custody, provenance, mutation, control, campaign, diff,
unit, sign, public-boundary, and fresh-build review.

No packet repair is required.  The packet is suitable for scoped
publication as a rank-eleven route cut, subject to retaining the exact
parent dependency and current nonclaims.  The next mathematical obligation
is the named same-line cross-pair compatibility/owner theorem; this review
does not supply or approve that missing payment.
