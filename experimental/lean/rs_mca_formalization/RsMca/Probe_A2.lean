import Std

example {α β γ : Type} (f : α → β) (g : β → γ) (l : List α) :
    (l.map f).map g = l.map (fun x => g (f x)) := List.map_map
example (a b : Nat) : ((a * b : Nat) : Int) = (a : Int) * (b : Int) := by push_cast; rfl
example (n : Nat) : ((3^n : Nat) : Int) = (3:Int)^n := by push_cast; rfl
-- the key inductive cast step shape
example (e o : Nat) : ((e + 2*o : Nat) : Int) = (e:Int) + 2*(o:Int) := by omega
example (e o : Nat) : ((2*e + o : Nat) : Int) = 2*(e:Int) + (o:Int) := by omega
-- filter / mem lemmas maybe needed
example (n : Nat) : (List.range n).length = n := List.length_range
