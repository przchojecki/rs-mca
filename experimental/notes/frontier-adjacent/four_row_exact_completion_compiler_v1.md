# Four-row exact-completion compiler v1

**Status:** HISTORICAL GRANDE FINALE v3 EXACT-ARITHMETIC COMPILER /
SUPERSEDED AS CURRENT-ARTIFACT AUTHORITY / FOUR DEPLOYED ROWS OPEN.

**Supersession notice (2026-08-10).** Active Grande Finale v4 replaces the
v3 MCA additive atom interface below by the maximum-type S/A/E endgame and
adds `U_ext` to the list chronology. Consequently this packet remains useful
for its exact row calibration and historical candidate-schema route cut, but
its source hashes and `CURRENT_ARTIFACT_SET` terminal are not live authority.
Its imported partial-`U_paid` packet is consumed only for row parameter
calibration; no common-support/global-slope inference from that historical
dependency is banked. Do not use the replay commands below as a current-v4
acceptance gate.

This packet implements the literal completion interface required by
`experimental/grande_finale.tex`, Section `sec:exact-completion-ledger`, for
the four deployed adjacent rows.  It does not prove a new safe agreement.
It makes three facts executable:

1. every closing charge must live in one frozen, witness-exhaustive Grande
   Finale v3 first-match partition and use the same row, units, residual, and
   received-line quantifier;
2. the exact row budgets and prefix-average capacities are recomputed with
   big integers; and
3. the current repository does not yet contain a complete compatible atom
   set for any row.

The terminal emitted today is

```text
ARCHITECTURE_ROUTE_CUT_CURRENT_ARTIFACT_SET
```

not `SAFE`, and not a Reed--Solomon counterexample.

## 1. Statement compiled

For an MCA row, Grande Finale v3 requires

\[
 U_{\rm total}=U_{\rm paid}+U_Q+U_{\rm BC}+U_{\rm new}\le B^*.
\tag{1.1}
\]

For a list row, `U_BC` is replaced by `U_list-int`.  The active theorem also
requires an exhaustive first-match compiler with no unresolved cell.  In
particular, `U_paid` is not a free scalar: its tangent, common-support,
quotient, planted, field-drop, extension, rank, and previously certified
subcells must all be covered in the same partition.

The machine candidate schema consequently requires exactly four top-level
atoms:

```text
MCA:  U_paid, U_Q, U_BC,       U_new
list: U_paid, U_Q, U_list_int, U_new.
```

Every atom is an exact nonnegative integer in units of distinct bad slopes
per received line.  The partition digest, row id, architecture id, and
uniform quantifier must agree.  Owner ids must be disjoint.  The total is
summed once and compared with the literal row budget.

The runtime mirrors the published schema without an optional dependency and
then requires typed, payload-hashed adapters for the partition, each atom,
every Q component, and any legacy-to-active architecture/owner map.  All
source paths must be canonical, repository-contained, allowlisted proof
artifacts; equivalent path aliases, unused sources, unbound digests, and
schema-extra fields are rejected.  Flattening the four atom owner lists must
reproduce the partition's first-match owner order exactly.  A legacy bridge
must enumerate its entire declared legacy-owner domain, give each source
owner a nonempty and disjoint active-owner image, and reproduce an ordered
subsequence of the active `U_paid` owner universe; a boolean `complete` flag
alone is not accepted.  It must also carry the exact inherited charge, which
the active `U_paid` atom must include.  These checks establish internal
consistency of the declared map, not that the candidate-authored legacy
domain is the true exhaustive #995 owner universe.

This is only a **necessary structural preflight** for identity, scope, and
composition.  Candidate-authored adapters can be internally consistent while
their mathematical assertions are false.  Accordingly, `--audit-candidate`
always returns `closure_certified=false` and cannot bank an atom.  The present
trusted-source registry is empty; banking requires independent proof review
followed by an explicit compiler/registry update.  The convenience detector
forces a mapping for canonical, digest-identical, parseably embedded, and
plain-text-marked legacy rank-nine inputs, but it is not a complete detector
of arbitrary provenance transforms (for example, an encoded or semantically
rewritten copy).  That is why detector success can never substitute for the
trusted registry gate.  The registry update must also verify the complete
transitive dependency graph: every adapter chain must terminate in reviewed,
registry-pinned leaves, and self-citations or cycles must be rejected.  The
present structural preflight does not claim that stronger trust property.

## 2. Exact row replay

The compiler independently recomputes `B*`, `w`, the ceiling of the full
prefix-fiber average, and the largest full-budget multiplier.  No floating
point number decides a gate.

