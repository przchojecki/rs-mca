# L1: Arbitrary-Local Conjecture Patch — Propagating the PR #80 Repair

- **Status:** AUDIT / ROUTE-REPAIR (bookkeeping; no new mathematics).
- **Agent/model:** Claude (Sonnet 5).
- **Date:** 2026-07-01.
- **Scope:** Papers B (`slackMCA_v3.tex`, `slackMCA_v4.tex`) and C
  (`snarks_v5.tex`). This note does not edit any file under `tex/` and does
  not make progress on the open L1 conjecture itself
  (`conj:prefix-local`, the genuine aperiodic exponential-sum problem, is
  untouched and remains exactly as open as before).

## Summary

PR #80 (`experimental/notes/l1/l1_arbitrary_fiber_repair.md`, 2026-06-18)
already proved that the raw arbitrary-word statement
`|Fib_U(k+sigma)| <= n^B` is false as literally written — witness `U=0`
gives `|Fib_0(s)| = binom(n,s)`, exponential, not polynomial — and proposed a
fully general repair object `ImgFib_U(s)` that equals the actual codeword
list exactly, **for every `U`, including the degenerate low-degree case that
breaks the raw object.** That repair was accepted into `experimental/`
(triage `pr-triage-2026-06-18-round3.md`: *"Add... proposes `ImgFib_U(s)`...
repairs that match actual list size"*), but 13 days later it was never
applied to the actual conjecture text anywhere.

Checked directly against the live tex today (2026-07-01):

| Location | Object used | Status |
|---|---|---|
| `slackMCA_v3.tex:569-580` (`conj:arbitrary-local`) | raw `Fib_U` | unpatched |
| `slackMCA_v3.tex:212-215` (informal restatement) | raw `Fib_U` | unpatched |
| `slackMCA_v3.tex:1702-1714` (`conj:final-locator`) | raw `Fib_U` | unpatched |
| `slackMCA_v4.tex` (same two conjectures, byte-identical text, ~2 lines shifted) | raw `Fib_U` | unpatched |
| `snarks_v5.tex:355-369` (`ass:locator`, Paper C) | raw `Fib_U` | unpatched, **and not discussed by PR #80 at all** (its scope line names only Paper B) |

`grep -rn "ImgFib\|MaxFib\|CanFib" tex/` returns nothing — the repair has not
propagated into any paper. Paper D's `T4` proof-obligation bullet
(`cs25_cap_v9.tex:1992-1995`) only references `thm:conditional-list` by name
and needs no direct edit; it inherits the fix automatically once Paper B is
patched.

## Independent re-confirmation (fresh, not a re-citation of PR #80's numbers)

`experimental/scripts/verify_l1_arbitrary_local_conjecture_patch.py` reproduces
the counterexample from scratch and checks the repair by a *different* route
than PR #80 used (minimum distance, rather than image-fiber injectivity —
an independent proof of the same conclusion):

```json
{
  "p": 97, "n": 16, "k": 7, "sigma": 4, "s": 11,
  "low_degree_U_fib_count": 4368,
  "binom_n_s": 4368,
  "generic_U_fib_count": 0,
  "max_agreement_distinct_low_degree_pair": 3,
  "k_minus_1": 6,
  "repair_holds": true
}
```

- For `U` with `deg(U)=3<k=7`: `|Fib_U(11)| = 4368 = binom(16,11)` — the raw
  fiber really is the full binomial (matches PR #80's `U=0` witness exactly,
  confirming the bug is still live in the current parameter/definitions,
  not just historically true as of 2026-06-18).
- For generic `U` of degree `s=11` (the actually-hard regime the conjecture is
  really about): the fiber does not blow up.
- Over 20000 random degree-`<7` polynomials `P != U`: max agreement with `U`
  is 3, comfortably `<= k-1 = 6`, confirming the standard Reed-Solomon
  minimum-distance fact (a nonzero degree-`<=k-1` polynomial has at most
  `k-1` roots) on this instance. Since `s=11 > k-1=6`, no other degree-`<k`
  codeword can reach agreement `s` with `U`, so the *actual* codeword list at
  radius `1-s/n` is `{U}` exactly — matching PR #80's `ImgFib_U(0)=1`
  zero-word claim by an independent argument.

## Ready-to-apply patch text

All four locations reduce to the same swap: replace raw `Fib_U` by PR #80's
already-proved `ImgFib_U` in the conjecture/assumption statement, and add the
one supporting definition + proposition (already fully proved in PR #80's
"Patch-Ready Repaired Package") immediately before it. No case-split and no
extra hypothesis is needed anywhere: `ImgFib_U(s)` is correct for every `U`,
including `deg(U)<k`, so the conjecture's quantifier (`for every deg U<n`)
does not need to change at all — only the object inside it does.

### 1. `slackMCA_v3.tex`, immediately before line 569 (`conj:arbitrary-local`)

