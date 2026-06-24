# M2 ABF/GG Line-Decoding Parameter Match

**Status:** AUDIT / SOURCE-CONDITIONED / PROVED local composition.

This note resolves the first parameter-level M2 follow-up in
`m2_line_decoding_mca_bridge.md`, subject to the same source caveat as the
Cycle120 ABF audit: the direct ePrint PDF was not fetched in this environment,
so the external wording is checked against the hash-pinned PR #96 ABF text
extracts.

## Source-Conditioned External Definition

The PR #96 ABF text extract records Definition 4.20, attributed there to GG25
Definition 3.1. In the notation used by the extract, a code is

```text
(delta,a,b) line-decodable
```

if for every line `f1+gamma f2` and every decoded assignment
`U:F -> C`, the implication holds:

```text
Pr_gamma[ distance(f1+gamma f2, U(gamma)) <= delta ] >= a/|F|
  => exists u1,u2 in C with
     Pr_gamma[ U(gamma) = u1+gamma u2 ] >= b/|F|.
```

The same extract records Theorem 4.21:

```text
If C is (delta,a,n+1) line-decodable, then
epsilon_mca(C,delta) <= a/|F|.
```

Thus the external `a` is exactly the line-decoding numerator consumed by the
MCA ledger, and the external `b=n+1` is the collinearity threshold in the
imported GG/ABF implication.  The line-decoding section has no second distance
parameter analogous to the CA proximity-loss pair `(delta_fld,delta_int)`.

## Local M2 Composition

The local support-wise bridge proves, for every linear code `C <= F^D`,

```text
epsilon_mca(C,delta)
  = LD_sw(C,ceil((1-delta)n)) / |F|.
```

Composing the two statements gives the exact finite-length M2 parameter match:

```text
C is (delta,a,n+1) line-decodable
  => LD_sw(C,ceil((1-delta)n)) <= a
  => epsilon_mca(C,delta) <= a/|F|.
```

For the corrected smooth-domain RS conjecture, the line-decoding form can
therefore use the same numerator as the support-wise residue-line packing
bound:

```text
a_LD(n,rho,eta)
  = n^{1+o(1)}
    + 2^((beta(rho)/H(rho)) Q_H(a_agree,k) (1+o(1))),
a_agree = ceil((rho+eta)n),
delta = 1-rho-eta,
b = n+1.
```

The displayed `a_agree=ceil((rho+eta)n)` is the agreement threshold in the
local `LD_sw` predicate; the external `a_LD` is the numerator in the
line-decodability statement.  Keeping these two quantities named separately
avoids a common ambiguity in M2 notes.

## What This Does And Does Not Prove

This closes a parameter-matching issue, not the positive M2 theorem.  It says
that if a future theorem proves ABF/GG `(delta,a_LD,n+1)` line-decodability
for the smooth RS row, then the existing M2 bridge gives the intended MCA
budget with no hidden square-root loss and no additional proximity-loss
parameter.

It does not prove that smooth RS codes are line-decodable with the corrected
reserve numerator, and it does not independently reprove GG25 Theorem 3.5.
The official ABF ePrint/source retrieval and revision check also remain open.

## Verifier

The verifier

```bash
python3 experimental/scripts/verify_m2_abf_gg_line_decoding_parameter_match.py
python3 experimental/scripts/verify_m2_abf_gg_line_decoding_parameter_match.py --json
```

checks the PR #96 text extract hashes, checks that page 22 contains the
Definition 4.20 and Theorem 4.21 fragments needed above in both text
extracts, and emits the composed M2 parameter conclusion.
