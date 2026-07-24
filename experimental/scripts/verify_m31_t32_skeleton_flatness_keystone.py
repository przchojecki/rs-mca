#!/usr/bin/env python3
"""Deterministic replay for the M31 T32-skeleton flatness keystone."""
from __future__ import annotations
import argparse, copy, hashlib, itertools, json, math, sys
from collections import Counter, defaultdict
from pathlib import Path

P=2**31-1; S2048=pow(2,-2047,P); S32=pow(2,-63,P)
BASE="d968e1cb9a3a6dbcfba35ecf9f448b4a373a35bb"
UPSTREAM="71f64349a8fa8cbf05678a6e9d4e00e8e06d7de5"
BRANCH="agent/m31-t32-skeleton-cap"
CERT=Path("experimental/data/certificates/m31-t32-skeleton-flatness-keystone-v1/m31_t32_skeleton_flatness_keystone.json")
FILES=[
 "experimental/notes/thresholds/m31_t32_skeleton_flatness_keystone.md",
 "experimental/scripts/verify_m31_t32_skeleton_flatness_keystone.py",
 "experimental/lean/m31_flatness_keystone/.gitignore",
 "experimental/lean/m31_flatness_keystone/CORRESPONDENCE.md",
 "experimental/lean/m31_flatness_keystone/M31FlatnessKeystone.lean",
 "experimental/lean/m31_flatness_keystone/M31FlatnessKeystone/SelectorAtlas.lean",
 "experimental/lean/m31_flatness_keystone/lake-manifest.json",
 "experimental/lean/m31_flatness_keystone/lakefile.lean",
 "experimental/lean/m31_flatness_keystone/lean-toolchain"]
PROVENANCE={"fork_base_sha":BASE,"upstream_sha":UPSTREAM,
 "integrated_sources":{
  "experimental/grande_finale.tex":"8a5d9791900ca9eed773feba146b92ad296704ce",
  "experimental/notes/thresholds/m31_quotient_band_swap_census_t16_mixing.md":"9f2756cd3225787d4990acca9474fffb7ccd7e9e",
  "experimental/data/certificates/m31-quotient-band-swap-census-t16-mixing/m31_quotient_band_swap_census_t16_mixing.json":"3df12263d914b66be3d9b69b96179e15ea3fa96b",
  "experimental/notes/thresholds/m31_quotient_t16_mixing_floor.md":"a8576317dfcbbdd4d516167a1c61e500b1a6e1fc",
  "experimental/data/certificates/m31-quotient-t16-mixing-floor/m31_quotient_t16_mixing_floor.json":"7ab0fbebf018dd740526bbf0ccdcb1ad2a5a00fd"},
 "steering_files_are_recorded_not_pinned":True}

def req(c,m):
 if not c: raise AssertionError(m)
def fsha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def isha(xs): return hashlib.sha256(",".join(map(str,xs)).encode()).hexdigest()
def nsha(rows):
 h=hashlib.sha256()
 for r in rows: h.update((",".join(map(str,r))+"\n").encode())
 return h.hexdigest()
def mul(a,b): return ((a[0]*b[0]-a[1]*b[1])%P,(a[0]*b[1]+a[1]*b[0])%P)
def pw(a,e):
 z=(1,0)
 while e:
  if e&1:z=mul(z,a)
  a=mul(a,a);e//=2
 return z
def labels_pow():
 g=(1717986917,1288490189)
 return {r:S2048*pw(g,r*2**19)[0]%P for r in range(1,2048,2)}
def labels_rec():
 g=(1717986917,1288490189);a=pw(g,2**19);s=mul(a,a);o={}
 for j in range(1024): o[2*j+1]=S2048*a[0]%P;a=mul(a,s)
 return o
def cheb(x,n):
 for _ in range(n):x=(2*x*x-1)%P
 return x
def sigma32(r,L): return cheb(2*L[r]%P,5)
def pmul(q,r):
 o=[0]*(len(q)+1)
 for i,c in enumerate(q):o[i]=(o[i]-r*c)%P;o[i+1]=(o[i+1]+c)%P
 return o
def poly(xs):
 q=[1]
 for x in xs:q=pmul(q,x)
 return q
def comb(n,k):
 req(0<=k<=n,"bad binomial");v=1
 for i in range(1,k+1):
  req(v*(n-k+i)%i==0,"nonintegral binomial");v=v*(n-k+i)//i
 return v

def half_rows(W):
 for c in itertools.product(*([range(-2,3)]*7+[range(-1,2)])):
  yield c,sum(a*b for a,b in zip(c,W))%P
def canon(r):
 r=tuple(r);n=tuple(-x for x in r);return min(r,n)
