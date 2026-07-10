import Lake
open Lake DSL

package «petal_fiber» where

@[default_target]
lean_lib «PetalFiber» where
  roots := #[`PetalFiber]
