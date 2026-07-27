# E1 first-band variance route boundary v1

**Status:** PROVED ROUTE CUT / TOOL-RELATIVE / NO VARIANCE LEVEL DECIDED /
FIRST-BAND TARGET OPEN.

This packet is a **route cut**. It states, exactly and with a rigorous
rational certificate, where the cubic-Hermite norm majorant used against
`e_1` first-band collisions stops being able to exclude anything. It decides
no variance level, closes no profile, and is not a counterexample to any
exclusion already in the tree.

It attaches to `experimental/notes/roadmaps/e1_collision_norm_criterion.md`.
That note supplies the gate — a genuine collision needs a row prime dividing
an explicit bounded nonzero norm — but not a method for discharging candidates
against it. One natural method is a moment majorant: bound the third moment
`M_3` of the autocorrelation and show the resulting norm falls below `2^250`.
This packet says how far that method reaches.

## Setup

Work in the `N=256` band with folded profile `(3,4,0)`: three coefficients of
magnitude two and four of magnitude one, so the square mass is

```text
m_1 = 3*2^2 + 4*1^2 = 16.
```

Let `V` be the autocorrelation variance (`V = 2E`, `E = sum_d A_d^2` over the
positive-half negacyclic autocorrelation) and let `M_3` be the third-moment
parameter of the majorant. The cubic-Hermite certificate evaluates a fixed
rational Hermite basis `h_0, h_1, h_2, h_3` — **the same basis at every
variance level** — against the three moments

```text
m_1 = 16,      m_2 = 256 + V,      m_3 = 4096 + 48 V + M_3,
```

producing a log-form tested against `250 log 2` in the shape

```text
margin(V, M_3) = c(V,M_3) log 2 + a(V,M_3) log(8/7) + b(V,M_3) log(64/57) - d(V,M_3),
```

and a candidate is excluded when `margin > 0`.

## Theorem (route boundary)

1. **Affineness.** `m_2` and `m_3` are affine in `(V, M_3)` and the Hermite
   basis does not depend on `V`. Hence `a, b, c, d` are affine in `(V, M_3)`,
   and so is `margin`.
2. **Monotonicity.** `d margin / d M_3 < 0` exactly. The exclusion boundary
   `M_3^*(V) = max { M_3 : margin(V, M_3) > 0 }` is therefore well defined,
   and by (1) it is an **affine function of `V`**.
3. **Slope.** `d M_3^* / d V` lies strictly inside `(107, 108)`. The three
   published thresholds are consequently collinear by structure, not by
   coincidence:

   ```text
   V = 68 -> M_3^* = 1947      V = 66 -> M_3^* = 1732      V = 64 -> M_3^* = 1517
   ```

   Each is pinned **two-sided** by the verifier: positive margin at `M_3^*`,
   negative margin at `M_3^* + 1`.
4. **The cut.** The boundary crosses zero near `V = 49.9`. Concretely:

   ```text
   V = 50:  margin(50, 0) > 0,  threshold M_3^* = 13   (still alive)
   V <= 48: margin(V, 0)  < 0   for every even V in 2..48
   ```

   So for every even `V <= 48` the certificate fails already at `M_3 = 0`, and
   therefore excludes no chamber whose third-moment maximum is nonnegative.
   The cut is sharp at even-level granularity: `V = 50` works, `V = 48` does
   not.

All of (1)–(4) are verified in exact rational arithmetic with rigorous
Taylor-remainder bounds on the three logarithms. There is no floating point in
the verifier, and two mutation controls (perturbing the Hermite basis;
perturbing the moment structure) confirm the reproduction in (3) has content.

## Why this matters, stated without inflation

The method reaches the top of the first band and stops well above the bottom.
For orientation — and this is context, not a claim of this packet — the
majorant has been used to clear the levels `V = 68` and `V = 66` in our tree,
with observed chamber maxima running `1188`–`1770` against thresholds `1947`
and `1732`, i.e. margins of 5–39%. Continuing to `V = 52` would require
chamber maxima below `228`, and below `V = 50` no positive threshold exists at
all.

Two further orientation points:

- The residual range after the top of the band is `0 < V <= 64` even, so **32
  levels remain** for this profile alone, before profile `(4,2,0)` or the
  later swap bands are touched.
- `e1_n256_proper_conductor_collision_exclusion` records a **certified
  full-conductor `(3,4,0)` vector at variance 36**. At `V = 36` this majorant
  is dead by (4), and the conductor reduction does not apply to a
  full-conductor vector. That exhibit is *not* a counterexample to anything;
  it is a witness that these two tools together stop short of the bottom of
  the band.

**The escape hatch.** Not every exclusion needs the majorant. In our tree the
profile `(0,8)` at `V = 64` is excluded by an exhaustive census that retains
**zero** vectors — a geometric/parity emptiness, independent of any threshold.
Arguments of that shape are not bound by this route cut. If the first band is
to be cleared below `V ~ 50`, it will have to be on emptiness grounds rather
than norm-majorant grounds.

## Non-claims

- No variance level is decided by this packet.
- No claim that the `V = 68` / `V = 66` closures are reproduced here; they are
  cited as the source of the three certified thresholds only. Their census
  chain (19 nodes, ~5.9e9 census vectors, two independent engines per census)
  is **available on request** and is deliberately not exported: its terminal
  is still open.
- No claim about profile `(4,2,0)`, about the later swap bands, or about any
  `N != 256`.
- No claim that the cubic-Hermite majorant is the only or the best route —
  only that *this* majorant, with *this* moment structure, expires where
  stated.
- The `V = 36` exhibit is a full-conductor vector, not a certified collision.

## Falsifier

Any of the following refutes this packet: a variance level `V <= 48` at which
the same cubic-Hermite certificate excludes a chamber with nonnegative
third-moment maximum; a published first-band threshold inconsistent with an
affine `M_3^*(V)` of slope in `(107, 108)`; a disagreement between the
two-sided pin and any of the three certified thresholds; or a demonstration
that the tested form is not affine in `(V, M_3)`.

## Provenance

Derived 2026-07-27 during an audit of the E1 variance descent. The Hermite
basis and the four log-2 coefficients carried in the verifier are transcribed
from the exact rational certificates that produced the three published
thresholds; they are inputs to this audit, not outputs of it.

- Verifier: `experimental/scripts/verify_e1_first_band_variance_route_boundary_v1.py`
- Certificate: `experimental/data/certificates/e1-first-band-variance-route-boundary-v1/e1_first_band_variance_route_boundary_v1.json`
