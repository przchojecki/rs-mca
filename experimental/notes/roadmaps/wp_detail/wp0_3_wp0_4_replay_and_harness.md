# WP-0.3 + WP-0.4 detail (L3): replay audits + the verification harness

- **Status:** execution plan; grounded counts from main (144 `verify_*`
  scripts in `experimental/scripts/`, 6 checkers in `scripts/`, 15
  certificate directories — the corpus is real and big enough to need
  automation).
- **Executability:** AGENT throughout (WP-0.3 is audit-only interaction
  with others' PRs: replays and comments, never edits; integration itself
  is MAINT).
- **Parents:** r2 WP-0.3, WP-0.4; standing orders 3 and 12; consumes
  `wp2_3` (the dedup convention) and `s8_s9` (the refusal rule).

## 1. WP-0.3: integration-readiness replay for #170/#171

**Protocol, per PR (pin to a named head SHA in the report):**

```text
(i)   enumerate: every verifier + certificate in the PR head (file list
      from the PR API; no local edits to their branches);
(ii)  replay: run each verifier in a clean checkout of the PR head;
      record exit status, runtime class, any nondeterminism;
(iii) independent re-derivation of the two LOAD-BEARING definitions:
      - Phi_{m,r,h}: re-derive from the spectral identity from scratch
        (my s3b_iii_2 V^T D V factorization is already an independent
        derivation of the underlying syndrome-section object — diff the
        two constructions symbolically at small m);
      - the rank-6 ambient sharpness example: reconstruct it from its
        stated properties, not its files;
(iv)  spot-audit three named theorems: affine-pivot compression,
      affine-pivot gcd-equivalence, subgroup syndrome-section — statement,
      proof step list, one numeric check each at toy scale;
(v)   divergence report: verifier | replayed? | matches derivation? |
      divergence notes — one table per PR;
(vi)  agents-log merge plan by timestamp (for MAINT's integration).
```

**Acceptance test:** the two replay notes exist with zero unexplained
divergences, and the alpha/beta target definitions match the independent
re-derivations — this is the unblocking condition for WP-2.1/2.2 scans
(standing order 12). **Failure branches:** a verifier fails replay ->
flag in the report and (if useful) as a PR comment, never a push to their
branch; a definition mismatch -> restate the alpha/beta targets against
the re-derived form BEFORE any scan (the scan must test mathematics, not
a transcription); PR head moves -> re-pin, diff, note the churn.

## 2. WP-0.4: `run_all_verifiers` + checker hardening

**Harness spec (`scripts/run_all_verifiers.py` or make target):**

```text
discovery   glob experimental/scripts/verify_*.py + scripts/check_*.py
            (144 + 6 today; new scripts auto-discovered);
manifest    per-script expected outcome (PASS / PASS-with-PENDING /
            SKIP-slow / MANUAL), runtime tier (fast <10s, slow, manual),
            and for certificate-consuming checkers the SHA-256 of every
            file under experimental/data/certificates/** (15 dirs today);
output      one PASS/FAIL/PENDING table + a one-line repo verdict;
            nonzero exit iff any non-manifest deviation;
CI shape    single entry point, no network, deterministic seeds only.
```

**Checker hardening (the packet checker, per r2 + s8_s9 refusal rule):**

```text
H1 removed-ledger references resolve to real ledger artifacts;
H2 declared numerators are RECOMPUTED from the packet's own root tables,
   never trusted;
H3 residual labels are from the allowed set (towards-prize §4.6);
H4 object / sampler / denominator / endpoint blocks present (S0 axes);
H5 cross-packet paid-root dedup enforced as checker logic, with the
   wp2_3 tree order as the single normative convention;
H6 the refusal rule: any prize-facing packet with an OPEN S0 axis or a
   conjectural ledger dependency fails outside labeled conditional mode.
```

**Negative-control suite (the part that makes the hardening real):** one
intentionally corrupted packet per failure class — dangling ledger ref,
inflated declared numerator, illegal residual label, missing sampler
block, double-counted paid root, unlabeled conditional dependency — and
the acceptance test is that ALL of them FAIL with the right diagnostic:

```text
PASS(harness) = green on main's existing corpus (manifest-normalized)
                AND all six negative controls red with correct reasons.
```

**Failure branches:** legacy verifiers exit nonzero on PENDING ->
manifest expectation, not code edits; slow verifiers -> tiered, CI runs
fast tier, cron runs slow tier; certificate regeneration churns hashes ->
manifest update is a reviewed diff, which is exactly the audit trail
wanted; a main verifier fails genuinely -> that is a FINDING for the
maintainer, filed with the replay-report format from §1.

## 3. What this buys

WP-0.3 converts "trust the PR's own green checkmarks" into independent
replay + re-derivation (the difference between testing mathematics and
testing transcription), and WP-0.4 turns 150 ad-hoc scripts into one
deterministic gate with a negative-control suite — the enforcement layer
that every downstream table (M4), packet, and dossier claim silently
assumes. Both are pure-AGENT work with no mathematical risk, schedulable
immediately and in parallel with everything else.