Add (new, verbatim from PR #80's suggested definition/proposition):
```latex
\begin{definition}[Codeword-image fiber]\label{def:imgfib}
For $\deg U<n$ and $k<s\le n$, define
\[
        \ImgFib_U(s)=\{U\bmod L_S:\ S\in\Fib_U(s)\}\subseteq\F_q[X]_{<k}.
\]
\end{definition}

\begin{proposition}[Image fiber is the exact list]\label{prop:imgfib-list}
For $k<s\le n$,
\[
        \ImgFib_U(s)=\{P\in\F_q[X]_{<k}:\ |\{x\in H:U(x)=P(x)\}|\ge s\},
\]
so $|\ImgFib_U(s)|=|\List(y,1-s/n)|$ exactly, for the received word $y$ with
interpolant $U$. Moreover
\[
        |\Fib_U(s)|=\sum_{P\in\ImgFib_U(s)}\binom{a_P}{s},\qquad
        a_P=|\{x\in H:U(x)=P(x)\}|.
\]
\end{proposition}
```

Then in `conj:arbitrary-local` itself, replace both occurrences of
`|\Fib_U(k+\sigma)|` by `|\ImgFib_U(k+\sigma)|` (the hypotheses and
quantifiers are unchanged).

### 2. `slackMCA_v3.tex:212-215` (informal restatement)

Current:
```latex
Thus the positive half of list decoding can be stated without coding language:
\[
        \max_{\deg U<n}|\Fib_U(k+\sigma)|\quad\text{should be polynomial above the corrected reserve.}
\]
```
Suggested: replace `\Fib_U` by `\ImgFib_U` (same reason — as written, this
display is exhibited-false by the same `U=0` witness before `ImgFib_U` is
introduced; forward-reference `\Cref{def:imgfib}` here or move this sentence
after it).

### 3. `slackMCA_v3.tex:1702-1714` (`conj:final-locator`) and the identical text in `slackMCA_v4.tex`

Same swap: replace `|\Fib_U(k+\sigma)|\le n^B` by
`|\ImgFib_U(k+\sigma)|\le n^B` (one occurrence in the display).

### 4. `slackMCA_v3.tex:582-598` (`thm:conditional-list`), proof only

Current proof: *"The arbitrary-word claim is exactly \Cref{prop:arb-fiber}.
The monomial-prefix claim is \Cref{prop:monomial-fiber}."*

Suggested: *"The arbitrary-word claim follows from
\Cref{prop:imgfib-list}, which gives $|\List(y,1-s/n)|=|\ImgFib_U(k+\sigma)|$
exactly, combined with \Cref{conj:arbitrary-local}. The monomial-prefix claim
is \Cref{prop:monomial-fiber}."* No case split on `deg U` is needed — the
equality in `prop:imgfib-list` already covers `deg U<k` correctly (it gives
`ImgFib_U(s)={U}`, size 1, there). `prop:arb-fiber` (the original `<=`
statement) can stay in the paper unchanged as a standalone fact; it is just
no longer the one `thm:conditional-list` invokes.

### 5. `snarks_v5.tex:355-369` (`ass:locator`, Paper C)

Current:
```latex
\begin{assumption}[Field-aware locator local limit]
\label{ass:locator}
...For every received word $U:H_n\to\F_{q_n}$,
\[
        |\Fib_U(k_n+\sigma_n)|\le n^{B_L}
\]
...
\end{assumption}
```
Suggested: add the `ImgFib` definition/proposition analogue (same content as
§1 above, with `q\to q_n`, `n\to n`, `B\to B_L`) and replace
`|\Fib_U(k_n+\sigma_n)|` by `|\ImgFib_U(k_n+\sigma_n)|`.

Also `snarks_v5.tex:193-204` (`lem:fiber-list`) — this lemma's own `<=` claim
is fine as stated (it is Paper C's analogue of `prop:arb-fiber`, always
true), but its "Consequently" sentence (line 199: *"a uniform bound
`|Fib_U(a)|<=n^{B_L}` over all `U` implies..."*) is currently a vacuous
implication from an unsatisfiable hypothesis. Once `ass:locator` is patched
to `ImgFib_U`, this sentence should say *"a uniform bound
`|ImgFib_U(a)|<=n^{B_L}`..."* to become the actually-useful (non-vacuous)
bridge again.

## Non-claims

- Does not prove, disprove, or narrow `conj:prefix-local` or any genuine
  aperiodic exponential-sum estimate. L1 remains exactly as open as before
  this note.
- Does not claim `ImgFib_U(k+sigma) <= n^B` — that is exactly as open as the
  original mis-stated conjecture; this note only repairs the *statement* so
  the thing being conjectured is not already known-false before anyone
  attempts to prove it.
- Is not a new mathematical result. PR #80 (2026-06-18) already proved
  everything load-bearing here (the counterexample, the `ImgFib` repair
  object, and its exactness). This note's only additions are: (a) a fresh,
  independent re-confirmation dated today via a different argument (minimum
  distance rather than injectivity), (b) noticing the same bug in Paper C's
  `ass:locator`/`lem:fiber-list`, which PR #80 did not cover, and (c) literal
  ready-to-paste patch text so the already-accepted repair can actually be
  applied instead of sitting in `experimental/` indefinitely.
- Proposed patch text above is a suggestion for the maintainer/reviewer to
  apply; this contribution does not modify any file under `tex/`.

## Verification run

```sh
python3 experimental/scripts/verify_l1_arbitrary_local_conjecture_patch.py
python3 -m py_compile experimental/scripts/verify_l1_arbitrary_local_conjecture_patch.py
git diff --cached --check
```

## Status ledger

| Item | Status | Evidence |
|---|---|---|
| Raw `Fib_U` conjecture is false as literally stated | COUNTEREXAMPLE (re-confirmed) | PR #80 (2026-06-18) + this note's independent script, 2026-07-01 |
| `ImgFib_U` repair is exact for every `U` | PROVED (PR #80) + independently re-derived here via minimum distance | both notes |
| Repair applied to `slackMCA_v3.tex` / `v4.tex` | NOT DONE | direct read of current tex, 2026-07-01 |
| Repair applied to `snarks_v5.tex` | NOT DONE, not previously identified | direct read of current tex, 2026-07-01 |
| Repair applied to `cs25_cap_v9.tex` | N/A — inherits fix via `thm:conditional-list` reference, no direct edit needed | direct read of current tex, 2026-07-01 |