def relation_atlas(pair,single):
 left={}
 for c,s in half_rows(pair[:7]+[single[0]]):req(s not in left,"left collision");left[s]=c
 right=set();rels=[]
 for c,s in half_rows(pair[7:]+[single[1]]):
  req(s not in right,"right collision");right.add(s);a=left.get(-s%P)
  if a is not None:
   r=a[:7]+c[:7]+(a[7],c[7])
   if any(r):rels.append(r)
 req(len(left)==len(right)==234375,"half count")
 req(len(rels)==len(set(rels))==18,"signed relation count")
 req(set(rels)=={tuple(-x for x in r) for r in rels},"sign symmetry")
 C=sorted({canon(r) for r in rels});req(len(C)==9,"canonical count")
 for r in C:req((sum(r[i]*pair[i] for i in range(14))+r[14]*single[0]+r[15]*single[1])%P==0,"bad relation")
 return C,{"left_half_count":len(left),"right_half_count":len(right),"nonzero_signed_relation_count":18,"canonical_relation_count":9}
def pattern_pairs(r):
 choices=[]
 for i,d in enumerate(r):
  states=(-1,0,1) if i<14 else (0,1);choices.append([x for x in states if x+d in states])
 for b in itertools.product(*choices):yield tuple(b[i]+r[i] for i in range(16)),tuple(b)
