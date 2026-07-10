import Lake
open Lake DSL

package «single_circuit_ray» where
  -- Core-only Lean 4 package: no mathlib (W39 bar = w6/w24/w37/w38).

@[default_target]
lean_lib «SingleCircuitRay» where
  roots := #[`SingleCircuitRay]
