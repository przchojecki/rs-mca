# b=0 complete-fiber audit + CircleCode.lean formalization (circle twin-coset chain)

**Base:** `c35a6da31ed0905afcbaaefe4eb0f242572ebb35` (origin/main).
**Status: AUDIT + Lean formalization (proof status conservative).**  The Lean
statements listed in
`experimental/lean/cs25_cap_v12/CIRCLE_FIBER_CORRESPONDENCE.md` are proved with
zero `sorry` on the package's pinned toolchain (`leanprover/lean4:v4.28.0`,
mathlib tag `v4.28.0`); everything they do NOT cover (see NON-CLAIMS) keeps its
prior status.  **No `.tex`/`.pdf` edited.**

**Object.** The complete-fiber ("b = 0") chain behind the circle rows:
twin-coset preamble + `lem:torus-fibers` (`tex/cs25_cap_v12.tex:3908/:3910`),
`lem:cheb-fibers` (`:3923`), `rem:standard-position` (`:3953`), and the
submission draft's compressed rebuild `def:circle-twin-domain`
(`experimental/rs_mca_thresholds.tex:2791`) + `lem:cheb-smooth` (`:2873`), as
consumed by `thm:fixed-length-prime-density`(c) (`:3009`) and
`cor:circle-32-family` (`:3047`), and cited (as `H5`) by the pay-per-bit ledger
rows for `cor:circle-deployed(a)/(b)`.

## (a) Complete fibers at every dyadic scale, including the b=0 boundary

`lem:cheb-fibers`' load-bearing content is that on a twin-coset `x`-domain the
Chebyshev folding maps have **complete** fibers of size exactly `a` at every
scale `a ∣ M` with `g^{2a} ∉ H^{(a)}` — no ramified/fixed endpoints, i.e. the
exceptional-endpoint count is `b = 0` (a twin coset contains no self-inverse
element).  This is now machine-checked in
`experimental/lean/cs25_cap_v12/cs25_cap_v12/CircleCode.lean`:

- no self-inverse element: `RSCap.twinCoset_no_self_inverse`;
- exact fiber counts at every admissible scale (`(T_a, a)`-smooth `x`-domain,
  `(X^a, a)`-smooth torus domain): `RSCap.lem_cheb_fibers`,
  `RSCap.lem_torus_fibers`, with the `2a`-point solution-set count
  `RSCap.twin_coset_pow_pair_card` / `RSCap.htwin_of_twin_coset`;
- all scales simultaneously ⟺ `ord(g) ∤ 2M`: `RSCap.twin_coset_all_scales_iff`
  (the boundary scale `a = M` is exactly the `⟸` pivot of that proof).

