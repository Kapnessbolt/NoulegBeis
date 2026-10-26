// BlueAge deck library v3 — tema, layout e componenti per i deck BlueAge (corsi e presentazioni).
// Uso: const B = require('./blueage_lib'); const pres = B.newDeck({...}); ... await B.save(pres, 'out.pptx');
const pptxgen = require('pptxgenjs');
const React = require('react');
const ReactDOMServer = require('react-dom/server');
const sharp = require('sharp');
const lu = require('react-icons/lu');
const path = require('path');
const fs = require('fs');

const SKILL = process.env.PPTX_SKILL_DIR || '';
const ASSETS = process.env.BLUEAGE_ASSETS || [path.join(__dirname, 'assets'), path.join(__dirname, '..', 'assets')].find((d) => fs.existsSync(path.join(d, 'logo_blueage_chiaro.png'))) || path.join(__dirname, 'assets');

// ---------- Palette (hex) ----------
const HEX = {
  navy: '0B2C4D', notte: '050E2D', teal: '1C9EB1', tealChiaro: '7FD3DC', blu: '2F80ED', bluScuro: '4A90E2',
  testo: '3A4750', grigio: '6E7C87', grigioAzzurro: '8FA3B5', linea: 'D5DEE5',
  sfondo: 'FFFFFF', card: 'F2F5F8', cardForte: 'E6EEF3', tintaTeal: 'E3F4F6', bianco: 'FFFFFF',
  // Fuori palette, solo RED TAG
  vermiglio: 'E8452C', giallo: 'FFC629',
};
const FONT = 'Plus Jakarta Sans';

const THEME = {
  name: 'BlueAge',
  headFontFace: FONT,
  bodyFontFace: FONT,
  colors: {
    dk1: HEX.navy, lt1: HEX.bianco, dk2: HEX.testo, lt2: HEX.card,
    accent1: HEX.teal, accent2: HEX.tealChiaro, accent3: HEX.notte, accent4: HEX.blu,
    accent5: HEX.cardForte, accent6: HEX.grigio, hlink: HEX.blu, folHlink: HEX.grigio,
  },
};

// ---------- Griglia (pollici) ----------
const G = {
  W: 10, H: 5.625, X: 0.5, CW: 9, R: 9.5,
  HEAD_H: 0.4,          // banda di testa
  TIT_Y: 0.62,          // titolo
  BODY_Y: 1.35,         // inizio contenuto
  BODY_B: 5.0,          // fine contenuto
  FOOT_Y: 5.2,          // linea di piede
};
const LOGO_RATIO = 2316 / 516;
// Icone generate a runtime: cartella temporanea scrivibile (la skill installata può essere in sola lettura)
const GEN = path.join(require('os').tmpdir(), 'blueage-gen');

let C; // scheme colors

const logoFile = (v) => path.join(ASSETS, 'logo_blueage_' + v + '.png');

// Piede di pagina: linea sottile, numero, nome del corso, logotipo ufficiale
function footerObjs(dark, corso) {
  const lh = 0.17, lw = lh * LOGO_RATIO;
  return [
    { line: { x: G.X, y: G.FOOT_Y, w: G.CW, h: 0, line: { color: dark ? '1E3355' : HEX.linea, width: 0.75 } } },
    { text: { text: corso, options: { x: 0.95, y: G.FOOT_Y + 0.08, w: 6, h: 0.25, fontSize: 7.5, color: dark ? C.accent6 : C.accent6, margin: 0, valign: 'middle', fontFace: FONT } } },
    { image: { path: logoFile(dark ? 'scuro' : 'chiaro'), x: G.R - lw, y: G.FOOT_Y + 0.115, w: lw, h: lh } },
  ];
}
function slideNum(color) {
  return { x: G.X, y: G.FOOT_Y + 0.08, w: 0.4, h: 0.25, fontFace: FONT, fontSize: 8, bold: true, color, margin: 0, valign: 'middle' };
}

