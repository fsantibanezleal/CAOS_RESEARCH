import { createRequire } from 'node:module';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import path from 'node:path';

const args=Object.fromEntries(process.argv.slice(2).reduce((rows,x,i,all)=>{
  if (x.startsWith('--')) rows.push([x.slice(2),all[i+1]]);
  return rows;
},[]));
const require=createRequire(import.meta.url);
const { chromium }=require(process.env.PLAYWRIGHT_MODULE);
const out=path.resolve(args.output);
await mkdir(out,{recursive:true});
const sha=bytes=>createHash('sha256').update(bytes).digest('hex');
const receipt={schema:'riemann-clarified-copy-ui-v1',release:'0.76.000',
  scope:'Actual pointer-driven rendering of the two clarified paragraphs. Supplements the full six-tab and 28-record replay; no scientific proof claim.',
  candidate_commit:args.commit,build_manifest_sha256:sha(await readFile(args.manifest)),
  script_sha256:sha(await readFile(new URL(import.meta.url))),base_url:args.base,
  started_utc:new Date().toISOString(),finished_utc:null,passed:false,scenarios:[],error:null};
const labels={
  en:{language:'Switch language',theme:'Toggle light / dark',tabs:['References & approaches','Open questions'],
    expected:['These global distinct-zero arguments are separate from the short-window moment proved internally in EXP-028.','EXP-023 is budget-stopped and incomplete.'],
    further:'A further short-window improvement requires extending the internally reviewed analytic range of EXP-028.'},
  es:{language:'Cambiar idioma',theme:'Cambiar claro / oscuro',tabs:['Referencias y enfoques','Preguntas abiertas'],
    expected:['Estos argumentos globales de ceros distintos son independientes del momento en ventanas cortas probado internamente en EXP-028.','EXP-023 se detuvo por presupuesto y sigue incompleto.'],
    further:'Una mejora adicional en ventanas cortas requiere ampliar el rango analítico de EXP-028 revisado internamente.'}
};
let browser;
try {
  for (const [width,height] of [[390,844],[1280,800],[1600,900],[2560,1440],[1440,1000]]) {
    for (const lang of ['en','es']) for (const theme of ['light','dark']) {
      browser=await chromium.launch({headless:true,executablePath:process.env.RIEMANN_CHROMIUM_EXECUTABLE});
      const version=browser.version();
      if (receipt.browser_version && receipt.browser_version!==version) throw Error('Browser changed');
      receipt.browser_version=version;
      const context=await browser.newContext({viewport:{width,height},deviceScaleFactor:1,
        isMobile:width<640,hasTouch:width<640,colorScheme:'light',reducedMotion:'reduce'});
      const page=await context.newPage();page.setDefaultTimeout(20000);
      const row={id:`${width}x${height}-${lang}-${theme}`,viewport:{width,height},lang,theme,
        passed:false,console_errors:[],page_errors:[],http_errors:[],images:[]};
      receipt.scenarios.push(row);
      page.on('console',m=>{if(m.type()==='error')row.console_errors.push(m.text());});
      page.on('pageerror',e=>row.page_errors.push(String(e)));
      page.on('response',r=>{if(r.status()>=400)row.http_errors.push({url:r.url(),status:r.status()});});
      await page.goto(new URL('/problems/riemann-hypothesis',args.base).href,{waitUntil:'domcontentloaded',timeout:60000});
      await page.locator('[data-evidence="EXP-028"]').waitFor({state:'visible'});
      if(lang==='es')await page.getByRole('button',{name:labels.en.language,exact:true}).click();
      if(await page.locator('html').getAttribute('data-theme')!==theme)
        await page.getByRole('button',{name:labels[lang].theme,exact:true}).click();
      if(await page.locator('html').getAttribute('data-theme')!==theme)throw Error('Wrong theme');
      const tablist=page.locator('.rh-page > .tabs > .tablist');
      for(const [i,tab] of ['approaches','open'].entries()){
        await tablist.getByRole('tab',{name:labels[lang].tabs[i],exact:true}).click();
        const panel=page.locator('.rh-page > .tabs > .tabpanel:not([hidden])');
        const distinct=panel.locator(`[data-testid="distinct-${tab}"]`);
        const text=await distinct.innerText();
        if(!text.includes(labels[lang].expected[i]))throw Error('Clarified paragraph absent');
        if(i===1&&!text.includes(labels[lang].further))throw Error('Further-gain boundary absent');
        if(text.includes('still lacks its uniform cancellation estimate')||text.includes('todavía carece de una estimación uniforme'))throw Error('Stale copy remains');
        const paragraph=distinct.locator('p').filter({hasText:labels[lang].expected[i]}).first();
        await paragraph.scrollIntoViewIfNeeded();
        await page.evaluate(()=>document.fonts.ready);
        const box=await paragraph.boundingBox();
        if(!box||box.x<0||box.x+box.width>width+1||box.y<0||box.y+box.height>height+1)throw Error('Paragraph does not fit viewport');
        const file=`${row.id}-${tab}.png`;
        const bytes=await page.screenshot({path:path.join(out,file),fullPage:false});
        row.images.push({file,bytes:bytes.length,sha256:sha(bytes),paragraph_box:box,exact_copy_verified:true});
      }
      if(row.console_errors.length||row.page_errors.length||row.http_errors.length)throw Error('Browser errors');
      row.passed=true;await browser.close();browser=null;
      console.log(JSON.stringify({scenario:row.id,passed:true,images:row.images.length}));
    }
  }
  receipt.passed=receipt.scenarios.length===20&&receipt.scenarios.every(s=>s.passed&&s.images.length===2);
} catch(e){receipt.error=String(e.stack||e);}
finally {
  if(browser)await browser.close();receipt.finished_utc=new Date().toISOString();
  await writeFile(path.join(out,'receipt.json'),JSON.stringify(receipt,null,2)+'\n');
}
console.log(JSON.stringify({passed:receipt.passed,scenarios:receipt.scenarios.length,error:receipt.error}));
process.exitCode=receipt.passed?0:1;
