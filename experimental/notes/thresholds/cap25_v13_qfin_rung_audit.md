# CAP25 v13 raw: conj:Q divisor-lattice rung audit at a0+1 (KB-MCA)

Status: `AUDIT` / `EXACT_LEDGER` / `PROVED-LOCAL(identity D)` / `OPEN(reductions)`.

**Data:** `experimental/data/certificates/frontier-adjacent/kb_mca_conjq_rung_audit_v1.json`.
**Verifier:** `experimental/scripts/verify_kb_mca_conjq_rung_audit.py` (zero-arg,
`--tamper-selftest` supported).

**What this note is.** It executes the `grande_finale.tex` Work-Plan paragraph
"Rung audit" for the KoalaBear MCA v13 raw row `(1116047, 1116048)`:

> "Before trying to prove hard equidistribution, run the exact divisor-lattice
> audit at `a_0+1` for all quotient scales. If any periodic rung exceeds the
> budget, the adjacent conjecture is false for a paid reason and the edge must
> move. If every rung is below budget with printed margin, the remaining work
> is genuinely primitive." (`grande_finale.tex`, Work Plan, `\paragraph{Rung
> audit}`)

Equivalently, it is the maintainer synthesis note's
(`cap25_v13_qfin_primitive_wall_synthesis.md`, "Next exact wall") **route 3**:
*"replace max-orbit flatness by an image-level quotient/descent compiler with
exact per-rung bit losses."* Because `n = 2^21`, the divisor lattice of `n`
**is** the 2-adic tower `j = 0..21`, so the audit below is complete: every
scale of the lattice is covered, not a sample.

**What this note is not.** It does **not** prove `conj:Q`; it does **not**
prove `U(1116048) <= B*`; it does **not** move the frontier edge. It reduces
the full-target wall exactly to `conj:Q`'s subset-primitive core plus an
explicit, budget-negligible, four-rung ladder, all `BELOW` budget with printed
margin (verdict `GREEN`). It is also **distinct** from this packet family's
existing `kb_mca_v1.packet.json` `.rung_margin_audit` block, which is a
different object (the lower-side periodic-floor audit) -- see Sec. 8 below
for the reconciliation.

---

## 1. Setup and constants (KB-MCA safe row)

Quoted exactly from `cap25_v13_qfin_primitive_wall_synthesis.md`:

```text
p = 2^31 - 2^24 + 1 = 2130706433,
q = p^6,
n = 2^21 = 2097152,
k = 2^20 = 1048576,
B* = floor(q / 2^128) = 274980728111395087.

m_unsafe = 1116047,   w_unsafe = m_unsafe - k - 1 = 67470,
m_safe   = 1116048,   w_safe   = m_safe   - k - 1 = 67471.

avg = binom(n, m_safe) / p^w_safe,   log2(avg) ~= 35.735246417.
log2(B*) ~= 57.932108125,
log2(B*/avg) ~= 22.196861708,
K_raw = floor(B* p^w_safe / binom(n, m_safe)) = 4807520.
```

One further exact fact this audit needs, not stated in the synthesis note:
`v2(m_safe) = 4` (`m_safe = 2^4 * 69753`). This integer is the hard cap on
how many rungs the descent ladder below can reach (Sec. 3).

The domain is a multiplicative-coset row `D = alpha*mu_n subset F_p^*`
(KoalaBear: `mu_n` is the order-`n` subgroup). The prefix moment map is
`Phi_w(M) = (p_1(M), ..., p_w(M))`, `p_i(M) = sum_{x in M} x^i in F_p`, for
`m`-subsets `M subset D`. The twist action `M -> zeta*M` (`zeta in mu_n`) sends
`z_i -> zeta^i z_i` and preserves fiber size; the target stabilizer is
`Stab(z) = mu_{gcd(n, I(z))}`, `I(z) = {i <= w : z_i != 0}` (with
`gcd(n, empty) = n` for the all-zero target).

---

## 2. The exact image-level descent identity (D)

**Stratification.** Write `v(z) = min_{i in I(z)} v2(i)` (capped at `21`, and
`= 21` for the all-zero target). Stratum `j := {z : v(z) = j}`; `j = 0` is
primitive.

**Power map.** `pi_j : D -> D_j := alpha^{2^j} mu_{n/2^j}`, `x -> x^{2^j}`, is
exactly `2^j`-to-1. For any `m`-subset `M`, its fiber-count profile
`c_M : D_j -> {0,...,2^j}`, `c_M(y) = |M cap pi_j^{-1}(y)|`, satisfies
`sum_y c_M(y) = m`. For every `i' >= 1`,

