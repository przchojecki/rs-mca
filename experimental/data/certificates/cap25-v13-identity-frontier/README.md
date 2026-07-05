# CAP25 v13 Identity-Frontier Certificate: Lower Staircase L(a0) > Threshold

- **Status:** EXPERIMENTAL / CONDITIONAL / AUDIT (matches the repo-wide status
  of `experimental/cap25_v13_experimental.tex`; **not** a Paper-D theorem row).
- **Agent/model:** Claude Fable 5, packaging pass (Wave-2 engineering task).
- **Scope:** this packet gives the v13 identity-scale (`c=1`) prefix-floor
  checker script a committed JSON certificate + README, matching the
  convention of every other 2026-07-04/05 packet under
  `experimental/data/certificates/`. It was the one exception found by
  Wave-1 recon: a bare script with no committed certificate trail.

## V14 update (2026-07-05)

The four printed `c=1` identity certificates above and in `certificate.json`
remain **exact as printed** — every `a0`, `a0+1`, `w`, `K`, edge fraction, and
margin bracket in this packet is unchanged, and `replay.sh` still replays it
untouched. What changes: the two **MCA** rows' "conjectured first safe"
reading of `a0+1` (KB MCA `1,116,044`; M31 MCA `1,116,022`) is **superseded by
the v14 moved frontier** — upstream PR #310, commit `f049b91` ("Material
correction: quantitative-deep-list-floor flips 1116044–1116047"), composes
`lem:v13f1-identity-prefix-floor` with `prop:quantitative-deep-list-floor`
and moves the two MCA rows' frontier pairs forward to `(1,116,047,
1,116,048)` (KB) and `(1,116,023, 1,116,024)` (M31); cross-validated against
the maintainer's v14 auxiliary script at commit `2b5b7ce`
(`python3 "experimental/scripts/towards v13/cap25_v14_moved_frontier_checks.py"`,
re-run this session, exit 0, margins `8.978`/`−22.197` bits KB-MCA,
`27.927`/`−3.259` bits M31-MCA). The two **list**-row certificates (KB list,
M31 list) are untouched by this correction. See the companion
`experimental/data/certificates/frontier-adjacent/{kb_mca,m31_mca}_v1.packet.json`
`v14_moved_pair` blocks and `experimental/notes/frontier-adjacent/frontier_adjacent_v13_rows_v1.md`'s
"V14 moved-frontier addendum (2026-07-05)" section for the full re-audit at
the moved pairs.

## What this certifies (and what it does not)

This packet certifies **only the lower (unsafe) staircase**:

```text
L(a0) > B*        (the identity-prefix construction produces more than the
                    row's threshold-many bad witnesses at agreement a0)
L(a0+1) <= B*      (the SAME construction no longer does, at a0+1)
```

for four deployed rows (`n=2^21, k=2^20, rho=1/2`: KoalaBear MCA/list,
Mersenne-31 line-round MCA/list), plus the superseded `c=2` and old `c=16/32`
rows as historical cross-checks (12 checks total).

**It does NOT certify the safe side.** "`a0+1` is the first safe agreement" is
an open problem (`prob:v13f1-frontier`, `experimental/cap25_v13_experimental.tex`
L1448-1464) — no exact upper ledger `U(a0+1) <= B*` exists anywhere in the
repo for any of the four rows (confirmed by exhaustive grep across
`experimental/`, `site/`, `tex/`, `scripts/`). `L(a0+1) <= B*` only shows this
*particular unsafe construction* stops firing one step past `a0` — per
`experimental/cap25_v13_experimental.tex` itself, this is not a safety proof.
See the companion packet family
`experimental/data/certificates/frontier-adjacent/` (`kb_mca_v1.packet.json`,
`kb_list_v1.packet.json`, `m31_mca_v1.packet.json`, `m31_list_v1.packet.json`)
for the (currently incomplete, `safe_certificates.status="OPEN"`) safe-side
ledger scaffold, covering all four rows.

## Source

- Checker script (unmodified, run as-is):
  `experimental/scripts/towards v13/cap25_v13_frontier_identity_exact_checks.py`
- Tex labels:
  - `lem:v13f1-identity-prefix-floor` — `experimental/cap25_v13_experimental.tex` L1341-1369
    (the pigeonhole construction: for every `m` with `K<=m<=n`, some received
    word explains `>= ceil(C(n,m)/|B|^w)` codewords/slopes, `w=m-K`).
  - `prop:v13f1-identity-frontier` — `experimental/cap25_v13_experimental.tex` L1373-1397
    (the deployed-row instantiation, `n=2^21, k=2^20`, giving the four `a0`
    values below).
  - `rem:v13f1-closure` — `experimental/cap25_v13_experimental.tex` L1466-1468
    (identity scale `c=1` is strictly the extremal member of the
    `c=1,2,4,8,16,32` family; supersedes the old `c=16/32` v12 rows and the
    superseded `c=2` addendum).

## Method (see `certificate.json["method"]` for the full description)

1. The checker script is run **unmodified**, as a subprocess, from the repo
   root; its stdout is the source of truth for each check's `name`, `c`,
   `m`, `w`, `Delta = m*c-k`, and edge fraction, and for the PASS/FAIL
   verdict itself.
2. Because the stdout does not print bit-length or margin data, the
   generator additionally **reimplements** (does not import) the script's
   exact Kummer/Legendre prime-factorization binomial routine
   (`binom_prime`/`binom_table`, attributed in `certificate.json["method"]`)
   to independently recompute the LHS/RHS of each checked inequality and
   derive:
   - **structural formula** (e.g. `C(N,m)*threshold_den > pbase^w * threshold_num`),
   - **bit lengths** of the LHS/RHS composite products (never the raw
     `C(N,m)` itself — see "Why no raw binomials" below),
   - an **exact integer bit-bracket** `[2^L, 2^U)` (`L,U` integers, found and
     verified by `bit_length`/shift arithmetic, no floats in the verdict) for
     the ratio LHS/RHS at `m` (**orientation margin at m**, must be `>0`) and
     at `m+1` (**orientation margin at m+1**, must be `<=0`) — this is the
     "orientation" signal: the sign flips exactly once, between `m` and
     `m+1`, certifying the identity-prefix construction's own crossing point.

All 12 recomputed brackets were cross-checked against the tex's own quoted
"orientation" values (`+25.7/-5.5`, `+9.2/-22.0`, `+10.3/-20.9`, `+28.1/-3.1`
bits for the four identity rows, `experimental/cap25_v13_experimental.tex`
L1382-1385) and against an independent parallel derivation
(`A1_ledger_numbers.json`, this session) — all three computations agree.

### Why no raw binomials

`C(2^21, ~1.1M)` itself runs to **~2.09 million bits**
(`n*H2(m/n)` with `n=2^21`, `m/n~0.532` gives `H2(0.532)~0.9975`, so
`log2 C(n,m) ~ 2.0919e6` bits) — per task instruction, `certificate.json`
records only `bit_length()`s of the composite LHS/RHS products and the
resulting small (tens-of-bits) orientation-margin brackets, never the full
integers.

## Per-row headline (the four identity-scale, `c=1` checks)

| row | a0 (unsafe) | a0+1 (conjectured safe) | w | K | edge = 1-a0/n | margin@a0 | margin@a0+1 |
|---|---:|---:|---:|---:|---|---|---|
| KB MCA | 1,116,043 | 1,116,044 | 67,466 | k+1 | 981109/2097152 ≈ 0.4678292 | [2^25,2^26) | [2^-6,2^-5) |
| KB list | 1,116,046 | 1,116,047 | 67,470 | k | 490553/1048576 ≈ 0.4678278 | [2^9,2^10) | [2^-23,2^-22) |
| M31 MCA | 1,116,021 | 1,116,022 | 67,444 | k+1 | 981131/2097152 ≈ 0.4678397 | [2^10,2^11) | [2^-21,2^-20) |
| M31 list | 1,116,022 | 1,116,023 | 67,446 | k | 490565/1048576 ≈ 0.4678392 | [2^28,2^29) | [2^-4,2^-3) |

For the two MCA rows, the checked threshold is the **deep-point conversion
threshold** `(q+k)/k` (`thm:A`), a sufficient proxy for unsafety — **not** a
literal comparison against `B* = floor(eps* * q_line)`. For the two list
rows, the checked threshold **is** `eps* * q_line` directly (`B*` is its
floor), so the margin literally is `B*/F(a)`. See `certificate.json`'s
per-check `threshold` block and the companion packet's `packet.json` for the
full `B*` vs. deep-point-threshold reconciliation.

The Mersenne-31 rows use target `epsilon* = 2^-100`, **not** `2^-128`
(`q_m31 = p'^4 < 2^124` makes `2^-128` degenerate — `prop:small-field` forces
`delta* = 0` there).

