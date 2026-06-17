# Quotient-Core Interleaving Packet Certificate

- **Status:** PROVED for the closed-form quotient-core packet count.
- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Scope:** This note certifies
  `experimental/quotient_core_interleaving.py`, a deterministic calculator for
  the aligned L2 contribution of the quotient-core support packet.

## Claim Audited

Use the quotient-core construction from `tex/slackMCA_v3.tex`.  Let `K <= H`
have order `M`, put `N=n/M`, assume `M | k`, write `ell=k/M`, and choose one
omitted quotient coset with a slack set `T` of size `sigma<M`.  The base
quotient-core packet has

```text
L = binom(N-1,ell)
```

codewords, indexed by `ell`-subsets `A` of the remaining quotient cosets.  The
corresponding full agreement support is

```text
S_A = T union U_A,
```

where `U_A` is the union of the selected `K`-cosets.

For `mu` aligned rows using the same slack set `T`, the packet contribution to
the interleaved list at agreement `a=k+sigma` is exactly `L`, while the
Cartesian packet size is `L^mu`.  More explicitly,

```text
|S_{A_1} cap ... cap S_{A_mu}|
  = sigma + M |A_1 cap ... cap A_mu|,
```

so threshold `k+sigma=M ell+sigma` is reached iff all quotient choices are
equal.  If the row slack sets have common intersection smaller than `sigma`,
then the same exact-threshold packet contributes zero interleaved tuples.

The script checks the divisibility and slack hypotheses, then prints `L`,
`L^mu`, the aligned interleaved packet count, and the exact rational ratio
between the interleaved and Cartesian packet counts.  Small integers are
printed exactly; deployed-scale binomial coefficients are reported by digit and
bit length to keep JSON output bounded.

The script also supports arbitrary agreement thresholds through
`--agreement`.  If the common intersection of the row slack sets has size
`tau`, then the packet count at threshold `a` is determined by

```text
h = ceil((a-tau)/M).
```

If `h <= 0`, every Cartesian tuple contributes.  If `h > ell`, no tuple
contributes.  Otherwise the exact count is

```text
sum_{c=h}^ell binom(N-1,c) E_empty(N-1-c,ell-c,mu),

E_empty(R,b,mu)
  = sum_{j=0}^b (-1)^j binom(R,j) binom(R-j,b-j)^mu.
```

This is the common-intersection spectrum of `mu` ordered `ell`-subsets of the
`N-1` available quotient cosets.  It specializes to `L` at `a=k+sigma` with
aligned slack sets, and to `L^mu` once the threshold is low enough that no
common quotient coset is required.

## Reproducible Checks

Tiny dyadic quotient packet:

```bash
python3 experimental/quotient_core_interleaving.py \
  --n 8 \
  --k 4 \
  --sigma 1 \
  --M 2 \
  --rows 2
```

The same parameters with disjoint row slack sets:

```bash
python3 experimental/quotient_core_interleaving.py \
  --n 8 \
  --k 4 \
  --sigma 1 \
  --M 2 \
  --rows 2 \
  --slack-intersection 0
```

One step below the exact quotient-core threshold:

```bash
python3 experimental/quotient_core_interleaving.py \
  --n 8 \
  --k 4 \
  --sigma 1 \
  --M 2 \
  --rows 2 \
  --agreement 3
```

JSON mode is intended for later connection to the quotient-profile scanner:

```bash
python3 experimental/quotient_core_interleaving.py \
  --n 1048576 \
  --k 524288 \
  --sigma 1 \
  --M 2 \
  --rows 2 \
  --format json
```

## Use in the Program

This supports the L2 target in `agents.md`: test whether quotient-core lower
bounds multiply under interleaving or share the same support structure.  The
aligned quotient-core packet is diagonal under column interleaving.  It remains
a base-list obstruction, but it is not by itself a reason to charge the L2
ledger with the full Cartesian exponent.
