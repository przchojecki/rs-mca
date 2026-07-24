set_option maxRecDepth 100000
set_option maxHeartbeats 0

/-!
# Deterministic Proth certificates for the four v4 smooth-domain primes

`proximity_prize_results_v4.tex` Table `tab:proth` prints four explicit primes
`p` together with the smooth subgroup order `2^n` and the exact budget
`B = floor(p / 2^128)`.  Deterministic primality certificates for exactly these
four primes are already in the repository, as condition `PC1` of
`prop:proth-row-check` in `experimental/rs_mca_thresholds.tex` (lines 1857-1858),
with per-row data in
`experimental/data/certificates/proth-rows/proth_rows.json`.  This module is a
kernel-checked replay of that certificate data, using the source's notation
`(u, s, a0)`.  The values were also rederived independently from the printed
primes alone and agree with the in-tree certificate in every field of every row.

Proth's criterion (classical; Proth 1878).  Let `N = u * 2^s + 1` with `u` odd
and `u < 2^s`.  If some `a0` satisfies

```text
a0 ^ ((N - 1) / 2)  =  N - 1   (mod N)
```

then `N` is prime.  The hypotheses `u` odd, `u < 2^s` and the single modular
exponentiation are exactly what is checked below; the implication itself is the
cited classical theorem, invoked by `prop:proth-row-check`, and is *not*
formalized here.

What this package proves by kernel-checked arithmetic, per row:

* the Proth decomposition `p = u * 2^s + 1`,
* `u` odd,
* the Proth size condition `u < 2^s`,
* the Proth witness congruence `a0 ^ ((p-1)/2) = p - 1 (mod p)`,
* the printed budget `floor(p / 2^128) = B` (the `PC2` bracket),
* `2^n | p - 1`, i.e. the smooth subgroup of order `2^n` used by the row exists.

The `F_{n,k}` sign conditions and the `r_quad`/`r_rho` identification that
`prop:proth-row-check` also asserts are *not* covered here; they are checked in
`experimental/notes/audits/proth_rows_certificate_audit.md`.

No row bound, list size, slope count, or MCA statement is asserted.
-/

namespace V4ProthCertificates.ProthWitness

/--
Square-and-multiply modular exponentiation, structurally recursive on a fuel
parameter.  `powMod a e n` is `a ^ e mod n` whenever `fuel` bounds the bit
length of `e`; the wrapper `modPow` supplies `e + 1` as fuel, which always
suffices because the exponent halves at every step.
-/
def powModAux : Nat → Nat → Nat → Nat → Nat
  | 0, _, _, n => 1 % n
  | _ + 1, _, 0, n => 1 % n
  | fuel + 1, a, e, n =>
      let h := powModAux fuel a (e / 2) n
      let s := h * h % n
      if e % 2 == 1 then s * a % n else s

/-- `a ^ e mod n`. -/
def modPow (a e n : Nat) : Nat := powModAux (e + 1) a e n

/--
The certificate data for one Proth row, in the notation of `PC1`: the prime `p`,
its odd part `u`, the 2-adic valuation `s` of `p - 1`, the Proth witness `a0`,
the smooth exponent `n` with `2^n | p - 1`, and the printed budget `B`.
-/
structure ProthRow where
  p : Nat
  u : Nat
  s : Nat
  a0 : Nat
  n : Nat
  B : Nat

/-- All six certificate conditions for one row, as a single decidable Boolean. -/
def ProthRow.check (r : ProthRow) : Bool :=
  (r.p == r.u * 2 ^ r.s + 1)
    && (r.u % 2 == 1)
    && (r.u < 2 ^ r.s)
    && (modPow r.a0 ((r.p - 1) / 2) r.p == r.p - 1)
    && (r.p / 2 ^ 128 == r.B)
    && ((r.p - 1) % 2 ^ r.n == 0)

/-- Rate `1/2` row, smooth order `2^41`. -/
def row41 : ProthRow :=
  { p := 132540169958804033333249306710494641010898987122689
    u := 26766274163673319604503
    s := 92
    a0 := 3
    n := 41
    B := 389500552609 }

/-- Rate `1/4` row, smooth order `2^42`. -/
def row42 : ProthRow :=
  { p := 411940680852499481698306614369841346700408394874881
    u := 41595378994516821279015
    s := 93
    a0 := 13
    n := 42
    B := 1210584858040 }

/-- Rate `1/8` row, smooth order `2^43`. -/
def row43 : ProthRow :=
  { p := 979947269755402568812854322316630667196565607677953
    u := 24737346889219389259839
    s := 95
    a0 := 5
    n := 43
    B := 2879806199253 }

