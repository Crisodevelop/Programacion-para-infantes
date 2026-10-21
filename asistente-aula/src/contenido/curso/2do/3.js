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
var CLASE={"nivel": "2do", "semana": 3, "items": [{"id": "calent", "nombre": "Calentamiento", "pts": 5}, {"id": "teoria", "nombre": "¿Lo entendí?", "pts": 5}, {"id": "r1", "nombre": "Reto 1", "pts": 10}, {"id": "r2", "nombre": "Reto 2", "pts": 10}, {"id": "r3", "nombre": "Reto 3", "pts": 10}, {"id": "r4", "nombre": "Reto 4", "pts": 10}, {"id": "x1", "nombre": "Reto extra 1", "pts": 10}, {"id": "x2", "nombre": "Reto extra 2", "pts": 10}, {"id": "primera", "nombre": "Tu primer ciclo", "pts": 10}, {"id": "juego", "nombre": "Mini juego", "pts": 10}, {"id": "juego2", "nombre": "Otro juego", "pts": 10}, {"id": "practica", "nombre": "La práctica", "pts": 15}, {"id": "salida", "nombre": "Ticket de salida", "pts": 5}]};

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

M.bucle=function(r){
  var tr=JSON.parse(r.dataset.traza),cuerpo=ver(r,'tbody'),res=ver(r,'[data-res]'),bs=ver(r,'[data-sig]'),bt=ver(r,'[data-todo]');
  var cab=ver(r,'[data-cab]'),k=0,reloj=null,ap=ver(r,'[data-apuesta]');
  if(ap){
    // Hasta que no apuesten, la traza no se mueve: primero se piensa.
    bs.disabled=true;bt.disabled=true;
    todos(ap,'[data-ap]').forEach(function(b){on(b,'click',function(){
      var bien=b.hasAttribute('data-ok');
      todos(ap,'[data-ap]').forEach(function(x){
        x.disabled=true;x.dataset.estado=x.hasAttribute('data-ok')?'bien':(x===b?'mal':'');
      });
      bs.disabled=false;bt.disabled=false;
      fb(r,bien,bien?'¡Esa! Ahora míralo vuelta por vuelta.':'Todavía no. Córrelo y mira dónde se te fue.');
    });});
  }
  function fin(){bs.disabled=true;bt.disabled=true;res.textContent=tr.final;
    gana(r)&&fb(r,true,'El bucle dio '+tr.filas.length+(tr.filas.length===1?' vuelta.':' vueltas.'));}
  function sig(){
    if(k>=tr.filas.length){fin();return false;}
    var t=tr.filas[k++],fila=document.createElement('tr');
    [t.vuelta,t['var'],t.acum].forEach(function(x){var td=document.createElement('td');td.textContent=x;fila.appendChild(td);});
    cuerpo.appendChild(fila);
    cab.classList.add('a-toma');setTimeout(function(){cab.classList.remove('a-toma');},QUIETO?0:220);
    if(k>=tr.filas.length)fin();
    return true;
  }
  function reiniciar(){clearInterval(reloj);reloj=null;k=0;cuerpo.innerHTML='';bs.disabled=false;bt.disabled=false;res.textContent='';fb(r,null,'');}
  on(bs,'click',sig);
  on(bt,'click',function(){bt.disabled=true;bs.disabled=true;reloj=setInterval(function(){if(!sig()||k>=tr.filas.length){clearInterval(reloj);reloj=null;}},QUIETO?40:380);});
  on(ver(r,'[data-reiniciar]'),'click',reiniciar);
  pausas.push(function(){if(reloj){clearInterval(reloj);reloj=null;if(k<tr.filas.length){bs.disabled=false;bt.disabled=false;}}});
};