function defineLayouts(pres, corso) {
  const titleLight = { placeholder: { options: { name: 'title', type: 'title', align: 'left', x: G.X, y: G.TIT_Y, w: G.CW, h: 0.6, fontSize: 26, bold: true, color: C.text1, margin: 0, valign: 'middle', fontFace: FONT }, text: '' } };
  const headBand = { rect: { x: 0, y: 0, w: G.W, h: G.HEAD_H, fill: { color: HEX.navy }, line: { type: 'none' } } };

  // Contenuto: testa navy, piede con linea e logo
  pres.defineSlideMaster({
    title: 'BA Contenuto', background: { color: HEX.sfondo },
    objects: [headBand, titleLight, ...footerObjs(false, corso)],
    slideNumber: slideNum(C.text1),
  });

  // Tocca a voi: pannello teal a sinistra, domande a destra
  const tw = 2.9;
  pres.defineSlideMaster({
    title: 'BA Tocca a voi', background: { color: HEX.sfondo },
    objects: [
      headBand,
      { rect: { x: 0, y: G.HEAD_H, w: tw, h: G.FOOT_Y - G.HEAD_H - 0.12, fill: { color: HEX.teal }, line: { type: 'none' } } },
      { image: { path: path.join(GEN, 'icona_conversazione.png'), x: G.X, y: 0.95, w: 0.62, h: 0.62 } },
      { text: { text: 'TOCCA A VOI', options: { x: G.X, y: 1.8, w: tw - 0.8, h: 0.3, fontSize: 11, bold: true, charSpacing: 3, color: C.background1, margin: 0, fontFace: FONT } } },
      { placeholder: { options: { name: 'invito', type: 'body', x: G.X, y: 2.15, w: tw - 0.8, h: 1.6, fontSize: 17, bold: true, color: C.background1, margin: 0, valign: 'top', fontFace: FONT }, text: '' } },
      { placeholder: { options: { name: 'title', type: 'title', align: 'left', x: tw + 0.45, y: G.TIT_Y, w: G.R - tw - 0.45, h: 0.6, fontSize: 22, bold: true, color: C.text1, margin: 0, valign: 'middle', fontFace: FONT }, text: '' } },
      ...footerObjs(false, corso),
    ],
    slideNumber: slideNum(C.text1),
  });

  // Copertina
  pres.defineSlideMaster({
    title: 'BA Copertina', background: { color: HEX.notte },
    objects: [
      { image: { path: logoFile('scuro'), x: G.X, y: 0.55, w: 0.3 * LOGO_RATIO, h: 0.3 } },
      { placeholder: { options: { name: 'occhiello', type: 'body', x: G.X, y: 1.45, w: 7, h: 0.3, fontSize: 10, bold: true, color: C.accent2, charSpacing: 3, margin: 0, fontFace: FONT }, text: '' } },
      { placeholder: { options: { name: 'title', type: 'title', align: 'left', x: G.X, y: 1.8, w: 7.2, h: 1.55, fontSize: 36, bold: true, color: C.background1, margin: 0, valign: 'top', fontFace: FONT }, text: '' } },
      { placeholder: { options: { name: 'sottotitolo', type: 'body', x: G.X, y: 3.45, w: 7, h: 0.4, fontSize: 14, color: C.accent2, margin: 0, fontFace: FONT }, text: '' } },
      { line: { x: G.X, y: 4.62, w: 0.6, h: 0, line: { color: HEX.blu, width: 2 } } },
      { placeholder: { options: { name: 'docenti', type: 'body', x: G.X, y: 4.75, w: 7, h: 0.3, fontSize: 10, color: C.background1, margin: 0, fontFace: FONT }, text: '' } },
      { text: { text: 'ADVISORY  ·  EXECUTION  ·  DATA  ·  TECHNOLOGY', options: { x: G.X, y: 5.07, w: 7, h: 0.25, fontSize: 7.5, color: C.accent6, charSpacing: 2, margin: 0, fontFace: FONT } } },
    ],
  });

  // Sezione (scura, con indice dei capitoli a destra)
  pres.defineSlideMaster({
    title: 'BA Sezione', background: { color: HEX.notte },
    objects: [
      { placeholder: { options: { name: 'numero', type: 'body', x: G.X, y: 0.85, w: 3, h: 1.3, fontSize: 88, bold: true, color: C.accent4, margin: 0, valign: 'bottom', fontFace: FONT }, text: '' } },
      { placeholder: { options: { name: 'title', type: 'title', align: 'left', x: G.X, y: 2.35, w: 5.2, h: 1.3, fontSize: 28, bold: true, color: C.background1, margin: 0, valign: 'top', fontFace: FONT }, text: '' } },
      { placeholder: { options: { name: 'sottotitolo', type: 'body', x: G.X, y: 3.7, w: 5.2, h: 0.9, fontSize: 12.5, color: C.accent2, margin: 0, valign: 'top', fontFace: FONT }, text: '' } },
      { line: { x: 6.25, y: 0.8, w: 0, h: 4.0, line: { color: '1E3355', width: 0.75 } } },
      ...footerObjs(true, corso),
    ],
    slideNumber: slideNum(C.accent2),
  });

  // Scura (pausa, chiusura)
  pres.defineSlideMaster({
    title: 'BA Scura', background: { color: HEX.notte },
    objects: [
      { placeholder: { options: { name: 'title', type: 'title', align: 'left', x: G.X, y: 0.75, w: G.CW, h: 0.65, fontSize: 28, bold: true, color: C.background1, margin: 0, valign: 'middle', fontFace: FONT }, text: '' } },
      ...footerObjs(true, corso),
    ],
    slideNumber: slideNum(C.accent2),
  });

  // RED TAG: fuori palette, senza testa né piede (rompe la cornice)
  for (const [nome, bg, fg, accent] of [['vermiglio', HEX.vermiglio, 'FFFFFF', '2A0A05'], ['giallo', HEX.giallo, HEX.notte, HEX.notte]]) {
    pres.defineSlideMaster({
      title: 'BA RED TAG ' + nome, background: { color: bg },
      objects: [
        { placeholder: { options: { name: 'etichetta', type: 'body', x: 0.95, y: 0.7, w: 5, h: 0.3, fontSize: 10, bold: true, color: accent, charSpacing: 3, margin: 0, valign: 'middle', fontFace: FONT }, text: '' } },
        { placeholder: { options: { name: 'frase', type: 'body', x: 0.6, y: 1.75, w: 8.9, h: 3.1, fontSize: 42, bold: true, color: fg, margin: 0, valign: 'bottom', fontFace: FONT, lineSpacingMultiple: 0.98 }, text: '' } },
      ],
      slideNumber: { x: 9.0, y: 5.15, w: 0.5, h: 0.25, fontFace: FONT, fontSize: 8, bold: true, color: fg, margin: 0, align: 'right' },
    });
  }
}

