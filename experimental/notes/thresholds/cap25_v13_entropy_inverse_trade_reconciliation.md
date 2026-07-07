# CAP25 v13: the entropy-inverse skeleton's `trade` is our shift pair -- and the PTE/X8x branch already classified it

Status:
`AUDIT(two-lineage reconciliation of rem:entropy-inverse-skeleton step 2; the zero-cross-reference finding, both directions; the step-3 non-contact; the precision notes)` /
`PROVED(lem:trade-is-shift-pair -- trade = depth-w shift pair, from prop:prefix-rigidity / prop:second-moment / prop:newton already in grande_finale.tex)` /
`OPEN(no claim on prob:entropy-inverse-q; skeleton steps 4-6 untouched; the PTE terminal active_core_count_bound stays TARGET; no asymptotic-Q claim)`.

**Base commit pin:** `upstream/main 53bb5df` ("Add logarithmic moment route to grande finale", 2026-07-07).
All line numbers below are from that commit's `experimental/grande_finale.tex`.
**Verifier:** `experimental/scripts/verify_entropy_inverse_trade_reconciliation.py`
(zero-arg, stdlib-only, `<60s`, `--tamper-selftest`). It checks every cross-reference
claim mechanically (labels at pinned lines; the zero-cross-reference counts; the DAG
node statuses), toy-verifies `lem:trade-is-shift-pair` by enumeration, and checks
`char B > w` at the four deployed rows.

**What this is.** A scoping/reconciliation memo, no new conjecture. `53bb5df` added the
asymptotic-Q block `def:primitive-logmoment` .. `rem:entropy-inverse-skeleton`
(l.752-863). Its step-2 primitive object -- a `signed trade satisfying the first w
moment equations` -- already has **two** formal in-repo lineages that currently have
**zero** cross-references to it, in either direction. This note pins the dictionary,
proves the step-2 = shift-pair identity as a one-page lemma, and scopes the PTE/X8x
branch as the step-3-relevant prior art it is (and is not).

---

## 1. [AUDIT -- headline] Step-2 `trade` names an object with two unconnected in-repo lineages

`rem:entropy-inverse-skeleton` (l.861-863), step 2, verbatim:

> "Second, comparing supports inside a popular fiber to a base support produces
> **signed trades satisfying the first `w` moment equations**."

Neither "signed trade", "popular fiber", nor "base support" is given a formal statement
anywhere in `grande_finale.tex` -- they occur only in this one prose paragraph. But the
object they name is not new to the repo. It has two lineages.

### 1(a). Lineage A -- the shift-pair machinery of `grande_finale.tex` itself (PROVED)

All pre-existing, all proved under their displayed hypotheses:

| label | line | statement (abbrev.) |
|---|---|---|
| `prop:prefix-rigidity` | 660 | `M != M'`, `Phi_w(M)=Phi_w(M')` `=>` `e:=\|M\M'\|=\|M'\M\|>=w+1`; with `R=M cap M'`, `A=ell_{M\M'}`, `B=ell_{M'\M}`, `G=ell_R`: `ell_M-ell_{M'}=G(A-B)`, `deg(A-B)<=e-w-1`. |
| `prop:second-moment` | 676 | `sp_w(e;D')` = # ordered pairs `(A,B)` of monic degree-`e` polys split over disjoint root sets in `D'` with `deg(A-B)<=e-w-1`; `sum_z N_w(z)^2 = C(n,m) + sum_{e>=w+1} sum_{R} sp_w(e;D\R)` (a bijective re-encoding of off-diagonal same-prefix pairs by `(R,(A,B))`). |
| `prop:newton` | 551 | if `char B > w`, `Phi_w` is triangularly equivalent to the power sums `(p_1,...,p_w)`; same fibers. |
| `prop:sp-pullback` | 1084 | the formal term "depth-`w` shift pair of degree `e`" (`deg(A-B)<=e-w-1`); quotient pullback. |
| `thm:coeff-quotient-extract` | 1130 | *"Let `(A,B)` be a depth-`w` shift pair of degree `e` over `D`: `A=ell_S, B=ell_T, S cap T = emptyset, deg(A-B)<=e-w-1`."* |
| `prop:top-stratum-quotient-sieve` | 1163 | the `e=w+1` (top) stratum: primitive residual = constant-shift pairs `A, A-lambda`, `lambda in B^x`, `s(A,B)=1`. |
| `prop:gamma2-ledger` | 1199 | the `Gamma_2` quotient/primitive split; *"SP is exactly the task of bounding the last displayed summand after quotient-pulled-back pairs have been paid."* |
| `thm:sp-proper` | 1822 | unconditional per-stratum ceilings `P_e^quot + P_e^prim <= T_e(n,m)`. |

