# Generator-Economy Design Search

- **Status:** EXPERIMENTAL / evidence packet.
- **Agent:** Codex acting autonomously for Allen Graham Hart.
- **Roadmap link:** E12 / QA.15 (`generator_economy`).
- **Verifier:** `experimental/scripts/verify_generator_economy_design_search.py`.
- **Artifact:** `experimental/data/certificates/generator-economy-design-search/generator_economy_design_search.json`.

This packet is a conservative toy search for the Row-C far-pair
generator-economy problem.  It does not prove or disprove the existence of
large generator-economy designs.  Its role is to test the easiest lift of the
root-difference germ and to measure whether plain cyclic-orbit constructions
grow family size faster than the number of generator templates.

## Object

Work in the quotient exponent group `Z/NZ`.  An `ell`-sum center is represented
by an `ell`-subset `S`.  A pair difference is the cyclotomic coefficient vector

```text
1_S - 1_T in Z[zeta_N].
```

Two differences use the same template generator if they differ by a cyclotomic
unit and sign:

```text
1_S - 1_T  ~  +/- zeta^a (1_U - 1_V).
```

The verifier counts these unit/sign templates.  One template corresponds to
one norm check in the most conservative generator-economy baseline.  No
multiplicative semigroup compression between templates is attempted here.

This keeps the circularity guard clean: the search uses only explicit subset
centers and pair differences, not fiber counts.

## Results

The singleton root-difference germ is reproduced exactly:

```text
N=16:  orbit size 16, template generators 8
N=32:  orbit size 32, template generators 16
```

For `N=16`, the verifier enumerates all cyclic-orbit representatives.  Greedy
unions of such orbits give:

```text
N=16, ell=8
budget g    family size    generators used
8           16             8
16          24             16
32          34             30
64          52             62
128         80             125
256         130            249

N=16, ell=9
budget g    family size    generators used
8           16             8
16          16             8
32          32             29
64          48             62
128         64             104
256         96             220
```

For `N=32`, the verifier uses a deterministic sample of `512` cyclic-orbit
representatives:

```text
N=32, ell=16
budget g    family size    generators used
8           2              1
16          32             16
32          34             18
64          66             62
128         66             62
256         130            240

N=32, ell=17
budget g    family size    generators used
8           0              0
16          32             16
32          32             16
64          64             64
128         64             64
256         128            256
```

## Interpretation

The cyclic germ does lift: an `ell`-sum cyclic orbit of full size `N` still has
only about `N/2` unit/sign difference templates.  But in these toy searches,
unions of cyclic orbits grow only roughly linearly with the template budget.
This is an early-cap signal for the naive construction.

So the current evidence says:

```text
plain cyclic-orbit unions are not enough;
look next for genuine multiplicative compression of templates,
or import structured abelian difference-set designs.
```

This is still useful progress.  It turns the E12 fork from a vague design hope
into a concrete target: beat the template-linear baseline above without using
fiber-count input.

Non-claims:

- no nonexistence theorem for generator-economy designs;
- no actual Row-C modular value certificate;
- no multiplicative semigroup factorization among templates;
- no exhaustive `N=32` search.

## Replay

```bash
python3 experimental/scripts/verify_generator_economy_design_search.py
python3 experimental/scripts/verify_generator_economy_design_search.py --emit
python3 experimental/scripts/verify_generator_economy_design_search.py --check experimental/data/certificates/generator-economy-design-search/generator_economy_design_search.json
python3 -m py_compile experimental/scripts/verify_generator_economy_design_search.py
```
