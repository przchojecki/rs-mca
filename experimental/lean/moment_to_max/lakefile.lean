import Lake
open Lake DSL

package «moment_to_max» where

@[default_target]
lean_lib «MomentToMax» where
  roots := #[`MomentToMax]
