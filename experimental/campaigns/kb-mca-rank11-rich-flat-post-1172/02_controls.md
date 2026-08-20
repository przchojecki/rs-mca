# Controls

## Positive controls

1. **Actual anchor, not complete core.** The counting universe is
   `G_0=S_0 cap H_{e_0}`, whose size is at most `m`.  The complete pair core
   itself can exceed `m` and is never used as the numerator universe.
2. **Rank-one partition.** For fixed row space `<P>`, all pair differences have
   the same right factor and fall under PR #1171's `8,147,918` ray cap.
3. **Rank-two partition.** For fixed two-plane `U`, both endpoints lie in
   affine translates of `U`; the exact dimension-two pair cap is `252`.
4. **Labeled columns.** Repeated or zero evaluation vectors count with their
   coordinate multiplicities.  Concentration is therefore detected rather
   than silently quotiented away.
5. **Finite matroid audit.** The primary verifier exhausts `2,077` small
   multiset configurations, and the independently written audit checks `1,286`
   rank-at-most-two configurations.

## Hostile controls

1. A pair core may be much larger than `m`; replacing the actual anchor-good
   set by the complete core invalidates the row-space count.
2. Different fixed-right row spaces are not one anticode.  They are summed only
   after the anchor gives a disjoint row-space partition.
3. A rank-two group is not charged as one ray.  It uses the full dimension-two
   interleaved pair cap and the per-pair slope multiplier.
4. The ordered-basis denominator is not `binomial(c,t)`.  It is only
   `(c-h)^t`, which remains valid with arbitrary dependencies and clones.
5. Failure of transversality is not called a payment.  It emits a strictly
   larger common-factor subspace with exact actual-coordinate provenance.
6. No external subspace-design theorem is imported for the special deployed
   evaluation set.

## Exact boundary controls

- `h=42,452` at `tau=1,547` leaves slack `2,007,222,636,724`.
- `h=42,453` at the same cutoff is over budget by `17,108,854,816,460`.
- Exhaustive cutoff scan finds global maximum `h=42,452`, attained at
  `tau=1,547,1,548,1,549`.