**Tie to the live watch-item fuse (#690 rung ledger).**
`experimental/notes/audits/envelope_rung_ledger.md` records the only sub-bit
rung: `m31_mca Gceil c=2048: M=12,769,758 vs B*=16,777,215 (-0.3938 b, TIGHT)`,
with the explicit sensitivity block: *"the −0.3938 watch-item rung would fire
under any multiplier `>= 2^0.3938` — even the crude `b = 1` factor flips it"*,
and `b = 0` there is *"cited to `lem:cheb-fibers`/`rem:standard-position`
rather than assumed"*.  This packet upgrades the citation target: the
no-self-inverse and complete-fiber facts behind `b = 0` are now Lean-proved for
enumerated twin cosets (generic finite field), not only printed.  The ledger
itself, its integer gates, and its NON-CLAIMS are untouched; the watch-item
remains live and TIGHT.

## (b) Crosswalk v12 ↔ thresholds draft, with the two compression gaps

Same mathematical object, three presentations; hypotheses are identical
(`a ∣ |H|`, `g^{2a} ∉ H^{(a)} = {hᵃ : h ∈ H}`, all-scales ⟺ `ord(g) ∤ 2|H|`):

| v12 (proved in print) | thresholds draft (compressed) | Lean discharge |
| --- | --- | --- |
| preamble `:3908` (no self-inverse; `χ` two-to-one; `\|D\| = M`) | asserted inside `def:circle-twin-domain` `:2791` and `lem:cheb-smooth`'s proof `:2878` | `twinCoset_no_self_inverse`, `chi_eq_chi_iff`, `chi_pair_image_card`, `twin_coset_chi_card` |
| `lem:torus-fibers` `:3910` (kernel, a-to-one, dichotomy, all scales) | first three sentences of `lem:cheb-smooth`'s proof `:2878` | `card_pow_eq_one_of_dvd_card`, `coset_pow_fiber_card`, `coset_pow_fiber_cross_empty`, `twin_coset_image_coincident`, `twin_coset_all_scales_iff` |
| `lem:cheb-fibers` `:3923` with the `E_w` count `:3935`–`:3951` | `lem:cheb-smooth` `:2873` (one-sentence fiber step) | `twin_coset_pow_pair_card`, `htwin_of_twin_coset`, `lem_cheb_fibers` |
| `rem:standard-position` `:3953` | inline in `thm:fixed-length-prime-density`(c) proof (`ord(g)=4n ∤ 2n`) | `standard_position_twin_coset` |

**Gap 1 (two-to-one/no-self-inverse step asserted, not proved).**
`lem:cheb-smooth`'s proof (`experimental/rs_mca_thresholds.tex:2878`) asserts
verbatim: *"Since \(\chi\) is exactly two-to-one on both twin cosets and
identifies only inverse points, the equation \(T_a(x)=y\) on \(D\) has exactly
\(a\) solutions for each \(y\in T_a(D)\)."*  v12 proves this via the
inversion-closed, self-inverse-free `2a`-point set `E_w` (`:3935`–`:3951`); the
draft compresses it to one sentence.  Discharged: `chi_pair_image_card` +
`twin_coset_pow_pair_card` + `lem_cheb_fibers`.

**Gap 2 (cardinality claim baked unproved into a definition).**
`def:circle-twin-domain` (`:2809`–`:2813`) states verbatim: *"a \emph{twin
coset}.  Its projected set \(D(g,H)=\chi(\Dcal(g,H))\subseteq\F_p\) has
cardinality \(\abs H\)"* — inside the definition, with no proof anywhere in the
draft (v12 proves it in the preamble `:3908`).  Discharged:
`twin_coset_chi_card` (`2·|χ(𝒟)| = |𝒟| = 2|H|`).

**Finding 3 (NEW — in-tree Lean skeleton hypothesis was vacuous).**  The prior
`lem_cheb_fibers` skeleton in `CircleCode.lean` assumed the `2a`-count `htwin`
on the same index type that `hdom : Function.Injective dom` forces to enumerate
the `x`-domain.  A `χ`-section meets each inversion pair of the solution set
at most once, so the index-level count is at most `a + 1 < 2a` for `a ≥ 2`
(and exactly `1 < 2` at `a = 1`), never `2a`: `htwin` + `hdom` are jointly
unsatisfiable on a nonempty index type, and the skeleton was provable only
vacuously.  The statement has been repaired to the papers' actual twin-coset
hypotheses and proved; `chebyshev_semiconjugacy` also gained the (necessary)
`(2 : F) ≠ 0` hypothesis, false to omit in characteristic two.  Details in
`CIRCLE_FIBER_CORRESPONDENCE.md`.

## (c) `thm:fixed-length-prime-density`(c) instantiation certified

The draft instantiates the chain with `g ∈ 𝕌` of order `4n`, `H = ⟨g⁴⟩`
(`|H| = n`), twin coset `gH ⊔ g⁻¹H` (`:3038`–`:3044`).  Certified lines:

- `g² ∉ ⟨g⁴⟩`: `g² = g^{4t}` forces `4n ∣ 4t − 2`, impossible mod 4 —
  Lean: `RSCap.standard_position_twin_coset` (second conjunct).
