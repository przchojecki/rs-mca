# L1: `m*(19) = 10` attained — `ell = 19` joins the `(ell+1)/2` law

**Type: POSITIVE completion of an integrated note's named open row.**
The integrated note `experimental/notes/l1/l1_prime_ell_key_lemma_refuted.md`
left exactly one attainment question open: its §1 table marks the `ell = 19`
row "`m=10` listing OPEN", and its `ell = 19` listing-question paragraph
records that a dedicated hunt "found no `m = 10` listing and no `E_3 >= 18`
at any `n >= 19` prime — the question REMAINS OPEN". This note resolves that
row **positively**: an explicit full witness at `p = 647` lists at
`m = 10 = (ell+1)/2`, so `ell = 19` is **regular** — the attainment half of
`m*(ell) = (ell+1)/2` now holds unconditionally at `ell in {11, 13, 17, 19, 23}`,
with no exceptional prime.

**Ground rule honored:** this note does not edit the integrated note or its
verifier; every statement it supersedes was coverage-scoped ("at any tested
prime") and is superseded by deeper sampling, not contradicted. Filed at
`experimental/notes/l1/l1_ell19_attainment.md`. Companion zero-arg verifier:
`experimental/scripts/verify_l1_ell19_attainment.py` (stdlib, deterministic,
offline, exit 0 iff all gates pass; `--tamper-selftest` flips one datum per
gate and confirms each then fails). Companion engine:
`experimental/scripts/l1_ell19_bigfiber_v2.py` (the deepened
plant-big-fibers-then-exact-solve constructor that found the witness; by
default it re-derives the `E_3 = 18` hit at `ell = 19, p = 647` from
scratch under the shipped seed — a full seeded re-run of the 2240-trial
pass, minutes-scale, deterministic — not a replay of stored coefficients;
`--fresh-seed N` hunts with a new seed, expected ~1/3000 hit rate per
trial).

Notation inherited from the integrated notes. `ell` odd prime, `ell | p-1`,
`n = (p-1)/ell` cosets, `Gamma(X) = sum_{r=1}^{ell-1} gamma_r X^r`
constant-free mixed; per coset `mu_b` = max fiber (level-set) size; spectrum
= the `mu_b` sorted descending (per-coset-MAX convention, `spectrum_A`);
`E_3 := sum_b (mu_b - 2)_+`; `top-m` = sum of the `m` largest `mu_b`;
listing threshold `top-m >= 2 ell`. All arithmetic exact over `F_p`, stdlib
only.

**Status legend:** WITNESS (explicit object, full 16-gate chain) /
PROVED-LOCAL (proof included, finite scope stated) / AUDIT (root cause,
independently observed) / EXPERIMENTAL (well-supported, not proved) /
SURVIVES (integrated claim unchanged).

---

## 0. Headline

1. **WITNESS — full `m = 10 = (ell+1)/2` listing at `ell = 19`, `p = 647`**
   (`n = 34`). `gamma = [298, 638, 143, 294, 14, 111, 237, 78, 464, 166,
   355, 385, 207, 68, 465, 369, 316, 1]` (coefficients of `X^1..X^18`).
   Spectrum `[12, 7, 4, 3, 2 x10, 1 x20]`; `E_3 = 18`;
   `top-10 = 38 = 2 ell` **exactly** (the proved bound `top-m <= 2m + E_3`
   is saturated: `2*10 + 18 = 38`). All 16 gates of the integrated
   `run_witness_chain` pass, including `lambda`-freeness, `L5_minimal`, and
   `L6_primitive_mixed`. Verified three independent ways pre-ship: the
   hunt's own chain, a from-scratch replay from the raw `gamma` only, and a
   third independent spectrum/count implementation. Hence
   **`m*(19) <= 10 = (ell+1)/2` unconditionally**, with equality exactly to
   the extent the vacancy half holds (see §5 — the vacancy half's status
   changed concurrently; the attainment fact shipped here is unaffected).

2. **WITNESS (companion) — `m = 11` listing at the same prime.**
   `gamma = [318, 474, 374, 319, 297, 217, 24, 346, 0, 609, 514, 362, 499,
   309, 174, 383, 93, 1]`, spectrum `[12, 7, 3, 3, 2 x6, 1 x24]`, `E_3 = 17`,
   `top-11 = 38 = 2 ell`, 16/16 gates. Found first (it settled
   `m*(19) <= 11`); the `m = 10` witness of item 1 supersedes it as the
   onset. Shipped because two full-chain listings at the same prime, at
   consecutive `m` and with distinct `E_3`, make `p = 647` the cleanest
   single-prime laboratory row in the family.

3. **AUDIT — the prior `ell = 19` nulls were a search-depth artifact, the
   second recorded instance of the constructor-undershoot failure mode.**
   At `p = 647` the deepened constructor's `E_3` histogram over 3005
   exact-solved plants is `{12: 74, 13: 398, 14: 1057, 15: 1373, 16: 99,
   17: 3, 18: 1}` — an `E_3 = 18` rate of ~1/3000 per trial. The integrated
   note's dedicated hunt and this weekend's first passes budgeted an order
   of magnitude fewer trials per prime, reliably reaching the ~1/30 tail
   (`E_3 = 16..17`) and never the ~1/3000 tail. The first recorded instance
   of this failure mode is the integrated note's own headline (the
   `E_3 <= ell-2` law survived a >700k-config census before the deeper
   constructor refuted it). Process rule reinforced: a bounded-search null
   at rate-`r` sampling says nothing about events rarer than ~`1/r`.

