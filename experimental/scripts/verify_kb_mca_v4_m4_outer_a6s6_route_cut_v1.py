#!/usr/bin/env python3
"""Verify the KoalaBear m4 outer A6/S6 route cut."""

from __future__ import annotations

import argparse, copy, hashlib, json, subprocess
from itertools import combinations, permutations
from pathlib import Path
from typing import Any, Callable

if not __debug__:
    raise RuntimeError("verifier refuses optimized Python execution")

class VerificationError(RuntimeError): pass
def require(condition: bool, message: str) -> None:
    if not condition: raise VerificationError(message)

ROOT=Path(__file__).resolve().parents[1]
REPO_ROOT=ROOT.parent
CERTIFICATE=ROOT/"data"/"certificates"/"kb-mca-v4-m4-outer-a6s6-route-cut-v1"/"kb_mca_v4_m4_outer_a6s6_route_cut_v1.json"
SCHEMA="kb-mca-v4-m4-outer-a6s6-route-cut-v1"
COMPILER_COMMIT="e287c54252c7872e1745c7594cfef62b74a65cf5"
COMPILER_PATH="experimental/data/certificates/kb-mca-v4-degree60-source-pencil-rank-compiler-v1/kb_mca_v4_degree60_source_pencil_rank_compiler_v1.json"
COMPILER_BLOB="5c16c7884b349d7e474b8dfc1267ab357ef0d477"
COMPILER_PAYLOAD="6d4bc83e40e491f02f7d265b021628ffb7d52b1978c0655f83e5a9d3e0a9f4bb"
FRONTIER_COMMIT="30be68b9421ba37155499d52a0635fa7b10ae3b2"
FRONTIER_PATH="experimental/data/certificates/kb-mca-v4-m6-scott-cartesian-degree2-router-v1/kb_mca_v4_m6_scott_cartesian_degree2_router_v1.json"
FRONTIER_BLOB="af5fd87a5c28f3b021fc05971a665e6d92f978af"
FRONTIER_PAYLOAD="b34e096730f3d93644c283f95d65f622100d6868e9882ed2b901fa109b3d6116"
M12_COMMIT="c23eb801af8853d0369a72ea8834c84e7a3242f6"
M12_PATH="experimental/data/certificates/kb-mca-v4-m12-diagonal-socle-degree5-close-v1/kb_mca_v4_m12_diagonal_socle_degree5_close_v1.json"
M12_BLOB="9e1bd3d89dac6409f148dc134fda46d3bf644c11"
M12_PAYLOAD="456b51c78e837c8a27ffda0b43409c63c88128b254be320723728868db096e6f"
M4_ROWS=[[1,16],[2,8],[4,4],[8,2]]
CATALOGUE=[
 {"group":"A7","order":2520,"subdegrees":[1,14]},
 {"group":"A6","order":360,"subdegrees":[1,6,8]},
 {"group":"S6","order":720,"subdegrees":[1,6,8]},
 {"group":"PSL(4,2)","order":20160,"subdegrees":[1,14]},
 {"group":"A15","order":653837184000,"subdegrees":[1,14]},
 {"group":"S15","order":1307674368000,"subdegrees":[1,14]},
]
NONCLAIMS=["The surviving A6/S6 outer type is not deleted or paid.","No endpoint-record census or carrier, data, explaining-polynomial, or slope bridge is claimed.","No u=2, K3, or KoalaBear row closure is claimed.","No ledger quantity moves."]

def canonical_json(value: Any)->str: return json.dumps(value,sort_keys=True,separators=(",",":"))
def payload_hash(value: dict[str,Any])->str:
    unhashed=dict(value); unhashed.pop("payload_sha256",None)
    return hashlib.sha256(canonical_json(unhashed).encode()).hexdigest()
def reject_duplicates(pairs):
    result={}
    for key,value in pairs:
        if key in result: raise VerificationError(f"duplicate JSON key: {key}")
        result[key]=value
    return result
def parse_json(text: str,label: str)->dict[str,Any]:
    try: value=json.loads(text,object_pairs_hook=reject_duplicates)
    except (json.JSONDecodeError,VerificationError) as error: raise VerificationError(f"cannot parse {label}: {error}") from error
    require(isinstance(value,dict),f"{label} is not object"); return value
def git_output(*args: str)->str:
    try: result=subprocess.run(["git",*args],cwd=REPO_ROOT,check=True,capture_output=True,text=True)
    except subprocess.CalledProcessError as error: raise VerificationError(error.stderr.strip()) from error
    return result.stdout.strip()
