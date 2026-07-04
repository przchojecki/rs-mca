# F2/E37: moment-trade census, first large-prime threshold

- **DAG node:** `x4b_moment_trade_exclusion`.
- **Task:** F2 / E37.
- **Status:** EVIDENCE.  U2 survives the checked bands; this is not a proof.
- **Verifier:** `experimental/scripts/verify_f2_moment_trade_census.py`.

## Scope

The scan searches for primitive 0/1 dual words on `mu_n` with `t=3` leading
zero syndromes:

```text
sum_{e in E} zeta^(r e) = 0,      r = 1,2,3.
```

The exact MITM band is capped at

```text
b = 4,5,6,7,8.
```

The full F2 spec asks for `b in (t,2t+4] = 4..10`; the `b=9,10` bands are
left unscanned here because they require the `n=64`, `h=5` half-table.  This
keeps the PR within the machine's RAM budget.

The primitive filter removes blocks with nontrivial rotational or reflection
stabilizer, i.e. the quotient/dihedral paid sector.

## Results

Known witness replay:

```text
n=64, p=193, zeta=11,
E={0,1,2,4,16,45,50,60}
```

has zero syndromes for `r=1,2,3`, nonzero power sum at `r=4`, and trivial
dihedral stabilizer.

Threshold scan at `n=64`, `t=3`, `b=8`, first ten primes `p == 1 mod 64`:

```text
primitive hits: p=193, 257, 577
first later no-hit prime: p=641
no primitive b=8 hit in the checked primes p=641..1601
```

Representative rows for `n in {16,32,64}` at scales near `n`, `n^2`, `n^3`,
and `2^61` were scanned for every `b=4..8`.  No representative row at scale
`n^2` or above had a primitive block.  All zero-syndrome blocks found there
were quotient/dihedral-structured.

Adversarial exponent-pattern scan:

```text
arithmetic progressions, b=4..8
```

found no primitive zero-syndrome hits on the representative rows.  In prime
fields there is no proper subfield-supported construction; prime-power
subfield rows remain a separate construction check.

## Interpretation

This supports the large-prime U2 direction: primitive moment trades appear in
the small-prime edge of the `n=64` toy row, but disappear in the checked
large-prime bands.  The observed primitive range is below

```text
log(p)/log(n) < 1.56
```

for the checked `n=64,b=8` threshold row, while representative scales
`n^2`, `n^3`, and `2^61` are clean through `b=8`.

The remaining F2 work is exactly named:

```text
F2-large-band: complete or certify b=9,10, and replace the finite evidence
with a Weil/character-sum exclusion theorem for official rows.
```

## Verification

Run:

```bash
python3 experimental/scripts/verify_f2_moment_trade_census.py
```

The run is CPU-only and processes one prime at a time; the peak table is the
`n=64,h=4` half-table.
