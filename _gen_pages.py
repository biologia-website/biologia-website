# -*- coding: utf-8 -*-
"""佰洛生物 ① GitHub Pages 站：批量生成产品/服务独立静态页 + sitemap.xml
读取 data/products.json、data/services.json，输出：
  products/{id}.html  (15)
  services/{slug}.html (6)
  sitemap.xml
所有页面含 JSON-LD(Product/Service + ImageObject + Breadcrumb) + canonical + OG/Twitter。
"""
import os, json, html

REPO = os.path.dirname(os.path.abspath(__file__))
SITE = "https://www.biologia.cn"
DATA = os.path.join(REPO, "data")
PROD = json.load(open(os.path.join(DATA, "products.json"), encoding="utf-8"))
SERV = json.load(open(os.path.join(DATA, "services.json"), encoding="utf-8"))

# 服务 id -> 干净 URL slug（与 ② 保持一致，利于已有索引延续）
SVC_SLUG = {
    "svc-ipsc": "ipsc-reprogramming",
    "svc-bli": "bli-affinity",
    "svc-virus": "virus-packaging",
    "svc-antibody": "antibody-custom",
    "svc-crispr": "crispr-editing",
    "svc-cart": "cart-vector",
}
CAT_CN = {"reagents": "试剂与耗材", "instruments": "实验仪器"}
SC_CN = {"s1": "干细胞", "s2": "生物物理", "s3": "病毒载体", "s4": "抗体", "s5": "基因编辑", "s6": "细胞治疗"}

def e(s):
    return html.escape(str(s), quote=True)

def brand_of(detail):
    for sp in detail.get("specs", []):
        k = sp.get("key", "")
        if "品牌" in k or "厂商" in k:
            return sp.get("val", "")
    return "佰洛生物"

def gallery_html(images):
    if not images:
        return ""
    slides = []
    for i, im in enumerate(images):
        src = e(im["src"])
        cap = e(im.get("caption", ""))
        cls = "gallery-slide" + ("" if i == 0 else "")
        slides.append(f'<figure class="gallery-slide"><img src="{src}" alt="{cap}" loading="{"eager" if i==0 else "lazy"}"><figcaption>{cap}</figcaption></figure>')
    dots = "".join(f'<button class="gallery-dot{" active" if i==0 else ""}" data-i="{i}" aria-label="图{i+1}"></button>' for i in range(len(images)))
    nav = ""
    if len(images) > 1:
        nav = '<button class="gallery-nav prev" aria-label="上一张">‹</button><button class="gallery-nav next" aria-label="下一张">›</button>'
    return f'''
    <section class="section-card">
      <h2>产品图片</h2>
      <div class="gallery-carousel" id="gallery">
        <div class="gallery-track">{''.join(slides)}</div>
        {nav}
        <div class="gallery-dots">{dots}</div>
      </div>
    </section>
    <script>
    (function(){{
      var g=document.getElementById('gallery'); if(!g) return;
      var track=g.querySelector('.gallery-track'); var dots=g.querySelectorAll('.gallery-dot');
      var idx=0; var n={len(images)};
      function go(i){{ idx=(i+n)%n; track.style.transform='translateX(-'+(idx*100)+'%)'; dots.forEach(function(d,k){{d.classList.toggle('active',k===idx);}}); }}
      g.querySelectorAll('.gallery-nav').forEach(function(b){{ b.onclick=function(){{ go(idx+(b.classList.contains('next')?1:-1)); }}; }});
      dots.forEach(function(d,k){{ d.onclick=function(){{ go(k); }}; }});
    }})();
    </script>'''

def product_jsonld(p):
    d = p.get("detail", {})
    imgs = d.get("images", [])
    img_urls = [SITE + "/" + im["src"] for im in imgs]
    ld = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": p["name"],
        "description": d.get("intro", p.get("summary", ""))[:200],
        "brand": {"@type": "Brand", "name": brand_of(d)},
        "category": CAT_CN.get(p.get("cat"), ""),
        "offers": {
            "@type": "Offer",
            "priceCurrency": "CNY",
            "availability": "https://schema.org/InStock",
            "url": SITE + "/products/" + p["id"] + ".html",
            "seller": {"@type": "Organization", "name": "佰洛生物"}
        }
    }
    if img_urls:
        ld["image"] = img_urls
    bc = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "首页", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "产品中心", "item": SITE + "/products.html"},
            {"@type": "ListItem", "position": 3, "name": p["name"], "item": SITE + "/products/" + p["id"] + ".html"}
        ]
    }
    return [ld, bc]

