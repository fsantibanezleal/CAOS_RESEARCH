"""EXP-024 P2/P3: comment-aware static scan of Tomar's stored Lean sources for kernel-bypass constructs.

Usage (from the repository root):
  .venv/Scripts/python.exe problems/dynamical-systems/central-configurations/experiments/EXP-024-five-body-claims-audit/scan.py <lean_full root>
The Lean sources are read as text; nothing is executed. Writes artifacts/scan.json.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PATTERNS = {
    "sorry": r"\bsorry\b",
    "admit": r"\badmit\b",
    "axiom_declaration": r"^\s*(?:private\s+|protected\s+|noncomputable\s+)*axiom\s",
    "native_decide": r"\bnative_decide\b",
    "implemented_by": r"implemented_by",
    "extern": r"@\[\s*extern",
    "ofReduceBool": r"ofReduceBool",
    "unsafe": r"\bunsafe\b",
    "debug_skipKernelTC": r"skipKernelTC|debug\.skipKernelTC",
}


def strip_comments(text: str) -> str:
    """Remove Lean block comments (nested /- ... -/) and line comments (-- ...), keeping line numbers."""
    out, depth, i, n = [], 0, 0, len(text)
    in_string = False
    while i < n:
        two = text[i:i + 2]
        ch = text[i]
        if depth == 0 and not in_string and ch == '"':
            in_string = True
            out.append(ch)
            i += 1
            continue
        if in_string:
            if ch == "\\" and i + 1 < n:
                out.append(text[i:i + 2])
                i += 2
                continue
            if ch == '"':
                in_string = False
            out.append(ch)
            i += 1
            continue
        if two == "/-":
            depth += 1
            i += 2
            continue
        if depth > 0 and two == "-/":
            depth -= 1
            i += 2
            continue
        if depth > 0:
            out.append("\n" if ch == "\n" else " ")
            i += 1
            continue
        if two == "--":
            j = text.find("\n", i)
            j = n if j == -1 else j
            out.append(" " * (j - i))
            i = j
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def main() -> int:
    root = Path(sys.argv[1])
    files = sorted(root.rglob("*.lean"))
    hits = []
    for f in files:
        code = strip_comments(f.read_text(encoding="utf-8", errors="replace"))
        for lineno, line in enumerate(code.splitlines(), 1):
            for name, pat in PATTERNS.items():
                if re.search(pat, line):
                    hits.append({"file": str(f.relative_to(root)).replace("\\", "/"), "line": lineno,
                                 "pattern": name, "text": line.strip()[:200]})
    main_file = root / "CC5Full/Core/Compose/Main.lean"
    deps = sorted(set(re.findall(r"^import\s+(\S+)", main_file.read_text(encoding="utf-8"), re.M)))
    missing = []
    for d in deps:
        path = root / (d.replace(".", "/") + ".lean")
        if not path.exists():
            missing.append(d)
    generated_dirs = ["CC5Full/Core/E3/Run", "CC5Full/Core/Strata/Big/F1_2_3_4_5", "CC5Full/Core/ResidualCert/All",
                      "CC5Full/Core/D14a/B"]
    present = {g: (root / g).exists() and any((root / g).rglob("*.lean")) for g in generated_dirs}
    out = {"files_scanned": len(files), "hits": hits, "hit_count": len(hits),
           "by_pattern": {p: sum(1 for h in hits if h["pattern"] == p) for p in PATTERNS},
           "main_imports": deps, "main_imports_missing_from_stored_sources": missing,
           "generated_families_present_in_stored_sources": present}
    (HERE / "artifacts").mkdir(exist_ok=True)
    (HERE / "artifacts" / "scan.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "hits"}, indent=1))
    for h in hits[:40]:
        print(h)
    return 0


if __name__ == "__main__":
    sys.exit(main())
