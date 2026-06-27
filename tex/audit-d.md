# Audit of Paper D's CS25 dependency

Date: 2026-06-26

Files audited:

- `cs25_cap_v4(2).tex`
- supporting cross-checks in `slackMCA_v3(2).tex`, `experiments(6).tex`, and `snarks_v4(2).tex`

## Verdict

Paper D's use of the Crites--Stewart conversion is internally consistent, and the main cap proof uses only a very shallow consequence of the imported theorem.

More importantly, the imported CS25 consequence used in Paper D can be reproved directly by the simple-pole/deep-point argument already present in the experimental notes. Thus the main universal cap in Paper D does not need to remain conditional on CS25 for this specific conversion: Paper D can replace its imported Theorem A by a self-contained theorem with the same constants.

The remaining external dependencies are then:

1. historical/provenance citations to CS25 and ABF26;
2. the separate slacked BCHKS/ABF fallback route, which is not used for the main cap;
3. any claim that wants to identify Paper D's conversion with CS25's published theorem rather than use the self-contained proof.

## What Paper D imports

Paper D currently states an imported theorem:

Let `C = RS[F,D,k]`, `C^+ = RS[F,D,k+1]`, `q = |F|`, `n = |D|`, and `f_delta = floor(delta n)`. If

```text
f_delta < n-k-1
```

and for some `eta in [0,1)`

```text
epsilon_ca(C,delta) <= eta * (1/k - n/(kq)),
```

then

```text
List(C^+,delta) <= ceil(q * epsilon_ca(C,delta)/(1-eta)).
```

Paper D cites this as implied by Crites--Stewart Theorem 2 and then applies it with `eta = 1/2`.

## Self-contained proof of the imported consequence

The consequence follows from a direct deep-point argument.

Let `U : D -> F` have `L` distinct nearby `C^+` codewords `P_1,...,P_L` at integer error `f`, so each `P_i` agrees with `U` on at least

```text
a = n-f
```

positions. Assume `f < n-k-1`, hence `a > k+1 > k`.

For each deep point `alpha in Omega := F \ D`, define

```text
f_alpha(x) = U(x)/(x-alpha),
g_alpha(x) = -1/(x-alpha).
```

For every listed polynomial `P_i`, the slope

```text
z_i(alpha) = P_i(alpha)
```

makes

```text
f_alpha(x) + z_i(alpha) g_alpha(x)
= (P_i(x)-P_i(alpha))/(x-alpha)
```

on the agreement support of `P_i`. The right side has degree `< k`, so the line point is `delta`-close to `C`.

The pair `(f_alpha,g_alpha)` is globally `C^2`-far at radius `delta`: if `g_alpha` agreed with a degree-`<k` polynomial on more than `k` points, then `(X-alpha)G(X)+1` would be a degree-`<=k` polynomial with more than `k` roots but value `1` at `alpha`, impossible.

Thus distinct values among the evaluations `P_i(alpha)` are CA-bad slopes.

For distinct `P_i,P_j`, the polynomial `P_i-P_j` has degree at most `k`, so it has at most `k` roots in `Omega`. Averaging collisions over `Omega` gives some `alpha` with at least

```text
M(alpha) >= L(q-n)/(q-n+kL)
```

distinct values. Hence

```text
epsilon_ca(C,delta) >= M(alpha)/q >= L(q-n)/(q(q-n+kL)).
```

Solving for `L`, with `epsilon = epsilon_ca(C,delta)`, gives

```text
L <= epsilon q (q-n)/(q-n-k epsilon q),
```

provided `epsilon < (q-n)/(kq)`. If

```text
epsilon <= eta (q-n)/(kq),
```

then the denominator is at least `(1-eta)(q-n)`, so

```text
L <= q epsilon/(1-eta).
```

This is exactly the relative-radius conversion Paper D imports, up to the harmless ceiling.

## Audit of Paper D's use of the conversion

### 1. Integer-radius condition

Paper D applies the conversion only for

```text
delta < 1-rho-1/n.
```

Then

```text
floor(delta n) < n-k-1,
```

so the imported/self-contained theorem is admissible.

At the endpoint

```text
delta_N = 1-rho-2/N,
```

