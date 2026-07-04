# B1: the characteristic-zero giant-coset theorem

- **DAG node:** `b1_char0_giant_coset_theorem` (PROVED, key). This note is
  the standalone packet the node lacked (its proof previously lived only in
  the node's `statement` field).
- **Status:** PROVED (Galois-orbit / valuation argument, elementary and
  self-contained) + toy-verified.
- **Verifier:** `experimental/scripts/verify_b1_giant_coset.py`
  (10/10 PASS: exact cyclotomic arithmetic; full brute at `(16,4)`; exact
  rational-nullspace both-directions proofs at `(16,4)`, `(32,4)`, `(32,8)`;
  pinned certificate).
- **Consumers:** `b2_modp_giant_extras` (the mod-p residue at prize-max —
  see the Frobenius gap, Remark 1), `u2c_boundary_scale_column` (the
  `M = t` boundary column that this theorem's `M > t` fence excludes).
- **Provenance:** `u2c_giant_block_statement.md`;
  `u2_large_characteristic_lift` (the uniform-in-`b`, large-`p` companion).

## Critical-path role

This packet closes the characteristic-zero giant-block branch of the
conditional prize proof path. It proves that, in the dyadic cyclotomic
model, every 0/1 block with vanishing first `t` power sums is already a
paid coset union. The only remaining giant-block work is therefore the
finite-field Frobenius residue, handled by the separate `b2_modp_giant_extras`
and boundary-column packets.

## Theorem

> **B1 (char-0 giant coset).** Let `n = 2^s` and let `zeta = zeta_n` be a
> primitive `n`-th root of unity over a field of characteristic zero. Let
> `B subset mu_n` be a subset whose power sums vanish through order `t`:
>
> ```text
>     p_r(B) := sum_{b in B} b^r = 0      for r = 1, 2, ..., t.
> ```
>
> Then `B` is a union of cosets of `mu_M`, where `M` is the **least
> 2-power strictly greater than `t`**, `M = 2^{floor(log2 t) + 1}`.

(In characteristic zero the power-sum nullity `p_1 = ... = p_t = 0` is
equivalent, by Newton's identities, to the elementary-symmetric nullity
`e_1 = ... = e_t = 0` used in `u2c_giant_block_statement.md`; the two are
interchangeable here.)

## Proof

Identify `mu_n` with `Z/n` via `zeta^j <-> j`, and encode `B` by its
**exponent polynomial**

```text
    f_B(X) = sum_{j : zeta^j in B} X^j    in    Z[X].
```

Its coefficients are the 0/1 indicator of `B`, so `f_B in Z[X]` — this
integrality is the entire engine. The Fourier coefficient (frequency `r`)
of `B` is `f_B(zeta^r)`, and

```text
    p_r(B) = sum_{j in B} (zeta^r)^j = f_B(zeta^r).
```

**Step 1 (Galois propagation).** Fix `r in {1, ..., t}` with `p_r(B) = 0`,
i.e. `f_B(zeta^r) = 0`. Because `f_B` has **rational** coefficients, every
Galois automorphism `sigma in Gal(Q(zeta_n)/Q) = (Z/n)^*` fixes `f_B` and
sends `zeta^r` to another root:

```text
    0 = sigma(f_B(zeta^r)) = f_B(sigma(zeta^r)) = f_B(zeta^{u r}),
    u in (Z/n)^* arbitrary.
```

So `f_B` vanishes at the **entire Galois orbit** of `zeta^r`. For
`n = 2^s`, the orbit of `zeta^r` is `{ zeta^{r'} : v_2(r') = v_2(r) }` —
all frequencies of the same 2-adic valuation. (Reason: `zeta^r` is a
primitive `n/gcd(n,r)`-th root of unity; `gcd(2^s, r) = 2^{v_2(r)}`, and
the conjugates of a primitive `2^m`-th root are exactly all primitive
`2^m`-th roots, i.e. all `zeta^{r'}` with `2^{v_2(r')} = 2^{v_2(r)}`.)

**Step 2 (which valuations are forced).** As `r` runs over `{1, ..., t}`
it realises every 2-adic valuation `v` with `2^v <= t`, namely `v = 0`
(take `r = 1`), `v = 1` (`r = 2`), ..., up to `v = floor(log2 t)`
(`r = 2^{floor(log2 t)} <= t`). Combining Steps 1-2:

```text
    f_B(zeta^{r'}) = 0     for every r' with  v_2(r') <= floor(log2 t),
                           i.e. for every r' NOT divisible by M,
    where M = 2^{floor(log2 t)+1} = least 2-power > t.
```

Equivalently the spectrum of `B` is supported on `M*Z` (the frequency `0`
mean plus the multiples of `M`): `hat{B}(r') = 0` unless `M | r'`.

**Step 3 (spectrum in `M*Z` => coset union).** A function on `Z/n` whose
Fourier support lies in `M*Z` is invariant under translation by the dual
subgroup: for `r' = M*l`, the character `j -> zeta^{j M l}` has period
`n/M` in `j`, so the inverse transform gives `1_B(j) = 1_B(j + n/M)` for
all `j`. Thus `B` is invariant under adding `n/M`, i.e. under multiplication
by `zeta^{n/M}` — the generator of `mu_M`. A `mu_M`-invariant, `{0,1}`-valued
indicator is **constant on each `mu_M`-coset** (all-`0` or all-`1`), hence
`B` is a union of full `mu_M`-cosets. ∎

**Count.** There are `n/M` cosets, so exactly `2^{n/M} = sum_{j} C(n/M, j)`
subsets are `t`-null — every one a coset union.

## Remarks

**1. The Frobenius gap (why there is no mod-`p` analogue).** The proof
consumes exactly one thing: `f_B` has integer coefficients and Galois acts
on the frequencies `zeta^r` through `(Z/n)^*`. Over a finite field `F_q`
with `q = 1 mod n` (forced by the tame `n | q-1` domain), the Frobenius
`x -> x^q` fixes every `n`-th root of unity — it acts **trivially** on
frequencies. So the mod-`p` world has no Galois orbit to propagate the
single vanishing `f_B(zeta^r) = 0` across valuations, and genuine
non-coset `t`-null blocks **can** exist. This char-0/finite-field gap is
fundamental, not technical; it is precisely what `b2_modp_giant_extras`
must bound (with its 123-bit first-moment cushion). The verifier makes the
point concretely: the 0/1-ness is load-bearing — the signed antipodal word
`zeta^1 + zeta^9 = 0` in `mu_16` is a `t`-null relation that is **not** a
coset union, available only once `{0,1}` is relaxed to `{-1,0,1}` (the
finite-field escape hatch's shape).

**2. The X-8 boundary blocks are finite-field-only extras.** The
boundary-scale zero-sum quotient blocks (the `M = t` construction that
refuted `u2c_giant_block_dichotomy`; `qa25_boundary_scale_column.md`) live
**outside** this theorem's `M > t` fence and are finite-field objects
consistent with Remark 1: char 0 forces `M > t` strictly, so no boundary
block exists there; over `F_q` they appear and are charged separately by
`u2c_boundary_scale_column`.

**3. Comparison to X24.** X24 (`x24_char0_dyadic_descent.md`) classifies
char-0 **signed small-`h` trades** (disjoint `h`-subsets with equal first
`h-1` power sums): none for non-2-power `h`, full `mu_h`-fibers for 2-power
`h`. B1 is the **0/1 giant** analogue and is strictly easier — a 0/1
indicator with integer exponent polynomial hands the Galois argument its
integrality for free, whereas X24's signed words need the antipodal
descent. Both are the same 2-adic-valuation phenomenon read at opposite
ends of the `h`-scale (small signed `h` vs giant 0/1 blocks).

## Verification (toy censuses)

```bash
python3 experimental/scripts/verify_b1_giant_coset.py
```

Exact cyclotomic arithmetic in `Z[zeta_n] = Z[X]/(X^{n/2}+1)` — the
`t`-nullity test is exact integer equality (zero tolerance; no floating
point). Three cases, each verified two independent ways:

- **`(n,t) = (16,4)`, `M = 8`.** Full `2^16` brute force returns **exactly
  4** `t`-null 0/1 vectors — the empty set, the two `mu_8`-cosets (even and
  odd exponents), and their union `mu_16` — i.e. "the two `mu_8`-cosets and
  their union" as the DAG statement predicts. Cross-checked by the exact
  rational-nullspace computation: nullity `= n/M = 2`.
- **`(n,t) = (32,4)`, `M = 8`, `n/M = 4`.** Forward: all `2^4 = 16`
  `mu_8`-coset unions are `t`-null, and `16 = sum_j C(4,j)` exactly. Reverse
  (both directions, no `2^32` brute): the exact rational constraint matrix
  has nullity `= 4 = n/M`, and the 4 coset indicators lie in — hence span —
  the nullspace, so the rational solution space **equals** the
  `mu_8`-invariant subspace; every `t`-null 0/1 vector is therefore a coset
  union. (This linear-algebra route reproduces the Galois propagation
  computationally, standing in for the `2^32` brute that is out of budget.)
- **`(n,t) = (32,8)`, `M = 16`, `n/M = 2`.** `2^2 = 4` `mu_16`-coset
  unions, all `t`-null, `4 = sum_j C(2,j)`; exact nullity `= 2`.
- The pinned certificate
  `experimental/data/certificates/b1-giant-coset/b1_giant_coset.json` matches
  the checked cases and the signed-antipodal sanity witness.

Current run **10/10 PASS**.
