-- EXP-001 stage 1a (gate G3): the known answers, with the package's own generators.
--   M2 --script known.m2 P      P = 101, 32003 or 0 (QQ)
needsPackage "BoijSoederberg"
p = value scriptCommandLine#1
kk = if p == 0 then QQ else ZZ/p
emit = s -> (stdio << s << endl << flush;)
item = (label, okv, detail, t0, cell) -> emit("{\"event\":\"known\",\"p\":" | toString p | ",\"label\":\"" | label | "\",\"ok\":"
    | (if okv then "true" else "false") | ",\"detail\":\"" | detail | "\",\"cell\":\"" | cell | "\",\"ms\":" | toString(round((cpuTime()-t0)*1000)) | "}")
tab = l -> new BettiTally from l
pureHit = (L, m, M) -> M != 0 and betti res M == m * pureBettiDiagram L
gens2 = {"socle", "module"}
mk = (gen, L, m) -> if gen == "socle" then randomSocleModule(L, m, CoefficientRing => kk) else randomModule(L, m, CoefficientRing => kk)

-- the eight documentation rays of Table A at m = 1 (either generator, seeds 1 to 3)
for L in {{0,1,3,6},{0,2,3,6},{0,3,4,6},{0,3,5,6},{0,4,5,7},{0,2,3,7},{0,2,3,9},{0,6,7,9}} do (
    t0 := cpuTime(); found := ""; cell := "";
    for gen in gens2 do for seed from 1 to 3 do if found == "" then (
        setRandomSeed seed;
        if pureHit(L, 1, mk(gen, L, 1)) then (found = gen | " seed " | toString seed;
            cell = demark(",", apply(L, toString)) | " 1 " | gen | " " | toString seed));
    item("doc ray " | toString L | " m=1", found != "", found, t0, cell));

-- randomModule({0,4,9,10}, m): m = 1 gives the Koszul table, m = 2, 3 give m times the pure diagram (Table B)
t0 = cpuTime(); setRandomSeed 1; L = {0,4,9,10};
koszulT = tab {(0,{0},0) => 1, (1,{4},4) => 3, (2,{8},8) => 3, (3,{12},12) => 1};
item("randomModule (0,4,9,10) m=1 is the Koszul table", betti res randomModule(L, 1, CoefficientRing => kk) == koszulT, "", t0, "");
for m in {2,3} do (t0 = cpuTime(); setRandomSeed 1;
    item("randomModule (0,4,9,10) m=" | toString m | " is " | toString m | " x pure", pureHit(L, m, randomModule(L, m, CoefficientRing => kk)), "", t0, "0,4,9,10 " | toString m | " module 1"));

-- the Ext^3 dual of that m=2 module has the table 2 x pure of the dual ray (0,1,6,10) (G6, second ray)
t0 = cpuTime(); setRandomSeed 1;
M = randomModule(L, 2, CoefficientRing => kk); R = ring M;
N = Ext^3(M, R^{-10});
item("Ext^3 of randomModule (0,4,9,10) m=2 has 2 x pure (0,1,6,10)", betti res prune N == 2 * pureBettiDiagram {0,1,6,10}, "", t0, "");

-- package tests 16
t0 = cpuTime(); setRandomSeed 1; L = {0,1,3,4};
t14 = tab {(0,{0},0) => 1, (1,{1},1) => 2, (2,{2},2) => 1, (1,{2},2) => 1, (2,{3},3) => 2, (3,{4},4) => 1};
item("randomSocleModule (0,1,3,4) m=1 is the non-pure table", betti res randomSocleModule(L, 1, CoefficientRing => kk) == t14, "", t0, "");
for m in {2,3} do (t0 = cpuTime(); setRandomSeed 1;
    item("randomSocleModule (0,1,3,4) m=" | toString m | " is " | toString m | " x pure", pureHit(L, m, randomSocleModule(L, m, CoefficientRing => kk)), "", t0, "0,1,3,4 " | toString m | " socle 1"));
for m in {1,2,3} do (t0 = cpuTime(); setRandomSeed 1;
    item("randomSocleModule (0,2,3,6) m=" | toString m | " is " | toString m | " x pure", pureHit({0,2,3,6}, m, randomSocleModule({0,2,3,6}, m, CoefficientRing => kk)), "", t0, "0,2,3,6 " | toString m | " socle 1"));
emit("{\"event\":\"finished\"}");
