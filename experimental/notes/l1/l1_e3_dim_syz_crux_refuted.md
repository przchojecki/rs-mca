# L1: the `dim Syz <= K` crux is already decided — the `E_3 <= ell-2` route-cut transports

**Type: ROUTE-CUT / RECONCILIATION of two co-integrated lineages.** The
2026-07-06 integration (0fa9427) banked, side by side: (a) the L1 E3
proof-program package (notes `experimental/notes/l1/l1_e3_status_and_paper_connection.md`,
`l1_e3_subspace_upper_bound.md`, `experimental/notes/roadmaps/l1_e3_next_steps_and_tools.md`,
obligations `experimental/l1_e3_obligation_v2.md`, Lean skeleton
`experimental/lean/l1_e3_level_set/`), whose named crux — **`dim Syz <= K`
for `K >= 3`, equivalent by its own proved reduction to
`E_3 <= ell - 2`** — is labeled OPEN throughout; and (b) the integrated
counterexample note `experimental/notes/l1/l1_prime_ell_key_lemma_refuted.md`,
which refutes `E_3 <= ell - 2` outright with explicit witnesses at
`ell in {11, 13, 17, 19, 23}`. This note reconciles the record: **the crux
is not open — it is decided (false), by witnesses already on main**, and
the proof-program's own equivalence is exactly what transports the
refutation. The same-day consolidated agents-log names "the L1
`dim Syz<=K` theorem for `K>=3`" as next proof work; the corrected
sharpest live target is stated in §6.

**Ground rule honored:** no integrated note, obligation file, Lean package,
or verifier is edited; everything the proof-program labels PROVED survives
and is re-verified here on the deciding witnesses (§5). Filed at
`experimental/notes/l1/l1_e3_dim_syz_crux_refuted.md`. Companion zero-arg
verifier: `experimental/scripts/verify_l1_e3_dim_syz_crux.py` (stdlib,
offline, deterministic, exit 0 iff all gates pass; `--tamper-selftest`).

Notation: as in the integrated L1 notes (`ell` odd prime, `ell | p - 1`,
`Gamma` constant-free mixed of degree `<= ell - 1`, spectrum = per-coset-MAX
fibers, `E_3 = sum (mu - 2)_+`); the proof-program's `Syz` = the
degree-bounded co-fiber syzygy module of the level sets (its files'
definition, quoted in §1); the sigma-calculus objects (`sigma`, `V_k`,
`dimU`, master identity) as in `experimental/notes/l1/l1_sigma_calculus.md`.

**Status legend:** ROUTE-CUT (a named open target is decided by existing
integrated material) / PROVED-LOCAL / AUDIT / SURVIVES.

---

## 0. Headline

1. **ROUTE-CUT — `dim Syz <= K` is false for `K >= 3`, on thirteen
   co-integrated witnesses.** Building the proof-program's `Syz` module
   verbatim on the 7 witnesses of the integrated key-lemma refutation and
   the 6 witnesses of the integrated `E_3 <= ell` refutation
   (`experimental/data/certificates/l1-e3-law/l1_e3_law_refutation.json`),
   every hypothesis of the crux met (`K_3 = #{mu_k >= 3} >= 3`,
   realizable, in-scope): **`dim Syz > K` on all thirteen**, with margin
   `dim Syz - K = E_3 - (ell - 2)` exactly, ranging `+1` to `+4`.
   Headline: `ell = 23, p = 139`, spectrum `[13, 10, 4, 3, 3, 2]`,
   `E_3 = 23 = ell`, `K = 5`, **`dim Syz = 7 = K + 2`**. Two integrated
   saturator controls at `E_3 = ell - 2` return `dim Syz = K` exactly —
   the computation reproduces the bound precisely where it holds.

2. **AUDIT — why this was already decided on paper.** The proof-program
   itself PROVES the equivalence `dim Syz <= K <=> E_3 <= ell - 2` (its
   obligation file, quoted §1), and `E_3 <= ell - 2` is refuted by the
   co-integrated counterexample note. The contrapositive of its own proved
   upper half gives `E_3 >= ell - 1 ==> dim Syz >= K + 1`; the exact
   margin identity is `dim Syz - K = E_3 - dim(sum V_k)` with
   `dim(sum V_k) <= ell - 2`. The sigma-calculus note §2.1 already tables
   the corresponding slice as REFUTED. The two lineages entered main
   without a cross-reference; this note supplies it.

