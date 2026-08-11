# Semantic C1--C8 owner-or-envelope: source/Lean correspondence

## Authority and status

Source-facing notes:

- `experimental/notes/thresholds/m31_q_semantic_owner_shell.md`
- `experimental/notes/thresholds/m31_q_deployed_owner_profiles.md`

Formal modules:

- `M31QRootedShell/SemanticOwner.lean`
- `M31QRootedShell/SemanticNaturalScale.lean`
- `M31QRootedShell/SemanticResidualFilter.lean`
- `M31QRootedShell/DeployedOwnerProfiles.lean`
- `M31QRootedShell/SemanticLineRegression.lean`

Status:

```text
PROVED SEMANTIC INTERFACE AND COMPILERS
PROVED EXECUTABLE RESIDUAL FILTER
PROVED TWO DEPLOYED LINE-PROFILE CONSTRUCTORS
PROVED GENUINE F_241 SEMANTIC TWO-OWNER REGRESSION
CONDITIONAL UNIVERSAL SO3+7 INPUT
OPEN DEPLOYED M31 RESIDUAL
```

The modules import the rooted-shell arithmetic and multiplicative route cut
from upstream PR #1005.  They do not repeat either proof or finite support
catalogue.

## Declaration map

| Source object | Lean declaration | Statement audit |
|---|---|---|
| ordered earlier-owner identifiers | `OwnerId` | Exactly C1 through C8; C9 is the residual. |
| executable fixed-before-line owner function | `FixedOwnerFunction`, `FixedOwnerFunction.classify` | Eight Boolean triggers are stored once and checked in literal C1--C8 order. |
| owner-free regression adapter | `allResidualOwnerFunction`, `allResidualOwnerFunction_classify` | Every trigger is false; every explanation is classified `none`. |
| received line -> explanation -> witness -> codeword -> ray -> slope | `SemanticChain` | Every map is explicit. Direct support/codeword/ray/slope projections have compatibility laws with the displayed chain. |
| natural prefix denominator | `NaturalProfileScale.denominator` | Literally `profileFieldCard ^ prefixDepth`. |
| integral natural average | `NaturalProfileScale.averageCeil` | `ceil(fullSupportMass / denominator)` through the local natural-number `ceilDiv`. |
| natural paid numerator | `NaturalProfileScale.naturalNumerator` | Literally `loss * (1 + averageCeil)`. |
| exact slope numerator and denominator | `ExactSlopeBudget` | Stores `U_owner`, positive `q_slope`, and `U_owner <= q_slope`; no equality with the prefix denominator is assumed. |
| distinct line-local slope image | `PaidSlopeProfile` | The slope list is duplicate-free and its cardinality is at most the exact numerator, which is at most the natural numerator. |
| semantic owner soundness | `PaidOwnerLedger` | The global owner function is separate from line-local profiles. Positive classification proves semantic validity and membership of the actual slope in the paid image. |
| one concrete earlier owner | `EarlierOwnerCertificate` | Stores the exact first-match equality `classify x = some owner`. |
| proposition-valued owner branch | `HasEarlierOwner` | Defined as `Nonempty (EarlierOwnerCertificate ...)`, so the semantic disjunction remains a proposition without erasing the concrete certificate type. |
| full chain preservation | `EarlierOwnerCertificate.preserves_chain` | Prints support/witness, codeword/witness, ray/codeword, slope/ray equalities and paid slope-image membership. |
| exact and natural budget chain | `EarlierOwnerCertificate.budget_chain` | Produces `#slopes <= U_owner <= q_slope` and `U_owner <= naturalNumerator`. |
| rooted semantic shell | `RootedShell` | One line, prefix target, anchor, shell, valid explanations, and duplicate-free support projections. |
| generic local rooted-shell inequality | `LocalEnvelopeAt` | Exact natural subtraction `Q * (degree-b) <= c * ambientShell`. |
| literal profile-scale inequality | `LocalNaturalEnvelopeAt`, `localNaturalEnvelopeAt_iff` | The coefficient is definitionally `profileFieldCard ^ prefixDepth`; this is the printed `q_prof^w` formula. |
| abstract actual residual predicate | `IsActualPostC1C8Residual` | Every shell explanation is classified `none` by the same global owner function. |
| generic semantic disjunction | `SemanticEnvelopeOrOwner` | Generic local envelope or a concrete explanation satisfying `HasEarlierOwner`. |
| literal natural-scale semantic disjunction | `SemanticNaturalEnvelopeOrOwner` | Specializes the generic coefficient to `NaturalProfileScale.denominator`. |
| owner branch impossible on actual residual | `actualResidual_has_no_certified_owner` | Contradicts `classify x = none` with the certificate's `classify x = some owner`. |
| actual-residual `3+7` compiler | `semantic_three_plus_seven_on_actual_residual` | The generic semantic disjunction at literal `(b,c)=(3,7)` implies the local envelope on the actual residual. |
| natural-scale actual-residual compiler | `semantic_natural_three_plus_seven_on_actual_residual` | Produces `q_prof^w * max(d-3,0) <= 7 H` on the actual residual. |
| violation-to-owner compiler | `violation_forces_certified_earlier_owner` | A strict generic local-envelope violation eliminates the first disjunct and returns the concrete owner certificate. |
| natural-scale violation compiler | `natural_violation_forces_certified_earlier_owner` | Uses the literal `profileFieldCard ^ prefixDepth` coefficient. |
| executable residual and owned filters | `residualOf`, `ownedOf`, `residualNeighbors`, `ownedNeighbors` | The same fixed owner function partitions one line's semantic explanations into the `none` fiber and the earlier-owned complement. |
| exact filter partition | `residualOf_length_add_ownedOf_length`, `residual_owned_length_eq` | Residual count plus earlier-owned count equals the original rooted degree. |
| actual executable residual shell | `residualShell`, `residualShell_is_actual` | Filtering preserves the line, prefix, shell distance, semantic validity, and duplicate-free support projections; every retained explanation is classified `none`. |
| semantic certificate for each owned explanation | `ownedNeighbor_has_certificate` | Every member of the executable owned filter supplies `HasEarlierOwner`; a support-only label cannot enter the filter without `PaidOwnerLedger` soundness. |
| residual-bound-to-semantic-target compiler | `semanticNaturalEnvelopeOrOwner_of_residualShell` | A bound on the executable residual yields the requested disjunction on the original shell. If the owned filter is empty, the residual equals the full shell; otherwise a concrete certified owner is returned. |
| imported F_241 envelope failure | `f241_localEnvelope_fails` | Reuses PR #1005's `three_plus_seven_fails` after identifying the rooted degree. |
| exact F_241 natural scale | `f241NaturalScale`, `f241NaturalScale_denominator` | `q_prof=241`, `w=2`, full support mass `choose 20 10`, loss one, and denominator exactly the imported `q=58,081`. |
| mandatory generic F_241 owner regression | `f241_semantic_target_forces_certified_owner` | Every generic semantic disjunction on the ten-neighbor packet returns an earlier paid owner. |
| mandatory natural-scale F_241 owner regression | `f241_semantic_natural_target_forces_certified_owner` | The exact `241^2` target returns an earlier paid owner. |
| F_241 residual degree floor | `f241_residualShell_degree_le_eight` | The exact residual `3+7` inequality forces residual rooted degree at most eight. |
| F_241 minimum semantic deletion | `f241_residualShell_bound_forces_two_owned_neighbors` | Since the original degree is ten and the filters partition exactly, at least two neighbors must be earlier-owned. |
| all-residual rejection | `f241_all_residual_rejects_semantic_target`, `f241_all_residual_rejects_semantic_natural_target` | An actual-residual declaration plus either semantic target would imply the false F_241 envelope. |
| explicit owner-free rejection | `f241_owner_free_function_rejects_semantic_target` | Instantiates the fixed all-false C1--C8 classifier and rejects the semantic target. |