def exact_keys(value: Any,expected: set[str],label: str)->None:
    require(isinstance(value,dict),f"{label} object")
    require(set(value)==expected,f"{label} keys: {sorted(set(value)^expected)}")

def verify_schema(data):
    exact_keys(data,{"schema","payload_sha256","statement","parent_compiler","incoming_frontier","degree_twelve_import","degree_fifteen_catalogue","proper_factor_route","survivor","external_source_custody","source_bindings","conclusion","nonclaims"},"certificate")
    exact_keys(data["statement"],{"workboard_item","row","object","agreement","B_star","endpoint_degree","original_inner_degree","original_outer_degree","status","ledger_movement"},"statement")
    exact_keys(data["parent_compiler"],{"commit","certificate_path","certificate_blob_oid","certificate_payload_sha256","imported_terminal","imported_m4_rows"},"parent")
    exact_keys(data["incoming_frontier"],{"commit","certificate_path","certificate_blob_oid","certificate_payload_sha256","imported_terminal","global_transverse_type_count","live_inner_degrees"},"frontier")
    exact_keys(data["degree_twelve_import"],{"commit","certificate_path","certificate_blob_oid","certificate_payload_sha256","terminal"},"m12")
    for i,row in enumerate(data["degree_fifteen_catalogue"]): exact_keys(row,{"group","order","subdegrees"},f"catalogue {i}")
    exact_keys(data["proper_factor_route"],{"excluded_outer_subdegrees","proper_right_factor_degrees","resulting_endpoint_inner_degrees","degree_twelve_terminal","degree_twenty_source_ramification","degree_twenty_RH_budget","degree_twenty_survives","terminal"},"factor route")
    exact_keys(data["survivor"],{"outer_subdegree","correspondence_degree","outer_groups","action","action_degree","point_stabilizer_subdegrees","pole_cycle_type","pole_profile_compatible","terminal"},"survivor")
    exact_keys(data["external_source_custody"],{"gap_primgrp_commit","gap_degree15_entry_bytes","gap_degree15_entry_sha256"},"custody")
    for i,row in enumerate(data["source_bindings"]): exact_keys(row,{"binding_id","commit","path","blob_oid","role"},f"binding {i}")
    exact_keys(data["conclusion"],{"excluded_m4_rows","surviving_m4_rows","remaining_global_transverse_type_count","remaining_inner_degrees","terminal","m4_closed","u2_closed","K3_closed","row_closed"},"conclusion")

def verify_semantics(data):
    require(data["schema"]==SCHEMA,"schema")
    require(data["statement"]=={"workboard_item":"K3","row":"KoalaBear MCA at 2^-128","object":"MCA","agreement":1116048,"B_star":"274980728111395087","endpoint_degree":60,"original_inner_degree":4,"original_outer_degree":15,"status":"PROVED_M4_ONLY_R8_DELTA2_A6S6_OUTER_SURVIVES_OTHER_K3_ROWS_OPEN","ledger_movement":0},"statement")
    require(data["degree_fifteen_catalogue"]==CATALOGUE,"catalogue")
    possible={r for row in CATALOGUE for r in row["subdegrees"][1:] if r in {1,2,4,8}}
    require(possible=={8},"candidate subdegrees")
    require([row["group"] for row in CATALOGUE if 8 in row["subdegrees"]]==["A6","S6"],"survivor groups")
    route=data["proper_factor_route"]
    require(route=={"excluded_outer_subdegrees":[1,2,4],"proper_right_factor_degrees":[3,5],"resulting_endpoint_inner_degrees":[12,20],"degree_twelve_terminal":"M12_DECOMPOSITION_ROW_EMPTY","degree_twenty_source_ramification":48,"degree_twenty_RH_budget":38,"degree_twenty_survives":False,"terminal":"R1_R2_R4_OUTER_TYPES_EMPTY"},"factor route")
    require(48>38,"RH contradiction")
    survivor=data["survivor"]
    require(survivor=={"outer_subdegree":8,"correspondence_degree":2,"outer_groups":["A6","S6"],"action":"two-subsets of six points","action_degree":15,"point_stabilizer_subdegrees":[1,6,8],"pole_cycle_type":[5,5,5],"pole_profile_compatible":True,"terminal":"ONLY_R8_DELTA2_A6S6_OUTER_SURVIVES"},"survivor")
    conclusion=data["conclusion"]
    require(conclusion["excluded_m4_rows"]==[[1,16],[2,8],[4,4]],"excluded rows")
    require(conclusion["surviving_m4_rows"]==[[8,2]],"surviving row")
    require(conclusion["remaining_global_transverse_type_count"]==9==12-3,"count")
    require(conclusion["remaining_inner_degrees"]==[2,3,4],"degrees")
    require(conclusion["terminal"]=="M4_ONLY_R8_DELTA2_A6S6_OUTER_SURVIVES","terminal")
    for key in ("m4_closed","u2_closed","K3_closed","row_closed"): require(conclusion[key] is False,f"forbidden {key}")
    require(data["nonclaims"]==NONCLAIMS,"nonclaims")