we have

```text
delta_N n = n-k-2(n/N),
```

so the condition also holds. Paper D proves the CA lower bound on the CS-admissible interval and extends only MCA to all larger sub-capacity radii by support-wise MCA monotonicity. This is correct.

### 2. Augmented code `C^+`

Paper D's locator-fiber lemma produces codewords in

```text
RS[F,D,k+1]
```

because the remainder has degree `<= k`, i.e. degree `< k+1`. This matches the augmented code consumed by the conversion.

The slack-two construction avoids the false divisibility demand `n/N | k+1`; the required divisibility is only `n/N | k`, which Paper D verifies.

### 3. List monotonicity in radius

The locator-fiber lemma gives a list at radius

```text
delta_N = 1-rho-2/N.
```

Paper D uses this list at every `delta >= delta_N` by monotonicity of list size in the radius. This is correct.

### 4. CA normalization

The proof above uses exactly Paper D's no-loss CA normalization: density over finite slopes `gamma in F`, denominator `q = |F|`, and a global pair-distance condition to `C^2` at the same radius. No projective-slope or extension-denominator adjustment is hidden.

### 5. Extension-field sampling

The proof works over the actual ambient field `F` and chooses `alpha in F \ D`, so the denominator is `q = |F|`. If `D` lies in a subfield `B`, the resulting certifying line is generally genuinely `F`-valued, consistent with Paper D's subfield-confinement corollary.

### 6. Constants and ceilings

With `eta = 1/2`, the conversion gives

```text
List(C^+,delta) <= ceil(2q epsilon_ca(C,delta)).
```

If

```text
epsilon_ca(C,delta) <= (1/(2k))(1-n/q),
```

then

```text
List(C^+,delta) <= ceil((q-n)/k) < (q-n)/k + 1 <= q/k + 1.
```

Paper D's locator lower bound gives

```text
List(C^+,delta) >= binom(N,rho N+2)/|B| >= q/k + 1,
```

contradiction. The strict/weak inequalities are correctly oriented.

### 7. CA-to-MCA transfer

Paper D proves `epsilon_ca(C,delta) <= epsilon_mca(C,delta)` from the definitions. This is correct: a CA-bad slope supplies a large support explaining the line point, while global pair-farness rules out simultaneous explanation on any support of that size, hence on the chosen support.

### 8. MCA monotonicity

Paper D's MCA extension from `delta_N` to all larger `delta < 1-rho` is valid for support-wise MCA: the same witness support remains large enough when the radius increases.

## Remaining caveats

1. The current text should stop saying the main cap is conditional on CS25 once the self-contained proof is inserted. It can say the theorem is the same consequence attributed to Crites--Stewart, but Paper D proves the needed form directly.

2. The separate slacked fallback through BCHKS/ABF remains external. It is not needed for the main universal cap.

3. The external CS25 paper was not available in this environment because the ePrint page is blocked to the web fetcher. Therefore this audit does not certify that Paper D quotes CS25 word-for-word. Instead, it shows that the quoted consequence is true by an independent proof.

4. The result is still a coding-theoretic CA/MCA cap, not a complete protocol soundness theorem. Protocol use still needs the Paper C ledgers: challenge field, interleaving, curve/folding/query terms, and cryptographic terms.

## Recommended Paper D patch

Replace the proof of Theorem A with the self-contained deep-point proof. Rename the theorem to something like:

```latex
\begin{theorem}[deep-point list-to-CA conversion]
```

and cite CS25 only in a remark:

```latex
This is the consequence of Crites--Stewart used in earlier drafts; we include the direct proof to remove the black-box dependency.
```

Then update the verification caveat from:

```text
readers should treat Corollary grand as conditional on the correctness of the direct CS25 conversion
```

to:

```text
the main cap no longer depends on CS25; only the independent slacked fallback remains imported.
```

## Bottom-line status

- **Main Paper D cap:** can be made self-contained, modulo only the locator-fiber lemma already proved in Paper D.
- **CS25 dependency:** no longer load-bearing for the main cap after adding the deep-point proof.
- **Best next action:** patch Theorem A and the discussion/abstract to remove conditional language, while retaining CS25 as historical/provenance citation.
