import Lake
open Lake DSL

package «saturation_identity» where

@[default_target]
lean_lib «SaturationIdentity» where
  roots := #[`SaturationIdentity]
