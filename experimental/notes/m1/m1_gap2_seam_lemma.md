# M1: GAP-2 quotient-periodic seam lemma

- **Status:** PROVED arithmetic lemma + verifier.
- **Agent/model:** Codex, acting autonomously for AllenGrahamHart.
- **Date:** 2026-07-02.
- **DAG target:** `gap2_seam`.
- **Verifier:** `experimental/scripts/verify_m1_gap2_seam_lemma.py`.
- **Artifact:** `experimental/data/certificates/m1-gap2-seam/gap2_seam_certificate.json`.

## Statement

Let `n` be the smooth-domain length, `k` the RS dimension, `A` an exact
agreement level, and write

```text
j = n - A,          t_win = A - k,          r = n - k.
```

Thus

```text
j + t_win = r.
```

Let `M > 1`.

1. If a residue-line denominator is a pullback

```text
E(X) = g(X^M),
```

then its denominator degree `t_denom = deg(E)` is divisible by `M`.

2. If `M | gcd(n,k)`, then `M | r`.  Hence for every exact bucket,

```text
M | j       if and only if       M | t_win.
```

On these buckets the quotient parameters

```text
n/M,  k/M,  A/M,  j/M,  t_win/M
```

are all integral.  Therefore the line-side quotient-periodic strip
`M | gcd(n,k)` and the support-side `M | gcd(n,j)` strip coincide exactly on
rate-preserving quotient descents.

3. If `M | n` and `M | j` but `M` does not divide `k`, then `A=n-j` descends
but `k` and `t_win=A-k` do not.  This is a non-rate-preserving seam, not a
quotient row of dimension `k/M`.

## Proof

For (1), `deg(g(X^M)) = M deg(g)`.

For (2), `M | n` and `M | k` imply `M | r=n-k`.  Since `r=j+t_win`, reducing
modulo `M` gives

```text
j == -t_win  (mod M).
```

Thus one of `j,t_win` is divisible by `M` exactly when the other is.  If this
happens, then `A=n-j` is also divisible by `M`, and all quotient bucket
parameters displayed above are integral.

For (3), `M | n` and `M | j` imply `M | A=n-j`.  If `M` does not divide `k`,
then `M` cannot divide `t_win=A-k`.  So the support folds, but the RS dimension
and syndrome-window count do not descend to a same-rate quotient instance.

## Consequence

This closes the arithmetic part of the GAP-2 seam flagged in the strip-periodic
roadmap:

```text
rate-preserving quotient strip:  M | gcd(n,k)
support-side periodic bucket:    M | j
window-side quotient bucket:     M | t_win
```

Inside the rate-preserving hypothesis, the two bucket divisibility conditions
are equivalent.  Outside it, the seam is real but should be labelled
non-rate-preserving rather than priced by the quotient-row recursion.

This note does not prove that every stable support gives a pullback
denominator, does not price the GAP-1 non-equivariant periodic mass, and does
not prove the aperiodic local limit.

## Reproduce

```bash
python3 experimental/scripts/verify_m1_gap2_seam_lemma.py --emit
python3 experimental/scripts/verify_m1_gap2_seam_lemma.py
```
