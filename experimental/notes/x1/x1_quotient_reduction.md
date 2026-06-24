# X1: the quotient reduction — period-`d` mass is the same-rate L1 problem on `H_{n/d}`

- **Status:** PROVED (the reduction `Q_d(H_n) = Q_1(H_{n/d})`, same rate) +
  verified (`verify_x1_quotient_reduction.py`). The per-scale **reserve**
  bookkeeping (full growing-`d` resolution) remains open — see caveat.
- **Agent/model:** Claude Opus 4.8 (L2/X1 lane, branch `allen/l2-x1-interleaved-mca`).
- **Date:** 2026-06-24.
- **Scope:** the growing-`d` open piece left by `x1_nonequivariant_product_bound.md`;
  unifies the slope-side QuotientBudget analysis with Codex's Möbius `Q_d`
  decomposition (#106). Does not edit Papers A–D.

## The reduction

Let `H_n = ⟨ω⟩` be cyclic of order `n`, `d | n`, `K_d` the unique order-`d`
subgroup, and `φ : x ↦ x^d` the `d`-to-1 map onto the **quotient domain**
`H_{n/d}` (its fibers are exactly the `K_d`-cosets). Then:

1. A `K_d`-stable support `S` (a union of `K_d`-cosets) pushes to `S' = φ(S)` on
   `H_{n/d}` with `|S'| = |S|/d`.
2. **`Stab_{H_n}(S) = K_d` exactly ⟺ `S'` is primitive (trivial stabilizer) on
   `H_{n/d}`.** (`H_n` cyclic ⟹ a unique subgroup of each order, so "exact
   stabilizer order `d`" means `Stab = K_d`; the induced action gives
   `Stab(S)/K_d ≅ Stab_{H_{n/d}}(S')`.) Hence, with `Q_d` = exact-stabilizer-`d`
   mass and `Q_1` = primitive mass,
   ```
   Q_d(H_n)  =  Q_1(H_{n/d}).
   ```
3. The folded codewords `P = G(X^d)` of degree `< k` correspond bijectively to
   codewords `G` of degree `< k/d` on `H_{n/d}`, with `P(x) = G(x^d)`. The
   **rate is preserved**: `(k/d)/(n/d) = k/n`.

Verified exactly over `F_13`, `H_12`, for `d ∈ {2,3,6}`: `φ` is `d`-to-1 with
`K_d`-coset fibers, rate `1/2 → 1/2`, the stabilizer bijection holds, and the
folded↔quotient codeword bijection holds. (`verify_x1_quotient_reduction.py`.)

## Two consequences

### (A) The growing-`d` mass does not blow up — it shrinks the domain
The product bound `≤ C^d` (`x1_nonequivariant_product_bound.md`) is a gross
overestimate. The period-`d` QuotientBudget mass is the **same-rate L1 fiber
problem on the smaller domain `H_{n/d}`**. As `d` grows, `n/d` shrinks, so
large-period mass is governed by a *smaller* instance of the very same problem —
not an exponential `C^d`. For the deep cap (`d = a_q`), the relevant domain is
`H_{n/a_q} = H_N`, the small parameter `N` that `lem:fiber` already counts on.

### (B) This *is* Codex's Möbius decomposition — multi-scale, one recursion
Codex's ledger (#106) is `|Fib_U| = Σ_{d|n} Q_d(H_n)`. By the reduction this is
```
|Fib_U(H_n)|  =  Σ_{d | n}  Q_1(H_{n/d}),
```
the sum over divisors of the **primitive mass at each quotient scale**
`H_{n/d}`. So the slope-side confinement/QuotientBudget analysis
(`x1_confinement_from_stabilizer.md`, `x1_prefix_locator_slope_principle.md`) and
Codex's stabilizer budget are the **same multi-scale recursion** seen from two
sides: each `Q_d` is the primitive core of a same-rate problem one quotient level
down. The L1 conjecture `Q_1(H_m) ≤ m^B` is therefore a statement applied at
*every* scale `m = n/d`.

## Honest caveat — the per-scale reserve is the real remaining content

The L1 conjecture bounds `Q_1(H_m) ≤ m^B` only **above the reserve at scale `m`**.
The reduction does *not* by itself bound the QuotientBudget, because the quotient
problems may be **below** their own reserve. Indeed `lem:fiber`'s exponential mass
is exactly `Q_1` on a quotient `H_N` that sits **below `H_N`'s reserve** — which is
why it can be exponential without contradicting the conjecture. So:

> The growing-`d` question is *not* "does `C^d` stay polynomial" (it is the wrong
> bound); it is **"at which quotient scales `H_{n/d}` does the reserve hold?"** —
> a sharper, structured, multi-scale reserve-bookkeeping question. Resolving it is
> the genuine remaining work; this note reduces the growing-`d` concern to it.

This is honest progress: the open piece is now a precise multi-scale reserve
condition, tied to the *same* per-scale `Q_1` objects Codex's conjecture concerns,
rather than a vague "non-equivariant mass might blow up."

## Verification

```bash
python3 experimental/scripts/verify_x1_quotient_reduction.py
```

## Ledger impact

- **Growing-`d` (reframed):** period-`d` QuotientBudget = same-rate L1 on
  `H_{n/d}`; the open piece is the per-scale reserve, not a `C^d` blow-up.
- **Unification with #106:** Codex's Möbius `Q_d` = primitive mass `Q_1(H_{n/d})`
  at quotient scale; slope-side and combinatorial-side analyses are one
  multi-scale recursion. Each `Q_d` is a smaller same-rate instance.
