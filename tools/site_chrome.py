"""熟客簿中文頁共用的頁首與頁尾（網站地圖 v2）。

導覽平鋪：功能｜價格｜店家方案｜學習資源｜語言｜免費試用；頁尾 4 欄＋語言列。
用絕對路徑（網站在 hueihetech.com 根目錄），任何深度的頁面都能直接套用。
build_guides.py（中文指南與教學）與 apply_chrome.py（其餘靜態頁）共用這裡，改一次全站生效。
"""

GLOBE = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">'
         '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>')
MENU = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">'
        '<line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="20" y2="17"/></svg>')

LANGS = [('中文', '/shukebu/'), ('English', '/en/veloce/'), ('日本語', '/ja/veloce/'), ('한국어', '/ko/veloce/'), ('Français', '/fr/veloce/')]
ITEMS = [('features', '功能', '/shukebu/features/', ''),
         ('pricing', '價格', '/shukebu/pricing/', ''),
         ('team', '店家方案', '/shukebu/team/', '<span class="soon">即將推出</span>'),
         ('learn', '學習資源', '/shukebu/learn/', '')]


def active_for(path: str) -> str:
    """依網址判斷目前在哪一區（給導覽列標示目前位置）"""
    p = path.strip('/')
    for key, prefixes in (('features', ('shukebu/features', 'shukebu/store', 'shukebu/line-oa')),
                          ('pricing', ('shukebu/pricing',)),
                          ('team', ('shukebu/team',)),
                          ('learn', ('shukebu/learn', 'shukebu/how-to', 'shukebu/guide', 'shukebu/changelog'))):
        if any(p == x or p.startswith(x + '/') for x in prefixes):
            return key
    return ''


def zh_header(active: str = '', cta: str = 'trial') -> str:
    cur = lambda k: ' aria-current="page"' if k == active else ''
    links = ''.join(f'<a href="{href}"{cur(k)}>{label}{extra}</a>' for k, label, href, extra in ITEMS)
    cta_html = ('<a class="cta" href="#waitlist">搶先登記</a>' if cta == 'waitlist'
                else '<a class="cta" href="/shukebu/download/">免費試用 14 天</a>')
    cur_lang = ' aria-current="true"'
    langs = ''.join(f'<a href="{h}"{cur_lang if n == "中文" else ""}>{n}</a>' for n, h in LANGS)
    mobile = ''.join(f'<a href="{href}"{cur(k)}>{label}{extra}</a>' for k, label, href, extra in ITEMS)
    return f"""<header class="site">
  <div class="wrap">
    <a class="logo" href="/shukebu/"><img src="/assets/shukebu-icon.png" alt="熟客簿"><span class="lt"><b>熟客簿</b><small>by 暉和智慧科技</small></span></a>
    <nav class="main" aria-label="主選單">
      {links}
      <details class="lang"><summary>{GLOBE}中文</summary><div class="pop">{langs}</div></details>
      {cta_html}
    </nav>
    <details class="menu"><summary aria-label="開啟選單">{MENU}</summary>
      <div class="sheet">{mobile}<div class="mlang">{GLOBE}{langs}</div>{cta_html}</div>
    </details>
  </div>
</header>"""


def zh_footer() -> str:
    col = lambda title, rows: (f'<div><h4>{title}</h4>' + ''.join(f'<p><a href="{h}">{t}</a></p>' for t, h in rows) + '</div>')
    langs = ' · '.join(f'<a href="{h}">{n}</a>' for n, h in LANGS)
    return f"""<footer class="site">
  <div class="wrap">
    <div class="fcols">
      <div>
        <div class="brandline"><img src="/assets/shukebu-icon.png" alt="">熟客簿</div>
        <p style="margin-top:10px">業務與店家的客戶經營 App<br>by 暉和智慧科技有限公司</p>
        <p><a href="mailto:support@hueihetech.com">support@hueihetech.com</a></p>
      </div>
      {col('產品', [('功能介紹', '/shukebu/features/'), ('LINE 官方帳號', '/shukebu/store/'), ('價格', '/shukebu/pricing/'), ('店家團隊方案', '/shukebu/team/'), ('免費下載', '/shukebu/download/')])}
      {col('學習資源', [('所有文章', '/shukebu/learn/'), ('使用教學', '/shukebu/how-to/'), ('經營指南', '/shukebu/guide/'), ('更新紀錄', '/shukebu/changelog/')])}
      {col('公司', [('暉和智慧科技', '/'), ('企業系統整合服務', '/services/'), ('聯絡我們', 'mailto:support@hueihetech.com')])}
      {col('條款', [('隱私權政策', '/legal/privacy.html'), ('服務條款', '/legal/terms.html'), ('刪除帳號', '/legal/delete-account.html')])}
    </div>
    <p class="fine flangs">{GLOBE} {langs}</p>
    <p class="fine">© 2026 暉和智慧科技有限公司 All rights reserved.</p>
  </div>
</footer>"""


