# Statement-source correspondence

The package is a stdlib-only formal shadow of
`experimental/notes/thresholds/m31_flatness_conjecture_a1_s3.md`.

| Source claim | Lean declaration |
|---|---|
| One restored puncture yields a direct depth-32 packet longer than the scalar cap | `M31FlatnessConjectureA1S3.single_puncture_boundary_packet_exact` |
| The one-puncture relaxation of the uniform shell cap is false | `M31FlatnessConjectureA1S3.single_puncture_uniform_cap_refuted` |
| The exact pinned domain yields a direct depth-31 packet longer than the scalar cap, with a certified coefficient-32 break | `M31FlatnessConjectureA1S3.depth31_boundary_packet_exact` |
| The depth-31 relaxation is false | `M31FlatnessConjectureA1S3.depth31_uniform_cap_refuted` |
| Pooling the exact deficiencies 64, 128, and 192 gives a direct 1,723-neighbor packet | `M31FlatnessConjectureA1S3.aggregate_shell_packet_exact` |
| The aggregate-band replacement for the pointwise shell cap is false | `M31FlatnessConjectureA1S3.aggregate_uniform_cap_refuted` |
| Removing duplicate-freeness from the list interface permits repetition inflation | `M31FlatnessConjectureA1S3.duplicate_guard_boundary_exact` |
| Exact family and threshold arithmetic | `M31FlatnessConjectureA1S3.boundary_family_arithmetic` |

Every declaration is followed by `#print axioms`. The closed support packets and
arithmetic use `native_decide`; the three logical refutations use only the
proved packet equalities and elementary natural-number contradiction. No custom
axiom, `sorry`, `admit`, unsafe declaration, Mathlib import, or Python artifact is
part of this package.

The direct prefix checker is
`M31QuotientT16MixingFloor.Witness.locatorPrefix`. It performs truncated
multiplication by every one of the 479 linear factors; compressed T32 and T64
parameter equations are used only to design the packets, never as their final
verification layer.
