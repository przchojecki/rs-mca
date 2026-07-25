import Lake
open Lake DSL

package m31FlatnessConjectureC1 where

require asymptoticSpine from "../asymptotic_spine"
require m31QRootedShell from "../m31_q_rooted_shell"
require m31FlatnessKeystone from "../m31_flatness_keystone"
require m31QuotientBandMixing from "../m31_quotient_band_mixing"
require m31QuotientT16MixingFloor from "../m31_quotient_t16_mixing_floor"

@[default_target]
lean_lib M31FlatnessConjectureC1 where
  roots := #[`M31FlatnessConjectureC1]