- all-scale criterion: `ord(g) = 4n ∤ 2n` — Lean: third conjunct; combined with
  `RSCap.twin_coset_all_scales_iff` this yields `g^{2a} ∉ H^{(a)}` for every
  `a ∣ n` simultaneously (the draft's "so lem:cheb-smooth proves smoothness at
  every dyadic scale").

The same lemma also gives `gH₀ = gK ⊔ g⁻¹K` with `K = ⟨g⁴⟩`, `|K| = M` — i.e.
v12's `rem:standard-position`; the two papers' instantiations are literally the
same Lean statement.  Numerical spot-check (stdlib-only, first two primes of
the family for `n = 8` and `n = 32`):

```python
#!/usr/bin/env python3
"""Stdlib check: thm:fixed-length-prime-density(c) instantiation
(experimental/rs_mca_thresholds.tex L3009) = rem:standard-position
(tex/cs25_cap_v12.tex L3953).

For p = -1 mod 4n, work in F_{p^2} = F_p[i] (i^2 = -1, valid since p = 3 mod 4).
Norm-one torus U = {u : u^{p+1} = 1} is cyclic of order p+1.  Take g of order
4n, H = <g^4> (|H| = n), twin coset D_cal = gH u g^-1 H, D = chi(D_cal).
Certify: (1) g^2 not in H; (2) ord(g) = 4n does not divide 2n;
(3) g^{2a} not in H^(a) for every dyadic a | n (all scales, incl. boundary a=n);
(4) no self-inverse element in D_cal (endpoint count b = 0);
(5) |chi(D_cal)| = |H| = n (draft def:circle-twin-domain cardinality claim);
(6) T_a is exactly a-to-1 on D at every dyadic scale a | n (complete fibers).
"""


def run(p, n):
    assert p % (4 * n) == 4 * n - 1 and p % 4 == 3

    def mul(x, y):  # F_{p^2} as pairs (a, b) = a + b*i, i^2 = -1
        return ((x[0] * y[0] - x[1] * y[1]) % p, (x[0] * y[1] + x[1] * y[0]) % p)

    def upow(x, e):
        r, b = (1, 0), x
        while e:
            if e & 1:
                r = mul(r, b)
            b = mul(b, b)
            e >>= 1
        return r

    one = (1, 0)
    # find g of order 4n in U (order p+1): take any z with z^{p+1}=1 of full
    # order p+1 is not needed; search elements u = (x+iy) with x^2+y^2=1
    g = None
    for x in range(p):
        y2 = (1 - x * x) % p
        y = next((yy for yy in range(p) if yy * yy % p == y2), None)
        if y is None:
            continue
        u = (x, y)
        if upow(u, 4 * n) == one and all(
            upow(u, (4 * n) // q) != one for q in {2} | set()
        ):
            # order divides 4n and not 2n => order exactly 4n on the 2-part
            if upow(u, 2 * n) != one:
                g = u
                break
    assert g is not None, "no g of order 4n found"
    ginv = upow(g, 4 * n - 1)
    H = {upow(g, 4 * k) for k in range(n)}
    assert len(H) == n
    # (1) g^2 not in H
    assert upow(g, 2) not in H, "(1) FAIL"
    # (2) 4n does not divide 2n
    assert (2 * n) % (4 * n) != 0, "(2) FAIL"
    Dcal = {mul(g, h) for h in H} | {mul(ginv, h) for h in H}
    assert len(Dcal) == 2 * n
    inv2 = pow(2, p - 2, p)

    def chi(u):
        uin = upow(u, p)  # u^{-1} = u^p on the norm-one torus
        assert mul(u, uin) == one
        assert uin[1] == (-u[1]) % p and uin[0] == u[0]
        return (u[0] + uin[0]) * inv2 % p  # = u[0], the x-coordinate

    # (4) no self-inverse element (b = 0)
    for u in Dcal:
        assert upow(u, p) != u, "(4) FAIL: self-inverse element"
    D = {chi(u) for u in Dcal}
    # (5) |chi(Dcal)| = |H|
    assert len(D) == n, "(5) FAIL"
    a = 1
    while a <= n:  # dyadic scales a | n, including the boundary a = n
        # (3) g^{2a} not in H^(a)
        Ha = {upow(h, a) for h in H}
        assert upow(g, 2 * a) not in Ha, f"(3) FAIL at a={a}"
        # (6) T_a exactly a-to-1 on D: T_a(chi(u)) = chi(u^a)
        img = {}
        for u in Dcal:
            img.setdefault(chi(upow(u, a)), set()).add(chi(u))
        # Chebyshev recurrence check of the same fibers
        for w, fib in img.items():
            assert len(fib) == a, f"(6) FAIL at a={a}: fiber {len(fib)} != {a}"
        assert len(img) == n // a
        # independent Chebyshev-polynomial evaluation of T_a on D
        for x in D:
            t0, t1 = 1, x
            for _ in range(a - 1):
                t0, t1 = t1, (2 * x * t1 - t0) % p
            Ta = t1 if a >= 1 else 1
            u = next(v for v in Dcal if chi(v) == x)
            assert Ta % p == chi(upow(u, a)), f"T_{a} recurrence mismatch"
        a *= 2
    print(f"p={p}, n={n}: (1)-(6) PASS "
          f"(scales a in {sorted(2**k for k in range((n).bit_length()))}, b=0)")


run(31, 8)     # p = -1 mod 32
run(383, 32)   # p = -1 mod 128 (the cor:circle-32-family circle regime size)
```

Run output:

```text
p=31, n=8: (1)-(6) PASS (scales a in [1, 2, 4, 8], b=0)
p=383, n=32: (1)-(6) PASS (scales a in [1, 2, 4, 8, 16, 32], b=0)
```

## (d) Pay-per-bit H5 tie-in

`experimental/notes/audits/pay_per_bit_86bit_conditional_rows.md` marks both
M31 circle rows **blocked** on `H5`:

- `cor:circle-deployed(a)`: *"`H5`: `chi(twin coset)` is `(T_a,a)`-smooth, not
  a multiplicative coset"*;
- `cor:circle-deployed(b)`: *"`H5`: twin coset is a union of 2 cosets, and
  `k_c` is always odd so `a nmid k_c`"*;

and notes *"`H5` failing is not a technicality"*.  The `(T_a, a)`-smoothness
that `H5` names is exactly what this packet proves (`lem_cheb_fibers`), and
`lem_torus_fibers` produces exactly the `hsmooth : DomSmooth torus (·^a) a`
hypothesis consumed by the (still-`sorry`) `cor_circle_grand`.  Under the
readme's pay-per-bit framing (readme.md L12–23), this is legible progress on
the circle lane: the smoothness input of the `thm:phi-cap` route is now
machine-checked.  It does **not** change any row's blocked status — see
NON-CLAIMS.

## Self-Red-Team

- *Did we "prove" the skeleton by exploiting its vacuity?*  No — that was the
  trap.  The old `htwin` + `hdom` pair is inconsistent (Finding 3), so the old
  statement admits a vacuous discharge; we instead restated it with the papers'
  hypotheses and proved the real counting.  The vacuity claim itself was
  checked by hand (section pairing argument) and is falsifiable: exhibit
  `torus`, `dom` injective with `dom i = χ(torus i)` and any `i` with the
  `2a`-count — the pairing bound caps the count at `a + 1 < 2a` for `a ≥ 2`
  and at `1 < 2` for `a = 1`.
- *Is the Lean statement secretly weaker than the paper's?*  The main risks:
  (i) `lem_cheb_fibers` requires a **full** enumeration (`hcover`) — so does the
  paper (`D = χ(𝒟)`, all of it); (ii) fibers are counted inside the domain
  index set, which is `def:map-smooth`'s "(φ,c)-smooth as a subset of D"
  reading, matching `RSCap.DomSmooth` used by `cor_circle_grand`; (iii) the
  image-domain/tower clauses of `lem:cheb-fibers` are NOT formalized — declared
  in scope boundaries, not silently claimed.
- *Instance/axiom hygiene:* `#print axioms` on all 25 statement-map
  declarations (28 including the auxiliary lemmas `pow_card_subgroup_eq_one`,
  `twin_coset_pow_eq_card_left`, `twin_coset_pow_eq_card_right`): no axioms
  beyond `[propext, Classical.choice, Quot.sound]` (several use a proper
  subset); no `native_decide`, no `sorryAx`.  Classical `Decidable` instances
  appear only in `Finset.filter` plumbing.
- *Could the script's `g`-search bias the check?*  `n` is a power of two, so
  `u^{4n} = 1 ∧ u^{2n} ≠ 1` pins `ord(u) = 4n` exactly; every check is an
  exhaustive enumeration over the 2n-element twin coset, no sampling.
- *Line-number rot:* every `:NNNN` above was re-grepped at base `c35a6da`
  (`lem:torus-fibers:3910`, `lem:cheb-fibers:3923`, `rem:standard-position:3953`,
  `def:circle-twin-domain:2791`, `lem:cheb-smooth:2873`,
  `thm:fixed-length-prime-density:3009`, `cor:circle-32-family:3047`).

## NON-CLAIMS

1. **No M31 row unblocked.**  `cor:circle-deployed(a)/(b)` remain **blocked**
   on `H5` in the pay-per-bit ledger's sense: their certifying route
   (`thm:phi-cap` → `cor:circle-grand` with `lem:circle-rs` transport) is not
   formalized; `RSCap.cor_circle_grand`, `RSCap.lem_circle_rs`,
   `RSCap.lem_stereographic` are still `sorry`.  This packet formalizes the
   smoothness input only.
2. **No new bound, radius, or bit margin.**  Nothing here moves any printed
   number, the −0.3938 watch-item margin, or any safe-set endpoint.
3. **No torus construction.**  `𝕌`, `F_{p²}`, norm maps, primes, and densities
   are not formalized; Lean statements are for subgroups of `Fˣ`, generic
   finite field `F` (with `(2 : F) ≠ 0` where χ is involved).
4. **No claim about `lem:cheb-smooth`'s correctness beyond the discharged
   steps.**  The draft lemma's statement is confirmed (its hypotheses match
   v12's and the Lean proofs), but the draft's downstream uses
   (`cor:circle-32-family` SC3 numerics etc.) were not re-audited here.
5. **The rung ledger is not Lean-verified.**  Item (a) upgrades the *citation
   target* for `b = 0`; the ledger's integer gates and floors stand on their
   own prior verification.

## Use Rule

When citing this packet:

```text
object   = complete-fiber (b=0) twin-coset chain, Lean-proved in cs25_cap_v12
scope    = lem:torus-fibers + lem:cheb-fibers + rem:standard-position (v12)
           = lem:cheb-smooth + def:circle-twin-domain cardinality (draft)
verdict  = PROVED in Lean (25 mapped declarations, standard axioms only);
           two draft compression gaps discharged; in-tree htwin skeleton
           found vacuous and repaired (statement-level fix, documented)
watch    = unchanged: m31_mca Gceil c=2048 (-0.3938 b, TIGHT) — b=0 backing
           upgraded from printed to machine-checked
NOT      = an unblocking of cor:circle-deployed(a)/(b) (H5 rows stay blocked;
           cor_circle_grand / lem_circle_rs / lem_stereographic remain sorry)
```

Safety-side statements sourced from this packet MUST carry the qualifier
"smoothness input only"; any claim that a circle row's certification chain is
formalized MUST wait for `cor_circle_grand` and `lem_circle_rs`.

## Reproducibility

```text
cd experimental/lean/cs25_cap_v12 && lake build
```

(pinned `lean-toolchain` v4.28.0; `lake exe cache get` first on a cold cache).
Expected: build succeeds; `declaration uses 'sorry'` warnings only for
`lem_circle_rs`, `cor_circle_grand`, `lem_stereographic` in `CircleCode.lean`
and the pre-existing skeleton files (`Fiber`, `QuotientRemainder`, `ECFFT`,
`InterleavingTransfer`, `AperiodicHankel`).