4. **PROVED-LOCAL — two structural floors of the plant family** (proofs in
   §4; these explain *why* shallow passes plateau at `E_3 = 16`):
   (a) the concentrated single-fiber design (`K = 1`, one fiber of size
   `ell - 1`) is, up to the `X -> cX` rescale, the unique `gamma_r == 1`
   family and has `E_3 = 16` at `ell = 19` for **every** prime (spectrum
   `[ell-1, 1, ...]`); verified with zero variance across all 36 admissible
   primes `p < 6000`. (b) any rank-cap-saturating two-fiber plant
   (`K = 2`, planted sizes `s_1 + s_2 = ell`) contributes
   `E_3 = (s_1 - 2) + (s_2 - 2) = ell - 4 = 15` identically, independent of
   the split — so every point of the coverage table above 15 is *emergent*
   (incidental extra fibers of size >= 3 in unplanted cosets), which is
   exactly the rare-tail event of item 3.

---

## 1. The `m = 10` witness in full

```text
ell = 19, p = 647, n = (p-1)/ell = 34 cosets
gamma (X^1..X^18) = [298, 638, 143, 294, 14, 111, 237, 78, 464, 166,
                     355, 385, 207, 68, 465, 369, 316, 1]
spectrum_A = [12, 7, 4, 3, 2,2,2,2,2,2,2,2,2,2, 1 x20]   (34 entries)
E_3 = (12-2) + (7-2) + (4-2) + (3-2) = 18
top-10 = 12+7+4+3+2*6 = 38 = 2*ell   top-9 = 36 < 38   top-11 = 40
16-gate chain: L1_topm>=2ell, cosets_distinct, LF_map_zeroconst,
  LF_rank_m_surjective, LF_c_distinct_nonzero, L3_degP<=m*ell, L3_mixed,
  L3_petal_full, L4_R>=2ell, L4_agreements>=s, L4_retained==maxfiber,
  dom_distinct_pts, L5_M_kernel, L5_identity, L5_minimal,
  L6_primitive_mixed — ALL TRUE.  lambda-free: TRUE.
provenance: bigfiber-v2 engine, seed_base 314159265, trial 2240 of 2240,
  planted [12, 7] on two distinct cosets, emergent [4] and [3] fibers.
```

Note `top-9 = 36 < 38`: this witness lists at `m = 10` and **not** at
`m = 9`, consistent with the (conditional) vacancy band `m <= (ell-1)/2 = 9`
— the witness saturates the boundary exactly rather than crossing it.

## 2. The `m = 11` companion witness

```text
ell = 19, p = 647
gamma (X^1..X^18) = [318, 474, 374, 319, 297, 217, 24, 346, 0, 609,
                     514, 362, 499, 309, 174, 383, 93, 1]
spectrum_A = [12, 7, 3, 3, 2,2,2,2,2,2, 1 x24]   E_3 = 17
top-10 = 37 < 38   top-11 = 38 = 2*ell   16/16 gates TRUE, lambda-free
provenance: weekend m=10 hunt best-E_3 trial, first checked at m = 11.
```

## 3. Coverage table and honest limits

