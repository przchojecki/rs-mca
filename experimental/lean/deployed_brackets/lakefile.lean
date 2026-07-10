import Lake
open Lake DSL

package «deployed_brackets» where
  -- Core-only Lean 4 package: no mathlib (W37 bar = w6/w24).

@[default_target]
lean_lib «DeployedBrackets» where
  roots := #[`DeployedBrackets]