```text
p_{2^j i'}(M) = sum_{x in M} (x^{2^j})^{i'} = sum_{y in D_j} c_M(y) y^{i'}.     (*)
```

So the power sums of `M` at indices divisible by `2^j` are exactly the
weighted power sums of the pushforward profile `c_M` on the quotient domain
`D_j`.

**Subset symmetry.** The subset stabilizer `Stab(M) = {zeta in mu_n : zeta M =
M} = mu_{2^s}`, `s = s(M)`. `M` is `mu_{2^s}`-symmetric iff `c_M in {0, 2^s}`
(each coset fully in or out); such `M` are unions of size-`2^s` cosets, so
`2^s | m`, hence **`s(M) <= v2(m) = 4` for every `m`-subset at this row.**
Also `Stab(M) subset Stab(Phi_w(M))` (subset symmetry implies target symmetry,
never the converse). Splitting a fiber by member symmetry level:

```text
|Phi_w^{-1}(z)| = sum_{s=0}^{min(v(z),4)} N_s(z),   N_s(z) = #{M in fiber : s(M) = s}.   (E)
```

**Identity (D), and its proof.** A `mu_{2^s}`-symmetric `M` equals
`pi_s^{-1}(Mbar)` for a unique `Mbar subset D_s`, `|Mbar| = m/2^s`; using
`sum_{u in mu_{2^s}} u^i = 2^s [2^s | i]`,

```text
p_i(M) = 0 for 2^s nmid i,     p_{2^s i'}(M) = 2^s P_{i'}(Mbar),
```

where `P_{i'}(Mbar) = sum_{y in Mbar} y^{i'}` is the quotient power sum. So the
full length-`w` prefix of a symmetric `M` is *determined* by `Mbar`'s
length-`w_s` quotient prefix. Hence, for any target `z` supported on
index multiples of `2^s` (in particular whenever `s <= v(z)` -- the only
regime the ladder uses; off-support targets have zero symmetric part), the
**`mu_{2^s}`-symmetric part** of its fiber equals the *entire* (unrestricted)
quotient-row fiber:

```text
Nsym_s(z) := #{M in Phi_w^{-1}(z) : M is mu_{2^s}-symmetric}
           = | (Phi_{w_s}^{D_s})^{-1}( z_down^{(s)} ) |,   row_s = (n/2^s, m/2^s, floor(w/2^s)),
z_down^{(s)}_{i'} = z_{2^s i'} / 2^s (mod p),  i' = 1..w_s.                                    (D)
```

`(D)` is the exact image-level descent: the `mu_{2^s}`-symmetric part of any
fiber is a genuine prefix fiber of the smaller quotient row `row_s` on the
`2^s`-power-image domain -- i.e. `Phi` *does* factor through the power map
`x -> x^{2^s}` on the symmetric classes, and only those. **Proof:** character
orthogonality on `mu_{2^s}` gives the vanishing of the off-`2^s` moments;
`(*)` gives the surviving ones; the coset-collapse `M <-> Mbar` is the stated
bijection. **PROVED**, and verified to the integer by exhaustive enumeration
on toy rows (Sec. 6, gate iii of the verifier): for every target `z` hit by
some subset, `N_s(z) == Pi_s(z_down)` exactly, where `s = v(z)` is the
target's own stratum and `Pi_s` is the independently re-enumerated quotient
fiber count.

