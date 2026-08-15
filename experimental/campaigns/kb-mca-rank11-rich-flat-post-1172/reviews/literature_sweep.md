# Targeted literature sweep

Date: 2026-08-15

Question: does an existing theorem directly bound the collection of actual
rank-one/rank-two minimizing-pair row spaces whose annihilators contain many
columns from one special Reed--Solomon evaluation subcode?

Primary source inspected:

- V. Guruswami and S. Kopparty, *Explicit Subspace Designs*, FOCS 2013;
  Combinatorica 36 (2016), 161--185.

That work proves strong subspace-design bounds for specifically constructed
families of multiplicity or folded-evaluation subspaces, using classical and
folded Wronskians.  It strongly motivates the next Wronskian attack here, but
its hypotheses do not identify the arbitrary, received-line-dependent
annihilator flats emitted by PR #1172.  Importing its numerical design
parameter would therefore be unjustified.

The present ordered-basis lemma is elementary and self-contained.  No external
theorem is load-bearing.  The literature sweep sharpens the successor problem:
prove that the special cyclic Reed--Solomon evaluation columns form a strong
design against the *actual emitted common-factor flag*, or derive an equivalent
Wronskian multiplicity bound with source chronology retained.
