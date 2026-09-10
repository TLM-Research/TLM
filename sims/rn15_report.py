"""Generate the current RN-15 TLA report using exact integer accounting."""
import random
from rn15_tla import clear, check

BF = 30


def heading(text):
    print(f"\n{'='*78}\n{text}\n{'='*78}")


heading("1. A BLOCK UNDER CURRENT TLA - base_fee = 30 wei/gas")
block=[(200_000,150_000,60,8,400_000),(200_000,90_000,45,3,200_000),
       (100_000,50_000,50,2,0),(60_000,40_000,29,1,-200_000),
       (60_000,30_000,25,1,-400_000)]
rows,meta=clear(block,BF)
print(f"pool={meta['A']:,}; reserved={meta['reserved']:,}; settled={meta['used']:,}; "
      f"released={meta['released']:,}; refunded={meta['refunded']:,}")
print("side mf TLA band shortfall temporal total-paid per-gas")
for x in rows:
    temporal=x["pay_extra"] if x["side"]=="C" else (-x["S"] if x["side"]=="P" else 0)
    pg="-" if x["payment"] is None or not x["g"] else f"{x['payment']/x['g']:.6f}"
    print(x["side"],x["mf"],x["tla"],x["band"],x["s"],temporal,x["payment"],pg)
print("funding order:",meta["funding_order"],"execution order:",meta["execution_order"])
print("checks:",check(rows,meta) or "all pass")


heading("2. RESERVE AND SETTLE")
print("g_real reserved settled released pays_per_gas")
for g in (21_000,50_000,80_000,100_000):
    rows,meta=clear([(200_000,100_000,60,2,1_000_000),(100_000,g,25,0,-100_000)],BF)
    print(g,meta["reserved"],meta["used"],meta["released"],rows[1]["payment"]//g)


heading("3. NEGATIVE TLA CHANGES ORDERING, NOT SUBSIDY")
print("TLA band reservation settlement")
for tla in (-200_000,-400_000,-500_000,-900_000):
    rows,meta=clear([(200_000,100_000,60,2,1_000_000),(100_000,30_000,25,0,tla)],BF)
    print(tla,rows[1]["band"],rows[1]["R"],rows[1]["S"])


heading("4. IDENTICAL PROVIDERS: FULL SIGNED PRIORITY FEE")
A=1000
print("signed_priority need_each funded builder_revenue pool_to_base_shortfall")
for p in range(6):
    need=5+p; n=A//need
    print(p,need,n,n*p,n*5)


heading("5. HETEROGENEOUS PROVIDERS: BUILDER SELECTS SET, NOT TIP")
txs=[("consumer",100,1,40,0,1_000),("large",100,20,25,5,-100_000),
     ("small",20,20,25,4,-200_000)]
rows,meta=clear(txs,BF)
rev=sum(x["to_builder"] for x in rows if x["side"]=="P")
print("funded funding_order builder_provider_tip reservation")
print(meta["funded"],meta["funding_order"],rev,meta["reserved"])


heading("6. TLA INSIDE max_fee VERSUS A SEPARATE PAYMENT")
print("realised_g inside_max_fee separate")
for g in (21_000,150_000):
    inside=min(g*5, g*500_000//200_000)
    print(g,inside,500_000)
print("consumer_g inside_pool inside_funded separate_pool separate_funded")
for g in (21_000,60_000,150_000):
    inside=4*min(g*5, g*500_000//200_000)
    print(g,inside,inside>=300_000,2_000_000,True)


heading("7. EXACT PROPERTIES - 60,000 RANDOM BLOCKS")
properties=["provider price not max_fee","provider tip outside authorization",
            "provider priority fee not full signed maximum",
            "provider shortfall accounting","temporal charge outside TLA",
            "execution fee above max_fee","neutral charged temporal amount",
            "balance","pool overdrawn","negative payment",
            "provider funding order","TLA band order","block gas limit"]


def fuzz(n=60_000):
    rng=random.Random(11); failures={}
    for _ in range(n):
        bf=rng.choice([1,7,30,120,1000]); txs=[]
        for j in range(rng.randint(0,25)):
            L=rng.choice([21_000,60_000,200_000,1_000_000]); g=rng.randint(0,L)
            if rng.random()<.4:
                mf=rng.randrange(bf) if bf else 0
                txs.append((j,L,g,mf,rng.randint(0,min(5,mf)),-rng.randint(1,500_000_000)))
            else:
                mf=bf+rng.randint(0,60)
                txs.append((j,L,g,mf,rng.randint(0,min(20,mf)),
                            rng.choice([0,rng.randint(1,500_000_000)])))
        rows,meta=clear(txs,bf)
        for failure in check(rows,meta): failures[failure]=failures.get(failure,0)+1
    return failures


results=fuzz()
print("property violations")
for prop in properties:
    print(prop,results.get(prop,0))
print("blocks 60000")