## Deployed profile instantiations

| Source object | Lean declaration | Statement audit |
|---|---|---|
| active M31 list-row constants | `m31ListPrime`, `m31ListDomainSize`, `m31ListComplementSize`, `m31ListPrefixDepth`, `m31ListAverageCeil` | Exact integers used by the active adjacent list row. |
| primitive one-pencil arithmetic | `m31List_onePencilCap_eq_two` | Kernel-checks `floor(2,097,152/981,129)=2`. |
| calibrated M31 natural scale | `M31ListNaturalScaleCalibration` | Keeps the huge support mass explicit while binding `q_prof`, `w`, average ceiling, and loss. |
| exact calibrated denominator/numerator | `M31ListNaturalScaleCalibration.denominator_eq`, `.naturalNumerator_eq` | Prints `q_prof^w` and `1+1,993,678=1,993,679`. |
| near-rational profile input | `M31NearRationalCertificate` | Requires a deduplicated line-local slope list of length at most one as an explicit hypothesis.  The active source no longer supplies that cap for an arbitrary line; its support-wise replacement is `<=2w`. |
| primitive one-pencil profile input | `M31PrimitiveOnePencilCertificate` | Requires a deduplicated line-local slope list bounded by the active moving-root quotient `floor(n/omega)`. |
| conditional singleton compiler | `m31NearRationalProfile` | Exact numerator one, `q_slope=p`, and natural-scale comparison for a supplied singleton certificate; not a payment of the full deployed near-rational branch. |
| paid primitive C8 profile | `m31PrimitiveOnePencilProfile` | Exact numerator two, `q_slope=p`, and natural-scale comparison. |
| denominator separation | `m31PrimitiveOnePencilProfile_denominators` | Prints `q_prof^67,447` and `q_slope=p` as distinct fields. |
| exact primitive budget chain | `m31PrimitiveOnePencilProfile_budget` | Gives `#slopes<=2<=q_slope` and `2<=naturalNumerator`. |

