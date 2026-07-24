# M31 rank-seven shallow master-denominator cut certificate

This packet proves an exact master-denominator normalization, a rank loss on
every proper fixed-`G` slice, and a reciprocal-convex refinement of the
codimension-one endpoint dual.

Its exact consequences are:

```text
proper fixed-G slice cap:       9,471,941
pure fixed-G cutoff:            g >= 328,678
new harmonic payment:           354,973 <= g <= 354,998
new rank-seven residual:         72,428 <= g <= 354,972
```

The packet does not sum different fixed-`G` slices, close rank seven, exclude
rank at least eight, or move a Grande Finale v4 ledger atom.

The immediate sealed predecessor payload is:

```text
914ee52fa6c4df6697268ca36d825f01361cad4a6a9d6d1c3f0edd822f379cd8
```

## Replay

From the repository root:

```bash
python3 experimental/scripts/verify_m31_rank7_shallow_master_denominator_cut_v1.py --check
python3 -O experimental/scripts/verify_m31_rank7_shallow_master_denominator_cut_v1.py --check
python3 experimental/scripts/verify_m31_rank7_shallow_master_denominator_cut_v1.py --tamper-selftest
sage experimental/scripts/verify_m31_rank7_shallow_master_denominator_cut_v1.sage
python3 experimental/scripts/verify_m31_rank7_shallow_master_denominator_cut_packet_v1.py
python3 experimental/scripts/verify_m31_rank7_shallow_master_denominator_cut_packet_v1.py --tamper-selftest
```

To regenerate the canonical manifest after an intentional source change:

```bash
python3 experimental/scripts/verify_m31_rank7_shallow_master_denominator_cut_packet_v1.py --write-manifest
```

Then rerun the full packet verifier and its tamper self-test.

## Interpretation

The new fixed-slice theorem is source-bound: `P` is the exact lcm of the
canonical shallow locators, and multiplication by `A0/P` preserves the
zero-anchored codeword rank.  A proper locator slice lies in a proper
divisibility hyperplane of that normalized span.

The new harmonic bound is also uniform: the predecessor dual remains on
profiles with `e>Q`, while convexity of `1/P(z)` supplies a stronger dual on
the endpoint profiles with `e<=Q`.

The terminal after this packet is the aggregate mixed-`G` split-divisor,
fixed-syndrome incidence.  Per-slice caps cannot be added without a new
global theorem.
