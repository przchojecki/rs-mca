# Audit: v4 synthesis bibliography and source pins (v2)

```yaml
workboard_item: K0
row: KoalaBear MCA and Mersenne-31 list contract constants, audited inside the whole v4 catalogue (four Proth rows, F_{17^32}, corridor rows, deployed floors)
object: OTHER (bibliography, cite/bibitem integrity, blob pins, printed integers, status labels)
target_epsilon: n/a (row targets 2^-128 and 2^-100 carried through unchanged)
agreement: n/a (audit spans rows)
B_star: 274980728111395087 (KoalaBear) and 16777215 (Mersenne-31), both re-derived
direct_statement: on the checked scope every \cite resolves to a \bibitem, every printed integer and status label re-derives from its named source or from exact arithmetic, all 18 pinned paths exist at 5ecb9ab5 and at b13de81, and the four thm:proth primes carry deterministic Proth certificates; six pre-circulation defects remain open (F1-F5, F7), one of them submission-critical
architecture: DIRECT (provenance audit; no partition)
partition_digest: n/a (DIRECT)
atom_or_cell: DIRECT
quantifier: exhaustive over the checked scope; the unchecked scope is enumerated explicitly
projection_and_unit: bibliography entries, cite/bibitem keys, blob-pin paths, exact integers, status labels
claimed_bound: 0 integer defects and 0 status-inflation defects on the checked scope; 6 open pre-circulation defects
status: AUDIT
impact: LOCAL_ONLY
falsifier: any checked integer that does not re-derive; any \cite without a \bibitem; any pinned path missing at either commit; any checked status label stronger than its source supports; any thm:proth row whose Proth decomposition, size condition, or witness congruence fails
replay: cd experimental/lean/v4_proth_certificates && lake build   (stdlib-only, clean build under 1 s; native_decide disclosed). Citation, orphan, and pin checks replay as the git and grep one-liners printed in the note.
```

- **Date:** 2026-07-24.
- **Author:** Holm Buar.
- **Base:** `b13de81`. `experimental/proximity_prize_results_v4.tex` is byte-identical
  to the audited `f6a20fa` revision (`git diff f6a20fa b13de81 -- <path>` is empty),
  so every line reference below is valid at both commits; the pin, orphan, and
  count checks were nevertheless re-run at `b13de81`.
- **Scope.** Bibliography, citation integrity, printed exact integers and status
  labels, and source pins of `experimental/proximity_prize_results_v4.tex`,
  checked against the cited manuscripts and packets pinned at
  `5ecb9ab538a0a57dcb81018b17f32849049fb998`. Prompted by the maintainer's
  request to audit the v4 bibliography and source pins before external
  circulation. This note edits neither the manuscript nor any source.

## Verdict

**OPEN GAP.**

- **Workboard item:** K0. The audit maintains the provenance of the frozen row
  contract: the constants it re-derives are the ones the active contract and its
  candidate atoms bind to (`B*`, the printed reserve, the four deployed unsafe
  agreements and their radius fractions, and the eighteen source pins).
- **Smallest missing object:** an auditable source for `ChoComp26`. Concretely,
  the new-in-v4 figure "at least `1133314` projective minimum directions"
  (v4:472) is the only integer in `thm:m31-companion` that neither an in-repo
  file nor exact arithmetic reproduces. Supplying `ChoComp26` as an ePrint or in
  the source-release bundle closes the gap; nothing smaller does, because the
  theorem's remaining integers already re-derive (F1 mitigant).

On the checked scope there are **0 integer defects and 0 status-inflation
defects**: every exact integer and every status label re-derives from its named
source or from exact arithmetic, every `\cite` resolves, and all eighteen pinned
repository paths exist at both the pin commit and the base commit. Six
bibliography/label items (F1-F5, F7) remain open and should be fixed before
external circulation; only F1 gates circulation. F6 records seven descriptive
citation brackets that are correct as printed.

The predecessor packet ended `NO ISSUE`. That verdict was wrong under the
repository audit rule: an audit that records actionable defects, including a
submission-critical missing source, ends `OPEN GAP` unless the defects are
repaired in-tree and the verdict becomes `FIXED`. The defects here are in the
maintainer's manuscript, which this packet does not edit, so `OPEN GAP` is the
terminal verdict for it.

## Findings

