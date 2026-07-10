import Lake
open Lake DSL

package «integer_staircase» where

@[default_target]
lean_lib «IntegerStaircase» where
  roots := #[`IntegerStaircase]
