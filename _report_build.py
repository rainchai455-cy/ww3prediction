import json, math, html, os, time, csv
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "_report_data.json"), encoding="utf-8"))
SC = D["scenarios"]; HZ = D["horizon"]; L12 = D["p12"]; L21 = D["p21"]; LR = D["rho"]; SD = D["seeds"]
FONT = "'Microsoft YaHei','Segoe UI',system-ui,sans-serif"
INK = "#1f2430"; MUT = "#68707f"; GRID = "#dfe4ec"
C1, C2, C3, CAUT = "#2f6fb2", "#3f9d78", "#d08b1f", "#b4433a"

def pct(x, nd=3):
    return ("%." + str(nd) + "f%%") % (100 * x)

def pfmt(x):
    """自适应小数位：概率跨 4 个数量级时固定小数位会把小值显示成 0.000%。"""
    v = 100 * x
    if v == 0:
        return "0"
    nd = 4 if v < 0.1 else 3 if v < 10 else 2
    return "%.*f%%" % (nd, v)

def nice_log(vmin, vmax):
    lo = 10 ** math.floor(math.log10(max(vmin, 1e-7))); hi = 10 ** math.ceil(math.log10(vmax))
    ts = []
    e = lo
    while e <= hi * 1.0000001:
        ts.append(e); e *= 10
    if len(ts) < 4:
        ts = []
        e = lo
        while e <= hi * 1.0000001:
            for m in (1, 3):
                if e * m <= hi * 1.0000001: ts.append(e * m)
            e *= 10
        ts = sorted(set(ts))
    return ts

def svg_log_bars(items, w=1090, h=330, pad_l=252, pad_r=24, pad_t=26, pad_b=64, unit="%",
                 axlab="对数轴（五年累计概率，单位 %）"):
    """items: [(label, value, lo, hi, color, note)]"""
    vals = [v for _, v, _, _, _, _ in items] + [x for _, _, x, _, _, _ in items if x] + \
            [y for _, _, _, y, _, _ in items if y]
    vmin, vmax = min(v for v in vals if v > 0), max(vals)
    if vals[0] == 0 or any(v == 0 for _, v, _, _, _, _ in items):
        vmin = vmin / 10
    tmin, tmax = math.log10(vmin) - 0.35, math.log10(vmax) + 0.25
    X = lambda v: pad_l + (math.log10(v) - tmin) / (tmax - tmin) * (w - pad_l - pad_r)
    n = len(items); rowh = (h - pad_t - pad_b) / n
    s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="100%%" font-family="%s">' % (w, h, FONT)]
    s.append('<rect x="0" y="0" width="%d" height="%d" fill="#fff"/>' % (w, h))
    ticks = nice_log(10 ** tmin, 10 ** tmax)
    for t in ticks:
        x = X(t)
        if x < pad_l + 14 or x > w - pad_r:
            continue
        s.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s"/>' % (x, pad_t, x, h - pad_b, GRID))
        v = t * 100
        lab = ("%g" % v) if v >= 0.01 else ("%.3g" % v)
        s.append('<text x="%.1f" y="%d" font-size="12" fill="%s" text-anchor="middle">%s%s</text>' % (x, h - pad_b + 18, MUT, lab, unit))
    for i, (lab, v, lo, hi, col, note) in enumerate(items):
        y = pad_t + i * rowh + rowh * 0.18; bh = rowh * 0.5
        s.append('<text x="%d" y="%.1f" font-size="13.5" fill="%s" text-anchor="end">%s</text>' % (pad_l - 10, y + bh * 0.66, INK, html.escape(lab)))
        if v > 0:
            s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" rx="2"/>' % (pad_l, y, X(v) - pad_l, bh, col))
        if hi:
            s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.6"/>' %
                     (X(max(lo, 10 ** tmin)), y + bh / 2, X(hi), y + bh / 2, INK))
            for xx in (X(max(lo, 10 ** tmin)), X(hi)):
                s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.6"/>' % (xx, y + 2, xx, y + bh - 2, INK))
        txt = pfmt(v)
        s.append('<text x="%.1f" y="%.1f" font-size="13" font-weight="600" fill="%s">%s</text>' %
                 (X(hi if hi else max(v, 10 ** tmin)) + 8, y + bh * 0.66, INK, txt))
        if note:
            s.append('<text x="%.1f" y="%.1f" font-size="11.5" fill="%s">%s</text>' % (pad_l + 4, y + bh + 13, MUT, html.escape(note)))
    s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s"/>' % (pad_l, h - pad_b, w - pad_r, h - pad_b, MUT))
    s.append('<text x="%d" y="%d" font-size="11.5" fill="%s">%s</text>' % (pad_l, h - 8, MUT, html.escape(axlab)))
    s.append('</svg>')
    return "".join(s)

def svg_line(xs, ys, lo, hi, w=1090, h=300, pad_l=92, pad_r=24, pad_t=22, pad_b=48, xlab="预测窗口（月）"):
    ymax = max(hi) * 1.25
    X = lambda i: pad_l + i * (w - pad_l - pad_r) / (len(xs) - 1)
    Y = lambda v: h - pad_b - v / ymax * (h - pad_t - pad_b)
    s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="100%%" font-family="%s">' % (w, h, FONT)]
    s.append('<rect width="%d" height="%d" fill="#fff"/>' % (w, h))
    for k in range(5):
        v = ymax * k / 4; y = Y(v)
        s.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s"/>' % (pad_l, y, w - pad_r, y, GRID))
        s.append('<text x="%d" y="%.1f" font-size="12" fill="%s" text-anchor="end">%s</text>' % (pad_l - 8, y + 4, MUT, ("%.2g%%" % (100 * v))))
    band = "M " + " L ".join("%.1f %.1f" % (X(i), Y(hi[i])) for i in range(len(xs))) + " " + \
           "L ".join("%.1f %.1f" % (X(i), Y(lo[i])) for i in range(len(xs) - 1, -1, -1)) + " Z"
    s.append('<path d="%s" fill="%s" opacity="0.16"/>' % (band, C1))
    s.append('<polyline fill="none" stroke="%s" stroke-width="2.4" points="%s"/>' % (C1, " ".join("%.1f,%.1f" % (X(i), Y(ys[i])) for i in range(len(xs)))))
    for i, x in enumerate(xs):
        s.append('<circle cx="%.1f" cy="%.1f" r="3.4" fill="%s"/>' % (X(i), Y(ys[i]), C1))
        s.append('<text x="%.1f" y="%d" font-size="12" fill="%s" text-anchor="middle">%d</text>' % (X(i), h - pad_b + 20, INK, x))
        s.append('<text x="%.1f" y="%.1f" font-size="11.5" font-weight="600" fill="%s" text-anchor="middle">%s</text>' %
                 (X(i), Y(hi[i]) - 8, INK, pct(ys[i], 4)))
    s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s"/>' % (pad_l, h - pad_b, w - pad_r, h - pad_b, MUT))
    s.append('<text x="%d" y="%d" font-size="11.5" fill="%s">%s ｜ 阴影=Wilson 95%% 区间</text>' % (pad_l, h - 8, MUT, xlab))
    s.append('</svg>')
    return "".join(s)

