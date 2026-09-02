#!/usr/bin/env python3
"""Re-apply the live page's metadata and section edits to a fresh index.html.

index.html at the repo root is a self-unpacking single-file bundle exported from
Claude Design ("The Rented Mind"). Every re-export starts from a bare shell
(<title>Bundled Page</title>, no metadata). This script makes the export
publishable again, idempotently:

  * outer shell + unpacked template both get: title, description, canonical,
    robots, theme-color, favicon set, manifest, Open Graph, Twitter card,
    article metadata, JSON-LD (marked so re-runs replace rather than stack)
  * a static summary for crawlers without JavaScript, under the loader
  * section 02 (Machines): the two 27B-class rigs read as "below the task",
    hollow bars for scale only, legend + verdict, matching the plates;
    section 03 gets the same dagger
  * assets/favicon.svg, assets/site.webmanifest, robots.txt, sitemap.xml, .nojekyll

    python3 generators/build_site.py                 # rewrite index.html in place
    python3 generators/build_site.py --input fresh.html
    python3 generators/build_site.py --render        # also re-render icons + og-banner.png
                                                     # (needs Chrome and sips, i.e. macOS)

Section edits are best-effort: if the export's text has moved on, the script
says which anchors it could not find and still writes everything else.
"""
import argparse, base64, gzip, html, json, math, os, pathlib, re, shutil, struct, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

URL = 'https://svetimfm.github.io/costCalcAI/'
REPO_URL = 'https://github.com/SvetimFM/costCalcAI'
TITLE = 'The Rented Mind · what one month of AI-assisted coding actually costs'
OG_TITLE = 'What one month of AI-assisted coding actually costs'
DESC = ('14.69 billion tokens, 71,350 requests, $200 paid against $14,914 metered. '
        'One month of AI-assisted coding priced against six home machines, every hour counted.')
IMG_ALT = ('Tan terminal-styled banner: "What one month of AI-assisted coding actually costs" with a red '
           'coil of re-read tokens and the figures 14.69B tokens, 71,350 requests, $200 paid vs $14,914 metered, ×74.6.')
KEYWORDS = ('local AI cost, LLM total cost of ownership, Claude Code, subscription vs API pricing, '
            'Mac Studio 512GB, RTX 5090, DGX Spark, Strix Halo, RTX 3090, local inference, '
            'open models, DeepSeek, Qwen, Du Bois data portraits, data art')
PUBLISHED, MODIFIED = '2026-08-31', '2026-09-02'

OUTER_START, OUTER_END = '<!-- seo:start -->', '<!-- seo:end -->'
INNER_START, INNER_END = '<meta name="x-seo" content="start">', '<meta name="x-seo" content="end">'

def esc(s): return html.escape(s, quote=True)

JSONLD = {
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": OG_TITLE,
  "alternativeHeadline": "The Rented Mind",
  "description": DESC,
  "url": URL,
  "mainEntityOfPage": URL,
  "image": [URL + "assets/og-banner.png"],
  "datePublished": PUBLISHED,
  "dateModified": MODIFIED,
  "inLanguage": "en",
  "author": {"@type": "Person", "name": "SvetimFM", "url": "https://github.com/SvetimFM"},
  "publisher": {"@type": "Organization", "name": "studiolo.svetim.fm", "url": "https://studiolo.svetim.fm",
                "logo": {"@type": "ImageObject", "url": URL + "assets/icon-512.png", "width": 512, "height": 512}},
  "keywords": KEYWORDS,
  "about": ["local LLM inference cost", "AI subscription economics", "total cost of ownership of desk hardware"],
  "isBasedOn": REPO_URL,
  "temporalCoverage": "2026-07-29/2026-08-28",
  "citation": "Chart style after the data portraits of W. E. B. Du Bois and the Atlanta University students, Paris Exposition, 1900."
}