### F1 [SUBMISSION-CRITICAL] `ChoComp26` has no in-repo source and no ePrint number

`ChoComp26` carries load-bearing unconditional statements: the first Mersenne
primitive cell and Delsarte-barrier theorem `thm:m31-companion` (v4:453-475), the
`S+A+E` contract (v4:692-694), and the closing attribution (v4:476):

> "The cubic certificate, exact full Delsarte optimum, critical-core abundance,
> field descent, and owner concentration are in \cite{ChoComp26}." (v4:476)

The bibliography entry (v4:749-752) resolves to nothing checkable:

> "P. Chojecki, RS--MCA v4.4: ..., companion preprint included with the source
> release of the present paper, 2026." (v4:751-752)

It is the only bibliography key carrying **neither** an IACR ePrint report number
**nor** a pinned repository href. A grep at the base commit for the entry's
identifying integers and phrases (`16760701`, `16838532`, `critical core`, `owner
concentration`, `execution ledger`, and the paraphrase `Cubic closure`) returns
hits **only** inside `proximity_prize_results_v4.tex`, or none at all. There is no
in-repo file backing these theorems.

*Mitigant.* Every reconstructible integer in `thm:m31-companion` re-derives under
exact arithmetic: the Johnson-scheme Delsarte LP optimum
`1031427641435096867222903646984 / 61254010871010657240949 =
16838532.3143506... > 16777215`; the cubic-cell bound `16760701 < 2^24`; and the
owner concentration `ceil(63684220 * C(440837,8) / C(1053558,8)) = 59838`. The
one figure new in v4, "at least `1133314` projective minimum directions"
(v4:472), has no in-repo source and is **not** reconstructed here; it is the
named missing object of the `OPEN GAP` verdict above.

*Fix.* Give `ChoComp26` an IACR ePrint report number, or ship the companion in
the source-release bundle, before the paper circulates externally.

### F2 [DISCLOSURE-COVERAGE] the unpinned-field caveat omits the length-1024 rows

The corridor remark scopes its unpinned-prime disclaimer to the prize-scale rows
only:

> "The prize-scale corridor packet uses a pinned exact budget convention
> corresponding to a line field near $2^{255.9}$; it does not yet pin one literal
> prime in the paper." (v4:293-295)

The source packet flags **both** scales in its Non-claims section:

> "Row C's literal ~2^250 prime is unpinned (qa3 flag C1(b)); prize 2^255.9 is a
> convention." (`corridor-unconditional-safe-edges/README.md`, Non-claims)

The three length-1024 (Row C, `n = 2^10`) rows in `tab:corridor` (v4:283-285)
therefore rest on the same idealized, not-yet-pinned field, but the remark
mentions only the prize-scale (`n = 2^41`) rows. The values themselves are
digit-for-digit correct: the six safe radii `512, 663, 769, 1092724518963,
1415997755216, 1644686143216` match the packet's Haböck column and the
`tab:corridor` column exactly.

*Fix.* Extend the remark's unpinned-field caveat to the length-1024 rows.

### F3 [LABEL-IMPRECISE] `ChoThresholds26` citation bracket names a non-existent section

Corollary `cor:abf`(iii) points at a titled statement that does not exist:

> "...the explicit integer consequences stated in \cite[Line decoding and
> list-decoding consequences]{ChoThresholds26}." (v4:332)

At the base commit, `experimental/rs_mca_thresholds.tex` has **zero**
section/subsection/theorem headings containing "line decoding" or "list-decoding"
(0 heading hits). The only occurrence of "list-decoding" is prose (thresholds:
3795); the underlying list-size-consequence content is present but untitled. The
bracket text reproduces a section name from the retired v3 synthesis, not a
statement in `ChoThresholds26`.

*Fix.* Point the bracket at the actual list-consequence statement in
`rs_mca_thresholds.tex`, or drop the descriptive bracket.

### F4 [OBVIOUS-FIX] two orphan bibliography entries: `CS25`, `GG25`

`\bibitem[CS25]{CS25}` (v4:801) and `\bibitem[GG25]{GG25}` (v4:806) are defined
but never `\cite`d anywhere in the body (orphan set `== {CS25, GG25}`).
`GG25`'s subject appears only as prose:

> "This is not the stronger Goyal--Guruswami notion of $(\delta,A,B)$
> line-decodability." (v4:320)