These are consumers of theorem-certified line-local slope lists.  They are not
an all-chart census or an exhaustive deployed owner function.

## Genuine `F_241` semantic line regression

| Source object | Lean declaration | Statement audit |
|---|---|---|
| one explicit received line | `actualLine`, `actualU0`, `actualU1` | Twenty coordinate values over the displayed `F_241` domain. |
| eleven explanation supports/codewords/rays/slopes | `supportTable`, `coefficientTable`, `rayCoordinateTable`, `slopeTable` | Ten rooted-shell neighbors plus the anchor. |
| exact agreement certificates | `agreementCheck`, `all_explanations_agree_on_their_supports` | Every degree-`<8` polynomial evaluates to `u0+gamma*u1` on its selected support. |
| noncommon parity certificates | `parityMomentCheck`, `parityDirectionCheck`, `all_parity_certificates_valid` | Each dual row annihilates monomials `0,...,7` but not the line direction. |
| exact codeword-ray normalization | `rayCheck`, `all_ray_certificates_valid` | Coefficients are a nonzero scalar multiple of a normalized last-coordinate-one ray. |
| complete semantic validity | `semanticValid`, `all_explanations_semantically_valid` | Combines support shape, common prefix, received-line agreement, noncommon parity, and ray checks. |
| distinct rays and slopes | `semantic_rays_nodup`, `semantic_slopes_nodup` | No projective or slope duplicates occur in the eleven-state catalogue. |
| concrete semantic chain | `F241SemanticLine.chain` | Instantiates the full line/explanation/witness/codeword/ray/slope interface. |
| common-GCD locator pair | `locatorA`, `locatorB`, `owner_pair_common_core_exact` | The two owner supports have exact common core `[0,1,15]`. |
| exact two-endpoint projective pencil | `splitPencilParameters`, `splitPencilParameters_exact` | Exhausts all 242 projective parameters; only zero and infinity have seven moving roots. |
| fixed C3 trigger | `c3Trigger`, `F241SemanticLine.ownerFn`, `classify_eq_some_iff` | Exactly the two semantic common-GCD/pencil states are classified, in fixed C1--C8 order. |
| exact two-slope profile | `c3Profile`, `c3Profile_budget_chain` | Slopes `[115,22]`, exact numerator two, `q_slope=241`, `q_prof^w=58,081`, natural numerator five. |
| instantiated paid ledger | `F241SemanticLine.ledger` | Positive classification proves semantic validity and slope membership. |
| exact filters | `ownedNeighbors_exact`, `residualNeighbors_exact` | The owned list has the two certified states; the residual has the other eight. |
| genuine owner certificates | `ownerA_has_certificate`, `ownerB_has_certificate` | Both owned states inhabit `EarlierOwnerCertificate`. |
| literal residual theorem | `residualShell_degree_exact`, `residualShell_three_plus_seven` | Exact degree eight and `58,081*(8-3)<=7*44,100`. |
| actual residual and semantic compilation | `residualShell_actual`, `semantic_owner_or_shell` | The residual is the `none` fibre and proves the original semantic disjunction. |
| sharp generic regression | `exactly_two_owned_neighbors`, `generic_two_owner_regression_is_sharp` | The generic lower bound of two owners is attained exactly. |

