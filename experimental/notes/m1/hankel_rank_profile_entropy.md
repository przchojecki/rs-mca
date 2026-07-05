# Hankel Rank-Profile Entropy Packet

- **Status:** PROVED / fixed-cutoff entropy bound.
- **DAG node:** `hankel_rank_profile_entropy`.
- **Certificate:** `experimental/data/certificates/hankel-rank-profile-entropy/hankel_rank_profile_entropy.json`.
- **Verifier:** `python3 experimental/scripts/verify_hankel_rank_profile_entropy_packet.py --check experimental/data/certificates/hankel-rank-profile-entropy/hankel_rank_profile_entropy.json`.

This packet packages the rank-profile dichotomy used to bound unpaid primitive
saturated Hankel states. It consumes the support-lattice accounting packet and
the rational-defect separation packet.

## Claim

Fix the sparse cutoff `W`. For a saturated Hankel state
`P = ker(S_{i+c})`, there are three cases.

## Row-Deficient Case

If the Hankel matrix has row deficiency, the corrected binary-apolarity
argument shows that the kernel is a principal GRS segment after the
root-at-infinity strip:

```text
P = q K[X]_{<=D-1},
X^alpha P = qtilde K[X]_{<=D-1}.
```

After this strip, the zero-support matroid is MDS and contributes no unpaid
closure entropy. The working record verifies the corrected torus lemma on
`5086` cases, including `2966` boundary cases.

## Row-Full Wide Case

If

```text
j - t + 3 > 2W,
```

then the rational-defect separation packet forces all weight-`<= W` sparse
atoms to lie in one saturated rational class. Same-class collapse gives a
single atom closure, so `Delta_u <= 1`.

## Row-Full Narrow Case

If

```text
j - t + 3 <= 2W,
```

then

```text
dim P = j + 1 - t <= 2W - 2.
```

Thus the branch has only `O(W)` dimension-dropping levels, each with at most
`n^W` child closures.

## Consequence

Combining these three cases with the support-lattice accounting identity and
the entropy/Kraft budget gives

```text
number of unpaid primitive saturated states <= n^{O(W^2)}
```

for fixed `W`.

## DAG Use

`f_termination_hankel` consumes this packet as the state-count input. The
separate `hankel_moment_clean_leaves` packet supplies the terminal member-count
bound.

## Non-Claims

- This packet requires fixed `W`; it does not give a uniform bound when `W`
  grows with `n`.
- This packet does not supply the terminal moment/member count.
- This packet does not by itself assemble `f_termination_hankel`.
- This packet does not edit Papers A-D.