which is not a `\cite`. There is no dangling citation in the other direction:
every `\cite` key in the body resolves to a `\bibitem`.

*Fix.* Cite each entry where its result is used, or remove the two orphan
entries.

### F5 [MINOR] `ChoShort26` title drift against its own source file

The bibliography entry prints:

> "MDS paving bounds for Reed--Solomon MCA, version 9.2, IACR Cryptology ePrint
> Archive, Report 2026/1463, 2026." (v4:729-730)

The source file's own title line reads differently:

> "\title{Shortening Bounds for Reed--Solomon MCA}" (`RS_MCA_Paving_v9.2.tex`:130)

The ePrint number (2026/1463) and version (9.2) are correct; only the
human-readable title drifts. The cited "MDS paving bounds..." matches the
published ePrint and the repository index name, while the file's `\title` still
reads "Shortening Bounds...".

*Fix.* Reconcile the two: update the file's `\title` to the published title, or
match the bibliography to the file's `\title`.

### F7 [LABEL-IMPRECISE] the Acknowledgements misname the attribution mechanism

The Acknowledgements state where contributor credit lives:

> "Contributor-specific results are attributed in theorem headings and
> bibliography entries." (v4:708)

In v4 the theorem headings carry no contributor names at all. Across every
`theorem`, `proposition`, `lemma`, `corollary`, and `conjecture` heading in the
manuscript, the count of occurrences of any acknowledged contributor's name is
zero; the headings are uniformly descriptive, e.g. `[Source-coordinate tangent
atom]` and `[KoalaBear rank-nine moving-root boundary cut]`.

Per-result attribution in v4 lives instead in the `\source{...}` lines. There are
33 of them; 12 name a contributor directly:

> "\source{Holm Buar, \cite{BuarKBTangent26}. ...}" (v4:496)
>
> "\source{Danny, \cite{DannyCoordinateSpan26}. ...}" (v4:509)
>
> "\source{Scott Hughes, \cite{HughesKBM126}. ...}" (v4:544)

The sentence is inherited rather than newly wrong. Its v3 ancestor read "The
theorem headings and bibliography identify the source of each collaborative
result" (`proximity_prize_results_v3.tex` at `5ecb9ab5`), and that was accurate
for v3: v3 carried twelve name-bearing headings — `[Buar: source-coordinate
tangent atom]`, `[Danny: pole-tolerant scalar-locator localization]`, `[Hughes:
fixed-$G$ universal embedding]`, and nine more — and zero `\source` lines. The
v3->v4 rewrite inverted the mechanism (12 named headings -> 0; 0 `\source` lines
-> 33) and reworded the sentence, but kept "theorem headings".

The "bibliography entries" half remains correct, including for the two
contributors who appear in no `\source` name position: Latif and Hart are
credited through the packets cited at v4:292 and v4:207, whose `\bibitem`
entries carry their names.

*Fix.* Reword to name the mechanism v4 actually uses, e.g. "Contributor-specific
results are attributed in the per-result source lines and bibliography entries."
No theorem, exact value, or status label is affected.

## F6 [NO ISSUE] descriptive citation brackets that paraphrase source titles

Seven `\cite[...]` brackets restate the cited source's own section/theorem title
rather than quoting it verbatim. The cited result exists in each case, so these
are acceptable as printed and are listed only for completeness:

- v4 `[Quadratic staircase]` -> source title "Exact quadratic staircase".
- v4 `[Exact target compiler]` -> source "self-contained / almost-half-distance
  target compiler".
- v4 `[Four certified smooth rows]` -> `ChoThresholds26` "Certified
  Proximity-Prize rows at all four rates".
- v4 `[Binary additive-domain rows]` -> source "exact binary additive-domain
  examples".
- v4 `[Large scalar-extension exponent]` -> `ChoGF26` "unconditional
  shallow-prefix RS--MCA exponent".
- v4 `[Universal field-size cap]` -> `ChoCap26` "...for the challenge envelope".
- v4 `[Corrected deployed identity-prefix floors]` -> `ChoCap26` "deployed MCA
  frontier floors".

## The four `thm:proth` rows: source-bound deterministic certificates

The predecessor packet asserted primality of the four `tab:proth` primes "under
deterministic Miller-Rabin". Two things are wrong with that. First, a fixed
small-base Miller-Rabin battery is not a deterministic primality test at these
sizes: the four values are 167 to 171 bits, far above the range where a fixed
base set is proved to decide primality. Second, and more to the point, the
repository already contains deterministic certificates for exactly these four
primes, and the audit should have source-bound to them instead of re-testing the
primes probabilistically.