| row | `a+` | `w` | `ceil(binomial(n,a+)/p^w)` | `B*` | full-budget multiplier floor |
|---|---:|---:|---:|---:|---:|
| KoalaBear MCA | 1116048 | 67471 | 57198030366 | 274980728111395087 | 4807520 |
| KoalaBear list | 1116047 | 67471 | 65065153468 | 274980728111395087 | 4226236 |
| Mersenne-31 MCA | 1116024 | 67447 | 1752700 | 16777215 | 9 |
| Mersenne-31 list | 1116023 | 67447 | 1993678 | 16777215 | 8 |

The last column is a Q calibration only:

\[
 \left\lfloor
 \frac{B^*p^w}{\binom n{a_+}}
 \right\rfloor.
\tag{2.1}
\]

It is not an extension-chart degree ceiling and is not a proved `U_Q` value.
The fixed-line extension audit already produced a counterexample to the old
interpretation and is a mandatory supersession input to this compiler.

## 3. Architecture boundary exposed by the current stack

The KoalaBear rank-nine stack through #995 is exact within its declared
legacy M1 first-match architecture.  Its current local values are

\[
 U_{\rm paid}^{\rm M1}=422354730332,
 \qquad
 B_{\rm rem}^{\rm M1}=274980305756664755,
\tag{3.1}
\]

and its Q multiplier is `4807513`.  The same certificate explicitly records

```text
U_Q = null,
residual_U_A = null,
non-full-outside source load open,
rank nine open,
KoalaBear row open.
```

The local packet concerns coefficient rank two and the full-outside source
load, written after fixing a received pair and an SP3 translation.  Fixing an
arbitrary pair and choosing one SP3 normalization per pair is not by itself a
quantifier failure: the target numerator is a per-line maximum, and the SP3
theorem preserves the bad-slope set.  Likewise, the packet is correct to
forbid summing alternative pairs or translations.  The decisive gap is
different: no source-bound theorem identifies its legacy owners with one
active v3 priority map, proves exhaustive active-cell coverage and
support-to-parameter coalescing, or supplies the still-null Q/interior/
residual atoms.  Thus its field name `U_paid` is not yet the active row-global
`U_paid` of (1.1).

The stack was deliberately repinned to byte-identical archived v2 theorem
sources because the promoted Grande Finale v3 manuscript does not contain the
literal legacy first-match anchors.  No current artifact supplies a theorem
mapping #995's partition and terminals into (1.1).  The compiler therefore
reports (3.1) as exact **legacy stack-local progress**, but does not silently
subtract it from a Grande Finale v3 completion candidate.

This is the main architecture route cut:

> A legacy M1 charge may enter the active completion ledger only through an
> explicit, source-bound partition/owner mapping certificate.  Equality of
> row parameters or similarity of cell names is not such a certificate.

The cut does not invalidate #995.  It identifies the missing composition
lemma needed to turn that work into an active-row payment.

## 4. Q-lane result

The exact Q interface pins:

- row and object kind (`MCA` versus `LIST`);
- `n`, `K`, `a+`, `w`, and base-field size;
- evaluation-domain, priority-map, residual-predicate, target-map, and
  support-to-parameter coalescing digests;
- agreement/complement orientation and any transport theorem;
- realized effective-image normalization; and
- a joint maximum on the frozen residual.

Each of those components is a typed manifest with the same row, active
architecture, partition digest, and row parameters; its payload and proof
sources are hash-bound.  Complement orientation requires a typed total
transport adapter, ambient normalization requires a typed full-image adapter,
and the joint-max adapter must repeat the exact `U_Q` upper integer together
with the evaluation-domain, priority, residual, target, coalescing,
orientation/transport, normalization, and effective-image digests it jointly
maximizes.  Passing these mechanical adapters is structural preflight only;
it does not prove their cited mathematics or certify a row.

The current value of `U_Q` is `null` on all four rows.  Existing exact
ingredients do not change that conclusion:

- the Johnson/anticode upper is theorem-level but far above every deployed
  budget;
- shallow Fourier flatness stops near depth 21--22, not depth 67447--67471;
- the proved M31 one-shell cap `2029705 < 16777215` pays only its explicitly
  certified one-shell subcell; unrestricted multishell coverage is open; and
- moment, participation-ratio, Route-D, quotient-rung, and small-row packets
  are reductions, route cuts, or evidence rather than a deployed exhaustive
  max-fiber integer.

Targets, average ceilings, lower floors, separately normalized residuals, and
conditional allocations are rejected as `U_Q` upper bounds.

## 5. Uniform direct-extension dimension route cut

Suppose an exactly disjoint extension chart is paid by the proved direct
dimension--degree form

\[
 U_{\rm ext}=\Delta p^{e_Y},\qquad \Delta\ge1.
\tag{5.1}
\]

