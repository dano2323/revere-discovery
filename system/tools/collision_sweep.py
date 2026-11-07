#!/usr/bin/env python3
"""Gate D sweep for a Revere Discovery deck (system/build-playbook.md, Gate D step 2).

Renders the deck headless at 1280x720 and checks each slide. Hard gates fail the build; advisory
checks are listed for a person to confirm.

  Hard    fit · spill · foot · stack · scaling · navigation · orphans · title lines
          position tags · one value per figure · blur placeholders · Draft mark · inline styles
  Advisory  Index arithmetic · words ("every", "ChatGPT")

Reads the slide surface of revere-design-system (.rv-stage, .rv-slide, .rv-slide__foot) and its
sweep hooks (data-position, data-subject/data-comps, data-metric/data-value, data-rank/data-place).
Geometry is generic: it checks the content each slide actually draws, so no selector list to keep.

Usage:
  collision_sweep.py DECK.html [--out DIR] [--fonts DIR] [--publish]
    --out     report and screenshots (default: <deck>-sweep/ beside the deck)
    --fonts   folder of Outfit / JetBrains Mono woff2 files, served in place of Google Fonts
              (for a sandbox without web access; names like outfit-latin-700-normal.woff2)
    --publish the deck is approved to publish: skip the Draft-mark check
Exit: 0 all hard gates pass · 1 a hard gate fails · 2 cannot measure (fonts did not load)
"""
import argparse, json, pathlib, re, sys
from playwright.sync_api import sync_playwright

W, H, TOL = 1280, 720, 4
VIEWPORTS = [(1280, 720), (1920, 1080), (1440, 900), (900, 600), (768, 1024), (390, 844)]
ORPHAN_SEL = '.rv-title, .rv-lede2, .rv-cover__name, .rv-cover__title, .rv-cover__signal, .rv-cover__read, .rv-close__head, .rv-close__cta'
WORDS = [(r'\bevery\b', '"every": prefer "each," "all" or the count'), (r'\bChatGPT\b', '"ChatGPT": write "GPT"')]

