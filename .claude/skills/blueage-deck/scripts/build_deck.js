// Generatore generico dei deck BlueAge: legge uno storyboard approvato e produce il .pptx (style guide v3).
// Uso: node build_deck.js <storyboard.md> <deck.json> <out.pptx> [media.json]
//   deck.json  impostazioni del deck (modulo, capitoli, piede…): formato in references/storyboard_format.md
//   media.json immagini e video per numero di slide; se manca si cerca <cartella dello storyboard>/media/media.json
// Il build non inventa contenuti: ogni testo viene dallo storyboard.
// Storia: nasce da build_M1.js v02 (corso Meccanotecnica, 09/10/2026), reso generico con la decisione D41.
const fs = require('fs');
const path = require('path');
const B = require('./blueage_lib');
const { G, HEX, icon, iconDot, header, card, label, compassRings } = B;

const [SB, CFG_FILE, OUT, MEDIA_ARG] = process.argv.slice(2);
if (!SB || !CFG_FILE || !OUT) {
  console.error('Uso: node build_deck.js <storyboard.md> <deck.json> <out.pptx> [media.json]');
  process.exit(1);
}
const CFG = JSON.parse(fs.readFileSync(CFG_FILE, 'utf8'));
const MEDIA_FILE = MEDIA_ARG || path.join(path.dirname(SB), 'media', 'media.json');
const MEDIA = fs.existsSync(MEDIA_FILE) ? JSON.parse(fs.readFileSync(MEDIA_FILE, 'utf8')) : {};
const MEDIA_DIR = path.dirname(MEDIA_FILE);

// Impostazioni del deck (deck.json)
const DECK = {
  modulo: CFG.modulo || '',
  titoloModulo: CFG.titolo_modulo || '',
  capitoli: CFG.capitoli || [],
};
// Lettere COMPASS evidenziate nella slide COMPASS: posizioni 1-7 (C O M P A S S)
const COMPASS_HL = (CFG.compass_evidenza || []).map((n) => n - 1);
// Parole che non devono mai comparire nei testi visibili né nelle note (es. PAIN, D13)
const VIETATE = CFG.parole_vietate || ['PAIN'];
const AVVISO = 'B04A2E'; // colore dei segnaposto [DA VERIFICARE …] visibili in slide