The certificates are `prop:proth-row-check` in `experimental/rs_mca_thresholds.tex`
(condition `PC1`, lines 1857-1858), with the per-row data also machine-readable in
`experimental/data/certificates/proth-rows/proth_rows.json`:

> `p = u 2^s + 1`, `u` odd, `u < 2^s`, `a_0^{(p-1)/2} = -1 (mod p)`. `PC1`

The Miller-Rabin claim is withdrawn. Primality of the four rows is source-bound to
`prop:proth-row-check`; what this packet adds is an independent rederivation and a
kernel-checked replay.

**Independent rederivation.** The Proth data was recomputed here from the printed
primes alone, without reading the certificate section, by factoring out the
2-part of `p - 1` and searching for the smallest Proth witness. The result agrees
with the in-tree certificate on every field of every row — `(s, u, a_0)` identical
in all four cases:

| rate | `n` | bits of `p` | `s` | bits of `u` | `u < 2^s` | witness `a_0` | `B = floor(p/2^128)` |
|---|---:|---:|---:|---:|:---:|---:|---:|
| `1/2`  | `2^41` | 167 | 92 | 75 | yes | `3`  | `389500552609` |
| `1/4`  | `2^42` | 169 | 93 | 76 | yes | `13` | `1210584858040` |
| `1/8`  | `2^43` | 170 | 95 | 75 | yes | `5`  | `2879806199253` |
| `1/16` | `2^44` | 171 | 97 | 74 | yes | `5`  | `6233898019554` |

**Proth's criterion** (Proth 1878, classical). Let `N = u * 2^s + 1` with `u` odd
and `u < 2^s`. If some `a_0` satisfies `a_0^((N-1)/2) = N - 1 (mod N)`, then `N`
is prime.

The criterion's implication is cited, not formalized; it is the implication
`prop:proth-row-check` itself invokes. What the Lean package proves, per row, by
kernel-checked arithmetic, is exactly the certificate's hypotheses and the
witness congruence:

1. the decomposition `p = u * 2^s + 1`;
2. `u` odd;
3. the size condition `u < 2^s` (each `u` is 74-76 bits against `s = 92-97`, so
   the condition holds with room, and `2^s` exceeds `sqrt(p)`);
4. the witness congruence `a_0^((p-1)/2) = p - 1 (mod p)` at the certified `a_0`;
5. the printed budget `floor(p / 2^128) = B` (the `PC2` bracket
   `B 2^128 <= p < (B+1) 2^128` in the same proposition);
6. `2^n | p - 1`, so the smooth subgroup of order `2^n` that the row uses exists.

Three controls are included so the check is visibly non-vacuous: `a = 2` is
proved **not** to be a Proth witness for the rate-`1/2` row; the composite
`3 * 2^92 + 1` of the same shape is proved to have no witness among the 62 bases
below 64; and the modular-exponentiation routine is proved to agree with `a^e % 97`
on all `a, e < 12`.

Each row's six conditions are also available as one Boolean, `ProthRow.check`,
and `allRows_check` states that all four rows pass together.

Not covered here: the `F_{n,k}` sign conditions and the `r_quad`/`r_rho`
identification, which `prop:proth-row-check` also asserts and which the existing
in-tree audit `experimental/notes/audits/proth_rows_certificate_audit.md` already
checks. This packet re-derives the primality and budget data only.

## Verified clean (independently re-derived)

The positive content behind the "0 integer defects" half of the verdict.

1. **Four Proth rows (`thm:proth`, tab v4:185-188).** Certified as above:
   deterministic Proth certificate per row source-bound to `prop:proth-row-check`
   and independently rederived, `2^n | p-1`, and exact `B = floor(p/2^128)` for
   all four rows.
2. **Exact `F_{17^32}` threshold (`thm:f17`).** `floor(17^32/2^128) = 6`, hence the
   printed complete safe set `[0, 6/512)`.
3. **Corridor table vs packet, digit-for-digit.** The six safe integer radii in
   `tab:corridor` equal the Haböck column of the `Corridor26` packet README and
   the hardcoded expected six, all three identical. "The Haböck bound is the
   stronger of the two in all six rows" (v4:271) matches the packet; the packet's
   "delta <= 0.2045 < 1/4" line is the deployed-KoalaBear row, **not** a corridor
   row, so there is no status inflation. `GKL24` is cited as version 3.
