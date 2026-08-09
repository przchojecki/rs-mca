# K3 cell-5 xi=3 pairings 3-5: exact local route-cut audit

```yaml
workboard_item: K3
row: KoalaBear MCA at target epsilon 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: the guarded positive 433-1b source-role cell-5 xi=3 representatives 3, 4, and 5 are empty over F_2130706433
architecture: K3 coordinate-positive 433-1b source-role workboard
partition_digest: public-DAG-433-1b-router@28b3bc8a
atom_or_cell: source-role cell 5; xi=3; pairings 3,4,5
quantifier: all 20 exact source/colored sign rows printed in the certificate
projection_and_unit: local matching labels; not yet a v4 slope atom
claimed_bound: zero witnesses in the declared local cells
status: EXPERIMENTAL_REVIEW_REQUIRED
impact: ROUTE_CUT
falsifier: a covered witness, final pair solution, unresolved branch, unhandled degree drop, or source-hash mismatch
replay: certificate verifier plus source-bound local FLINT/SymPy run
```

## Statement audited

The implication from the public cell-5 four-basis tower and compact kernel to
emptiness of the `xi=3` pairing representatives `3`, `4`, and `5`.

The source inputs are pinned to
[`AllenGrahamHart/rs-mca-prize-dag@28b3bc8a`](https://github.com/AllenGrahamHart/rs-mca-prize-dag/commit/28b3bc8ab13e94c25088e904251eb5cf49e68ad2).
The cell-4 compilers are reused without changing their algebra; the adapter
replaces only the structure rows by the cell-5 `c_row_index=6` base, `b`, and
`c` relations and reclassifies a free `b` or `c` only when the corresponding
cell-5 leading coefficient vanishes.

## Exact census

| Pairing | Signed rows | Target roots | Candidates | Source routes | `z` / `q` candidates | Final pairs | Witnesses |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 8 | 32 | 88 | 80 | 0 / 0 | 0 | 0 |
| 4 | 4 | 40 | 80 | 144 | 24 / 24 | 0 | 0 |
| 5 | 8 | 48 | 128 | 208 | 0 / 0 | 0 | 0 |
| **Total** | **20** | **120** | **296** | **432** | **24 / 24** | **0** | **0** |

The certificate also records 180 guarded boundary rows, 40 target-product
boundaries, and 96 no-lift rows.  None is silently counted as a generic root.

## Independent tool checks and method input

Wolfram independently checked one representative pairing-3 no-`b` lift.  At
`(r,t)=(396444866,310013572)`, the cell-5 quadratic in `b` has coefficients

```text
(1629468848, 1735544835, 1629468848) mod 2130706433,
```

discriminant `1527757769`, and Euler value `2130706432 = -1 mod p`; Wolfram
also returned `PrimeQ[p]=True`.  Thus that recorded `NO_B_ROOT` classification
is independently reproduced.  This is a representative arithmetic check,
not an independent proof of all 20 rows.

The literature search identified Chen--Moreno Maza's specialization theorem
for subresultants as the relevant safeguard for the remaining branch audit:
[Algorithms for computing triangular decomposition of polynomial systems](https://www.csd.uwo.ca/~mmorenom/Publications/Chen.Moreno_Maza.JSC.47.2012.610-642.pdf),
JSC 47 (2012), Theorems 4--6.  Its practical lesson here is precise: a generic
resultant is insufficient unless vanishing initials and degree drops are
separately represented.  The packet therefore treats leading boundaries as
first-class rows; it does not invoke the paper as a theorem about RS-MCA.

## Dependency and parameter audit

- **PROVED upstream:** the cell-5 four-basis tower and compact kernel; the
  three cell-4 compilers; the universal outside-role transport theorem.
- **Exact computation here:** all 20 deployed-field rows have no witness or
  unresolved branch.
- **Unreviewed here:** correctness of the adapter substitution, completeness
  of the boundary reclassification, and composition with the source-role
  transport and exact labeled add-back.
- **Parameter dependence:** this result is only over the deployed prime field
  `F_2130706433`, at source-role cell `5`, `xi=3`, and pairings `3,4,5`.
- **Layer-cake / dyadic summability:** not applicable.
- **Moment / Markov / Chebyshev:** not applicable.
- **Asymptotics:** none; this is an exact deployed-field computation.

## Verdict

**YELLOW — strong exact route-cut evidence, independent review required.**

If a fresh review is GREEN, this removes three of the six pairing
representatives left after the public pairing-1/2 result.  The next common
compiler family is `xi=3` pairings `7`, `8`, and `11`.  No v4 ledger value,
K3 closure, or KoalaBear-row closure is claimed.
