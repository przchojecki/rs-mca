# Frontier-extension-cell targets: naming the `paid_extension` open cell for the four deployed v14 rows

**Repo head this note was audited against:** `5e50037` (upstream `main`).
**Data:** `experimental/data/certificates/frontier-adjacent/extension_cell_targets_v1.json`.
**Verifier:** `experimental/scripts/verify_frontier_extension_cell_targets.py` (zero-arg,
`--tamper-selftest` supported).

**This note does not pay the `paid_extension` cell and makes no safety claim.**
It (a) proves the `K=B` and `B<K<F` slope-strata are `PAID_BY_THEOREM` by
routing them to strictly-lower-arity base cells, (b) states the exact integer
target the one remaining `K=F` (full-orbit) stratum must hit, with a named
open input and a falsifier, and (c) records a per-branch paid/open ledger.
Nothing here upper-bounds `U(a0+1)` against `B_*`, and the `K=F` branch stays
`OPEN`. See "Merge hygiene" below for how this lands alongside `#329`.

**Status:** `CONDITIONAL` derivation. The four-row bit-budget targets and the
Galois stratification are `AUDIT`-grade (exact integer margins, independently
re-derived below and by the companion verifier); the open-part specification
is a **named-input target**, not a proof. This note converts `#329`'s
`paid_extension = TBD` cell into a per-row, per-branch target with a
falsifier.

**Scope:** `n=2^21`, `k=2^20`, rate `1/2`; KB sextic `F=F_{p^6}`,
`p=2130706433`; M31 quartic `F=F_{p'^4}`, `p'=2147483647`.

---

## 0. What the `paid_extension` cell is (and the pair-field vs slope-field split)

Per `agents.md` L104-118 the safe upper certificate is
`U(a)=paid_tangent+paid_quotient+paid_extension+paid_CA+paid_L1+paid_M1+residuals`.
The **`paid_extension(a)`** cell must upper-bound the MCA/CA-bad slopes
`γ ∈ F` of a *fixed received line* `f_1+γf_2` that are **genuinely
extension-line** and not already charged to a base bucket.

Two "K = B / B<K<F / K=F" trichotomies are in play and MUST NOT be conflated
(process mandate: witness-vs-lemma consistency):

- **Pair-field trichotomy (about the witness).** `lem:confine`+`cor:Fvalued`
  [Ref C1,C2] say: any pair *rational over a subfield* `K⊊F` (up to a common
  scalar) has bad-slope density `≤ |K|/q`, so it cannot attain the deployed
  lower bound. **Consequence:** every deployed witness pair is genuinely
  `F`-valued (`K=F` as a *pair*). This is the confinement story; it fixes the
  witness, not the cell count.
- **Slope-field trichotomy (about the cell).** For that (genuinely `F`-valued)
  pair, its bad *slopes* `γ` still spread across minimal fields
  `K = B(γ)`, `B ≤ K ≤ F` (`f1_minimal_field_descent` [Ref G1]). The cell
  counts them; the open part is the `K=F` slope-stratum.

The exact coordinate object is fixed by `f1_extension_coordinate_transfer`
[Ref G5] + `thm:weil-lines` [Ref C4]: with `D⊆B` and a `B`-basis of `F`, the
`F`-line becomes the **multiplication-slice family** `Φ(f_1)+M_γ·Φ(f_2)`,
`γ∈F`, inside the `e`-interleaved base code `C_B^e`, `e=[F:B]`. The bad `γ` are
exactly the bad parameters of this structured `{M_γ : γ∈F} ⊂ Mat_e(B)` slice.
`thm:weil-lines` proves `B_ext(a)` is *definitionally* a base interleaved
numerator — **weave: CONSISTENT** — but the arity-`e` band bound it reduces to
is `Open Problem prob:band` at arity `e` — **weave: AWAITS**. The v13/v14
ledger keeps `paid_extension` as a *separate* cell precisely because that
arity-`e` residue is not covered by the arity-1 base cells.

---

## 1. Consumed local inputs (GrahamHart extension lane)

All PROVED; consumed with weave labels.

