# -*- coding: utf-8 -*-
"""Générateur du site (version 2, française).

Usage :
    python build.py
Lit les textes dans content.py (même dossier) et écrit index.html et les pages détaillées.
"""
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from content import (BEYOND, EXTRA_TIMELINE, LETTERS, PAGES, PERSON, PROJECTS,  # noqa: E402
                     SKILLS, TIMELINE_ORDER, UI)

L = "fr"
u = UI[L]
sk = SKILLS[L]
PAGE = {p["slug"]: p for p in PAGES}
FONTS = ("https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300..900"
         "&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap")

# image associée à chaque étape du parcours (aucune = panneau typographique)
STOP_IMG = {
    "mobilis": ("mobilis-dispositif.jpg", "plan", ""),
    "cirris": ("laval-campus.jpg", "", ""),
    "libm": ("libm-campus.jpg", "", "Photo : F. Pépellin, CC BY-SA 4.0"),
    "licence-staps": ("usmb-presidence.jpg", "", ""),
    "gendarmerie": ("gend-ceremonie.jpg", "tall", ""),
    "premieres-experiences": ("armee.jpg", "tall", ""),
}
CREDITS = {"libm-campus.jpg": "Photo : F. Pépellin, CC BY-SA 4.0"}


def e(s):
    return html.escape(s, quote=True)


def page_url(p):
    return f"{p['section']}/{p['slug']}.html"


def lines(*parts):
    """Titre découpé en lignes masquées, pour l'apparition ligne par ligne."""
    return "".join(f'<span class="line"><span>{p}</span></span>' for p in parts)


def sec_head(num, title, note=""):
    note_html = f'<span class="sec-note mono">{e(note)}</span>' if note else ""
    return (f'<header class="sec-head"><span class="sec-num mono">{num}</span>'
            f'<h2 class="sec-title">{lines(e(title))}</h2>{note_html}</header>')


import hashlib  # noqa: E402
with open(os.path.join(HERE, "assets", "img", "portrait.webp"), "rb") as _fh:
    PORTRAIT_V = hashlib.md5(_fh.read()).hexdigest()[:8]

ARROW = '<svg class="arr" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 19L19 5M8 5h11v11" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'

# ------------------------------------------------------------------ hero
stats = "".join(
    f'<div class="stat rv"><span class="stat-v" data-count>{e(v)}</span><span class="stat-l">{e(l)}</span></div>'
    for v, l in u["stats"])

marquee_items = ["ISO 13485", "SolidWorks", "Biomécanique", "MATLAB", "Audit", "ISO/IEC 17025", "Traitement du signal",
                 "Python", "Dispositifs médicaux", "Encadrement d'équipe", "Protocoles expérimentaux", "Anglais C1"]
marquee = "".join(f"<span>{e(m)}</span><i></i>" for m in marquee_items)

hero = f"""
<section class="hero" id="top" data-bg="#0b0b0c">
  <div class="wrap hero-grid">
    <p class="hero-meta mono rv"><span>Portfolio</span><span>{e(PERSON['city'][L])}</span><span>{e(u['eyebrow'])}</span></p>
    <h1 class="name" aria-label="Yoan Rousselot">
      <span class="line n1"><span>Yoan</span></span>
      <span class="line n2"><span>Rousselot</span></span>
    </h1>
    <figure class="hero-portrait" aria-hidden="true">
      <img src="assets/img/portrait.webp?v={PORTRAIT_V}" alt="" width="1100" height="1467">
    </figure>
    <p class="tagline rv">De sous-officier de gendarmerie <em>à l'ingénierie biomédicale.</em></p>
    <div class="hero-foot">
      <p class="lead rv">{e(u['hero_lead'])}</p>
      <div class="hero-side rv">
        <p class="avail"><i aria-hidden="true"></i>{e(u['availability'])}</p>
        <p class="hero-actions"><a class="btn" href="#parcours">Voir mon parcours{ARROW}</a><a class="tlink" href="#contact">Me contacter</a></p>
      </div>
    </div>
  </div>
  <div class="wrap"><div class="stats">{stats}</div></div>
</section>"""

