"""One-off migration: WordPress/Elementor JSON -> Jekyll pages, posts, images."""
import json, re, sys, os, hashlib, urllib.request, urllib.parse
from bs4 import BeautifulSoup, Comment

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_scrape")
IMG = os.path.join(ROOT, "assets", "img")
os.makedirs(IMG, exist_ok=True)
HOST = "https://mbientlab.com"
KEEP = {"h1","h2","h3","h4","h5","h6","p","ul","ol","li","a","img","table","thead","tbody","tr","th","td",
        "strong","em","b","i","br","iframe","blockquote","figure","figcaption","hr","code","pre","video","source","div","section"}
SKIP_SLUGS = {"3669a-blog","my-account","checkout","cart","shop"}
fetched = {}

def localize(url):
    url = urllib.parse.urljoin(HOST, url).replace("://www.mbientlab.com", "://mbientlab.com")
    if not url.startswith(HOST + "/wp-content/"):
        return url
    if url in fetched:
        return fetched[url]
    name = os.path.basename(urllib.parse.urlparse(url).path)
    dest = os.path.join(IMG, name)
    if not os.path.exists(dest):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r, open(dest, "wb") as f:
                f.write(r.read())
        except Exception as e:
            print("  !! download failed", url, e, file=sys.stderr)
            fetched[url] = url
            return url
    fetched[url] = "{{ '/assets/img/%s' | relative_url }}" % name
    return fetched[url]

def clean(html):
    soup = BeautifulSoup(html, "lxml")
    for t in soup(["script","style","noscript","svg","form","input","button","select"]):
        t.decompose()
    for c in soup.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    for img in soup.find_all("img"):
        src = img.get("data-src") or img.get("data-lazy-src") or img.get("src") or ""
        if src.startswith("data:") or not src:
            img.decompose(); continue
        alt = img.get("alt", "")
        img.attrs = {"src": localize(src), "alt": alt, "loading": "lazy"}
    for a in soup.find_all("a"):
        h = a.get("href")
        a.attrs = {}
        if h:
            h = h.replace("://www.mbientlab.com", "://mbientlab.com")
            if h.startswith(HOST):
                h = h[len(HOST):] or "/"
            if h.startswith("/wp-content/"):
                h = localize(HOST + h)
            elif h.startswith("/"):
                # WooCommerce product pages and retired paths have no static equivalent
                if re.match(r"/(store|boards)/.+|^/boards$", h): h = "/store/"
                elif h.startswith("/tutorials/"): h = "/gettingstarted/"
                elif h.startswith("/software"): h = "https://docs.mbientlab.com"
                h = "{{ '%s' | relative_url }}" % h
            a["href"] = h
            txt = a.get_text(strip=True)
            if txt and len(txt) <= 24 and txt.upper() == txt and not a.find("img"):
                a["class"] = "btn btn--primary"
    for f in soup.find_all("iframe"):
        s = f.get("src") or f.get("data-src") or f.get("data-lazy-src") or ""
        f.attrs = {"src": s, "loading": "lazy", "allowfullscreen": "", "title": f.get("title","Embedded video")}
    for t in soup.find_all(True):
        if t.name in ("html","body"): continue
        if t.name not in KEEP:
            t.unwrap(); continue
        if t.name not in ("a","img","iframe"):
            t.attrs = {}
    body = soup.body
    # unwrap generic div/section wrappers so Markdown-free HTML stays flat
    for t in body.find_all(["div","section"]):
        t.unwrap()
    for t in body.find_all(["p","h1","h2","h3","h4","h5","h6","li","a","td","th"]):
        if not t.get_text(strip=True) and not t.find(["img","iframe"]):
            t.decompose()
    out = body.decode_contents()
    out = re.sub(r"\n\s*\n+", "\n\n", out).strip()
    return out

def fm(d):
    lines = ["---"]
    for k, v in d.items():
        if isinstance(v, bool): lines.append(f"{k}: {str(v).lower()}")
        elif isinstance(v, (int, float)): lines.append(f"{k}: {v}")
        elif isinstance(v, list):
            lines.append(f"{k}:"); lines += [f"  - {json.dumps(x)}" for x in v]
        else: lines.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
    lines.append("---\n")
    return "\n".join(lines)

def unesc(s):
    return BeautifulSoup(s, "lxml").get_text()

def main():
    pages = json.load(open(f"{SRC}/pages.json"))
    posts = json.load(open(f"{SRC}/posts.json"))
    os.makedirs(f"{ROOT}/_pages", exist_ok=True)
    os.makedirs(f"{ROOT}/_posts", exist_ok=True)
    for p in pages:
        if p["slug"] in SKIP_SLUGS: continue
        title = unesc(p["title"]["rendered"])
        home = p["link"].rstrip("/") == HOST
        data = {"title": title, "permalink": "/" if home else f"/{p['slug']}/", "layout": "single",
                "classes": "wide", "author_profile": False, "last_modified_at": p["modified"][:10]}
        if home: data["title"] = "Wearable Wireless 9-axis IMUs & Environmental Sensors"
        body = clean(p["content"]["rendered"])
        if home:
            data["layout"] = "splash"
        else:
            body = re.sub(r"^\s*<h1>.*?</h1>\s*", "", body, count=1, flags=re.S)
        fn = "index.html" if home else f"{p['slug']}.html"
        open(f"{ROOT}/_pages/{fn}", "w").write(fm(data) + body + "\n")
        print("page", fn, len(body))
    for p in posts:
        title = unesc(p["title"]["rendered"])
        date = p["date"][:10]
        slug = p["slug"]
        body = clean(p["content"]["rendered"])
        exc = re.sub(r"\s*READ MORE\s*$", "", unesc(p["excerpt"]["rendered"]).strip()).strip()
        m = re.fullmatch(r"<p>(https?://\S+)</p>", body)
        if m:
            body = (f"<p>{exc}</p>\n\n" if exc else "") + f'<p><a class="btn btn--primary" href="{m.group(1)}">Read the paper</a></p>'
        data = {"title": title, "date": p["date"].replace("T"," ")+" +0000", "layout": "single",
                "permalink": f"/blog/{slug}/", "author_profile": False}
        if exc: data["excerpt"] = exc[:300]
        open(f"{ROOT}/_posts/{date}-{slug}.html", "w").write(fm(data) + body + "\n")
    print("posts", len(posts), "images", len(os.listdir(IMG)))
main()
