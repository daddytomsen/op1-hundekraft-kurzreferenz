/* Offline-Betrieb der OP-1-Kurzreferenz. App und Texte: erst Netz, sonst Cache (so kommen Updates sofort an).
   Bilder ändern sich nicht: erst Cache, sonst Netz. */
const C="op1ref-v1";
const CORE=["./","index.html","anleitung.js","manifest.webmanifest","icon-180.png","icon-512.png","manual/keys/PLAY.png","manual/keys/REC.png","manual/keys/STOP.png","manual/keys/T1.png","manual/keys/T2.png","manual/keys/T3.png","manual/keys/T4.png","manual/keys/drop.png","manual/keys/drum.png","manual/keys/help.png","manual/keys/knob-b.png","manual/keys/knob-g.png","manual/keys/knob-o.png","manual/keys/knob-w.png","manual/keys/left.png","manual/keys/lift.png","manual/keys/metronome.png","manual/keys/mixer.png","manual/keys/right.png","manual/keys/scissors.png","manual/keys/seq.png","manual/keys/synth.png","manual/keys/tape.png"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting()))});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
const keep=(r,x)=>{if(x&&x.ok){const cp=x.clone();caches.open(C).then(c=>c.put(r,cp))}return x};
self.addEventListener("fetch",e=>{
  const r=e.request;if(r.method!=="GET")return;
  const u=new URL(r.url);if(u.origin!==location.origin)return;
  if(u.pathname.includes("/manual/")){e.respondWith(caches.match(r,{ignoreSearch:true}).then(h=>h||fetch(r).then(x=>keep(r,x))));return}
  e.respondWith(fetch(r).then(x=>keep(r,x)).catch(()=>caches.match(r,{ignoreSearch:true}).then(h=>h||caches.match("index.html"))));
});
