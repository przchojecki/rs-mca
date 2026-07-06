# PROVENANCE: five kernel certificates from the toy-case menu

Produced by a verifier-bounded proof pipeline (MathSolver MVP): proposer ->
Lean 4 kernel (sole authority on correctness) -> typed failure ledger ->
retention gate (sole authority on retention), with every verification act
recorded as a hashed, replayable event. Event schema:
https://github.com/manifoldcontrol/verification-events. Proof-term
introspection: https://github.com/manifoldcontrol/lean-introspect.

Toolchain: leanprover/lean4:v4.30.0, mathlib rev c5ea0035 (pinned in the
accompanying lakefile/manifest). Run: run_1783357387 (2026-07-05), 57-theorem
corpus, 47/47 expected outcomes on graded bands, zero verifier errors.
Ground truth for each statement below was established by exhaustive
enumeration before formalization. Statements were adequacy-audited by two
independent LLM reviewers (deepseek-v4-pro auditor, gpt-5.5 judge, verdicts
recorded as parent-linked events) with human adjudication closing disputes.

| theorem | tactic | proof term | heartbeats | axioms | adequacy |
|---|---|---|---|---|---|
| rsmca_f17_pow4_card | `by aesop` | closed, 541 nodes | 27430702 | none (constructive) | audited |
| rsmca_f17_psi2_card | `by aesop` | closed, 1952 nodes | 27558894 | none (constructive) | audited |
| rsmca_f17_two_square_cover | `by decide` | closed, 4245 nodes | 27449930 | none (constructive) | audited |
| rsmca_f257_pow16_card | `by aesop` | closed, 541 nodes | 27430736 | none (constructive) | audited |
| rsmca_dither_active_scale | `by aesop` | closed, 149 nodes | 27606545 | none (constructive) | audited |

Heartbeat note: costs are per-file and dominated by `import Mathlib`
elaboration (~27.4M); marginal proof cost is the small residual between rows.

## Adequacy audit trail (event ids in the pipeline's canonical log)

- **rsmca_f17_pow4_card**: ve_2f6c74c128dc=audited(llm[deepseek/deepseek-v4-pro]); ve_201e3f466bc6=audited(llm[openai/gpt-5.5])
- **rsmca_f17_psi2_card**: ve_a308d4332556=audited(llm[deepseek/deepseek-v4-pro]); ve_7bc74e87e8c1=audited(llm[openai/gpt-5.5]); ve_1ba41308be86=mismatch(llm[deepseek/deepseek-v4-pro]); ve_a5ff4cb37359=audited(james)
- **rsmca_f17_two_square_cover**: ve_e94032379e02=audited(llm[deepseek/deepseek-v4-pro]); ve_88c3afbc46e5=audited(llm[openai/gpt-5.5]); ve_b6865a6131dd=mismatch(llm[deepseek/deepseek-v4-pro]); ve_44f71742e934=audited(james)
- **rsmca_f257_pow16_card**: ve_fb6fd957924b=audited(llm[deepseek/deepseek-v4-pro]); ve_cbc2824fd021=audited(llm[openai/gpt-5.5])
- **rsmca_dither_active_scale**: ve_04340e4d14da=mismatch(llm[deepseek/deepseek-v4-pro]); ve_57f9af83bbaa=mismatch(llm[openai/gpt-5.5]); ve_6e8deffec2ff=audited(llm[deepseek/deepseek-v4-pro]); ve_4da682a67a23=audited(llm[openai/gpt-5.5]); ve_6b2d69f48c7e=audited(james)

The audit sequence per theorem reads chronologically: adversarial auditor
verdict, judge verdict (parent-linked), and where the pair disagreed, a
recorded human closure. Two statements' informal declarations were corrected
during review (domain qualification; an index-window qualification); the
formal statements were verified unchanged throughout.

## Reproduce

```
cd experimental/lean-certificates
lake exe cache get
lake build
```