All other charges are nonnegative.  Therefore `p^e_Y` itself must not exceed
the available row budget.  This gives a row-uniform route cut before any
chart discovery:

| accounting scope | available integer | largest possible `e_Y` | largest `Delta` at that `e_Y` |
|---|---:|---:|---:|
| active KB MCA, full budget | 274980728111395087 | 1 | 129056130 |
| legacy #995 KB MCA remainder | 274980305756664755 | 1 | 129055932 |
| active KB list, full budget | 274980728111395087 | 1 | 129056130 |
| active M31 MCA, full budget | 16777215 | 0 | 16777215 |
| active M31 list, full budget | 16777215 | 0 | 16777215 |

Thus a positive-dimensional (`e_Y >= 1`) direct extension chart cannot be
part of a closing ledger under (5.1) on either M31 row, and a chart with
`e_Y >= 2` cannot be paid by this direct route on either KoalaBear row.  These
are **absolute route cuts for this charge form**, not nonexistence theorems for
the underlying charts.
The displayed `Delta` capacities are all-remainder ceilings, not banked
allocations: `U_Q` and the other cells still consume the same budget.

The compiler binds this charge theorem directly to the promoted current source
`tex/cs25_cap_v13_2.tex`.  The older fixed-line correction packet remains the
source for the Frobenius counterexample and supersession rule, but its own
standalone Python acceptance command currently has a stale source pin to the
moved `tex/cs25_cap_v12.tex` (and a removed raw-ledger path).  Its core Python
census and independent Sage counterexample replay pass; the stale all-source
gate is recorded, not concealed or treated as a passing verifier.

## 6. Current four-row verdict

No current row has all of the following in the active architecture:

1. a complete `U_paid` with exact extension and quotient subcells;
2. a deployed row-sharp `U_Q` integer;
3. exhaustive MCA balanced-core or list-interior coverage;
4. `U_new=0` or exact payments for every named residual; and
5. a complete, chronology-correct add-back certificate.

Therefore the current artifact set cannot instantiate the active exact
completion theorem for any of the four rows.  This is a sharp source and
architecture audit, not a claim that the rows are false or that no future
theorem can close them.

## 7. Replay and mutations

From the repository root:

```bash
python3 experimental/scripts/verify_four_row_exact_completion_compiler_v1.py --check
python3 -O experimental/scripts/verify_four_row_exact_completion_compiler_v1.py --check
python3 experimental/scripts/verify_four_row_exact_completion_compiler_v1.py --tamper-selftest
python3 -O experimental/scripts/verify_four_row_exact_completion_compiler_v1.py --tamper-selftest
python3 experimental/scripts/verify_four_row_exact_completion_compiler_v1_independent.py --check
python3 -O experimental/scripts/verify_four_row_exact_completion_compiler_v1_independent.py --check
```

The fixed-line correction's full standalone Python command is currently a
known provenance failure after source promotion.  This packet instead binds
the live v13.2 dimension--degree theorem and separately replays the correction's
core census/Sage witness.  A future compatibility PR should repin that older
packet without changing its mathematics.

The semantic mutation suite rejects, among other failures:

- a closed claim with null atoms or unresolved cells;
- a legacy #995 charge transplanted without an architecture mapping;
- a lower floor, target, average, or allocation relabeled as an upper bound;
- an MCA/list or KB/M31 row swap;
- ambient normalization without a full-image certificate;
- a Q component whose typed row, partition, payload, or exact upper drifts;
- a separately generated residual or partition digest;
- duplicate owner assignments or first-match chronology drift;
- a noncanonical `/./` alias, symlink, hidden path, unused source, or an
  unrelated file relabeled as a typed atom/mapping adapter;
- a schema-extra field, non-string owner, Unicode digit, or oversized decimal;
- the superseded extension multiplier interpretation;
- a scalar route cut relabeled as a deployed counterexample; and
- exact charge or budget drift by one.

## 8. Nonclaims and maximal continuation

- No deployed adjacent safe row is proved.
- No `U_Q`, balanced-core, list-interior, or complete extension value is
  invented.
- The one-shell M31 theorem is not promoted to multishell coverage.
- #995 remains a local exact result and route cut; it is not discarded.
- The candidate schema and typed adapters check internal identity, declared
  scope, composition, and arithmetic.  They do not establish the truth or
  exhaustiveness of a candidate-authored theorem/owner universe.  The command
  never certifies closure; independent proof review and an explicit trusted
  source-registry update remain mandatory.

The maximal continuation is a row-uniform theorem packet that simultaneously
supplies the Grande Finale v3 partition mapping, exact Q contract, exhaustive
interior terminals, extension subcells, and add-back.  A packet that instead
finds a compatible primitive component must terminate explicitly as
`UNPAID_PRIMITIVE`; it must not be forced into a named owner.
