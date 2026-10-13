"""Ícono adaptativo de Android en alta resolución (capas de 108 dp sin recortes extra).
Uso: python3 design/android_icons.py  (después de design/render.py y de `npx capacitor-assets generate`)"""
import pathlib
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parent.parent
RES = ROOT / 'android/app/src/main/res'
fg = Image.open(ROOT / 'design/out/adaptive-foreground.png').convert('RGBA')
bg = Image.open(ROOT / 'assets/icon-background.png').convert('RGBA')
for d, px in {'mdpi': 108, 'hdpi': 162, 'xhdpi': 216, 'xxhdpi': 324, 'xxxhdpi': 432}.items():
    fg.resize((px, px), Image.LANCZOS).save(RES / f'mipmap-{d}/ic_launcher_foreground.png')
    bg.resize((px, px), Image.LANCZOS).convert('RGB').save(RES / f'mipmap-{d}/ic_launcher_background.png')
xml = '''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@mipmap/ic_launcher_background" />
    <foreground android:drawable="@mipmap/ic_launcher_foreground" />
    <monochrome android:drawable="@drawable/ic_stat_fish_mono" />
</adaptive-icon>
'''
for n in ('ic_launcher.xml', 'ic_launcher_round.xml'):
    (RES / 'mipmap-anydpi-v26' / n).write_text(xml)
print('ok')
