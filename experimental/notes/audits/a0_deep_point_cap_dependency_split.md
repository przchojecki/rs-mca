# A0 Deep-Point Cap Dependency Split

## Status

PROVED local algebra / CONDITIONAL on existing local X1 lemmas.

This note records the A0 dependency split created by the X1 deep-point route.
It does not certify the external Crites--Stewart theorem.  Instead it isolates
which part of Paper D's universal cap no longer needs that import.

## Claim

Assume the local ingredients already recorded in the X1 notes:

1. `lem:fiber(ii)` gives a word in `C+ = RS[F,D,k+1]` with a list of size
   `L` at the Paper D cap radius.
2. The simple-pole deep-point identity turns the deep image of that list into
   support-wise MCA-bad slopes for `C=RS[F,D,k]`.
3. Averaging over deep points gives a line with at least

```text
M >= L / (1 + k(L-1)/(q-n))
```

bad slopes, where `q=|F|` and `n=|D|`.

Then the Paper D hypothesis

```text
L >= q/k + 1
```

implies the same MCA cap constant as `thm:main`:

```text
emca(C,delta) >= M/q >= (1/(2k)) (1 - n/q).
```

Thus the headline MCA cap has a CS25-free route once the local deep-point
identity and `lem:fiber(ii)` are accepted.  The original CS25/ABF import still
needs source verification for the original CA-to-list proof, the Paper B import
surface, and any statement that explicitly cites the imported theorem.

## Algebra

The desired comparison is

```text
L(q-n) / ( q(q-n+k(L-1)) ) >= (q-n)/(2kq).
```

Since `q>n`, this is equivalent to

```text
2kL >= q-n+k(L-1),
```

or

```text
kL - q + n + k >= 0.
```

The Paper D fiber hypothesis `L >= q/k+1` gives `kL >= q+k`, so the last
quantity is at least `n+2k`, hence positive.  This proves the local cap
constant directly from the deep-point construction.

## Dependency Consequence

The A0 status should therefore be split:

- **Original CS25 route:** still conditional until the external theorem is
  checked against the Paper D restatement.
- **Headline MCA cap route:** no longer needs CS25 as a load-bearing theorem;
  it can use `lem:fiber(ii)`, the deep-point identity, and the algebra above.
- **Promotion caveat:** Papers A--D should not be edited from this note alone.
  A human review should first check the local X1 identity, the `lem:fiber(ii)`
  proof, and notation compatibility with Paper D.

## Verifier

Run from the repository root:

```sh
python3 experimental/scripts/verify_a0_deep_point_cap_algebra.py
python3 experimental/scripts/verify_a0_deep_point_cap_algebra.py --json
```

The verifier checks the exact rational inequality on a grid of finite
parameters and records the symbolic residual
`kL-q+n+k` controlling the comparison.
