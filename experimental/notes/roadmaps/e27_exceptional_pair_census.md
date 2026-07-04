# E27 — the exceptional-pair census at the toy corridor (wave 4, RK axis Q)

- **Status:** EVIDENCE (deterministic seeded census at toy scale, counts
  frozen in the verifier) + one **elementary proved identity** (the
  two-slope pencil cascade, sect. 5(b), one paragraph of algebra). Nothing
  else is PROVED; all rates are observations at `n = 16` only.
- **Agent/model:** Claude (Fable 5), L1 lane, branch `allen/prize-dag-delta`.
- **Date:** 2026-07-03.
- **DAG target:** RK **axis Q** (average -> worst case), the
  exceptional-pair phenomenon; the FORCING form of FACE 4
  (`rigidity_kernel.md`); wave-4 probe E27 of `evidence_plan_codex.md`.
- **Inputs:** `rigidity_kernel.md` (RK schema, 4-branch taxonomy, face 4
  consumption map), `evidence_plan_codex.md` E27 spec,
  `qa3_e14_fm_margin_tables.md` sect. 1 conventions
  (`FM(A) = C(n,j) q^(1-t)`, `t = A-k`, `j = n-A`).
- **Verifier:** `experimental/scripts/verify_e27_exceptional_pairs.py`
  (numpy, deterministic seeds, ~5 min single process, 10 sections
  S1-S7, exit 0 iff all PASS; every count below is frozen there).

## 0. The question

E27 (wave 4, "the central one"): at an FM-suppressed operating point,
record the **multiplicity spectrum** of deep bad slopes over pairs
`(u, v)` and **classify** every multiplicity->=2 pair against the
4-branch taxonomy + the trivial construction `u := c - z0 v on T`.
Exhaustive pair enumeration is impossible (`97^32` pairs); this census
uses the constructive + orbit approach: planted constructions give a
conditional sample of exceptional pairs, an organic random sample gives
the control, and the corridor arithmetic normalizes both.

## 1. Pinned setup (S1-S3)

```text
row      RS[F_97, mu_16, k = 8]: n = 16, q = 97, omega = 8 = 5^6
         (order 16), rate 1/2; codewords = evals of deg < 8 polys.
deep bad slope of (u,v) at agreement A: z in F_97 such that u + z v
         agrees with SOME codeword on >= A of the 16 points.
corridor A* := first A with FM(A) = C(n,n-A) q^(1-(A-k)) < 1:
           FM(10) = 8008/97  ~ 82.5567  (> 1)
           FM(11) = 4368/9409 ~ 0.46424 (< 1)   =>  A* = 11 (t = 3),
         contrast point A*-1 = 10.  NOTE: FM(A*) = Theta(1), NOT << 1 —
         at toy scale the clause-(ii) remainder is VISIBLE (sect. 4).
aperiodicity  all 4368 size-11 supports lie in free rotation orbits
         (|J| = 11 odd => no periodic support; 273 orbit reps, checked
         exhaustively): every deep slope at A* is automatically
         aperiodic, and the MULT branch is parity-blocked at |J| = 11.
detection  syndrome/rank only, no codeword enumeration:
         per support S the GRS dual rows r_m(i) = lam_i x_i^m
         (lam_i = prod_{j != i}(x_i - x_j)^{-1}, m < |S|-k); the slope
         PENCIL <r, u> + z <r, v> kills z on {}, {one z}, or F_q, so a
         support aligns at z iff all its rows kill z — 2 syndrome
         vectors per pair instead of 97 words.  Cross-checked three
         ways (S3): pencil == per-word dual syndrome == brute-force
         interpolation through all C(16,8) point sets, on seeded
         planted + random words, exact agreement.
```

## 2. Constructed exceptional pairs: the spectrum (S4)

2000 seeded triples `(T, z0, c, v)`, `u := c - z0 v` on `T`, uniform off
`T`; the support sample = **all 273 aperiodic orbit representatives** +
1727 uniform draws. Every constructed pair has the planted deep slope
(checked: support `T` aligns at `z0` for all 2000).

```text
multiplicity      1       2      3+
pairs          1309     562     129     (of 2000)
```

Extra (slope, support) events: 869 observed vs the exact first moment
`2000 * 96 * 4368 / 97^3 = 918.9` (pre-registered +-5 sqrt band: PASS).
The spectrum matches Poisson(FM) on top of the guaranteed slope
(`e^-0.437 = 0.646` vs `1309/2000 = 0.654`): **the trivial construction
generically buys exactly ONE deep slope**, and its excess-slope rate is
the FM rate of fresh random words, not an amplification.

