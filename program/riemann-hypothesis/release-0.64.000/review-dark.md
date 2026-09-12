# Frozen Riemann release: independent dark-view review

Reviewed 2026-09-12 against the frozen local release at `http://127.0.0.1:4182/`. No source, data, or UI changes were made. All filenames below are relative to the local archive `tmp/riemann-release-ui/`.

Result: no new material defect found in the reviewed views. Visual review covers 68 explicitly listed screenshots, not all 960 screenshots in the complete automated matrix.

- Dark EN and ES at 390x844 and 1600x900: sampled all six main tabs, including middle content, long-decimal tables, source comparisons, proof/triangle diagrams, scope paragraphs, and persisted experiment-record mathematics.
- Architecture: all four initial tabs inspected in those four dark scenarios. Method and Science correctly describe Riemann experiments, retained spectral stability, signed off-line pairs, triples with normalized span at most R, and the fixed-test/outer-limit order. RH and global-record boundaries remain explicit.
- New Method/Science lower diagrams and all bottom source links were then pointer-scrolled and visually inspected in EN/ES, light/dark, and both sizes: all 16 combinations passed. All four source-link centers hit the proper anchor, all links were inside the scroll panel, every panel reached its actual bottom, document dimensions matched the viewport, navigation stayed on one row, and no page error occurred. External links were hit-tested, not opened.
- The phone main tabs and proof controls use horizontal scrolling; the screenshots show the currently visible section of each row. The main long equations similarly use their own horizontal scroll area. The supplementary check here concerns modal vertical scrolling; separate earlier pointer evidence covers equation scrolling.
- Method/Science diagrams are fully visible at the modal bottom and their localized labels fit in both themes. Shared App/Deploy SVGs remain compact on phones and retain their existing English diagram labels; their surrounding prose is localized. This review did not change those repository-wide diagrams.

Automated evidence read: `390x844/receipt.json` and `1600x900/receipt.json` each report PASS for their four EN/ES x light/dark scenarios. Additional direct checks are in `architecture-lower/receipt.json` (16/16 PASS), produced by `review-architecture-lower.cjs` using normal Playwright clicks and mouse-wheel events. The supplementary script resolves Playwright through PLAYWRIGHT_MODULE or the package name and contains no local machine path.

## Exact screenshots visually inspected

### 1600x900/1600x900-en-dark

```text
002-summary-top.png
010-context-scroll-01.png
013-approaches-scroll-01.png
017-strategy-scroll-02.png
021-results-scroll-01.png
040-open-top.png
042-architecture-1.png
043-architecture-2.png
044-architecture-3.png
045-architecture-4.png
031-EXP-002-verdict.png
```

### 390x844/390x844-en-dark

```text
002-summary-top.png
004-summary-scroll-02.png
006-summary-scroll-04.png
014-context-scroll-02.png
021-approaches-scroll-03.png
027-strategy-scroll-03.png
029-strategy-scroll-05.png
034-results-scroll-03.png
061-open-scroll-01.png
064-architecture-1.png
065-architecture-2.png
066-architecture-3.png
067-architecture-4.png
039-EXP-001-verdict.png
054-EXP-002-complete-record-scroll-05.png
```

### 390x844/390x844-es-dark

```text
002-summary-top.png
004-summary-scroll-02.png
007-summary-scroll-05.png
015-context-scroll-02.png
021-approaches-scroll-02.png
029-strategy-scroll-03.png
032-strategy-scroll-06.png
039-results-scroll-04.png
067-open-scroll-02.png
070-architecture-1.png
071-architecture-2.png
072-architecture-3.png
073-architecture-4.png
044-EXP-001-verdict.png
059-EXP-002-complete-record-scroll-05.png
```

### 1600x900/1600x900-es-dark

```text
003-summary-scroll-01.png
010-context-scroll-01.png
013-approaches-scroll-01.png
018-strategy-scroll-03.png
022-results-scroll-02.png
041-open-scroll-01.png
042-architecture-1.png
043-architecture-2.png
044-architecture-3.png
045-architecture-4.png
035-EXP-002-complete-record-scroll-03.png
```

### architecture-lower

```text
390x844-en-light-method-bottom.png
390x844-en-light-science-bottom.png
390x844-en-dark-method-bottom.png
390x844-en-dark-science-bottom.png
390x844-es-light-method-bottom.png
390x844-es-light-science-bottom.png
390x844-es-dark-method-bottom.png
390x844-es-dark-science-bottom.png
1600x900-en-light-method-bottom.png
1600x900-en-light-science-bottom.png
1600x900-en-dark-method-bottom.png
1600x900-en-dark-science-bottom.png
1600x900-es-light-method-bottom.png
1600x900-es-light-science-bottom.png
1600x900-es-dark-method-bottom.png
1600x900-es-dark-science-bottom.png
```

Additional `architecture-lower/*-middle.png` captures were recorded during the pointer checks but are not included in the visual-review attestation above; the listed bottom captures display each complete four-stage diagram and all four source links.
