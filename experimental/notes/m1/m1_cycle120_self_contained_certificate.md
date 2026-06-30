# M1 Cycle120 Self-Contained MCA Witness Audit

Status: EXPERIMENTAL / SELF-CONTAINED-WITNESS / ABF-DEFINITION-AUDIT.

Companion script:

```text
python3 experimental/scripts/verify_m1_cycle120_self_contained_certificate.py
```

(pure stdlib, ~3 min, exit 0; reproduces under multiple seeds.)

## What this adds over the existing Cycle120 notes

The earlier integration
(`m1_cycle120_abf_counterexample_candidate.md`,
`m1_cycle120_standalone_ldsw_proof.md`) made the negative ABF statement
*conditional on two unaudited inputs*: the Cycle84 finite census
`N = 52,747,567,092` (a 26-billion-entry C++ computation that lived in a rejected
archive) and the "Cycle116 slot identity" (flagged as an open reviewer input).
This witness audit removes both dependencies:

1. **The fixed-jet "slot identity" is now PROVED, not assumed.** For the published
   model `F16 = F_17[X]/(X^16+X^8+3)`, `eta = 6X^9` (order 256, `D0 = <eta>`),
   `beta = X+2`, and the three 8-element exponent sets `E_SET_i`, *every* seven-slot
   support `support(T)` is a genuine 113-subset of `D0` whose locator
   `P_T(X) = prod_{x in support(T)} (X-x)` has constant top-6 coefficients
   `[1,16,0,0,0,0]`, i.e. `P_T = X^113 - X^112 + O(X^107)`. Reason: the support's
   power sums satisfy `p_1=...=p_5=1` for every `T`, because per slot
   `sum y = sum y^2 = sum y^4 = 0` — exactly the identities `sum_{e in E_SET_i} 3^e
   = sum_{e in E_SET_i} 9^e = 0 (mod 17)`. And `sum y^6 != 0` (so `sigma` is exactly
   6). Hence the fixed-jet hypothesis of the locator transfer (Lemma 1) holds by a
   short structural argument, not by computer census.

2. **The 26-billion census is not load-bearing.** Since
   `floor(17^32 / 2^128) = 6`, the ABF density gate
   `emca >= M/17^32 > 2^-128` is cleared as soon as `M >= 7` distinct bad slopes.
   The census `N ~ 5.3e10` only sharpens the density from `~2^-128` to `~2^-95`.
   This note exhibits and fully machine-checks **`M = 40` explicit distinct
   slopes** — a conservative, self-contained sample, with no external data.

## The checked statement

```text
K = F_17^32,  H = <theta> <= K^*,  |H| = 512,  C = RS[K,H,256].
```

The script machine-checks, with pure-stdlib arithmetic and no external input:

```text
emca_sw(C, 125/256)  >=  40 / 17^32  =  2^-125.48  >  2^-128,
```

where `emca_sw` is the **support-wise** mutual-correlated-agreement error: there is
one affine line `f1 + gamma f2` and (at least) 40 distinct parameters
`gamma in K` such that, for each, the line point `f1 + gamma f2` agrees with a
degree-`<256` codeword on a support `S_gamma subset H` of size
`262 = (1 - 125/256) * 512`, while the pair `(f1, f2)` is **not** jointly
degree-`<256` explained on that same `S_gamma`.

## What the script checks (every step, no sub-sampling over the 40 slopes)

```text
Field setup:  X^16+X^8+3 irreducible; ord(eta)=256; eta^16=3; beta not in D0;
              K = F16[theta]/(theta^2-eta), ord(theta)=512 (v2(17^32-1)=9);
              sum 3^e = sum 9^e = 0 (mod 17) for each E_SET_i.
Step 1:       41 distinct slopes z_T = 1/P_T(beta) (1 anchor + 40 counted);
              fixed jet p1..p5=1, p6!=1 / top-6 coeffs [1,16,0,0,0,0], deg 113.
Step 2 (F16): native Lemma 1 line (f,g); for ALL 40 members, f+z_T g equals a
              degree-<137 codeword on D0 \ support(T) (size 143, agreement 143),
              and g is NOT degree-<137 explained there (real noncontainment).
Step 3 (K):   Lemma 2 smooth padding, A subset theta*D0 with |A|=119, L_A deg 119;
              f1 = L_A f, f2 = L_A g on D0, 0 on A. For ALL 40 members the explicit
              witness W_T = L_A c_T has degree exactly 255 < 256 and equals
              f1 + z_T f2 at all 262 points of S = (D0 \ support(T)) union A; and a
              DIRECT linear-algebra check confirms (f1,f2) is not jointly
              degree-<256 explained on S.
Step 4:       floor(17^32/2^128)=6; M=40>6; emca_sw >= 40/17^32 > 2^-128.
```

The witness audit was independently reproduced by an adversarial re-implementation
(schoolbook field arithmetic, independent Newton-divided-difference rank test) that
cross-checked the exact 40 slopes byte-for-byte and confirmed non-vacuity (a real
degree-`<256` codeword is correctly reported "explained"; the line point is a codeword
on `S` while `f2` is not).