function newDeck(meta = {}) {
  const pres = new pptxgen();
  pres.layout = 'LAYOUT_16x9';
  pres.author = meta.author || 'BlueAge';
  pres.title = meta.title || '';
  pres.theme = { headFontFace: FONT, bodyFontFace: FONT };
  C = pres.SchemeColor;
  defineLayouts(pres, meta.corso || 'BlueAge');
  return pres;
}

// ---------- Icone (Lucide, stile lineare come il PDF COMPASS) ----------
const iconCache = {};
async function iconBuf(name, hex, px = 256, stroke = 1.75) {
  const Comp = lu[name];
  if (!Comp) throw new Error('Icona non trovata: ' + name);
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: '#' + hex, size: px, strokeWidth: stroke }));
  return sharp(Buffer.from(svg)).png().toBuffer();
}
async function icon(name, hex, px = 256) {
  const key = name + hex;
  if (!iconCache[key]) iconCache[key] = 'image/png;base64,' + (await iconBuf(name, hex, px)).toString('base64');
  return iconCache[key];
}
async function prepareAssets() {
  fs.mkdirSync(GEN, { recursive: true });
  fs.writeFileSync(path.join(GEN, 'icona_conversazione.png'), await iconBuf('LuMessagesSquare', HEX.bianco, 256, 1.5));
}

