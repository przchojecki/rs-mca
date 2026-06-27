# L1 Monomial Dyadic Descent Audit Checklist

- **Status:** AUDIT checklist for `l1_monomial_dyadic_descent_survivors.md`.
- **Agent/model:** Codex.
- **Date:** 2026-06-27.
- **Scope:** Review helper only. This file is not a separate theorem.

## Core Claims to Check

1. **Degree convention.** The note uses `deg P <= 256`. With this convention, `A`-admissibility is equivalent to

   ```text
   e_1(S)=e_2(S)=...=e_(A-257)(S)=0.
   ```

2. **Newton direction.** The proof uses only

   ```text
   e_1=...=e_d=0 => p_1=...=p_d=0.
   ```

   This direction does not require division by `1,2,...,d`, so there is no characteristic-17 issue.

3. **Local length-16 classification.** For `omega=3 in F_17` and

   ```text
   Delta(U)=sum_{q=0}^7 Delta_q U^q,
   Delta_q in {-1,0,1},
   ```

   the solutions to

   ```text
   Delta(omega)=Delta(omega^3)=0
   ```

   are exactly zero and the `16` signed skew shifts of

   ```text
   Delta_0(U)=U^2-U^3-U^4+U^5+U^6+U^7 mod U^8+1.
   ```

   Only zero also satisfies `Delta(omega^5)=0`.

4. **Basis comparison.** For `N in {512,256,128,64,32,16}`, with `h=N/16` and `G_N=<alpha>`, the basis

   ```text
   1, alpha, alpha^2, ..., alpha^(h-1)
   ```

   is valid over `F_17`, because `alpha^h=3` and `X^h-3` is irreducible for the listed powers of two. For `h>1`, use the binomial criterion with `ord_{F_17^*}(3)=16`, the only prime divisor `2 | 16`,

   ```text
   gcd(h, (17-1)/16) = gcd(h,1) = 1,
   ```

   and, when `4 | h`,

   ```text
   17 == 1 mod 4.
   ```

5. **Descent threshold.** The descent step uses only `p_q`, `p_(3q)`, and `p_(5q)`, so the threshold is

   ```text
   m >= 5 * 2^r.
   ```

6. **Quotient high-degree index.** If `S` is `K_Q`-periodic and `T=phi_Q(S)`, then

   ```text
   L_S(X)=L_T(X^Q).
   ```

   The coefficient `e_i(T)` occurs at degree `Q(B-i)`. Terms above degree `256` are those with `Q(B-i)>256`, i.e. `i <= B-D-1` for `D=256/Q`.

7. **Divisibility gate.** For `A`-admissible supports:

   ```text
   5 * 2^r <= A - 257 => 2^(r+1) divides A.
   ```

8. **Survivor table.** The candidate sizes left by the gate are:

   ```text
   258, 259, 260, 261, 262, 264, 266, 268,
   272, 276, 280, 288, 296, 304, 320, 336,
   352, 384, 416, 448, 512.
   ```

9. **Impossible rows.** The rows

   ```text
   261, 266, 276, 296, 336, 416
   ```

   are impossible because `d=4` and the complement size is odd, while `p_1=p_3=0` forces even local fiber sizes. The row `448` is impossible because its quotient complement has one nonzero point and cannot satisfy `p_1=0`.

10. **Existing rows.** The admissible sizes are exactly:

   ```text
   258, 259, 260, 262, 264, 268, 272, 280,
   288, 304, 320, 352, 384, 512.
   ```

11. **Family-vs-orbit scope.** The admissible-size classification is complete. The structural families `Z_1`, `Z_2`, and `Z_3` are normal forms for all quotient complements, not literal orbit-representative lists.

12. **Scope discipline.** The note should not be cited as an arbitrary-word locator bound, MCA bound, line-decoding bound, interleaved-list bound, or protocol theorem.

## Local Verifier

The local lemma is checked by enumerating the `3^8` imbalance vectors:

```bash
python experimental/scripts/verify_l1_monomial_dyadic_descent_local16.py
```

The verifier checks:

```text
len(solutions_13) == 17
weights == {0,6}
only zero also vanishes at 3^5
Delta_0 has values 0,0,15 at 3,3^3,3^5
```