4. **Deployed unsafe floors (`thm:deployed-unsafe`).** The four unsafe agreements
   `1116047` / `1116023` (MCA) and `1116046` / `1116022` (list) match
   `tex/cs25_cap_v13_2.tex`; the four radius fractions `981105/2097152`,
   `490553/1048576`, `981129/2097152`, `490565/1048576` reduce consistently from
   `(n - a_0)/n` at `n = 2^21`; the Mersenne-31 target is correctly `2^-100`, not
   `2^-128`.
5. **Universal-cap terminal edges (`tab:threshold-map`, v4:385-387).** The three
   prize-corridor unsafe edges are exact:

   ```text
   383/512  = 1 - 1/4  - 2^-9      prize corridor, rate 1/4
   447/512  = 1 - 1/8  - 2^-9      prize corridor, rate 1/8
   959/1024 = 1 - 1/16 - 2^-10     prize corridor, rate 1/16
   ```

   The manuscript is correct as printed. The predecessor packet's rate labels for
   these three rows were shifted by one; see "Corrections to the predecessor
   packet" below.
6. **KoalaBear tangent reserve (`thm:kb-tangent`).** With `p_KB = 2^31-2^24+1 =
   2130706433` read back from `Conjectures_and_Barriers_RS_MCA_v4_1.tex`:1072,
   `floor(p_KB^6/2^128) = 274980728111395087` (the deployed `B*`) and the printed
   reserve `274980728111395087 - 981104 = 274980728110413983`.
7. **Pin integrity, 18/18 at both commits.** Every one of the eighteen `blob`
   hrefs pinned at `5ecb9ab5` resolves via `git cat-file -e` at both
   `5ecb9ab5` (pin) and `b13de81` (base); no pin broke in the v3->v4 move, and
   the short form `5ecb9ab5` at v4:77 is a correct prefix.
8. **No dangling citations, including the deliberately dropped keys.** Every
   `\cite` resolves; the dropped `RepoLog26` (coordination log, not proof
   authority, v4:77) and the dropped `BuarKBQ26` / `Bua26b` (conditional cut)
   leave no dangling `\cite` — all three keys are fully absent from the body.

## Unchecked (with reasons)

- **`ChoComp26` entirely (F1).** No in-repo source; the reconstructible integers
  re-derive under exact arithmetic, but the underlying theorems and the new-in-v4
  `1133314` figure are not verifiable against any in-repo file.
- **Eleven pull-request-linked citations** (`#1048`, `#1055`, `#1056`, `#1057`,
  `#993`, `#1058`, `#1060`, `#1061`, `#1015`-`#1018`). These resolve to remote
  pull-request URLs, not offline-checkable here; all fall inside the reviewed
  integration waves recorded in the repository coordination log.
- **`thm:active-payments` exact values.** The `b_0` thresholds `70230` / `108962`,
  the certified maxima `274974976450914526`, `274975238687487221`, `16776934`,
  `16776950`, and the paving-basis `J_{B*}` tables are source-bound to `ChoGF26`
  and were not recomputed.
- **`thm:high-ledger` interior.** The coding-ledger identity `N_coding = l + sum
  d_i(r+1)` and items (i)-(iii): the pinned packet exists but was not
  deep-checked.
- **External ePrint theorem numbers.** `ABF26` Thms 5.2 / 5.3 / 4.21, the
  `BCHKS25` two-radius theorem, `GKL24` Thm 3, `Hab25` Thm 2: the ePrints were
  not opened.

## Corrections to the predecessor packet

The predecessor submission (closed with a repair list) contained four defects of
its own. None of them is a defect in `proximity_prize_results_v4.tex`; all four
are in the audit packet, and all four are repaired here.

1. **Verdict.** It ended `NO ISSUE` while recording six actionable defects, one
   submission-critical. Under the repository audit rule the correct terminal
   verdict is `OPEN GAP`, which this note now carries, with the workboard item
   and the smallest missing object named.
2. **`workboard_item: n/a`.** The packet header requires a live item. Bound here
   to K0, with the K0-relevant checked constants listed explicitly.