**The correction term, made explicit.** The naive hope "stratum-`j` target
implies `mu_{2^j}`-symmetric support" is **false**. In the `(E)`/`(D)`
language this is exactly the statement that for a stratum-`j` target the terms
`N_s(z)` with `s < j` are generally nonzero: `sum_{s<j} N_s(z)` is the
correction, the members whose target is `2^j`-stabilized but whose support has
strictly smaller symmetry. It is not hand-waved -- each `N_s(z) =
Pi_s(z_down^{(s)})` is a concrete subset-primitive quotient fiber. The
synthesis note's `F_17` witness `M = {1,2,4,10}`, `z = (0,2)` (`p=17, n=16,
w=2`) is exactly this: `s(M)=0` (subset-primitive support), `v(z)=1` (a
`mu_2`-stabilized target) -- i.e. a term in the `s=0`, `j=1` correction
bucket. The verifier's gate iii checks this named witness directly: `p_1(M) =
1+2+4+10 = 0`, `p_2(M) = 1+4+16+100 = 2` (mod 17), and `M` is not closed under
multiplication by `-1 = 16` (the generator of `mu_2`), confirming `s(M)=0 < 1
= v(z)`.

**Why naive relaxation FAILS (exact).** Dropping the vanishing constraints
`p_i(M) = 0` (`2^j nmid i`) and keeping only `(*)` gives a relaxed count
`G_j(z_down) = #{M : (*) holds}`, whose average over the `p^{w_j}` descended
targets is `binom(n,m)/p^{w_j}`, i.e.

```text
avg(G_j) / avg = p^{w - w_j} = p^{w - floor(w/2^j)}.
```

For `j=1` at the deployed row this is `p^{33736} ~ 2^{1.05e6}` --
astronomically over budget. So the off-`2^j` moments are load-bearing: the
descent is a genuine **correspondence `(D)`, not a relaxation.** The
verifier's gate iv checks this mechanism on a toy row (`F_17`, `m=9`, `w=2`,
`j=1`): the true average fiber is `~39.58`, the *relaxed* average is
`~672.94`, and their ratio is exactly `17^1 = p^{w-w_j}`; the enumerated
maximum relaxed bucket (`696`) already exceeds the true average by more than
that factor. The subset-symmetry split `(E)`/`(D)` is the *correct*
image-level descent precisely because symmetric members automatically satisfy
the off-`2^j` vanishing (character orthogonality), so no information is
thrown away.

---

## 3. The 5-rung ladder

Taking `max_z` of `(E)`: `MAXFIBER := max_z |Phi_w^{-1}(z)| <= maxPi_0 +
sum_{s=1}^{4} maxPi_s`, where `maxPi_0` is the subset-**primitive** prefix
fiber (the residual `conj:Q` core, depth `w_0 = 67471`) and `maxPi_s`
(`s=1..4`) is the max subset-primitive fiber of the strictly smaller quotient
row `row_s`. The reach stops at `s=4` because `v2(m_safe) = 4` is a hard cap
(Sec. 1): no `m_safe`-subset can have subset-symmetry level `s > 4`.

**What absorbs strata `j = 5..16, 21`.** For these `j`, `2^j` does **not**
divide `m_safe`, so no `mu_{2^j}`-symmetric `m_safe`-subset exists at all: the
entire fiber of any such target is a sum of the *same* five `Pi_s`
(`s=0..4`) functions via `(E)`/`(D)` -- no sixth object, no new proof
obligation. In particular the refuted "mode-at-null" object (`prop:mode-null-
false`; the all-zero target is stratum `j=21`) is just `sum_{s<=4} N_s(0)`; no
separate null-flatness hypothesis is needed.

**Strata `j = 17..20` are vacuous (PROVED).** The maximum `v2(i)` for `i <=
w_safe = 67471` is `16` (attained only at `i = 65536 = 2^16`), so no index
`i <= w_safe` has `v2(i) >= 17`; these four strata are empty by construction,
not merely small.