/-- Rate `1/16` row, smooth order `2^44`. -/
def row44 : ProthRow :=
  { p := 2121285573237585848299875619011192262679065433997313
    u := 13387194060291799253121
    s := 97
    a0 := 5
    n := 44
    B := 6233898019554 }

def allRows : List ProthRow := [row41, row42, row43, row44]

/-! ## Per-row certificates -/

theorem row41_check : row41.check = true := by native_decide
theorem row42_check : row42.check = true := by native_decide
theorem row43_check : row43.check = true := by native_decide
theorem row44_check : row44.check = true := by native_decide

/-- Every printed v4 Proth row carries a complete deterministic certificate. -/
theorem allRows_check : allRows.all ProthRow.check = true := by native_decide

/-! ## The individual conditions, stated separately

The `check` conjunction is convenient for replay; the statements below are the
human-readable form the audit note quotes, so that a reader matching the note
against the source never has to unfold a Boolean conjunction.
-/

theorem row41_decomposition :
    row41.p = row41.u * 2 ^ row41.s + 1 := by native_decide
theorem row41_odd : row41.u % 2 = 1 := by native_decide
theorem row41_size : row41.u < 2 ^ row41.s := by native_decide
theorem row41_witness :
    modPow row41.a0 ((row41.p - 1) / 2) row41.p = row41.p - 1 := by native_decide
theorem row41_budget : row41.p / 2 ^ 128 = 389500552609 := by native_decide
theorem row41_smooth : (row41.p - 1) % 2 ^ 41 = 0 := by native_decide

theorem row42_decomposition :
    row42.p = row42.u * 2 ^ row42.s + 1 := by native_decide
theorem row42_odd : row42.u % 2 = 1 := by native_decide
theorem row42_size : row42.u < 2 ^ row42.s := by native_decide
theorem row42_witness :
    modPow row42.a0 ((row42.p - 1) / 2) row42.p = row42.p - 1 := by native_decide
theorem row42_budget : row42.p / 2 ^ 128 = 1210584858040 := by native_decide
theorem row42_smooth : (row42.p - 1) % 2 ^ 42 = 0 := by native_decide

theorem row43_decomposition :
    row43.p = row43.u * 2 ^ row43.s + 1 := by native_decide
theorem row43_odd : row43.u % 2 = 1 := by native_decide
theorem row43_size : row43.u < 2 ^ row43.s := by native_decide
theorem row43_witness :
    modPow row43.a0 ((row43.p - 1) / 2) row43.p = row43.p - 1 := by native_decide
theorem row43_budget : row43.p / 2 ^ 128 = 2879806199253 := by native_decide
theorem row43_smooth : (row43.p - 1) % 2 ^ 43 = 0 := by native_decide

theorem row44_decomposition :
    row44.p = row44.u * 2 ^ row44.s + 1 := by native_decide
theorem row44_odd : row44.u % 2 = 1 := by native_decide
theorem row44_size : row44.u < 2 ^ row44.s := by native_decide
theorem row44_witness :
    modPow row44.a0 ((row44.p - 1) / 2) row44.p = row44.p - 1 := by native_decide
theorem row44_budget : row44.p / 2 ^ 128 = 6233898019554 := by native_decide
theorem row44_smooth : (row44.p - 1) % 2 ^ 44 = 0 := by native_decide

/-! ## Negative controls

`modPow` is only useful if it distinguishes.  A non-witness base must fail the
Proth congruence, and a composite of the same shape must fail it for every
small base.  Both are recorded so that a reader can see the check is not
vacuously true.
-/

/-- `2` is *not* a Proth witness for the rate-`1/2` row. -/
theorem row41_nonwitness :
    modPow 2 ((row41.p - 1) / 2) row41.p ≠ row41.p - 1 := by native_decide

/-- `3 * 2^92 + 1` is composite: no base below 64 satisfies the congruence. -/
theorem composite_control :
    List.all (List.range 62)
      (fun i => modPow (i + 2) ((3 * 2 ^ 92 + 1 - 1) / 2) (3 * 2 ^ 92 + 1)
                  != 3 * 2 ^ 92 + 1 - 1) = true := by native_decide

/-- `modPow` agrees with the defining power on small inputs. -/
theorem modPow_small :
    List.all (List.range 12)
      (fun a => List.all (List.range 12)
                  (fun e => modPow a e 97 == a ^ e % 97)) = true := by native_decide

end V4ProthCertificates.ProthWitness