## 3. Classification of every multiplicity->=2 constructed pair (S5)

Operational classes for an extra slope `z'` with alignment `(c', J')`
against the planted anchor `(c, J0)` — priority order as listed:

```text
TANGENT       |J0 ^ J'| >= k+1 = 9 (two-slope forced words on > k pts)
MULT          J' invariant under a nontrivial subgroup shift
              (support a union of mu_M'-cosets, pullback branch)
DIHEDRAL      J' = e - J' for some e (inversion-closed up to rotation)
EXTENSION     VACUOUS at this row: F_97 is prime, no proper tower acts
              on mu_16 — branch flagged not-testable at n = 16 (the
              n = 32 / extension-field row is the follow-up).
UNSTRUCTURED  none of the above.
```

Result, 691 pairs / 857 extra slopes, vs chance baselines (null:
independent uniform 11-sets; hypergeometric `P(o >= 9) = 606/4368 =
.1387`; dihedral support fraction `336/4368 = .0769`):

```text
class          count   rate    chance null        deviation
TANGENT          123   .144    .139               +0.4 sigma
MULT               0   0       ~0 (parity)        —
DIHEDRAL          44   .051    .066 (adj.)        -1.8 sigma
UNSTRUCTURED     690   .805    (remainder)        —
```

Anchor-overlap histogram of the 857 extra slopes:
`{6: 75, 7: 326, 8: 333, 9: 109, 10: 14}`. The 14 slopes at overlap 10
sit on just **3 pairs — the cascade stratum of sect. 5** (all 14
pencil-verified; expected trigger events `2000*96*55/97^3 = 11.6`).
Also: 15 pairs are u- or v-deep (vs ~12 expected; u-deep forces slope
0 — the pair-close branch proper), and `|J0|` sizes are
`{11: 659, 12: 32}` (~36 expected at 12). **No class shows an excess
over chance**; fully-structured pairs: 111/691, the chance-composition
rate.

## 4. Organic control: the FM remainder, in band (S6)

100000 seeded uniform pairs (the pre-registered FM control):

```text
multiplicity        0        1       2      3+
pairs           64454    28365    6123    1058
Poisson(.4393)  64454    28315    6199*   1017    (*mult=2 = 7216-1017)
```

(z,S) events: **46205 vs the exact first moment
`10^5 * 4368/97^2 = 46423.6`** (+-1077 pre-registered band: PASS); all
deviations from Poisson self-consistency <= 1.3 sigma. Extra-slope
classes of the 7181 mult->=2 pairs: TANGENT .122, MULT 0, DIHEDRAL
.067, UNSTRUCTURED .811 — each at its (migration-adjusted, sect. 5)
chance value.

**Honest reading of "essentially no organic exceptional pairs":** the
corridor arithmetic of sect. 1 already forces the FM-normalized form of
the pre-registered interpretation — `FM(A*) = 0.464 = Theta(1)` at toy
scale, so chance mult->=2 pairs at rate `~FM^2/2` (~7%) are REQUIRED by
counting, and RK clause (ii) explicitly budgets them. The control
confirms the FM prediction in that exact sense: the organic
exceptional-pair mass equals the first moment to within 1 sigma, with
no structured excess. At prize corridors (`FM = 2^-hundreds`, qa3
tables) the same stratum is empty; "essentially no" is the asymptotic
shadow of this in-band statement.

## 5. THE FINDING: the forcing threshold at core size A-1 (S6b, S6c)

Not pre-registered; **discovered in the census, then verified
algebraically** (labeled accordingly).

**(a) Exclusion.** Among the 6123 exactly-2-slope organic pairs, the
max common-core histogram is `{6: 674, 7: 2367, 8: 2347, 9: 735}` —
**cores >= 10 = A*-1 are entirely absent from multiplicity 2** (the
independence null puts ~76 support-pairs at overlap 10; a -8.8 sigma
hole, and o <= 9 bins are null-consistent).

**(b) The cascade (proved, elementary).** If slopes `z1 != z2` align on
supports sharing a core `T` then on `T`: `v = b := (c1-c2)/(z1-z2)`,
`u = a := c1 - z1 b` (two-slope forced words). If `|T| = A-1`, EVERY
point `p` off `T` with `v(p) != b(p)` upgrades exactly one slope
`z_p = (a(p)-u(p))/(v(p)-b(p))` to full agreement `A` on `T + {p}`.
So a core of size `A-1` forces multiplicity `~ n - |T|` (= 6 here); a
core `>= A` forces all 97 slopes; a core `<= A-2` forces nothing (each
new slope needs >= 2 cooperating off-core points). **Forcing engages
exactly at core `A-1 = k+t-1`.**

