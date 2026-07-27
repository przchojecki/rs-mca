# KoalaBear K3 equality-wall prerequisite packet

```yaml
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
agreement: 1116048
B_star: 274980728111395087
architecture: source-bound equality-wall prerequisite chain
partition_digest: N/A - this packet imports theorem prerequisites and does not define a new partition
atom_or_cell: declared source-bound equality-wall residual
quantifier: exact deployed-row statements over every record admitted by the cited source-bound packets
projection_and_unit: distinct affine bad slopes per received line
direct_statement: the 22 verifier families in the endpoint import closure are replayable prerequisites for the equality-wall normalization
status: PROVED_LOCAL_PREREQUISITES
impact: ROUTE_REDUCTION_ONLY
falsifier: any failed exact replay, manifest mismatch, optimized-mode acceptance, or failed Lean build
```

## Scope

This packet imports only the source-bound theorem families reached by the five
equality-wall endpoint verifiers. It also includes four theorem families cited
as exact source bindings by that import closure. It excludes the remaining
six historical or unrelated verifier families, the unrelated
`kb_uq_post_rational_restriction` Lean package, and edits to the global agent
log or script index.

The packet is proof provenance for the child normalization PR. It does not
prove the normalized equality-wall endpoint by itself.

## Exact dependency closure

The imported families are:

1. active carrier-incidence replay;
2. active full-histogram replay;
3. C5/twist/Frobenius-9208 adapter;
4. first-gap complement-locator linearization;
5. first-gap source-interpolation pencil;
6. first-gap source-pencil image owner;
7. next-slack source-plane closure;
8. post-first-gap histogram replay;
9. post-next-slack histogram replay;
10. post-second-successor histogram replay;
11. post-successor histogram replay;
12. reciprocal-kernel plane sweep;
13. second-successor upper intrinsic-plane descent;
14. successor lower-stratum Segre descent;
15. successor upper-stratum quadratic-adjugate reduction;
16. tangent-deep owner adapter;
17. tangent-deep source-rational adapter;
18. tangent-deep source-rational C5 adapter;
19. first-gap projective-residue C5 rank dichotomy;
20. second-successor lower source plane.
21. first-gap outlier-basis residue transform;
22. post-reciprocal-kernel full-histogram replay.

The tangent-deep owner Lean package is retained because it formalizes one
load-bearing member of this closure.

## Portable replay

From the repository root:

```bash
python3 experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_prerequisites_v1/replay.py --quick
python3 experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_prerequisites_v1/replay.py --full
```

`--quick` validates committed exact certificates. `--full` additionally runs
all tamper suites and builds the retained Lean package. Child processes use the
same interpreter through `sys.executable`.

The formal build was replayed with:

```text
Lake version 5.0.0-src+68218e8 (Lean version 4.31.0)
Lean commit 68218e876d2a38b1985b8590fff244a83c321783
lake build
```

The committed module prints its axiom dependencies during the build.
`activeOwner_cases_of_bad`, `frontload_tangent_paid_union`, and
`activeDeep_characterization` depend only on `propext`;
`firstOwner_unique` and `deployedConstantsExact` report no axioms.

The packet replay refuses optimized execution before invoking any child
verifier. The imported verifiers use explicit validation functions rather than
load-bearing Python assertions. Integrity checks, exact replays, and formal
builds are reported separately; a SHA-256 match is not described as a
mathematical proof.

## Nonclaims

This packet produces no `U_Q`, `U_BC`, `U_new`, global chart census, complete
K3 slope payment, KoalaBear row certificate, or active-endpoint movement. It
does not derive the global pencil-chart census missing from the local route cut
or aggregate any fixed-union transverse-secant payment.
