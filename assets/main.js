/* Portfolio : apparitions, couleurs de fond par section, parcours horizontal sur deux hauteurs. Sans bibliothèque. */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var mobile = window.matchMedia("(max-width: 860px)");
  var clamp = function (v, a, b) { return Math.min(b, Math.max(a, v)); };

  /* Décalage progressif des lignes d'un même titre */
  document.querySelectorAll(".line").forEach(function (l) {
    l.style.setProperty("--i", Array.prototype.indexOf.call(l.parentNode.children, l));
  });
  /* Décalage progressif des éléments voisins qui apparaissent ensemble */
  [".stats", ".pillars", ".quals", ".by-grid", ".c-rows", ".proj-grid", ".tri"].forEach(function (sel) {
    document.querySelectorAll(sel).forEach(function (group) {
      Array.prototype.forEach.call(group.children, function (el, i) { el.style.setProperty("--d", (i % 4) * 0.08 + "s"); });
    });
  });

  /* Entrée de la page */
  requestAnimationFrame(function () {
    document.body.classList.add("ready");
    document.querySelectorAll(".hero .name .line, .d-title .line").forEach(function (l) { l.classList.add("in"); });
  });

  /* Apparitions au défilement (textes et blocs ; les images ne sont jamais masquées) */
  var targets = document.querySelectorAll(".rv, .sec-title, .statement, .feature-body h3, .giant, .tri-col, .d-title");
  function show(t) {
    t.classList.add("in");
    var c = t.querySelector && t.querySelector("[data-count]");
    if (c) count(c);
  }
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { show(en.target); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });
    targets.forEach(function (t) { io.observe(t); });
    /* sécurité : tout ce qui est déjà passé au-dessus de l'écran est affiché */
    window.addEventListener("scroll", function () {
      targets.forEach(function (t) {
        if (!t.classList.contains("in") && t.getBoundingClientRect().top < window.innerHeight * 0.9) show(t);
      });
    }, { passive: true });
  } else {
    targets.forEach(show);
  }

  /* Chiffres qui défilent (seul le nombre change, le texte autour reste) */
  function count(el) {
    if (reduce || el.dataset.done) return;
    el.dataset.done = "1";
    var txt = el.textContent, m = txt.match(/\d+/);
    if (!m) return;
    var end = parseInt(m[0], 10), t0 = performance.now(), dur = 1100;
    (function step(t) {
      var p = clamp((t - t0) / dur, 0, 1), eased = 1 - Math.pow(1 - p, 3);
      el.textContent = txt.replace(/\d+/, String(Math.round(end * eased)));
      if (p < 1) requestAnimationFrame(step);
    })(t0);
    setTimeout(function () { el.textContent = txt; }, dur + 400);
  }

  /* Couleur de fond : chaque section a sa nuance, le passage se fait en fondu */
  var zones = Array.prototype.slice.call(document.querySelectorAll("[data-bg]"));
  var navLinks = document.querySelectorAll(".top-nav a");
  function paint() {
    var mid = window.scrollY + window.innerHeight * 0.5, cur = zones[0];
    zones.forEach(function (z) { if (z.offsetTop <= mid) cur = z; });
    if (document.body.dataset.bg !== cur.dataset.bg) {
      document.body.dataset.bg = cur.dataset.bg;
      document.body.style.backgroundColor = cur.dataset.bg;
    }
    navLinks.forEach(function (a) { a.classList.toggle("on", a.getAttribute("href") === "#" + cur.id); });
  }

  /* En-tête : se masque en descendant, revient en remontant */
  var top = document.querySelector(".top"), bar = document.querySelector(".progress span"), lastY = 0;
  var burger = document.querySelector(".burger"), nav = document.querySelector(".top-nav");
  function onScroll() {
    var y = window.scrollY, max = doc.scrollHeight - window.innerHeight;
    top.classList.toggle("solid", y > 40);
    top.classList.toggle("hide", y > lastY && y > 400 && !nav.classList.contains("open"));
    lastY = y;
    bar.style.transform = "scaleX(" + (max > 0 ? y / max : 0) + ")";
    paint();
    pinTarget();
  }
  burger.addEventListener("click", function () {
    var open = burger.getAttribute("aria-expanded") !== "true";
    burger.setAttribute("aria-expanded", String(open));
    nav.classList.toggle("open", open);
  });
  nav.addEventListener("click", function (e) {
    if (e.target.closest("a")) { burger.setAttribute("aria-expanded", "false"); nav.classList.remove("open"); }
  });

  /* Parcours horizontal : la section se fige et les étapes glissent pendant le défilement vertical */
  var hs = document.querySelector(".hscroll"), track = hs ? hs.querySelector(".track") : null;
  if (!hs) {
    pinTarget = function () {};
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
    lightbox();
    return;
  }
  var stops = Array.prototype.slice.call(track.querySelectorAll(".stop"));
  var figs = stops.map(function (s) { return s.querySelector(".stop-fig"); });
  var fill = hs.querySelector(".ruler-fill"), countEl = hs.querySelector(".ruler-count b"), yearEl = hs.querySelector(".ruler-year");
  var overflow = 0, target = 0, cur = 0, running = false;

  function measure() {
    if (mobile.matches) { hs.classList.remove("pin"); hs.style.height = ""; track.style.transform = ""; overflow = 0; return; }
    hs.classList.add("pin");
    overflow = Math.max(0, track.scrollWidth - window.innerWidth);
    hs.style.height = window.innerHeight + overflow + "px";
    pinTarget(); cur = target; draw();
  }
  function pinTarget() {
    if (!overflow) return;
    target = clamp((window.scrollY - hs.offsetTop) / overflow, 0, 1) * overflow;
    if (!running) { running = true; requestAnimationFrame(tick); }
  }
  function tick() {
    cur += (target - cur) * (reduce ? 1 : 0.12);
    if (Math.abs(target - cur) < 0.3) cur = target;
    draw();
    if (cur !== target) requestAnimationFrame(tick); else running = false;
  }
  function draw() {
    track.style.transform = "translate3d(" + -cur + "px,0,0)";
    fill.style.transform = "scaleX(" + (overflow ? cur / overflow : 0) + ")";
    var w = window.innerWidth, centre = cur + w * 0.4, active = 0;
    var inView = hs.getBoundingClientRect().top < window.innerHeight * 0.6;
    stops.forEach(function (s, i) {
      var x = s.offsetLeft - cur;                      /* position de l'étape dans l'écran */
      if (s.offsetLeft <= centre) active = i;
      if (inView && x < w * 0.9) s.classList.add("seen");
      /* les photos glissent un peu moins vite que le texte : léger effet de profondeur */
      if (figs[i] && !reduce) figs[i].style.transform = "translate3d(" + clamp((x - w * 0.4) * 0.05, -40, 40) + "px,0,0)";
    });
    countEl.textContent = (active + 1 < 10 ? "0" : "") + (active + 1);
    yearEl.textContent = stops[active].querySelector(".stop-year").textContent;
  }
  /* Au clavier, atteindre un lien d'une étape fait défiler la page jusqu'à elle */
  track.addEventListener("focusin", function (e) {
    var s = e.target.closest(".stop");
    if (!s || !overflow) return;
    window.scrollTo({ top: hs.offsetTop + clamp(s.offsetLeft - window.innerWidth * 0.2, 0, overflow), behavior: reduce ? "auto" : "smooth" });
  });

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", function () { measure(); onScroll(); });
  window.addEventListener("load", function () { measure(); onScroll(); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { measure(); onScroll(); });
  measure(); onScroll();

  /* Visionneuse : un clic sur une image des pages détaillées l'affiche en grand */
  function lightbox() {
    var lb = document.querySelector(".lightbox");
    if (!lb) return;
    var img = lb.querySelector("img"), cap = lb.querySelector("figcaption"), last = null;
    function close() { lb.hidden = true; document.body.style.overflow = ""; if (last) last.focus(); }
    document.querySelectorAll(".zoom").forEach(function (b) {
      b.addEventListener("click", function () {
        last = b; img.src = b.dataset.src; img.alt = b.dataset.cap; cap.textContent = b.dataset.cap;
        lb.hidden = false; document.body.style.overflow = "hidden"; lb.querySelector(".lb-close").focus();
      });
    });
    lb.addEventListener("click", close);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !lb.hidden) close(); });
  }
})();
