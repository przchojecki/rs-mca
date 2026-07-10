/-!
# Map-smooth fiber + collision-aware cap (W41-FIX M2, path B)

Serves **K4* petal kernel** (map-smooth is the petal entry machinery).

FIX: dropped fabricated `thm:fiber-to-slope` (no such label in frontiers).
Rebuilt as a faithful instance of the real proved statements:

Source labels (frontiers draft):
- lem:map-smooth-fiber (L2741): ℓ=⌊k/a⌋+2, A=aℓ, if ℓ≤N−1 then a list of
  size ≥ binom(N,ℓ)/|B| codewords agrees on ≥ A positions; and
  k+a+1 ≤ A ≤ k+2a (equality A=k+2a if a∣k)
- prop:map-smooth-cap (L2764): with L=⌈binom(N,ℓ)/|B|⌉,
  B_MCA(m) ≥ ⌈ L(q−n) / (q−n + k(L−1)) ⌉ for k+1 ≤ m ≤ A

Explicit integer toy (a∣k so A equals k+2a):
- a=2, k=2, N=4 (so n=a·N=8 for complete a-fibers), ℓ=⌊2/2⌋+2=3
- ℓ≤N−1: 3≤3 OK
- A=a·ℓ=6
- k+a+1=5 ≤ A=6 ≤ k+2a=6, and A=k+2a since a∣k
- |B|=2: L=⌈C(4,3)/2⌉=⌈4/2⌉=2
- Cap: q−n=2, L=2, k=2 → L(q−n)/(q−n+k(L−1))=4/(2+2)=1 exact

No `sorry`. No mathlib. Dual `native_decide` / `decide`.
-/

namespace PetalFiber

-- Serves K4* petal kernel (path B: lem:map-smooth-fiber + prop:map-smooth-cap).

def binom : Nat → Nat → Nat
  | _, 0 => 1
  | 0, _ + 1 => 0
  | n + 1, k + 1 => binom n (k + 1) + binom n k

/-- Ceil division ⌈num/den⌉ for den > 0. -/
def ceilDiv (num den : Nat) : Nat := (num + den - 1) / den

/-! ## Map-smooth parameters (lem:map-smooth-fiber) -/

def a : Nat := 2
def k : Nat := 2
def Nq : Nat := 4
def n : Nat := a * Nq
def Bsize : Nat := 2

def ell : Nat := k / a + 2
def Aagree : Nat := a * ell

theorem ell_value : ell = 3 := by native_decide
theorem n_value : n = 8 := by native_decide
theorem Aagree_value : Aagree = 6 := by native_decide

/-- Side condition ℓ ≤ N−1. -/
theorem ell_le_N_minus_1 : ell ≤ Nq - 1 := by native_decide

/-- Agreement window: k+a+1 ≤ A ≤ k+2a. -/
theorem A_lower : k + a + 1 ≤ Aagree := by native_decide
theorem A_upper : Aagree ≤ k + 2 * a := by native_decide

/-- Equality case a ∣ k ⇒ A = k+2a. -/
theorem a_divides_k : k % a = 0 := by native_decide
theorem A_eq_k_plus_2a : Aagree = k + 2 * a := by native_decide

/-! ## List size L = ⌈binom(N,ℓ)/|B|⌉ -/

def Llist : Nat := ceilDiv (binom Nq ell) Bsize

theorem binom_4_3 : binom 4 3 = 4 := by native_decide
theorem Llist_value : Llist = 2 := by native_decide
theorem Llist_exact_div : binom Nq ell / Bsize = 2 := by native_decide

/-- Lemma conclusion shape: list size lower bound is Llist. -/
theorem list_size_lower : Llist ≥ 1 := by native_decide

/-! ## prop:map-smooth-cap lower bound (exact integer) -/

def qMinusN : Nat := 2
def capNum : Nat := Llist * qMinusN
def capDen : Nat := qMinusN + k * (Llist - 1)
def capExact : Nat := capNum / capDen
def capCeil : Nat := ceilDiv capNum capDen

theorem capDen_value : capDen = 4 := by native_decide
theorem capNum_value : capNum = 4 := by native_decide
theorem cap_divides : capNum = capExact * capDen := by native_decide
theorem capExact_value : capExact = 1 := by native_decide
theorem capCeil_eq_exact : capCeil = capExact := by native_decide

/-- Main cap instance: B_MCA ≥ 1 on this toy. -/
theorem map_smooth_cap_instance : capExact = 1 := by native_decide
theorem map_smooth_cap_pos : capExact ≥ 1 := by native_decide

/-- Threshold range nonempty: k+1 ≤ m ≤ A with m=k+1. -/
def mThresh : Nat := k + 1
theorem m_ge_k_plus_1 : k + 1 ≤ mThresh := by native_decide
theorem m_le_A : mThresh ≤ Aagree := by native_decide

/-! ## Dual via `decide` -/

theorem ell_value' : ell = 3 := by decide
theorem A_eq_k_plus_2a' : Aagree = k + 2 * a := by decide
theorem ell_le_N_minus_1' : ell ≤ Nq - 1 := by decide
theorem Llist_value' : Llist = 2 := by decide
theorem capExact_value' : capExact = 1 := by decide
theorem A_lower' : k + a + 1 ≤ Aagree := by decide
theorem A_upper' : Aagree ≤ k + 2 * a := by decide

end PetalFiber
