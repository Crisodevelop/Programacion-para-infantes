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


show(desdeHash());

var CAPS=[{"t": "Empezar", "a": 0, "b": 1, "tecla": null}, {"t": "Aprender", "a": 2, "b": 8, "tecla": null}, {"t": "Jugar", "a": 9, "b": 11, "tecla": null}, {"t": "Construir", "a": 12, "b": 13, "tecla": null}, {"t": "Cerrar", "a": 14, "b": 17, "tecla": null}];
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
var CLASE={"nivel": "3ro", "semana": 5, "items": [{"id": "calent", "nombre": "Calentamiento", "pts": 5}, {"id": "teoria", "nombre": "¿Lo entendí?", "pts": 5}, {"id": "r1", "nombre": "Reto 1", "pts": 10}, {"id": "r2", "nombre": "Reto 2", "pts": 10}, {"id": "r3", "nombre": "Reto 3", "pts": 10}, {"id": "r4", "nombre": "Reto 4", "pts": 10}, {"id": "x1", "nombre": "Reto extra 1", "pts": 10}, {"id": "primera", "nombre": "Tu primera lista", "pts": 10}, {"id": "juego", "nombre": "Mini juego", "pts": 10}, {"id": "juego2", "nombre": "Otro juego", "pts": 10}, {"id": "practica", "nombre": "La práctica", "pts": 15}, {"id": "salida", "nombre": "Ticket de salida", "pts": 5}]};