| Input | What it gives | Weave |
|---|---|---|
| `f1_minimal_field_descent` [G1] | unique minimal field `K`, `B≤K≤F`; exhaustive split `K=B / B<K<F / K=F` (divisor lattice) | CONSISTENT (routing) |
| `ef_galois_stabilizer_descent` [G2] | stabilizer trichotomy of horizontal components: full→base-descended, proper→tower-confined, trivial→full-orbit; **does not exclude** full-orbit | CONSISTENT (routing) |
| `ef_full_orbit_cycle_descent` [G3] | a pole-free full Galois orbit descends to a `B`-defined reduced cycle, still pole-free | AWAITS (reduces, does not close) |
| `ef_descended_cycle_inventory_soundness` [G4a] | an inventory covering all descended pole-free `B`-cycles with verified labels ⇒ classification payload | AWAITS (conditional) |
| `ef_descended_cycle_classification_soundness` [G4b] | a complete base/tower/noncontainment classification ⇒ `ef_pole_free_cycle_exclusion` | AWAITS (conditional) |
| `f1_extension_coordinate_transfer` [G5] | exact `Φ(C_F)=C_B^e`; bad `γ` = bad params of `{M_γ}`-slice; extension-line MCA is a structured matrix problem | CONSISTENT |
| `f1_extension_import` §1 [G6] | a nondegenerate base-rational pencil has its isolated slope forced into `B` (`F\B` slope ⇒ degenerate/non-isolated) | CONSISTENT |

**Key reading of G2-G4:** the local inputs are *soundness/routing* lemmas. They
(a) route every datum into base / tower / full-orbit, and (b) reduce
"exclude the full-orbit leakage" to "**produce a classified descended-cycle
inventory**." They do **not** produce that inventory. That missing inventory
(equivalently a pole-forcing theorem, or a zero-dimensional Weil-restricted
eliminant) is the whole content of the open cell.

---

## 2. (Q1) What `B_ext(a)` counts, and the per-branch paid/open ledger

For a fixed genuinely-`F`-valued received line, stratify its bad slopes `γ` by
`K=B(γ)`. Under `ef_galois_stabilizer_descent` [G2] the branches are:

| Branch (stabilizer) | Slopes | Paid by | Charged to | Status |
|---|---|---|---|---|
| **`K=B`** (full `Gal(F/B)`, base-descended) | `γ∈B` | `lem:confine` [C1] + `thm:weil-lines`(iii) diagonal [C4] + `cor:base-rational-line-inertness-chart` [C3] + [G6] | arity-1 base cells (`paid_tangent`/`paid_quotient`/`paid_M1`) | **PAID_BY_THEOREM** — 0 new |
| **`B<K<F`** (proper nontrivial, tower-confined) | `γ∈K\B`, `b\|d\|N`, `b<d<N` | `ef_galois_stabilizer_descent` [G2] + `f1_minimal_field_descent` [G1] + `thm:weil-lines` tower `F/K` [C4] | arity-`[F:K]` intermediate base cell (`< e`) | **PAID_BY_THEOREM** (confined/routed) |
| **`K=F`** (trivial, full-orbit) | `γ` generates `F/B`; size-`e` Frobenius orbits | `ef_full_orbit_cycle_descent` [G3] (partial) + `ef_*_soundness` [G4a,G4b] (conditional) | — (not reducible to lower arity) | **OPEN → CONDITIONAL_ON_NAMED_INPUT** |

So **`paid_extension(a) = deg`(K=F residual chart)** — the only mass not routed
to a strictly-lower-arity base cell. Its value on the safe side is delivered by
`thm:extension-line-dimension-degree-ledger` [C5]: a Weil-restricted chart of
degree `Δ` and dimension `e_Y` over `B` contributes `Δ · q_gen^{e_Y}` bad
`B`-parameters (= bad `F`-slopes), normalized `Δ·q_gen^{e_Y}/q_line`. This is
exactly the implemented `extension_chart_upper(q_gen, [(Δ,e_Y),…])`
(`verify_paid_ledger_functions.py` L122), whose emitted certificate already
carries the non-claim *"does not classify every extension-valued residual
chart"* (L265) — i.e. it computes `Σ Δ q_gen^{e_Y}` but supplies **no `(Δ,e_Y)`
for the deployed `K=F` residual**. That missing `(Δ,e_Y)` is `#329`'s TBD.

---

## 3. (Q2) The exact bit-budget target the open part must satisfy

