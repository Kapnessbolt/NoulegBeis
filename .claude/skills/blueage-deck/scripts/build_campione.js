// Deck campione v02: una slide per tipo, contenuti da indice del corso e PDF COMPASS.
const B = require('./blueage_lib');
const { G, HEX, icon, iconDot, header, card, label, fonte, tag, compassRings } = B;

const M1 = {
  modulo: 'M1',
  titoloModulo: 'L\'AI nei contesti industriali',
  capitoli: ['COMPASS', 'Applicazioni per funzione', 'Stato dell\'arte', 'Normativa e regole', 'Fondamenti dell\'AI', 'Orientarsi negli strumenti', 'Dal prompt al contesto', 'Tre modalità d\'impiego', 'Strumenti, modelli e costi', 'Dalla prova al processo'],
};
const H = (s, cap) => header(s, Object.assign({ corrente: cap }, M1));

(async () => {
  await B.prepareAssets();
  const pres = B.newDeck({ title: 'Deck campione v02 · AI & Data-Driven Management' });
  const C = B.C;
  const T = (s, txt, o) => s.addText(txt, Object.assign({ isTextBox: true, margin: 0, valign: 'top' }, o));
  const bullets = (arr, o = {}) => arr.map((t, k) => ({ text: t, options: Object.assign({ bullet: { indent: 13 }, breakLine: k < arr.length - 1, paraSpaceAfter: o.gap || 5 }, o) }));

  // 1 · COPERTINA
  let s = pres.addSlide({ masterName: 'BA Copertina' });
  compassRings(s);
  s.addText('MECCANOTECNICA UMBRA  ·  AI & DATA-DRIVEN MANAGEMENT', { placeholder: 'occhiello' });
  s.addText('L\'intelligenza artificiale nei contesti industriali', { placeholder: 'title' });
  s.addText('Modulo 1  ·  Sessione 1  ·  Giovedì 15 ottobre 2026', { placeholder: 'sottotitolo' });
  s.addText('Leonardo Pinsone  ·  Lorenzo Curione', { placeholder: 'docenti' });
  s.addNotes('Tipo COPERTINA. Presentazione dei docenti, obiettivo del modulo in una frase.');

  // 2 · AGENDA
  s = pres.addSlide({ masterName: 'BA Contenuto' });
  H(s, null); tag(s, 'CAMPIONE · AGENDA');
  s.addText('Tre sessioni, otto ore, un dossier che cresce', { placeholder: 'title' });
  const sess = [
    ['1', '15/10', '4 ore · presenza', 'Fondamenti e prima pratica', ['COMPASS e prime domande sui processi', 'Applicazioni e stato dell\'arte', 'Normativa e regole d\'ingaggio', 'Fondamenti dell\'AI', 'Prompt, contesto e laboratorio']],
    ['2', '22/10', '2 ore · distanza', 'Modalità, strumenti e costi', ['Ripresa della sfida 1', 'Predittiva, generativa, agentica', 'Demo di un agente', 'Strumenti, modelli e costi', 'Laboratorio su contesto e verifica']],
    ['3', 'X1 · da fissare', '2 ore · presenza', 'Dalla prova al processo', ['Ripresa della sfida 2', 'Dalla prova al processo operativo', 'Pre-mortem', 'Lettura complessiva dell\'azienda', 'Scelta del processo filo rosso']],
  ];
  sess.forEach((c, i) => {
    const x = G.X + i * 3.05, w = 2.85, y = G.BODY_Y + 0.05;
    card(s, { x, y, w, h: 3.2 });
    s.addText(c[0], { shape: 'ellipse', x: x + 0.22, y: y + 0.22, w: 0.42, h: 0.42, fill: { color: i === 0 ? C.accent4 : C.text1 }, line: { type: 'none' }, color: C.background1, fontSize: 14, bold: true, align: 'center', valign: 'middle', margin: 0 });
    T(s, c[1], { x: x + 0.78, y: y + 0.2, w: w - 0.9, h: 0.25, fontSize: 12, bold: true, color: C.text1 });
    T(s, c[2], { x: x + 0.78, y: y + 0.44, w: w - 0.9, h: 0.22, fontSize: 9.5, color: C.accent6 });
    T(s, c[3], { x: x + 0.22, y: y + 0.88, w: w - 0.4, h: 0.3, fontSize: 13, bold: true, color: C.accent1 });
    T(s, bullets(c[4]), { x: x + 0.22, y: y + 1.28, w: w - 0.35, h: 1.8, fontSize: 11, color: C.text2 });
  });
  T(s, 'Ogni sessione aggiunge un pezzo al dossier di ciascun dirigente.', { x: G.X, y: 4.72, w: G.CW, h: 0.3, fontSize: 12.5, bold: true, color: C.text1 });
  s.addNotes('Tipo AGENDA. La data di X1 è da confermare il 15/10.');

  // 3 · COMPASS
  s = pres.addSlide({ masterName: 'BA Contenuto' });
  H(s, 1); tag(s, 'CAMPIONE · COMPASS');
  s.addText('Sette modi di usare l\'AI, ognuno con un verbo', { placeholder: 'title' });
  const cx = 1.85, cy = 3.05, R = 1.08, d = 0.42;
  s.addShape('ellipse', { x: cx - R, y: cy - R, w: 2 * R, h: 2 * R, fill: { color: C.background2 }, line: { color: C.text1, width: 1.25 }, objectName: 'bussola' });
  s.addShape('ellipse', { x: cx - R * 0.7, y: cy - R * 0.7, w: 2 * R * 0.7, h: 2 * R * 0.7, fill: { type: 'none' }, line: { color: HEX.linea, width: 1 } });
  s.addShape(pres.ShapeType.triangle, { x: cx - 0.1, y: cy - 0.68, w: 0.2, h: 0.68, fill: { color: C.accent4 }, line: { type: 'none' }, objectName: 'ago-nord' });
  s.addShape(pres.ShapeType.triangle, { x: cx - 0.1, y: cy, w: 0.2, h: 0.55, fill: { color: C.text1 }, line: { type: 'none' }, rotate: 180, objectName: 'ago-sud' });
  s.addShape('ellipse', { x: cx - 0.045, y: cy - 0.045, w: 0.09, h: 0.09, fill: { color: C.background1 }, line: { color: C.text1, width: 0.75 } });
  const hl = [5, 6];
  ['C', 'O', 'M', 'P', 'A', 'S', 'S'].forEach((L, i) => {
    const a = -Math.PI / 2 + i * 2 * Math.PI / 7, on = hl.includes(i);
    s.addText(L, { shape: 'ellipse', x: cx + R * Math.cos(a) - d / 2, y: cy + R * Math.sin(a) - d / 2, w: d, h: d, fill: { color: on ? C.accent4 : C.text1 }, line: { color: C.background1, width: 2 }, color: C.background1, fontSize: 12, bold: true, align: 'center', valign: 'middle', margin: 0 });
  });
  T(s, 'La bussola orienta.\nLa direzione la sceglie chi guida.', { x: 0.5, y: 4.33, w: 2.7, h: 0.5, fontSize: 10, italic: true, color: C.text2, align: 'center' });
  const modi = [
    ['C', 'Codify', 'Mettere a sistema', 'Trasforma l\'esperienza delle persone in conoscenza consultabile.'],
    ['O', 'Orchestrate', 'Automatizzare', 'Toglie le operazioni ripetitive: flussi, integrazioni e AI lavorano insieme.'],
    ['M', 'Monitor', 'Sorvegliare', 'Segnala ciò che esce dalla norma, anche quando ogni valore da solo è nei limiti.'],
    ['P', 'Predict', 'Prevedere', 'Dallo storico stima cosa succederà prima che succeda.'],
    ['A', 'Analyze', 'Analizzare e interpretare', 'Trova le relazioni nei dati. L\'interpretazione resta a chi ha l\'esperienza.'],
    ['S', 'Synthesize', 'Leggere e sintetizzare', 'Legge in un minuto quello che richiede un pomeriggio.'],
    ['S', 'Spar', 'Ragionare in coppia', 'Sparring partner: allarga le ipotesi, aiuta a scegliere, fa le domande giuste.'],
  ];
  const lx0 = 3.7, rh = 0.4;
  modi.forEach((m, i) => {
    const y = G.BODY_Y + 0.02 + i * rh, on = hl.includes(i);
    s.addText(m[0], { shape: 'ellipse', x: lx0, y: y + 0.04, w: 0.28, h: 0.28, fill: { color: on ? C.accent4 : C.text1 }, line: { type: 'none' }, color: C.background1, fontSize: 9.5, bold: true, align: 'center', valign: 'middle', margin: 0 });
    T(s, [
      { text: m[1], options: { bold: true, color: C.text1, fontSize: 11 } },
      { text: '  ' + m[2], options: { color: C.accent1, fontSize: 10.5, bold: true, breakLine: true } },
      { text: m[3], options: { color: C.text2, fontSize: 10.5 } },
    ], { x: lx0 + 0.4, y, w: 5.4, h: rh, lineSpacingMultiple: 0.95 });
  });
  s.addShape('rect', { x: lx0, y: 4.25, w: 5.8, h: 0.5, fill: { color: C.text1 }, line: { type: 'none' } });
  s.addImage({ data: await icon('LuDatabase', HEX.tealChiaro), x: lx0 + 0.14, y: 4.36, w: 0.28, h: 0.28 });
  T(s, [{ text: 'DATA  ', options: { bold: true, fontSize: 12, color: C.background1 } }, { text: 'La base di tutto: dati completi, coerenti, collegati e sufficienti.', options: { fontSize: 10.5, color: C.background1 } }],
    { x: lx0 + 0.55, y: 4.25, w: 5.15, h: 0.5, valign: 'middle' });
  fonte(s, 'Fonte: COMPASS · l\'AI al lavoro, BlueAge');
  s.addNotes('Tipo COMPASS. In M1 si presenta la bussola completa; evidenziate le lettere provate subito (Synthesize, Spar). Negli altri moduli si evidenziano le lettere del modulo.');

  // 4 · SEZIONE
  s = pres.addSlide({ masterName: 'BA Sezione' });
  tag(s, 'CAMPIONE · SEZIONE', true);
  s.addText('02', { placeholder: 'numero' });
  s.addText('Dove può essere utile l\'AI: applicazioni per funzione', { placeholder: 'title' });
  s.addText('Produzione e qualità · Area tecnica · Amministrazione e finanza · Commerciale · Direzione e business unit', { placeholder: 'sottotitolo' });
  M1.capitoli.forEach((c, i) => {
    const y = 0.8 + i * 0.4, on = i === 1, done = i < 1;
    if (on) s.addShape('ellipse', { x: 6.52, y: y + 0.12, w: 0.1, h: 0.1, fill: { color: C.accent4 }, line: { type: 'none' } });
    T(s, [{ text: String(i + 1).padStart(2, '0') + '   ', options: { bold: true, color: on ? C.accent4 : '5B7088' } }, { text: c, options: { bold: on, color: on ? C.background1 : done ? C.accent2 : '8FA3B5' } }],
      { x: 6.75, y, w: 2.75, h: 0.34, fontSize: 10.5, valign: 'middle' });
  });
  s.addNotes('Tipo SEZIONE. Apre un capitolo; a destra la posizione nel modulo.');

  // 5-6 · RED TAG, due varianti fuori palette
  for (const v of ['vermiglio', 'giallo']) {
    s = pres.addSlide({ masterName: 'BA RED TAG ' + v });
    const dark = v === 'vermiglio';
    s.addImage({ data: await icon('LuTag', dark ? '2A0A05' : HEX.notte), x: 0.6, y: 0.7, w: 0.28, h: 0.28 });
    s.addText('RED TAG  ·  02', { placeholder: 'etichetta' });
    s.addText([
      { text: 'Non partire dall\'AI.', options: { breakLine: true, color: dark ? 'FFFFFF' : '7A5A00' } },
      { text: 'Parti da ciò che non funziona.', options: { color: dark ? '2A0A05' : HEX.notte } },
    ], { placeholder: 'frase' });
    s.addText('CAMPIONE · RED TAG · ' + v.toUpperCase(), { x: 3.5, y: 5.2, w: 3, h: 0.25, fontSize: 7, color: dark ? 'FFFFFF' : HEX.notte, align: 'center', margin: 0, isTextBox: true });
    s.addNotes('Tipo RED TAG, variante ' + v + '. RT-M1-02. Nucleo: problemi prima delle soluzioni. Pausa di qualche secondo.');
  }

  // 7 · TOCCA A VOI
  s = pres.addSlide({ masterName: 'BA Tocca a voi' });
  H(s, 1); tag(s, 'CAMPIONE · TOCCA A VOI');
  s.addText('Raccontateci come funziona da voi.', { placeholder: 'invito' });
  s.addText('Come lavorano oggi i vostri processi', { placeholder: 'title' });
  const qx = 3.35, qw = G.R - qx;
  const qs = ['Quali processi attraversano la tua area?', 'Dove il lavoro si ferma in attesa di informazioni o decisioni?', 'Quali attività vengono ripetute, ricopiate o ricostruite?', 'Dove ricorrono errori, rilavorazioni o eccezioni?', 'Quale esempio concreto descrive meglio il problema?'];
  qs.forEach((q, i) => {
    const y = G.BODY_Y + 0.02 + i * 0.5;
    T(s, String(i + 1).padStart(2, '0'), { x: qx, y, w: 0.45, h: 0.42, fontSize: 13, bold: true, color: C.accent1, valign: 'middle' });
    T(s, q, { x: qx + 0.5, y, w: qw - 0.5, h: 0.42, fontSize: 13.5, color: C.text1, valign: 'middle' });
    if (i < qs.length - 1) s.addShape('line', { x: qx + 0.5, y: y + 0.46, w: qw - 0.5, h: 0, line: { color: HEX.linea, width: 0.5 } });
  });
  card(s, { x: qx, y: 4.0, w: qw, h: 0.82, tint: true });
  s.addImage({ data: await icon('LuLightbulb', HEX.teal), x: qx + 0.18, y: 4.23, w: 0.34, h: 0.34 });
  T(s, 'Un esempio concreto vale più di un\'opinione: che cosa è successo, quanto spesso, con quali conseguenze. Parliamo di processi, non di persone.',
    { x: qx + 0.65, y: 4.0, w: qw - 0.8, h: 0.82, fontSize: 11.5, color: C.text1, valign: 'middle' });
  s.addNotes('Tipo TOCCA A VOI. Chiedere un esempio concreto per ogni risposta. Annotare: processo, problema, esempio, conseguenze, come si gestisce oggi.');

  // 8 · CONTENUTO (dispensa)
  s = pres.addSlide({ masterName: 'BA Contenuto' });
  H(s, 1); tag(s, 'CAMPIONE · CONTENUTO');
  s.addText('S · Synthesize: leggere e sintetizzare', { placeholder: 'title' });
  await iconDot(s, 'LuScanText', G.X, G.BODY_Y + 0.1, 0.6);
  T(s, [{ text: 'Legge in un minuto quello che richiede un pomeriggio. ', options: { bold: true, color: C.text1 } }, { text: 'L\'AI legge documenti lunghi ed estrae quello che serve: requisiti, scadenze, temi che ritornano. Il risultato è un punto di partenza, non un documento finale.' }],
    { x: G.X, y: 2.15, w: 4.2, h: 1.45, fontSize: 14, color: C.text2, lineSpacingMultiple: 1.12 });
  T(s, 'In questo modulo lo si prova subito sul proprio lavoro, con materiali consentiti.',
    { x: G.X, y: 3.65, w: 4.2, h: 0.6, fontSize: 12.5, bold: true, color: C.text1 });
  card(s, { x: 5.1, y: G.BODY_Y + 0.1, w: 4.4, h: 2.0 });
  label(s, 'ESEMPI', 5.35, G.BODY_Y + 0.28, 3.9);
  T(s, bullets(['Un capitolato di 80 pagine: requisiti e differenze dallo standard', 'Un contratto fornitore: penali, scadenze, rinnovi', 'Un anno di reclami: i temi che ritornano']), { x: 5.35, y: G.BODY_Y + 0.6, w: 3.95, h: 1.4, fontSize: 12, color: C.text2 });
  card(s, { x: 5.1, y: 3.6, w: 4.4, h: 0.95, dark: true });
  label(s, 'ATTENZIONE', 5.35, 3.73, 3.9, C.accent2);
  T(s, 'Numeri e clausole si verificano sull\'originale.', { x: 5.35, y: 4.0, w: 3.95, h: 0.4, fontSize: 13, bold: true, color: C.background1 });
  fonte(s, 'Fonte: COMPASS · l\'AI al lavoro, BlueAge');
  s.addNotes('Tipo CONTENUTO, densità da dispensa.');

  // 9 · QUATTRO CARD
  s = pres.addSlide({ masterName: 'BA Contenuto' });
  H(s, 5); tag(s, 'CAMPIONE · QUATTRO CARD');
  s.addText('Quattro controlli prima di dare i dati all\'AI', { placeholder: 'title' });
  const ctl = [['LuListChecks', 'Completi', 'I campi che servono ci sono.'], ['LuScale', 'Coerenti', 'Stesse unità, codici, definizioni.'], ['LuLink', 'Collegati', 'Ogni evento risale alla sua origine: lotto, cliente, ordine.'], ['LuLayers', 'Sufficienti', 'Abbastanza casi per imparare qualcosa.']];
  for (let i = 0; i < 4; i++) {
    const x = G.X + (i % 2) * 4.6, y = G.BODY_Y + 0.05 + Math.floor(i / 2) * 1.38, w = 4.4, h = 1.22;
    card(s, { x, y, w, h });
    await iconDot(s, ctl[i][0], x + 0.25, y + 0.25, 0.5);
    T(s, ctl[i][1], { x: x + 0.95, y: y + 0.22, w: 3.2, h: 0.32, fontSize: 15, bold: true, color: C.text1, valign: 'middle' });
    T(s, ctl[i][2], { x: x + 0.95, y: y + 0.58, w: 3.25, h: 0.55, fontSize: 12, color: C.text2 });
  }
  T(s, 'Dati sporchi producono risposte sporche, dette con la stessa sicurezza di quelle giuste.', { x: G.X, y: 4.2, w: G.CW, h: 0.4, fontSize: 13, bold: true, color: C.accent1, valign: 'middle' });
  fonte(s, 'Fonte: COMPASS · l\'AI al lavoro, BlueAge');
  s.addNotes('Tipo QUATTRO CARD. In M2 questa griglia diventa lo strumento di diagnosi.');

  // 10 · AFFERMAZIONE + DOMANDA
  s = pres.addSlide({ masterName: 'BA Contenuto' });
  H(s, 4); tag(s, 'CAMPIONE · AFFERMAZIONE + DOMANDA');
  s.addText('Guardrail sempre validi', { placeholder: 'title' });
  T(s, '2', { x: G.X, y: 1.3, w: 1.0, h: 1.1, fontSize: 66, bold: true, color: C.accent4 });
  T(s, 'L\'AI propone, la persona decide e firma.', { x: 1.6, y: 1.45, w: 7.9, h: 0.6, fontSize: 22, bold: true, color: C.text1, valign: 'middle' });
  T(s, 'La responsabilità di un risultato resta a chi lo usa. Per questo ogni prova del corso registra anche come è stato verificato il risultato, non solo che cosa ha prodotto l\'AI.',
    { x: 1.6, y: 2.2, w: 7.6, h: 1.0, fontSize: 14, color: C.text2, lineSpacingMultiple: 1.1 });
  card(s, { x: 1.6, y: 3.5, w: 7.9, h: 0.95, tint: true });
  s.addImage({ data: await icon('LuMessageCircleQuestion', HEX.teal), x: 1.8, y: 3.8, w: 0.34, h: 0.34 });
  T(s, 'Nella tua area, chi firmerebbe oggi un documento preparato con l\'AI? Con quale controllo?', { x: 2.3, y: 3.5, w: 7.0, h: 0.95, fontSize: 14, italic: true, color: C.text1, valign: 'middle' });
  s.addNotes('Tipo AFFERMAZIONE + DOMANDA. Domanda di esempio, non ancora validata.');

  // 11 · TABELLA
  s = pres.addSlide({ masterName: 'BA Contenuto' });
  H(s, 10); tag(s, 'CAMPIONE · TABELLA');
  s.addText('Si parte dal problema, poi si sceglie il modo', { placeholder: 'title' });
  const hdr = (t) => ({ text: t, options: { bold: true, color: C.background1, fontSize: 8.5, charSpacing: 1.5, fill: { color: C.text1 } } });
  const rows = [
    ['Tutto sta in testa a poche persone', 'C · Codify', 'M4'], ['Ricopiamo a mano', 'O · Orchestrate', 'M4'], ['Ce ne accorgiamo tardi', 'M · Monitor', 'M3'],
    ['Vogliamo saperlo prima', 'P · Predict', 'M3'], ['Non sappiamo perché succede', 'A · Analyze + S · Spar', 'M3, M5'], ['Troppi documenti da leggere', 'S · Synthesize', 'M1'], ['Dobbiamo preparare o decidere', 'S · Spar', 'M1, M5'],
  ];
  const tb = [[hdr('IL PROBLEMA'), hdr('LA LETTERA'), hdr('DOVE SI APPROFONDISCE')]].concat(rows.map((r, k) => {
    const f = { color: k % 2 ? C.background1 : C.background2 };
    return [{ text: r[0], options: { color: C.text2, fill: f } }, { text: r[1], options: { bold: true, color: C.text1, fill: f } }, { text: r[2], options: { color: C.text2, fill: f } }];
  }));
  s.addTable(tb, { x: G.X, y: G.BODY_Y + 0.05, w: G.CW, colW: [4.0, 2.6, 2.4], rowH: 0.37, fontSize: 12, fontFace: B.FONT, valign: 'middle', margin: [0.03, 0.12, 0.03, 0.12], border: { type: 'none' } });
  fonte(s, 'Fonte: COMPASS · l\'AI al lavoro, BlueAge. Colonna "dove si approfondisce" dall\'indice del corso.');
  s.addNotes('Tipo TABELLA. Serve anche alla scelta del filo rosso (sessione X1).');

  // 12 · DUE CARD
  s = pres.addSlide({ masterName: 'BA Contenuto' });
  H(s, 7); tag(s, 'CAMPIONE · DUE CARD');
  s.addText('La stessa richiesta, scritta in due modi', { placeholder: 'title' });
  const cy2 = G.BODY_Y + 0.05, ch = 2.95;
  card(s, { x: G.X, y: cy2, w: 3.6, h: ch });
  label(s, 'RICHIESTA VAGA', 0.75, cy2 + 0.22, 3);
  T(s, '«Riassumimi questo capitolato.»', { x: 0.75, y: cy2 + 0.55, w: 3.1, h: 0.45, fontSize: 15, italic: true, color: C.text1 });
  T(s, 'Il modello deve indovinare che cosa serve, a chi e in quale forma. Il risultato sembra completo, ma è difficile da verificare.', { x: 0.75, y: cy2 + 1.2, w: 3.1, h: 1.5, fontSize: 12, color: C.text2 });
  card(s, { x: 4.3, y: cy2, w: 5.2, h: ch, dark: true });
  label(s, 'RICHIESTA STRUTTURATA', 4.55, cy2 + 0.22, 4, C.accent2);
  const parts = [['Ruolo', 'Sei un tecnico commerciale che prepara un\'offerta.'], ['Dati', 'In allegato il capitolato del cliente, anonimizzato.'], ['Compito', 'Estrai i requisiti tecnici e le differenze dallo standard.'], ['Limiti', 'Se un dato manca scrivi "non presente", non dedurlo.'], ['Formato', 'Tabella: requisito, pagina, note.']];
  parts.forEach((p, k) => {
    const y = cy2 + 0.58 + k * 0.45;
    T(s, p[0], { x: 4.55, y, w: 0.95, h: 0.4, fontSize: 11, bold: true, color: C.accent2 });
    T(s, p[1], { x: 5.5, y, w: 3.8, h: 0.4, fontSize: 11.5, color: C.background1 });
  });
  T(s, 'Ruolo · dati · compito · limiti · formato: la richiesta ben fatta secondo COMPASS.', { x: G.X, y: 4.5, w: G.CW, h: 0.3, fontSize: 12.5, bold: true, color: C.accent1 });
  s.addNotes('Tipo DUE CARD. Esempio sul caso richieste d\'offerta (illustrativo). Testi delle richieste da validare.');

  // 13 · ESERCIZIO
  s = pres.addSlide({ masterName: 'BA Contenuto' });
  H(s, 7); tag(s, 'CAMPIONE · ESERCIZIO');
  s.addText('Laboratorio: l\'AI su una tua attività', { placeholder: 'title' });
  const steps = [
    ['Scegli', 'un\'attività reale e un materiale che puoi usare: pubblico, interno non riservato o anonimizzato.'],
    ['Chiedi', 'come faresti oggi e annota il risultato.'],
    ['Riscrivi', 'la richiesta con ruolo, dati, compito, limiti e formato. Confronta i due risultati.'],
    ['Verifica', 'sull\'originale: che cosa è corretto, che cosa manca, che cosa è inventato.'],
  ];
  steps.forEach((st, i) => {
    const y = G.BODY_Y + 0.08 + i * 0.78;
    s.addText(String(i + 1), { shape: 'ellipse', x: G.X, y, w: 0.42, h: 0.42, fill: { color: C.accent1 }, line: { type: 'none' }, color: C.background1, fontSize: 13, bold: true, align: 'center', valign: 'middle', margin: 0 });
    if (i < steps.length - 1) s.addShape('line', { x: G.X + 0.21, y: y + 0.46, w: 0, h: 0.3, line: { color: HEX.linea, width: 1 } });
    T(s, [{ text: st[0] + ' ', options: { bold: true, color: C.text1 } }, { text: st[1], options: { color: C.text2 } }], { x: 1.1, y: y + 0.02, w: 4.9, h: 0.65, fontSize: 12.5 });
  });
  card(s, { x: 6.45, y: G.BODY_Y + 0.05, w: 3.05, h: 3.05, dark: true });
  await iconDot(s, 'LuFileText', 6.7, G.BODY_Y + 0.3, 0.5, { dark: true });
  label(s, 'OUTPUT', 6.7, 2.35, 2.6, C.accent2);
  T(s, 'Scheda di prova nel dossier: attività, richiesta, risultato, verifica.', { x: 6.7, y: 2.6, w: 2.6, h: 0.8, fontSize: 12, color: C.background1 });
  label(s, 'REGOLA', 6.7, 3.5, 2.6, C.accent2);
  T(s, 'Solo strumenti autorizzati e materiali consentiti.', { x: 6.7, y: 3.75, w: 2.6, h: 0.55, fontSize: 12, color: C.background1 });
  s.addNotes('Tipo ESERCIZIO. Tempi da definire nella scheda M1.');

  // 14 · PAUSA
  s = pres.addSlide({ masterName: 'BA Scura' });
  tag(s, 'CAMPIONE · PAUSA', true);
  s.addImage({ data: await icon('LuCoffee', HEX.tealChiaro), x: G.X, y: 1.75, w: 0.5, h: 0.5 });
  T(s, 'Pausa', { x: G.X, y: 2.4, w: G.CW, h: 0.8, fontSize: 40, bold: true, color: C.background1, valign: 'middle' });
  T(s, 'Dieci minuti', { x: G.X, y: 3.2, w: G.CW, h: 0.4, fontSize: 15, color: C.accent2 });
  s.addNotes('Tipo PAUSA.');

  // 15 · CHIUSURA
  s = pres.addSlide({ masterName: 'BA Scura' });
  tag(s, 'CAMPIONE · CHIUSURA', true);
  label(s, 'PRIMA DELLA PROSSIMA SESSIONE', G.X, 0.5, 6, C.accent2);
  s.addText('Sfida 1 · dal 15 al 22 ottobre', { placeholder: 'title' });
  await iconDot(s, 'LuFlag', G.X, 1.75, 0.5, { dark: true });
  T(s, 'Trenta minuti di lavoro individuale con l\'AI', { x: 1.2, y: 1.75, w: 8, h: 0.5, fontSize: 14, bold: true, color: C.accent2, valign: 'middle' });
  T(s, bullets(['Prova l\'AI su un\'attività ricorrente del tuo lavoro.', 'Annota dove funziona e dove no.', 'Elenca 2-3 processi candidati a diventare il tuo filo rosso.'], { gap: 7 }), { x: 1.2, y: 2.45, w: 8.3, h: 1.4, fontSize: 15, color: C.background1 });
  T(s, 'Il 22/10 si riparte da qui: quindici minuti di ripresa della sfida.', { x: 1.2, y: 4.1, w: 8, h: 0.35, fontSize: 12.5, color: C.accent2 });
  s.addNotes('Tipo CHIUSURA.');

  await B.save(pres, process.argv[2] || 'Deck_campione_v02.pptx');
  console.log('ok');
})();