def verify_parents(data,check_git=True):
    require(data["parent_compiler"]=={"commit":COMPILER_COMMIT,"certificate_path":COMPILER_PATH,"certificate_blob_oid":COMPILER_BLOB,"certificate_payload_sha256":COMPILER_PAYLOAD,"imported_terminal":"TRANSVERSE_OUTER_CORRESPONDENCE_UNPAID","imported_m4_rows":M4_ROWS},"parent")
    require(data["incoming_frontier"]=={"commit":FRONTIER_COMMIT,"certificate_path":FRONTIER_PATH,"certificate_blob_oid":FRONTIER_BLOB,"certificate_payload_sha256":FRONTIER_PAYLOAD,"imported_terminal":"M6_NO_TERMINAL_PRODUCER_ROUTES_TO_M2_OR_EXCLUDED_M5","global_transverse_type_count":12,"live_inner_degrees":[2,3,4]},"frontier")
    require(data["degree_twelve_import"]=={"commit":M12_COMMIT,"certificate_path":M12_PATH,"certificate_blob_oid":M12_BLOB,"certificate_payload_sha256":M12_PAYLOAD,"terminal":"M12_DECOMPOSITION_ROW_EMPTY"},"m12 import")
    expected=[
      {"binding_id":"KB_M4_CUT::compiler_certificate","commit":COMPILER_COMMIT,"path":COMPILER_PATH,"blob_oid":COMPILER_BLOB,"role":"four m4 transverse rows and exhaustive source profiles"},
      {"binding_id":"KB_M4_CUT::incoming_frontier_certificate","commit":FRONTIER_COMMIT,"path":FRONTIER_PATH,"blob_oid":FRONTIER_BLOB,"role":"12-type frontier after m6 routing"},
      {"binding_id":"KB_M4_CUT::m12_certificate","commit":M12_COMMIT,"path":M12_PATH,"blob_oid":M12_BLOB,"role":"deletion of the degree-twelve proper-factor route"},
    ]
    require(data["source_bindings"]==expected,"bindings")
    if not check_git: return
    for row in expected: require(git_output("rev-parse",f"{row['commit']}:{row['path']}")==row["blob_oid"],f"binding {row['binding_id']}")
    compiler=parse_json(git_output("show",f"{COMPILER_COMMIT}:{COMPILER_PATH}"),"compiler")
    require(payload_hash(compiler)==compiler["payload_sha256"]==COMPILER_PAYLOAD,"compiler payload")
    m4=next(row for row in compiler["transverse_outer_terminal"]["rows"] if row["m"]==4)
    require(m4["r_delta"]==M4_ROWS,"historical m4")
    frontier=parse_json(git_output("show",f"{FRONTIER_COMMIT}:{FRONTIER_PATH}"),"frontier")
    require(payload_hash(frontier)==frontier["payload_sha256"]==FRONTIER_PAYLOAD,"frontier payload")
    require(frontier["conclusion"]["remaining_global_transverse_type_count"]==12,"frontier count")
    m12=parse_json(git_output("show",f"{M12_COMMIT}:{M12_PATH}"),"m12")
    require(payload_hash(m12)==m12["payload_sha256"]==M12_PAYLOAD,"m12 payload")
    require(m12["conclusion"]["terminal"]=="M12_DECOMPOSITION_ROW_EMPTY","m12 terminal")

POINTS=tuple(range(6)); PAIRS=tuple(combinations(POINTS,2)); BASE=(0,1)
def parity(p): return sum(p[i]>p[j] for i in POINTS for j in range(i+1,6))%2
def act(p,pair): return tuple(sorted((p[pair[0]],p[pair[1]])))
def subdegrees(group):
    stabilizer=[g for g in group if act(g,BASE)==BASE]; unseen=set(PAIRS); lengths=[]
    while unseen:
        pair=min(unseen); orbit={act(g,pair) for g in stabilizer}; unseen-=orbit; lengths.append(len(orbit))
    return sorted(lengths)
