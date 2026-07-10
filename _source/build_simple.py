#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, html, shutil
from bs4 import BeautifulSoup

SRC = "/home/claude/orig/bakardi/bakardi-main/bakardi-main"
BUILD = "/home/claude/build"
OUT = "/home/claude/build/simple_site"
os.makedirs(OUT, exist_ok=True)
os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)

CSS = open(os.path.join(BUILD, "simple.css"), encoding="utf-8").read()
JS  = open(os.path.join(BUILD, "leto-green.js"), encoding="utf-8").read()  # toggle+nav+reveal (cursor self-gates on data-cursor, which we never set)

for f in os.listdir(os.path.join(BUILD, "assets")):
    shutil.copy(os.path.join(BUILD, "assets", f), os.path.join(OUT, "assets", f))

FONTS = ""  # fonts are self-hosted via @font-face in the stylesheet

def esc(s): return html.escape(s or "", quote=True)
def vis(s): return html.escape(s or "", quote=False)

def svg(body):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{body}</svg>'
IC = {
 "phone":svg('<path d="M6.5 3.5 9 4l1 4-2 1.5a12 12 0 0 0 6 6L15 14l4 1 .5 2.5a2 2 0 0 1-2 2.3A16 16 0 0 1 4.2 5.5a2 2 0 0 1 2.3-2Z"/>'),
 "pin":svg('<path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11Z"/><circle cx="12" cy="10" r="2.6"/>'),
 "clock":svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>'),
 "arrow":svg('<path d="M7 17 17 7M9 7h8v8"/>'),
 "back":svg('<path d="M15 6l-6 6 6 6"/>'),
 "coffee":svg('<path d="M4 9h13v4a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5Z"/><path d="M17 10h2.4a2.4 2.4 0 0 1 0 4.8H17"/><path d="M8 5.5c-.5.6-.5 1.2 0 1.8M12 5c-.5.6-.5 1.2 0 1.8"/>'),
 "grill":svg('<circle cx="12" cy="10" r="7"/><path d="M8 8h8M8 11h8M9 17l-1 4M15 17l1 4"/>'),
 "beer":svg('<path d="M6 7h10v11a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2Z"/><path d="M16 9h2.5a2.5 2.5 0 0 1 0 5H16"/><path d="M6 7c0-2 2.2-3 5-3s5 1 5 3"/><path d="M9 12v5M12.5 12v5"/>'),
 "instagram":svg('<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17" cy="7" r="1.1" fill="currentColor" stroke="none"/>'),
 "facebook":svg('<path d="M14 8h2V5h-2a3 3 0 0 0-3 3v2H9v3h2v6h3v-6h2.2l.8-3H14v-2a1 1 0 0 1 1-1Z" fill="currentColor" stroke="none"/>'),
 "new":svg('<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M18 6l-2.5 2.5M8.5 15.5 6 18"/><circle cx="12" cy="12" r="2.4"/>'),
 "breakfast":svg('<ellipse cx="11" cy="13" rx="8" ry="6"/><circle cx="11" cy="13" r="3.2" fill="currentColor" stroke="none" opacity=".85"/>'),
 "salads":svg('<path d="M4 11h16a8 8 0 0 1-16 0Z"/><path d="M9 11c0-3 2-5 4-5M13 11c1-2 3-3 5-3"/>'),
 "starters":svg('<path d="M7 9h10l-.8 9.5a1.5 1.5 0 0 1-1.5 1.4H9.3a1.5 1.5 0 0 1-1.5-1.4Z"/><path d="M9 9V5.5M12 9V5M15 9V5.5"/>'),
 "furnarinki":svg('<ellipse cx="12" cy="12" rx="9" ry="6"/><path d="M7 10.5c1.5 1 3 1 4.5 0M12.5 13c1.4 1 3 1 4.5 0"/>'),
 "pizza":svg('<path d="M12 3 21 19a1 1 0 0 1-1 1.4L4.5 19.7A1 1 0 0 1 4 18.2L11 3.5a.6.6 0 0 1 1 0Z"/><circle cx="11" cy="10" r="1.1" fill="currentColor" stroke="none"/><circle cx="9.5" cy="14" r="1.1" fill="currentColor" stroke="none"/><circle cx="13" cy="14.5" r="1.1" fill="currentColor" stroke="none"/>'),
 "cheese":svg('<path d="M3 15 14 6l7 3v6a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1Z"/><circle cx="8" cy="13" r="1" fill="currentColor" stroke="none"/><circle cx="13" cy="12" r="1" fill="currentColor" stroke="none"/>'),
 "pasta":svg('<path d="M4 13h16a8 8 0 0 1-16 0Z"/><path d="M7 13c0-4 1-8 2-9M11 13c0-4 .5-8 1-9M15 13c0-4 1-8 2-9"/>'),
 "panzerotti":svg('<path d="M5 12a7 7 0 0 1 14 0Z"/><path d="M5 12a7 7 0 0 0 14 0"/><path d="M9 9.5c1 .8 2 .8 3 0"/>'),
 "specials":svg('<path d="M12 3.5 14 9l5.5.2-4.4 3.4L16.7 18 12 14.8 7.3 18l1.6-5.4L4.5 9.2 10 9Z"/>'),
 "daska":svg('<rect x="3" y="6" width="14" height="12" rx="2"/><path d="M17 9h3M17 12h4M17 15h3"/><path d="M7 9.5h6M7 12h5"/>'),
 "sandwich":svg('<path d="M4 8.5C4 6.6 7.6 5 12 5s8 1.6 8 3.5"/><path d="M4 8.5h16M4 12h16M5 15.5h14"/><path d="M4 15.5c0 1.9 3.6 3.5 8 3.5s8-1.6 8-3.5"/>'),
 "rolls":svg('<rect x="3.5" y="8" width="17" height="8" rx="4"/><path d="M8 8v8M13 8v8"/>'),
 "extras":svg('<circle cx="12" cy="12" r="9"/><path d="M12 8v8M8 12h8"/>'),
 "desserts":svg('<path d="M6 11h12l-1.4 8.2a1.5 1.5 0 0 1-1.5 1.3H8.9a1.5 1.5 0 0 1-1.5-1.3Z"/><path d="M9 11a3 3 0 0 1 6 0"/><circle cx="12" cy="4" r="1.2" fill="currentColor" stroke="none"/><path d="M12 5v3"/>'),
 "hotbev":svg('<path d="M4 9h13v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5Z"/><path d="M17 10h2.5a2.5 2.5 0 0 1 0 5H17"/><path d="M8 5.5c-.6.7-.6 1.3 0 2M12 5c-.6.7-.6 1.3 0 2"/>'),
 "nonalc":svg('<path d="M9 3h6M10 3v2.5l-1.6 3A4 4 0 0 0 8 10.4V19a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2v-8.6a4 4 0 0 0-.4-1.9L14 5.5V3"/><path d="M8 13h8"/>'),
 "wine":svg('<path d="M7 3h10l-.6 5a4.4 4.4 0 0 1-8.8 0Z"/><path d="M12 12.5V19M8.5 21h7"/>'),
 "alcohol":svg('<path d="M10 3h4M11 3v3M13 3v3M10.5 6.5 9 9v10a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2V9l-1.5-2.5"/><path d="M9 14h6"/>'),
}
PHONE="076-599-566"; PHONE2="078-640-222"; IG="https://www.instagram.com/bakardikicevo/"; FB="https://www.facebook.com/bakardiofficial"

