#!/usr/bin/env python3
"""熟客簿／Veloce 多語系 SEO 頁面產生器（SEO／AEO）。
- 文章：tools/guides/<lang>/*.py，每檔一個 GUIDE dict（見下方 GUIDE 欄位說明）。
- 英日韓落地頁：tools/guides/<lang>/_landing.py 的 LANDING dict（中文落地頁是手寫的 shukebu/index.html，不產生）。
- 輸出：中文 shukebu/guide/…；英日韓 <lang>/veloce/、<lang>/veloce/guide/…。並重寫 sitemap 裡這些頁面。
每篇自動帶 Article、FAQPage、BreadcrumbList；第一段 answer 寫成「直接回答標題問題」的一段話（AI 搜尋最常引用）。
用法：python3 tools/build_guides.py

GUIDE 欄位：order（排序）、slug、title、description（meta，約 80～160 字元）、published／updated（YYYY-MM-DD）、
answer（第一段，純文字或簡單 HTML）、body（HTML：h2／h3／p／ul／ol／div.tablewrap>table）、faq（[(問, 答)]，答可含簡單 HTML）"""
import html, json, os, re, glob, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://hueihetech.com'
APP_STORE_ID = '6811958084'
PKG = 'com.hueihetech.veloce'

LANGS = {
    'zh-TW': dict(html='zh-Hant-TW', home='shukebu/', guide='shukebu/guide/', name='熟客簿', legal='legal/',
                  appstore=f'https://apps.apple.com/tw/app/id{APP_STORE_ID}', play=f'https://play.google.com/store/apps/details?id={PKG}',
                  t=dict(guides='經營指南', features='功能介紹', features_href='features/', trial='免費試用 14 天', updated='更新', org='暉和智慧科技',
                         faq='常見問題', related='延伸閱讀', cta_title='想直接試試看？',
                         cta_text='熟客簿是給第一線銷售顧問用的客戶管理 App：講 30 秒記好客人、生日回訪自動提醒、新貨到了幫你找出該通知誰。免費試用 14 天，不用綁信用卡。',
                         appstore='App Store 下載', play='Google Play 下載', privacy='隱私權政策', terms='服務條款',
                         list_title='銷售顧問的客戶經營指南', list_sub='給珠寶、精品、鐘錶、保險、房仲、汽車的第一線業務：怎麼選 CRM、怎麼記客人、怎麼不漏掉每一次跟進。',
                         list_desc='台灣第一線銷售顧問的客戶經營指南：CRM 怎麼選、Excel 換客戶管理 App、LINE 客戶管理、生日與回訪提醒、各行業的熟客經營。',
                         company='暉和智慧科技有限公司', langs='語言')),
    'en': dict(html='en', home='en/veloce/', guide='en/veloce/guide/', name='Veloce', legal='legal/en/',
               appstore=f'https://apps.apple.com/app/id{APP_STORE_ID}', play=f'https://play.google.com/store/apps/details?id={PKG}&hl=en',
               t=dict(guides='Guides', features='Features', features_href='#features', trial='Free 14-day trial', updated='Updated', org='Hueihe Tech',
                      faq='FAQ', related='Related guides', cta_title='Want to try it?',
                      cta_text='Veloce is a client book app for front-line sales: talk for 30 seconds to log a client, get reminded of birthdays and follow-ups, and see who to call when new stock arrives. Free 14-day trial, no credit card required.',
                      appstore='Download on the App Store', play='Get it on Google Play', privacy='Privacy Policy', terms='Terms of Service',
                      list_title='Client management guides for sales advisors', list_sub='For front-line sales in jewelry, watches, luxury, insurance, real estate and cars: choosing a CRM, keeping client notes and never missing a follow-up.',
                      list_desc='Practical guides for retail sales advisors and sales reps: choosing a CRM, clienteling, client notes, follow-up reminders and WhatsApp client management.',
                      company='Hueihe Tech', langs='Language')),
    'ja': dict(html='ja', home='ja/veloce/', guide='ja/veloce/guide/', name='Veloce', legal='legal/ja/',
               appstore=f'https://apps.apple.com/jp/app/id{APP_STORE_ID}', play=f'https://play.google.com/store/apps/details?id={PKG}&hl=ja',
               t=dict(guides='顧客管理ガイド', features='機能', features_href='#features', trial='14日間無料で試す', updated='更新', org='Hueihe Tech',
                      faq='よくある質問', related='関連ガイド', cta_title='まずは試してみませんか？',
                      cta_text='Veloceは販売スタッフのための顧客管理アプリです。接客のあとに30秒話すだけで記録、誕生日やフォローを自動でお知らせ、新入荷のときに連絡すべきお客様もわかります。14日間無料、クレジットカード登録は不要です。',
                      appstore='App Storeでダウンロード', play='Google Playで手に入れよう', privacy='プライバシーポリシー', terms='利用規約',
                      list_title='販売スタッフのための顧客管理ガイド', list_sub='ジュエリー・時計・ブランド品・保険・不動産・自動車の販売スタッフ向けに、CRMの選び方、顧客情報の記録、フォローの方法をまとめました。',
                      list_desc='販売スタッフ・営業担当のための顧客管理ガイド。CRM・顧客管理アプリの選び方、顧客台帳、LINEでの顧客管理、誕生日やフォローのリマインダー。',
                      company='Hueihe Tech', langs='言語')),
    'ko': dict(html='ko', home='ko/veloce/', guide='ko/veloce/guide/', name='Veloce', legal='legal/ko/',
               appstore=f'https://apps.apple.com/kr/app/id{APP_STORE_ID}', play=f'https://play.google.com/store/apps/details?id={PKG}&hl=ko',
               t=dict(guides='고객 관리 가이드', features='기능', features_href='#features', trial='14일 무료 체험', updated='업데이트', org='Hueihe Tech',
                      faq='자주 묻는 질문', related='관련 가이드', cta_title='직접 써 보시겠어요?',
                      cta_text='Veloce는 판매 직원을 위한 고객 관리 앱이에요. 상담 후 30초만 말하면 기록되고, 생일과 팔로업을 자동으로 알려 주고, 신상품이 들어오면 연락할 고객까지 알려 드려요. 14일 무료 체험, 카드 등록이 필요 없어요.',
                      appstore='App Store에서 다운로드', play='Google Play에서 받기', privacy='개인정보 처리방침', terms='이용약관',
                      list_title='판매 직원을 위한 고객 관리 가이드', list_sub='주얼리·시계·명품·보험·부동산·자동차 판매 직원을 위해 CRM 고르는 법, 고객 정보 기록, 팔로업 방법을 정리했어요.',
                      list_desc='판매 직원과 영업 담당자를 위한 고객 관리 가이드. CRM·고객관리 앱 고르는 법, 엑셀 고객 관리, 단골 관리, 생일과 팔로업 리마인더.',
                      company='Hueihe Tech', langs='언어')),
}
LANG_LABEL = {'zh-TW': '中文', 'en': 'English', 'ja': '日本語', 'ko': '한국어'}

