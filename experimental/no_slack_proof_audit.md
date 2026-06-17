# Paper A No-Slack Proof Audit

- **Status:** AUDIT
- **Agent/model:** Codex acting autonomously through AllenGrahamHart
- **Date:** 2026-06-17
- **Supports:** `tex/proximity_blueprint_v3.tex` M1 and `agents.md` A1.

## Purpose

Milestone M1 asks for a lemma-by-lemma verification table for Paper A
(`tex/RS_disproof_v3.tex`). This audit maps the no-slack obstruction proof to
the symbolic arguments and finite-computation records that should support it.
It is not a proof authority and does not promote any statement in the paper.

## Local Anchors

The current Paper A labels used by this audit are:

```text
def:mca
thm:main
lem:locator
lem:dsh
lem:monotone
lem:fermat
lem:value-family
lem:granularity
thm:sieve
ex:babybear
ex:257
lem:ext-coset-subgroup
lem:ext-tower-criterion
thm:ext-smooth-towers
prop:ext-density
cor:fermat-proth-towers
ex:goldilocks-density
app:verify
```

## Verification Table

- `def:mca`: support-wise line-MCA definition.
  Evidence needed: definition-alignment check against the survey. Status: open.
- `lem:locator`: quotient locator identity and bad-slope witness.
  Evidence needed: symbolic proof plus end-to-end polynomial check. Status:
  symbolic proof present; finite checks needed for examples.
- `lem:dsh`: restricted-sum coverage via Dias da Silva--Hamidoune.
  Evidence needed: citation plus parameter inequality for every use. Status:
  citation present; per-instance inequality table needed.
- `lem:monotone`: radius monotonicity for MCA/list size.
  Evidence needed: symbolic proof. Status: present locally.
- `lem:fermat`: Fermat digit coverage mechanism.
  Evidence needed: symbolic proof plus exact small-prime coverage records.
  Status: present plus `app:verify` records; commands missing.
- `lem:value-family`: exact-support cyclotomic value family.
  Evidence needed: symbolic proof and enumeration cross-check. Status:
  enumeration command missing.
- `lem:granularity`: granularity step in sieve argument.
  Evidence needed: symbolic proof. Status: present locally.
- `thm:sieve`: inverse-polylogarithmic bad-slope density.
  Evidence needed: symbolic proof plus Siegel--Walfisz input. Status:
  external analytic input named; no finite script needed.
- `thm:main` part (a): error one on deployed-style fields.
  Evidence needed: DSH inequality and divisor checks for each field/rate.
  Status: needs explicit table or script certificate.
- `thm:main` part (b): Fermat-prime density examples.
  Evidence needed: Fermat coverage and special `(17,1/4)` exhaustive record.
  Status: `app:verify` states record; command artifact missing.
- `thm:main` part (c): infinite-prime non-negligible density.
  Evidence needed: `thm:sieve` proof and parameter translation. Status:
  symbolic chain present; audit table needed.
- `thm:main` part (d): worst-case list lower bound.
  Evidence needed: pigeonhole proof and small-field count certificate. Status:
  q=17 certificate should be linked once merged.
- `ex:babybear`: BabyBear and related deployed-field floor.
  Evidence needed: field order, subgroup divisibility, DSH inequality. Status:
  needs reproducible parameter certificate.
- `ex:257`: fully checked Fermat instance.
  Evidence needed: coverage, locator expansion, support agreement. Status:
  `app:verify` states exact checks; command artifact missing.
- `thm:ext-smooth-towers`: extension-tower full-density examples.
  Evidence needed: order criterion and coordinate-wise DSH coverage. Status:
  symbolic proof present; parameter examples need table.
- `prop:ext-density`: box-density extension bound.
  Evidence needed: coordinate-box counting and explicit density lower bound.
  Status: Goldilocks instance needs certificate.
- `ex:goldilocks-density`: Goldilocks density example.
  Evidence needed: exact `m,d,theta` values and final density. Status:
  needs reproducible arithmetic certificate.
- `app:verify`: exact finite computations.
  Evidence needed: script command, seed if any, output hash or JSON. Status:
  records results but not commands.

## Finite Certificates To Attach

The following artifacts would close the machine-verification gap:

1. **Deployed field divisor table.**
   Include BabyBear, KoalaBear, and `3*2^30+1`; for each prize rate print
   `p`, `n`, `N`, `a`, `rho N`, and the DSH inequality value.
2. **Fermat coverage certificate.**
   Recompute restricted-sum coverage for `(M+1)` and `(M/2+1)` subsets of `Q`
   for `p=17,257,65537`, including the unique missing residue.
3. **Locator end-to-end certificate.**
   For `p=257`, expand `prod_{b in A}(X^16-b)` for representative subsets,
   check top coefficients, and verify agreement on the `144`-point support.
4. **q=17 list-pigeonhole certificate.**
   Link the q=17/n=16 exhaustive checker once it lands, or record an exact
   command that reproduces the `672/673` count in `app:verify`.
5. **Sieve-family enumeration.**
   Recompute the `N=16`, `r=9`, `3280` characteristic-zero value count and the
   listed reductions modulo primes.
6. **Extension-tower arithmetic certificate.**
   For Fermat/Proth and Goldilocks examples, print the order criterion,
   field decomposition parameters, and density lower bound.

## Suggested Status Labels

| Paper A object | Suggested status |
| --- | --- |
| `lem:locator`, `lem:monotone`, `lem:granularity` | `PROVED` |
| `lem:dsh` uses | `PROVED`, with external citation |
| `thm:sieve` | `PROVED`, with analytic external input named |
| `app:verify` finite records | `AUDIT` until commands/certificates land |
| Explicit deployed/Fermat/Goldilocks examples | `AUDIT` until reproduced |

## Reproduction Commands For This Audit

```sh
labels='def:mca|thm:main|lem:locator|lem:dsh|lem:monotone'
labels="$labels"'|lem:fermat|lem:value-family|lem:granularity|thm:sieve'
labels="$labels"'|ex:babybear|ex:257|lem:ext-coset-subgroup'
labels="$labels"'|lem:ext-tower-criterion|thm:ext-smooth-towers'
labels="$labels"'|prop:ext-density|cor:fermat-proth-towers'
labels="$labels"'|ex:goldilocks-density|app:verify'
rg -n '\\label\{('"$labels"')\}' tex/RS_disproof_v3.tex
sed -n '517,530p' tex/RS_disproof_v3.tex
sed -n '634,641p' tex/proximity_blueprint_v3.tex
sed -n '306,318p' agents.md
```

## Promotion Rule

Do not edit Paper A's theorem statements from this audit alone. First attach
machine-readable certificates or exact commands for every finite claim listed
above, then promote only the rows whose evidence is reproducible.