def head(title, desc=""):
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
      '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
      f'<title>{esc(title)}</title>'+(f'<meta name="description" content="{esc(desc)}">' if desc else '')
      +'<link rel="icon" href="assets/favicon.ico">'+FONTS+f'<style>{CSS}</style></head>')

def header(active=""):
    def L(href,en,mk,key):
        c="navlink active" if active==key else "navlink"
        return f'<a class="{c}" href="{href}" data-en="{esc(en)}" data-mk="{esc(mk)}">{en}</a>'
    return ('<header class="site-header"><div class="wrap">'
      '<a class="brand" href="index.html"><img src="assets/bakardi-cream.png" alt="Bakardi"></a>'
      '<nav class="nav" aria-label="Main">'
      +L("standard%20menu.html","Standard Menu","\u0421\u0442\u0430\u043d\u0434\u0430\u0440\u0434\u043d\u043e \u041c\u0435\u043d\u0438","standard")
      +L("fasting-menu.html","Fasting Menu","\u041f\u043e\u0441\u043d\u043e \u041c\u0435\u043d\u0438","fasting")
      +L("Drinks.html","Drinks","\u041f\u0438\u0458\u0430\u043b\u043e\u0446\u0438","drinks")
      +'<div class="lang" role="group" aria-label="Language"><button data-lang="en" class="on" type="button">EN</button><button data-lang="mk" type="button">MK</button></div>'
      f'<a class="call-chip" href="tel:076599566">{IC["phone"]}{PHONE}</a></nav>'
      '<button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>'
      '</div></header>')

