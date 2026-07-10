# Split-pencil census: G2 support-forcing repair

Status: COUNTEREXAMPLE / PROVED SET-LEVEL REPAIR / OPEN PRICING SEAM.

This packet vendors the prize-side G2 finding into the CAP25-v13
**base-field-normalized split-pencil census** lane.  The original G2 slot was
intended to force top-band petal/support contributors into either a staircase
quotient cell or a primitive residual cell.  The falsification run shows that
the fixed-scale statement is false, while the all-scales closure is true for
a tautological reason.  The real remaining content is the small-scale pricing
class.

## Original fixed-M form

Let `D = H <= F_p^*` have 2-power order `n`.  For a power-map scale `M | n`,
`M > 1`, a support `S` is fixed-M staircase if, up to a tail of size `< M`, it
is a union of complete fibers of `x -> x^M`.  It is fixed-M primitive if its
stabilizer under the order-`M` subgroup is trivial.

The false fixed-M dichotomy said that every top-defect-band contributor is
fixed-M staircase or fixed-M primitive.

## Counterexamples

Two exact witnesses are replayed:

```text
(p,n,M,k,sigma) = (17,8,4,3,1)
(p,n,k,sigma)   = (97,32,12,1), with M = 4 and M = 8
```

In each case there is a codeword whose agreement set lies in the fixed-M top
band, is not tail-plus-full-`M`-fibers, and has nontrivial order-`M`
stabilizer.  Thus the fixed-M dichotomy cannot be used as a theorem-level
split-pencil census input.

The `n=32` witness also illustrates the repair: the same support is a union
of seven order-2 fibers, so it is a quotient/staircase object at a smaller
scale even though it is a fixed-M hybrid at `M=4` and `M=8`.

## All-scales closure

If the statement is changed to "staircase at some dyadic scale `M >= 2` or
aperiodic", then it becomes a set-level theorem for 2-power domains:

```text
periodic support  =>  union of fibers for its stabilizer scale
                   =>  staircase at some dyadic scale.
```

The replay exhausts all nonempty subsets of `Z_8` and `Z_16`, and all
periodic subsets of `Z_32` represented as unions of antipodal fibers.  It
finds no third class.  This is useful as a consistency check, but it is not a
meaningful pricing theorem: the statement is true because it is essentially
the stabilizer partition.

## Corrected Open Problem

The contentful replacement is:

```text
At official rows, every top-band full-petal contributor is either
staircase at some dyadic scale M > t, or aperiodic, or belongs to a
separately priced small-scale quotient class.
```

Equivalently, the real G2 burden is not "prove all periodic supports are
quotient-like"; it is to price the periodic-only-at-scales-`<= t` class.  The
fixed-M counterexamples show that this class is real and can be
p-independent at small rows.

## Nonclaims

This packet does not prove the split-pencil census, the petal-growth node, or
the primitive K4 bound.  It contributes a precise negative result and a repair
target:

```text
REFUTED: fixed-M support-forcing dichotomy.
PROVED:  all-scales closure as a set-level stabilizer statement.
OPEN:    official-row small-scale quotient pricing.
```

## Replay

```bash
python3 experimental/scripts/verify_split_pencil_g2_support_forcing_repair.py
```

Expected digest:

```text
SPLIT_PENCIL_G2_SUPPORT_FORCING_REPAIR_PASS fixed_m_witnesses=2 closure_rows=3
```