def svg_matrix(rows, cols, cells, w=1090, h=None, cellw=150, cellh=42, pad_l=300, pad_t=54):
    h = h or (pad_t + cellh * len(rows) + 58)
    s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="100%%" font-family="%s">' % (w, h, FONT)]
    s.append('<rect width="%d" height="%d" fill="#fff"/>' % (w, h))
    for j, c in enumerate(cols):
        s.append('<text x="%.1f" y="%d" font-size="12.5" font-weight="600" fill="%s" text-anchor="middle">%s</text>' %
                 (pad_l + cellw * j + cellw / 2, pad_t - 12, INK, html.escape(c)))
    for i, r in enumerate(rows):
        s.append('<text x="%d" y="%.1f" font-size="12.5" fill="%s" text-anchor="end">%s</text>' % (pad_l - 14, pad_t + cellh * i + cellh / 2 + 5, INK, html.escape(r)))
        for j in range(len(cols)):
            state, txt = cells[(i, j)]
            fill = {"pass": "#d8ecdf", "partial": "#f6e6c8", "fail": "#f4d9d6", "na": "#eef1f6"}[state]
            ink = {"pass": "#1d6b3c", "partial": "#8a5a10", "fail": "#8f2b22", "na": MUT}[state]
            s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="#fff" rx="3"/>' %
                     (pad_l + cellw * j, pad_t + cellh * i + 4, cellw - 8, cellh - 8, fill))
            s.append('<text x="%.1f" y="%.1f" font-size="11.5" fill="%s" text-anchor="middle">%s</text>' %
                     (pad_l + cellw * j + (cellw - 8) / 2, pad_t + cellh * i + cellh / 2 + 5, ink, html.escape(txt)))
    leg = [("pass", "通过"), ("partial", "部分通过"), ("fail", "不通过"), ("na", "不适用/无该字段")]
    x = pad_l
    for st, lab in leg:
        s.append('<rect x="%d" y="%d" width="16" height="12" fill="%s" rx="2"/>' % (x, h - 30, {"pass": "#d8ecdf", "partial": "#f6e6c8", "fail": "#f4d9d6", "na": "#eef1f6"}[st]))
        s.append('<text x="%d" y="%d" font-size="12" fill="%s">%s</text>' % (x + 22, h - 20, MUT, lab))
        x += 118
    s.append('</svg>')
    return "".join(s)

def svg_tornado(items, w=1090, h=None, pad_l=300, pad_r=48, pad_t=44, rowh=44):
    """items: [(label, mult_low, mult_high, color)]，对数横轴，基准竖线 = 1×（支持 <1 的反向条）"""
    h = h or (pad_t + rowh * len(items) + 54)
    vals = [v for _, a, b, _ in items for v in (a, b)]
    lo_lim = 10 ** math.floor(math.log10(min(vals)))
    hi_lim = 10 ** math.ceil(math.log10(max(vals)))
    plotw = w - pad_l - pad_r
    X = lambda v: pad_l + (math.log10(v) - math.log10(lo_lim)) / (math.log10(hi_lim) - math.log10(lo_lim)) * plotw
    s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="100%%" font-family="%s">' % (w, h, FONT)]
    s.append('<rect width="%d" height="%d" fill="#fff"/>' % (w, h))
    t = lo_lim
    while t <= hi_lim * 1.000001:
        for m in (1, 3):
            v = t * m
            if lo_lim <= v <= hi_lim and X(v) >= pad_l - 1:
                x = X(v)
                s.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s"/>' % (x, pad_t - 10, x, h - 42, "#c9d2e0"))
                s.append('<text x="%.1f" y="%d" font-size="11.5" fill="%s" text-anchor="middle">%s</text>' % (x, h - 28, MUT, ("基准 1×" if abs(v - 1) < 1e-9 else ("×%g" % v))))
        t *= 10
    s.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1.4"/>' % (X(1), pad_t - 12, X(1), h - 40, INK))
    for i, (lab, a, b, col) in enumerate(items):
        y = pad_t + rowh * i + 8
        lo_v, hi_v = min(a, b), max(a, b)
        s.append('<text x="%d" y="%.1f" font-size="12.5" fill="%s" text-anchor="end">%s</text>' % (pad_l - 14, y + 14, INK, html.escape(lab)))
        xb = X(1.0)
        if hi_v <= 1.0000001:
            # 纯压低：条从 lo_v 画到基准线，标签放左端
            s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="20" fill="%s" rx="2"/>' %
                     (X(lo_v), y, max(3.0, xb - X(lo_v)), col))
            s.append('<text x="%.1f" y="%.1f" font-size="12" font-weight="600" fill="%s" text-anchor="end">%s</text>' %
                     (X(lo_v) - 8, y + 15, INK, "×%.3f" % lo_v))
        else:
            s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="20" fill="%s" rx="2"/>' %
                     (min(X(lo_v), xb), y, max(3.0, X(hi_v) - xb), col))
            s.append('<text x="%.1f" y="%.1f" font-size="12" font-weight="600" fill="%s" text-anchor="start">%.2f×</text>' %
                     (X(hi_v) + 8, y + 15, INK, hi_v))
    s.append('<text x="%d" y="%d" font-size="11.5" fill="%s">对数横轴：相对中间先验基准的倍数（同一批 n=10^6、同种子；&lt;1 表示压低概率）</text>' % (pad_l, h - 8, MUT))
    s.append('</svg>')
    return "".join(s)

def card(title, sub, body, tag=None, tagc=C1):
    t = ('<span class="tag" style="background:%s">%s</span>' % (tagc, html.escape(tag))) if tag else ""
    return '<section class="card">%s<h2>%s</h2><p class="sub">%s</p>%s</section>' % (t, title, sub, body)

base = SC["middle"]
mid_p, mid_lo, mid_hi = base["p"], base["lo"], base["hi"]
ceiling = 1 - math.exp(-5 * math.log(20) / 80)
ceiling_fold = 1 - math.exp(-5 * math.log(20) / 3518)
ceiling_3012 = 1 - math.exp(-5 * math.log(20) / 3012)
p12_by = {round(x["factor"], 3): x for x in L12}
r3 = p12_by[3.0]["p"] / p12_by[1.0]["p"]
r3_lo = p12_by[0.333]["p"] / p12_by[1.0]["p"]
elast = math.log(p12_by[3.0]["p"] / p12_by[1.0]["p"]) / math.log(3)
p21_by = {x["p21"]: x for x in L21}
# 方向更正：延长 state 2 停留（p21 变小）抬高 P；先前笔记写的"p21 0.025→0.5 ⇒ ×5.7"方向记反了
rp21 = p21_by[0.025]["p"] / p21_by[0.5]["p"]
rho_by = {x["rho"]: x for x in LR}
rrho = rho_by[8.0]["p"] / rho_by[1.0]["p"]
sp = [x["p"] for x in SD]
spread = max(sp) / min(sp) if min(sp) > 0 else None
ratio_prior_ceiling = ceiling / mid_p
lam95 = math.log(20) / 80.0
ent_mid = base["p2_entries_per_region_year"]
share_mid = base["p2_month_share"]
compat = lam95 / ent_mid

s1 = svg_log_bars([
  ("low 先验", SC["low"]["p"], SC["low"]["lo"], SC["low"]["hi"], C2, "%d/1e6" % SC["low"]["events"]),
  ("middle 先验（基准）", mid_p, mid_lo, mid_hi, C1, "%d/1e6" % base["events"]),
  ("high 先验", SC["high"]["p"], SC["high"]["lo"], SC["high"]["hi"], C3, "%d/1e6" % SC["high"]["events"]),
], h=250, axlab="对数轴（五年累计代理触发比例，单位 %）")

