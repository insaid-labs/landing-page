const { readFileSync } = require("node:fs");
const { resolve } = require("node:path");
const vm = require("node:vm");
const assert = require("node:assert/strict");
class Element {
  constructor(data = {}) { this.dataset = data; this.attrs = {}; this.events = {}; this.hidden = false; this.open = false; this.isConnected = true; this.textContent = ""; this.classes = new Set(); this.classList = { add: n => this.classes.add(n), remove: n => this.classes.delete(n), toggle: (n,on) => on ? this.classes.add(n) : this.classes.delete(n) }; }
  setAttribute(n,v) { this.attrs[n] = v; }
  getAttribute(n) { return this.attrs[n] ?? null; }
  removeAttribute(n) { delete this.attrs[n]; }
  addEventListener(n,fn) { (this.events[n] ??= []).push(fn); }
  emit(n,extra={}) { const event={ target:this, preventDefault(){}, ...extra }; (this.events[n]??[]).forEach(fn=>fn(event)); }
  click() { this.emit("click"); }
  focus() { this.focused = true; }
  querySelectorAll(q) { return this.queries?.[q] ?? []; }
  querySelector(q) { return this.querySelectorAll(q)[0] ?? null; }
  showModal() { this.open = true; }
  close() { this.open = false; this.emit("close"); }
  closest() { return null; }
  contains(e) { return e === this; }
  getBoundingClientRect() { return { left:10,right:200,top:10,bottom:200 }; }
}
function verify(lang) {
 const doc=new Element(); doc.documentElement=new Element(); doc.documentElement.lang=lang; doc.body=new Element();
 const menu=new Element(); menu.attrs["aria-expanded"]="false"; const nav=new Element(); nav.hidden=true;
 const contact=new Element(); const game=new Element(); const pos=new Element(); const dialogs=[contact,game,pos];
 dialogs.forEach(d=>{ const close=new Element(); d.queries={"[data-close]":[close]}; });
 const general=new Element(); const service=new Element({service:lang==="es"?"Software a medida":"Custom software"}); const fromProject=new Element();
 const triggers=[new Element({project:"gameclub"}),new Element({project:"pos"})];
 const filters=["all","product","client"].map(filter=>new Element({filter}));
 const cards=["product","product","product","client","client"].map(category=>new Element({category}));
 const faqs=Array.from({length:6},()=>new Element());
 const servicePanels=Array.from({length:4},()=>new Element());
 const caseLink=new Element();caseLink.setAttribute("href","#case-udp");
 doc.getElementById=id=>id==="case-udp"?cards[2]:null;
 const heroFrame=new Element();const heroPhoto=new Element();heroPhoto.complete=true;heroPhoto.naturalWidth=0;heroPhoto.closest=()=>heroFrame;let reducedMotion=false;
 const brandFrame=new Element();const brandPhoto=new Element();brandPhoto.complete=true;brandPhoto.naturalWidth=0;brandPhoto.closest=()=>brandFrame;
 const stackLink=new Element();const stackImage=new Element();stackImage.complete=true;stackImage.naturalWidth=0;stackImage.closest=()=>stackLink;
 const photoFrame=new Element();const photo=new Element();photo.complete=true;photo.naturalWidth=0;photo.closest=()=>photoFrame;
 const context=new Element(); const status=new Element(); const back=new Element(); const mobileLink=new Element();
 doc.queries={".menu-toggle":[menu],"#mobile-nav":[nav],"#mobile-nav a":[mobileLink],".language-switch[open]":[],".back-top":[back],"dialog":dialogs,"[data-contact], [data-service]":[general,service,fromProject],"#service-context":[context],"#contact-modal":[contact],"[data-project]":triggers,"#project-gameclub":[game],"#project-pos":[pos],"[data-filter]":filters,".project-card":cards,"#filter-status":[status],".faq-item":faqs,".service-detail":servicePanels,"[data-stock-photo]":[photo],"[data-hero-photo]":[heroPhoto],"[data-official-brand]":[brandPhoto],"[data-stack-asset]":[stackImage],"a[href^=\"#case-\"]":[caseLink]};
 let scrollCalled=false; let mediaHandler;
 const win={location:{hash:""},scrollTo:()=>{scrollCalled=true},matchMedia:query=>({matches:query.includes("prefers-reduced-motion")?reducedMotion:false,addEventListener:(_,fn)=>{mediaHandler=fn}})};
 vm.runInNewContext(readFileSync(resolve(__dirname,"../public/interaction.js"),"utf8"),{document:doc,window:win,console});
 assert.ok(heroFrame.classes.has("hero-photo-unavailable"));heroPhoto.emit("load");assert.equal(heroFrame.classes.has("hero-photo-unavailable"),false);heroPhoto.emit("error");assert.ok(heroFrame.classes.has("hero-photo-unavailable"));
 assert.ok(brandFrame.classes.has("brand-logo-unavailable"));brandPhoto.emit("load");assert.equal(brandFrame.classes.has("brand-logo-unavailable"),false);brandPhoto.emit("error");assert.ok(brandFrame.classes.has("brand-logo-unavailable"));
 assert.ok(stackLink.classes.has("stack-asset-unavailable"));stackImage.emit("load");assert.equal(stackLink.classes.has("stack-asset-unavailable"),false);stackImage.emit("error");assert.ok(stackLink.classes.has("stack-asset-unavailable"));
 menu.click(); assert.equal(nav.hidden,false); assert.equal(menu.attrs["aria-expanded"],"true");
 mobileLink.click(); assert.equal(nav.hidden,true);
 menu.click(); doc.emit("keydown",{key:"Escape"}); assert.equal(nav.hidden,true); assert.equal(menu.focused,true);
 menu.click(); mediaHandler({matches:true}); assert.equal(nav.hidden,true);
 filters[1].click(); assert.equal(cards.filter(c=>!c.hidden).length,3); assert.ok(cards.slice(3).every(c=>c.hidden)); assert.equal(filters[1].attrs["aria-pressed"],"true");
 filters[2].click(); assert.ok(cards.slice(0,3).every(c=>c.hidden)); assert.equal(cards.filter(c=>!c.hidden).length,2);
 filters[0].click(); assert.equal(cards.filter(c=>!c.hidden).length,5); assert.ok(status.textContent.startsWith("5"));
 filters[2].click();assert.ok(cards[2].hidden);caseLink.click();assert.equal(cards[2].hidden,false);assert.equal(cards.filter(c=>!c.hidden).length,5);
 assert.ok(photoFrame.classes.has("photo-unavailable"));photo.emit("load");assert.equal(photoFrame.classes.has("photo-unavailable"),false);photo.emit("error");assert.ok(photoFrame.classes.has("photo-unavailable"));
 servicePanels[0].open=true;servicePanels[1].open=true;servicePanels[1].emit("toggle");assert.equal(servicePanels[0].open,false);assert.equal(servicePanels[1].open,true);assert.equal(contact.open,false);
 service.click(); assert.ok(contact.open); assert.equal(context.hidden,false); assert.ok(context.textContent.includes(service.dataset.service)); assert.ok(doc.body.classes.has("modal-open"));
 contact.queries["[data-close]"][0].click(); assert.equal(contact.open,false); assert.ok(service.focused); assert.equal(doc.body.classes.has("modal-open"),false);
 general.click(); assert.equal(context.hidden,true); contact.close();
 triggers[0].click(); assert.ok(game.open); fromProject.click(); assert.equal(game.open,false); assert.ok(contact.open); contact.close(); assert.ok(triggers[0].focused);
 triggers[1].click(); assert.ok(pos.open); pos.emit("click",{clientX:0,clientY:0}); assert.equal(pos.open,false);
 faqs[0].open=true; faqs[1].open=true; faqs[1].emit("toggle"); assert.equal(faqs[0].open,false); assert.equal(faqs[1].open,true);
 back.click(); assert.ok(scrollCalled);
 console.log(`${lang}: PASS — mobile menu, Escape, resize, 5 projects, 3 filters, deep-link recovery, hero/portrait/brand/stack fallbacks, service accordions, live status, service context, dialogs, focus restoration, backdrop, FAQ, back-to-top`);
}
verify("es"); verify("en");
