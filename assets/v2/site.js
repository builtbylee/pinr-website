/* eslint-env browser */
/* getpinr.com: loops play only while on screen, and nothing moves with reduced motion. */
(() => {
  const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const ua = navigator.userAgent;
  const ios = /iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1);
  const android = /Android/.test(ua);
  const APP = 'https://apps.apple.com/us/app/pinr-travel-made-social/id6757422507';
  const PLAY = 'https://play.google.com/store/apps/details?id=com.builtbylee.app80days';

  // "Get the app" goes straight to the right store on a phone
  document.querySelectorAll('[data-get]').forEach(a => { if (ios) a.href = APP; else if (android) a.href = PLAY; });

  // the globe loops: transparent video, HEVC for Safari and every iPhone browser, VP9 for the rest
  const webkit = ios || (/Safari\//.test(ua) && !/Chrome|Chromium|CriOS|Edg|OPR|Firefox|FxiOS/.test(ua));
  const vids = [...document.querySelectorAll('video.loop')];
  if (!RM) vids.forEach(v => {
    const small = v.dataset.name === 'hero' && innerWidth < 560;
    v.src = `/assets/v2/${v.dataset.name}${small ? '-sm' : ''}.${webkit ? 'mov' : 'webm'}`;
    v.preload = 'auto';
    new IntersectionObserver(([e]) => { if (e.isIntersecting) v.play().catch(() => {}); else v.pause(); }, { rootMargin: '80px' }).observe(v);
  });

  const countUp = (el, to, dur, fmt = n => String(n)) => {
    if (!el) return;
    if (RM) { el.textContent = fmt(to); return; }
    const t0 = performance.now();
    const step = now => { const t = Math.min(1, (now - t0) / dur), k = 1 - Math.pow(1 - t, 3); el.textContent = fmt(Math.round(to * k)); if (t < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };
  const nf = n => n.toLocaleString('en-GB');

  // sections: fade up once, loops run while on screen
  const counted = new WeakSet();
  const io = new IntersectionObserver(es => es.forEach(e => {
    const s = e.target;
    if (e.isIntersecting) {
      s.classList.add('seen'); s.classList.add('go');
      if (!counted.has(s)) {
        counted.add(s);
        countUp(s.querySelector('#x8Km'), 3866, 2400, nf);
        const n = s.querySelector('[data-count]'); if (n) countUp(n, +n.dataset.count, 1600);
      }
    } else s.classList.remove('go');
  }), { threshold: .18 });
  document.querySelectorAll('.rv').forEach(s => io.observe(s));

  // hero: the notes arrive, the phone shows the real screens in turn
  const hero = document.querySelector('.hero');
  if (!hero) return;
  const nA = hero.querySelector('.note.a'), nB = hero.querySelector('.note.b');
  if (RM) { nA.classList.add('in'); nB.classList.add('in'); return; }
  setTimeout(() => nA.classList.add('in'), 900);
  setTimeout(() => nB.classList.add('in'), 2200);
  let heroOn = true;
  new IntersectionObserver(([e]) => { heroOn = e.isIntersecting; }).observe(hero);
  const shots = [...hero.querySelectorAll('.screens img')];
  let i = 0;
  setInterval(() => {
    if (!heroOn || document.hidden) return;
    const cur = shots[i]; i = (i + 1) % shots.length; const nxt = shots[i];
    cur.classList.remove('on'); cur.classList.add('off');
    nxt.classList.remove('off'); void nxt.offsetWidth; nxt.classList.add('on');
    setTimeout(() => cur.classList.remove('off'), 800);
  }, 3200);
  setInterval(() => {
    if (!heroOn || document.hidden) return;
    nB.classList.remove('in'); setTimeout(() => nB.classList.add('in'), 650);
  }, 6400);
})();