Budgets (exact, independently re-derived by the verifier): `B*_KB =
⌊p^6/2^128⌋ = 274980728111395087 = 2^57.93`; `B*_M31 = ⌊p'^4/2^100⌋ =
16777215 = 2^24.00`. Fail-margins (headroom at `a0+1`) come from the same
identity-prefix construction as `cap25_v14_moved_frontier_checks.py` (MCA
rows, v14-moved) and `prop:v13f1-identity-frontier` (list rows, unchanged):

**Cost of a positive-dimensional chart** (`e_Y≥1` ⇒ `≥ q_gen` bad slopes):

- KB: `q_gen = p = 2^30.99`. `e_Y=1` *fits the absolute* `B*=2^57.93` but
  costs 31 bits — busts every fail-margin. `e_Y=2 → p^2 = 2^61.98 > B*`: busts
  the absolute budget.
- M31: `q_gen = p' = 2^31.00 > B* = 2^24.00`. **`e_Y=1` busts the absolute
  budget outright**, before any margin argument.

**⇒ `e_Y = 0` is forced in all four rows.** The `K=F` locus must be
**zero-dimensional**; `paid_extension` is then the finite degree `Δ_ext`, a
field-size-independent constant, and must fit the fail-margin:

| row | `(a0, a0+1)` | frontier | fail-margin | `e_Y` | `Δ_ext` ceiling (exact) | binding constraint |
|---|---|---|---|---|---|---|
| **KB-MCA** | (1116047,1116048) | v14-moved | **22.197 b** | `0` | `≤ 4,807,520` | fail-margin only |
| **KB-list** | (1116046,1116047) | unchanged | **22.011 b** | `0` | `≤ 4,226,236` | fail-margin only |
| **M31-MCA** | (1116023,1116024) | v14-moved | **3.259 b** | `0` | `≤ 9` | **absolute budget** + margin |
| **M31-list** | (1116022,1116023) | unchanged | **3.073 b** | `0` | `≤ 8` | **absolute budget** + margin (row binds the whole cell) |

*Exact integer ceiling `= floor(p^(w+1)·B* / L(a0+1))`, computed as an exact
integer ratio (no floating point) by the companion verifier's gate G7. See
"Independent audit" below for a correction to two of these four values versus
the session draft this note is built from.*

Design target across all rows: **`e_Y=0`, `Δ_ext = O(1)` constant.** The
**M31-list row is the binding constraint**: the genuinely-`F`-valued residual
must have total degree `≤ 8`. (Contrast the v13 frontier, where KB-MCA at 5.5 b
was tightest; the v14 MCA move `1116043→1116047` / `1116021→1116023` relocated
the tightness to the M31 pair.)

Note the exact-integer replay confirms `unsafe(a0)=True` and `safe(a0+1)=True`
for all four rows, so the frontier pairs themselves are sound; only the
`paid_extension` chart data is unspecified.

---

## 4. (Q3) Galois structure: sextic diamond vs quartic chain, per-stratum

**KB sextic `F_{p^6}/F_p`, `Gal=Z/6`, divisor lattice `{1,2,3,6}` — a diamond**
(`2,3` incomparable): `F_p ⊂ F_{p^2} ⊂ F_{p^6}` and `F_p ⊂ F_{p^3} ⊂ F_{p^6}`,
`F_{p^2}∩F_{p^3}=F_p`, `F_{p^2}·F_{p^3}=F_{p^6}`. Two nontrivial intermediate
strata:

| `K` | stab `Gal(F/K)` | branch | route arity `[F:K]` | confinement density \|K\|/q |
|---|---|---|---|---|
| `F_p` | `Z/6` | base-descended | 1 | `p^-5 = 2^-154.9` |
| `F_{p^2}` | `Z/3` | tower-confined | 3 | `p^-4 = 2^-124.0` |
| `F_{p^3}` | `Z/2` | tower-confined | 2 | `p^-3 = 2^-93.0` |
| `F_{p^6}` | `1` | **full-orbit (OPEN)** | — | `2^0` |

**M31 quartic `F_{p'^4}/F_{p'}`, `Gal=Z/4`, divisor lattice `{1,2,4}` — a chain:**
`F_{p'} ⊂ F_{p'^2} ⊂ F_{p'^4}`. One nontrivial intermediate stratum:

| `K` | stab `Gal(F/K)` | branch | route arity `[F:K]` | confinement density \|K\|/q |
|---|---|---|---|---|
| `F_{p'}` | `Z/4` | base-descended | 1 | `p'^-3 = 2^-93.0` |
| `F_{p'^2}` | `Z/2` | tower-confined | 2 | `p'^-2 = 2^-62.0` |
| `F_{p'^4}` | `1` | **full-orbit (OPEN)** | — | `2^0` |

