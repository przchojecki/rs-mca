# Row-sharp Q full-ladder dictionary

Status: `PROVED` dictionary lemma / `AUDIT` packet.

This packet records a small algebraic input for the row-sharp Q and
prefix-fiber programs.  It removes the unnecessary `char(B) > w`
restriction from the zero-prefix dictionary by replacing the first `t`
elementary coefficients with the exact `q`-free coefficient list.

It does not prove row-sharp Q, image-scale MI/MA, a Sidon payment, or any
finite adjacent upper ledger.  It only identifies the exact prefix object
that those arguments must bound.

## Statement

Let `F` have characteristic `q`, let `S` be a finite subset of `F`, and
write the reversed locator

```text
ell*_S(X) = prod_{x in S} (1 - x X)
          = 1 + c_1 X + ... + c_b X^b.
```

For every integer `t >= 0`,

```text
sum_{x in S} x^j = 0 for every 1 <= j <= t
```

if and only if

```text
c_i = 0 for every 1 <= i <= min(t,b) with q not dividing i.
```

The indices divisible by `q` are genuinely free at this dictionary level:
they disappear under formal differentiation.  Indices `i > b` impose no
condition because `deg ell*_S = b`.

## Proof

The logarithmic derivative gives

```text
(ell*_S)' / ell*_S
  = sum_{x in S} -x / (1 - xX)
  = -sum_{j >= 0} (sum_{x in S} x^{j+1}) X^j.
```

Since `ell*_S(0) = 1`, the first `t` power sums vanish if and only if
`(ell*_S)'` is zero modulo `X^t`.  The coefficient of `X^{i-1}` in
`(ell*_S)'` is `i c_i`, so this is equivalent to `c_i = 0` exactly for
the indices `1 <= i <= min(t,b)` that are nonzero in characteristic `q`.

## Why This Matters

Several Q-facing discussions use the Newton/power-sum dictionary in the
large-characteristic form `w < char(B)`.  That is correct when all indices
through the prefix depth are invertible, but the row-sharp zero-prefix
object has a cleaner all-depth form: it is a divisor census with vanishing
locator coefficients only at the `q`-free indices.

This is useful for the current frontiers-paper hard inputs because it
keeps the Q/prefix flatness target honest across ladders and tower
transfers.  It also prevents a false negative conclusion when a prefix
condition lands on a Frobenius-redundant coefficient.

## Myerson Placement

At zero prefix, this dictionary identifies the Q object with a subgroup
linear-equation / Gaussian-period norm census of the kind studied in the
Myerson-Habegger line of work.  That connection is a placement of the
difficulty, not an imported theorem: the available fixed-order results do
not supply the growing-order max-fiber estimate needed by the deployed
frontier rows.

## Replay

Run:

```bash
python3 experimental/scripts/verify_rowsharp_q_full_ladder_dictionary.py
```

The verifier writes
`experimental/data/certificates/rowsharp-q-full-ladder-dictionary/rowsharp_q_full_ladder_dictionary.json`.
It checks two independent finite layers:

- subgroup-subset rows over prime fields, including rows with `t > q`;
- exhaustive formal-derivative rows that exercise the `q | i` free-index
  rule directly.

The script is a replay aid for the algebra above, not a replacement for
the proof.
