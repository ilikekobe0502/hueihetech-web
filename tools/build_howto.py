#!/usr/bin/env python3
"""熟客簿功能教學頁產生器：tools/howto/zh-TW/*.py 每檔一個 HOWTO dict，輸出 shukebu/how-to/<slug>/ 與教學列表 shukebu/how-to/。
版型、頁首頁尾沿用 build_guides.py；結構化資料用 HowTo＋FAQPage＋BreadcrumbList。
用法：python3 tools/build_howto.py

HOWTO 欄位：order、slug、title、description、published／updated、
scenario（情境故事 HTML，第一段直接講「這功能幫你解決什麼」）、image（主截圖，站內路徑，如 'assets/phone-voice.png'）、
minutes（大約幾分鐘學會）、steps（[(步驟標題, 說明 HTML)]）、tips（HTML，可空）、faq（[(問, 答)]）"""
import glob, importlib.util, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_guides as G

LANG = 'zh-TW'
BASE = 'shukebu/how-to/'
CSS = """
.howto .scenario{background:var(--bg-soft);border-left:4px solid var(--brand);border-radius:10px;padding:16px 18px;margin-top:22px}
.howto .scenario p{margin-top:8px}
.howto .hero-shot{width:min(280px,72vw);border-radius:22px;box-shadow:0 14px 36px rgba(15,23,42,.18);margin:28px auto 0}
.howto ol.steps{list-style:none;padding:0;counter-reset:s}
.howto ol.steps>li{counter-increment:s;position:relative;padding-left:46px;margin-top:22px}
.howto ol.steps>li::before{content:counter(s);position:absolute;left:0;top:2px;width:32px;height:32px;border-radius:50%;background:var(--brand);color:#fff;font-weight:700;display:flex;align-items:center;justify-content:center}
.howto ol.steps h3{margin-top:0;font-size:17px}
.howto .ui{background:var(--teal-soft);color:var(--brand-dark);border-radius:6px;padding:1px 6px;font-weight:600;white-space:nowrap}
"""


def load():
    out = []
    for f in sorted(glob.glob(os.path.join(G.ROOT, 'tools', 'howto', LANG, '*.py'))):
        spec = importlib.util.spec_from_file_location('howto_' + os.path.basename(f)[:-3], f)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        out.append(m.HOWTO)
    return sorted(out, key=lambda h: h['order'])


def build():
    L = G.LANGS[LANG]
    items = load()
    paths = []
    for h in items:
        path = f"{BASE}{h['slug']}/"
        url = f'{G.SITE}/{path}'
        steps = ''.join(f'<li><h3>{G.esc(n)}</h3><p>{d}</p></li>' for n, d in h['steps'])
        faq = ''.join(f'<dt>{G.esc(q)}</dt><dd>{a}</dd>' for q, a in h['faq'])
        related = ''.join(f'<a href="../{o["slug"]}/">{G.esc(o["title"])}</a>' for o in items if o['slug'] != h['slug'])
        img = G.rel(path, h['image'])
        body = f"""<main class="guide howto wrap">
  <p class="crumb"><a href="{G.rel(path, L['home'])}">熟客簿</a> › <a href="../">使用教學</a></p>
  <h1>{G.esc(h['title'])}</h1>
  <p class="meta">約 {h['minutes']} 分鐘學會・更新：{h['updated']}</p>
  <div class="scenario">{h['scenario']}</div>
  <img class="hero-shot" src="{img}" alt="{G.esc(h['title'])}" loading="lazy">
  <h2>操作步驟</h2>
  <ol class="steps">{steps}</ol>
  {('<h2>小技巧</h2>' + h['tips']) if h.get('tips') else ''}
  <h2>常見問題</h2>
  <dl class="faq">{faq}</dl>
  {G.cta(LANG)}
  <h2>更多教學</h2>
  <div class="related">{related}</div>
</main>"""
        jsonld = [
            {'@context': 'https://schema.org', '@type': 'HowTo', 'name': h['title'], 'description': h['description'], 'inLanguage': 'zh-Hant-TW',
             'image': f"{G.SITE}/{h['image']}", 'totalTime': f"PT{h['minutes']}M",
             'tool': [{'@type': 'HowToTool', 'name': '熟客簿 App（iOS／Android）'}],
             'step': [{'@type': 'HowToStep', 'position': i + 1, 'name': n, 'text': G.strip(d), 'url': f'{url}#step-{i + 1}'} for i, (n, d) in enumerate(h['steps'])]},
            {'@context': 'https://schema.org', '@type': 'FAQPage',
             'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': G.strip(a)}} for q, a in h['faq']]},
            {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': '熟客簿', 'item': f"{G.SITE}/{L['home']}"},
                {'@type': 'ListItem', 'position': 2, 'name': '使用教學', 'item': f'{G.SITE}/{BASE}'},
                {'@type': 'ListItem', 'position': 3, 'name': h['title'], 'item': url}]},
        ]
        html = G.page(LANG, path, f"{h['title']}｜熟客簿使用教學", h['description'], body, jsonld)
        html = html.replace('</style>', CSS + '</style>', 1)
        # 步驟加錨點，方便從 App 或貼文直接連到某一步
        for i in range(len(h['steps'])):
            html = html.replace('<li><h3>', f'<li id="step-{i + 1}"><h3>', 1)
        paths.append(G.write(path, html))
    lst = ''.join(f'<a class="item" href="{h["slug"]}/"><b>{G.esc(h["title"])}</b><p>{G.esc(h["description"])}</p></a>' for h in items)
    lst += '<a class="item" href="../line-oa/"><b>連接 LINE 官方帳號</b><p>把你的 LINE 官方帳號接上熟客簿，客人傳來的訊息自動歸到客戶檔案。</p></a>'
    body = f"""<main class="guide-list wrap">
  <p class="crumb"><a href="../">熟客簿</a> › 使用教學</p>
  <h1>熟客簿使用教學</h1>
  <p style="color:var(--ink-2);margin-top:10px">每個功能用一個真實情境帶你走一遍：接待完怎麼記、什麼時候會提醒你、新貨到了怎麼找客人、訊息怎麼寫。</p>
  {lst}
</main>"""
    jsonld = [{'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': '熟客簿使用教學', 'url': f'{G.SITE}/{BASE}', 'inLanguage': 'zh-Hant-TW'}]
    paths.append(G.write(BASE, G.page(LANG, BASE, '熟客簿使用教學｜語音速記、提醒、貨找人、AI 擬訊', '熟客簿功能教學：語音速記、生日與回訪提醒、貨找人、AI 擬訊、LINE 速記、報價與成交，每個功能都有情境與分步驟說明。', body, jsonld, None, 'website')))
    G.update_sitemap(paths)
    print('howto pages', len(paths))


if __name__ == '__main__':
    build()
