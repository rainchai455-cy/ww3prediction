# 从 index.html 生成 README.md + assets/figN.png
# 目的：让 GitHub 仓库首页直接渲染报告内容（GitHub 会剥掉 Markdown 里的原始 HTML 与 <svg>，
# 所以图必须先栅格化；正文由本脚本从同一份 HTML 转换，不手抄数字）。
# 依赖：标准库 + 系统 ImageMagick（带 RSVG delegate）。
import html as H
import os
import re
import subprocess
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "index.html")
OUT = os.path.join(HERE, "README.md")
ASSETS = os.path.join(HERE, "assets")
MAGICK = "magick"

VOID = {"meta", "br", "img", "hr", "input", "link"}


class Node(object):
    def __init__(self, tag, attrs=None, parent=None):
        self.tag, self.attrs, self.parent = tag, dict(attrs or {}), parent
        self.kids = []

    def cls(self):
        return self.attrs.get("class", "")


class Tree(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=False)
        self.root = Node("root")
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.kids.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.kids.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n.parent and n.tag != tag:
            n = n.parent
        if n.parent:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.kids.append(data)

    # convert_charrefs=False 时实体不走 handle_data；不接住就会被静默丢掉（&gt; / &amp; 消失过）。
    def handle_entityref(self, name):
        self.cur.kids.append("&%s;" % name)

    def handle_charref(self, name):
        self.cur.kids.append("&#%s;" % name)


def walk(n):
    for k in n.kids:
        yield k
        if isinstance(k, Node):
            for g in walk(k):
                yield g


def inline(n):
    if isinstance(n, str):
        return n
    t = "".join(inline(k) for k in n.kids)
    if n.tag == "b":
        return "**" + t.strip() + "**" if t.strip() else t
    if n.tag == "code":
        return "`" + t.strip() + "`"
    if n.tag in ("sup", "sub"):
        return "<%s>%s</%s>" % (n.tag, t, n.tag)
    if n.tag == "br":
        return " / "
    return t


def text(n):
    s = "".join(inline(k) for k in n.kids) if isinstance(n, Node) else n
    s = H.unescape(s)
    s = re.sub(r"[ \t]*\n[ \t]*", " ", s)
    return s.strip()


def cells(tr):
    return [text(td).replace("|", "\\|") for td in tr.kids if isinstance(td, Node) and td.tag in ("th", "td")]


def find(n, tag, cls=None):
    out = []
    for k in n.kids:
        if isinstance(k, Node):
            if k.tag == tag and (cls is None or cls in k.cls()):
                out.append(k)
            out += find(k, tag, cls)
    return out


def md_table(tb):
    rows = [cells(tr) for tr in find(tb, "tr")]
    rows = [r for r in rows if r]
    w = max(len(r) for r in rows)
    rows = [r + [""] * (w - len(r)) for r in rows]
    head, body = rows[0], rows[1:]
    if not head:
        head = [""] * w
    for i in range(w):
        head[i] = head[i] or " "
    L = ["| " + " | ".join(head) + " |", "|" + "---|" * w]
    L += ["| " + " | ".join(r) + " |" for r in body]
    return "\n".join(L)


def md_kpi(d):
    items = [k for k in d.kids if isinstance(k, Node) and k.tag == "div"]
    L = ["| 值 | 含义 |", "|---|---|"]
    for it in items:
        v = find(it, "b")
        s = find(it, "span")
        L.append("| **%s** | %s |" % (text(v[0]) if v else "", text(s[0]) if s else ""))
    return "\n".join(L)


BLOCKY = ("div", "section", "header", "body")
HASBLOCK = BLOCKY + ("table", "ul", "ol", "h1", "h2", "p", "svg")


def has_block(k):
    return any(isinstance(x, Node) and x.tag in HASBLOCK for x in k.kids)


def quote(body):
    return "> " + body.replace("\n", "\n> ")


