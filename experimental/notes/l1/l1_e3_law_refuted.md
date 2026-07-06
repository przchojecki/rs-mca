# L1: `E_3 <= ell` refuted at `T >= 5` — the sigma-calculus falsifier is attained

**Type: first-class NEGATIVE result (self-correction of our own integrated
notes, same pattern as `l1_prime_ell_key_lemma_refuted.md`).** This note
supersedes two claims of the integrated L1 notes:

- the **NEW KEY LEMMA CANDIDATE** `E_3 <= ell` of
  `experimental/notes/l1/l1_prime_ell_key_lemma_refuted.md` (its §3,
  EXPERIMENTAL there, with falsifier "any `E_3 >= ell+1`"), and
- **RC** (the Residual Conjecture, `T >= 5 ==> E_3 <= ell`) of
  `experimental/notes/l1/l1_sigma_calculus.md` — its named "open core",

which are **REFUTED** by six explicit, realizable, independently
re-verified `Gamma` at `ell in {17, 23, 29}`, with observed maximum
**`E_3 = ell + 2`**. The refutation attains the sigma-calculus note's own
named falsifier signature (`sigma >= K + dimU + 1`); its Theorem 1
(covered chart `T <= 4`), the pairwise cap, the master identity, and every
claim it labels PROVED **SURVIVE** — each holds *on* the counterexamples.
**Ground rule honored:** no integrated note or verifier is edited; the
integrated verifiers still exit 0 (the violations live on the residual
chart their gates do not sweep).

Filed at `experimental/notes/l1/l1_e3_law_refuted.md`. Companion zero-arg
verifier: `experimental/scripts/verify_l1_e3_law_refuted.py` (stdlib,
offline, deterministic, exit 0 iff all gates pass; `--tamper-selftest`).
Companion constructor:
`experimental/scripts/l1_pencil_family_sweep.py` (exhaustively re-derives
the `ell = 17, p = 137` violation from scratch — deterministic, no seed:
it enumerates a complete pencil family).

Notation inherited from the integrated notes. `ell` odd prime,
`ell | p - 1`, `n = (p-1)/ell` cosets; `Gamma(X) = sum_{r=1}^{ell-1}
gamma_r X^r` constant-free mixed; per coset `mu_b` = max fiber size;
spectrum = the `mu_b` sorted descending (per-coset-MAX, `spectrum_A`);
`E_3 = sum_b (mu_b - 2)_+`; `K` = number of fibers of size `>= 2` in the
selected configuration; **`T = sum_{k >= 3} (mu_k - 2)_+` computed on the
descending spectrum from the THIRD-largest fiber onward** (the
sigma-calculus residual parameter — note this is *not* `#{mu >= 3}`, a
misreading worth guarding against); `sigma`, `dimU`, `rho` as in the
sigma-calculus note. All arithmetic exact over `F_p`, stdlib only.

**Status legend:** COUNTEREXAMPLE / PROVED-LOCAL (proof included) / AUDIT /
EXPERIMENTAL / SURVIVES.

---

## 0. Headline

1. **COUNTEREXAMPLE — RC is false, and with it the law `E_3 <= ell` on the
   residual chart.** Three flagship witnesses (three more in the
   certificate JSON), each verified by four independent implementations
   pre-ship (constructor, brute-force recount, the integrated verifier's
   own two spectrum implementations, and a from-scratch PI recount):

   | id | ell | p | n | spectrum | E_3 | T | K | mu1+mu2 | sigma |
   |----|-----|---|---|----------|-----|---|---|---------|-------|
   | W3 | 17 | 137 | 8 | `[14,3,3,3,3,3,3,3]` | **19 = ell+2** | 6 | 8 | 17 = ell | 12 = K+dimU+2 |
   | W1 | 29 | 233 | 8 | `[15,14,4,3,3,3,2,2]` | **30 = ell+1** | 5 | 8 | 29 = ell | 11 = K+dimU+1 |
   | W2 | 23 | 139 | 6 | `[14,9,4,4,3,2]` | **24 = ell+1** | 5 | 6 | 23 = ell | 9 = K+dimU+1 |

   Full `gamma` vectors in §1. Every witness satisfies the PROVED pairwise
   cap `mu_1 + mu_2 <= ell` (tight, `= ell`, on five of six); every witness
   has `T >= 5`, so the PROVED Theorem 1 (`T <= 4`) is inapplicable — the
   refutation lives entirely on the conjectural chart. The master identity
   `sigma = E_3 + K - ell + dimU` holds on each witness: as in the previous
   refutation, the reduction chain is internally correct and only its
   conjectured endpoint is false.

