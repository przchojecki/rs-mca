import Lake
open Lake DSL

package lRootliftBridge where

@[default_target]
lean_lib LRootliftBridge where
  roots := #[`LRootliftBridge]
