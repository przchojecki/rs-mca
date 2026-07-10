import Lake
open Lake DSL

package «moving_root_toy» where
  -- Core-only Lean 4 package: no mathlib (W38 bar = w6/w24/w37).

@[default_target]
lean_lib «MovingRootToy» where
  roots := #[`MovingRootToy]
