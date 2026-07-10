import Lake
open Lake DSL

package «syndrome_secant» where

@[default_target]
lean_lib «SyndromeSecant» where
  roots := #[`SyndromeSecant]
