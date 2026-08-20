# Targeted interleaving literature sweep

Date: 2026-08-13

Exa reviewed 20 search results across two targeted workstreams and fetched
the two most relevant primary papers.

1. Gopalan, Guruswami, and Raghavendra, *List decoding tensor products and
   interleaved codes*, STOC 2009,
   <https://dl.acm.org/doi/10.1145/1536414.1536419>.  This proves broad
   combinatorial/radius results for interleaving.  It does not state the
   exact finite-field projection bound used here.
2. Guo, Li, Shangguan, Tamo, and Wootters, *Improved List-Decodability of
   Reed--Solomon Codes via Tree Packings*, arXiv:2011.04453,
   <https://arxiv.org/abs/2011.04453>.  This develops intersection-matrix and
   tree-packing methods for RS list decoding/list recovery.  It is relevant
   to the next aggregate pair/core-incidence problem, but is not an input to
   the present theorem.

The present sub-square-root collapse is proved self-contained by averaging
linear projections and counting pair collisions.  No external theorem is
load-bearing.  The literature search mainly confirms that the next rank-11
joint belongs to aggregate intersection/list-recovery structure, not to the
one-pair multiplicity already shown sharp by the GF(11) control.
