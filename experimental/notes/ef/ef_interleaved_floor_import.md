# EF Interleaved Floor Import

## Status

PROVED under the stated multiplication-slice hypotheses. This note vendors the
`interleaved_floor_import` seam from the smooth-RS prize DAG into the upstream
extension-fiber/F1 terminology.

It does not classify arbitrary extension-valued received pairs. It says that
once a genuinely full-field EF component has already been reduced to the
`e`-interleaved base-list multiplication-slice form, the existing extension-pole
floor applies and there is no additional S9 ledger class at this seam.

Replay:

```bash
python3 experimental/scripts/verify_ef_interleaved_floor_import.py
```

## Setup

Let `B <= E` be a finite extension, let `D subset B`, and fix a `B`-basis of
`E`. Write

```text
Phi : E^D -> (B^D)^e
```

for coordinate expansion, where `e=[E:B]`. For `z in E`, let `M_z` be the
`B`-linear multiplication-by-`z` matrix in this basis.

The EF reduction upstream already uses the following shape: a genuinely
full-field, non-tower, non-base-descended component is represented, on its
generic point, by an `E`-valued line

```text
f + z g
```

whose `B`-coordinate expansion is the coupled interleaved base equation

```text
Phi(f) + M_z Phi(g).
```

The load-bearing hypothesis of this note is that the component is in this
multiplication-slice essential image. That hypothesis is exactly the output of
the local prize node `ef_fvalued_word_source_is_interleaved_witness`.

## Interleaved Witness Lemma

Because `D subset B`, syndrome formation and polynomial restriction commute
with `B`-basis expansion:

```text
Syn_E(sum_i y_i omega_i) = sum_i Syn_B(y_i) omega_i.
```

Multiplication by `z` in `E` is `B`-linear, hence represented by `M_z`.
Therefore an `E`-linear equation for `f + z g` is equivalent, after `Phi`, to
an `e`-row interleaved `B`-linear equation with rows coupled by `M_z`.
Noncontainment is preserved because an `E`-vector is zero if and only if all its
`B`-coordinates are zero.

This proves that an `F`-valued word source in the multiplication-slice image is
not an ordinary base-list witness; it is an interleaved base-list witness with a
common support and the `M_z` coupling.

## Singleton Floor Import

Let `K` be an extension field containing `B`, let `C_K=RS[K,D,kappa]`, and let
`alpha in K \ B`. Suppose a singleton multiplication-slice witness comes from
`P in K[X]_{< kappa+1}` and `U:D -> K`, agreeing on a support `S` with
`|S|>kappa`:

```text
P(x) = U(x)       for x in S.
```

Define

```text
f_alpha(x) = U(x)/(x-alpha),
g_alpha(x) = -1/(x-alpha),
z = P(alpha).
```

Then on `S`,

```text
f_alpha(x) + z g_alpha(x)
  = (P(x)-P(alpha))/(x-alpha)
  = Q_alpha(x),
```

where `deg Q_alpha < kappa`. Thus the line is explained by `C_K` on `S`.

The second coordinate is not separately explained on any support of size
`>kappa`. If a polynomial `G` of degree `<kappa` agreed with `g_alpha` on such
a support, then

```text
H(X) = (X-alpha)G(X) + 1
```

would have degree at most `kappa`, more than `kappa` roots, and hence be
identically zero. But `H(alpha)=1`, contradiction.

So the singleton interleaved multiplication-slice witness meets the
extension-pole divisor. The Paper D extension-pole/list-window floor applies
with effective list size `L_eff=1`, and

```text
N(1) = ceil((|K|-|B|)/(|K|-|B|+kappa)) = 1
```

whenever `|K|>|B|`.

## Consequence For EF/F1

Under the previously proved EF reductions:

1. full Galois orbits descend to `B`-defined pole-free cycles;
2. nontrivial stabilizers are tower-confined;
3. trivial-stabilizer full-field components reduce to either the pole mechanism
   or an `F`-valued word source; and
4. the `F`-valued word source lies in the multiplication-slice interleaved
   essential image;

this note closes the last seam: the interleaved source is already caught by the
extension-pole floor. Therefore it does not create a new S9 ledger class.

Equivalently, the proof route is:

```text
F-valued word source
  -> multiplication-slice interleaved witness
  -> singleton extension-pole floor
  -> no pole-free full-field escape at this seam.
```

## Nonclaims

- This note does not prove that every extension-valued pair is in the
  multiplication-slice essential image.
- It does not replace the EF descent and stabilizer lemmas.
- It does not promote a new finite-prize threshold row.
- It does not change Papers A-D; it records an experimental theorem-chain
  import and a replayable toy check.
