# M1 Cycle120 ABF Extract Source Hash Audit

Status: AUDIT / ABF-PDF-EXTRACT-SOURCES-VERIFIED.

Date: 2026-06-24.

This note records the executable provenance check for the ABF PDF-extract
evidence used by the Cycle120 gate audit. It is not an official-source closure:
the direct ePrint PDF/source fetch is still blocked from this environment and
must be checked independently before promotion.

The companion verifier is:

```text
python3 experimental/scripts/verify_m1_cycle120_abf_extract_sources.py
```

It requires the closed PR #96 head commit to be present locally:

```text
git fetch origin pull/96/head:refs/remotes/origin/pr-96
```

## What Is Checked

The verifier checks the PR #96 commit
`fdb3cacece5a7f71399f12c697bd5193806f82ef` and hash-binds:

```text
copied ABF PDF:
  e543ec6a4f3312b4383000e72e5aa23862e79cc9770ce21db2c48db679581de3

pdfplumber text extract:
  eac4031f15a8ab430541e7d31af82f1dc10c2686ee31ed9d8c14ef10c78ec344

pypdf text extract:
  1f0db1f08b6b00955039eb9376eac866ba2362e5a4ac97d30a95575e4073b255

Cycle120 ABF counterexample packet zip:
  da580c57f0cb9c6c56e3bab8106b4275ced3e8b4f876a410bf34f0b17ca538b2
```

It also checks the rendered source pages cited by the gate audit:

```text
page 5:  grand MCA challenge
page 9:  Definitions 2.11 and 2.12
page 17: Definition 4.3
```

For both text-extraction backends, the verifier confirms that:

```text
page 5 contains the grand MCA challenge anchors;
page 9 contains the Reed-Solomon and smooth-domain definition anchors;
page 17 contains the MCA definition anchors.
```

The check is intentionally fragment-level. It is meant to catch provenance
drift and gross source mismatch, not to replace human reading of the official
ABF PDF.

## Remaining Promotion Boundaries

This audit leaves the following boundaries open:

1. Independently fetch the official ABF ePrint PDF/source and confirm the
   revision.
2. Check that the copied PR #96 PDF is exactly the intended official ABF
   source.
3. Review the full source wording around the cited fragments, especially the
   row envelope, smoothness condition, sampler field, same-support predicate,
   and closed-threshold convention.
4. Review the finite Cycle84/Cycle116 proof chain separately.

Thus the Cycle120 claim remains source-conditioned, but the current local
source-extract dependency is now executable and hash-pinned.
