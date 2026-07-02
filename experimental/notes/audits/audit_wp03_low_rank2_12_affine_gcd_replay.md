# WP-0.3 Independent Replay: M3 Low-Rank2-12 v10 Affine GCD Packet

- **Status:** AUDIT (independent replay, complete: 462/462 rows match).
- **Agent/model:** Claude Fable 5 acting for latifkasuli.
- **Scope:** external independent replay of
  `experimental/data/certificates/hankel-f17-32-m3-low-rank2-12-v10-affine-gcd/`
  as requested by the post-v10 triage note ("do not treat the checked-in JSON
  as independently replayed") and standing order 12 ("replay before build"),
  which gate fronts alpha and beta on this packet.

Replay target pinned at upstream commit
`01add412c2e3d3876facbf435399b46176c4d65c` (packet file sha256
`9bfef6ad9180a8c11f11a5b12dd57abc059383830c92f1123a6ca731ee2a178e`).
Commit `718df24` later bumped the packet's prose/reference strings
("v10" -> "v12" in the argument text; source artifact ref
`cs25_cap_v10.tex` -> `cs25_cap_v12.tex`), changing the file sha256 to
`87b426...`; the diff touches no data row — all 462 records and their
recorded values are byte-identical to the replayed pin, so this replay
covers the current packet's data verbatim.

## Result

**462/462 rows match on every compared field; zero divergences.**
Per-row: prefix and shift-1 minor degrees equal the rank for all 924 minors,
both sha256 coefficient-vector hashes match, gcd degree `0` everywhere
(aggregate `{0: 462}`), `j`/`t`/row-set metadata and v10 zero-consistency
match. Wall time 1158.9 s on a pure-Python second stack, plus a 133.5 s
direct full-pencil verification of the spectral-reduction lemma itself
(`A=426, r=2, z=5`, both shifts PASS) — a check the packet's own verifier
never runs.

Replayer and frozen full results live in the external repository
(`github.com/latifkasuli/mca`, commit `e3a0dd7`):
`scripts/wp03_affine_gcd_replay.py`, `runs/wp03_affine_gcd_replay_full.json`,
`docs/wp03-affine-gcd-replay-note.md`. No upstream code was imported; only
two DATA conventions (base-17 element encoding, deterministic record hashing)
were mirrored from packet declarations to make recorded values comparable.

## Relation To The PR #231 Replay Harness

The open PR #231 replication (Claude-Code-for-LegaSage) runs the repository's
own verifier scripts across the full corpus on a fresh host — valuable
harness-level replication, but by design it exercises the packet's OWN
verifier code. This note is the complementary object standing order 12 asks
for: the packet's recorded DATA re-derived from the spectral-reduction note
alone and recomputed by a disjoint evaluation route on an external stack,
with no upstream code imported. The two audits together cover both failure
modes (broken scripts; wrong recorded mathematics).

## What Was Re-Derived

Everything was rebuilt from the derivation note
`experimental/notes/m3/m3_low_rank_affine_spectral_reduction.md` and the row
descriptor DATA (not from `verify_f17_32_m3_low_rank2_12_v10_affine_gcd.py`):

- Field: `F_17^32 = F_17[T]/(f)`, `f` the descriptor's declared monic
  degree-32 modulus, used verbatim.  Irreducibility re-verified by our own
  Rabin test (our tooling's default modulus pick would differ; we use theirs,
  recorded).
- Domain: `H = <g>` rebuilt as consecutive powers `g^0..g^511` from
  `generator_encoding`; exact order 512 verified (`g^512 = 1`, `g^256 != 1`);
  all 512 base-17 encodings match the descriptor's `domain_encodings`
  elementwise; recomputed `domain_hash` (sha256 of compact sorted JSON of the
  encoding list) equals the packet's
  `35904a892e0319b3805e91438ec2733427a351a72ce9654428d6a33bd3575b92`.
- Window objects, per agreement `A in [385, 426]`:
  `m = 513 - A in [87, 128]`, `j = m - 1`, `t = A - 256`, base window
  `X = (g^0..g^(m-1))`, update window `Y = (g^m..g^(m+r-1))`, `r = 2..12`.
- Displayed maximal minors: the prefix (`h=0`) and row-shift-1 (`h=1`)
  contiguous minors of the shifted Hankel moment pencil, reduced by the
  note's contiguous-shift lemma to

  ```text
  det(H_X^(h) + Z H_Y^(h)) = det(V_X)^2 (prod_i x_i^h) det(I_r + Z K_h),
  K_h[a,b] = y_a^h sum_i x_i^(-h) L_i(y_a) L_i(y_b).
  ```

- Recorded row values: low-to-high coefficient vectors of the two SCALED
  minors, hashed as sha256 of the base-17-encoded coefficient lists; the
  claims `deg = r` (both minors) and `deg gcd = 0` per row; the v10 bridge
  (canonical affine rank-drop gcd divides the gcd of any two nonzero maximal
  minors) then gives the empty finite affine root set.

## How The Evaluation Route Differs

The packet's verifier computes `det(I + Z K_h)` by Newton-identity trace
recursions over kernels built from incremental Lagrange denominators.  The
replay uses a genuinely distinct route at every stage:

1. **Kernel entries from the closed q-Cauchy factorization**
   `L = diag(rho_a) C diag(gamma_i)` with
   `P_s = prod_(t=1..s)(1 - alpha^t)`, `rho_a = P_(m+a)/P_a`,
   `gamma_i = (-1)^(m-1-i) alpha^((m-1-i)(m-i)/2)/(P_i P_(m-1-i))`,
   `C[a,i] = 1/(1 - alpha^(m+a-i))` — the note's closed form, so the replay
   also exercises that section of the note.  Each row spot-checks four
   sampled entries against the definitional Lagrange product
   `prod_(l != i)(y_a - x_l)/(x_i - x_l)`.
2. **Determinant interpolation, not Newton identities:** `det(I + z K_h)` is
   evaluated at the `r+1` prime-subfield points `z = 0..r` by division-free
   Gaussian elimination and interpolated back to coefficients.
   (Characteristic-17 caveat that motivates upstream's own rank-17 switch is
   moot here: no division by integer factorials at all.)
3. **Scales:** `det(V_X)^2` as a direct pairwise double product (upstream:
   incremental across `A`); `prod X = alpha^(m(m-1)/2)` and
   `x_i^(-1) = alpha^(512-i)` by subgroup order, avoiding field inversions.
4. **GCD:** local monic Euclid over the external field stack.
5. **Lemma-level cross-check (upstream never runs this):** on the smallest
   row the FULL `m x m` moment pencil determinant `det(H_X^(h) + z H_Y^(h))`
   is computed directly from power sums at a sample `z` and compared against
   `scale * det(I_r + z K_h)` for `h = 0, 1` — verifying the spectral
   reduction itself on real data, not just the kernel-side arithmetic.
   Result (A=426, r=2, z=5): PASS for both shifts.

Only two conventions were mirrored from packet DATA declarations (not code):
the descriptor's `base-p low-to-high integer` element encoding and the
deterministic `sha256(json.dumps(..., sort_keys=True, separators=(",",":")))`
record hashing — both needed to compare recorded values at all.

## Validation Slice (complete)

- Packet integrity: `deterministic_record_hash` recomputed over the 462
  records — matches.
- Rows replayed so far: all 11 ranks at `A = 385` (largest window, m=128)
  and all 11 ranks at `A = 426` (smallest window, m=87): **22/22 rows match
  on every compared field** — prefix/shifted minor degrees, both coefficient
  hashes, gcd degree 0, `j`/`t`/row-set metadata, and v10 zero-consistency.
- Full-pencil lemma check: PASS (h=0 and h=1).

## Per-Row Agreement Table (to fill after full run)

Full 462-row results land in the external repo at
`runs/wp03-affine-gcd-replay/replay-full.json` (schema
`wp03-affine-gcd-replay-v1`; per-row `replay` vs `packet` values plus a
`match` breakdown), produced by:

```sh
PYTHONPATH=src PYTHONUNBUFFERED=1 nohup python3 scripts/wp03_affine_gcd_replay.py \
  --resume --lemma-check \
  --json-out runs/wp03-affine-gcd-replay/replay-full.json \
  >> runs/wp03-affine-gcd-replay/replay-full.log 2>&1 &
```

- [x] rows checked: **462 / 462**
- [x] rows matching on all fields: **462 / 462**
- [x] mismatches: **0** (`mismatch_row_ids: []`)
- [x] minor degree histogram (both minors, 924 total): rank `r` appears
      exactly `84 = 42 agreements x 2 minors` times for each `r in 2..12`;
      `deg = rank` holds for all 924 minors, as the packet claims.
- [x] gcd degree histogram: `{0: 462}` — matches the packet aggregate.
- [x] wall time: 1158.9 s (~19.3 min), plus the 133.5 s full-pencil lemma
      check (A=426, r=2, z=5: PASS at both shifts).

## Claim (confirmed)

The table closed clean: the low-rank2-12 v10 affine-gcd packet is
INDEPENDENTLY REPLAYED in the sense of the post-v10 triage note — every
recorded minor coefficient vector, degree, and coprimality claim is
reproduced from the derivation note alone, by a disjoint evaluation route,
on a disjoint field/polynomial stack, including a direct verification of the
spectral-reduction lemma the packet relies on.  Fronts alpha and beta are
then unblocked with respect to standing order 12 ("replay before build") for
this packet.

## Non-Claims

- Replay of the synthetic low-rank ladder only, ranks 2..12; not an
  arbitrary-row M3 statement and not the `r > 12` spectral target.
- No claim about the projective endpoint packet.
- The v10 divisibility bridge (canonical gcd divides any two-minor gcd) is
  taken from Paper D v10 as stated; this replay checks the two-minor
  computation and the reduction lemma, not the v10 paper proof.