# ------------------------------------------------------------------ profil
about = u["about"]
pillars = "".join(
    f'<div class="pillar rv"><span class="mono idx">{chr(65 + i)}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>'
    for i, (_ico, t, d) in enumerate(u["pillars"]))
a_title = [p.strip() for p in u["about_title"].split(",")]
a_lines = [e(p) + ("," if i < len(a_title) - 1 else ".") for i, p in enumerate(a_title)]
profil = f"""
<section class="sec" id="profil" data-bg="#100f0d">
  <div class="col">
    {sec_head('01', 'Profil')}
    <div class="profil-grid">
      <h3 class="statement">{lines(*a_lines)}</h3>
      <div class="prose">
        {"".join(f'<p class="rv">{p}</p>' for p in about)}
      </div>
    </div>
    <div class="pillars">{pillars}</div>
  </div>
</section>"""

# ------------------------------------------------------------------ compétences
rows = ""
for i, (title, sub, chips) in enumerate(sk["tech"], 1):
    # les intitulés longs passent en dernier, sur toute la largeur : les colonnes restent alignées
    short = [c for c in chips if len(c) <= 32]
    wide = [c for c in chips if len(c) > 32]
    items = "".join(f"<li>{e(c)}</li>" for c in short) + "".join(f'<li class="wide">{e(c)}</li>' for c in wide)
    rows += (f'<div class="skill-row rv"><h3>{e(title)}</h3>'
             f'<div class="skill-body"><p class="skill-sub">{e(sub)}</p><ul class="dots">{items}</ul></div></div>')
soft = "".join(f"<li>{e(s)}</li>" for s in sk["soft"])
langs = "".join(
    f'<div class="lang"><div class="lang-top"><strong>{e(n)}</strong><span class="mono">{e(lv)}</span></div>'
    f'<div class="gauge"><span style="--w:{w}%"></span></div></div>' for n, lv, w in sk["languages"])
certs = "".join(f"<li>{e(c)}</li>" for c in sk["certs"])
quals = "".join(f'<div class="qual rv"><h4>{e(q)}</h4><p>{e(d)}</p></div>' for q, d in sk["qualities"])
competences = f"""
<section class="sec" id="competences" data-bg="#0b1214">
  <div class="col">
    {sec_head('02', 'Compétences', u['skills_title'])}
    <div class="skill-table">{rows}</div>
    <div class="tri">
      <div class="tri-col rv"><h4 class="mono cap">{e(u['skills_soft'])}</h4><ol class="num-list">{soft}</ol></div>
      <div class="tri-col rv"><h4 class="mono cap">{e(u['languages'])}</h4>{langs}</div>
      <div class="tri-col rv"><h4 class="mono cap">{e(u['certs'])}</h4><ul class="plain">{certs}</ul></div>
    </div>
    <h3 class="sub-display rv">{e(u['qualities'])}</h3>
    <div class="quals">{quals}</div>
  </div>
</section>"""

# ------------------------------------------------------------------ parcours (défilement horizontal)
stops = ""
entries = []
for item in TIMELINE_ORDER:
    if isinstance(item, int):
        x = EXTRA_TIMELINE[item]
        entries.append((x[L], x["kind"], x["year"], None, None))
    else:
        p = PAGE[item]
        entries.append((p[L], p["kind"], p["year"], page_url(p), item))