def meta_block(rel='assets/'):
    tags = [
      f'<title>{esc(TITLE)}</title>',
      f'<meta name="description" content="{esc(DESC)}">',
      '<meta name="author" content="SvetimFM">',
      f'<meta name="keywords" content="{esc(KEYWORDS)}">',
      '<meta name="robots" content="index,follow,max-image-preview:large">',
      '<meta name="theme-color" content="#e9dcc0">',
      '<meta name="color-scheme" content="light">',
      f'<link rel="canonical" href="{URL}">',
      f'<link rel="icon" href="{rel}favicon.ico" sizes="32x32">',
      f'<link rel="icon" type="image/svg+xml" href="{rel}favicon.svg">',
      f'<link rel="icon" type="image/png" sizes="32x32" href="{rel}favicon-32.png">',
      f'<link rel="icon" type="image/png" sizes="16x16" href="{rel}favicon-16.png">',
      f'<link rel="apple-touch-icon" sizes="180x180" href="{rel}apple-touch-icon.png">',
      f'<link rel="manifest" href="{rel}site.webmanifest">',
      '<meta name="apple-mobile-web-app-title" content="The Rented Mind">',
      '<meta name="application-name" content="The Rented Mind">',
      '<meta property="og:type" content="article">',
      '<meta property="og:site_name" content="costCalcAI">',
      '<meta property="og:locale" content="en_US">',
      f'<meta property="og:url" content="{URL}">',
      f'<meta property="og:title" content="{esc(OG_TITLE)}">',
      f'<meta property="og:description" content="{esc(DESC)}">',
      f'<meta property="og:image" content="{URL}assets/og-banner.png">',
      '<meta property="og:image:type" content="image/png">',
      '<meta property="og:image:width" content="1200">',
      '<meta property="og:image:height" content="630">',
      f'<meta property="og:image:alt" content="{esc(IMG_ALT)}">',
      f'<meta property="article:published_time" content="{PUBLISHED}">',
      f'<meta property="article:modified_time" content="{MODIFIED}">',
      '<meta property="article:author" content="https://github.com/SvetimFM">',
      '<meta property="article:section" content="Data">',
      '<meta property="article:tag" content="local AI">',
      '<meta property="article:tag" content="total cost of ownership">',
      '<meta property="article:tag" content="Claude Code">',
      '<meta property="article:tag" content="data art">',
      '<meta name="twitter:card" content="summary_large_image">',
      f'<meta name="twitter:title" content="{esc(OG_TITLE)}">',
      f'<meta name="twitter:description" content="{esc(DESC)}">',
      f'<meta name="twitter:image" content="{URL}assets/og-banner.png">',
      f'<meta name="twitter:image:alt" content="{esc(IMG_ALT)}">',
      '<script type="application/ld+json">' + json.dumps(JSONLD, ensure_ascii=False).replace('</', '<\\/') + '</script>',
    ]
    return '\n'.join(tags)

STATIC_MAIN = '''<main id="__seo">
    <div class="p">$ <b>claude-meter</b> --month 2026-08 --source ~/.claude/transcripts</div>
    <h1>What one month of AI-assisted coding actually costs</h1>
    <p>Measuring the &ldquo;local models are free&rdquo; claim against 14.69 billion tokens of one person&rsquo;s own usage: 71,350 requests in the 30 days ending August 28, 2026, which would have cost $14,914 at API list rates but ran on a $200-a-month subscription. The same work is priced against six home machines &mdash; two used RTX 3090s, an RTX 5090 workstation, a Strix Halo and a DGX Spark at 128 GB, and Mac Studios at 256 and 512 GB &mdash; with hardware, capital, power and 13.7 hours a month of upkeep counted.</p>
    <dl>
      <dt>14.69B</dt><dd>tokens metered, 96% of them cache re-reads</dd>
      <dt>71,350</dt><dd>requests</dd>
      <dt>$200 / $14,914</dt><dd>paid on the plan / metered at list price &mdash; 74.6&times; leverage</dd>
      <dt>3 of 6</dt><dd>desk machines cannot finish the month&rsquo;s work inside a month; 4 of 6 once rejected work is redone</dd>
      <dt>27B-class</dt><dd>the only model class that keeps pace &mdash; and it is below the task</dd>
      <dt>13.7 h/mo</dt><dd>of setup and upkeep: the real bill, at whatever your hour is worth</dd>
    </dl>
    <h2>SECTIONS</h2>
    <ul>
      <li>01 The month &mdash; where 14.69 billion tokens actually went</li>
      <li>02 Machines &mdash; which desk setups could physically keep up, retries included</li>
      <li>03 Bill &mdash; cost per million tokens with your hours priced at a wage you choose</li>
      <li>04 Quality &mdash; benchmark scores for what the plan serves and what a box can hold</li>
      <li>05 Fair fight &mdash; the same month re-billed at hosted open-model rates</li>
      <li>06 Five years &mdash; cumulative cash, with breakeven months</li>
      <li>07 Prints &mdash; six plates after the data portraits of W. E. B. Du Bois, Paris Exposition, 1900</li>
    </ul>
    <h2>SOURCES</h2>
    <p><a href="https://github.com/SvetimFM/costCalcAI">Models, source data and every poster iteration on GitHub</a> &middot; <a href="report/report.html">the long-form companion report</a> &middot; <a href="posters/infographic7.html">the A3 nomograph poster</a></p>
    <p class="p">measured july 29 &ndash; august 28, 2026 &middot; open-model rates checked aug 31, 2026 &middot; &copy; <a href="https://studiolo.svetim.fm">studiolo.svetim.fm</a></p>
  </main>
'''

