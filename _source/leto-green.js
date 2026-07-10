/* BAKARDI — interactions */
(function(){
  var loader=document.querySelector('.loader');
  if(loader){window.addEventListener('load',function(){setTimeout(function(){loader.classList.add('done');},650);});
    setTimeout(function(){loader.classList.add('done');},2200);}

  function applyLanguage(lang){
    document.querySelectorAll('[data-en]').forEach(function(el){
      var v=el.getAttribute('data-'+lang); if(v!==null) el.textContent=v;
    });
    document.querySelectorAll('.lang button').forEach(function(b){
      b.classList.toggle('on', b.getAttribute('data-lang')===lang);
    });
    document.documentElement.setAttribute('lang', lang);
  }
  function setLanguage(lang){try{localStorage.setItem('preferredLanguage',lang);}catch(e){} applyLanguage(lang);}
  document.querySelectorAll('.lang button').forEach(function(b){
    b.addEventListener('click',function(){setLanguage(b.getAttribute('data-lang'));});
  });
  var saved='en'; try{saved=localStorage.getItem('preferredLanguage')||'en';}catch(e){}
  applyLanguage(saved);

  var burger=document.querySelector('.burger'), nav=document.querySelector('.nav');
  if(burger&&nav){
    burger.addEventListener('click',function(){var o=nav.classList.toggle('open');burger.setAttribute('aria-expanded',o);});
    nav.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){nav.classList.remove('open');});});
  }

  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.12});
    document.querySelectorAll('.reveal').forEach(function(el){io.observe(el);});
  }else{document.querySelectorAll('.reveal').forEach(function(el){el.classList.add('in');});}

  if(document.body.hasAttribute('data-cursor') &&
     window.matchMedia('(hover:hover) and (pointer:fine)').matches &&
     !window.matchMedia('(prefers-reduced-motion:reduce)').matches){
    var ICONS=[
      '<svg viewBox="0 0 32 32"><ellipse cx="16" cy="16" rx="8" ry="11" fill="#2C6E49"/><ellipse cx="16" cy="16" rx="3.4" ry="5" fill="#57A567"/></svg>',
      '<svg viewBox="0 0 32 32"><path d="M6 18C6 9 13 4 24 4c0 9-7 15-18 15Z" fill="#57A567"/><path d="M9 16c4-3 8-5 12-6" stroke="#122019" stroke-width="1.4" fill="none"/></svg>',
      '<svg viewBox="0 0 32 32"><path d="M16 3l3.4 8.2 8.9.7-6.8 5.8 2.1 8.7L16 20.6 8.4 26.4l2.1-8.7-6.8-5.8 8.9-.7Z" fill="#E0A73C"/></svg>',
      '<svg viewBox="0 0 32 32"><ellipse cx="16" cy="16" rx="10" ry="7" fill="#6B4A2B"/><path d="M9 16c4-3 10-3 14 0" stroke="#F1E7CC" stroke-width="1.6" fill="none"/></svg>',
      '<svg viewBox="0 0 32 32"><circle cx="16" cy="16" r="11" fill="#F0C05A"/><path d="M16 16 16 6M16 16 25 16M16 16 8 23M16 16 24 23M16 16 7 12" stroke="#E0A73C" stroke-width="1.3"/></svg>'
    ];
    var N=5, bits=[], pts=[], mouse={x:innerWidth/2,y:innerHeight/2}, moved=false;
    for(var i=0;i<N;i++){var d=document.createElement('div');d.className='cursor-bit';d.innerHTML=ICONS[i%ICONS.length];
      document.body.appendChild(d);bits.push(d);pts.push({x:mouse.x,y:mouse.y});}
    addEventListener('mousemove',function(e){mouse.x=e.clientX;mouse.y=e.clientY;moved=true;});
    addEventListener('click',function(e){bits.forEach(function(b){var a=Math.random()*6.28,r=40+Math.random()*50;
      b.animate([{transform:b.style.transform+' translate(0,0)'},{transform:b.style.transform+' translate('+Math.cos(a)*r+'px,'+Math.sin(a)*r+'px)'}],{duration:500,easing:'cubic-bezier(.2,.8,.3,1)'});});});
    (function loop(){
      var lx=mouse.x,ly=mouse.y;
      for(var i=0;i<N;i++){var p=pts[i];p.x+=(lx-p.x)*.32;p.y+=(ly-p.y)*.32;
        var s=1-i*0.11;bits[i].style.transform='translate('+(p.x-13)+'px,'+(p.y-13)+'px) scale('+s+') rotate('+(p.x+p.y+i*40)*0.4+'deg)';
        bits[i].style.opacity=moved?(0.95-i*0.13):0; lx=p.x;ly=p.y;}
      requestAnimationFrame(loop);
    })();
  }
})();