def cycle_lengths(p):
    unseen=set(PAIRS); lengths=[]
    while unseen:
        start=min(unseen); orbit=set(); point=start
        while point not in orbit: orbit.add(point); point=act(p,point)
        unseen-=orbit; lengths.append(len(orbit))
    return sorted(lengths)
def verify_actions():
    s6=list(permutations(POINTS)); a6=[g for g in s6 if parity(g)==0]
    require((len(a6),len(s6),len(PAIRS))==(360,720,15),"action orders")
    require(subdegrees(a6)==subdegrees(s6)==[1,6,8],"two-subset subdegrees")
    five=(1,2,3,4,0,5); require(parity(five)==0 and cycle_lengths(five)==[5,5,5],"pole cycle")

def verify_certificate(data,check_git=True,run_actions=True):
    verify_schema(data); require(payload_hash(data)==data["payload_sha256"],"payload hash")
    verify_semantics(data); verify_parents(data,check_git)
    require(data["external_source_custody"]=={"gap_primgrp_commit":"5612e113d50ac23a7d10945383936e20440b4e14","gap_degree15_entry_bytes":894,"gap_degree15_entry_sha256":"d24658310cb386c9663e95ab9024eab9142d79f849131f499da36eeda82c003e"},"custody")
    if run_actions: verify_actions()
def reseal(data): data["payload_sha256"]=payload_hash(data)
def tamper_selftest(original):
    mutations: list[tuple[str,Callable]]=[
      ("drop-group",lambda v:v["degree_fifteen_catalogue"].pop()),
      ("add-r4",lambda v:v["degree_fifteen_catalogue"][0]["subdegrees"].append(4)),
      ("factor",lambda v:v["proper_factor_route"].__setitem__("proper_right_factor_degrees",[3])),
      ("RH",lambda v:v["proper_factor_route"].__setitem__("degree_twenty_RH_budget",50)),
      ("keep-r2",lambda v:v["proper_factor_route"]["excluded_outer_subdegrees"].remove(2)),
      ("survivor",lambda v:v["survivor"].__setitem__("outer_subdegree",4)),
      ("pole",lambda v:v["survivor"].__setitem__("pole_cycle_type",[5,5,1,1,1,1,1])),
      ("parent",lambda v:v["parent_compiler"].__setitem__("certificate_payload_sha256","0"*64)),
      ("frontier",lambda v:v["incoming_frontier"].__setitem__("global_transverse_type_count",13)),
      ("m12",lambda v:v["degree_twelve_import"].__setitem__("terminal","OPEN")),
      ("binding",lambda v:v["source_bindings"][0].__setitem__("blob_oid","0"*40)),
      ("count",lambda v:v["conclusion"].__setitem__("remaining_global_transverse_type_count",10)),
      ("close",lambda v:v["conclusion"].__setitem__("m4_closed",True)),
      ("ledger",lambda v:v["statement"].__setitem__("ledger_movement",1)),
      ("nonclaim",lambda v:v["nonclaims"].pop()),
      ("extra",lambda v:v.__setitem__("extra",1)),
    ]; passed=0
    for name,mutate in mutations:
        candidate=copy.deepcopy(original); mutate(candidate); reseal(candidate)
        try: verify_certificate(candidate,False,False)
        except VerificationError: passed+=1
        else: raise VerificationError(f"tamper survived: {name}")
    bad=copy.deepcopy(original); bad["payload_sha256"]="0"*64
    try: verify_certificate(bad,False,False)
    except VerificationError: passed+=1
    else: raise VerificationError("tamper survived: hash")
    try: parse_json('{"x":1,"x":2}',"duplicate")
    except VerificationError: passed+=1
    else: raise VerificationError("duplicate survived")
    return passed
def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--check",action="store_true"); parser.add_argument("--tamper-selftest",action="store_true"); args=parser.parse_args()
    if not args.check and not args.tamper_selftest: parser.error("at least one action is required")
    data=parse_json(CERTIFICATE.read_text(),str(CERTIFICATE)); verify_certificate(data)
    print("PASS: m4 cuts to the r=8 delta=2 A6/S6 outer type")
    if args.tamper_selftest:
        count=tamper_selftest(data); print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0
if __name__=="__main__": raise SystemExit(main())