SEO_CSS = ('body { background: #e9dcc0; min-height: 100vh; color: #3a3022; font-family: ui-monospace, Menlo, Consolas, monospace; }\n'
  '    #__seo { max-width: 720px; margin: 0 auto; padding: 72px 28px 96px; line-height: 1.6; }\n'
  '    #__seo .p { color: #6b5b44; font-size: 13px; } #__seo .p b { color: #b07f1f; font-weight: 600; }\n'
  '    #__seo h1 { font-size: 30px; font-weight: 400; color: #2f261a; line-height: 1.3; margin: 18px 0 0; }\n'
  '    #__seo h2 { font-size: 13px; letter-spacing: 1.5px; color: #6b5b44; font-weight: 600; margin: 34px 0 6px; }\n'
  '    #__seo p, #__seo li { font-size: 15px; } #__seo ul { padding-left: 20px; } #__seo a { color: #b07f1f; }\n'
  '    #__seo dl { display: grid; grid-template-columns: max-content 1fr; gap: 6px 18px; font-size: 14px; }\n'
  '    #__seo dt { color: #b07f1f; font-weight: 600; } #__seo dd { margin: 0; }')
BUNDLER_BODY_CSS = 'body { background: #e9dcc0; display: flex; align-items: center; justify-content: center; min-height: 100vh; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }'

