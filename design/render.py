"""Genera el ícono, el splash y el gráfico destacado de la tienda a partir de design/art.js.

Uso: python3 design/render.py   (desde la raíz del proyecto, después de `npm run build`)
"""
import asyncio
import pathlib
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
ART = (ROOT / 'design' / 'art.js').read_text(encoding='utf8')
BASE = f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="fonts.css"><style>
html,body{{margin:0;background:transparent}}
.t{{font-family:'Bricolage Grotesque';font-weight:800;color:#E8F7F8;letter-spacing:-.02em;line-height:.95}}
.t span{{background:linear-gradient(90deg,#40E0E8,#9AFBFF);-webkit-background-clip:text;color:transparent}}
.s{{font-family:'Atkinson Hyperlegible';color:#A9D3DE}}
</style><script>{ART}</script></head><body>"""

PAGES = {
    'assets/icon-only.png': (1024, 1024, "<div id=x style='width:1024px;height:1024px'></div><script>x.innerHTML=ART.iconFull()</script>"),
    'assets/icon-foreground.png': (1024, 1024, "<div id=x style='width:1024px;height:1024px'></div><script>x.innerHTML=ART.iconFg()</script>"),
    'design/out/adaptive-foreground.png': (1024, 1024, "<div id=x style='width:1024px;height:1024px'></div><script>x.innerHTML=ART.iconFg().replace('scale(.9)','scale(.6)')</script>"),
    'assets/icon-background.png': (1024, 1024, "<div id=x style='width:1024px;height:1024px'></div><script>x.innerHTML=ART.iconBg()</script>"),
    'store/icono-512.png': (512, 512, "<div id=x style='width:512px;height:512px'></div><script>x.innerHTML=ART.iconFull().replace('width=\"1024\" height=\"1024\"','width=\"512\" height=\"512\"')</script>"),
}
SPLASH = """<div id=x style="width:2732px;height:2732px;background:#03111A;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px">
<div id=f style="width:820px;height:820px"></div><div class=t style="font-size:132px;margin-top:-90px">Mi Primer <span>Acuario</span></div></div>
<script>f.innerHTML=ART.fishOnly(1.05)</script>"""
FEATURE = """<div id=x style="width:1024px;height:500px;position:relative;overflow:hidden;background:radial-gradient(circle at 74% 34%,#13798A 0,#073543 38%,#03111A 78%)">
<div style="position:absolute;inset:0;background:repeating-linear-gradient(100deg,rgba(255,255,255,0) 0 90px,rgba(255,255,255,.04) 90px 150px,rgba(255,255,255,0) 150px 260px)"></div>
<div id=f style="position:absolute;left:470px;top:-40px;width:580px;height:580px"></div>
<div style="position:absolute;inset:0;background:linear-gradient(90deg,#03111A 28%,rgba(3,17,26,.55) 46%,rgba(3,17,26,0) 60%)"></div>
<div style="position:absolute;left:64px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;gap:22px;width:500px">
<div class=t style="font-size:76px">Mi Primer<br><span>Acuario</span></div>
<div class=s style="font-size:27px;line-height:1.3">Aprende a cuidar peces cuidándolos: un acuario vivo en tiempo real.</div></div></div>
<script>f.innerHTML=ART.fishOnly(.95)</script>"""


async def main():
    (ROOT / 'store').mkdir(exist_ok=True)
    (ROOT / 'assets').mkdir(exist_ok=True)
    (ROOT / 'design' / 'out').mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        jobs = dict(PAGES)
        jobs['assets/splash.png'] = (2732, 2732, SPLASH)
        jobs['assets/splash-dark.png'] = (2732, 2732, SPLASH)
        jobs['store/grafico-destacado-1024x500.png'] = (1024, 500, FEATURE)
        for out, (w, h, body) in jobs.items():
            pg = await b.new_page(viewport={'width': w, 'height': h})
            tmp = ROOT / 'www' / 'fonts' / '_render.html'
            tmp.write_text(BASE + body + '</body></html>', encoding='utf8')
            await pg.goto(tmp.as_uri())
            await pg.evaluate('document.fonts.ready')
            await pg.wait_for_timeout(150)
            transparent = 'foreground' in out
            await pg.locator('#x').screenshot(path=str(ROOT / out), omit_background=transparent)
            await pg.close()
            tmp.unlink()
            print('ok', out)
        await b.close()

asyncio.run(main())
