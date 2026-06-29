import RsMca.Basic

namespace RsMca

/-!
# Quotient-periodic support overlap: the whole-fiber strict-overlap reduction

Stdlib-only (`Nat`) formalization of the *size/threshold arithmetic* of the
PROVED note `notes/m1/m1_quotient_periodic_overlap_profile.md`.

Setup: a domain split into `N` disjoint fibers of size `m`.  A "whole-fiber"
support is a union of `L` fibers, so it has size `L*m`; two such supports that
differ by `h` exchanged fibers have set difference `|S \ T| = h*m` and
intersection `|S ∩ T| = (L-h)*m`.

At agreement size `s = k+t`, the strict M1 high-overlap range is `|S ∩ T| > k`,
i.e. `|S \ T| < t`.  Since every whole-fiber exchange has `|S \ T| = h*m` with
`h ≥ 1`, the note's reduction is pure `Nat` arithmetic:

* `strict_overlap_iff`: strict overlap `|S∩T| > k` is exactly `|S\T| < t`;
* `no_strict_when_t_le_m` / `not_strict_when_t_le_m`: **no strict high-overlap
  pairs when `t ≤ m`** (note lines 68-70);
* `strict_needs_t_gt_fiber`: the first nonzero correction needs `t ≥ m+1`;
* `first_band_unique`: in the first active band `m < t ≤ 2m` only `h = 1` is
  strict (note lines 102-107);
* `active_scale_iff`: an exchange scale `h` is strict-active iff
  `h ≤ ⌊(t-1)/m⌋`, so the active-scale count is `⌊(t-1)/m⌋` (note lines 91-99);
* `fiberSize_dvd_support`: a whole-fiber family is empty at any agreement size
  `s` with `¬ (m ∣ s)`.

The binomial COUNT identities (`|A_QP| = C(N,L)`, the Johnson exchange profile
`Δ_{hm} = C(N,L) C(L,h) C(N-L,h)`) are the note's combinatorial content and need
`Mathlib`-level finite-set reasoning; they are not reproved here.  This file
certifies the size/threshold arithmetic that the M1 reduction actually consumes.
-/

/-- A whole-fiber quotient-periodic configuration: `numFibers` fibers each of
    size `fiberSize`, with `selected` of them chosen for the support. -/
structure WholeFiberConfig where
  fiberSize : Nat       -- m
  numFibers : Nat       -- N
  selected : Nat        -- L
  selected_le : selected ≤ numFibers
  deriving Repr

namespace WholeFiberConfig

variable (p : WholeFiberConfig)

/-- Domain size `N*m`. -/
def domainSize : Nat := p.numFibers * p.fiberSize

/-- Whole-fiber support size `s = L*m`. -/
def supportSize : Nat := p.selected * p.fiberSize

/-- Set difference `|S \ T| = h*m` when `h` fibers are exchanged. -/
def exchangeSize (h : Nat) : Nat := h * p.fiberSize

/-- Intersection `|S ∩ T| = (L-h)*m` when `h ≤ L` fibers are exchanged. -/
def intersectionSize (h : Nat) : Nat := (p.selected - h) * p.fiberSize

/-- Every exchange size is a multiple of the fiber size (`Δ_j = 0` unless `m ∣ j`). -/
theorem fiberSize_dvd_exchange (h : Nat) : p.fiberSize ∣ p.exchangeSize h :=
  ⟨h, by rw [exchangeSize, Nat.mul_comm]⟩

/-- The support size is a multiple of the fiber size; so a whole-fiber family is
    empty at any agreement size `s` with `¬ (m ∣ s)`. -/
theorem fiberSize_dvd_support : p.fiberSize ∣ p.supportSize :=
  ⟨p.selected, by rw [supportSize, Nat.mul_comm]⟩