2. **COUNTEREXAMPLE (secondary) — the top-concentrated weakening is also
   false.** The natural prize-facing weakening ("excess in the top
   `(ell-1)/2` fibers `<= ell`", sufficient for the vacancy band via
   `top-m <= 2m + E_3`) fails too: W3 and W2 have `K <= (ell-1)/2`, so
   **all** of their excess lies in the top `(ell-1)/2` fibers.

3. **AUDIT — why ~166k prior law-evidence configs and >700k census configs
   missed this (third recorded constructor-undershoot instance).** The
   winning method: under-plant a big-fiber pair (`mu_1 + mu_2 = ell - 1`,
   nullspace dim 2, or `ell - 2` seeded on an integrated saturator's top
   two, dim 3) and **exhaustively sweep the entire projective nullspace
   family**, reading each member's emergent spectrum — `p + 1` members for
   a pencil, ~50k for `d = 3` (W1 came from a 54,523-member family seeded
   on an integrated saturator's `[14,13]` top pair). The shipped greedy
   constructor reads only one nullspace vector (`basis[0]`); random
   censuses sample the family with probability ~`1/p` per config. Both
   systematically miss the extremal members. Process rule reinforced: a
   family with a cheap exhaustive parametrization must be swept
   exhaustively before its extremes are called.

4. **AUDIT — extremal structure of the violators** (feeds any future
   ceiling attempt): all six are rank-maximal (`rho = ell - 2`,
   `dimU = 2`); five of six are pairwise-cap-tight (`mu_1 + mu_2 = ell`)
   with the excess escaping into a `min-mu >= 3` tail of size-3..5 fibers
   (W3's shape `[ell-3, 3 x7]` is the clean model: one big fiber, seven
   threes, all `n = 8` cosets active). This **corrects the sub-cap
   heuristic**: the proved statement "residual `E_3 = ell` saturators sit
   strictly below the pairwise cap" (§2 item 4) is `E_3 = ell`-specific
   and does not extend to excess `>= 1` — the `E_3 >= ell + 1` violators
   sit exactly ON the cap. Also: the `E_3 = ell + 1` violators already
   occur at `T = 5` (W1, W2) — the smallest residual `T`, so no gap opens
   between Theorem 1's boundary and the violations (the integrated tight
   saturators sit at `T in {6, 9}`).

5. **AUDIT — coverage.** Confirmed violation at `ell in {17, 23, 29}`
   (multiple independent spectra at 29). Shallow sweeps (1-17 pairs/prime)
   reached exactly `E_3 = ell` — the boundary — at `ell = 13` (`p in
   {53, 79}`; the passes at `p in {131, 157}` reached only `ell - 1`),
   `ell = 19` (`p = 191`, deeper rerun; the shallow `p = 229` pass reached
   only `ell - 1`), and `ell = 31` (`p = 311`), all without crossing:
   EXPERIMENTAL, and by item 3's lesson these are expected to cross under
   a deeper family sweep, not to indicate an `ell`-dependent boundary.
   Small `n < K` rows structurally cannot host a `T >= 5` violation.

6. **NEW OPEN TARGET (replacing the dead law):** the observed excess is
   `E_3 - ell in {1, 2}`. Open in both directions: (a) is there a uniform
   ceiling `E_3 <= ell + C` (falsifier: excess `>= 3`), and (b) does the
   excess grow with `ell` or with `n`? Downstream note: the residual-lane
   consumers of the L1 program require polynomial *count* control, for
   which any `E_3 <= ell + O(1)` serves; no wired DAG node depends on the
   exact constant. The vacancy half of `m*(ell) = (ell+1)/2` loses its
   conditional support entirely and returns to fully OPEN (the attainment
   half — unconditional witnesses at `ell in {11, 13, 17, 19, 23}` — is
   untouched; see the concurrent companion note
   `experimental/notes/l1/l1_ell19_attainment.md`).

