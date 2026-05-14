const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const BASE_URL = 'https://364fec8b-2b82-4893-84eb-0cf7d9024e5c-00-1bio1s9oa7u49.worf.replit.dev';
const SCREENSHOTS_DIR = path.join(__dirname, 'bt-qa-screenshots');
const WAIT = 'domcontentloaded';
const NAV_TIMEOUT = 45000;

if (!fs.existsSync(SCREENSHOTS_DIR)) fs.mkdirSync(SCREENSHOTS_DIR, { recursive: true });

async function screenshot(page, name) {
  const p = path.join(SCREENSHOTS_DIR, `${name}.png`);
  await page.screenshot({ path: p, fullPage: false });
  console.log(`📸 ${name}`);
}

async function login(page) {
  await page.goto(`${BASE_URL}/login`, { waitUntil: 'domcontentloaded', timeout: NAV_TIMEOUT });
  await page.waitForTimeout(3000);
  await screenshot(page, 'debug-login-fresh');
  // Use data-testid selectors from the login page
  await page.waitForSelector('[data-testid="input-email"]', { timeout: 30000 });
  await page.fill('[data-testid="input-email"]', 'test@survivorpulse.com');
  await page.fill('[data-testid="input-password"]', 'YCoF7ho8i?94AGsz');
  await page.click('button[type="submit"]');
  await page.waitForTimeout(5000);
  console.log('Post-login URL:', page.url());
}

async function goToBacktester(page) {
  await page.goto(`${BASE_URL}/backtester`, { waitUntil: WAIT, timeout: NAV_TIMEOUT });
  await page.waitForTimeout(5000);
  console.log('Backtester URL:', page.url());
}