---

## 4. The table, j = 0..21

Exact per-rung margin below the `K_raw` budget, all 22 scales of the 2-adic
divisor lattice (from `verify_kb_mca_conjq_rung_audit.py`'s from-scratch
recompute, matching the shipped
`kb_mca_conjq_rung_audit_v1.json`; margins to 9 decimals). "share" = the
per-rung pessimistic `K_raw` consumption (floor); "margin" = `log2(K_raw /
share)`; verdict is one of `RESIDUAL` / `BELOW` / `VACUOUS` (never `EXCEEDS`).

```text
conj:Q DIVISOR-LATTICE RUNG AUDIT @ a0+1 = 1116048  (KB-MCA, v13 raw)
wall: CAP25-V13-QFIN-PRIMITIVE-MAX-ORBIT-FLATNESS-KB-MCA-1116048
K_raw=4807520 (log2=22.196861429)  budget B*/avg=22.196861708 bits

  j  2^j        n_j       w_j   descend  m_j        log2 a_j        margin_below_Kraw(bits)  pess.share      verdict
  0      1    2097152    67471  trivial -         -              0.0                    -             RESIDUAL (this IS the primitive wall conj:Q; margin=0 by construction)
  1      2    1048576    33735  True    558024    28.450587712   7.284658705            30833         BELOW budget
  2      4     524288    16867  True    279012    25.058258099   10.676988317           2936          BELOW budget
  3      8     262144     8433  True    139506    23.612092775   12.123153642           1077          BELOW budget
  4     16     131072     4216  True    69753     23.139009074   12.596237343           776           BELOW budget
  5     32      65536     2108  False   -         -              -                      0             BELOW budget (no independent mass; covered by s<=4 ladder)
  6     64      32768     1054  False   -         -              -                      0             BELOW budget (no independent mass; covered by s<=4 ladder)
  7    128      16384      527  False   -         -              -                      0             BELOW budget (no independent mass; covered by s<=4 ladder)
  8    256       8192      263  False   -         -              -                      0             BELOW budget (no independent mass; covered by s<=4 ladder)
  9    512       4096      131  False   -         -              -                      0             BELOW budget (no independent mass; covered by s<=4 ladder)
 10   1024       2048       65  False   -         -              -                      0             BELOW budget (no independent mass; covered by s<=4 ladder)
 11   2048       1024       32  False   -         -              -                      0             BELOW budget (no independent mass; covered by s<=4 ladder)
 12   4096        512       16  False   -         -              -                      0             BELOW budget (no independent mass; covered by s<=4 ladder)
 13   8192        256        8  False   -         -              -                      0             BELOW budget (no independent mass; covered by s<=4 ladder)
 14  16384        128        4  False   -         -              -                      0             BELOW budget (no independent mass; covered by s<=4 ladder)
 15  32768         64        2  False   -         -              -                      0             BELOW budget (no independent mass; covered by s<=4 ladder)
 16  65536         32        1  False   -         -              -                      0             BELOW budget (no independent mass; covered by s<=4 ladder)
 17 131072         16        0          -         -              -                      -             VACUOUS (PROVED empty)
 18 262144          8        0          -         -              -                      -             VACUOUS (PROVED empty)
 19 524288          4        0          -         -              -                      -             VACUOUS (PROVED empty)
 20 1048576          2        0          -         -              -                      -             VACUOUS (PROVED empty)
 21 2097152          1        0  False   -         -              -                      0             BELOW budget (no independent mass; covered by s<=4 ladder)
```

Every rung is `RESIDUAL`, `BELOW`, or `VACUOUS`. **No rung `EXCEEDS`.**

---

## 5. Aggregate: residual primitive budget and the rounding policy

The four nonprimitive-rung pessimistic shares (`s=1..4`: `30833.322195,
2936.482065, 1077.676000, 776.382660`) are **exact rationals** sharing a
common denominator `binom(n, m_safe)`; their sum, `35623.862920`, is not an
integer.

