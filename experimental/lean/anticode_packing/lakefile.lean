import Lake
open Lake DSL

package «anticode_packing» where
  -- Core-only Lean 4 package: no mathlib (W39 bar = w6/w24/w37/w38).

@[default_target]
lean_lib «AnticodePacking» where
  roots := #[`AnticodePacking]