def footer():
    return ('<footer class="site-footer"><div class="wrap">'
      '<div class="foot-top">'
        '<div class="foot-logo"><img src="assets/bakardi-cream.png" alt="Bakardi"></div>'
        '<div class="foot-grid">'
          '<div><h4 data-en="Address" data-mk="\u0410\u0434\u0440\u0435\u0441\u0430">Address</h4>'
            '<p data-en="Bul. Ilinden 18" data-mk="\u0411\u0443\u043b. \u0418\u043b\u0438\u043d\u0434\u0435\u043d \u0431\u0440.18">Bul. Ilinden 18</p>'
            '<p data-en="Ki\u010devo, 6250" data-mk="\u041a\u0438\u0447\u0435\u0432\u043e, 6250">Ki\u010devo, 6250</p>'
            '<p><a href="lokacija.html" data-en="Location \u2192" data-mk="\u041b\u043e\u043a\u0430\u0446\u0438\u0458\u0430 \u2192">Location \u2192</a></p></div>'
          '<div><h4 data-en="Hours" data-mk="\u0420\u0430\u0431\u043e\u0442\u043d\u043e \u0432\u0440\u0435\u043c\u0435">Hours</h4>'
            '<p data-en="Mon - Sat  07-00" data-mk="\u041f\u043e\u043d - \u0421\u0430\u0431  07-00">Mon - Sat  07-00</p>'
            '<p data-en="Sun  15-00" data-mk="\u041d\u0435\u0434  15-00">Sun  15-00</p></div>'
          '<div><h4 data-en="Contact" data-mk="\u041a\u043e\u043d\u0442\u0430\u043a\u0442">Contact</h4>'
            f'<p><span data-en="Delivery" data-mk="\u0414\u043e\u0441\u0442\u0430\u0432\u0430">Delivery</span>: <a href="tel:076599566">{PHONE}</a></p>'
            f'<p><span data-en="Pick-up" data-mk="\u041f\u043e\u0434\u0438\u0433\u043d\u0443\u0432\u0430\u045a\u0435">Pick-up</span>: <a href="tel:078640222">{PHONE2}</a></p>'
            f'<div class="foot-socials"><a href="{IG}" aria-label="Instagram" target="_blank" rel="noopener">{IC["instagram"]}</a>'
            f'<a href="{FB}" aria-label="Facebook" target="_blank" rel="noopener">{IC["facebook"]}</a></div></div>'
        '</div>'
      '</div>'
      '<div class="foot-bottom"><span>© 2026 Bakardi · Ki\u010devo</span>'
      '<span data-en="Restaurant · Lounge Bar" data-mk="\u0420\u0435\u0441\u0442\u043e\u0440\u0430\u043d · Lounge Bar">Restaurant · Lounge Bar</span></div>'
      '</div></footer>')

def scripts(): return f'<script>{JS}</script></body></html>'

# ---------- bilingual text reconstruction ----------
def el_bilingual(el):
    from bs4 import NavigableString, Tag
    if el is None: return "",""
    if el.has_attr('data-en'):
        return el['data-en'].strip(), el.get('data-mk', el['data-en']).strip()
    en,mk=[],[]
    for node in el.children:
        if isinstance(node,NavigableString):
            t=str(node).strip()
            if t: en.append(t); mk.append(t)
        elif isinstance(node,Tag):
            e,m=el_bilingual(node)
            if e: en.append(e)
            if m: mk.append(m)
    return re.sub(r'\s+',' ',' '.join(en)).strip(), re.sub(r'\s+',' ',' '.join(mk)).strip()

def parse_standard(soup):
    sections=[]
    for cont in soup.select('.menu-container'):
        te=cont.find(class_='ovakvo'); ten,tmk=el_bilingual(te) if te else ("","")
        entries=[]
        for mi in cont.select('.menu-item'):
            meats=mi.find(class_='meats')
            if meats:
                h=mi.find(['h3','h2']); hen,hmk=el_bilingual(h) if h else ("","")
                items=[]
                for p in meats.select('p.explain'):
                    e,m=el_bilingual(p)
                    if e: items.append((e.lstrip('-').strip(),m.lstrip('-').strip()))
                entries.append(('list',hen,hmk,items)); continue
            drink=mi.find(class_='drink')
            if not drink: continue
            nen,nmk=el_bilingual(drink)
            price=mi.find(class_='price') or mi.find(class_='specialprice')
            pen,pmk=el_bilingual(price) if price else ("","")
            den=dmk=""
            sib=mi.find_next_sibling()
            while sib and getattr(sib,'name',None) and 'explain' not in (sib.get('class') or []) and sib.name=='div' and not sib.get('class'):
                sib=sib.find_next_sibling()
            if sib and 'explain' in (sib.get('class') or []): den,dmk=el_bilingual(sib)
            entries.append(('item',nen,nmk,pen,pmk,den,dmk))
        sections.append((ten,tmk,"","",entries))
    return sections

