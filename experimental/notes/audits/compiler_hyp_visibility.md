# Compiler-hypothesis visibility audit

## Status
EXPERIMENTAL / AUDIT. **Verdict: CLEAN.**

Hard inputs: (b) Sidon/MI-MA, (c) ray compiler, (d) profile-envelope.
Strategy: agents.md #2 — every conditional compiler input visible or cited
in theorem statements. Weave #523/#530.

## Dual routes
- generator: parse thm/prop/cor envs; statement-vs-proof token match; resolve
  defined terms (closed-ledger L3, admissible A4/A6/A7); curated second pass
- checker: independent statement-window re-read + resolve defined terms to
  definition clauses; require SILENT=0 and main-ledger CITED via L3

## Compiler registry (C)

| ID | Label | Line | Hard input |
|----|-------|------|------------|
| RC | hyp:ray-compiler / eq:ray-compiler | L6033 / L6051 | (c) |
| SIDON_A4 | def:admissible-sequence (A4) + def:sidon-paid-cell | L896 / L5130 | (b) |
| ENVELOPE_A7 | def:admissible-sequence (A7) + eq:profile-envelope | L896 / L862 | (d) |
| CLOSED L3 | def:closed-asymptotic-ledger (L3) distinct-ray compiler | L1097 / L1111-1114 | (c) |

Paste:
```
6033:\begin{hypothesis}[Ray compiler]\label{hyp:ray-compiler}
6051: \tag{RC}\label{eq:ray-compiler}
896:\label{def:admissible-sequence}
1097:\label{def:closed-asymptotic-ledger}
1125:\begin{theorem}[Compiler for closed ledgers]\label{thm:main-ledger}
```

## Primary table (curated)

| Result | Compiler | Visibility | Definition clause that discharges |
|--------|----------|------------|-----------------------------------|
| prop:q-implies-sp L6059 | RC | **VISIBLE** | statement names (RC) explicitly |
| thm:q-sp-to-mca-final L6902 | RC | **VISIBLE** | statement names (RC) |
| thm:main-smooth-circle L957 | A4+RC+A7 | **CITED** | ledger-admissible → A4/A6/A7 |
| prop:primitive-residual-numerator L6073 | RC | **CITED** | ledger-admissible → (A6) RC |
| prop:numerator-bound L6084 | A4+RC | **CITED** | ledger-admissible → (A4)+(A6) |
| thm:intro-asymptotic-rs-mca L989 | envelope | **VISIBLE** | "profile-envelope budget is safe" |
| thm:exact-finite-profile-compiler L6737 | RC form | **VISIBLE** | inlines H,J incidence |
| thm:primitive-to-q-final L6890 | Sidon | **VISIBLE** | Sidon moment hypotheses named |
| cor:frontier-final L6913 | RC+envelope | **CITED** | envelope + q-sp-to-mca-final names RC |
| thm:main-ledger L1125 | RC | **CITED** | **closed asymptotic ledger** = def L1097 **(L3)** requires distinct-ray compiler |

## Verdict: CLEAN

Every audited conditional compiler input is **surfaced or cited**:
- **RC** via explicit (RC) in statements, or **closed-ledger (L3)**, or **ledger-admissible (A6)**
- **Sidon/MI-MA** via explicit Sidon hyp or **ledger-admissible (A4)**
- **Envelope** via explicit budget language or **ledger-admissible (A7)**

W48 initial SILENT call on thm:main-ledger was a **false positive**: the hypothesis
term "closed asymptotic ledger" already includes the ray compiler in def clause (L3).
Token heuristics must resolve defined terms before claiming SILENT.

## Reproducibility
```
py -3.13 experimental/scripts/verify_compiler_hyp_visibility.py --emit-defaults
py -3.13 experimental/scripts/verify_compiler_hyp_visibility.py --check
py -3.13 experimental/scripts/verify_compiler_hyp_visibility_check.py --check
```

## Nonclaims
Does not prove the ray compiler; visibility verification only.
