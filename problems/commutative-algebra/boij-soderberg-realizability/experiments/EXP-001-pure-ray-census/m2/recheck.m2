-- EXP-001 stage 1d: re-verify a saved hit in a fresh Macaulay2 process.
--   M2 --script recheck.m2 fresh HITFILE   rebuild the saved presentation over its own field, resolve, compare
--   M2 --script recheck.m2 qq HITFILE      repeat the construction over QQ with the generator matrix lifted to
--                                          symmetric integer representatives (same seed is not reused: the matrix is)
-- The comparison is betti res M == m * pureBettiDiagram L (exact degrees).
needsPackage "BoijSoederberg"
mode = scriptCommandLine#1
hitFile = scriptCommandLine#2
emit = s -> (stdio << s << endl << flush;)
csv = l -> demark(",", apply(toList l, toString))
txt = lines get hitFile
value txt#1
cc = #hitD - 1
Bt = pureBetti hitD
Bd = pureBettiDiagram hitD
kk = if hitP == 0 then QQ else ZZ/hitP
R = kk[a,b,c]
pres = apply(value txt#2, row -> apply(row, g -> sub(g, R)))
fmat = apply(value txt#3, row -> apply(row, g -> sub(g, R)))
t0 = cpuTime()
report = (okv, totals, extra) -> emit("{\"event\":\"recheck\",\"mode\":\"" | mode | "\",\"ok\":" | (if okv then "true" else "false")
    | ",\"totals\":[" | csv totals | "],\"ms\":" | toString(round((cpuTime()-t0)*1000)) | extra | "}")
if mode == "fresh" then (
    P = map(R^(#pres), R^{(#(pres#0)):-hitD#1}, pres);
    F = res coker P;
    report(betti F == hitM * Bd, apply(0..length F, i -> rank F_i), "")
) else (
    liftEntry = g -> apply(listForm g, t -> (e := lift(t#1, ZZ); {t#0, if e > hitP//2 then e - hitP else e}));
    lifted = apply(fmat, row -> apply(row, liftEntry));
    Q = QQ[a,b,c];
    toQ = tl -> 0_Q + sum(tl, t -> (t#1) * product(3, k -> (gens Q)#k^((t#0)#k)));
    mat = apply(lifted, row -> apply(row, toQ));
    if hitGen == "socle" then (
        r = last hitD - first hitD - cc;
        s = cc*r;
        mQ = ideal apply(gens Q, x -> x^(r+1));
        f = map(Q^(hitM*Bt_cc), Q^{hitM*Bt_0:-s+r}, mat);
        M = prune (image (f ** (Q^{s-r}/mQ)));
    ) else (
        M = coker map(Q^(hitM*Bt_0), Q^{hitM*Bt_1:-hitD#1}, mat);
    );
    if M == 0 then report(false, {}, ",\"reason\":\"zero module\"")
    else (
        F = res M;
        report(betti F == hitM * Bd, apply(0..length F, i -> rank F_i), "")
    )
)
