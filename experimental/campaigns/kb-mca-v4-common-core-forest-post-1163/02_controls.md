# Control Zoo

| Control ID | Object | Preserved structure | Target behavior | Mechanism behavior | Status |
|---|---|---|---|---|---|
| C-001 | #1160 deployed near-rational line | actual line, slopes, supports, noncontainment | excluded before BC/forest | all displayed slopes fail `d1>=w` guard | imported/replayed |
| C-002 | public-DAG GF(11) local-core collision | actual line, unique explanations, maximal supports | reject record-local core owner | overlapping critical records have different cores | imported/replayed |
| C-003 | guarded `K=k+1` boundary counterexample | same lattice envelope | reject silent dimension shift | `s_k<=omega` fails exactly at degree `k` | imported/replayed |
| C-004 | PR #1163 GF(17) inverse-lifted atom | five slopes and common-core cancellation | preserve slopes through cancellation | cancellation succeeds | imported |
| C-005 | all critical subsets of GF(11) collision | complete realizable records | test global priority/fibers | seven-record atlas exhausted; three local cores; one global core | passed |
| C-006 | mutated received coordinate/support/core and metadata | all other certificate fields | verifier must reject | all 29 hostile mutations rejected | passed |

Controls span positive, negative, boundary, and adversarial cases.  The GF(11)
fixture is not evidence about the deployed row unless an implication is proved.
