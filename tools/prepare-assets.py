"""Prepare original, undistorted screenshots. Requires Pillow; no network requests."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"public/images"
source=ROOT/"design/source"
im=Image.open(source/"pharmalogic.png").convert("RGB")
im.crop((346,771,1345,1336)).save(OUT/"pharma-screen.webp",quality=96)
im=Image.open(source/"optiwallet.png").convert("RGB")
# Crop before the landing-page counters: the supplied brief and screenshot differ.
# The original product UI and copy remain undistorted.
im.crop((0,0,1676,990)).save(OUT/"opti-screen.webp",quality=95)
im=Image.open(source/"udp-map.png").convert("RGB")
im.save(OUT/"udp-map.webp",quality=93)
im.crop((0,150,1320,1200)).save(OUT/"udp-map-detail.webp",quality=93)
# Sharing artwork is a flat editorial composition, not a screenshot of the website.
im=Image.new("RGB",(1200,630),"#fcfcfa");d=ImageDraw.Draw(im)
font=lambda n:ImageFont.load_default(size=n)
d.rectangle((54,48,77,71),outline="#2457ef",width=3)
d.rectangle((68,62,91,85),outline="#2457ef",width=3)
d.text((109,49),"InsideLabs",font=font(31),fill="#15202e")
d.text((53,175),"Tu próximo salto.",font=font(55),fill="#15202e")
d.text((53,253),"Lo construimos.",font=font(55),fill="#2457ef")
d.text((56,359),"Software a medida. IA. Seguridad.",font=font(20),fill="#596a7f")
d.rounded_rectangle((55,425,328,483),radius=8,fill="#2457ef")
d.text((77,446),"Hablemos de tu proyecto",font=font(19),fill="white")
d.text((55,565),"DESDE CHILE. SIN FRONTERAS.",font=font(13),fill="#667a96")
d.rounded_rectangle((635,51,1152,579),radius=18,fill="#153f92")
d.rectangle((762,168,928,334),outline="#95baff",width=5)
d.rectangle((849,255,1015,421),outline="#95baff",width=5)
d.text((672,87),"INSIDELABS / SOFTWARE CON PROPÓSITO",font=font(13),fill="#b9d3ff")
d.text((672,489),"Construir bien. Pensar más allá.",font=font(21),fill="#f0f6ff")
im.save(OUT/"social-card.png",optimize=True)
print("4 real screenshot assets and matching sharing artwork prepared.")