s2 = svg_line([x["H"] for x in HZ], [x["p"] for x in HZ], [x["lo"] for x in HZ], [x["hi"] for x in HZ],
              xlab="预测窗口（月）；纵轴=累计代理触发比例")

tor = [
  ("ρ 1 → 8（跨区耦合，p21=0.10）", 1.0, rrho, C1),
  ("p12 ×3（升级概率）", 1.0, r3, C3),
  ("p21 0.5 → 0.025（state 2 停留 2→40 月）", 1.0, rp21, C2),
  ("p12 ×1/3（反向）", r3_lo, 1.0, "#7f93ad"),
  ("蒙特卡洛换 4 个种子（对照噪声）", 1.0, spread, "#9aa3b2"),
]
s3 = svg_tornado(tor)

rows = ["UCDP Dyadic 26.1", "UCDP/PRIO ACD 26.1", "GED v26.1 (1989–2025)", "ICB v16", "COW majors v2024", "COW MID 5.0"]
cols = ["Q1 致命交战可核验", "Q2 ≥2 日级日期 ≤90天", "Q3 日期=实际交战记录", "三条件同时"]
cells = {
 (0,0):("partial","无死亡列"), (0,1):("fail","1969 中苏仅 1 日期"), (0,2):("partial","dyad-year 单日期"), (0,3):("fail","0"),
 (1,0):("partial","无死亡列"), (1,1):("fail","同上"), (1,2):("partial","同上"), (1,3):("fail","0"),
 (2,0):("pass","有日精度致命"), (2,1):("fail","大国对=0 行"), (2,2):("pass","事件级"), (2,3):("fail","0"),
 (3,0):("fail","无任何致命性列"), (3,1):("fail","边界日非交战日"), (3,2):("fail","感知日"), (3,3):("fail","0"),
 (4,0):("na","名单表，非交战源"), (4,1):("na","—"), (4,2):("na","—"), (4,3):("na","用于 pair 判定"),
 (5,0):("partial","17 争端双侧致命"), (5,1):("fail","仅争端边界日"), (5,2):("fail","1993 年前无事件层"), (5,3):("fail","0"),
}
s4 = svg_matrix(rows, cols, cells, w=1090, cellw=190)

s5 = svg_log_bars([
  ("N=80（可核验 pair-year 暴露）", ceiling, None, None, C1, "同一对象：单一大国 pair 的严格终端事件五年累计率"),
  ("N=3,012（仅剔除日精度不足 506 行）", ceiling_3012, None, None, C3, ""),
  ("N=3,518（现实现：缺失折成负例）", ceiling_fold, None, None, CAUT, "分母折叠后的虚假收窄（见卡 6）"),
], h=250, axlab="对数轴（对象=单一大国 pair 的严格终端事件五年累计率；画的是它的 95% 上界，单位 %）")

def tbl(head, body):
    return '<table><thead><tr>' + "".join("<th>%s</th>" % h for h in head) + "</tr></thead><tbody>" + \
           "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in body) + "</tbody></table>"

def sd(x):
    return str(x.get("seed", "—"))

sc_rows = [[k, pct(SC[k]["p"], 4), "%s – %s" % (pct(SC[k]["lo"], 4), pct(SC[k]["hi"], 4)),
            "{:,}".format(SC[k]["events"]), sd(SC[k]), "L3 先验情景"] for k in ("low", "middle", "high")]
hz_rows = [[str(x["H"]), pct(x["p"], 4), "{:,}".format(x["events"]), pct(x["hi"], 4), sd(x)] for x in HZ]
p12_lbl = {0.333: "×1/3", 1.0: "×1", 2.0: "×2", 3.0: "×3", 5.0: "×5"}
p12_rows = [[p12_lbl.get(round(x["factor"], 3), "×%g" % x["factor"]),
             "%.4f" % x["p12"], pct(x["p"], 4), "{:,}".format(x["events"]),
             "%.2f×" % (x["p"] / p12_by[1.0]["p"]), sd(x)] for x in L12]
p21_rows = [["%.3f" % x["p21"], "%.1f 月" % x["dwell"], pct(x["p"], 4),
             "%.2f×" % (x["p"] / p21_by[0.025]["p"]), sd(x)] for x in L21]
rho_rows = [["%.0f" % x["rho"], pct(x["p"], 4), "%.2f×" % (x["p"] / rho_by[1.0]["p"]), sd(x)] for x in LR]
seed_rows = [[sd(x), pct(x["p"], 4), "{:,}".format(x["events"])] for x in SD]
hz_slope = math.log(HZ[-1]["p"] / HZ[0]["p"]) / math.log(HZ[-1]["H"] / HZ[0]["H"])