/-- Intersection plus difference recovers the support size (`|S∩T| + |S\T| = |S|`). -/
theorem intersection_add_exchange (h : Nat) (hh : h ≤ p.selected) :
    p.intersectionSize h + p.exchangeSize h = p.supportSize := by
  unfold intersectionSize exchangeSize supportSize
  rw [← Nat.add_mul, Nat.sub_add_cancel hh]

/-- `|S ∩ T| = s - |S \ T| = (L-h)*m`, the note's intersection identity. -/
theorem intersection_eq_support_sub_exchange (h : Nat) (hh : h ≤ p.selected) :
    p.intersectionSize h = p.supportSize - p.exchangeSize h := by
  have := p.intersection_add_exchange h hh
  omega

/-- Strict M1 high-overlap (`|S∩T| > k`) is exactly `|S\T| < t`, at agreement
    size `s = k + t`.  (Note lines 60-61.) -/
theorem strict_overlap_iff (h k t : Nat) (hh : h ≤ p.selected)
    (hs : p.supportSize = k + t) :
    k < p.intersectionSize h ↔ p.exchangeSize h < t := by
  have hadd := p.intersection_add_exchange h hh
  omega

/-- No strict high-overlap pairs when `t ≤ m`: every whole-fiber exchange has
    `|S\T| = h*m ≥ m ≥ t` for `h ≥ 1`.  (Note lines 68-70.) -/
theorem no_strict_when_t_le_m (h t : Nat) (hh : 1 ≤ h) (ht : t ≤ p.fiberSize) :
    t ≤ p.exchangeSize h := by
  unfold exchangeSize
  calc t ≤ p.fiberSize := ht
    _ = 1 * p.fiberSize := (Nat.one_mul _).symm
    _ ≤ h * p.fiberSize := Nat.mul_le_mul hh (Nat.le_refl _)

/-- Equivalent predicate form: when `t ≤ m`, no whole-fiber exchange (`h ≥ 1`)
    lies in the strict range `< t`. -/
theorem not_strict_when_t_le_m (h t : Nat) (hh : 1 ≤ h) (ht : t ≤ p.fiberSize) :
    ¬ p.exchangeSize h < t := by
  have := p.no_strict_when_t_le_m h t hh ht
  omega

/-- The first nonzero strict-overlap correction needs `t ≥ m+1`: any exchange in
    the strict range forces `m < t`.  (Note lines 102-103.) -/
theorem strict_needs_t_gt_fiber (h t : Nat) (hh : 1 ≤ h)
    (hstrict : p.exchangeSize h < t) : p.fiberSize < t := by
  have hle : p.fiberSize ≤ p.exchangeSize h := by
    unfold exchangeSize
    calc p.fiberSize = 1 * p.fiberSize := (Nat.one_mul _).symm
      _ ≤ h * p.fiberSize := Nat.mul_le_mul hh (Nat.le_refl _)
  omega

/-- In the first active band `m < t ≤ 2m`, only the single-fiber exchange `h = 1`
    can be strict.  (Note lines 102-107.) -/
theorem first_band_unique (h t : Nat) (hh : 1 ≤ h)
    (hstrict : p.exchangeSize h < t) (_hlo : p.fiberSize < t)
    (hhi : t ≤ 2 * p.fiberSize) : h = 1 := by
  unfold exchangeSize at hstrict
  rcases Nat.lt_or_ge h 2 with h2 | h2
  · omega
  · exfalso
    have : 2 * p.fiberSize ≤ h * p.fiberSize := Nat.mul_le_mul h2 (Nat.le_refl _)
    omega

/-- An exchange scale `h` is strict-active (`h*m ≤ t-1`) iff `h ≤ ⌊(t-1)/m⌋`; so
    the number of active scales is `⌊(t-1)/m⌋`.  (Note lines 91-99.) -/
theorem active_scale_iff (h t : Nat) (hm : 0 < p.fiberSize) :
    h ≤ (t - 1) / p.fiberSize ↔ p.exchangeSize h ≤ t - 1 := by
  unfold exchangeSize
  exact Nat.le_div_iff_mul_le hm

end WholeFiberConfig

end RsMca
