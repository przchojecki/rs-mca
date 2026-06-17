# M2 Line-Decoding to MCA Bridge

**Status:** PROVED for the finite-support implications below; AUDIT for matching
external line-decoding theorems to this predicate.

This note isolates the exact line-decoding object that implies the support-wise
MCA bound used in `tex/snarks_v4.tex`.  It is meant as a small step toward the
M2 target in `agents.md`: restating the corrected residue-line packing
conjecture as a line-decoding statement with explicit parameters.  It does not
prove the corrected asymptotic MCA conjecture.

## Setup

Let `C <= F^D` be a linear code over a finite field `F`, with `|D|=n`.
For `S subset D`, write `C|S` for the punctured code on `S`.  Let

```text
a(delta) = ceil((1-delta)n).
```

For a line `ell_z = f + z g`, with `f,g in F^D`, call a slope `z`
support-wise noncontained at agreement size `a` if there is a support
`S subset D` such that

```text
|S| >= a,
(f + z g)|S in C|S,
and there do not exist c_f,c_g in C with f|S=c_f|S and g|S=c_g|S.
```

Define the support-wise line-decoding numerator

```text
LD_sw(C,a) =
  max_{f,g in F^D} #{z in F : z is support-wise noncontained for f+z g
                    at agreement size a}.
```

This is the line-decoding numerator that the MCA ledger can consume directly.

## Exact Bridge

For every linear code `C <= F^D` and every `delta in [0,1]`,

```text
eps_mca(C,delta) = LD_sw(C,ceil((1-delta)n)) / |F|.
```

This is an equality, not only an implication.  The support-wise MCA definition
maximizes over the same pairs `(f,g)` and counts the same slopes `z`: a large
support explaining the line point but not simultaneously explaining `(f,g)`.
The only conversion is from radius to agreement size by
`a=ceil((1-delta)n)`.

Consequently, any theorem proving

```text
LD_sw(C,a(delta)) <= a_LD
```

immediately gives

```text
eps_mca(C,delta) <= a_LD / |F|.
```

This is the precise finite-length content behind the manuscript phrase
`(delta,a_LD,n+1) line-decodable => eps_mca <= a_LD/|F|`.

## Per-Support Algebra

Fix `S subset D`.  The set of slopes that make the line point land in the
punctured code is

```text
E_S(f,g) = {z in F : f|S + z g|S in C|S}.
```

Because `C|S` is a linear subspace:

1. If `g|S in C|S` and `f|S in C|S`, then `E_S(f,g)=F`, but the support is
   contained and contributes no support-wise MCA-bad slope.
2. If `g|S in C|S` and `f|S notin C|S`, then `E_S(f,g)` is empty.
3. If `g|S notin C|S`, then `E_S(f,g)` has size at most one.  If it is
   nonempty, its unique element is noncontained on `S`.

Thus every contributing support contributes at most one bad slope.  For
Reed-Solomon codes, when `|S|>k`, the condition `g|S notin C|S` is exactly the
condition that the direction is not explained on that support by a degree `< k`
polynomial.  This is the local algebra behind both the one-bad-parameter
support bound and the residue-line packing formulation.

## What an External Line-Decoding Theorem Must Prove

A close-point line-decoding bound with a contained-line exception,

```text
either f+F g is contained in C, or #{z : dist(f+z g,C) <= delta} <= a_LD,
```

is sufficient, since support-wise noncontained slopes are a subset of close
line points, and a line contained in `C` has no support-wise noncontained
slopes.  This sufficient condition is usually stronger than necessary.

For a theorem with an exceptional "the line is explained" alternative, the
exception must be checked in the support-wise sense: for every close slope and
every large explaining support consumed by the protocol, the same support must
also explain both `f` and `g`.  A theorem that only says many line points are
close to `C` is not enough by itself, because MCA is sensitive to the common
support.

Therefore the corrected M2 target can be stated as:

```text
For C_n = RS[F_qn,H_n,k_n], delta_n = 1-rho-eta_n,
and a_n = ceil((1-delta_n)n),

LD_sw(C_n,a_n)
  <= n^{1+o(1)}
     + 2^{(beta(rho)/H(rho)) Q_Hn(a_n,k_n)(1+o(1))}
```

under the same entropy and quotient-profile hypotheses as the corrected MCA
conjecture.  The MCA statement is then the immediate corollary obtained by
dividing this numerator by `q_n`.

## Follow-Up Checks

- Match the external `(delta,a_LD,n+1)` line-decoding definition used in
  protocol papers against `LD_sw(C,a)`.
- Express the residue-line packing number in `tex/slackMCA_v3.tex` as this
  `LD_sw` numerator.
- Decide whether the `n+1` parameter is only a codeword-uniqueness threshold or
  whether it hides an additional proximity-loss convention.