## Source-statement comparison

The research target is

```text
q_prof^w * max(d_e(A)-3,0) <= 7 H_e
or
an excess neighbor has a certified earlier paid slope owner.
```

`SemanticNaturalEnvelopeOrOwner` is the exact finite interface.  The owner
certificate is stronger than a support tag because its type includes semantic
validity, the entire witness/codeword/ray/slope chain, membership in a
deduplicated line-local slope image, the exact slope numerator and slope
denominator, and the owner's natural prefix-profile scale.

`residualShell` makes “actual post-C1--C8 residual” executable: it is literally
the `none` fibre of the same globally fixed first-match function.
`semanticNaturalEnvelopeOrOwner_of_residualShell` shows that proving the local
inequality there is sufficient for the requested disjunction on the full shell.

The new `F_241` line fixture supplies the previously missing semantic data.  Its
common core alone is not booked.  The two owner states pass the received-line
agreement, noncommon parity, normalized-ray, distinct-slope, exact-pencil, and
paid-profile checks; only then does the fixed C3 trigger fire.  Deleting those
two explanations leaves the exact eight-state residual satisfying `3+7`.

## Proof boundary

Lean kernel-checks the types, finite logical compilers, budget propagation, the
literal natural normalization, executable residual filtering, the generic
`F_241` minimum-owner regression, two scoped deployed profile constructors, and
the complete arithmetic of the genuine finite semantic line fixture.

The parity interpretation uses the elementary source proof: a linear
functional annihilating monomials of degrees `0,...,7` annihilates every
degree-`<8` polynomial evaluation, so its nonzero value on `u1` excludes a
common explanation.  Lean checks every displayed moment and nonzero value.

The following remain hypotheses or future instantiations:

- row-uniform executable definitions of all eight deployed C1--C8 triggers;
- proof-backed slope profiles and chart counts for every positive trigger;
- witness-exhaustive deployed first-match classification;
- the local natural-scale bound on every deployed `residualShell`;
- row-sharp Q, an adjacent safe row, and the global summed completion ledger.

The profile constructors do not promote support-only quotient/dihedral symmetry
or planted-core pruning.  The finite line fixture demonstrates the stronger
semantic evidence required, but it is not itself the deployed Mersenne-31 row.

## Validation policy

The package is stdlib-only and targets Lean `v4.31.0`.  The package root
`M31QRootedShell.lean` imports every module, including the five
semantic/profile modules.  Validation is a direct `lake build` of the package;
every load-bearing declaration ends with `#print axioms`, and the censuses are
empty apart from the `native_decide` certificates declared in
`DeployedOwnerProfiles.lean` and `SemanticLineRegression.lean`.
