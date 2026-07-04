# A1: staircase cap assembly packet

- **DAG node:** `deep_link_staircase`.
- **Task:** A1.
- **Status:** CONDITIONAL-ASSEMBLED.  The fixed-subcore rich-line residue is
  closed after the unified strip; the full deep-link staircase still needs the
  lower-overlap / occupied-subcore accounting step named below.
- **Verifier:** `experimental/scripts/verify_a1_staircase_cap_assembly.py`.
- **Certificate:**
  `experimental/data/certificates/a1-staircase-cap-assembly/a1_staircase_cap_assembly.json`.

## Assembly

The three integrated inputs are:

```text
P1: fixed-(k-1)-subcore reduction
F3: affine-net absorption by mixed b=2 degree-1 pullbacks
E33: toy constants for the near-k link population
```

P1 proves that partners through a fixed `(k-1)`-subcore `R subset T0` are
exactly `(t+1)`-rich points in the affine parameter plane `(z,a)`.  Each
off-core point contributes one affine branch

```text
a = alpha_x + beta_x z.
```

A partner through `R` is therefore a rich point incident to at least `t+1`
branches.

F3 proves the missing charge for the P3 obstruction.  If a rich point is
multi-directional, choose a pivot branch `L_0`; for every other incident
branch `L_i`, the equality

```text
L_i(z) - L_0(z) = 0
```

is a nonzero degree-1 fiber condition.  The incident block is covered by the
spanning tree of mixed `b=2` pair cells.  Hence every multi-direction affine
net rich point is paid by the unified pullback strip.  The single-direction
case is tangent/pencil bookkeeping.

Therefore the P1 fixed-subcore rich-line residue is removed by the unified
strip.

## Constants

The replayed constants are:

```text
P1 pre-strip fixture: rich parameters 65 > n=46
F3 charged rich points: 342
F3 mixed b=2 pair trades: 726
E33 max partner events through one subcore: 5
E33 max partner events per anchor: 72 = 4.5n
```

These are the constants the final staircase proof should use for calibration;
they are not, by themselves, a general occupied-subcore theorem.

## Remaining Gap

The full deep-link staircase still requires the accounting step already
separated in P1:

```text
a1_lower_overlap_occupied_subcore_accounting
```

Statement: every post-strip near-k partner in the full overlap range
`k/2 < |T cap T0| < k`, including lower-overlap bands such as `k-2`, must be
assigned to `O(n)` occupied deep-subcore witnesses to which the fixed-subcore
cap applies.

Once this accounting is supplied, P1's conditional count gives the linear
staircase bound:

```text
# partners <= C * B * n,
```

where `C` is the fixed-subcore residual cap and `B*n` is the occupied-subcore
witness count.

## Interpretation

A1 closes the rich-line chapter at the fixed-subcore model level: the P3
affine-net obstruction is paid by F3.  It does not honestly flip
`deep_link_staircase` to `PROVED`, because the lower-overlap / occupied-subcore
accounting is not proved in the integrated packets.

## Verification

Run:

```bash
python3 experimental/scripts/verify_a1_staircase_cap_assembly.py
```

The verifier replays:

```bash
python3 experimental/scripts/verify_p1_deep_link_staircase_conditional.py
python3 experimental/scripts/verify_f3_net_absorption.py
python3 experimental/scripts/verify_e33_deep_link_staircase.py
```