M.vueltas=function(r){
  var cfg=JSON.parse(r.dataset.cfg),rondas=cfg.rondas,k=0;
  var inA=ver(r,'[data-a]'),inB=ver(r,'[data-b]'),inP=ver(r,'[data-p]'),sale=ver(r,'[data-sale]');
  function lista(a){return a.length?a.join(', '):'nada';}
  function secuencia(){
    var a=parseInt(inA.value,10),b=parseInt(inB.value,10),p=parseInt(inP.value,10);
    if(isNaN(a)||isNaN(b)||isNaN(p)||p===0)return null;
    var out=[],x=a,tope=0;
    while((p>0?x<b:x>b)&&tope++<200){out.push(x);x+=p;}
    return out;
  }
  function verSalida(){
    var s=secuencia();
    sale.textContent=s===null?'— (el salto no puede ser 0)':lista(s);
  }
  function luces(){
    var caja=ver(r,'[data-luces]');caja.innerHTML='';
    rondas.forEach(function(_,i){
      var d=document.createElement('span');
      d.className='a-vu-luz'+(i<k?' a-ok':i===k?' a-now':'');
      d.textContent=i<k?'✓':String(i+1);caja.appendChild(d);
    });
  }
  function pintar(){
    var ro=rondas[Math.min(k,rondas.length-1)];
    ver(r,'[data-num]').textContent=k>=rondas.length?'¡Fábrica dominada!':'Ronda '+(k+1)+' de '+rondas.length;
    ver(r,'[data-meta]').textContent=k>=rondas.length?'ya está':lista(ro.objetivo);
    ver(r,'[data-pista]').textContent=k>=rondas.length?'':(ro.pista||'');
    ver(r,'[data-probar]').disabled=k>=rondas.length;
    [inA,inB,inP].forEach(function(x){x.disabled=k>=rondas.length;});
    luces();verSalida();
  }
  function probar(){
    if(k>=rondas.length)return;
    var s=secuencia(),meta=rondas[k].objetivo;
    if(s===null){fb(r,false,'El salto no puede ser 0: el ciclo no avanzaría nunca.');return;}
    if(!s.length){fb(r,false,'Así no da ninguna vuelta: con salto positivo, hasta tiene que ser mayor que desde.');return;}
    if(s.length===meta.length&&s.every(function(x,i){return x===meta[i];})){
      k++;
      if(k>=rondas.length){gana(r);fb(r,true,'¡Las cinco! range(desde, hasta, salto): el hasta nunca entra.');}
      else fb(r,true,'¡Clavado! Siguiente ronda.');
      pintar();return;
    }
    var p=[];
    if(s[0]!==meta[0])p.push('empieza en '+s[0]+' y debería empezar en '+meta[0]);
    if(s.length!==meta.length)p.push('da '+s.length+' números y hacen falta '+meta.length);
    else if(s.length>1&&(s[1]-s[0])!==(meta[1]-meta[0]))p.push('salta de '+(s[1]-s[0])+' en '+(s[1]-s[0]));
    fb(r,false,'Tu ciclo da '+lista(s)+(p.length?': '+p.join(' y ')+'.':'.'));
  }
  [inA,inB,inP].forEach(function(x){on(x,'input',verSalida);});
  on(ver(r,'[data-probar]'),'click',probar);
  on(ver(r,'[data-reiniciar]'),'click',function(){k=0;inA.value=0;inB.value=5;inP.value=1;fb(r,null,'');pintar();});
  pintar();
};