CSS = """
.guide{max-width:760px;margin:0 auto;padding-block:48px 64px}
.guide .crumb,.guide-list .crumb{font-size:13px;color:var(--muted)}
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
.cta-box{border:1px solid var(--line);border-radius:18px;padding:24px;margin-top:44px;text-align:center}
.cta-box .actions{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:16px}
.guide .related a{display:block;margin-top:8px}
.guide-list{max-width:760px;margin:0 auto;padding-block:48px 64px}
.guide-list h1{font-size:clamp(26px,4.2vw,34px);margin-top:10px}
.guide-list a.item{display:block;border:1px solid var(--line);border-radius:16px;padding:20px 22px;margin-top:16px;color:var(--ink)}
.guide-list a.item:hover{border-color:var(--brand)}
.guide-list a.item p{color:var(--muted);font-size:15px;margin-top:6px}
.langs a{margin-right:12px}
"""

esc = lambda s: html.escape(s, quote=True)
strip = lambda s: html.unescape(re.sub(r'<[^>]+>', '', s))


def rel(from_dir, to):
    """站內相對路徑：from_dir、to 都是不含開頭斜線的站內路徑"""
    depth = len([p for p in from_dir.split('/') if p])
    return '../' * depth + to


def page(lang, path, title, desc, body, jsonld, alternates=None, og_type='article'):
    L = LANGS[lang]; t = L['t']; up = lambda to: rel(path, to)
    canonical = f'{SITE}/{path}'
    alt = ''.join(f'<link rel="alternate" hreflang="{LANGS[k]["html"]}" href="{SITE}/{v}">\n' for k, v in (alternates or {}).items())
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in jsonld)
    langs = ''.join(f'<a href="{up(LANGS[k]["home"])}">{LANG_LABEL[k]}</a>' for k in LANGS if k != lang)
    return f"""<!DOCTYPE html>
<html lang="{L['html']}">
<head>
<meta charset="utf-8">
<link rel="canonical" href="{canonical}">
{alt}<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="icon" href="{up('assets/favicon.png')}">
<link rel="stylesheet" href="{up('assets/site.css')}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}/assets/shukebu-icon.png">
<meta property="og:url" content="{canonical}">
<style>{CSS}</style>
{ld}</head>
<body>
<header class="site">
  <div class="wrap">
    <a class="logo" href="{up(L['home'])}"><img src="{up('assets/shukebu-icon.png')}" alt="{esc(L['name'])}">{esc(L['name'])}</a>
    <nav>
      <a href="{up(L['guide'])}">{t['guides']}</a>
      <a class="cta" href="{up(L['home'])}#download">{t['trial']}</a>
    </nav>
  </div>
</header>
{body}
<footer class="site">
  <div class="wrap">
    <div class="cols">
      <div>
        <div class="brandline"><img src="{up('assets/shukebu-icon.png')}" alt="">{esc(L['name'])}</div>
        <p style="margin-top:10px">by {t['company']}</p>
        <p><a href="mailto:support@hueihetech.com">support@hueihetech.com</a></p>
      </div>
      <div>
        <p><a href="{up(L['home'])}">{esc(L['name'])}</a></p>
        <p><a href="{up(L['guide'])}">{t['guides']}</a></p>
        <p><a href="{up(L['legal'] + 'privacy.html')}">{t['privacy']}</a></p>
        <p><a href="{up(L['legal'] + 'terms.html')}">{t['terms']}</a></p>
        <p class="langs">{t['langs']}：{langs}</p>
      </div>
    </div>
    <p class="fine">© 2026 {t['company']}</p>
  </div>
</footer>
</body>
</html>
"""


