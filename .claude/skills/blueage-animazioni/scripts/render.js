#!/usr/bin/env node
// render.js · skill blueage-animazioni
// Uso:
//   node render.js check      <file.html>             controlli (fermano il lavoro se ci sono ERRORI)
//   node render.js fotogrammi <file.html> [t1,t2,...] fotogrammi chiave (default CONFIG.fotogrammi) + tavola da mandare in chat
//   node render.js video      <file.html>             MP4 1920x1080 H.264 + poster (solo animazioni)
//   node render.js png        <file.html>             PNG a 2x (illustrazioni)
//   node render.js font       <file.html>             incorpora Plus Jakarta Sans nell'HTML (fatto anche dagli altri comandi)
// Opzioni: --out <cartella> (default: cartella dell'HTML) · --forza (prosegue anche con errori del controllo)
// Attenzione: ogni comando incorpora il font nell'HTML e lo riscrive (il file diventa autosufficiente). Non lanciarlo su file in sola lettura.
'use strict';
const fs = require('fs');
const path = require('path');
const os = require('os');
const { spawn, execSync, execFileSync } = require('child_process');

function req(m) {
  try { return require(m); } catch (e) {
    const g = execSync('npm root -g').toString().trim();
    return require(path.join(g, m));
  }
}
const { chromium } = req('playwright');

const FONT_DIR = path.join(__dirname, '..', 'assets', 'font');
const PESI = [400, 500, 700];
const MIN_PX = 20, MIN_DISCLAIMER = 16, MARGINE = 40;

const args = process.argv.slice(2);
const cmd = args[0];
const file = args[1] && path.resolve(args[1]);
const opt = (k) => { const i = args.indexOf(k); return i > 0 ? args[i + 1] : null; };
const forza = args.includes('--forza');
if (!cmd || !file || !fs.existsSync(file)) {
  console.log('Uso: node render.js check|fotogrammi|video|png|font <file.html> [opzioni]');
  process.exit(2);
}
const nome = path.basename(file, '.html');
const outDir = path.resolve(opt('--out') || path.dirname(file));
fs.mkdirSync(outDir, { recursive: true });

// ---------- font ----------
function cssFont() {
  return PESI.map((w) => {
    const f = path.join(FONT_DIR, `plus-jakarta-sans-latin-${w}-normal.woff2`);
    const b64 = fs.readFileSync(f).toString('base64');
    return `@font-face{font-family:'Plus Jakarta Sans';font-style:normal;font-weight:${w};font-display:block;src:url(data:font/woff2;base64,${b64}) format('woff2');}`;
  }).join('\n');
}
function incorporaFont() {
  let s = fs.readFileSync(file, 'utf8');
  if (s.includes('/*BA_FONT*/')) {
    s = s.replace('/*BA_FONT*/', cssFont());
  } else if (!/@font-face[^}]*Plus Jakarta Sans/.test(s)) {
    s = s.replace(/<head>/i, `<head>\n<style id="ba-font">${cssFont()}</style>`);
  } else return false;
  fs.writeFileSync(file, s);
  console.log('Font Plus Jakarta Sans incorporato nell\'HTML (400, 500, 700).');
  return true;
}

