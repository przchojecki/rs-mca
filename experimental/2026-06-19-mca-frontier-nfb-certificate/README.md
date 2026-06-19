# Deep-hole F\B N_FB certificate packet

Status: **AUDIT / PROOF-COMPOSITION / EXPERIMENTAL PACKET**.

This folder records a small, self-contained certificate packet for the
extension-valued deep-hole line mechanism behind `cor:Fvalued`-style density.
It is meant as an experimental companion to Paper D and the F1 direction in
`agents.md`, not as an edit to the main papers.

The packet deliberately separates imported mathematics from the local
certificate layer:

| Item | Status in this packet |
|---|---|
| quotient-locator / heavy-fiber machinery | imported from the repo papers and proximity-gap literature |
| CS25 distinct-evaluation / collision bound | imported; separately audited by existing A0 material |
| explicit deep-hole lift to F-valued lines | local proof-composition target |
| base-coefficient non-base bound | local lemma recorded here |
| toy arithmetic and deployed inequality | frozen JSON certificate |

## Result recorded

Let `B = F_p` and `F/B` be an extension with smooth domain `D subset B`.
For a heavy quotient-locator word `u` with list codewords `c_A in B[X]`, choose
a deep hole `a in F\B` and set

```text
f = u / (x - a)
g = 1 / (x - a).
```

For every list element `c_A`, the slope

```text
z_A = -c_A(a)
```

is a candidate extension-valued bad slope for the fixed line `(f,g)`.  The
useful count is

```text
N_FB(f,g) = #{z in F\B : z is MCA/CA-bad for the fixed line}.
```

The frozen certificate `nfb_deployed_certificate.json` records three checks:

1. At the toy instance `F_17^2`, `n=16`, `k=8`, the deep-hole family has
   `250` distinct evaluations and at least `235` verified `F\B` bad slopes.
2. The base-coefficient non-base lemma is checked exhaustively on the toy
   fiber: all `472` codewords are nonconstant and
   `max_A #{a in F : c_A(a) in B} = 53 <= p*k = 136`.
3. At the KoalaBear-sextic deployment arithmetic, the composed lower bound
   satisfies

```text
log2 N_FB lower bound ~= 165.93
log2 ((q-n)/(2k))    ~= 164.93
```

so the arithmetic clears the cap target by about one bit, conditional on the
imported heavy-fiber and CS25 collision inputs.

## Base-coefficient non-base lemma

For `c_A in B[X]` nonconstant of degree at most `k`, the set of extension points
where `c_A(a)` lands back in `B` is bounded by `p*k`: it is the union, over the
`p` base values, of at most `k` roots each.  On the `z0=0` fiber, nonconstancy
follows from the divisibility condition `ell nmid N`; in the recorded deployed
row, `ell=130` and `N=256`.

This is the local step that converts a distinct-evaluation bound into an
`F\B` bad-slope lower bound.  It does not claim the quotient-locator
construction itself as new.

## Scope

- The certificate is a proof-composition / arithmetic audit packet.
- It depends on imported heavy-fiber and CS25 collision statements.
- It is not a standalone proof of the full positive MCA conjecture.
- It is not a replacement for the existing Paper D proof; it is a candidate
  explicit-line companion to the nonconstructive `cor:Fvalued` discussion.

## Reproducibility

This PR does not rely on a private external repository.  The JSON file is a
frozen certificate payload with all numerical inputs and computed claims needed
for review.  If this packet is promoted later, the next step is to add a
standalone verifier script under `experimental/` or `scripts/`.
