"""Capturas de la ficha de la tienda (1080x1920) con un texto arriba.

Uso: npm run build && python3 design/screens.py
Simula el modo teléfono con un puente falso para que la app muestre lo mismo que en Android."""
import asyncio, pathlib, subprocess, time
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'store' / 'capturas'
RAW = ROOT / 'design' / 'out' / 'raw'
MOCK = """window.AQN={platform:'android',version:async()=>'1.0.0',store:{get:async k=>localStorage.getItem('m:'+k),set:async(k,v)=>localStorage.setItem('m:'+k,v),remove:async()=>{}},
haptic(){},notif:{status:async()=>'granted',request:async()=>'granted',replace:async()=>{},onTap(){}},shareFile:async()=>{},onBack(){},onState(){},minimize:async()=>{},hideSplash:async()=>{}};"""
SHOTS = [
    ('01-acuario', 'Un acuario vivo,', 'en tiempo real'),
    ('02-alimentar', 'Aliméntalos', 'con tus propias manos'),
    ('03-pez', 'Conoce a cada pez', 'y ponle nombre'),
    ('04-kit', 'Mide el agua como', 'con un kit de gotas real'),
    ('05-cambio', 'Cambia el agua', 'y sifonea el fondo'),
    ('06-agua', 'Entiende qué pasa', 'en el agua'),
    ('07-avisos', 'Te avisa cuando', 'tus peces te necesitan'),
    ('08-noche', 'De día y de noche,', 'como un acuario de verdad'),
]
FRAME = """<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{fonts}">
<style>html,body{{margin:0}}#x{{width:1080px;height:1920px;position:relative;overflow:hidden;background:radial-gradient(circle at 50% 18%,#13798A 0,#073543 40%,#03111A 80%);font-family:'Bricolage Grotesque'}}
.c{{position:absolute;top:96px;left:0;right:0;text-align:center;color:#E8F7F8;font-weight:800;font-size:76px;line-height:1.02;letter-spacing:-.02em}}
.c span{{display:block;background:linear-gradient(90deg,#40E0E8,#9AFBFF);-webkit-background-clip:text;color:transparent}}
.p{{position:absolute;left:50%;top:330px;width:820px;height:1600px;transform:translateX(-50%);border-radius:64px;overflow:hidden;box-shadow:0 0 0 14px #0B1F27,0 0 0 16px rgba(150,230,240,.25),0 40px 120px rgba(0,0,0,.6)}}
.p img{{width:100%;display:block}}</style></head><body><div id=x><div class=c>{a}<span>{b}</span></div><div class=p><img src="{img}"></div></div></body></html>"""