# --- in-page measurement of the active slide (canvas px) ---------------------------------------
MEASURE = r"""({tol, orphanSel}) => {
  const stage = document.querySelector('.rv-stage.is-active');
  const slide = stage.querySelector('.rv-slide') || stage;
  const sb = slide.getBoundingClientRect(), k = sb.width / 1280;
  const box = (r) => ({ l: (r.left - sb.left) / k, t: (r.top - sb.top) / k, r: (r.right - sb.left) / k, b: (r.bottom - sb.top) / k });
  const name = (e) => {
    const c = (e.getAttribute('class') || '').split(/\s+/).filter(Boolean).slice(0, 2).join('.');
    const txt = (e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40);
    return (c ? '.' + c : e.tagName.toLowerCase()) + (txt ? ` "${txt}"` : '');
  };
  const inSvg = (e) => e.ownerSVGElement != null;
  const visible = (e) => { const s = getComputedStyle(e); return s.display !== 'none' && s.visibility !== 'hidden' && +s.opacity > 0; };
  const hasText = (e) => [...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
  const painted = (e) => { const s = getComputedStyle(e);
    return (s.backgroundColor !== 'rgba(0, 0, 0, 0)' && s.backgroundColor !== 'transparent') || s.backgroundImage !== 'none'; };
  const foot = slide.querySelector('.rv-slide__foot');

  // Content = what the slide draws: text, images, svg figures, painted boxes. Full-bleed backgrounds
  // (cover photo, scrim) and table cells/rows (painted grid, checked as text) are not blocks.
  const all = [...slide.querySelectorAll('*')].filter((e) => !inSvg(e) && visible(e));
  const content = all.filter((e) => {
    const r = e.getBoundingClientRect(); if (r.width < 1 || r.height < 1) return false;
    if (r.width * r.height > 0.85 * sb.width * sb.height) return false;
    if (hasText(e) || e.tagName === 'IMG' || e.tagName === 'svg' || e.tagName === 'HR') return true;
    return painted(e) && !/^(TD|TH|TR|TBODY|THEAD|TFOOT|TABLE)$/.test(e.tagName) && !e.closest('table');
  }).map((e) => ({ e, b: box(e.getBoundingClientRect()), text: hasText(e) }));

  const out = { fit: [], spill: [], foot: [], stack: [], orphans: [], titleLines: [], inline: [] };

  // fit: nothing past the canvas
  if (slide.scrollWidth > 1281 || slide.scrollHeight > 721) out.fit.push({ el: 'slide', w: slide.scrollWidth, h: slide.scrollHeight });
  for (const c of content) if (c.b.l < -1 || c.b.t < -1 || c.b.r > 1281 || c.b.b > 721)
    out.fit.push({ el: name(c.e), box: [c.b.l, c.b.t, c.b.r, c.b.b].map(Math.round) });

  // spill: a clipping box hides part of its content (text cut off, a table scrolling). Content that
  // overhangs an unclipped box is caught by foot and stack, where it lands on something.
  for (const e of all) {
    const st = getComputedStyle(e);
    if (e === slide || st.display.startsWith('inline') || (st.overflowX === 'visible' && st.overflowY === 'visible')) continue;
    const dh = e.scrollHeight - e.clientHeight, dw = e.scrollWidth - e.clientWidth;
    if (e.clientHeight > 0 && (dh > 2 || dw > 2) && (e.textContent || '').trim())
      out.spill.push({ el: name(e), hidden: [dw, dh] });
  }

  // foot: no content crosses the slide foot
  if (foot) {
    const f = box(foot.getBoundingClientRect());
    for (const c of content) {
      if (foot.contains(c.e) || c.e.contains(foot)) continue;
      const ox = Math.min(c.b.r, f.r) - Math.max(c.b.l, f.l);
      if (ox > tol && c.b.b > f.t + tol && c.b.t < f.b) out.foot.push({ el: name(c.e), bottom: Math.round(c.b.b), footTop: Math.round(f.t) });
    }
  }

  // stack: no two blocks overlap, where at least one carries text (bars may layer; words may not)
  for (let i = 0; i < content.length; i++) for (let j = i + 1; j < content.length; j++) {
    const A = content[i], B = content[j];
    if (!A.text && !B.text) continue;
    if (A.e.contains(B.e) || B.e.contains(A.e)) continue;
    const ox = Math.min(A.b.r, B.b.r) - Math.max(A.b.l, B.b.l), oy = Math.min(A.b.b, B.b.b) - Math.max(A.b.t, B.b.t);
    if (ox > tol && oy > tol) out.stack.push({ a: name(A.e), b: name(B.e), overlap: [Math.round(ox), Math.round(oy)] });
  }

  // orphans (last word alone on its line) and title line count, from the rendered words
  const words = (el) => {
    const res = [], walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    for (let n; (n = walker.nextNode());) for (const m of n.textContent.matchAll(/\S+/g)) {
      const r = document.createRange(); r.setStart(n, m.index); r.setEnd(n, m.index + m[0].length);
      const rr = r.getClientRects(); if (rr.length) res.push({ w: m[0], top: rr[0].top, h: rr[0].height });
    }
    return res;
  };
  for (const el of slide.querySelectorAll(orphanSel)) {
    const ws = words(el); if (ws.length < 2) continue;
    const lines = []; for (const w of ws) if (!lines.length || w.top > lines[lines.length - 1] + w.h / 2) lines.push(w.top);
    const last = ws[ws.length - 1], prev = ws[ws.length - 2];
    if (last.top > prev.top + last.h / 2) out.orphans.push({ el: name(el), word: last.w });
    if (el.matches('.rv-title') && lines.length > 2) out.titleLines.push({ el: name(el), lines: lines.length });
  }

  // inline styles may carry data (a width, a position, an image), never a color, font or border
  for (const e of [stage, ...stage.querySelectorAll('[style]')]) {
    const st = e.getAttribute('style') || '';
    const bad = st.split(';').map((d) => d.split(':')[0].trim().toLowerCase())
      .filter((p) => /^(color|font|border|outline|fill|stroke|text-decoration)/.test(p) || (p.startsWith('background') && p !== 'background-image'));
    if (bad.length) out.inline.push({ el: name(e), props: bad });
  }
  return out;
}"""

