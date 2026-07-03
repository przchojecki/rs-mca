# Hankel-Kernel Coset-Pattern Census

- **Status:** EXPERIMENTAL / COUNTEREXAMPLE.
- **Agent:** Codex acting autonomously for Allen Graham Hart.
- **Roadmap link:** Fable evidence task `E17` / `QF.14`
  (`f_termination_hankel` / `f_descent_termination`).
- **Verifier:** `experimental/scripts/verify_hankel_kernel_coset_census.py`.
- **Artifact:** `experimental/data/certificates/hankel-kernel-coset-census/hankel_kernel_coset_census_f17_n16.json`.

This packet tests the E17 prediction that sparse-dual-word supports of
Hankel-kernel flats are always unions of nontrivial multiplicative cosets.  It
does not prove a general theorem.  It gives a small replayable failure branch
for the divisor-poset-only termination picture.

## Object

Let `K = F_17`, let `H = F_17^*`, and write `H = <3>` with exponents
`0..15`.  For a degree `j` and a full-rank `t x (j+1)` Hankel rowspace
`R`, a support `S subset H` is counted as an exact sparse dual support when

```text
R cap span{ (1,x,x^2,...,x^j) : x in S } != 0
```

and the corresponding linear combination has every coefficient on `S`
nonzero.  Thus the census records exact supports, not zero-coefficient
supersets.

The verifier tests support sizes `1,2,3` in three deterministic sampled
Hankel cases:

| case | accepted full-rank rowspaces | non-coset exact supports | nontrivial coset-union supports | singleton supports |
| --- | ---: | ---: | ---: | ---: |
| `j=3,t=2` kernel lines | 128 | 60975 | 53 | 11 |
| `j=4,t=2` kernel planes | 256 | 7134 | 6 | 1 |
| `j=5,t=3` kernel planes | 512 | 14312 | 16 | 0 |

In the E7-style `j=5,t=3` case, `511/512` sampled rowspaces have at least one
non-coset exact support of size at most `3`.  The minimum non-coset support
size is already `2`.

## Explicit Counterexample

The certificate records this `j=5,t=3` Hankel rowspace:

```text
r0 = ( 6, 12,  9, 10,  7,  3)
r1 = (12,  9, 10,  7,  3, 15)
r2 = ( 9, 10,  7,  3, 15, 15)
```

The exact support is the pair with exponents `{2,3}`, i.e. values `{9,10}`.
The relation is

```text
5 r0 + 6 r1 + 15 r2
  = 15 ev(9) + ev(10)
  = (16, 9, 6, 1, 6, 7)           mod 17.
```

Both support coefficients are nonzero, so the support is exactly `{9,10}`.
For a two-point support in the cyclic group of order `16`, the only possible
nontrivial coset union is an order-`2` coset pair, whose exponents differ by
`8`.  The exponents `2` and `3` differ by `1`, so this support is not a
nontrivial coset union.

## Interpretation

The pre-registered E17 verdict is the failure branch:

```text
NONCOSET_SPARSE_SUPPORT_FOUND__COSET_UNION_PREDICTION_FALSE
```

Consequently `QF.14` should not rely on a divisor-poset-only support lattice
for general Hankel-kernel flats.  The descent termination route should use the
general sparse-support lattice accounting unless an added hypothesis excludes
these supports, for example by restricting to a top-rich or primitive-twin
subfamily.

Non-claims:

- no theorem about all Hankel kernels;
- no exhaustive enumeration of all syndrome sequences or rowspaces;
- no support-size scan beyond `3`;
- singletons are recorded as common-root/tangent supports, not as coset-union
  failures.

## Replay

```bash
python3 experimental/scripts/verify_hankel_kernel_coset_census.py
python3 experimental/scripts/verify_hankel_kernel_coset_census.py --emit
python3 experimental/scripts/verify_hankel_kernel_coset_census.py --check experimental/data/certificates/hankel-kernel-coset-census/hankel_kernel_coset_census_f17_n16.json
python3 -m py_compile experimental/scripts/verify_hankel_kernel_coset_census.py
```
