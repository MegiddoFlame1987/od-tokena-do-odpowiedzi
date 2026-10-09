/* fx.js — ruch i panele dla wszystkich zakładek. Bez zależności.
   1. tytuł składany z tokenów, 2. pole tokenów w tle, 3. rozdziały kręcone scrollem,
   4. panele wjeżdżające przy przewijaniu, 5. światło za kursorem w demach, 6. pasek postępu. */
(function(){
'use strict';
var RM=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var root=document.documentElement;
var SVGNS='http://www.w3.org/2000/svg';
function clamp(x,a,b){return x<a?a:x>b?b:x;}
function rnd(seed){var s=seed||1;return function(){s=(s*16807)%2147483647;return (s-1)/2147483646;};}

/* ---------- 1. tytuł z tokenów ---------- */
function tokenizeTitle(){
  var h=document.querySelector('.hero h1');if(!h||h.dataset.fx)return;
  var text=h.textContent.trim();h.dataset.fx='1';
  h.setAttribute('aria-label',text);
  var vis=document.createElement('span');vis.setAttribute('aria-hidden','true');
  var r=rnd(text.length*97+13),idx=0;
  text.split(/\s+/).forEach(function(word,wi){
    if(wi)vis.appendChild(document.createTextNode(' '));
    var w=document.createElement('span');w.className='fx-w';
    var parts=[],i=0;
    while(i<word.length){var n=word.length-i<=4?word.length-i:(r()<.5?2:3);parts.push(word.slice(i,i+n));i+=n;}
    parts.forEach(function(p){
      var t=document.createElement('span');t.className='fx-t';t.textContent=p;
      t.style.setProperty('--fx-sx',((r()-.5)*260).toFixed(0)+'px');
      t.style.setProperty('--fx-sy',((r()-.5)*140).toFixed(0)+'px');
      t.style.setProperty('--fx-sr',((r()-.5)*40).toFixed(0)+'deg');
      t.style.transitionDelay=(idx*55)+'ms';idx++;
      w.appendChild(t);
    });
    vis.appendChild(w);
  });
  h.textContent='';h.appendChild(vis);h.classList.add('fx-tok');
  if(RM){h.classList.add('fx-in');return;}
  requestAnimationFrame(function(){requestAnimationFrame(function(){
    h.classList.add('fx-in','fx-chips');
    setTimeout(function(){h.classList.remove('fx-chips');},idx*55+1500);
  });});
}

/* ---------- 2. pole tokenów w tle ---------- */
var field=null;
function setupField(){
  var c=document.createElement('canvas');c.id='fx-field';c.setAttribute('aria-hidden','true');
  document.body.insertBefore(c,document.body.firstChild);
  var ctx=c.getContext('2d');if(!ctx)return;
  var words=(document.querySelector('main, .wrap')||document.body).innerText.split(/[^A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+/).filter(function(w){return w.length>3;});
  var r=rnd(4242),P=[],W=0,H=0,colL=0,colR=0,dpr=1,col='#534AB7',vel=0;
  function color(){var v=getComputedStyle(root).getPropertyValue('--purple').trim();if(v)col=v;}
  function frag(){var w=words[(r()*words.length)|0]||'token',s=(r()*(w.length-2))|0;return w.slice(s,s+2+((r()*2)|0)).toLowerCase();}
  function size(){
    dpr=Math.min(window.devicePixelRatio||1,2);W=window.innerWidth;H=window.innerHeight;
    colL=(W-800)/2;colR=(W+800)/2;
    c.width=W*dpr;c.height=H*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);
    var n=Math.round(clamp(W*H/16000,18,70));
    while(P.length<n)P.push({x:r()*W,y:r()*H,z:.3+r()*.7,t:frag(),a:r()*6.28});
    P.length=n;color();
  }
  function draw(dt){
    ctx.clearRect(0,0,W,H);ctx.textBaseline='middle';
    for(var i=0;i<P.length;i++){
      var p=P[i];
      p.y-=(6+vel*.9)*p.z*dt;p.a+=dt*.2;p.x+=Math.sin(p.a)*4*p.z*dt;
      if(p.y<-30){p.y=H+30;p.x=r()*W;p.t=frag();}
      if(p.y>H+40){p.y=-20;}
      var fs=10+p.z*9;ctx.font='600 '+fs.toFixed(0)+'px "JetBrains Mono",ui-monospace,monospace';
      var tw=ctx.measureText(p.t).width+fs*.8,th=fs*1.5;
      var dim=(p.x+tw>colL&&p.x<colR)?.35:1;
      ctx.globalAlpha=(.05+p.z*.10)*dim;ctx.strokeStyle=col;ctx.lineWidth=1;
      ctx.beginPath();if(ctx.roundRect)ctx.roundRect(p.x,p.y-th/2,tw,th,fs*.35);else ctx.rect(p.x,p.y-th/2,tw,th);ctx.stroke();
      ctx.globalAlpha=(.07+p.z*.13)*dim;ctx.fillStyle=col;ctx.fillText(p.t,p.x+fs*.4,p.y+1);
    }
    ctx.globalAlpha=1;
  }
  size();window.addEventListener('resize',size);
  if(window.matchMedia)window.matchMedia('(prefers-color-scheme: dark)').addEventListener&&window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change',color);
  field={kick:function(d){vel=clamp(vel+Math.abs(d)*.6,0,240);}};
  if(RM){draw(0);return;}
  var last=performance.now(),run=true;
  document.addEventListener('visibilitychange',function(){run=!document.hidden;if(run){last=performance.now();requestAnimationFrame(loop);}});
  function loop(now){if(!run)return;var dt=Math.min(.05,(now-last)/1000);last=now;vel*=.92;draw(dt);requestAnimationFrame(loop);}
  requestAnimationFrame(loop);
}

/* ---------- 3. rozdziały ---------- */
var chapters=[];
function orb(seed){
  var r=rnd(seed*131+7),s=document.createElementNS(SVGNS,'svg');
  s.setAttribute('viewBox','0 0 600 600');s.setAttribute('class','fx-orb');s.setAttribute('aria-hidden','true');
  var defs=document.createElementNS(SVGNS,'defs'),g=document.createElementNS(SVGNS,'linearGradient');
  g.id='fxg'+seed;g.setAttribute('x1','0');g.setAttribute('y1','0');g.setAttribute('x2','1');g.setAttribute('y2','1');
  [['0','#AFA9EC'],['.5','#5DCAA5'],['1','#EF9F27']].forEach(function(st){var e=document.createElementNS(SVGNS,'stop');e.setAttribute('offset',st[0]);e.setAttribute('stop-color',st[1]);g.appendChild(e);});
  defs.appendChild(g);s.appendChild(defs);
  function el(n,a,p){var e=document.createElementNS(SVGNS,n);for(var k in a)e.setAttribute(k,a[k]);(p||s).appendChild(e);return e;}
  var ring1=el('g',{}),ring2=el('g',{'class':'fx-ring2'});
  /* pierścienie z „tokenów”: przerywane łuki */
  [250,205,160].forEach(function(R,i){
    var dash=(8+r()*30).toFixed(0)+' '+(6+r()*22).toFixed(0);
    el('circle',{cx:300,cy:300,r:R,fill:'none',stroke:'url(#fxg'+seed+')','stroke-width':i===0?2:1.2,'stroke-dasharray':dash,opacity:(.9-i*.2).toFixed(2)},i===1?ring2:ring1);
  });
  /* punkty i łuki uwagi między nimi */
  var pts=[],n=9+((r()*5)|0);
  for(var k=0;k<n;k++){var a=k/n*6.283+r()*.3;pts.push([300+250*Math.cos(a),300+250*Math.sin(a)]);}
  for(var j=0;j<n+3;j++){
    var A=pts[(r()*n)|0],B=pts[(r()*n)|0];if(A===B)continue;
    var cx=300+(r()-.5)*120,cy=300+(r()-.5)*120;
    el('path',{d:'M'+A[0].toFixed(1)+' '+A[1].toFixed(1)+' Q'+cx.toFixed(1)+' '+cy.toFixed(1)+' '+B[0].toFixed(1)+' '+B[1].toFixed(1),fill:'none',stroke:['#AFA9EC','#5DCAA5','#EF9F27','#F0997B'][j%4],'stroke-width':(0.6+r()*1.8).toFixed(2),opacity:(.25+r()*.5).toFixed(2)},ring1);
  }
  pts.forEach(function(p,i){el('circle',{cx:p[0].toFixed(1),cy:p[1].toFixed(1),r:i%3?3:6,fill:['#AFA9EC','#5DCAA5','#EF9F27','#F0997B'][i%4]},ring1);});
  el('circle',{cx:300,cy:300,r:34,fill:'none',stroke:'#ECEAF7','stroke-width':1,opacity:.5},ring1);
  return s;
}
function setupChapters(){
  var hs=document.querySelectorAll('.part>header');
  Array.prototype.forEach.call(hs,function(h,i){
    h.classList.add('fx-ch');
    var k=h.querySelector('.k'),m=k&&k.textContent.match(/\b([IVX]{1,4})\b/);
    var num=document.createElement('div');num.className='fx-num';num.setAttribute('aria-hidden','true');
    num.textContent=m?m[1]:(k&&/koniec/i.test(k.textContent)?'Σ':String(i+1));
    h.insertBefore(num,h.firstChild);h.insertBefore(orb(i+1),h.firstChild);
    chapters.push(h);
  });
}

/* ---------- 4. panele wjeżdżające ---------- */
var sliders=[];
function setupSliders(){
  var list=document.querySelectorAll('.demo, .tbl, .status, article.news, .chain');
  var n=0;
  Array.prototype.forEach.call(list,function(e){
    if(e.parentElement&&e.parentElement.closest('.demo, .tbl, header.fx-ch'))return;
    e.classList.add('fx-slide');
    if(e.classList.contains('status')||e.classList.contains('chain'))e.classList.add('fx-soft');
    e.style.setProperty('--fx-dir',n%2?'-1':'1');n++;
    sliders.push(e);
  });
}

/* ---------- 5. światło w demach ---------- */
function setupGlow(){
  Array.prototype.forEach.call(document.querySelectorAll('.demo'),function(d){
    if(d.parentElement&&d.parentElement.closest('.demo'))return;
    d.classList.add('fx-glow');
    d.addEventListener('pointermove',function(ev){var b=d.getBoundingClientRect();d.style.setProperty('--fx-mx',(ev.clientX-b.left)+'px');d.style.setProperty('--fx-my',(ev.clientY-b.top)+'px');});
  });
}

/* ---------- 6. scroll: jeden handler ---------- */
function setupScroll(){
  var bar=document.createElement('div');bar.id='fx-bar';bar.setAttribute('aria-hidden','true');document.body.appendChild(bar);
  var lastY=window.scrollY,ticking=false;
  function update(){
    ticking=false;
    var vh=window.innerHeight,y=window.scrollY,max=Math.max(1,document.documentElement.scrollHeight-vh);
    root.style.setProperty('--fx-prog',(y/max).toFixed(4));
    if(field)field.kick(y-lastY);lastY=y;
    if(RM)return;
    for(var i=0;i<chapters.length;i++){
      var b=chapters[i].getBoundingClientRect();
      if(b.bottom<-200||b.top>vh+200)continue;
      chapters[i].style.setProperty('--fx-p',clamp((vh-b.top)/(vh+b.height),0,1).toFixed(3));
    }
    for(var j=0;j<sliders.length;j++){
      var e=sliders[j],r=e.getBoundingClientRect();
      if(r.bottom<-50||r.top>vh+50){continue;}
      var v=clamp((vh-r.top)/(vh*.38),0,1);
      v=1-Math.pow(1-v,3);
      e.style.setProperty('--fx-r',v.toFixed(3));
    }
  }
  function on(){if(!ticking){ticking=true;requestAnimationFrame(update);}}
  window.addEventListener('scroll',on,{passive:true});window.addEventListener('resize',on);
  update();
}

function init(){
  try{tokenizeTitle();}catch(e){}
  try{setupChapters();}catch(e){}
  try{setupSliders();}catch(e){}
  try{setupGlow();}catch(e){}
  try{setupField();}catch(e){}
  try{setupScroll();}catch(e){}
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
