# M1 half-turn pair-core compression v1 report

Status: `PROVED_LOCAL_BRANCH_ALGEBRA_WITH_CONDITIONAL_LEDGER_DECOMPOSITION`.

The `{1,3}` classification is proved over the honest characteristic-zero
2-power cyclotomic model.  Finite-field deployed use requires a separate
generated-collision ledger; this report records a finite-field guardrail
showing why that transfer cannot be assumed.

## M1 wall localization

This packet does not close `CAP25-V13-M1-UNIFORM-SPLIT-LOCATOR-DETERMINANT-COMPRESSION`.  It localizes one half-turn coefficient-shadow subbranch: `{1,3}` pair-core mass is slope-small over the honest model, `{1,3}` finite-field failures are generated collisions of `F3(R)`, and `{1,4}` residuals decompose into pair-small, recursive lower-domain, and half-turn-balance ledgers.

## Deployed KoalaBear branch arithmetic

These rows check the parity and budget arithmetic for the honest characteristic-zero `{1,3}` branch.  They do not certify the actual finite-field KoalaBear slope image.

| A | j=n-A | parity | slope bound | below B* | bit margin |
| -: | -: | :-: | -: | :-: | -: |
| 1116044 | 981108 | even | 1 | yes | 57.932108 |
| 1116045 | 981107 | odd | 2097152 | yes | 36.932108 |
| 1116046 | 981106 | even | 1 | yes | 57.932108 |
| 1116047 | 981105 | odd | 2097152 | yes | 36.932108 |

## Finite-field transfer guardrail

Over `F_17` with `n=16` and generator `3`, support exponents `[0, 1, 3, 14]` satisfy the `{1,3}` rows with finite slope `16` but have half-turn residual size `4`.  This is a counterexample to naive finite-field transfer of the characteristic-zero `{1,3}` classification.
The same residual-defect identity classifies the example: `F3(R)=e1(R)e2(R)-e3(R)` is nonzero over `Q(zeta_16)` with key `1,3,3,1,2,0,0,-2`, but reduces to `0` modulo `17`.

## Small exact {1,3} cyclotomic enumerations

| n | j | survivor supports | predicted supports | slopes | bound |
| -: | -: | -: | -: | -: | -: |
| 8 | 3 | 24 | 24 | 8 | 8 |
| 8 | 4 | 6 | 6 | 1 | 1 |
| 8 | 5 | 24 | 24 | 8 | 8 |
| 8 | 6 | 4 | 4 | 1 | 1 |
| 8 | 7 | 8 | 8 | 8 | 8 |
| 8 | 8 | 1 | 1 | 1 | 1 |
| 16 | 3 | 112 | 112 | 16 | 16 |
| 16 | 4 | 28 | 28 | 1 | 1 |
| 16 | 5 | 336 | 336 | 16 | 16 |
| 16 | 6 | 56 | 56 | 1 | 1 |
| 16 | 7 | 560 | 560 | 16 | 16 |
| 16 | 8 | 70 | 70 | 1 | 1 |

## Small exact {1,4} residual-core checks

| n | j | survivor supports | slopes | residual-choice bound | residual sizes |
| -: | -: | -: | -: | -: | :-- |
| 8 | 4 | 0 | 0 | 41 | none |
| 8 | 5 | 0 | 0 | 40 | none |
| 8 | 6 | 0 | 0 | 25 | none |
| 8 | 7 | 8 | 8 | 8 | 1:8 |
| 8 | 8 | 1 | 1 | 1 | 0:1 |
| 16 | 4 | 0 | 0 | 1233 | none |
| 16 | 5 | 0 | 0 | 2256 | none |
| 16 | 6 | 0 | 0 | 3025 | none |
| 16 | 7 | 80 | 16 | 3280 | 1:80 |
| 16 | 8 | 42 | 17 | 3281 | 0:10, 2:32 |

## {1,4} residual-image ledger bound

After charging lower-domain shadow and higher-pair balanced residual ledgers, the primitive `{1,4}` residual image is bounded by `2097153`.

| bound | below B* | bit margin |
| -: | :-: | -: |
| 2097153 | yes | 36.932107 |

## Small {1,4} residual parity obstructions

| s | q | zero-sum length | conclusion |
| -: | -: | -: | :-- |
| 2 | 1 | 3 | odd length cannot be half-turn-balanced |
| 3 | 1 | 9 | odd length cannot be half-turn-balanced |
| 4 | 1 | 25 | odd length cannot be half-turn-balanced |
| 4 | 0 | 15 | odd length cannot be half-turn-balanced |
| 5 | 0 | 45 | odd length cannot be half-turn-balanced |
| 6 | 0 | 105 | odd length cannot be half-turn-balanced |