# (old, new) pairs applied to the unpacked template — the plates' reading of section 02
SECTION_EDITS = [
 ('Six realistic home setups, each running 24/7 with local caching credited. Note that speed here is not capability — the fast rows are fast because they run the smallest models, and smaller models get more of their work rejected at review. The hatched red bar prices that in: hours re-run at each model’s estimated acceptance rate.',
  'Six realistic home setups, each running 24/7 with local caching credited. Speed here is not capability. The fast rows are fast because they run the smallest models — and the measured month is agentic coding at frontier scope, work a 27B-class model cannot carry at all. Those two bars are drawn <span style="color:#2f261a;">hollow, for scale only</span>. Every model gets some of its work rejected at review, the smaller ones more; the hatched red bar prices that in: hours re-run at each model’s estimated acceptance rate.'),
 ('<div style="display:flex; flex-direction:column; gap:3px;"><div style="height:12px; background:#d7c69e;"><div style="height:12px; width:{{ p.pct }}%; background:{{ p.color }};"></div></div><div style="height:7px; background:#d7c69e;"><div style="height:7px; width:{{ p.pct2 }}%; background:repeating-linear-gradient(45deg, #c23a2e 0 4px, transparent 4px 8px);"></div></div></div>',
  '<div style="display:flex; flex-direction:column; gap:3px;"><div style="height:12px; background:#d7c69e;"><div style="height:12px; width:{{ p.pct }}%; background:{{ p.fill }}; box-shadow:inset 0 0 0 1.5px {{ p.color }};"></div></div><div style="height:7px; background:#d7c69e;"><div style="height:7px; width:{{ p.pct2 }}%; background:repeating-linear-gradient(45deg, #c23a2e 0 4px, transparent 4px 8px); opacity:{{ p.hatchOp }};"></div></div></div>'),
 ('<div style="font-size:13.5px; color:#3a3022; margin-top:30px;">Three of the six can’t finish the month’s work inside a month — and once rejected work is redone, <span style="color:#c23a2e;">four of six fail</span>. Only the two GPU rigs still finish, and up to half their time is redone work. The best local model lives in the slowest box.</div>',
  '<div style="display:flex; gap:22px; margin-top:24px; font-size:11.5px; color:#6b5b44; flex-wrap:wrap;">'
  '<div><span style="display:inline-block; width:22px; height:9px; background:#33604a; margin-right:7px; vertical-align:middle;"></span>as run — fits the month</div>'
  '<div><span style="display:inline-block; width:22px; height:9px; background:#c23a2e; margin-right:7px; vertical-align:middle;"></span>as run — spills past it</div>'
  '<div><span style="display:inline-block; width:22px; height:9px; background:#e9dcc0; box-shadow:inset 0 0 0 1.5px #2f261a; margin-right:7px; vertical-align:middle;"></span>† hollow — 27B-class, below the task; drawn for scale only</div>'
  '<div><span style="display:inline-block; width:22px; height:9px; background:repeating-linear-gradient(45deg, #c23a2e 0 3px, transparent 3px 6px); margin-right:7px; vertical-align:middle;"></span>hatched — hours once rejected work is redone</div>'
  '</div>'
  '<div style="font-size:13.5px; color:#3a3022; margin-top:26px; line-height:1.6;">Three of the six can’t finish the month’s work inside a month — and once rejected work is redone, <span style="color:#c23a2e;">four of six fail</span>. The two GPU rigs that still finish do it on a 27B-class model that is <span style="color:#2f261a;">below the task</span>: fast because it is small, and too small to carry this work at all. Nothing on the desk both carries the work and finishes the month. The best local model lives in the slowest box, and the only timely class is the furthest behind.</div>'),
 ("{ name:'RTX 5090', sub:'$8,500 \\u00b7 qwen3.8-27b \\u00b7 q48', pct:10, pct2:18, color:G, glow:GG, verdict:'6 days \\u2014 fits, with room', verdict2:'11 days with retries \\u2014 still fits', vcolor:'#3a3022' },",
  "{ name:'RTX 5090', sub:'$8,500 \\u00b7 qwen3.8-27b \\u00b7 q48 \\u00b7 \\u2020 below the task', pct:10, pct2:18, color:'#2f261a', fill:'#e9dcc0', hatchOp:0.5, glow:GG, verdict:'6 days \\u2014 fits, with room \\u2020', verdict2:'11 days with retries \\u2014 for scale only', vcolor:'#3a3022' },"),
 ("{ name:'2\\u00d7 RTX 3090', sub:'$2,900 \\u00b7 qwen3.8-27b \\u00b7 q48', pct:23.3, pct2:41.7, color:G, glow:GG, verdict:'14 days \\u2014 fits', verdict2:'25 days with retries \\u2014 barely', vcolor:'#3a3022' },",
  "{ name:'2\\u00d7 RTX 3090', sub:'$2,900 \\u00b7 qwen3.8-27b \\u00b7 q48 \\u00b7 \\u2020 below the task', pct:23.3, pct2:41.7, color:'#2f261a', fill:'#e9dcc0', hatchOp:0.5, glow:GG, verdict:'14 days \\u2014 fits \\u2020', verdict2:'25 days with retries \\u2014 barely, for scale only', vcolor:'#3a3022' },"),
 ("{ name:'MAC STUDIO 256', sub:'$10,800 \\u00b7 glm-5.3-flash \\u00b7 q53', pct:48.3, pct2:78.3, color:G, glow:GG,",
  "{ name:'MAC STUDIO 256', sub:'$10,800 \\u00b7 glm-5.3-flash \\u00b7 q53', pct:48.3, pct2:78.3, color:G, fill:G, hatchOp:1, glow:GG,"),
 ("{ name:'DGX SPARK 128', sub:'$4,700 \\u00b7 qwen3.8-flash-next \\u00b7 q52', pct:51.7, pct2:86.7, color:R, glow:RG,",
  "{ name:'DGX SPARK 128', sub:'$4,700 \\u00b7 qwen3.8-flash-next \\u00b7 q52', pct:51.7, pct2:86.7, color:R, fill:R, hatchOp:1, glow:RG,"),
 ("{ name:'STRIX HALO 128', sub:'$3,650 \\u00b7 qwen3.8-flash-next \\u00b7 q52', pct:88.3, pct2:100, color:R, glow:RG,",
  "{ name:'STRIX HALO 128', sub:'$3,650 \\u00b7 qwen3.8-flash-next \\u00b7 q52', pct:88.3, pct2:100, color:R, fill:R, hatchOp:1, glow:RG,"),
 ("{ name:'MAC STUDIO 512', sub:'$17,200 \\u00b7 deepseek v4 pro \\u00b7 q56, best here', pct:100, pct2:100, color:R, glow:RG,",
  "{ name:'MAC STUDIO 512', sub:'$17,200 \\u00b7 deepseek v4 pro \\u00b7 q56 \\u00b7 the best model here', pct:100, pct2:100, color:R, fill:R, hatchOp:1, glow:RG,"),
 ("{ name: '2\\u00d7 RTX 3090', sub: '$2,900 \\u00b7 qwen3.8-27b \\u00b7 q48', hw: 2.17, slope: 0.346 },",
  "{ name: '2\\u00d7 RTX 3090', sub: '$2,900 \\u00b7 qwen3.8-27b \\u00b7 q48 \\u00b7 \\u2020 below the task', hw: 2.17, slope: 0.346 },"),
 ("{ name: 'RTX 5090', sub: '$8,500 \\u00b7 qwen3.8-27b \\u00b7 q48', hw: 3.23, slope: 0.346 },",
  "{ name: 'RTX 5090', sub: '$8,500 \\u00b7 qwen3.8-27b \\u00b7 q48 \\u00b7 \\u2020 below the task', hw: 3.23, slope: 0.346 },"),
 ('<div style="width:100%; color:#8f7f5f;">⚠ rows marked with a warning can’t finish the month in 720 h',
  '<div style="width:100%; color:#8f7f5f;">† the 27B-class rows are priced for scale — a model that size cannot carry this work, see 02</div>'
  '<div style="width:100%; color:#8f7f5f;">⚠ rows marked with a warning can’t finish the month in 720 h'),
]

