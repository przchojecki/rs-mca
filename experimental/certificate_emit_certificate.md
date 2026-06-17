# Certificate Emitter Certificate

- **Status:** PROVED
- **Agent/model:** Codex acting autonomously through AllenGrahamHart
- **Script:** `experimental/certificate_emit.py`
- **Date:** 2026-06-17

## Purpose

This note records a deterministic smoke test for the planned
`experimental/certificate_emit.py` utility. The emitter consumes a JSON object using
the `agents.md` script-output fields and renders a reviewable Markdown or TeX
certificate.

## Reproduction

```sh
python3 experimental/certificate_emit.py \
  --input experimental/certificate_emit_example.json \
  --format markdown \
  --output /tmp/certificate_emit_example.md
```

The checked output should match `experimental/certificate_emit_example.md`.

## Scope

This emitter is intentionally schema-light. It does not validate the Paper C
reserve-certificate schema from the open schema PR; it only formats script
outputs that already contain the standard fields:

```text
input_parameters
mathematical_object
result
proof_certificate
theorem_or_problem
status
```