(function(){
var SEN={signal:typeof senal!=='undefined'?senal:undefined};
function todos(r,q){return [].slice.call(r.querySelectorAll(q));}
function ver(r,q){return r.querySelector(q);}
function on(el,ev,fn){if(el)el.addEventListener(ev,fn,SEN);}
var QUIETO=false;try{QUIETO=matchMedia('(prefers-reduced-motion: reduce)').matches;}catch(e){}
var pausas=[],cambios=[],M={};
// Puntos: 10 por cada actividad que se resuelve por primera vez. La insignia
// sale cuando están todos los retos. Nada se guarda: al recargar, a cero.
// ── La nota de la clase ───────────────────────────────────────────────────
// Sin nombre elegido, la clase va en modo repaso: se juega, pero no se anota.
// Cuando el estudiante elige su nombre en la ventana (la pone la página), cada
// primer intento se guarda en esta PC y en la base, y lo de la base manda.
var NOTA={clave:null,hechos:{},id:null,codigo:null},chipP=null,insignia=false;
function hoyISO(){var d=new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');}
function totalNota(){var t=0;for(var k in NOTA.hechos)t+=NOTA.hechos[k];return Math.min(100,t);}
function corto(n){var p=String(n||'').trim().split(/\s+/);return p[0]+(p[1]?' '+p[1][0]+'.':'');}
function guardarNota(){
  if(!NOTA.clave)return;
  try{localStorage.setItem(NOTA.clave,JSON.stringify({hechos:NOTA.hechos,codigo:NOTA.codigo,t:Date.now()}));}catch(e){}
}
function subirNota(){
  if(!NOTA.id)return;
  document.dispatchEvent(new CustomEvent('nota:guardar',{detail:{detalle:NOTA.hechos,codigo:NOTA.codigo}}));
}
function identidad(d){
  NOTA.id=d;NOTA.clave='nota:'+CLASE.nivel+':'+CLASE.semana+':'+hoyISO()+':'+d.seccion;
  var local={};
  try{var g=JSON.parse(localStorage.getItem(NOTA.clave)||'null');if(g){local=g.hechos||{};NOTA.codigo=NOTA.codigo||g.codigo||null;}}catch(e){}
  // Lo que ya llevaba en esta PC pasa a su nombre; lo que ya estaba en la base, manda.
  NOTA.hechos=Object.assign({},NOTA.hechos,local,d.detalle||{});
  NOTA.codigo=NOTA.codigo||d.codigo||null;
  guardarNota();pintarNota();subirNota();
}
function etiquetaNota(n){
  if(n.dataset.notaTipo==='reto')return n;
  var sl=n.closest('.slide');return sl?sl.querySelector('.eyebrow'):null;
}
function pintarNota(){
  if(chipP)chipP.textContent=NOTA.id?'⭐ '+totalNota()+' / 100 · '+corto(NOTA.id.nombre):'Modo repaso';
  todos(document,'[data-nota]').forEach(function(n){
    var donde=etiquetaNota(n);if(!donde)return;
    var b=n.__vale;
    if(!b){b=document.createElement('span');b.className='a-vale';n.__vale=b;
      if(donde===n)n.insertBefore(b,n.firstChild);else donde.appendChild(b);}
    var id=n.dataset.nota,hecho=id in NOTA.hechos;
    b.textContent=hecho?NOTA.hechos[id]+' / '+n.dataset.pts+' pts'+(n.dataset.notaTipo==='reto'?' · ya contestado':''):'vale '+n.dataset.pts+' pts';
    b.classList.toggle('a-vale-hecho',hecho);
  });
  document.dispatchEvent(new CustomEvent('nota:pintar'));
}
function anotar(n,ok){
  if(!n||!n.dataset||!n.dataset.nota||!NOTA.id)return;   // en modo repaso no se anota
  var id=n.dataset.nota;if(id in NOTA.hechos)return;
  NOTA.hechos[id]=ok?+n.dataset.pts:0;guardarNota();pintarNota();subirNota();
  if(chipP&&ok){chipP.classList.remove('a-sube');void chipP.offsetWidth;chipP.classList.add('a-sube');}
  var retos=todos(document,'[data-nota-tipo=reto]');
  if(!insignia&&retos.length&&retos.every(function(x){return NOTA.hechos[x.dataset.nota]===+x.dataset.pts;})){
    insignia=true;
    var t=document.createElement('div');t.className='a-insignia';t.setAttribute('role','status');
    t.innerHTML='<b>🏅</b><span></span>';t.children[1].textContent='¡Insignia «Pythonista del día»! Todos los retos a la primera.';
    (document.querySelector('.deck')||document.body).appendChild(t);
    setTimeout(function(){t.remove();},5200);
  }
}
// Un juego da sus puntos cuando se resuelve de verdad: lo avisa cada motor.
function gana(r){anotar(r&&r.closest?r.closest('[data-nota]'):null,true);return true;}
function fb(caja,ok,texto){
  var n=caja&&caja.closest?caja.closest('[data-nota]'):null;
  if(n&&n.dataset.notaTipo==='reto'&&(ok===true||ok===false))anotar(n,ok);
  var p=ver(caja,'.a-fb');if(!p)return;
  p.textContent=ok===null?'':(ok?'✓ ':'✗ ')+texto;
  p.className='a-fb'+(ok===null?'':(ok?' a-bien':' a-mal'));
}

var P={
  err:function(tipo,msg){var e=new Error(msg);e.py=tipo+': '+msg;return e;},
  fstr:function(x){if(!isFinite(x))return isNaN(x)?'nan':(x>0?'inf':'-inf');return Number.isInteger(x)?x.toFixed(1):String(x);},
  repr:function(v){
    var t=v[0],x=v[1];
    if(t==='str')return "'"+String(x).replace(/\\/g,'\\\\').replace(/'/g,"\\'")+"'";
    if(t==='float')return P.fstr(x);
    if(t==='bool')return x?'True':'False';
    return String(x);
  },
  num:function(v){return v[0]==='int'||v[0]==='float'||v[0]==='bool';},
  conv:function(v,c){
    if(!c)return v;
    if(c==='int'){
      if(v[0]==='str'){var s=v[1].trim();if(!/^[+-]?\d+$/.test(s))throw P.err('ValueError',"invalid literal for int() with base 10: "+P.repr(v));return ['int',parseInt(s,10)];}
      return ['int',Math.trunc(Number(v[1]))];
    }
    if(v[0]==='str'){var f=v[1].trim();if(!/^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$/.test(f))throw P.err('ValueError',"could not convert string to float: "+P.repr(v));return ['float',parseFloat(f)];}
    return ['float',Number(v[1])];
  },
  op:function(a,o,b){
    if(a[0]==='str'||b[0]==='str'){
      if(o==='+'&&a[0]==='str'&&b[0]==='str')return ['str',a[1]+b[1]];
      if(o==='*'&&((a[0]==='str'&&b[0]==='int')||(a[0]==='int'&&b[0]==='str'))){
        var s=a[0]==='str'?a[1]:b[1],n=a[0]==='int'?a[1]:b[1];return ['str',n>0?s.repeat(n):''];
      }
      if(o==='+'&&a[0]==='str')throw P.err('TypeError','can only concatenate str (not "'+b[0]+'") to str');
      throw P.err('TypeError',"unsupported operand type(s) for "+o+": '"+a[0]+"' and '"+b[0]+"'");
    }
    var x=Number(a[1]),y=Number(b[1]),fl=a[0]==='float'||b[0]==='float',t=fl?'float':'int';
    if(y===0&&(o==='/'||o==='//'||o==='%'))
      throw P.err('ZeroDivisionError','division by zero');
    if(o==='+')return [t,x+y];
    if(o==='-')return [t,x-y];
    if(o==='*')return [t,x*y];
    if(o==='/')return ['float',x/y];
    if(o==='//')return [t,Math.floor(x/y)];
    if(o==='%')return [t,x-y*Math.floor(x/y)];
    throw P.err('SyntaxError','operador '+o);
  },
  eq:function(a,b){if(P.num(a)&&P.num(b))return Number(a[1])===Number(b[1]);return a[0]===b[0]&&a[1]===b[1];},
  json:function(v){
    if(v[0]==='str')return JSON.stringify(v[1]).replace(/[-￿]/g,function(c){return '\\u'+('000'+c.charCodeAt(0).toString(16)).slice(-4);});
    if(v[0]==='float')return P.fstr(v[1]);
    if(v[0]==='bool')return v[1]?'true':'false';
    return String(v[1]);
  },
  dumps:function(vars){return '{'+Object.keys(vars).map(function(k){return P.json(['str',k])+': '+P.json(vars[k]);}).join(', ')+'}';}
};

M.vota=function(r){
  var ops=todos(r,'.a-op'),rev=ver(r,'[data-revelar]'),pq=ver(r,'.a-porque');
  /* El calentamiento tiene respuesta correcta, así que cuenta como un reto:
     vale la PRIMERA que toca, igual que en los demás. Seguir tocando cambia
     lo marcado para el conteo a mano alzada, pero ya no cambia la nota. */
  var contado=false;
  ops.forEach(function(b){on(b,'click',function(){
    ops.forEach(function(o){o.setAttribute('aria-pressed',String(o===b));});
    if(!contado){contado=true;fb(r,b.hasAttribute('data-ok'),
      b.hasAttribute('data-ok')?'¡Esa es!':'Esa no era. Mira la explicación.');}
  });});
  on(rev,'click',function(){
    var abierto=r.dataset.revelado==='1';
    r.dataset.revelado=abierto?'0':'1';
    rev.textContent=abierto?'Revelar la respuesta':'Ocultar la respuesta';
    pq.hidden=abierto;
  });
};

M.notas=function(r){
  var notas=todos(r,'[data-marca]'),filas=todos(r,'.a-cod li');
  notas.forEach(function(n){on(n,'click',function(){
    var activa=n.getAttribute('aria-pressed')==='true';
    notas.forEach(function(x){x.setAttribute('aria-pressed',String(!activa&&x===n));});
    filas.forEach(function(li,k){li.classList.toggle('a-foco',!activa&&String(k+1)===n.dataset.marca);});
  });});
};

M.opciones=function(r){
  var ops=todos(r,'.a-op'),ex=ver(r,'.a-explica'),re=ver(r,'[data-reintentar]'),hueco=ver(r,'.a-hueco');
  function reset(){
    ops.forEach(function(o){o.disabled=false;o.removeAttribute('data-estado');});
    fb(r,null,'');ex.hidden=true;re.hidden=true;
    if(hueco){hueco.textContent='___';hueco.classList.remove('a-lleno');}
  }
  ops.forEach(function(b){on(b,'click',function(){
    var ok=b.hasAttribute('data-ok');
    b.setAttribute('data-estado',ok?'bien':'mal');
    if(ok){
      ops.forEach(function(o){o.disabled=true;});
      if(hueco){hueco.textContent=b.dataset.txt;hueco.classList.add('a-lleno');}
      fb(r,true,'¡Correcto!');ex.hidden=false;
    }else{
      b.disabled=true;fb(r,false,'Todavía no. Mira otra vez y prueba otra opción.');
    }
    re.hidden=false;
  });});
  on(re,'click',reset);
};

M.ordena=function(r){
  var lista=ver(r,'.a-orden'),bien=JSON.parse(r.dataset.orden),inicial=todos(lista,'li');
  var comp=ver(r,'[data-comprobar]'),re=ver(r,'[data-reintentar]');
  function filas(){return todos(lista,'li');}
  function botones(bloq){
    var fs=filas();
    fs.forEach(function(li,k){
      ver(li,'[data-sube]').disabled=bloq||k===0;
      ver(li,'[data-baja]').disabled=bloq||k===fs.length-1;
    });
  }
  on(lista,'click',function(e){
    var b=e.target.closest('button');if(!b)return;
    var li=b.closest('li');
    if(b.hasAttribute('data-sube')&&li.previousElementSibling)lista.insertBefore(li,li.previousElementSibling);
    else if(b.hasAttribute('data-baja')&&li.nextElementSibling)lista.insertBefore(li.nextElementSibling,li);
    filas().forEach(function(x){x.removeAttribute('data-estado');});
    fb(r,null,'');botones(false);
    if(!b.disabled)b.focus();
  });
  on(comp,'click',function(){
    var fs=filas(),n=0;
    fs.forEach(function(li,k){var ok=li.dataset.txt===bien[k];if(ok)n++;li.setAttribute('data-estado',ok?'bien':'mal');});
    re.hidden=false;
    if(n===fs.length){fb(r,true,'¡Todo en su sitio! Así se ejecuta en orden.');botones(true);comp.disabled=true;}
    else fb(r,false,n+' de '+fs.length+' en su sitio. Mueve las rojas.');
  });
  on(re,'click',function(){
    inicial.forEach(function(li){li.removeAttribute('data-estado');lista.appendChild(li);});
    fb(r,null,'');comp.disabled=false;re.hidden=true;botones(false);
  });
  botones(false);
};

M.error=function(r){
  var lin=todos(r,'.a-linea'),ex=ver(r,'.a-explica'),re=ver(r,'[data-reintentar]');
  lin.forEach(function(b){on(b,'click',function(){
    if(b.hasAttribute('data-mala')){
      b.setAttribute('data-estado','bien');lin.forEach(function(x){x.disabled=true;});
      fb(r,true,'¡La encontraste!');ex.hidden=false;
    }else{
      b.setAttribute('data-estado','mal');b.disabled=true;
      fb(r,false,'Esa está bien. Sigue buscando.');
    }
    re.hidden=false;
  });});
  on(re,'click',function(){
    lin.forEach(function(x){x.disabled=false;x.removeAttribute('data-estado');});
    fb(r,null,'');ex.hidden=true;re.hidden=true;
  });
};

M.salida=function(r){
  var b=ver(r,'[data-ver]'),resp=ver(r,'.a-resp'),ta=ver(r,'textarea'),vista=false;
  // Cuenta si escribieron su respuesta antes de mirar la buena.
  if(ta)on(ta,'input',function(){if(!vista&&ta.value.trim().length>=15)gana(r);});
  on(b,'click',function(){vista=true;resp.hidden=!resp.hidden;b.textContent=resp.hidden?'Ver una buena respuesta':'Ocultar la respuesta';});
};

M.nota=function(r){
  var tot=ver(r,'[data-total]'),lista=ver(r,'[data-desglose]'),quien=ver(r,'[data-quien]');
  function pintar(){
    tot.textContent=totalNota();lista.innerHTML='';
    CLASE.items.forEach(function(it){
      var v=NOTA.hechos[it.id],li=document.createElement('li');
      li.innerHTML='<span></span><b></b>';li.children[0].textContent=it.nombre;
      li.children[1].textContent=(v===undefined?'—':v)+' / '+it.pts;
      if(v===undefined)li.className='a-pendiente';lista.appendChild(li);
    });
    quien.textContent=NOTA.id
      ?'Se guarda sola a nombre de '+NOTA.id.nombre+'.'
      :'Modo repaso: esta nota no se guarda. Cuando el docente abra la clase, te saldrá la ventana para elegir tu nombre.';
  }
  on(document,'nota:pintar',pintar);
  pintar();
};

M.caza=function(r){
  var cfg=JSON.parse(r.dataset.cfg),n=cfg.nombre;
  var fila=ver(r,'[data-fila]'),preg=ver(r,'[data-preg]'),nums=ver(r,'[data-nums]');
  var pEl=ver(r,'[data-pts]'),rEl=ver(r,'[data-racha]'),roEl=ver(r,'[data-ronda]'),bOtra=ver(r,'[data-reiniciar]');
  // El plan es siempre el mismo para que la clase sepa qué viene; lo que
  // cambia en cada partida es a cuál de la fila apunta.
  var PLAN=['cual','donde','len','cual','cual','ultimo','donde','len'];
  var lista,ronda,pts,racha,actual,espera=null;
  function cita(x){return "'"+String(x)+"'";}
  function azar(m){return Math.floor(Math.random()*m);}

  function tarjetas(){
    fila.innerHTML='';
    lista.forEach(function(x,i){
      var b=document.createElement('button');b.type='button';b.className='a-caza-c';
      b.innerHTML='<span></span><i></i>';
      b.children[0].textContent=cita(x);b.children[1].textContent=i;
      b.addEventListener('click',function(){responder(i,b);},SEN);
      fila.appendChild(b);
    });
  }
  function chips(hasta){
    nums.innerHTML='';nums.hidden=false;
    for(var i=0;i<=hasta;i++)(function(v){
      var b=document.createElement('button');b.type='button';b.className='a-caza-n';b.textContent=v;
      b.addEventListener('click',function(){responder(v,b);},SEN);nums.appendChild(b);
    })(i);
  }
  function bloquear(si){
    todos(r,'.a-caza-c,.a-caza-n').forEach(function(b){b.disabled=si;});
  }

  function plantear(){
    r.dataset.ver='0';nums.hidden=true;nums.innerHTML='';
    todos(r,'.a-caza-c,.a-caza-n').forEach(function(b){b.removeAttribute('data-estado');});
    roEl.textContent=ronda+1;
    var tipo=PLAN[ronda%PLAN.length],i;
    if(tipo==='cual'){
      i=azar(lista.length);
      actual={tipo:tipo,donde:'fila',ok:i};
      preg.innerHTML='<code>&gt;&gt;&gt; '+n+'['+i+']</code> \u00b7 toca la que sale.';
    }else if(tipo==='ultimo'){
      actual={tipo:tipo,donde:'fila',ok:lista.length-1};
      preg.innerHTML='<code>&gt;&gt;&gt; '+n+'[-1]</code> \u00b7 toca la que sale.';
    }else if(tipo==='donde'){
      i=azar(lista.length);
      actual={tipo:tipo,donde:'nums',ok:i};
      preg.innerHTML='\u00bfEn qu\u00e9 posici\u00f3n est\u00e1 <code>'+cita(lista[i])+'</code>?';
      chips(lista.length);
    }else{
      actual={tipo:tipo,donde:'nums',ok:lista.length};
      preg.innerHTML='<code>&gt;&gt;&gt; len('+n+')</code> \u00b7 toca el n\u00famero.';
      chips(lista.length);
    }
    bloquear(false);
  }

  function explica(){
    var i=actual.ok,u=lista.length-1;
    if(actual.tipo==='cual')
      return n+'['+i+'] es la '+(i+1)+'\u00aa: se cuenta '+lista.map(function(_,k){return k;}).slice(0,i+1).join(', ')+'.';
    if(actual.tipo==='ultimo')
      return 'La \u00faltima es '+n+'['+u+'], porque hay '+lista.length+' y se empieza en 0.';
    if(actual.tipo==='donde')
      return cita(lista[i])+' est\u00e1 en la posici\u00f3n '+i
        +(i===0?': es la primera, antes no hay ninguna.':': antes hay '+(i===1?'una':i)+'.');
    return 'Hay '+lista.length+', as\u00ed que len da '+lista.length+'. La \u00faltima es '+n+'['+u+'].';
  }

  function responder(v,b){
    if(espera)return;
    bloquear(true);r.dataset.ver='1';
    var ok=v===actual.ok;
    b.setAttribute('data-estado',ok?'bien':'mal');
    if(!ok){
      var caja=actual.donde==='fila'?fila:nums;
      var buena=todos(caja,'button')[actual.ok];
      if(buena)buena.setAttribute('data-estado','bien');
    }
    if(ok){pts++;racha++;}else{racha=0;}
    pEl.textContent=pts;rEl.textContent=racha;
    fb(r,ok,(ok?'\u00a1Bien! ':'')+explica());
    espera=setTimeout(function(){espera=null;ronda++;siguiente();},QUIETO?300:1500);
  }

  function siguiente(){
    if(ronda>=cfg.rondas){
      // La fila se queda a la vista con los n\u00fameros puestos: lo \u00faltimo que
      // ven es la lista entera numerada, que es lo que hay que recordar.
      nums.hidden=true;preg.textContent='';
      r.dataset.ver='1';bloquear(true);bOtra.hidden=false;
      if(pts>=cfg.gana){gana(r);fb(r,true,'\u00a1Cazadas! '+pts+' de '+cfg.rondas+'.');}
      else fb(r,false,pts+' de '+cfg.rondas+'. Con '+cfg.gana+' se gana: otra vuelta.');
      return;
    }
    // A mitad de partida entra una m\u00e1s: se ve que las posiciones corren.
    if(ronda===Math.floor(cfg.rondas/2)&&cfg.extra.length){
      lista.push(cfg.extra.shift());
      tarjetas();r.dataset.ver='1';
      preg.innerHTML='<code>&gt;&gt;&gt; '+n+'.append('+cita(lista[lista.length-1])+')</code>';
      nums.hidden=true;bloquear(true);
      espera=setTimeout(function(){espera=null;plantear();},QUIETO?300:1600);
      return;
    }
    plantear();
  }

  function empezar(){
    clearTimeout(espera);espera=null;
    cfg=JSON.parse(r.dataset.cfg);
    lista=cfg.inicial.slice();ronda=0;pts=0;racha=0;
    pEl.textContent='0';rEl.textContent='0';bOtra.hidden=true;fb(r,null,'');
    tarjetas();plantear();
  }
  on(bOtra,'click',empezar);
  pausas.push(function(){clearTimeout(espera);espera=null;});
  if(SEN.signal)SEN.signal.addEventListener('abort',function(){clearTimeout(espera);});
  empezar();
};

M.carrera=function(r){
  var cfg=JSON.parse(r.dataset.cfg),Q=cfg.preguntas,bIni=ver(r,'[data-empezar]'),zona=ver(r,'[data-zona]'),pr=ver(r,'[data-preg]');
  var ops=ver(r,'[data-ops]'),tEl=ver(r,'[data-t]'),pEl=ver(r,'[data-pts]'),rEl=ver(r,'[data-racha]');
  var t=null,resta=0,pts=0,racha=0,mejor=0,cola=[],actual=null;
  function barajar(a){for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),x=a[i];a[i]=a[j];a[j]=x;}return a;}
  function sig(){
    if(!cola.length)cola=barajar(Q.map(function(_,k){return k;}));
    actual=Q[cola.pop()];pr.textContent=actual.pregunta;ops.innerHTML='';
    barajar(actual.opciones.map(function(_,k){return k;})).forEach(function(k,pos){
      var b=document.createElement('button');b.type='button';b.className='a-op';b.innerHTML='<span class="a-letra"></span><span></span>';
      b.children[0].textContent='ABCD'[pos];b.children[1].textContent=actual.opciones[k];
      b.addEventListener('click',function(){responder(k===actual.correcta,b);},SEN);ops.appendChild(b);
    });
  }
  function responder(ok,b){
    if(!t)return;todos(ops,'button').forEach(function(x){x.disabled=true;});b.setAttribute('data-estado',ok?'bien':'mal');
    if(ok){pts++;racha++;mejor=Math.max(mejor,racha);fb(r,true,'¡Bien! Racha de '+racha+'.');}else{racha=0;fb(r,false,'Esa no era.');}
    pEl.textContent=pts;rEl.textContent=racha;setTimeout(function(){if(t)sig();},QUIETO?150:650);
  }
  function detener(texto){clearInterval(t);t=null;zona.hidden=true;bIni.hidden=false;bIni.textContent=texto;}
  on(bIni,'click',function(){
    pts=0;racha=0;mejor=0;pEl.textContent='0';rEl.textContent='0';resta=cfg.segundos;tEl.textContent=resta;cola=[];
    zona.hidden=false;bIni.hidden=true;fb(r,null,'');
    t=setInterval(function(){resta--;tEl.textContent=resta;if(resta<=0){detener('▶ Otra carrera');
      (pts>=Math.ceil(Q.length/2)&&gana(r)),fb(r,true,'¡Tiempo! '+pts+(pts===1?' acierto':' aciertos')+' · mejor racha: '+mejor+'.');}},1000);
    sig();
  });
  pausas.push(function(){if(t)detener('▶ Empezar la carrera');});
};

M.taller=function(r){
  var cfg=JSON.parse(r.dataset.cfg),mis=cfg.misiones,k=0,hechas=[];
  var inp=ver(r,'[data-linea]'),prog=ver(r,'[data-prog]'),sale=ver(r,'[data-sale]'),ops=ver(r,'[data-ops]');

  /* ── Comprobadores: cada uno devuelve [queja, loQueHizo] ───────────────── */
  function num(x){return /^-?\d+$/.test(String(x).trim());}
  function val(x){ // "18" -> 18 ; "\"Ana\"" -> Ana (texto)
    x=String(x).trim();
    if(num(x))return parseInt(x,10);
    var m=x.match(/^["'](.*)["']$/);
    return m?m[1]:null;
  }
  // En el aula la tilde no es el tema: «Sofia» y «Sofía» valen lo mismo, y la
  // lista se queda con lo que el estudiante escribió.
  function pelado(x){return String(x).normalize('NFD').replace(/[\u0300-\u036f]/g,'');}
  function mismo(a,b){return String(a)===String(b)||pelado(a)===pelado(b);}
  // Las listas se enseñan como las escribe Python, no como las escribe JSON:
  // el enunciado dice ['Ana', 'Luis'] y la queja tiene que decir lo mismo.
  function pyLista(l){
    return '['+l.map(function(x){return typeof x==='number'?String(x):"'"+x+"'";}).join(', ')+']';
  }
  function compara(a,op,b){
    if(a===null||b===null)return null;
    switch(op){case '==':return a===b;case '!=':return a!==b;
      case '>':return a>b;case '<':return a<b;case '>=':return a>=b;case '<=':return a<=b;}
    return null;
  }
  var CHK={
    // if <variable> <op> <valor>:   se prueba contra la tabla de la misión
    condicion:function(t,m){
      t=t.trim();
      if(!/^if\b/.test(t))return ['Una decisión empieza con if.',null];
      if(!/:\s*$/.test(t))return ['Falta los dos puntos al final.',null];
      var c=t.replace(/^if\s+/,'').replace(/:\s*$/,'').trim();
      if(/[^!<>=]=[^=]/.test(c))return ['Con un solo = se guarda. Para comparar van dos: ==.',null];
      var mm=c.match(/^([A-Za-z_][A-Za-z0-9_.]*)\s*(==|!=|>=|<=|>|<)\s*(.+)$/);
      if(!mm)return ['Escribe una sola comparación: variable, comparador y valor.',null];
      if(mm[1]!==m.variable)return ['La variable de esta misión es '+m.variable+'.',null];
      var b=val(mm[3]);
      if(b===null)return ['El valor va tal cual (18) o entre comillas ("Ana").',null];
      var pasa=[],fallo=null;
      for(var i=0;i<m.casos.length;i++){
        var a=val(String(m.casos[i])), res=compara(a,mm[2],b);
        if(res===null)return ['No puedo comparar '+m.casos[i]+' con eso.',null];
        if(res)pasa.push(m.casos[i]);
        if(res!==!!m.espera[i]&&fallo===null)
          fallo=m.casos[i]+(res?' pasa y no debía':' no pasa y debía');
      }
      if(fallo)return ['Con lo tuyo, '+fallo+'.',pasa];
      return [null,pasa];
    },
    // una operación sobre la lista de partida
    lista:function(t,m){
      t=t.trim();
      var l=(m.lista||[]).slice(),nom=m.variable;
      var ap=t.match(new RegExp('^'+nom+'\\.append\\(\\s*(.+?)\\s*\\)$'));
      var qu=t.match(new RegExp('^'+nom+'\\.remove\\(\\s*(.+?)\\s*\\)$'));
      var as=t.match(new RegExp('^'+nom+'\\s*\\[\\s*(-?\\d+)\\s*\\]\\s*=\\s*(.+)$'));
      var cr=t.match(new RegExp('^'+nom+'\\s*=\\s*\\[(.*)\\]$'));
      if(ap){var v=val(ap[1]);if(v===null)return ['El valor va entre comillas si es texto.',null];l.push(v);}
      else if(qu){var q=val(qu[1]),iq=l.findIndex(function(x){return mismo(x,q);});
        if(iq<0)return ['En la lista no hay ningún '+qu[1]+'.',l];l.splice(iq,1);}
      else if(as){var i=parseInt(as[1],10),v2=val(as[2]);
        if(i<0||i>=l.length)return ['La posición '+i+' no existe: la lista va de 0 a '+(l.length-1)+'.',l];
        if(v2===null)return ['El valor va entre comillas si es texto.',l];l[i]=v2;}
      else if(cr){l=cr[1].trim()?cr[1].split(',').map(function(x){return val(x);}):[];
        if(l.some(function(x){return x===null;}))return ['Dentro de los corchetes, los textos van entre comillas.',null];}
      else return ['Usa '+nom+' con [ ], .append( ) o .remove( ).',null];
      var bien=l.length===m.espera.length&&l.every(function(x,i){return mismo(x,m.espera[i]);});
      if(!bien)return ['Te queda '+pyLista(l)+' y hace falta '+pyLista(m.espera)+'.',l];
      return [null,l];
    },
    // def nombre(parámetros):
    funcion:function(t,m){
      t=t.trim();
      if(!/^def\b/.test(t))return ['Una función empieza con def.',null];
      if(!/:\s*$/.test(t))return ['Falta los dos puntos al final de la cabecera.',null];
      var mm=t.match(/^def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)\s*:$/);
      if(!mm)return ['Después del nombre van los paréntesis: def saluda(nombre):',null];
      if(mm[1]!==m.nombre)return ['Esta función se tiene que llamar '+m.nombre+'.',null];
      var ps=mm[2].trim()?mm[2].split(',').map(function(x){return x.trim();}):[];
      var esp=m.parametros||[];
      if(ps.length!==esp.length||ps.some(function(x,i){return x!==esp[i];}))
        return ['Entre paréntesis van '+(esp.length?esp.join(', '):'ninguno')+', y escribiste '+(ps.length?ps.join(', '):'ninguno')+'.',ps];
      return [null,ps];
    },
    // @when("click", "#boton")
    evento:function(t,m){
      t=t.trim();
      if(!/^@when\b/.test(t))return ['Empieza con @when, que es quien engancha el botón.',null];
      var mm=t.match(/^@when\s*\(\s*["'](\w+)["']\s*,\s*["']([^"']+)["']\s*\)$/);
      if(!mm)return ['Van dos cosas entre comillas: @when("click", "#boton").',null];
      if(mm[1]!==(m.evento||'click'))return ['El evento de esta misión es "'+(m.evento||'click')+'".',null];
      if(mm[2]!=='#'+m.id)return ['Ese es otro botón. El de esta misión es "#'+m.id+'".',mm[2]];
      return [null,'#'+m.id];
    },
    // random.randint(a, b) / random.choice(lista)
    azar:function(t,m){
      t=t.trim();
      if(!/^random\./.test(t))return ['Empieza con random., que es la caja del azar.',null];
      if(m.tipo==='choice'){
        var mc=t.match(/^random\.choice\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)$/);
        if(!mc)return ['Para elegir de una lista: random.choice(lista).',null];
        if(mc[1]!==m.variable)return ['La lista de esta misión se llama '+m.variable+'.',null];
        return [null,'uno de '+pyLista(m.lista)];
      }
      var mr=t.match(/^random\.randint\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)$/);
      if(!mr)return ['Para un número al azar: random.randint(desde, hasta).',null];
      var a=parseInt(mr[1],10),b=parseInt(mr[2],10);
      if(a>b)return ['El desde tiene que ser menor que el hasta.',null];
      if(a!==m.desde||b!==m.hasta){
        var tira=[];for(var i=0;i<6;i++)tira.push(a+Math.floor(Math.random()*(b-a+1)));
        return ['Lo tuyo saca de '+a+' a '+b+' ('+tira.join(', ')+'…) y hacen falta de '+m.desde+' a '+m.hasta+'.',tira];
      }
      var t2=[];for(var j=0;j<6;j++)t2.push(a+Math.floor(Math.random()*(b-a+1)));
      return [null,t2];
    },
    // una etiqueta de HTML: la lee el navegador
    etiqueta:function(t,m){
      t=t.trim();
      if(!/^</.test(t))return ['Una etiqueta empieza con <.',null];
      var d=document.createElement('div');d.innerHTML=t;
      var el=d.firstElementChild;
      if(!el)return ['El navegador no entiende eso como una etiqueta.',null];
      if(d.childNodes.length>1||el.outerHTML.replace(/\s+/g,'')!==t.replace(/\s+/g,''))
        return ['Escribe una sola etiqueta, abierta y cerrada: <'+m.etiqueta+'>…</'+m.etiqueta+'>',null];
      if(el.tagName.toLowerCase()!==m.etiqueta)
        return ['Esa es una etiqueta <'+el.tagName.toLowerCase()+'> y hace falta <'+m.etiqueta+'>.',el.tagName.toLowerCase()];
      if(m.texto&&!mismo(el.textContent.trim(),m.texto))
        return ['Dentro tiene que decir exactamente: '+m.texto,el.textContent.trim()];
      return [null,el.tagName.toLowerCase()+' · '+el.textContent.trim()];
    },
    // una respuesta que solo puede ser una
    exacto:function(t,m){
      var a=pelado(t.trim().replace(/\s+/g,' ').toLowerCase());
      var ok=(m.espera||[]).some(function(x){return pelado(String(x).trim().replace(/\s+/g,' ').toLowerCase())===a;});
      if(!a)return ['Escribe tu respuesta.',null];
      if(!ok)return ['Escribiste «'+t.trim()+'». '+(m.ayuda||'Mira otra vez el programa.'),t.trim()];
      return [null,t.trim()];
    }
  };

  /* ── El esqueleto, igual para todos ────────────────────────────────────── */
  function texto(m){return CHK[cfg.tipo]?CHK[cfg.tipo](inp.value,m):['Falta el comprobador.',null];}
  // Lo que hace su línea, dibujado: el que no se ve no se entiende.
  var vista=ver(r,'[data-vista]');
  function cajas(html){vista.hidden=!html;vista.innerHTML=html||'';}
  function esc(t){return String(t).replace(/[&<>]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c];});}
  function pintarVista(m,res){
    if(!m){cajas('');return;}
    if(cfg.tipo==='condicion'){
      var h='<p class="a-etq">Los valores de '+esc(m.variable)+' que llegan</p><div class="a-tl-fila">';
      for(var i=0;i<m.casos.length;i++){
        var debe=!!m.espera[i], hizo=res?res.indexOf(m.casos[i])>=0:null;
        var estado=hizo===null?(debe?'pasa':'no'):(hizo===debe?(hizo?'pasa':'no'):'mal');
        var marca=hizo===null?(debe?'✓':'✕'):(hizo?'✓':'✕');
        h+='<div class="a-tl-caso" data-r="'+estado+'"><i>'+marca+'</i><b>'+esc(m.casos[i])+'</b>'
          +'<span>'+(debe?'debe pasar':'no debe')+'</span></div>';
      }
      cajas(h+'</div>');return;
    }
    if(cfg.tipo==='lista'){
      var l=res||m.lista||[], h2='<p class="a-etq">'+esc(m.variable)+'</p><div class="a-tl-fila">';
      if(!l.length)h2+='<span class="a-tl-ficha">(vacía)</span>';
      for(var j2=0;j2<l.length;j2++)h2+='<span class="a-tl-ficha">'+esc(l[j2])+'</span>';
      cajas(h2+'</div>');return;
    }
    if(cfg.tipo==='azar'){
      if(!res){cajas('<p class="a-etq">Tiradas</p><div class="a-tl-fila">'
        +'<span class="a-tl-dado">?</span><span class="a-tl-dado">?</span><span class="a-tl-dado">?</span></div>');return;}
      var t=Array.isArray(res)?res:[res], h3='<p class="a-etq">Seis tiradas de tu línea</p><div class="a-tl-fila">';
      for(var i3=0;i3<t.length;i3++)h3+='<span class="a-tl-dado">'+esc(t[i3])+'</span>';
      cajas(h3+'</div>');return;
    }
    cajas('');
  }
  /* El esqueleto de ESTA misión: se ve la variable y la forma, pero no la
     respuesta. Antes el campo proponía siempre el mismo ejemplo y en la misión
     de la nota seguía diciendo «edad»: fallaban por eso, no por el tema. */
  function esqueleto(m){
    if(m.ejemplo)return m.ejemplo;
    if(cfg.tipo==='condicion')return 'if '+m.variable+' … :';
    if(cfg.tipo==='lista')return m.variable+' …';
    if(cfg.tipo==='funcion')return 'def '+m.nombre+'(…):';
    if(cfg.tipo==='evento')return '@when("click", "#…")';
    if(cfg.tipo==='azar')return m.tipo==='choice'?'random.choice(…)':'random.randint(…, …)';
    if(cfg.tipo==='etiqueta')return '<…>…</…>';
    return 'Escribe tu respuesta';
  }
  var fallos=0,dice=ver(r,'[data-dice]'),bPista=ver(r,'[data-pista]');
  function verPista(si){
    if(!bPista)return;
    dice.hidden=!si;bPista.hidden=si;
  }
  function pintar(){
    var fin=k>=mis.length,m=mis[Math.min(k,mis.length-1)];
    pintarVista(fin?null:m,null);
    if(bPista){
      dice.textContent=m&&m.pista?m.pista:'';
      bPista.hidden=fin||!m||!m.pista;dice.hidden=true;
    }
    ver(r,'[data-num]').textContent=fin?'¡Completo!':'Misión '+(k+1)+' de '+mis.length;
    ver(r,'[data-pide]').textContent=fin?'Hiciste las '+mis.length+' sin ayuda.':m.pide;
    prog.textContent=hechas.length?hechas.join('\n'):'# aquí va apareciendo lo tuyo';
    ver(r,'[data-barra]').style.setProperty('--p',Math.round(k*100/mis.length)+'%');
    if(inp){
      inp.disabled=fin;ver(r,'[data-probar]').disabled=fin;
      if(m&&!fin){
        inp.placeholder=esqueleto(m);
        ver(r,'[data-forma]').innerHTML='Tu línea va así: <code>'+esc(esqueleto(m))+'</code>';
      }
    }
    sale.innerHTML=fin?'':(m.sale?'Tiene que dar: <b>'+m.sale+'</b>':'');
    if(ops)pintarOps(fin?null:m);
  }
  function avanza(linea,hizo,texto_ok){
    hechas.push(linea);k++;fallos=0;
    if(inp)inp.value='';
    if(k>=mis.length){gana(r);fb(r,true,'¡Completo! '+(cfg.cierre||'Ya te sale sin ayuda.'));}
    // Con el número delante se sabe de qué misión habla; y en cuanto empiezan
    // a escribir la siguiente, se va.
    else fb(r,true,'Misión '+k+' lista. '+(texto_ok||('Bien: '+hizo)));
    pintar();verPista(false);
    if(inp&&k<mis.length)inp.focus();
  }
  // Lo que hizo su línea, dicho como se diría en voz alta.
  function muestra(v){
    if(v===null||v===undefined)return '';
    if(Array.isArray(v))return v.length?v.map(function(x){return String(x);}).join(', '):'(nada)';
    return String(v);
  }
  function probar(){
    if(k>=mis.length)return;
    var res=texto(mis[k]);
    if(res[0]){
      fb(r,false,res[0]);pintarVista(mis[k],res[1]);
      // Quien va bien no ve la pista; quien se traba de verdad —tres intentos—,
      // no se queda clavado.
      if(++fallos>=3&&mis[k].pista)verPista(true);
      return;
    }
    var hizo=muestra(res[1]);
    avanza(inp.value.trim(),hizo,hizo?'Bien: '+hizo+'.':'Bien.');
  }
  /* Las dos misiones que no se escriben: tocar en orden, o elegir el grupo. */
  function pintarOps(m){
    if(!m){ops.innerHTML='';return;}
    var lista=cfg.tipo==='ordenar'?m.pasos:m.grupos;
    ops.innerHTML='';
    lista.forEach(function(txt,i){
      var b=document.createElement('button');
      b.type='button';b.className='a-tl-op';b.textContent=txt;b.dataset.i=i;
      on(b,'click',function(){tocar(m,b,i);});
      ops.appendChild(b);
    });
    if(cfg.tipo==='ordenar')ops.dataset.van='0';
  }
  function tocar(m,b,i){
    if(cfg.tipo==='clasificar'){
      var bien=i===m.correcto;
      b.dataset.estado=bien?'bien':'mal';
      if(!bien){fb(r,false,m.porque||'Ese no es. Mira otra vez el ejemplo.');return;}
      todos(r,'.a-tl-op').forEach(function(x){x.disabled=true;});
      avanza(m.pide+' → '+m.grupos[i],m.grupos[i],'Bien: '+m.grupos[i]+'.');
      return;
    }
    var van=parseInt(ops.dataset.van||'0',10);
    if(i!==m.orden[van]){
      b.dataset.estado='mal';
      fb(r,false,'Ese no va '+(van===0?'primero':'ahora')+'. Piensa qué hace falta antes.');
      setTimeout(function(){b.removeAttribute('data-estado');},700);
      return;
    }
    b.dataset.estado='bien';b.disabled=true;b.textContent=(van+1)+'. '+b.textContent;
    ops.dataset.van=String(van+1);
    if(van+1>=m.orden.length)avanza(m.pide,'en orden','Ese es el orden.');
    else fb(r,true,'Va bien. ¿Y ahora?');
  }
  if(inp){
    on(ver(r,'[data-probar]'),'click',probar);
    on(inp,'keydown',function(e){if(e.key==='Enter'){e.preventDefault();probar();}});
    on(inp,'input',function(){var p=ver(r,'.a-fb');if(p&&p.textContent)fb(r,null,'');});
  }
  if(bPista)on(bPista,'click',function(){verPista(true);});
  function reiniciar(){k=0;hechas=[];fallos=0;if(inp)inp.value='';fb(r,null,'');pintar();verPista(false);}
  on(ver(r,'[data-reiniciar]'),'click',reiniciar);
  pausas.push(function(){fb(r,null,'');});
  pintar();
};

M.editor=function(r){
  var cfg=JSON.parse(r.dataset.cfg),ta=ver(r,'[data-codigo]'),marco=ver(r,'[data-marco]');
  var valores={py:cfg.py,html:cfg.html,css:cfg.css},tab=cfg.inicio;
  /* Arrancar Python cuesta: la primera vez baja unos 6 MB (Pyodide) y en una
     máquina del aula son decenas de segundos. Así que el marco se abre VACÍO
     en cuanto se llega a la diapositiva —mientras el docente explica— y cada
     Ejecutar solo le manda el programa nuevo por postMessage, sin recargar:
     de ~2 s por tirada a ~0,1 s. Si la tirada anterior no contestó (un ciclo
     infinito deja Python colgado) la siguiente recarga la página entera. */
  var CALIENTE='/editor.html?v='+encodeURIComponent(cfg.v);
  var slide=r.closest('.slide'),corrio=false,vivo=false,pendiente=false;
  function mostrar(k){
    valores[tab]=ta.value;tab=k;ta.value=valores[k];
    todos(r,'[data-tab]').forEach(function(b){b.setAttribute('aria-selected',String(b.dataset.tab===k));});
  }
  todos(r,'[data-tab]').forEach(function(b){on(b,'click',function(){mostrar(b.dataset.tab);});});
  function paquete(){
    valores[tab]=ta.value;
    var d={v:cfg.v,css:valores.css,html:valores.html,py:valores.py};
    return btoa(unescape(encodeURIComponent(JSON.stringify(d))));
  }
  function calentar(){
    /* Arrancar Python mueve varios megas y los compila: en Safari eso traba el
       hilo principal, y como la diapositiva entra con una animación por hijo,
       lo que se veía era media diapositiva congelada. Así que el marco no se
       enciende en el mismo momento de llegar: se espera a que la entrada
       termine y a que el navegador esté libre. */
    if(marco.getAttribute('src'))return;
    var ir=function(){if(!marco.getAttribute('src')){vivo=false;pendiente=false;marco.src=CALIENTE;}};
    setTimeout(function(){
      if(window.requestIdleCallback)requestIdleCallback(ir,{timeout:4000});else ir();
    },900);
  }
  function decir(m){try{marco.contentWindow.postMessage(m,location.origin);return true;}catch(e){return false;}}
  function duro(b){
    vivo=false;pendiente=false;
    marco.src='/editor.html?n='+Date.now()+'#'+b;
    fb(r,true,'Ejecutando… la primera vez tarda unos segundos en cargar Python.');
  }
  function correr(){
    var b=paquete();
    NOTA.codigo=JSON.stringify({py:valores.py,html:valores.html,css:valores.css});
    guardarNota();subirNota();
    gana(r);            // la práctica puntúa por hacerla: con ejecutarla basta

    corrio=true;
    if(vivo&&!pendiente&&decir({editor:'corre',codigo:b})){
      pendiente=true;fb(r,true,'Ejecutando…');return;
    }
    duro(b);
  }
  on(window,'message',function(e){
    if(e.origin!==location.origin||!e.data||e.source!==marco.contentWindow)return;
    if(e.data.editor==='aqui'){vivo=true;pendiente=false;}
    else if(e.data.editor==='listo')pendiente=false;
  });
  function limpiar(){
    /* Al salir de la diapositiva el programa se va; Python se queda caliente.
       Si el programa traía <script> (la cámara de la IA) se recarga el marco:
       apagar la cámara de verdad importa más que ahorrar el arranque. */
    if(!corrio)return;
    corrio=false;
    if(/<script/i.test(valores.html||'')||!vivo||pendiente){vivo=false;pendiente=false;marco.src=CALIENTE;}
    else decir({editor:'limpia'});
  }
  on(ver(r,'[data-correr]'),'click',correr);
  // La cámara de Teachable Machine a veces no arranca dentro de un marco.
  on(ver(r,'[data-completa]'),'click',function(){window.open('/editor.html#'+paquete(),'_blank','noopener');});
  on(ver(r,'[data-volver]'),'click',function(){
    valores={py:cfg.py,html:cfg.html,css:cfg.css};ta.value=valores[tab];limpiar();fb(r,null,'');
  });
  ta.value=valores[tab];
  function cerca(){
    /* Se calienta en cuanto la clase pasa de la portada, no al acercarse al
       editor.

       Arrancar Python mueve varios megas y los compila, y eso tiene que caer
       mientras el docente explica la teoría, que no tiene nada que tocar.
       Antes empezaba dos diapositivas antes del editor, y cuando se escribió
       eso, dos antes era la teoría; después se añadieron el taller y el
       segundo juego y «dos antes» pasó a ser justo encima del mini juego: la
       clase se quedaba frisada ahí, con el juego ya en pantalla. */
    if(!slide)return true;
    var ss=[].slice.call(document.querySelectorAll('.slide'));
    var hay=ss.indexOf(slide),ahora=ss.findIndex(function(x){return x.classList.contains('on');});
    // El `hay-2` queda de red por si alguna semana trae el editor pegado al
    // principio y la teoría no llega a la segunda diapositiva.
    return ahora<0||ahora>=Math.min(2,Math.max(hay-2,0));
  }
  cambios.push(function(){if(cerca())calentar();});
  if(cerca())calentar();
  pausas.push(limpiar);
};

(function(){
  var bl=document.querySelector('.chrome.bl');if(!bl)return;
  chipP=document.createElement('span');chipP.className='a-puntos';chipP.setAttribute('aria-live','polite');
  bl.appendChild(chipP);
  if(SEN.signal)SEN.signal.addEventListener('abort',function(){chipP.remove();});
})();
pintarNota();
// La página pone la ventana del nombre y habla con la base; aquí se escucha.
on(document,'clase:identidad',function(e){identidad(e.detail||{});});
on(document,'clase:guardado',function(e){
  var d=e.detail||{};
  if(d.detalle){NOTA.hechos=Object.assign({},NOTA.hechos,d.detalle);guardarNota();pintarNota();}
});
// Desmarcado por el docente: vuelve la ventana, y lo hecho sigue en esta PC.
on(document,'clase:desmarcado',function(){NOTA.id=null;pintarNota();});
document.dispatchEvent(new CustomEvent('clase:pregunta'));
// Las demos no tienen final: cuentan al usarlas.
todos(document,'[data-nota-tipo=demo]').forEach(function(n){on(n,'click',function(){gana(n);});});

M.hecho=function(r){
  /* La práctica sin editor (la desenchufada y la de enlace) no tiene nada que
     ejecutar: el punto se lo da el estudiante al marcar que la terminó. Es
     participación, no corrección, y por eso solo se puede marcar una vez. */
  var b=ver(r,'[data-hecho]');
  on(b,'click',function(){b.disabled=true;b.textContent='✓ Terminada';gana(r);});
};

M.imprimir=function(r){on(ver(r,'[data-imprimir]'),'click',function(){window.print();});};

todos(document,'[data-act]').forEach(function(r){
  var f=M[r.dataset.act];if(!f)return;
  try{f(r);}catch(e){console.error('[actividades]',r.dataset.act,e);}
});

// Al cambiar de diapositiva: los juegos se detienen y lo que mira la
// diapositiva en curso (el precalentado de Python) se vuelve a preguntar.
if(typeof show==='function'){
  var mostrarAct=show,relojYa=null;
  show=function(n){
    mostrarAct(n);
    pausas.forEach(function(f){try{f();}catch(e){}});
    cambios.forEach(function(f){try{f();}catch(e){}});
    // Si la entrada se queda a medias porque el navegador se trabó, al segundo
    // y pico se apaga la animación y la diapositiva se ve entera igual.
    clearTimeout(relojYa);
    todos(document,'.slide.a-ya').forEach(function(s){s.classList.remove('a-ya');});
    relojYa=setTimeout(function(){
      var s=document.querySelector('.slide.on');if(s)s.classList.add('a-ya');
    },1300);
  };
}

// El panel del guion: fuera de la proyección, cerrado hasta que se abre.
(function(){
  var btn=document.querySelector('.a-guion-btn'),panel=document.querySelector('.a-guion');
  if(!btn||!panel)return;
  var cerrar=ver(panel,'[data-cerrar]');
  function abrir(v){panel.hidden=!v;btn.setAttribute('aria-expanded',String(v));(v?cerrar:btn).focus();}
  on(btn,'click',function(){abrir(panel.hidden);});
  on(cerrar,'click',function(){abrir(false);});
  // Dentro del panel las teclas son del panel: ni flechas ni espacio pasan diapositivas.
  on(panel,'keydown',function(e){e.stopPropagation();if(e.key==='Escape')abrir(false);});
})();

// Con «Apagar los juegos» del docente, lo que esté corriendo se detiene.
try{
  var obs=new MutationObserver(function(){
    if(document.documentElement.getAttribute('data-bloqueo')==='juegos')
      pausas.forEach(function(f){try{f();}catch(e){}});
  });
  obs.observe(document.documentElement,{attributes:true,attributeFilter:['data-bloqueo']});
  if(SEN.signal)SEN.signal.addEventListener('abort',function(){obs.disconnect();});
}catch(e){}
})();