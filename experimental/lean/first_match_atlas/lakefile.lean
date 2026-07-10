import Lake
open Lake DSL

package «first_match_atlas» where

@[default_target]
lean_lib «FirstMatchAtlas» where
  roots := #[`FirstMatchAtlas]