## ABF Definition 4.3 (verified against ePrint 2026/680)

The repository's `open-proximity.pdf` is **byte-identical** (MD5
`df2a2bff7abff8604201bc47447aacea`) to the official Cryptology ePrint Archive
**2026/680** — Arnon, Boneh, Fenzi, *Open Problems in List Decoding and Correlated
Agreement* (companion survey to the Proximity Prize). Its Definition 4.3 (p. 17) defines
the MCA error verbatim as

```text
eps_mca(C, delta) := max_{f1,f2} Pr_{gamma <- F}[ exists S = S_gamma, |S| >= (1-delta) n :
                       Delta_S(f1 + gamma f2, C) = 0  AND  Delta_S((f1,f2), C^{=2}) > 0 ].
```

Matching this against the audit, term by term:

```text
gamma <- F          : gamma uniform over the FULL field F = K = F_17^32      [cert: yes]
exists S = S_gamma  : SUPPORT-WISE, the set may depend on gamma (inside Pr)   [cert: yes, per-slope S_T]
|S| >= (1-delta)n   : closed threshold; at delta=125/256, n=512 -> |S|>=262   [cert: yes]
Delta_S(...) = 0    : f1+gamma f2 agrees with a codeword on S                 [cert: explicit deg-<256 witness]
Delta_S((f1,f2))>0  : the pair is NOT jointly explained on the SAME S         [cert: direct linear algebra]
(no extra filter)   : a bare max/Pr -- no q_chal/quotient/endpoint/dup charge [cert: counts all 40]
```

So `emca_sw` as certified **is exactly** ABF's `eps_mca`. The one prior worry —
support-wise vs. a single common support — resolves in the audit's favour: ABF is
support-wise (`exists S_gamma` sits *inside* `Pr_gamma`). The row is in scope:
`rho = 256/512 = 1/2`, `L = H` smooth of order `512 = 2^9` with `2^9 || 17^32 - 1`,
`k = 256 <= 2^40`, `|F| = 17^32 < 2^256`. Hence, against ABF's exact quantity,

```text
eps_mca(RS[F_17^32,H,256], 125/256)  >=  40/17^32  >  2^-128,
```

and therefore (`eps_mca` nondecreasing in `delta`, Paper A Lem 3.3) a machine-checked
upper bound on the safe MCA radius for this row: **`delta*_C < 125/256`**.

## Scale: relation to the Paper D v7 universal cap

For orientation against the canonical caps: Paper D v7's rate-`1/2` field-size-universal cap is
`delta*_C <= 1 - rho - 2^-9 = 255/512` (equivalently its first-grid cap `1 - rho - 1/n` at `n = 512`).
This row-specific bound `delta*_C < 125/256 = 250/512` lies `5/512` *inside* that
universal envelope, backed by an exact machine-checked witness. It does **not** sharpen the universal
theorem (a worst-case-over-rows cap; an individual row may sit strictly below it) — it is a concrete,
verifiable obstruction for one prize row, situated below the published cap.

## Exact scope and nonclaims

- **What it is.** A self-contained, machine-checked, adversarially-verified *exact finite
  witness* that ABF's `eps_mca` exceeds `2^-128` at `delta = 125/256` for this concrete
  smooth row — concretizing ABF's Table 1 near-capacity statement
  (`eps_mca >= n^{Omega(1)}/|F|`) with an explicit constant, and giving the upper bound
  `delta*_C < 125/256`.
- **What it is NOT.** It does **not** refute any inequality ABF asserts — ABF prints no
  upper bound `eps_mca(C,125/256) <= 2^-128`. On the contrary, `delta = 125/256 = 1/2 - 3/256`
  sits just below `delta_min = 257/512` (and far above the Johnson radius ~0.294), the
  near-capacity zone where ABF's own Table 1 already expects large error. The result is
  therefore **consistent with** ABF and contributes to the *open* grand-MCA challenge (the
  negative side, for one row); qualitative MCA failure this close to `delta_min` is
  expected — the contribution is the *exact, self-contained, machine-checked* witness and
  the audited construction, not a surprise about where MCA fails.
- It does **not** determine `delta*_C` exactly (only the upper bound), does not prove an
  ordinary list-decoding lower bound, and is not an accepted Proximity-Prize solution.

## Relation to the prior notes

This is the clean, self-contained successor to the conditional chain in
`m1_cycle120_standalone_ldsw_proof.md`. The transfer Lemmas 1 (fixed-jet locator) and
2 (smooth padding) are the same; what changed is that their hypotheses are now
discharged from first principles and the bad-slope count is an explicit machine-checked
`40`, so the result no longer depends on the Cycle84/Cycle116 finite computation or any
rejected archive. This integration reviews the constants as supplied in PR #146; it does
not audit Danny's external fork or any generated census machinery.

It also **corrects the framing** of those notes: they described the result as a
"counterexample candidate to the printed ABF grand MCA inequality." Per ePrint 2026/680
ABF prints no such inequality at this radius — so the accurate statement is a
machine-checked `delta*_C < 125/256` that concretizes ABF's Table 1, not a refutation.