# --- deck-level reads -------------------------------------------------------------------------
FACTS = r"""() => {
  const stages = [...document.querySelectorAll('.rv-stage')];
  const res = { metrics: [], ranks: [], positions: [], blur: [], draft: !!document.querySelector('.rv-draft'), text: [], arithmetic: [] };
  stages.forEach((s, i) => {
    const n = i + 1;
    for (const e of s.querySelectorAll('[data-metric]')) res.metrics.push({ slide: n, key: e.dataset.metric, value: +e.dataset.value });
    for (const e of s.querySelectorAll('[data-rank]')) res.ranks.push({ slide: n, rank: +e.dataset.rank, of: +e.dataset.of });
    for (const e of s.querySelectorAll('[data-place]')) res.ranks.push({ slide: n, rank: parseInt(e.dataset.place, 10), of: +e.dataset.of });
    for (const tr of s.querySelectorAll('tr[data-comps]')) {
      const tag = tr.querySelector('[data-position]');
      const cell = tr.querySelector('td.rv-subj');
      res.positions.push({ slide: n, row: tr.cells[0].textContent.trim(), subject: +tr.dataset.subject,
        comps: JSON.parse(tr.dataset.comps), tag: tag ? tag.dataset.position : null, shown: cell ? +cell.textContent.trim() : null });
    }
    for (const e of s.querySelectorAll('.rv-blur')) res.blur.push({ slide: n, text: e.textContent.trim() });
    const mark = s.querySelector('.rv-mark[data-metric="index"]'), parts = [...s.querySelectorAll('[data-weight]')];
    if (mark && parts.length) res.arithmetic.push({ slide: n, index: +mark.dataset.value,
      sum: parts.reduce((a, p) => a + (+p.dataset.weight) * (+p.dataset.value), 0), weights: parts.reduce((a, p) => a + (+p.dataset.weight), 0) });
    res.text.push({ slide: n, text: s.innerText });
  });
  return res;
}"""

def expect_position(subject, comps):
    if comps and all(subject > c for c in comps): return 'Leading'
    if comps and all(subject < c for c in comps): return 'Lagging'
    return 'Inline'