**(c) Observed.** Organic cascade pairs per 100000: primary seed **1**
(multiplicity 7) — a disclosed low-tail draw against the exact first
moment `8008 * 10^5/97^4 = 9.05` (`P(N<=1) ~ 1.2e-3`); two replication
seeds fixed before freezing give **8 and 9** cascade pairs with
multiplicities 4-8; pooled 18 vs 27.1 (-1.75 sigma, in the 5 sigma
band; not reshuffled). **Every cascade pair pencil-verifies**:
`(u,v) = (a,b)` off <= `n - |core|` points — the pair is
codeword-line-close, the tangent branch of RK clause (i). The
constructed census shows the same stratum (sect. 3: 3 pairs, 14
slopes). The mult-2 tangent rate sits at the migration-adjusted null
(.1275 predicted after evacuating the o>=10 mass, .1222 observed,
-1.5 sigma): the raw-null deficit IS the forcing theorem's shadow.

## 6. Verdict under the pre-registered interpretation

Both pre-registered clauses fire, and RK's own clause (ii) resolves
them into one decomposition:

- **Unstructured mult->=2 pairs exist, and their precise name is: the
  FM remainder** (RK clause (ii)) — cores <= A-2, rate exactly
  `C(n,j) q^(1-t)`-Poisson (in band everywhere), no mechanism, empty at
  prize-scale FM. They are not a new exceptional class; a new class
  would be an excess over this band, and none is observed.
- **Every pair above the forcing threshold (core >= A-1) is
  structured**, and its structure is the tangent pencil — the FACE 4
  forcing chain (multiplicity -> overlap -> forced words -> clause (i))
  observed end-to-end at toy scale, with its engagement threshold
  MEASURED: core `A-1 = k+t-1`.

So the observed axis-Q decomposition seed is the two-stratum split
`{tangent-pencil above core A-1} + {FM remainder below it}` — the
forcing form of face 4 holds at toy scale in this FM-normalized sense.
Negative findings that also feed the taxonomy: no multiplicative excess
(parity-blocked at odd |J|, ~0.2 expected via |J| = 12, 0 observed), no
dihedral excess at the base row (chance-level rates; modest negative
evidence on E25's base-row side), no fifth shape. Additionally
computed: the pigeonhole overlap `2A*-n = 6 << A*-1 = 10`, so
multiplicity alone does NOT force overlaps at the FM corridor —
face 4's pigeonhole step genuinely needs the corridor-radius regime
(axis R), consistent with RK's axis table; E28's band map should locate
the crossover radius.

## 7. Caveats (all deliberate)

- Toy scale only: one row, one field, one rate; the E27 spec's n = 32
  sampled row (where the extension branch becomes testable) is not run.
- "Unpaid" is not netted against the asymptotic ledgers here; the
  census classifies raw alignments with chance-normalization instead.
- Poisson BANDS are approximations (events cluster mildly); all FIRST
  MOMENTS quoted are exact rationals, computed in the verifier.
- The primary organic seed's cascade count (1 vs 9.05) is a low-tail
  draw: disclosed, replicated on two pre-fixed seeds (8, 9), never
  reshuffled. Frozen values include all three seeds.
- Constructed-pair classification is anchor-based (vs the planted
  codeword); organic classification anchors at the lex-least alignment
  of the least bad slope (deterministic, stated in the script).

## 8. Verifier map

```text
S1   corridor arithmetic, exact fractions        (A* = 11 computed)
S2   domain/orbit audit                          (aperiodicity, baselines)
S3a  pencil == per-word syndrome, 40 pairs       (planted all found)
S3b  per-word == brute C(16,8) interpolation     (8 words)
S4   constructed spectrum, frozen + FM band
S5   constructed classification, frozen; cascades pencil-verified
S6   organic control, frozen + FM band + chance-level classes
S6b  forcing stratum: no core >= A-1 at mult 2; cascades verified
S6c  cascade replication seeds (987654, 13579) + pooled band
S7   contrast A = 10: FM = 82.56 > 1, mean multiplicity ~ 55 (both
     populations) — the corridor cliff against mean <= 1.5 at A* = 11
```
