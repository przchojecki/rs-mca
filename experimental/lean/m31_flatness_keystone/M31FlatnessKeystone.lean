import M31FlatnessKeystone.SelectorAtlas

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

/-!
# M31 flatness keystone

The public module re-exports the exact selector atlas and kernel-checks the
max-versus-average integer thresholds used in the packet note.
-/

namespace M31FlatnessKeystone

open SelectorAtlas

def Q32 : Nat := fieldPrime ^ 32

def supportCount : Nat := fastBinomial 1022 479

theorem packet_selector_atlas :
    atlasSummary = expectedAtlasSummary :=
  selector_relation_atlas_exact

theorem quotient_average_exact :
    supportCount / Q32 = 3614119 ∧
    (supportCount + Q32 - 1) / Q32 = 3614120 := by
  native_decide

theorem keystone_threshold_arithmetic :
    3432 * 1053 = 3613896 ∧
    3614120 - 3432 * 1053 = 224 ∧
    3432 * 1054 = 3617328 ∧
    3432 * 4888 = 16775616 ∧
    16777215 - 3432 * 4888 = 1599 ∧
    3432 * 4889 = 16779048 ∧
    3432 * 4889 - 16777215 = 1833 ∧
    3432 + 8 = 3440 ∧
    (3440 + 3432 - 1) / 3432 = 2 := by
  decide

#print axioms packet_selector_atlas
#print axioms quotient_average_exact
#print axioms keystone_threshold_arithmetic

end M31FlatnessKeystone