---

## 1. The witnesses in full

```text
W3: ell=17 p=137 n=8   E_3 = 19 = ell+2   T=6  K=8  sigma=12  dimU=2
gamma = [95, 83, 94, 43, 16, 101, 72, 52, 93, 129, 47, 76, 80, 45, 64, 1]
spectrum_A = [14, 3, 3, 3, 3, 3, 3, 3]     mu1+mu2 = 17 = ell (cap-tight)

W1: ell=29 p=233 n=8   E_3 = 30 = ell+1   T=5  K=8  sigma=11  dimU=2
gamma = [126, 24, 50, 214, 172, 207, 131, 212, 64, 48, 179, 143, 189, 59,
         86, 107, 196, 67, 125, 47, 63, 162, 110, 189, 69, 218, 156, 1]
spectrum_A = [15, 14, 4, 3, 3, 3, 2, 2]    mu1+mu2 = 29 = ell (cap-tight)

W2: ell=23 p=139 n=6   E_3 = 24 = ell+1   T=5  K=6  sigma=9   dimU=2
gamma = [91, 120, 12, 78, 12, 136, 48, 11, 118, 111, 69, 66, 43, 110, 6,
         14, 54, 38, 104, 2, 76, 1]
spectrum_A = [14, 9, 4, 4, 3, 2]           mu1+mu2 = 23 = ell (cap-tight)
```

Three further brute-verified witnesses (spectra `[20,9,4,3,3,3,2,2]` and
`[16,13,4,3,3,3,2,2]` at `(29, 233)`; `[11,5,5,4,3,2]` at `(17, 103)`,
`E_3 = 18 = ell+1` sub-cap `mu_1+mu_2 = 16 < ell` — the one non-cap-tight
violator) are shipped in the certificate JSON with the same fields.
Realizability is by construction: the `gamma` are exhibited and every
quantity is recomputed from them.

## 2. Two PROVED-LOCAL reductions (proofs; they frame the refutation)

1. **The sigma-calculus identity web is realizability-free.** The master
   identity `sigma = E_3 + K - ell + dimU` (and `dim(Vsum) = ell - dimU`)
   holds for arbitrary fiber collections, realizable or not: it is linear
   bookkeeping on the spaces `V_k = h_k F_p[X]_{<= mu_k - 2}`, nowhere
   consuming the existence of a realizing `Gamma`. Verification: the
   non-realizable profile `[6, 6]` at `ell = 7` (`mu_1 + mu_2 = 12 > ell`,
   excluded by the pairwise cap) satisfies it exactly
   (`sigma = 4 = 8 + 2 - 7 + 1`). *Diagnostic consequence* (the
   sigma-calculus note's own N1 no-go, here confirmed on non-realizable
   profiles): a dimension count on `(D, Z, U, V_k)` alone cannot bound
   `E_3` — it re-derives the identity. The law's content was geometric,
   and it is now refuted geometry.