Merged coverage (weekend passes + this session's deepened engine), grand
max `E_3` per prime at `ell = 19`; "eligible" means `n >= 2m - 1 = 19` so a
full `m = 10` chain is checkable:

| p | n | eligible | max E_3 | source |
|---|---|---|---|---|
| 191 | 10 | no | 18 | integrated note's anchor (not listing-eligible) |
| 229 | 12 | no | 17 | weekend bigfiber |
| 419 | 22 | yes | 16 | concentrated floor (closed form) |
| 457 | 24 | yes | 17 | weekend bigfiber |
| 571 | 30 | yes | 17 | this session, deeper pass (weekend: 16) |
| **647** | **34** | **yes** | **18** | **this session — full m=10 listing** |
| 761 | 40 | yes | 17 | this session, deeper pass (weekend: 16) |
| 1103 | 58 | yes | 17 | weekend, reconfirmed |
| 1217 | 64 | yes | 16 | weekend / concentrated floor |
| 1483, 1559 | 78, 82 | yes | 16 | weekend twofiber + this session |
| 1597..5701 (25 primes) | 84..300 | yes | 16 | this session, first coverage (see limits) |

Limits, stated for the record (all EXPERIMENTAL): of the 25 fresh primes,
8 (1597..2357) received a shallow bigfiber search pass (131-410 trials
each) and the remaining 17 (2699..5701) carry **only** the closed-form
concentrated floor of §4(a) — no random search at all — so an `E_3 = 18`
hit in that range is entirely unexcluded, merely unneeded now;
the near-miss primes at 17 (571, 761, 1103) plausibly reach 18 with ~2-4x
this session's per-prime budget, given the observed tail rates; only the
two-big-fiber rank-cap family plus the two `K = 1`-adjacent controls were
searched (K >= 3 designs are dominated at the plant level: planted
`E_3 = 17 - K` decreases in `K`, and the weekend `deeper_19_*` K >= 3 data
capped at 15-16).

## 4. The two structural floors (proofs)

**(a) Concentrated `K = 1` floor.** A single fiber of size `ell - 1`
saturating the rank cap forces (after the `X -> cX` rescale that moves the
fiber's coset to `mu_ell` and fixes the fiber value) the unique solution
`gamma_r = 1` for all `r`, i.e. `Gamma(x) = x + x^2 + ... + x^{ell-1}
= (x^ell - x)/(x - 1)` for `x != 1`. On any coset `b mu_ell` with
`b^ell = W != 1` fixed, `Gamma(x) = (W - x)/(x - 1)` is a Mobius map of
`x`, injective on the coset; on the identity coset the `ell - 1` points
`x != 1` collapse to the single value `-1` (the designed size-`(ell-1)`
fiber), while `x = 1` maps to `ell - 1`.
Hence spectrum `[ell - 1, 1, 1, ...]` and `E_3 = ell - 3 = 16` at
`ell = 19`, for every admissible prime: a hard floor with **zero** search
freedom (nulldim 1). Confirmed computationally at all 36 admissible
`p < 6000` with zero variance.

**(b) Two-fiber plant identity.** A `K = 2` plant with fiber sizes
`s_1, s_2` imposes `(s_1 - 1) + (s_2 - 1)` linear coincidence conditions;
saturating the rank cap `ell - 2` gives `s_1 + s_2 = ell`, whence the
planted contribution to `E_3` is `(s_1 - 2) + (s_2 - 2) = ell - 4 = 15`,
independent of the split. So the split choice cannot matter at the plant
level; all variation above 15 is emergent. (Both floors are consistent
with, and explain, the coverage table's plateau at 16 = floor (a), and the
near-misses at 17 = one emergent triple over floor (b).)

## 5. What SURVIVES / what is superseded

- **Relationship to the `E_3 <= ell` law: this note does not depend on
  it.** Both shipped witnesses live on the **covered chart of the
  sigma-calculus Theorem 1** (`T = sum_{k >= 3}(mu_k - 2)_+`, computed on
  the descending spectrum from the third-largest fiber onward): the §1
  witness has `T = (4-2) + (3-2) = 3` and the §2 witness `T = 2`, both
  `<= 4`, where `E_3 <= ell` is *proved*. Their `E_3` values (18, 17) are
  therefore theorem-backed, and RC (`T >= 5`) is not invoked anywhere in
  this note. **Concurrent same-session work (companion note, shipped
  separately: `experimental/notes/l1/l1_e3_law_refuted.md`) REFUTES the
  `E_3 <= ell` law on the residual chart `T >= 5`** (explicit witnesses up
  to `E_3 = ell + 2`); that refutation does not touch Theorem 1, the
  covered chart, or anything shipped here. The `m = 10` witness saturates
  the pairwise cap exactly (`mu_1 + mu_2 = 12 + 7 = 19 = ell`). The
  sigma-calculus note (`experimental/notes/l1/l1_sigma_calculus.md`) and
  its Theorem 1 are untouched.
- **Integrated `ell = 19` table row "`m = 10` listing OPEN": RESOLVED
  (attained).** The integrated hunt statement "no `E_3 >= 18` at any
  `n >= 19` prime" was explicitly coverage-scoped and is superseded by
  deeper sampling at a prime already at the prior eligible-prime maximum
  (`p = 647` shared the record `E_3 = 17` with `p in {457, 571, 761,
  1103}`).
- **Frontier attainment half `m*(ell) = (ell+1)/2`: now unconditional at
  five consecutive admissible `ell` — {11, 13, 17, 19, 23}** (the first
  four from the integrated note; `ell = 19` here). The vacancy half
  (`m <= (ell-1)/2` lists nothing) is now **fully OPEN**: its previous
  conditional support (`E_3 <= ell`) is refuted at `T >= 5` by the
  concurrent companion note, and no unconditional replacement is claimed
  here. On the covered chart `T <= 4` the vacancy bound stands
  theorem-backed as before. `ell = 7` unaffected (Theorem R). So this note
  certifies `m*(19) <= 10` unconditionally, and equality `m*(19) = 10`
  exactly to the extent the vacancy half holds — the same status every
  other attained `ell` now has.
- **Relationship to concurrent work (2026-07-06 sweep #345-#354):** none of
  the ten packets integrated today touches `ell = 19`, the `E_3`
  law/saturators, or this lane's objects (verified against each packet's
  integrated files during today's PR sync); no dependency in either
  direction. This note is self-contained over the integrated L1 notes.

## 6. Non-claims

This note does not prove vacancy at `m = 9` (the `m*(19) = 10` equality is
conditional on the vacancy half exactly as at every other `ell`); does not
claim the `ell = 19` ceiling is `E_3 = 18` (only that 18 is attained and
`<= ell` is unviolated in all coverage); does not claim coverage
completeness at the shallow primes of §3; and promotes nothing — WITNESS /
AUDIT / PROVED-LOCAL scope only, `experimental/` placement.

## 7. Verifier contract

`experimental/scripts/verify_l1_ell19_attainment.py`, zero-arg, stdlib
only, offline, deterministic, exit 0 iff all gates pass:

- **Gate i:** recompute the full spectrum of witness §1 from the raw
  `gamma` (fresh implementation, not the engine's), and check spectrum,
  `E_3 = 18`, `top-9 = 36`, `top-10 = 38`, `top-11 = 40` exactly.
- **Gate ii:** same for witness §2 (`E_3 = 17`, `top-10 = 37`,
  `top-11 = 38`).
- **Gate iii:** run the integrated 16-gate `run_witness_chain` logic on
  both witnesses (`m = 10` for §1, `m = 11` for §2), all gates True,
  lambda-free True.
- **Gate iv:** re-derive floor (a): construct `gamma_r == 1` at
  `p in {191, 419, 647, 1103}`, check spectrum `[18, 1 x(n-1)]` and
  `E_3 = 16` each.
- **Gate v:** check identity (b) symbolically for all splits
  `s_1 + s_2 = 19`, `s_i >= 2`: `(s_1 - 2) + (s_2 - 2) = 15`.
- **Gate vi:** coverage-consistency: every row of the §3 table with a
  stored witness in the companion JSON recomputes to its claimed `E_3`.
- `--tamper-selftest`: flip one datum per gate (a `gamma` coefficient, a
  spectrum entry, a claimed count) and confirm each gate then fails.

Runtime ~225 s zero-arg (gate iii dominates: it runs the full 16-gate
chain live for both witnesses, including the expensive `L5_minimal`);
`--tamper-selftest` ~240 s. Companion data:
`experimental/data/certificates/l1-ell19/l1_ell19_witnesses.json` (both
`gamma` vectors, spectra, gate vectors, provenance seeds, coverage rows).

## Refs

- `experimental/notes/l1/l1_prime_ell_key_lemma_refuted.md` (the open row
  this note closes; witness-chain and spectrum conventions).
- `experimental/notes/l1/l1_prime_ell_frontier_corrected.md` (frontier
  framing; `top-m <= 2m + E_3` bridge).
- `experimental/notes/l1/l1_sigma_calculus.md` (law statement `E_3 <= ell`,
  Theorem 1, RC; untouched here).
- `experimental/scripts/verify_l1_key_lemma_refuted.py` (16-gate chain
  conventions this verifier re-implements).
