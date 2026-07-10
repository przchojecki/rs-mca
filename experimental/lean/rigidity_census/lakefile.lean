import Lake
open Lake DSL

package «rigidity_census» where

@[default_target]
lean_lib «RigidityCensus» where
  roots := #[`RigidityCensus]