// ---------------- Parser dello storyboard ----------------
function parse(md) {
  const lines = md.replace(/\r/g, '').split('\n');
  const slides = [];
  let cap = null, cur = null, key = null;
  for (const ln of lines) {
    let m;
    if ((m = ln.match(/^# (.*)$/))) {
      const c = m[1].match(/^CAP\. (\d+)/);
      cap = c ? parseInt(c[1], 10) : null;
      cur = null; key = null; continue;
    }
    if ((m = ln.match(/^## (\d+) · (\w+)\s*$/))) {
      cur = { n: parseInt(m[1], 10), tipo: m[2], cap, f: {} };
      slides.push(cur); key = null; continue;
    }
    if (!cur) continue;
    if (ln.startsWith('---')) { cur = null; key = null; continue; }
    if ((m = ln.match(/^([a-z_]+): \|\s*$/))) { key = m[1]; cur.f[key] = []; continue; }
    if ((m = ln.match(/^([a-z_]+): (.*)$/))) { key = null; cur.f[m[1]] = m[2]; continue; }
    if (key && ln.startsWith('  ')) { cur.f[key].push(ln.slice(2)); continue; }
    if (key && ln.trim() === '') continue;
  }
  for (const s of slides) for (const k in s.f) if (Array.isArray(s.f[k])) s.f[k] = s.f[k].join('\n');
  return slides;
}

// ---------------- Testo ----------------
// Testo senza marcatura (per stimare lunghezze)
const plain = (t) => (t || '').replace(/\*\*/g, '').replace(/<br>/g, ' ').replace(/(^|[\s(«"'])_([^_]+)_/g, '$1$2');
// Divide un testo in run: **grassetto**, _corsivo_, <br> (a capo), [DA VERIFICARE …] in rosso
function runs(txt, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|(?<=^|[\s(«"'>])_[^_]+_(?=$|[\s.,;:!?)»"'<])|\[DA VERIFICARE[^\]]*\]|<br>)/g;
  let last = 0, m;
  const push = (text, opt) => { if (text) out.push({ text, options: { ...base, ...opt } }); };
  txt = txt || '';
  while ((m = re.exec(txt))) {
    push(txt.slice(last, m.index), {});
    const tok = m[0];
    if (tok === '<br>') { if (out.length) out[out.length - 1].options.breakLine = true; else out.push({ text: '', options: { ...base, breakLine: true } }); }
    else if (tok.startsWith('**')) push(tok.slice(2, -2), { bold: true });
    else if (tok.startsWith('[DA VERIFICARE')) push(tok, { color: AVVISO, bold: true });
    else push(tok.slice(1, -1), { italic: true });
    last = m.index + tok.length;
  }
  push(txt.slice(last), {});
  if (!out.length) out.push({ text: '', options: { ...base } });
  return out;
}
// Paragrafi: "- " elenco puntato, "1. " elenco numerato, altrimenti paragrafo
function paras(txt, { gap = 6, base = {} } = {}) {
  const ls = (txt || '').split('\n').filter((l) => l.trim() !== '');
  const out = [];
  ls.forEach((l, i) => {
    let opt = { paraSpaceAfter: gap };
    let t = l;
    if (l.startsWith('- ')) { t = l.slice(2); opt.bullet = { indent: 13 }; }
    let num = null;
    if (!l.startsWith('- ') && /^\d+\. /.test(l)) { num = l.match(/^(\d+)\. /)[1]; t = l.replace(/^\d+\. /, ''); }
    const rr = runs(t, base);
    if (num) rr.unshift({ text: num + '   ', options: { ...base, bold: true, color: B.C.accent4 } });
    rr[0].options = { ...rr[0].options, ...opt };
    rr[rr.length - 1].options.breakLine = i < ls.length - 1;
    out.push(...rr);
  });
  return out;
}
const words = (t) => plain(t).split(/\s+/).filter(Boolean).length;
const num = (v) => parseFloat(String(v).replace(/\./g, '').replace(',', '.'));

// ---------------- Componenti locali ----------------
const T = (s, txt, o) => s.addText(txt, Object.assign({ isTextBox: true, margin: 0, valign: 'top' }, o));
function occhiello(s, txt) { if (txt) label(s, txt, G.X, 0.47, 6.5); }
function fonte(s, txt) {
  if (!txt) return 0;
  const lunga = txt.length > 165;
  const h = lunga ? 0.34 : 0.2;
  T(s, runs(txt), { x: G.X, y: G.FOOT_Y - 0.06 - h, w: G.CW, h, fontSize: 7.5, color: B.C.accent6, valign: 'bottom', objectName: 'fonte' });
  return h + 0.1; // spazio occupato sopra il piede
}
const bottomOf = (fh) => G.FOOT_Y - 0.08 - Math.max(fh, 0.2);
function note(s, sl) {
  let t = (sl.f.note || '').split('\n').filter(Boolean).map((l) => l.replace(/^- /, '• ')).join('\n');
  if (sl.f.alternative) t += (t ? '\n' : '') + 'Proposte da scegliere:\n' + sl.f.alternative.split('\n').filter(Boolean).map((l) => '   ' + l.replace(' | ', ' ')).join('\n');
  const min = (sl.f.min || '').replace('0 · solo dispensa', 'solo dispensa, in aula si salta');
  s.addNotes((t ? t + '\n' : '') + 'Tempo: ' + (/^[\d.]+$/.test(min) ? min.replace('.', ',') + ' min' : min));
}
function iconeDa(visual) {
  const m = (visual || '').match(/icone Lucide: (.*)$/);
  return m ? m[1].split(',').map((x) => 'Lu' + x.trim()) : [];
}
function sintesi(s, txt, y, h = 0.42) {
  if (!txt) return;
  T(s, runs(txt), { x: G.X, y, w: G.CW, h, fontSize: plain(txt).length > 150 ? 11 : 12, bold: true, color: B.C.accent1, valign: 'middle', objectName: 'sintesi' });
}
// Riquadro segnaposto per immagini non ancora disponibili
function segnaposto(s, x, y, w, h, testo) {
  s.addShape('rect', { x, y, w, h, fill: { color: 'FBEDEA' }, line: { color: AVVISO, width: 1, dashType: 'dash' } });
  T(s, '[DA INSERIRE · ' + testo + ']', { x: x + 0.2, y, w: w - 0.4, h, fontSize: 10, bold: true, color: AVVISO, align: 'center', valign: 'middle' });
}
let fatti = [];
const H = (s, sl) => header(s, Object.assign({ corrente: sl.cap, fatti: fatti.filter((c) => c !== sl.cap) }, DECK));

// ---------------- Renderer per tipo ----------------
const R = {};

R.COPERTINA = async (pres, sl) => {
  const s = pres.addSlide({ masterName: 'BA Copertina' });
  compassRings(s);
  s.addText(sl.f.occhiello, { placeholder: 'occhiello' });
  s.addText(sl.f.titolo, { placeholder: 'title' });
  s.addText(sl.f.sottotitolo, { placeholder: 'sottotitolo' });
  s.addText(sl.f.docenti, { placeholder: 'docenti' });
  return s;
};

R.DOMANDA = async (pres, sl) => {
  const s = pres.addSlide({ masterName: 'BA Contenuto' });
  H(s, sl); occhiello(s, sl.f.occhiello);
  s.addText(sl.f.titolo, { placeholder: 'title' });
  const ls = sl.f.corpo.split('\n').filter(Boolean);
  const intro = ls.filter((l) => !l.startsWith('- '));
  const items = ls.filter((l) => l.startsWith('- ')).map((l) => l.slice(2));
  T(s, intro.join(' '), { x: G.X, y: G.BODY_Y + 0.05, w: G.CW, h: 0.4, fontSize: 16, bold: true, color: B.C.accent1 });
  const ic = ['LuUser', 'LuGauge', 'LuTarget', 'LuMessageCircleQuestion'];
  for (let i = 0; i < items.length; i++) {
    const y = G.BODY_Y + 0.7 + i * 0.85;
    await iconDot(s, ic[i % ic.length], G.X, y, 0.6);
    T(s, runs(items[i]), { x: G.X + 0.85, y, w: 7.8, h: 0.6, fontSize: 20, color: B.C.text1, valign: 'middle' });
  }
  return s;
};

R.AGENDA = async (pres, sl) => {
  const s = pres.addSlide({ masterName: 'BA Contenuto' });
  H(s, sl); occhiello(s, sl.f.occhiello);
  s.addText(sl.f.titolo, { placeholder: 'title' });
  const sess = [];
  for (const l of sl.f.corpo.split('\n').filter(Boolean)) {
    if (l.startsWith('- ')) sess[sess.length - 1].items.push(l.slice(2));
    else { const p = l.split(' · '); sess.push({ num: p[0].replace(/\D/g, ''), data: p[1], modo: p[2] + ' · ' + p[3], tit: p[4], items: [] }); }
  }
  sess.forEach((c, i) => {
    const x = G.X + i * 3.05, w = 2.85, y = G.BODY_Y + 0.05;
    card(s, { x, y, w, h: 3.2 });
    s.addText(c.num, { shape: 'ellipse', x: x + 0.22, y: y + 0.22, w: 0.42, h: 0.42, fill: { color: i === 0 ? B.C.accent4 : B.C.text1 }, line: { type: 'none' }, color: B.C.background1, fontSize: 14, bold: true, align: 'center', valign: 'middle', margin: 0 });
    T(s, c.data, { x: x + 0.78, y: y + 0.2, w: w - 0.9, h: 0.25, fontSize: 12, bold: true, color: B.C.text1 });
    T(s, c.modo, { x: x + 0.78, y: y + 0.44, w: w - 0.9, h: 0.22, fontSize: 9.5, color: B.C.accent6 });
    T(s, c.tit, { x: x + 0.22, y: y + 0.88, w: w - 0.4, h: 0.3, fontSize: 13, bold: true, color: B.C.accent1 });
    T(s, paras(c.items.map((t) => '- ' + t).join('\n'), { gap: 5 }), { x: x + 0.22, y: y + 1.28, w: w - 0.35, h: 1.8, fontSize: 10.5, color: B.C.text2 });
  });
  if (sl.f.sintesi) T(s, sl.f.sintesi, { x: G.X, y: 4.72, w: G.CW, h: 0.3, fontSize: 12.5, bold: true, color: B.C.text1 });
  return s;
};

R.CONTENUTO = async (pres, sl) => {
  const s = pres.addSlide({ masterName: 'BA Contenuto' });
  H(s, sl); occhiello(s, sl.f.occhiello);
  s.addText(sl.f.titolo, { placeholder: 'title' });
  const bottom = bottomOf(fonte(s, sl.f.fonte));
  const y0 = G.BODY_Y + 0.05;
  const hasR = sl.f.esempi || sl.f.attenzione;
  const lw = hasR ? 4.45 : G.CW;
  const nw = words(sl.f.corpo);
  const soloNumeri = !hasR && sl.f.corpo.split('\n').filter(Boolean).every((l) => /^\d+\. /.test(l));
  const fs0 = hasR ? (nw > 105 ? 11.5 : nw > 90 ? 12 : nw > 75 ? 12.5 : nw > 55 ? 13 : 14) : (nw > 110 ? 13 : 14);
  T(s, paras(sl.f.corpo, { gap: soloNumeri ? 12 : 8 }), { x: G.X, y: y0 + (soloNumeri ? 0.1 : 0), w: lw, h: bottom - y0, fontSize: soloNumeri ? 18 : fs0, color: B.C.text2, lineSpacingMultiple: 1.08, objectName: 'corpo' });
  if (!hasR) return s;
  const rx = 5.2, rw = G.R - rx;
  const attH = sl.f.attenzione ? (plain(sl.f.attenzione).length > 85 ? 1.05 : plain(sl.f.attenzione).length > 50 ? 0.9 : 0.8) : 0;
  if (sl.f.esempi) {
    const eh = bottom - y0 - (attH ? attH + 0.15 : 0);
    card(s, { x: rx, y: y0, w: rw, h: eh });
    label(s, 'IN PRATICA', rx + 0.25, y0 + 0.18, rw - 0.5);
    const ew = words(sl.f.esempi);
    T(s, paras(sl.f.esempi, { gap: 4 }), { x: rx + 0.25, y: y0 + 0.5, w: rw - 0.45, h: eh - 0.62, fontSize: ew > 58 ? 9.5 : ew > 50 ? 10 : ew > 40 ? 11 : 12, color: B.C.text2, objectName: 'esempi' });
  }
  if (sl.f.attenzione) {
    const ay = sl.f.esempi ? bottom - attH : y0;
    card(s, { x: rx, y: ay, w: rw, h: attH, dark: true });
    label(s, 'ATTENZIONE', rx + 0.25, ay + 0.13, rw - 0.5, B.C.accent2);
    T(s, runs(sl.f.attenzione), { x: rx + 0.25, y: ay + 0.38, w: rw - 0.45, h: attH - 0.46, fontSize: plain(sl.f.attenzione).length > 85 ? 11.5 : 12.5, bold: true, color: B.C.background1, objectName: 'attenzione' });
  }
  return s;
};

R.QUATTRO_CARD = async (pres, sl) => {
  const s = pres.addSlide({ masterName: 'BA Contenuto' });
  H(s, sl); occhiello(s, sl.f.occhiello);
  s.addText(sl.f.titolo, { placeholder: 'title' });
  const ls = sl.f.corpo.split('\n').filter(Boolean);
  const intro = ls.filter((l) => !l.startsWith('- ')).join(' ');
  const items = ls.filter((l) => l.startsWith('- ')).map((l) => l.slice(2).split(' · '));
  const ic = iconeDa(sl.f.visual);
  const fh = fonte(s, sl.f.fonte);
  let y0 = G.BODY_Y + 0.02;
  if (intro) { T(s, runs(intro), { x: G.X, y: y0, w: G.CW, h: 0.28, fontSize: 12, italic: true, color: B.C.text2 }); y0 += 0.36; }
  const maxDesc = Math.max(...items.map((it) => plain(it[it.length - 1]).length));
  const sintH = sl.f.sintesi ? 0.5 : 0;
  const ch = Math.min((bottomOf(fh) - y0 - sintH - 0.13) / 2, maxDesc > 120 ? 1.6 : intro ? 1.18 : 1.27);
  const dfs = maxDesc > 150 ? 10.5 : maxDesc > 110 ? 11 : 11.5;
  for (let i = 0; i < 4; i++) {
    const it = items[i]; if (!it) continue;
    const x = G.X + (i % 2) * 4.6, y = y0 + Math.floor(i / 2) * (ch + 0.13), w = 4.4;
    card(s, { x, y, w, h: ch });
    await iconDot(s, ic[i] || 'LuSparkles', x + 0.22, y + 0.22, 0.5);
    const tit = [{ text: it[0], options: { bold: true, color: B.C.text1 } }];
    let desc = it.slice(1).join(' · ');
    const tagSopra = it.length === 3 && /^[A-ZÀ-Ü ]+$/.test(it[1]);
    let ty = y + 0.17;
    if (tagSopra) { label(s, it[1], x + 0.9, y + 0.13, w - 1.05, B.C.accent4); ty = y + 0.33; desc = it[2]; }
    else if (it.length === 3) { tit.push({ text: '   ' + it[1], options: { bold: true, color: B.C.accent4 } }); desc = it[2]; }
    T(s, tit, { x: x + 0.9, y: ty, w: w - 1.05, h: 0.32, fontSize: 14, valign: 'middle' });
    T(s, runs(desc), { x: x + 0.9, y: ty + 0.35, w: w - 1.05, h: ch - (ty - y) - 0.42, fontSize: dfs, color: B.C.text2 });
  }
  if (sl.f.sintesi) sintesi(s, sl.f.sintesi, y0 + 2 * ch + 0.13 + 0.06, 0.45);
  return s;
};

// Stima delle righe occupate da un testo (con <br>) in una colonna larga w pollici
const righe = (t, w, cw) => (t || '').split('<br>').reduce((a, p) => a + Math.max(1, Math.ceil((plain(p).length * cw * 1.12) / Math.max(0.3, w - 0.2))), 0);

R.TABELLA = async (pres, sl) => {
  const s = pres.addSlide({ masterName: 'BA Contenuto' });
  H(s, sl); occhiello(s, sl.f.occhiello);
  s.addText(sl.f.titolo, { placeholder: 'title' });
  const fh = fonte(s, sl.f.fonte);
  let y0 = G.BODY_Y + 0.02;
  if (sl.f.intro) { const ih = plain(sl.f.intro).length > 120 ? 0.42 : 0.26; T(s, runs(sl.f.intro), { x: G.X, y: y0 - 0.02, w: G.CW, h: ih, fontSize: 11.5, color: B.C.text2, valign: 'middle' }); y0 += ih + 0.08; }
  const rows = sl.f.righe.split('\n').filter(Boolean).map((r) => r.split(' | '));
  const nc = rows[0].length, nr = rows.length - 1;
  void nc;
  const avail = bottomOf(fh) - y0 - (sl.f.sintesi ? 0.5 : 0);
  const col = (c) => rows.slice(1).map((r) => r[c] || '');
  const peso = rows[0].map((_, c) => { const v = col(c).map((t) => plain(t).length); return 0.5 * (v.reduce((a, b) => a + b, 0) / nr) + 0.5 * Math.max(...v); });
  // prova corpi decrescenti finché la tabella sta nello spazio disponibile
  let fsz, colW, tabH, rowH;
  for (fsz of [12, 11.5, 11, 10.5, 10, 9.5, 9]) {
    const cw = 0.0056 * fsz;
    const minW = rows[0].map((h, c) => Math.max(0.9, Math.max(...col(c).flatMap((t) => plain(t).split(/\s+/)).map((w) => w.length)) * cw * (c === 0 ? 1.75 : 1.2) + 0.25, Math.max(...h.split(' ').map((w) => w.length)) * 0.1 + 0.3));
    colW = peso.map((p) => G.CW * p / peso.reduce((a, b) => a + b, 0));
    for (let it = 0; it < 6; it++) {
      colW = colW.map((w, c) => Math.max(w, minW[c]));
      const extra = colW.reduce((a, b) => a + b, 0) - G.CW; if (extra <= 0.001) break;
      const liberi = colW.map((w, c) => w - minW[c]); const tl = liberi.reduce((a, b) => a + b, 0);
      colW = colW.map((w, c) => w - extra * liberi[c] / tl);
    }
    rowH = nr <= 6 ? 0.36 : 0.3;
    const rs = rows.map((r) => Math.max(...r.map((t, c) => righe(t, colW[c], cw * (c === 0 ? 1.1 : 1)))));
    tabH = rs.reduce((a, l, i) => a + Math.max(i === 0 ? 0.3 : rowH, l * fsz / 72 * 1.22 + 0.1), 0);
    if (tabH <= avail * 0.92) break;
  }
  const hdr = (t) => ({ text: t, options: { bold: true, color: B.C.background1, fontSize: 8, charSpacing: 1.5, fill: { color: B.C.text1 } } });
  const tb = [rows[0].map(hdr)].concat(rows.slice(1).map((r, kk) => {
    const f = { color: kk % 2 ? B.C.background1 : B.C.background2 };
    return r.map((t, c) => ({ text: runs(t), options: { color: c === 0 ? B.C.text1 : B.C.text2, bold: c === 0, fill: f } }));
  }));
  s.addTable(tb, { x: G.X, y: y0, w: G.CW, colW, rowH, fontSize: fsz, fontFace: B.FONT, valign: 'middle', margin: [0.05, 0.1, 0.05, 0.1], border: { type: 'none' }, objectName: 'tabella' });
  if (sl.f.sintesi) sintesi(s, sl.f.sintesi, bottomOf(fh) - 0.45);
  return s;
};

R.DUE_CARD = async (pres, sl) => {
  const s = pres.addSlide({ masterName: 'BA Contenuto' });
  H(s, sl); occhiello(s, sl.f.occhiello);
  s.addText(sl.f.titolo, { placeholder: 'title' });
  const fh = fonte(s, sl.f.fonte);
  const y = G.BODY_Y + 0.05;
  const dx = sl.f.card_dx.split('\n').filter(Boolean), sx = sl.f.card_sx.split('\n').filter(Boolean);
  const kv = dx.slice(1).filter((l) => /^(\*\*)?[A-ZÀ-Ü][a-zà-ù]+(\*\*)? · /.test(l)).length >= 3;
  const wL = kv ? 3.6 : 4.4, xR = G.X + wL + 0.2, wR = G.R - xR;
  const lineH = (l, w, f = 13) => Math.ceil(plain(l).length * 1.1 / (w * 11.5 * 13 / f)) * 0.24 * f / 13 + 0.12;
  const casoH = sl.f.caso ? 0.62 : 0;
  const maxCh = bottomOf(fh) - y - casoH - (sl.f.sintesi ? 0.5 : 0) - 0.05;
  const need = (lines, w, f) => 0.55 + (lines[0].includes(' · ') ? 0.7 : 0) + (kv && lines === dx ? (lines.length - 1) * 0.46 : lines.slice(1).reduce((a, l) => a + (l.startsWith('«') ? 0.6 : lineH(l, w - 0.5, f) + 0.04), 0)) + 0.2;
  let bf = 13;
  while (bf > 11 && Math.max(need(sx, wL, bf), need(dx, wR, bf)) > maxCh) bf -= 0.5;
  const ch = Math.min(maxCh, Math.max(2.0, need(sx, wL, bf), need(dx, wR, bf)));
  const side = (lines, x, w, dark) => {
    card(s, { x, y, w, h: ch, dark });
    const [lab, big] = lines[0].split(' · ');
    label(s, lab, x + 0.25, y + 0.22, w - 0.5, dark ? B.C.accent2 : B.C.accent1);
    let yy = y + 0.55;
    const col = dark ? B.C.background1 : B.C.text1, col2 = dark ? 'D7E2EC' : B.C.text2;
    if (big) { T(s, big, { x: x + 0.25, y: yy, w: w - 0.5, h: 0.55, fontSize: 28, bold: true, color: dark ? B.C.accent2 : B.C.accent4 }); yy += 0.7; }
    const rest = lines.slice(1);
    if (kv && dark) {
      rest.forEach((l, k2) => {
        const [kk, vv] = l.replace(/\*\*/g, '').split(' · ');
        T(s, kk, { x: x + 0.25, y: yy + k2 * 0.46, w: 0.95, h: 0.4, fontSize: 11, bold: true, color: B.C.accent2 });
        T(s, runs(vv), { x: x + 1.2, y: yy + k2 * 0.46, w: w - 1.4, h: 0.44, fontSize: 11, color: B.C.background1 });
      });
      return;
    }
    rest.forEach((l) => {
      if (l.startsWith('«')) { T(s, l, { x: x + 0.25, y: yy, w: w - 0.5, h: 0.45, fontSize: 15, italic: true, color: col }); yy += 0.6; return; }
      const nh = lineH(l, w - 0.5, bf);
      T(s, runs(l, dark ? { color: col2 } : {}), { x: x + 0.25, y: yy, w: w - 0.5, h: nh, fontSize: bf, color: col2 });
      yy += nh + 0.04;
    });
  };
  side(sx, G.X, wL, false);
  side(dx, xR, wR, true);
  let yb = y + ch + 0.1;
  if (sl.f.caso) {
    card(s, { x: G.X, y: yb, w: G.CW, h: casoH - 0.08, tint: true });
    label(s, 'CASO REALE', G.X + 0.2, yb + 0.06, 1.5);
    T(s, runs(sl.f.caso), { x: G.X + 1.6, y: yb, w: G.CW - 1.8, h: casoH - 0.08, fontSize: 11, color: B.C.text1, valign: 'middle' });
    yb += casoH;
  }
  if (sl.f.sintesi) sintesi(s, sl.f.sintesi, yb - 0.02, 0.48);
  return s;
};

R.ESERCIZIO = async (pres, sl) => {
  const s = pres.addSlide({ masterName: 'BA Contenuto' });
  H(s, sl); occhiello(s, sl.f.occhiello);
  s.addText(sl.f.titolo, { placeholder: 'title' });
  fonte(s, sl.f.fonte);
  const steps = sl.f.passi.split('\n').filter(Boolean).map((l) => l.replace(/^\d+ · /, ''));
  const n = steps.length, sp = n >= 5 ? 0.67 : 0.8;
  steps.forEach((st, i) => {
    const y = G.BODY_Y + 0.25 + i * sp;
    s.addText(String(i + 1), { shape: 'ellipse', x: G.X, y, w: 0.4, h: 0.4, fill: { color: B.C.accent1 }, line: { type: 'none' }, color: B.C.background1, fontSize: 13, bold: true, align: 'center', valign: 'middle', margin: 0 });
    if (i < n - 1) s.addShape('line', { x: G.X + 0.2, y: y + 0.44, w: 0, h: sp - 0.48, line: { color: HEX.linea, width: 1 } });
    const c = st.indexOf(':');
    const t = c > 0 && c < 22 ? [{ text: st.slice(0, c + 1) + ' ', options: { bold: true, color: B.C.text1 } }, { text: st.slice(c + 1).trim(), options: { color: B.C.text2 } }] : runs(st, { color: B.C.text1 });
    T(s, t, { x: 1.1, y: y + 0.2 - (sp - 0.05) / 2, w: 5.0, h: sp - 0.05, fontSize: n >= 5 ? 12 : 13, valign: 'middle' });
  });
  const cx = 6.45, cw = 3.05, cy = G.BODY_Y + 0.05, chh = 3.25;
  card(s, { x: cx, y: cy, w: cw, h: chh, dark: true });
  const occ = (sl.f.occhiello || '').toUpperCase();
  const ic = occ.includes('ESPERIMENTO') ? 'LuFlaskConical' : occ.includes('LABORATORIO') ? 'LuFileText' : 'LuListChecks';
  await iconDot(s, ic, cx + 0.25, cy + 0.25, 0.5, { dark: true });
  label(s, 'RISULTATO', cx + 0.25, cy + 0.95, cw - 0.5, B.C.accent2);
  T(s, runs(sl.f.output), { x: cx + 0.25, y: cy + 1.2, w: cw - 0.45, h: 0.95, fontSize: 12, color: B.C.background1 });
  label(s, 'REGOLA', cx + 0.25, cy + 2.2, cw - 0.5, B.C.accent2);
  T(s, runs(sl.f.regola), { x: cx + 0.25, y: cy + 2.45, w: cw - 0.45, h: 0.75, fontSize: plain(sl.f.regola).length > 90 ? 11 : 12, color: B.C.background1 });
  return s;
};

R.COMPASS = async (pres, sl) => {
  const s = pres.addSlide({ masterName: 'BA Contenuto' });
  H(s, sl); occhiello(s, sl.f.occhiello);
  s.addText(sl.f.titolo, { placeholder: 'title' });
  const ls = sl.f.corpo.split('\n').filter(Boolean);
  const modi = ls.filter((l) => l.startsWith('- ')).map((l) => {
    const m = l.slice(2).match(/^(\w) · (\w+) · ([^:]+): (.*)$/);
    return [m[1], m[2], m[3], m[4].charAt(0).toUpperCase() + m[4].slice(1)];
  });
  const dataLine = ls.find((l) => l.startsWith('DATA'));
  const hl = COMPASS_HL;
  const cx = 1.85, cy = 3.05, Rr = 1.08, d = 0.42;
  s.addShape('ellipse', { x: cx - Rr, y: cy - Rr, w: 2 * Rr, h: 2 * Rr, fill: { color: B.C.background2 }, line: { color: B.C.text1, width: 1.25 } });
  s.addShape('ellipse', { x: cx - Rr * 0.7, y: cy - Rr * 0.7, w: 2 * Rr * 0.7, h: 2 * Rr * 0.7, fill: { type: 'none' }, line: { color: HEX.linea, width: 1 } });
  s.addShape(pres.ShapeType.triangle, { x: cx - 0.1, y: cy - 0.68, w: 0.2, h: 0.68, fill: { color: B.C.accent4 }, line: { type: 'none' } });
  s.addShape(pres.ShapeType.triangle, { x: cx - 0.1, y: cy, w: 0.2, h: 0.55, fill: { color: B.C.text1 }, line: { type: 'none' }, rotate: 180 });
  s.addShape('ellipse', { x: cx - 0.045, y: cy - 0.045, w: 0.09, h: 0.09, fill: { color: B.C.background1 }, line: { color: B.C.text1, width: 0.75 } });
  modi.forEach((m, i) => {
    const a = -Math.PI / 2 + i * 2 * Math.PI / 7, on = hl.includes(i);
    s.addText(m[0], { shape: 'ellipse', x: cx + Rr * Math.cos(a) - d / 2, y: cy + Rr * Math.sin(a) - d / 2, w: d, h: d, fill: { color: on ? B.C.accent4 : B.C.text1 }, line: { color: B.C.background1, width: 2 }, color: B.C.background1, fontSize: 12, bold: true, align: 'center', valign: 'middle', margin: 0 });
  });
  T(s, 'La bussola orienta.\nLa direzione la sceglie chi guida.', { x: 0.5, y: 4.33, w: 2.7, h: 0.5, fontSize: 10, italic: true, color: B.C.text2, align: 'center' });
  const lx0 = 3.7, rh = 0.4;
  modi.forEach((m, i) => {
    const y = G.BODY_Y + 0.02 + i * rh, on = hl.includes(i);
    s.addText(m[0], { shape: 'ellipse', x: lx0, y: y + 0.04, w: 0.28, h: 0.28, fill: { color: on ? B.C.accent4 : B.C.text1 }, line: { type: 'none' }, color: B.C.background1, fontSize: 9.5, bold: true, align: 'center', valign: 'middle', margin: 0 });
    T(s, [
      { text: m[1], options: { bold: true, color: B.C.text1, fontSize: 11 } },
      { text: '  ' + m[2], options: { color: B.C.accent1, fontSize: 10.5, bold: true, breakLine: true } },
      { text: m[3], options: { color: B.C.text2, fontSize: 10 } },
    ], { x: lx0 + 0.4, y, w: 5.4, h: rh, lineSpacingMultiple: 0.95 });
  });
  s.addShape('rect', { x: lx0, y: 4.25, w: 5.8, h: 0.5, fill: { color: B.C.text1 }, line: { type: 'none' } });
  s.addImage({ data: await icon('LuDatabase', HEX.tealChiaro), x: lx0 + 0.14, y: 4.36, w: 0.28, h: 0.28 });
  const dtxt = dataLine.replace(/^DATA · /, '');
  T(s, [{ text: 'DATA  ', options: { bold: true, fontSize: 12, color: B.C.background1 } }, { text: dtxt, options: { fontSize: 10.5, color: B.C.background1 } }], { x: lx0 + 0.55, y: 4.25, w: 5.15, h: 0.5, valign: 'middle' });
  fonte(s, sl.f.fonte);
  return s;
};

R.SEZIONE = async (pres, sl) => {
  const s = pres.addSlide({ masterName: 'BA Sezione' });
  const n = parseInt(sl.f.numero, 10);
  s.addText(sl.f.numero, { placeholder: 'numero' });
  s.addText(sl.f.titolo, { placeholder: 'title' });
  s.addText(runs(sl.f.sottotitolo), { placeholder: 'sottotitolo' });
  DECK.capitoli.forEach((c, i) => {
    const y = 0.8 + i * 0.4, on = i + 1 === n, done = fatti.includes(i + 1);
    if (on) s.addShape('ellipse', { x: 6.52, y: y + 0.12, w: 0.1, h: 0.1, fill: { color: B.C.accent4 }, line: { type: 'none' } });
    T(s, [{ text: String(i + 1).padStart(2, '0') + '   ', options: { bold: true, color: on ? B.C.accent4 : '5B7088' } }, { text: c, options: { bold: on, color: on ? B.C.background1 : done ? B.C.accent2 : '8FA3B5' } }],
      { x: 6.75, y, w: 2.75, h: 0.34, fontSize: 10.5, valign: 'middle' });
  });
  return s;
};

let rtVariante = CFG.red_tag_variante || 'vermiglio';
R.RED_TAG = async (pres, sl) => {
  const v = sl.f.variante || rtVariante;
  const s = pres.addSlide({ masterName: 'BA RED TAG ' + v });
  const dark = v === 'vermiglio';
  s.addImage({ data: await icon('LuTag', dark ? '2A0A05' : HEX.notte), x: 0.6, y: 0.7, w: 0.28, h: 0.28 });
  s.addText(sl.f.etichetta.replace(' · ', '  ·  '), { placeholder: 'etichetta' });
  const [a, b] = sl.f.frase.split(' | ');
  s.addText([
    { text: a, options: { breakLine: true, color: dark ? 'FFFFFF' : '7A5A00' } },
    { text: b, options: { color: dark ? '2A0A05' : HEX.notte } },
  ], { placeholder: 'frase', fontSize: (a.length + b.length) > 70 ? 36 : 42 });
  return s;
};

R.TOCCA_A_VOI = async (pres, sl) => {
  const s = pres.addSlide({ masterName: 'BA Tocca a voi' });
  H(s, sl);
  s.addText(sl.f.invito, { placeholder: 'invito' });
  s.addText(sl.f.titolo, { placeholder: 'title' });
  const qx = 3.35, qw = G.R - qx;
  const qs = sl.f.domande.split('\n').filter(Boolean).map((l) => l.replace(/^\d+ /, ''));
  const rh = 0.53;
  qs.forEach((q, i) => {
    const y = G.BODY_Y - 0.02 + i * rh;
    T(s, String(i + 1).padStart(2, '0'), { x: qx, y, w: 0.45, h: rh - 0.06, fontSize: 13, bold: true, color: B.C.accent1, valign: 'middle' });
    T(s, q, { x: qx + 0.5, y, w: qw - 0.5, h: rh - 0.06, fontSize: q.length > 80 ? 11.5 : 12.5, color: B.C.text1, valign: 'middle' });
    if (i < qs.length - 1) s.addShape('line', { x: qx + 0.5, y: y + rh - 0.03, w: qw - 0.5, h: 0, line: { color: HEX.linea, width: 0.5 } });
  });
  const by = G.BODY_Y - 0.02 + qs.length * rh + 0.08;
  card(s, { x: qx, y: by, w: qw, h: 0.78, tint: true });
  s.addImage({ data: await icon('LuLightbulb', HEX.teal), x: qx + 0.18, y: by + 0.22, w: 0.34, h: 0.34 });
  T(s, sl.f.suggerimento, { x: qx + 0.65, y: by, w: qw - 0.8, h: 0.78, fontSize: 11, color: B.C.text1, valign: 'middle' });
  return s;
};

R.PAUSA = async (pres, sl) => {
  const s = pres.addSlide({ masterName: 'BA Scura' });
  s.addImage({ data: await icon('LuCoffee', HEX.tealChiaro), x: G.X, y: 1.75, w: 0.5, h: 0.5 });
  T(s, sl.f.titolo, { x: G.X, y: 2.4, w: G.CW, h: 0.8, fontSize: 40, bold: true, color: B.C.background1, valign: 'middle' });
  T(s, sl.f.durata, { x: G.X, y: 3.2, w: G.CW, h: 0.4, fontSize: 15, color: B.C.accent2 });
  return s;
};

R.CHIUSURA = async (pres, sl) => {
  const s = pres.addSlide({ masterName: 'BA Scura' });
  label(s, sl.f.etichetta, G.X, 0.5, 6, B.C.accent2);
  s.addText(sl.f.titolo, { placeholder: 'title' });
  await iconDot(s, 'LuFlag', G.X, 1.75, 0.5, { dark: true });
  T(s, sl.f.sottotitolo, { x: 1.2, y: 1.75, w: 8, h: 0.5, fontSize: 14, bold: true, color: B.C.accent2, valign: 'middle' });
  T(s, paras(sl.f.corpo, { gap: 7 }), { x: 1.2, y: 2.35, w: 8.3, h: 1.8, fontSize: 13.5, color: B.C.background1 });
  T(s, sl.f.aggancio, { x: 1.2, y: 4.3, w: 8, h: 0.35, fontSize: 12.5, color: B.C.accent2 });
  return s;
};

// NUMERI: grafico nativo (facoltativo) + numeri grandi + box "come è stato misurato" + sintesi
R.NUMERI = async (pres, sl) => {
  const s = pres.addSlide({ masterName: 'BA Contenuto' });
  H(s, sl); occhiello(s, sl.f.occhiello);
  s.addText(sl.f.titolo, { placeholder: 'title' });
  const fh = fonte(s, sl.f.fonte);
  const bottom = bottomOf(fh);
  let y0 = G.BODY_Y + 0.02;
  const nums = (sl.f.numeri || '').split('\n').filter(Boolean).map((l) => l.split(' | '));
  const sintH = sl.f.sintesi ? 0.5 : 0;
  const critH = sl.f.criterio ? (plain(sl.f.criterio).length > 105 ? 0.8 : 0.66) : 0;
  const zoneB = bottom - sintH - critH;
  // corpo breve in alto
  if (sl.f.corpo) {
    const ls = sl.f.corpo.split('\n').filter(Boolean);
    const h = ls.reduce((a, l) => a + Math.ceil(plain(l).length / 130) * 0.21, 0) + 0.06 * (ls.length - 1) + 0.04;
    T(s, paras(sl.f.corpo, { gap: 4 }), { x: G.X, y: y0, w: G.CW, h, fontSize: 12, color: B.C.text2, valign: 'top' });
    y0 += h + 0.12;
  }
  let nx = G.X, nw = G.CW;
  if (sl.f.grafico) {
    const gl = sl.f.grafico.split('\n').filter(Boolean);
    const titolo = (gl.find((l) => l.startsWith('titolo:')) || '').replace('titolo: ', '');
    const dati = gl.filter((l) => l.includes(' | ')).map((l) => l.split(' | '));
    const labels = dati.map((d) => d[0]);
    const vals = dati.map((d) => num(d[1]));
    // la barra di confronto ("UE", "Europa", "media") in un colore diverso: due serie impilate
    const isCfr = (l) => /UE|Europa|media/i.test(l);
    const data = [
      { name: 'Serie', labels, values: vals.map((v, i) => (isCfr(labels[i]) ? 0 : v)) },
      { name: 'Confronto', labels, values: vals.map((v, i) => (isCfr(labels[i]) ? v : 0)) },
    ];
    const gw = 4.6;
    T(s, titolo, { x: G.X, y: y0, w: gw, h: 0.26, fontSize: 9.5, bold: true, color: B.C.text1 });
    s.addChart(pres.charts.BAR, data, {
      x: G.X - 0.05, y: y0 + 0.26, w: gw, h: zoneB - y0 - 0.36, barDir: 'col', barGrouping: 'stacked', barGapWidthPct: 55,
      chartColors: [HEX.blu, HEX.navy], showLegend: false, showValue: true, dataLabelFormatCode: '0.0;;;', dataLabelColor: 'FFFFFF', dataLabelFontSize: 10, dataLabelFontBold: true, dataLabelPosition: 'inEnd',
      catAxisLabelColor: HEX.testo, catAxisLabelFontSize: 9, catAxisLabelFontFace: B.FONT, valAxisHidden: true, valGridLine: { style: 'none' }, catAxisLineShow: false,
      dataLabelFontFace: B.FONT, objectName: 'grafico',
    });
    nx = G.X + gw + 0.25; nw = G.R - nx;
  }
  // numeri grandi
  if (nums.length) {
    const zone = zoneB - y0 - 0.08;
    if (!sl.f.grafico) {
      // in riga (3 o 4 colonne)
      const n = nums.length, gap = 0.18, w = (G.CW - gap * (n - 1)) / n, h = Math.min(zone, 1.75);
      nums.forEach(([v, t], i) => {
        const x = G.X + i * (w + gap);
        const neg = /^[−-]/.test(v);
        card(s, { x, y: y0, w, h, dark: neg });
        T(s, v, { x: x + 0.2, y: y0 + 0.12, w: w - 0.3, h: 0.55, fontSize: v.length > 8 ? 21 : v.length > 6 ? 25 : 30, bold: true, color: neg ? B.C.accent2 : B.C.accent4, valign: 'middle' });
        T(s, runs(t), { x: x + 0.2, y: y0 + 0.72, w: w - 0.3, h: h - 0.8, fontSize: 10.5, color: neg ? B.C.background1 : B.C.text2 });
      });
    } else {
      const n = nums.length, gap = 0.12, h = (zone - gap * (n - 1)) / n;
      nums.forEach(([v, t], i) => {
        const y = y0 + i * (h + gap);
        card(s, { x: nx, y, w: nw, h });
        T(s, v, { x: nx + 0.2, y, w: 1.45, h, fontSize: v.length > 6 ? 22 : 26, bold: true, color: B.C.accent4, valign: 'middle' });
        T(s, runs(t), { x: nx + 1.7, y, w: nw - 1.85, h, fontSize: 11, color: B.C.text2, valign: 'middle' });
      });
    }
  }
  if (sl.f.criterio) {
    const cy = zoneB + 0.04;
    card(s, { x: G.X, y: cy, w: G.CW, h: critH - 0.08, tint: true });
    s.addImage({ data: await icon('LuRuler', HEX.teal), x: G.X + 0.18, y: cy + (critH - 0.08) / 2 - 0.14, w: 0.28, h: 0.28 });
    label(s, 'COME È STATO MISURATO', G.X + 0.6, cy + 0.07, 3);
    T(s, runs(sl.f.criterio), { x: G.X + 0.6, y: cy + 0.29, w: G.CW - 0.8, h: critH - 0.08 - 0.33, fontSize: 10.5, color: B.C.text1, valign: 'top' });
  }
  if (sl.f.sintesi) sintesi(s, sl.f.sintesi, bottom - sintH + 0.02, 0.46);
  return s;
};

// TIMELINE: tappe in orizzontale collegate da una linea
R.TIMELINE = async (pres, sl) => {
  const s = pres.addSlide({ masterName: 'BA Contenuto' });
  H(s, sl); occhiello(s, sl.f.occhiello);
  s.addText(sl.f.titolo, { placeholder: 'title' });
  const fh = fonte(s, sl.f.fonte);
  const bottom = bottomOf(fh);
  const steps = sl.f.passi.split('\n').filter(Boolean).map((l) => l.split(' | '));
  const n = steps.length, gap = 0.15, w = (G.CW - gap * (n - 1)) / n;
  const y0 = G.BODY_Y + 0.1, d = 0.42, ly = y0 + d / 2;
  s.addShape('line', { x: G.X + w / 2, y: ly, w: G.CW - w, h: 0, line: { color: HEX.linea, width: 2 } });
  const sintH = sl.f.sintesi ? 0.55 : 0;
  const ch = bottom - sintH - (y0 + d + 0.15) - 0.05;
  const maxD = Math.max(...steps.map((st) => plain(st[2]).length));
  const dfs = n >= 5 ? (maxD > 110 ? 9.5 : 10.5) : (maxD > 140 ? 11 : 12);
  steps.forEach(([q, nome, desc], i) => {
    const x = G.X + i * (w + gap), last = i === n - 1;
    s.addText(String(i + 1), { shape: 'ellipse', x: x + w / 2 - d / 2, y: y0, w: d, h: d, fill: { color: last ? B.C.accent4 : B.C.text1 }, line: { color: B.C.background1, width: 2 }, color: B.C.background1, fontSize: 13, bold: true, align: 'center', valign: 'middle', margin: 0 });
    const cy = y0 + d + 0.15;
    card(s, { x, y: cy, w, h: ch });
    const isNum = /^\d{1,2}$/.test(q);
    let yy = cy + 0.15;
    if (!isNum) { label(s, q.toUpperCase(), x + 0.15, yy, w - 0.3, B.C.accent1); yy += 0.27; }
    const nm = nome.split(' · ');
    T(s, nm[0], { x: x + 0.15, y: yy, w: w - 0.3, h: 0.5, fontSize: n >= 5 ? 12.5 : 14, bold: true, color: B.C.text1, valign: 'top' });
    yy += plain(nm[0]).length * (n >= 5 ? 0.092 : 0.1) > w - 0.3 ? 0.48 : 0.28;
    if (nm[1]) { T(s, nm[1], { x: x + 0.15, y: yy, w: w - 0.3, h: 0.25, fontSize: 10.5, italic: true, color: B.C.accent1 }); yy += 0.3; }
    T(s, runs(desc), { x: x + 0.15, y: yy + 0.05, w: w - 0.3, h: cy + ch - yy - 0.15, fontSize: dfs, color: B.C.text2 });
  });
  if (sl.f.sintesi) sintesi(s, sl.f.sintesi, bottom - sintH + 0.03, 0.5);
  return s;
};

// IMMAGINE: testo a sinistra, immagine grande a destra (cliccabile se c'è un video), didascalia
R.IMMAGINE = async (pres, sl) => {
  const s = pres.addSlide({ masterName: 'BA Contenuto' });
  H(s, sl); occhiello(s, sl.f.occhiello);
  s.addText(sl.f.titolo, { placeholder: 'title' });
  const md = MEDIA[String(sl.n)] || {};
  const fh = fonte(s, sl.f.fonte);
  const bottom = bottomOf(fh);
  const y0 = G.BODY_Y + 0.05;
  const lw = 4.25, ix = G.X + lw + 0.3, iw = G.R - ix;
  // testo
  let yy = y0;
  if (sl.f.lettera) {
    s.addText(sl.f.lettera, { shape: 'roundRect', rectRadius: 0.05, x: G.X, y: yy, w: Math.max(1.4, plain(sl.f.lettera).length * 0.085 + 0.3), h: 0.3, fill: { color: B.C.accent4 }, line: { type: 'none' }, color: B.C.background1, fontSize: 10, bold: true, align: 'center', valign: 'middle', margin: 0 });
    yy += 0.42;
  }
  const extraH = sl.f.esempi ? 0.7 : 0;
  const nw = words(sl.f.corpo);
  T(s, paras(sl.f.corpo, { gap: 6 }), { x: G.X, y: yy, w: lw, h: bottom - yy - extraH, fontSize: nw > 75 ? 11.5 : nw > 60 ? 12 : 12.5, color: B.C.text2, lineSpacingMultiple: 1.05, objectName: 'corpo' });
  if (sl.f.esempi) {
    card(s, { x: G.X, y: bottom - extraH + 0.05, w: lw, h: extraH - 0.05, tint: true });
    T(s, runs(sl.f.esempi), { x: G.X + 0.15, y: bottom - extraH + 0.05, w: lw - 0.3, h: extraH - 0.05, fontSize: 10.5, color: B.C.text1, valign: 'middle' });
  }
  // immagine
  const capH = sl.f.didascalia ? 0.32 : 0;
  const vidH = (md.video || sl.f.video) ? 0.38 : 0;
  const ih = bottom - y0 - capH - vidH;
  if (md.file && fs.existsSync(path.join(MEDIA_DIR, md.file))) {
    const f = path.join(MEDIA_DIR, md.file);
    const meta = await require('sharp')(f).metadata();
    const r = meta.width / meta.height;
    let w = iw, h = iw / r;
    if (h > ih) { h = ih; w = ih * r; }
    const x = ix + (iw - w) / 2;
    const opt = { path: f, x, y: y0, w, h, objectName: 'immagine' };
    if (md.video) opt.hyperlink = { url: md.video, tooltip: 'Guarda il video' };
    s.addImage(opt);
    if (md.video && md.play !== false) {
      // pulsante "play" sopra l'immagine
      const pd = 0.7;
      s.addShape('ellipse', { x: x + w / 2 - pd / 2, y: y0 + h / 2 - pd / 2, w: pd, h: pd, fill: { color: '000000', transparency: 40 }, line: { color: 'FFFFFF', width: 2 }, hyperlink: { url: md.video } });
      s.addShape(pres.ShapeType.triangle, { x: x + w / 2 - 0.1, y: y0 + h / 2 - 0.16, w: 0.3, h: 0.32, fill: { color: 'FFFFFF' }, line: { type: 'none' }, rotate: 90, hyperlink: { url: md.video } });
    }
    if (md.schema) {
      // etichette di uno schema sovrapposto: agganci attorno al centro dell'immagine
      md.schema.forEach((t, i) => {
        const a = -Math.PI / 2 + (i * 2 * Math.PI) / md.schema.length;
        const bx = x + w / 2 + (w / 2 - 0.75) * Math.cos(a) - 0.65, by = y0 + h / 2 + (h / 2 - 0.3) * Math.sin(a) - 0.15;
        s.addText(t, { shape: 'roundRect', rectRadius: 0.06, x: bx, y: by, w: 1.3, h: 0.3, fill: { color: B.C.text1, transparency: 8 }, line: { color: B.C.background1, width: 1 }, color: B.C.background1, fontSize: 9.5, bold: true, align: 'center', valign: 'middle', margin: 0 });
      });
      s.addText(md.schema_centro || 'MODELLO', { shape: 'roundRect', rectRadius: 0.06, x: x + w / 2 - 0.6, y: y0 + h / 2 - 0.17, w: 1.2, h: 0.34, fill: { color: B.C.accent4 }, line: { color: B.C.background1, width: 1.5 }, color: B.C.background1, fontSize: 10.5, bold: true, align: 'center', valign: 'middle', margin: 0 });
    }
  } else {
    segnaposto(s, ix, y0, iw, ih, plain(sl.f.immagine || 'immagine').slice(0, 90));
  }
  let cy = y0 + ih + 0.05;
  if (md.video) {
    s.addText([{ text: '▶  Guarda il video', options: { hyperlink: { url: md.video, tooltip: md.video_titolo || 'Video' }, bold: true, color: B.C.accent4 } }, { text: md.video_titolo ? '   ' + md.video_titolo : '', options: { color: B.C.accent6 } }],
      { x: ix, y: cy, w: iw, h: 0.3, fontSize: 10.5, margin: 0, valign: 'middle', isTextBox: true, objectName: 'link-video' });
    cy += vidH;
  } else if (sl.f.video) {
    T(s, '[DA INSERIRE · link del video]', { x: ix, y: cy, w: iw, h: 0.3, fontSize: 9.5, bold: true, color: AVVISO, valign: 'middle' });
    cy += 0.32;
  }
  if (sl.f.didascalia) T(s, runs(sl.f.didascalia), { x: ix, y: cy, w: iw, h: 0.28, fontSize: 9, italic: true, color: B.C.accent6, valign: 'middle' });
  return s;
};

// NORMA: regola a sinistra; a destra caso reale (card scura) e scenario in fabbrica (card chiara)
R.NORMA = async (pres, sl) => {
  const s = pres.addSlide({ masterName: 'BA Contenuto' });
  H(s, sl); occhiello(s, sl.f.occhiello);
  s.addText(sl.f.titolo, { placeholder: 'title' });
  const bottom = bottomOf(fonte(s, sl.f.fonte));
  const y0 = G.BODY_Y + 0.05;
  const lw = 4.45, rx = 5.2, rw = G.R - rx;
  const nw = words(sl.f.corpo);
  T(s, paras(sl.f.corpo, { gap: 8 }), { x: G.X, y: y0, w: lw, h: bottom - y0, fontSize: nw > 95 ? 12 : nw > 75 ? 12.5 : nw > 55 ? 13 : 14, color: B.C.text2, lineSpacingMultiple: 1.08, objectName: 'corpo' });
  const tot = bottom - y0;
  const lc = plain(sl.f.caso || '').length, ls = plain(sl.f.scenario || '').length;
  const gap = 0.15;
  const hc = sl.f.caso ? (sl.f.scenario ? (tot - gap) * Math.max(0.38, Math.min(0.62, (lc + 60) / (lc + ls + 120))) : tot) : 0;
  const hs = sl.f.scenario ? (sl.f.caso ? tot - hc - gap : Math.min(tot, Math.max(1.6, 0.75 + Math.ceil(ls / 48) * 0.22))) : 0;
  if (sl.f.caso) {
    card(s, { x: rx, y: y0, w: rw, h: hc, dark: true });
    s.addImage({ data: await icon('LuNewspaper', HEX.tealChiaro), x: rx + 0.22, y: y0 + 0.16, w: 0.24, h: 0.24 });
    label(s, 'CASO REALE', rx + 0.55, y0 + 0.17, rw - 0.8, B.C.accent2);
    T(s, runs(sl.f.caso), { x: rx + 0.22, y: y0 + 0.5, w: rw - 0.42, h: hc - 0.6, fontSize: lc > 210 ? 10.5 : lc > 160 ? 11 : 11.5, color: B.C.background1, objectName: 'caso' });
  }
  if (sl.f.scenario) {
    const sy = y0 + (sl.f.caso ? hc + gap : 0);
    card(s, { x: rx, y: sy, w: rw, h: hs });
    s.addImage({ data: await icon('LuFactory', HEX.teal), x: rx + 0.22, y: sy + 0.16, w: 0.24, h: 0.24 });
    label(s, 'IN FABBRICA', rx + 0.55, sy + 0.17, rw - 0.8);
    T(s, runs(sl.f.scenario), { x: rx + 0.22, y: sy + 0.5, w: rw - 0.42, h: hs - 0.6, fontSize: ls > 210 ? 10.5 : ls > 160 ? 11 : 11.5, color: B.C.text2, objectName: 'scenario' });
  }
  return s;
};

// ---------------- Main ----------------
(async () => {
  const md = fs.readFileSync(SB, 'utf8');
  const vm = md.match(/RED TAG: variante (\w+)/); if (vm) rtVariante = vm[1];
  const slides = parse(md);
  await B.prepareAssets();
  const pres = B.newDeck({ title: CFG.titolo_deck || '', corso: CFG.corso });
  const vietata = new RegExp('\\b(' + VIETATE.join('|') + ')\\b');
  for (const sl of slides) {
    if (!R[sl.tipo]) throw new Error('Tipo non gestito: ' + sl.tipo + ' (slide ' + sl.n + ')');
    const s = await R[sl.tipo](pres, sl);
    note(s, sl);
    if (sl.cap && !fatti.includes(sl.cap)) fatti.push(sl.cap);
    // controllo: le parole vietate non devono comparire in slide né nelle note
    const visibili = Object.entries(sl.f).filter(([k]) => !['rif', 'visual', 'min'].includes(k)).map(([, v]) => v).join(' ');
    if (VIETATE.length && vietata.test(visibili)) throw new Error('Parola vietata nella slide ' + sl.n + ': ' + visibili.match(vietata)[0]);
  }
  await B.save(pres, OUT);
  console.log('ok', slides.length, 'slide');
})().catch((e) => { console.error(e); process.exit(1); });