**Structural reading.** The KB diamond forces the EF trichotomy to split the
tower branch over *two incomparable* intermediate fields (arity-3 and arity-2
sub-problems that meet only at the base) — the descended-cycle inventory [G4]
must certify both `F_{p^2}` and `F_{p^3}` confinement independently. The M31
chain has a *single* arity-2 intermediate — the simplest nontrivial descent.
The `K=F` full-orbit stratum has orbits of size `e` (6 / 4), so a per-line
**divisibility check** is available: the genuinely-`F`-valued bad-slope count
is `≡ 0 (mod e)` (a cheap consistency test for any scanner or witness hunt,
independently re-verified by the companion verifier's gate G4).

Ambient `K=F` counts (`Σ_{d|e} μ(e/d)p^d`) and proper-subfield ambient counts
(`p^3+p^2+p = 2^93.0` KB; `p'^2+p' = 2^62.0` M31) are recorded in the JSON;
these are the raw stratum sizes the routing/zero-dim certificate must avoid
charging directly (raw would be `2^93` / `2^62`, far above `B*`).

The paid strata are **routed, not counted raw**: `K=B` is the arity-1 diagonal
already in the base cells; each `B<K<F` is Weil-restricted `F/K` to an
arity-`[F:K]` intermediate base cell. (The `|K|/q` densities in the tables are
the *confinement ceilings for subfield-rational attack pairs* — the pair-field
story [C1] — reproduced here to show every subfield-rational attack is inert;
they are not the fixed-line slope-strata counts, which are bounded by routing.)

---

## 5. (Q4) Falsifiable prediction and the toy search that tests it

**Prediction P (`CONJECTURAL_WITH_FALSIFIER`).** For each deployed row and its
toy tower analogue, the genuinely-`F`-valued (`K=F`) MCA-bad slopes of any
band-regime received line form a **finite** set: a union of complete Frobenius
orbits of size `e` (6 KB / 4 M31) whose total size is a **field-size-independent
constant** `Δ_ext`, not growing with `q_gen`. Equivalently: the `{M_γ}`-slice
[G5] admits no positive-dimensional genuinely-`F`-valued bad locus.
**Scope (slack qualifier, see §5.1):** Prediction P is about the *band regime* —
the toy slack `t≥2` analogue of agreement strictly inside the band, which is
where `paid_extension` is charged. The minimal-slack `t=1` boundary (agreement
only just exceeding the code dimension `k`) is a **degenerate regime explicitly
outside** P's scope; the shipped scanner shows the two regimes behave oppositely.

**Falsifier (`COUNTEREXAMPLE_NEW_FLOOR`).** A band-regime `F`-valued pair over a
toy tower whose `K=F` bad-slope count **grows with the base prime** `p_0`
(e.g. `∝ p_0`, i.e. a positive-dimensional `e_Y≥1` chart). By §3 this makes
`paid_extension` unpayable at the deployed margins (already at `e_Y=1`), so it
would refute the adjacent-pair frontier `prob:v13f1-frontier` on the extension
side — the exact `F1` "lift or counterexample" fork (`agents.md` L453). The
shipped scan's `t=1` combinatorial growth is **not** this falsifier: `t=1` is the
degenerate minimal-slack boundary, not a band-regime pair — it is labeled `AUDIT`
in §5.1, and the band regime (`t≥2`) is where the scan is *consistent* with P.

**Search shape (`agents.md` F1 toy menu L466-473; `f1_extension_coordinate_transfer` "Next Step").**

- **KB analogue:** tower `F_{p_0^6}/F_{p_0}`, `p_0∈{2,3,5}` (diamond lattice
  `{1,2,3,6}`, orbit size 6). Field sizes `64,729,15625` — feasible by brute
  force with care.
- **M31 analogue:** tower `F_{p_0^4}/F_{p_0}`, `p_0∈{2,3,5,7}` (chain `{1,2,4}`,
  orbit size 4). Field sizes `16,81,625,2401` — easily feasible; this is the
  *binding* row, run first.
- **Params:** `ρ=1/2`, slack `t∈{1,2}`, `D` a multiplicative coset in `F_{p_0}`,
  agreement at the toy-scale band edge (analogue of `a0+1`).
- **Procedure:** enumerate/sample `F_{p_0^e}`-valued pairs `(f,g)`; brute-force
  all support-wise MCA-bad slopes `γ∈F_{p_0^e}`; classify each by
  `deg(F_{p_0}(γ)/F_{p_0})∈` divisors of `e`; tabulate `#{K=F}` vs `p_0`; fit
  the growth. **Constant ⇒ target holds** (`e_Y=0`, `Δ_ext=O(1)`); **linear in
  `p_0` ⇒ falsifier** (`e_Y=1`). Cross-check `#{K=F} ≡ 0 (mod e)` and the
  Frobenius-orbit structure at every field.

This is a stdlib-only scanner (env: no numpy/sympy). **Shipped in this branch:**
`experimental/scripts/f1_extension_full_orbit_scan.py` (zero-arg, deterministic,
`--tamper-selftest`) emits
`experimental/data/certificates/frontier-adjacent/f1_full_orbit_scan_v1.json`
with the per-tower `(p_0, #{K=F}, orbit_check)` table and a fitted growth verdict
for the whole menu (chain `p_0∈{2,3,5,7}`, diamond `p_0∈{2,3,5}`, `t∈{1,2}`). Its
result is a **slack-dependent split**, which sharpens Q4 with the qualifier below.

### 5.1 Slack-scope qualifier (scanner result)

The scan does **not** return a single growth verdict; it splits on the toy slack
`t` (support-wise agreement size `= k+t`):

| toy slack | `K=F` count (fixed genuinely-`F` `β`) | reading |
|---|---|---|
| **`t=1`** (minimal, degenerate boundary) | `= C(n,k+1)` exactly: `1, 1, 4, 15` at `p_0=2,3,5,7` | grows with `p_0` — **`AUDIT` (boundary characterization), NOT a falsifier** |
| **`t≥2`** (band regime, the charged cell) | `0` at every feasible `p_0` (chain `p_0=5,7`; diamond `p_0=5`; `p_0=2,3` infeasible, `k+t>n`); in fact `0` bad slopes of *any* field | matches **Prediction P** (`e_Y=0`) with room to spare |

**Why `t=1` is a degenerate boundary (divided-difference mechanism, 3 sentences).**
At minimal slack `t=1` each size-`k+1` support `S={x_0,…,x_k}` has a
one-dimensional degree-`<k` parity space — a single divided-difference weight `c`
(the unique up-to-scale null vector of the `k×(k+1)` Vandermonde, normalized to
`c_i = 1/∏_{j≠i}(x_i−x_j)`) — so the bad-slope condition collapses to the one
scalar equation `A+γB=0` with `A=Σ_i c_i f_β(x_i)` and `B=Σ_i c_i x_i^{k}`.
Because `B` is the `k`-th divided difference `[x_0,…,x_k]\,x^{k}`, which equals
the leading coefficient `1` of `x^{k}` and so never vanishes, every one of the
`C(n,k+1)` supports yields exactly one slope `γ=−A/B`, and since
`A=[x_0,…,x_k]\,(x−β)^{-1}=(−1)^{k}/∏_i(x_i−β)` is a nonzero genuinely-`F`-valued
quantity (it carries `β∈F∖B`), each such `γ` is `K=F`. Hence the `t=1` count is
exactly `C(n,k+1)` — `1,1,4,15` at `p_0=2,3,5,7`, independently re-verified here
at `p_0=2,3,5` by from-scratch brute force — whereas at `t≥2` the size-`k+2`
support carries **two** checks, the single monomial `g=x^{k}` can cancel only
one, and the residual `γ`-free divided-difference condition on `f_β` is
generically nonvanishing, collapsing the count to identically `0` (consistent
with the forced `e_Y=0`).

**Consequence for Q4.** Prediction P and its `COUNTEREXAMPLE_NEW_FLOOR` falsifier
concern the **band regime** (toy `t≥2`), where the scan found the `K=F` locus
*empty* at every feasible `p_0` — evidence for, not proof of, `e_Y=0`. The `t=1`
growth is the minimal-slack degeneracy (agreement barely exceeding the code
dimension `k`); it is labeled **`AUDIT`**, a boundary characterization **outside
the prediction's scope**, and is *not* the falsifier of §5. **Anyone attacking
Prediction P should attack the `t≥2` / band regime**, not `t=1`: the `t=1`
combinatorial count `C(n,k+1)` does not bear on the extension cell. The
toy-fidelity caveat still stands (and is carried in the scanner's own emitted
verdict): this is the audited `f1_extension_slope_sweep.py` pencil
(`f_β=1/(x−β)`, `g=x^k`) generalized to towers of degree `e∈{4,6}` and slack
`t∈{1,2}`, not the deployed witness, and the correspondence between the toy `t`
and the deployed `(a_0,a_0+1)` fail-margin is not established here.

---

## 6. Independent audit (this note's own contribution beyond the session draft)

Every numeric field in `extension_cell_targets_v1.json` was independently
recomputed from `n`, `k`, and the two field primes alone (not transcribed),
by the companion verifier plus an ad hoc higher-precision cross-check. Both
the field primes' `prime_form` identities and primality, the two `B*`
budgets, the subfield-lattice divisors and confinement densities, the exact
Möbius `K=F`-stratum counts and Frobenius-orbit divisibility, the `e_Y` cost
verdicts, the four canonical `(a0,a0+1)` pairs and their `w_at_a0` values, and
the exact `unsafe(a0)`/`safe(a0+1)` integer inequalities all check out exactly.

**One arithmetic slip was caught and corrected.** The session draft
(`wave9_extension_numbers.json`) computed each row's `Delta_ext_ceiling_int`
by printing `2**fail_margin_bits` with Python's `':,.0f'` format, which
**rounds to nearest** rather than **flooring**. The design semantics require
the floor (`Δ_ext` is a nonnegative integer degree that must satisfy
`Δ_ext ≤ 2^{fail\_margin}`, so the largest integer it may take is the floor,
not the nearest integer). Recomputing the ceiling as the *exact* integer ratio
`floor(p^{w+1}·B* / L(a_0+1))` (no floating point at all — this is a ratio of
two huge cached integers) gives:

| row | session draft (round-to-nearest) | corrected (exact floor) |
|---|---|---|
| KB-MCA | 4,807,521 | **4,807,520** |
| KB-list | 4,226,237 | **4,226,236** |
| M31-MCA | 9 | 9 (unchanged — already the exact floor) |
| M31-list | 8 | 8 (unchanged — already the exact floor) |

Both KB rows were off by exactly `+1` in the unsafe direction: the draft's
stored ceiling was one integer *more permissive* than the true bound. The
shipped values are the exact floors in all four rows. For the record,
round-to-nearest would have misprinted THREE of the four rows, not two:
`2^{margin}` has fractional part above `0.5` for KB-MCA (`4807520.938`),
KB-list (`4226236.539`), **and M31-MCA (`9.572`)** — round would give
`4807521 / 4226237 / 10` where the true floors are `4807520 / 4226236 / 9`.
Only M31-list (`8.415`, fractional part below `0.5`) has floor equal to
round. The correction to the draft's stored integers affected only the two
KB rows because the draft happened to store the M31 floors correctly, not
because their rounding is benign. The shipped
`experimental/data/certificates/frontier-adjacent/extension_cell_targets_v1.json`
carries the corrected values and an explicit `audit_corrections` block
documenting this; `verify_frontier_extension_cell_targets.py` gate G7 checks
against the corrected values via the exact-integer route (never the
round-to-nearest one) and would fail against the original draft numbers.

No other discrepancy was found. All tex/markdown citations in the Refs
section below were confirmed to exist by grep against this repo head; where a
citation's line number points at a `\begin{...}` line one above the matching
`\label{...}` line, that is an existing citation convention already used
elsewhere in this repo (confirmed by inspection at `cor:base-rational-line-inertness-chart`
and `thm:extension-line-dimension-degree-ledger`), not a broken reference.

---

## 7. Merge hygiene: this branch alongside `#329`

`#329` (`frontier-adjacent-v13-rows`, open at the time this branch was cut)
introduces `experimental/data/certificates/frontier-adjacent/` for the first
time, with four packet files: `kb_list_v1.packet.json`,
`kb_mca_v1.packet.json`, `m31_list_v1.packet.json`, `m31_mca_v1.packet.json`,
plus `experimental/notes/frontier-adjacent/frontier_adjacent_v13_rows_v1.md`
and `experimental/scripts/verify_frontier_adjacent_v13_rows.py`. Because
`#329` has not merged, neither the `experimental/data/certificates/frontier-adjacent/`
nor `experimental/notes/frontier-adjacent/` directory exists on this branch's
base commit; this branch creates both fresh.

This note's three new paths —
`experimental/notes/frontier-adjacent/frontier_extension_cell_targets_v1.md`,
`experimental/data/certificates/frontier-adjacent/extension_cell_targets_v1.json`,
`experimental/scripts/verify_frontier_extension_cell_targets.py` — share **no
filename** with any of `#329`'s five new paths. The two branches touch the
same two directories but disjoint files within them, so they **merge cleanly
in either order** (a directory-level union, no content conflict). This note
is explicitly designed to plug into `#329`'s ledger as a follow-up: once both
land, `#329`'s `paid_extension: TBD` line can be replaced by the target block
in §3/§2 above, with a reference to this note — but that edit is not made
here, to avoid taking a dependency on `#329`'s merge order.

**Other concurrent PRs in this wave**, noted for context, no functional
dependency either direction:

- **`#328`** (`cap25-v13-identity-frontier-cert`) packages the *unsafe*-side
  certificate for the v13 identity-scale frontier only; it does not touch
  `paid_extension` or any extension-cell material.
- **`#330`** (`l1-key-lemma-refuted`) is an L1-track counterexample (the `E_3
  ≤ ell-2` key lemma fails at five `ell` values); unrelated field/track (L1
  petal syzygy, not F1/EF extension-line structure).
- **`#335`** (`l1-sigma-calculus`) packages L1 sigma-calculus lemmas for the
  petal syzygy space, built on `#330`'s counterexample Gammas; also an L1
  track, no overlap with this note's F1/EF Galois-stratification content.

---

## Refs

`experimental/rs_mca_proximity_prize_status.md` (prize submission memo, upstream 5e50037: final-form envelope + renormalized band; this note's extension cell is one of the memo's open safe-side inputs) |

- **C1** `lem:confine` (subfield confinement) — `tex/cs25_cap_v12.tex` L3693.
- **C2** `cor:Fvalued` (certifying lines genuinely `F`-valued) — L3714.
- **C3** `cor:base-rational-line-inertness-chart` — L2855.
- **C4** `thm:weil-lines` (restriction of scalars) + `cor:T3-status` — L4600, L4622.
- **C5** `thm:extension-line-dimension-degree-ledger` (`Δ·|B|^e` chart) — L2823.
- **C6** `thm:conditional-mca` (`B_ext(a)` term) — L4211; `rem:conditional-status` L4925.
- **C7** `cor:extension-pole-deep-list-floor` / `-quotient-remainder-floor` (lower side) — L498/L543.
- **V1** `prop:v13-extension` (extension-pole conversion cell, `q_gen`/`q_line`) — `experimental/cap25_v13_experimental.tex` L243.
- **V2** `prop:v13f1-identity-frontier` (list-row margins) — L1375; `prob:v13f1-frontier` L1448.
- **G1** `f1_minimal_field_descent` — `experimental/notes/f1/f1_minimal_field_descent.md`.
- **G2** `ef_galois_stabilizer_descent`; **G3** `ef_full_orbit_cycle_descent`;
  **G4a** `ef_descended_cycle_inventory_soundness`; **G4b** `ef_descended_cycle_classification_soundness` — `experimental/notes/ef/`.
- **G5** `f1_extension_coordinate_transfer`; **G6** `f1_extension_import_lemma` — `experimental/notes/f1/`.
- **S** scanner: `extension_chart_upper` / `extension_only_cell` — `experimental/scripts/verify_paid_ledger_functions.py` L108-130; non-claim L265.
- **N** numbers + exact replay: `experimental/data/certificates/frontier-adjacent/extension_cell_targets_v1.json`,
  `experimental/scripts/verify_frontier_extension_cell_targets.py`,
  `experimental/scripts/towards v13/cap25_v14_moved_frontier_checks.py`.
- **F1S** F1 full-orbit toy scanner (shipped, §5.1): `experimental/scripts/f1_extension_full_orbit_scan.py`
  (zero-arg, deterministic, `--tamper-selftest`); certificate
  `experimental/data/certificates/frontier-adjacent/f1_full_orbit_scan_v1.json`.
  Cross-executed by `verify_frontier_extension_cell_targets.py` gate G10.