**Rounding policy (one sentence).** The aggregate nonprimitive charge is
rounded *conservatively* -- `charge := ceil(sum_{s=1}^{4} share_s)`, never
`floor` -- so that the residual primitive budget quoted for `conj:Q`'s core is
never overstated, giving `charge = 35624` and `residual := K_raw - charge =
4771896` (with `charge + residual == K_raw` exactly by construction).

**Reconciling a known discrepancy.** Lane C's own derivation script
(`laneC_rung_audit.py`) truncates the summed share via Python's `int()`
(equivalent to `floor`), printing `charge=35623` and `residual=4771897`; an
earlier prose pass instead used `ceil`, printing `charge=35624` and
`residual=4771896`. Both numbers are computed from the *same* exact rationals
-- this is a `+/-1` aggregation-convention choice, not a new arithmetic error;
every per-rung share, every rung verdict, and the combined margin below are
identical either way. This note, the shipped JSON, and the verifier all adopt
the **conservative pair `charge=35624`, `residual=4771896`** throughout (gate
v of the verifier checks exactly this pair, and checks
`charge + residual == K_raw`).

```text
AGGREGATE (conservative rounding policy: charge = ceil, not floor)
  nonprimitive rungs (s=1..4) total pessimistic share (exact float) = 35623.862920
  ... floor(share) = 35623  (Lane C's own script value; residual would be 4771897 -- NOT adopted)
  ... ceil(share)  = 35624  (ADOPTED charge)
  combined margin below K_raw                     = 7.076305084 bits
  residual PRIMITIVE budget for conj:Q core        = 4771896   (0.992590 of K_raw)
  residual log2                                    = 22.186131170  (loss 0.010730259 bit)
  charge + residual == K_raw ?                       True
  any rung EXCEEDS budget?  NO      all rungs BELOW/RESIDUAL/VACUOUS?  YES
  VERDICT: GREEN
```

---

## 6. Minimal lemmas per rung, PROVED / OPEN-REDUCTION

The **periodic-rung proof obligations** of this audit, one per nonprimitive
rung, plus the `s=0` primitive core:

| rung | statement (ladder threshold) | standalone slack vs `B*` (bits, informational) | status |
|---|---|---:|---|
| `(D)` itself (all `s`) | the descent identity of Sec. 2 | -- | **PROVED** (character orthogonality; exhaustively toy-verified) |
| empty strata `j=17..20` | vacuous, no index `i<=w` has `v2(i)>=17` | -- | **PROVED** (vacuous) |
| `L_1` (`row_1 = (1048576, 558024, 33735)`) | `maxPi_1 <= rho_1 a_1`, `log2 rho_1 <= 22.196861 (= log2 K_raw)` | `29.5` | **OPEN-REDUCTION** |
| `L_2` (`row_2 = (524288, 279012, 16867)`) | `maxPi_2 <= rho_2 a_2`, `log2 rho_2 <= 22.196861 (= log2 K_raw)` | `32.9` | **OPEN-REDUCTION** |
| `L_3` (`row_3 = (262144, 139506, 8433)`) | `maxPi_3 <= rho_3 a_3`, `log2 rho_3 <= 22.196861 (= log2 K_raw)` | `34.3` | **OPEN-REDUCTION** |
| `L_4` (`row_4 = (131072, 69753, 4216)`) | `maxPi_4 <= rho_4 a_4`, `log2 rho_4 <= 22.196861 (= log2 K_raw)` | `34.8` | **OPEN-REDUCTION** |
| `s=0` core (`conj:Q` proper) | `maxPi_0 <= rho_0 avg` at depth `w_0=67471`, domain `n_0=2097152` | `22.1969` (the whole budget) | **OPEN** (head-depth `w<=21-22` **PROVED**, `rem:proved-q-part`) |

