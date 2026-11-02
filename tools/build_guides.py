#!/usr/bin/env python3
"""熟客簿指南文章產生器（SEO／AEO）：文章內容寫在 tools/guides/*.py，執行後輸出 shukebu/guide/<slug>/index.html 與 shukebu/guide/index.html。
每篇自動帶 Article、FAQPage、BreadcrumbList 結構化資料；第一段請寫成「直接回答標題問題」的一段話（AI 搜尋最常引用）。
用法：python3 tools/build_guides.py"""
import html, json, os, importlib.util, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://hueihetech.com'
APP_STORE = 'https://apps.apple.com/tw/app/id6811958084'
PLAY = 'https://play.google.com/store/apps/details?id=com.hueihetech.veloce'

CSS = """
.guide{max-width:760px;margin:0 auto;padding-block:48px 64px}
.guide .crumb{font-size:13px;color:var(--muted)}
.guide h1{font-size:clamp(26px,4.2vw,34px);line-height:1.4;margin-top:10px;text-wrap:balance}
.guide .meta{font-size:13px;color:var(--muted);margin-top:8px}
.guide .answer{background:var(--teal-soft);border-radius:14px;padding:18px 20px;margin-top:24px;font-size:16.5px;color:var(--ink)}
.guide h2{font-size:22px;margin-top:40px;line-height:1.45}
.guide h3{font-size:18px;margin-top:26px}
.guide p,.guide li{font-size:16px;color:var(--ink-2);margin-top:12px}
.guide ul,.guide ol{padding-left:1.4em}
.guide table{border-collapse:collapse;margin-top:16px;font-size:15px;width:100%}
.guide th,.guide td{border:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top}
.guide th{background:var(--bg-soft)}
.guide .tablewrap{overflow-x:auto}
.guide .faq dt{font-weight:700;color:var(--ink);margin-top:20px}
.guide .faq dd{color:var(--ink-2);margin-top:6px}
.guide .cta-box{border:1px solid var(--line);border-radius:18px;padding:24px;margin-top:44px;text-align:center}
.guide .cta-box .actions{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:16px}
.guide .related a{display:block;margin-top:8px}
.guide-list{max-width:760px;margin:0 auto;padding-block:48px 64px}
.guide-list a.item{display:block;border:1px solid var(--line);border-radius:16px;padding:20px 22px;margin-top:16px;color:var(--ink)}
.guide-list a.item:hover{border-color:var(--brand)}
.guide-list a.item p{color:var(--muted);font-size:15px;margin-top:6px}
"""

def esc(s):
    return html.escape(s, quote=True)

def page(title, desc, canonical, body, jsonld, depth):
    up = '../' * depth
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in jsonld)
    return f"""<!DOCTYPE html>
<html lang="zh-Hant-TW">
<head>
<meta charset="utf-8">
<link rel="canonical" href="{canonical}">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="icon" href="{up}assets/favicon.png">
<link rel="stylesheet" href="{up}assets/site.css">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}/assets/shukebu-icon.png">
<meta property="og:url" content="{canonical}">
<style>{CSS}</style>
{ld}</head>
<body>
<header class="site">
  <div class="wrap">
    <a class="logo" href="{up}shukebu/"><img src="{up}assets/shukebu-icon.png" alt="熟客簿">熟客簿</a>
    <nav>
      <a href="{up}shukebu/guide/">經營指南</a>
      <a href="{up}shukebu/features/">功能介紹</a>
      <a class="cta" href="{up}shukebu/#download">免費試用 14 天</a>
    </nav>
  </div>
</header>
{body}
<footer class="site">
  <div class="wrap">
    <div class="cols">
      <div>
        <div class="brandline"><img src="{up}assets/shukebu-icon.png" alt="">熟客簿</div>
        <p style="margin-top:10px">by 暉和智慧科技有限公司</p>
        <p><a href="mailto:support@hueihetech.com">support@hueihetech.com</a></p>
      </div>
      <div>
        <p><a href="{up}shukebu/">熟客簿</a></p>
        <p><a href="{up}shukebu/guide/">經營指南</a></p>
        <p><a href="{up}legal/privacy.html">隱私權政策</a></p>
        <p><a href="{up}legal/terms.html">服務條款</a></p>
      </div>
    </div>
    <p class="fine">© 2026 暉和智慧科技有限公司 All rights reserved.</p>
  </div>
</footer>
</body>
</html>
"""