def parse_fasting(soup):
    from bs4 import Tag
    sections=[]
    for mi in soup.select('.menu-column > .menu-item'):
        h2=mi.find('h2'); h3=mi.find('h3')
        ten,tmk=el_bilingual(h2) if h2 else ("","")
        suben,submk=el_bilingual(h3) if h3 else ("","")
        entries=[]; ul=mi.find('ul'); pending=None
        if ul:
            for node in ul.children:
                if not isinstance(node,Tag): continue
                if node.name=='li':
                    b=node.find('b'); nen,nmk=el_bilingual(b) if b else el_bilingual(node)
                    full=node.get_text(" ",strip=True); bt=b.get_text(" ",strip=True) if b else ""
                    price=full.replace(bt,"",1).strip().lstrip('-').strip()
                    pending=['item',nen,nmk,price,price,"",""]; entries.append(pending)
                elif node.name=='span':
                    e,m=el_bilingual(node)
                    if pending is not None: pending[5]=e; pending[6]=m
        sections.append((ten,tmk,suben,submk,[tuple(x) for x in entries]))
    return sections

# ---------- render ----------
def render_entries(entries):
    out=['<div class="rows">']
    for e in entries:
        if e[0]=='item':
            _,nen,nmk,pen,pmk,den,dmk=e
            nm=f'<span class="nm" data-en="{esc(nen)}" data-mk="{esc(nmk)}">{vis(nen)}</span>'
            pr=f'<span class="dots"></span><span class="pr" data-en="{esc(pen)}" data-mk="{esc(pmk or pen)}">{vis(pen)}</span>' if pen else ''
            desc=f'<div class="desc" data-en="{esc(den)}" data-mk="{esc(dmk or den)}">{vis(den)}</div>' if den else ''
            out.append(f'<div class="item"><div class="top">{nm}{pr}</div>{desc}</div>')
        elif e[0]=='list':
            _,hen,hmk,items=e
            chips=''.join(f'<span class="chip" data-en="{esc(a)}" data-mk="{esc(b)}">{vis(a)}</span>' for a,b in items)
            out.append(f'</div><div class="note"><h4 data-en="{esc(hen)}" data-mk="{esc(hmk)}">{vis(hen)}</h4><div class="chips">{chips}</div></div><div class="rows">')
    out.append('</div>'); return ''.join(out)

def render_section(sec):
    ten,tmk,suben,submk,entries=sec; h=''
    if ten: h+=f'<div class="sec-title"><h2 data-en="{esc(ten)}" data-mk="{esc(tmk)}">{vis(ten)}</h2><span class="rule"></span></div>'
    if suben: h+=f'<p class="sec-sub" data-en="{esc(suben)}" data-mk="{esc(submk)}">{vis(suben)}</p>'
    return f'<div class="menu-section reveal">{h}{render_entries(entries)}</div>'

def menu_page(title_en,title_mk,sections,parent,active,sub_en="",sub_mk=""):
    ph,pl=parent
    back=f'<a class="back-link" href="{ph}" data-en="{esc(pl[0])}" data-mk="{esc(pl[1])}">{IC["back"]}{pl[0]}</a>'
    sub=f'<p class="sub" data-en="{esc(sub_en)}" data-mk="{esc(sub_mk)}">{vis(sub_en)}</p>' if sub_en else ''
    body=''.join(render_section(s) for s in sections)
    return (head(f"Bakardi — {title_en}")+'<body>'+header(active)+
      f'<section class="page-hero"><div class="narrow">{back}<h1 data-en="{esc(title_en)}" data-mk="{esc(title_mk)}">{vis(title_en)}</h1>{sub}</div></section>'
      f'<section class="menu-body"><div class="narrow">{body}</div></section>'+footer()+scripts())

def hub_page(title_en,title_mk,eye_en,eye_mk,active,cats):
    cards=''.join(
      f'<a class="cat reveal" href="{href}"><div class="top"><span class="cat-ic">{IC[icon]}</span><span class="arrow">{IC["arrow"]}</span></div>'
      f'<h3 data-en="{esc(en)}" data-mk="{esc(mk)}">{vis(en)}</h3>'
      f'<p data-en="{esc(ten)}" data-mk="{esc(tmk)}">{vis(ten_:=ten)}</p></a>'
      for en,mk,href,icon,ten,tmk in cats)
    return (head(f"Bakardi — {title_en}")+'<body>'+header(active)+
      f'<section class="page-hero"><div class="wrap"><a class="back-link" href="index.html" data-en="Home" data-mk="\u041f\u043e\u0447\u0435\u0442\u043d\u0430">{IC["back"]}Home</a>'
      f'<h1 data-en="{esc(title_en)}" data-mk="{esc(title_mk)}">{vis(title_en)}</h1></div></section>'
      f'<section class="hub"><div class="wrap"><div class="cat-grid">{cards}</div></div></section>'+footer()+scripts())

