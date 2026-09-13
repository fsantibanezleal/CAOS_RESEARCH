const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs=require('node:fs/promises');
const path=require('node:path');
(async()=>{
 const browser=await chromium.launch({headless:true});const checks=[];
 const out=path.join(__dirname,'architecture-lower');await fs.mkdir(out,{recursive:true});
 for(const [size,viewport] of [['390x844',{width:390,height:844}],['1600x900',{width:1600,height:900}]])
 for(const lang of ['en','es'])for(const theme of ['light','dark']){
  const page=await browser.newPage({viewport,colorScheme:'light'});const errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:4182/problems/riemann-hypothesis',{waitUntil:'networkidle'});
  if(lang==='es')await page.locator('.header-actions button').nth(1).click();
  if(theme==='dark')await page.locator('.header-actions button').nth(2).click();
  await page.waitForTimeout(250);await page.locator('.header-actions button').first().click();
  for(const tab of ['method','science']){
   await page.locator('[role=dialog]').getByRole('tab',{name:tab==='method'?(lang==='en'?'The method':'El metodo'):(lang==='en'?'The science':'La ciencia'),exact:true}).click();
   await page.waitForTimeout(150);
   const panel=page.locator('[role=dialog] [role=tabpanel]');
   const before=await panel.evaluate(el=>({scrollTop:el.scrollTop,max:el.scrollHeight-el.clientHeight}));
   const box=await panel.boundingBox();await page.mouse.move(box.x+box.width/2,box.y+box.height/2);
   await page.mouse.wheel(0,Math.max(0,before.max/2-before.scrollTop));await page.waitForTimeout(150);
   const prefix=`${size}-${lang}-${theme}-${tab}`;
   await page.screenshot({path:path.join(out,`${prefix}-middle.png`)});
   await page.mouse.wheel(0,5000);await page.waitForTimeout(150);
   await page.screenshot({path:path.join(out,`${prefix}-bottom.png`)});
   const metrics=await page.locator('[role=dialog]').evaluate(el=>{
    const p=el.querySelector('[role=tabpanel]'),pr=p.getBoundingClientRect();
    return {scrollTop:p.scrollTop,max:p.scrollHeight-p.clientHeight,viewport:[document.documentElement.scrollWidth,document.documentElement.scrollHeight],rows:new Set([...el.querySelectorAll('[role=tab]')].map(t=>Math.round(t.getBoundingClientRect().y))).size,links:[...el.querySelectorAll('svg a')].map(a=>{const r=a.getBoundingClientRect();const h=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return{href:a.getAttribute('href'),visible:r.y>=pr.y&&r.bottom<=pr.bottom,centerHitsLink:a===h||a.contains(h)};})};
   });
   const passed=metrics.rows===1&&Math.abs(metrics.scrollTop-metrics.max)<2&&metrics.links.length===4&&metrics.links.every(a=>a.visible&&a.centerHitsLink)&&metrics.viewport[0]===viewport.width&&metrics.viewport[1]===viewport.height&&errors.length===0;
   checks.push({size,lang,theme,tab,passed,errors,...metrics});
  }
  await page.close();
 }
 await fs.writeFile(path.join(out,'receipt.json'),JSON.stringify({base_url:'http://127.0.0.1:4182/',scope:'Real mouse clicks and wheel scroll; no injected application state; source links hit-tested without navigating',checks,passed:checks.every(x=>x.passed)},null,2));
 console.log(JSON.stringify({checks:checks.length,passed:checks.every(x=>x.passed)}));await browser.close();
 if(checks.some(x=>!x.passed))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