HTML_DOC = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>WW3 五年风险模型 — 最终模拟结果与可识别性报告（2026-10-15）</title>
<style>
:root{{--ink:#1f2430;--mut:#68707f;--line:#e3e7ee;--bg:#f6f7fa}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:'Microsoft YaHei','Segoe UI',system-ui,sans-serif;font-size:15px;line-height:1.62}}
.wrap{{max-width:1160px;margin:0 auto;padding:26px 20px 64px}}
header{{padding:22px 26px;background:#fff;border:1px solid var(--line);border-radius:12px}}
h1{{font-size:23px;margin:0 0 6px}}
.head{{font-size:13px;color:var(--mut)}}
.alert{{margin:16px 0 0;padding:13px 16px;border-left:4px solid #b4433a;background:#fdf1f0;border-radius:6px;font-size:14px}}
.card{{background:#fff;border:1px solid var(--line);border-radius:12px;padding:18px 22px 20px;margin:18px 0;position:relative}}
.card h2{{font-size:17px;margin:0 0 3px}}
.sub{{color:var(--mut);font-size:13.4px;margin:0 0 14px}}
.tag{{position:absolute;top:18px;right:22px;color:#fff;font-size:11.5px;padding:3px 9px;border-radius:20px}}
table{{border-collapse:collapse;width:100%;font-size:13.6px;margin:6px 0 2px}}
th{{background:#eef2f8;text-align:left;padding:7px 10px;font-weight:600;border-bottom:1px solid var(--line)}}
td{{padding:6px 10px;border-bottom:1px solid var(--line);font-variant-numeric:tabular-nums}}
tr:last-child td{{border-bottom:none}}
.kpi{{display:flex;gap:14px;flex-wrap:wrap;margin:4px 0 12px}}
.kpi div{{flex:1 1 210px;border:1px solid var(--line);border-radius:10px;padding:12px 14px;background:#fbfcfe}}
.kpi b{{display:block;font-size:22px;line-height:1.25}}
.kpi span{{font-size:12.6px;color:var(--mut)}}
.note{{font-size:12.8px;color:var(--mut);margin:10px 0 0}}
.sum{{margin:16px 0 0;padding:16px 20px;border:1px solid #cfd8e6;border-left:4px solid #2f6fb2;background:#fbfcfe;border-radius:8px}}
.sum b.tt{{display:block;font-size:15px;margin-bottom:6px}}
.sum ol{{margin:6px 0 0;padding-left:22px}}
.sum li{{margin:7px 0;font-size:14.2px}}
.sum .stop{{margin:12px 0 0;padding:10px 13px;background:#fdf3f2;border-radius:6px;font-size:13.6px}}
ul{{margin:8px 0 0;padding-left:20px}}
li{{margin:4px 0}}
code{{background:#f1f3f8;padding:1px 5px;border-radius:4px;font-size:12.6px}}
svg{{display:block;width:100%;height:auto;margin:2px 0 0}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
@media(max-width:900px){{.grid2{{grid-template-columns:1fr}}}}
</style></head><body><div class="wrap">
<header>
<h1>WW3 五年风险模型 — 代理事件模拟结果与可识别性报告</h1>
<div class="head">预测窗口 2026-10-15 → 2031-10-15 ｜ 生成于 {GEN} ｜ n = 10<sup>6</sup> 路径／情景，H = 60 个月，5 个区域态，基准种子 {SEED}（每个 run 的种子逐行列在表内）</div>
<div class="alert"><b>读数前提（不可省略）</b>：本报告只有一个可报告对象——<b>代理事件</b>（模拟器判据：滚动 3 个月记忆内 ≥2 个区域处于 state 2）的<b>先验条件触发比例</b>。
它<b>不是</b>"真实 WW3 的五年发生概率"。真实 WW3 的五年概率在本模型中<b>没有被估计，也不可识别</b>：模型里没有严格终端层（≥2 个日级日期、≤90 天、双侧致命、同一升级事件、双方可核实），而六个历史来源提供的可核验正例为 <b>0</b>（Q1 部分通过／Q2 不通过／Q3 不通过），闸门已于 2026-10-15 关闭。
因此蒙特卡洛跑 10<sup>6</sup> 次只是把先验假设采样得很精确，不会把它变成历史校准；<code>0→1</code> 层也只能说"危机起始标签可观测"，不等于完成概率校准。</div>
{SUM}
</header>

{BODY}

</div></body></html>"""

body = []
r_prior = SC["high"]["p"] / SC["low"]["p"]
kpi1 = '<div class="kpi">' + "".join(
    '<div><b>%s</b><span>%s</span></div>' % (v, lab) for v, lab in (
        (pct(mid_p, 4), "中间先验：五年至少一次代理触发（%d/10<sup>6</sup>）" % base["events"]),
        ("%s – %s" % (pct(mid_lo, 4), pct(mid_hi, 4)), "其 Wilson 95% 区间（仅蒙特卡洛抽样误差）"),
        ("%.0f×" % r_prior, "low ↔ high 先验跨度（同一判据同一单位 ⇒ 可比）"),
        ("未估计", "真实 WW3 的五年发生概率（模型无严格终端层，历史 0 正例）"),
    )) + "</div>"
note1 = ('<p class="note">最重要的结果不是中间值，而是这个跨度：同一套判据下三档先验相差 <b>%.0f 倍</b>（low %s ↔ high %s）。'
         '因此<b>不能因为 middle 在中间就把它当"最合理预测"</b>——%s 是一组假设下的条件输出，不是数据给出的最佳估计。'
         '三档之间可比（同对象）；它们与卡 2 的历史上界<b>不可比</b>（不同对象）。'
         '只给单一数字而不给这套对照，就是把先验伪装成预测。</p>') % (r_prior, pct(SC["low"]["p"], 4), pct(SC["high"]["p"], 4), pct(mid_p, 4))
body.append(card("1. 模拟输出：代理事件的五年累计触发比例（三档先验）",
  "判据为模拟器的<b>代理规则</b>：滚动 3 个月记忆内 ≥2 个区域处于 state 2。区间是 Wilson 95%，只含蒙特卡洛抽样误差，不含先验不确定性。",
  kpi1 + s1 + tbl(["先验档", "五年累计代理触发 P", "Wilson 95%", "命中路径", "种子", "层级"], sc_rows) + note1,
  tag="L3 先验", tagc=C3))

body.append(card("2. 统计上界约束的是另一个对象：不能与卡 1 相除",
  "零正例给出的 17.07% 是对<b>单一大国 pair 在一年内发生严格定义终端事件</b>的年率上界，再按恒定率假设换算成同一 pair 的五年累计；它不是本报告系统级代理概率的上界。",
  s5 + '<div class="kpi">' + "".join(
      '<div><b>%s</b><span>%s</span></div>' % (v, lab) for v, lab in (
          ("%.5f /pair-year" % (math.log(20) / 80.0), "λ<sub>95</sub> = −ln(0.05)/N，N=80 可核验 pair-year 暴露"),
          (pct(ceiling, 2), "P<sub>95</sub>(5) = 1−exp(−5λ<sub>95</sub>)（恒定率假设）"),
          ("0 例", "六个来源里满足严格终端定义的可核验正例"),
          ("不可比", "17.07% 与 0.0145% 之间任何倍数的解释力"),
      )) + "</div>" + \
  '<p class="note"><b>17.07% 成立的三个前提</b>：①事件率恒定且 pair-year 之间独立（把 0/80 换成 Poisson 单侧上界）；'
  '②N=80 所代表的总体与 2026–2031 的目标总体同源；③事件定义=严格终端定义（≥2 个日级日期、≤90 天、双侧致命、同一升级事件、双方可核实）。'
  '三条里任何一条不成立，17.07% 就只是某个特定对象上的数，不能搬去约束别的对象。</p>' + \
  '<p class="note"><b>为什么不能算 1178×</b>：17.07% 的估计对象是"单一大国对的五年累计严格终端率"，'
  '0.0145% 的对象是"五个区域组成的系统至少出现一次两区域同时 state 2 的代理事件"。'
  '两者在①观察单位（pair-year ↔ 区域路径）、②事件定义（严格终端 ↔ 代理判据）、③随机变量（单对累计 ↔ 系统联合）三层上都不一致，'
  '相除得到的倍数没有统计含义。<b>本报告已把它从 KPI 与摘要中撤下</b>——这是我上一版的口径错误，在此正文更正。</p>' + \
  '<p class="note"><b>"先验主导"这个结论仍然成立，但换了依据</b>：依据不是跨对象比值，而是模型的实际估计流程——'
  'p01/p10/p12/p21/ρ 在 notebook 里全部是硬编码常数，没有任何一行代码用历史数据拟合它们，'
  '终端层也没有可核验正例可供拟合。所以历史数据对输出的影响是<b>结构性的零</b>（无通道），'
  '而不是"通过某个比值测出它没有约束力"。附带地，因为模型里根本没有严格终端层，'
  '现在连"用 0 正例去否证模拟"都做不到：模型侧没有可比的量。这一条排在 P0 之后。</p>' + \
  ('<p class="note"><b>唯一能做的跨对象对照（带显式换算假设，不是校准）</b>：把 1 个"区域-年"强行当作 1 个"pair-year"暴露，'
   '中间先验下模拟的 state 2 进入率为 <b>%.5f／区域-年</b>（state 2 月度暴露占比 %.4f%%），'
   '而数据对<b>更严格</b>事件的上界是 %.5f／pair-年 ⇒ 模型的代理事件比上界还稀 <b>%.0f 倍</b>。'
   '因为代理判据比严格终端定义更宽松（代理 ⊇ 严格），"更松的事件反而更罕见"与数据不相矛盾，所以一致性检验<b>通过</b>；'
   '但正因为相差 %.0f 倍，N=80 的零正例对这个模型<b>几乎没有检验功效</b>——它否证不了任何东西。'
   '结论与撤掉 1178× 后一致：历史数据目前只能说明"可识别性很弱"，不能给模型定标。</p>'
   % (ent_mid, 100 * share_mid, lam95, compat, compat)),
  tag="口径", tagc=CAUT))

body.append(card("3. 时间维度：中间先验下的累计代理触发曲线",
  "同一先验参数下，把预测窗口从 12 个月延长到 60 个月的累计命中比例。",
  s2 + tbl(["窗口(月)", "P", "命中路径", "上界 95%", "种子／批次"], hz_rows) +
  '<p class="note"><b>批次标注（避免误读为同一组路径）</b>：本表 60 月点 = %s（%d/10<sup>6</sup>），'
  '与卡 1 主结果 middle 的 %s（%d/10<sup>6</sup>）来自<b>不同种子</b>（本批 seed=%d，主结果 seed=%d）；'
  '两者相差 %.1f%%，在 4 个种子的散布 %.3f× 之内，属抽样波动而非矛盾。'
  '五个窗口共用同一条随机流、只截断长度，所以曲线按构造单调嵌套。</p>'
  '<p class="note"><b>不是线性</b>：在本次这 5 个期限上，log-log 斜率 = %.2f（12 月 %s → 60 月 %s，窗口 5 倍、概率 %.0f 倍）。'
  '机理是代理判据要求"3 个月滚动记忆内 ≥2 个区域处于 state 2"，长窗口给两次进入留出重叠机会。'
  '<b>但这只是对已模拟期限的经验拟合</b>：它描述这条曲线，不能外推到未模拟的期限，也不构成"真实危机风险按固定幂次增长"的结构定律。'
  '可用的定性结论只有一条：把月度先验按年率线性外推成五年概率会系统性低估。</p>'
  % (pct(HZ[-1]["p"], 4), HZ[-1]["events"], pct(mid_p, 4), base["events"],
     HZ[-1]["seed"], base["seed"], 100 * (HZ[-1]["p"] / mid_p - 1), spread,
     hz_slope, pct(HZ[0]["p"], 4), pct(HZ[-1]["p"], 4), HZ[-1]["p"] / HZ[0]["p"]),
  tag="L3 先验", tagc=C3))

body.append(card("4. 敏感性：哪些旋钮真正在推动代理触发比例",
  "单变量扫描（其余固定为中间先验），倍数值相对同组基准；对象始终是代理触发比例，不是真实 WW3 概率。",
  s3 + '<div class="grid2">' +
  tbl(["p12 倍率", "月率", "五年 P", "命中", "×基准", "种子"], p12_rows) +
  tbl(["p21", "state2 平均停留", "五年 P", "×(p21=0.025)", "种子"], p21_rows) + '</div>' +
  tbl(["ρ（跨区耦合）", "五年 P", "×ρ=1", "种子"], rho_rows) +
  '<p class="note">弹性实测：∂lnP/∂lnp12 = <b>%.2f</b>（p12×3 ⇒ P×%.2f）；ρ=8 ⇒ P×%.2f；'
  '<b>p21 的方向是反的</b>——state 2 停留越长（p21 从 0.5 降到 0.025）P 越<b>高</b>，倍数 %.2f×；'
  '我先前笔记里写的"p21 0.025→0.5 ⇒ ×5.7"方向记反，本轮按同一脚本重跑已更正为 0.5→0.025 ⇒ ×5.72。'
  '对照：换 4 个种子的蒙特卡洛散布只有 <b>%.3f×</b>，Wilson 区间上/下界之比 %.3f×。'
  '<b>对账口径</b>：三张表各自用独立种子，组内基准（p12 组 %.4f%%、p21 组 %.4f%%）与主结果 middle 的 %.4f%% 相差 %.1f%%／+%.1f%%，'
  '都在种子散布 %.3f× 之内；ρ 组的基准天然更低（%.4f%%），因为它把 p21 固定成 0.10（停留 10 月）而不是 0.025。'
  '所有倍数只在同组、同批种子内相除，不跨组比较。'
  '⇒ 结论对先验设定的敏感度比抽样噪声高约 <b>%.0f 倍</b>，这是本报告把区间叫"先验区间"而不是"置信区间"的量化理由。</p>'
  % (elast, r3, rrho, rp21, spread, (mid_hi / mid_lo),
     100 * p12_by[1.0]["p"], 100 * p21_by[0.025]["p"], 100 * mid_p,
     100 * (p12_by[1.0]["p"] / mid_p - 1), 100 * (p21_by[0.025]["p"] / mid_p - 1),
     spread, 100 * rho_by[1.0]["p"],
     (r3 / spread) if spread else float("nan")), tag="杠杆", tagc=C1))

body.append(card("5. 为什么终端数字只能是先验：六个来源的可识别性矩阵",
  "Q1 致命交战可核验／Q2 同一大国对 ≥2 个日级日期且 ≤90 天／Q3 日期来自实际交战记录。",
  s4 + '<ul>'
  '<li>UCDP Dyadic／PRIO：1946–2025 大国×大国 dyad-year 只有 <b>1 行</b>（1969-03-02 中苏，Ussuri），且每个 dyad-year 只带一个交战日期 ⇒ Q2 恒不成立。</li>'
  '<li>GED v26.1（1989–2025，417,968 行、358,130 行日精度）：<b>两端均为大国的事件行数 = 0</b> ⇒ "有日精度致命性"与"大国对"交集为空。</li>'
  '<li>ICB v16：512 危机、1,131 行为体行，<b>无任何致命性列</b>；TRIGDATE/TERMDATE 官方定义是"感知日"；50 个日期字段 day∈{66,77,88} 非法 ⇒ <code>errors="coerce"</code> 静默丢成 NaT（必须记 indeterminate，不能记 negative）。</li>'
  '<li>COW MID 5.0：大国对争端 232 个／33 dyad，<code>fatality≥1</code> 39 个，其中 <b>38 个开始于 1993 年前</b>（事件层无覆盖）；改为"双侧致命"只剩 <b>17 个</b>且各只给 1 个争端级日期；事件层（唯一日期即交战日的层）大国对 234 个事件里致命 <b>1</b> 个（2001-04-01）⇒ 致命多日期组合 = <b>0</b>。</li>'
  '<li>1969 中苏 MID 349：start→end = <b>286 天</b>，连"首尾两日期"都超 90 天窗。</li></ul>', tag="证据", tagc="#3f9d78"))

body.append(card("6. 唯一还没闭合的可靠性缺口（P0）",
  "标签三态未实现：classifier 里的 <code>_as_bool</code> 与 <code>.fillna(False)</code> 把「证据不足」实现成「确认未发生」。",
  '<div class="kpi"><div><b>%s</b><span>N=80：单对严格终端五年累计率的上界</span></div>'
  '<div><b>%s</b><span>N=3,012（仅剔除 506 行日精度缺口）</span></div>'
  '<div><b>%s</b><span>N=3,518（现实现行为）</span></div>'
  '<div><b>%.1f×</b><span>同一对象、同一正例数下的虚假收窄倍数</span></div></div>'
  '<p class="note"><b>为什么这里的 %.1f× 有效、卡 2 撤下的 1178× 无效</b>：本卡三条上界是<b>同一个估计对象</b>'
  '（单一大国 pair 的严格终端五年累计率），只有分母 N 不同（80 → 3,012 → 3,518），所以相除得到的是纯粹的分母口径差异；'
  '卡 2 的 1178× 则跨了对象（单对严格率 ↔ 系统级代理事件），没有统计含义。上界族的图形见卡 2。</p>'
  '<p class="note">误标面实测：UCDP 日精度缺口 506/3,518=14.38%%；MID 致命大国对行 <code>fatalpre</code> 未知 82/83=98.80%%；ICB1 非法日历日 50/512=9.77%%。'
  '口径限定：三个 N 的总体不同（pair-year vs dyad-year），本卡只演示"分母折叠"这一种错误的量级，不构成合法上界。P0 的 6 条验收判据见 <code>ww3_task_priority_v1.md</code> §1，代码尚未落地。</p>'
  % (pct(ceiling, 2), pct(ceiling_3012, 2), pct(ceiling_fold, 2), ceiling / ceiling_fold, ceiling / ceiling_fold), tag="待办", tagc=CAUT))

body.append(card("7. 复现信息、更正记录与结果边界",
  "所有数字可用同一脚本一次重跑得到；每个 run 的种子随结果一起落进 <code>_report_data.json</code>。",
  tbl(["项目", "取值"], [
    ["脚本", "<code>_report_sim.py</code>（跑数）／<code>_report_build.py</code>（图与报告）"],
    ["代理判据", "滚动 3 月记忆内 ≥2 区域处于 state 2（notebook 原逻辑，未通过历史验证）"],
    ["中间先验参数", "p01=[.005,.005,.003,.007,.003]／月，p10=.15，p12=.003，p21=.025，ρ=1"],
    ["区域", "5 个区域态；初始状态全 0（notebook 设定，未用当前状态证据表替换）"],
    ["批次划分", "scenarios=SEED+0/1/2；horizon=SEED+3（五个窗口共用一条流）；p12=SEED+21；p21=SEED+11；ρ=SEED+31（p21 固定 0.10）；种子复测=SEED+101..104"],
    ["随机数", "numpy default_rng，基准种子 %s" % D["meta"]["seed_base"]],
    ["运行耗时", "27 个 run（n=10<sup>6</sup>，H=12–60），重跑事件数逐一复现"],
    ["未包含", "当前起点证据（P1-c）、战区 map（P1-d）、时间外验证（P1-b）——三者均在 P0 之后"],
  ]) +
  tbl(["种子", "五年代理触发 P", "命中路径"], seed_rows) +
  '<p class="note"><b>更正记录（本轮）</b>：'
  '①<b>撤回</b>上一版"统计上界 ÷ 中间先验 = 1178× ⇒ 历史数据未被使用"的论证——两个数不是同一个估计对象，比值无解释（改由估计流程本身论证，见卡 2）；'
  '②卡 1 与卡 2 的条形图<b>拆分</b>，此前把代理概率与 pair-year 上界画在同一坐标下，视觉上暗示可比；'
  '③卡 3 的 60 月点（%s）与主结果（%s）此前未标注批次差，现逐行给出种子；'
  '④P ∝ H<sup>%.2f</sup> 从"结构性放大"降级为"对已模拟 5 个期限的经验拟合"；'
  '⑤p21 方向更正（卡 4）。'
  '⑥另把全部结果统一改称"<b>代理触发比例</b>"，不再简称"终端概率"。</p>'
  '<ul><li><b>可以声称</b>：在先验参数 X 与代理判据下，模型给出五年累计代理触发比例 %s（先验区间 %s–%s）。</li>'
  '<li><b>不可以声称</b>：该数值经历史校准、是"后验"、可用于赔付/决策阈值设定，或"是真实 WW3 的五年概率"。</li>'
  '<li><b>上界参照（限定对象）</b>：零正例上界 %s 约束的是<b>单一大国 pair 的严格终端五年累计率</b>，'
  '与本报告的系统级代理概率不同对象，故只作为"历史可识别性有多弱"的定性证据，不参与任何倍数比较。</li>'
  '<li>关联决策记录：<code>ww3_terminal_layer_gate_freeze_v1.md</code>（闸门关闭）、<code>ww3_task_priority_v1.md</code>（P0）、'
  '<code>audit/independent_gate_report_2026-10-15.md</code>（证据，§0–§7 前 153 行锚点 <code>87575855…f404c6</code>）。</li></ul>'
  % (pct(HZ[-1]["p"], 4), pct(mid_p, 4), hz_slope,
     pct(mid_p, 4), pct(mid_lo, 4), pct(mid_hi, 4), pct(ceiling, 2)), tag="方法", tagc=MUT))

# ================= 卡 8：美债补充项（数字在构建时从一手 CSV 重算） =================
FISC_PATH = os.path.join(HERE, "us_debt", "evidence", "_tyc2026.csv")
_ys = []
if os.path.exists(FISC_PATH):
    with open(FISC_PATH, newline="", encoding="utf-8") as _f:
        for _r in csv.DictReader(_f):
            if _r.get("10 Yr"):
                _mm, _dz, _yy = _r["Date"].split("/")
                _ys.append((date(int(_yy), int(_mm), int(_dz)), float(_r["10 Yr"]),
                            float(_r["2 Yr"]) if _r.get("2 Yr") else None,
                            float(_r["3 Mo"]) if _r.get("3 Mo") else None))
_ys.sort()
if not _ys:
    raise SystemExit("缺 us_debt/evidence/_tyc2026.csv：美债补充项禁止用记忆里的数字出图")
_by = {d: (v10, v2, v3m) for d, v10, v2, v3m in _ys}
_y10 = [(d, v10) for d, v10, v2, v3m in _ys]
_TR = min(_y10, key=lambda x: x[1]); _PK = max(_y10, key=lambda x: x[1]); _LAST = _y10[-1]
N_OBS = len(_y10)

def ten_delta(end):
    a = _by[end]; b = _by[_TR[0]]
    return tuple(round((x - y) * 100) for x, y in ((a[0], b[0]), (a[1], b[1]), (a[2], b[2])))

D19, D20, D24, D26 = (ten_delta(date(2026, 3, 19)), ten_delta(date(2026, 3, 20)),
                      ten_delta(date(2026, 3, 24)), ten_delta(date(2026, 3, 26)))
EPISODES = 0; BEST = (0.0, None, None)
for _i in range(len(_ys)):
    for _j in range(_i + 1, len(_ys)):
        _cal = (_ys[_j][0] - _ys[_i][0]).days
        if _cal > 30:
            break
        _d10 = _ys[_j][1] - _ys[_i][1]
        if _d10 > BEST[0]:
            BEST = (_d10, _ys[_i][0], _ys[_j][0])
        if 0.40 <= _d10 <= 0.45:
            _sv, _sd0 = _ys[_i][1], _ys[_i][0]
            if not any(_ys[_k][1] < _sv and _sd0 < _ys[_k][0] < _sd0 + timedelta(days=30)
                       for _k in range(len(_ys))):
                EPISODES += 1
AT439 = [d.isoformat() for d, v in _y10 if abs(v - 4.39) < 1e-9]

FR, FO, FF, FB = 5.00, 7.00, 4.60, 1.10
P_OUT, P_REC, GAP90 = 100 * FF / FO, 100 * FF / FR, 0.90 * FO - FF
EL = {}
for _b in (4.0, 4.7, 5.5):
    _inc = 0.01 * _b / FB
    EL[_b] = (_b * 1000.0, 100 * _inc, math.log(1.10) / math.log(1 + _inc))
EL_LO, EL_HI = min(v[2] for v in EL.values()), max(v[2] for v in EL.values())
F_MOVE = 1.10 ** elast
F_ORD = math.log10(r_prior / F_MOVE)

def svg_yield(series, bands, marks, w=1090, h=340, pad_l=78, pad_r=190, pad_t=30, pad_b=58):
    xs = [d.toordinal() for d, _ in series]
    x0, x1 = min(xs), max(xs)
    vs = [v for _, v in series]
    ylo, yhi = math.floor(min(vs) * 10 - 1) / 10.0, math.ceil(max(vs) * 10 + 1) / 10.0
    X = lambda o: pad_l + (o - x0) / float(x1 - x0) * (w - pad_l - pad_r)
    Y = lambda v: h - pad_b - (v - ylo) / float(yhi - ylo) * (h - pad_t - pad_b)
    s = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="%s">'
         % (w, h, w, h, FONT)]
    for d0, d1, lab, col in bands:
        s.append('<rect x="%.1f" y="%d" width="%.1f" height="%d" fill="%s" opacity="0.14"/>'
                 % (X(d0.toordinal()), pad_t, X(d1.toordinal()) - X(d0.toordinal()), h - pad_t - pad_b, col))
        s.append('<text x="%.1f" y="%d" font-size="11.5" fill="%s">%s</text>'
                 % (X(d0.toordinal()) + 3, pad_t + 27, col, html.escape(lab)))
    t = int(round(ylo * 10))
    while t <= int(round(yhi * 10)):
        v = t / 10.0
        s.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s"/>' % (pad_l, Y(v), w - pad_r, Y(v), GRID))
        s.append('<text x="%d" y="%.1f" font-size="12" fill="%s" text-anchor="end">%.1f</text>'
                 % (pad_l - 8, Y(v) + 4, MUT, v))
        t += 2
    seen = set()
    for d, _ in series:
        if d.month not in seen:
            seen.add(d.month)
            s.append('<text x="%.1f" y="%d" font-size="12" fill="%s" text-anchor="middle">%d月</text>'
                     % (X(d.toordinal()), h - pad_b + 20, MUT, d.month))
    pts = " ".join("%.1f,%.1f" % (X(d.toordinal()), Y(v)) for d, v in series)
    s.append('<polyline fill="none" stroke="%s" stroke-width="1.9" points="%s"/>' % (C1, pts))
    for d, v, lab, col, dx, dy in marks:
        s.append('<circle cx="%.1f" cy="%.1f" r="3.4" fill="%s"/>' % (X(d.toordinal()), Y(v), col))
        s.append('<text x="%.1f" y="%.1f" font-size="12" font-weight="600" fill="%s">%s</text>'
                 % (X(d.toordinal()) + dx, Y(v) + dy, col, html.escape(lab)))
    s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s"/>' % (pad_l, h - pad_b, w - pad_r, h - pad_b, MUT))
    s.append('<text x="%d" y="%d" font-size="11.5" fill="%s">美国 10 年期国债票面收益率（%%），日度；阴影=两个 +40bp 量级的窗口</text>'
             % (pad_l, h - 8, MUT))
    s.append('</svg>')
    return "".join(s)

S8 = svg_yield(_y10,
   [(_TR[0], date(2026, 3, 26), "被引用的 3 月窗口", C3),
    (BEST[1], BEST[2], "年内更大的 +%.0fbp 窗口" % (BEST[0] * 100), CAUT)],
   [(_TR[0], _TR[1], "02/27 低点 %.2f%%" % _TR[1], INK, 6, 18),
    (date(2026, 3, 20), 4.39, "4.39%%（三次出现）" % (), C3, 8, -8),
    (_PK[0], _PK[1], "10/05 峰 %.2f%%" % _PK[1], MUT, 10, -20),
    (_LAST[0], _LAST[1], "10/14 %.2f%%（一手）" % _LAST[1], C1, 10, 4)],
   h=350)

S8K = '<div class="kpi">' + "".join('<div style="flex:1 1 186px"><b>%s</b><span>%s</span></div>' % (v, l) for v, l in (
    ("%.2f%%" % _LAST[1], "2026-10-14 的 10Y（一手 CSV，197 观测）"),
    ("不可识别", "3 月窗口对所声称的避险机制（不等于「不存在关系」）"),
    ("%d 次" % EPISODES, "年内从局部低点起 ≤30 日 ≥40bp 的上行次数"),
    ("%.1f%% vs %.1f%%" % (P_OUT, P_REC), "四项刚性合计 ÷支出 与 ÷收入（分母才是关键）"),
    ("%.2f 个数量级" % F_ORD, "财政扰动（×%.3f）相对先验跨度（%.0f×）" % (F_MOVE, r_prior)),
)) + "</div>"

S8T = tbl(["声称", "判定", "一手 / 二手"], [
    ["FY2026 净利息 &gt;$1T", "二手相符；一手未取到", "cbo.gov 直连与代理均 403（DataDome）"],
    ["FY2026 赤字 ~$2T、利息 ~$1.1T", "二手", "MTS 返回 JS 壳；fiscaldata API 根路径 404"],
    ["国防 ~$1T", "口径混用在来源侧：2025-12-18 是 NDAA 授权", "二手（ Reuters/媒体一致）"],
    ["Krainin, Ramsay, Wang &amp; Ruggiero (2022)", "文献真实；被概括成单调 p12 乘数不准确", "一手：SAGE + DOI 10.1177/07388942211024947"],
    ["10Y = 5.19%（2026-10-14）", "一手确认", "Treasury 日度曲线 CSV（本卡即由它重算）"],
    ["3.96% → 4.39%（冲突后）", "起点值不在序列里（全年最低 %.2f%%）；端点非唯一" % _TR[1], "一手 CSV"],
    ["达利欧 2026-04 CNBC 引语", "无源，不得作直接引语", "未找到逐字稿或原视频"],
])

S8N1 = ('<p class="note"><b>三条不可识别证据</b>（起点同为 %s 的年内低点 %.2f%%）：'
        '①<b>非唯一</b>——从局部低点起 ≤30 日、涨幅 40–45bp 的上行有 <b>%d 次</b>，年内最大 30 日升幅 <b>+%.0fbp</b>（%s→%s），大于被引那一次；'
    '②<b>端点不唯一</b>——4.39%% 出现在 %s；被当作起点的 3.96%% 与 4.14%% 在全年序列里<b>各出现 0 次</b>；'
    '③<b>曲线形态方向相反</b>——至 03/24 为 10Y +%dbp／2Y +%dbp／3M +%dbp，至 03/26 为 +%dbp／+%dbp／+%dbp：'
    '两种配对下 <b>2 年期涨幅都不小于 10 年期、3 个月期只有个位数 bp</b>，这是政策路径/通胀预期重定价的形状，'
    '不是"仅长端因避险消失而上抬"的形状；且到 03/19 已 +%dbp（占该段 %.0f%%）。'
    '结论固定为：<b>该窗口对避险机制不可识别</b>，不是"已证明避险属性逆转"，也不是"已证明避险机制不存在"。</p>') % (
    _TR[0].isoformat(), _TR[1], EPISODES, BEST[0] * 100, BEST[1].isoformat(), BEST[2].isoformat(),
    "、".join(AT439), D24[0], D24[1], D24[2], D26[0], D26[1], D26[2], D19[0], 100.0 * D19[0] / D26[0])

S8N2 = ('<p class="note"><b>"&gt;90%% 的预算"是分母错误而不是数字错误</b>：按本轮口径输入（收入 ~$%.1fT、支出 ~$%.1fT，'
        '净利息+国防+社保+医疗 ~$%.2fT），÷支出 = <b>%.1f%%</b>，÷收入 = <b>%.1f%%</b>。'
        '">90%%" 只在以收入为分母时成立；要在支出分母上达到 90%%，四项需再多 ~$%.2fT，口径修订补不上。'
        '该比率是水平量、无边际含义，不构成风险阈值（同"没有理由把 利息/军费=1 设为阈值"）。</p>') % (FR, FO, FF, P_OUT, P_REC, GAP90)

S8N3 = ('<p class="note"><b>量级链：接线也推不动决策</b>：+100bp 只作用在一年内滚存本息上，'
        '再融资基数 4.0–5.5T ⇒ +$%.0f–%.0fB ⇒ 净利息账单 +%.1f–%.1f%%；要把它写成 p12 ×1.10，'
        '隐含"利息账单→p12"弹性需为 <b>%.2f–%.2f</b>，本轮未找到任何来源支持弹性 &gt;1。'
        '取本数据自推的指数 P ∝ p12<sup>%.2f</sup>，p12 ×1.10 只给 <b>P ×%.3f</b>，而三档先验跨度是 %.0f×，'
        '相差 <b>%.2f 个数量级</b>。<b>范围限定（不得升级）</b>：这否证的只是"当前先验跨度下财政变量足以改变决策输出"，'
        '不是"财政压力与战争风险无关"；先验跨度一被压缩，本条须重测。</p>') % (
    EL[4.0][0], EL[5.5][0], EL[4.0][1], EL[5.5][1], EL_LO, EL_HI, elast, F_MOVE, r_prior, F_ORD)

S8N4 = ('<p class="note"><b>文献许可的是交互项，且带两个符号相反的主效应</b>：原文（样本为 Lemke 2003 大国对 1816–1992）'
        '强调战争激励取决于权力转移性质与债务市场基本面的<b>交互</b>，低概率但更极端的权力转移尤其危险；'
        '同时"一般利率上升经战争成本使战争更不可能"与"主权债利息上升使战争更可能"两条主效应符号相反。'
        '因此若将来纳入财政指标，须<b>同时保留这两个主项再交互</b>——只写交互项是欠设定而非保守设定；'
        '理论结论不得当作本模型的系数直接引用。</p>')

S8N5 = tbl(["阶段", "验收目标", "本卡的状态"], [
    ["P0（唯一高优先级）", "三态标签；缺失不转 <code>False</code>；未核验暴露退出负例分母（判据沿用 <code>ww3_task_priority_v1.md</code> §1 六条）", "未实现"],
    ["P1", "时间有效协变量规范：<code>vintage</code>／<code>as_of</code>／<code>missing_reason</code>；缺失语义与 P0 三态同一套机制", "未开始"],
    ["P1-b", "含无危机观察期与观察分母的 0→1 风险集；时间外验证", "未开始"],
    ["后续", "具备识别条件后才讨论 p12、ρ 与财政变量的关系；单条美国序列与年份固定效应完全共线（有效 N = 年份数，行数不解决识别）", "被识别性阻塞"],
])

body.append(card("8. 补充项：美债财政压力（候选协变量，不进估计流程）",
  "本节不改动 p12、ρ 与终端定义；依 <code>ww3_terminal_layer_gate_freeze_v1.md</code> 冻结④，涉及 ρ 的新机制在冻结文件被正式修订前只能是 L3 先验情景。"
  "卡内收益率与曲线数字在构建时由 <code>us_debt/evidence/_tyc2026.csv</code> 重算（与 <code>us_debt/check_fiscal_claims.py</code> 同一条链），财政口径为二手转述。",
  S8K + S8 + S8T + S8N1 + S8N2 + S8N3 + S8N4 + S8N5 +
  '<p class="note"><b>为什么不进正式摘要</b>：摘要按既定规则只写三件事（模拟输出／可识别性／决策含义）。'
  '本节是<b>补充项</b>：它提供的是"哪些路径有数据可检验、哪些仍须留在先验"，不是新的概率估计。</p>'
  '<p class="note">更正登记：本卡初稿曾把三个不同终点的涨幅写成一组（10Y +45／2Y +52／3M +7），'
  '现按同一终点的配对重算并显示；缺失处理与 P0 同源，缺数据一律走 <code>indeterminate_resolution</code> 而不是折成"财政压力低"。</p>',
  tag="先验假设，未估计", tagc=CAUT))

SUM = ('<div class="sum"><b class="tt">正式摘要（只写三件事）</b><ol>'
 '<li><b>模拟输出</b>：在人为设定的三档先验与代理判据下，五年累计<b>代理触发比例</b>分别为 %s、%s、%s'
 '（每档 10<sup>6</sup> 条路径，命中 %s／%s／%s）。这是"代理事件的模拟概率"，<b>不是</b>"真实 WW3 的五年发生概率"。</li>'
 '<li><b>可识别性</b>：经审计的六类历史来源没有提供满足严格终端定义的可验证正例，'
 '因此目前无法从这些资料估计可靠的真实 WW3 五年发生概率。零正例上界 %s 约束的是"单一大国 pair 的严格终端五年累计率"，'
 '与上面三条不是同一个估计对象，故不参与任何倍数比较。</li>'
 '<li><b>决策含义</b>：p<sub>12</sub>（×3 ⇒ ×%.2f）、state 2 停留时长（p<sub>21</sub> 0.5→0.025 ⇒ ×%.2f）'
 '与跨区耦合 ρ（1→8 ⇒ ×%.2f）都会显著改变输出，且全部远大于换随机种子的散布 %.3f×；'
 '因此<b>任何单一结果都不应作为经历史校准的风险数字使用</b>。</li></ol>'
 '<div class="stop"><b>升级前提</b>：在 P0（三态标签把"确认发生／确认未发生／证据不足"严格分开，修掉缺失值被转成 <code>False</code>）'
 '以及当前状态证据审核（P1-c）、时间外验证（P1-b）完成之前，本报告的分层结论与曲线<b>不升级为现实风险预测</b>。'
 '继续扩充模拟不是下一步。</div></div>'
 % (pct(SC["low"]["p"], 4), pct(mid_p, 4), pct(SC["high"]["p"], 4),
    "{:,}".format(SC["low"]["events"]), "{:,}".format(base["events"]), "{:,}".format(SC["high"]["events"]),
    pct(ceiling, 2), r3, rp21, rrho, spread))

doc = HTML_DOC.format(GEN=time.strftime("%Y-%m-%d %H:%M"), SEED=D["meta"]["seed_base"], SUM=SUM, BODY="\n".join(body))
outp = os.path.join(HERE, "output", "ww3_final_simulation_report_2026-10-16.html")
os.makedirs(os.path.dirname(outp), exist_ok=True)
open(outp, "w", encoding="utf-8").write(doc)
print("WROTE", outp, len(doc), "bytes")
print("mid_p=%s ci=[%s,%s] ceiling=%s fold=%s r3=%.2f rp21=%.2f rrho=%.2f spread=%s elast=%.2f" %
      (pct(mid_p, 4), pct(mid_lo, 4), pct(mid_hi, 4), pct(ceiling, 2), pct(ceiling_fold, 3), r3, rp21, rrho,
       ("%.3f" % spread) if spread else "n/a", elast))
