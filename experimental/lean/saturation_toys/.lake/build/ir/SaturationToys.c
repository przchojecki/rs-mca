// Lean compiler output
// Module: SaturationToys
// Imports: Init
#include <lean/lean.h>
#if defined(__clang__)
#pragma clang diagnostic ignored "-Wunused-parameter"
#pragma clang diagnostic ignored "-Wunused-label"
#elif defined(__GNUC__) && !defined(__CLANG__)
#pragma GCC diagnostic ignored "-Wunused-parameter"
#pragma GCC diagnostic ignored "-Wunused-label"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
#endif
#ifdef __cplusplus
extern "C" {
#endif
static uint8_t l_SaturationToys_census2__toy2___nativeDecide__1___closed__4;
static lean_object* l_SaturationToys_census2__toy2___nativeDecide__1___closed__1;
static uint8_t l_SaturationToys_census2__toy3___nativeDecide__1___closed__5;
LEAN_EXPORT lean_object* l_List_foldl___at_SaturationToys_census2___spec__1___boxed(lean_object*, lean_object*);
static lean_object* l_SaturationToys_census2__toy3___nativeDecide__1___closed__1;
LEAN_EXPORT uint8_t l_SaturationToys_toy3__sum___nativeDecide__1;
lean_object* lean_nat_div(lean_object*, lean_object*);
static lean_object* l_SaturationToys_census2__toy3___nativeDecide__1___closed__3;
LEAN_EXPORT lean_object* l_SaturationToys_census2(lean_object*);
LEAN_EXPORT lean_object* l_SaturationToys_census2___boxed(lean_object*);
LEAN_EXPORT lean_object* l_SaturationToys_binom2___boxed(lean_object*);
LEAN_EXPORT uint8_t l_SaturationToys_census2__toy3___nativeDecide__1;
static lean_object* l_SaturationToys_census2__toy2___nativeDecide__1___closed__3;
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
static lean_object* l_SaturationToys_census2__toy3___nativeDecide__1___closed__4;
static lean_object* l_SaturationToys_census2__toy3___nativeDecide__1___closed__2;
lean_object* lean_nat_sub(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_foldl___at_SaturationToys_census2___spec__1(lean_object*, lean_object*);
lean_object* lean_nat_mul(lean_object*, lean_object*);
LEAN_EXPORT uint8_t l_SaturationToys_toy2__sum___nativeDecide__1;
LEAN_EXPORT uint8_t l_SaturationToys_toy1__C4__2___nativeDecide__1;
lean_object* lean_nat_add(lean_object*, lean_object*);
LEAN_EXPORT uint8_t l_SaturationToys_census2__toy2___nativeDecide__1;
static lean_object* l_SaturationToys_census2__toy2___nativeDecide__1___closed__2;
LEAN_EXPORT lean_object* l_SaturationToys_binom2(lean_object*);
static uint8_t _init_l_SaturationToys_toy1__C4__2___nativeDecide__1() {
_start:
{
uint8_t x_1; 
x_1 = 1;
return x_1;
}
}
static uint8_t _init_l_SaturationToys_toy2__sum___nativeDecide__1() {
_start:
{
uint8_t x_1; 
x_1 = 1;
return x_1;
}
}
static uint8_t _init_l_SaturationToys_toy3__sum___nativeDecide__1() {
_start:
{
uint8_t x_1; 
x_1 = 1;
return x_1;
}
}
LEAN_EXPORT lean_object* l_SaturationToys_binom2(lean_object* x_1) {
_start:
{
lean_object* x_2; lean_object* x_3; lean_object* x_4; lean_object* x_5; lean_object* x_6; 
x_2 = lean_unsigned_to_nat(1u);
x_3 = lean_nat_sub(x_1, x_2);
x_4 = lean_nat_mul(x_1, x_3);
lean_dec(x_3);
x_5 = lean_unsigned_to_nat(2u);
x_6 = lean_nat_div(x_4, x_5);
lean_dec(x_4);
return x_6;
}
}
LEAN_EXPORT lean_object* l_SaturationToys_binom2___boxed(lean_object* x_1) {
_start:
{
lean_object* x_2; 
x_2 = l_SaturationToys_binom2(x_1);
lean_dec(x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* l_List_foldl___at_SaturationToys_census2___spec__1(lean_object* x_1, lean_object* x_2) {
_start:
{
if (lean_obj_tag(x_2) == 0)
{
return x_1;
}
else
{
lean_object* x_3; lean_object* x_4; lean_object* x_5; lean_object* x_6; 
x_3 = lean_ctor_get(x_2, 0);
x_4 = lean_ctor_get(x_2, 1);
x_5 = l_SaturationToys_binom2(x_3);
x_6 = lean_nat_add(x_1, x_5);
lean_dec(x_5);
lean_dec(x_1);
x_1 = x_6;
x_2 = x_4;
goto _start;
}
}
}
LEAN_EXPORT lean_object* l_SaturationToys_census2(lean_object* x_1) {
_start:
{
lean_object* x_2; lean_object* x_3; 
x_2 = lean_unsigned_to_nat(0u);
x_3 = l_List_foldl___at_SaturationToys_census2___spec__1(x_2, x_1);
return x_3;
}
}
LEAN_EXPORT lean_object* l_List_foldl___at_SaturationToys_census2___spec__1___boxed(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = l_List_foldl___at_SaturationToys_census2___spec__1(x_1, x_2);
lean_dec(x_2);
return x_3;
}
}
LEAN_EXPORT lean_object* l_SaturationToys_census2___boxed(lean_object* x_1) {
_start:
{
lean_object* x_2; 
x_2 = l_SaturationToys_census2(x_1);
lean_dec(x_1);
return x_2;
}
}
static lean_object* _init_l_SaturationToys_census2__toy2___nativeDecide__1___closed__1() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = lean_box(0);
x_2 = lean_unsigned_to_nat(2u);
x_3 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_3, 0, x_2);
lean_ctor_set(x_3, 1, x_1);
return x_3;
}
}
static lean_object* _init_l_SaturationToys_census2__toy2___nativeDecide__1___closed__2() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = lean_unsigned_to_nat(3u);
x_2 = l_SaturationToys_census2__toy2___nativeDecide__1___closed__1;
x_3 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_3, 0, x_1);
lean_ctor_set(x_3, 1, x_2);
return x_3;
}
}
static lean_object* _init_l_SaturationToys_census2__toy2___nativeDecide__1___closed__3() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = lean_unsigned_to_nat(0u);
x_2 = l_SaturationToys_census2__toy2___nativeDecide__1___closed__2;
x_3 = l_List_foldl___at_SaturationToys_census2___spec__1(x_1, x_2);
return x_3;
}
}
static uint8_t _init_l_SaturationToys_census2__toy2___nativeDecide__1___closed__4() {
_start:
{
lean_object* x_1; lean_object* x_2; uint8_t x_3; 
x_1 = l_SaturationToys_census2__toy2___nativeDecide__1___closed__3;
x_2 = lean_unsigned_to_nat(4u);
x_3 = lean_nat_dec_eq(x_1, x_2);
return x_3;
}
}
static uint8_t _init_l_SaturationToys_census2__toy2___nativeDecide__1() {
_start:
{
uint8_t x_1; 
x_1 = l_SaturationToys_census2__toy2___nativeDecide__1___closed__4;
return x_1;
}
}
static lean_object* _init_l_SaturationToys_census2__toy3___nativeDecide__1___closed__1() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = lean_box(0);
x_2 = lean_unsigned_to_nat(0u);
x_3 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_3, 0, x_2);
lean_ctor_set(x_3, 1, x_1);
return x_3;
}
}
static lean_object* _init_l_SaturationToys_census2__toy3___nativeDecide__1___closed__2() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = lean_unsigned_to_nat(3u);
x_2 = l_SaturationToys_census2__toy3___nativeDecide__1___closed__1;
x_3 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_3, 0, x_1);
lean_ctor_set(x_3, 1, x_2);
return x_3;
}
}
static lean_object* _init_l_SaturationToys_census2__toy3___nativeDecide__1___closed__3() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = lean_unsigned_to_nat(5u);
x_2 = l_SaturationToys_census2__toy3___nativeDecide__1___closed__2;
x_3 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_3, 0, x_1);
lean_ctor_set(x_3, 1, x_2);
return x_3;
}
}
static lean_object* _init_l_SaturationToys_census2__toy3___nativeDecide__1___closed__4() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = lean_unsigned_to_nat(0u);
x_2 = l_SaturationToys_census2__toy3___nativeDecide__1___closed__3;
x_3 = l_List_foldl___at_SaturationToys_census2___spec__1(x_1, x_2);
return x_3;
}
}
static uint8_t _init_l_SaturationToys_census2__toy3___nativeDecide__1___closed__5() {
_start:
{
lean_object* x_1; lean_object* x_2; uint8_t x_3; 
x_1 = l_SaturationToys_census2__toy3___nativeDecide__1___closed__4;
x_2 = lean_unsigned_to_nat(13u);
x_3 = lean_nat_dec_eq(x_1, x_2);
return x_3;
}
}
static uint8_t _init_l_SaturationToys_census2__toy3___nativeDecide__1() {
_start:
{
uint8_t x_1; 
x_1 = l_SaturationToys_census2__toy3___nativeDecide__1___closed__5;
return x_1;
}
}
lean_object* initialize_Init(uint8_t builtin, lean_object*);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_SaturationToys(uint8_t builtin, lean_object* w) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin, lean_io_mk_world());
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
l_SaturationToys_toy1__C4__2___nativeDecide__1 = _init_l_SaturationToys_toy1__C4__2___nativeDecide__1();
l_SaturationToys_toy2__sum___nativeDecide__1 = _init_l_SaturationToys_toy2__sum___nativeDecide__1();
l_SaturationToys_toy3__sum___nativeDecide__1 = _init_l_SaturationToys_toy3__sum___nativeDecide__1();
l_SaturationToys_census2__toy2___nativeDecide__1___closed__1 = _init_l_SaturationToys_census2__toy2___nativeDecide__1___closed__1();
lean_mark_persistent(l_SaturationToys_census2__toy2___nativeDecide__1___closed__1);
l_SaturationToys_census2__toy2___nativeDecide__1___closed__2 = _init_l_SaturationToys_census2__toy2___nativeDecide__1___closed__2();
lean_mark_persistent(l_SaturationToys_census2__toy2___nativeDecide__1___closed__2);
l_SaturationToys_census2__toy2___nativeDecide__1___closed__3 = _init_l_SaturationToys_census2__toy2___nativeDecide__1___closed__3();
lean_mark_persistent(l_SaturationToys_census2__toy2___nativeDecide__1___closed__3);
l_SaturationToys_census2__toy2___nativeDecide__1___closed__4 = _init_l_SaturationToys_census2__toy2___nativeDecide__1___closed__4();
l_SaturationToys_census2__toy2___nativeDecide__1 = _init_l_SaturationToys_census2__toy2___nativeDecide__1();
l_SaturationToys_census2__toy3___nativeDecide__1___closed__1 = _init_l_SaturationToys_census2__toy3___nativeDecide__1___closed__1();
lean_mark_persistent(l_SaturationToys_census2__toy3___nativeDecide__1___closed__1);
l_SaturationToys_census2__toy3___nativeDecide__1___closed__2 = _init_l_SaturationToys_census2__toy3___nativeDecide__1___closed__2();
lean_mark_persistent(l_SaturationToys_census2__toy3___nativeDecide__1___closed__2);
l_SaturationToys_census2__toy3___nativeDecide__1___closed__3 = _init_l_SaturationToys_census2__toy3___nativeDecide__1___closed__3();
lean_mark_persistent(l_SaturationToys_census2__toy3___nativeDecide__1___closed__3);
l_SaturationToys_census2__toy3___nativeDecide__1___closed__4 = _init_l_SaturationToys_census2__toy3___nativeDecide__1___closed__4();
lean_mark_persistent(l_SaturationToys_census2__toy3___nativeDecide__1___closed__4);
l_SaturationToys_census2__toy3___nativeDecide__1___closed__5 = _init_l_SaturationToys_census2__toy3___nativeDecide__1___closed__5();
l_SaturationToys_census2__toy3___nativeDecide__1 = _init_l_SaturationToys_census2__toy3___nativeDecide__1();
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