## {1,4} parity-empty residue classes

- `q=0` half-turn-balance is parity-empty for `s mod 8` in `3, 4, 5, 6`.
- `q=1` half-turn-balance is parity-empty for `s mod 8` in `1, 2, 3, 4`.

## Twofold lower-fiber counterexample

In `mu_{16}`, residuals `[2]` and `[0, 4]` have the same `(A_R,B_R)` but are neither equal nor antipodal.  This rules out unrestricted twofold lower-fiber rigidity.

## Fixed-size AB-rigidity base case

The packet includes the proved `s=2` base case as a machine-checkable sanity check: every tested fixed-size `(A_R,B_R)` fiber is exactly the antipodal pair `{R,-R}`.

| n | residuals checked | AB fibers | max residuals/AB |
| -: | -: | -: | -: |
| 8 | 24 | 12 | 2 |
| 16 | 112 | 56 | 2 |
| 32 | 480 | 240 | 2 |
| 64 | 1984 | 992 | 2 |

## Half-turn-balance valid-range caveat

The bare statement that no half-turn-free residual with `|R|>=2` has `B_R=0` is false: in `mu_{16}`, residual `[0, 2]` has `B_R=0`.  This is outside the actual `q=0` `{1,4}` range, where `j=s>=4`.

## Imbalance-vector reduction targets

Status: `REDUCTION_TARGETS_NOT_PROVED_HERE`.

For a positive multiset M of 2^m-th roots, Delta_M(xi) is mult_M(xi)-mult_M(-xi).  Over Q(zeta_{2^m}), sum(M)=0 iff Delta_M is identically zero.

Half-turn-balance emptiness reduces to:

- q=0 valid range `s>=4, R half-turn-free`: `Delta(Bcal_R) is not identically zero`.
- q=1 valid range `s>=2, R half-turn-free, u in mu_{2^{m-1}} \ R^2`: `Delta(Bcal_R disjoint_union (-u*Acal_R)) is not identically zero`.

The still-open congruence classes are q=0 `s mod 8` in `0, 1, 2, 7` and q=1 `s mod 8` in `0, 5, 6, 7`.

Fixed-size AB-rigidity reduces to:

- For |R|=|R'|>=3, equality of Delta(Acal_R),Delta(Bcal_R) with Delta(Acal_R'),Delta(Bcal_R') forces R'=R or R'=-R.
- Proved base case: `|R|=|R'|=2`.

## Experiment evidence for next targets

Status: `EXPERIMENTAL_EVIDENCE_NOT_A_PROOF`.

- Half-turn-balance: no `q=0` or `q=1` hits were found in the extended exact/sampled rows.
- Fixed-size AB fibers: max residuals per `(A_R,B_R)` fiber was `2`, max slopes per fiber was `2`, and every observed twofold fiber was antipodal.

Recommended next targets:

- valid-range half-turn-balance emptiness.
- fixed-size imbalance-profile rigidity modulo antipodal symmetry for residual sizes >=3.
- sparse/nonconsecutive row-slice inverse classification.
- finite-field generated-collision accounting.

## Conclusion

The small exact enumerations match the symbolic classification: the `{1,3}` characteristic-zero branch consists exactly of half-turn pair cores plus at most one residual singleton.  The deployed KoalaBear rows record only the corresponding parity/budget arithmetic for that honest branch, not a finite-field slope certificate.  The `{1,4}` checks verify the exact residual-core equation and confirm that paired-core completions do not multiply slopes.  The residual-image ledger theorem then leaves only the `n+1` pair-small primitive remainder after the lower-domain and higher-pair balanced residual branches are charged.

## Non-claims

- Does not cover finite-field generated-collision amplification.
- Does not cover finite-field {1,3} generated-collision emptiness or budget-smallness.
- Does not cover deployed KoalaBear finite-field {1,3} slope image.
- Does not cover a standalone numerical cost theorem for the recursive lower-domain ledger.
- Does not cover a standalone numerical cost theorem for the half-turn-balance ledger.
- Does not cover full valid-range half-turn-balance emptiness.
- Does not cover fixed-size imbalance-profile rigidity modulo antipodal symmetry for residual sizes >=3.
- Does not cover arbitrary nonconsecutive coefficient windows.
- Does not cover sparse Hankel-proxy row slices.
- Does not cover full M1 closure or deployed safe-side certificate.
