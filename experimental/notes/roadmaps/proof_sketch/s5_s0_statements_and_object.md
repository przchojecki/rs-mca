# S5 + S0: the per-rate theorem as it would be submitted, and the object axes

- **Status:** consolidation of verified constants + CONJECTURE-level theorem
  shapes + the S0 audit ledger. NOT rigorous; the theorem statements are
  targets, not claims.
- **Parent:** `prize_proof_sketch_spine.md` S5 and S0. Numerics re-derived
  and machine-checked this turn.

## 1. The master per-rate table [verified, log2 q_line = 256, generating rows]

```text
rate | cap (unsafe,     | MCA quotient    | tau* = FM       | list window
     |  PROVED)         | crossing        | (= list_hi)     | (unsafe, proved-shape)
1/2  | 0.498047         | 0.493809        | 0.496094        | [0.492188, 0.496094]
1/4  | 0.748047         | 0.744141        | 0.746811        | [0.743662, 0.746831]
1/8  | 0.873047         | 0.870854        | 0.872853        | [0.870753, 0.872877]
1/16 | 0.936523         | 0.934888        | 0.936162        | [0.934865, 0.936182]
ordering at every rate:  list_lo < quot < tau* = list_hi < cap   (verified)
```

Reading: the deepest unsafe mechanism is the quotient-core LIST bound
(H/128 slack), then the MCA quotient value-set crossing (beta/128), then
the shared entropy point tau* (which is simultaneously the FM crossing and
the list window's upper end — H/256), then the proved cap. The official
exact-rate rule makes `k` a 2-power, so the dyadic quotient structure is
MAXIMAL on admissible rows — the prize parameters sit at the adversarially
richest point (verified: all scales `M = 2^i <= k` divide `k`).

## 2. Grand MCA, per-rate theorem (conjectured form — the program's target)

```text
THEOREM SHAPE (per rate rho; NOT claimed).
Hypotheses:
  H1  D = mu_n <= F*, n a 2-power, k = rho n exactly, k <= 2^40;
  H2  |F| < 2^256, char(F) odd (automatic: p coprime to 2-power n);
  H3  GENERATING: F = F_p(D)  (else the imported-window column applies, S6);
  H4  sampler and endpoint conventions per the S0 table below, both
      affine and projective gates printed;
  H5  quotient profile: dyadic-maximal (forced by H1);
  H6  [the unproved core] R2 (rigidity, via SPI or XR + Conj F) and the
      zone-(b) collision resolution.
Conclusion:
  a_safe(C)/n = rho + eta*(rho) with eta*(rho) in the S2/S7 bracket, i.e.
  delta*(C) = 1 - rho - c_rho / log2(q_line),
  c_rho in [H(rho)/2 ... 2 beta(rho) ... 2^{256-cap_exp}] per the table,
  pinned to adjacent grid agreements by the assembly compiler (S8) given
  the row's certificate packets.
Unconditional TODAY (no H6): the pinned-row 506/507 partial (proved);
the list-side unsafe half at the gate (thm:qcore, conventions pending);
the cap (unsafe above, proved).
```

Grand List (challenge 2) has the same shape with the S7 window as the
conclusion bracket, the interleaved conversion budgets (`B <= 1.60` worst /
`3.20` a-regular at `n = 2^40, mu = 2`), and the challenge-field
denominator printed.

## 3. The hypothesis table — what each buys [assessment]

```text
generating (H3):   kills B_ext (S6); without it the S7 window binds and
                   the base row is tiny (q_gen < 2^128). FAVORABLE.
exact rate (H1):   forces 2-power k => maximal quotient structure. This is
                   ADVERSE but unavoidable if rules demand exact rates;
                   if WP-0.2 finds dither latitude (k odd-adjusted), the
                   dyadic quotient-core mechanism DIES (no M | k scales)
                   and the corridor narrows to the entropy scale — a
                   one-rules-question swing of ~half the reserve.
char exclusions:   p odd suffices for separability (X^n - 1, 2-power n);
                   the displacement identities (WP-4.1) may add small-p
                   exclusions — print them.
q-columns:         q_gen, q_line, q_chal all printed; tau* evaluated at
                   q_gen for conj:B/L1, q_line for the MCA gate (S4).
projective gate:   floor((q+1)/2^128) can exceed the affine gate by 1
                   exactly when 2^128 | q+1 (demo: q = 3*2^128 - 1 gives
                   gates 2 vs 3) — print both, always (S0 axis 5).
```

## 4. S0 — the object-equality axes, end-of-sketch status

```text
axis                          status after this session
1 batching shape              OPEN (ABF sampler exact form; step-1 flag)
2 ell > 2 batching            OPEN (pairs C^{==2} vs ell-tuples; list side
                              handled by codegree at any m; MCA side needs
                              the tuple-to-pair reduction or a per-ell gate)
3 quantifier order            VERIFIED (step-1)
4 noncontainment predicate    SHARPENED-BUT-OPEN: def:residue's version =
                              degenerate-pencil exclusion (S4, exact);
                              remaining: ABF's Delta_S predicate = this
                              same-support version — ONE definitional axis
5 finite vs projective        VERIFIED for the pinned row; general rows:
                              print both gates (edge case demonstrated)
6 q_gen/q_line/q_chal         DICTIONARY DONE (S4); enforcement -> checker
7 closed-grid vs supremum     VERIFIED (step-1)
8 generating hypothesis       NEW (S6): check the official family
9 exact-rate vs dither        NEW (this node): a rules question with a
                              half-reserve swing; WP-0.2
```

Zero-OPEN (axes 1, 2, 4, 8, 9) remains the gate for any prize-facing
claim, exactly as r2/WP-0.1 demands. Axes 1/2/4 are definitional audits
against the official text; 8/9 are rules lookups. None require new
mathematics — they require care.

## 5. Forks

```text
F1 (axis 2 adverse): if the official MCA quantifies ell-tuples and no
    tuple-to-pair reduction exists, the pair-based ledgers under-count;
    the per-ell gate becomes a new compiler input. Moderate rework, no
    wall.
F2 (axis 9 latitude): dither allowed -> quotient cores die -> corridor
    narrows to [tau*, cap]-ish and the zone-(b) question loses force;
    the sketch's threshold prediction would move UP toward tau*. This is
    the single largest sensitivity in the whole sketch and it is a RULES
    question, not mathematics.
F3 (axis 8 adverse): official family includes non-generating rows -> the
    imported S7 window binds there; per-row two-column tables mandatory.
F4: any S0 axis resolves against the repo convention -> denominators
    reprint, constants shift by bounded factors, no structural change —
    the sketch is built to re-run mechanically (that is what S8 is for).
```
