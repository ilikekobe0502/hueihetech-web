#!/usr/bin/env python3
"""把共用頁首頁尾（site_chrome.py）套到 shukebu/ 底下所有手寫的中文頁。
重複執行沒關係：每次都整段換掉 <header class="site">…</header> 與 <footer class="site">…</footer>。
用法：python3 tools/apply_chrome.py
"""
import glob, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import site_chrome as C

ROOT = os.path.join(os.path.dirname(__file__), '..')
SKIP = {'shukebu/open'}  # App 內部跳轉頁，沒有頁首頁尾

changed = 0
for f in sorted(glob.glob(os.path.join(ROOT, 'shukebu', '**', 'index.html'), recursive=True)):
    rel = os.path.relpath(os.path.dirname(f), ROOT).replace(os.sep, '/')
    if rel in SKIP:
        continue
    s = open(f, encoding='utf-8').read()
    if '<header class="site">' not in s:
        continue
    cta = 'waitlist' if rel == 'shukebu/team' else 'trial'
    new = re.sub(r'<header class="site">.*?</header>', lambda _: C.zh_header(C.active_for('/' + rel + '/'), cta), s, count=1, flags=re.S)
    new = re.sub(r'<footer class="site">.*?</footer>', lambda _: C.zh_footer(), new, count=1, flags=re.S)
    if new != s:
        open(f, 'w', encoding='utf-8').write(new)
        changed += 1
        print('updated', rel)
for lang in C.INTL:
    for f in sorted(glob.glob(os.path.join(ROOT, lang, 'veloce', '**', 'index.html'), recursive=True)):
        rel = os.path.relpath(os.path.dirname(f), ROOT).replace(os.sep, '/')
        s = open(f, encoding='utf-8').read()
        if '<header class="site">' not in s:
            continue
        new = re.sub(r'<header class="site">.*?</header>', lambda _: C.intl_header(lang, C.intl_active('/' + rel + '/')), s, count=1, flags=re.S)
        new = re.sub(r'<footer class="site">.*?</footer>', lambda _: C.intl_footer(lang), new, count=1, flags=re.S)
        if new != s:
            open(f, 'w', encoding='utf-8').write(new)
            changed += 1
            print('updated', rel)
print('pages changed:', changed)
