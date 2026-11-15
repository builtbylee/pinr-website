#!/usr/bin/env python3
"""Moves the FAQ, privacy and terms pages onto the Souvenir layout. Their wording is kept exactly; only the markup changes.
Run once on the old pages (it reads the old structure); afterwards edit the generated pages directly."""
import html, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build import NAV, FOOT
R = pathlib.Path(__file__).resolve().parent.parent

def clean(fragment):
    f = re.sub(r'(?s)<!--.*?-->', '', fragment)
    f = re.sub(r'<i data-feather="[^"]*"></i>', '', f)
    f = re.sub(r'\s(class|style|id|onclick|target|rel)="[^"]*"', '', f)
    f = re.sub(r'(?s)<script.*?</script>', '', f)
    f = re.sub(r'/cdn-cgi/l/email-protection#[0-9a-f]+', 'mailto:lee@getpinr.com', f)
    f = re.sub(r'<span data-cfemail="[0-9a-f]+">\[email&#160;protected\]</span>', 'lee@getpinr.com', f)
    f = f.replace('<span>[email&#160;protected]</span>', 'lee@getpinr.com')
    return re.sub(r'[ \t]*\n[ \t]*', '\n', f).strip()

def shell(title, desc, h1, sub, body, path):
    sub_html = f'<p>{sub}</p>' if sub else ''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#E9FBFF">
<link rel="canonical" href="https://getpinr.com/{path}">
<link rel="icon" type="image/png" href="/favicon-v4.png">
<link rel="preload" href="/assets/v2/fonts/bricolage.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/v2/site.css">
</head>
<body class="page">
<a class="skip" href="#main">Skip to content</a>
{NAV}
<main id="main">
<header class="top"><div class="cl c2" aria-hidden="true" style="left:auto;right:6%;top:84px"><img src="/assets/v2/cloud-b.webp" alt="" width="120" height="71"></div><div class="cl c5" aria-hidden="true" style="left:auto;right:22%;top:170px;display:block"><img src="/assets/v2/cloud-a.webp" alt="" width="90" height="53"></div>
  <div class="wrap"><h1>{h1}</h1>{sub_html}</div></header>
<div class="body wrap">
{body}
</div>
</main>
{FOOT}
</body>
</html>
'''

def legal(name, title, desc):
    s = (R / name).read_text()
    b = s[s.index('</nav>') + 6: s.rindex('</body>')]
    b = re.sub(r'(?s)<footer.*?</footer>', '', b)
    h1 = re.search(r'<h1>(.*?)</h1>', b).group(1)
    b = re.sub(r'<h1>.*?</h1>\s*', '', b)
    b = re.sub(r'<p><strong>Last Updated:</strong>\s*(.*?)</p>', r'<p class="meta">Last updated: \1</p>', b, count=1)
    b = clean(b)
    while b.endswith('</div>') and b.count('<div') < b.count('</div>'): b = b[:-6].rstrip()
    (R / name).write_text(shell(title, desc, h1, '', f'<article class="card prose">\n{b}\n</article>', name))

def faq():
    s = (R / 'faq.html').read_text()
    out = []
    for sec in re.finditer(r'(?s)<div class="faq-section"[^>]*>(.*?)(?=<div class="faq-section"|<div class="contact-section")', s):
        body = sec.group(1)
        t = re.search(r'(?s)<h2 class="section-title">.*?<span>(.*?)</span>', body).group(1).strip()
        out.append(f'<h2 class="group">{t}</h2>')
        for q in re.finditer(r'(?s)<div class="faq-question">(.*?)</div>\s*<div class="faq-answer">(.*?)</div>\s*</div>', body):
            a = clean(q.group(2))
            if not a.startswith('<'): a = '<p>' + a
            a = re.sub(r'(?<=[^>])\n(?=<(ol|ul)>)', '</p>\n', a)
            if a.startswith('<p>') and '</p>' not in a: a += '</p>'
            out.append(f'<details class="card"><summary>{clean(q.group(1))}</summary><div class="a">{a}</div></details>')
    assert len(out) > 10, 'faq parse failed'
    help_ = '<div class="card help"><div><h2>Still have questions?</h2><p>Write to us and we will get back to you.</p></div><a class="btn fill" href="mailto:lee@getpinr.com">Contact support</a></div>'
    body = '<div class="faq">\n' + '\n'.join(out) + '\n</div>\n' + help_
    (R / 'faq.html').write_text(shell('Pinr FAQ', 'Answers to common questions about Pinr: pins, friends, games, privacy and your account.', 'Frequently asked questions', 'Everything you need to know about Pinr.', body, 'faq.html'))
    print('faq questions', sum(1 for x in out if x.startswith('<details')))

if __name__ == '__main__':
    faq()
    legal('privacy-policy.html', 'Pinr Privacy Policy', 'How Pinr collects, uses and protects your information.')
    legal('terms-of-service.html', 'Pinr Terms of Service and Code of Conduct', 'The terms for using Pinr, and the community rules.')