def load_guides():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'tools', 'guides', '*.py'))):
        spec = importlib.util.spec_from_file_location(os.path.basename(f)[:-3], f)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        out.append(m.GUIDE)
    return sorted(out, key=lambda g: g['order'])

CTA = f"""<div class="cta-box">
  <h3 style="margin-top:0">想直接試試看？</h3>
  <p>熟客簿是給第一線銷售顧問用的客戶管理 App：講 30 秒記好客人、生日回訪自動提醒、新貨到了幫你找出該通知誰。免費試用 14 天，不用綁信用卡。</p>
  <div class="actions">
    <a class="btn primary" href="{APP_STORE}" target="_blank" rel="noopener">App Store 下載</a>
    <a class="btn primary" href="{PLAY}" target="_blank" rel="noopener">Google Play 下載</a>
  </div>
</div>"""

def build():
    guides = load_guides()
    base = f'{SITE}/shukebu/guide/'
    for g in guides:
        url = f"{base}{g['slug']}/"
        faq_html = ''.join(f'<dt>{esc(q)}</dt><dd>{a}</dd>' for q, a in g['faq'])
        others = [o for o in guides if o['slug'] != g['slug']]
        related = ''.join(f'<a href="../{o["slug"]}/">{esc(o["title"])}</a>' for o in others)
        body = f"""<main class="guide wrap">
  <p class="crumb"><a href="../../">熟客簿</a> › <a href="../">經營指南</a></p>
  <h1>{esc(g['title'])}</h1>
  <p class="meta">更新：{g['updated']}・暉和智慧科技</p>
  <p class="answer">{g['answer']}</p>
  {g['body']}
  <h2>常見問題</h2>
  <dl class="faq">{faq_html}</dl>
  {CTA}
  <h2>延伸閱讀</h2>
  <div class="related">{related}</div>
</main>"""
        strip = lambda s: html.unescape(__import__('re').sub(r'<[^>]+>', '', s))
        jsonld = [
            {'@context': 'https://schema.org', '@type': 'Article', 'headline': g['title'], 'description': g['description'],
             'datePublished': g['published'], 'dateModified': g['updated'], 'inLanguage': 'zh-Hant-TW', 'mainEntityOfPage': url,
             'author': {'@type': 'Organization', 'name': '暉和智慧科技有限公司', 'url': SITE},
             'publisher': {'@type': 'Organization', 'name': '暉和智慧科技有限公司', 'logo': {'@type': 'ImageObject', 'url': f'{SITE}/assets/shukebu-icon.png'}}},
            {'@context': 'https://schema.org', '@type': 'FAQPage',
             'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': strip(a)}} for q, a in g['faq']]},
            {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': '熟客簿', 'item': f'{SITE}/shukebu/'},
                {'@type': 'ListItem', 'position': 2, 'name': '經營指南', 'item': base},
                {'@type': 'ListItem', 'position': 3, 'name': g['title'], 'item': url}]},
        ]
        out = os.path.join(ROOT, 'shukebu', 'guide', g['slug'], 'index.html')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(page(f"{g['title']}｜熟客簿", g['description'], url, body, jsonld, 3))
        print('wrote', out)
    items = ''.join(f'<a class="item" href="{g["slug"]}/"><b>{esc(g["title"])}</b><p>{esc(g["description"])}</p></a>' for g in guides)
    body = f"""<main class="guide-list wrap">
  <p class="crumb" style="font-size:13px;color:var(--muted)"><a href="../">熟客簿</a> › 經營指南</p>
  <h1 style="font-size:clamp(26px,4.2vw,34px);margin-top:10px">銷售顧問的客戶經營指南</h1>
  <p style="color:var(--ink-2);margin-top:10px">給珠寶、精品、鐘錶、保險、房仲、汽車的第一線業務：怎麼選 CRM、怎麼記客人、怎麼不漏掉每一次跟進。</p>
  {items}
</main>"""
    jsonld = [{'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': '銷售顧問的客戶經營指南', 'url': base, 'inLanguage': 'zh-Hant-TW'}]
    open(os.path.join(ROOT, 'shukebu', 'guide', 'index.html'), 'w', encoding='utf-8').write(
        page('銷售顧問的客戶經營指南｜熟客簿', '台灣第一線銷售顧問的客戶經營指南：CRM 怎麼選、Excel 換客戶管理 App、LINE 客戶管理、生日與回訪提醒。', base, body, jsonld, 2))
    print('wrote guide index')
    return guides

if __name__ == '__main__':
    build()