3. **AUDIT — translation dictionary (proved by computation, all 15
   objects).** The proof-program's `dim Syz` IS the sigma-calculus `sigma`
   (same degree-bounded co-fiber syzygy module), up to index convention:
   the proof-program sums over excess cosets (`mu_k >= 3`, count `K_3`),
   the sigma-calculus over all multi-fibers (`mu_k >= 2`, count `K_2`).
   Both conventions obey `dim Syz - K = E_3 - dim(sum V_k)`; **no
   convention choice rescues the inequality.** Master identity
   (`sigma = E_3 + K_2 - ell + dimU`, verified with `dimU = 2` on all
   thirteen witnesses) exhibits the crux as its `dim(sum V_k) = ell - 2`
   slice.

4. **The corrected target (§6):** the ladder `dim Syz <= K`
   (`<=> E_3 <= ell - 2`) is dead; `<= K + 1` (`<=> E_3 <= ell - 1`) is
   dead at `ell = 23`; `<= K + 2` (`<=> E_3 <= ell`) is PROVED on the
   covered chart `T <= 4` (sigma-calculus Theorem 1) and REFUTED on the
   residual chart `T >= 5` (integrated witnesses at `E_3 = ell + 1` and
   `ell + 2`). The sharpest live statement is bounded excess:
   `dim Syz <= K + C` (`<=> E_3 <= ell + C - 2`)... with `C >= 4` forced
   by the `E_3 = ell + 2` witness — equivalently `E_3 <= ell + C'` with
   `C' >= 2` — on the residual chart, where the open core is the tight
   `(W, lambda)`-Veronese transversality of `>= 3` big fibers. Downstream
   consumers need only some `E_3 <= ell + O(1)`.

---

## 1. The crux as integrated (verbatim)

From `experimental/notes/l1/l1_e3_status_and_paper_connection.md`:

> "**Status:** PROVED (upper half) + REDUCTION + banked route-eliminations.
> The headline `E_3 <= ell-2` is OPEN — and confirmed to be the same
> finite max-fiber problem CAP25 v13 leaves open."

From `experimental/notes/roadmaps/l1_e3_next_steps_and_tools.md`: the title
announces "the confirmed-open status", and the roadmap ranks proof routes
for the crux. From `experimental/l1_e3_obligation_v2.md`: the reduction chain

> `E_3 <= ell - 2  <=>  dim(sum V_k) >= E_3  <=>  dim Syz <= K`

(rendered here in ASCII; the source states this three-way equivalence with
proof) (the direction used here is the proved upper half
plus the dimension count; the verifier recomputes both sides on every
witness rather than trusting either).

