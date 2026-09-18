"""Write results-table.tex from the EXP-007 result files (no LaTeX passes through a shell)."""

import io
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ART = HERE.parents[2] / "problems/combinatorics/petersen-coloring/experiments/EXP-007-colorable-only-by-itself/artifacts"
BS = chr(92)
NAMES = {"G52": BS + "Ga", "G52b": BS + "Gb", "G68": BS + "Gsix"}


def fmt(n) -> str:
    s = f"{int(n):,}"
    return s.replace(",", "{,}")


def rows(graph: str) -> list[str]:
    out = []
    files = sorted(ART.glob(f"result-{graph}-k*.json"), key=lambda p: -int(p.stem.split("-k")[1]))
    for p in files:
        d = json.loads(p.read_text(encoding="utf-8"))
        if d.get("status") != "UNSAT" or not d.get("verified"):
            continue
        out.append(" & ".join([
            "$" + NAMES[graph] + "$", str(d["k"]), fmt(d["variables"]), fmt(d["clauses"]),
            f"{d['certify_solve_seconds']:,.0f}".replace(",", "{,}"), fmt(d["proof_bytes"]),
            f"{d['check_seconds']:,.0f}".replace(",", "{,}"),
        ]) + " " + BS + BS)
    return out


def main() -> None:
    lines = [BS + "begin{table}[h]" + BS + "centering" + BS + "small",
             BS + "begin{tabular}{lrrrrrr}", BS + "toprule",
             "graph & $k$ & variables & clauses & solve (s) & proof (bytes) & check (s)" + BS + BS, BS + "midrule"]
    for i, g in enumerate(("G52", "G52b", "G68")):
        r = rows(g)
        if r and i and lines[-1] != BS + "midrule":
            lines.append(BS + "midrule")
        lines += r
    lines += [BS + "bottomrule", BS + "end{tabular}",
              BS + "caption{Target orders $k$ refuted with DRAT proofs accepted by " + BS + "texttt{drat-trim}. The formula "
              "of order $k$ is unsatisfiable: no loopless cubic graph on $k$ vertices colors the graph with a vertex map of "
              "kind (O), (E0) or (E1). Times were measured while other computations shared the machine.}" + BS + "label{tab:orders}",
              BS + "end{table}"]
    io.open(HERE / "results-table.tex", "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    for g in ("G52", "G52b", "G68"):
        ks = sorted(int(p.stem.split("-k")[1]) for p in ART.glob(f"result-{g}-k*.json")
                    if json.loads(p.read_text(encoding="utf-8")).get("verified") and json.loads(p.read_text(encoding="utf-8")).get("status") == "UNSAT")
        print(g, ks)


if __name__ == "__main__":
    main()
