"""V9 structural verification; not a real browser audit."""
from pathlib import Path
from collections import Counter
from bs4 import BeautifulSoup
import json,re,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
names=["Gabriel González","Ezequiel Morales","Maximiliano Solorza"]
portrait="https://images.unsplash.com/photo-1594672830234-ba4cfe1202dc?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
for route,lang in [("index.html","es"),("en/index.html","en")]:
    soup=BeautifulSoup((ROOT/"dist"/route).read_text(),"html.parser")
    assert soup.html["lang"]==lang
    assert len(soup.select("main"))==len(soup.select("h1"))==1
    counts={".project-card":5,".project-featured":3,".service-detail":4,".service-panel li":12,".process-deliverable":3,".testimonial-card":3,".quote-disclaimer":3,".team-card":3,".faq-item":6,".stack-logos img":6,".stack-logos [data-stack-asset]":3,".security-practices>div":3,".security-reference":1,".service-security-hint":1}
    for selector,count in counts.items():assert len(soup.select(selector))==count,selector
    assert not soup.select("astro-island,.interface-board,.hero-art,.floating-chip,.cinematic-eyebrow,.hero-photo-credit,.contact-alt,.portrait-credit,.contact-trust,.footer-photo-credit")
    ids=[n["id"] for n in soup.select("[id]")]
    assert not [key for key,count in Counter(ids).items() if count>1]
    for a in soup.select("a[href]"):
        if a["href"].startswith("#"):assert a["href"][1:] in ids
    for n in soup.select("[aria-labelledby],[aria-describedby],[aria-controls]"):
        for attr in ["aria-labelledby","aria-describedby","aria-controls"]:
            for value in n.get(attr,"").split():assert value in ids,(attr,value)
    for node in soup.select("img,script[src],link[rel=stylesheet],link[rel=preload]"):
        url=node.get("src") or node.get("href")
        if url.startswith("/"):assert (ROOT/"dist"/url.lstrip("/")).exists(),url
    for image in soup.select("img"):assert image.has_attr("alt")
    for link in soup.select("a[target=_blank]"):assert "noopener" in link.get("rel",[])
    for button in soup.select("button"):assert button.get_text(strip=True) or button.get("aria-label")
    assert [n.text.strip() for n in soup.select(".team-info h3")]==names
    assert [n.text.strip() for n in soup.select(".contact-person strong")]==names
    schema=json.loads(soup.select_one("script[type=\"application/ld+json\"]").string)
    assert [f["name"] for f in schema["founder"]]==names
    assert soup.select(".team-card img")[1]["src"]==portrait
    hero=soup.select_one(".photo-hero")
    assert hero and len(hero.select("img"))==1
    assert not hero.select("svg,[data-motion-replay],.square-piece")
    assert hero.select_one("[data-hero-photo]")["src"]=="https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=1600&q=90"
    assert hero.select_one("#photo-caption")
    assert not soup.select(".motion-hero,[data-motion-replay]")
    preload=soup.select_one("link[rel=preload][as=image]")
    assert preload and preload["href"]==hero.select_one("img")["src"]
    assert "/download?" not in hero.select_one("img")["src"]
    assert len(soup.select("#contact-title>span"))==2
    cta=soup.select_one(".contact-content button[data-contact]")
    assert cta.get_text(strip=True)==("Hablemos de tu idea" if lang=="es" else "Let’s talk about your idea")
    assert len(cta.select("svg"))==1
    assert len(soup.select("#contact-modal .contact-person"))==3
    for brand in ["optiwallet","pharmalogic","gameclub"]:
        marks=[x for x in soup.select("[data-brand-key]") if x["data-brand-key"]==brand]
        assert len(marks)==2
        assert len({x.select_one("img")["src"] for x in marks})==1
    reference=soup.select_one(".security-reference")
    assert "ISO/IEC 27001:2022" in reference.text and "01-DIC-2026" in reference.text
    assert ("no declara una certificación ISO" if lang=="es" else "does not claim ISO certification") in reference.text
    print(lang,"PASS: exact direct photo URL, direct-CDN laptop photo, no replay, no hero animation, removed credits, simple CTA, preserved 3-founder chooser, brands, ARIA and anchors")
css=(ROOT/"public/styles.css").read_text()
assert css.count("{")==css.count("}")
assert "@media(min-width:1800px)" in css and "prefers-reduced-motion:reduce" in css
assert "@keyframes il-squares-meet" not in css
assert ".photo-hero .hero-editorial-photo" in css
assert "animation:none!important;transform:none!important;transition:none!important" in css
for svg in (ROOT/"public").rglob("*.svg"):ET.parse(svg)
print("PASS: mobile/2K CSS, static photographic hero and reduced-motion fallback")
