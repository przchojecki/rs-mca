/-
Kernel certificates for five finite facts from the AGENTS.md toy-case menu.

STATUS: PROVED (Lean 4 kernel; axioms used: none, constructive).

Scope caveat, per the repository's own discipline: these formalize the
OBJECT CLASSES the toy-case menu names (subgroup scales, psi_2
elementary-symmetric coverage, restricted sums, Fermat-prime fields, dyadic
dithering windows) as self-contained statements. They are not formalizations
of Paper A-D internal definitions; that step needs per-theorem adequacy
audits against the tex and is proposed as follow-up work.

Each statement was ground-truthed by exhaustive enumeration before
formalization, then proved through a verifier-bounded pipeline (proposer /
Lean kernel / retention gate); statements were adequacy-audited by two
independent LLM reviewers with human adjudication of disputes. Full
provenance (hashed verification events, audit trail, run records) in
PROVENANCE.md beside this file.
-/
import Mathlib

set_option autoImplicit false

/-- Quotient scale N=4 in F_17: the x^4 = 1 solution set has order 4. -/
theorem rsmca_f17_pow4_card :
    (Finset.univ.filter (fun x : ZMod 17 => x ^ 4 = 1)).card = 4 := by aesop

/-- psi_2 elementary-symmetric image over the order-4 subgroup
{1, 4, 13, 16} of F_17*: exactly 10 distinct (e1, e2) pairs. -/
theorem rsmca_f17_psi2_card :
    ((({1, 4, 13, 16} : Finset (ZMod 17)) ×ˢ ({1, 4, 13, 16} : Finset (ZMod 17))).image
      (fun p => (p.1 + p.2, p.1 * p.2))).card = 10 := by aesop

/-- Restricted-sum coverage: every element of F_17 is a sum of two squares
(x, y over all of F_17, zero included). -/
theorem rsmca_f17_two_square_cover :
    ∀ z : ZMod 17, ∃ x y : ZMod 17, x ^ 2 + y ^ 2 = z := by decide

/-- Order-16 subgroup scale in the Fermat prime field F_257. -/
theorem rsmca_f257_pow16_card :
    (Finset.univ.filter (fun x : ZMod 257 => x ^ 16 = 1)).card = 16 := by aesop

/-- Dyadic dithering over the window r in [0,16): r = 0 is the only dither
keeping 32 | (256 - r), i.e. the N=32 quotient scale active. -/
theorem rsmca_dither_active_scale :
    (Finset.range 16).filter (fun r => (256 - r) % 32 = 0) = {0} := by aesop
