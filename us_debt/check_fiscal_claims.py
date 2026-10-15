"""美债部分唯一可执行核验：从 evidence/_tyc2026.csv 重算正文引用的每个数字。
纯标准库（csv/datetime/math），无 numpy、无网络。用法：
    <python> us_debt/check_fiscal_claims.py
"""
import csv, math, os
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, "evidence", "_tyc2026.csv")
TEN = ("3 Mo", "2 Yr", "10 Yr")

rows = {}
with open(CSV, newline="", encoding="utf-8") as f:
    for d in csv.DictReader(f):
        if d.get("10 Yr"):
            m, dd, y = d["Date"].split("/")
            rows[date(int(y), int(m), int(dd))] = {k: float(d[k]) for k in TEN}
ser = sorted(rows.items())
print("观测数 =", len(ser))

lo = min(ser, key=lambda x: x[1]["10 Yr"]); hi = max(ser, key=lambda x: x[1]["10 Yr"])
print("10Y 最低 %.2f @%s ｜ 最高 %.2f @%s" % (lo[1]["10 Yr"], lo[0], hi[1]["10 Yr"], hi[0]))
print("10/14 观测 10Y = %.2f" % rows[date(2026, 10, 14)]["10 Yr"])

for v in (3.96, 4.14, 4.39, 4.42):
    ds = [d for d, r in ser if abs(r["10 Yr"] - v) < 1e-9]
    print("  10Y == %.2f 出现 %d 次 %s" % (v, len(ds), ds))

# 30 日窗口内的上行：非唯一性检验
ep, best = [], None
for i in range(len(ser)):
    for j in range(i + 1, len(ser)):
        cal = (ser[j][0] - ser[i][0]).days
        if cal > 30:
            break
        d10 = ser[j][1]["10 Yr"] - ser[i][1]["10 Yr"]
        if best is None or d10 > best[0]:
            best = (d10, ser[i][0], ser[i][1]["10 Yr"], ser[j][0], ser[j][1]["10 Yr"], cal)
        if 0.40 <= d10 <= 0.45:
            sv, s = ser[i][1]["10 Yr"], ser[i][0]
            if not any(r["10 Yr"] < sv and s < d < s + timedelta(days=30) for d, r in ser):
                ep.append(d10)
print("从局部低点起 <=30 日、涨幅 40-45bp 的上行 = %d 次" % len(ep))
print("年内最大 30 日升幅 = +%.0fbp（%s %.2f -> %s %.2f）" % (best[0] * 100, best[1], best[2], best[3], best[4]))

for e in (date(2026, 3, 19), date(2026, 3, 20), date(2026, 3, 24), date(2026, 3, 26)):
    d = {k: (rows[e][k] - rows[lo[0]][k]) * 100 for k in TEN}
    print("  %s -> 10Y %+.0f ｜ 2Y %+.0f ｜ 3M %+.0f bp" % (e, d["10 Yr"], d["2 Yr"], d["3 Mo"]))

# 财政比率（口径输入写死在此，便于复核；来源限制见 audit_findings.md）
rec, out, four, bill = 5.00, 7.00, 4.60, 1.10
print("\n四类合计 %.2fT：/支出 %.1f%% ｜ /收入 %.1f%% ｜ 到支出的90%%需再 %.2fT"
      % (four, 100 * four / out, 100 * four / rec, 0.90 * out - four))
print("+100bp 作用在一年内再融资本金：")
el = []
for base in (4.0, 4.7, 5.5):
    inc = 0.01 * base / bill
    need = math.log(1.10) / math.log(1 + inc)
    el.append((math.log(1.10) / math.log(1 + 0.01 * 4.0 / bill), need))
    print("   基数 %.1fT -> +%.0fB = 账单 +%.1f%% ；凑 p12 x1.10 隐含对数弹性 %.2f"
          % (base, base * 10, 100 * inc, need))
print("   隐含弹性区间 %.2f-%.2f（无任何来源支持 >1）" % (min(x[1] for x in el), max(x[1] for x in el)))
k = 2.02
print("P = p12^%.2f -> p12 x1.10 给 x%.3f；4811 / %.3f = %.0f 倍 = %.2f 个数量级"
      % (k, 1.10 ** k, 1.10 ** k, 4811 / 1.10 ** k, math.log10(4811 / 1.10 ** k)))
