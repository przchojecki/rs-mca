# Monolithic moving-cell Sage replay: external Singular IPC deadlock

On 2026-08-01 the full eight-direct-cell compiler was first run in one Sage
process.  It completed substantial exact algebra but stopped making progress
while building a later parity localization.  Process inspection showed:

```text
Sage/Python: blocked in select(), waiting for the Singular prompt
Singular:    blocked in fgets(), waiting for new input
```

A one-second stack sample confirmed the reciprocal-read state.  Interrupting
the run produced Sage's external-interface restart traceback; no certificate
was emitted and no mathematical terminal was claimed from that run.

The individual hard cell `M01-R11` had already passed cleanly in a fresh
process.  The adopted repair therefore isolates every direct cell in a fresh
Sage/Singular process and assembles the final payload only after all eight
child payloads pass exact identity, terminal, order, and uniqueness checks.
The sharded full replay completed successfully.

This is an operational dead end, not evidence for or against the algebraic
closure statement.  Do not restore the monolithic full-cell execution path
without an explicit external-interface regression test.
