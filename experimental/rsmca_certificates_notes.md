## Claim

Five finite statements from the AGENTS.md toy-case menu, formalized in
Lean 4 and kernel-certified: the x^4 = 1 solution count in F_17 (quotient
scale N=4); the psi_2 elementary-symmetric image cardinality (10) over the
order-4 subgroup {1, 4, 13, 16} of F_17*; two-square coverage of F_17;
the x^16 = 1 solution count (16) in the Fermat prime field F_257; and the
dyadic-dither window fact that r = 0 is the only r in [0,16) keeping
32 | (256 - r).

Scope: these formalize the OBJECT CLASSES the toy menu names as
self-contained statements. They are not formalizations of Paper A-D
internal definitions (locator fibers, quotient profiles, reserve ledgers);
that step needs per-statement adequacy audits against the tex and is
proposed as the follow-up.

## Status

PROVED (Lean 4 kernel, v4.30.0 + mathlib; axioms used: none; proof terms
closed; `sorry`-free by construction and by kernel introspection).

## Parameters

q = 17 (subgroup orders 4, 8), q = 257 (subgroup order 16),
dyadic n = 256 with dither window r in [0,16) and quotient order N = 32.

## Existing paper dependency

None used. Statements were ground-truthed by exhaustive enumeration
independently of Papers A-D, then formalized and kernel-checked.

## Proof idea or experiment

Formalization plus kernel decision procedures: four statements close by
`aesop`, the two-square coverage by `decide` (a 17^3 enumeration inside the
kernel). Statements were adequacy-audited before verification by two
independent LLM reviewers with an adversarial brief, disputes closed by a
recorded human verdict; two informal declarations were tightened during
review while the formal statements survived unchanged.

## Ledger impact

None of the reserve ledgers move. The contribution is infrastructural:
script-certificate-class claims upgraded to kernel-certified statements
with machine-readable provenance (see PROVENANCE.md), the direction PR
suggestion 9 asks to start small on.

## Constants

Exact and explicit in each statement: 4, 10, 17, 16, 257, {0}.

## Reproducibility

`experimental/lean-certificates/`: pinned toolchain and manifest;
`lake exe cache get && lake build`. PROVENANCE.md carries per-theorem proof
tactics, proof-term sizes, kernel heartbeat costs, and the adequacy-audit
event trail (hashed, replayable events; schema:
github.com/manifoldcontrol/verification-events).
