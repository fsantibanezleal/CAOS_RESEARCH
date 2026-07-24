# EXP-083: re-audit the 24 [125,150] configs vs the GGV2 excluded family + remark.
# Honest partition: EXCLUDED (sourced) / VERIFY (named but discrepant) / OPEN /
# DERIVATION-NEEDED (A0' unprinted). No claim beyond what the sources support.
fail=[]
def ck(n,ok,d=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {n}"+(f"  {d}" if d else ""),flush=True)
    if not ok: fail.append(n)

# (cfg, maxdeg, (degP,degQ), A0, A0'_printed or None, family)
CFG=[
 ("C01",125,(75,125),(5,20),(1,0),"F2 j=1"),
 ("C02",126,(84,126),(7,35),None,"sporadic L1"),
 ("C03",126,(126,84),(12,30),None,"sporadic L2"),
 ("C04",128,(96,128),(8,24),(2,0),"F24 j=0"),
 ("C05",132,(88,132),(11,33),None,"sporadic L1"),
 ("C06",135,(135,90),(9,36),None,"sporadic L1"),
 ("C07",135,(90,135),(9,36),None,"sporadic L1"),
 ("C08",135,(90,135),(12,33),None,"sporadic L1"),
 ("C09",135,(90,135),(9,36),None,"sporadic L2"),
 ("C10",140,(84,140),(7,21),(1,0),"F9 j=1"),
 ("C11",140,(56,140),(7,21),(1,0),"F11 j=0"),
 ("C12",144,(108,144),(8,28),None,"sporadic L1"),
 ("C13",144,(144,96),(8,40),None,"sporadic L2"),
 ("C14",144,(96,144),(12,36),None,"sporadic L2"),
 ("C15",144,(96,144),(12,36),None,"sporadic L2"),
 ("C16",144,(96,144),(12,36),None,"sporadic L2"),
 ("C17",144,(96,144),(12,36),None,"sporadic L2"),
 ("C18",144,(144,96),(12,36),None,"sporadic L3"),
 ("C19",147,(42,147),(6,15),(1,0),"F7 j=0"),
 ("C20",147,(63,147),(6,15),(1,0),"F8 j=0"),
 ("C21",147,(147,98),(7,42),None,"sporadic L1"),
 ("C22",147,(98,147),(7,42),None,"sporadic L1"),
 ("C23",150,(150,100),(10,40),None,"sporadic L2"),
 ("C24",150,(150,100),(10,40),None,"sporadic L2"),
]

def excluded_family(a,b):
    # wp(n',n'-1), n'>=2 : GGV2 Prop casos imposibles (rigorous)
    wp=a-b
    if wp<=0 or a%wp or b%wp: return False
    return a//wp>=2 and b//wp==a//wp-1

# GGV2 remark (tex ~1053) named A0-forcings to impossible A0':
REMARK_A0_EXCL={(10,25):"(2,1)",(14,35):"(6,3)/(3,2)",(7,21):"(2,1)",
                (8,28):"(8,4)? [B0=(8,28),B1=(8,40) only]",(9,21):"(9,6)",(6,15):"(6,3)? [B1=(6,18+6k) cond]"}

ck("1: (2,1),(3,2),(6,3),(8,4),(9,6) are excluded-family",
   all(excluded_family(*c) for c in [(2,1),(3,2),(6,3),(8,4),(9,6)]))
ck("1: (1,0),(2,0) NOT excluded ((t,0) always a possible last lower corner)",
   not excluded_family(1,0) and not excluded_family(2,0))

excluded=[]; verify=[]; openc=[]; derivneed=[]
for cfg,mx,deg,A0,A0p,fam in CFG:
    if cfg=="C13":
        excluded.append((cfg,"GGV2 remark: B0=(8,28),B1=(8,40)->A0'=(8,4) impossible"))
    elif A0p is not None and excluded_family(*A0p):
        excluded.append((cfg,f"printed A0'={A0p} in excluded family"))
    elif A0p is not None and A0 in REMARK_A0_EXCL:
        verify.append((cfg,f"A0={A0} named in GGV2 remark (->{REMARK_A0_EXCL[A0]}) BUT dossier prints A0'={A0p}: reconcile GGV5 vs GGV2 A0' notions"))
    elif A0p is not None:
        openc.append((cfg,f"printed A0'={A0p} not excluded (family case)"))
    elif A0 in REMARK_A0_EXCL:
        verify.append((cfg,f"A0={A0} named in GGV2 remark (->{REMARK_A0_EXCL[A0]}); A0' unprinted: derive the forcing (EXP-077 method) then apply"))
    else:
        derivneed.append((cfg,f"A0={A0}, A0' unprinted: force A0' via GGV1 Thm7.6 then test"))

print("\n=== PARTITION ===",flush=True)
print(f"EXCLUDED (sourced): {len(excluded)}")
for c,r in excluded: print(f"  {c}: {r}")
print(f"VERIFY (named/discrepant, source reconciliation): {len(verify)}")
for c,r in verify: print(f"  {c}: {r}")
print(f"OPEN (printed A0' not excluded): {len(openc)}")
for c,r in openc: print(f"  {c}: {r}")
print(f"DERIVATION-NEEDED (A0' unprinted, no remark match): {len(derivneed)}")
for c,r in derivneed: print(f"  {c}: {r}")
ck("2: all 24 configs partitioned", len(excluded)+len(verify)+len(openc)+len(derivneed)==24,
   f"{len(excluded)}+{len(verify)}+{len(openc)}+{len(derivneed)}")
print("RESULT: "+("ALL CHECKS PASS." if not fail else f"{len(fail)} FAILED: {fail}"),flush=True)
if fail: raise SystemExit(1)
