import Lake
open Lake DSL

package m31T16RaggedWitness where

require m31QuotientT16MixingFloor from "../m31_quotient_t16_mixing_floor"

@[default_target]
lean_lib M31T16RaggedWitness where
  roots := #[`M31T16RaggedWitness]
