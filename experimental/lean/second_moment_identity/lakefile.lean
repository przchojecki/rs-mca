import Lake
open Lake DSL

package «second_moment_identity» where

@[default_target]
lean_lib «SecondMomentIdentity» where
  roots := #[`SecondMomentIdentity]
