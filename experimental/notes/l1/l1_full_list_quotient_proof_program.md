# L1 Full-List Quotient Proof Program

Status: CONJECTURAL / PROOF PROGRAM.

Date: 2026-06-24.

Agent/model: Codex.

## Conjecture 1. Full-List Quotient-Budgeted L1

Fix a rate window and an entropy slack `epsilon > 0`.  There should be
constants `B,C,N_0`, depending only on the window and on `epsilon`, with the
following property.

Let `H_n <= F_q^*` be a smooth cyclic domain of order `n >= N_0`, with
generated field `q = poly(n)`.  Let

```text
k = rho n + O(1),
s = k + sigma,
```

and assume the generated-field reserve and lower cutoff clear:

```text
sigma log_2(q) >= (1 + epsilon) log_2 binom(n,s),
sigma >= C n / log n.
```

For every received word `U : H_n -> F_q`, define the actual Reed--Solomon list

```text
ImgFib_U(s) = { P in F_q[X] : deg P < k and
                |{x in H_n : U(x)=P(x)}| >= s }.
```

For `P in ImgFib_U(s)`, put

```text
A_P(U) = { x in H_n : U(x)=P(x) },
Stab(P;U) = { h in H_n : h A_P(U) = A_P(U) }.
```

For each divisor `d | n`, let

```text
Q_d^list(U,s) = #{ P in ImgFib_U(s) : |Stab(P;U)| = d }.
```

The conjecture is the primitive full-list bound

```text
Q_1^list(U,k+sigma) <= n^B
```

uniformly in `U`.  Equivalently,

```text
|ImgFib_U(k+sigma)|
  <= sum_{d>1} Q_d^list(U,k+sigma) + n^B.
```

This statement is deliberately about listed codewords, not raw support
subfibers.  The quotient term is not claimed small here; it is the structured
mass that must be charged to the separate quotient ledger.

## Why This Is The Right Object

The raw arbitrary-word support fiber is too large for a positive local limit:
one high-agreement codeword contributes every `s`-subsupport of its agreement
set.  Passing to `ImgFib_U(s)` removes that artificial multiplicity while
retaining the actual list object consumed by the repaired L1 package.

The exact stabilizer split also avoids treating quotient-periodic structure as
noise.  A large list caused by cyclic quotient symmetry should be paid for by
the quotient ledger.  Conjecture 1 asks only that the stabilizer-primitive
remainder is polynomial once the entropy reserve and lower cutoff clear.

## Proof Strategy

The intended proof is by contradiction.

1. **Sparse-syndrome formulation.**  Identify `ImgFib_U(s)` with the set of
   low-weight errors in one syndrome coset,

   ```text
   M_C e = z,        wt(e) <= n-s.
   ```

   The agreement set of the corresponding listed codeword is the zero set of
   `e`.

2. **High-multiplicity extraction.**  If `Q_1^list(U,s) > n^B`, extract a
   bounded-complexity sublist certificate: a small agreement hypergraph or RIM
   rank-defect witness whose listed codewords are still primitive after the
   quotient ledger is removed.

3. **Quotient and low-defect removal.**  Separate exact quotient-periodic
   strata, folded strata, and low-defect quotient closures before calling the
   remaining family aperiodic.  Exact stabilizer one is not by itself a
   sufficient aperiodicity condition.

4. **Aperiodic extension counting.**  For each extracted certificate `c`,
   prove a uniform bound

   ```text
   sum_c |E_b^aper(c)| <= n^(B-theta)
   ```

   for some `theta > 0`, after the quotient extension sets are charged to the
   quotient ledger.

5. **Packing closure.**  Combine the certificate packing lemma with the
   quotient and aperiodic extension budgets.  The leftover packing term is
   `O(log n)` at the intended cutoff and is absorbed by `n^B`.

## First Lemma Target

The first obstruction family isolated by the falsification scans is a
glued-codeword sunflower.  Let `C subset H_n` have size `k-1`, let
`T_1,...,T_M` be disjoint petals in `H_n \ C` of size `sigma+1`, and define

```text
L_C(X) = prod_{x in C}(X-x),
P_i(X) = c_i L_C(X)
```

with distinct nonzero `c_i`.  Define `U` by putting `U=P_i` on `T_i`, and
`U=0` on `C` and the unused background.

**Lemma target.**  For this sunflower received word, the number of non-planted
primitive listed codewords whose agreement sets mix several petals is bounded
by a fixed polynomial in `n`, and preferably by a small polynomial in the
planted floor

```text
M <= floor((n-k+1)/(sigma+1)).
```

Equivalently, if mixed-petal amplification is super-polynomial, then the
agreement equations must force quotient, low-defect, or another explicitly
budgeted structured family.

## Development Ledger

- **Conjecture 1 full-list primitive remainder:** CONJECTURAL.  Main proof
  target for this branch.
- **Sparse-syndrome formulation:** PROVED / AUDIT.  Import from the repaired
  L1 package and scanner.
- **Quotient exact-stabilizer ledger:** PROVED / AUDIT.  Use only as a
  separation ledger, not as an upper bound.
- **High-multiplicity certificate extraction:** PROVED / AUDIT.  Check that
  extracted certificates apply to the full-list object.
- **Quotient and low-defect removal:** PROVED / CONJECTURAL.  Import proved
  defect stripping; formulate the remaining arbitrary-word quotient upper
  budget.
- **Aperiodic extension counting:** CONJECTURAL.  Main quantitative theorem
  needed for Conjecture 1.
- **Mixed-petal sunflower amplification:** CONJECTURAL.  First focused lemma
  to prove or refute.