def home_page():
    hero=('<section class="hero"><div class="wrap">'
      '<img class="logo-mark" src="assets/bakardi-green.png" alt="Bakardi">'
      '<span class="eyebrow" data-en="Restaurant · Lounge Bar · Ki\u010devo" data-mk="\u0420\u0435\u0441\u0442\u043e\u0440\u0430\u043d · Lounge Bar · \u041a\u0438\u0447\u0435\u0432\u043e">Restaurant · Lounge Bar · Ki\u010devo</span>'
      '<p class="tag" data-en="Tasty food, good coffee and a full bar — from morning mekici to a cold beer." '
        'data-mk="\u0412\u043a\u0443\u0441\u043d\u0430 \u0445\u0440\u0430\u043d\u0430, \u0434\u043e\u0431\u0440\u043e \u043a\u0430\u0444\u0435 \u0438 \u043f\u043e\u043b\u043d \u0431\u0430\u0440 — \u043e\u0434 \u0458\u0443\u0442\u0440\u0435\u0448\u043d\u0438 \u043c\u0435\u043a\u0438\u0446\u0438 \u0434\u043e \u043b\u0430\u0434\u043d\u043e \u043f\u0438\u0432\u043e.">Tasty food, good coffee and a full bar — from morning mekici to a cold beer.</p>'
      '<div class="cta">'
        '<a class="btn btn-green" href="standard%20menu.html" data-en="Standard Menu" data-mk="\u0421\u0442\u0430\u043d\u0434\u0430\u0440\u0434\u043d\u043e \u041c\u0435\u043d\u0438">Standard Menu</a>'
        '<a class="btn btn-outline" href="fasting-menu.html" data-en="Fasting Menu" data-mk="\u041f\u043e\u0441\u043d\u043e \u041c\u0435\u043d\u0438">Fasting Menu</a>'
        '<a class="btn btn-outline" href="Drinks.html" data-en="Drinks" data-mk="\u041f\u0438\u0458\u0430\u043b\u043e\u0446\u0438">Drinks</a>'
      '</div></div></section>')
    info=('<section class="section alt"><div class="wrap"><div class="info-grid">'
      f'<div class="info reveal"><div class="ic">{IC["pin"]}</div><h3 data-en="Address" data-mk="\u0410\u0434\u0440\u0435\u0441\u0430">Address</h3>'
        '<p data-en="Bul. Ilinden 18, Ki\u010devo, 6250" data-mk="\u0411\u0443\u043b. \u0418\u043b\u0438\u043d\u0434\u0435\u043d \u0431\u0440.18, \u041a\u0438\u0447\u0435\u0432\u043e, 6250">Bul. Ilinden 18, Ki\u010devo, 6250</p>'
        '<p><a href="lokacija.html" data-en="Open map \u2192" data-mk="\u041e\u0442\u0432\u043e\u0440\u0438 \u043c\u0430\u043f\u0430 \u2192">Open map \u2192</a></p></div>'
      f'<div class="info reveal"><div class="ic">{IC["clock"]}</div><h3 data-en="Hours" data-mk="\u0420\u0430\u0431\u043e\u0442\u043d\u043e \u0432\u0440\u0435\u043c\u0435">Hours</h3>'
        '<p data-en="Mon - Sat  07-00" data-mk="\u041f\u043e\u043d - \u0421\u0430\u0431  07-00">Mon - Sat  07-00</p>'
        '<p data-en="Sun  15-00" data-mk="\u041d\u0435\u0434  15-00">Sun  15-00</p></div>'
      f'<div class="info reveal"><div class="ic">{IC["phone"]}</div><h3 data-en="Contact" data-mk="\u041a\u043e\u043d\u0442\u0430\u043a\u0442">Contact</h3>'
        f'<p><span data-en="Delivery" data-mk="\u0414\u043e\u0441\u0442\u0430\u0432\u0430">Delivery</span>: <a href="tel:076599566">{PHONE}</a></p>'
        f'<p><span data-en="Pick-up" data-mk="\u041f\u043e\u0434\u0438\u0433\u043d\u0443\u0432\u0430\u045a\u0435">Pick-up</span>: <a href="tel:078640222">{PHONE2}</a></p></div>'
      '</div>'
      '<div class="info-foot reveal">'
        '<a class="btn btn-outline" href="lokacija.html" data-en="Find us" data-mk="\u041d\u0430\u0458\u0434\u0438 \u043d\u0435">Find us</a>'
        f'<div class="socials"><a href="{IG}" aria-label="Instagram" target="_blank" rel="noopener">{IC["instagram"]}</a>'
        f'<a href="{FB}" aria-label="Facebook" target="_blank" rel="noopener">{IC["facebook"]}</a></div>'
      '</div></div></section>')
    return (head("Bakardi Restaurant Kicevo | Meals, Coffee & Drinks",
                 "Bakardi Restaurant in Ki\u010devo — tasty food, good coffee and a full bar.")
      +'<body>'+header('')+hero+info+footer()+scripts())

