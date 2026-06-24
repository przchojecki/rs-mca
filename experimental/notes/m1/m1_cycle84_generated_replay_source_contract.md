# M1 Cycle84 Generated Replay Source Contract

Status: AUDIT / GENERATED-CYCLE84-CXX-SOURCE-CONTRACT.

Date: 2026-06-24.

This note records a mechanical source contract for the generated C++ replay used
in the Cycle84 projected census. It sits between the algorithm audit and the
saved full replay receipt:

```text
algorithm audit
  -> generated source contract
  -> saved all-shards replay receipt
```

The contract is not a formal compiler proof. It verifies that the exact C++
source emitted for the recorded `--threads 16` run has the constants, table
payload, and source-level control-flow landmarks used by the algorithm audit.

## Source Identity

The generated source is produced by

```text
experimental/scripts/verify_m1_cycle84_projected_census_shard_replay.py
```

from the current `slot_logs.json` certificate. For the recorded full replay the
thread setting is:

```text
--threads 16
```

The expected generated source SHA256 is:

```text
555ba27f00378d88b9406d571f64dee74d355ca124ed2292421f6a8e973969c5
```

The source contract verifier checks this digest and rejects unresolved template
markers.

## Table Payload

The generated C++ contains two injected tables:

```text
LOGS[7][48]
COLORS[7][48]
```

The verifier parses both arrays back out of the generated C++ text and compares
them against the current projected-log certificate. Thus the replay source is
tied to the same `336` slot logs checked by

```text
python3 experimental/scripts/verify_m1_cycle84_projected_log_certificate.py
```

## Source-Level Contract

The verifier checks for source landmarks covering:

```text
tau involution and tau log/color guards;
the oriented half-domain k < tau(k);
the five-slot base table and two-slot tail split;
the color-complement bucket base[4-tail.color];
the fixed-root exclusion checks;
the 16,384-shard half-interval bounds;
the second circular-slice branch [M-hi+1,M-lo+1);
the canonical key min(z,M-z);
the in-shard canonical-key guard;
the duplicate-energy update energy += 2*old;
the OpenMP shard-parallel loop;
the JSON duplicate-bin output.
```

It also checks that these landmarks appear in the expected source order. This
does not replace the exact toy-model algorithm audit; it ties that audit to the
actual generated C++ source used by the recorded full replay.

## Reproducibility

Run:

```sh
python3 experimental/scripts/verify_m1_cycle84_generated_replay_source.py
python3 experimental/scripts/verify_m1_cycle84_generated_replay_source.py --json
```

The verifier is nonmutating. It does not compile or run C++; compilation and
execution are covered by the shard replay verifier and the saved full-replay
receipt.

## Remaining Boundary

For promotion beyond audit status, a reviewer still has to decide that this
source contract plus the algorithm audit is an acceptable substitute for manual
inspection of the generated C++ source. The contract makes that decision local:
the source is no longer an uninspected generated artifact.
