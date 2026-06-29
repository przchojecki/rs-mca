# A1 Paper A finite-verification crosswalk

**Status:** AUDIT / PROVED for the finite computations listed below.

**Agent/model:** Codex, reviewing Claude Opus 4.8 output and the integrated
`rs-mca` experimental layer on 2026-06-18.

**Scope.** This note reconciles Claude's `PaperA-verification.md` claim with
the current repository scripts. It does not add a new asymptotic theorem and
does not edit Paper A. Its purpose is to make the Appendix A finite claims
reviewable from already-integrated, reproducible commands.

## Claim

Paper A `tex/RS_disproof_v3.tex`, Appendix A, records exact finite checks V1
through V5. Claude's note says these checks reproduce the paper values. The
current repository already contains scripts that reproduce the same finite
arithmetic, but the coverage is split across several files.

This crosswalk identifies the exact script path for each Appendix A item,
records the command that was rerun, and separates verified material from
Claude export files that should not be committed without recovery.

## Claude files reviewed

The Claude output set was surfaced as an export under a Claude local-agent
session and included:

```text
experimental/agents-log.md
experimental/PaperA-verification.md
experimental/README.md
experimental/verify_paperA_finite.py
experimental/verify_paperA_finite.report.json
experimental/verify_paperB_finite.py
experimental/verify_paperB_finite.report.json
experimental/__pycache__/
```

Only `agents-log.md` and `PaperA-verification.md` had already been copied into
the Codex workspace output tree. The short-path references to the verifier
scripts and JSON reports resolve as Claude export handles, but the underlying
`outputs/rs-mca/experimental` directory is not reliably traversable from this
workspace. Therefore this note does **not** import those files. Instead it
verifies the same Paper A claims through the current repository scripts.

The `verify_paperB_finite.py` / `.json` pair is not assessed here. It should be
reviewed separately against Paper B labels and must not be bundled into an A1
Paper A commit without a separate status note.

## Crosswalk

| Paper A item | Paper claim | Repository command | Status |
|---|---|---|---|
| V1 | Fermat quotient coverage: for `p in {17,257,65537}`, the relevant restricted sumset in `Q=<2>` has size `p-1` and misses only `0`. | `experimental/scripts/restricted_sum_dp.py` commands listed below. | PROVED finite DP. |
| V2 | `p=257` locator expansion and pointwise agreement for all 144 support points. | `python3 experimental/scripts/p257_locator_certificate.py` | PROVED exact enumeration. |
| V3 | For `p=17,n=16,k=8`, 9-subset sums have distribution `672/673`. | `python3 experimental/scripts/verify_q17_locator_mca.py` | PROVED exact exhaustive scan. |
| V4 | Ladder rung: `p=12289`, `N=256`, `|129^wedge Q_256|=12289`. | `python3 experimental/scripts/restricted_sum_dp.py --p 12289 --subgroup-order 256 --r 129 --expect-full` | PROVED finite DP. |
| V5 | `N=16,r=9` cyclotomic family count `3280` and reductions at six primes. | `python3 experimental/scripts/sieve_mechanism_certificate.py` | PROVED exact formal/enumerated certificate. |
| Deployed-field arithmetic around Paper A main theorem (a) | BabyBear, KoalaBear, and `3*2^30+1` DSH divisor inequalities. | `python3 experimental/scripts/deployed_dsh_certificate.py` | PROVED integer arithmetic certificate. |
| Extension/tower arithmetic | Fermat/Proth full-density and Goldilocks density prerequisites. | `python3 experimental/scripts/extension_full_density_certificate.py`; `python3 experimental/scripts/goldilocks_density_certificate.py` | PROVED arithmetic certificates for stated scope. |

## Reproducible command log

Run from the repository root with `python3` (all scripts live in
`experimental/scripts/`).

```bash
python3 experimental/scripts/deployed_dsh_certificate.py
python3 experimental/scripts/p257_locator_certificate.py
python3 experimental/scripts/sieve_mechanism_certificate.py
python3 experimental/scripts/extension_full_density_certificate.py
python3 experimental/scripts/goldilocks_density_certificate.py
python3 experimental/scripts/verify_q17_locator_mca.py
```

V1 Fermat quotient coverage uses the quotient subgroup `Q=<2>`, whose order is
`2M` for `p=2^M+1`. These are the exact commands rerun:

```bash
python3 experimental/scripts/restricted_sum_dp.py --p 17 --subgroup-order 8 --r 5 --expect-size 16
python3 experimental/scripts/restricted_sum_dp.py --p 17 --subgroup-order 8 --r 3 --expect-size 16
python3 experimental/scripts/restricted_sum_dp.py --p 257 --subgroup-order 16 --r 9 --expect-size 256
python3 experimental/scripts/restricted_sum_dp.py --p 257 --subgroup-order 16 --r 5 --expect-size 256
python3 experimental/scripts/restricted_sum_dp.py --p 65537 --subgroup-order 32 --r 17 --expect-size 65536
python3 experimental/scripts/restricted_sum_dp.py --p 65537 --subgroup-order 32 --r 9 --expect-size 65536
```

V4 ladder rung:

```bash
python3 experimental/scripts/restricted_sum_dp.py --p 12289 --subgroup-order 256 --r 129 --expect-full
```

## Verification notes

- The V1 checks must use the small quotient subgroup `Q=<2>`, not the full
  group `F_p^*`. Running the same DP on `F_p^*` gives full-field coverage
  including `0`, which is a different object and does not match Appendix A's
  "unique missing element is 0" statement.
- The DP invariant in `restricted_sum_dp.py` is the exact finite statement:
  after processing a prefix of the element list, `state[j]` is exactly the set
  of sums of `j` distinct processed elements. Descending updates ensure each
  element is used at most once.
- `p257_locator_certificate.py` checks the actual locator mechanism, not just
  a count: all `11440` subsets are examined, all supports have size `144`, and
  all expanded locator identities pass.
- `experimental/scripts/verify_q17_locator_mca.py` contains the V3 distribution as
  the `N=16`, `rho=1/2`, slack-one case: one slope has `672` supports and the
  other sixteen slopes have `673`, totaling `binom(16,9)=11440`.
- The extension and Goldilocks certificates are arithmetic support for Paper A
  examples. They do not verify analytic inputs such as Siegel-Walfisz or any
  asymptotic density theorem.

## Integration decision

Do not commit Claude's `__pycache__/`.

Do not commit the Claude `verify_paperA_finite.py` or JSON report unless the
actual files are recovered and reviewed. They may still be useful as a
single-script convenience wrapper, but the finite claims are already covered by
repository-native scripts listed above.

This note itself is commit-ready as an `experimental/` audit aid because it:

1. replaces a prose-only Claude claim with exact commands;
2. prevents a reviewer from confusing `Q=<2>` with the full multiplicative
   group in V1;
3. records which Paper A finite checks are already covered by existing scripts;
4. keeps Paper B verifier files out of the Paper A audit lane until separately
   reviewed.

## Commit placement

If accepted, commit this file on a fresh branch from:

```text
przchojecki/rs-mca main @ 84b6dfa108b3825b4da1fda7d150ecf12f969232
```

Suggested branch:

```text
codex/a1-paperA-crosswalk
```

Suggested commit message:

```text
Add Paper A finite verification crosswalk
```
