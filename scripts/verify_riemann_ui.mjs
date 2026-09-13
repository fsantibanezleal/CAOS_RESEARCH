#!/usr/bin/env node
/**
 * Pointer-driven Riemann replay QA. No storage injection, forced clicks, or
 * React-state mutation is used. Start a baked frontend separately, then run:
 *
 *   node scripts/verify_riemann_ui.mjs --base-url http://127.0.0.1:4173 \
 *     --output-dir tmp/riemann-ui-review
 *
 * Install Playwright in the invoking project, or set PLAYWRIGHT_MODULE to a
 * resolvable package name, package directory, or module entry file. No local
 * machine path is part of the committed harness.
 *
 * Default coverage: 1440x1000 and 390x844, EN/ES, light/dark, all six tabs.
 * --adr-viewports adds ADR-0071's 1280x800, 1600x900, and 2560x1440 sizes.
 * --content-screenshots all captures every successive panel viewport; the
 * default top-bottom mode also captures every exercised interactive state.
 * A passing receipt is automated evidence, not a claim of human visual review.
 */
import { createHash } from 'node:crypto';
import { existsSync, statSync } from 'node:fs';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

const SCRIPT = fileURLToPath(import.meta.url);
const ROOT = path.resolve(path.dirname(SCRIPT), '..');
const argv = process.argv.slice(2);
const options = {
  baseUrl: process.env.RIEMANN_UI_BASE_URL || 'http://127.0.0.1:4173',
  outputDir: null,
  headed: false,
  adr: false,
  overwrite: false,
  contentScreenshots: 'top-bottom',
  viewports: [{ width: 1440, height: 1000 }, { width: 390, height: 844 }],
};
function usage() {
  console.log(`Usage: node scripts/verify_riemann_ui.mjs --output-dir DIR [options]
  --base-url URL                 Existing baked frontend (default 127.0.0.1:4173)
  --viewports WxH,WxH            Override the requested two-size matrix
  --adr-viewports                Add 1280x800, 1600x900, 2560x1440
  --content-screenshots MODE     top-bottom (default) or all
  --headed                      Show the controlled Chromium window
  --overwrite                   Allow an existing receipt output directory
  --help                        Print this help without opening a browser
Environment: PLAYWRIGHT_MODULE overrides portable Playwright resolution.
Exit 0 means all automated gates passed; exit 1 includes a saved failure receipt.`);
}
function valueAfter(index, option) {
  const value = argv[index + 1];
  if (!value || value.startsWith('--')) throw new Error(`${option} requires a value`);
  return value;
}
for (let i = 0; i < argv.length; i += 1) {
  const arg = argv[i];
  if (arg === '--help') { usage(); process.exit(0); }
  if (arg === '--output-dir') options.outputDir = valueAfter(i++, arg);
  else if (arg === '--base-url') options.baseUrl = valueAfter(i++, arg);
  else if (arg === '--content-screenshots') options.contentScreenshots = valueAfter(i++, arg);
  else if (arg === '--viewports') {
    options.viewports = valueAfter(i++, arg).split(',').map((entry) => {
      const match = /^(\d+)x(\d+)$/.exec(entry);
      if (!match || Number(match[1]) < 320 || Number(match[2]) < 480) {
        throw new Error(`Invalid viewport ${entry}; minimum 320x480`);
      }
      return { width: Number(match[1]), height: Number(match[2]) };
    });
  } else if (arg === '--headed') options.headed = true;
  else if (arg === '--adr-viewports') options.adr = true;
  else if (arg === '--overwrite') options.overwrite = true;
  else throw new Error(`Unknown argument: ${arg}`);
}
if (!options.outputDir) { usage(); throw new Error('--output-dir is required'); }
if (!['top-bottom', 'all'].includes(options.contentScreenshots)) {
  throw new Error('--content-screenshots must be top-bottom or all');
}
if (options.adr) options.viewports.push(
  { width: 1280, height: 800 }, { width: 1600, height: 900 }, { width: 2560, height: 1440 },
);
options.viewports = [...new Map(options.viewports.map((v) => [`${v.width}x${v.height}`, v])).values()];
const base = new URL(options.baseUrl);
if (!['http:', 'https:'].includes(base.protocol)) throw new Error('Base URL must be HTTP(S)');
const out = path.resolve(options.outputDir);
const receiptPath = path.join(out, 'receipt.json');
if (existsSync(receiptPath) && !options.overwrite) {
  throw new Error(`Receipt exists at ${receiptPath}; choose a fresh directory or --overwrite`);
}
await mkdir(out, { recursive: true });
const started = new Date().toISOString();
const receipt = {
  schema: 'riemann-pointer-ui-qa-v1', started_utc: started, finished_utc: null,
  base_url: base.href, output_directory: out,
  script_sha256: createHash('sha256').update(await readFile(SCRIPT)).digest('hex'),
  requested_viewports: options.viewports, languages: ['en', 'es'], themes: ['light', 'dark'],
  evidence_scope: {
    pointer_navigation: 'Program portfolio link to Riemann; mouse move/down/up with hit testing',
    language_theme: 'Actual shell controls; no injected storage or application state',
    content_screenshots: options.contentScreenshots,
    visual_review: 'Screenshots recorded for separate human/agent inspection; not automatically attested',
    adr_0071_sizes_covered: ['1280x800', '1600x900', '2560x1440'].every((key) =>
      options.viewports.some((v) => `${v.width}x${v.height}` === key)),
    viewport_gate: 'Riemann route and open dialogs; legacy Program dimensions are recorded, not certified',
    workbench_viz_area_gate: 'Not applied: this is a research prose replay, not an App/focus instrument',
  },
  scenarios: [], fatal_error: null, passed: false,
};
const labels = {
  en: {
    language: 'Switch language', theme: 'Toggle light / dark',
    problem: 'Riemann hypothesis', heading: 'Riemann zeta: zeros in short intervals',
    architecture: 'Architecture / How it works', close: 'Close',
    hypothesis: 'Hypothesis (declared before the run)', verdict: 'Verdict (persisted after the run)',
    tabs: ['Summary', 'Context & history', 'References & approaches', 'Strategy', 'Experiments & results', 'Open questions'],
  },
  es: {
    language: 'Cambiar idioma', theme: 'Cambiar claro / oscuro',
    problem: 'Hipótesis de Riemann', heading: 'Zeta de Riemann: ceros en intervalos cortos',
    architecture: 'Arquitectura / Cómo funciona', close: 'Cerrar',
    hypothesis: 'Hipotesis (declarada antes de la corrida)', verdict: 'Veredicto (persistido despues de la corrida)',
    tabs: ['Resumen', 'Contexto e historia', 'Referencias y enfoques', 'Estrategia', 'Experimentos y resultados', 'Preguntas abiertas'],
  },
};
const tabIds = ['summary', 'context', 'approaches', 'strategy', 'results', 'open'];
const norm = (text) => String(text ?? '').replace(/\s+/g, ' ').trim();
const shortError = (error) => String(error?.stack || error);
const slug = (text) => String(text).replace(/[^a-zA-Z0-9_-]+/g, '-').replace(/^-|-$/g, '').slice(0, 100);
let browser;