def location_page():
    MAP="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d24604.561699648322!2d20.962551217612578!3d41.50395449744132!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x1351376ecee5f839%3A0x1d46ecf39a0eefcf!2sLounge%20Bar%20Bakardi!5e0!3m2!1sen!2smk!4v1695235475731!5m2!1sen!2smk"
    return (head("Bakardi — Location")+'<body>'+header('')+
      '<section class="page-hero"><div class="wrap">'
      f'<a class="back-link" href="index.html" data-en="Home" data-mk="\u041f\u043e\u0447\u0435\u0442\u043d\u0430">{IC["back"]}Home</a>'
      '<h1 data-en="Location" data-mk="\u041b\u043e\u043a\u0430\u0446\u0438\u0458\u0430">Location</h1></div></section>'
      '<section class="map-wrap"><div class="wrap">'
      f'<div class="map-frame reveal"><iframe src="{MAP}" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Bakardi on Google Maps"></iframe></div>'
      '<div class="map-meta">'
      '<div class="reveal"><h4 data-en="Address" data-mk="\u0410\u0434\u0440\u0435\u0441\u0430">Address</h4><p data-en="Bul. Ilinden 18, Ki\u010devo, 6250" data-mk="\u0411\u0443\u043b. \u0418\u043b\u0438\u043d\u0434\u0435\u043d \u0431\u0440.18, \u041a\u0438\u0447\u0435\u0432\u043e, 6250">Bul. Ilinden 18, Ki\u010devo, 6250</p></div>'
      '<div class="reveal"><h4 data-en="Hours" data-mk="\u0420\u0430\u0431\u043e\u0442\u043d\u043e \u0432\u0440\u0435\u043c\u0435">Hours</h4><p data-en="Mon-Sat 07-00 · Sun 15-00" data-mk="\u041f\u043e\u043d-\u0421\u0430\u0431 07-00 · \u041d\u0435\u0434 15-00">Mon-Sat 07-00 · Sun 15-00</p></div>'
      f'<div class="reveal"><h4 data-en="Contact" data-mk="\u041a\u043e\u043d\u0442\u0430\u043a\u0442">Contact</h4><p><span data-en="Delivery" data-mk="\u0414\u043e\u0441\u0442\u0430\u0432\u0430">Delivery</span>: <a href="tel:076599566">{PHONE}</a><br><span data-en="Pick-up" data-mk="\u041f\u043e\u0434\u0438\u0433\u043d\u0443\u0432\u0430\u045a\u0435">Pick-up</span>: <a href="tel:078640222">{PHONE2}</a></p></div>'
      '</div></div></section>'+footer()+scripts())

def read(f): return BeautifulSoup(open(os.path.join(SRC,f),encoding="utf-8").read(),'html.parser')

