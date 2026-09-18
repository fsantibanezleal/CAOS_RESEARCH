"""Fail when a manuscript talks about itself instead of the science.

Binding rule: conventions/manuscript-scientific-voice.md. A manuscript body describes the
problem, method, experiments, results, limits and conclusions. It does not narrate its own
versions, its Zenodo deposit, or the working vocabulary of the process that produced it
("honest", "verdict", "campaign", "ledger", "smoke gate", ...).

What is scanned: every .tex file under the given paths (a directory is walked recursively;
`versions/` snapshots are skipped). What is exempt:
  * the preamble, except \\title{...}, which is checked for self-assessment words;
  * the page-1 front matter between \\begin{document} and the abstract (or the first
    \\section), for DOI, Zenodo and version tokens only (the header block lives there);
  * running-header and metadata lines (\\fancyhead, \\markboth, \\date, DOI macros);
  * the bibliography (thebibliography environment, \\bibliography, .bib files);
  * the paragraph that starts with "Declaration of generative AI use", for AI terms;
  * any line carrying the marker `% voice-ok` (a reviewed, legitimate use, for example the
    archive of an external work cited in running text).

Usage:
    python tools/zenodo/check_manuscript_voice.py <tex-dir-or-file> [...]
Exit status 0 when clean, 1 when any finding remains.
"""
import re
import sys
from pathlib import Path

FLAGS = re.IGNORECASE

# (rule, regex) pairs. Word boundaries keep "gradient deposited", "ore deposit", circuit
# "gates" and "audit of the published claims" out of the net; those are science.
VERSION_TOKENS = [
    ("version-narrative", r"\bthis (version|revision|release)\b"),
    ("version-narrative", r"\b(earlier|previous|prior|first|last|next|new|later|future) (versions?|revisions?) of (this|the) (paper|manuscript|note|report|record|preprint|document)\b"),
    ("version-narrative", r"\b(an?|the) (earlier|previous|prior) (version|revision)s?\b"),
    ("version-narrative", r"\bnew in this\b"),
    ("version-narrative", r"\bwhen this (version|paper|manuscript) was frozen\b"),
    ("version-narrative", r"\bv\d+\.\d+\b"),
    ("version-narrative", r"\bversion \d+\.\d+\b"),
    # Integer versions ("Correction to version 1") and retraction verbs: the convention forbids
    # "we withdraw the earlier statement", and a correction section written with "withdrawn" and
    # "version 1" passed every pattern above (found 2026-09-17 on espira/beyond-macrospin).
    ("version-narrative", r"\bversion \d+\b"),
    ("version-narrative", r"\bwithdraw(n|s|ing)?\b"),
    ("deposit-narrative", r"\bzenodo\b"),
    ("deposit-narrative", r"\b(concept|version) doi\b"),
]
ALWAYS = [
    ("document-as-artifact", r"\bthis (manuscript|record)\b"),
    ("document-as-artifact", r"\bmachine record\b"),
    ("document-as-artifact", r"\bpurpose-driven\b"),
    ("document-as-artifact", r"\bcontributions of this\b"),
    ("process-vocabulary", r"\bcampaigns?\b"),
    ("process-vocabulary", r"\bverdicts?\b"),
    ("process-vocabulary", r"\bledgers?\b"),
    ("process-vocabulary", r"\bdossiers?\b"),
    ("process-vocabulary", r"\bsmoke[- ]?(run|test|gate|check)s?\b"),
    ("process-vocabulary", r"\b(declared|regression|smoke) (gate|budget|hypothes[ie]s|campaign|regression gate)s?\b"),
    ("process-vocabulary", r"\bhypothes[ie]s (were |was |are )?(declared|committed)\b"),
    ("process-vocabulary", r"\bdeclared (before|in advance)\b"),
    ("process-vocabulary", r"\b\d+-(second|minute|hour) gate\b"),
    ("process-vocabulary", r"\bno-ship\b|\bship rules?\b|\bship rule\b"),
    ("process-vocabulary", r"\bsessions?\b"),
    ("process-vocabulary", r"\bcommissioned\b"),
    ("process-vocabulary", r"\badversarial (review|audit|validation|pass|reasoning|calibration|support|check|control|corruption|mutation|negation|novelty)s?\b"),
    ("process-vocabulary", r"\bRESUME\b|\bwip/|\bmethodology/\d"),
    ("self-assessment", r"\bhonest(ly|y)?\b"),
    ("self-assessment", r"\bon the record\b"),
    ("self-assessment", r"\bover-?claim"),
    ("self-assessment", r"\bbelievable\b"),
    ("ai-narrative", r"\b(ai assistance|automated assistants?|generative ai|claude)\b"),
    ("em-dash", r"(?<!-)---(?!-)|\u2014"),
]
TITLE_ONLY = [("self-assessment", r"\bhonest(ly|y)?\b")]

