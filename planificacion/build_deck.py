# -*- coding: utf-8 -*-
"""Genera presentacion-criso.html (deck de la primera clase)"""
import base64, os, sys, re, json, subprocess, html

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import contenido as C
import ilustra as IL
# El retrato ya recortado a 800×1000 vive en el proyecto: así generar.sh
# funciona en cualquier ordenador, no solo en el de Criso.
SRC = os.path.join(HERE, "recursos", "criso.jpg")

def foto():
    with open(SRC, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()

CSS = r"""
:root{
  --bg:#081422; --bg2:#0D1F33; --panel:#12293F; --panel2:#183551;
  --tx:#EAF3FA; --tx2:#B7CBDD; --mut:#7E9AB4; --line:#1E3B57;
  --aqua:#4FC9E8; --sand:#E5B98D; --mint:#7BD8A8; --lilac:#BBA6F7;
  --lvl:var(--aqua);
  --fd:"Bricolage Grotesque",Verdana,sans-serif;
  --fb:"Public Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  --fm:"JetBrains Mono",ui-monospace,Menlo,monospace;
}
[data-lvl="2do"]{--lvl:var(--mint)}
[data-lvl="3ro"]{--lvl:var(--lilac)}

/* Temas para proyectar. El oscuro se ve precioso en la pantalla del portátil y
   se lava en cuanto el proyector es viejo o entra sol por la ventana; en un
   aula a las ocho de la mañana el claro es el que se lee. Se cambia desde la
   propia diapositiva porque eso se descubre al proyectar, no antes.

   Van después de :root a propósito: al exportar a la app ese bloque se
   reescribe como `.pg`, misma especificidad, así que gana el que va después. */
[data-tema="claro"]{
  --bg:#F4F7FB; --bg2:#FFFFFF; --panel:#E9EFF6; --panel2:#DCE6F1;
  --tx:#0E1A2B; --tx2:#33455C; --mut:#5B6E86; --line:#C6D4E3;
  --aqua:#0A6F96; --mint:#0F7343; --lilac:#5628BC;
}
/* Para proyectar contra pared, no contra pantalla blanca.

   Lo intuitivo es teñir el fondo de frío para compensar el cálido del marrón.
   Medido, no sirve: proyectar multiplica la luz por el color de la pared, y
   multiplicar conserva la proporción entre fondo y texto. El tinte cambia el
   tono y no el contraste, y encima cuesta luz —una pared marrón refleja sobre
   todo el canal rojo, así que quitarle rojo al blanco es tirar brillo—.

   Lo que sí sube el contraste es el rango: blanco puro contra negro puro. En
   la simulación sobre marrón medio da 4,8:1 frente a los 4,2:1 del Claro. Los
   grises intermedios sí van fríos, que ahí no cuesta nada y evita que la
   pantalla se vea sucia. */
[data-tema="pared"]{
  --bg:#FFFFFF; --bg2:#FFFFFF; --panel:#E7EFF8; --panel2:#D5E3F1;
  --tx:#000000; --tx2:#0E1A26; --mut:#3C5568; --line:#9BB3C8;
  --aqua:#00435F; --mint:#04482B; --lilac:#2E1178;
}
*{box-sizing:border-box}
html,body{height:100%}
/* Las dos propiedades de abajo se heredan, así que valen para toda la
   diapositiva. JetBrains Mono junta == en una barra larga, >= en ≥ y != en ≠:
   precioso para quien ya programa, una trampa para quien está aprendiendo a
   distinguir el = que guarda del == que compara. */
body{margin:0;background:var(--bg);color:var(--tx);font-family:var(--fb);
  font-variant-ligatures:none;font-feature-settings:"liga" 0,"calt" 0;
  overflow:hidden;-webkit-font-smoothing:antialiased}
/* Los campos no heredan lo de arriba: el navegador les reinicia la fuente, y
   en el taller se escribía >= y se veía ≥. */
input,textarea,select,button{font-variant-ligatures:none;font-feature-settings:"liga" 0,"calt" 0}
h1,h2,h3{font-family:var(--fd);font-weight:700;line-height:1.04;margin:0;
  letter-spacing:-.028em;text-wrap:balance}
p{margin:0}

/* chrome */
.prog{position:fixed;top:0;left:0;height:3px;background:var(--lvl);z-index:60;
  width:0;transition:width .32s cubic-bezier(.4,0,.2,1)}
.chrome{position:fixed;z-index:50;display:flex;gap:8px;align-items:center}
.chrome.tr{top:20px;right:24px}
.chrome.br{bottom:20px;right:24px}
.chrome.bl{bottom:20px;left:24px}
.chrome.tl{top:20px;left:24px}
/* La salida. Sin esto, estando dentro de un deck solo se sale escribiendo la
   URL o dando atrás en el navegador. */
.volver{font-family:var(--fm);font-size:12px;letter-spacing:.06em;padding:6px 13px;
  color:var(--mut);border:1px solid var(--line);border-radius:999px;text-decoration:none;
  transition:color .16s,border-color .16s}
.volver:hover{color:var(--tx);border-color:var(--lvl)}
.volver:focus-visible{outline:2px solid var(--lvl);outline-offset:2px}
.lvlbtn{font-family:var(--fm);font-size:12px;letter-spacing:.06em;padding:6px 12px;
  background:transparent;color:var(--mut);border:1px solid var(--line);cursor:pointer;
  border-radius:999px;transition:color .16s,border-color .16s}
.lvlbtn:hover{color:var(--tx)}
.lvlbtn[aria-pressed="true"]{color:var(--bg);background:var(--lvl);border-color:var(--lvl);font-weight:600}
.lvlbtn:focus-visible{outline:2px solid var(--lvl);outline-offset:2px}
.tembtn{font-family:var(--fm);font-size:11px;letter-spacing:.06em;padding:5px 10px;
  background:transparent;color:var(--mut);border:1px solid var(--line);cursor:pointer;
  border-radius:999px;transition:color .16s,border-color .16s}
.tembtn:hover{color:var(--tx);border-color:var(--tx2)}
.tembtn[aria-pressed="true"]{color:var(--bg);background:var(--tx2);border-color:var(--tx2);
  font-weight:600}
.tembtn:focus-visible{outline:2px solid var(--lvl);outline-offset:2px}
/* Una raya fina entre los dos grupos: el curso y el color no son lo mismo y
   seis botones seguidos se leen como una sola fila de seis cosas iguales. */
.sep{width:1px;align-self:stretch;background:var(--line);margin:2px 4px}
.navb{width:38px;height:38px;display:grid;place-items:center;background:transparent;
  border:1px solid var(--line);color:var(--tx2);cursor:pointer;border-radius:999px;
  font-size:15px;line-height:1;transition:border-color .16s,color .16s}
.navb:hover{border-color:var(--lvl);color:var(--lvl)}
.navb:focus-visible{outline:2px solid var(--lvl);outline-offset:2px}
.count{font-family:var(--fm);font-size:12px;color:var(--mut);
  font-variant-numeric:tabular-nums;letter-spacing:.08em}

/* slides */
/* 100dvh y no 100%: al servirse como ruta de Next.js hay un contenedor de
   por medio, y una cadena de height:100% se rompe en cuanto un eslabón tiene
   altura automática. Con dvh la altura no depende de ningún ancestro. */
.deck{height:100dvh;position:relative}
.slide{position:absolute;inset:0;padding:76px clamp(24px,6vw,86px);
  display:none;align-content:center;opacity:0;overflow-y:auto;overscroll-behavior:contain}
.slide.on{display:grid;animation:in .42s cubic-bezier(.2,.7,.3,1) forwards}
@keyframes in{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.inner{width:100%;max-width:1180px;margin:0 auto}
.eyebrow{font-family:var(--fm);font-size:clamp(10px,1.1vw,12px);letter-spacing:.2em;
  text-transform:uppercase;color:var(--lvl);margin-bottom:20px}
.big{font-size:clamp(34px,6.4vw,80px)}
.mid{font-size:clamp(27px,4.4vw,52px)}
.say{margin-top:22px;font-size:clamp(16px,2vw,23px);color:var(--tx2);
  max-width:46ch;line-height:1.45}

/* 1 portada */
.hero{display:grid;gap:clamp(28px,4vw,64px);align-items:center;
  grid-template-columns:1fr}
@media(min-width:900px){.hero{grid-template-columns:1.15fr .85fr}}
.shot{position:relative;justify-self:center;width:100%;max-width:360px}
.shot img{display:block;width:100%;height:auto;border-radius:2px;
  filter:saturate(.94) contrast(1.03)}
.shot::after{content:"";position:absolute;inset:0;
  background:linear-gradient(180deg,rgba(8,20,34,0) 55%,rgba(8,20,34,.62) 100%);
  pointer-events:none;border-radius:2px}
.shot .frame{position:absolute;inset:-12px -12px 12px 12px;border:1px solid var(--lvl);
  opacity:.45;border-radius:2px;z-index:0}
.shot img{position:relative;z-index:1}
@media(max-width:899px){.shot{max-width:210px}.shot .frame{display:none}}
.sig{margin-top:26px;padding-top:18px;border-top:1px solid var(--line);
  font-family:var(--fm);font-size:clamp(11px,1.2vw,13px);color:var(--mut);
  letter-spacing:.05em}

/* listas */
.pts{list-style:none;margin:34px 0 0;padding:0;display:grid;gap:16px;max-width:62ch}
.pts li{display:grid;grid-template-columns:26px 1fr;gap:14px;align-items:start;
  font-size:clamp(15px,1.85vw,21px);color:var(--tx2);line-height:1.45}
.pts li::before{content:"";width:9px;height:9px;margin-top:.55em;
  background:var(--lvl);transform:rotate(45deg)}
.pts b{color:var(--tx);font-weight:600}

/* cadena */
.chain{display:flex;flex-wrap:wrap;gap:10px;margin-top:30px;align-items:center}
.chain span{font-family:var(--fd);font-weight:600;font-size:clamp(14px,2vw,23px);
  padding:9px 17px;border:1px solid var(--line);background:var(--bg2);border-radius:2px;
  transition:border-color .2s,color .2s,background .2s}
/* El resaltado lo pone el JS con una clase. Antes era `span:nth-child(5)`, que
   contaba también las flechas `<i>`: mover un eslabón desplazaba el color sin
   que nadie se enterara. */
.chain .esl.act{border-color:var(--lvl);color:var(--lvl);background:var(--panel)}
.chain .esl.hecho{color:var(--tx2);border-color:var(--tx2)}
.chain i{color:var(--mut);font-style:normal;font-size:clamp(13px,1.7vw,19px)}
.punch{margin-top:42px;font-family:var(--fd);font-weight:700;
  font-size:clamp(21px,3.4vw,40px);line-height:1.14;max-width:22ch;text-wrap:balance}
.punch em{font-style:normal;color:var(--lvl)}
.punch+.say{margin-top:14px}

/* reglas */
.rules{display:grid;gap:1px;background:var(--line);border:1px solid var(--line);
  margin-top:38px;grid-template-columns:1fr}
@media(min-width:880px){.rules{grid-template-columns:repeat(3,1fr)}}
.rule{background:var(--bg2);padding:clamp(18px,2.4vw,28px)}
.rule .n{font-family:var(--fm);font-size:13px;color:var(--lvl);font-weight:600;
  letter-spacing:.1em;display:block;margin-bottom:12px}
.rule h3{font-size:clamp(17px,2.1vw,24px);margin-bottom:10px}
.rule p{font-size:clamp(13.5px,1.4vw,16px);color:var(--tx2);line-height:1.5}

/* pasos */
.steps{display:grid;gap:1px;background:var(--line);border:1px solid var(--line);
  margin-top:36px;grid-template-columns:1fr}
@media(min-width:820px){.steps{grid-template-columns:repeat(3,1fr)}}
.step{background:var(--bg2);padding:clamp(16px,2.2vw,26px)}
.step .n{font-family:var(--fm);font-size:12px;letter-spacing:.14em;color:var(--mut);
  display:block;margin-bottom:11px}
.step h3{font-size:clamp(16px,1.9vw,22px);margin-bottom:8px;color:var(--lvl)}
.step p{font-size:clamp(13.5px,1.4vw,16px);color:var(--tx2);line-height:1.5}

/* evaluacion */
.bars{margin-top:28px;display:grid;gap:11px;max-width:760px}
/* El quiz de entrada no puntúa, así que no va entre las barras: va debajo,
   como lo que es, algo que se juega hoy y no cuenta para la nota. */
.quiz-fila{display:flex;gap:24px;align-items:center;flex-wrap:wrap;margin-top:22px}
.qr-caja{display:grid;gap:7px;justify-items:center}
/* La dirección del diagnóstico tiene tres veces más caracteres que la de
   kahoot.it, así que el código tiene un tercio más de módulos y cada uno sale
   más pequeño. Se compensa con tamaño: esto se escanea desde un pupitre. */
.qr{width:clamp(104px,12vw,156px);height:auto;display:block;border-radius:3px;
  background:#fff;padding:8px}
.qr-pie{font-family:var(--fm);font-size:clamp(10px,1.1vw,13px);color:var(--tx2);
  letter-spacing:.08em}
.quiz{display:inline-grid;gap:3px;padding:14px 20px;max-width:520px;
  background:var(--bg2);border:1px solid var(--line);border-left:3px solid var(--lvl);
  text-decoration:none;transition:border-color .16s,background .16s}
.quiz:hover{border-color:var(--lvl);background:var(--panel)}
.quiz:focus-visible{outline:2px solid var(--lvl);outline-offset:3px}
.quiz-k{font-family:var(--fm);font-size:clamp(10px,1.1vw,13px);letter-spacing:.16em;
  text-transform:uppercase;color:var(--lvl)}
.quiz-t{font-family:var(--fd);font-weight:700;font-size:clamp(19px,2.6vw,32px);
  color:var(--tx);line-height:1.1}
.quiz-p{font-size:clamp(13px,1.5vw,17px);color:var(--tx2);margin-top:4px}
.quiz-p b{color:var(--tx)}
/* Cada fila es un botón: se marca lo que ya se hizo y el total sube solo.
   Hereda tipografía y color porque un <button> trae los suyos. */
.bar{display:grid;grid-template-columns:1fr 52px;gap:14px;align-items:center;
  width:100%;border:0;background:transparent;color:inherit;font:inherit;
  text-align:left;cursor:pointer;padding:5px 8px;border-radius:5px;
  transition:background .16s}
.bar:hover{background:var(--bg2)}
.bar:focus-visible{outline:2px solid var(--lvl);outline-offset:2px}
.bar[aria-pressed="true"] .lab{color:var(--tx)}
.bar[aria-pressed="true"] .lab::before{content:"\2713\00a0";color:var(--lvl)}
.bar[aria-pressed="false"] .fill{opacity:.28}
.bar .lab{font-size:clamp(14px,1.6vw,18px);color:var(--tx2)}
.bar .pc{font-family:var(--fm);font-size:clamp(13px,1.5vw,17px);color:var(--lvl);
  text-align:right;font-variant-numeric:tabular-nums;font-weight:600}
.bar .track{grid-column:1/-1;height:5px;background:var(--panel);position:relative;
  border-radius:99px;overflow:hidden}
.bar .fill{position:absolute;inset:0 auto 0 0;background:var(--lvl);opacity:.85;
  border-radius:99px;width:0;transition:width .6s cubic-bezier(.3,.8,.4,1)}
.slide.on .bar .fill{width:var(--w)}

/* reto */
.card{margin-top:34px;border:1px solid var(--line);background:var(--bg2);
  border-left:3px solid var(--lvl);padding:clamp(20px,2.8vw,32px);max-width:70ch}
.card h3{font-size:clamp(20px,2.8vw,32px);margin-bottom:14px}
.card p{font-size:clamp(14.5px,1.7vw,19px);color:var(--tx2);line-height:1.5}
.card p+p{margin-top:12px}
.go{margin-top:40px;font-family:var(--fd);font-weight:700;
  font-size:clamp(30px,5.6vw,66px);color:var(--lvl);letter-spacing:-.03em}

/* lista de la clase */
.aviso{display:inline-block;margin-top:14px;font-family:var(--fm);font-size:11px;
  letter-spacing:.12em;text-transform:uppercase;color:var(--bg);background:var(--sand);
  padding:5px 11px;border-radius:999px;font-weight:600}
.roster{list-style:none;margin:30px 0 0;padding:0;display:grid;gap:8px;
  grid-template-columns:repeat(auto-fill,minmax(190px,1fr));max-height:52vh;overflow:auto}
.roster li{display:grid;grid-template-columns:26px 1fr;gap:10px;align-items:baseline;
  padding:9px 13px;background:var(--bg2);border:1px solid var(--line);border-radius:3px;
  font-size:clamp(13px,1.5vw,17px)}
.roster b{font-family:var(--fm);font-size:11px;color:var(--lvl);font-weight:600;
  font-variant-numeric:tabular-nums}
.conteo{margin-top:18px;font-family:var(--fm);font-size:clamp(11px,1.2vw,13px);
  color:var(--mut);letter-spacing:.08em}

[data-only]{display:none}
.hint{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);z-index:50;
  font-family:var(--fm);font-size:11px;color:var(--mut);letter-spacing:.08em;
  opacity:.7;pointer-events:none}
/* En un teléfono la fila de arriba son seis botones —tres cursos y tres
   colores— y se salía por la derecha. Se deja envolver y se encoge; el ancho
   tope evita que invada el enlace de vuelta, que vive en la otra esquina. */
@media(max-width:760px){.hint{display:none}.chrome.bl{left:16px}.chrome.br{right:16px}
  .chrome.tr{top:12px;right:12px;flex-wrap:wrap;justify-content:flex-end;
    max-width:calc(100vw - 150px);gap:5px}
  .chrome.tl{top:12px;left:12px}
  .chrome.tr .sep{display:none}
  .lvlbtn{padding:5px 9px;font-size:11px}
  .tembtn{padding:4px 8px;font-size:10px}
  .slide{padding:66px 20px 84px}}
@media(prefers-reduced-motion:reduce){
  .slide.on{animation:none;opacity:1}
  .prog,.bar .fill{transition:none}
}
"""

JS = r"""
var S=[].slice.call(document.querySelectorAll('.slide')),i=0;
var prog=document.getElementById('prog'),cnt=document.getElementById('cnt');
function show(n){
  i=Math.max(0,Math.min(S.length-1,n));
  S.forEach(function(s,k){s.classList.toggle('on',k===i);});
  prog.style.width=((i+1)/S.length*100)+'%';
  cnt.textContent=String(i+1).padStart(2,'0')+' / '+String(S.length).padStart(2,'0');
}
/* Se puede llegar a una diapositiva concreta: #d7 o #practica, que es lo que
   usa el botón «Volver a la clase» del pen. */
function desdeHash(){
  var h=(location.hash||'').replace('#','');
  if(/^d\d+$/.test(h))return parseInt(h.slice(1),10)-1;
  if(h==='practica'){
    for(var k=0;k<S.length;k++)if(S[k].querySelector('[data-act=pen],[data-act=editor]'))return k;
  }
  return 0;
}
document.getElementById('prev').onclick=function(){show(i-1);};
document.getElementById('next').onclick=function(){show(i+1);};
document.addEventListener('keydown',function(e){
  if(e.target.tagName==='BUTTON'&&e.key===' ')return;
  /* Desde que hay campos de texto dentro de las diapositivas, escribir un
     espacio o mover el cursor no puede pasar de diapositiva. */
  var t=e.target.tagName;
  if(t==='INPUT'||t==='TEXTAREA'||t==='SELECT'||e.target.isContentEditable)return;
  if(['ArrowRight','PageDown',' '].indexOf(e.key)>-1){e.preventDefault();show(i+1);}
  else if(['ArrowLeft','PageUp'].indexOf(e.key)>-1){e.preventDefault();show(i-1);}
  else if(e.key==='Home'){show(0);} else if(e.key==='End'){show(S.length-1);}
},{signal:typeof senal!=='undefined'?senal:undefined});
function setTema(t){
  document.documentElement.setAttribute('data-tema',t);
  // Y en el envoltorio de la app, por lo mismo que setLvl: dentro de Next el
  // `:root` del deck es `.pg`, y si el tema solo va en <html> queda por debajo.
  var pg=document.querySelector('.pg');
  if(pg)pg.setAttribute('data-tema',t);
  document.querySelectorAll('.tembtn').forEach(function(b){
    b.setAttribute('aria-pressed',String(b.dataset.tema===t));
  });
  try{localStorage.setItem('deck-tema',t);}catch(e){}
}
document.querySelectorAll('.tembtn').forEach(function(b){
  b.onclick=function(){setTema(b.dataset.tema);};
});
var temas=[].map.call(document.querySelectorAll('.tembtn'),function(b){return b.dataset.tema;});
var tema='';
try{tema=localStorage.getItem('deck-tema')||'';}catch(e){}
if(temas.indexOf(tema)<0)tema=temas[0]||'oscuro';
setTema(tema);

function setLvl(l){
  document.documentElement.setAttribute('data-lvl',l);
  // Y en el envoltorio de la app. Al exportar, el `:root` del deck se reescribe
  // como `.pg`, que vuelve a fijar --lvl y tapa el color del nivel: el botón se
  // pintaba del color del curso y las barras seguían en cian. Puesto en el
  // mismo elemento gana la regla del nivel, que va después en la hoja.
  var pg=document.querySelector('.pg');
  if(pg)pg.setAttribute('data-lvl',l);
  document.querySelectorAll('[data-only]').forEach(function(el){
    el.style.display=(el.dataset.only===l)?'block':'none';
  });
  document.querySelectorAll('.lvlbtn').forEach(function(b){
    b.setAttribute('aria-pressed',String(b.dataset.lvl===l));
  });
  try{localStorage.setItem('deck-lvl',l);}catch(e){}
  // Para la app: el panel del docente escucha el cambio de curso. Va después
  // del corte `function setLvl`, así que los decks de taller y curso no lo llevan.
  try{window.dispatchEvent(new CustomEvent('deck:nivel',{detail:l}));}catch(e){}
}
document.querySelectorAll('.lvlbtn').forEach(function(b){
  b.onclick=function(){setLvl(b.dataset.lvl);};
});
var saved='1ro';
try{saved=localStorage.getItem('deck-lvl')||'1ro';}catch(e){}
if(['1ro','2do','3ro'].indexOf(saved)<0)saved='1ro';
setLvl(saved);show(desdeHash());
"""


# ─────────────────────────────────────────────────────────────────────────
#  La lista de la clase
#
#  Se lee de `listas/1ro.csv`, `listas/2do.csv`, `listas/3ro.csv`: un nombre
#  por línea. Mientras no existan, se muestran nombres de ejemplo CON UN
#  AVISO VISIBLE. Proyectar nombres inventados delante del grupo sin que se
#  note que son de relleno sería peor que no tener la diapositiva.
# ─────────────────────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════
#  Aquí vivía `cargar_lista()`, que leía `listas/*.csv` y horneaba los nombres
#  en el HTML. Con nombres de ejemplo daba igual; con 256 menores, no: esta
#  presentación se publica en internet.
#
#  Ahora la diapositiva deja un hueco y los nombres solo los pinta el panel del
#  docente, que los pide con su sesión. Así no hay manera de que un nombre real
#  acabe en la página pública por descuido, ni hoy ni dentro de seis meses.
# ═══════════════════════════════════════════════════════════════════════

# El cuarto campo de cada paso es la demo que lo acompaña. Antes esta
# diapositiva llevaba un dibujo a la derecha: se le decía a un grupo de doce
# años «vas a hacer que un personaje se mueva arrastrando piezas» enseñándole
# el dibujo de unas piezas. Ahora las mueven ellos.
CONSTRUIR = {
 "1ro": ("Tus propios juegos, en Python.",
   [("Primero", "Instrucciones", "Antes de escribir, piensas como programador: pasos en orden, repetir y decidir. Cada pieza es una orden y el personaje hace exactamente lo que dice.", "bloques"),
    ("Después", "Python", "Escribes esas mismas órdenes en Python, el lenguaje con el que empieza casi todo el mundo. Variables, decisiones y repeticiones.", "codigo"),
    ("Al final", "Tu juego", "Lo juntas todo en un juego tuyo: dados, puntos, preguntas y alguien que gana.", "dado")],
   "En diciembre vas a poder abrir tu juego en el celular de tu casa y retar a quien quieras."),
 "2do": ("Tu sitio web, con Python y con IA.",
   [("Primero", "La página", "HTML y CSS: la estructura y el diseño. Tu sitio, con tu nombre y tus colores, hecho por ti.", "pagina"),
    ("Después", "Python", "Variables, decisiones y repeticiones en Python. Botones que responden y una página que cambia cuando la tocas.", "codigo"),
    ("Al final", "Inteligencia artificial", "Entrenas tu propio modelo con la cámara, sin código, y tu programa en Python decide qué hacer con lo que ve.", "ia")],
   "Vas a terminar con un sitio web tuyo que responde a lo que haces y reconoce lo que le enseñaste."),
 "3ro": ("Datos, Python e IA para un problema real.",
   [("Primero", "Los datos", "Guardar información en Python, buscarla, filtrarla y que no se pierda al cerrar la página.", "datos"),
    ("Después", "Python e IA", "Formularios que Python revisa mientras escribes y un modelo de IA entrenado por ti, en una página que se ve bien también en el celular.", "formulario"),
    ("Al final", "El proyecto", "Eliges un problema de esta escuela y lo resuelves con datos, Python e IA: lo construyes, lo pruebas y lo presentas.", "app")],
   "El año cierra con una feria: tu proyecto expuesto, funcionando, y gente probándolo delante de ti."),
}

# La escena de ilustra.py del reto. «Qué vas a construir» ya no lleva dibujo:
# lleva demos, y el hueco de la derecha desapareció con él.
ESCENA_RETO = {"1ro": "robot", "2do": "periodico", "3ro": "periodico"}

RETO = {
 "1ro": ("Programa a un humano",
   ["Uno de ustedes va a ser el robot. Solo obedece cuatro órdenes: AVANZA, GIRA IZQUIERDA, GIRA DERECHA y REPITE.",
    "En parejas van a escribir las instrucciones para llegar a la meta. Máximo diez. El robot obedece exactamente lo que dice la tarjeta, no lo que ustedes querían decir."]),
 "2do": ("Hackea el periódico",
   ["Abran un periódico digital y presionen F12. Van a ver el código de la página, tal como lo escribió alguien.",
    "Vamos a cambiar el titular y el color del fondo, y les enseño la tercera capa: un botón que responde en Python. Después les explico por qué el periódico no cambió para nadie más."]),
 "3ro": ("Hackea el periódico · y después, ¿qué app harías?",
   ["Primero abrimos un periódico con F12 y le cambiamos el titular en diez minutos.",
    "Después, en equipos: escriban tres problemas reales de esta escuela que se podrían resolver con una aplicación. Esa lista no se borra: de ahí van a salir sus proyectos finales."]),
}


def juegos_de(nivel):
    """Los juegos de reserva de la primera clase de un curso, si ya existen en
    contenido.py. Lista vacía si el curso no tiene: entonces no se pinta nada."""
    for d in C.SEMANA1_DINAMICAS:
        if d["nivel"].lower() == nivel.lower():
            return d.get("juegos", []) or []
    return []


EVAL = [("Retos prácticos de cada semana",30),("Ejercicios y programas",20),
        ("Proyecto final",25),("Participación y trabajo en clase",15),
        ("Presentar y explicar lo que hiciste",10)]




# Paginación de dos niveles. Arriba los capítulos: dónde estoy. Abajo los
# pasos de este capítulo: cuánto me queda. Con cincuenta y ocho diapositivas,
# una barra de progreso dice muy poco y el contador «34 / 58» todavía menos.
#
# Vive aquí y no en build_taller porque la usan los tres generadores de deck, y
# de aquí ya importan CSS y JS. Los capítulos son opcionales: sin ellos queda
# una sola fila de puntos, que es lo que necesita un deck de seis diapositivas.
# El ejemplo a la derecha y el movimiento. Solo lo carga esta presentación: los
# otros sesenta y cinco decks importan CSS pero no esto, y una diapositiva de
# taller con seis viñetas no gana nada entrando escalonada.
CSS_MOV = """
.conej{display:grid;gap:clamp(22px,3.4vw,52px);align-items:center;grid-template-columns:1fr}
@media(min-width:900px){.conej{grid-template-columns:1.05fr .95fr}}
/* El panel va en el CSS y no dentro del SVG: así los rellenos del dibujo se
   pueden animar sin que el fondo entero parpadee con ellos. */
.esc{background:#F3F7FB;border-radius:6px;padding:clamp(10px,1.6vw,20px);
  justify-self:center;width:100%;max-width:560px}
/* Sobre fondo claro el panel desaparecía contra la diapositiva. */
[data-tema="claro"] .esc,[data-tema="pared"] .esc{background:#fff;border:1px solid var(--line)}
.esc svg{display:block;width:100%;height:auto}
.mstr-caja{display:grid;gap:10px;justify-items:center}
/* El vídeo es vertical, así que manda el alto: por ancho se comería la
   diapositiva entera. */
.mstr{display:block;max-height:min(56vh,470px);width:auto;max-width:100%;
  border-radius:8px;box-shadow:0 18px 50px -24px rgba(0,0,0,.75)}
.mstr-pie{font-family:var(--fm);font-size:clamp(10px,1.1vw,13px);letter-spacing:.06em;
  color:var(--mut);text-align:center;max-width:30ch}
@media(max-width:899px){.esc{max-width:380px}}

/* Entradas escalonadas. La diapositiva entera ya aparecía de golpe; ahora sus
   piezas llegan una detrás de otra, que es lo que da sensación de que algo
   pasa al avanzar. */
@keyframes sube{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
.slide.on .inner>*{animation:sube .5s cubic-bezier(.2,.7,.3,1) both}
.slide.on .inner>*:nth-child(1){animation-delay:.04s}
.slide.on .inner>*:nth-child(2){animation-delay:.13s}
.slide.on .inner>*:nth-child(3){animation-delay:.22s}
.slide.on .inner>*:nth-child(4){animation-delay:.31s}
.slide.on .inner>*:nth-child(5){animation-delay:.40s}
.slide.on .inner>*:nth-child(n+6){animation-delay:.48s}
/* Red de seguridad: la animación empieza en opacity:0 y, si el navegador se
   traba justo al entrar —Safari con algo pesado cargando—, lo que queda es
   media diapositiva invisible. Pasado un segundo largo, el JS marca la
   diapositiva y la animación se apaga: lo que haya, se ve. */
.slide.on.a-ya .inner>*,.slide.on.a-ya .steps>*,.slide.on.a-ya .rules>*,
.slide.on.a-ya .bar{animation:none}
.slide.on .steps>*,.slide.on .rules>*,.slide.on .bar{animation:sube .5s cubic-bezier(.2,.7,.3,1) both}
.slide.on .steps>*:nth-child(2),.slide.on .rules>*:nth-child(2),
.slide.on .bar:nth-child(2){animation-delay:.10s}
.slide.on .steps>*:nth-child(3),.slide.on .rules>*:nth-child(3),
.slide.on .bar:nth-child(3){animation-delay:.20s}
.slide.on .bar:nth-child(4){animation-delay:.30s}
.slide.on .bar:nth-child(5){animation-delay:.40s}

/* El dibujo se traza solo. `ruta()` emite stroke como atributo, así que
   [stroke] los alcanza a todos sin tocar ilustra.py. Los rellenos entran por
   detrás con fill-opacity y no con opacity: opacity apagaría también el trazo
   que se está dibujando encima. */
@keyframes trazo{from{stroke-dashoffset:2600}}
@keyframes rellena{from{fill-opacity:0}}
.slide.on .esc [stroke]{stroke-dasharray:2600;animation:trazo 1.05s ease-out}
.slide.on .esc [fill]:not([fill="none"]){animation:rellena .8s ease-out}
/* Casi toda caja tiene contorno Y relleno, así que le tocan las dos reglas de
   arriba; y como `animation` es abreviada, la segunda borraba la primera y el
   trazo no llegaba a dibujarse nunca. Aquí van juntas, y esta regla gana por
   tener un selector más específico. */
.slide.on .esc [stroke][fill]:not([fill="none"]){
  animation:trazo 1.05s ease-out,rellena .8s ease-out}

/* Va al final de todo a propósito: este bloque tiene que ganarle a las reglas
   de arriba, y el que trae CSS queda antes en la hoja. */
@media(prefers-reduced-motion:reduce){
  .slide.on .inner>*,.slide.on .steps>*,.slide.on .rules>*,.slide.on .bar,
  .slide.on .esc [stroke],.slide.on .esc [fill]:not([fill="none"]),
  .slide.on .esc [stroke][fill]:not([fill="none"]){animation:none}
  .slide.on .esc [stroke]{stroke-dasharray:none}
}
"""


# ═══════════════════════════════════════════════════════════════════════
#  CSS_JUEGO — lo que se toca
#
#  Hasta aquí, dentro de una diapositiva no había un solo botón: todo lo
#  pulsable vivía en el chrome. A un grupo de doce años se le decía «vas a
#  hacer que un personaje se mueva arrastrando piezas» enseñándole el dibujo
#  de unas piezas.
#
#  Va DESPUÉS de CSS_MOV y lleva su propio bloque de movimiento reducido al
#  final. `@media(prefers-reduced-motion)` no añade especificidad: solo gana
#  por posición, así que un bloque que quedara antes de estas reglas no las
#  apagaría. Es un error que ya se cometió una vez en este archivo.
# ═══════════════════════════════════════════════════════════════════════

CSS_JUEGO = """
/* ─── las tres tarjetas de «qué vas a construir» ─── */
.cons{display:grid;gap:16px;margin-top:26px}
@media(min-width:980px){.cons{grid-template-columns:repeat(3,1fr);gap:14px}}
.tarj{display:flex;flex-direction:column;gap:9px;padding:15px 15px 16px;
  background:var(--bg2);border:1px solid var(--line);border-top:3px solid var(--lvl)}
.tarj .n{font-family:var(--fm);font-size:clamp(9px,1vw,11px);letter-spacing:.18em;
  color:var(--lvl)}
.tarj h3{font-family:var(--fd);font-weight:700;font-size:clamp(17px,2.1vw,25px);
  line-height:1.08;margin:0}
.tarj p{font-size:clamp(12px,1.25vw,15px);color:var(--tx2);line-height:1.42;margin:0}
.demo{margin-top:auto;padding-top:11px;border-top:1px dashed var(--line)}
.pista{font-family:var(--fm);font-size:clamp(9px,1vw,11px);letter-spacing:.1em;
  color:var(--mut);margin:0 0 7px}

/* ─── bloques (Scratch) ─── */
.bq-prog{min-height:64px;display:flex;flex-direction:column;gap:0;padding:5px;
  background:var(--panel);border:1px dashed var(--line);border-radius:4px}
.bq-vacio{font-size:11.5px;color:var(--mut);padding:14px 6px;text-align:center}
.bq-banco{display:flex;flex-wrap:wrap;gap:5px;margin-top:8px}
.bq{position:relative;border:0;background:transparent;padding:0;cursor:pointer;
  width:108px;height:33px;flex:0 0 auto}
.bq:disabled{cursor:default;opacity:.32}
.bq:focus-visible{outline:2px solid var(--lvl);outline-offset:2px}
.bq svg{position:absolute;inset:0;width:100%;height:100%;display:block}
.bq svg path{fill:var(--lvl);stroke:none;transition:filter .16s}
.bq:hover:not(:disabled) svg path{filter:brightness(1.18)}
.bq b{position:relative;display:block;line-height:27px;font-family:var(--fm);
  font-size:11px;font-weight:600;color:#fff;pointer-events:none;letter-spacing:.02em}
.bq-prog .bq{margin-bottom:-6px;cursor:default}
.bq-mundo{display:flex;align-items:center;gap:12px;
  margin-top:9px;padding:7px 9px;background:var(--panel);border:1px solid var(--line)}
.bq-mark{padding-left:12px;border-left:1px solid var(--line)}
.bq-piso{position:relative;flex:1;height:26px}
.bq-per{position:absolute;bottom:0;left:0;font-size:18px;line-height:1;
  transition:left .3s cubic-bezier(.3,1.4,.5,1),transform .25s}
.bq-meta{position:absolute;bottom:0;right:0;font-size:16px;color:var(--lvl)}
.bq-mark{font-family:var(--fm);font-size:11.5px;color:var(--tx2);margin:0;white-space:nowrap}
.bq-mark b{color:var(--lvl);font-size:15px}
.ok{font-family:var(--fm);font-size:11px;color:var(--lvl);margin:7px 0 0;min-height:14px}

/* ─── tu página ─── */
.pg-fila{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.campo{flex:1;min-width:110px;padding:7px 9px;font:inherit;font-size:13px;
  background:var(--panel);border:1px solid var(--line);color:var(--tx);border-radius:4px}
.campo:focus-visible{outline:2px solid var(--lvl);outline-offset:1px}
.pg-cols{display:flex;gap:5px}
.pg-col{width:21px;height:21px;border-radius:99px;border:2px solid transparent;
  background:var(--c);cursor:pointer;padding:0}
.pg-col[aria-pressed="true"]{border-color:var(--tx)}
.pg-col:focus-visible{outline:2px solid var(--lvl);outline-offset:2px}
.pg-vista{margin-top:9px;background:#fff;border:1px solid var(--line);border-radius:4px;
  overflow:hidden}
.pg-barra{display:flex;gap:4px;padding:6px 8px;background:#E7EAF0}
.pg-barra i{width:7px;height:7px;border-radius:99px;background:#B8C0CE}
.pg-cuerpo{padding:11px 12px 14px}
.pg-cuerpo h4{margin:0;font-family:var(--fd);font-weight:800;color:var(--c);
  font-size:clamp(15px,1.9vw,21px);line-height:1.1;word-break:break-word}
.pg-cuerpo p{margin:3px 0 0;font-size:11.5px;color:#5A6474}
.pg-btn{display:inline-block;margin-top:9px;padding:5px 12px;border-radius:99px;
  background:var(--c);color:#fff;font-size:11px;font-family:var(--fm)}

/* ─── una línea de código ─── */
.cd-caja{background:#0B1020;border:1px solid var(--line);border-radius:4px;
  padding:10px 11px;font-family:var(--fm);font-size:12px;line-height:1.6;color:#D7DEEC}
.cd-caja .k{color:#7DD3FC}
.cd-caja .v{color:#FDBA74}
.btn{border:1px solid var(--lvl);background:var(--lvl);color:#fff;font:inherit;
  font-size:12.5px;font-weight:600;padding:7px 13px;border-radius:4px;cursor:pointer;
  transition:filter .16s}
.btn:hover:not(:disabled){filter:brightness(1.12)}
.btn:disabled{opacity:.4;cursor:default}
.btn:focus-visible{outline:2px solid var(--lvl);outline-offset:2px}
.btn2{background:transparent;color:var(--tx2);border-color:var(--line)}
.cd-fila{display:flex;gap:9px;align-items:center;margin-top:9px;flex-wrap:wrap}
.cd-out{font-family:var(--fm);font-size:12px;color:var(--tx2)}
.cd-out b{color:var(--lvl);font-size:16px}

/* ─── el dado: una línea de Python y el azar ─── */
.dd-cara{display:grid;place-items:center;width:38px;height:38px;border-radius:7px;
  background:var(--panel);border:1px solid var(--lvl);color:var(--lvl);
  font-family:var(--fd);font-weight:800;font-size:21px;line-height:1;
  font-variant-numeric:tabular-nums}
@keyframes rueda{from{transform:rotate(-160deg) scale(.6)}to{transform:none}}
.dd-cara.tira{animation:rueda .38s cubic-bezier(.3,1.4,.5,1)}

/* ─── IA: así responde un modelo (simulado) ─── */
.ia-ejs{display:flex;gap:6px}
.ia-ej{flex:1;font-size:22px;line-height:1;padding:7px 0;background:var(--panel);
  border:1px solid var(--line);border-radius:4px;cursor:pointer;transition:border-color .16s}
.ia-ej:hover{border-color:var(--tx2)}
.ia-ej[aria-pressed="true"]{border-color:var(--lvl);box-shadow:inset 0 0 0 1px var(--lvl)}
.ia-ej:focus-visible{outline:2px solid var(--lvl);outline-offset:2px}
.ia-res{margin:9px 0;display:grid;gap:5px}
.ia-fila{display:grid;grid-template-columns:60px 1fr 34px;gap:7px;align-items:center;
  font-family:var(--fm);font-size:11px;color:var(--mut)}
.ia-fila.gana{color:var(--tx)}
.ia-pista{height:6px;background:var(--panel);border-radius:99px;overflow:hidden}
.ia-lleno{display:block;height:100%;width:0;background:var(--lvl);opacity:.4;border-radius:99px;
  transition:width .5s cubic-bezier(.3,.8,.4,1)}
.ia-fila.gana .ia-lleno{opacity:1}
.ia-pc{text-align:right;font-variant-numeric:tabular-nums}

/* ─── lista, buscador, formulario ─── */
.ls{list-style:none;margin:8px 0 0;padding:0;max-height:118px;overflow-y:auto;
  display:grid;gap:2px}
.ls li{display:flex;justify-content:space-between;gap:8px;align-items:center;
  padding:4px 8px;background:var(--panel);font-size:12px;border-radius:3px}
.ls li span{color:var(--mut);font-family:var(--fm);font-size:10px}
.ls .quitar{border:0;background:transparent;color:var(--mut);cursor:pointer;
  font-size:14px;line-height:1;padding:0 2px}
.pie-n{font-family:var(--fm);font-size:11px;color:var(--tx2);margin:7px 0 0}
.pie-n b{color:var(--lvl)}
.fm-msg{font-family:var(--fm);font-size:11px;margin:7px 0 0;min-height:14px}
.mal{color:#F4A4A4}
.bien{color:#7CD9A6}
.campo.mal{border-color:#F4A4A4}
.campo.bien{border-color:#7CD9A6}

/* ─── Snake ───
   Rejilla y no <canvas>: los colores salen de las variables del tema, así que
   funciona igual en oscuro, claro y pared sin repintar nada al cambiarlo, y no
   hay que pelearse con la densidad de pantalla del proyector. */
.juego{margin-top:16px;display:grid;gap:18px;align-items:start;
  padding:14px;background:var(--bg2);border:1px solid var(--line);max-width:880px}
/* El juego a la derecha, el marcador a la izquierda. El orden va en el markup
   y no con `order`: con `order` lo que se lee y lo que se tabula quedarían al
   revés de lo que se ve. */
@media(min-width:820px){.juego{grid-template-columns:minmax(170px,250px) minmax(0,1fr)}}

/* Manda el ANCHO, y el alto lo dan las celdas, que son cuadradas.
   Antes era al revés —alto definido y ancho deducido de la proporción— dentro
   de una columna `auto`. Como las 187 celdas son <i> vacíos, el contenido mide
   cero: Chrome deducía el ancho de la proporción y WebKit dejaba la columna en
   cero, así que en Safari el tablero no se veía. Se proyecta desde Safari. */
.jg-tablero{display:grid;gap:1px;background:var(--line);border:1px solid var(--line);
  grid-template-columns:repeat(var(--c),1fr);
  width:100%;max-width:520px;justify-self:end;touch-action:none}
.jg-tablero i{background:var(--panel);display:block;aspect-ratio:1}
.jg-tablero i.cue{background:var(--lvl);opacity:.55}
.jg-tablero i.cab{background:var(--lvl);opacity:1}
.jg-tablero i.man{background:var(--sand);border-radius:99px}
.jg-lado{display:grid;gap:10px;align-content:start}
.jg-marca{font-family:var(--fm);font-size:13px;color:var(--tx2);margin:0}
.jg-marca b{color:var(--lvl);font-size:23px;font-variant-numeric:tabular-nums}
.jg-rec{display:block;font-size:11px;color:var(--mut);margin-top:2px;min-height:14px}
.ci-msg{font-family:var(--fm);font-size:clamp(11px,1.3vw,14px);margin:0;min-height:34px;
  line-height:1.45}
.ci-btns{display:flex;gap:9px;flex-wrap:wrap}

/* ─── evaluación: el total y el vídeo ─── */
.ev-total{font-family:var(--fd);font-weight:700;margin:16px 0 0;
  font-size:clamp(19px,2.6vw,30px);line-height:1.1}
.ev-total b{color:var(--lvl);font-variant-numeric:tabular-nums}
.ev-pista{font-family:var(--fm);font-size:clamp(10px,1.1vw,12px);color:var(--mut);
  letter-spacing:.08em;margin:22px 0 -14px}
.vid-caja{display:grid;gap:9px;align-content:start}
.vid{position:relative;display:block;width:100%;padding:0;border:1px solid var(--line);
  background:#0B1020;cursor:pointer;overflow:hidden;border-radius:6px;aspect-ratio:16/9}
.vid:hover .vid-play{transform:scale(1.09)}
.vid:focus-visible{outline:2px solid var(--lvl);outline-offset:3px}
.vid-mini{width:100%;height:100%;object-fit:cover;display:block;opacity:.62}
.vid-play{position:absolute;inset:0;margin:auto;width:56px;height:56px;border-radius:99px;
  background:var(--lvl);color:#fff;display:grid;place-items:center;font-size:21px;
  transition:transform .2s;box-shadow:0 8px 26px -8px rgba(0,0,0,.8)}
.vid-tit{position:absolute;left:0;right:0;bottom:0;padding:9px 11px;text-align:left;
  font-family:var(--fm);font-size:11.5px;color:#fff;
  background:linear-gradient(transparent,rgba(0,0,0,.82))}
.vid-marco{width:100%;aspect-ratio:16/9;border:1px solid var(--line);border-radius:6px}
.vid-pie{font-family:var(--fm);font-size:clamp(10px,1.1vw,12px);color:var(--mut);
  margin:0;text-align:center}

/* Estas tres diapositivas son más altas que un teléfono, así que el contenido
   pasa por debajo del chrome fijo y antes se leía a través de él: el título
   del curso encima del texto de una tarjeta. Dos bandas sólidas lo resuelven,
   y de paso arreglan la lista de clase, que ya era larga. Van por debajo del
   chrome (z-index 45 contra 50) y no capturan el ratón. */
@media(max-width:899px){
  .deck::before,.deck::after{content:"";position:fixed;left:0;right:0;height:118px;
    z-index:45;pointer-events:none}
  .deck::before{top:0;background:linear-gradient(var(--bg) 64%,transparent)}
  .deck::after{bottom:0;height:96px;
    background:linear-gradient(transparent,var(--bg) 42%)}
}

/* Los temas claros: las cajas de demo necesitan su propio contraste. */
[data-tema="claro"] .pg-barra,[data-tema="pared"] .pg-barra{background:#DFE4EC}

/* ─── el bloqueo del docente ───
   Lo enciende el panel poniendo `data-bloqueo` en el elemento raíz. Va aquí y
   no en el componente de React porque lo que hay que apagar son las demos y el
   juego, que viven en esta hoja. */
[data-bloqueo="juegos"] .demo,[data-bloqueo="juegos"] .juego{
  pointer-events:none;opacity:.38;filter:saturate(.3)}
[data-bloqueo="juegos"] .cons::after,[data-bloqueo="juegos"] .chain::after{
  content:"Ahora estamos explicando";display:block;margin-top:12px;
  font-family:var(--fm);font-size:clamp(11px,1.3vw,14px);color:var(--lvl);
  letter-spacing:.06em}

/* El hueco de la lista, que llena el panel del docente. */
.roster-caja{min-height:60px}

/* Va al final de esta hoja a propósito, por lo mismo que en CSS_MOV. */
@media(prefers-reduced-motion:reduce){
  .bq-per,.vid-play,.bar,.chain span,.bq svg path,
  .pg-vista,.campo,.ia-lleno,.ia-ej{transition:none}
  .dd-cara.tira{animation:none}
}
"""

CSS_PAG = """
/* Paginación de dos niveles, abajo del todo. Discreta: en clase se mira el
   avión, no el índice, pero tiene que estar ahí cuando alguien pregunte
   «¿puedes volver al del candado?». */
.paginacion{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:55;
  display:grid;gap:7px;justify-items:center;max-width:min(94vw,760px)}
.caps{display:flex;gap:5px;flex-wrap:wrap;justify-content:center}
.caps[hidden]{display:none}
.cap{font-family:var(--fm);font-size:11px;letter-spacing:.04em;padding:4px 10px;
  background:transparent;color:var(--mut);border:1px solid var(--line);border-radius:999px;
  cursor:pointer;transition:color .16s,border-color .16s,background .16s;white-space:nowrap}
.cap:hover{color:var(--tx);border-color:var(--lvl)}
.cap[aria-current="true"]{color:var(--bg);background:var(--lvl);border-color:var(--lvl);
  font-weight:600}
.cap:focus-visible,.pas:focus-visible{outline:2px solid var(--lvl);outline-offset:2px}
.pass{display:flex;gap:6px;align-items:center;min-height:12px}
.pas{width:7px;height:7px;padding:0;border-radius:999px;cursor:pointer;
  background:var(--line);border:0;transition:background .16s,transform .16s}
.pas:hover{background:var(--mut)}
.pas[aria-current="true"]{background:var(--lvl);transform:scale(1.5)}
@media(max-width:700px){.cap{font-size:10px;padding:3px 8px}}
"""

JS_PAG = """
var CAPS=%s;
var cajaCap=document.getElementById('caps'),cajaPas=document.getElementById('pass');
// En desarrollo React ejecuta este script dos veces (monta, desmonta, monta).
// Los escuchadores se van con la señal de aborto, pero los botones ya creados
// se quedaban en el DOM y la paginación salía duplicada. Se empieza de cero.
cajaCap.innerHTML='';cajaPas.innerHTML='';delete cajaPas.dataset.k;
// Un deck de seis diapositivas no tiene capítulos que valga la pena separar:
// se trata como uno solo y queda la fila de puntos, que es toda la paginación
// que necesita. El mismo código sirve para seis que para cincuenta y ocho.
if(!CAPS.length){CAPS=[{t:'',a:0,b:S.length-1,tecla:null}];cajaCap.hidden=true;}
function capDe(n){for(var k=0;k<CAPS.length;k++){if(n>=CAPS[k].a&&n<=CAPS[k].b)return k;}return 0;}

CAPS.forEach(function(c,k){
  var b=document.createElement('button');
  b.className='cap';b.textContent=c.t;b.dataset.k=k;
  b.title=c.tecla?('Tecla '+c.tecla):c.t;
  b.onclick=function(){show(c.a);};
  cajaCap.appendChild(b);
});

function pintarPag(){
  var k=capDe(i),c=CAPS[k],total=c.b-c.a+1;
  [].forEach.call(cajaCap.children,function(b,j){
    b.setAttribute('aria-current',String(j===k));
  });
  if(cajaPas.dataset.k!==String(k)){
    cajaPas.dataset.k=String(k);
    cajaPas.innerHTML='';
    for(var p=0;p<total;p++){
      var d=document.createElement('button');
      d.className='pas';d.dataset.p=String(p);
      d.setAttribute('aria-label','Paso '+(p+1)+' de '+total);
      d.onclick=(function(x){return function(){show(c.a+x);};})(p);
      cajaPas.appendChild(d);
    }
  }
  [].forEach.call(cajaPas.children,function(d,j){
    d.setAttribute('aria-current',String(j===i-c.a));
  });
}

var mostrarBase=show;
show=function(n){mostrarBase(n);pintarPag();};

document.addEventListener('keydown',function(e){
  if(e.metaKey||e.ctrlKey||e.altKey)return;
  /* Escribiendo en un campo, las flechas mueven el cursor y no el capítulo. */
  var t=e.target&&e.target.tagName;
  if(t==='INPUT'||t==='TEXTAREA'||t==='SELECT'||(e.target&&e.target.isContentEditable))return;
  var k=capDe(i);
  if(e.key==='ArrowDown'){e.preventDefault();if(k<CAPS.length-1)show(CAPS[k+1].a);}
  else if(e.key==='ArrowUp'){e.preventDefault();show(i>CAPS[k].a?CAPS[k].a:CAPS[Math.max(0,k-1)].a);}
  else{
    for(var j=0;j<CAPS.length;j++){
      if(CAPS[j].tecla===e.key){e.preventDefault();show(CAPS[j].a);return;}
    }
  }
},{signal:typeof senal!=='undefined'?senal:undefined});

pintarPag();
"""


# ═══════════════════════════════════════════════════════════════════════
#  JS_INTER — el comportamiento de las demos
#
#  Va el ÚLTIMO del <script>, después de JS y de js_pag, y por una razón
#  concreta: build_taller.py y build_curso.py construyen su script con
#  `JS.split("function setLvl")[0]`, así que todo lo que se escriba dentro de
#  JS antes de esa línea viaja a los 29 decks del taller y los 36 del curso,
#  donde este markup no existe. Un TypeError ahí se lleva por delante el
#  resto del script, la paginación incluida. Aquí no puede pasar: esta
#  constante solo la concatena este archivo.
#
#  Todo escuchador pasa la señal de aborto. PaginaGenerada.tsx ejecuta el
#  script con `new Function("senal", js)` y aborta al desmontar; sin la señal
#  los escuchadores se duplicarían cada vez que se entra y se sale de la
#  presentación.
# ═══════════════════════════════════════════════════════════════════════

JS_INTER = r"""
(function(){
var SEN={signal:typeof senal!=='undefined'?senal:undefined};
function ver(r,q){return r.querySelector(q);}
function todos(r,q){return [].slice.call(r.querySelectorAll(q));}
var reinicios=[];

/* ── bloques: se pulsan y el gato hace caso ── */
todos(document,'[data-demo="bloques"]').forEach(function(d){
  var prog=ver(d,'[data-prog]'),banco=ver(d,'[data-banco]'),vacio=ver(d,'.bq-vacio'),
      per=ver(d,'[data-per]'),pts=ver(d,'[data-pts]'),ok=ver(d,'[data-ok]');
  var paso=0,puntos=0,puestas=0;
  function pintar(){per.style.left=(paso*22)+'%';pts.textContent=puntos;}
  todos(banco,'.bq').forEach(function(b){
    b.addEventListener('click',function(){
      if(b.disabled)return;
      b.disabled=true;
      var copia=b.cloneNode(true);copia.disabled=true;
      vacio.hidden=true;prog.appendChild(copia);
      var k=+b.getAttribute('data-b');
      if(k===0){if(paso<3)paso++;}
      else if(k===1){per.style.transform='translateY(-13px)';
        setTimeout(function(){per.style.transform='';},250);}
      else{puntos++;}
      pintar();
      puestas++;
      if(puestas===3)ok.textContent='Eso ya es un programa.';
    },SEN);
  });
  reinicios.push(function(){
    paso=0;puntos=0;puestas=0;ok.textContent='';vacio.hidden=false;
    todos(prog,'.bq').forEach(function(c){c.remove();});
    todos(banco,'.bq').forEach(function(b){b.disabled=false;});
    per.style.transform='';pintar();
  });
});

/* ── tu página: se escribe y cambia ── */
todos(document,'[data-demo="pagina"]').forEach(function(d){
  var nom=ver(d,'[data-nom]'),tit=ver(d,'[data-tit]'),vista=ver(d,'[data-vista]'),
      cols=todos(d,'.pg-col'),base=vista.style.getPropertyValue('--c');
  nom.addEventListener('input',function(){
    tit.textContent=nom.value.trim()||'Tu nombre';
  },SEN);
  cols.forEach(function(b){
    b.addEventListener('click',function(){
      cols.forEach(function(o){o.setAttribute('aria-pressed',String(o===b));});
      vista.style.setProperty('--c',b.getAttribute('data-c'));
    },SEN);
  });
  reinicios.push(function(){
    nom.value='';tit.textContent='Tu nombre';vista.style.setProperty('--c',base);
    cols.forEach(function(o,k){o.setAttribute('aria-pressed',String(k===0));});
  });
});

/* ── una línea de código que se ejecuta de verdad ── */
todos(document,'[data-demo="codigo"]').forEach(function(d){
  var run=ver(d,'[data-run]'),out=ver(d,'[data-out]'),ok=ver(d,'[data-ok]'),
      paso=+(d.getAttribute('data-paso')||1),n=0;
  run.addEventListener('click',function(){
    n+=paso;out.textContent=n;
    if(n>=10&&ok)ok.textContent='Diez. Eso es un marcador.';
  },SEN);
  reinicios.push(function(){n=0;out.textContent='0';if(ok)ok.textContent='';});
});

/* ── el dado: random.randint(1, 6), simulado con Math.random ── */
todos(document,'[data-demo="dado"]').forEach(function(d){
  var tirar=ver(d,'[data-tirar]'),cara=ver(d,'[data-cara]'),pts=ver(d,'[data-pts]'),
      ok=ver(d,'[data-ok]'),puntos=0;
  tirar.addEventListener('click',function(){
    var n=1+Math.floor(Math.random()*6);
    puntos+=n;
    cara.textContent=n;pts.textContent=puntos;
    cara.classList.remove('tira');void cara.offsetWidth;cara.classList.add('tira');
    if(puntos>=20)ok.textContent='Veinte puntos. Eso ya es un juego.';
    else if(n===6)ok.textContent='¡Seis! Lo decidió el azar, no tú.';
    else ok.textContent='';
  },SEN);
  reinicios.push(function(){
    puntos=0;cara.textContent='–';pts.textContent='0';ok.textContent='';
    cara.classList.remove('tira');
  });
});

/* ── IA: un clasificador simulado. Los porcentajes son de mentira, la forma
   de responder es la de verdad: una clase y lo seguro que está. ── */
todos(document,'[data-demo="ia"]').forEach(function(d){
  var CLASES=['manzana','guineo','mano'];
  var BASE=[[94,4,2],[8,89,3],[2,1,97]];
  var ejs=todos(d,'.ia-ej'),filas=todos(d,'.ia-fila'),
      clase=ver(d,'[data-clase]'),ok=ver(d,'[data-ok]');
  function pintar(ps){
    var mx=ps.indexOf(Math.max.apply(null,ps));
    filas.forEach(function(f,k){
      f.classList.toggle('gana',k===mx);
      ver(f,'.ia-lleno').style.width=ps[k]+'%';
      ver(f,'.ia-pc').textContent=ps[k]+'%';
    });
    return mx;
  }
  ejs.forEach(function(b){
    b.addEventListener('click',function(){
      var ps=BASE[+b.getAttribute('data-ej')].slice();
      /* Un poco de ruido: un modelo nunca da dos veces el mismo número. */
      var top=ps.indexOf(Math.max.apply(null,ps)),otra=(top+1)%3,j=Math.floor(Math.random()*5);
      ps[top]-=j;ps[otra]+=j;
      ejs.forEach(function(o){o.setAttribute('aria-pressed',String(o===b));});
      var mx=pintar(ps);
      clase.textContent='"'+CLASES[mx]+'"';
      ok.textContent=CLASES[mx]==='manzana'
        ?'El if se cumple: ¡Es una manzana!'
        :'El if no se cumple: no pasa nada.';
    },SEN);
  });
  reinicios.push(function(){
    ejs.forEach(function(o){o.setAttribute('aria-pressed','false');});
    filas.forEach(function(f){
      f.classList.remove('gana');
      ver(f,'.ia-lleno').style.width='0';ver(f,'.ia-pc').textContent='–';
    });
    clase.textContent='?';ok.textContent='';
  });
});

/* ── una app diminuta: escribir, agregar, contar ── */
todos(document,'[data-demo="app"]').forEach(function(d){
  var caja=ver(d,'[data-in]'),add=ver(d,'[data-add]'),lista=ver(d,'[data-lista]'),
      n=ver(d,'[data-n]');
  function contar(){n.textContent=lista.children.length;}
  function agregar(){
    var t=caja.value.trim();
    if(!t)return;
    var li=document.createElement('li');
    li.appendChild(document.createTextNode(t));
    var x=document.createElement('button');
    x.className='quitar';x.type='button';x.textContent='×';
    x.setAttribute('aria-label','Quitar '+t);
    x.addEventListener('click',function(){li.remove();contar();},SEN);
    li.appendChild(x);lista.appendChild(li);caja.value='';contar();
  }
  add.addEventListener('click',agregar,SEN);
  caja.addEventListener('keydown',function(e){
    if(e.key==='Enter'){e.preventDefault();agregar();}
  },SEN);
  reinicios.push(function(){caja.value='';lista.innerHTML='';contar();});
});

/* ── veinte datos y un buscador ── */
todos(document,'[data-demo="datos"]').forEach(function(d){
  var q=ver(d,'[data-q]'),n=ver(d,'[data-n]'),filas=todos(d,'.ls li');
  function filtrar(){
    var t=q.value.trim().toLowerCase(),v=0;
    filas.forEach(function(li){
      var cabe=!t||li.getAttribute('data-t').indexOf(t)>-1;
      li.hidden=!cabe;if(cabe)v++;
    });
    n.textContent=v;
  }
  q.addEventListener('input',filtrar,SEN);
  reinicios.push(function(){q.value='';filtrar();});
});

/* ── un formulario que avisa mientras escribes ── */
todos(document,'[data-demo="formulario"]').forEach(function(d){
  var c=ver(d,'[data-mail]'),m=ver(d,'[data-msg]'),env=ver(d,'[data-env]');
  var BIEN=/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  function mirar(){
    var v=c.value.trim(),ok=BIEN.test(v);
    c.classList.toggle('bien',ok);c.classList.toggle('mal',!ok);
    m.classList.toggle('bien',ok);m.classList.toggle('mal',!ok);
    m.textContent=ok?'Correcto. Ya puedes enviar.':
      (v.indexOf('@')<0?'Falta el arroba.':'Falta el punto y lo de después.');
    env.disabled=!ok;
  }
  c.addEventListener('input',mirar,SEN);
  env.addEventListener('click',function(){m.textContent='Enviado.';},SEN);
  reinicios.push(function(){c.value='';c.className='campo';mirar();});
});

/* ── Snake ──
   Se juega con las flechas, y el deck pasa de diapositiva con las flechas. El
   escuchador va en fase de CAPTURA: registrado aquí corre antes que el de JS,
   así que mientras se juega la flecha mueve la serpiente y no cambia de
   diapositiva, y sin jugar navega como siempre. Se resuelve aquí y no tocando
   JS porque JS viaja a los 65 decks de taller y curso.

   La cadena de arriba sigue el estado del juego: es lo que mantiene el sentido
   de la diapositiva. Perder no es un fallo del alumno, es el paso 3 del ciclo. */
todos(document,'[data-demo="snake"]').forEach(function(d){
  var COLS=+d.getAttribute('data-cols'),FILAS=+d.getAttribute('data-filas');
  var tab=ver(d,'[data-tablero]'),pts=ver(d,'[data-pts]'),rec=ver(d,'[data-rec]'),
      msg=ver(d,'[data-msg]'),go=ver(d,'[data-go]'),
      esl=todos(document,'[data-cadena] .esl');
  var celdas=[],cuerpo,dir,pedido,manzana,puntos,record=0,intentos=0,
      reloj=null,fase='quieto',pausa=false;

  tab.style.setProperty('--c',COLS);
  tab.style.setProperty('--f',FILAS);
  tab.innerHTML='';  // la segunda pasada de React no duplica el tablero
  for(var k=0;k<COLS*FILAS;k++){
    var c=document.createElement('i');tab.appendChild(c);celdas.push(c);
  }

  function cadena(k){
    esl.forEach(function(e,j){
      e.classList.toggle('act',j===k);e.classList.toggle('hecho',j<k);
    });
  }
  function pintar(){
    for(var j=0;j<celdas.length;j++)celdas[j].className='';
    if(manzana)celdas[manzana.y*COLS+manzana.x].className='man';
    for(var j=0;j<cuerpo.length;j++){
      celdas[cuerpo[j].y*COLS+cuerpo[j].x].className=j===0?'cab':'cue';
    }
  }
  function nuevaManzana(){
    var libres=[];
    for(var y=0;y<FILAS;y++)for(var x=0;x<COLS;x++){
      var ocupada=cuerpo.some(function(s){return s.x===x&&s.y===y;});
      if(!ocupada)libres.push({x:x,y:y});
    }
    manzana=libres[Math.floor(Math.random()*libres.length)];
  }
  function parar(){if(reloj){clearInterval(reloj);reloj=null;}}

  function perder(contra){
    parar();fase='perdido';
    var mejor=puntos>record;
    if(mejor)record=puntos;
    intentos++;
    if(mejor&&intentos>1){
      cadena(4);
      msg.className='ci-msg bien';
      msg.textContent=puntos+', mejor que antes. ¿Qué hiciste distinto?';
    }else{
      cadena(2);
      msg.className='ci-msg mal';
      msg.textContent='Chocaste con '+contra+'. Comiste '+puntos+
        '. Eso no baja la nota: ya sabes qué pasó.';
    }
    rec.textContent=record?'tu mejor: '+record:'';
    go.textContent='Otra vez';
  }

  function paso(){
    if(pausa)return;
    dir=pedido;
    var cab={x:cuerpo[0].x+dir.x,y:cuerpo[0].y+dir.y};
    if(cab.x<0||cab.y<0||cab.x>=COLS||cab.y>=FILAS)return perder('la pared');
    if(cuerpo.some(function(s){return s.x===cab.x&&s.y===cab.y;}))
      return perder('tu propia cola');
    cuerpo.unshift(cab);
    if(manzana&&cab.x===manzana.x&&cab.y===manzana.y){
      puntos++;pts.textContent=puntos;nuevaManzana();
      parar();reloj=setInterval(paso,Math.max(90,170-puntos*4));
    }else{
      cuerpo.pop();
    }
    pintar();
  }

  function jugar(){
    parar();
    cuerpo=[{x:4,y:5},{x:3,y:5},{x:2,y:5}];
    dir=pedido={x:1,y:0};puntos=0;pausa=false;fase='jugando';
    pts.textContent='0';nuevaManzana();pintar();
    cadena(intentos===0?1:3);
    msg.className='ci-msg';
    msg.textContent=intentos===0
      ? 'Vas jugando. Si chocas no pasa nada.'
      : 'Otra vez, sabiendo dónde chocaste.';
    go.textContent='Otra vez';
    reloj=setInterval(paso,170);
  }

  function girar(v){
    /* No se puede dar media vuelta sobre uno mismo: sería perder al instante
       por un roce del dedo, y eso no enseña nada. */
    if(dir.x===-v.x&&dir.y===-v.y)return;
    pedido=v;
  }

  var TECLAS={ArrowUp:{x:0,y:-1},ArrowDown:{x:0,y:1},
              ArrowLeft:{x:-1,y:0},ArrowRight:{x:1,y:0}};

  /* Qué se traga y qué no, que aquí hay tres cosas peleándose por las flechas:
     el juego, el paso de diapositiva (izquierda/derecha) y el salto de
     capítulo de la paginación (arriba/abajo).

     · Jugando: las cuatro son del juego. Para salir queda el espacio, que
       pasa de diapositiva igual que en todas las demás.
     · Sin jugar: arriba y abajo arrancan la partida en esa dirección, que es
       lo que hace cualquier Snake. Sin esto, un alumno que acaba de chocar
       pulsa una flecha para volver a jugar y se va a otra diapositiva.
     · Sin jugar, izquierda y derecha siguen navegando: el docente mueve la
       presentación con las flechas todo el rato y no se le puede quitar. */
  document.addEventListener('keydown',function(e){
    if(e.metaKey||e.ctrlKey||e.altKey)return;
    /* Si el docente escribe en un panel, una flecha no arranca la partida. */
    var tg=e.target&&e.target.tagName;
    if(tg==='INPUT'||tg==='TEXTAREA'||tg==='SELECT'||(e.target&&e.target.isContentEditable))return;
    var v=TECLAS[e.key];
    if(!v)return;
    if(fase==='jugando'){
      e.preventDefault();e.stopPropagation();girar(v);return;
    }
    if(e.key==='ArrowUp'||e.key==='ArrowDown'){
      e.preventDefault();e.stopPropagation();
      jugar();pedido=v;
    }
  },{capture:true,signal:typeof senal!=='undefined'?senal:undefined});

  /* Deslizar el dedo. No hay botones en pantalla a propósito —los controles
     son el teclado— pero sin esto, en un celular el juego sería imposible.
     No ocupa un solo píxel de la diapositiva. */
  var tx=0,ty=0;
  tab.addEventListener('touchstart',function(e){
    var t=e.changedTouches[0];tx=t.clientX;ty=t.clientY;
  },{passive:true,signal:typeof senal!=='undefined'?senal:undefined});
  tab.addEventListener('touchend',function(e){
    if(fase!=='jugando')return;
    var t=e.changedTouches[0],dx=t.clientX-tx,dy=t.clientY-ty;
    if(Math.abs(dx)<24&&Math.abs(dy)<24)return;   /* un toque no es un gesto */
    girar(Math.abs(dx)>Math.abs(dy)
      ? {x:dx>0?1:-1,y:0}
      : {x:0,y:dy>0?1:-1});
  },SEN);

  go.addEventListener('click',jugar,SEN);
  /* Con la pestaña oculta no se juega solo: se pausa y se sigue al volver. */
  document.addEventListener('visibilitychange',function(){
    if(document.visibilityState==='hidden'&&fase==='jugando')pausa=true;
  },SEN);

  function limpiar(){
    parar();
    fase='quieto';pausa=false;puntos=0;record=0;intentos=0;
    cuerpo=[];manzana=null;
    for(var j=0;j<celdas.length;j++)celdas[j].className='';
    pts.textContent='0';rec.textContent='';
    msg.className='ci-msg';
    msg.textContent='Pulsa Jugar. Se juega con las flechas.';
    go.textContent='▶ Jugar';cadena(0);
  }
  reinicios.push(limpiar);
  limpiar();
});

/* ── la nota, marcándola ── */
todos(document,'[data-demo="eval"]').forEach(function(d){
  var filas=todos(d,'.bar'),total=ver(d.parentNode,'[data-total]');
  function sumar(){
    var t=0;
    filas.forEach(function(b){
      if(b.getAttribute('aria-pressed')==='true')t+=+b.getAttribute('data-pc');
    });
    total.textContent=t;
  }
  filas.forEach(function(b){
    b.addEventListener('click',function(){
      b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')==='true'?'false':'true');
      sumar();
    },SEN);
  });
  reinicios.push(function(){
    filas.forEach(function(b){b.setAttribute('aria-pressed','false');});
    sumar();
  });
});

/* ── el vídeo: no se le pide nada a YouTube hasta que se pulsa ── */
todos(document,'[data-demo="video"]').forEach(function(d){
  var btn=ver(d,'[data-play]'),id=d.getAttribute('data-yt'),portada=btn;
  btn.addEventListener('click',function(){
    var f=document.createElement('iframe');
    f.className='vid-marco';
    f.src='https://www.youtube-nocookie.com/embed/'+id+'?rel=0&autoplay=1';
    f.title='Vídeo';f.allowFullscreen=true;
    f.setAttribute('allow','autoplay; encrypted-media; picture-in-picture; fullscreen');
    btn.replaceWith(f);
  },SEN);
  reinicios.push(function(){
    var f=ver(d,'.vid-marco');
    if(f)f.replaceWith(portada);
  });
});

/* Al cambiar de diapositiva, todo a cero. Que el docente vuelva a la 4 y
   encuentre los bloques puestos de la clase anterior sería lo peor de todo.
   Mismo truco que usa js_pag para engancharse a `show`. */
var showBase=show;
function reiniciarTodo(){reinicios.forEach(function(f){try{f();}catch(e){}});}
show=function(n){showBase(n);reiniciarTodo();};

/* El bloqueo del docente. El panel pone `data-bloqueo` en el elemento raíz;
   el CSS ya impide tocar nada, pero una partida ya empezada seguiría corriendo
   sola detrás del cartel. Aquí se para de verdad. */
new MutationObserver(function(){
  if(document.documentElement.getAttribute('data-bloqueo')==='juegos')reiniciarTodo();
}).observe(document.documentElement,{attributes:true,attributeFilter:['data-bloqueo']});
})();
"""
MUESTRA_JPG = os.path.join(HERE, "..", "asistente-aula", "public", "muestra", "tienda.jpg")


def muestra(url=None):
    """La tienda de verdad, en «Quién soy».

    La diapositiva dice que construye tiendas; enseñar una es más corto que
    explicarlo. Va en bucle y en silencio: nadie la va a mirar dos veces, tiene
    que contarse sola mientras él habla.

    En la app es un vídeo servido desde public/. En el HTML suelto no puede
    serlo —ese archivo viaja solo, por correo— así que ahí va el primer
    fotograma incrustado. Peor, pero entero: un vídeo roto es peor que una foto."""
    if url:
        return (f'<video class="mstr" src="{url}" poster="{url[:-4]}.jpg" '
                f'autoplay muted loop playsinline '
                f'aria-label="Una tienda en línea construida por el docente"></video>')
    with open(MUESTRA_JPG, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return (f'<img class="mstr" src="data:image/jpeg;base64,{b64}" '
            f'alt="Una tienda en línea construida por el docente">')


# El sitio publicado. El QR de una diapositiva se escanea con un teléfono que no
# está en la red del aula, así que no puede apuntar a localhost.
SITIO = C.SITIO

TEMAS = (("oscuro", "Oscuro"), ("claro", "Claro"), ("pared", "Pared"))


def botones_tema():
    """Los tres colores de fondo, arriba a la derecha."""
    return "".join(f'<button class="tembtn" data-tema="{t}" aria-pressed="false">{n}</button>'
                   for t, n in TEMAS)


def chrome_pag(capitulos=None, enlace_indice=None):
    """El marcado de la paginación y del enlace de vuelta.

    Devuelve las tres piezas que van en sitios distintos del deck: el enlace
    arriba a la izquierda, la paginación abajo, y el `<script>` que la pinta.
    `capitulos` vacío da la fila de puntos; con capítulos salen también los
    chips. `enlace_indice` a None deja el deck sin salida, que es lo que quiere
    el HTML suelto: ahí no hay ningún índice a donde volver."""
    volver = (f'<div class="chrome tl"><a class="volver" href="{enlace_indice}">'
              f'&#8592; Presentaciones</a></div>') if enlace_indice else ""
    pag = ('<div class="paginacion"><div class="caps" id="caps"></div>'
           '<div class="pass" id="pass"></div></div>')
    js = JS_PAG % json.dumps(capitulos or [], ensure_ascii=False)
    return volver, pag, js


ACENTO_NIVEL = {"1ro": "n1", "2do": "n2", "3ro": "n3"}

# El lienzo de ilustra.py mide 1200×675 porque su destino son PNG a pantalla
# completa para el Kahoot; aquí el dibujo va en media diapositiva y con tanto
# margen queda perdido. Las escenas que se usan ocupan de 270 a 930 en x y de
# 101 a 558 en y, medido sobre el SVG: este recorte las deja holgadas y aumenta
# el dibujo vez y media. Si algún día se mete una escena más ancha, se verá
# cortada y habrá que volver a medir.
RECORTE = "220 55 760 560"


def escena(nombre, nivel):
    """Una escena de ilustra.py, lista para meter en una diapositiva.

    Se generan las tres de una vez, cada una con el color de su curso, porque
    el nivel se cambia en el navegador y no al generar: no hay a quién
    preguntarle el acento en tiempo de dibujo.

    `lienzo()` fija width y height en píxeles, que en una columna elástica deja
    el dibujo clavado a 1200 px de ancho; se le quitan para que mande el
    viewBox. Y el fondo va en el CSS y no en el SVG, para poder animar los
    rellenos sin que el panel entero parpadee con ellos."""
    svg = IL.dibujar(nombre, "#" + C.PALETA[ACENTO_NIVEL[nivel]], "none")
    svg = svg.replace('width="1200" height="675" ', "", 1)
    return svg.replace('viewBox="0 0 1200 675"', f'viewBox="{RECORTE}"', 1)


# ═══════════════════════════════════════════════════════════════════════
#  Las demos de «qué vas a construir»
#
#  Ocho, repartidas entre los nueve pasos de los tres cursos. Cada una
#  demuestra en cinco segundos lo que el texto de al lado promete para
#  diciembre. El comportamiento vive en JS_INTER; aquí solo el markup.
#
#  Se pulsa, no se arrastra. Arrastrar en un proyector con trackpad falla
#  delante de treinta personas, y en el celular de un estudiante es peor;
#  pulsar una pieza y que salte a su sitio demuestra exactamente lo mismo.
# ═══════════════════════════════════════════════════════════════════════

# La silueta real de un bloque de Scratch, la misma de ilustra.py, para que
# las piezas que se pulsan sean las que ya salen en el resto del material.
_PIEZA_D = IL._pieza(0.5, 0.5, 107.0, 26.0, r=5.0, entrada=14.0, ancho=13.0, prof=6.0)

BQ_PIEZAS = (("mover", "→"), ("saltar", "↑"), ("+1 punto", "★"))

DATOS_EJEMPLO = [
    ("Free Fire", "Battle royale"), ("Minecraft", "Construcción"),
    ("Roblox", "Plataforma"), ("Fortnite", "Battle royale"),
    ("FIFA", "Deportes"), ("Among Us", "Social"),
    ("Mario Kart", "Carreras"), ("Clash Royale", "Estrategia"),
    ("Stumble Guys", "Carreras"), ("Brawl Stars", "Acción"),
    ("Subway Surfers", "Corredor"), ("GTA", "Mundo abierto"),
    ("Call of Duty", "Disparos"), ("Geometry Dash", "Plataforma"),
    ("Candy Crush", "Puzles"), ("Valorant", "Disparos"),
    ("Pokémon", "Aventura"), ("Just Dance", "Baile"),
    ("The Sims", "Simulación"), ("Terraria", "Construcción"),
]

COLORES_PAGINA = ("#F97316", "#2563EB", "#10B981", "#A855F7", "#EF4444")


def demo(nombre, nivel):
    """El markup de una demo. `nivel` solo se usa para textos, no para ids:
    los tres cursos conviven en el DOM y un id repetido rompería el primero."""
    if nombre == "bloques":
        piezas = "".join(
            f'<button class="bq" data-b="{i}" type="button" aria-label="Pieza {t}">'
            f'<svg viewBox="0 0 108 33" aria-hidden="true"><path d="{_PIEZA_D}"/></svg>'
            f'<b>{t}</b></button>'
            for i, (t, _) in enumerate(BQ_PIEZAS))
        return (f'<div class="demo" data-demo="bloques">'
                f'<p class="pista">PULSA LAS PIEZAS</p>'
                f'<div class="bq-prog" data-prog>'
                f'<span class="bq-vacio">Tu programa, vac&#237;o</span></div>'
                f'<div class="bq-banco" data-banco>{piezas}</div>'
                f'<div class="bq-mundo"><span class="bq-piso">'
                f'<span class="bq-per" data-per>&#128049;</span>'
                f'<span class="bq-meta">&#9733;</span></span>'
                f'<span class="bq-mark">Puntos <b data-pts>0</b></span></div>'
                f'<p class="ok" data-ok role="status"></p></div>')

    if nombre == "pagina":
        cols = "".join(
            f'<button class="pg-col" type="button" data-c="{c}" style="--c:{c}"'
            f' aria-label="Color" aria-pressed="{"true" if i == 0 else "false"}"></button>'
            for i, c in enumerate(COLORES_PAGINA))
        return (f'<div class="demo" data-demo="pagina">'
                f'<p class="pista">ESCRIBE Y ELIGE COLOR</p>'
                f'<div class="pg-fila"><input class="campo" data-nom maxlength="16"'
                f' placeholder="Tu nombre" aria-label="Tu nombre">'
                f'<span class="pg-cols">{cols}</span></div>'
                f'<div class="pg-vista" data-vista style="--c:{COLORES_PAGINA[0]}">'
                f'<div class="pg-barra"><i></i><i></i><i></i></div>'
                f'<div class="pg-cuerpo"><h4 data-tit>Tu nombre</h4>'
                f'<p>Mi primera p&#225;gina web</p>'
                f'<span class="pg-btn">Cont&#225;ctame</span></div></div></div>')

    if nombre == "codigo":
        # Python de verdad: cada pulsación ejecuta estas líneas una vez más.
        if nivel == "2do":
            linea = ('<span class="k">for</span> i <span class="k">in</span> '
                     '<span class="k">range</span>(<span class="v">3</span>):<br>'
                     '&#160;&#160;&#160;&#160;puntos += <span class="v">2</span><br>'
                     '<span class="k">display</span>(puntos)')
            paso, pista = 6, "PULSA Y CUENTA"
        else:
            linea = ('puntos = puntos + <span class="v">1</span><br>'
                     '<span class="k">display</span>(puntos)')
            paso, pista = 1, "PULSA ▶ Y MIRA EL N&#218;MERO"
        return (f'<div class="demo" data-demo="codigo" data-paso="{paso}">'
                f'<p class="pista">{pista}</p>'
                f'<div class="cd-caja">{linea}</div>'
                f'<div class="cd-fila">'
                f'<button class="btn" type="button" data-run>&#9654; Ejecutar</button>'
                f'<span class="cd-out">puntos &#8594; <b data-out>0</b></span></div>'
                f'<p class="ok" data-ok role="status"></p></div>')

    if nombre == "dado":
        return ('<div class="demo" data-demo="dado">'
                '<p class="pista">PULSA Y TIRA EL DADO</p>'
                '<div class="cd-caja">dado = random.<span class="k">randint</span>'
                '(<span class="v">1</span>, <span class="v">6</span>)<br>'
                'puntos += dado</div>'
                '<div class="cd-fila">'
                '<button class="btn" type="button" data-tirar>&#127922; Tirar</button>'
                '<span class="dd-cara" data-cara aria-live="polite">&#8211;</span>'
                '<span class="cd-out">puntos &#8594; <b data-pts>0</b></span></div>'
                '<p class="ok" data-ok role="status"></p></div>')

    if nombre == "ia":
        ejemplos = "".join(
            f'<button class="ia-ej" type="button" data-ej="{i}" aria-pressed="false"'
            f' aria-label="Ejemplo: {n}">{e}</button>'
            for i, (e, n) in enumerate((("&#127822;", "manzana"), ("&#127820;", "guineo"),
                                        ("&#9995;", "mano"))))
        filas = "".join(
            f'<div class="ia-fila"><span>{n}</span><span class="ia-pista">'
            f'<span class="ia-lleno"></span></span><span class="ia-pc">&#8211;</span></div>'
            for n in ("manzana", "guineo", "mano"))
        return (f'<div class="demo" data-demo="ia">'
                f'<p class="pista">AS&#205; RESPONDE UN MODELO &#183; TOCA UNO</p>'
                f'<div class="ia-ejs">{ejemplos}</div>'
                f'<div class="ia-res">{filas}'
                f'<p class="cd-out">clase &#8594; <b data-clase>?</b></p></div>'
                f'<div class="cd-caja"><span class="k">if</span> clase == '
                f'<span class="v">"manzana"</span>:<br>'
                f'&#160;&#160;&#160;&#160;<span class="k">display</span>'
                f'(<span class="v">"&#161;Es una manzana!"</span>)</div>'
                f'<p class="ok" data-ok role="status"></p></div>')

    if nombre == "app":
        return ('<div class="demo" data-demo="app">'
                '<p class="pista">ESCRIBE Y AGREGA</p>'
                '<div class="pg-fila"><input class="campo" data-in maxlength="22"'
                ' placeholder="Una idea" aria-label="Una idea">'
                '<button class="btn" type="button" data-add>Agregar</button></div>'
                '<ul class="ls" data-lista></ul>'
                '<p class="pie-n"><b data-n>0</b> en la lista</p></div>')

    if nombre == "datos":
        filas = "".join(f'<li data-t="{t.lower()}"><span class="nm">{t}</span>'
                        f'<span>{g}</span></li>' for t, g in DATOS_EJEMPLO)
        return (f'<div class="demo" data-demo="datos">'
                f'<p class="pista">ESCRIBE PARA FILTRAR</p>'
                f'<input class="campo" data-q placeholder="Buscar entre 20"'
                f' aria-label="Buscar"><ul class="ls" data-lista>{filas}</ul>'
                f'<p class="pie-n"><b data-n>20</b> de 20</p></div>')

    if nombre == "formulario":
        return ('<div class="demo" data-demo="formulario">'
                '<p class="pista">ESCRIBE UN CORREO</p>'
                '<input class="campo" data-mail placeholder="nombre@escuela.do"'
                ' aria-label="Correo" autocomplete="off">'
                '<p class="fm-msg mal" data-msg role="status">Falta el arroba.</p>'
                '<button class="btn" type="button" data-env disabled>Enviar</button></div>')

    raise SystemExit(f"\n  ABORTADO: no existe la demo '{nombre}'.\n")


def qr(texto):
    """El QR de un enlace, dibujado en el build y metido en el HTML.

    Lo genera el paquete `qrcode`, instalado en la app como dependencia de
    desarrollo solo para esto (la app no lo usa en marcha): no se descarga
    de ningún servicio, porque un QR que depende de una API es un QR que un día
    sale roto delante de la clase. Sale en negro sobre blanco aunque el deck sea
    oscuro; un QR invertido lo lee mal la mitad de los teléfonos."""
    guion = ("require('qrcode').toString(process.argv[1],"
             "{type:'svg',margin:2,errorCorrectionLevel:'M'},"
             "(e,s)=>{if(e)throw e;process.stdout.write(s)})")
    r = subprocess.run(["node", "-e", guion, texto], capture_output=True, text=True,
                       cwd=os.path.join(HERE, "..", "asistente-aula"))
    if r.returncode:
        raise SystemExit(f"\n  ABORTADO: no se pudo generar el QR de {texto}.\n"
                         f"  Hace falta `npm install` en asistente-aula/.\n  {r.stderr.strip()}\n")
    caja = re.search(r'viewBox="([^"]+)"', r.stdout).group(1)
    trazo = re.findall(r'<path stroke="[^"]*" d="([^"]+)"', r.stdout)[0]
    return (f'<svg class="qr" viewBox="{caja}" shape-rendering="crispEdges" '
            f'role="img" aria-label="Código QR de {texto}">'
            f'<path fill="#fff" d="M0 0h999v999H0z"/>'
            f'<path stroke="#000" d="{trazo}"/></svg>')


def build(enlace_indice: str | None = None, url_muestra: str | None = None):
    """`enlace_indice` solo lo pasa el exportador de la app. El HTML suelto de
    salida/ no tiene índice a donde volver, y un enlace roto en el archivo que
    se manda por correo es peor que ninguno."""
    lvlbtns = "".join(f'<button class="lvlbtn" data-lvl="{l}" aria-pressed="false">{l}</button>'
                      for l in ("1ro", "2do", "3ro"))


    # El hueco de la lista. Lo llena el panel del docente en el navegador; en
    # el HTML no viaja ni un nombre.
    s_lista = ""
    for l in ("1ro", "2do", "3ro"):
        s_lista += f'''<div data-only="{l}">
      <h2 class="mid">Y ustedes.</h2>
      <div class="roster-caja" data-roster="{l}">
        <p class="conteo">La lista aparece al entrar con tu cuenta.</p>
      </div></div>'''

    # Tres tarjetas, cada una con su demo. La rejilla va en un hijo del
    # `data-only` y no en él: setLvl le escribe `style.display='block'`
    # inline y machacaría cualquier `grid`.
    s3 = ""
    for l, (tit, pasos, cierre) in CONSTRUIR.items():
        tarjetas = "".join(f'''<div class="tarj"><span class="n">{n.upper()}</span>
        <h3>{t}</h3><p>{d}</p>{demo(dm, l)}</div>''' for n, t, d, dm in pasos)
        s3 += f'''<div data-only="{l}">
      <h2 class="mid">{tit}</h2>
      <div class="cons">{tarjetas}</div>
      <p class="say">{cierre}</p>
    </div>'''

    s7 = ""
    for l, (tit, ps) in RETO.items():
        # Los juegos de reserva, en una línea discreta: se leen si hacen falta.
        juegos = juegos_de(l)
        sobra = (f'<p class="conteo">Si sobra tiempo: '
                 f'{" &#183; ".join(html.escape(str(j[0])) for j in juegos)}</p>'
                 if juegos else "")
        s7 += f'''<div data-only="{l}"><div class="conej">
      <div class="card"><h3>{tit}</h3>
      {"".join(f"<p>{p}</p>" for p in ps)}</div>
      <div class="esc">{escena(ESCENA_RETO[l], l)}</div>
    </div>{sobra}</div>'''

    # El diagnóstico de entrada, uno por nivel. El enlace abre el Kahoot para
    # lanzarlo; quien juega entra en kahoot.it con el PIN que sale al
    # proyectarlo, y eso se dice en la propia diapositiva porque es la pregunta
    # que hacen treinta personas a la vez.
    # El QR lleva el curso en la dirección, así que al escanearlo desde 1ro
    # solo salen las tres secciones de 1ro. Uno por curso, no uno genérico.
    QR_CURSO = {l: qr(f"{SITIO}/diagnostico?curso={l}") for l in ("1ro", "2do", "3ro")}
    volver, pag, js_pag = chrome_pag(None, enlace_indice)
    video_id, video_tit = C.VIDEO_EVAL
    tembtns = botones_tema()
    s_muestra = muestra(url_muestra)
    s_quiz = ""
    for l in ("1ro", "2do", "3ro"):
        s_quiz += (f'<div data-only="{l}"><div class="quiz-fila">'
                   f'<a class="quiz" target="_blank" rel="noopener"'
                   f' href="{SITIO}/diagnostico?curso={l}">'
                   f'<span class="quiz-k">{l} &#183; diez preguntas</span>'
                   f'<span class="quiz-t">Antes de empezar</span>'
                   f'<span class="quiz-p">Escaneen el c&#243;digo. No lleva nota: es para '
                   f'saber de d&#243;nde partimos</span></a>'
                   f'<div class="qr-caja">{QR_CURSO[l]}'
                   f'<span class="qr-pie">escanea aqu&#237;</span></div></div></div>')

    # Cada fila es un botón que se marca. Marcando solo lo semanal se llega a
    # 75 sin tocar el proyecto final, que es exactamente lo que dice la frase
    # de abajo y que hasta ahora había que creerse.
    #
    # El `data-pc` lleva el porcentaje de verdad; el `--w` es 2.6 veces mayor
    # y es solo ancho visual, para que la pista se llene. El total suma
    # `data-pc`, nunca el ancho.
    bars = "".join(f'''<button class="bar" type="button" aria-pressed="false"
      data-pc="{pc}"><span class="lab">{lab}</span>
      <span class="pc">{pc}%</span>
      <span class="track"><span class="fill" style="--w:{pc*2.6}%"></span></span></button>'''
      for lab, pc in EVAL)

    pagina = f'''<title>Hola, soy Criso</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Public+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap">
<style>{CSS}{CSS_PAG}{CSS_MOV}{CSS_JUEGO}</style>

<div class="prog" id="prog"></div>
{volver}
<div class="chrome tr">
  <span role="group" aria-label="Nivel del grupo" style="display:flex;gap:8px">{lvlbtns}</span>
  <span class="sep" aria-hidden="true"></span>
  <span role="group" aria-label="Color de la pantalla" style="display:flex;gap:6px">{tembtns}</span>
</div>

<main class="deck">

  <section class="slide">
   <div class="inner hero">
    <div>
      <p class="eyebrow">Programación · Secundaria · 2026 – 2027</p>
      <h1 class="big">Hola,<br>soy Criso.</h1>
      <p class="say">Este año no vamos a estudiar programación. La vamos a hacer.</p>
      <p class="sig">Criso · Docente de Programación · 1ro a 3ro</p>
    </div>
    <figure class="shot" style="margin:0">
      <span class="frame" aria-hidden="true"></span>
      <img src="{foto()}" alt="Retrato de Criso" width="800" height="1000">
    </figure>
   </div>
  </section>

  <section class="slide">
   <div class="inner">
    <p class="eyebrow">Quién soy</p>
    <div class="conej">
     <div>
      <h2 class="mid">Soy desarrollador frontend.</h2>
      <ul class="pts">
      <li><span><b>Construyo páginas y aplicaciones web</b> para empresas reales. Gente que paga porque algo funcione.</span></li>
      <li><span>Este año ustedes aprenden <b>Python</b>: el lenguaje con el que empieza casi todo el mundo y <b>el lenguaje de la inteligencia artificial</b>.</span></li>
      <li><span>Sitios que la gente usa todos los días: <b>tiendas, reservas,
        formularios</b>. Cosas que si fallan, alguien se queda sin comprar.</span></li>
      <li><span>Y me sigo equivocando todos los días. <b>Eso no es fallar: eso es el trabajo.</b></span></li>
      </ul>
     </div>
     <div class="mstr-caja">{s_muestra}
       <p class="mstr-pie">Una tienda que hice. Esto es lo que hay detrás.</p>
     </div>
    </div>
   </div>
  </section>

  <section class="slide">
   <div class="inner">
    <p class="eyebrow">Quiénes son</p>
    {s_lista}
   </div>
  </section>

  <section class="slide">
   <div class="inner">
    <p class="eyebrow">Qué vas a construir</p>
    {s3}
   </div>
  </section>

  <section class="slide">
   <div class="inner">
    <p class="eyebrow">Cómo trabajamos</p>
    <h2 class="mid">Siempre el mismo ciclo.</h2>
    <div class="chain" data-cadena>
      <span class="esl act">Construir</span><i>→</i><span class="esl">Probar</span><i>→</i><span class="esl">Equivocarse</span>
      <i>→</i><span class="esl">Corregir</span><i>→</i><span class="esl">Explicar</span>
    </div>
    <div class="juego" data-demo="snake" data-cols="17" data-filas="11">
      <div class="jg-lado">
        <p class="jg-marca">Comiste <b data-pts>0</b><span class="jg-rec" data-rec></span></p>
        <p class="ci-msg" data-msg role="status">Pulsa Jugar. Se juega con las flechas.</p>
        <div class="ci-btns">
          <button class="btn" type="button" data-go>&#9654; Jugar</button>
        </div>
      </div>
      <div class="jg-tablero" data-tablero aria-hidden="true"></div>
    </div>
    <p class="punch">Aquí el error no baja la nota. <em>El error es información.</em></p>
    <p class="say">Lo que sí cuenta es qué hiciste cuando apareció: si lo leíste, si lo buscaste, si lo arreglaste y si puedes contar cómo.</p>
   </div>
  </section>

  <section class="slide">
   <div class="inner">
    <p class="eyebrow">El laboratorio</p>
    <h2 class="mid">Tres reglas. Nada más.</h2>
    <div class="rules">
      <div class="rule"><span class="n">01</span>
        <h3>Intenta dos minutos antes de preguntar.</h3>
        <p>Pelea con el problema. Después levanta la mano. La ayuda llega igual, pero ya aprendiste algo en el camino.</p></div>
      <div class="rule"><span class="n">02</span>
        <h3>Nadie se ríe del error de otro.</h3>
        <p>El que hoy no entiende, en tres semanas está explicándole a alguien más. Siempre pasa. Siempre.</p></div>
      <div class="rule"><span class="n">03</span>
        <h3>Lo que construyes, lo explicas.</h3>
        <p>Si no lo puedes explicar con tus palabras, todavía no es tuyo. Y si lo puedes explicar, ya no se te olvida.</p></div>
    </div>
   </div>
  </section>

  <section class="slide">
   <div class="inner">
    <p class="eyebrow">Cómo se evalúa</p>
    <h2 class="mid">La nota se construye, no se salva al final.</h2>
    <div class="conej">
      <div>
        <p class="ev-pista">M&#193;RCALO Y MIRA C&#211;MO SUBE</p>
        <div class="bars" data-demo="eval">{bars}</div>
        <p class="ev-total">Llevas <b data-total>0</b>%</p>
        <p class="say">Tres cuartos de la nota se ganan cada semana, haciendo.</p>
      </div>
      <div class="vid-caja" data-demo="video" data-yt="{video_id}">
        <button class="vid" type="button" data-play>
          <img class="vid-mini" src="https://img.youtube.com/vi/{video_id}/hqdefault.jpg" alt="">
          <span class="vid-play" aria-hidden="true">&#9654;</span>
          <span class="vid-tit">{video_tit}</span>
        </button>
        <p class="vid-pie">Empezaron a tu edad.</p>
      </div>
    </div>
   </div>
  </section>

  <section class="slide">
   <div class="inner">
    <p class="eyebrow">Antes del reto</p>
    <h2 class="mid">Diez preguntas, para ver de dónde partimos.</h2>
    <p class="say">No cuenta para la nota. Sirve para saber qué hay que reforzar
      y qué se puede dar por sabido.</p>
    {s_quiz}
   </div>
  </section>

  <section class="slide">
   <div class="inner">
    <p class="eyebrow">El reto de hoy</p>
    {s7}
    <p class="go">Empezamos ahora.</p>
   </div>
  </section>

</main>

<div class="chrome bl"><span class="count" id="cnt">01 / __TOTAL_DIAPOS__</span></div>
<div class="chrome br">
  <button class="navb" id="prev" aria-label="Diapositiva anterior">&#8592;</button>
  <button class="navb" id="next" aria-label="Diapositiva siguiente">&#8594;</button>
</div>
{pag}

<script>{JS}{js_pag}{JS_INTER}</script>'''
    # El contador de antes de que corra el script. Estaba escrito a mano
    # («01 / 07») y se quedó atrás en cuanto el deck creció: se cuenta.
    total = pagina.count('<section class="slide">')
    return pagina.replace("__TOTAL_DIAPOS__", f"{total:02d}", 1)


if __name__ == "__main__":
    out = os.path.join(HERE, "salida", "presentacion-criso.html")
    open(out, "w", encoding="utf-8").write(build())
    print("escrito:", out, os.path.getsize(out), "bytes")
