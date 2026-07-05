# Deep-Point Identity Packet

- **Status:** PROVED / identity bridge.
- **DAG node:** `deep_point`.
- **Certificate:** `experimental/data/certificates/deep-point/deep_point.json`.
- **Verifier:** `python3 experimental/scripts/verify_deep_point_packet.py --check experimental/data/certificates/deep-point/deep_point.json`.

This packet names the deep-point identity consumed by the L2 `codegree` packet.
It packages the identity boundary from
`experimental/notes/x1/x1_deep_point_interleaved_bridge.md`.

## Claim

For the simple-pole line at a deep point `alpha notin D`,

```text
f_alpha(x) = U(x)/(x-alpha),
g_alpha(x) = -1/(x-alpha),
```

the bad-slope set equals the deep-point image of the one-degree-higher list:

```text
Bad_CA(f_alpha,g_alpha; delta_a)
  = Bad_MCA(f_alpha,g_alpha; delta_a)
  = { P(alpha) : deg(P) < k+1 and P agrees with U on >= a points }.
```

The interleaved form is the row-wise vector identity

```text
BadVec(alpha; a)
  = { (P_1(alpha),...,P_mu(alpha)) :
      deg(P_i) < k+1 and all P_i agree with U_i on a common >=a support }.
```

This is the forward list-to-bad-slope bridge used by the list/L2 ledger.

## Evidence

The existing upstream verifiers replay independent finite checks:

```text
experimental/scripts/verify_x1_deep_point_identity.py
experimental/scripts/verify_x1_interleaved_deep_point.py
```

The packet certificate records the formulas and keeps the evidence boundary
separate from deployed-row threshold claims.

## DAG Consequence

`deep_point` is the parent node for `codegree`. The codegree reduction uses the
deep-point bridge to keep the interleaved list object and bad-slope object in
the same support/column-distance convention.

## Non-Claims

- This packet does not prove `list_safe`.
- This packet does not prove a deployed adjacent upper certificate.
- This packet does not prove a full list-to-MCA equivalence outside the
  simple-pole/deep-point bridge.
- This packet does not edit Papers A-D.
