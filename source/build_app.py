"""Build the installable web app (GitHub Pages PWA) from the artifact page into scratchpad/app/."""
import os, re, shutil, json, hashlib
S='/tmp/claude-0/-home-claude/f0ab6655-4acc-54ae-87fe-327961bfcf77/scratchpad/'
A=S+'app/'
h=open(S+'kompozit-konusma.html').read()
def rep(a,b,src=None):
    global h
    assert h.count(a)==1,(h.count(a),a[:80]); h=h.replace(a,b)

# --- Claude: the artifact's sample capability becomes a direct API call with the user's own key ---
rep('''let sample=null;
const aiReady = (async()=>{try{sample=await window.claude?.use?.("sample")}catch{sample=null}
  if(!sample) aiOff(); return sample})();''','''let sample=null;
/* The app calls the Claude API directly from the browser with the learner's own key (kept only on this device). */
const SDK_URL=new URL("vendor/anthropic-sdk.mjs",location.href).href; // @anthropic-ai/sdk 0.131.0, bundled
const MODEL="claude-opus-5-5";
let sdkP=null;
function apiKey(){try{return localStorage.getItem("lt.apikey")||""}catch{return ""}}
function makeSample(){
  if(!apiKey()) return null;
  return {async json(input,opts={}){
    sdkP=sdkP||import(SDK_URL);
    const {default:Anthropic}=await sdkP;
    const client=new Anthropic({apiKey:apiKey(),dangerouslyAllowBrowser:true});
    const messages=typeof input==="string"?[{role:"user",content:input}]:input;
    let r;
    try{
      r=await client.beta.messages.create({model:MODEL,max_tokens:4000,output_config:{effort:"low"},
        betas:["server-side-fallback-2026-07-01"],fallbacks:"default",messages},{signal:opts.signal});
    }catch(e){
      if(e instanceof Anthropic.AuthenticationError) throw {code:"bad_key"};
      if(e instanceof Anthropic.RateLimitError) throw {code:"rate_limited"};
      if(e instanceof Anthropic.APIUserAbortError) throw {code:"aborted"};
      if(e instanceof Anthropic.APIConnectionError) throw {code:"offline"};
      throw {code:"api_error",message:e?.message};
    }
    if(r.stop_reason==="refusal") throw {code:"refusal"};
    const text=r.content.filter(b=>b.type==="text").map(b=>b.text).join("");
    const m=text.match(/\\{[\\s\\S]*\\}/); if(!m) throw {code:"invalid_json"};
    try{return JSON.parse(m[0])}catch{throw {code:"invalid_json"}}
  }};
}
const aiReady=(async()=>{sample=makeSample(); if(!sample) aiOff(); return sample})();''')
rep('''  if(c==="rate_limited") return "Çok sık istek gitti. Biraz bekleyip tekrar gönder.";''','''  if(c==="rate_limited") return "Çok sık istek gitti. Biraz bekleyip tekrar gönder.";
  if(c==="bad_key") return "API anahtarı kabul edilmedi. Ayarlar'dan anahtarı kontrol et.";
  if(c==="offline") return "İnternet bağlantısı yok. Bağlanınca tekrar gönder.";
  if(c==="refusal") return "Claude bu mesaja cevap vermedi. Başka bir şekilde yaz.";
  if(c==="aborted") return "Durduruldu.";
  if(c==="api_error") return "Claude'a ulaşılamadı: "+(e.message||"bilinmeyen hata");''')
# --- offline-capable voice engine: all scripts served from the app itself ---
rep('loadScript("https://cdnjs.cloudflare.com/ajax/libs/onnxruntime-web/1.18.0/ort.min.js")','loadScript("ort/ort.min.js")')
rep('''    try{ph=await import("https://cdn.jsdelivr.net/npm/phonemizer@1.2.1/dist/phonemizer.js")}
    catch{ph=await import(new URL("tts/phonemizer.js",location.href).href)}''','''    ph=await import(new URL("tts/phonemizer.js",location.href).href);''')
