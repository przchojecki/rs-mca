# XR Stripped Inverse Candidate Scan

- **Status:** EXPERIMENTAL / candidate-family evidence.
- **Agent:** Codex acting autonomously for Allen Graham Hart.
- **Roadmap link:** E11 / E2b (`xr_inverse_toy`).
- **Verifier:** `experimental/scripts/verify_xr_stripped_inverse_candidates.py`.
- **Artifact:** `experimental/data/certificates/xr-stripped-inverse-candidates/xr_stripped_inverse_candidates.json`.

This packet is a scoped version of the stripped XR inverse falsifier.  It does
not enumerate actual Reed-Solomon word pairs, and it does not prove the XR
inverse theorem.  It tests the part of the E11 prediction that can be checked
cleanly in the Johnson-support model: after paid quotient-profile cells are
removed, the largest `E_3` examples in the natural candidate dictionary should
be fixed-root/fixed-hole first-eigenspace structures.

## Energy

On the Johnson graph `J(n,j)`, write

```text
E_3^J(A) = Pr[T_0,T_1,T_2,T_3 all lie in A],
```

where each step is one random exchange.  The verifier uses exact rational
formulas for three candidate families:

```text
fixed_core(c)       {T : C subset T, |C|=c}
fixed_hole(c)       {T : T cap C = empty, |C|=c}
quotient_profile    one labelled block-profile cell for a proper divisor block partition
```

The quotient-profile cells are marked as paid and stripped before interpreting
the inverse theorem.  The fixed-hole family is not asserted to be a paid MCA
ledger; it is recorded because it is the complementary first-eigenspace support
structure and ties fixed-core at half size.

## Results

For `J(16,8)`, the raw top list begins:

```text
fixed_core(1)          E_3 = 343/1024
fixed_hole(1)          E_3 = 343/1024
fixed_core(2)          E_3 = 63/640
fixed_hole(2)          E_3 = 63/640
quotient m=8 (4,4)     E_3 = 245/5148
```

After stripping quotient-profile cells, the top candidates are only
fixed-core or fixed-hole families.  The residual max-degree shadow gives the
comparison cap

```text
E_3 <= 1/512
```

for a density-one family whose induced residual one-exchange degree is at most
`j`.

For `J(32,16)`, the raw top list begins:

```text
fixed_core(1)           E_3 = 3375/8192
fixed_hole(1)           E_3 = 3375/8192
fixed_core(2)           E_3 = 5145/31744
fixed_hole(2)           E_3 = 5145/31744
fixed_core(3)           E_3 = 15379/253952
fixed_hole(3)           E_3 = 15379/253952
quotient m=16 (8,8)     E_3 = 920205/26714684
```

Again, after quotient stripping the top candidates are fixed-core/fixed-hole
only.  The corresponding residual degree cap is

```text
E_3 <= 1/4096.
```

## Interpretation

This moves the E11 prior in the positive direction, but only inside the tested
candidate dictionary.  It supports the intended order of operations:

```text
1. strip paid quotient-profile cells;
2. treat the remaining top exchange-energy examples as first-eigenspace
   tangent-side structures;
3. run the full actual A_{u,v} pair-orbit scanner before claiming an XR
   inverse theorem.
```

The packet also explains why stripping matters: quotient-profile cells do
appear in the raw high-`E_3` list, so interpreting raw exchange energy without
the quotient ledger would mix paid quotient structure into the inverse target.

Non-claims:

- no proof of `xr_inverse`;
- no exhaustive enumeration of arbitrary Johnson families;
- no enumeration of actual Reed-Solomon word-pair orbits;
- no claim that fixed-hole support structure is already a paid MCA ledger.

## Replay

```bash
python3 experimental/scripts/verify_xr_stripped_inverse_candidates.py
python3 experimental/scripts/verify_xr_stripped_inverse_candidates.py --emit
python3 experimental/scripts/verify_xr_stripped_inverse_candidates.py --check experimental/data/certificates/xr-stripped-inverse-candidates/xr_stripped_inverse_candidates.json
python3 -m py_compile experimental/scripts/verify_xr_stripped_inverse_candidates.py
```
