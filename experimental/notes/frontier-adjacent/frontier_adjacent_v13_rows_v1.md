# Frontier-adjacent packet family: exact adjacent-budget ledgers and the complete rung-margin audit for the four deployed v13 rows

> **v14 status note (2026-07-05).** The KB-MCA and M31-MCA `(a0, a0+1)` pairs
> analyzed throughout this note's original content below are **(v13 identity
> pairs -- superseded for the two MCA rows by the v14 composition; retained
> as the strategy-note Audit-1 record)**. Upstream PR #310, commit
> `f049b91`, composes `lem:v13f1-identity-prefix-floor` with
> `prop:quantitative-deep-list-floor` to move the two MCA rows' frontier
> pairs to `(1116047, 1116048)` (KB) and `(1116023, 1116024)` (M31); the two
> **list** rows (KB list, M31 list) are unchanged. Nothing in the original
> v13-pair content below is altered by this note -- see "V14 moved-frontier
> addendum (2026-07-05)" at the end of this file for the full re-audit at
> the moved pairs.

**This note executes Audit 1 (rung margins) of
`experimental/cap25_v13_missing_inputs_strategy.md` sec 2.1 for all four
deployed v13 adjacent rows, and packages the result as a complete four-row
frontier-adjacent packet family (agents.md progress items 1-2).**