## Replay

```text
bash replay.sh
```

`replay.sh` runs the existing checker script, unmodified, from the repo
root, and exits `0` iff all 12 checks print `PASS` and the script's own
"All exact frontier checks passed." trailer appears. It performs **no
writes** and does not regenerate `certificate.json` (regeneration is
`gen_identity_cert.py`, kept alongside this session's other Wave-2 artifacts,
not part of this packet, since the task only asked for `certificate.json` +
`README.md` + `replay.sh`).

## Non-claims

- **Not a safety proof.** See "What this certifies" above. `a0+1` safe is
  conjectural; closing it needs a complete `U(a0+1)` upper ledger (tangent +
  quotient + extension + sparse/CA + L1/interleaved-list + M1/aperiodic +
  named residuals), none of which exists yet for any of the four rows.
- **Not a Paper-D theorem row.** `experimental/cap25_v13_experimental.tex` is
  unmerged into `tex/cs25_cap_v12.tex`; per `agents.md` and
  `experimental/agents-log.md`, call this `EXPERIMENTAL`, `CONDITIONAL`, or
  `AUDIT`, never `PROVED`, until promoted and replayed as part of Paper D.
  `tex/cs25_cap_v12.tex` and `tex/towards-prize.tex` contain zero occurrences
  of any of the four `a0` values above.
- **Only 3 of the 4 rows are published on the live site.** Only KoalaBear MCA
  has a `site/data/rate-leaderboards.json` entry (id
  `cap25-v13-identity-kb-mca-edge`); KoalaBear list, Mersenne-31 MCA, and
  Mersenne-31 list have none. This packet does not add site entries.
- **Orientation margins are exactly what their name says** — signed integer
  bit-brackets showing the construction's own pass/fail crossing at `m`,
  `m+1`. They are not a distance to any *proved* safe threshold; the nearest
  proved-or-conditional safe theorem sits 377,020+ agreement points away from
  every row's `a0+1` (see the companion
  `experimental/data/certificates/frontier-adjacent/` packet family's per-row
  `applicability_audit_gap_table` in each `*_v1.packet.json`).
- **No hashes.** Consistent with the rest of the repo's certificate family
  (confirmed: no packet under `experimental/data/certificates/` uses
  `sha256`/checksums for its committed JSON), integrity here is by exact
  byte-for-byte re-derivability of `certificate.json` from the unmodified
  source script plus the reimplemented (attributed) bit-bracket routines.
