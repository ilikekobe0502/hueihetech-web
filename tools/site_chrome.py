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