n = len(entries)
for i, (d, kind, year, href, slug) in enumerate(entries, 1):
    big = re.findall(r"\d{4}", year)[0]
    tag = u["type_labels"][kind]
    fig = ""  # pas de photo dans le parcours : toutes les étapes ont la même forme
    link = f'<a class="tlink" href="{href}">{e(u["see_detail"])}{ARROW}</a>' if href else ""
    text = f'<p class="stop-desc">{e(d["timeline"])}</p>' if d["timeline"] else ""
    side = "up" if i % 2 else "down"
    stops += f"""<article class="stop {side}" data-kind="{kind}">
  <div class="stop-text">
    <p class="mono stop-meta"><span>{i:02d} / {n:02d}</span><span class="k-{kind}">{e(tag)}</span><span>{e(d['period'])}</span></p>
    <h3>{e(d['title'])}</h3>
    <p class="stop-org">{e(d['org'])}</p>
    {text}
    {link}
  </div>
  <div class="stop-node" aria-hidden="true"><i></i></div>
  <div class="stop-alt">
    <span class="stop-year" aria-hidden="true">{big}</span>
    {fig}
  </div>
</article>"""
ticks = "".join("<i></i>" for _ in range(n))
parcours = f"""
<section class="hscroll" id="parcours" data-bg="#15110b">
  <div class="hscroll-sticky">
    <div class="col hscroll-head">
      {sec_head('03', 'Parcours', 'Du plus récent au plus ancien')}
    </div>
    <div class="track">
      <div class="stop-intro">
        <p class="mono">Faites défiler</p>
        <p class="intro-big">{n} étapes,<br>de 2026 à 2017.</p>
        <span class="intro-arrow" aria-hidden="true">→</span>
      </div>
      {stops}
    </div>
    <div class="col ruler" aria-hidden="true">
      <span class="mono ruler-count"><b>01</b> / {n:02d}</span>
      <div class="ruler-bar"><span class="ruler-fill"></span><div class="ruler-ticks">{ticks}</div></div>
      <span class="mono ruler-year">2026</span>
    </div>
  </div>
</section>"""

# ------------------------------------------------------------------ projets
feat = PROJECTS[0]
fp = PAGE[feat["slug"]]
others = ""
for pr in PROJECTS[1:]:
    p = PAGE[pr["slug"]]
    d = pr[L]
    credit = CREDITS.get(pr.get("image") or "", "")
    cap = f'<figcaption class="mono">{e(credit)}</figcaption>' if credit else ""
    others += f"""<a class="proj rv" href="{page_url(p)}">
  <figure><div class="ph"><img src="assets/img/{pr['image']}" alt="" loading="lazy"></div>{cap}</figure>
  <p class="mono proj-meta">{e(p[L]['period'])}</p>
  <h3>{e(d['title'])}</h3>
  <p>{e(d['text'])}</p>
  <ul class="slash">{"".join(f"<li>{e(t)}</li>" for t in d['tags'])}</ul>
  <span class="tlink">{e(u['see_project'])}{ARROW}</span>
</a>"""
projets = f"""
<section class="sec" id="projets" data-bg="#0d0e12">
  <div class="col">
    {sec_head('04', 'Projets', u['projects_intro'])}
    <a class="feature" href="{page_url(fp)}">
      <figure class="feature-fig"><div class="ph"><img src="assets/img/{feat['image']}" alt="Modèle 3D annoté du dispositif Mobilis" loading="lazy"></div>
        <span class="crop tl"></span><span class="crop tr"></span><span class="crop bl"></span><span class="crop br"></span>
        <figcaption class="mono">Fig. 01 · Modèle 3D annoté du dispositif</figcaption></figure>
      <div class="feature-body rv">
        <p class="mono proj-meta">Projet R&amp;D · {e(fp[L]['period'])}</p>
        <h3>{lines('Mobilis', 'orthèse de', 'rééducation', 'du poignet')}</h3>
        <p>{e(feat[L]['text'])}</p>
        <ul class="slash">{"".join(f"<li>{e(t)}</li>" for t in feat[L]['tags'])}</ul>
        <span class="btn">{e(u['see_project'])}{ARROW}</span>
      </div>
    </a>
    <div class="proj-grid">{others}</div>
  </div>
</section>"""