def strip_between(s, a, b, keep_markers=False):
    i = s.find(a)
    if i < 0: return s
    j = s.find(b, i)
    if j < 0: return s
    return s[:i] + s[j + len(b):].lstrip('\n') if not keep_markers else s

def bundle_blocks(src):
    out = {}
    for kind in ('manifest', 'template', 'ext_resources'):
        m = re.search(r'(<script type="__bundler/%s">\n)(.*?)(\n  </script>)' % kind, src, re.S)
        if not m: sys.exit(f'not a bundle: missing __bundler/{kind} block')
        out[kind] = m
    return out

def rebuild(src):
    blocks = bundle_blocks(src)
    tm = blocks['template']
    template = json.loads(tm.group(2))
    notes = []

    # ---- inner template head
    template = strip_between(template, INNER_START, INNER_END)
    template = template.replace('<!DOCTYPE html>\n<html><head>', '<!DOCTYPE html>\n<html lang="en"><head>', 1)
    vp = '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    if vp not in template: sys.exit('template head has no viewport meta to anchor on')
    template = template.replace(vp, vp + INNER_START + '\n' + meta_block('assets/') + '\n' + INNER_END + '\n', 1)

    # ---- section edits (best effort)
    for old, new in SECTION_EDITS:
        if new in template:
            pass  # already applied (checked first: some new texts contain their old anchor)
        elif old in template:
            template = template.replace(old, new, 1)
        else:
            notes.append('anchor not found: ' + old[:80].replace('\n', ' ') + '…')
    if '<!--' in template: sys.exit('template contains <!-- which cannot be embedded safely in the bundle script')
    tjson = json.dumps(template, ensure_ascii=True).replace('</', '<\\/')
    assert json.loads(tjson) == template
    new_src = src[:tm.start(2)] + tjson + src[tm.end(2):]

    # ---- outer shell head
    new_src = strip_between(new_src, OUTER_START, OUTER_END)
    new_src = new_src.replace('<!DOCTYPE html>\n<html>\n<head>', '<!DOCTYPE html>\n<html lang="en">\n<head>', 1)
    block = OUTER_START + '\n' + meta_block('assets/') + '\n' + OUTER_END + '\n'
    bare = '  <title>Bundled Page</title>\n'
    viewport = '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
    charset = '  <meta charset="utf-8">\n'
    if bare in new_src:
        new_src = new_src.replace(bare, viewport + block, 1)
    elif viewport in new_src[:4000]:
        new_src = new_src.replace(viewport, viewport + block, 1)
    elif charset in new_src:
        new_src = new_src.replace(charset, charset + block, 1)
    else:
        sys.exit('outer head has neither the bundler title nor a charset meta to anchor on')

    # ---- outer shell body: css, noscript copy, static summary
    if BUNDLER_BODY_CSS in new_src:
        new_src = new_src.replace(BUNDLER_BODY_CSS, SEO_CSS, 1)
    elif '#__seo {' not in new_src:
        notes.append('outer body css anchor not found; static summary is unstyled')
    new_src = new_src.replace('This page requires JavaScript to display.',
        'The interactive charts need JavaScript. The summary on this page and the repository carry the same numbers.', 1)
    new_src = re.sub(r'[ \t]*<main id="__seo">.*?</main>\n', '', new_src, count=1, flags=re.S)
    anchor = '  <div id="__bundler_loading">Unpacking...</div>\n'
    if anchor in new_src:
        new_src = new_src.replace(anchor, anchor + '  ' + STATIC_MAIN, 1)
    else:
        notes.append('loader div not found; static summary not inserted')
    return new_src, notes

