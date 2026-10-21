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

var CAPS=[];
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