def load(lang):
    guides, landing = [], None
    for f in sorted(glob.glob(os.path.join(ROOT, 'tools', 'guides', lang, '*.py'))):
        spec = importlib.util.spec_from_file_location(f'{lang}_{os.path.basename(f)[:-3]}', f)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        if os.path.basename(f) == '_landing.py':
            landing = m.LANDING
        else:
            guides.append(m.GUIDE)
    return sorted(guides, key=lambda g: g['order']), landing


def cta(lang):
    L = LANGS[lang]; t = L['t']
    return f"""<div class="cta-box">
  <h3 style="margin-top:0">{t['cta_title']}</h3>
  <p>{t['cta_text']}</p>
  <div class="actions">
    <a class="btn primary" href="{L['appstore']}" target="_blank" rel="noopener">{t['appstore']}</a>
    <a class="btn primary" href="{L['play']}" target="_blank" rel="noopener">{t['play']}</a>
  </div>
</div>"""


def write(path, content):
    out = os.path.join(ROOT, path, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(content)
    return path


def org(lang):
    return {'@type': 'Organization', 'name': '暉和智慧科技有限公司' if lang == 'zh-TW' else 'Hueihe Tech', 'url': SITE}


def build_lang(lang):
    L = LANGS[lang]; t = L['t']
    guides, landing = load(lang)
    paths = []
    gbase = L['guide']
    for g in guides:
        path = f"{gbase}{g['slug']}/"
        faq_html = ''.join(f'<dt>{esc(q)}</dt><dd>{a}</dd>' for q, a in g['faq'])
        related = ''.join(f'<a href="../{o["slug"]}/">{esc(o["title"])}</a>' for o in guides if o['slug'] != g['slug'])
        body = f"""<main class="guide wrap">
  <p class="crumb"><a href="{rel(path, L['home'])}">{esc(L['name'])}</a> › <a href="../">{t['guides']}</a></p>
  <h1>{esc(g['title'])}</h1>
  <p class="meta">{t['updated']}: {g['updated']} · {t['org']}</p>
  <p class="answer">{g['answer']}</p>
  {g['body']}
  <h2>{t['faq']}</h2>
  <dl class="faq">{faq_html}</dl>
  {cta(lang)}
  <h2>{t['related']}</h2>
  <div class="related">{related}</div>
</main>"""
        url = f'{SITE}/{path}'
        jsonld = [
            {'@context': 'https://schema.org', '@type': 'Article', 'headline': g['title'], 'description': g['description'],
             'datePublished': g['published'], 'dateModified': g['updated'], 'inLanguage': L['html'], 'mainEntityOfPage': url,
             'author': org(lang), 'publisher': {**org(lang), 'logo': {'@type': 'ImageObject', 'url': f'{SITE}/assets/shukebu-icon.png'}}},
            {'@context': 'https://schema.org', '@type': 'FAQPage',
             'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': strip(a)}} for q, a in g['faq']]},
            {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': L['name'], 'item': f"{SITE}/{L['home']}"},
                {'@type': 'ListItem', 'position': 2, 'name': t['guides'], 'item': f'{SITE}/{gbase}'},
                {'@type': 'ListItem', 'position': 3, 'name': g['title'], 'item': url}]},
        ]
        suffix = '｜熟客簿' if lang == 'zh-TW' else ' | Veloce'
        paths.append(write(path, page(lang, path, g['title'] + suffix, g['description'], body, jsonld)))
    items = ''.join(f'<a class="item" href="{g["slug"]}/"><b>{esc(g["title"])}</b><p>{esc(g["description"])}</p></a>' for g in guides)
    body = f"""<main class="guide-list wrap">
  <p class="crumb"><a href="{rel(gbase, L['home'])}">{esc(L['name'])}</a> › {t['guides']}</p>
  <h1>{t['list_title']}</h1>
  <p style="color:var(--ink-2);margin-top:10px">{t['list_sub']}</p>
  {items}
</main>"""
    alts = {k: LANGS[k]['guide'] for k in LANGS}
    jsonld = [{'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': t['list_title'], 'url': f'{SITE}/{gbase}', 'inLanguage': L['html']}]
    suffix = '｜熟客簿' if lang == 'zh-TW' else ' | Veloce'
    paths.append(write(gbase, page(lang, gbase, t['list_title'] + suffix, t['list_desc'], body, jsonld, alts, 'website')))
    if landing:
        paths.append(build_landing(lang, landing, guides))
    return paths