# --- progress: on this device, plus backup/restore file ---
rep('''  if(!db||!me?.id){ accState("Giriş yapılmadığı için ilerleme sadece bu cihazda tutuluyor"); showResume(); return }''','''  if(!db||!me?.id){ accState("İlerlemen bu cihazda kaydediliyor","ok"); showResume(); return }''')
# --- texts: the real microphone works here ---
rep('''Son turda söylediklerini buraya konuşarak yazdır: kutuya tıkla, Windows'ta <b>Win + H</b>, Mac'te <b>Fn</b> tuşuna iki kez bas ve mikrofona konuş. Sonra "Daha doğal nasıl söylenir?"e bas:''','''Turlar sırasında konuştukların mikrofonla otomatik yazılır (Chrome ve Edge); son turun metni bu kutuya gelir. Olmazsa kutuya tıklayıp Windows'ta <b>Win + H</b> ile dikte et. Sonra "Daha doğal nasıl söylenir?"e bas:''')
rep('''placeholder="Mikrofonla konuşmak için kutuya tıkla, Windows'ta Win + H (Mac'te Fn iki kez) bas. İngilizce bulamadığın kelimeyi Türkçe söyleyebilirsin."''','''placeholder="Cevabını yaz ya da Konuş tuşuna basıp söyle. İngilizce bulamadığın kelimeyi Türkçe söyleyebilirsin."''')
rep('''Konuşma partneri bu görünümde çalışmıyor. 1. ve 2. istasyonlar ve ifade kurtarıcı sözlüğü yine kullanılabilir.''','''Konuşma partneri için en üstteki "Ayarlar"dan Claude API anahtarını gir. Anahtar olmadan 1. ve 2. istasyonlar ve ifade sözlüğü yine çalışır.''')
rep('''    <div class="resume" id="resume" hidden>''','''    <details class="settings">
      <summary>Ayarlar ve yedek</summary>
      <div class="set-body">
        <label for="apiKeyIn">Claude API anahtarı (toplantı partneri, doğal hali ve kelime bulma için)</label>
        <div class="ctrls"><input type="password" id="apiKeyIn" placeholder="sk-ant-..." autocomplete="off"><button id="apiKeySave">Kaydet</button><button id="apiKeyDel">Sil</button></div>
        <p class="muted" style="font-size:.8rem">Anahtar sadece bu cihazda saklanır ve doğrudan Anthropic'e gönderilir. Kullanım ücreti bu anahtarın hesabından düşer. Anahtarı console.anthropic.com adresinden alabilirsin.</p>
        <div class="ctrls"><button id="bkOut">İlerlemeyi yedekle (dosya)</button><label class="btnlike" for="bkIn">Yedeği yükle</label><input type="file" id="bkIn" accept="application/json,.json" hidden></div>
        <p class="muted" style="font-size:.8rem">Telefondan bilgisayara geçerken: bir cihazda yedekle, dosyayı diğer cihaza gönder ve orada yükle.</p>
      </div>
    </details>
    <div class="resume" id="resume" hidden>''')