STD=("standard%20menu.html",("Standard menu","\u0421\u0442\u0430\u043d\u0434\u0430\u0440\u0434\u043d\u043e \u043c\u0435\u043d\u0438"))
DRK=("Drinks.html",("Drinks","\u041f\u0438\u0458\u0430\u043b\u043e\u0446\u0438"))
CAT_PAGES=[
 ("new.html","New","\u041d\u043e\u0432\u043e",STD,"standard"),("breakfast.html","Breakfast","\u0414\u043e\u0440\u0443\u0447\u0435\u043a",STD,"standard"),
 ("salads.html","Salads","\u0421\u0430\u043b\u0430\u0442\u0438",STD,"standard"),("starters.html","Starters","\u041c\u0435\u0437\u0435",STD,"standard"),
 ("furnarinki.html","Furnarinki","\u0424\u0443\u0440\u043d\u0430\u0440\u0438\u043d\u043a\u0438",STD,"standard"),("pizza.html","Pizza","\u041f\u0438\u0446\u0430",STD,"standard"),
 ("cheese.html","Cheese","\u0421\u0438\u0440\u0435\u045a\u0435",STD,"standard"),("pasta.html","Pasta","\u041f\u0430\u0441\u0442\u0430",STD,"standard"),
 ("panzerotti.html","Panzerotti","\u041f\u0430\u043d\u0446\u0435\u0440\u043e\u0442\u0438",STD,"standard"),("specials.html","Specials","\u0421\u043f\u0435\u0446\u0438\u0458\u0430\u043b\u0438\u0442\u0435\u0442\u0438",STD,"standard"),
 ("daska.html","Daska","\u0414\u0430\u0441\u043a\u0430",STD,"standard"),("sandwich.html","Sandwiches","\u0421\u0435\u043d\u0434\u0432\u0438\u0447\u0438",STD,"standard"),
 ("rollS.html","Roll Sandwiches","\u0420\u043e\u043b \u0421\u0435\u043d\u0434\u0432\u0438\u0447\u0438",STD,"standard"),("extras.html","Extras","\u0414\u043e\u0434\u0430\u0442\u043e\u0446\u0438",STD,"standard"),
 ("desserts.html","Desserts","\u0414\u0435\u0441\u0435\u0440\u0442\u0438",STD,"standard"),
 ("hotbev.html","Hot Beverages","\u0422\u043e\u043f\u043b\u0438 \u041f\u0438\u0458\u0430\u043b\u043e\u0446\u0438",DRK,"drinks"),("nonAlc.html","Non-Alcoholic","\u0411\u0435\u0437\u0430\u043b\u043a\u043e\u0445\u043e\u043b\u043d\u0438",DRK,"drinks"),
 ("beer.html","Beer","\u041f\u0438\u0432\u043e",DRK,"drinks"),("wine.html","Wine","\u0412\u0438\u043d\u043e",DRK,"drinks"),("alcohol.html","Alcohol","\u0410\u043b\u043a\u043e\u0445\u043e\u043b",DRK,"drinks"),
]
STD_CATS=[
 ("New","\u041d\u043e\u0432\u043e","new.html","new","Latest additions","\u041d\u043e\u0432\u0438 \u0458\u0430\u0434\u0435\u045a\u0430"),
 ("Breakfast","\u0414\u043e\u0440\u0443\u0447\u0435\u043a","breakfast.html","breakfast","Omelettes & mekici","\u041e\u043c\u043b\u0435\u0442\u0438 \u0438 \u043c\u0435\u043a\u0438\u0446\u0438"),
 ("Salads","\u0421\u0430\u043b\u0430\u0442\u0438","salads.html","salads","Fresh & light","\u0421\u0432\u0435\u0436\u0438 \u0438 \u043b\u0435\u0441\u043d\u0438"),
 ("Starters","\u041c\u0435\u0437\u0435","starters.html","starters","To begin","\u0417\u0430 \u043f\u043e\u0447\u0435\u0442\u043e\u043a"),
 ("Furnarinki","\u0424\u0443\u0440\u043d\u0430\u0440\u0438\u043d\u043a\u0438","furnarinki.html","furnarinki","Baked flatbreads","\u041f\u0435\u0447\u0435\u043d\u0438 \u043b\u0435\u043f\u0447\u0438\u045a\u0430"),
 ("Pizza","\u041f\u0438\u0446\u0430","pizza.html","pizza","& Pastrmajlija","\u0438 \u041f\u0430\u0441\u0442\u0440\u043c\u0430\u0458\u043b\u0438\u0458\u0430"),
 ("Cheese","\u0421\u0438\u0440\u0435\u045a\u0435","cheese.html","cheese","Grilled & fresh","\u041d\u0430 \u0441\u043a\u0430\u0440\u0430 \u0438 \u0441\u0432\u0435\u0436\u043e"),
 ("Pasta","\u041f\u0430\u0441\u0442\u0430","pasta.html","pasta","Macaroni & spaghetti","\u041c\u0430\u043a\u0430\u0440\u043e\u043d\u0438 \u0438 \u0448\u043f\u0430\u0433\u0435\u0442\u0438"),
 ("Panzerotti","\u041f\u0430\u043d\u0446\u0435\u0440\u043e\u0442\u0438","panzerotti.html","panzerotti","Folded & filled","\u0421\u043e \u0440\u0430\u0437\u043d\u0438 \u043f\u043e\u043b\u043d\u0435\u045a\u0430"),
 ("Specials","\u0421\u043f\u0435\u0446\u0438\u0458\u0430\u043b\u0438\u0442\u0435\u0442\u0438","specials.html","specials","House favourites","\u041a\u0443\u045c\u043d\u0438 \u0441\u043f\u0435\u0446\u0438\u0458\u0430\u043b\u0438\u0442\u0435\u0442\u0438"),
 ("Daska","\u0414\u0430\u0441\u043a\u0430","daska.html","daska","Sharing boards","\u0414\u0430\u0441\u043a\u0438 \u0437\u0430 \u0441\u043f\u043e\u0434\u0435\u043b\u0443\u0432\u0430\u045a\u0435"),
 ("Sandwiches","\u0421\u0435\u043d\u0434\u0432\u0438\u0447\u0438","sandwich.html","sandwich","& Burgers","\u0438 \u0411\u0443\u0440\u0433\u0435\u0440\u0438"),
 ("Roll Sandwiches","\u0420\u043e\u043b \u0421\u0435\u043d\u0434\u0432\u0438\u0447\u0438","rollS.html","rolls","Wraps & burritos","\u0420\u043e\u043b\u043e\u0432\u0438 \u0438 \u0431\u0443\u0440\u0438\u0442\u0430"),
 ("Extras","\u0414\u043e\u0434\u0430\u0442\u043e\u0446\u0438","extras.html","extras","Sides & sauces","\u041f\u0440\u0438\u043b\u043e\u0437\u0438 \u0438 \u0441\u043e\u0441\u043e\u0432\u0438"),
 ("Desserts","\u0414\u0435\u0441\u0435\u0440\u0442\u0438","desserts.html","desserts","Something sweet","\u041d\u0435\u0448\u0442\u043e \u0441\u043b\u0430\u0442\u043a\u043e"),
]
DRK_CATS=[
 ("Hot Beverages","\u0422\u043e\u043f\u043b\u0438 \u041f\u0438\u0458\u0430\u043b\u043e\u0446\u0438","hotbev.html","hotbev","Coffee & tea","\u041a\u0430\u0444\u0435 \u0438 \u0447\u0430\u0458"),
 ("Non-Alcoholic","\u0411\u0435\u0437\u0430\u043b\u043a\u043e\u0445\u043e\u043b\u043d\u0438","nonAlc.html","nonalc","Soft drinks & juice","\u0421\u043e\u043a\u043e\u0432\u0438 \u0438 \u043e\u0441\u0432\u0435\u0436\u0443\u0432\u0430\u045a\u0430"),
 ("Beer","\u041f\u0438\u0432\u043e","beer.html","beer","Draft & bottled","\u0422\u043e\u0447\u0435\u043d\u043e \u0438 \u0448\u0438\u0448\u0435"),
 ("Wine","\u0412\u0438\u043d\u043e","wine.html","wine","By glass or bottle","\u0427\u0430\u0448\u0430 \u0438\u043b\u0438 \u0448\u0438\u0448\u0435"),
 ("Alcohol","\u0410\u043b\u043a\u043e\u0445\u043e\u043b","alcohol.html","alcohol","Spirits & rakija","\u0416\u0435\u0441\u0442\u043e\u043a\u043e \u0438 \u0440\u0430\u043a\u0438\u0458\u0430"),
]

