import Lake
open Lake DSL

package «first_match_partition» where
  -- Core-only Lean 4 package: no mathlib (W37 bar = w6/w24).

@[default_target]
lean_lib «FirstMatchPartition» where
  roots := #[`FirstMatchPartition]
