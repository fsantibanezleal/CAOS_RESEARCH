-- EXP-001 search cell runner (stages 1b, 1c, 1e). One process handles the cells of one ray, one line each:
--   <L csv> <m> <socle|module> <seed> <p>          (p = 0 means QQ)
-- usage: M2 --script cells.m2 CELLS_FILE OUT_DIR
-- Every cell prints a flushed JSON line "start" then "done". A hit (betti res M == m * pureBettiDiagram L, exact
-- degrees) saves the presentation and the generator matrix to OUT_DIR as <tag>.hit.m2 and <tag>.sing.
-- The two generators replicate randomSocleModule and randomModule of BoijSoederberg.m2 (file SHA-256 in
-- hypothesis.md) line by line, so that the random matrix f is available for the QQ lift.
needsPackage "BoijSoederberg"
cellsFile = scriptCommandLine#1
outDir = scriptCommandLine#2
emit = s -> (stdio << s << endl << flush;)
csv = l -> demark(",", apply(toList l, toString))
jl = l -> "[" | csv l | "]"

entriesText = P -> toString apply(entries P, row -> apply(row, toString))

runCell = (L, m, gen, seed, p) -> (
    tag := demark("-", apply(L, toString)) | "_m" | toString m | "_" | gen | "_s" | toString seed | "_p" | toString p;
    base := "{\"d\":" | jl L | ",\"m\":" | toString m | ",\"gen\":\"" | gen | "\",\"seed\":" | toString seed | ",\"p\":" | toString p;
    emit(base | ",\"event\":\"start\"}");
    t0 := cpuTime();
    setRandomSeed seed;
    c := #L - 1;
    kk := if p == 0 then QQ else ZZ/p;
    R := kk[vars(0..c-1)];
    Bt := pureBetti L;
    Bd := pureBettiDiagram L;
    outcome := "miss"; reason := ""; totals := {}; files := {};
    (M, F) := (null, null);
    FM := null;
    ok := try (
        if gen == "socle" then (
            r := last L - first L - c;
            s := c*r;
            mR := ideal apply(gens R, x -> x^(r+1));
            FM = random(R^(m*Bt_c), R^{m*Bt_0:-s+r});
            M = prune (image (FM ** (R^{s-r}/mR)));
        ) else (
            FM = random(R^{m*Bt_0:-L_0}, R^{m*Bt_1:-L_1});
            M = coker FM;
        );
        true) else false;
    if not ok then (outcome = "error"; reason = "construction failed")
    else if M == 0 then (outcome = "miss"; reason = "zero module")
    else (
        res0 := try (F = res M; true) else false;
        if not res0 then (outcome = "error"; reason = "resolution failed")
        else (
            totals = apply(0..length F, i -> rank F_i);
            if betti F == m * Bd then (
                outcome = "hit";
                P := presentation M;
                B0 := numrows P; B1 := numcols P;
                f1 := outDir | "/" | tag | ".hit.m2";
                f1 << "-- EXP-001 hit " << tag << endl
                   << "hitD = " << toString L << "; hitM = " << m << "; hitGen = \"" << gen << "\"; hitSeed = " << seed << "; hitP = " << p << ";" << endl
                   << "hitPres = " << entriesText P << ";" << endl
                   << "hitF = " << entriesText FM << ";" << endl << close;
                f2 := outDir | "/" | tag | ".sing";
                f2 << "ring r=" << (if p == 0 then 0 else p) << ",(" << demark(",", apply(gens R, toString)) << "),dp;" << endl
                   << "matrix P[" << B0 << "][" << B1 << "]=" << demark(",", apply(flatten entries P, toString)) << ";" << endl
                   << "module M=module(P);" << endl << close;
                files = {tag | ".hit.m2", tag | ".sing"};
            ) else (
                reason = "table differs";
                if dim M > 0 then reason = "table differs; module not of finite length";
            );
        );
    );
    secs := cpuTime() - t0;
    emit(base | ",\"event\":\"done\",\"outcome\":\"" | outcome | "\",\"reason\":\"" | reason | "\",\"totals\":" | jl totals
        | ",\"ms\":" | toString(round(secs*1000)) | ",\"files\":[" | demark(",", apply(files, x -> "\"" | x | "\"")) | "]}");
    );

for line in lines get cellsFile do if #line > 0 then (
    parts := separate(" ", line);
    L := value("{" | parts#0 | "}");
    runCell(L, value parts#1, parts#2, value parts#3, value parts#4);
    );
emit("{\"event\":\"finished\"}");
