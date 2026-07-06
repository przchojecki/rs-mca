# L1: `m*(19) <= 9` — the vacancy band is refuted at `p = 571`

**Type: NEGATIVE correction of two integrated notes, established by a
POSITIVE witness** (same self-correction lineage as the two notes it
supersedes). This note supersedes two claims of already-integrated L1
notes:

- the `m*(19) = 10` framing (equality pending the vacancy half) of
  `experimental/notes/l1/l1_ell19_attainment.md` (its title, and its §5
  closing line: "So this note certifies `m*(19) <= 10` unconditionally,
  and equality `m*(19) = 10` exactly to the extent the vacancy half
  holds"), and
- the **named falsifier** of `experimental/notes/l1/l1_e3_law_refuted.md`
  §4: "a listing-eligible (`n >= 2m - 1`) witness with `E_3 = ell + 2`
  concentrated as in W3 would refute the vacancy band outright — that is
  the natural next target,"

both **SUPERSEDED** by an explicit, independently-reverified full listing
at `m = 9 = (ell-1)/2` (one below the `(ell+1)/2` onset) at `ell = 19,
p = 571`. **Ground rule honored: neither integrated note nor its verifier
is edited by this note** — both continue to exit 0 on every gate
unchanged (re-run below); the new witness lives outside the region either
note's own gates sweep. Everything either integrated note labels WITNESS,
PROVED, or SURVIVES **remains SURVIVES**, in particular the `m = 10` and
`m = 11` attainment witnesses of `l1_ell19_attainment.md` (they become
earlier rungs of an attainment ladder `m = 9, 10, 11`, all listing) and
Theorem 1 / the pairwise cap / the master identity of `l1_e3_law_refuted.md`
and `experimental/notes/l1/l1_sigma_calculus.md`.

Filed at `experimental/notes/l1/l1_ell19_band_refuted.md`. Companion
zero-arg verifier: `experimental/scripts/verify_l1_ell19_band_refuted.py`
(stdlib, deterministic, offline, exit 0 iff all gates pass;
`--tamper-selftest`; self-contained — does NOT import either integrated
verifier, matching the ground rule). Companion engine:
`experimental/scripts/l1_ell19_triple_tally.py` (deterministic, seedless,
exhaustive triple-collision-tally re-derivation of the `p = 571` hit from
the plant alone). Companion data:
`experimental/data/certificates/l1-ell19/l1_ell19_band_witness.json` (a
NEW file; the already-integrated `l1_ell19_witnesses.json` is not
touched).

Notation inherited from the integrated notes. `ell` odd prime, `ell | p-1`,
`n = (p-1)/ell` cosets, `Gamma(X) = sum_{r=1}^{ell-1} gamma_r X^r`
constant-free mixed; per coset `mu_b` = max fiber (level-set) size;
spectrum = the `mu_b` sorted descending (per-coset-MAX convention,
`spectrum_A`); `E_3 := sum_b (mu_b - 2)_+`; `T = sum_{k>=3}(mu_k-2)_+`
computed on the descending spectrum from the THIRD-largest fiber onward
(the sigma-calculus residual parameter); `top-m` = sum of the `m` largest
`mu_b`; listing threshold `top-m >= 2 ell`. All arithmetic exact over
`F_p`, stdlib only.

**Status legend:** WITNESS (explicit object, full 16-gate chain) /
COUNTEREXAMPLE (refutes a named claim, explicit object) / AUDIT (root
cause, independently observed) / PROVED-LOCAL (proof included, finite
scope stated) / EXPERIMENTAL (well-supported, not proved) / SURVIVES
(integrated claim unchanged).

---

## 0. Headline

1. **WITNESS / COUNTEREXAMPLE — full `m = 9 = (ell-1)/2` listing at
   `ell = 19`, `p = 571`** (`n = 30`), refuting the vacancy half of
   `m*(ell) = (ell+1)/2` BY WITNESS at `ell = 19`: one below the
   `(ell+1)/2 = 10` onset, this assembles a full 16-gate crossing at
   `m = (ell-1)/2`.

   ```text
   ell = 19, p = 571, n = (p-1)/ell = 30 cosets
   gamma (X^1..X^18) = [545, 15, 163, 341, 470, 274, 474, 224, 174, 556,
                        179, 28, 321, 233, 543, 54, 203, 1]
   spectrum_A = [16, 3^6, 2^6, 1^17]              (30 entries)
   E_3 = (16-2) + 6*(3-2) = 20 = ell + 1
   T (sigma-calculus, from 3rd-largest onward) = 5*(3-2) = 5
   top-8 = 36 < 38 (m=8 does NOT cross)   top-9 = 38 = 2*ell (CROSSES)
   top-10 = 40
   16-gate chain: L1_topm>=2ell, cosets_distinct, LF_map_zeroconst,
     LF_rank_m_surjective, LF_c_distinct_nonzero, L3_degP<=m*ell, L3_mixed,
     L3_petal_full, L4_R>=2ell, L4_agreements>=s, L4_retained==maxfiber,
     dom_distinct_pts, L5_M_kernel, L5_identity, L5_minimal,
     L6_primitive_mixed — ALL TRUE.  lambda-free: TRUE.
   provenance: triple-tally engine (plant-big-fiber + exhaustive
     triple-collision tally); plant [16] = H minus H-indices {0, 1, 6};
     family member (a, b) = (395, 497), the UNIQUE maximum of the tally
     (26,874 distinct family members tallied, checked directly).
   ```

   So **`m*(19) <= 9`** unconditionally. Reverified four independent ways
   pre-ship: plant-reconstruction from the dropset, a from-scratch
   spectrum recount with the explicit fibers exhibited, the 16-gate chain
   (determinism), and eligibility (`n = 30 >= 2m-1 = 17`). `top-8 = 36`
   with this same `gamma`, so `m = 8` does **not** cross: `m*(19) in
   {8, 9}`, the lower end left open (§4).

2. **SUPERSESSION — `experimental/notes/l1/l1_ell19_attainment.md`'s
   `m*(19) = 10` framing.** That note's title and §5 close by certifying
   `m*(19) <= 10` "unconditionally, and equality `m*(19) = 10` exactly to
   the extent the vacancy half holds." Item 1's witness is strictly
   tighter (`<= 9 < 10`) and additionally REFUTES the vacancy half
   outright at `ell = 19` (so the conditional reading "equality iff the
   vacancy half holds" no longer applies — the vacancy half does not hold
   here). That note's own `m = 10` (`p = 647`, `E_3 = 18`) and `m = 11`
   (`p = 647`, `E_3 = 17`) witnesses **SURVIVE UNCHANGED**: they are
   correct, fully-gated listings in their own right, now read as the next
   two rungs of an attainment ladder `m = 9, 10, 11` (all list, discovered
   in the order 11, 10, and — this note — 9). Nothing in the integrated
   note is edited; its verifier `verify_l1_ell19_attainment.py` still
   exits 0 unchanged (re-run below).

3. **SUPERSESSION (ATTAINED, REFINED) —
   `experimental/notes/l1/l1_e3_law_refuted.md`'s §4 named falsifier.**
   That note's non-claims section names the natural next target: "a
   listing-eligible (`n >= 2m - 1`) witness with `E_3 = ell + 2`
   concentrated as in W3 would refute the vacancy band outright." Item 1's
   witness IS such a listing-eligible, fully-assembling witness — the
   vacancy band is refuted at `ell = 19` — but **refines** the falsifier's
   own stated sufficient condition: `top-m >= 2 ell` is the true
   requirement, and `E_3 = ell + 1` (not `ell + 2`) suffices, PROVIDED two
   extra size-2 fibers supply the remaining `top-m` mass (here: one size-16
   fiber plus six size-3 fibers already reach `top-7 = 34 = 2ell-4`; two
   more size-2 fibers carry `top-9` up to `38 = 2 ell` without adding to
   `E_3`, since `mu - 2 = 0` at size 2). So `E_3 = ell + 2` is **not**
   necessary for a crossing; `E_3 = ell + 1` (which that note also
   observed, at its own `T = 5` witnesses W1/W2) already suffices when the
   spectrum shape cooperates. Neither the integrated note nor its verifier
   is edited; `verify_l1_e3_law_refuted.py` still exits 0 unchanged
   (re-run below) — its gate vii already independently confirms the
   companion attainment witnesses sit on the disjoint `T <= 4` chart, and
   this note's own witness is a THIRD, `T = 5` chart object that gate does
   not touch.

4. **EXPERIMENTAL — the key reduction formula behind item 1** (full
   derivation, method, and honest coverage in §2): with a planted size-
   `(ell-3)` fiber at `m = (ell-1)/2`, `top-m <= 2*ell - 6 + a` (the
   pairwise cap forces every non-planted fiber `<= 3`), where `a` =
   the number of OTHER cosets simultaneously carrying an (emergent) size-
   `>= 3` fiber at the same family member, with EQUALITY iff at least
   `(m - 1 - a)` further cosets carry a size-2 fiber. So `a >= 6` is
   NECESSARY for the crossing unconditionally, and sufficient together
   with the size-2 proviso (at `p = 571`: `m - 1 - a = 2` needed, six
   present). Observed max `a`: `ell = 17 -> 5` (24 eligible primes +
   exhaustive `p = 307` check), `ell = 19 -> 6` at `p = 571` (the unique
   crossing found), `ell = 23 -> 5` (6 eligible primes). No law is
   conjectured; this is a coverage-scoped, EXPERIMENTAL empirical formula
   for one specific plant shape.

5. **AUDIT — search-depth artifact, consistent with both integrated
   notes' own findings.** The triple-collision-tally method (§2) is
   EXHAUSTIVE over all triples in all non-planted cosets at a fixed
   dropset — it does not miss any size-`>= 3` fiber achievable by that
   plant, unlike a random/greedy single-fiber search. Both integrated
   notes independently record the same lesson at their own scale
   (`l1_ell19_attainment.md`'s own `E_3 = 18` hit was a ~1/3000-per-trial
   rare event that shallower budgets missed; `l1_e3_law_refuted.md`'s
   audit item attributes its violations to exhaustively sweeping a
   nullspace family instead of reading one vector or random-sampling).
   This note's witness is a further instance of the same general pattern,
   at the `m = 9` / vacancy-band question specifically.

---

## 1. The witness in full

Full data already given in §0 item 1 (`ell = 19, p = 571, n = 30`,
`gamma`, spectrum, gate list, provenance); not repeated here.
Eligibility: `n = 30 >= 2m - 1 = 17` for `m = 9`. Pairwise cap check:
`mu_1 + mu_2 = 16 + 3 = 19 = ell` (tight, consistent with the PROVED
pairwise cap `mu_1 + mu_2 <= ell` of the sigma-calculus note, untouched
here).

**Relationship to Theorem 1 / RC (sigma-calculus note, untouched).** This
witness's `T = 5` (five size-3 fibers beyond the top two, `mu_1 = 16,
mu_2 = 3`), so it sits on the RESIDUAL chart, not the `T <= 4` chart where
Theorem 1 proves `E_3 <= ell`. This does **not** make the witness
conditional: its validity is the direct output of the 16-gate
`run_witness_chain` on an exhibited `gamma`, independent of any
`E_3`-bounding theorem or conjecture. What `T = 5` explains is *why* this
witness's high `E_3 = ell + 1 = 20` was possible at all — it is a sibling
of `l1_e3_law_refuted.md`'s own `T = 5` counterexamples W1, W2 (also
`E_3 = ell + 1` there), now additionally listing-eligible and crossing.

## 2. The key reduction formula, method, and honest coverage

**The formula.** Plant a single big fiber of size `ell - 3` on one coset;
the residual nullspace has dimension 3 (a projective plane `P^2` of
candidate `gamma`). At `m = (ell-1)/2`, for a family member carried by `a`
OTHER cosets each simultaneously hosting a (separately emergent) size-
`>= 3` fiber:

```text
top-m <= 2*ell - 6 + a         (at m = (ell-1)/2, this plant shape;
                                the a emergent fibers are each exactly 3
                                by the pairwise cap)
equality iff >= (m-1-a) further size-2 fibers exist
==> crossing REQUIRES a >= 6;  a >= 6 + the size-2 proviso SUFFICES
listing gate top-m >= 2*ell  <=>  a >= 6
```

Sanity check against item 1: `ell = 19`, `a = 6` gives
`top-9 = 2*19 - 6 + 6 = 38 = 2*19`. Exact.

**Method (TRIPLE-COLLISION TALLY).** A naive sweep of all `p^2` family
members is not needed: a size-`>= 3` fiber at a non-planted coset, at
member `(a, b)`, means three points there share a `Gamma`-value, i.e. two
simultaneous linear conditions on `(a, b)` — a 2x2 solve. Enumerating every
triple in every non-planted coset and tallying which `(a, b)` is hit by
the most DISTINCT cosets finds the maximally-concentrated member exactly,
without evaluating `Gamma` at a member chosen by chance. The top tally
candidates are confirmed by an exact from-scratch spectrum recompute
(this also catches size-2 fibers, which the tally does not track).
Companion engine: `experimental/scripts/l1_ell19_triple_tally.py`
(deterministic, no seed anywhere; re-derives the `p = 571` hit and
reconstructs the exact `gamma` from the plant alone; asserts `a >= 6`).

**Observed max `a` per `ell` (EXPERIMENTAL; coverage stated honestly):**

| ell | max a observed | crosses (a >= 6)? | coverage |
|---|---|---|---|
| 17 | 5 | no (caps at `top-8 = 2*17-1 = 33`) | 24 eligible primes (307..2857) + an exhaustive all-`C(17,3)=680`-dropset check at `p = 307` confirming the same max either way |
| **19** | **6** | **YES, at `p = 571`** | 8 eligible primes (419..1483) |
| 23 | 5 | no (caps at `top-11 = 2*23-1 = 45`) | 6 eligible primes (599..1151) |

**Honest coverage caveats (all EXPERIMENTAL):**

1. The `[1, a, b]` affine chart used by the tally misses the `p + 1`
   family members with zero leading coefficient — recorded, not swept;
   measure `~1/p`, and the confirm step (exact spectrum recompute) is
   exact on the chart regardless.
2. Coverage is thin in absolute terms: 8 primes at `ell = 19`, 24 (+1
   exhaustive) at `ell = 17`, 6 at `ell = 23` — nowhere near exhaustive
   over all admissible primes, so an `a >= 6` crossing at `ell in
   {17, 23}` is entirely unexcluded at an untested prime.
3. Only the single-big-fiber-of-size-`(ell-3)` plant shape was swept this
   way; other plant shapes (e.g. two-fiber splits) are unexplored by this
   method.
4. The `x -> zeta*x` orbit reduction (sweeping `~ell` dropset
   representatives instead of `C(ell,3)`) was confirmed loss-free by the
   exhaustive `p = 307` check at `ell = 17` (same max, 33, either way) but
   not reconfirmed at every prime.
5. `E_3 = ell + 1` at the crossing witness is consistent with, but not
   explained by, `l1_e3_law_refuted.md`'s observed (not proved)
   `E_3 <= ell + 2` — no ceiling is claimed here, and no relationship
   between `a` and `E_3` beyond the formula above is asserted.

## 3. What SURVIVES (both integrated notes, unedited)

- `l1_ell19_attainment.md`: its `m = 10` (`p = 647`) and `m = 11`
  (`p = 647`) witnesses, its two structural floors (concentrated `K = 1`
  and two-fiber `K = 2`), and its own AUDIT/coverage findings all SURVIVE
  unchanged — this note supersedes only its headline equality framing
  (§0 item 2). Its verifier `verify_l1_ell19_attainment.py` is unedited
  and still exits 0 (re-run below, unchanged).
- `l1_e3_law_refuted.md`: its six `E_3 in {ell+1, ell+2}` counterexamples
  (`ell in {17, 23, 29}`), Theorem 1 (`T <= 4 => E_3 <= ell`), the
  pairwise cap, the master identity, and its two PROVED-LOCAL reductions
  all SURVIVE unchanged — this note supersedes only its §4 falsifier's
  stated sufficient condition (`E_3 = ell + 2`; refined to
  `E_3 = ell + 1` with the caveat above). Its verifier
  `verify_l1_e3_law_refuted.py` is unedited and still exits 0 (re-run
  below, unchanged).
- `experimental/notes/l1/l1_sigma_calculus.md`: Theorem 1 and RC's FALSE
  status (per the companion note) are both untouched by this note.
- **Relationship to other concurrently-integrated L1 material (same
  integration commit, `0fa9427`):** a separate contribution
  (`l1_e3_status_and_paper_connection.md` and its `l1_e3_*` sibling notes,
  PR #360) frames the OLDER `E_3 <= ell-2` ceiling as OPEN with a "PROVED
  upper half + `dim Syz <= K` reduction," in apparent tension with
  `l1_prime_ell_key_lemma_refuted.md`'s own COUNTEREXAMPLE-status claim
  that `E_3 <= ell-2` is FALSE (explicit witnesses at `ell in
  {11,13,17,19,23}`). This note does not touch, rely on, or attempt to
  reconcile that separate tension — it concerns a stricter ceiling
  (`ell - 2`, not `ell`) than either note in this note's own supersession
  chain, and this note's own claims (`E_3 = ell + 1` at `ell = 19`) are
  unaffected either way. Flagged here for the record, not resolved.

## 4. Non-claims

Does **not** determine `m*(19)` exactly: it is `8` or `9`. Item 1 refutes
vacancy at `m = 9` via one `gamma`, but does not rule out a full crossing
at `m = 8` via some OTHER `gamma` — `top-8 = 36 < 38` is a fact about that
specific witness only, not a proof that `m = 8` is vacant for `ell = 19`.
Does **not** refute the vacancy band at `ell = 17` or `ell = 23`: the
deepest triple-tally coverage to date caps at `top-m = 2 ell - 1` (one
below crossing) at both (§2) — those two remain OPEN, neither refuted nor
reaffirmed. Does not conjecture any new law: the `a >= 6` reduction
formula of §2 is an EXPERIMENTAL, coverage-scoped empirical finding for
one plant shape, not a general claim about `top-m` or `E_3` at other `ell`
or other constructions. Does not claim any `E_3` ceiling beyond what
`l1_e3_law_refuted.md` already reports as OBSERVED (`E_3 <= ell + 2` so
far, explicitly not proved extremal there). Does not claim coverage
completeness anywhere in §2 (explicitly partial; see its own limits
list). Does not edit, and is not gated by, either integrated note or
verifier. Promotes nothing — WITNESS / COUNTEREXAMPLE / AUDIT /
PROVED-LOCAL / EXPERIMENTAL scope only, `experimental/` placement.

## 5. Verifier contract

`experimental/scripts/verify_l1_ell19_band_refuted.py`, zero-arg, stdlib
only, offline, deterministic, exit 0 iff all gates pass. Self-contained:
does NOT import `verify_l1_ell19_attainment.py`, `verify_l1_e3_law_refuted.py`,
or any other sibling verifier at runtime — every piece of arithmetic is a
fresh, from-scratch reimplementation.

- **Gate i:** recompute the full spectrum of the witness from the raw
  `gamma` via two independent implementations (coset-key `x^ell mod p` +
  Horner; generator-power-coset walk + ascending power-sum), require they
  AGREE, and check `E_3 = 20`, `T = 5`, `top-8 = 36`, `top-9 = 38`,
  `top-10 = 40` exactly.
- **Gate ii:** run a fresh port of the integrated 16-gate
  `run_witness_chain` logic on the witness at `m = 9`: all 16 gates True,
  lambda-free True, `top_m = 38`.
- **Gate iii:** the reduction-formula check: recompute `a` (the number of
  non-planted cosets carrying a size-`>= 3` fiber at the witness's family
  member, via the same triple-tally construction) directly from the
  witness's `gamma` and confirm `a = 6` and `top-9 == 2*19 - 6 + a`.
- **Gate iv:** structural/eligibility checks: `n = 30 >= 2*9-1 = 17`;
  `Gamma` constant-free and mixed; pairwise cap `mu_1 + mu_2 = 19 <= ell`
  (tight); `T = 5` via the sigma-calculus formula (third-largest fiber
  onward).
- `--tamper-selftest`: flip one datum per gate (a `gamma` coefficient, a
  spectrum entry, a claimed count) and confirm each gate then fails.

Ground-rule compliance (neither integrated note nor verifier edited, both
still exit 0) is confirmed by manually re-running
`verify_l1_ell19_attainment.py` and `verify_l1_e3_law_refuted.py`
unmodified at packaging time (results in the shipping commit message /
PR); it is not wired into this verifier as a gate, to keep this verifier
strictly self-contained (no invocation of any sibling file, not even as a
subprocess) as the "do NOT import the integrated verifiers" contract
requires.

## Refs

- `experimental/notes/l1/l1_ell19_attainment.md` (integrated; supersedes
  its `m*(19) = 10` framing — its `m = 10`/`m = 11` witnesses SURVIVE).
- `experimental/notes/l1/l1_e3_law_refuted.md` (integrated; supersedes
  its §4 named falsifier — attained and refined; its counterexamples and
  Theorem 1 SURVIVE).
- `experimental/notes/l1/l1_prime_ell_key_lemma_refuted.md` (grand-
  ancestor; the `E_3 <= ell-2` and vacancy-half refutations both notes
  above build on; untouched).
- `experimental/notes/l1/l1_sigma_calculus.md` (Theorem 1, RC, master
  identity; untouched).
- `experimental/scripts/l1_ell19_bigfiber_v2.py`,
  `experimental/scripts/l1_pencil_family_sweep.py` (the two integrated
  notes' own companion engines; unrelated method, not reused here).