From `experimental/notes/l1/l1_prime_ell_key_lemma_refuted.md` (integrated
2026-07-06, commit d254f80 — before the proof-program's fork point):

> "**STATUS: COUNTEREXAMPLE.** `E_3 <= ell-2` refuted at
> `ell in {11,13,17,19,23}`"

## 2. The transport

For a realizable configuration with spectrum `{mu_k}`, the proof-program's
module satisfies (its own §, re-derived and verified here)

```text
dim Syz = E_3 + K - dim(sum V_k),      dim(sum V_k) <= ell - 2,
==>  dim Syz - K = E_3 - dim(sum V_k) >= E_3 - (ell - 2).
```

So any integrated witness with `E_3 >= ell - 1` forces `dim Syz >= K + 1`
— the crux fails with margin exactly `E_3 - (ell - 2)` whenever
`dim(sum V_k)` attains `ell - 2` (it does on all thirteen witnesses;
gate ii checks the attainment rather than assuming it).

## 3. The thirteen witnesses (computed table)

| source | ell | p | spectrum | E_3 | K_3 | dim Syz | margin |
|---|---|---|---|---|---|---|---|
| key-lemma note §1 | 11 | 199 | `[7,4,3,3,3]` | 10 | 5 | 6 | +1 |
| key-lemma note §1 | 13 | 313 | `[8,5,3,3,3,2,2,2,2,2]` | 12 | 5 | 6 | +1 |
| key-lemma note §1 | 13 | 79 | `[6,6,6,2,2]` | 12 | 3 | 4 | +1 |
| key-lemma note §1 | 17 | 103 | `[10,7,3,3,3,2]` | 16 | 5 | 6 | +1 |
| key-lemma note §1 | 19 | 191 | `[11,8,4,3,2,2]` | 18 | 4 | 5 | +1 |
| key-lemma note §1 | 23 | 139 | `[13,10,4,3,3,2]` | 23 | 5 | 7 | **+2** |
| key-lemma note §1 | 11 | 67 | `[8,3,3,3,3,2]` | 10 | 5 | 6 | +1 |
| e3-law W1 | 29 | 233 | `[15,14,4,3,3,3,2,2]` | 30 | 6 | 9 | +3 |
| e3-law W2 | 23 | 139 | `[14,9,4,4,3,2]` | 24 | 5 | 8 | +3 |
| e3-law W3 | 17 | 137 | `[14,3,3,3,3,3,3,3]` | 19 | 8 | 12 | **+4** |
| e3-law EXTRA1 | 29 | 233 | `[20,9,4,3,3,3,2,2]` | 30 | 6 | 9 | +3 |
| e3-law EXTRA2 | 29 | 233 | `[16,13,4,3,3,3,2,2]` | 30 | 6 | 9 | +3 |
| e3-law EXTRA3 | 17 | 103 | `[11,5,5,4,3,2]` | 18 | 5 | 8 | +3 |

(`K_2`, `dim(sum V_k)` attainment, and `dimU` are in the certificate JSON;
the verifier recomputes every cell from the raw integrated `gamma` vectors.
Controls: two integrated `E_3 = ell - 2` saturators — `ell=11,p=331` and
`ell=23,p=139` (D3), both from `l1_sigma_calculus.md`'s own witness set —
return `dim Syz = K` exactly (`4=4`, `6=6`), margin 0.)

## 4. What SURVIVES of the proof-program packet

Everything it labels PROVED, re-verified here on the deciding witnesses:
the upper half `dim(sum V_k) <= ell - 2`; the reduction
`dim Syz <= K <=> E_3 <= ell - 2` itself (it is what transports the
refutation — a correct and useful theorem); the `K = 2` case; the banked
route-eliminations (their targets were the `ell - 2` statement — the
eliminations stand as eliminations); the Lean skeleton as a formalization
scaffold (its main theorem carries an annotated `sorry` and now has a
definite truth value: false as stated — the skeleton remains reusable for
the corrected target of §6). The cyclotomic/directions literature bridge
is untouched by this note.

## 5. Non-claims

This note refutes exactly one inequality (`dim Syz <= K`, `K >= 3`, and
its `<= K + 1` strengthening via the `ell = 23` witness); it does not
touch the proof-program's proved content, does not edit any integrated
file, does not resolve the residual-chart open core, does not conjecture a
value of the bounded-excess constant, and promotes nothing — ROUTE-CUT /
AUDIT / SURVIVES scope only, `experimental/` placement.

## 6. Corrected sharpest live target

```text
covered chart (T <= 4):  E_3 <= ell  PROVED  (sigma-calculus Theorem 1)
residual chart (T >= 5): E_3 <= ell + C',  C' >= 2 forced (E_3 = ell + 2
                          attained);  open in both directions:
                          uniform C'?  growth with ell or n?
equivalently:            dim Syz <= K + C on the residual chart
open core:               tight (W, lambda)-Veronese transversality of
                          >= 3 big fibers (all local routes dead — see the
                          integrated sigma-calculus and e3-law notes)
downstream requirement:  any E_3 <= ell + O(1) suffices for the L1
                          residual-lane consumers (poly count control)
```

## 7. Verifier contract

`experimental/scripts/verify_l1_e3_dim_syz_crux.py`, zero-arg, stdlib,
offline, deterministic, exit 0 iff all gates pass:

- **Gate i:** for each of the 13 witnesses (raw `gamma` embedded from the
  integrated sources), recompute the spectrum fresh and build `Syz` in the
  proof-program's convention: check `dim Syz`, `K_3`, and
  `margin = E_3 - (ell - 2)` exactly; plus the two `E_3 = ell - 2`
  saturator controls at margin 0.
- **Gate ii:** the transport identity per witness:
  `dim Syz - K = E_3 - dim(sum V_k)` with `dim(sum V_k) = ell - 2`
  attained (recomputed, not assumed).
- **Gate iii:** the convention dictionary: recompute `sigma` (K_2
  convention) and check `sigma = E_3 + K_2 - ell + dimU` (master
  identity) with `dimU` recomputed; check the `K_3`/`K_2` translation on
  every witness.
- **Gate iv:** in-scope checks per witness (odd prime, `ell | p - 1`,
  constant-free mixed `Gamma`, realizability by construction,
  `K_3 >= 3`).
- `--tamper-selftest`: flip one datum per gate; each gate must then fail.

Runtime target < 30 s. Companion certificate:
`experimental/data/certificates/l1-e3-law/l1_dim_syz_crux_table.json`.

## Refs

- `experimental/l1_e3_obligation_v2.md` + `experimental/notes/l1/l1_e3_status_and_paper_connection.md`
  (the crux and the proved reduction).
- `experimental/notes/l1/l1_prime_ell_key_lemma_refuted.md` (the
  transported refutation; witnesses).
- `experimental/notes/l1/l1_e3_law_refuted.md` +
  `experimental/data/certificates/l1-e3-law/l1_e3_law_refutation.json`
  (the `T >= 5` witnesses; the residual-chart open core).
- `experimental/notes/l1/l1_sigma_calculus.md` (sigma, master identity,
  Theorem 1; its §2.1 table).