rep('''.resume{display:flex;''','''.settings{flex:1 1 100%;order:3}
.settings summary{cursor:pointer;font-size:.88rem;color:var(--muted)}
.set-body{display:flex;flex-direction:column;gap:8px;padding-top:8px}
.set-body input[type=password]{flex:1 1 220px;min-width:0}
.btnlike{display:inline-flex;align-items:center;border:1px solid var(--line);border-radius:6px;padding:8px 14px;cursor:pointer;background:var(--surface)}
.resume{display:flex;''')
APPJS='''
/* ---------- app shell: settings, backup, offline ---------- */
$("#apiKeyIn").value=apiKey()?"••••••••":"";
$("#apiKeySave").onclick=()=>{const v=$("#apiKeyIn").value.trim(); if(!v||v.startsWith("•")) return;
  try{localStorage.setItem("lt.apikey",v)}catch{} sample=makeSample(); $("#apiKeyIn").value="••••••••";
  $("#aiOff").hidden=true; $("#send").disabled=false; $("#say").disabled=false; $("#txFeedback").disabled=false; accState("API anahtarı kaydedildi","ok")};
$("#apiKeyDel").onclick=()=>{try{localStorage.removeItem("lt.apikey")}catch{} sample=null; $("#apiKeyIn").value=""; aiOff()};
$("#bkOut").onclick=()=>{const kv={}; SYNC_KEYS.forEach(k=>{const v=store.get(k,undefined); if(v!==undefined) kv[k]=v});
  const blob=new Blob([JSON.stringify({app:"laminate-talk",v:1,updatedAt:+store.get("lt.updatedAt",Date.now()),kv})],{type:"application/json"});
  const a=document.createElement("a"); a.href=URL.createObjectURL(blob); a.download="laminate-talk-yedek-"+dayKey()+".json"; a.click(); setTimeout(()=>URL.revokeObjectURL(a.href),5000)};
$("#bkIn").onchange=async e=>{const f=e.target.files[0]; if(!f) return;
  try{const d=JSON.parse(await f.text()); if(d.app!=="laminate-talk"||!d.kv) throw 0; applyRemote({...d,updatedAt:Date.now()}); store.put("lt.updatedAt",Date.now()); showResume(); accState("Yedek yüklendi","ok")}
  catch{accState("Bu dosya bir Laminate Talk yedeği değil","warn")} e.target.value=""};
if("serviceWorker" in navigator) addEventListener("load",()=>navigator.serviceWorker.register("sw.js").catch(()=>{}));
'''
h=re.sub(r'</script>\s*$', lambda m: APPJS+'</script>\n', h.rstrip(), count=1) if h.rstrip().endswith('</script>') else h
assert 'bkOut").onclick' in h, 'app js not appended'
# head
h=h.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
h=('<!doctype html>\n<html lang="tr">\n<head>\n<meta charset="utf-8">\n'
   '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
   '<meta name="theme-color" content="#0d7a69">\n<meta name="description" content="Kompozit mühendisleri için İngilizce konuşma pratiği">\n'
   '<link rel="manifest" href="manifest.webmanifest">\n<link rel="icon" href="icons/icon-192.png">\n<link rel="apple-touch-icon" href="icons/icon-192.png">\n'
   '<meta name="apple-mobile-web-app-capable" content="yes">\n</head>\n<body>\n'+h+'\n</body>\n</html>\n')
# --- write app ---
os.makedirs(A,exist_ok=True)
open(A+'index.html','w').write(h)
for d in ['audio','tts','ort','vendor']:
    os.makedirs(A+d,exist_ok=True)
for f in os.listdir(S+'pub/audio'): shutil.copy(S+'pub/audio/'+f,A+'audio/'+f)
for f in ['phonemizer.js','voice.json','voice0.wasm','voice1.wasm']: shutil.copy(S+'pub/tts/'+f,A+'tts/'+f)
shutil.copy(S+'pub/ort/ort-wasm-simd.wasm',A+'ort/'); shutil.copy(S+'sdkt/anthropic-sdk.mjs',A+'vendor/'); shutil.copy(S+'npm/p3/package/dist/ort.min.js',A+'ort/')
json.dump({"name":"Laminate Talk","short_name":"Laminate Talk","description":"Kompozit mühendisleri için İngilizce konuşma pratiği",
  "lang":"tr","start_url":"./","scope":"./","display":"standalone","background_color":"#f2f4f3","theme_color":"#0d7a69",
  "icons":[{"src":"icons/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icons/icon-512.png","sizes":"512x512","type":"image/png"},
           {"src":"icons/icon-512-maskable.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]},open(A+'manifest.webmanifest','w'),ensure_ascii=False,indent=1)
ver=hashlib.sha1(h.encode()).hexdigest()[:10]
open(A+'sw.js','w').write(open(S+'build2/sw.template.js').read().replace('__VER__',ver))
print('app built',len(h),ver)