# ------------------------------------------------------------------ recommandations
recos = ""
for i, key in enumerate(("hti", "laval", "usmb"), 1):
    R = LETTERS[key]
    d = R[L]
    recos += f"""<figure class="reco rv">
  <figcaption>
    <span class="mono idx">{i:02d}</span>
    <strong>{e(R['name'])}</strong>
    <span>{e(d['role'])}</span>
    <span class="mono dim">{e(d['date'])}</span>
    <a class="tlink" href="assets/docs/{R['pdf']}" target="_blank" rel="noopener">{e(u['read_letter'])}{ARROW}</a>
  </figcaption>
  <blockquote>{e(d['quote'])}</blockquote>
</figure>"""
recommandations = f"""
<section class="sec" id="recommandations" data-bg="#12100d">
  <div class="col">
    {sec_head('05', 'Recommandations', u['reco_title'])}
    <div class="recos">{recos}</div>
  </div>
</section>"""

# ------------------------------------------------------------------ au-delà du CV
beyond = ""
for i, b in enumerate(BEYOND, 1):
    t, txt = b[L]
    beyond += f"""<article class="by rv">
  <div class="ph"><img src="assets/img/{b['image']}" alt="" loading="lazy"></div>
  <div class="by-body"><span class="mono idx">{i:02d}</span><h3>{e(t)}</h3><p>{e(txt)}</p></div>
</article>"""
au_dela = f"""
<section class="sec" id="au-dela" data-bg="#0b0f0e">
  <div class="col">
    {sec_head('06', u['beyond_title'], u['beyond_intro'])}
    <div class="by-grid">{beyond}</div>
  </div>
</section>"""

# ------------------------------------------------------------------ contact
import urllib.parse as up  # noqa: E402
mail = f"mailto:{PERSON['email']}?subject={up.quote(u['mail_subject'])}"
sms = f"sms:{PERSON['phone_intl']}?&body={up.quote(u['sms_body'])}"
contact = f"""
<section class="sec contact" id="contact" data-bg="#0b0b0c">
  <div class="col">
    {sec_head('07', 'Contact', u['contact_intro'])}
    <p class="giant" aria-hidden="true">{lines('Échangeons.')}</p>
    <div class="c-rows">
      <a class="c-row rv" href="{e(sms)}"><span class="mono">Téléphone · SMS</span><strong>{PERSON['phone_display']}</strong>{ARROW}</a>
      <a class="c-row rv" href="{e(mail)}"><span class="mono">E-mail</span><strong>{PERSON['email']}</strong>{ARROW}</a>
      <a class="c-row rv" href="{PERSON['linkedin']}" target="_blank" rel="noopener"><span class="mono">LinkedIn</span><strong>yoan-rousselot</strong>{ARROW}</a>
      <div class="c-row rv static"><span class="mono">Ville</span><strong>{e(PERSON['city'][L])}</strong><em>{e(u['c_mobile'])}</em></div>
    </div>
    <p class="call-line rv"><a class="tlink" href="tel:{PERSON['phone_intl']}">Ou appelez-moi directement{ARROW}</a></p>
  </div>
  <footer class="foot col mono"><span>© 2026 Yoan Rousselot</span><a href="#top">Haut de page ↑</a></footer>
</section>"""

NAV = [("profil", "Profil"), ("competences", "Compétences"), ("parcours", "Parcours"), ("projets", "Projets"),
       ("recommandations", "Recommandations"), ("contact", "Contact")]


def shell(title, body, root="", home=""):
    """Gabarit commun. root : chemin vers la racine ("" ou "../") ; home : préfixe des ancres ("" ou "../index.html")."""
    nav_html = "".join(f'<a href="{home}#{a}"><i class="mono">{i:02d}</i>{e(t)}</a>' for i, (a, t) in enumerate(NAV, 1))
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="robots" content="noindex">
<meta name="theme-color" content="#0b0b0c">
<link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{root}assets/style.css">
</head>
<body>
<div class="grain" aria-hidden="true"></div>
<div class="progress" aria-hidden="true"><span></span></div>
<header class="top">
  <a class="mark" href="{home}#top" aria-label="Accueil"><b>YR</b><span>Yoan Rousselot</span></a>
  <nav class="top-nav" aria-label="Navigation">{nav_html}</nav>
  <button class="burger" aria-expanded="false" aria-label="Menu"><span></span><span></span></button>