async def main():
    OUT.mkdir(parents=True, exist_ok=True); RAW.mkdir(parents=True, exist_ok=True)
    srv = subprocess.Popen(['python3', '-m', 'http.server', '8771', '-d', str(ROOT / 'www')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch()
            ctx = await b.new_context(viewport={'width': 410, 'height': 800}, device_scale_factor=3, has_touch=True)
            await ctx.route('**/native.js', lambda r: r.fulfill(body=MOCK, content_type='application/javascript'))
            pg = await ctx.new_page()
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto('http://localhost:8771/index.html'); await pg.wait_for_timeout(900)
            await pg.evaluate("localStorage.setItem('ba-tour4','1');localStorage.setItem('ba-notif','1')")
            await pg.click('[data-act=sample]'); await pg.wait_for_timeout(900)
            await pg.evaluate("""(()=>{const t=curTank(),S=simOf(t.id);S.fish=S.fish.filter(f=>!f.dead);S.fish.forEach(f=>{f.dz=null;f.hp=Math.max(f.hp,92);f.hun=30;f.diet=Math.max(f.diet,70)});
              S.left=0;S.algae=S.algae.map(a=>a*.25);S.medH=0;set().name='Fernando';const d=new Date(S.clock);d.setHours(10,30);S.clock=d.getTime();act()})()""")
            await pg.evaluate("document.querySelector('#toast').innerHTML='';window.scrollTo(0,0)")
            await pg.wait_for_timeout(2500)
            hide = "document.querySelector('#toast').innerHTML=''"
            async def raw(name):
                await pg.evaluate(hide); await pg.wait_for_timeout(250)
                await pg.screenshot(path=str(RAW / f'{name}.png'))
            await raw('01-acuario')
            bb = await pg.locator('#stage-slot').bounding_box()
            await pg.click('[data-act=food][data-k=flake]')
            for i in range(4):
                await pg.mouse.click(bb['x'] + bb['width'] * (.3 + i * .13), bb['y'] + bb['height'] * .1); await pg.wait_for_timeout(120)
                await pg.evaluate("ui.fpop=null;{const b=document.querySelector('#fpop');if(b)b.hidden=true}")
            await pg.wait_for_timeout(1500); await raw('02-alimentar')
            pos = await pg.evaluate("(()=>{const f=STAGE.fish.find(x=>!x.dead&&x.sp.id==='escalar')||STAGE.fish.find(x=>!x.dead);const r=STAGE.cv.getBoundingClientRect();return [r.left+f.x,r.top+f.y]})()")
            await pg.mouse.click(pos[0], pos[1]); await pg.wait_for_timeout(500); await raw('03-pez')
            await pg.click('[data-act=fp-close]')
            await pg.click('.toolbar [data-k=test]'); await pg.wait_for_timeout(300)
            await pg.click('[data-act=qstart][data-quick="0"]'); await pg.wait_for_timeout(200)
            for i in range(3): await pg.click('[data-act=qdrop]'); await pg.wait_for_timeout(60)
            await pg.click('[data-act=qshake]'); await pg.wait_for_timeout(4200); await raw('04-kit')
            await pg.click('#sheet .sw >> nth=3'); await pg.wait_for_timeout(150); await pg.click('[data-act=qnext]')
            for k in range(3):
                n = await pg.evaluate("KIT[['ph','nh3','no2','no3'][ui.sheet.i]].drops")
                for i in range(n): await pg.click('[data-act=qdrop]'); await pg.wait_for_timeout(30)
                await pg.wait_for_timeout(300); await pg.click('[data-act=qshake]'); await pg.wait_for_timeout(3600)
                await pg.click('#sheet .sw >> nth=0'); await pg.wait_for_timeout(150); await pg.click('[data-act=qnext]'); await pg.wait_for_timeout(200)
            await pg.click('[data-act=qsave]'); await pg.wait_for_timeout(500)
            await pg.click('.toolbar [data-k=wc]'); await pg.wait_for_timeout(300)
            hb = await pg.locator('[data-hold=drain]').bounding_box()
            await pg.mouse.move(hb['x'] + hb['width'] / 2, hb['y'] + hb['height'] / 2); await pg.mouse.down(); await pg.wait_for_timeout(1300); await pg.mouse.up(); await pg.wait_for_timeout(300)
            await raw('05-cambio')
            await pg.click('[data-act=close]'); await pg.wait_for_timeout(300)
            await pg.click('[data-act=tab][data-tab=agua] >> visible=true'); await pg.wait_for_timeout(600); await raw('06-agua')
            await pg.click('[data-act=tab][data-tab=acuario] >> visible=true'); await pg.wait_for_timeout(500)
            await pg.evaluate("openSheet({type:'nask'})"); await pg.wait_for_timeout(600); await raw('07-avisos')
            await pg.evaluate("closeSheet()")
            await pg.evaluate("(()=>{const S=simOf(ui.tankId);const d=new Date(S.clock);d.setHours(21,30);S.clock=d.getTime();S.lightK=0;S.light=false})()"); await pg.wait_for_timeout(1800)
            await raw('08-noche')
            fonts = (ROOT / 'www' / 'fonts' / 'fonts.css').as_uri()
            for name, a, bline in SHOTS:
                f = await b.new_page(viewport={'width': 1080, 'height': 1920})
                tmp = RAW / f'{name}.html'
                tmp.write_text(FRAME.format(fonts=fonts, a=a, b=bline, img=(RAW / f'{name}.png').as_uri()), encoding='utf8')
                await f.goto(tmp.as_uri()); await f.evaluate('document.fonts.ready'); await f.wait_for_timeout(200)
                await f.locator('#x').screenshot(path=str(OUT / f'{name}.png'))
                await f.close(); tmp.unlink()
            print('errores', errs)
            await b.close()
    finally:
        srv.terminate()

asyncio.run(main())
