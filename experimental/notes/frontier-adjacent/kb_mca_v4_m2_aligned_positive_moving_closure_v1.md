---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
atom_or_cell: K3_M2_DIAGONAL_112_ALIGNED_POSITIVE_MOVING_MOVING
quantifier: all four moving-moving source assignments and all three aligned-positive residual-root targets, as twelve literal atlas cells
projection_and_unit: exact factor-first q-slice ideals and full J/I quotient parity on the declared named open over GF(2130706433); geometric emptiness persists to the challenge field GF(p^6)
claimed_bound: all twelve moving-moving aligned-positive (1,1,2) atlas cells are empty
status: PROVED_EXACT_LOCAL_LEMMA_REVIEW_REQUIRED_K3_OPEN
impact: deletes twelve atlas cells; together with the pinned F02/F03 deletion exactly eighteen fixed-moving cells remain open; no owner, charge, or ledger movement
falsifier: a failed source pin, a missing moving assignment or target, a surviving named-open component after the recorded J/I parity equations, failed literal b-inversion, or a noncanonical remainder treated as a proof invariant
replay: sage experimental/scripts/compile_kb_mca_v4_m2_aligned_positive_moving_closure_v1.sage --check && python3 experimental/scripts/verify_kb_mca_v4_m2_aligned_positive_moving_closure_v1.py --check --tamper-selftest
---

# Exact deletion of all aligned-positive moving--moving cells

## 0. Verdict and fence

The aligned-positive `(1,1,2)` atlas has four moving--moving assignments

```text
M00={E02,E03},  M01={E02,E12},
M02={E03,E13},  M03={E12,E13}
```

and three residual-root targets `R02,R11,R20`.  This packet proves that all
twelve literal assignment/target cells are empty on their complete declared
named opens.

The proof is assembled without a covariance shortcut:

```text
8 cells  rebuilt and localized directly,
3 cells  transported by the checked full-source map b -> b^-1,
1 cell   imported operationally from the exact GREEN PR #1138 object.
```

The preceding `F02/F03` packet deletes six fixed--moving cells.  Consequently
the exact 36-cell fence becomes

```text
6 fixed-moving cells deleted on the pinned base,
12 moving-moving cells deleted here,
18 fixed-moving cells still open.
```

This is a local deletion lemma.  It moves no ledger quantity and does not
close K3 or the KoalaBear row.

## 1. Direct q-slice systems

The load-bearing Sage compiler imports the exact 36-cell atlas only after
checking its raw SHA-256 and git-blob identity.  For each of

```text
M00-R02, M00-R20,
M01-R02, M01-R11, M01-R20,
M03-R02, M03-R11, M03-R20,
```

it reconstructs the actual source `U,V,z`, clears the complete projective
q-slice equations, factors before localization, and removes only declared
named units.  The `w=0` boundary and the full `w` chart are tested
separately.  No generic saturation is used.

Six direct full charts are empty from the q-slice equations alone.  The two
balanced charts `M01-R11` and `M03-R11` survive the q-slice localization and
therefore receive the complete quotient-parity equations described next.

## 2. Balanced full-quotient parity

For each balanced survivor the compiler independently reconstructs the
complete source polynomial

```text
G(T,W)=U(T,W)^2-W V(T,W)^2
```

and derives the coefficient-one equations in the full `J` and `I` quotient
identities.  Denominators are factored and cleared only by the displayed
named divisors; genuine residual factors such as `L2` are retained.

For both balanced cells, adjoining `J` leaves a two-dimensional named-open
scheme.  Adjoining `I` makes the named localizer nilpotent with exact index
two.  Thus both named-open schemes are empty.

The large parity inputs, augmented Groebner bases, localizer normal forms,
and localizer powers are pinned by exact polynomial hashes in the emitted
certificate.  The two `I` stages terminate with the zero second localizer
power.

## 3. Canonical remainder discipline

The compiler originally stored the textual hash of the normal-form
remainder of `J` or `I` against a `singular:slimgb` basis.  That basis is a
Groebner basis but is not required to be reduced; identical runs can choose
different representatives of the same quotient class.  A replay exposed
this correctly as a fail-closed hash mismatch even though every augmented
ideal and nilpotence witness agreed.

The repaired certificate does not treat that representative as an
invariant.  At each parity stage it checks exactly

```text
parity_polynomial - chosen_remainder in prior_ideal.
```

Hence adjoining the parity polynomial and adjoining the chosen remainder
give the same ideal.  The representative retains degree/support metrics as
execution guards, but no representative SHA-256.  The augmented Groebner
basis, localizer, and nilpotence witnesses remain exactly hashed.  Hostile
mutations must therefore break a mathematical ideal or terminal field, not
merely choose another valid normal form.

## 4. Literal transport and imported cell

The map `b -> b^-1` is checked on the complete source data, not assumed from
an endpoint orbit.  It sends `M01` to `M02`, transports `U,V,z`, the named
open, all four q-slice equations, and every `J,I,K,R` factor multiset.  Thus
the three `M02` targets inherit the three direct `M01` deletions.

The remaining cell `M00-R11` is an operational import from PR #1138.  The
compiler resolves its exact commit, reads the certificate and Sage objects
from that commit, and checks their git blobs, raw SHA-256 values, payload,
field, scope, conclusion, nonclaims, and independent GREEN review record.
No conclusion about another cell is imported.

## 5. Evidence level and replay

Run the full exact compiler:

```bash
env HOME=/private/tmp/rs_mca_sage_home /usr/local/bin/sage \
  experimental/scripts/compile_kb_mca_v4_m2_aligned_positive_moving_closure_v1.sage \
  --check
```

Run the fail-closed semantic and mutation verifier:

```bash
python3 \
  experimental/scripts/verify_kb_mca_v4_m2_aligned_positive_moving_closure_v1.py \
  --check --tamper-selftest
```

Each direct cell runs in a fresh Sage/Singular process before the compiler
assembles the single canonical payload.  This prevents long-lived
Sage--Singular prompt state from coupling otherwise independent cells; the
assembler rejects a missing, duplicate, failed, or reordered shard.

The Sage calculation is exact over `GF(2130706433)`.  Empty localization is
geometric and therefore remains empty over the declared challenge extension
`GF(p^6)`.  There is no floating point, sampling, asymptotic inference,
layer cake, or Markov/Chebyshev step.

## 6. Status and next attack

The exact local proof and compiler are complete, but promotion remains gated
on a fresh independent review.  Until then the packet is
`PROVED_EXACT_LOCAL_LEMMA_REVIEW_REQUIRED`, not a banked GREEN result.

After review, the next aligned-positive attack is the eighteen fixed-moving
cells

```text
F00,F01,F04,F05,F06,F07  x  R02,R11,R20.
```

They must remain literal atlas cells and terminate in exact emptiness, a
named same-record owner, or an explicit primitive route cut.  This packet
does not authorize any K3 or row-level conclusion.
