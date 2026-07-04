import Lake
open Lake DSL

package l1ThresholdLedger where

@[default_target]
lean_lib L1Threshold where
  roots := #[`L1Threshold]