(async () => {
  const browser = await chromium.launch({ headless: true });

  // ── Desktop session ────────────────────────────────────────────────────────
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();

  console.log('\n=== AUTH ===');
  await login(page);
  await screenshot(page, '00-post-login');

  console.log('\n=== BACKTESTER LOAD ===');
  await goToBacktester(page);
  await screenshot(page, '01-backtester-desktop');

  const bodyLen = await page.evaluate(() => document.body.innerText.length);
  console.log('Page content length:', bodyLen);

  // ── SST-123: Design checks ─────────────────────────────────────────────────
  console.log('\n=== SST-123 DESIGN ===');

  // TC1: .label-structural font
  const labelStyles = await page.evaluate(() => {
    const el = document.querySelector('.label-structural');
    if (!el) return null;
    const s = window.getComputedStyle(el);
    return { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, letterSpacing: s.letterSpacing };
  });
  console.log('TC1 .label-structural:', JSON.stringify(labelStyles));

  // TC1: .sp-table
  const spTableStyles = await page.evaluate(() => {
    const el = document.querySelector('.sp-table');
    if (!el) return null;
    const s = window.getComputedStyle(el);
    return { present: true, width: s.width, borderCollapse: s.borderCollapse };
  });
  console.log('TC1 .sp-table:', JSON.stringify(spTableStyles));

  // TC1: WeekRow hover state — check for onMouseEnter handler
  const weekRowHover = await page.evaluate(() => {
    const rows = document.querySelectorAll('tbody tr');
    return { rowCount: rows.length };
  });
  console.log('TC1 WeekRow rows found:', weekRowHover.rowCount);

  // Hover over first row to trigger state
  try {
    const firstRow = page.locator('tbody tr').first();
    await firstRow.hover();
    await page.waitForTimeout(500);
    const hoverBg = await firstRow.evaluate(el => window.getComputedStyle(el).background);
    console.log('TC1 WeekRow hover bg:', hoverBg.substring(0, 80));
  } catch (e) {
    console.log('TC1 WeekRow hover check skipped:', e.message.substring(0, 80));
  }
  await screenshot(page, '02-sst123-design-check');

  // TC2: ScenarioControls
  const scenarioEl = await page.evaluate(() => {
    const candidates = [
      ...document.querySelectorAll('[data-testid*="scenario"], [class*="scenario"], [class*="Scenario"], [class*="config"], [class*="Config"]')
    ];
    return candidates.length > 0 ? candidates[0].className.substring(0, 100) : 'not found';
  });
  console.log('TC2 ScenarioControls/Config panel:', scenarioEl);

  // TC3: Chart/visualization
  const hasChart = await page.evaluate(() => {
    return {
      canvas: !!document.querySelector('canvas'),
      svg: !!document.querySelector('svg'),
      recharts: !!document.querySelector('.recharts-wrapper'),
    };
  });
  console.log('TC3 Chart elements:', JSON.stringify(hasChart));

  // TC4: SeasonReplayView desktop layout
  const layoutCheck = await page.evaluate(() => {
    const root = document.querySelector('#root');
    const width = root ? root.getBoundingClientRect().width : 0;
    return { rootWidth: width, bodyWidth: document.body.getBoundingClientRect().width };
  });
  console.log('TC4 Desktop layout widths:', JSON.stringify(layoutCheck));
  await screenshot(page, '03-sst123-full-desktop');

  // TC5: Mobile viewport
  console.log('\n=== SST-123 TC5 MOBILE ===');
  await ctx.close();
  const mobileCtx = await browser.newContext({ viewport: { width: 375, height: 812 } });
  const mobilePage = await mobileCtx.newPage();
  await login(mobilePage);
  await goToBacktester(mobilePage);
  await screenshot(mobilePage, '04-sst123-mobile');
  const mobileLayout = await mobilePage.evaluate(() => {
    return { bodyWidth: document.body.getBoundingClientRect().width };
  });
  console.log('TC5 Mobile body width:', mobileLayout.bodyWidth);
  await mobileCtx.close();

  // ── SST-125: Weekly results ────────────────────────────────────────────────
  console.log('\n=== SST-125 WEEKLY RESULTS ===');
  const ctx2 = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page2 = await ctx2.newPage();
  await login(page2);
  await goToBacktester(page2);
  await screenshot(page2, '05-sst125-initial');

  // TC1: Week rows present
  const rows = await page2.evaluate(() => {
    const trs = document.querySelectorAll('tbody tr');
    return Array.from(trs).slice(0, 5).map(r => r.innerText.substring(0, 60));
  });
  console.log('TC1 First 5 rows:', JSON.stringify(rows));
  await screenshot(page2, '06-sst125-week-rows');

  // TC1: Click Week 1
  const clickedW1 = await page2.evaluate(() => {
    const trs = Array.from(document.querySelectorAll('tbody tr'));
    const w1 = trs.find(r => /week\s*1\b|wk\s*1\b/i.test(r.innerText));
    if (w1) { w1.click(); return w1.innerText.substring(0, 60); }
    // fallback: click first row
    if (trs[0]) { trs[0].click(); return 'first row: ' + trs[0].innerText.substring(0, 60); }
    return 'no rows';
  });
  console.log('TC1 Clicked:', clickedW1);
  await page2.waitForTimeout(2000);
  await screenshot(page2, '07-sst125-week1-selected');

  // TC2: Click Week 2
  const clickedW2 = await page2.evaluate(() => {
    const trs = Array.from(document.querySelectorAll('tbody tr'));
    const w2 = trs.find(r => /week\s*2\b|wk\s*2\b/i.test(r.innerText));
    if (w2) { w2.click(); return w2.innerText.substring(0, 60); }
    if (trs[1]) { trs[1].click(); return 'row2: ' + trs[1].innerText.substring(0, 60); }
    return 'not found';
  });
  console.log('TC2 Clicked Week 2:', clickedW2);
  await page2.waitForTimeout(2000);
  await screenshot(page2, '08-sst125-week2-selected');

  // TC3: Back to Week 1
  const clickedW1Again = await page2.evaluate(() => {
    const trs = Array.from(document.querySelectorAll('tbody tr'));
    const w1 = trs.find(r => /week\s*1\b|wk\s*1\b/i.test(r.innerText));
    if (w1) { w1.click(); return true; }
    if (trs[0]) { trs[0].click(); return true; }
    return false;
  });
  console.log('TC3 Back to Week 1:', clickedW1Again);
  await page2.waitForTimeout(2000);
  await screenshot(page2, '09-sst125-week1-back');

  // TC4: Check for zero-games empty state
  const emptyCheck = await page2.evaluate(() => {
    const text = document.body.innerText;
    return {
      hasNoResults: /no results|not available|no games/i.test(text),
      hasNullCell: document.body.innerHTML.includes('>null<') || document.body.innerHTML.includes('>undefined<'),
    };
  });
  console.log('TC4 Empty state check:', JSON.stringify(emptyCheck));
  await screenshot(page2, '10-sst125-empty-state-check');

  // TC5: Navigate to Week 14
  const clickedW14 = await page2.evaluate(() => {
    const trs = Array.from(document.querySelectorAll('tbody tr'));
    const w14 = trs.find(r => /week\s*14\b|wk\s*14\b/i.test(r.innerText));
    if (w14) { w14.click(); return w14.innerText.substring(0, 80); }
    return 'Week 14 not found — row count: ' + trs.length;
  });
  console.log('TC5 Week 14:', clickedW14);
  await page2.waitForTimeout(2500);
  await screenshot(page2, '11-sst125-week14');

  const week14Text = await page2.evaluate(() => {
    const main = document.querySelector('main, [class*="replay"], [class*="Replay"], #root');
    return main ? main.innerText.substring(0, 600) : '';
  });
  console.log('TC5 Week 14 content:\n', week14Text.substring(0, 400));

  await ctx2.close();
  await browser.close();

  console.log('\n✅ Done. Screenshots:', SCREENSHOTS_DIR);
})();
