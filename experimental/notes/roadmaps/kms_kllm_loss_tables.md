# E20 KMS/KLLM Loss-Exponent Tables

- **Status:** AUDIT / STATEMENT ARITHMETIC.
- **Agent:** Codex acting autonomously for Allen Graham Hart.
- **Roadmap link:** E20 / `QX.10` (`xr_kms_parameter_matching`).
- **Verifier:** `experimental/scripts/verify_kms_kllm_loss_tables.py`.
- **Artifact:** `experimental/data/certificates/kms-kllm-loss-tables/kms_kllm_loss_tables.json`.

This packet performs the E20 source-extraction arithmetic.  It does not prove
an import theorem.  It records which published small-set engines emit a
finite `q`-power loss at the first-moment scale

```text
mu ~= q^(1-t),
```

where `t=A-k` is the FM1 split-locator slack convention.

## Source Extraction

| source | extracted quantitative content | direct FM-scale verdict |
| --- | --- | --- |
| Khot-Minzer-Moshkovitz-Safra, *Small-Set Expansion in the Johnson Graph*, Theory of Computing 2025, Theorem 1.3 | For fixed `alpha, eta`, sufficiently pseudorandom Johnson sets have expansion `>1-eta`; non-expansion implies correlation with a bounded-width intersection of dictators. | **No direct `q`-power import.** The theorem is the right structural tangent/junta statement, but its public form is qualitative/asymptotic for E20 purposes. |
| Dinur-Khot-Kindler-Minzer-Safra, *On non-optimally expanding sets in Grassmann graphs*, Israel J. Math. 2021 | Expansion below the constant threshold `7/8` forces non-pseudorandomness. | **No direct `q`-power import.** The threshold is constant-scale, too coarse for `mu=q^(1-t)` accounting. |
| Khot-Minzer-Safra, *Pseudorandom sets in Grassmann graph have near-perfect expansion*, Annals 2023 | Pseudorandom Grassmann sets have expansion `1-o(1)`. | **No direct finite exponent as stated.** It is the qualitative endpoint, but E20 still needs explicit finite margins before paying FM ledgers. |
| Keevash-Lifshitz-Long-Minzer, *Hypercontractivity for global functions and sharp thresholds*, JAMS 2024 / arXiv:2103.04604 | If generalized influences are `beta`-small, the highlighted `(4,2)` statement gives `||T_{1/5} f||_4 <= beta^(1/4)||f||_2`. | **Conditional carry.** A `beta<=q^(-g)` globalness certificate gives an explicit `q`-power loss. |

The decision is therefore not "KMS imports the XR wall."  The honest statement
is narrower:

```text
raw KMS/DKKMS as stated:  fails as a finite q-power FM engine
KLLM route:               survives if QX.11 proves q-power globalness
```

## KLLM Arithmetic

Let `f=1_A`, with

```text
mu = E f = q^(-(t-1)).
```

Assume the KLLM generalized-influence/globalness hypothesis holds with

```text
beta <= q^(-g).
```

The extracted KLLM loss gives

```text
||T f||_4 <= q^(-g/4) ||f||_2
           = q^(-g/4) mu^(1/2).
```

By Holder,

```text
E[f T f] <= ||f||_{4/3} ||T f||_4
          <= mu^(3/4) q^(-g/4) mu^(1/2)
          = q^(-g/4) mu^(5/4).
```

Thus the conditional probability that a KLLM-noise step remains inside `A` is

```text
E[f T f] / mu <= q^(-(g+t-1)/4).
```

So the E20 exponent formula is:

```text
KLLM internal-stay exponent = (g+t-1)/4.
```

To match the full FM stay exponent `t-1`, the globalness certificate must give

```text
g >= 3(t-1).
```

## Tables

With no extra globalness exponent beyond applicability (`g=0`):

| slack `t` | FM measure | KLLM stay exponent | `g` needed to match full FM stay exponent |
| ---: | ---: | ---: | ---: |
| 2 | `q^-1` | `1/4` | 3 |
| 3 | `q^-2` | `1/2` | 6 |
| 4 | `q^-3` | `3/4` | 9 |
| 5 | `q^-4` | `1` | 12 |
| 6 | `q^-5` | `5/4` | 15 |
| 8 | `q^-7` | `7/4` | 21 |

The extracted theorem exponents are rate-independent for

```text
rho in {1/2, 1/4, 1/8, 1/16}.
```

Rate enters later through which FM slack rows and paid tangent/globalness
ledgers the XR assembly has to certify, not through the KMS/KLLM loss formula
itself.

## Interpretation

E20's verdict is the middle branch:

```text
KLLM survives conditionally; raw KMS/DKKMS do not directly survive FM scale.
```

This makes the next obligation precise.  `QX.11` must turn the paid tangent
ledger into a generalized-influence/globalness exponent `g` for the actual
post-strip alignment sets.  Then `QX.14` can compare `(g+t-1)/4` against the
rate/slack row being assembled.  If `QX.11` cannot produce any positive
`q`-power globalness margin, the XR wall needs a strengthened small-set theorem
or a new paid leakage ledger.

Non-claims:

- no KMS/DKKMS/KLLM import proof;
- no verification that RS alignment sets satisfy KLLM globalness;
- no final XR wall arithmetic;
- no hidden-constant extraction from the primary papers.

## Primary Sources

- <https://theoryofcomputing.org/articles/v021a002/>
- <https://doi.org/10.1007/s11856-021-2164-7>
- <https://doi.org/10.4007/annals.2023.198.1.1>
- <https://doi.org/10.1090/jams/1027>
- <https://arxiv.org/abs/2103.04604>

## Replay

```bash
python3 experimental/scripts/verify_kms_kllm_loss_tables.py
python3 experimental/scripts/verify_kms_kllm_loss_tables.py --emit
python3 experimental/scripts/verify_kms_kllm_loss_tables.py --check experimental/data/certificates/kms-kllm-loss-tables/kms_kllm_loss_tables.json
python3 -m py_compile experimental/scripts/verify_kms_kllm_loss_tables.py
```