async function loadPlaywright() {
  const require = createRequire(import.meta.url);
  const override = process.env.PLAYWRIGHT_MODULE;
  if (override) {
    let resolved = override;
    if (existsSync(override)) {
      resolved = statSync(override).isDirectory() ? require.resolve(path.resolve(override)) : path.resolve(override);
      return import(pathToFileURL(resolved).href);
    }
    return import(override);
  }
  const failures = [];
  for (const name of ['playwright', 'playwright-core']) {
    try { return await import(name); } catch (error) { failures.push(`${name}: ${error.code || error.message}`); }
  }
  const frontendRequire = createRequire(path.join(ROOT, 'frontend', 'package.json'));
  try { return await import(pathToFileURL(frontendRequire.resolve('playwright')).href); }
  catch (error) { failures.push(`frontend resolution: ${error.code || error.message}`); }
  throw new Error(`Playwright unavailable. Install it or set PLAYWRIGHT_MODULE. ${failures.join('; ')}`);
}
async function saveReceipt() {
  receipt.finished_utc = new Date().toISOString();
  receipt.passed = !receipt.fatal_error && receipt.scenarios.length === options.viewports.length * 4
    && receipt.scenarios.every((s) => s.completed && !s.failures.length);
  await writeFile(receiptPath, `${JSON.stringify(receipt, null, 2)}\n`);
}
function check(scenario, name, condition, details = null) {
  const item = { name, passed: Boolean(condition), details };
  scenario.checks.push(item);
  if (!condition) scenario.failures.push(item);
  return condition;
}
function requireCondition(condition, message) {
  if (!condition) throw new Error(message);
}
async function settle(page) {
  await page.evaluate(() => new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve))));
  await page.waitForTimeout(65);
}
async function pointerClick(page, locator, scenario, name) {
  await locator.waitFor({ state: 'visible', timeout: 20000 });
  requireCondition(await locator.isEnabled(), `Disabled pointer target: ${name}`);
  // Native scrolling only reveals the existing control; the state change is
  // always produced by actual pointer events, never dispatchEvent or evaluate.
  await locator.scrollIntoViewIfNeeded();
  // A wrapped inline anchor has one client rectangle per rendered line. The
  // center of their union can be a line-height gap belonging to the table cell,
  // even though both text fragments are genuinely clickable. Choose a point
  // inside an actual visible fragment and keep the real browser hit test.
  const point = await locator.evaluate((el) => {
    const rects = [...el.getClientRects()].map((r) => ({
      left: Math.max(1, r.left), top: Math.max(1, r.top),
      right: Math.min(innerWidth - 1, r.right), bottom: Math.min(innerHeight - 1, r.bottom),
    })).filter((r) => r.right > r.left && r.bottom > r.top)
      .sort((a, b) => (b.right - b.left) * (b.bottom - b.top)
        - (a.right - a.left) * (a.bottom - a.top));
    const attempts = [];
    for (const [index, r] of rects.entries()) {
      for (const [fx, fy] of [[0.5, 0.5], [0.25, 0.5], [0.75, 0.5], [0.5, 0.25], [0.5, 0.75]]) {
        const x = r.left + (r.right - r.left) * fx;
        const y = r.top + (r.bottom - r.top) * fy;
        const top = document.elementFromPoint(x, y);
        const hit = top ? `${top.tagName}.${top.className?.baseVal ?? top.className}` : null;
        attempts.push({ x, y, hit });
        if (top && (top === el || el.contains(top))) {
          return { x, y, hit, client_rect_index: index, visible_client_rects: rects, attempts };
        }
      }
    }
    return { x: null, y: null, visible_client_rects: rects, attempts };
  });
  requireCondition(point.x !== null && point.y !== null,
    `No visible pointer-hit point for ${name}: ${JSON.stringify(point)}`);
  const { x, y } = point;
  await page.mouse.move(x, y, { steps: 8 });
  // Recheck after the pointer walk so hover-driven overlays cannot silently
  // invalidate the selected point before mouse-down.
  const hit = await locator.evaluate((el, point) => {
    const top = document.elementFromPoint(point.x, point.y);
    return { matches: Boolean(top && (top === el || el.contains(top))),
      top: top ? `${top.tagName}.${top.className?.baseVal ?? top.className}` : null };
  }, { x, y });
  requireCondition(hit.matches, `Pointer target occluded: ${name}; hit ${hit.top}`);
  await page.mouse.down();
  await page.mouse.up();
  scenario.pointer_actions.push({ name, x, y, url: page.url(), hit: hit.top,
    client_rect_index: point.client_rect_index, visible_client_rects: point.visible_client_rects });
  await settle(page);
}

