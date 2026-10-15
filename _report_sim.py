import math, json, time, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20261015
REG = 5
SC = {
 "low":    dict(p01=np.array([.0020,.0020,.0015,.0025,.0015]), p10=.20, p12=.0010, p21=.040),
 "middle": dict(p01=np.array([.0050,.0050,.0030,.0070,.0030]), p10=.15, p12=.0030, p21=.025),
 "high":   dict(p01=np.array([.0120,.0120,.0070,.0150,.0070]), p10=.10, p12=.0100, p21=.015),
}

def sim(p, n, seed, H=60, rho=1.0):
    """与 notebook 相同的转移与终端判定；终端事件 = 滚动 3 月记忆内 >=2 个区域处于 state 2。"""
    rng = np.random.default_rng(seed)
    st = np.zeros((n, REG), dtype=np.int8)
    hist = np.zeros((3, n, REG), dtype=np.int8)
    hit = np.zeros(n, dtype=bool)
    p01 = np.asarray(p["p01"], float); p10, p12, p21 = p["p10"], p["p12"], p["p21"]
    s2months = 0; s2entries = 0; prev2 = np.zeros((n, REG), dtype=bool)
    for t in range(H):
        old = st.copy(); new = old.copy()
        u0 = rng.random(old.shape); m0 = old == 0
        new[m0 & (u0 < p01[None, :])] = 1
        u1 = rng.random(old.shape); m1 = old == 1
        down = m1 & (u1 < p10); esc = m1 & (u1 >= p10) & (u1 < p10 + p12)
        if rho != 1.0:
            other2 = (old == 2).sum(axis=1, keepdims=True) > ((old == 2).astype(int))
            extra = m1 & (~esc) & other2 & (u1 >= p10 + p12) & (u1 < p10 + p12 + (rho - 1) * p12)
            esc = esc | extra
        new[down] = 0; new[esc] = 2
        u2 = rng.random(old.shape); m2 = old == 2
        new[m2 & (u2 < p21)] = 1
        st = new; hist[t % 3] = st
        now2 = (st == 2)
        s2months += int(now2.sum()); s2entries += int((now2 & ~prev2).sum()); prev2 = now2
        hit |= (np.any(hist == 2, axis=0)).sum(axis=1) >= 2
    ev = int(hit.sum()); ph = ev / n; z = 1.96
    den = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / den
    half = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / den
    return dict(n=n, H=H, seed=int(seed), events=ev, p=ph,
                p2_month_share=s2months / float(n * H * REG),
                p2_entries_per_region_year=s2entries * 12.0 / float(n * H * REG),
                lo=max(0.0, c - half), hi=min(1.0, c + half))

def w(p21=None, p12f=1.0, rho=1.0):
    q = dict(SC["middle"])
    q["p12"] = q["p12"] * p12f
    if p21 is not None: q["p21"] = p21
    return q, rho

out = {"meta": {"seed_base": SEED, "regions": REG, "terminal_rule":
                "rolling 3-month memory: >=2 regions in state 2",
                "n_main": 1_000_000, "H_main": 60,
                "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")},
       "scenarios": {}, "horizon": [], "p12": [], "p21": [], "rho": [], "seeds": []}
out["meta"]["batches"] = {
    "scenarios": "low=SEED+0, middle=SEED+1, high=SEED+2",
    "horizon": "全部 H 共用 SEED+3（同一条随机流，H 只截断长度）",
    "p12": "SEED+21", "p21": "SEED+11", "rho": "SEED+31（并把 p21 固定为 0.10）",
    "seeds": "SEED+101..104"}
t0 = time.time()

for i, k in enumerate(["low", "middle", "high"]):
    out["scenarios"][k] = sim(SC[k], 1_000_000, SEED + i)
    print("scenario %-7s p=%.5f%% ci=[%.5f,%.5f] ev=%d  %.0fs" %
          (k, 100*out["scenarios"][k]["p"], 100*out["scenarios"][k]["lo"],
           100*out["scenarios"][k]["hi"], out["scenarios"][k]["events"], time.time()-t0), flush=True)

for H in (12, 24, 36, 48, 60):
    r = sim(SC["middle"], 1_000_000, SEED + 3, H=H)
    out["horizon"].append(r)
    print("horizon %2dm p=%.5f%% ev=%d  %.0fs" % (H, 100*r["p"], r["events"], time.time()-t0), flush=True)

for f in (1/3, 1.0, 2.0, 3.0, 5.0):
    q, _ = w(p12f=f)
    r = sim(q, 1_000_000, SEED + 21)
    out["p12"].append(dict(factor=f, p12=q["p12"], **{k: r[k] for k in ("p","lo","hi","events","seed")}))
    print("p12 x%.3f p=%.5f%% ev=%d  %.0fs" % (f, 100*r["p"], r["events"], time.time()-t0), flush=True)

for v in (0.010, 0.025, 0.050, 0.100, 0.250, 0.500):
    q, _ = w(p21=v)
    r = sim(q, 1_000_000, SEED + 11)
    out["p21"].append(dict(p21=v, dwell=1/v, **{k: r[k] for k in ("p","lo","hi","events","seed")}))
    print("p21 %.3f p=%.5f%% ev=%d  %.0fs" % (v, 100*r["p"], r["events"], time.time()-t0), flush=True)

for rho in (1.0, 2.0, 4.0, 8.0):
    q, r_ = w(p21=0.10, rho=rho)
    r = sim(q, 1_000_000, SEED + 31, rho=rho)
    out["rho"].append(dict(rho=rho, p21=0.10, **{k: r[k] for k in ("p","lo","hi","events","seed")}))
    print("rho %.1f p=%.5f%% ev=%d  %.0fs" % (rho, 100*r["p"], r["events"], time.time()-t0), flush=True)

for s in range(4):
    r = sim(SC["middle"], 1_000_000, SEED + 101 + s)
    out["seeds"].append(r)
    print("seed+%d p=%.5f%% ev=%d  %.0fs" % (101+s, 100*r["p"], r["events"], time.time()-t0), flush=True)

ps = [x["p"] for x in out["seeds"]]
out["meta"]["seed_spread"] = {"min": min(ps), "max": max(ps), "ratio": max(ps)/min(ps),
                              "wilson_widths": [x["hi"]-x["lo"] for x in out["seeds"]]}
json.dump(out, open(os.path.join(HERE, "_report_data.json"), "w"), indent=1)
print("DONE %.0fs  seed spread ratio=%.3f" % (time.time()-t0, out["meta"]["seed_spread"]["ratio"]), flush=True)
