-- EXP-001 gate G1: print Macaulay2's pureBetti and pureAll for the 220 rays (compared by census.py --check-m2).
needsPackage "BoijSoederberg"
csv = l -> demark(",", apply(toList l, toString))
for d1 from 1 to 10 do for d2 from d1+1 to 11 do for d3 from d2+1 to 12 do (
    L = {0,d1,d2,d3};
    print("RAY|" | csv L | "|" | csv pureBetti L | "|" | csv pureAll L);
    );
print("G7|" | toString pureCharFree {0,4,9,13});