M.escalera=function(r){
  var cfg=JSON.parse(r.dataset.cfg),mis=cfg.misiones,k=0,lineas=[];
  var inp=ver(r,'[data-linea]'),prog=ver(r,'[data-prog]'),yo=ver(r,'[data-yo]'),sale=ver(r,'[data-sale]');
  function lista(a){return a.length>8?a.slice(0,6).join(', ')+' … '+a[a.length-1]:a.join(', ');}
  // Los números que de verdad produce su línea. null si no se puede leer.
  function corre(t){
    var m=t.match(/^for\s+([A-Za-z_][A-Za-z0-9_]*)\s+in\s+range\s*\(([^)]*)\)\s*:?\s*$/);
    if(!m)return null;
    var args=m[2].split(',').map(function(x){return x.trim();});
    if(args.length<1||args.length>3)return null;
    var nums=[];
    for(var i=0;i<args.length;i++){
      if(!/^-?\d+$/.test(args[i]))return null;
      nums.push(parseInt(args[i],10));
    }
    var a=nums.length===1?0:nums[0],b=nums.length===1?nums[0]:nums[1],p=nums.length===3?nums[2]:1;
    if(p===0)return 'salto0';
    var out=[],x=a,tope=0;
    while((p>0?x<b:x>b)&&tope++<500){out.push(x);x+=p;}
    return out;
  }
  // Qué le falta a la cabecera, dicho como lo diría el docente. null si está bien.
  function revisar(t,m){
    t=t.trim();
    if(!t)return ['Escribe la cabecera completa: for i in range(…):',null];
    if(!/^for\b/.test(t))return ['Un ciclo empieza con for.',null];
    if(!/\bin\b/.test(t))return ['Entre el nombre y range va in: for i in range(5):',null];
    if(!/range\s*\(/.test(t))return ['Dentro va range(...): es quien dice cuántas vueltas.',null];
    if(!/:\s*$/.test(t))return ['Falta los dos puntos al final de la cabecera.',null];
    var sec=corre(t);
    if(sec==='salto0')return ['El salto no puede ser 0: el ciclo no avanzaría nunca.',null];
    if(sec===null)return ['Dentro de range van números enteros separados por comas.',null];
    if(!sec.length)return ['Tu línea no da ninguna vuelta: revisa el desde y el hasta.',sec];
    if(sec.length!==m.secuencia.length||sec.some(function(x,i){return x!==m.secuencia[i];}))
      return ['El tuyo da '+lista(sec)+' y hacen falta '+lista(m.secuencia)+'.',sec];
    return [null,sec];
  }
  function pintar(){
    r.style.setProperty('--k',k);yo.style.setProperty('--k',k);
    var m=mis[Math.min(k,mis.length-1)];
    ver(r,'[data-num]').textContent=k>=mis.length?'¡Meta!':'Misión '+(k+1)+' de '+mis.length;
    ver(r,'[data-pide]').textContent=k>=mis.length?'Escribiste '+mis.length+' ciclos sin ayuda.':m.pide;
    prog.textContent=lineas.length?lineas.join('\n'):'# aquí van apareciendo tus ciclos';
    inp.disabled=k>=mis.length;ver(r,'[data-subir]').disabled=k>=mis.length;
    if(k<mis.length)sale.innerHTML='Tiene que dar: <b>'+lista(m.secuencia)+'</b>';
    else sale.textContent='';
    r.classList.toggle('a-cima',k>=mis.length);
  }
  function subir(){
    if(k>=mis.length)return;
    var res=revisar(inp.value,mis[k]),falla=res[0],sec=res[1];
    if(falla){
      fb(r,false,falla);
      yo.classList.remove('a-es-tropieza');void yo.offsetWidth;yo.classList.add('a-es-tropieza');
      return;
    }
    lineas.push(inp.value.trim()+'\n    display(i)');k++;inp.value='';
    if(k>=mis.length){gana(r);fb(r,true,'¡Meta! Ya sabes decirle a Python cuántas vueltas dar y en qué orden.');}
    else fb(r,true,'Da '+lista(sec)+'. Subes un escalón.');
    pintar();inp.focus();
  }
  on(ver(r,'[data-subir]'),'click',subir);
  on(inp,'keydown',function(e){if(e.key==='Enter'){e.preventDefault();subir();}});
  on(ver(r,'[data-reiniciar]'),'click',function(){k=0;lineas=[];inp.value='';fb(r,null,'');pintar();});
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