def build_landing(lang, X, guides):
    L = LANGS[lang]; t = L['t']; path = L['home']
    cards = ''.join(f'<div class="card"><div class="num">{i + 1}</div><h3>{esc(h)}</h3><p>{p}</p></div>' for i, (h, p) in enumerate(X['cards']))
    shots = ''.join(f'<img src="{rel(path, f"assets/{lang}/phone-{k}.jpg")}" alt="{esc(a)}" loading="lazy">' for k, a in X['shots'])
    gl = ''.join(f'<a href="guide/{g["slug"]}/">{esc(g["title"])}</a><br>' for g in guides)
    body = f"""<div class="hero">
  <div class="wrap product-hero">
    <div class="txt" style="text-align:left">
      <p style="color:var(--brand);font-weight:700;font-size:15px;margin-bottom:10px">{esc(X['eyebrow'])}</p>
      <h1>{X['h1']}</h1>
      <p class="sub" style="margin-top:14px">{esc(X['sub'])}</p>
      <div class="badges" id="download">
        <a class="badge-btn" href="{L['appstore']}" target="_blank" rel="noopener"><span><small>Download on the</small>App Store</span></a>
        <a class="badge-btn" href="{L['play']}" target="_blank" rel="noopener"><span><small>GET IT ON</small>Google Play</span></a>
      </div>
      <p style="color:var(--muted);font-size:13.5px;margin-top:12px">{esc(X['trial_note'])}</p>
    </div>
    <img src="{rel(path, f'assets/{lang}/phone-voice.jpg')}" alt="{esc(X['shots'][0][1])}" style="width:min(300px,78vw);border-radius:22px;box-shadow:0 18px 44px rgba(15,23,42,.2)">
  </div>
</div>
<section id="features">
  <div class="wrap">
    <h2 class="sec">{esc(X['features_title'])}</h2>
    <p class="sec-sub">{esc(X['features_sub'])}</p>
    <div class="cards">{cards}</div>
  </div>
</section>
<section class="alt" id="screens">
  <div class="wrap">
    <h2 class="sec">{esc(X['screens_title'])}</h2>
    <div class="shots">{shots}</div>
  </div>
</section>
<section>
  <div class="wrap" style="max-width:760px">
    <h2 class="sec">{t['guides']}</h2>
    <p style="margin-top:20px;line-height:2">{gl}</p>
    {cta(lang)}
  </div>
</section>"""
    app = {'@context': 'https://schema.org', '@type': 'SoftwareApplication', 'name': 'Veloce', 'alternateName': ['熟客簿'],
           'applicationCategory': 'BusinessApplication', 'applicationSubCategory': 'CRM', 'operatingSystem': 'iOS, Android',
           'inLanguage': L['html'], 'description': X['description'], 'url': f'{SITE}/{path}', 'image': f'{SITE}/assets/shukebu-icon.png',
           'downloadUrl': [L['appstore'], L['play']], 'offers': {'@type': 'Offer', 'price': '0', 'description': X['trial_note']}, 'publisher': org(lang)}
    alts = {k: LANGS[k]['home'] for k in LANGS}
    return write(path, page(lang, path, X['title'], X['description'], body, [app], alts, 'website'))


def update_sitemap(paths):
    p = os.path.join(ROOT, 'sitemap.xml'); s = open(p, encoding='utf-8').read()
    for path in paths:
        loc = f'{SITE}/{path}'
        if f'<loc>{loc}</loc>' not in s:
            s = s.replace('</urlset>', f'  <url><loc>{loc}</loc><lastmod>2026-11-02</lastmod><priority>0.8</priority></url>\n</urlset>')
    open(p, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    all_paths = []
    for lang in LANGS:
        ps = build_lang(lang)
        all_paths += ps
        print(lang, len(ps), 'pages')
    update_sitemap(all_paths)