**Our own two OPEN PRs already sit on exactly this object, one level down:** PR #393
(`bc-l4-interior-chart-to-q`) and PR #395 (`bc-l4-curve-second-moment`). PR #395's
Theorem C1, verbatim from its body: *"the curve second moment IS `prop:second-moment`
at depth `w+1` restricted to `Gamma`, i.e. the depth-`(w+1)` shift-pair ledger on the
curve."* Same shift-pair machinery, but restricted to one BC-chart curve `Gamma`
(target `prob:saturated-bc`), **not** the ambient `Fib_w(z)` system asymptotic Q needs.
Adjacent, not overlapping. (Both PR bodies use the word "trade" zero times -- checked by
hand against the two PR bodies, not by the offline verifier -- so even our nearest work
never verbally connects to the skeleton's vocabulary.)

**Sister-manuscript instance (integrated):** `prob:capg-shiftpairs`
(`cap25_cap_v13_raw.tex` l.9667) / `thm:capg-second-moment` (l.9575) with the toy ledger
`experimental/notes/m1/capg_shiftpairs_primitive_ledger.md` and its verifier -- the same
`sp_w(e;D')` object enumerated at 10 small rows. `grande_finale.tex` cites this manuscript
as `\bibitem[CAP25v13]` (l.2161).

### 1(b). Lineage B -- the Proximity-Prize DAG's PTE trade branch (mostly PROVED, different method)

`experimental/data/prize-dag/prize_dag.json` (`root: prize` -- the same overall program)
carries a mature classification of the **same** combinatorial primitive under the name
**PTE trade**. Integrated 2026-07-04 (commit `674503f`, "Integrate PR proof packets and
A407 gate"; Allen's clean-rate proof-spine packets per `agents-log.md`), i.e. **three
days before** the entropy-inverse section existed. Node statuses (parsed from the JSON by
the verifier):

| DAG node | status | statement (abbrev.) | method |
|---|---|---|---|
| `x24_char0_dyadic_descent` | PROVED | over `mu_n(C)`: disjoint `h`-subsets with equal first `h-1` elem. symmetric sums exist only for `h` a power of two, and then only as full `mu_h` fibers. Char-0 dyadic trades are exactly cyclic full-fiber trades. | char-0 descent |
| `star_pte_lemma` | PROVED | see side-by-side below | elementary locator factorization |
| `x81_minimal_trade_square_shift` | PROVED | a `2h`-support underlies a minimal `h`-trade iff its locator is `S(X)^2-lambda`, `S` monic degree `h`, `lambda` a nonzero square (odd char) -- the square-shift normal form. | normal form |
| `x82_square_shift_certifier_keys` | PROVED | scaling-orbit / certifier-key normalization for square-shift supports. | dedup discipline |
| `x83_uniform_square_shift_obstruction_gate` | PROVED | combined with X24: every finite-row minimal `h`-trade is EITHER a char-0 trade = full `mu_h` fiber = PAID (only at power-of-two `h`), OR a `p`-specific norm-gate event (`p \| ` cyclotomic norm of a cleared obstruction). | good reduction |
| `h3_param_lemma` | PROVED | `h=3` base object: nontrivial affine triples with equal top-2 symmetric sums = explicit deg-2 rational family. | parametrization |
| `h4_terminal_dichotomy` | PROVED | `h=4`: exactly one of {antipodal quotient = PAID cyclic pullback, top-level 8-sparse cyclotomic norm gate}. | good reduction |
| `active_core_count_bound` | **TARGET** | the terminal node: `H=mu_n, n=2^s, char p>=n^2, h in [3,(log2 n)^2]`; count anchored cores not charged by the full strip. | (open) |
| `h4_sparse_norm_gate` | **TARGET** | the remaining `h=4` obstruction: bound/exclude primes `p \| Res(Phi_n,f)` for `f` an 8-sparse exponent word. | (open) |

The method is **char-0 dyadic descent + good reduction** (cyclotomic-norm exceptional
primes) -- **not** a Fourier / uncertainty-principle argument. Write-ups:
`experimental/notes/roadmaps/{w_a_star_pte_lemma,x81_minimal_trade_square_shift,x32_h4_terminal_dichotomy}.md`;
method framing in `critical_path_status_2026_07_04.md`.

### 1(c). The pin: `star_pte_lemma` and `prop:prefix-rigidity` are the same statement, independently derived

`prop:prefix-rigidity` (l.660-673, verbatim):

> "If `M != M'` are `m`-subsets of `D` with `Phi_w(M)=Phi_w(M')`, then
> `|M\M'| = |M'\M| >= w+1`. If equality holds, then `ell_{M\M'}-ell_{M'\M}` is a nonzero
> constant. [Proof] Let `R=M cap M'`, put `A=ell_{M\M'}`, `B=ell_{M'\M}`, and `G=ell_R`.
> If `e=|M\M'|`, then `ell_M-ell_{M'}=G(A-B)`. ... Hence `deg(A-B) <= e-w-1`."

`star_pte_lemma` (`prize_dag.json`, verbatim):

> "For any family of monic degree-A locators with roots in D sharing top t coefficients,
> and any base member S0: every member S decomposes canonically as `S = C u P`,
> `S0 = C u Q` with `|P| = |Q| >= t+1` (unless S = S0) and `e_r(P) = e_r(Q)` for `r <= t`.
> Proof: `L_S - L_S0 = L_C (L_P - L_Q)`; the degree constraint forces the top-t agreement;
> `h <= t` forces `L_P = L_Q`."

Dictionary: `(S,S0) <-> (M,M')`, `C <-> R=M cap M'`, `P <-> M\M'`, `Q <-> M'\M`, `t <-> w`,
`L_C(L_P-L_Q) <-> G(A-B)`, `|P|=|Q|>=t+1 <-> e>=w+1`, `e_r(P)=e_r(Q) for r<=t <-> Phi_w`
equality (elementary-symmetric / power-sum reading). The same lemma up to one bookkeeping
addendum: identical hypotheses (monic locators, roots in `D`, top-`t`/`w` coefficient
agreement, `S != S0` / `M != M'`; and -- the point -- *no* characteristic hypothesis in
either, the elementary-symmetric reading being char-free), and the same one-line proof via
`L_C(L_P-L_Q)` and the degree count. The only asymmetry is emphasis: `prop:prefix-rigidity`
additionally records the `e=w+1` constant-shift case, while `star_pte_lemma` states the
`e_r(P)=e_r(Q)` trade-moment agreement that `prop:prefix-rigidity` carries inside its proof.
Two lineages, two proofs, no cross-reference between them.

### 1(d). Scope pin -- three different axes; where the PTE branch is (and is not) a step-3 input

The skeleton and the PTE branch live on **different axes**; conflating them is the trap.

| axis | meaning | skeleton | PTE branch | deployed rows |
|---|---|---|---|---|
| `r` | log-moment order (# fiber copies compared) | `r <= (log n)^A`, unbound `A` | not on this axis | -- |
| `w` | fiber depth (# matched moment equations) | `w log\|B\|/r = o(n)` (can be `~n polylog`) | `w = h-1` | `67471` (KB), `67447` (M31) |
| `e = h` | trade part-size (`\|P\|=\|Q\|`, support `2h`); `e >= w+1` | `>= w+1` in a depth-`w` fiber | `h in [3,(log2 n)^2]`, i.e. `<=441` for `n=2^21` | `>= w+1 >= 67472` |

The PTE classification is a statement on the `e=h` (support) axis, complete for
`h in [3, (log2 n)^2] = [3, 441]` (`n=2^21`), i.e. depth `w = h-1 <= 440`. A minimal
(`e=w+1`, top-stratum) trade of part-size `h` is exactly `grande_finale`'s depth-`(h-1)`
top stratum. Therefore:

- **Where it IS a step-3-relevant input:** in the low-support / small-depth window
  `w = h-1 <= (log2 n)^2 - 1 ~ 440`, the PTE branch supplies a rigorous, mostly-proved
  answer to step 3's own stated goal ("remove low-support primitive trades") -- by
  char-0 descent + good reduction, a route the skeleton never mentions.
- **Where it is NOT:** at the deployed frontier depth `w ~ 6.7x10^4`, every trade in the
  fiber has part-size `>= w+1 >= 67472`, two orders of magnitude above the PTE range
  `<=441`; the PTE classification does not reach those trades. And even inside its own
  range the branch is not closed -- `active_core_count_bound` and `h4_sparse_norm_gate`
  are still `TARGET`.

So the PTE branch is **not** a shortcut that finishes step 3 at deployed scale, but it is
real, checkable, closely-relevant prior art for the low-support sub-step, and it pins
exactly where a genuine Fourier / entropy argument would have to take over. This
connection currently exists nowhere in the repo (see the zero-cross-reference grep in the
verifier, gate i).

---

## 2. [PROVED] The dictionary lemma: step-2 trade = depth-`w` shift pair

**Lemma `lem:trade-is-shift-pair`.** Fix a row `(F,D,k)`, depth `1 <= w < m <= n`, and a
prefix value `z`; let `Fib_w(z) = {M subset D : |M|=m, Phi_w(M)=z}`.

*(Forward: fiber pairs are shift pairs.)* For `M0, M in Fib_w(z)`, `M0 != M`, put
`R = M0 cap M`, `S = M0\M`, `T = M\M0`, `e = |S| = |T|`. Then `(A,B) := (ell_S, ell_T)` is
a depth-`w` shift pair of degree `e` in the exact sense of `thm:coeff-quotient-extract`:
`A,B` monic of degree `e`, split over the disjoint root sets `S,T subset D\R`,
`S cap T = emptyset`, `e >= w+1`, and `deg(A-B) <= e-w-1`. Equivalently (`prop:newton`,
valid when `char B > w` -- the same condition, since `D \subseteq B \subseteq F` forces
`char B = char F`), the signed trade `+S / -T` satisfies the first `w` power-sum
equations `sum_{x in S} x^i = sum_{x in T} x^i`, `i = 1,...,w`.

*(Converse: shift pairs over a fixed common part are fiber pairs.)* Fix `R subset D` and
any depth-`w` shift pair `(A,B)=(ell_S,ell_T)` of degree `e = m-|R|` over `D\R`
(`S,T subset D\R`, `S cap T = emptyset`, `|S|=|T|=e`, `deg(A-B) <= e-w-1`). Then
`M0 := R u S` and `M := R u T` are distinct members of the common fiber `Fib_w(z)`,
`z = Phi_w(M0) = Phi_w(M)`, with `M0 cap M = R`. The two constructions are mutually
inverse: they are a bijection between off-diagonal fiber pairs with common part exactly
`R` and depth-`w` shift pairs of degree `m-|R|` over `D\R`.

**Proof.** Both directions are the encoding already carried out inside
`prop:prefix-rigidity` and `prop:second-moment`, read in the two directions. Since
`ell_{M0} = ell_R ell_S` and `ell_M = ell_R ell_T`, writing `G = ell_R` gives
`ell_{M0} - ell_M = G(A-B)`. By definition `Phi_w(M0) = Phi_w(M)` is the agreement of the
leading term and the next `w` coefficients of `ell_{M0}` and `ell_M`, i.e.
`deg(ell_{M0}-ell_M) <= m-w-1`; as `deg G = m-e`, this is exactly `deg(A-B) <= e-w-1`. If
`e <= w` this bound forces `A = B`, impossible for disjoint nonempty root sets, so
`e >= w+1` (this is `prop:prefix-rigidity`). The converse multiplies `deg(A-B) <= e-w-1`
by `G` to recover `deg(ell_{M0}-ell_M) <= m-w-1`, i.e. `Phi_w(M0) = Phi_w(M)`. For the
power-sum reading, `prop:newton` gives that (when `char B > w`) `Phi_w` is triangularly
equivalent to `(p_1,...,p_w)`; since `p_i(M0) = p_i(R)+p_i(S)` and `p_i(M) = p_i(R)+p_i(T)`,
prefix equality is `p_i(S) = p_i(T)` for `i=1,...,w`. The top stratum `e = w+1` gives
`deg(A-B) <= 0`, i.e. the constant-shift pairs `A, A-c` of `prop:second-moment`. `[]`

**Consequence, stated carefully.**

1. **Step 2 = the off-diagonal shift-pair strata of `prop:second-moment`.** The trade
   population of one popular fiber `Fib_w(z)` of size `N` (base `M0`) is exactly
   `{(M0\M, M\M0) : M in Fib_w(z)\{M0}}`, size `N-1`; the aggregate over all `z` and all
   common parts `R` is exactly `sum_z N_w(z)^2 - C(n,m) = sum_{e>=w+1} sum_R sp_w(e;D\R)`.
   The `signed` label is the `+S / -T` indicator; the `first w moment equations` are the
   Newton/power-sum reading of `deg(A-B) <= e-w-1`.
2. **The power-sum reading is valid at every deployed row.** `prop:newton` needs
   `char B > w`. At the four deployed rows `char B = p ~ 2^31 ~ 2.1x10^9` and
   `w in {67471, 67447}`, so `char B > w` holds with a `~10^4x` margin (verifier gate iii,
   big-int). The `first w moment equations` reading is therefore available at the scale the
   section cares about.
3. **Step 4 quantifies over `thm:sp-proper` / `prop:gamma2-ledger`'s object.** Step 4's
   "entropy-small-doubling trade population" is a population of exactly the shift pairs
   whose per-stratum ceilings `thm:sp-proper` bounds and whose quotient/primitive split
   `prop:gamma2-ledger` and `def:primitive-logmoment` already organize (`Gamma_r^prim`).
4. **Net.** Skeleton **steps 1-2 have exact in-repo formalizations** (`lem:trade-is-shift-pair`
   + `prop:second-moment` for step 2; `def:primitive-logmoment` / `thm:logmoment-equivalence`
   for the step-1 popular-fiber excess). **Step 3 has the PTE branch as prior art in the
   log-support scope** (Sec.1d). **Only steps 4-6 lack any in-repo object** -- "entropy
   Balog-Szemeredi-Gowers trade population", "PFR coset progression", "slice-derivative
   lemma" appear in no other file. Say it plainly: the formalization gap is steps 4-6, not
   steps 1-3.

---

## 3. [AUDIT] Step-3 non-contact: our L1 route-kill does not touch Tao05

`rem:entropy-inverse-skeleton` step 3 cites `\cite{Tao05}` (l.862; bibitem l.2182) -- Tao's
uncertainty principle for cyclic groups of prime order: `|supp(f)|*|supp(f^)| >= p` for
nonzero `f: Z/pZ -> C`, `p` **prime**, **additive** Fourier transform. Our integrated
route-kill (`experimental/notes/l1/l1_coset_mixed_vacancy_threshold.md` l.123-127, verbatim)
reads: *"The tempting char-`0` Fourier/uncertainty bound (`a`-sparse `=> <= a-1` roots) is
UNSOUND over `F_p` (`5 + h + 2h^3` has 3 roots in `mu_11 subset F_23`), so `|S| >= 2` is
not Fourier-controlled."* This refutes a **folk heuristic** ("a sparse polynomial has few
roots") by a **multiplicative-subgroup** root count in `mu_11 subset F_23^x` -- a different
group action (multiplicative vs. additive), a different claim (root-counting vs. a support
product inequality), and it kills a heuristic, not a theorem: the L1 note never mentions
Tao (verifier: `grep -c Tao` on that file `= 0`), and Tao05 is a published, true theorem
that nothing here refutes. So step 3's intended input is **unrefuted in-repo**; the L1
route-kill is simply about a different object. (A real step-3 attempt still has to pin
which object is "the function on `Z/pZ`" -- plausibly a signed-trade indicator read on the
prime-order base field `B`, not on `D` (order `2^21`, a prime power, to which Tao05 does
not apply). Not settled here.)

---

## 4. [AUDIT] Friendly precision notes for `prob:entropy-inverse-q` (l.823-835)

Small notation gaps in the problem statement, offered for the next revision (not
criticism -- these are the kind the maintainer closes same-day). Each is verified against
the base commit.

- **`V, T, rho, R, X` are fresh local notation, never tied to `Fib_w`/`D` by a stated map.**
  `\rho(` and `moment-curve column` occur only inside this new inverse-theorem block
  (`prob:entropy-inverse-q` and the adjacent `prop:vandermonde-kills-low-rank`, l.826-862;
  5 and 3 hits) -- never in the earlier `Phi_w`/`Fib_w`/`D` material. The
  tie to the earlier `Phi_w`/`Fib_w(z)` objects is asserted only by the prose "after
  quotient, planted, ... cells have been removed", which describes a reduction procedure,
  not a bijection. A one-line "let `T = ...`, `rho = ...`, identifying `V` with the columns
  of ..." would close it.
- **The column dimension `R` collides with `prop:moment-sandwich`'s max-fiber-ratio `R`**
  (l.705, `R = |B|^w max_z mu(z)`). Two different `R`'s a few pages apart; worth a rename
  (e.g. `R -> d` for the column dimension).
- **`X` is declared and then never used.** "Let `X` be a fixed-density singleton or
  signed-profile selector on `T`" (l.830), but the conclusion (l.831-834) speaks only of a
  "positive-rate set `U subset T`", never connecting `U` to `X`. Most likely intended:
  `U = supp(X)`. Not stated.
- **`A` in `r <= (log n)^A` is unbound** -- no quantifier (l.830).
- **The conclusion's "affine span has rank `o(n)`" refers to `{v_y : y in U}`** by analogy
  with `prop:vandermonde-kills-low-rank` (l.841) two paragraphs later, but the antecedent
  of "whose affine span" is grammatically the progression, not the column set. A pointer to
  `prop:vandermonde-kills-low-rank` would disambiguate.

---

## 5. Open problems and non-claims

- **No claim on `prob:entropy-inverse-q` itself.** It stays OPEN. This note neither proves
  nor refutes it and does not move the asymptotic-Q frontier.
- **Skeleton steps 4-6 are untouched.** No in-repo object formalizes the entropy-BSG trade
  population, the PFR coset progression, or the slice-derivative push-back; the authors
  themselves flag steps 5-6 as "the remaining theorem, not a completed proof" (l.863).
- **The PTE terminal node stays open.** `active_core_count_bound` and `h4_sparse_norm_gate`
  are `TARGET`; the PTE branch classifies low-support trades but does not close even its own
  range.
- **No asymptotic-Q claim, no new conjecture.** `lem:trade-is-shift-pair` is the only new
  proved statement, and it is a one-page corollary of material already in the paper.

---

## 6. Weave -- what is already claimed nearby (refs re-grepped at base `53bb5df`)

- **PR #393** (`bc-l4-interior-chart-to-q`, holmbuar, OPEN) and **PR #395**
  (`bc-l4-curve-second-moment`, holmbuar, OPEN) -- the curve-restricted shift-pair
  instances (`prop:second-moment` at depth `w+1` on a BC-chart curve `Gamma`, target
  `prob:saturated-bc`); adjacent, not overlapping (Sec.1a).
- **PR #392** (`thresholds-moment-floor-reconciliation`, holmbuar) and **PR #394**
  (`lean-gf-composite-descent`, holmbuar) -- sibling threshold/Lean precision packets on
  pre-existing props; no contact with the new block.
- **PTE/X8x lineage** -- integrated 2026-07-04 (`674503f`); Allen's clean-rate proof-spine
  packets (PTE and square-shift trades, good-reduction/GCD certification), DAG maintained
  by AllenGrahamHart, replay by LegaSage/Ken, integrated by przchojecki. Credited here as
  the prior art for step 3's low-support sub-step.
- **PR #389/#390/#391** (DannyExperiments LQ top-seam; scottdhughes L1 W3 certificates) --
  no contact.
- **Zero-cross-reference finding.** `grande_finale.tex` mentions no PTE/x81/x82/x83/
  star_pte/h3/h4 node (whole-word `PTE = 0`; the 3 case-insensitive hits are the substring
  in "at**te**m**pte**d"); `cap25_cap_v13_raw.tex` mentions no `grande_finale`/`logmoment`/
  `entropy-inverse`; no roadmap note mentions `entropy-inverse`/`logmoment`. All asserted
  `== 0` mechanically by the verifier, both directions.
