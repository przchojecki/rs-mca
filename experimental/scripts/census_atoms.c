/* census_atoms.c -- fast-path enumerator for the M31 aligned depth-32
 * collision census (packet: m31_aligned_collision_census_v1).
 *
 * Exhaustive T_d-fiber census: find all (anchor a-subset X, complement a-subset
 * Y) whose 32-power-sum vectors are equal (= depth-32 collision) rooted at the
 * band anchor.  Reads atoms_dD.bin, written by gen_atoms.py, whose header is
 * (d, nA, nC) followed by nA*32 + nC*32 little-endian uint32 power-sum values
 * (mod p = 2^31 - 1).  The anchor side (smaller) is hashed; the complement side
 * is streamed; every fingerprint hit is exact-verified on the full 32-vector.
 * Each true collision prints as:  HIT <a anchor idx> | <a comp idx>
 * An empty stdout hit log therefore certifies zero collisions.
 *
 * Build : cc -O3 -o census_atoms experimental/scripts/census_atoms.c
 * Usage : ./census_atoms atoms_d8.bin 7 > hits_d8_a7.txt   (2>stderr audit)
 * The e = 8*a (T8) sweeps are the recorded long-run results; the T16 sweeps
 * (d=16, a=3,4) are also re-run cheaply by the Python verifier.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

#define P 2147483647u   /* 2^31 - 1 */
static uint32_t (*A)[32];   /* anchor atom power-sum vectors */
static uint32_t (*C)[32];   /* comp   atom power-sum vectors */
static int nA, nC, aK, dD;

/* open-addressing table: slot = {fp (8B), code (8B)} ; fp==0 means empty */
static uint64_t *TBL_fp;
static uint64_t *TBL_code;
static uint64_t MASK;

static inline uint64_t mix(const uint32_t *v){
    uint64_t h = 1469598103934665603ULL;
    for(int i=0;i<32;i++){ h ^= v[i]; h *= 1099511628211ULL; }
    if(h==0) h=1;  /* reserve 0 for empty */
    return h;
}
static inline void acc_add(uint32_t *dst, const uint32_t *s){
    for(int i=0;i<32;i++){ uint32_t t=dst[i]+s[i]; if(t>=P)t-=P; dst[i]=t; }
}

/* ---- build anchor table ---- */
static uint64_t nAnchorLeaves=0;
static void anchor_rec(int start, int depth, uint32_t *acc, uint64_t code){
    if(depth==aK){
        uint64_t fp=mix(acc);
        uint64_t s=fp & MASK;
        while(TBL_fp[s]!=0) s=(s+1)&MASK;
        TBL_fp[s]=fp; TBL_code[s]=code;
        nAnchorLeaves++;
        return;
    }
    for(int i=start;i<=nA-(aK-depth);i++){
        uint32_t na[32]; memcpy(na,acc,sizeof na); acc_add(na, A[i]);
        anchor_rec(i+1, depth+1, na, code | ((uint64_t)i << (8*depth)));
    }
}

/* ---- stream comp side ---- */
static uint64_t nCompLeaves=0, nHits=0, nFpProbes=0;
static void decode_and_check(uint64_t acode, const uint32_t *cacc, uint64_t ccode){
    /* recompute anchor vector from code, exact-compare to comp acc */
    uint32_t acc[32]; memset(acc,0,sizeof acc);
    int idx[8];
    for(int k=0;k<aK;k++){ int i=(acode>>(8*k))&0xff; idx[k]=i; acc_add(acc, A[i]); }
    if(memcmp(acc,cacc,sizeof acc)!=0) return; /* fingerprint false positive */
    /* true collision */
    printf("HIT");
    for(int k=0;k<aK;k++) printf(" %d", idx[k]);
    printf(" |");
    for(int k=0;k<aK;k++) printf(" %d", (int)((ccode>>(8*k))&0xff));
    printf("\n");
    nHits++;
}
static void comp_rec(int start, int depth, uint32_t *acc, uint64_t code){
    if(depth==aK){
        nCompLeaves++;
        uint64_t fp=mix(acc);
        uint64_t s=fp & MASK;
        while(TBL_fp[s]!=0){
            if(TBL_fp[s]==fp){ nFpProbes++; decode_and_check(TBL_code[s], acc, code); }
            s=(s+1)&MASK;
        }
        return;
    }
    for(int i=start;i<=nC-(aK-depth);i++){
        uint32_t na[32]; memcpy(na,acc,sizeof na); acc_add(na, C[i]);
        comp_rec(i+1, depth+1, na, code | ((uint64_t)i << (8*depth)));
    }
}

static uint64_t choose(int n,int k){ uint64_t r=1; for(int i=0;i<k;i++){ r=r*(n-i)/(i+1);} return r; }

int main(int argc,char**argv){
    if(argc<3){ fprintf(stderr,"usage: %s atoms.bin a\n",argv[0]); return 1; }
    FILE*f=fopen(argv[1],"rb"); if(!f){perror("open");return 1;}
    uint32_t hdr[3]; if(fread(hdr,4,3,f)!=3){return 1;} dD=hdr[0]; nA=hdr[1]; nC=hdr[2];
    aK=atoi(argv[2]);
    A=malloc(sizeof(uint32_t)*32*nA); C=malloc(sizeof(uint32_t)*32*nC);
    if(fread(A,4,32*nA,f)!=(size_t)32*nA){return 1;}
    if(fread(C,4,32*nC,f)!=(size_t)32*nC){return 1;}
    fclose(f);
    uint64_t nsub=choose(nA,aK);
    uint64_t slots=1; while(slots < nsub*2) slots<<=1; if(slots<1024)slots=1024;
    MASK=slots-1;
    fprintf(stderr,"[d=%d fiber=%d] nA=%d nC=%d a=%d e=%d  anchorSubsets=%llu compSubsets=%llu slots=%llu(%.1fGB)\n",
        dD,dD,nA,nC,aK,dD*aK,(unsigned long long)nsub,(unsigned long long)choose(nC,aK),
        (unsigned long long)slots, slots*16.0/1e9);
    TBL_fp=calloc(slots,8); TBL_code=calloc(slots,8);
    if(!TBL_fp||!TBL_code){fprintf(stderr,"alloc fail\n");return 1;}
    struct timespec t0,t1,t2; clock_gettime(CLOCK_MONOTONIC,&t0);
    { uint32_t z[32]; memset(z,0,sizeof z); anchor_rec(0,0,z,0); }
    clock_gettime(CLOCK_MONOTONIC,&t1);
    { uint32_t z[32]; memset(z,0,sizeof z); comp_rec(0,0,z,0); }
    clock_gettime(CLOCK_MONOTONIC,&t2);
    double tb=(t1.tv_sec-t0.tv_sec)+(t1.tv_nsec-t0.tv_nsec)/1e9;
    double ts=(t2.tv_sec-t1.tv_sec)+(t2.tv_nsec-t1.tv_nsec)/1e9;
    fprintf(stderr,"anchorLeaves=%llu (%.1fs)  compLeaves=%llu (%.1fs)  fpProbes=%llu  HITS=%llu\n",
        (unsigned long long)nAnchorLeaves,tb,(unsigned long long)nCompLeaves,ts,
        (unsigned long long)nFpProbes,(unsigned long long)nHits);
    return 0;
}