</header>
<main>
{body}
</main>
<div class="lightbox" hidden role="dialog" aria-modal="true" aria-label="Image agrandie">
  <button class="lb-close mono" aria-label="Fermer">Fermer ×</button>
  <figure><img alt=""><figcaption class="mono"></figcaption></figure>
</div>
<script src="{root}assets/main.js" defer></script>
</body>
</html>
"""


def write(rel, content):
    path = os.path.join(HERE, *rel.split("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)


write("index.html", shell("Yoan Rousselot · Portfolio",
                          hero + profil + competences + parcours + projets + recommandations + au_dela + contact))

# ------------------------------------------------------------------ pages détaillées
PHOTO = ("gend-", "armee", "blockout", "voyage", "parachut", "profil", "rouge-et-or", "usmb", "libm", "laval", "curiosite")
BACK = '<svg class="arr back-arr" viewBox="0 0 24 24" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'


def kind_of(img):
    return "" if img.startswith(PHOTO) else " plan"


def expand(body, root):
    """Balises du contenu : [[fig:image|légende]], [[stats:valeur~libellé;...]], [[formulas:formule~libellé;...]]."""
    def fig(m):
        img, cap = m.group(1), m.group(2)
        return (f'<figure class="d-fig{kind_of(img)}"><button class="zoom" data-src="{root}assets/img/{img}" data-cap="{e(cap)}" aria-label="Agrandir : {e(cap)}">'
                f'<img src="{root}assets/img/{img}" alt="{e(cap)}" loading="lazy"></button><figcaption class="mono">{e(cap)}</figcaption></figure>')

    def tiles(cls):
        def render(m):
            items = [it.split("~", 1) for it in m.group(1).split(";")]
            return f'<div class="{cls}">' + "".join(
                f'<div class="tile"><span class="tile-v">{e(v)}</span><span class="tile-l">{e(l)}</span></div>' for v, l in items) + "</div>"
        return render

    body = re.sub(r"\[\[fig:([^|\]]+)\|([^\]]+)\]\]", fig, body)
    body = re.sub(r"\[\[stats:([^\]]+)\]\]", tiles("tiles"), body)
    body = re.sub(r"\[\[formulas:([^\]]+)\]\]", tiles("tiles formulas"), body)
    return body


ordered = [PAGE[s] for s in TIMELINE_ORDER if isinstance(s, str)]
for i, p in enumerate(ordered):
    d = p[L]
    root, home = "../", "../index.html"
    tag = u["type_labels"][p["kind"]]
    back_anchor = "projets" if p["kind"] == "project" else "parcours"
    back_label = u["back_projects"] if p["kind"] == "project" else u["back_path"]

    cover = ""
    if p.get("cover"):
        credit = p.get("cover_credit", {}).get(L, "")
        cap = f'<figcaption class="mono">{e(credit)}</figcaption>' if credit else ""
        cover = (f'<figure class="d-cover{kind_of(p["cover"])}{" wide" if p.get("cover_class") else ""} rv">'
                 f'<img src="{root}assets/img/{p["cover"]}" alt="">{cap}</figure>')

    facts = "".join(f'<div class="fact"><dt class="mono">{e(k)}</dt><dd>{e(v)}</dd></div>'
                    for k, v in ((u["period"], d["period"]), (u["place"], d["place"]), (u["role"], d["role"])))
    highlights = ""
    if d.get("highlights"):
        highlights = '<div class="stats d-stats">' + "".join(
            f'<div class="stat rv"><span class="stat-v">{e(v)}</span><span class="stat-l">{e(l)}</span></div>' for v, l in d["highlights"]) + "</div>"

    blocks = ""
    for k, (h, body) in enumerate(d["sections"], 1):
        blocks += (f'<section class="d-block"><header class="d-block-head rv"><span class="mono idx">{k:02d}</span><h2>{e(h)}</h2></header>'
                   f'<div class="d-content rv">{expand(body, root)}</div></section>')
    k = len(d["sections"]) + 1
    blocks += (f'<section class="d-block"><header class="d-block-head rv"><span class="mono idx">{k:02d}</span><h2>{e(u["skills_dev"])}</h2></header>'
               f'<div class="d-content rv"><ul class="dots three">{"".join(f"<li>{e(x)}</li>" for x in d["skills"])}</ul></div></section>')
    if p.get("letter"):
        R = LETTERS[p["letter"]]
        r = R[L]
        k += 1
        blocks += f"""<section class="d-block"><header class="d-block-head rv"><span class="mono idx">{k:02d}</span><h2>{e(u['reco_short'])}</h2></header>
  <figure class="d-content d-reco rv">
    <blockquote>{e(r['quote'])}</blockquote>
    <figcaption><strong>{e(R['name'])}</strong><span>{e(r['role'])}</span>
      <a class="tlink" href="{root}assets/docs/{R['pdf']}" target="_blank" rel="noopener">{e(u['read_letter'])}{ARROW}</a></figcaption>
  </figure></section>"""
    if p.get("gallery"):
        k += 1
        items = "".join(
            f'<figure class="g{kind_of(img)}"><button class="zoom" data-src="{root}assets/img/{img}" data-cap="{e(cfr)}" aria-label="Agrandir : {e(cfr)}">'
            f'<img src="{root}assets/img/{img}" alt="{e(cfr)}" loading="lazy"></button><figcaption class="mono">{e(cfr)}</figcaption></figure>'
            for img, cfr, _cen in p["gallery"])
        blocks += (f'<section class="d-block"><header class="d-block-head rv"><span class="mono idx">{k:02d}</span><h2>{e(u["gallery"])}</h2></header>'
                   f'<div class="d-content d-gallery rv">{items}</div></section>')

    prev_p = ordered[i - 1] if i > 0 else None
    next_p = ordered[i + 1] if i + 1 < len(ordered) else None

    def pn(q, label, cls):
        if not q:
            return "<span></span>"
        return (f'<a class="pn {cls}" href="{root}{page_url(q)}"><span class="mono">{e(label)}</span>'
                f'<strong>{e(q[L]["short"])}</strong><span class="mono dim">{e(q[L]["period"])}</span></a>')

    title_words = d["title"].split(" : ")
    body = f"""