HEADER_LINE = re.compile(
    r"\\fancyhead|\\markboth|\\markright|\\date\s*\{|\\hypersetup|pdfauthor|pdftitle|"
    r"\\newcommand\s*\{\\(doc|version|concept|Version|Concept)\w*\}|\\renewcommand\s*\{\\doc",
)
COMMENT = re.compile(r"(?<!\\)%.*$")


def strip_comment(line: str) -> str:
    return COMMENT.sub("", line)


def scan_file(path: Path):
    findings = []
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    has_document = "\\begin{document}" in text
    in_preamble = has_document
    in_front = False
    in_bib = False
    in_ai_decl = False
    for n, raw in enumerate(lines, 1):
        if "voice-ok" in raw:
            continue
        line = strip_comment(raw)
        if "\\begin{document}" in line:
            in_preamble, in_front = False, True
            continue
        if in_front and re.search(r"\\begin\{abstract\}|\\section\*?\{|\\begin\{IEEEkeywords\}", line):
            in_front = False
        if "\\begin{thebibliography}" in line:
            in_bib = True
        if in_bib:
            if "\\end{thebibliography}" in line:
                in_bib = False
            continue
        if re.search(r"\\bibliography\{|\\printbibliography", line):
            continue
        if re.search(r"Declaration of generative AI use", line, FLAGS):
            in_ai_decl = True
        elif in_ai_decl and not line.strip():
            in_ai_decl = False
        if in_preamble:
            if re.search(r"\\title\s*[\[{]", line):
                for rule, rx in TITLE_ONLY:
                    for m in re.finditer(rx, line, FLAGS):
                        findings.append((n, rule, m.group(0), raw.strip()))
            continue
        header_line = bool(HEADER_LINE.search(line))
        rules = list(ALWAYS)
        if not (in_front or header_line):
            rules += VERSION_TOKENS
        for rule, rx in rules:
            if rule == "ai-narrative" and in_ai_decl:
                continue
            if rule == "em-dash" and header_line and "---" not in line:
                continue
            for m in re.finditer(rx, line, 0 if rule == "process-vocabulary" and rx.startswith(r"\bRESUME") else FLAGS):
                findings.append((n, rule, m.group(0), raw.strip()))
    return findings


def iter_tex(paths):
    for p in paths:
        p = Path(p)
        if p.is_dir():
            for f in sorted(p.rglob("*.tex")):
                if "versions" in f.relative_to(p).parts:
                    continue
                yield f
        elif p.suffix == ".tex":
            yield p


def main(argv):
    if not argv:
        sys.exit(__doc__)
    total = 0
    for f in iter_tex(argv):
        for n, rule, hit, raw in scan_file(f):
            total += 1
            print(f"{f}:{n}: [{rule}] '{hit}' | {raw[:160]}")
    if total:
        print(f"\n{total} finding(s). See conventions/manuscript-scientific-voice.md.")
        return 1
    print("manuscript voice: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