def font_routes(page, fonts_dir):
    files = {p.name: p for p in pathlib.Path(fonts_dir).glob('*.woff2')}
    css = []
    for fname in files:
        m = re.match(r'(outfit|jetbrains-mono)-latin-(\d+)-normal\.woff2$', fname)
        if m:
            fam = 'Outfit' if m[1] == 'outfit' else 'JetBrains Mono'
            css.append(f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{m[2]};font-display:block;src:url(https://fonts.local/{fname}) format('woff2');}}")
    page.route('https://fonts.googleapis.com/**', lambda r: r.fulfill(status=200, content_type='text/css', body='\n'.join(css)))
    page.route('https://fonts.local/**', lambda r: r.fulfill(status=200, content_type='font/woff2', headers={'access-control-allow-origin': '*'},
                                                         body=files[r.request.url.rsplit('/', 1)[1]].read_bytes()))

def open_deck(browser, url, fonts, vw=1280, vh=720, scale=1):
    page = browser.new_page(viewport={'width': vw, 'height': vh}, device_scale_factor=scale)
    if fonts: font_routes(page, fonts)
    # Nothing else leaves the machine; a remote image that cannot load is reported, not waited on.
    page.route(re.compile(r'^https?://(?!fonts\.(googleapis\.com|local)/)'), lambda r: r.abort())
    page.goto(url, wait_until='load')
    page.wait_for_selector('.rv-stage')
    page.evaluate('document.fonts.ready')
    page.wait_for_timeout(250)
    return page

def go(page, i):
    page.click(f'[data-slide="{i}"]')
    page.wait_for_timeout(40)

def run(deck, out, fonts, publish):
    url = deck.resolve().as_uri()
    hard, adv, notes = {}, {}, []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = open_deck(browser, url, fonts)
        msgs = []
        page.on('console', lambda m: m.type == 'error' and msgs.append(m.text))

        fonts_ok = page.evaluate("""async () => { const f = ['400 16px Outfit', '700 16px Outfit', '400 16px "JetBrains Mono"'];
            await Promise.all(f.map((x) => document.fonts.load(x).catch(() => null)));
            return f.every((x) => [...document.fonts].some((ff) => ff.status === 'loaded' && x.includes(ff.family.replace(/"/g, '')))
                                   && document.fonts.check(x)); }""")
        if not fonts_ok:
            browser.close()
            return None, ['Fonts did not load (Outfit / JetBrains Mono): geometry would be measured in a fallback font. '
                          'Run with --fonts, or where Google Fonts is reachable.']
        n = page.eval_on_selector_all('.rv-stage', 'e => e.length')

        # per slide
        per = {k: [] for k in ('fit', 'spill', 'foot', 'stack', 'orphans', 'titleLines', 'inline')}
        for i in range(n):
            go(page, i)
            m = page.evaluate(MEASURE, {'tol': TOL, 'orphanSel': ORPHAN_SEL})
            for k in per:
                if m[k]: per[k].append({'slide': i + 1, 'items': m[k]})
        for k, label in (('fit', 'fit'), ('spill', 'spill'), ('foot', 'foot'), ('stack', 'stack'),
                         ('orphans', 'orphans'), ('titleLines', 'title_two_lines'), ('inline', 'inline_styles')):
            hard[label] = per[k]

        # navigation: one slide at a time, counter, arrows, keys
        page.keyboard.press('Home'); page.wait_for_timeout(40)
        nav = page.evaluate("""() => ({ items: document.querySelectorAll('.rv-nav__item').length,
            active: document.querySelectorAll('.rv-stage.is-active').length,
            counter: document.querySelector('.rv-counter')?.textContent.trim(),
            prevOff: document.querySelector('.rv-arrow--prev')?.disabled })""")
        page.keyboard.press('ArrowRight'); page.wait_for_timeout(40)
        nav['afterNext'] = page.evaluate("() => document.querySelector('.rv-counter')?.textContent.trim()")
        page.keyboard.press('End'); page.wait_for_timeout(40)
        nav['nextOffAtEnd'] = page.evaluate("() => document.querySelector('.rv-arrow--next')?.disabled")
        nav_fail = []
        if nav['items'] != n: nav_fail.append(f"{nav['items']} nav items for {n} slides")
        if nav['active'] != 1: nav_fail.append(f"{nav['active']} slides showing at once")
        if nav['counter'] != f'1 / {n}': nav_fail.append(f"counter reads {nav['counter']!r} on slide 1")
        if nav['afterNext'] != f'2 / {n}': nav_fail.append(f"ArrowRight: counter reads {nav['afterNext']!r}")
        if not nav['prevOff']: nav_fail.append('previous arrow live on slide 1')
        if not nav['nextOffAtEnd']: nav_fail.append('next arrow live on the last slide')
        hard['navigation'] = nav_fail

        # facts: tags, figures, blur, Draft, words
        f = page.evaluate(FACTS)
        pos_fail = []
        for r in f['positions']:
            want = expect_position(r['subject'], r['comps'])
            if r['tag'] != want: pos_fail.append({**r, 'expected': want})
            elif r['shown'] != r['subject']: pos_fail.append({**r, 'issue': 'shown subject value differs from the value tagged'})
        hard['position_tags'] = pos_fail

        by_key = {}
        for m in f['metrics']: by_key.setdefault(m['key'], []).append((m['slide'], m['value']))
        hard['one_value_per_figure'] = [{'figure': k, 'reads': v} for k, v in by_key.items() if len({x for _, x in v}) > 1]
        ranks = {(r['rank'], r['of']) for r in f['ranks']}
        if len(ranks) > 1: hard['one_value_per_figure'].append({'figure': 'placement', 'reads': f['ranks']})
        if not by_key.get('index'): notes.append('No Index figure carries a sweep hook; the one-Index check did not run.')
        notes.append('The cover states the placement in words; check it against slides 2 and 4 by eye.')

        hard['blur_placeholders'] = [b for b in f['blur'] if not re.fullmatch(r'0+', b['text'])]
        hard['draft_mark'] = [] if (publish or f['draft']) else ['No Draft mark on the cover.']

        adv['index_arithmetic'] = [a for a in f['arithmetic'] if abs(a['weights'] - 1) > 0.01 or abs(a['sum'] - a['index']) > 1]
        word_hits = []
        for t in f['text']:
            for pat, why in WORDS:
                c = len(re.findall(pat, t['text'], re.I))
                if c: word_hits.append({'slide': t['slide'], 'count': c, 'rule': why})
        adv['words'] = word_hits

        # scaling: the composition holds at each window size, 16:9, no reflow
        drift = []
        ref = None
        for vw, vh in VIEWPORTS:
            page.set_viewport_size({'width': vw, 'height': vh}); page.wait_for_timeout(350)
            snap = []
            for i in range(n):
                go(page, i)
                snap.append(page.evaluate("""() => {
                  const s = document.querySelector('.rv-stage.is-active'), b = s.getBoundingClientRect();
                  const els = [...s.querySelectorAll('.rv-title, .rv-lede2, .rv-reading, table, svg, .rv-slide__foot, .rv-cover__name')].slice(0, 30);
                  return { ar: b.width / b.height, inView: b.left >= -1 && b.top >= -1 && b.right <= innerWidth + 1 && b.bottom <= innerHeight + 1,
                           pts: els.map(e => { const r = e.getBoundingClientRect(); return [(r.left - b.left) / b.width, (r.top - b.top) / b.height]; }) };
                }"""))
            if ref is None: ref = snap
            for i, (a, b) in enumerate(zip(ref, snap)):
                d = max([abs(x[0] - y[0]) + abs(x[1] - y[1]) for x, y in zip(a['pts'], b['pts'])] + [0])
                if d > 0.004 or len(a['pts']) != len(b['pts']) or abs(b['ar'] - 16 / 9) > 0.02 or not b['inView']:
                    drift.append({'viewport': f'{vw}x{vh}', 'slide': i + 1, 'drift': round(d, 4), 'ratio': round(b['ar'], 3), 'inView': b['inView']})
        hard['scaling'] = drift

        imgs = page.evaluate("() => [...document.querySelectorAll('.rv-cover__img')].map(e => getComputedStyle(e).backgroundImage)")
        if any('http' in i for i in imgs): notes.append('Cover photo is remote and was not loaded here; look at it in the browser.')
        if msgs: notes.append(f'Console errors: {msgs[:3]}')

        # screenshots at slide scale, for the look at each slide (Gate D step 3)
        page.close()
        shot = open_deck(browser, url, fonts, 1280 + 300, 760, 1)
        shots = out / 'shots'; shots.mkdir(parents=True, exist_ok=True)
        for i in range(n):
            go(shot, i)
            shot.locator('.rv-stage.is-active').screenshot(path=str(shots / f'slide_{i + 1:02d}.png'))
        browser.close()
    return {'deck': deck.name, 'slides': n, 'hard': hard, 'advisory': adv}, notes

def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('deck', type=pathlib.Path)
    ap.add_argument('--out', type=pathlib.Path)
    ap.add_argument('--fonts', type=pathlib.Path)
    ap.add_argument('--publish', action='store_true')
    a = ap.parse_args()
    out = a.out or a.deck.with_name(a.deck.stem + '-sweep')
    res, notes = run(a.deck, out, a.fonts, a.publish)
    if res is None:
        print('CANNOT MEASURE:', *notes, sep='\n  '); sys.exit(2)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'sweep.json').write_text(json.dumps({**res, 'notes': notes}, indent=1))
    print(f"Gate D sweep · {res['deck']} · {res['slides']} slides")
    for group, label in (('hard', 'Hard gates'), ('advisory', 'Advisory (confirm by eye)')):
        print(f'\n{label}')
        for k, v in res[group].items():
            print(f"  [{'FAIL' if v and group == 'hard' else 'FLAG' if v else 'pass'}] {k}")
            for item in v[:6]: print('        ', json.dumps(item, ensure_ascii=False)[:300])
            if len(v) > 6: print(f'         … {len(v) - 6} more in sweep.json')
    if notes: print('\nNotes', *notes, sep='\n  ')
    failed = [k for k, v in res['hard'].items() if v]
    print('\n' + (f'HARD-GATE FAILURES: {", ".join(failed)}' if failed else 'All hard gates pass.'), f'\nReport and screenshots: {out}')
    sys.exit(1 if failed else 0)

if __name__ == '__main__':
    main()