<section class="d-hero" data-bg="#0b0b0c">
  <div class="col">
    <a class="tlink back" href="{home}#{back_anchor}">{BACK}{e(back_label)}</a>
    <p class="mono d-meta rv"><span class="idx">{e(tag)}</span><span>{e(d['period'])}</span><span>{e(d['place'])}</span></p>
    <h1 class="d-title">{lines(*[e(w) for w in title_words])}</h1>
    <p class="d-org rv">{e(d['org'])}</p>
    <div class="d-top{' has-cover' if cover else ''}">
      <p class="d-summary rv">{e(d['summary'])}</p>
      {cover}
    </div>
    <dl class="facts rv">{facts}</dl>
    {highlights}
  </div>
</section>
<section class="sec d-body" data-bg="#100f0d">
  <div class="col">{blocks}</div>
</section>
<section class="d-end" data-bg="#0b0b0c">
  <nav class="col pn-row" aria-label="Autres pages">
    {pn(prev_p, u['prev'], 'pn-prev')}
    {pn(next_p, u['next'], 'pn-next')}
  </nav>
  <footer class="foot col mono"><span>© 2026 Yoan Rousselot</span><a href="{home}#contact">Me contacter ↗</a></footer>
</section>"""
    write(page_url(p), shell(f"{d['title']} · Yoan Rousselot", body, root, home))

print("pages écrites :", 1 + len(ordered))
