// Construye www/ (lo que va dentro de la app Android/iPhone) a partir de src/app.html.
// - Quita las fuentes de Google (la app debe funcionar sin internet) y usa copias locales.
// - Envuelve la página en un documento completo con los meta de una app móvil.
// - Compila el puente nativo (src/native.js) con esbuild.
import { readFileSync, writeFileSync, mkdirSync, copyFileSync, rmSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSync } from 'esbuild';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const www = join(root, 'www');
const nm = join(root, 'node_modules');
rmSync(www, { recursive: true, force: true });
mkdirSync(join(www, 'fonts'), { recursive: true });

// 1. Fuentes locales
const fonts = [
  ['Atkinson Hyperlegible', '400', '@fontsource/atkinson-hyperlegible/files/atkinson-hyperlegible-latin-400-normal.woff2', 'woff2'],
  ['Atkinson Hyperlegible', '700', '@fontsource/atkinson-hyperlegible/files/atkinson-hyperlegible-latin-700-normal.woff2', 'woff2'],
  ['Bricolage Grotesque', '200 800', '@fontsource-variable/bricolage-grotesque/files/bricolage-grotesque-latin-opsz-normal.woff2', 'woff2-variations'],
  ['Bricolage Grotesque', '200 800', '@fontsource-variable/bricolage-grotesque/files/bricolage-grotesque-latin-ext-opsz-normal.woff2', 'woff2-variations', 'U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF'],
  ['IBM Plex Mono', '400', '@fontsource/ibm-plex-mono/files/ibm-plex-mono-latin-400-normal.woff2', 'woff2'],
  ['IBM Plex Mono', '500', '@fontsource/ibm-plex-mono/files/ibm-plex-mono-latin-500-normal.woff2', 'woff2'],
];
let css = '';
for (const [family, weight, file, format, range] of fonts) {
  const name = file.split('/').pop();
  copyFileSync(join(nm, file), join(www, 'fonts', name));
  css += `@font-face{font-family:'${family}';font-style:normal;font-display:swap;font-weight:${weight};src:url(./${name}) format('${format}')${range ? `;unicode-range:${range}` : ''}}\n`;
}
writeFileSync(join(www, 'fonts', 'fonts.css'), css);

// 2. Página
let app = readFileSync(join(root, 'src', 'app.html'), 'utf8');
const before = app.length;
app = app.replace(/<link rel="preconnect"[^>]*>\s*/g, '').replace(/<link rel="stylesheet" href="https:\/\/fonts\.googleapis\.com[^>]*>\s*/g, '');
if (app.length === before || /fonts\.googleapis/.test(app)) throw new Error('No se pudieron quitar las fuentes de Google de src/app.html');
const cut = app.indexOf('</style>') + '</style>'.length;
if (cut < 8) throw new Error('src/app.html no tiene <style>');
const head = app.slice(0, cut);
const body = app.slice(cut);
const html = `<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">
<meta name="theme-color" content="#03111A">
<meta name="color-scheme" content="dark">
<meta name="format-detection" content="telephone=no">
<link rel="stylesheet" href="fonts/fonts.css">
<script src="native.js"></script>
${head}
</head>
<body>
${body.trim()}
</body>
</html>
`;
writeFileSync(join(www, 'index.html'), html);

// 3. Puente nativo
buildSync({
  entryPoints: [join(root, 'src', 'native.js')],
  outfile: join(www, 'native.js'),
  bundle: true,
  format: 'iife',
  minify: true,
  target: ['es2019'],
  legalComments: 'none',
});

console.log('www/ listo:', Math.round(html.length / 1024) + ' KB de página');
