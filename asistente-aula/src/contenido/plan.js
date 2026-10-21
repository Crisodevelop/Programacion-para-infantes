var OPC={signal:typeof senal!=='undefined'?senal:undefined};
document.querySelectorAll('.week-head').forEach(function(b){
  b.addEventListener('click',function(){
    var open=b.getAttribute('aria-expanded')==='true';
    b.setAttribute('aria-expanded',String(!open));
    document.getElementById(b.getAttribute('aria-controls')).hidden=open;
  },OPC);
});
document.querySelectorAll('[data-toggle-all]').forEach(function(btn){
  btn.addEventListener('click',function(){
    var box=document.getElementById('weeks-'+btn.dataset.toggleAll);
    var open=btn.dataset.state==='open';
    box.querySelectorAll('.week-head').forEach(function(h){
      h.setAttribute('aria-expanded',String(!open));
      document.getElementById(h.getAttribute('aria-controls')).hidden=open;
    });
    btn.dataset.state=open?'closed':'open';
    btn.textContent=open?'Abrir todas':'Cerrar todas';
  },OPC);
});
var links=[].slice.call(document.querySelectorAll('.lateral a[href^="#"]'));
// getElementById y no querySelector: los identificadores de los cursos son
// «1ro», «2do» y «3ro», y un selector CSS no puede empezar por dígito.
// querySelector('#1ro') lanza SyntaxError y se llevaba por delante todo lo
// que venía detrás — el resaltado de sección y el cajón de móvil.
var secs=links.map(function(a){return document.getElementById(a.getAttribute('href').slice(1));});
var io=new IntersectionObserver(function(es){
  es.forEach(function(e){
    if(!e.isIntersecting)return;
    var i=secs.indexOf(e.target);
    if(i<0)return;
    links.forEach(function(l){l.classList.remove('on');});
    links[i].classList.add('on');
  });
},{rootMargin:'-56px 0px -72% 0px'});
secs.forEach(function(s){if(s)io.observe(s);});
if(OPC.signal)OPC.signal.addEventListener('abort',function(){io.disconnect();});

// En móvil la lateral es un cajón. Se cierra al elegir una sección: dejarla
// abierta taparía justo lo que se acaba de pedir ver.
var lateral=document.getElementById('lateral');
var abrir=document.getElementById('latAbrir');
var velo=document.getElementById('latVelo');
function cajon(abierta){
  if(!lateral)return;
  lateral.classList.toggle('abierta',abierta);
  if(velo)velo.hidden=!abierta;
  if(abrir)abrir.setAttribute('aria-expanded',String(abierta));
}
if(abrir)abrir.addEventListener('click',function(){
  cajon(!lateral.classList.contains('abierta'));
},OPC);
if(velo)velo.addEventListener('click',function(){cajon(false);},OPC);
links.forEach(function(a){a.addEventListener('click',function(){cajon(false);},OPC);});
document.addEventListener('keydown',function(e){
  if(e.key==='Escape')cajon(false);
},OPC);