The ladder threshold is the SAME flatness bar at every rung: each `L_s`
demands `rho_s <= K_raw = 2^22.196861` -- the quotient row must be at least
as flat as the primitive row itself. (The `29.5..34.8`-bit column is each
row's *standalone* budget `log2(B*/a_s)`, recorded because it is why the
smaller rows may be easier to prove -- it is NOT the ladder threshold;
at `rho_s ~ 2^29.5` a single rung would already consume the whole `K_raw`.)
So `L_s` is a **REDUCTION in depth only** (`w_s = w/2^s`, halving toward the
proved head-depth base cases, `rem:proved-q-part`), not a weakening of the
flatness requirement. Trivial-cost
consistency of the ladder itself -- i.e. that `(E)`/`(D)` correctly charges
every nonprimitive stratum to `L_0..L_4` with no sixth object -- is **PROVED**
(Sec. 2-3); it is only the *bounding* of `Pi_1..Pi_4` (and of `Pi_0` itself,
`conj:Q` proper) that remains open.

---

## 7. Frame verdict (honest, verbatim)

Verbatim from the Lane C compiler design note's Sec. 9 ("Frame verdict
(honest)"), numbers unchanged by this PR's rounding-policy adoption (Sec. 5
tightens the design note's own `>= 4771896` to an exact `= 4771896`, in the
same direction):

> **The compiler CLEANS the wall's statement and PROVES the descent
> structure; it does NOT shrink the primitive core.** Precisely:
>
> 1. It replaces the synthesis note's deferred phrase *"stabilized targets
>    require image-level quotient descent or another explicit ledger
>    payment"* with an EXACT finite object: identity `(E)`/`(D)`, five
>    subset-primitive rows, and printed per-rung budget shares.
> 2. Every nonprimitive stratum (`j=1..16`, `j=21`) is reduced to the four
>    shallower rungs `s=1..4`, which are **budget-negligible**: even
>    pessimistically (each no flatter than the primitive row) they consume
>    `Delta = 35623.86` of `K_raw = 4807520` (`0.741%`), leaving `>= 4771896`
>    (`99.259%` of `K_raw`, `log2 = 22.1861` bits, a loss of only `0.0107`
>    bit) for the primitive core `s=0`. So the finite certificate's primitive
>    cell keeps essentially the full `K_raw = 4807520` budget; the compiler
>    does not buy the primitive cell any meaningful slack.
> 3. What it DOES buy: (a) rigor -- the nonprimitive strata are now
>    *provably* not the obstruction **under `L_1..L_4`** (which bound them by `Delta`), so the wall
>    is honestly reduced to `maxPi_0`; (b) a descent LADDER whose rungs step
>    the depth `w` down by factors of two toward the proved head-depth base
>    cases (`w<=21`), i.e. an explicit multiscale scaffold for the eventual
>    primitive proof; (c) the reason the reach stops at `s=4`: `v2(m_safe)=4`,
>    a hard cap set by the row.
>
> **Verdict: the compiler shrinks the STATEMENT (full-target wall ->
> subset-primitive `conj:Q` core `maxPi_0` + a paid 4-rung ladder), not the
> primitive BUDGET (remaining `4771896` of `4807520`, a `0.0107`-bit loss).**
> Both were flagged valuable by the task; this is the "cleans its statement"
> outcome, quantified to the integer, and it is the `GREEN` outcome
> grande_finale's Rung audit asks for: *remaining work genuinely primitive.*

---

## 8. Non-claims

This audit does **not** prove any of the following:

```text
conj:Q (grande_finale.tex \label{conj:Q}),
L_1, L_2, L_3, or L_4 (Sec. 6),
U(1116048) <= B*,
that the frontier edge (1116047, 1116048) moves in either direction.
```

It also does **not** touch `conj:BC` (split-pencil census, `\label{conj:BC}`)
or `conj:SP` (primitive shift-pair control, `\label{conj:SP}`).