def render(n):
    out, pend = [], None
    for k in n.kids:
        if isinstance(k, str):
            s = H.unescape(re.sub(r"\s+", " ", k)).strip()
            if s:
                out.append(s)
            continue
        c, t = k.cls(), k.tag
        if t == "span" and "tag" in c:
            pend = text(k)
            continue
        if t == "b" and "tt" in c:
            out.append("### " + text(k))
        elif t == "h1":
            out.append("# " + text(k))
        elif t == "h2":
            out.append("## " + (("%s ｜ " % pend) if pend else "") + text(k))
            pend = None
        elif t == "table":
            out.append(md_table(k))
        elif t == "div" and "kpi" in c:
            out.append(md_kpi(k))
        elif t in ("ul", "ol"):
            items = []
            for i, li in enumerate([x for x in k.kids if isinstance(x, Node) and x.tag == "li"], 1):
                items.append(("%d. " % i if t == "ol" else "- ") + text(li))
            out.append("\n".join(items))
        elif t in BLOCKY or t == "p":
            if "note" in c or "alert" in c or "stop" in c:
                body = "\n\n".join(render(k)) if has_block(k) else text(k)
                if body.strip():
                    out.append(quote(body))
            elif has_block(k):
                # 结构性容器要摊平，否则整篇文档会被并成一个 block，前置说明就掉到文末。
                out.extend([b for b in render(k) if b.strip()])
            elif text(k).strip():
                out.append(text(k))
        elif text(k).strip():
            out.append(text(k))
    return out


def main():
    src = open(SRC, encoding="utf-8").read()
    svgs = re.findall(r"<svg.*?</svg>", src, re.S)
    if not os.path.isdir(ASSETS):
        os.makedirs(ASSETS)
    for i, s in enumerate(svgs, 1):
        w, h = re.search(r'viewBox="0 0 (\d+) (\d+)"', s).groups()
        fixed = s.replace('width="100%"', 'width="%s" height="%s"' % (w, h), 1)
        base = os.path.join(ASSETS, "fig%d" % i)
        open(base + ".svg", "w", encoding="utf-8").write(fixed)
        subprocess.run([MAGICK, "-density", "144", base + ".svg", base + ".png"], check=True)
    tok = src
    for i in range(len(svgs)):
        tok = re.sub(r"<svg.*?</svg>", "\x00FIGTOK%d\x00" % (i + 1), tok, count=1, flags=re.S)

    tree = Tree()
    tree.feed(tok)
    tree.close()
    body = find(tree.root, "body")[0]
    blocks = [b for b in render(body) if b.strip()]

    if blocks and blocks[0].startswith("# "):
        title, rest = blocks[0], blocks[1:]
    else:
        title, rest = "# WW3 五年风险模型", blocks
    pre = [
        title,
        "",
        "> **本仓库是「报告 + 可复现依赖」的快照，不是模型实现**：`label_status` 三态（P0）未实现，下面任何数字都未经历史校准。定稿快照直链：<https://rainchai455-cy.github.io/ww3prediction/ww3_final_simulation_report_2026-10-15.html>",
        "> **本文件由 `_readme_build.py` 从同目录 `index.html` 机械转换生成**（图经 ImageMagick/RSVG 栅格化为 `assets/figN.png`）。",
        "> 不要手改正文数字：改 `_report_build.py` → 重建 `index.html` → 重跑本脚本；逐文件哈希与复现命令见 `MANIFEST.md`。",
        "> 同一份内容的网页版：<https://rainchai455-cy.github.io/ww3prediction/>",
    ]
    md = "\n\n".join(pre + rest)
    md = re.sub(r"\x00FIGTOK(\d+)\x00", lambda m: "![图 %s](assets/fig%s.png)" % (m.group(1), m.group(1)), md)
    md = re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"
    open(OUT, "w", encoding="utf-8", newline="\n").write(md)
    png = sum(os.path.getsize(os.path.join(ASSETS, f)) for f in os.listdir(ASSETS) if f.endswith(".png"))
    print("WROTE README.md %d bytes  figs=%d  png_total=%d bytes" % (os.path.getsize(OUT), len(svgs), png))


if __name__ == "__main__":
    main()