**Concurrent-tracks status: supersedes-its-original-framing (2026-07-05).**
Upstream PR #310 (latifkasuli) originally packaged a KoalaBear-MCA-row
adjacent window at $(1{,}116{,}043, 1{,}116{,}044)$ (status
`UNDECIDED_WINDOW_OPEN`); where the two overlapped (KB MCA at $a_0+1$), its
reported conversion-route margin 5.4985 bits was consistent with this note's
exact bracket $[2^{5.4}, 2^{5.5})$ — an independent cross-validation
**against #310's original v13-pair framing**. PR #310's own commit
`f049b91` ("Material correction: quantitative-deep-list-floor flips
1116044–1116047") later composed `lem:v13f1-identity-prefix-floor` with
`prop:quantitative-deep-list-floor` and moved both MCA rows' frontier pairs
forward; #310's original framing is superseded by its own v14 correction
(see "V14 moved-frontier addendum (2026-07-05)" at the end of this file).
This family additionally covers the KB-list and both Mersenne-31 rows, the
complete 21-scale x 3-profile rung-margin audit at both $a_0$ and $a_0+1$,
the applicability-gap tables, and the named-input targets; no dependency on
#310 is taken for any of that, and the v14 addendum below independently
re-derives the moved-pair numbers from $n,k,p$ alone rather than from
#310's PR text.

## Claim

For each of the four deployed v13 frontier rows (KoalaBear MCA, KoalaBear
list, Mersenne-31 MCA, Mersenne-31 list) at the conjectured one-step adjacent
pair $(a_0, a_0+1)$:

1. Every currently-payable cell of the exact adjacent-budget ledger is printed
   *exactly* (pure integer arithmetic), and every open cell is stated as a
   **named input with the exact integer or bit target it must hit** for
   $U(a_0+1)\le B_*$ (§"Named-input targets" below).
2. The **complete rung-margin audit** (Audit 1 of the strategy note) is
   executed: every dyadic scale $c=2^j$, $j=0,\dots,20$, in all three slack
   profiles the v13 tex defines (graded prefix floor, quotient-remainder
   floor, planted quotient-core), at **both** $a_0$ and $a_0+1$, for all four
   rows. Result: **no floor that covers an agreement $\ge a_0+1$ fires or is
   within one bit of the budget** in any row (`GREEN`).

**This is explicitly NOT a safety claim.** $U(a_0+1)\le B_*$ is not
established for any row. This note supplies (a) the unsafe lower staircase
$L(a_0)>B_*$ (already `PAID_BY_EXACT_CERTIFICATE`, unchanged from
`prop:v13f1-identity-frontier`), (b) an exact-integer exclusion of the
periodic/quotient side as a source of a cheap counterexample to the adjacent
conjecture, and (c) the exact named-input targets that remain open. The
aperiodic (`prob:band`), L1 (`prob:v13-l1-residuals`,
`prob:v13-primitive-image-fiber`), and sparse (`prob:mutual`/`prob:sparse-mutual`)
cells are untouched and remain the open research problems they were before
this note.

## Status

- **`AUDIT`** for every arithmetic/verification claim in this note (the
  ledger, the rung-margin scan, all cross-checks): every verdict-bearing
  comparison is a pure integer comparison, independently re-derived by this
  packet family's own verifier
  (`experimental/scripts/verify_frontier_adjacent_v13_rows.py`), not merely
  transcribed. **Scope note on the descent-loss table:** its input, the
  per-row c=1 fail-margin $M$, is independently re-derived and gated (G5's
  `cross_check_c1_identity_margins`); the table's derived per-rung loss
  ceilings ($2^{M/21}$, $2^{M/\text{nondegenerate\_graded\_rungs}}$) are exact
  arithmetic from that margin and are hand-confirmed correct, but are not
  separately re-derived and gated by the verifier.
- **`CONDITIONAL_ON_NAMED_INPUT`** for the named-input targets section: each
  open ledger cell is reduced to an exact integer or bit-budget target, not a
  proof.
- **`CONJECTURAL_WITH_FALSIFIER`** for the overall "$a_0+1$ is the first safe
  agreement" statement (`prob:v13f1-frontier`, an open problem, not a
  theorem). **Falsifier:** exhibit, at $a_0+1$, more than $B_*$ MCA-bad finite
  slopes (MCA rows) or more than $B_*$ list codewords (list rows) -- e.g. a
  prefix-fiber of size $>B_*$, or an aperiodic residue-line packing exceeding
  the aperiodic-cell $n^C$ ceiling, or (per this note's own audit) a rung that
  turns out to fire or go tight at $a_0+1$ under a slack profile not yet
  scanned.

No `COUNTEREXAMPLE_NEW_FLOOR` is triggered anywhere in this note.

## Parameters

Shared: $n=2^{21}=2{,}097{,}152$, $k=2^{20}=1{,}048{,}576$, $\rho=k/n=1/2$.
Convention (`def:v13-staircase`): $B_*=\lfloor \varepsilon^* Q\rfloor$;
agreement $a$ is safe iff $N(a)\le B_*$; identity-prefix exponent $w=a-K$; MCA
rows use $K=k+1$ then the deep-point conversion (`thm:A`), list rows use
$K=k$.

| row | kind | $p$ | $q_{\rm line}=Q$ | $\varepsilon^*$ | $a_0$ | $a=a_0{+}1$ | $K$ | $w_a=a-K$ | $r=n-a$ |
|---|---|---|---|---|---:|---:|---:|---:|---:|
| KB MCA | mca | $2{,}130{,}706{,}433$ | $p^6$ (186-bit) | $2^{-128}$ | $1{,}116{,}043$ | $1{,}116{,}044$ | $k{+}1=1{,}048{,}577$ | $67{,}467$ | $981{,}108$ |
| KB list | list | $2{,}130{,}706{,}433$ | $p^6$ | $2^{-128}$ | $1{,}116{,}046$ | $1{,}116{,}047$ | $k=1{,}048{,}576$ | $67{,}471$ | $981{,}105$ |
| M31 MCA | mca | $2{,}147{,}483{,}647$ | $p'^4$ (124-bit) | $\mathbf{2^{-100}}$ | $1{,}116{,}021$ | $1{,}116{,}022$ | $k{+}1=1{,}048{,}577$ | $67{,}445$ | $981{,}130$ |
| M31 list | list | $2{,}147{,}483{,}647$ | $p'^4$ | $\mathbf{2^{-100}}$ | $1{,}116{,}022$ | $1{,}116{,}023$ | $k=1{,}048{,}576$ | $67{,}447$ | $981{,}129$ |

Exact line fields: $q_{\rm kb}=p^6=93{,}571{,}093{,}019{,}388{,}561{,}295{,}270{,}373{,}781{,}649{,}880{,}353{,}786{,}165{,}192{,}103{,}559{,}169$;
$q_{\rm m31}=p'^4=21{,}267{,}647{,}892{,}944{,}572{,}736{,}998{,}860{,}269{,}687{,}930{,}881$.
KoalaBear $D\subseteq\mathbb F_p^\times$ multiplicative subgroup, $\mathbb F=\mathbb F_{p^6}$
(sextic). Mersenne-31 "line round" $D=\chi(\text{twin coset})$ on the norm-one
torus, $\mathbb F=\mathbb F_{p'^4}$ (QM31 quartic) -- **not** a multiplicative subgroup.

**Budgets** ($B_*=\lfloor\varepsilon^* q_{\rm line}\rfloor$), exact:

$$B_*^{\rm KB}=\big\lfloor 2^{-128}p^6\big\rfloor=\mathbf{274{,}980{,}728{,}111{,}395{,}087}\quad(=2^{57.932\ldots},\ \text{58-bit})$$
$$B_*^{\rm M31}=\big\lfloor 2^{-100}p'^4\big\rfloor=\mathbf{16{,}777{,}215}=2^{24}-1\quad(24\text{-bit})$$

> **`AUDIT-1` (the $\varepsilon^*$ carve-out `agents.md` omits).** `agents.md`
> L43 frames the budget universally as $B_*=\lfloor 2^{-128}q_{\rm
> line}\rfloor$. This is **wrong for the two Mersenne-31 rows**:
> $q_{\rm m31}=p'^4<2^{124}<2^{128}$, so at $\varepsilon^*=2^{-128}$ the row is
> degenerate ($\lfloor 2^{-128}p'^4\rfloor=0$; `prop:small-field` forces
> $\delta^*_C=0$). The real M31 target is $\varepsilon^*=2^{-100}$
> (`cs25_cap_v12.tex` L4781; the checker script hardcodes `2**100` for M31).
> Any packet that inherits `agents.md`'s single-$\varepsilon^*$ framing
> silently zeroes the M31 rows. The two boxed integers above are the correct
> budgets, and every M31 packet in this family states `epsilon_star = "2^-100"`
> explicitly.

## Relevance to agents.md steering

This note and its packet family map onto `agents.md`'s
"Missing inputs strategy: `(A)` and `(Q)`" section and the "What counts as
progress now" list as follows:

- **Progress item 1** ("exact adjacent upper certificates for the four v13
  frontier rows"): the ledger sections below print every currently-payable
  cell exactly for all four rows (tangent floor, graded-prefix family, dedup
  rule), extending the earlier single-row (KB MCA) skeleton to the full
  four-row family.
- **Progress item 2** ("a complete `frontier-adjacent/*.json` packet family
  replayed by the certificate scanner"): `experimental/data/certificates/frontier-adjacent/{kb_mca,kb_list,m31_mca,m31_list}_v1.packet.json`,
  replayed by `verify_frontier_adjacent_v13_rows.py`.
- **Strategy note sec 2.1, "Audit 1 (rung margins -- pure exact arithmetic, do
  first)"**: this is the note's centerpiece (see below). The strategy note
  asks for exactly this computation as the first, lowest-risk deliverable of
  the `(Q)` program; it is executed here in full (not the earlier
  `c\in\{2,4,8,16,32\}` spot-check, but all 21 dyadic scales and all three
  slack profiles).
- **Strategy note sec 2.1, "Audit 2 (support vs image)"**: the descent
  recursion-loss table below is the exact-integer verification of the note's
  qualitative "$\sim1.2$" / "$\lesssim2$" per-rung-loss tolerance claims.
- **The near-term task list** ("normalize the left edge of `prob:band`
  ... build the exact prefix-collision ledger for `(Q)` ... run the
  rung-margin audit for the four deployed v13 adjacent rows ... test the
  mode-at-null / exchange-compression extremality conjectures"): this note
  discharges the third bullet exactly as scoped ("run the rung-margin audit");
  it does not touch the first, second, or fourth, which remain open.
- **`agents.md`'s $U(a)$ cell list and 5-status taxonomy**
  (`PAID_BY_THEOREM` / `PAID_BY_EXACT_CERTIFICATE` / `CONDITIONAL_ON_NAMED_INPUT`
  / `CONJECTURAL_WITH_FALSIFIER` / `COUNTEREXAMPLE_NEW_FLOOR`): every packet's
  `safe_cell_table` labels all seven cells with this taxonomy; no cell is
  hidden inside a point estimate.
- **The `AUDIT-1` $\varepsilon^*$ carve-out** (immediately above): recorded so
  that no future frontier-adjacent packet silently zeroes the M31 rows by
  inheriting `agents.md`'s universal-$\varepsilon^*$ phrasing.

## The exact adjacent-budget ledger

### Identity-prefix stratum mass $F(a)$ and the fail margin -- `PROVED` + `AUDIT`

$F(a):=\binom{n}{a}\big/|\mathbb B|^{\,a-K}$ is the identity-scale prefix-floor
list mass (`lem:v13f1-identity-prefix-floor`): a guaranteed list of
$\ge\lceil F(a)\rceil$ codewords in $\mathrm{RS}[\mathbb F,D,K]$ at agreement
$a$ -- the known sparse/list mass just below budget, the tightness driver.
Each bracket $[2^L,2^U)$ is exact-integer-verified (10th-power comparison on a
certified 0.1-bit enclosure), and every integer was recomputed two
independent ways (prime-factored `binom_prime` + bracket, and `math.comb` +
`Decimal.ln`); they agree to $<0.01$ bit.

| row | $F(a)$ | $F(a_0)$ | row threshold $\Theta$ | cert **fail** margin $\Theta/F(a)$ | $B_*/F(a)$ (literal) |
|---|---|---|---|---|---|
| KB MCA | $[2^{160.4},2^{160.5})$ | $[2^{191.6},2^{191.7})$ | $\tfrac{q+k}{k}=[2^{165.9},2^{166.0})$ | $[2^{5.4},2^{5.5})\approx\mathbf{5.5}$ | $[2^{-102.6},2^{-102.5})\approx-102.5$ |
| KB list | $[2^{35.9},2^{36.0})$ | $[2^{67.0},2^{67.1})$ | $\tfrac{q}{2^{128}}=[2^{57.9},2^{58.0})$ | $[2^{22.0},2^{22.1})\approx\mathbf{22.0}$ | $[2^{22.0},2^{22.1})\approx+22.0$ |
| M31 MCA | $[2^{83.1},2^{83.2})$ | $[2^{114.2},2^{114.3})$ | $\tfrac{q+k}{k}=[2^{103.9},2^{104.0})$ | $[2^{20.8},2^{20.9})\approx\mathbf{20.9}$ | $[2^{-59.2},2^{-59.1})\approx-59.1$ |
| M31 list | $[2^{20.9},2^{21.0})$ | $[2^{52.1},2^{52.2})$ | $\tfrac{q}{2^{100}}=[2^{23.9},2^{24.0})$ | $[2^{3.0},2^{3.1})\approx\mathbf{3.1}$ | $[2^{3.0},2^{3.1})\approx+3.1$ |

The fail-margin column is the exact factor by which the row's certificate
inequality fails at $a_0+1$; its $\log_2$ reproduces the tex's four
"orientation" values $-5.5,\,-22.0,\,-20.9,\,-3.1$
(`prop:v13f1-identity-frontier` L1382-85; `prop:v13f1-closing` L1479) to
$<0.02$ bit, and the pass margins at $a_0$ reproduce $+25.7,+9.2,+10.3,+28.1$
(computed $25.68,9.16,10.30,28.11$) -- the witness-vs-lemma consistency
closure for this panel.

> **`AUDIT-2` (the fail-margin denominator is NOT $B_*$ for the MCA rows).**
> The strategy note's cross-check phrase "fail margin $B_*/F(a)$" is
> literally correct **only for the two list rows**: there
> $\Theta_{\rm list}=\varepsilon^* q$ and $B_*=\lfloor\varepsilon^* q\rfloor$,
> so $\Theta/F(a)=B_*/F(a)$ to $<1$ ulp of $B_*$ ($+22.0$, $+3.1$ bits). For
> the **MCA rows** the certificate threshold is the deep-point conversion
> threshold $\Theta_{\rm mca}=(q+k)/k\approx q/k$ (`thm:A`), **not** $B_*$:
> $F(a)$ is the *auxiliary* list floor in dimension $K=k+1$, which sits
> $\approx q/k\approx2^{166}$ (KB) / $2^{104}$ (M31) -- the literal
> $B_*/F(a)$ is $\mathbf{-102.5}$ bits (KB MCA) / $\mathbf{-59.1}$ bits (M31
> MCA), i.e. $F(a)$ is $\sim\!100/59$ bits **above** $B_*$ and is divided down
> to $\varepsilon_{\rm mca}$ only through the deep-point conversion. The
> orientation margins $-5.5/-20.9$ measure distance to the *deep-point
> threshold*, not to budget -- do not read them as $B_*/F$.

### Graded-prefix family across scales $c\in\{2,4,8,16,32\}$ -- `PROVED`

Per `prop:graded-prefix-floor`: scale $c$ uses $N=n/c$, $m=\lfloor a/c\rfloor$,
$w=m-\lceil K/c\rceil$, covers agreement $mc\le a$, mass
$F_c=\binom{N}{m}/|\mathbb B|^{\,w}$. **Every scale is below threshold at
the target** (`fires=False` for all), confirming the identity scale $c=1$ was
the extremal member (`rem:v13f1-closure`) -- and now superseded by the full
21-scale, three-profile scan below, which extends this from "$c\le32$" to
"every $c\mid n$, every slack profile".

| row | $F_2$ | $F_4$ | $F_8$ | $F_{16}$ | $F_{32}$ | (all `fires=False`) |
|---|---|---|---|---|---|---|
| KB MCA | $[2^{90.7},2^{90.8})$ | $[2^{56.2},2^{56.3})$ | $[2^{54.7},2^{54.8})$ | $[2^{54.3},2^{54.4})$ | $[2^{38.7},2^{38.8})$ | vs $\Theta=2^{166}$: $-75\ldots-127$ b |
| KB list | $[2^{28.6},2^{28.7})$ | $[2^{25.2},2^{25.3})$ | $[2^{23.7},2^{23.8})$ | $[2^{23.3},2^{23.4})$ | $[2^{7.7},2^{7.8})$ | vs $\Theta=2^{58}$: $-29\ldots-50$ b |
| M31 MCA | $[2^{52.1},2^{52.2})$ | $[2^{52.5},2^{52.6})$ | $[2^{52.9},2^{53.0})$ | $[2^{37.8},2^{37.9})$ | $[2^{46.0},2^{46.1})$ | vs $\Theta=2^{104}$: $-51\ldots-66$ b |
| M31 list | $[2^{21.1},2^{21.2})$ | $[2^{21.5},2^{21.6})$ | $[2^{21.9},2^{22.0})$ | $[2^{6.8},2^{6.9})$ | $[2^{15.0},2^{15.1})$ | vs $\Theta=2^{24}$: $-2.9\ldots-17$ b |

### `paid_tangent` cell at $a_0+1$ -- `AUDIT` (conditional; not payable as an upper bound here)

Tangent count $r+1=n-a$: KB MCA $\mathbf{981{,}109}$, KB list $981{,}106$,
M31 MCA $981{,}131$, M31 list $981{,}130$.

- **Lower floor -- `PROVED`, unconditional.** The moving-root tangent
  construction gives $\ge r+1$ support-wise MCA-bad finite slopes at every
  radius (Paper-B `prop:floor`: $\varepsilon_{\rm mca}\ge \lfloor\delta
  n\rfloor/q=r/q$; `prop:v13-tangent` verified exactly over $\mathbb F_{13}$).
  So $B_{\rm tan}(a_0+1)\ge r+1$ **always**.
- **Upper bound $B_{\rm tan}(a)\le r+1$ -- `AUDIT`, NOT licensed at this row.**
  `thm:deep-mca` (`cs25_cap_v12.tex` L4514) proves $\varepsilon_{\rm
  mca}\le(r+1)/q$ **only** under $3r\le w_{\min}-1$, i.e. $r\le\lfloor
  (n-k)/3\rfloor=349{,}525$; `thm:mca-from-ca` gives the tangent split only
  under $2r\le n-k-1$ ($r\le524{,}287$). Here $r=981{,}108\ldots981{,}130\gg
  524{,}287$, so **both radius hypotheses fail**; $r+1$ is a lower floor at
  this row, not a certified upper cell.

Budget consumed by the tangent floor: negligible for KB ($2^{19.9}$ vs
$B_*=2^{57.9}$, 38 bits below) but **material for M31**
($B_*-(r+1)=\mathbf{15{,}796{,}084}$ (M31 MCA) / $\mathbf{15{,}796{,}085}$
(M31 list) -- only $\approx2^{23.9}$ of the $2^{24}$ budget survives the
tangent floor).

### Applicability audit -- no existing theorem pays the row -- `PROVED`

Agreement gap $=(a_0+1)-a_{\min\text{-safe}}$; **every gap is negative**.
Closest miss is $\ge 377{,}020$; farthest $674{,}009$.

| safe-side theorem | radius hyp. | $a_{\min\text{-safe}}$ | KB MCA | KB list | M31 MCA | M31 list |
|---|---|---:|---:|---:|---:|---:|
| `thm:deep-mca` (self-contained) | $3r\le n{-}k$ | $1{,}747{,}627$ | $-631{,}583$ | $-631{,}580$ | $-631{,}605$ | $-631{,}604$ |
| `cor:conditional-half` (BCIKS20 import) | $2r\le n{-}k$ | $1{,}572{,}864$ | $-456{,}820$ | $-456{,}817$ | $-456{,}842$ | $-456{,}841$ |
| `thm:elementary-ca` (half-Johnson) | $(n{-}2r)^2>(k{-}1)n$ | $1{,}790{,}031$ | $-673{,}987$ | $-673{,}984$ | $-674{,}009$ | $-674{,}008$ |
| PR271-280 BCHKS25 Thm 4.6 (conditional) | Johnson | $1{,}493{,}067$ | $-377{,}023$ | $-377{,}020$ | $-377{,}045$ | $-377{,}044$ |

None of the four reaches within $377{,}020$ agreement points of any target
row; the row sits deep inside the still-open v12 band
$\approx(1/4,\,0.4679)$, glued to its unsafe edge.

### Dedup / first-match ordering -- `PROVED` (bookkeeping)

Fixed cell order for $U(a)$ (matches `thm:conditional-mca`'s
$B^+(a)=B_{\rm tan}+B_Q^{\rm all}+B_{\rm ap}+B_{\rm ext}$ and `agents.md`'s
$U(a)$): `paid_tangent`, `paid_quotient` (union across divisor scales, **not**
a max), `paid_extension`, `paid_plain_CA_or_sparse`,
`paid_L1/interleaved_list_layer`, `paid_M1_aperiodic_or_SPI_layer`,
explicitly named residuals. **Coalescing rule:** first-match by descending
priority; a bad parameter already charged to an earlier cell (its root
divides $P_{\rm paid,\mathbb F}(Z)$) is removed by gcd before the next cell
counts (`def:paid-root-removal-regular-branch`), so the quotient cell counts
a union and never double-charges the tangent slopes.

## The complete rung-margin audit (Audit 1) -- centerpiece

**Scope.** Executes Audit 1 of `experimental/cap25_v13_missing_inputs_strategy.md`
sec 2.1 in full: the complete dyadic-rung floor/budget comparison, at **both**
$a=a_0$ and $a=a_0+1$, for all four deployed v13 rows, across the three
slack-profile variants the v13 tex defines. The question Audit 1 poses --
*does any rung or slack profile come out **tight** (sub-bit) or **inverted**
(fires) at $a_0+1$, threatening the adjacent-pair conjecture from the
periodic side?* -- is answered here with exact integers.

**Headline: `GREEN`.** No floor that covers an agreement $\ge a_0+1$ fires
(no inversion) or lands within one bit of the budget (no frontier-tight rung)
in any of the 4 rows, over all 21 dyadic scales and all three slack profiles.
The tightest frontier-bearing comparison is the **identity scale $c=1$**
itself, at the four printed fail margins $-5.50/-22.01/-20.89/-3.07$ bits.
**The periodic side does not threaten the conjecture; the cheap potential
refutation is excluded.** One sub-bit margin does appear in the $a_0+1$ scan
-- M31-list, scale $c=2048$, $-0.21$ bit -- but it belongs to a
**sub-frontier** cell (covered agreement $1{,}114{,}112 \ne a_0+1$), is
dominated there by the identity scale by $+59{,}588$ bits, and does not fire;
it is a documented watch-item, not a refutation (see "the one sub-bit
margin" below).

### The three slack-profile variants at a dyadic rung $c=2^j$

- **(Gfloor) graded prefix floor**, `prop:graded-prefix-floor` /
  `lem:v13f1-identity-prefix-floor`: $N=n/c$, $m=\lfloor a/c\rfloor$,
  $w=m-\lceil K/c\rceil$, mass $F_c=\binom Nm/|\mathbb B|^{w}$; **covers
  agreement $mc\le a$** -- the frontier agreement $a$ only when $c\mid a$.
- **(Gceil) graded floor with $m=\lceil a/c\rceil$**: covers agreement
  $mc\ge a$; the pure-scale floor that actually **bears on the frontier**
  (agreement $\ge a_0+1$) at every $c$, not only when $c\mid a$.
- **(Rem) quotient-remainder prefix floor**, `lem:quotient-remainder-prefix`,
  with residual $s=a-mc=a\bmod c$: covers agreement **exactly $a$** for every
  $c$; $M_{c,m,s}=\binom Nm\binom{n-mc}{s}$, prefix weight
  $w_c(s,\sigma)=\lfloor\sigma/c\rfloor(s{+}1)+\min(\sigma\bmod c,s)$,
  $\sigma=a-K$, mass $F=M_{c,m,s}/|\mathbb B|^{w_c}$. **$c=1$ is exactly the
  identity floor.**
- **(Plant) planted quotient-core**, `thm:v13-planted`: $M=c\mid\gcd(n,k)=k$,
  list count $P_c=\binom{n/c-1}{k/c}$ at agreement $k+\sigma$,
  $1\le\sigma<c$; **covers agreement $a$ iff $a-k<c$**.

A floor bears on the safety of $a_0+1$ only if it **covers** an agreement
$\ge a_0+1$. Hence the conjecture-relevant objects are Rem (all $c$), Gceil
(all $c$), Gfloor (only $c\mid a$), identity $c=1$, Plant ($c>a-k$). A Gfloor
cell with $mc<a$ is a floor at a *lower, already-unsafe* agreement and says
nothing about $a_0+1$ (it is reported separately, below, as sub-frontier).

### Headline verdict table -- `PROVED` (exact integer)

Across all 21 dyadic scales ($j=0..20$) and all three slack profiles,
evaluated at $a_0+1$:

| | KB MCA | KB list | M31 MCA | M31 list |
|---|---|---|---|---|
| any floor covering $\ge a_0{+}1$ **fires** (inverted)? | **No** | **No** | **No** | **No** |
| any floor covering $\ge a_0{+}1$ **within 1 bit** (tight)? | **No** | **No** | **No** | **No** |
| max floor covering $\ge a_0{+}1$ (vs $\Theta$) | $c{=}1$, $-5.4985$ | $c{=}1$, $-22.0109$ | $c{=}1$, $-20.8871$ | $c{=}1$, $-3.0730$ |
| its bracket | $[2^{160.4},2^{160.5})$ | $[2^{35.9},2^{36.0})$ | $[2^{83.1},2^{83.2})$ | $[2^{20.9},2^{21.0})$ |

In every row the identity scale $c=1$ is the **terminal (maximal) frontier
floor**; every $c\ge2$ graded/ceil/remainder floor and every planted core
covering $a_0+1$ is strictly below it, hence strictly below $\Theta$. The
adjacent-pair conjecture (`prob:v13f1-frontier`) is not threatened from the
periodic side.

### Graded-floor margin profile at $a_0+1$ ($m=\lfloor a/c\rfloor$ convention) -- `PROVED`

Margin $=\log_2(F_c/\Theta)$ (bits), all $<0$ (quiet) at $a_0+1$; `DEG` =
degenerate ($m<\lceil K/c\rceil$, i.e. $w<0$). Covered agreement $mc\le a$
(equals $a_0+1$ only when $c\mid a$).

| row | $c{=}1$ | $2$ | $4$ | $8$ | $16$ | $32$ | $64$ | $128$ | $256$ | $512$ | $1024$ | $2048$ | $4096$ | $8192$ | $16384$ | $2^{15}$ | $2^{16}$ | $2^{17}$ | $2^{18}$ | $2^{19}$ | $2^{20}$ |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| KB MCA | **−5.5** | −75 | −110 | −111 | −112 | −127 | −135 | −138 | −124 | −117 | −113 | −111 | −125 | −132 | −135 | −136 | −137 | DEG | DEG | DEG | DEG |
| KB list | **−22.0** | −29 | −33 | −34 | −35 | −50 | −58 | −61 | −47 | −40 | −36 | −34 | −48 | −55 | −58 | −59 | −60 | −44 | −52 | −55 | −57 |
| M31 MCA | **−20.9** | −52 | −52 | −51 | −66 | −58 | −54 | −51 | −65 | −56 | −52 | −49 | −63 | −70 | −73 | −75 | −75 | DEG | DEG | DEG | DEG |
| M31 list | **−3.1** | −2.9 | −2.5 | −2.1 | −17 | −8.9 | −4.5 | −2.1 | −16 | −7.4 | −2.8 | **−0.2** | −14 | −21 | −24 | −26 | −26 | −10 | −18 | −21 | −23 |

Notes. **(i)** $c=1$ (identity) is the tightest for KB MCA / KB list / M31
MCA and is the frontier certificate. **(ii)** MCA rows degenerate at
$c=2^{17}$ (because $K=k{+}1$ is not a power of $2$); list rows stay
non-degenerate to $c=2^{20}$ (because $K=k=2^{20}$ divides every dyadic $c$).
**(iii)** The oscillation in the M31-list row is the $s=a\bmod c$ /
$w=m-\lceil K/c\rceil$ rounding interplay; its minimum $-0.2$ at $c=2048$ is
the tightest cell anywhere in the audit (dissected below). **(iv)** For KB
rows and the M31 MCA row the coarse scales sit tens of bits below budget --
only the M31-list row (the smallest budget) has coarse floors grazing
$\Theta$.

**Firing analysis (`PROVED`, exact):** the *only* Gfloor cell that fires
anywhere is $c=1$ at $a_0$:

| | KB MCA | KB list | M31 MCA | M31 list |
|---|---|---|---|---|
| cells firing at $a_0$ | $c{=}1$ (+25.68) | $c{=}1$ (+9.16) | $c{=}1$ (+10.30) | $c{=}1$ (+28.11) |
| cells firing at $a_0+1$ | none | none | none | none |

So the identity scale is the **sole periodic certifier of unsafety at
$a_0$**, and nothing certifies unsafety at $a_0+1$ -- the exact-integer
statement of "identity scale is terminal" (`rem:v13f1-closure`), extended
here from $c=2$ to *all* $c\ge2$.

### Remainder floor (covers agreement exactly $a_0+1$) -- `PROVED`

The remainder profile is the honest "rung at exactly $a_0+1$" object. Margin
vs $\Theta$ (bits), selected scales:

| row | $c{=}1$ (=identity) | $c{=}2$ | $c{=}4$ | $c{=}16$ | $c{=}2048$ | $c{=}2^{16}$ | $c{=}2^{20}$ |
|---|--:|--:|--:|--:|--:|--:|--:|
| KB MCA | **−5.5** | −75 | −110 | $-1.57\times10^{6}$ | $-1.96\times10^{6}$ | $-9.97\times10^{4}$ | $-1.73\times10^{6}$ |
| KB list | **−22.0** | $-1.05\times10^{6}$ | $-1.57\times10^{6}$ | $-1.96\times10^{6}$ | $-1.96\times10^{6}$ | $-9.98\times10^{4}$ | $-1.73\times10^{6}$ |
| M31 MCA | **−20.9** | −52 | $-1.05\times10^{6}$ | $-7.8\times10^{5}$ | $-1.93\times10^{6}$ | $-9.85\times10^{4}$ | $-1.73\times10^{6}$ |
| M31 list | **−3.1** | $-1.05\times10^{6}$ | $-1.57\times10^{6}$ | $-9.1\times10^{5}$ | $-1.93\times10^{6}$ | $-9.85\times10^{4}$ | $-1.73\times10^{6}$ |

At **exactly** agreement $a_0+1$, the only non-suppressed floor is $c=1$.
For every $c\ge2$ the residual $s$ loose points force a prefix weight
$w_c(s,\sigma)$ that explodes (e.g. $c=2048$: $w_c=63{,}095$ slots
$\approx1.96\times10^{6}$ bits of $|\mathbb B|$ cost), driving the remainder
floor $\sim10^{6}$ bits below $\Theta$. **No remainder floor fires or is
tight at $a_0+1$.**

### Planted quotient-cores covering $a_0+1$ -- `PROVED` (dominated)

To cover agreement $a_0+1=k+\sigma$ the planted core needs slack
$\sigma=a_0{+}1{-}k\approx67{,}467<M=c$, so only $c\ge2^{17}$ is active, and
the count $P_c=\binom{n/c-1}{k/c}$ *shrinks* with $c$:

| scale $c$ | $P_c=\binom{n/c-1}{k/c}$ | bits | vs $B_*^{\rm KB}=2^{58}$ | vs $B_*^{\rm M31}=2^{24}$ |
|---|--:|--:|--:|--:|
| $2^{17}=131072$ | $\binom{15}{8}=6435$ | $2^{12.65}$ | $-45.28$ | $-11.35$ |
| $2^{18}=262144$ | $\binom{7}{4}=35$ | $2^{5.13}$ | $-52.80$ | $-18.87$ |
| $2^{19}=524288$ | $\binom{3}{2}=3$ | $2^{1.58}$ | $-56.35$ | $-22.41$ |
| $2^{20}=1048576$ | $\binom{1}{1}=1$ | $2^{0}$ | $-57.93$ | $-24.00$ |

The largest planted core reaching $a_0+1$ is $6435$ (at $c=2^{17}$), $45.3$
bits (KB) / $11.3$ bits (M31) below $B_*$. High agreement needs large slack
$\Rightarrow$ large $M=c$ $\Rightarrow$ small quotient order $N=n/c
\Rightarrow$ small count. **No planted core fires or is tight at $a_0+1$.**

### Cross-checks -- `PROVED`

**(a)** $c=1$ reproduces the identity-scale margins to $<0.02$ bit (pass @
$a_0$: $+25.676/+9.164/+10.299/+28.113$ vs tex $+25.7/+9.2/+10.3/+28.1$; fail
@ $a_0+1$: $-5.498/-22.011/-20.887/-3.073$ vs tex $-5.5/-22.0/-20.9/-3.1$).
**(b)** Gfloor at $a_0+1$, $c\in\{2,4,8,16,32\}$, matches the ledger's graded
scales exactly (all 20 brackets identical, `ALL MATCH: True`).
**(c)** `rem:v13f1-closure` ("$c=2$ and planted dominated at $a_0$") is
confirmed and strengthened to *all* $c\ge2$: at $a_0$, identity $c=1$ fires
in every row while $c=2$ graded and the planted max are strictly below
budget ($-43.96/-29.30/-20.67/-2.85$ quiet vs $+25.68/+9.16/+10.30/+28.11$
firing).

### Audit-2 -- descent recursion-loss table -- `AUDIT` (verifies the strategy note's $\sim1.2/\sim2$)

Cites strategy note sec 2.1, Audit 2: the intrinsic periodic *support* count
is $\sim10^6$ bits above budget, so the quotient bucket cannot be paid at
support level (`cor:periodic-support-count`); it must be paid at **image
level by descent** (`thm:fiber-descent`), whose per-rung losses **add in
bits**. With row fail-margin $M$ (bits) and descent depth $R$, the maximum
tolerable geometric-mean per-rung loss is $2^{M/R}$. The divisor lattice of
$n=2^{21}$ is the chain $1\mid2\mid\dots\mid2^{21}$, so $R=\log_2 n=21$.

| row | fail margin $M$ (bits) | $R=21$: max per-rung loss $2^{M/21}$ | strategy-note claim |
|---|--:|--:|---|
| KB MCA | $5.498$ | $\mathbf{1.199}$ | "$\sim1.2$" (exact) |
| KB list | $22.011$ | $\mathbf{2.068}$ | "$\lesssim2$" (exact $2.07$) |
| M31 MCA | $20.887$ | $\mathbf{1.993}$ | "$\sim2$" |
| M31 list | $3.073$ | $\mathbf{1.107}$ | (tightest tolerance after KB MCA) |

**Verdict on the strategy note's numbers: verified.** $2^{5.5/21}=1.199\approx
1.2$ and $2^{20.9/21}=1.993\approx2$ are exact. **One micro-correction:** the
$22.0$-bit row's exact ceiling is $2^{22.0/21}=\mathbf{2.068}$, i.e.
*marginally above* $2$; the note's "below $2$" is a safe conservative
rounding, but the true tolerance is $2.07$.

**Clarification on $R$ (a genuine subtlety).** The descent depth is the
divisor-lattice depth $\log_2 n=21$, **not** the number of non-degenerate
graded-prefix rungs. The graded floor degenerates at $c=2^{17}$ for the MCA
rows, giving **17** non-degenerate graded rungs (list rows: **21**). Using
$R=17$ would give $2^{5.5/17}=1.251$ (KB MCA) and $2^{20.9/17}=2.344$ (M31
MCA), which do **not** match the note's $1.2/2$. The note's figures are
reproduced only by $R=21$ -- confirming the Audit-2 recursion is the
**image-level** divisor descent (21 levels), a different object from the
graded-floor rung count. Recorded so the two "21 vs 17" counts are never
conflated.

**Consequence (as the strategy note asks): `(Q-fin)` demands a
near-lossless recursion** -- geometric-mean per-rung loss below $1.2$ (KB
MCA) / $1.11$ (M31 list) for the two tight rows, up to $\approx2.07$ for the
two $\sim21$-bit rows -- forcing the hybrid design the strategy note names in
sec 2.4: exact enumeration below a cut scale, theorems above it.

### The one sub-bit margin: M31-list, $c=2048$, $-0.21$ bit -- `AUDIT` (not a threat)

The single sub-bit number in the entire $a_0+1$ scan.

- Row M31-list, scale $c=2048$, $N=n/c=1024$, $m=\lfloor a/c\rfloor=544$,
  $w=m-\lceil K/c\rceil=544-512=32$.
- **Covered agreement $mc=544\cdot2048=1{,}114{,}112$** -- $1{,}911$ **below**
  $a_0+1=1{,}116{,}023$, i.e. a *sub-frontier, already-unsafe* agreement.
- Exact verdict: $\binom{1024}{544}\cdot2^{100}\ \le\ q\cdot p'^{32}$ is
  **True**, i.e. the cell is **QUIET** (does not fire); margin $-0.2106$ bit.

Three independent reasons this is not a frontier threat: **(1)** it does not
cover $a_0+1$ (the floors that do, at $c=2048$, are the ceil-graded
($-31.4$ bits) and the remainder ($-1.93\times10^{6}$ bits), both far below
$\Theta$); **(2)** it is massively dominated where it lives (at agreement
$1{,}114{,}112$ the identity scale sits $+59{,}588$ bits above $\Theta$, so
this cell is inert relative to the certified-unsafe identity witness there);
**(3)** it does not fire (margin $-0.21<0$ even at its own covered
agreement). This is exactly the phenomenon the strategy note's Audit 1
anticipated ("rung fail margins can shrink toward sub-bit values"). Recorded
as a **watch-item** (any future intermediate-scale accounting for the
M31-list row has $\approx$ zero slack), not a refutation.

### The union ledger at $a_0+1$ is dominated by the identity term -- `PROVED`

Assembling the sections above: the quotient/graded/planted union
$B_Q^{\rm all}(a_0+1)$, taken over all $c\mid n$ and all slack profiles, has
as its maximal member the identity floor $F(a_0+1)$, which is
$5.5/22.0/20.9/3.1$ bits **below** $\Theta$. Every other member is strictly
smaller at agreement $\ge a_0+1$. The periodic (quotient) contribution to the
upper ledger at $a_0+1$ is itself below budget by the identity margin, with
**no rung crossing zero**. The only way the adjacent pair fails from the
periodic side would be an inversion (some rung firing at $a_0+1$); this audit
excludes it exactly. Status of "$a_0+1$ safe" overall remains
`CONJECTURAL_WITH_FALSIFIER` (the aperiodic/L1/sparse cells below are still
open) -- Audit 1 closes only the **periodic veto**.

## Named-input targets -- the packet centerpiece -- `CONDITIONAL_ON_NAMED_INPUT`

Each open cell stated as a named input plus the exact integer/bit target it
must hit for $U(a_0+1)\le B_*$. A factor $n^C$ costs $C\log_2 n=\mathbf{21C}$
bits (`prop:v13f1-closing` L1483). Per Audit-2 above, the quotient cell's
target is now sharpened to the exact per-rung-loss ceiling
($1.20$-$2.07\times$, image-level, $R=21$) rather than an unquantified
"absorb the periodic bucket" statement.

**(i) Input `(Q)` -- per-fiber prefix-collision equidistribution
($w{+}1\approx67{,}467$).** The pigeonhole guarantees *some* prefix-fiber has
$\ge F(a)$ subsets; the upper ledger needs the **maximum** fiber. `(Q)`
certifies $\max\text{-fiber}\le\varrho_Q\cdot F(a)$. Affordable blow-up
$\log_2\varrho_Q$ = the row's fail margin:

| row | affordable $\log_2(\max/\text{avg})$ to stay $\le B_*$ | at 50% $B_*$ | at 10% $B_*$ | at 1% $B_*$ |
|---|---|---|---|---|
| KB list | $\mathbf{22.0}$ b ($=\log_2 B_*/F$) | $21.0$ | $18.7$ | $15.4$ |
| M31 list | $\mathbf{3.1}$ b | $2.1$ | $\mathbf{-0.25}$ (impossible) | $-3.6$ |
| KB MCA | $\mathbf{5.5}$ b (vs deep-point $\Theta$) | -- | -- | -- |
| M31 MCA | $\mathbf{20.9}$ b (vs deep-point $\Theta$) | -- | -- | -- |

**Target integers:** list-row max-fiber $\le B_*$, i.e.
$\le 274{,}980{,}728{,}111{,}395{,}087$ (KB list) / $\le 16{,}777{,}215$ (M31
list). **M31 list is the razor's edge:** only $3.07$ bits of headroom; it
cannot afford even $10\%$ of $B_*$ under any max/avg blow-up -- the
identity-prefix fibers must be *essentially perfectly equidistributed*.

**(ii) Input `(A)` -- `prob:band` aperiodic bound $B_{\rm ap}(a)\le
P(n)=n^C$.** Max affordable $C$ with $n^C\le B_*$ (and, after paying the
tangent floor, $n^C\le B_*-(r+1)$):

| row | $\log_2 B_*$ | $\log_2 B_*/21$ | **max integer $C$** (alone) | max $C$ after tangent |
|---|---|---|---|---|
| KB MCA / KB list | $57.93$ | $2.759$ | $\mathbf{2}$ | $2$ |
| M31 MCA / M31 list | $24.00$ | $1.143$ | $\mathbf{1}$ | $1$ ($B_*{-}(r{+}1)=2^{23.9}$) |

**KB affords $n^2$; M31 affords only $n^1$ -- the M31 aperiodic cell must be
LINEAR in $n$.** ($B_*^{\rm M31}/n\approx 8.0$: the entire M31 budget is
$\approx 8$ linear-sized cells; $B_*^{\rm KB}/n\approx2^{36.9}$.)

**(iii) L1 cells (`prob:v13-l1-residuals`, `prob:v13-primitive-image-fiber`)
-- $n^B$ budget.** Same mechanics: the mixed-petal / growing-defect residual
and the stabilizer-primitive image-fiber part must each be $\le n^B$ with
$21B\le\log_2(\text{cell's budget share})$. Per-cell ceiling $B\le2$ (KB) /
$B\le1$ (M31). **Sum constraint (binding for M31):** tangent + quotient-union
+ extension + sparse + L1 + aperiodic $\le B_*$; for M31 the whole right side
after tangent is $\le 15{,}796{,}084\approx7.5\cdot n$, so **all remaining
poly cells together** must fit in $\approx7.5$ linear-sized units.

**(iv) Sparse $\sigma_C$ at $\delta'=1-a/n$ via `thm:sparsify` -- exact
target.** `thm:sparsify`: $\varepsilon_{\rm mca}(C,\delta')=\max(\varepsilon_{\rm
ca}(C,\delta'),\sigma_C(\delta')/q)$, so $B_{\rm mca}(a)=\max(\varepsilon_{\rm
ca}\!\cdot\!q,\ \sigma_C)$. Since $\delta'>\tfrac14=(1-\rho)/2$ the mutual
layer **is** the sparse layer (`rem:sparsify-recover`). **Exact sparse-cell
target:**
$$\sigma_C\big(\delta'\big)\ \le\ B_*, \quad
\sigma_C\le 274{,}980{,}728{,}111{,}395{,}087\ (\text{KB}),\qquad
\sigma_C\le 16{,}777{,}215\ (\text{M31}),$$
at $\delta'=245277/524288$ (KB MCA), $981105/2097152$ (KB list),
$490565/1048576$ (M31 MCA), $981129/2097152$ (M31 list). Open problem
`prob:mutual`/`prob:sparse-mutual` for $(1-\rho)/2<\delta'<1-\rho-s_\rho/n$.

## Ledger impact

Relative to the previously shipped single-row (KB MCA) skeleton, this packet
family:

1. Extends the exact ledger (tangent, graded-prefix, dedup, applicability
   audit, named-input targets) from **one row to all four** deployed v13
   rows, with the M31 $\varepsilon^*=2^{-100}$ carve-out made explicit
   throughout (not just noted once).
2. Replaces the earlier `c\in\{2,4,8,16,32\}` "does not fire" spot-check with
   a **complete 21-scale, 3-profile exact scan** at both $a_0$ and $a_0+1$,
   upgrading `rem:v13f1-closure` from "$c=2$ dominated" to "all $c\ge2$
   dominated" and closing the periodic/quotient side of the adjacent
   conjecture as a source of a cheap counterexample.
3. Turns the strategy note's qualitative Audit-2 recursion-loss claim
   ("$\sim1.2$", "$\lesssim2$") into four exact per-row ceilings
   ($1.199,2.068,1.993,1.107$), sharpening the `(Q-fin)` named-input target.
4. Adds one documented watch-item (M31-list, $c=2048$, $-0.21$ bit,
   sub-frontier, dominated, non-firing) with a full three-part non-threat
   argument, rather than leaving sub-bit coarse-scale behavior unexamined.
5. Does **not** move any open-cell status: the aperiodic, L1, and sparse
   cells remain exactly as open as before this note. No cell is promoted to
   `PAID_BY_THEOREM` or `PAID_BY_EXACT_CERTIFICATE` beyond what was already
   established (the tangent lower floor and the unsafe-side identity
   certificate).

## Constants

| constant | value |
|---|---|
| $n$ | $2^{21}=2{,}097{,}152$ |
| $k$ | $2^{20}=1{,}048{,}576$ |
| $p_{\rm KB}$ | $2^{31}-2^{24}+1=2{,}130{,}706{,}433$ |
| $p_{\rm M31}$ | $2^{31}-1=2{,}147{,}483{,}647$ |
| $q_{\rm KB}=p_{\rm KB}^6$ | $93{,}571{,}093{,}019{,}388{,}561{,}295{,}270{,}373{,}781{,}649{,}880{,}353{,}786{,}165{,}192{,}103{,}559{,}169$ (186-bit) |
| $q_{\rm M31}=p_{\rm M31}^4$ | $21{,}267{,}647{,}892{,}944{,}572{,}736{,}998{,}860{,}269{,}687{,}930{,}881$ (124-bit) |
| $B_*^{\rm KB}$ | $274{,}980{,}728{,}111{,}395{,}087$ (58-bit) |
| $B_*^{\rm M31}$ | $16{,}777{,}215=2^{24}-1$ (24-bit) |
| descent depth $R$ | $\log_2 n=21$ |
| fail margins (bits) | $-5.4985$ (KB MCA), $-22.0109$ (KB list), $-20.8871$ (M31 MCA), $-3.0730$ (M31 list) |
| max per-rung loss at $R=21$ | $1.199$, $2.068$, $1.993$, $1.107$ (same row order) |

## Reproducibility

```text
python3 experimental/scripts/verify_frontier_adjacent_v13_rows.py
```

stdlib-only (Python 3, `math` only), no seeds, no external data. Exit code 0
means every gate (B* recomputation, unsafe-side replay at $a_0$, adjacent
stratum bit-bracket at $a_0+1$, safe-theorem gap table, packet-consistency
recompute, and the **full** rung-margin table recompute across all 21 scales
and all four rows) reproduced independently from `n`, `k`, `p_{\rm KB}`,
`p_{\rm M31}` alone, matching every number stored in the four
`experimental/data/certificates/frontier-adjacent/*_v1.packet.json` files
exactly. It does **not** mean $a_0+1$ is certified safe (see
`safe_certificates.status = "OPEN"` in every packet); the verifier prints the
open-cell named-input targets as `INFO`, never as a passing gate. Runtime
budget: under 180s (the rung-table recompute shares binomial computations
across rows/agreements/variants via anchor-and-ratio-update, rather than
recomputing each of the $4\times2\times21\times4$ cells from scratch, which
would exceed the budget).

Also reproducible independently: `python3 "experimental/scripts/towards v13/cap25_v13_frontier_identity_exact_checks.py"`
→ all 12 checks PASS (the four `*_identity` rows are the unsafe-side
certificates this note's ledger section is built on).

## Cross-references

- **tex labels:** `def:v13-staircase`, `cor:v13-endpoint`, `prop:onestep`,
  `lem:v13f1-identity-prefix-floor`, `prop:v13f1-identity-frontier`,
  `rem:v13f1-closure`, `prop:v13f1-closing`, `prob:v13f1-frontier`,
  `thm:A`, `thm:deep-mca`, `thm:mca-from-ca`, `thm:elementary-ca`,
  `cor:conditional-half`, `prop:graded-prefix-floor`,
  `lem:quotient-remainder-prefix`, `thm:v13-planted`, `cor:v13-list-unsafe`,
  `cor:periodic-support-count`, `thm:fiber-descent`, `thm:conditional-mca`,
  `def:paid-root-removal-regular-branch`, `thm:sparsify`,
  `rem:sparsify-recover`, `prob:mutual`/`prob:sparse-mutual`,
  `thm:johnson-list`, `prob:band`, `rem:quotient-borne`,
  `prob:v13-l1-residuals`, `prob:v13-primitive-image-fiber`.
- **`experimental/cap25_v13_missing_inputs_strategy.md`** sec 2.1 (Audit 1,
  Audit 2), the source this note's centerpiece executes; sec 1/2/3 (Routes
  $\alpha/\beta/\gamma$, Q1-Q3) for the still-open aperiodic/quotient
  analytic program this note does not touch.
- **`agents.md`**, "Missing inputs strategy: `(A)` and `(Q)`" section and
  "What counts as progress now" list (see "Relevance to agents.md steering"
  above).
- **Integrated PR271-280 batch** (commit `b9b23f2`, "Integrate PR 271-280
  experimental packets"): `experimental/data/certificates/koalabear-bchks25-jmca-safe-edge-v1/certificate.json`
  (`safe_A=1493067`), `.../koalabear-bchks25-jmca-bounds-v1/`,
  `.../koalabear-bchks25-jmca-param-squeeze-v2/` -- the applicability-audit
  table's conditional entry is read directly from the integrated
  `safe-edge-v1` certificate, not from recon prose.
- **In-flight, not-yet-integrated local-input tracks (informational only,
  no dependency taken here):** PR #282 and PR #283 (AllenGrahamHart). This
  note and its verifier are fully self-contained and do not read, require, or
  anticipate the content of those PRs.
- **Companion, not-yet-merged local branch** `cap25-v13-identity-frontier-cert`
  (this session's sibling submission, `experimental/data/certificates/cap25-v13-identity-frontier/`):
  covers the unsafe-side identity certificate only; this note's own
  `unsafe_certificates` fields and verifier gate `G2` independently reproduce
  the same numbers from scratch rather than depending on that branch's
  artifact, since the two submissions are not guaranteed to land in the same
  order.
- **Maintainer v14 auxiliary scripts** (commit `2b5b7ce`, "Add v13 v14
  auxiliary frontier scripts"): `experimental/scripts/towards v13/cap25_v14_moved_frontier_checks.py`
  and `.../collision_margins.py` -- both re-run in this session (exit 0).
  The former's printed margins (`8.978`/`-22.197` bits KB-MCA,
  `27.927`/`-3.259` bits M31-MCA) are **cross-validated to <0.05 bit** by
  this note's own independent recompute (see "V14 moved-frontier addendum"
  below and verifier gate `G7`); the latter is confirmed `EXPERIMENTAL`
  (its own header) and not updated to v14 m-values, as expected (it checks a
  different, calibration-only quantity).

## V14 moved-frontier addendum (2026-07-05)

**This section is the packet family's own v14 successor chapter**: it
documents the two MCA frontier pairs that moved between v13 and v14
(upstream #310, commit `f049b91`), recomputes their full adjacent-budget
ledgers and the complete 21-scale x 3-profile rung-margin audit at the moved
pairs from `n, k, p` alone, and states the updated named-input targets. The
two *list* rows (KB list, M31 list) are unchanged and are not re-derived
here; their content earlier in this file stands untouched.

**Provenance of the move.**
- Upstream **PR #310, commit `f049b91`** ("Material correction: quantitative
  deep-list floor flips 1116044–1116047; corrected pair {1116047, 1116048}").
- The maintainer's v14 auxiliary scripts at **commit `2b5b7ce`**:
  `experimental/scripts/towards v13/cap25_v14_moved_frontier_checks.py` and
  `.../collision_margins.py` (both re-run here; outputs reproduced exactly).
- Recompute machinery: `experimental/scripts/verify_frontier_adjacent_v13_rows.py`
  (#329), **imported, not re-derived**; its pre-existing `G1`-`G6` replay is
  green (6/6) on the four deployed v13 rows before its exact-integer
  routines are reused here at the moved values -- this same script's new
  `G7` (added by this commit) is what gates the moved-pair recompute below.

**Status labels.** Every arithmetic/verification claim below is **`AUDIT`**
(pure integer comparison, independently recomputed, cross-checked to the v14
script within `0.0003` bit). The "`a0'+1` is the first MCA-safe agreement"
statements stay **`CONJECTURAL_WITH_FALSIFIER`** (`prob:v13f1-frontier`). No
`COUNTEREXAMPLE_NEW_FLOOR` beyond the ones #310 already establishes at
`1116044…1116047`.

---

### Headline

| moved MCA row | moved pair `(a0', a0'+1)` | pass @ `a0'` | fail @ `a0'+1` | rung audit at `a0'+1` |
|---|---|---:|---:|---|
| **KoalaBear MCA** | `(1116047, 1116048)` | **+8.9777** b | **−22.1969** b | **GREEN** (tightest frontier rung = identity `c=1`, −22.20 b) |
| **Mersenne-31 MCA** | `(1116023, 1116024)` | **+27.927** b | **−3.2589** b | **TIGHT** — one frontier-covering rung within 1 bit |

**Tight/inverted flag (the answer to "any tight/inverted rung at the new
`a0'+1`?"):**

- **No inversion anywhere.** No floor covering an agreement `≥ a0'+1` fires at
  either moved open step; the adjacent-pair conjecture is not refuted from the
  periodic side for either row.
- **One frontier-tight rung, on the M31-MCA row:** the graded-ceil floor at
  scale `c = 2048` covers agreement `1116160 ≥ a0'+1` with mass
  `L = M = 12{,}769{,}758` against `B*_M31 = 16{,}777{,}215`, i.e. **−0.3938
  bit** — non-firing (quiet), but inside the one-bit band. It is a documented
  **watch-item**, not a falsifier (it does not fire; the conjecture survives).
  This tightness is a *new* consequence of #310's correction: it appears only
  because the corrected route compares against `B* ≈ 2^24` instead of the
  retired `(q+k)/k ≈ 2^104` deep-point threshold, and the M31 row carries the
  smallest budget.
- **KB-MCA is comfortably green:** its tightest frontier-bearing rung is the
  identity scale itself at −22.20 bit; every coarse graded/remainder/planted
  floor covering `a0'+1` sits −29 … −58 bits below `B*_KB ≈ 2^58`.

---

### 1. What moved, and why

#### 1.1 The composition (three lines, zero new mathematics — #310)

The v13 packet's `UNDECIDED_WINDOW_OPEN` verdict at `a = 1116044` was too
conservative. Composing two statements **already merged upstream** when the v13
packet shipped:

1. **`lem:v13f1-identity-prefix-floor`** at `K = k+1`, exponent `w = m-k-1`:
   some received word `U` has
   `L(m) = ceil( C(n,m) / p^{w} ) ≥ 1` distinct `RS[F,D,k+1]` codewords in the
   closed `(1-m/n)`-ball around it (varying per-codeword supports, each
   agreeing on `≥ m > k` points).
2. **`prop:quantitative-deep-list-floor`** (`tex/cs25_cap_v12.tex` L317–342,
   merged 2026-07-02; the sharp internal denominator `q-n+k(L-1)` is the
   conclusion of `thm:quant-deep-point` in the strict352 section, stated for
   `LD_sw` verbatim; the printed `q-n+kL` form is L383–386). This has **no
   density trigger** — any `L ≥ 1` qualifies — and yields a single received
   line with at least
   ```
   M(m) = ceil( L(q-n) / (q-n + k(L-1)) )
   ```
   support-wise MCA-bad finite slopes in the line field (a max-over-lines lower
   bound on the `def:mca` numerator, never a family sum).
3. Compare `M(m)` to `B* = floor(q / 2^{lam})` (`thm:v13-windows`:
   `M > B*  ⟹  certified MCA-unsafe`).

The old v13 MCA route measured `L(a)` against the **deep-point contrapositive
trigger** `(q+k)/k ≈ 2^{166}` (KB) / `2^{104}` (M31) — a much higher bar than
`B*`. `rem:quantitative-floor-vs-contrapositive` (v12 L426–436) prescribes the
quantitative form "when a quotient fiber is too small to cross the `1/(2k)`
trigger but still contributes a nonzero explicit bad-slope numerator" — exactly
this case. The `L → M` conversion is **lossless here** (`k(L-1) ≪ q-n` for
every `L ≤ 2^{67}` in range, so `M = L` to `< 1` unit), so the corrected
comparison is simply the identity-prefix list floor `L` against `B*`.

#### 1.2 The exact KB five-point sweep (AUDIT — anchors reproduce #310 exactly)

All five points recomputed here from `n, k, p_KB` alone (exact `L` and `M`
integers); every margin **matches `f049b91`**, and the boundary anchors
`L(1116044), M(1116044), M=L(1116047), M=L(1116048)` byte-match #310. The
conversion carries a `< 0.03`-bit loss (`M < L`) at `m ≤ 1116046` and is exactly
lossless (`M = L`) at the two boundary points:

```
m         w      L (identity-prefix list floor)                       M = deep-point count                                  margin/B*   verdict
1116044   67467  1973967916468083369044358670918132115633867608112    1931247427137429416005585529088676636591240959005    +102.4700   MCA-UNSAFE (was the v13 open step)
1116045   67468  814425913096566971889355562271699499566              814425913089134019045423823800425467007              +71.3269    MCA-UNSAFE
1116046   67469  336017770100260521299356569240                       336017770100260521298091300724                       +40.1523    MCA-UNSAFE
1116047   67470  138634741058327852652                                138634741058327852652  (= L, lossless)               +8.9777     MCA-UNSAFE — new edge a0'
1116048   67471  57198030366                                          57198030366            (= L, lossless)               −22.1969    new open step a0'+1
```

The certified MCA-unsafe interval widens from `[981109/2097152, 1/2)` to
`[981105/2097152, 1/2) = [0.4678273…, 1/2)`; the corridor becomes
`1116048 ≤ a*`. `prob:v13f1-frontier`'s finite prediction `a* = 1116044` is
refuted; no proved-*safe* statement is contradicted (nearest unconditional safe
radius `δ ≈ 0.2045`; Johnson at `a = 1482910`; exactness zone at `a ≥ 1747627`).

#### 1.3 The v14 four-row adjacent map

| row-object | pair `(a0, a0+1)` | status vs v13 |
|---|---|---|
| KB **MCA** (K=k+1) | `(1116047, 1116048)` | **MOVED** (was `(1116043, 1116044)`) |
| KB **list** (K=k) | `(1116046, 1116047)` | unchanged |
| M31 **MCA** (K=k+1) | `(1116023, 1116024)` | **MOVED** (was `(1116021, 1116022)`) |
| M31 **list** (K=k) | `(1116022, 1116023)` | unchanged |

Only the two MCA rows move: the correction is about the MCA-bad-slope count
crossing `B*`, and the K=k list rows already compare their list floor against
`B*` directly (no deep-point conversion), so their edges are untouched.

#### 1.4 Maintainer-script reproduction (AUDIT)

`cap25_v14_moved_frontier_checks.py` re-run from repo root — all exact checks
pass:

```
KoalaBear MCA:  m=1116047, w=67470, edge=981105/2097152
  pass/fail margins: 8.978 / 22.197 bits ;  safe adjacent=1116048 ;  finite moment order ≈ 94196
Mersenne-31 MCA: m=1116023, w=67446, edge=981129/2097152
  pass/fail margins: 27.927 / 3.259 bits ;  safe adjacent=1116024 ;  finite moment order ≈ 641593
All exact v14 moved-frontier checks passed.
```

The v14 script checks only the identity-scale (`c=1`) edge/open orientation
(fires at `a0'`, quiet at `a0'+1`); the full 21-scale × 3-profile rung audit of
§3 is **additive** to it and is where the M31 sub-bit rung surfaces.

`collision_margins.py` re-run (exit 0): entropy-sandwich `w0`-crossover
calibration; it is an **`EXPERIMENTAL` calibration cross-check only** (its own
header) and still evaluates the *old* frontier `m` values (KB MCA `1116043`,
`w0 = 21`; M31 line-round `1116021`, `w0 = 10`) — a different quantity from the
`B*` edge, not updated to v14 (expected).

---

### 2. The moved-pair adjacent-budget ledger (AUDIT)

All integers recomputed from `n=2^{21}, k=2^{20}, p` via #329's imported exact
routines; margins cross-checked to the v14 script within `0.0003` bit.

| ledger cell | KoalaBear MCA `(1116047, 1116048)` | Mersenne-31 MCA `(1116023, 1116024)` |
|---|---:|---:|
| `p` | `2^{31}-2^{24}+1 = 2130706433` | `2^{31}-1 = 2147483647` |
| `q = p^{ext}` | `p^6` (186-bit) | `p^4` (124-bit) |
| `ε*` | `2^{-128}` | `2^{-100}` |
| **`B* = ⌊ε* q⌋`** | **`274980728111395087`** (58-bit, `2^{57.9321}`) | **`16777215 = 2^{24}-1`** (24-bit) |
| `K = k+1` | `1048577` | `1048577` |
| `w0 = a0'-K`, `w1 = a0'+1-K` | `67470`, `67471` | `67446`, `67447` |
| identity floor `L(a0')` `= M(a0')` | `138634741058327852652` | `4281388998575706` |
| **pass margin `log2(M/B*)` @ `a0'`** | **`+8.9777`** b (fires ✔, MCA-unsafe) | **`+27.9270`** b (fires ✔) |
| identity floor `L(a0'+1)` `= M(a0'+1)` | `57198030366` | `1752700` |
| **fail margin `log2(M/B*)` @ `a0'+1`** | **`−22.1969`** b (quiet) | **`−3.2589`** b (quiet) |
| lossless `M = L`? | yes (both points) | yes (both points) |
| adjacent-stratum 1-bit bracket @ `a0'+1` | `[2^{-23}, 2^{-22})` | `[2^{-4}, 2^{-3})` |
| errors at open step `r = n-(a0'+1)` | `981104` | `981128` |
| **tangent lower floor** `= n-a0' = r+1` | `981105` | `981129` |
| tangent *upper* bound licensed? | **no** (needs `3r ≤ n-k`; `r ≫ 349525`) | **no** |
| lower mass at open step `= max(M, tangent)` | `57198030366` (quantitative dominates) | `1752700` (quantitative dominates) |
| budget after tangent `B*-(r+1)` | `274980728110413982` | `15796086` (`≈ 2^{23.913}`) |
| **deficit to *reach* `B*`** `= B*-max-lower` | `274980670913364721` | `15024515` |
| **deficit to *cross* `B*`** `= (B*+1)-max-lower` | **`274980670913364722`** (= #310) | `15024516` |
| closest safe-theorem gap | `−377019` | `−377043` |

**Deficit convention.** MCA-unsafe requires the bad-slope count to *exceed*
`B*` (i.e. reach `B*+1`); `deficit_to_cross = (B*+1) − M(a0'+1)`. For KB this is
`274980670913364722`, matching `f049b91` exactly. Lower certificates are
combined by **max, never sum**, so the tangent floor (981105 / 981129) is
dominated by the quantitative floor at both open steps and contributes nothing
extra.

**Applicability audit (every gap negative — no existing theorem pays either
row):**

| safe-side theorem | `a_min-safe` | KB-MCA `a0'+1 − a_min` | M31-MCA `a0'+1 − a_min` |
|---|---:|---:|---:|
| `thm:deep-mca` (self-contained, `3r ≤ n-k`) | `1747627` | `−631579` | `−631603` |
| `cor:conditional-half` (BCIKS20, `2r ≤ n-k`) | `1572864` | `−456816` | `−456840` |
| `thm:elementary-ca` (half-Johnson) | `1790031` | `−673983` | `−674007` |
| PR271-280 BCHKS25 Thm 4.6 (conditional) | `1493067` | `−377019` | `−377043` |

Closest miss `377019`/`377043` agreement points; the moved rows sit deep inside
the still-open v12 band `≈ (1/4, 0.4679)`, glued to their new unsafe edge.

---

### 3. The complete 21-scale × 3-profile rung-margin audit at the moved pairs (AUDIT)

**Question (Audit 1 of `cap25_v13_missing_inputs_strategy.md` §2.1, re-posed at
the moved pairs):** does any dyadic rung `c = 2^j` (`j = 0…20`) in any of the
three slack profiles the v13 tex defines — graded prefix floor (`Gfloor`
`m=⌊a/c⌋` / `Gceil` `m=⌈a/c⌉`), quotient-remainder floor (`Rem`, covers exactly
`a`), planted quotient-core (`Plant`) — come out **inverted** (fires) or
**tight** (within 1 bit of `B*`) at `a0'+1`, now that the comparison is against
`B*` via the lossless `L → M` conversion? Every verdict below is an exact integer
comparison `M > B*` / `B*/2 < M < 2 B*`.

#### 3.1 Verdict table (exact integer)

| | KoalaBear MCA | Mersenne-31 MCA |
|---|---|---|
| any frontier-covering floor **fires** (inverted) at `a0'+1`? | **No** | **No** |
| any frontier-covering floor **within 1 bit** (tight) at `a0'+1`? | **No** | **Yes — `Gceil c=2048`, −0.3938 b** |
| tightest frontier-covering floor @ `a0'+1` | `c=1` identity, **−22.1969 b** | `c=2048` `Gceil`, **−0.3938 b** |
| its exact mass / bracket | `M = 57198030366`, `[2^{-23},2^{-22})` vs `B*` | `M = 12769758`, `[2^{-1},2^{0})` vs `B*` |
| overall | **GREEN** | **TIGHT** (non-firing watch-item) |

#### 3.2 Graded-ceil margin profile `log2(M_c/B*)` at `a0'+1` (frontier-bearing at every `c`)

`Gceil` (`m=⌈a/c⌉`, covers `mc ≥ a`) is the pure-scale floor that bears on the
frontier at every scale. Margins (bits), all `< 0` (quiet):

| row | `c=1` | 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 | 512 | 1024 | **2048** | 4096 | 8192 | 2^14 | 2^15–2^16 | 2^17 | 2^18 | 2^19 | 2^20 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| **KB MCA** | −22.20 | −29.48 | −32.87 | −34.32 | −34.79 | −50.36 | −56.93 | −57.93 | −47.34 | −40.06 | −36.16 | −33.96 | −48.20 | −54.93 | −57.93 | −57.93 | −44.45 | −52.12 | −55.93 | −57.93 |
| **M31 MCA** | −3.26 | −3.04 | −2.68 | −2.25 | −17.37 | −9.10 | −4.71 | −2.27 | −16.39 | −7.61 | −2.96 | **−0.39** | −14.45 | −21.19 | −24.00 | −24.00 | −10.52 | −18.19 | −22.00 | −24.00 |

`Gceil` never degenerates for the MCA rows (unlike `Gfloor`, which degenerates
at `c ≥ 2^{17}` because `K = k+1` is not a power of two). For **KB-MCA** the
identity scale `c=1` is terminal (−22.20 b) and every coarse rung is tens of
bits below `B*`. For **M31-MCA** the small budget (`2^24`) lets several coarse
graded rungs graze the budget: `c ∈ {8, 128, 1024}` land at ≈ −2 to −3 b and
**`c = 2048` lands at −0.3938 b** — the single sub-bit frontier-covering
comparison in the entire moved audit.

#### 3.3 Dissection of the M31-MCA `Gceil c=2048` tight rung (the watch-item)

- `c = 2048`, `N = n/c = 1024`, `m = ⌈1116024/2048⌉ = 545`, covered agreement
  `mc = 545·2048 = 1116160 ≥ a0'+1 = 1116024` (frontier-covering), exponent
  `w = m − ⌈K/c⌉ = 545 − 513 = 32`.
- Mass `L = ⌈C(1024,545)/p'^{32}⌉ = 12{,}769{,}758`; deep-point count
  `M = 12{,}769{,}758` (lossless). Exact verdict `M · 1 ≤ B*_M31 · 1`, i.e.
  `12769758 ≤ 16777215` is **True** → **QUIET (does not fire)**; `2M > B*` and
  `M < 2 B*` → **TIGHT**. Margin `log2(M/B*) = −0.3938` b.
- **Why it is not a falsifier:** it does not fire (`M < B*`), so it certifies
  nothing unsafe at `1116160 ≥ a0'+1`; the open step `1116024` therefore stays
  conjecturally MCA-safe. Were this rung ever to *fire* (e.g. a fiber-imbalance
  giving `> B*` planted codewords at agreement `1116160`), unsafety would
  propagate down to `1116024` and refute `prob:v13f1-frontier` — hence it is
  the row's binding periodic watch-item, with essentially zero slack.
- **Companion non-threat, for completeness:** the `Gfloor c=2048` cell (`m=544`,
  covered `1114112 < a0'+1`) *does* fire (+30.79 b), but it is **sub-frontier**
  — it certifies unsafety at the already-unsafe agreement `1114112 ≤ a*`, not at
  `a0'+1`, and is correctly excluded from the inversion test.

#### 3.4 Remainder and planted profiles at `a0'+1` (AUDIT — dominated)

- **`Rem`** (covers exactly `a0'+1`): the residual `s = (a0'+1) mod c` forces a
  prefix weight `w_c(s,σ)` that explodes for every `c ≥ 2` (e.g. M31 `c=2048`:
  `s=1912`, `w_c = 63127`, mass `M = 1`, margin `−24.0` b). No remainder floor
  fires or is tight at either moved open step.
- **`Plant`** (`P_c = C(n/c-1, k/c)` vs `B*`): covers `a0'+1 = k+σ` only for
  `c > σ = a0'+1-k ≈ 67472`, i.e. `c ≥ 2^{17}`, where `P_c` shrinks
  (`C(15,8)=6435` at `c=2^{17}` → `1` at `c=2^{20}`); `−44.3…−57.9` b (KB) /
  `−11.4…−24.0` b (M31) below `B*`. No planted core fires or is tight.

---

### 4. Updated named-input targets (`CONDITIONAL_ON_NAMED_INPUT`)

A factor `n^C` costs `21C` bits. The `B*` budgets are unchanged by the move, so
the **aperiodic / sparse / L1 ceilings are unchanged**; the **descent per-rung
loss ceiling is re-based** on the new open-step fail margin (the old
`(q+k)/k`-gap descent numbers are RETIRED with the `(q+k)/k` framing).

| named input | KoalaBear MCA | Mersenne-31 MCA |
|---|---|---|
| sparse `σ_C(δ') ≤ B*` (`thm:sparsify`, `δ' = r(a0'+1)/n`: `981104/2097152` KB / `981128/2097152` M31) | `≤ 274980728111395087` | `≤ 16777215` |
| aperiodic `B_ap ≤ n^C` — max integer `C` | `C = 2` (`n^2 = 4398046511104`) | `C = 1` (`n^1 = 2097152`) |
| …after paying the tangent floor | still `C = 2` | still `C = 1` (`B*-(r+1)=2^{23.913}`) |
| list max-fiber `≤ B*` | `≤ 274980728111395087` | `≤ 16777215` |
| **descent fail margin `M`** (new open step, vs `B*`) | **`22.1969` b** | **`3.2589` b** |
| max geomean per-rung loss `2^{M/21}` (divisor-lattice depth `R=21`) | **`2.0806`** | **`1.1136`** |
| ref. only: `2^{M/17}` (Gfloor-nondeg count = 17, MCA degenerates at `c≥2^{17}`) | `2.472` | `1.1421` |

**KB affords `n^2`; M31 affords only `n^1`** — the M31 aperiodic cell must be
*linear* in `n` (`B*_M31/n ≈ 8`, so the whole M31 budget is ≈ 8 linear-sized
cells). The **binding descent tolerance is now M31-MCA's `2^{M/21} = 1.1136`**
(only `3.26` bits of headroom at the new open step), consistent with §3's
finding that the M31 row is the tight one; the recursion must be near-lossless
(geometric-mean per-rung loss below `1.11`). *Subtlety preserved from v13:* the
descent depth is the divisor-lattice depth `R = log2 n = 21`, **not** the
Gfloor-nondegenerate rung count (17 for MCA); the two must not be conflated.

---

### 5. Row-object clarifying remark — list vs MCA at agreement 1116047 (and 1116023)

The moved MCA edges land on agreements that are *also* named in the unchanged
list rows. This is **not** a contradiction — they are different row-objects with
different theta-thresholds:

- **`1116047`** is simultaneously (a) the KB-**list** row's conjectured-safe
  open step — the `a0+1` of the unchanged list pair `(1116046, 1116047)`, a
  statement about the **list-decoding object** `K = k` compared against
  `Θ_list = q/2^{128} = B*`; and (b) the KB-**MCA** row's new unsafe edge `a0'`
  — a statement about the **MCA object** `K = k+1` whose bad-slope count crosses
  `B*`. A word can be list-decoding-safe at `1116047` (`≤ B*` list codewords in
  dimension `k`) while the dimension-`k+1` deep-list construction plants a
  received line with `> B*` MCA-bad slopes: the MCA edge sits **exactly one
  agreement past the list edge**, which is precisely the `K = k+1` vs `K = k`
  offset (the new MCA edge `1116047` = list edge `1116046` + 1).
- Identically, **`1116023`** is the M31-**list** open step (`a0+1` of the
  unchanged `(1116022, 1116023)`) *and* the M31-**MCA** new unsafe edge `a0'`.

So "KB list conjectured-safe at `1116047`" (a LIST statement) and "KB MCA
unsafe at `1116047`" (an MCA statement) coexist without conflict; the packet
should carry this remark so the shared agreement number is never read as an
inconsistency.

---

### 6. Consistency, status, reproducibility

- **No proved-safe statement is contradicted.** Only the finite adjacent-pair
  *prediction* of `prob:v13f1-frontier` (an open Problem, route-relative) moves;
  the asymptotic ceiling `1 - ρ - g* = 0.4678266` (`def:v13f1-gstar`) survives,
  with the quantitative route realizing all but ≈ 1.5 steps of it.
- **Per-claim status:** §1–§4 ledger/rung arithmetic = **`AUDIT`**; named-input
  targets = **`CONDITIONAL_ON_NAMED_INPUT`**; "`a0'+1` first MCA-safe" =
  **`CONJECTURAL_WITH_FALSIFIER`** for both moved rows. **Explicit falsifier
  now on record for M31-MCA:** the `Gceil c=2048` rung firing (any construction
  yielding `> 16777215` planted codewords at agreement `1116160`) refutes the
  M31-MCA adjacent pair; it currently misses by `0.3938` bit
  (`16777215 − 12769758 = 4007457` codewords of headroom).
- **Reproducibility:**
  `python3 "experimental/scripts/towards v13/cap25_v14_moved_frontier_checks.py"`
  (maintainer script, commit `2b5b7ce`; edge/open orientation, exact) and
  `python3 experimental/scripts/verify_frontier_adjacent_v13_rows.py` --
  now **7/7 gates green** (`G1`-`G6` on the four deployed v13 rows,
  unchanged; the new `G7` independently recomputes every field of this
  section's moved-pair ledger and the M31 tight-rung finding from `n, k, p`
  alone, and cross-checks the maintainer script's margins to <0.1 bit). The
  moved-pair ledger fields are committed in the `v14_moved_pair` block of
  `kb_mca_v1.packet.json` / `m31_mca_v1.packet.json` (this note's own
  companion packets, superseding the scratch-only `wave7_v14_numbers.json`
  this addendum was originally drafted against); the KB anchors
  `L(1116044), M(1116044), M=L(1116047), M=L(1116048)` byte-match `f049b91`.

### Constants (v14 addendum)

| constant | value |
|---|---|
| `n = 2^{21}` | `2097152` |
| `k = 2^{20}` | `1048576` |
| `p_KB = 2^{31}-2^{24}+1` | `2130706433` |
| `p_M31 = 2^{31}-1` | `2147483647` |
| `q_KB = p_KB^6` | 186-bit |
| `q_M31 = p_M31^4` | 124-bit |
| `B*_KB = ⌊2^{-128} q_KB⌋` | `274980728111395087` (58-bit) |
| `B*_M31 = ⌊2^{-100} q_M31⌋` | `16777215` (24-bit) |
| moved KB-MCA pair | `(1116047, 1116048)`; margins `+8.9777 / −22.1969` b |
| moved M31-MCA pair | `(1116023, 1116024)`; margins `+27.9270 / −3.2589` b |
| M31-MCA tight rung | `Gceil c=2048`, `M=12769758` vs `B*=16777215`, `−0.3938` b |
| descent depth `R` | `log2 n = 21` |