def W(name,content):
    with open(os.path.join(OUT,name),"w",encoding="utf-8") as f: f.write(content)

W("index.html",home_page())
W("lokacija.html",location_page())
W("standard menu.html",hub_page("Standard Menu","\u0421\u0442\u0430\u043d\u0434\u0430\u0440\u0434\u043d\u043e \u041c\u0435\u043d\u0438","The full menu","\u0426\u0435\u043b\u043e\u0442\u043e \u043c\u0435\u043d\u0438","standard",STD_CATS))
W("Drinks.html",hub_page("Drinks","\u041f\u0438\u0458\u0430\u043b\u043e\u0446\u0438","From the bar","\u041e\u0434 \u0431\u0430\u0440\u043e\u0442","drinks",DRK_CATS))
W("fasting-menu.html",menu_page("Fasting Menu","\u041f\u043e\u0441\u043d\u043e \u041c\u0435\u043d\u0438",parse_fasting(read("fasting-menu.html")),("index.html",("Home","\u041f\u043e\u0447\u0435\u0442\u043d\u0430")),"fasting","Vegan & lenten dishes.","\u041f\u043e\u0441\u043d\u0438 \u0458\u0430\u0434\u0435\u045a\u0430."))
for file,ten,tmk,parent,active in CAT_PAGES:
    W(file,menu_page(ten,tmk,parse_standard(read(file)),parent,active))

print("Built",len([f for f in os.listdir(OUT) if f.endswith('.html')]),"pages")