async function domSnapshot(page) {
  return page.evaluate(() => {
    const visible = (el) => !!el && el.getClientRects().length > 0
      && getComputedStyle(el).visibility !== 'hidden';
    const rect = (el) => {
      if (!el) return null;
      const r = el.getBoundingClientRect();
      return { x: r.x, y: r.y, width: r.width, height: r.height, right: r.right, bottom: r.bottom };
    };
    const details = (el) => ({ tag: el.tagName, class: el.className?.baseVal ?? el.className,
      role: el.getAttribute('role'), box: rect(el), scroll_width: el.scrollWidth,
      client_width: el.clientWidth, scroll_height: el.scrollHeight,
      client_height: el.clientHeight, scroll_top: el.scrollTop,
      overflow_x: getComputedStyle(el).overflowX, overflow_y: getComputedStyle(el).overflowY });
    const active = document.querySelector('.rh-page > .tabs > .tabpanel:not([hidden])');
    const dialogs = [...document.querySelectorAll('[role="dialog"]')].filter(visible);
    const target = dialogs.at(-1) || active || document.querySelector('main') || document.body;
    const navs = [...document.querySelectorAll('.rh-page > .tabs > .tablist, [role="dialog"] [role="tablist"], .main-nav')]
      .filter(visible).map((el) => {
        const controls = [...el.querySelectorAll('[role="tab"],a.nav-link')].filter(visible);
        return { ...details(el), controls: controls.length,
          rows: new Set(controls.map((e) => Math.round(e.getBoundingClientRect().top))).size };
      });
    const math = [...target.querySelectorAll('.katex-display')].filter(visible).map((el) => {
      const html = el.querySelector('.katex-html');
      const owners = [];
      for (let p = el; p && p !== target.parentElement; p = p.parentElement) {
        if (['auto', 'scroll'].includes(getComputedStyle(p).overflowX)) owners.push(details(p));
      }
      return { ...details(el), math_box: rect(html), horizontal_scroll_owners: owners };
    });
    const rails = [...target.querySelectorAll('aside,[data-control-panel]')].filter(visible).map(details);
    const images = [...target.querySelectorAll('img')].filter(visible).map((el) => ({ src: el.currentSrc,
      complete: el.complete, natural_width: el.naturalWidth, box: rect(el) }));
    const visualAreas = [...target.querySelectorAll('svg,canvas')].filter(visible)
      .map((el) => { const b = el.getBoundingClientRect(); return b.width * b.height; });
    return {
      viewport: { width: innerWidth, height: innerHeight },
      document: { scroll_width: document.documentElement.scrollWidth,
        scroll_height: document.documentElement.scrollHeight,
        body_scroll_width: document.body.scrollWidth, body_scroll_height: document.body.scrollHeight,
        scroll_x: scrollX, scroll_y: scrollY },
      theme: document.documentElement.dataset.theme,
      html_lang: document.documentElement.lang,
      heading: document.querySelector('.rh-page h1')?.textContent?.trim() || null,
      page_body: rect(document.querySelector('.page-body')),
      footer: rect(document.querySelector('.site-footer')),
      active_panel: active ? details(active) : null,
      content_text_length: target.innerText?.trim().length || 0,
      tab_rows: navs, rails, math,
      katex_count: target.querySelectorAll('.katex').length,
      katex_errors: [...target.querySelectorAll('.katex-error')].map((el) => ({ text: el.textContent, title: el.title })),
      unresolved_citations: [...target.querySelectorAll('cite.cite-inline')].filter((el) =>
        /^\[riemann-/.test(el.textContent || '')).map((el) => el.textContent),
      broken_images: images.filter((img) => img.complete && img.natural_width === 0),
      dialogs: dialogs.map((el) => ({ name: el.getAttribute('aria-label'), box: rect(el),
        panel: rect(el.classList.contains('rs-modal') ? el : el.firstElementChild),
        focus_inside: el.contains(document.activeElement) })),
      largest_viz_viewport_fraction: Math.max(0, ...visualAreas) / (innerWidth * innerHeight),
      scroll_containers: [...target.querySelectorAll('*')].filter((el) => visible(el)
        && (el.scrollHeight > el.clientHeight + 2 || el.scrollWidth > el.clientWidth + 2)
        && /auto|scroll/.test(`${getComputedStyle(el).overflowX} ${getComputedStyle(el).overflowY}`))
        .slice(0, 35).map(details),
    };
  });
}
async function capture(page, scenario, name, { gate = true, needsMath = false } = {}) {
  await settle(page);
  const dom = await domSnapshot(page);
  const id = `${String(scenario.screenshots.length + 1).padStart(3, '0')}-${slug(name)}`;
  const filename = `${scenario.id}/${id}.png`;
  const screenshotPath = path.join(out, filename);
  await mkdir(path.dirname(screenshotPath), { recursive: true });
  await page.screenshot({ path: screenshotPath, fullPage: false, animations: 'disabled' });
  const shot = { name, file: filename.replaceAll('\\', '/'),
    sha256: createHash('sha256').update(await readFile(screenshotPath)).digest('hex'), dom };
  scenario.screenshots.push(shot);
  if (gate) {
    const prefix = `${name}: `;
    check(scenario, `${prefix}document fits viewport`,
      Math.abs(dom.document.scroll_width - dom.viewport.width) <= 1
      && Math.abs(dom.document.scroll_height - dom.viewport.height) <= 2,
      { document: dom.document, viewport: dom.viewport });
    check(scenario, `${prefix}footer in viewport`, dom.footer && dom.footer.y >= -1
      && dom.footer.bottom <= dom.viewport.height + 2, dom.footer);
    check(scenario, `${prefix}single-row navigation`, dom.tab_rows.every((row) => row.rows <= 1), dom.tab_rows);
    check(scenario, `${prefix}control rails fit`, dom.rails.every((rail) =>
      rail.scroll_height <= rail.client_height + 2), dom.rails);
    check(scenario, `${prefix}no KaTeX errors`, dom.katex_errors.length === 0, dom.katex_errors);
    check(scenario, `${prefix}all citations resolved`, dom.unresolved_citations.length === 0, dom.unresolved_citations);
    check(scenario, `${prefix}no broken visible images`, dom.broken_images.length === 0, dom.broken_images);
    check(scenario, `${prefix}expected theme`, dom.theme === scenario.theme, dom.theme);
    check(scenario, `${prefix}dialog panel fits`, dom.dialogs.every(({ panel }) => panel
      && panel.x >= -1 && panel.y >= -1 && panel.right <= dom.viewport.width + 1
      && panel.bottom <= dom.viewport.height + 2), dom.dialogs);
    if (needsMath) check(scenario, `${prefix}math rendered`, dom.katex_count > 0, dom.katex_count);
  }
  return shot;
}
async function wheelPanel(page, panel, delta) {
  const box = await panel.boundingBox();
  requireCondition(box && box.width > 0 && box.height > 0, 'Scrollable panel has no visible box');
  await page.mouse.move(box.x + Math.min(box.width * 0.55, box.width - 8),
    box.y + Math.min(box.height * 0.55, box.height - 8), { steps: 4 });
  await page.mouse.wheel(0, delta);
  await settle(page);
}
async function panelScreens(page, panel, scenario, name, needsMath = false) {
  await wheelPanel(page, panel, -100000);
  await capture(page, scenario, `${name}-top`, { needsMath });
  const initial = await panel.evaluate((el) => ({ client: el.clientHeight, scroll: el.scrollHeight, top: el.scrollTop }));
  if (initial.scroll <= initial.client + 2) return;
  if (options.contentScreenshots === 'top-bottom') {
    await wheelPanel(page, panel, 100000);
    const after = await panel.evaluate((el) => ({ top: el.scrollTop, max: el.scrollHeight - el.clientHeight }));
    check(scenario, `${name}: pointer scroll reaches bottom`, after.top >= after.max - 2, after);
    await capture(page, scenario, `${name}-bottom`);
  } else {
    let previous = initial.top, reached = false;
    for (let step = 1; step <= 60; step += 1) {
      await wheelPanel(page, panel, Math.max(100, initial.client * 0.8));
      const next = await panel.evaluate((el) => ({ top: el.scrollTop, max: el.scrollHeight - el.clientHeight }));
      if (next.top <= previous + 1 && next.top < next.max - 2) break;
      await capture(page, scenario, `${name}-scroll-${String(step).padStart(2, '0')}`);
      if (next.top >= next.max - 2) { reached = true; break; }
      previous = next.top;
    }
    check(scenario, `${name}: complete panel scroll walk`, reached, { maximum_steps: 60 });
  }
  await wheelPanel(page, panel, -100000);
}
async function proofControls(page, panel, scenario, tab) {
  const controls = panel.locator('.rh-stage-controls button[aria-pressed]');
  if (!(await controls.count())) return;
  check(scenario, `${tab}: four proof-stage controls`, await controls.count() === 4);
  const descriptions = [];
  for (let index = 0; index < await controls.count(); index += 1) {
    const button = controls.nth(index);
    const name = norm(await button.innerText());
    await pointerClick(page, button, scenario, `${tab}: proof stage ${index + 1} ${name}`);
    check(scenario, `${tab}: proof stage ${index + 1} selected`, await button.getAttribute('aria-pressed') === 'true'
      && await panel.locator('.rh-stage-controls button[aria-pressed="true"]').count() === 1);
    const detail = panel.locator('.rh-stage-detail');
    const text = norm(await detail.innerText());
    descriptions.push(text);
    check(scenario, `${tab}: proof stage ${index + 1} explanatory text`, text.length > 80, text);
    const href = await detail.locator('a').getAttribute('href');
    check(scenario, `${tab}: proof stage ${index + 1} source`, /^https:\/\/(arxiv\.org|github\.com|www\.mathnet\.ru)\//.test(href || ''), href);
    await capture(page, scenario, `${tab}-proof-stage-${index + 1}`);
  }
  check(scenario, `${tab}: stage content changes`, new Set(descriptions).size === 4);
}
async function experimentViews(page, panel, scenario, text) {
  const buttons = panel.locator('.rh-experiments .rs-exp-open');
  check(scenario, 'all four experiment launch controls present', await buttons.count() === 4);
  requireCondition(await buttons.count() === 4, 'Expected all four experiment records');
  for (const id of ['001', '002', '003', '004']) {
    const launch = buttons.filter({ hasText: new RegExp(`^EXP-${id}:`) });
    await pointerClick(page, launch, scenario, `open EXP-${id}`);
    const dialog = page.locator('.rs-modal[role="dialog"]');
    await dialog.waitFor({ state: 'visible' });
    check(scenario, `EXP-${id}: correct record opened`, (await dialog.getAttribute('aria-label') || '').startsWith(`EXP-${id}:`));
    const hypothesis = dialog.getByRole('heading', { name: text.hypothesis, exact: true });
    const verdict = dialog.getByRole('heading', { name: text.verdict, exact: true });
    check(scenario, `EXP-${id}: both persisted sections`, await hypothesis.count() === 1 && await verdict.count() === 1);
    await hypothesis.scrollIntoViewIfNeeded();
    await capture(page, scenario, `EXP-${id}-hypothesis`);
    await verdict.scrollIntoViewIfNeeded();
    await capture(page, scenario, `EXP-${id}-verdict`);
    const artifactLinks = dialog.locator('.rs-modal-artifacts a');
    check(scenario, `EXP-${id}: artifact links`, await artifactLinks.count() > 0);
    if (options.contentScreenshots === 'all') {
      await panelScreens(page, dialog.locator('.rs-modal-body'), scenario, `EXP-${id}-complete-record`);
    }
    await pointerClick(page, dialog.getByRole('button', { name: text.close, exact: true }), scenario, `close EXP-${id}`);
    await dialog.waitFor({ state: 'hidden' });
    check(scenario, `EXP-${id}: pointer close restores page`, await page.locator('.rh-page').isVisible());
  }
  for (const index of [0, 1]) {
    const detail = panel.locator('details.rh-details').nth(index);
    requireCondition(await detail.count() === 1, `Missing results disclosure ${index + 1}`);
    await pointerClick(page, detail.locator('summary'), scenario, `open results disclosure ${index + 1}`);
    check(scenario, `results disclosure ${index + 1}: opened`, await detail.getAttribute('open') !== null);
    await capture(page, scenario, `results-disclosure-${index + 1}`);
    await pointerClick(page, detail.locator('summary'), scenario, `close results disclosure ${index + 1}`);
  }
}
async function architectureViews(page, scenario, text) {
  await pointerClick(page, page.getByRole('button', { name: text.architecture, exact: true }), scenario, 'open architecture modal');
  const dialog = page.getByRole('dialog').filter({ has: page.getByRole('tablist') });
  await dialog.waitFor({ state: 'visible' });
  const tabs = dialog.getByRole('tab');
  const count = await tabs.count();
  requireCondition(count > 0 && count <= 6, `Unexpected architecture tab count ${count}`);
  for (let index = 0; index < count; index += 1) {
    const button = tabs.nth(index);
    const name = norm(await button.innerText());
    await pointerClick(page, button, scenario, `architecture tab ${index + 1} ${name}`);
    check(scenario, `architecture tab ${index + 1}: selected`, await button.getAttribute('aria-selected') === 'true');
    const panel = dialog.getByRole('tabpanel');
    await panel.locator('svg').waitFor({ state: 'visible' });
    check(scenario, `architecture tab ${index + 1}: prose and diagram`, norm(await panel.innerText()).length > 60
      && await panel.locator('svg').count() > 0);
    await capture(page, scenario, `architecture-${index + 1}`);
  }
  await pointerClick(page, dialog.getByRole('button', { name: scenario.lang === 'es' ? 'cerrar' : 'close', exact: true }), scenario, 'close architecture modal');
  await dialog.waitFor({ state: 'hidden' });
}

async function runScenario(viewport, lang, theme) {
  const scenario = {
    id: `${viewport.width}x${viewport.height}-${lang}-${theme}`, viewport, lang, theme,
    started_utc: new Date().toISOString(), completed: false,
    checks: [], failures: [], pointer_actions: [], screenshots: [],
    console_errors: [], console_warnings: [], page_errors: [], request_failures: [], http_errors: [],
    tabs_visited: [], error: null,
  };
  receipt.scenarios.push(scenario);
  const context = await browser.newContext({ viewport, deviceScaleFactor: 1,
    isMobile: viewport.width < 640, hasTouch: viewport.width < 640,
    colorScheme: 'light', locale: 'en-US', reducedMotion: 'reduce' });
  const page = await context.newPage();
  page.setDefaultTimeout(20000);
  page.setDefaultNavigationTimeout(60000);
  page.on('console', (message) => {
    if (message.type() === 'error') scenario.console_errors.push(message.text());
    if (message.type() === 'warning') scenario.console_warnings.push(message.text());
  });
  page.on('pageerror', (error) => scenario.page_errors.push(String(error)));
  page.on('requestfailed', (request) => scenario.request_failures.push({ url: request.url(),
    type: request.resourceType(), error: request.failure()?.errorText || 'unknown' }));
  page.on('response', (response) => {
    if (response.status() >= 400) scenario.http_errors.push({ url: response.url(), status: response.status() });
  });
  try {
    await page.goto(new URL('./', base).href, { waitUntil: 'domcontentloaded' });
    await page.getByRole('button', { name: labels.en.language, exact: true }).waitFor({ state: 'visible' });
    if (lang === 'es') {
      await pointerClick(page, page.getByRole('button', { name: labels.en.language, exact: true }), scenario, 'switch language EN to ES');
    }
    const text = labels[lang];
    check(scenario, 'language selected by real control', await page.getByRole('button', { name: text.language, exact: true }).count() === 1);
    const initialTheme = await page.locator('html').getAttribute('data-theme');
    if (initialTheme !== theme) await pointerClick(page,
      page.getByRole('button', { name: text.theme, exact: true }), scenario, `switch theme to ${theme}`);
    check(scenario, 'theme selected by real control', await page.locator('html').getAttribute('data-theme') === theme);
    const problem = page.locator('table').getByRole('link', { name: text.problem, exact: true });
    await problem.waitFor({ state: 'visible' });
    await problem.scrollIntoViewIfNeeded();
    await capture(page, scenario, 'program-portfolio-entry', { gate: false });
    await pointerClick(page, problem, scenario, 'Program portfolio to Riemann');
    await page.waitForURL(/\/problems\/riemann-hypothesis(?:[?#]|$)/);
    await page.getByRole('heading', { name: text.heading, exact: true }).waitFor({ state: 'visible' });
    await page.locator('.rh-results tbody tr').first().waitFor({ state: 'visible' });
    await page.evaluate(() => document.fonts.ready);
    check(scenario, 'recorded numerical result loaded', (await page.locator('.rh-results').innerText()).includes('0.4190768284253039967'));
    check(scenario, 'qualitative EXP-004 result is rendered', norm(await page.locator('.rh-page').innerText()).includes('EXP-004'));
    const tablist = page.locator('.rh-page > .tabs > .tablist');
    check(scenario, 'six research sections present', await tablist.getByRole('tab').count() === 6);
    for (let index = 0; index < tabIds.length; index += 1) {
      const id = tabIds[index];
      const tab = tablist.getByRole('tab', { name: text.tabs[index], exact: true });
      await pointerClick(page, tab, scenario, `research tab ${id}`);
      check(scenario, `${id}: selected tab`, await tab.getAttribute('aria-selected') === 'true');
      const panel = page.locator('.rh-page > .tabs > .tabpanel:not([hidden])');
      const panelId = await panel.getAttribute('id');
      requireCondition(panelId?.endsWith(`-panel-${id}`), `Wrong panel after ${id}: ${panelId}`);
      check(scenario, `${id}: substantive rendered content`, norm(await panel.innerText()).length >= 150);
      scenario.tabs_visited.push(id);
      await panelScreens(page, panel, scenario, id, ['summary', 'context', 'strategy'].includes(id));
      await proofControls(page, panel, scenario, id);
      if (id === 'results') await experimentViews(page, panel, scenario, text);
      console.log(JSON.stringify({ event: 'tab-reviewed', scenario: scenario.id, tab: id,
        failures: scenario.failures.length, screenshots: scenario.screenshots.length }));
    }
    await architectureViews(page, scenario, text);
    await capture(page, scenario, 'final-route');
    check(scenario, 'all six sections visited', scenario.tabs_visited.length === 6);
    scenario.completed = true;
  } catch (error) {
    scenario.error = shortError(error);
    check(scenario, 'scenario completed without navigation/interaction failure', false, scenario.error);
    try { await capture(page, scenario, 'failure-state', { gate: false }); } catch { /* Preserve initial failure. */ }
  } finally {
    check(scenario, 'no browser console errors', scenario.console_errors.length === 0, scenario.console_errors);
    check(scenario, 'no uncaught browser exceptions', scenario.page_errors.length === 0, scenario.page_errors);
    const failedRequests = scenario.request_failures.filter((failure) => failure.error !== 'net::ERR_ABORTED');
    check(scenario, 'no failed resource requests', failedRequests.length === 0, failedRequests);
    check(scenario, 'no HTTP error responses', scenario.http_errors.length === 0, scenario.http_errors);
    scenario.finished_utc = new Date().toISOString();
    await context.close();
    await saveReceipt();
    console.log(JSON.stringify({ event: 'scenario-finished', scenario: scenario.id,
      passed: scenario.completed && !scenario.failures.length, failures: scenario.failures.length,
      screenshots: scenario.screenshots.length }));
  }
}

try {
  const playwright = await loadPlaywright();
  const chromium = playwright.chromium || playwright.default?.chromium;
  requireCondition(chromium, 'Resolved module does not expose Playwright chromium');
  browser = await chromium.launch({ headless: !options.headed });
  for (const viewport of options.viewports) {
    for (const lang of ['en', 'es']) {
      for (const theme of ['light', 'dark']) await runScenario(viewport, lang, theme);
    }
  }
} catch (error) {
  receipt.fatal_error = shortError(error);
} finally {
  if (browser) await browser.close();
  await saveReceipt();
}
const summary = {
  passed: receipt.passed, scenarios: receipt.scenarios.length,
  expected_scenarios: options.viewports.length * 4,
  tabs_visited: receipt.scenarios.reduce((n, s) => n + s.tabs_visited.length, 0),
  screenshots: receipt.scenarios.reduce((n, s) => n + s.screenshots.length, 0),
  failures: receipt.scenarios.reduce((n, s) => n + s.failures.length, 0),
  fatal_error: receipt.fatal_error, receipt: receiptPath,
};
await writeFile(path.join(out, 'summary.json'), `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify(summary, null, 2));
process.exitCode = receipt.passed ? 0 : 1;