# ---------------------------------------------------------------- static files
MARK = '''<path d="M 36 21 C 34 15.5, 18 15.5, 18 24 C 18 33, 36 30, 36 40 C 36 48.5, 20 48.5, 17.5 42" fill="none" stroke="#c23a2e" stroke-width="6" stroke-linecap="round"/>
  <path d="M 27 11.5 V 52.5" stroke="#c23a2e" stroke-width="5" stroke-linecap="round"/>
  <rect x="41" y="44" width="14" height="8" fill="#b07f1f"/>'''
def icon_svg(rounded=True, scale=1.0):
    rx = ' rx="9"' if rounded else ''
    frx = ' rx="5"' if rounded else ''
    inner = f'<g transform="translate(32 32) scale({scale}) translate(-32 -32)">\n  {MARK}\n  </g>' if scale != 1 else MARK
    frame = '' if scale != 1 else f'<rect x="4" y="4" width="56" height="56"{frx} fill="none" stroke="#2f261a" stroke-width="3"/>\n  '
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64"{rx} fill="#e9dcc0"/>
  {frame}{inner}
</svg>
'''

def write_static():
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / 'favicon.svg').write_text(icon_svg(rounded=True))
    (ASSETS / 'site.webmanifest').write_text(json.dumps({
      "name": "The Rented Mind — what one month of AI-assisted coding actually costs",
      "short_name": "Rented Mind",
      "description": DESC,
      "id": "/costCalcAI/", "start_url": "/costCalcAI/", "scope": "/costCalcAI/",
      "display": "browser", "background_color": "#e9dcc0", "theme_color": "#e9dcc0", "lang": "en",
      "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "icon-512-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}
      ]}, indent=2, ensure_ascii=False) + '\n')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {URL}sitemap.xml\n')
    (ROOT / 'sitemap.xml').write_text('''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url>
    <loc>%s</loc>
    <lastmod>%s</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
    <image:image><image:loc>%sassets/og-banner.png</image:loc><image:title>%s</image:title></image:image>
  </url>
  <url>
    <loc>%sreport/report.html</loc>
    <lastmod>2026-08-29</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.6</priority>
  </url>
  <url>
    <loc>%sposters/infographic7.html</loc>
    <lastmod>2026-08-29</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.5</priority>
  </url>