def weight(a,t):
 z=sum(x==0 for x in a[:14]);base=sum(x!=0 for x in a[:14])+a[14]+a[15];d=t-base
 if d<0 or d%2 or d//2>z:return 0
 return math.comb(z,d//2)
def collision_atlas(C):
 E=set();V=set();counts=[]
 for r in C:
  n=0
  for a,b in pattern_pairs(r):
   e=(a,b) if a<b else (b,a);req(e not in E,"duplicate edge");req(a not in V and b not in V,"nonmatching endpoint")
   E.add(e);V|={a,b};n+=1
  counts.append(n)
 req(sum(counts)==len(E)==68896,"edge count");req(len(V)==137792==2*len(E),"endpoint count")
 best=(-1,None)
 for a,b in sorted(E):
  for t in range(31):
   x=weight(a,t);y=weight(b,t);v=x+y
   if v>best[0]:best=(v,(a,b,t,x,y))
 req(best[0]==482 and best[1][2:]==(15,20,462),"collision maximum")
 single=max(math.comb(z,k) for z in range(15) for k in range(z+1));req(single==3432,"binomial maximum")
 sums=[0,9803698,1263730590,1273534288]
 eq=[{"selector_size":14+((m&1)+((m>>1)&1)),"sigma_sum":s,"fiber_size":3432} for m,s in enumerate(sums)]
 req(all(tuple([0]*14+[m&1,(m>>1)&1]) not in V for m in range(4)),"equality collision")
 a,b,t,x,y=best[1]
 return {"relation_realization_counts":counts,"compressed_edge_count":len(E),"compressed_endpoint_count":len(V),
  "collision_graph_component_size":2,"largest_nontrivial_collision_fiber":482,
  "largest_nontrivial_collision_witness":{"left_pattern":list(a),"right_pattern":list(b),"selector_size":t,"left_weight":x,"right_weight":y},
  "single_compressed_pattern_maximum":single,"selector_fiber_maximum":single,"equality_patterns":eq,
  "endpoint_sha256":nsha(sorted(V)),"edge_sha256":nsha(list(a)+[99]+list(b) for a,b in sorted(E))}

def build(root):
 L=labels_pow();req(L==labels_rec(),"label routes");req(len(L)==len(set(L.values()))==1024,"label count")
 g=(1717986917,1288490189);req(mul(g,(g[0],-g[1]))==(1,0),"norm");req(pw(g,2**30)==(P-1,0) and pw(g,2**31)==(1,0),"order")
 Q=[r for r in range(1,2048,2) if r not in (1,3)];req(len(Q)==1022,"puncture")
 F=defaultdict(list)
 for r in range(1,2048,2):F[sigma32(r,L)].append(r)
 req(len(F)==32 and Counter(map(len,F.values()))=={32:32},"T32 fibers")
 intact=sorted((min(v),s,sorted(v)) for s,v in F.items() if 1 not in v and 3 not in v)
 punct=sorted((min(v),s,sorted(v)) for s,v in F.items() if 1 in v or 3 in v)
 req(len(intact)==30 and len(punct)==2,"intact/punctured count");req(all(set(v)<=set(Q) for _,_,v in intact),"fiber outside Q")
 loc={m:poly(L[r] for r in v) for m,_,v in intact};req(all(len(q)==33 and q[-1]==1 for q in loc.values()),"locator")
 template={tuple(q[1:]) for q in loc.values()};req(len(template)==1,"locator template")
 for m,s,_ in intact:req(loc[m][0]==S32*(1-s)%P,"constant normalization")
 by={s:m for m,s,_ in intact};pairs=[];sing=[];seen=set()
 for m,s,_ in intact:
  if s in seen:continue
  n=-s%P
  if n in by:pairs.append((m,by[n],s,n));seen|={s,n}
  else:sing.append((m,s));seen.add(s)
 pairs.sort();sing.sort();req(len(pairs)==14,"pair count");req(sing==[(61,9803698),(63,1263730590)],"singletons")
 reps=[(5,59),(7,57),(9,55),(11,53),(13,51),(15,49),(17,47),(19,45),(21,43),(23,41),(25,39),(27,37),(29,35),(31,33)]
 req([(a,b) for a,b,_,_ in pairs]==reps,"pair representatives");req((9803698+1263730590)%P==1273534288,"singleton sum")
 pair=[s for _,_,s,_ in pairs];single=[s for _,s in sing];C,rc=relation_atlas(pair,single);ca=collision_atlas(C)
 req(479-32==447 and 479-64==415 and 5**7*3==234375,"degree/table arithmetic")
 q32=P**32;M=math.comb(1022,479);req(M==comb(1022,479),"support routes")
 floor=M//q32;ceil=(M+q32-1)//q32;req((floor,ceil)==(3614119,3614120),"average")
 cap=ca["selector_fiber_maximum"];A=(ceil+cap-1)//cap;B=16777215;T=(B+1+cap-1)//cap
 req((A,T)==(1054,4889),"thresholds");req(cap*1053==3613896 and cap*1054==3617328 and ceil-cap*1053==224,"average products")
 req(cap*4888==16775616 and B-cap*4888==1599 and cap*4889==16779048 and cap*4889-B==1833,"budget products")
 req(3432+8==3440 and (3440+cap-1)//cap==2,"integrated floor")
 bindings={f:fsha(root/f) for f in FILES if req((root/f).is_file(),f"missing {f}") is None}
 return {"schema":"m31-t32-skeleton-flatness-keystone-v1","status":"PROVED_LOCAL_ROUTE_CUT_OPEN_GAP","activity":"PROVE",
  "workboard_item":"M1","row":"Mersenne-31 list at 2^-100","object":"LIST","target_epsilon":"2^-100","agreement":1116023,"B_star":B,
  "architecture":"DIRECT_PINNED_C2048_U0_V1_QUOTIENT_PROFILE","partition_digest":"N/A; fixed support-level quotient profile, no row atom banked",
  "atom_or_cell":"Q / PINNED_QUOTIENT_PREFIX_FIBER / T32_SKELETON",
  "quantifier":"Every fixed canonical remainder and every depth-32 target on the pinned punctured quotient domain; selector cap uniform over all available subsets of the thirty intact T32 fibers.",
  "projection_and_unit":"479-subsets per first-32 monic quotient-locator coefficient target; no received-word or codeword projection.",
  "direct_statement":"For a fixed canonical T32 remainder, at most 3432 supports have one depth-32 prefix. Equality is attained by the complete T64 selector family. Hence an average-sized fiber needs at least 1054 remainders and a budget-breaking fiber needs at least 4889.",
  "branch":BRANCH,"provenance":PROVENANCE,"profile":{"quotient_compression_c":2048,"fixed_template_u":0,"fixed_template_v":1,"support_size":479,"prefix_depth":32},
  "field":{"p":P,"p_power_32":str(q32),"monic_T2048_scale":S2048,"monic_T32_scale":S32,"norm_one_generator":[1717986917,1288490189]},
  "domain":{"full_quotient_size":1024,"punctured_reps":[1,3],"punctured_quotient_size":1022,"quotient_label_sha256":isha(L[r] for r in range(1,2048,2)),
   "T32_fiber_count":32,"T32_fiber_size":32,"intact_T32_fiber_count":30,"punctured_T32_fiber_count":2,
   "intact_T32_min_reps":[m for m,_,_ in intact],"intact_T32_sigma_values":[s for _,s,_ in intact],"intact_T32_fiber_sha256":nsha(v for _,_,v in intact),
   "common_nonconstant_locator_sha256":isha(next(iter(template)))},
  "selector_coordinates":{"opposite_pairs":[{"positive_min_rep":a,"negative_min_rep":b,"positive_sigma":s,"negative_sigma":n} for a,b,s,n in pairs],
   "singletons":[{"min_rep":m,"sigma":s} for m,s in sing],"pair_weights":pair,"singleton_weights":single},
  "relation_atlas":{**rc,"canonical_relations":[list(r) for r in C],"canonical_relation_sha256":nsha(C),**ca},
  "skeleton_arithmetic":{"block_size":32,"first_selector_difference_degree":447,"second_selector_difference_degree":415,"automatic_leading_coefficient_count":31,
   "half_table_formula":234375,"relation_realization_count_sum":sum(ca["relation_realization_counts"]),"equality_case_count":len(ca["equality_patterns"]),"singleton_sum":1273534288},
  "max_vs_average":{"support_count":str(M),"average_floor":floor,"average_ceil":ceil,"selector_fiber_cap":cap,"average_skeleton_threshold":A,
   "product_3432_times_1053":cap*1053,"average_threshold_margin":ceil-cap*1053,"product_3432_times_1054":cap*1054,"budget_break_skeleton_threshold":T,
   "product_3432_times_4888":cap*4888,"budget_safe_margin_at_4888":B-cap*4888,"product_3432_times_4889":cap*4889,"budget_excess_at_4889":cap*4889-B,
   "integrated_T64_family_size":3432,"integrated_non_T64_neighbors":8,"explicit_same_prefix_fiber_floor":3440,"explicit_fiber_minimum_skeletons":2},
  "bindings":bindings,"nonclaims":["No upper bound on the number of canonical T32 remainders in one prefix fiber.","No global maximum-fiber bound for all 479-subsets.",
   "No received-word realization or ordinary-list row closure.","No first-match survival, add-back, or deployed U_Q integer.","No claim that the exact global maximum is near the average."],"verdict":"OPEN GAP"}

def same(a,b,path="$"):
 if type(a)!=type(b):raise AssertionError(f"type at {path}")
 if isinstance(b,dict):
  req(set(a)==set(b),f"keys at {path}")
  for k in b:same(a[k],b[k],path+"."+k)
 elif isinstance(b,list):
  req(len(a)==len(b),f"length at {path}")
  for i,(x,y) in enumerate(zip(a,b)):same(x,y,f"{path}[{i}]")
 else:req(a==b,f"value at {path}: {a!r} != {b!r}")
def load(root):
 req((root/CERT).is_file(),"missing certificate");return json.loads((root/CERT).read_text())
def check(root):
 e=build(root);same(load(root),e);return e
def tamper(root):
 e=check(root);a=load(root);M=[]
 def add(label,fn):c=copy.deepcopy(a);fn(c);M.append((label,c))
 add("prime",lambda c:c["field"].__setitem__("p",P-2));add("puncture",lambda c:c["domain"]["punctured_reps"].__setitem__(1,5))
 add("intact",lambda c:c["domain"].__setitem__("intact_T32_fiber_count",29));add("relations",lambda c:c["relation_atlas"].__setitem__("canonical_relation_count",8))
 add("row",lambda c:c["relation_atlas"]["canonical_relations"][0].__setitem__(0,-1));add("edges",lambda c:c["relation_atlas"].__setitem__("compressed_edge_count",68895))
 add("collision",lambda c:c["relation_atlas"].__setitem__("largest_nontrivial_collision_fiber",483));add("cap",lambda c:c["max_vs_average"].__setitem__("selector_fiber_cap",3431))
 add("average",lambda c:c["max_vs_average"].__setitem__("average_ceil",3614119));add("A",lambda c:c["max_vs_average"].__setitem__("average_skeleton_threshold",1053))
 add("B",lambda c:c["max_vs_average"].__setitem__("budget_break_skeleton_threshold",4888));add("floor",lambda c:c["max_vs_average"].__setitem__("explicit_same_prefix_fiber_floor",3439))
 add("binding",lambda c:c["bindings"].__setitem__(FILES[0],"0"*64));add("status",lambda c:c.__setitem__("status","PROVED_ROW"));add("nonclaim",lambda c:c["nonclaims"].pop())
 for label,c in M:
  try:same(c,e)
  except AssertionError:continue
  raise AssertionError("tamper survived: "+label)
 print(f"tamper-selftest: PASS ({len(M)} mutations rejected)")
def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument("--check",action="store_true");g.add_argument("--tamper-selftest",action="store_true");g.add_argument("--emit-certificate",action="store_true",help=argparse.SUPPRESS);p.add_argument("--repo-root",type=Path);a=p.parse_args()
 root=(a.repo_root or Path(__file__).resolve().parents[2]).resolve()
 try:
  if a.emit_certificate:
   d=build(root);(root/CERT).parent.mkdir(parents=True,exist_ok=True);(root/CERT).write_text(json.dumps(d,sort_keys=True,separators=(",",":"))+"\n");print("wrote",root/CERT)
  elif a.check:
   d=check(root);m=d["max_vs_average"];print(f"check: PASS; selector cap {m['selector_fiber_cap']}, average skeleton threshold {m['average_skeleton_threshold']}, budget-break threshold {m['budget_break_skeleton_threshold']}")
  else:tamper(root)
 except (AssertionError,OSError,ValueError,json.JSONDecodeError) as e:print("FAIL:",e,file=sys.stderr);return 1
 return 0
if __name__=="__main__":raise SystemExit(main())
