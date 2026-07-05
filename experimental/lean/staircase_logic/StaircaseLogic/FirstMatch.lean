namespace StaircaseLogic

/-!
# First-match paid-root removal never double-counts (stdlib-only, no mathlib)

Stdlib-only (no mathlib) formalization of the **ordered first-match
deduplication** that every upper ledger `U(a)` uses to sum paid cells without
double-counting a root:

* `agents.md`, "The complete upper ledger to build at `a0 + 1`": `U(a)` is a
  *first-match, deduplicated* sum of paid/residual cells;
* `agents.md` row-packet schema, "deduplication rule: support/image/root
  coalescing theorem used";
* `def:paid-root-removal` ordering (paid-root subtraction);
* `experimental/notes/m5/m5_stratification_partition_theorem.md`: the leaves
  `L_i = T_i \ (T_0 ∪ … ∪ T_{i-1})` are pairwise disjoint with union `Ω`, so
  first-match counting *partitions* the roots.

We model each ledger cell as a `List Nat` of root ids and process the cells in
order.  A cell pays only its roots not already paid; the accumulator becomes the
running union.  The theorem is that this fold produces a duplicate-free paid set
whose members are exactly the union of all cells — so the running first-match
count is the number of *distinct* roots, and no root is ever paid twice
("sum equals the union count under disjointness-after-removal").

No `sorry`, no `native_decide`, no mathlib; `#print axioms` at the foot.
-/

/-- **First-match paid-root removal step** (m5 leaf `L_i = T_i \ paid`).  Given
the already-paid set `paid` and a cell `c`, the cell pays exactly its roots not
already in `paid`; the accumulator becomes the union `paid ∪ (c \ paid)`. -/
def paidStep (paid c : List Nat) : List Nat :=
  paid ++ c.filter (fun x => decide (x ∉ paid))

/-- Fold the ordered cell list under first-match removal, accumulating the paid
(union) set.  Written as explicit recursion so the kernel proofs stay elementary
(this is `List.foldl paidStep paid cells`). -/
def paidFold (paid : List Nat) : List (List Nat) → List Nat
  | [] => paid
  | c :: cs => paidFold (paidStep paid c) cs

@[simp] theorem paidFold_nil (paid : List Nat) : paidFold paid [] = paid := rfl

@[simp] theorem paidFold_cons (paid c : List Nat) (cs : List (List Nat)) :
    paidFold paid (c :: cs) = paidFold (paidStep paid c) cs := rfl

/-- **Membership telescopes to the union.**  A root is in the accumulated paid
set after the whole fold iff it was already paid or lies in some cell — the paid
set is exactly `paid ∪ (⋃ cells)`. -/
theorem mem_paidFold : ∀ (cells : List (List Nat)) (paid : List Nat) (x : Nat),
    x ∈ paidFold paid cells ↔ x ∈ paid ∨ x ∈ cells.flatten := by
  intro cells
  induction cells with
  | nil => intro paid x; simp
  | cons c cs ih =>
    intro paid x
    rw [paidFold_cons, ih (paidStep paid c) x]
    simp only [paidStep, List.mem_append, List.mem_filter, List.flatten_cons,
      decide_eq_true_eq]
    by_cases hx : x ∈ paid <;> simp [hx]

/-- **No double-count.**  If the starting paid set and every cell are
duplicate-free, the accumulated paid set stays duplicate-free: each cell
contributes only roots disjoint from all earlier ones (disjointness-after-removal
via `nodup_append`). -/
theorem nodup_paidFold : ∀ (cells : List (List Nat)) (paid : List Nat),
    (∀ c ∈ cells, c.Nodup) → paid.Nodup → (paidFold paid cells).Nodup := by
  intro cells
  induction cells with
  | nil => intro paid _ hp; simpa using hp
  | cons c cs ih =>
    intro paid hcells hp
    have hc : c.Nodup := hcells c List.mem_cons_self
    have hfilt : (c.filter (fun x => decide (x ∉ paid))).Nodup :=
      List.filter_sublist.nodup hc
    have hdisj : ∀ a, a ∈ paid → ∀ b,
        b ∈ c.filter (fun x => decide (x ∉ paid)) → a ≠ b := by
      intro a ha b hb hab
      have hbnp : b ∉ paid := of_decide_eq_true (List.mem_filter.mp hb).2
      exact hbnp (hab ▸ ha)
    have hstep : (paidStep paid c).Nodup := by
      unfold paidStep
      exact List.nodup_append.mpr ⟨hp, hfilt, hdisj⟩
    rw [paidFold_cons]
    exact ih (paidStep paid c)
      (fun c' hc' => hcells c' (List.mem_cons_of_mem _ hc')) hstep

/-! ## The shipped first-match statement -/

/-- The accumulated paid (union) set after first-match removal of the ordered
cells, starting from empty. -/
def firstMatchPaid (cells : List (List Nat)) : List Nat := paidFold [] cells

/-- The first-match count: how many distinct roots are paid overall.  Because the
fold only ever *appends* the newly-paid roots, this equals the sum over cells of
their first-match (disjointness-after-removal) contributions. -/
def firstMatchCount (cells : List (List Nat)) : Nat := (firstMatchPaid cells).length

/-- **First-match paid-root removal partitions the union** (`def:paid-root-removal`
ordering; `agents.md` `U(a)` first-match rule / deduplication rule; m5
stratification-partition theorem).  With duplicate-free cells, the accumulated
paid set is duplicate-free and its members are *exactly* the union of all cells.
Hence the running first-match count `firstMatchCount` is the number of distinct
roots, and no root is ever paid twice. -/
theorem firstMatch_partitions_union (cells : List (List Nat))
    (hcells : ∀ c ∈ cells, c.Nodup) :
    (firstMatchPaid cells).Nodup
      ∧ (∀ x, x ∈ firstMatchPaid cells ↔ x ∈ cells.flatten) := by
  refine ⟨nodup_paidFold cells [] hcells List.nodup_nil, ?_⟩
  intro x
  have h := mem_paidFold cells [] x
  simpa [firstMatchPaid] using h

/-! ## Concrete first-match census (kernel `decide`, axiom-free) -/

/-- A concrete first-match census: three overlapping cells with naive
length-sum `3 + 3 + 2 = 8` pay only `5` distinct roots.  The overlaps `{2,3}`
(cell 2) and `{3}` (cell 3) are charged once — disjointness-after-removal.  The
accumulated paid set is exactly the union `{1,2,3,4,5}`. -/
theorem firstMatch_example :
    firstMatchPaid [[1, 2, 3], [2, 3, 4], [3, 5]] = [1, 2, 3, 4, 5]
      ∧ firstMatchCount [[1, 2, 3], [2, 3, 4], [3, 5]] = 5
      ∧ [1, 2, 3].length + [2, 3, 4].length + [3, 5].length = 8 := by decide

end StaircaseLogic

#print axioms StaircaseLogic.mem_paidFold
#print axioms StaircaseLogic.nodup_paidFold
#print axioms StaircaseLogic.firstMatch_partitions_union
#print axioms StaircaseLogic.firstMatch_example
