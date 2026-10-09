"""Portable bilingual V9. Local assets embedded; direct-CDN hero and stock portraits remain remote."""
from pathlib import Path
from bs4 import BeautifulSoup
import argparse,base64,zipfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument("--out",type=Path,required=True)
args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
def embedded(path):
    f=ROOT/"public"/path.lstrip("/")
    mime={".svg":"image/svg+xml",".webp":"image/webp",".png":"image/png"}[f.suffix]
    return "data:"+mime+";base64,"+base64.b64encode(f.read_bytes()).decode()
css=(ROOT/"public/styles.css").read_text()
css=css.replace("url(\"/images/udp-map-detail.webp\")","url(\""+embedded("/images/udp-map-detail.webp")+"\")")
js=(ROOT/"public/interaction.js").read_text()
pages={}
for lang,path in [("es","index.html"),("en","en/index.html")]:
    soup=BeautifulSoup((ROOT/"dist"/path).read_text(),"html.parser")
    for image in soup.select("img"):
        if image["src"].startswith("/"):image["src"]=embedded(image["src"])
    for link in soup.select("a[href]"):
        if link["href"]=="/":link["href"]="?lang=es"
        elif link["href"]=="/en":link["href"]="?lang=en"
    pages[lang]="".join(str(n) for n in soup.body.contents)
    if lang=="es":
        for node in soup.head.select("link[rel=stylesheet],link[rel=preload],script[src]"):node.decompose()
        soup.head.select_one("link[rel=icon]")["href"]=embedded("/favicon.svg")
        soup.head.select_one("meta[name=robots]")["content"]="noindex,nofollow"
        head="".join(str(n) for n in soup.head.contents)
locale="""
const englishTemplate = document.getElementById("english-page");
if (new URLSearchParams(window.location.search).get("lang") === "en") {
  document.documentElement.lang = "en";
  document.title = "InsideLabs — Your next big step. We build it.";
  const englishContent = englishTemplate.innerHTML;
  document.body.innerHTML = englishContent;
} else {
  englishTemplate.remove();
}
"""
preview="<!doctype html>\n<html lang=\"es\"><head>"+head+"<style>"+css+"</style></head><body>"+pages["es"]+"<template id=\"english-page\">"+pages["en"]+"</template><script>"+locale+js+"</script></body></html>"
name="InsideLabs-v9.html"
(args.out/name).write_text(preview)
soup=BeautifulSoup(preview,"html.parser")
assert not soup.select("script[src],link[rel=stylesheet],link[rel=preload],img[src^=\"/\"],.portrait-credit,.contact-trust,.cinematic-hero")
assert len(soup.select("[data-stock-photo]"))==6
assert len(soup.select("[data-official-brand]"))==4
assert len(soup.select("[data-stack-asset]"))==6
assert len(soup.select(".project-card"))==10
assert len(soup.select(".service-detail"))==8
assert len(soup.select(".testimonial-card"))==6
assert not soup.select("[data-motion-replay],.motion-scene,.motion-hero")
assert len(soup.select("[data-hero-photo]"))==2
for lang,body in pages.items():
    content=BeautifulSoup(body,"html.parser")
    assert [n.text.strip() for n in content.select(".team-info h3")]==["Gabriel González","Ezequiel Morales","Maximiliano Solorza"]
    assert "photo-1594672830234-ba4cfe1202dc" in content.select("[data-stock-photo]")[1]["src"]
    photo=content.select_one(".photo-hero img")
    assert photo and photo["src"].startswith("https://images.unsplash.com/photo-1517336714731-489689fd1ca8")
    assert "/download?" not in photo["src"]
    assert not content.select("[data-motion-replay],.motion-scene")
    assert len(content.select("#contact-modal .contact-person"))==3
assert "url(\"/images/" not in css
archive=args.out/"InsideLabs-v9-source.zip"
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for file in sorted(ROOT.rglob("*")):
        if not file.is_file():continue
        if any(p in {"__pycache__",".astro","node_modules",".git"} for p in file.relative_to(ROOT).parts):continue
        z.write(file,Path("InsideLabs")/file.relative_to(ROOT))
    z.writestr("InsideLabs/preview/"+name,preview)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for expected in ["tools/hero-photo.html.j2","tools/brands.html.j2","src/components/Header.tsx","dist/en/index.html","public/interaction.js","README.md"]:
        assert "InsideLabs/"+expected in z.namelist(),expected
    print("Archive verified:",len(z.namelist()),"files")
for f in [args.out/name,archive]:print(f.name,f.stat().st_size,"bytes")
print("V9 verified: direct-CDN photographic hero without animation, exact direct portrait reference, retained contact selector.")