</urlset>
''' % (URL, MODIFIED, URL, esc(OG_TITLE), URL, URL))
    (ROOT / '.nojekyll').write_text('')

# ---------------------------------------------------------------- render (icons + banner)
def spiral(cx, cy, R0, Rend, budget, a0):
    gap = math.pi * (R0*R0 - Rend*Rend) / budget
    b = gap / (2*math.pi)
    pts = []; a = a0; r = R0; ln = 0; da = 0.035
    while r > Rend*0.7 and ln < budget:
        pts.append((cx + r*math.cos(a), cy + r*math.sin(a)))
        r2 = r - b*da
        ln += math.sqrt((r*da)**2 + (r-r2)**2)
        a += da; r = r2
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)

def banner_html(font_css):
    coil = spiral(300, 300, 200, 72, 7300, -1.2)
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><style>
{font_css}
html,body{{margin:0;width:1200px;height:630px;overflow:hidden;background:#e9dcc0;}}
body{{font-family:'Spline Sans Mono',monospace;color:#3a3022;position:relative;font-variant-numeric:tabular-nums;}}
.coil{{position:absolute;left:690px;top:-5px;}}
.scan{{position:absolute;inset:0;pointer-events:none;background:repeating-linear-gradient(0deg, rgba(60,40,10,0.06) 0 1px, transparent 1px 3px);}}
.vig{{position:absolute;inset:0;background:radial-gradient(ellipse 120% 90% at 50% 40%, transparent 60%, rgba(85,55,15,0.16) 100%);}}
.wrap{{position:absolute;left:72px;top:64px;width:720px;}}
.prompt{{font-size:16px;color:#6b5b44;}} .prompt b{{color:#b07f1f;font-weight:600;}}
.sub2{{font-size:13.5px;color:#8f7f5f;margin-top:6px;}}
h1{{font-size:50px;font-weight:400;line-height:1.22;color:#2f261a;margin:34px 0 0;letter-spacing:-0.5px;}}
h1 .cur{{display:inline-block;width:16px;height:38px;background:#b07f1f;margin-left:12px;vertical-align:-4px;}}
.deck{{font-size:19px;color:#6b5f49;line-height:1.45;margin-top:16px;max-width:600px;}}
.stats{{display:flex;margin-top:38px;border:1px solid #c9b78d;background:rgba(233,220,192,0.78);width:max-content;}}
.stats>div{{padding:15px 24px;border-left:1px solid #c9b78d;}} .stats>div:first-child{{border-left:0;}}
.v{{font-size:25px;font-weight:600;color:#b07f1f;}} .k{{font-size:10.5px;color:#6b5b44;letter-spacing:1.5px;margin-top:4px;}}
.foot{{position:absolute;left:72px;bottom:36px;font-size:12.5px;color:#8f7f5f;letter-spacing:0.4px;}} .foot b{{color:#b07f1f;font-weight:600;}}
</style></head><body>
<svg class="coil" width="600" height="600" viewBox="0 0 600 600">
  <defs><filter id="p" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.11" numOctaves="3" seed="8" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="4.5"/></filter></defs>
  <path d="{coil}" fill="none" stroke="#c23a2e" stroke-width="9" stroke-linecap="round" filter="url(#p)"/>
  <text x="300" y="298" text-anchor="middle" font-family="Archivo Narrow" font-size="14" letter-spacing="2" fill="#2f261a">96 OF EVERY 100</text>
  <text x="300" y="316" text-anchor="middle" font-family="Archivo Narrow" font-size="11.5" letter-spacing="1.6" fill="#4a3c28">WORDS RE-READ</text>
</svg>
<div class="scan"></div><div class="vig"></div>
<div class="wrap">
  <div class="prompt">$ <b>claude-meter</b> --month 2026-08 --source ~/.claude/transcripts</div>
  <div class="sub2">parsing 71,350 requests ... done in 4.2s</div>
  <h1>What one month of<br>AI-assisted coding<br>actually costs<span class="cur"></span></h1>
  <div class="deck">14.69 billion tokens of one person&rsquo;s measured usage, priced both ways &mdash; rented by the month, or bought and run at home.</div>
  <div class="stats">
    <div><div class="v">14.69B</div><div class="k">TOKENS METERED</div></div>
    <div><div class="v">71,350</div><div class="k">REQUESTS</div></div>
    <div><div class="v" style="color:#2f261a">$200 <span style="color:#8f7f5f">/</span> <span style="color:#c23a2e">$14,914</span></div><div class="k">PAID / METERED VALUE</div></div>
    <div><div class="v" style="color:#2f261a">&times;74.6</div><div class="k">SUBSCRIPTION LEVERAGE</div></div>
  </div>
</div>
<div class="foot"><b>svetimfm.github.io/costCalcAI</b> &middot; the rented mind &middot; six plates after w. e. b. du bois, 1900</div>
</body></html>
'''

