---
workboard_item: MCA
row: any RS[F_q, D, k]
object: MCA
direct_statement: Import of Haboeck ePrint 2025/2110 Theorem 2: the quadratic Johnson-range support-wise MCA bound |E_m| <= (ell_m^7/3)(rho n)^2.
status: PROVED (published theorem import; statement and proof audit)
impact: SUPPLIER
quantifier: every received pair over any finite field; pair-unexplained finite affine slopes at agreement >= (1-gamma_m)n
falsifier: a received pair and m >= 3 with more than (ell_m^7/3)(rho n)^2 pair-unexplained slopes at the stated radius
replay: python3 background/nodes/haboeck_quadratic_johnson_mca_import/verify.py at https://github.com/AllenGrahamHart/rs-mca-prize-dag @ 4e77e95b3acf
---

# Haboeck quadratic Johnson-range MCA theorem, imported

Source: Ulrich Haboeck, *A note on mutual correlated agreement for
Reed-Solomon codes*, IACR ePrint 2025/2110, Theorem 2 — the [Hab25] of
this repository's own `open-proximity.tex` bibliography, i.e. the public
proof of the mechanism BCHKS25 Thm 4.6 attributes to personal
communication. The unproved BCHKS25 linear-in-n refinement is EXPLICITLY
EXCLUDED from the import.

Audit chain: (i) this repository's own
`experimental/notes/audits/audit_bchks25_thm46_conditional_johnson_import.md`
@ 93fba1be — whose "resolved one level further" section records the
independent proof audit of ePrint 2025/2110 Thm 2 (external trail:
github.com/latifkasuli/mca, section "Hab25 proof audit"); (ii) a
28-attack adversarial certification of the import chain in the campaign
repo (object identity vs the support-wise MCA-bad predicate: word-for-word
match, same support, same conjunction; convention d = k-1 shown
load-bearing — rho = k/n would make the specialized thresholds unsafe by
exactly 1; both roundings safe-direction; full ladder m = 3..96 re-derived
from (HJ1) alone; field-general, no subfield/primality hypothesis).
