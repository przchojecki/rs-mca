import Lake
open Lake DSL

package «syndrome_line» where

@[default_target]
lean_lib «SyndromeLine» where
  roots := #[`SyndromeLine]