// ---------- controlli statici ----------
function controlliStatici(s, tipo) {
  const err = [], avv = [];
  const scena = s.includes('FINE BA_ANIM_LIB') ? s.split('FINE BA_ANIM_LIB')[1] : s;
  if (/#e8452c/i.test(s)) err.push('Usato il vermiglio #E8452C: è riservato ai RED TAG. Per le anomalie si usa #FF7A59');
  const urls = (s.match(/https?:\/\/[^\s"')]+/g) || []).filter((u) => !/^https?:\/\/www\.w3\.org\//.test(u));
  if (urls.length) err.push('Riferimenti esterni (niente CDN, niente risorse online): ' + [...new Set(urls)].slice(0, 5).join(', '));
  if (/<script[^>]+src=|<link[^>]+href=|@import/i.test(s)) err.push('Script, fogli di stile o import esterni: il file deve essere autosufficiente');
  if (tipo === 'animazione') {
    if (/setTimeout|setInterval|Date\.now|new Date|Math\.random/.test(scena)) err.push('Nella scena ci sono setTimeout, setInterval, orologio o Math.random: lo stato deve dipendere solo da t (per numeri casuali: BA.casuale(seme))');
    if (/@keyframes|animation\s*:|transition\s*:|<animate/i.test(s)) err.push('Animazioni CSS o SMIL: tutto il movimento va in renderAt(t)');
    if (!s.includes('BA_ANIM_LIB v')) avv.push('Animazione senza la libreria BA del template: i controlli dei componenti non valgono');
  }
  return { err, avv };
}

// ---------- browser ----------
async function apri(browser, w, h, dpr, hash) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: dpr || 1 });
  const page = await ctx.newPage();
  const errJs = [];
  page.on('pageerror', (e) => errJs.push(e.message));
  page.on('console', (m) => { if (m.type() === 'error') errJs.push(m.text()); });
  await page.goto('file://' + file + (hash || ''));
  return { ctx, page, errJs };
}

async function tipoPagina(page) {
  return page.evaluate(async () => {
    if (window.animReady) { await window.animReady; }
    if (document.fonts) await document.fonts.ready;
    return window.BA_INFO ? window.BA_INFO : (typeof window.renderAt === 'function' ? { tipo: 'animazione', durata: 18, fps: 30, poster: 17.5, fotogrammi: [1, 3.5, 8, 10, 13.5, 17.5] } : { tipo: 'illustrazione' });
  });
}

async function misuraIllustrazione(page) {
  return page.evaluate(() => {
    const b = document.body, svg = document.querySelector('body > svg');
    const cs = getComputedStyle(b);
    let w = parseFloat(cs.width), h = parseFloat(cs.height);
    if (svg && (!b.style.width && !/px/.test(cs.width) || w >= window.innerWidth - 1)) {
      w = parseFloat(svg.getAttribute('width')) || svg.getBoundingClientRect().width;
      h = parseFloat(svg.getAttribute('height')) || svg.getBoundingClientRect().height;
    }
    return { w: Math.round(w), h: Math.round(h) };
  });
}

// raccoglie i testi visibili: rettangolo, corpo effettivo, opacità effettiva
async function testi(page) {
  return page.evaluate(() => {
    const out = [];
    function opacita(e) { let o = 1; for (let n = e; n && n.nodeType === 1; n = n.parentNode) { const c = getComputedStyle(n); if (c.display === 'none' || c.visibility === 'hidden') return 0; o *= parseFloat(c.opacity); const a = n.getAttribute && n.getAttribute('opacity'); if (a !== null && a !== '' && c.opacity === '1') o *= parseFloat(a); } return o; }
    const nodi = [...document.querySelectorAll('svg text')];
    document.querySelectorAll('body *').forEach((e) => {
      if (e.closest('svg') || ['SCRIPT', 'STYLE'].includes(e.tagName) || e.id === 'ba-ora') return;
      const own = [...e.childNodes].some((c) => c.nodeType === 3 && c.textContent.trim());
      if (own) nodi.push(e);
    });
    const set = new Set(nodi);
    nodi.forEach((e, i) => { e.__ba = i; });
    nodi.forEach((e) => {
      const s = (e.textContent || '').trim(); if (!s) return;
      const anc = []; for (let n = e.parentNode; n && n.nodeType === 1; n = n.parentNode) if (set.has(n)) anc.push(n.__ba);
      const o = opacita(e); if (o < 0.15) return;
      const r = e.getBoundingClientRect(); if (r.width === 0) return;
      let px = parseFloat(getComputedStyle(e).fontSize);
      if (e.getScreenCTM) { const m = e.getScreenCTM(); if (m) px *= Math.sqrt(m.a * m.a + m.b * m.b); }
      out.push({ s: s.slice(0, 50), x: r.left, y: r.top, r: r.right, b: r.bottom, px: Math.round(px * 10) / 10, o, d: (e.closest('[data-ba]') || { getAttribute: () => '' }).getAttribute('data-ba') || '', i: e.__ba, anc });
    });
    return out;
  });
}

// campioni: [{quando, lista}] · un testo piccolo solo durante una transizione (es. mentre si ingrandisce) è un avviso, non un errore
function analizzaTesti(campioni, W, H, err, avv, margini) {
  const per = new Map(), visti = new Set();
  const una = (k, msg, dove) => { if (!visti.has(k)) { visti.add(k); dove.push(msg); } };
  campioni.forEach(({ quando, lista }) => {
    lista.forEach((t) => {
      if (t.r < 0 || t.x > W || t.b < 0 || t.y > H) return; // del tutto fuori: non si vede, non conta
      if (t.d === 'decoro') return; // testo che fa da texture (righe di un documento), non va letto
      const disc = t.d === 'disclaimer' || /^Illustrazione BlueAge/.test(t.s);
      const min = disc ? MIN_DISCLAIMER : MIN_PX;
      const k = t.i + '|' + t.s;
      const r = per.get(k) || { s: t.s, vis: 0, picc: 0, px: 99, quando: '' };
      r.vis++; if (t.px < min - 0.05) { r.picc++; if (t.px < r.px) { r.px = t.px; r.quando = quando; } r.min = min; }
      per.set(k, r);
      if (t.x < -1 || t.y < -1 || t.r > W + 1 || t.b > H + 1) una('f' + k, `${quando}: testo tagliato dal bordo · «${t.s}»`, err);
      else if (margini && (t.x < MARGINE / 2 || t.r > W - MARGINE / 2 || t.y < MARGINE / 2 || t.b > H - MARGINE / 4)) una('m' + k, `${quando}: testo a meno di ${MARGINE / 2} px dal bordo · «${t.s}»`, avv);
    });
    const vis = lista.filter((t) => t.o > 0.5);
    for (let i = 0; i < vis.length; i++) for (let j = i + 1; j < vis.length; j++) {
      const a = vis[i], b = vis[j];
      // il rettangolo del testo include l'interlinea: si riduce del 18% sopra e sotto
      const ia = (a.b - a.y) * 0.18, ib = (b.b - b.y) * 0.18;
      const ix = Math.min(a.r, b.r) - Math.max(a.x, b.x), iy = Math.min(a.b - ia, b.b - ib) - Math.max(a.y + ia, b.y + ib);
      if (ix <= 0 || iy <= 0) continue;
      if (a.anc.includes(b.i) || b.anc.includes(a.i)) continue;
      const area = ix * iy, min = Math.min((a.r - a.x) * (a.b - a.y), (b.r - b.x) * (b.b - b.y));
      if (area > 0.15 * min) una('s' + a.s + b.s, `${quando}: testi sovrapposti · «${a.s}» / «${b.s}»`, avv);
    }
  });
  per.forEach((r) => {
    if (!r.picc) return;
    if (r.picc >= Math.max(1, Math.ceil(r.vis * 0.5))) err.push(`corpo ${r.px} px < ${r.min} px (${r.quando}) · «${r.s}»`);
    else avv.push(`corpo ${r.px} px solo durante una transizione (${r.quando}) · «${r.s}»`);
  });
}

async function controlla(browser) {
  const s = fs.readFileSync(file, 'utf8');
  const { page, ctx, errJs } = await apri(browser, 1920, 1080, 1, '#render');
  const info = await tipoPagina(page);
  const { err, avv } = controlliStatici(s, info.tipo);
  let W = 1920, H = 1080;
  if (info.tipo === 'animazione') {
    const ok = await page.evaluate(() => typeof window.renderAt === 'function');
    if (!ok) err.push('window.renderAt non definita (o animReady mai risolta)');
    else {
      const font = await page.evaluate(() => document.fonts.check('700 28px "Plus Jakarta Sans"') && [...document.fonts].some((f) => f.family.replace(/["']/g, '') === 'Plus Jakarta Sans' && f.status === 'loaded'));
      if (!font) err.push('Plus Jakarta Sans non caricato');
      const d = info.durata;
      const ts = new Set([...Array(13).keys()].map((i) => Math.round((d * i / 12) * 100) / 100));
      (info.fotogrammi || []).forEach((t) => ts.add(t)); ts.add(info.poster);
      const camp = [];
      for (const t of [...ts].sort((a, b) => a - b)) {
        await page.evaluate((t) => window.renderAt(t), t);
        camp.push({ quando: `t=${t}s`, lista: await testi(page) });
      }
      analizzaTesti(camp, W, H, err, avv, true);
      // determinismo: lo stesso istante, raggiunto da punti diversi, deve dare lo stesso DOM (il confronto dei pixel è disturbato dalla rasterizzazione)
      const dom = (t) => page.evaluate((t) => { window.renderAt(t); return document.getElementById('s') ? document.getElementById('s').outerHTML : document.body.innerHTML; }, t);
      for (const [t, prima] of [[7.3, 2.1], [Math.round(d * 0.8 * 10) / 10, d - 0.1]]) {
        const a = await dom(t); await dom(prima); const b = await dom(t);
        if (a !== b) { err.push(`renderAt non deterministica: l'istante ${t} s dà due stati diversi a seconda di quello mostrato prima. Lo stato deve dipendere solo da t`); break; }
      }
      if (info.poster < d - 2) avv.push('Il poster non cade nel riepilogo finale (ultimi 2 s)');
    }
  } else {
    const m = await misuraIllustrazione(page); W = m.w; H = m.h;
    await page.setViewportSize({ width: W, height: H });
    const font = await page.evaluate(() => document.fonts.check('700 28px "Plus Jakarta Sans"'));
    if (!font) err.push('Plus Jakarta Sans non caricato');
    analizzaTesti([{ quando: 'illustrazione', lista: await testi(page) }], W, H, err, avv, false);
    const fondo = await page.evaluate(() => Math.max(...[...document.body.querySelectorAll('*')].filter((e) => !['SCRIPT', 'STYLE', 'symbol'].includes(e.tagName) && !e.closest('symbol')).map((e) => e.getBoundingClientRect()).filter((r) => r.width > 0 && r.height > 0).map((r) => r.bottom)));
    if (fondo < H * 0.88) avv.push(`Spazio vuoto in basso: il contenuto finisce a ${Math.round(fondo)} px su ${H}. Ridurre l'altezza (--h)`);
    if (fondo > H + 1) err.push(`Contenuto tagliato in basso: finisce a ${Math.round(fondo)} px su ${H}. Aumentare l'altezza (--h)`);
  }
  errJs.forEach((e) => err.push('Errore JavaScript: ' + e));
  await ctx.close();
  const uniq = (l) => [...new Set(l)];
  const E = uniq(err), A = uniq(avv);
  console.log(`\nCONTROLLO · ${path.basename(file)} · ${info.tipo}${info.tipo === 'animazione' ? ` ${info.durata} s` : ` ${W}x${H}`}`);
  E.forEach((e) => console.log('  ERRORE  ' + e));
  A.slice(0, 40).forEach((e) => console.log('  avviso  ' + e));
  if (A.length > 40) console.log(`  … altri ${A.length - 40} avvisi`);
  if (!E.length) console.log('  OK: nessun errore' + (A.length ? ` (${A.length} avvisi da guardare)` : ''));
  return { info, errori: E.length, W, H };
}

// ---------- fotogrammi chiave ----------
async function fotogrammi(browser, info) {
  const lista = (args[2] && !args[2].startsWith('--') ? args[2].split(',').map(Number) : info.fotogrammi);
  const dir = path.join(outDir, 'anteprime_' + nome);
  fs.mkdirSync(dir, { recursive: true });
  fs.readdirSync(dir).filter((f) => f.startsWith(nome + '_fotogramma_')).forEach((f) => fs.unlinkSync(path.join(dir, f)));
  const { page, ctx } = await apri(browser, 1920, 1080, 1, '#render');
  await tipoPagina(page);
  const files = [];
  for (let i = 0; i < lista.length; i++) {
    const t = lista[i];
    await page.evaluate((t) => window.renderAt(t), t);
    const f = path.join(dir, `${nome}_fotogramma_${i + 1}_t${String(t).replace('.', ',')}s.png`);
    await page.screenshot({ path: f }); files.push({ f, t });
  }
  await ctx.close();
  // tavola: 3 colonne, didascalia con l'istante
  const cols = 3, rows = Math.ceil(files.length / cols);
  const imgs = files.map((x) => `<figure><img src="data:image/png;base64,${fs.readFileSync(x.f).toString('base64')}"><figcaption>${String(x.t).replace('.', ',')} s</figcaption></figure>`).join('');
  const html = `<html><body style="margin:0;background:#050E2D;font:700 22px sans-serif;color:#7FD3DC"><div style="display:grid;grid-template-columns:repeat(${cols},640px);gap:16px;padding:16px">${imgs}</div><style>figure{margin:0}img{width:640px;height:360px;display:block;border:1px solid #13385E}figcaption{padding:6px 2px}</style></body></html>`;
  const tmp = path.join(os.tmpdir(), 'ba_tavola.html'); fs.writeFileSync(tmp, html);
  const c2 = await browser.newContext({ viewport: { width: cols * 656 + 16, height: rows * 416 + 16 } });
  const p2 = await c2.newPage(); await p2.goto('file://' + tmp);
  const tav = path.join(outDir, `${nome}_anteprime.png`);
  await p2.screenshot({ path: tav, fullPage: true }); await c2.close();
  console.log(`Fotogrammi: ${dir}\nTavola da mandare in chat: ${tav}`);
}

// ---------- video ----------
async function video(browser, info) {
  const d = info.durata, fps = info.fps || 30, n = Math.round(d * fps);
  const mp4 = path.join(outDir, nome + '.mp4');
  const { page, ctx } = await apri(browser, 1920, 1080, 1, '#render');
  await tipoPagina(page);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'slow', '-movflags', '+faststart', '-an', mp4]);
  let ffErr = ''; ff.stderr.on('data', (x) => { ffErr += x; });
  const fine = new Promise((res) => ff.on('close', res));
  const cdp = await page.context().newCDPSession(page); // cattura veloce senza perdita (4 volte più rapida di page.screenshot)
  for (let i = 0; i < n; i++) {
    await page.evaluate((t) => window.renderAt(t), i / fps);
    const buf = Buffer.from((await cdp.send('Page.captureScreenshot', { format: 'png', optimizeForSpeed: true })).data, 'base64');
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
    if (i % (fps * 3) === 0) process.stdout.write(`  ${Math.round(i / fps)} s / ${d} s\r`);
  }
  ff.stdin.end(); const code = await fine;
  if (code !== 0) { console.log('ffmpeg: ' + ffErr); process.exit(1); }
  await page.evaluate((t) => window.renderAt(t), info.poster);
  const poster = path.join(outDir, nome + '_poster.png');
  await page.screenshot({ path: poster }); await ctx.close();
  const pr = JSON.parse(execFileSync('ffprobe', ['-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate,nb_frames,duration', '-of', 'json', mp4]).toString()).streams[0];
  const mb = fs.statSync(mp4).size / 1048576;
  console.log(`Video: ${mp4}\n  ${pr.width}x${pr.height} · ${pr.r_frame_rate} fps · ${pr.nb_frames} fotogrammi · ${Number(pr.duration).toFixed(2)} s · ${mb.toFixed(1)} MB`);
  console.log(`Poster (t=${info.poster} s): ${poster}`);
  const probl = [];
  if (pr.width !== 1920 || pr.height !== 1080) probl.push('dimensioni diverse da 1920x1080');
  if (Math.abs(Number(pr.duration) - d) > 0.1) probl.push('durata diversa da ' + d + ' s');
  if (mb > 10) probl.push('peso oltre 10 MB');
  console.log(probl.length ? '  ERRORE  ' + probl.join('; ') : '  OK: formato, durata e peso');
  // tre fotogrammi presi dall'MP4 (non dall'HTML), per controllare che il video sia quello atteso
  const dir = path.join(outDir, 'anteprime_' + nome); fs.mkdirSync(dir, { recursive: true });
  const estratti = [0.3, 0.6, 0.97].map((k) => Math.round(d * k * 10) / 10).map((t) => {
    const f = path.join(dir, `${nome}_dal_video_t${String(t).replace('.', ',')}s.png`);
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-ss', String(t), '-i', mp4, '-frames:v', '1', f]); return f; });
  console.log('Fotogrammi estratti dal video, da guardare: ' + estratti.map((f) => path.basename(f)).join(', '));
}

// ---------- png (illustrazioni) ----------
async function png(browser, W, H) {
  const { page, ctx } = await apri(browser, W, H, 2, '');
  await tipoPagina(page);
  const f = path.join(outDir, nome + '.png');
  await page.screenshot({ path: f, clip: { x: 0, y: 0, width: W, height: H } });
  await ctx.close();
  console.log(`PNG: ${f} (${W * 2}x${H * 2}, da ${W}x${H} a 2x)`);
}

(async () => {
  incorporaFont();
  if (cmd === 'font') return;
  const browser = await chromium.launch();
  try {
    const r = await controlla(browser);
    if (cmd === 'check') { process.exitCode = r.errori ? 1 : 0; return; }
    if (r.errori && !forza) { console.log('\nCorreggere gli errori prima del render (oppure --forza per un\'anteprima di lavoro).'); process.exitCode = 1; return; }
    if (cmd === 'fotogrammi') { if (r.info.tipo !== 'animazione') throw new Error('fotogrammi: serve un\'animazione'); await fotogrammi(browser, r.info); }
    else if (cmd === 'video') { if (r.info.tipo !== 'animazione') throw new Error('video: serve un\'animazione'); await video(browser, r.info); }
    else if (cmd === 'png') { if (r.info.tipo === 'animazione') throw new Error('png: per le animazioni si usano fotogrammi o video'); await png(browser, r.W, r.H); }
    else console.log('Comando sconosciuto: ' + cmd);
  } finally { await browser.close(); }
})().catch((e) => { console.error(e.message); process.exit(1); });