3. **Primality.** It claimed the four `tab:proth` primes are prime "under
   deterministic Miller-Rabin". A fixed small-base battery is not deterministic at
   167-171 bits, and the repository already carries deterministic Proth
   certificates for these exact primes in `prop:proth-row-check`. The claim is
   withdrawn, source-bound, independently rederived, and kernel-checked.
4. **Rate labels on the corridor edges.** Clean-item 5 attached `383/512`,
   `447/512`, `959/1024` to `rho in {1/2,1/4,1/8}` plus `rho = 1/16`.
   `tab:threshold-map` has no rate-`1/2` corridor row; the three printed rows are
   rates `1/4`, `1/8`, `1/16`, and the `2^-9` / `2^-10` split follows the row, not
   the position. The three values were and are correct; only the packet's
   description of them was wrong. Corrected in clean-item 5.

The predecessor's shipped Python verifier is withdrawn under the no-shipped-Python
rule rather than repaired, so its `--tamper-selftest` exit convention no longer
applies to any shipped artifact. The mutation battery still ran as an internal
pre-ship gate on this packet's arithmetic, with the corrected convention (exit
zero exactly when every injected mutation is caught). Six mutations were injected
one at a time into the Lean certificate data — wrong witness, wrong odd part,
wrong 2-adic valuation, wrong budget, wrong smooth exponent, perturbed prime —
and the build failed on all six; the unmutated package rebuilds green.

Defect 4 was found by re-deriving the predecessor's arithmetic from the
manuscript rather than carrying it forward, which is the reason it is worth
re-deriving inherited numbers even when the predecessor passed its own gate.

## Nonclaims

This packet claims no payment, no atom, no row bound, and no proof route. It
kills no route. `LOCAL_ONLY`: no ledger term moves. The Proth package certifies
primality, the smooth divisibility, and the printed budgets of the four
`tab:proth` rows; it says nothing about MCA, list size, slopes, or any row
inequality. Proth's criterion is cited as classical and is not formalized here.

## Replay

Arithmetic, kernel-checked:

```bash
cd experimental/lean/v4_proth_certificates && lake clean && lake build
```

Stdlib-only, no dependencies, clean build under one second. `native_decide` is
used for every theorem in the package and is disclosed: the axiom census reports
exactly one `native_decide` axiom per theorem and no `sorryAx`, no `Classical.choice`,
and no `propext`.

Independently of the note, the certificate data can be checked against its
in-tree source:

```bash
git show b13de81:experimental/data/certificates/proth-rows/proth_rows.json \
  | grep -E '"p"|proth_s|proth_u|proth_witness_a0'    # matches the table above
git show b13de81:experimental/rs_mca_thresholds.tex | sed -n '1852,1866p'   # PC1/PC2
```

Citation, orphan, and pin checks, at base commit `b13de81`:

```bash
V=experimental/proximity_prize_results_v4.tex
git show b13de81:$V | grep -c '\\source{'                      # 33
git show b13de81:$V | grep -o '\\cite\[[^]]*\]{CS25}\|\\cite{CS25}' | wc -l   # 0, orphan (F4)
git show b13de81:$V | grep -o '\\cite\[[^]]*\]{GG25}\|\\cite{GG25}' | wc -l   # 0, orphan (F4)
git show b13de81:$V | grep -o 'blob/[0-9a-f]\{7,40\}/[^}#) ]*' \
  | sed 's|blob/[0-9a-f]*/||' | sort -u \
  | while read -r p; do git cat-file -e b13de81:"$p" || echo "MISSING $p"; done   # 18 paths, none missing
git diff f6a20fa b13de81 -- $V                                  # empty: v4 unchanged since the audited revision
```

Base commit `b13de818` (`experimental/proximity_prize_results_v4.tex` identical to
`f6a20fa39f8b3ebbf98056726c69133c82309e51`); pin commit
`5ecb9ab538a0a57dcb81018b17f32849049fb998`.

**Audit verdict: OPEN GAP** on workboard item K0; smallest missing object, an
auditable source for `ChoComp26`, concretely the `1133314` figure at v4:472. Six
pre-circulation bibliography/label fixes are recorded (F1-F5, F7); the strongest,
F1, gates external circulation. Credit to Latif for the `Corridor26` packet
cross-checked in F2 and clean-item 3, and to Hart for the `F17Audit26` note
pinned in clean-item 7.
