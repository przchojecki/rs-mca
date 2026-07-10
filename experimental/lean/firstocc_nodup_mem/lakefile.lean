import Lake
open Lake DSL

package «firstocc_nodup_mem» where

@[default_target]
lean_lib «FirstOccNodupMem» where
  roots := #[`FirstOccNodupMem]
