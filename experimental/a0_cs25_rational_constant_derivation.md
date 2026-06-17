# A0 Crites-Stewart Rational Constant Derivation

## Claim

Assume the Crites-Stewart correlated-agreement-to-list theorem has the
following exact rational form for `C = RS[F,D,k]`, `|D| = n`, `|F| = q`,
`C+ = RS[F,D,k+1]`, and `epsilon = eca(C,delta)`:

```text
if epsilon < (q - n)/(k q), then
Lst(C+,delta) <= ceil(epsilon q (q - n)/(q - n - k epsilon q)).
```

Then the relaxed import used in Paper D follows by one line of algebra:
for every `theta in [0,1)`,

```text
epsilon <= theta * (q - n)/(k q)
    implies
Lst(C+,delta) <= ceil(q epsilon/(1 - theta)).
```

In particular, `theta = 1/2` gives the local cap threshold

```text
eca(C,delta) > (1/(2k)) * (1 - n/q)
```

whenever the quotient-fiber lower bound gives a list of size at least
`q/k + 1` in `C+`.

## Status

AUDIT / CONDITIONAL.

This note checks only the constants in the rational implication. It does not
certify that the primary Crites-Stewart theorem has the exact displayed
hypotheses, field generality, radius range, or CA normalization needed by the
manuscript.

## Source Status

The exact rational statement above is the form reported in public summaries of
Crites-Stewart Theorem 2 and is compatible with the relaxed restatement already
printed in `tex/cs25_cap_v4.tex`. The primary source remains:

```text
https://eprint.iacr.org/2025/2046
```

That primary theorem should still be checked directly before promoting the
universal cap from conditional to source-certified.

## Derivation

Write

```text
R(epsilon) = epsilon q (q - n)/(q - n - k epsilon q).
```

If

```text
epsilon <= theta * (q - n)/(k q),
```

then

```text
k epsilon q <= theta (q - n),
q - n - k epsilon q >= (1 - theta)(q - n).
```

Substituting this lower bound in the denominator gives

```text
R(epsilon)
    <= epsilon q (q - n)/((1 - theta)(q - n))
     = q epsilon/(1 - theta).
```

After applying ceilings,

```text
Lst(C+,delta) <= ceil(q epsilon/(1 - theta)).
```

This is exactly the relaxed local import in Paper D after identifying the
theorem interpolation parameter with `theta`.

## The `theta = 1/2` Contrapositive

Set `theta = 1/2`. If

```text
epsilon <= (1/(2k)) * (1 - n/q),
```

then

```text
Lst(C+,delta)
    <= ceil(2 q epsilon)
    <= ceil((q - n)/k)
    < q/k + 1.
```

Therefore any construction producing

```text
Lst(C+,delta) >= q/k + 1
```

forces

```text
eca(C,delta) = epsilon > (1/(2k)) * (1 - n/q).
```

The MCA lower bound then follows only through the separate local inequality
`eca(C,delta) <= emca(C,delta)`.

## General Constant Knob

For a sharper constant, set the theorem interpolation parameter to `1 - alpha`
with `alpha in (0,1]`. The implication becomes

```text
epsilon <= (1 - alpha) * (q - n)/(k q)
    implies
Lst(C+,delta) <= ceil(q epsilon/alpha).
```

The upper bound is then at most

```text
ceil((1 - alpha)(q - n)/(alpha k)) < q/(alpha k) + 1.
```

Thus a quotient-fiber lower bound of size at least `q/(alpha k) + 1` forces

```text
eca(C,delta) > (1 - alpha) * (1/k) * (1 - n/q).
```

This matches Paper D's remark that the `1/2` choice is a cleanliness choice,
not an algebraic barrier: the error constant can approach `1/k` if the fiber
lower bound has the extra `1/alpha` slack.

## Audit Impact

This discharges the constant-manipulation part of the A0 checklist, conditional
on the exact rational theorem interface. The following items remain external
source checks:

- whether the theorem uses normalized CA error probability or an unnormalized
  slope count;
- whether the admissible `delta` range is exactly the one used in Paper D;
- whether `C+` is precisely `RS[F,D,k+1]`;
- whether the result is stated over all finite fields or only prime fields;
- whether the theorem's inequality is strict or non-strict at the threshold;
- whether list size is the maximum over received words in the same ambient
  field used by the line experiment.

Small strictness differences do not change the displayed constants, but field,
normalization, radius, or augmented-code differences would require editing the
manuscript import before the cap can be treated as source-certified.
