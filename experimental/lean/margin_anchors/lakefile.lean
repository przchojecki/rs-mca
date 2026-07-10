import Lake
open Lake DSL

package «margin_anchors» where
  -- Core-only / stdlib Lean 4 package: no mathlib pin (W24 fallback bar = w6 propext-only style).

@[default_target]
lean_lib «MarginAnchors» where
  roots := #[`MarginAnchors]