# ───── 英日韓法（Veloce）：只有首頁、指南、下載頁，選單精簡成 功能｜指南｜語言｜免費試用 ─────
INTL = {
    'en': dict(features='Features', guides='Guides', trial='Free 14-day trial', download='Download', home='Veloce',
               tagline='The client book app for shops and sales advisors', product='Product', resources='Resources',
               company='Company', legal='Legal', company_name='Hueihe Tech', contact='Contact us',
               privacy='Privacy Policy', terms='Terms of Service', delete='Delete account', menu='Open menu', nav='Main menu',
               dl=True),
    'ja': dict(features='機能', guides='顧客管理ガイド', trial='14日間無料で試す', download='ダウンロード', home='Veloce',
               tagline='お店と販売スタッフのための顧客管理アプリ', product='製品', resources='ガイド',
               company='会社', legal='規約', company_name='Hueihe Tech', contact='お問い合わせ',
               privacy='プライバシーポリシー', terms='利用規約', delete='アカウントの削除', menu='メニューを開く', nav='メインメニュー',
               dl=True),
    'ko': dict(features='기능', guides='고객 관리 가이드', trial='14일 무료 체험', download='다운로드', home='Veloce',
               tagline='매장과 판매 직원을 위한 고객 관리 앱', product='제품', resources='가이드',
               company='회사', legal='약관', company_name='Hueihe Tech', contact='문의하기',
               privacy='개인정보처리방침', terms='이용약관', delete='계정 삭제', menu='메뉴 열기', nav='주 메뉴',
               dl=False),
    'fr': dict(features='Fonctionnalités', guides='Guides', trial='Essai gratuit 14 jours', download='Télécharger', home='Veloce',
               tagline="L'app de fichier clients pour boutiques et vendeurs", product='Produit', resources='Ressources',
               company='Entreprise', legal='Mentions légales', company_name='Hueihe Tech', contact='Nous contacter',
               privacy='Politique de confidentialité', terms="Conditions d'utilisation", delete='Supprimer le compte', menu='Ouvrir le menu', nav='Menu principal',
               dl=False),
}
LANG_NAME = {'en': 'English', 'ja': '日本語', 'ko': '한국어', 'fr': 'Français'}


def intl_active(path: str) -> str:
    return 'guides' if '/guide' in path else ''


def _intl_links(lang):
    t = INTL[lang]
    base = f'/{lang}/veloce/'
    cta = base + ('download/' if t['dl'] else '#download')
    return t, base, cta


def intl_header(lang: str, active: str = '') -> str:
    t, base, cta = _intl_links(lang)
    cur = ' aria-current="page"'
    items = [('features', t['features'], base + '#features'), ('guides', t['guides'], base + 'guide/')]
    links = ''.join(f'<a href="{h}"{cur if k == active else ""}>{lab}</a>' for k, lab, h in items)
    cur_lang = ' aria-current="true"'
    langs = ''.join(f'<a href="{h}"{cur_lang if h == base else ""}>{n}</a>' for n, h in LANGS)
    cta_html = f'<a class="cta" href="{cta}">{t["trial"]}</a>'
    return f"""<header class="site">
  <div class="wrap">
    <a class="logo" href="{base}"><img src="/assets/shukebu-icon.png" alt="Veloce"><span class="lt"><b>Veloce</b><small>by Hueihe Tech</small></span></a>
    <nav class="main" aria-label="{t['nav']}">
      {links}
      <details class="lang"><summary>{GLOBE}{LANG_NAME[lang]}</summary><div class="pop">{langs}</div></details>
      {cta_html}
    </nav>
    <details class="menu"><summary aria-label="{t['menu']}">{MENU}</summary>
      <div class="sheet">{links}<div class="mlang">{GLOBE}{langs}</div>{cta_html}</div>
    </details>
  </div>
</header>"""


def intl_footer(lang: str) -> str:
    t, base, cta = _intl_links(lang)
    col = lambda title, rows: (f'<div><h4>{title}</h4>' + ''.join(f'<p><a href="{h}">{x}</a></p>' for x, h in rows) + '</div>')
    langs = ' · '.join(f'<a href="{h}">{n}</a>' for n, h in LANGS)
    legal = f'/legal/{lang}/'
    return f"""<footer class="site">
  <div class="wrap">
    <div class="fcols">
      <div>
        <div class="brandline"><img src="/assets/shukebu-icon.png" alt="">Veloce</div>
        <p style="margin-top:10px">{t['tagline']}<br>by Hueihe Tech</p>
        <p><a href="mailto:support@hueihetech.com">support@hueihetech.com</a></p>
      </div>
      {col(t['product'], [(t['features'], base + '#features'), (t['download'], cta)])}
      {col(t['resources'], [(t['guides'], base + 'guide/')])}
      {col(t['company'], [(t['company_name'], '/'), (t['contact'], 'mailto:support@hueihetech.com')])}
      {col(t['legal'], [(t['privacy'], legal + 'privacy.html'), (t['terms'], legal + 'terms.html'), (t['delete'], legal + 'delete-account.html')])}
    </div>
    <p class="fine flangs">{GLOBE} {langs}</p>
    <p class="fine">© 2026 Hueihe Tech. All rights reserved.</p>
  </div>
</footer>"""