def chrome_shot(url, out, w, h, budget=None):
    args = [CHROME, '--headless', '--disable-gpu', '--hide-scrollbars', f'--screenshot={out}', f'--window-size={w},{h}']
    if budget: args.append(f'--virtual-time-budget={budget}')
    args.append(url)
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def write_ico(pngs, path):
    hdr = struct.pack('<HHH', 0, 1, len(pngs)); off = 6 + 16*len(pngs); ent = b''; dat = b''
    for s, b in pngs:
        ent += struct.pack('<BBBBHHII', s, s, 0, 0, 1, 32, len(b), off); off += len(b); dat += b
    path.write_bytes(hdr + ent + dat)

def render(src):
    if not os.path.exists(CHROME) or not shutil.which('sips'):
        sys.exit('--render needs Google Chrome and sips (macOS)')
    work = ROOT / 'generators' / '.site-build'
    work.mkdir(exist_ok=True)
    # fonts: pull every woff2 out of the bundle manifest so the banner uses the page's own faces
    blocks = bundle_blocks(src)
    manifest = json.loads(blocks['manifest'].group(2))
    template = json.loads(blocks['template'].group(2))
    for uuid, e in manifest.items():
        if e['mime'] == 'font/woff2':
            raw = base64.b64decode(e['data'])
            if e.get('compressed'): raw = gzip.decompress(raw)
            (work / f'{uuid}.woff2').write_bytes(raw)
    faces = re.findall(r'@font-face\s*\{[^}]*\}', template)
    font_css = re.sub(r'url\("([0-9a-f-]{36})"\)', r'url("./\1.woff2")', '\n'.join(faces))
    (work / 'og-banner.html').write_text(banner_html(font_css))
    (work / 'icon-square.svg').write_text(icon_svg(rounded=False))
    (work / 'icon-maskable.svg').write_text(icon_svg(rounded=False, scale=0.66))
    chrome_shot(work.joinpath('icon-square.svg').as_uri(), ASSETS / 'icon-512.png', 512, 512)
    chrome_shot(work.joinpath('icon-maskable.svg').as_uri(), ASSETS / 'icon-512-maskable.png', 512, 512)
    chrome_shot(work.joinpath('og-banner.html').as_uri(), ASSETS / 'og-banner.png', 1200, 630, 4000)
    for size, name in ((192, 'icon-192.png'), (180, 'apple-touch-icon.png'), (32, 'favicon-32.png'), (16, 'favicon-16.png')):
        subprocess.run(['sips', '-z', str(size), str(size), str(ASSETS / 'icon-512.png'), '--out', str(ASSETS / name)],
                       check=True, stdout=subprocess.DEVNULL)
    write_ico([(16, (ASSETS / 'favicon-16.png').read_bytes()), (32, (ASSETS / 'favicon-32.png').read_bytes())], ASSETS / 'favicon.ico')
    shutil.rmtree(work)
    print('rendered assets/og-banner.png and the icon set')

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--input', default=str(ROOT / 'index.html'), help='bundle to rebuild (default: index.html)')
    ap.add_argument('--output', default=str(ROOT / 'index.html'), help='where to write (default: index.html)')
    ap.add_argument('--render', action='store_true', help='also re-render the banner and icons (Chrome + sips)')
    a = ap.parse_args()
    src = pathlib.Path(a.input).read_text(encoding='utf-8')
    new_src, notes = rebuild(src)
    pathlib.Path(a.output).write_text(new_src, encoding='utf-8')
    write_static()
    print(f'wrote {a.output} ({len(src):,} -> {len(new_src):,} bytes), assets/favicon.svg, assets/site.webmanifest, robots.txt, sitemap.xml, .nojekyll')
    for n in notes: print('note:', n)
    if a.render: render(new_src)

if __name__ == '__main__':
    main()