**This audit is distinct from the packet family's existing lower-side
audit -- do not conflate them.** `experimental/data/certificates/frontier-
adjacent/kb_mca_v1.packet.json` already carries a `.rung_margin_audit` block
-- the periodic **FLOOR** audit (`Gfloor`/`Gceil`/`Rem`/`Plant` slack profiles
vs. the deep-point threshold `Theta`, across `c = 2^0..2^20`), verdict
`GREEN`. That is a *lower-side* refutation check; this note is the
*complementary upper-side* check. This PR does **not modify**
`kb_mca_v1.packet.json` -- the new ledger ships as a sibling file,
`kb_mca_conjq_rung_audit_v1.json`, key `conjQ_rung_audit`.

| | Audit 1 (`kb_mca_v1.packet.json` `.rung_margin_audit`) | This audit (`conjQ_rung_audit`) |
|---|---|---|
| side | lower / periodic FLOOR mass | upper / `conj:Q` max-FIBER |
| object | `binom(N,m)/\|B\|^w` floors vs. `Theta` | quotient-pulled-back fibers charged to rungs |
| "exceeds" means | periodic refutation (edge moves) | cannot refute; conditional on `L_1..L_4` |
| verdict | `GREEN` | `GREEN` |

Both `GREEN`: no rung in either audit exceeds its budget, so the adjacent
`(1116047, 1116048)` conjecture is not falsified for a paid periodic reason,
and the edge does not move.

---

## 9. Verifier contract

`experimental/scripts/verify_kb_mca_conjq_rung_audit.py` is zero-arg,
stdlib-only, deterministic, and supports `--tamper-selftest`. Five gates:

- **gate i** -- recomputes the entire `j=0..21` table (Sec. 4) from raw
  constants with exact big-integer arithmetic and diffs every field against
  the shipped JSON.
- **gate ii** -- binomial/moment identity spot checks: `w_j = floor(w/2^j)`;
  the divisibility chain `2^s | m_safe` for `s=0..4`; `v2(m_safe) == 4`
  exactly.
- **gate iii** -- exhaustive toy-validation replay of identity `(D)` on 4 toy
  rows, including the named `F_17` witness (`M={1,2,4,10}`, `z=(0,2)`) and a
  genuine (non-trivial) coset row (`n=32`, `alpha=5`, over `F_97`).
- **gate iv** -- the relaxation-failure check of Sec. 2 on one toy row.
- **gate v** -- conservative-rounding consistency: `charge=35624`,
  `residual=4771896`, `charge + residual == K_raw`.

Expected runtime under 90s; expected exit code `0`. A nonzero exit code means
a genuine mismatch, not a judgment about `conj:Q` itself -- this verifier
never gates on whether `conj:Q` is true, only on whether this PR's own
arithmetic is internally consistent and matches its shipped JSON.

---

## Refs

- `experimental/notes/thresholds/cap25_v13_qfin_primitive_wall_synthesis.md`
  -- constants, the `F_17` witness, the moment barrier, and route 3 ("Next
  exact wall") that this note executes.
- `experimental/grande_finale.tex` -- `conj:Q` (`\label{conj:Q}`), `conj:BC`
  (`\label{conj:BC}`), `conj:SP` (`\label{conj:SP}`), `rem:proved-q-part`,
  `prop:mode-null-false`, and the Work-Plan "Rung audit" paragraph this note
  executes.
- `experimental/rs_mca_proximity_prize_status.md` -- row authority for the
  moved v13 raw pair `(1116047, 1116048)` and its `22.2`-bit fail margin.
- `experimental/data/certificates/frontier-adjacent/kb_mca_v1.packet.json`
  -- the sibling packet (not modified by this PR); its `.rung_margin_audit`
  is the distinct lower-side periodic-floor audit (Sec. 8).
- `experimental/data/certificates/frontier-adjacent/kb_mca_conjq_rung_audit_v1.json`
  -- this audit's data, key `conjQ_rung_audit`.
- `experimental/scripts/verify_kb_mca_conjq_rung_audit.py` -- this audit's
  verifier (Sec. 9).