// ---------- Componenti ----------
// Testa: breadcrumb a sinistra, tracker dei capitoli a destra (capitolo corrente evidenziato)
function header(slide, { modulo, titoloModulo, capitoli = [], corrente = null, fatti = null }) {
  // fatti: elenco dei capitoli già svolti (serve quando l'ordine di proiezione non è numerico)
  const cap = corrente ? capitoli[corrente - 1] : null;
  const runs = [
    { text: modulo + '  ·  ' + titoloModulo.toUpperCase(), options: { color: C.background1, bold: true } },
  ];
  if (cap) runs.push({ text: '   /   ' + String(corrente).padStart(2, '0') + '  ' + cap.toUpperCase(), options: { color: C.accent2, bold: true } });
  slide.addText(runs, { x: G.X, y: 0, w: 6.3, h: G.HEAD_H, fontSize: 7.5, charSpacing: 1.2, margin: 0, valign: 'middle', isTextBox: true, objectName: 'testa-percorso' });
  const n = capitoli.length, step = 0.27, x0 = G.R - n * step + 0.02;
  capitoli.forEach((_, i) => {
    const on = i + 1 === corrente;
    const o = { x: x0 + i * step, y: 0.095, w: 0.23, h: 0.21, fontSize: 7, bold: true, align: 'center', valign: 'middle', margin: 0, objectName: 'tracker-' + (i + 1),
      color: on ? C.background1 : ((fatti ? fatti.includes(i + 1) : (corrente && i + 1 < corrente)) ? C.accent2 : '5B7088') };
    if (on) Object.assign(o, { shape: 'roundRect', rectRadius: 0.04, fill: { color: C.accent4 }, line: { type: 'none' } });
    else o.isTextBox = true;
    slide.addText(String(i + 1).padStart(2, '0'), o);
  });
}

function card(slide, { x, y, w, h, dark = false, tint = false, name }) {
  slide.addShape('rect', { x, y, w, h, fill: { color: dark ? C.text1 : tint ? HEX.tintaTeal : C.background2 }, line: { type: 'none' }, objectName: name || 'card' });
}

// Icona in cerchio tinto (motivo ricorrente)
async function iconDot(slide, name, x, y, d = 0.46, { dark = false } = {}) {
  slide.addShape('ellipse', { x, y, w: d, h: d, fill: { color: dark ? '1C3A63' : HEX.tintaTeal }, line: { type: 'none' } });
  const p = d * 0.24;
  slide.addImage({ data: await icon(name, dark ? HEX.tealChiaro : HEX.teal), x: x + p, y: y + p, w: d - 2 * p, h: d - 2 * p });
}

// Motivo bussola: anelli concentrici con le sette posizioni COMPASS (copertina)
function compassRings(slide, cx = 9.45, cy = 2.95) {
  [[2.9, '12284A', 1], [2.15, '1C3A63', 1.5], [1.4, '12284A', 1]].forEach(([r, col, wd]) =>
    slide.addShape('ellipse', { x: cx - r, y: cy - r, w: 2 * r, h: 2 * r, fill: { type: 'none' }, line: { color: col, width: wd }, objectName: 'anello' }));
  for (let i = 0; i < 7; i++) {
    const a = -Math.PI / 2 + i * 2 * Math.PI / 7, r = 2.15, d = i === 0 ? 0.16 : 0.1;
    slide.addShape('ellipse', { x: cx + r * Math.cos(a) - d / 2, y: cy + r * Math.sin(a) - d / 2, w: d, h: d, fill: { color: i === 0 ? HEX.blu : '2A4B78' }, line: { type: 'none' }, objectName: 'punto-bussola' });
  }
}

// Etichetta piccola maiuscola
function label(slide, txt, x, y, w, color) {
  slide.addText(txt, { x, y, w, h: 0.22, fontSize: 8.5, bold: true, charSpacing: 2, color: color || C.accent1, margin: 0, valign: 'middle', isTextBox: true });
}

// Fonte in basso, sopra la linea di piede
function fonte(slide, txt) {
  slide.addText(txt, { x: G.X, y: G.FOOT_Y - 0.27, w: G.CW, h: 0.22, fontSize: 8, color: C.accent6, margin: 0, valign: 'bottom', isTextBox: true, objectName: 'fonte' });
}

// Etichetta di revisione (solo deck campione), nel piede al centro
function tag(slide, txt, dark) {
  slide.addText(txt, { x: 3.5, y: G.FOOT_Y + 0.08, w: 3, h: 0.25, fontSize: 7, color: dark ? C.accent2 : 'B04A2E', align: 'center', valign: 'middle', margin: 0, charSpacing: 1, isTextBox: true, objectName: 'tag-campione' });
}

async function save(pres, file) {
  await pres.writeFile({ fileName: file });
  const { applyTheme } = require(path.join(SKILL, 'scripts/apply_theme.js'));
  await applyTheme(file, THEME);
}

module.exports = { HEX, FONT, THEME, G, newDeck, prepareAssets, icon, iconDot, header, compassRings, card, label, fonte, tag, save, get C() { return C; } };