2. **`min-mu >= 3` normalization.** Removing a size-2 fiber preserves
   realizability (a sub-collection of the same `Gamma`'s fibers) and
   changes `E_3`, `T`, and the slack `ell + 2K - P` each by exactly zero.
   So violations normalize: W1 peels to `[15,14,4,3,3,3]`, W2 to
   `[14,9,4,4,3]` (W3 is already `min-mu >= 3`), with `E_3`, `T`
   unchanged — the verifier checks the peeled forms too.

## 3. What SURVIVES

Theorem 1 (`T <= 4 ==> E_3 <= ell`) — untouched, and both witnesses of the
companion attainment note live on its chart; the pairwise cap
`mu_1 + mu_2 <= ell` — holds on all six witnesses (tight on five); the
master identity and sigma-calculus L-lemmas — hold on all six; the
integrated saturators (`E_3 = ell` at `T >= 5`) — now interior points of a
larger extremal family rather than boundary candidates; the
`E_3 <= ell - 2` refutation and all witnesses of the integrated notes; the
attainment half of `m*(ell) = (ell+1)/2` at `ell in {11, 13, 17, 19, 23}`.

## 4. Non-claims

Does not establish any new ceiling (the `ell + 2` maximum is observed, not
proved extremal); does not refute Theorem 1, the pairwise cap, or any
PROVED integrated claim; does not exhibit a vacancy-band violation (no
shipped witness assembles a full listing below `(ell+1)/2`; the vacancy
question is reopened, not answered). One sharp near-miss must be stated
exactly: **W3 does reach the spectrum-side listing gate
`top-m >= 2 ell` at `m = (ell-1)/2 = 8`** (`top-8 = 35 >= 34`, forced by
§0.2: its `E_3 = ell + 2` excess sits entirely in the top 8 fibers, so
`top-8 = E_3 + (ell - 1) = 35`), but with only `n = 8 < 2m - 1 = 15`
cosets it cannot assemble a codeword. The five `E_3 = ell + 1` witnesses
stay below `2 ell` at `m <= (ell-1)/2`. Hence the named falsifier for the
vacancy band itself: **a listing-eligible (`n >= 2m - 1`) witness with
`E_3 = ell + 2` concentrated as in W3 would refute the vacancy band
outright** — that is the natural next target. Promotes nothing —
COUNTEREXAMPLE / AUDIT / PROVED-LOCAL scope only, `experimental/`
placement.

## 5. Verifier contract

`experimental/scripts/verify_l1_e3_law_refuted.py`, zero-arg, stdlib,
offline, deterministic, exit 0 iff all gates pass:

- **Gate i:** for each of the six witnesses, recompute the full spectrum
  from the raw `gamma` with a fresh implementation (coset key
  `x^ell mod p`, per-coset max fiber), and check spectrum, `E_3`,
  `mu_1 + mu_2`, and `E_3 - ell` (the violation margin) exactly.
- **Gate ii:** structural checks per witness: `Gamma` constant-free and
  mixed, `T >= 5` under the printed formula
  `T = sum_{k >= 3}(mu_k - 2)_+`, `n >= K`.
- **Gate iii:** the master identity on each witness: recompute `sigma`,
  `dimU`, `rho` per the sigma-calculus definitions and check
  `sigma = E_3 + K - ell + dimU` and the falsifier signature
  `sigma >= K + dimU + 1`.
- **Gate iv:** pairwise-cap sanity on each witness (`mu_1 + mu_2 <= ell`)
  — the refutation must not silently violate a PROVED bound.
- **Gate v:** `min-mu >= 3` peel of W1, W2 preserves (`E_3`, `T`) exactly.
- **Gate vi:** realizability-free demo: the `[6, 6]` profile at `ell = 7`
  satisfies the master identity while violating the pairwise cap.
- **Gate vii:** Theorem-1 boundary: verify the companion attainment
  witnesses (`ell = 19, p = 647`, both `gamma` embedded) have `T <= 4` —
  i.e. the refutation and the attainment results occupy disjoint charts.
- `--tamper-selftest`: flip one datum per gate; every gate must then fail.

Runtime target < 60 s. Companion data:
`experimental/data/certificates/l1-e3-law/l1_e3_law_refutation.json` (all
six `gamma`, spectra, derived quantities, per-witness verification
provenance, shallow-coverage table of §0.5).

## Refs

- `experimental/notes/l1/l1_prime_ell_key_lemma_refuted.md` (the
  superseded law candidate; constructor lineage; refutation-note pattern).
- `experimental/notes/l1/l1_sigma_calculus.md` (RC statement, Theorem 1,
  falsifier signature, sigma/dimU definitions).
- `experimental/notes/l1/l1_ell19_attainment.md` (concurrent companion:
  attainment at `ell = 19`; unaffected by this refutation).
- `experimental/scripts/verify_l1_sigma_calculus.py` (spectrum and
  sigma-calculus computational conventions).
