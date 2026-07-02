# E1 Row-C value-set sampling pilot

- **Status:** EXPERIMENTAL EVIDENCE / pre-registered pilot plus one
  birthday-pressure follow-up.  This is not a proof, threshold claim, or
  replacement for the full `sqrt(V)` run.
- **DAG node:** `e1_fullness`.
- **Queue item:** Fable evidence plan `E1`; execution queue `Q3.1
  [row_c_experiment]`.
- **Script:** `experimental/scripts/verify_row_c_e1_value_set_sampler.py`.
- **Artifacts:**
  `experimental/data/certificates/row-c-e1-sampling/row_c_e1_sampling_pilot.json`;
  `experimental/data/certificates/row-c-e1-sampling/row_c_e1_sampling_n64_2pow24_exact.json`.

## Object

Row C is the small-n probe

```text
n = 2^10,  rho = 1/2,  p = smallest prime > 2^250 with p = 1 mod 1024.
```

For a compatible quotient order `N' | n`, set `ell' = rho N' + 1`.
The sampled object is the Paper B quotient-exact slack-one value set

```text
{-e_1(B) mod p : B in binom(Q, ell')},
```

but sampled through its characteristic-zero antipodal class normal form.  With
`n1=N'/2`, an antipodal class is represented by `t` singleton pairs with signs
and `(ell'-t)/2` full antipodal pairs, where

```text
t == ell' mod 2,      0 <= t <= min(ell', N'-ell').
```

The number of such classes is

```text
A(N',ell') = sum_t binom(n1,t) 2^t.
```

The script samples these classes uniformly, reduces their `e_1` values modulo
`p`, and records duplicate-pair statistics.  This targets quotient-level
modular collisions directly; it deliberately does not sample raw subsets,
whose fibers over the same characteristic-zero value are non-uniform.

## Pre-registered interpretation

The committed pilot is intentionally small.  It should be read as a harness and
first sanity check; a later offline run should raise `--samples` toward the
birthday scale for `N'=64` before strong conclusions are drawn.

```text
density -> 1 / no collisions near birthday scale:
    e1_fullness prior up; the corridor lands near the quotient crossing and
    norm/amplification extensions deserve priority.

heavy collisions at some N':
    averaged_slope_conversion becomes load-bearing; inspect and package the
    collision structure as a grounded conjecture or counterexample packet.

mixed behavior by N':
    zone charts gain interval structure, with per-N' gates rather than one
    uniform fullness assertion.
```

If a run observes zero duplicate pairs among `S` samples, the script prints only
the standard birthday lower bound on the effective support at 95% confidence,

```text
S(S-1)/(2*(-log(0.05))).
```

That number is a lower bound on collision support, not an estimate of the full
value-set size.

## Compatibility correction

The Fable E1 sketch listed `N' in {64,96,128,192,256}`.  For Row C with
`n=2^10`, quotient orders must divide `n`, so the compatible cells in that list
are

```text
N' in {64,128,256}.
```

The non-dyadic cells `96` and `192` require a different row slate with a
3-factor in the domain order.  The JSON artifact records this explicitly rather
than silently dropping them.

## Pilot result

The committed deterministic pilot uses `262,144` class samples in each
compatible cell.  No duplicate pairs are observed in the default run.  This
rules out only
extreme collapse at the printed effective-support scale; it does not certify
fullness of the value set.

## Birthday-pressure follow-up

The second committed artifact uses exact canonical field values, not hashes, for

```text
N' = 64,   ell' = 33,   samples = 2^24.
```

It observes one duplicate pair.  Under the injective/full-value-set birthday
model the expected duplicate-pair count is about `0.156`, so the Poisson tail
for observing at least one duplicate is about `0.145`.  This is therefore
consistent with the fullness branch of the E1 interpretation table; it is not
evidence of a heavy-collision structure.  The run is still smaller than the
roadmap's suggested `2^25`--`2^26` decisive run, so the conservative conclusion
is only that no early heavy-collapse signal appeared.

## Reproduce

```bash
python3 experimental/scripts/verify_row_c_e1_value_set_sampler.py
python3 experimental/scripts/verify_row_c_e1_value_set_sampler.py --emit
python3 experimental/scripts/verify_row_c_e1_value_set_sampler.py \
  --orders 64 --samples 16777216 --mode exact-set --emit \
  --output experimental/data/certificates/row-c-e1-sampling/row_c_e1_sampling_n64_2pow24_exact.json
```
