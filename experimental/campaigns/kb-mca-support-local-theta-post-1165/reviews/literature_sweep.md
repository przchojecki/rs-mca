# Targeted external literature sweep

Date: 2026-08-12

After the final normal-flat gap was isolated, Exa was used for three
targeted searches covering 24 returned sources: finite-field
point--hyperplane incidence bounds, design-matrix/rich-flat rank bounds, and
affine-subspace structure in Reed--Solomon list decoding.  The purpose was
to find an existing theorem forcing the support-local quantity

```text
min_{gamma,b in C'} |{x in S_gamma : r1(x) != b(x)}|
```

to be large.  No such theorem is imported by this packet.

Representative primary sources screened:

- Phuong--Pham--Sang--Valculescu--Vinh, *Incidence bounds and applications
  over finite fields*, [arXiv:1601.00290](https://arxiv.org/abs/1601.00290).
- *A Point-Line Incidence Identity in Finite Fields, and Applications*,
  [arXiv:1601.03981](https://arxiv.org/abs/1601.03981).
- Dvir--Lovett, *Subspace Evasive Sets*,
  [author PDF](https://www.cs.princeton.edu/~zdvir/papers/DL12.pdf).
- Guruswami--Xing, *List decoding Reed--Solomon, Algebraic-Geometric, and
  Gabidulin subcodes up to the Singleton bound*,
  [ECCC TR12-146](https://eccc.weizmann.ac.il/report/2012/146/).

The incidence theorems control global incidence totals under field-size or
bipartite-subgraph hypotheses; they do not supply a uniform lower bound on
the last transverse support choice for each selected record.  Design-matrix
methods require overlap or regularity inputs absent from the active record
predicate.  Subspace-evasive constructions alter the code or message set
and do not constrain an arbitrary received-line support family.

Verdict: useful context, no load-bearing external lemma.  The exact local
margin `theta` remains the honest repaired invariant.  A new search should
begin only after the rank-10--12 direction-exception equations are frozen.