def service_jsonld(s):
    d = s.get("detail", {})
    ld = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": s["name"],
        "description": d.get("intro", s.get("summary", ""))[:200],
        "provider": {"@type": "Organization", "name": "佰洛生物", "url": SITE + "/"},
        "areaServed": "CN"
    }
    bc = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "首页", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "技术服务", "item": SITE + "/index.html#services"},
            {"@type": "ListItem", "position": 3, "name": s["name"], "item": SITE + "/services/" + SVC_SLUG.get(s["id"], s["id"]) + ".html"}
        ]
    }
    return [ld, bc]

def page_shell(title, desc, canonical, jsonld_list, body, css_extra=""):
    ld = "\n".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>" for x in jsonld_list)
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(canonical)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{e(canonical)}">
<meta property="og:site_name" content="佰洛生物">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
{ld}
<style>
:root{{--blue:#0a5c8a;--blue2:#064368;--accent:#00a896;}}
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;color:#1f2d3d;line-height:1.7;background:#f6f8fa;}}
a{{color:var(--blue);text-decoration:none;}}
header{{background:linear-gradient(135deg,var(--blue),var(--blue2));color:#fff;padding:14px 20px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;}}
header .logo{{font-weight:700;font-size:18px;}}
header nav a{{color:#dbeafe;margin-left:16px;font-size:14px;}}
.wrap{{max-width:1100px;margin:0 auto;padding:0 18px 60px;}}
/* 面包屑 */
.breadcrumb{{padding:14px 0;font-size:13px;color:#8a97a5;}}
.breadcrumb a{{color:var(--blue);}}
/* 深色 Hero 横幅（含内联CTA） */
.product-hero{{background:linear-gradient(135deg,#0a5c8a 0%,#064368 100%);color:#fff;padding:44px 0 38px;}}
.ph-inner{{display:flex;gap:32px;align-items:flex-start;}}
.ph-icon{{width:72px;height:72px;border-radius:16px;background:rgba(255,255,255,.15);display:flex;align-items:center;justify-content:center;font-size:34px;flex-shrink:0;}}
.ph-info{{flex:1;}}
.ph-cat{{display:inline-block;background:rgba(255,255,255,.18);font-size:12px;padding:3px 10px;border-radius:20px;margin-bottom:10px;}}
.ph-info h1{{font-size:28px;margin-bottom:8px;}}
.ph-summary{{opacity:.9;font-size:15px;max-width:600px;line-height:1.7;}}
.ph-cta{{margin-top:18px;display:flex;gap:10px;flex-wrap:wrap;}}
.btn{{display:inline-flex;align-items:center;gap:6px;padding:11px 24px;border-radius:8px;font-size:15px;font-weight:600;transition:transform .15s,box-shadow .15s;cursor:pointer;border:none;}}
.btn-primary{{background:#fff;color:var(--blue);}}
.btn-primary:hover{{transform:translateY(-1px);box-shadow:0 4px 12px rgba(0,0,0,.2);}}
.btn-outline{{background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.55);}}
.btn-outline:hover{{border-color:#fff;}}
/* 左右内容网格 */
.content-grid{{display:grid;grid-template-columns:1fr 340px;gap:28px;padding-top:28px;}}
@media(max-width:860px){{.content-grid{{grid-template-columns:1fr;}}.ph-inner{{flex-direction:column;gap:16px;}}}}
.section-card{{background:#fff;border-radius:14px;padding:24px;margin-bottom:18px;box-shadow:0 2px 12px rgba(0,0,0,.05);}}
.section-card h2{{font-size:18px;margin-bottom:14px;color:var(--blue2);border-left:4px solid var(--blue);padding-left:10px;}}
.intro-text{{color:#333;font-size:15px;line-height:1.85;}}
.intro-text strong{{color:#1f2d3d;}}
.feature-list{{padding-left:20px;}}
.feature-list li{{margin:6px 0;}}
.spec-table{{width:100%;border-collapse:collapse;}}
.spec-table td{{padding:10px 14px;border-bottom:1px solid #eef1f4;font-size:14px;}}
.spec-table td:first-child{{color:#6b7785;width:38%;background:#fafbfc;}}
.app-text{{color:#333;font-size:14px;line-height:1.8;}}
/* 右侧栏 */
.sidebar-card{{background:#fff;border-radius:14px;padding:22px;margin-bottom:18px;box-shadow:0 2px 12px rgba(0,0,0,.05);}}
.sidebar-card h3{{font-size:15px;color:var(--blue2);margin-bottom:12px;}}
.info-row{{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #f0f5fa;font-size:13px;}}
.info-row:last-child{{border-bottom:none;}}
.info-label{{color:#6b7785;}}
.info-value{{color:#1f2d3d;font-weight:600;}}
.cta-card{{background:linear-gradient(135deg,var(--blue),var(--accent));color:#fff;border-radius:14px;padding:28px;text-align:center;}}
.cta-card h3{{font-size:18px;margin-bottom:8px;}}
.cta-card p{{font-size:13px;opacity:.85;margin-bottom:18px;}}
.cta-card .btn{{background:#fff;color:var(--blue);width:100%;justify-content:center;}}
/* 图集 */
.gallery-carousel{{position:relative;max-width:100%;overflow:hidden;}}
.gallery-track{{display:flex;transition:transform .35s ease;}}
.gallery-slide{{min-width:100%;}}
.gallery-slide img{{width:100%;max-height:420px;object-fit:contain;background:#fff;border-radius:10px;}}
.gallery-slide figcaption{{text-align:center;font-size:13px;color:#6b7785;margin-top:8px;}}
.gallery-nav{{position:absolute;top:45%;transform:translateY(-50%);background:rgba(0,0,0,.4);color:#fff;border:none;font-size:22px;width:38px;height:38px;border-radius:50%;cursor:pointer;}}
.gallery-nav.prev{{left:8px;}}.gallery-nav.next{{right:8px;}}
.gallery-dots{{text-align:center;margin-top:10px;}}
.gallery-dot{{width:9px;height:9px;border-radius:50%;border:none;background:#cbd5e1;margin:0 4px;cursor:pointer;}}
.gallery-dot.active{{background:var(--blue);}}
.related{{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px;}}
.related a{{background:#fff;border-radius:10px;padding:14px;box-shadow:0 2px 8px rgba(0,0,0,.05);font-size:14px;}}
footer{{text-align:center;color:#8a97a5;font-size:13px;padding:30px;}}
{css_extra}
</style>
</head>
<body>
<header>
  <span class="logo">佰洛生物 BioLia</span>
  <nav><a href="{SITE}/">首页</a><a href="{SITE}/products.html">产品中心</a><a href="{SITE}/index.html#services">技术服务</a><a href="{SITE}/faq.html">常见问题</a><a href="{SITE}/contact.html">联系我们</a></nav>
</header>
<div class="wrap">
{body}
</div>
<footer>© 2026 佰洛生物（BioLia） · 干细胞 / iPSC / 细胞培养产品与技术服务 · service@biologia.cn</footer>
</body>
</html>'''

def build_product(p):
    d = p.get("detail", {})
    cat = CAT_CN.get(p.get("cat"), "")
    rel = [x for x in PROD if x["id"] != p["id"] and x.get("cat") == p.get("cat")]
    rel = (rel + [x for x in PROD if x["id"] != p["id"]])[:4]
    rel_html = "".join(f'<a href="{SITE}/products/{x["id"]}.html">{e(x["name"])}</a>' for x in rel)
    features = "".join(f"<li>{e(f)}</li>" for f in d.get("features", []))
    specs = "".join(f'<tr><td>{e(s["key"])}</td><td>{e(s["val"])}</td></tr>' for s in d.get("specs", []))
    # 产品图标 emoji 映射（按关键词模糊匹配）
    name_lower = p["name"].lower()
    intro_text = d.get("intro", "")
    if "ipsc" in name_lower or "重编程" in p["name"]: icon = "🧬"
    elif "fbs" in name_lower or "血清" in p["name"]: icon = "🩸"
    elif "培养基" in p["name"] or "media" in name_lower: icon = "🧪"
    elif "抗体" in p["name"] or "ab" in name_lower or "流式" in p["name"]: icon = "🔬"
    elif "染料" in p["name"] or "dye" in name_lower: icon = "🎨"
    elif "因子" in name_lower or "growth" in name_lower: icon = "💉"
    elif "酶" in p["name"] or "enzyme" in name_lower: icon = "⚗️"
    elif "载体" in name_lower or "vector" in name_lower or "cart" in name_lower: icon = "🔷"
    elif "病毒" in name_lower or "virus" in name_lower or "包装" in p["name"]: icon = "🦠"
    else: icon = "📦"

    # 订购信息行
    ord_parts = d.get("ordering", "").split("|")
    ord_rows = ""
    for part in ord_parts:
        part = part.strip()
        if not part: continue
        if "：" in part: label, val = part.split("：", 1)
        elif ":" in part: label, val = part.split(":", 1)
        else: label, val = part, ""
        ord_rows += f'<div class="info-row"><span class="info-label">{e(label)}</span><span class="info-value">{e(val)}</span></div>'

    body = f'''
<!-- 面包屑 -->
<div class="wrap">
<div class="breadcrumb"><a href="{SITE}/">首页</a><span>›</span><a href="{SITE}/products.html">产品中心</a><span>›</span>{e(p["name"])}</div>
</div>

<!-- Hero 横幅 -->
<section class="product-hero">
  <div class="wrap ph-inner">
    <div class="ph-icon">{icon}</div>
    <div class="ph-info">
      <div class="ph-cat">{e(cat)}</div>
      <h1>{e(p["name"])}</h1>
      <p class="ph-summary">{e(p.get("summary",""))}</p>
      <div class="ph-cta">
        <a href="{SITE}/contact.html" class="btn btn-primary">📞 获取报价</a>
        <a href="{SITE}/contact.html" class="btn btn-outline">📧 技术咨询</a>
      </div>
    </div>
  </div>
</section>

<!-- 左右内容 -->
<div class="wrap">
<div class="content-grid">
  <div class="content-main">
    <section class="section-card"><h2>产品概述</h2><div class="intro-text">{e(intro_text)}</div></section>
    {gallery_html(d.get("images", []))}
    <section class="section-card"><h2>产品特点</h2><ul class="feature-list">{features}</ul></section>
    <section class="section-card"><h2>技术规格</h2><table class="spec-table">{specs}</table></section>
    <section class="section-card"><h2>应用领域</h2><div class="app-text">{e(d.get("applications",""))}</div></section>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card"><h3>订购信息</h3>{ord_rows}</div>
    <div class="cta-card"><h3>询价 / 订购</h3><p>佰洛生物为您提供专业技术支持与报价</p><a href="{SITE}/contact.html" class="btn">联系我们</a></div>
  </aside>
</div>
<section class="section-card"><h2>相关产品</h2><div class="related">{rel_html}</div></section>
</div>
'''
    return page_shell(
        p["name"] + " | 佰洛生物",
        p.get("summary", ""),
        SITE + "/products/" + p["id"] + ".html",
        product_jsonld(p),
        body
    )

def build_service(s):
    d = s.get("detail", {})
    rel = [x for x in SERV if x["id"] != s["id"]][:4]
    rel_html = "".join(f'<a href="{SITE}/services/{SVC_SLUG.get(x["id"],x["id"])}.html">{e(x["name"])}</a>' for x in rel)
    features = "".join(f"<li>{e(f)}</li>" for f in d.get("features", []))
    specs = "".join(f'<tr><td>{e(sp["key"])}</td><td>{e(sp["val"])}</td></tr>' for sp in d.get("specs", []))
    flow = e(d.get("flow", ""))
    delivers = e(d.get("deliverables", ""))
    # 服务图标 emoji
    sid = s["id"]
    if "ipsc" in sid: svc_icon = "🧬"
    elif "bli" in sid: svc_icon = "🔬"
    elif "virus" in sid: svc_icon = "🦠"
    elif "antibody" in sid: svc_icon = "💉"
    elif "crispr" in sid: svc_icon = "⚗️"
    elif "cart" in sid: svc_icon = "🔷"
    else: svc_icon = "⚙️"

    body = f'''
<!-- 面包屑 -->
<div class="wrap">
<div class="breadcrumb"><a href="{SITE}/">首页</a><span>›</span><a href="{SITE}/index.html#services">技术服务</a><span>›</span>{e(s["name"])}</div>
</div>

<!-- Hero 横幅 -->
<section class="product-hero">
  <div class="wrap ph-inner">
    <div class="ph-icon">{svc_icon}</div>
    <div class="ph-info">
      <div class="ph-cat">{e(SC_CN.get(s.get("sc"),""))} · {e(s.get("tag",""))}</div>
      <h1>{e(s["name"])}</h1>
      <p class="ph-summary">{e(s.get("summary",""))}</p>
      <div class="ph-cta">
        <a href="{SITE}/contact.html" class="btn btn-primary">📞 咨询报价</a>
        <a href="{SITE}/contact.html" class="btn btn-outline">📧 技术交流</a>
      </div>
    </div>
  </div>
</section>

<!-- 左右内容 -->
<div class="wrap">
<div class="content-grid">
  <div class="content-main">
    <section class="section-card"><h2>服务介绍</h2><div class="intro-text">{d.get("intro","").strip()}</div></section>
    <section class="section-card"><h2>服务流程</h2><div class="app-text">{flow}</div></section>
    <section class="section-card"><h2>服务特点</h2><ul class="feature-list">{features}</ul></section>
    <section class="section-card"><h2>技术参数</h2><table class="spec-table">{specs}</table></section>
    <section class="section-card"><h2>交付物</h2><div class="app-text">{delivers}</div></section>
  </div>
  <aside class="sidebar">
    <div class="cta-card"><h3>咨询该服务</h3><p>佰洛生物技术团队为您提供定制方案</p><a href="{SITE}/contact.html" class="btn">联系我们</a></div>
  </aside>
</div>
<section class="section-card"><h2>相关服务</h2><div class="related">{rel_html}</div></section>
</div>
'''
    return page_shell(
        s["name"] + " | 佰洛生物技术服务",
        s.get("summary", ""),
        SITE + "/services/" + SVC_SLUG.get(s["id"], s["id"]) + ".html",
        service_jsonld(s),
        body
    )

def build_sitemap():
    urls = []
    def add(loc, pri, freq, imgs=None):
        img_xml = ""
        if imgs:
            for im in imgs:
                img_xml += (f'    <image:image><image:loc>{SITE}/{im["src"]}</image:loc>'
                            f'<image:caption>{e(im.get("caption",""))}</image:caption></image:image>\n')
        urls.append(f'''  <url>
    <loc>{loc}</loc>
    <lastmod>2026-07-14</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{pri}</priority>
{img_xml}  </url>''')
    add(SITE + "/", "1.0", "weekly")
    add(SITE + "/products.html", "0.9", "weekly")
    add(SITE + "/contact.html", "0.7", "monthly")
    add(SITE + "/faq.html", "0.7", "monthly")
    for p in PROD:
        imgs = p.get("detail", {}).get("images", [])
        add(SITE + "/products/" + p["id"] + ".html", "0.8", "monthly", imgs)
    for s in SERV:
        add(SITE + "/services/" + SVC_SLUG.get(s["id"], s["id"]) + ".html", "0.8", "monthly")
    return '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
''' + "\n".join(urls) + "\n</urlset>\n"

def main():
    pdir = os.path.join(REPO, "products")
    sdir = os.path.join(REPO, "services")
    os.makedirs(pdir, exist_ok=True)
    os.makedirs(sdir, exist_ok=True)
    for p in PROD:
        open(os.path.join(pdir, p["id"] + ".html"), "w", encoding="utf-8").write(build_product(p))
    for s in SERV:
        slug = SVC_SLUG.get(s["id"], s["id"])
        open(os.path.join(sdir, slug + ".html"), "w", encoding="utf-8").write(build_service(s))
    open(os.path.join(REPO, "sitemap.xml"), "w", encoding="utf-8").write(build_sitemap())
    print("Generated:", len(PROD), "product pages,", len(SERV), "service pages, sitemap.xml")

if __name__ == "__main__":
    main()
