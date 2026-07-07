# KB-MCA 1116048 first-match ledger v1 certificate

Status: `CONDITIONAL`.
Claim class: `PARTIAL_UPPER_LEDGER_AUDIT`.

Generated artifacts for the KoalaBear MCA `A=1116048` partial first-match ledger audit.

**This packet does not prove `U(1116048) <= B*`, does not certify the
KoalaBear MCA first-safe agreement, and does not promote v13 raw material
into Paper D.**

## Files

- `kb_mca_1116048_first_match_ledger_v1.json`: machine-readable certificate.
- `README.md`: this generated certificate-directory summary.
- `experimental/notes/certificate_scanner/outputs/kb_mca_1116048_first_match_ledger_v1.report.md`: generated Markdown report.

## Regeneration

```bash
python3 experimental/scripts/verify_kb_mca_1116048_first_match_ledger_v1.py --write
python3 experimental/scripts/verify_kb_mca_1116048_first_match_ledger_v1.py --check
python3 experimental/scripts/verify_kb_mca_1116048_first_match_ledger_v1.py --full --check
python3 -m json.tool experimental/data/certificates/kb-mca-1116048-first-match-ledger-v1/kb_mca_1116048_first_match_ledger_v1.json
```

## Partial claim

The generated-field collision bucket is paid by row-indexed generated-slope image cells
with cost `B_gen <= t*p`.  Q0 records the dyadic quotient/planted rung audit:
descent holds for every rung with `r_c<=w`, terminal rungs `c=65536,131072`
are raw-paid, and the remaining covered rungs are emitted as explicit lower-rung
max-fiber obligations.  The proved remaining multiplier is still `K_rem=4805007`.

Q1 records the exact split-prefix collision decomposition:
`sum_z N_w(z)^2 = binom(n,j) + sum_{e=w+1}^{min(j,n-j)} C_e`,
where `C_e` counts ordered support-pair collisions at one-sided
difference `e`.  The verifier replays this decomposition on small
cyclic-domain examples.

Q2 records the heavy-fiber twist-stabilizer theorem: the `mu_n` twist
action preserves prefix-fiber size, so a sufficiently small heavy-target
set forces nontrivial stabilizer and hence quotient-supported prefix
coordinates.  The verifier replays this stabilizer forcing on small
cyclic-domain examples.

Q2 also records the stabilized-fiber folding theorem.  Over exact
lifted cyclotomic fibers, an `h`-stabilized target with `h/2<=w`
forces every support in the fiber to be a union of `h`-cosets.
For finite KoalaBear use this is conditional on the generated bucket
including prefix-coordinate lift collisions.  Under that wrapper,
`h=2,4,8,16` descend to Q0 quotient rungs and `h=32,...,131072`
are empty in the exact lift because `h` does not divide `j=981104`.

The Q2 closure block records the precise remaining input:
primitive-heavy-orbit exclusion, or equivalently a support-level
generated-prefix multiplicity certificate for non-retained exact
lift classes.  The stronger global count `#heavy<=n/2` would imply
primitive-heavy exclusion, but is not necessary.  At the first useful
scale `h=2`, the heavy-target generated-prefix bucket has at most
`70748471296` image cells if paid separately, and the four
quotient-descended exact-lift lower rows all have max fiber bound `<=11440`.

The packet includes a small `F_17, n=16, j=8, w=1` replay showing
that generated-prefix image cells are not support payments: for the
primitive finite target `z=1`, there are `737` non-retained supports
after keeping the largest exact lift class, while `w*p=17`.

The packet also records failed-route evidence for Q2: Route A
(Delsarte/distance), Route B (local split-pair rank), Route C
(primitive excess moments), and Route D (dyadic folding defects).
Each is kept at its honest status.  Route D supplies the most useful
next target, but still lacks the large signed folding-defect support
certificate needed to pay generated-prefix multiplicity.

The packet also records why Q1 distance alone cannot prove that
orbitwise certificate: the Johnson-packing gap remains enormous.

The certificate proves the split-prefix collision-distance lemma: two distinct
supports in the same prefix fiber differ in at least `w+1=67472` points on
each side.  This is supporting rigidity, not the missing max-fiber theorem.

The certificate also records an honest cyclotomic exact-lift fiber bound `<=11440`.
That bound is not deducted for finite-field use because a valid finite-field lift-class
image cost model remains open.

## Remaining Q2 follow-up

Q1 is now proved as an exact pair-decomposition, and Q2 is proved as
twist-stabilizer forcing plus exact-lift folding rigidity.  The remaining
Q2 work is to supply a primitive-heavy-orbit exclusion certificate
from Q1/higher moments, or a support-level generated-prefix
multiplicity certificate for deployed use.  Once that orbitwise
certificate exists, Q2 routes threatening stabilized targets to generated-prefix
cells, empty exact-lift branches, or the four exact-lift-certified
quotient rungs `h=2,4,8,16`.

## Nonclaims

- Does not prove primitive Q-fin max-orbit flatness.
- Does not pay extension-valued, quotient/planted, sparse, or arbitrary M1 branches.
- Does not prove the Q0 lower-rung quotient/planted max-fiber bounds for `c=2..32768`.
- Does not pay arbitrary planted tails with `r_c>w`.
- Does not prove finite-field lift-class removal at cost `w*p` for prefix-vector fibers.
- Does not prove support multiplicity bounds for non-retained generated-prefix exact lift classes.
- Does not prove primitive-heavy-orbit exclusion needed to activate Q2 stabilizer forcing.
- Does not bound raw support multiplicity inside generated-field image cells.
