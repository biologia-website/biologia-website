# -*- coding: utf-8 -*-
"""生成新闻详情页 news/{id}.html（① 佰洛生物风格，单数据源 data/news.json）。
用法：python _gen_news.py
新增/修改资讯后，编辑 data/news.json 再运行本脚本即可。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, 'data', 'news.json')
OUTDIR = os.path.join(BASE, 'news')

CSS = """
  :root{
    --primary:#0a5c8a; --primary-light:#0d7ab5; --primary-dark:#064368;
    --accent:#00a896; --bg:#f7f9fc; --bg-card:#ffffff; --text:#1a202c;
    --text-muted:#718096; --border:#e2e8f0; --radius:10px; --shadow:0 2px 12px rgba(0,0,0,.06);
    --shadow-hover:0 6px 24px rgba(0,0,0,.10); --max-width:1200px;
  }
  *{box-sizing:border-box;margin:0;padding:0;}
  body{font-family:-apple-system,"Segoe UI","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--text);line-height:1.6;}
  a{color:inherit;}
  .nav{background:rgba(255,255,255,.95);backdrop-filter:blur(8px);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100;}
  .nav-inner{max-width:var(--max-width);margin:0 auto;padding:0 24px;height:64px;display:flex;align-items:center;justify-content:space-between;}
  .nav-logo{display:flex;align-items:center;gap:10px;font-weight:700;font-size:18px;color:var(--primary-dark);text-decoration:none;}
  .nav-logo .dot{width:10px;height:10px;border-radius:50%;background:var(--accent);}
  .nav-links{display:flex;gap:6px;list-style:none;}
  .nav-links a{padding:8px 14px;border-radius:6px;text-decoration:none;color:var(--text);font-size:15px;}
  .nav-links a:hover{color:var(--primary);background:#f0f4f8;}
  .nav-links a.active{color:var(--primary);font-weight:600;}
  .nav-cta{background:var(--primary);color:#fff;border:none;border-radius:6px;padding:8px 16px;font-size:14px;font-weight:600;text-decoration:none;}
  .page-hero{background:linear-gradient(135deg,var(--primary),var(--accent));color:#fff;padding:56px 24px 48px;}
  .page-hero .inner{max-width:820px;margin:0 auto;}
  .breadcrumb{font-size:13px;opacity:.85;margin-bottom:14px;}
  .breadcrumb a{color:#fff;text-decoration:none;opacity:.9;}
  .page-hero .nh-meta{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:14px;}
  .nh-cat{font-size:12px;font-weight:600;padding:3px 11px;border-radius:4px;background:rgba(255,255,255,.18);}
  .nh-cat.industry{background:rgba(255,255,255,.22);}
  .nh-cat.tech{background:rgba(255,255,255,.22);}
  .nh-date{font-size:13px;opacity:.85;}
  .nh-src{font-size:13px;opacity:.85;}
  .page-hero h1{font-size:30px;font-weight:700;line-height:1.4;letter-spacing:.5px;}
  .article{max-width:820px;margin:0 auto;padding:48px 24px 64px;}
  .article p{font-size:16px;color:#2d3748;line-height:1.9;margin-bottom:20px;}
  .article .back{display:inline-block;margin-top:16px;color:var(--primary);font-weight:600;text-decoration:none;}
  .article .back:hover{color:var(--primary-light);}
  .footer{background:var(--primary-dark);color:#fff;padding:40px 24px 28px;}
  .footer-inner{max-width:var(--max-width);margin:0 auto;display:grid;grid-template-columns:repeat(4,1fr);gap:24px;}
  .footer-col h4{font-size:15px;margin-bottom:12px;}
  .footer-col a,.footer-col p{display:block;color:rgba(255,255,255,.75);text-decoration:none;font-size:14px;margin-bottom:8px;}
  .footer-col a:hover{color:#fff;}
  .footer-bottom{max-width:var(--max-width);margin:24px auto 0;padding-top:18px;border-top:1px solid rgba(255,255,255,.12);text-align:center;font-size:13px;color:rgba(255,255,255,.5);}
  @media(max-width:768px){.nav-links{display:none;}.footer-inner{grid-template-columns:1fr 1fr;}.page-hero h1{font-size:24px;}}
"""

NAV = """
<nav class="nav">
  <div class="nav-inner">
    <a href="../index.html" class="nav-logo"><span class="dot"></span>佰洛生物</a>
    <ul class="nav-links">
      <li><a href="../products.html">产品中心</a></li>
      <li><a href="../index.html#services">技术服务</a></li>
      <li><a href="news.html" class="active">新闻资讯</a></li>
      <li><a href="../index.html#about">关于佰洛</a></li>
      <li><a href="../contact.html">联系我们</a></li>
    </ul>
    <a href="../contact.html" class="nav-cta">获取报价</a>
  </div>
</nav>
"""

FOOTER = """
<footer class="footer">
  <div class="footer-inner">
    <div class="footer-col"><h4>佰洛生物</h4><p>高品质生物试剂与技术服务</p><p>&copy; 2026 Bailuo Biotech</p></div>
    <div class="footer-col"><h4>产品</h4><a href="../products.html#reagents">试剂与耗材</a><a href="../products.html#instruments">实验仪器</a><a href="news.html">新闻资讯</a></div>
    <div class="footer-col"><h4>服务</h4><a href="../index.html#services">iPSC 重编程</a><a href="../index.html#services">BLI 亲和力测定</a><a href="../index.html#services">病毒包装</a></div>
    <div class="footer-col"><h4>联系方式</h4><p>邮箱：service@biologia.cn</p><p>电话：18768439420</p></div>
  </div>
  <div class="footer-bottom">佰洛生物科技 &copy; 2026 &nbsp;|&nbsp; 为生命科学工作者提供高品质试剂与专业服务</div>
</footer>
"""

CAT_CLASS = {'行业资讯': ' industry', '技术干货': ' tech'}


def esc(s):
    return (s if s is not None else '').replace('&', '&amp;').replace('<', '&lt;') \
        .replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')


def build_page(n):
    nid = n['id']
    title = n.get('title', '')
    date = n.get('date', '')
    cat = n.get('category', '资讯')
    src = n.get('source', '')
    rt = n.get('readTime', '')
    summary = n.get('summary', '')
    body = ''.join('<p>%s</p>' % p for p in n.get('content', []))
    catcls = CAT_CLASS.get(cat, '')

    jsonld = (
        '{'
        '"@context":"https://schema.org",'
        '"@type":"Article",'
        '"headline":' + json.dumps(title, ensure_ascii=False) + ','
        '"datePublished":' + json.dumps(date, ensure_ascii=False) + ','
        '"author":{"@type":"Organization","name":"佰洛生物"},'
        '"publisher":{"@type":"Organization","name":"佰洛生物","logo":{"@type":"ImageObject","url":"https://www.biologia.cn/images/ipsc-kit-front.png"}},'
        '"description":' + json.dumps(summary, ensure_ascii=False) + ','
        '"mainEntityOfPage":"https://www.biologia.cn/news/' + esc(nid) + '.html"'
        '}'
    )

    meta_bits = '<span class="nh-cat%s">%s</span>' % (catcls, esc(cat))
    if date:
        meta_bits += '<span class="nh-date">%s</span>' % esc(date)
    if src:
        meta_bits += '<span class="nh-src">来源：%s</span>' % esc(src)
    if rt:
        meta_bits += '<span class="nh-src">阅读约 %s</span>' % esc(rt)

    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__ | 佰洛生物</title>
<meta name="description" content="__SUMMARY__">
<meta name="keywords" content="佰洛生物,新闻资讯,__CAT__,iPSC,胎牛血清,BLI,细胞治疗">
<link rel="canonical" href="https://www.biologia.cn/news/__ID__.html">
<meta property="og:title" content="__TITLE__ | 佰洛生物">
<meta property="og:description" content="__SUMMARY__">
<meta property="og:image" content="https://www.biologia.cn/images/ipsc-kit-front.png">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
__JSONLD__
</script>
<style>__CSS__</style>
</head>
<body>
__NAV__
<section class="page-hero">
  <div class="inner">
    <div class="breadcrumb"><a href="news.html">新闻资讯</a> &nbsp;/&nbsp; __CAT__</div>
    <div class="nh-meta">__META__</div>
    <h1>__TITLE__</h1>
  </div>
</section>
<article class="article">
  __BODY__
  <a class="back" href="news.html">&larr; 返回资讯列表</a>
</article>
__FOOTER__
</body>
</html>
""".replace('__TITLE__', esc(title)).replace('__SUMMARY__', esc(summary)) \
        .replace('__CAT__', esc(cat)).replace('__ID__', esc(nid)) \
        .replace('__JSONLD__', jsonld).replace('__CSS__', CSS).replace('__NAV__', NAV) \
        .replace('__META__', meta_bits).replace('__BODY__', body).replace('__FOOTER__', FOOTER)


def main():
    with open(DATA, 'r', encoding='utf-8') as f:
        items = json.load(f)
    if not os.path.isdir(OUTDIR):
        os.makedirs(OUTDIR)
    for n in items:
        html = build_page(n)
        with open(os.path.join(OUTDIR, n['id'] + '.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        print('generated: news/%s.html' % n['id'])
    print('done, %d pages.' % len(items))


if __name__ == '__main__':
    main()
