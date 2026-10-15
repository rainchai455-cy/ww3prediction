# WW3 最终报告交付目录（release_2026-10-15）

建立时间 2026-10-16 00:04。本目录是自包含的**报告 + 执行依赖**快照，不是模型实现目录。里面没有任何代码通过 P0；`label_status` 三态仍未实现。

> **本仓库（公开站）与本地交付目录的映射**：本文件是从交付目录带过来的记录，表中路径按交付目录写。三处差异：① `index.html` = 表中的 `ww3_final_simulation_report_2026-10-16.html`（同字节、同哈希 `5f1f03b6…`）；② 表中 `us_debt/section10_draft_asis.md` 与 `us_debt/pending_patch.md` 未随本仓库发布（内部评审过程），其余文件逐字节一致；③ 本仓库另有**公开站专属产物**，不在下表：`README.md`、`_readme_build.py`、`assets/fig1..6.svg|png`（12 个文件）、`.nojekyll`、`.gitattributes`——详见 §8。文中 `<upstream>/` 指本地未发布的上游目录。

## 1. 目录内容

| 路径 | 字节 | sha256 | 角色 |
|---|---|---|---|
| `ww3_final_simulation_report_2026-10-15.html` | 38,433 | `69e78e0965460389b7d3246b3f5778dc8fe2c8f6f7e279e4eb76fc9388664202` | **定稿快照**（与 `<upstream>/` 同名文件逐字节一致，本目录内不参与被覆盖） |
| `_report_sim.py` | 5,102 | `adc9364f6d21b9d14e982e44d2e4c78feace96cf88ea3d191391a8a2df2eef8b` | 蒙特卡洛驱动（27 个 run，同批种子） |
| `_report_build.py` | 48,554 | `784c9b8ae6c81f37daf27a7926afdb5ef54327995749f12886d5367fc16ab939` | 图表/正文构建（纯 SVG，无绘图库依赖）。**本目录版含卡 8「美债补充项」163 行，与原工作区脚本不再等价**（见 §3）。本版修掉了 5/6 张图的 `font-family` 非法引号（见 §4） |
| `ww3_final_simulation_report_2026-10-16.html` | 50,847 | `5f1f03b69d10a4f4452b5876992eb471cb80775f7f4503702b92581e0e3bf688` | **当前版报告（8 卡 / 6 图）**，= 上面 build 脚本跑出的产物；含卡 8。本仓库内同一份字节以 `index.html` 发布 |
| `_report_data.json` | 6,581 | `910c9309f71ac480bbd3973adec9e702767c076769ba5b32b22737acca4d5ed0` | 唯一中间数据：全部结果 + 每个 run 的种子 + 代理暴露率 |
| `us_debt/evidence/_tyc2026.csv` | 16,067 | `bec74a6c0f118755eee4855ab6dc4fa924e6c08b6361e23b6c2e2590f2cb271c` | 一手证据（Treasury 日度曲线 2026，197 观测）。不是 `_report_sim.py` 的依赖，但**是 `_report_build.py` 卡 8 的构建期依赖**：缺文件即 `SystemExit`，卡内每个收益率数字都由它现算 |
| `us_debt/check_fiscal_claims.py` | 3,189 | `8392f5e50fbab5855450ae14703bd0b106cf9f4b820ad7062a291013fbb57c13` | 美债部分唯一可执行核验：从上面那个 CSV 重算正文每个数字（纯标准库，无 numpy、无网络） |
| `us_debt/evidence/check_output_2026-10-16.txt` | 1,242 | `0613e5bad9fcad368d4bf0815652af6a595f1b2146f0ef1b88a3ec1ea4252c5a` | 上述脚本上次运行的原样输出（21 行），供离线对账 |
| `us_debt/audit_findings.md` | 9,472 | `dfe2166c0cdc594c9777158f3b51f1c14a132e8c3e8aac33b18a91fefd84bee7` | 美债模块审计记录（出处门 7 项、不可识别判定、90% 分母、量级检验、三条阻塞、顺序表；71 行） |
| `us_debt/section10_draft_asis.md` | 7,640 | `1a58f30cc0391d9c16335302d7b7298e394bc82a7c74b0eec632fe0c9d1eef17` | 他方 §10 草稿的**原样快照**（未改一字，合并后仍按原样保留）。其中 3 处必改（P1–P3）已于 2026-10-16 在并入审计报告时执行，见该报告 §10.8。**未随本仓库发布** |
| `us_debt/pending_patch.md` | 5,237 | `47c984ec30f13caddb0e59e7efeea92876bc994b123e64fe4d36d72ffa39e0b9` | 7 条定点补丁（3 必改 + 4 建议）的**指令原件**；2026-10-16 已执行（P1–P5、P7 入 §10，P6 作废），顶部已标注执行状态，正文按原件保留未回改。**未随本仓库发布** |
| `output/`（重建后生成） | — | — | 你自己重跑时报告的落点；刻意与定稿分开，避免覆盖 |

依赖闭包：`numpy`（仅 `_report_sim.py`）+ 标准库（math/json/time/os/csv/html/datetime）。**无 matplotlib、无 pandas、无网络访问、无 notebook 参与**；全部图形是构建脚本自己拼的内联 SVG，产物是单文件 HTML（除 SVG 命名空间 URL 外无任何外部引用，可直接作静态首页）。

## 2. 复现命令（实测环境）

```
解释器  D:\OCR\PaddleOCR\.venv\Scripts\python.exe   python 3.12.10 / numpy 2.3.5
步骤 1  <python> _report_sim.py      # 约 158 s，覆写本目录 _report_data.json
步骤 2  <python> _report_build.py    # 秒级，读 _report_data.json + us_debt\evidence\_tyc2026.csv，写 output\ww3_final_simulation_report_2026-10-16.html，不碰 10-15 定稿快照
步骤 3  <python> us_debt\check_fiscal_claims.py   # 秒级，只读 us_debt\evidence\_tyc2026.csv，重算美债部分全部数字，不写文件
步骤 4  <python> _readme_build.py    # 仅公开站需要：读 index.html，写 README.md + assets\figN.svg/png；需系统 ImageMagick（带 RSVG delegate），不碰 HTML
```

单跑步骤 2 即可重建当前版报告（`_report_data.json` 与 CSV 都已在目录内；CSV 缺失时脚本以 `SystemExit` 明确失败，不会静默少一张卡）。单跑步骤 3 即可独立复核卡 8 每个数字——它与卡 8 读同一份 CSV、走同一条算式，但代码彼此独立，互为对照。三条阻塞与顺序表是决策记录，不需要重算。

## 3. 本目录脚本 vs 原工作区脚本

`_report_sim.py`：只做路径相对化，**删 1 行 / 增 3 行，零逻辑改动**。
`_report_build.py`：删 3 行 / 增 168 行 = 相对化（4 行）+ **卡 8「美债补充项」163 行插入**（437–599 行）。

```
-report_sim.py:1    import math, json, time, numpy as np
+report_sim.py:1-3  import math, json, time, os / import numpy as np / HERE = os.path.dirname(...)
-report_sim.py:100  open(r"C:\Users\...\_report_data.json", "w")
+report_sim.py:102  open(os.path.join(HERE, "_report_data.json"), "w")
-report_build.py:1  import json, math, html, os, time
+report_build.py:1-2 + csv / + from datetime import date, timedelta
-report_build.py:3  open(r"C:\Users\...\_report_data.json", encoding="utf-8")
+report_build.py:4-5 HERE = ... / open(os.path.join(HERE, "_report_data.json"), encoding="utf-8")
+report_build.py:437-599  卡 8 全部代码（读 CSV→现算→SVG 折线图→KPI/表/注）
-report_build.py:452 outp = r"<upstream>/ww3_final_simulation_report_2026-10-15.html"
+report_build.py:617 outp = os.path.join(HERE, "output", "ww3_final_simulation_report_2026-10-16.html")
```

**范围说明（不得略过）**：卡 8 是本轮新增内容，不是"相对化"。因此本目录的 build 脚本已**不能**再复现 10-15 定稿（它写 10-16 文件名并多出一张卡）；能复现定稿的是原工作区脚本 `6ad5eb5a…`。定稿快照在本目录内以字节形式保留，不靠脚本保证。

原工作区脚本与 `<upstream>/` 下的定稿**均未被本目录的操作改动**（`_report_sim.py` = `9edf3ea3…`，`_report_build.py` = `6ad5eb5a…`，定稿 = `69e78e09…`，本轮重算一致）。

## 4. 已验证的复现证据

- `py_compile` 两个脚本通过。
- **定稿复现证明（由加卡 8 之前的 build 版本 `8550b757…` 做出，当时实测）**：只跑步骤 2，产物 38,433 B；把生成时间戳归一化后与定稿逐字符相同（各 30,203 字符）。唯一差异是 `<div class="head">` 里的"生成于 2026-10-15 23:20" → "2026-10-16 00:04"。该证明**不适用于当前 build 脚本**（见 §3 范围说明）。
- **当前版（含卡 8）实测**：`_report_build.py` `d850d072…` 跑步骤 2 → `output/ww3_final_simulation_report_2026-10-16.html` 50,847 B / 39,740 字符 / 8 张卡 / 6 幅内联 SVG；根目录副本与 `output/` 那份同哈希 `08acf514…`。卡 8 的 18 个探针串全部命中（19 次、+54bp、5.19%、不可识别、65.7%、92.0%、1.70、1.95、2.67、×1.212、4811、3.60 个数量级、三次出现、indeterminate_resolution、+42bp、+58bp、Lemke、403）。**其后**修 `font-family` 合法性（`784c9b8a…`）重跑步骤 2：产物仍 50,847 B / 8 卡 / 6 图，哈希变为 `5f1f03b6…`，18 个探针串复测仍全部命中，定稿快照未被写。
- **界面自检**：headless Edge 1180×9500 截图，`-trim` 内容边界 1120×7138+30+26；卡 8 区域逐块目视过。修掉的三处排版缺陷：①右上 "10/05 峰 5.31%" 原先越出画布被裁；②橙色 "4.39%（03/20、03/24、05/01 三次出现）" 长标签压在折线上，改为 "4.39%（三次出现）"，三个日期改由正文注 ② 承载（`AT439` 现算）；③ 5 个 KPI 原先 4+1 换行、第 5 个被拉成整行，改内联 `flex:1 1 186px` 后单行等宽（页高 7229→7138）。
- **SVG 标记合法性缺陷（由栅格化管线发现，不是浏览器发现）**：卡 1–5 的 5 幅内联 SVG 写成 `font-family=''Microsoft YaHei',…'`——嵌套单引号让属性值提前闭合，不是合法 XML。浏览器按 HTML 解析器容错，所以网页版一直看着正常；librsvg 直接拒绝（`unable to read image data`）。定位前先做正对照（一张最小中文 SVG 能正常转 PNG），排除管线自身问题后才回到源文件。已在 `_report_build.py` 四处改为双引号包裹 ⇒ 10-16 版哈希 `08acf514…` → `5f1f03b6…`，字节数仍是 50,847。**定稿快照（`69e78e09…`）与原工作区脚本（`6ad5eb5a…`）仍带此缺陷，按"定稿不再改动"未回改**；它只影响严格 XML 解析（如栅格化），不影响浏览器渲染。
- 关键标量重建后一致：`mid_p=0.0145%`、`ci=[0.0123%,0.0171%]`、`ceiling=17.07%`、`fold=0.425%`、`r3=9.21`、`rp21=5.72`、`rrho=6.13`、`spread=1.095`、`elast=2.02`。
- 蒙特卡洛侧（上一轮已做，本目录未重跑）：同种子重跑 27 个 run，事件数逐一复现 3/145/14432；3/21/58/102/157；12/140/613/1289/3199；198/166/128/85/45/29；78/137/249/478；147/150/145/137。
- 美债侧（步骤 3，本目录内已实跑）：`check_fiscal_claims.py` 从 CSV 重算出 19 次 ≤30 日 40–45bp 上行、最大 30 日升幅 +54bp、3.96 与 4.14 各出现 **0 次**、4.39 出现 3 次、两组端点配对 42/52/7 与 45/58/6、65.7% 与 92.0%、补平支出分母需再 1.70T、隐含对数弹性 1.95–2.67、4811÷1.212 = 3,968 倍（3.60 个数量级）。与 `audit_findings.md` 引用值逐项一致；输出已落盘为 `evidence/check_output_2026-10-16.txt`。
- 本目录内做过的一次自我更正：`audit_findings.md` 初稿抄了我上一轮手写（未跑脚本）的 "+45／+52／+7"，端点混用；已按脚本值改写并在文中登记更正。MANIFEST 表格内的字节数也有一次照抄估算值被 `stat` 否证后改正（5,083→5,102、36,538→36,546、2,903→3,189、1,544→1,242、8,921→9,472）。

## 5. 引用本目录时必须保持的口径边界

1. 报告输出是**五年累计代理触发比例**（判据：滚动 3 月记忆内 ≥2 区域处于 state 2，该规则未经历史验证）；**真实 WW3 的五年发生概率未被估计，也不可识别**。
2. 中间档 0.0145% 不是"最合理预测"，最重要的结果是先验敏感性 **4811×**。
3. 17.07% 上界的对象是 pair-year 严格终端累计率，**不得与代理概率相除**；上一版的 1178× 论证已撤回（审计 §9）。卡 6 的 **40.2×** 仍有效，因为三条上界同一估计对象、只是分母 N 不同。
4. `P ∝ H^2.46` 只是本次 5 个已模拟期限上的经验斜率，不是结构定律。
5. ρ 与终端阈值受 `ww3_terminal_layer_gate_freeze_v1.md` 冻结④约束；任何涉及 ρ 的新机制在正式修订冻结前只能作为 L3 先验情景，不进估计流程。
6. **美债部分**：文献只支持交互机制（且原文含两个符号相反的主效应），不支持把利息支出写成单调 p12 乘数；">90%" 是以收入为分母（÷支出为 65.7%）；2026 年 3 月那个窗口对"避险属性翻转"**不可识别**——不可识别 ≠ 不存在关系。
7. 美债量级检验的范围限定：4811× ÷ 1.212 = **3,968 倍（3.60 个数量级）**，否证的只是"当前先验跨度下财政变量足以改变决策输出"，先验跨度一被压缩须重测。
8. **两版报告的关系**：10-15 那份是**定稿快照**（`69e78e09…`，7 卡，不再改动）；10-16 那份 = 定稿 + 卡 8（8 卡）。卡 8 带标签"先验假设，未估计"，**刻意不写进页首"正式摘要（只写三件事）"**：它提供的是"哪些路径有数据可检验、哪些仍停留在先验"，不是新的概率估计。引用 10-16 版时不得把卡 8 说成模型输入或已估计量。

## 6. 本目录刻意不含

- 模型代码与 notebook（P0 未动，不得声称已实现三态标签）。
- `ww3_terminal_layer_gate_freeze_v1.md`、`ww3_task_priority_v1.md`、审计报告正文——仍各自在原处，本目录只放快照与副本，不放第二真值源。
- §10 **已于 2026-10-16 合并进审计报告**（该报告不在本仓库，位于 `<upstream>/audit/independent_gate_report_2026-10-15.md`）：195 行 → 271 行 →（第二轮更正后）**291 行 / 47,954 B / sha256 `84eae4b9…`**；**纯追加**（末尾 `---` + 新 §10），前 153 行锚点复验仍为 `87575855…f404c6`，合并前备份 `<upstream>/audit/_premerge_backup_independent_gate_report_2026-10-16.md`（`7cc00a69…`）。执行 P1–P5、P7，**P6 作废**（目标措辞在两份 HTML 报告里各 0 处命中），依据与我方两处数字更正记在新 §10.8。第二轮（02:05）审计了他方 `1/` 目录的自建补丁，记在 §10.8.1：他们两处数字口径写错（19 次的判据区间、对数弹性写成 2.0–2.75）、P6 那条 0 命中指令再次出现、P7 缺项；**我方 10.2 犯过同一处 19/≥40 的错并已就地改正**，同时查出核对用的脚本判据有浮点边界（名义含端点应为 22 次），记录改为并列 19／22／50 三口径，脚本本身未动。本目录 `us_debt/` 里放的是**副本**（他方原样快照 + 我方审计记录 + 补丁指令原件），真值源是那份审计报告；`<upstream>/ww3_section10_append_draft_2026-10-15.md`（`1a58f30c…`，56 行）未被改动，他方的补丁也**没有**被应用到任何地方（避免第三份 §10）。
- `ww3_risk_model_v0_3_bundle.zip`（未重打包，与 bundle 目录不一致；重打包=覆盖既有产物，需另下指令）。

## 7. 已知未修项（沿用他 V0.3 工作单，本目录不掩盖）

- 报告正文写"六个"标签测试，代码实为 7 个（`PASS: 7 pair-aware label tests`）。
- 终端窗口上限代码 `>89` 天 vs 文档 `≤90` 天。
- `_as_bool` / `.fillna(False)` 仍把"证据不足"折成负例；`raise ValueError` 路径不产出状态。

## 8. 发布状态（首轮，2026-10-16 00:55 推送 / 01:05 Pages 实测）

- 已推到 `https://github.com/rainchai455-cy/ww3prediction`，分支 `main`；推送前 `ls-remote` 实测该仓库零 ref，故本次未覆盖任何既有内容。
- **线上逐字节验收**（走 contents API + `Accept: application/vnd.github.raw`，绕开 raw.githubusercontent 的 CDN 缓存）：`index.html` 50,847 B / sha256 `08acf514022930739e683ab56533177e6ac8313c6a15887769754610efa7aa5a`；`ww3_final_simulation_report_2026-10-15.html` 38,433 B / `69e78e0965460389b7d3246b3f5778dc8fe2c8f6f7e279e4eb76fc9388664202`。两条与 §1 记录一致 ⇒ `.gitattributes` 的 `* -text` 生效，CRLF 未被规范化。
- **Pages 已开启（2026-10-16 01:05 实测）**：<https://rainchai455-cy.github.io/ww3prediction/> 返回 HTTP 200、**50,847 B / sha256 `08acf514022930739e683ab56533177e6ac8313c6a15887769754610efa7aa5a`**，与仓库内 `index.html` 逐字节一致 ⇒ 报告即站点首页，且换行符未被改动。定稿直链 38,433 B、`us_debt/evidence/_tyc2026.csv` 16,067 B、`MANIFEST.md` 13,031 B 均 200；`_report_build.py` 也返回 200（证明 `.nojekyll` 生效，下划线开头文件没被 Jekyll 排除）。
- 一条如实记录的不一致：站点已可访问，但 `GET /repos/…/pages`（未鉴权）仍返回 **HTTP 404**。以站点实测 200 为准；该 API 结果不作为"未部署"的证据。

## 9. 公开站专属产物：README 直接渲染报告（2026-10-16 01:20）

仓库首页只渲染 `README.md`（不会内联渲染 `.html`），而 GitHub 的 Markdown 管线会**剥掉原始 HTML 与 `<svg>`** ⇒ 要让首页"看起来就是报告"，只能把 HTML 机械转成 Markdown、把 6 幅 SVG 栅格化成 PNG。做法是派生产物而非手抄：

| 文件 | 字节 | sha256（前 8） | 角色 |
|---|---|---|---|
| `_readme_build.py` | 7,888 | `c6149345df7fd85e8e85c58e13984a69c54417594e4290d1f1441fcfeacc3460` | HTML→Markdown 转换器（纯标准库 + 系统 `magick`）。输入 `index.html`，输出 `README.md` + `assets/figN.svg/png` |
| `README.md` | 22,265 | `8b8dbb3763bf74dbc0082f64cdbc2feb30a8adb24473b414c4d72691fe79b7e3` | 由上者生成，212 行：1 个 H1 + 8 个 H2（卡标题带原标签前缀，如 `## L3 先验 ｜ 1. …`）+ 1 个 H3、**13 张 Markdown 表 / 76 行表体**（KPI 也转成表）、6 处 `![图 N](assets/figN.png)`、23 条引用块（原 note/alert + 4 条前置说明） |
| `assets/fig1..6.svg` | 2,919 / 1,846 / 2,685 / 3,014 / 6,363 / 5,881 | `d177d0b1` `50d7e2c8` `474281ec` `a59e249d` `f2e18e31` `49da5e2c` | 从 HTML 里原样抽出的 SVG，仅把 `width="100%"` 替换成显式 `width`/`height`（前插会产生重复属性 ⇒ 非法 XML）。**这 6 个哈希才是图的稳定身份**：重跑步骤 4 不变 |
| `assets/fig1..6.png` | 24,174 / 15,587 / 39,175 / 33,597 / 54,509 / 104,043 | `c40b8d20` `381d4507` `d4295a96` `dda43c49` `05184510` `f4731b01` | `magick -density 144`，尺寸 1635×375 / ×375 / ×450 / ×477 / ×546 / ×525，合计 271,085 B。**PNG 内嵌 tIME 文本块，每次重栅格化哈希都会变**（字节数不变）⇒ 上列哈希只对应 `db7dd68` 这次提交，不能当幂等性检验；幂等只看 `README.md` |

一致性与自检（全部实测）：

- **数字同源性**：README 正文与 `index.html` 由同一棵树转换得出，脚本内没有硬编码任何报告数字；唯一硬编码的是那三行"本文件为派生产物"的说明。
- **实体不丢**：转换器用 `convert_charrefs=False` 并显式接住 `handle_entityref`/`handle_charref`。早期版本把 `&gt;`/`&amp;` 静默丢掉过，现以三个探针复验：`净利息 >$1T`、`Wang & Ruggiero`、`弹性 >1` 各命中 1 次。
- **图无裁切**：6 张 PNG 逐一 `-trim` 取内容边界，右边界距画布边缘 25–36 px（fig2 左边界仅剩 1 px 但未被切）；fig2–fig5 拼成一张 1635×1880 蒙太奇后目视过（中文正常、坐标轴与图例完整）。
- **一处布局 bug 由自检发现并修**：结构性容器原本被并成单个 block，导致"派生产物"说明落到文末；改为摊平后它在 H1 正下方，正文部分逐字节未变（前后 diff 只有那 6 行的位置）。
- **幂等**：连跑两次 `README.md` 同哈希；PNG 只 tIME 变（见上表）。一处自身更正：§9 初稿里的 6 个 PNG 哈希取自"最后一次重栅格化之前"，与线上比对时被否证（尺寸同、哈希异），已按提交 `db7dd68` 的实际字节改正——这正是 PNG 哈希不该当幂等判据的原因。
- **它替换掉了什么**：首轮提交（`b993e80`）的 `README.md` 是 5,291 B 手写仓库说明，已被本派生版整体覆盖。手写版里的三样东西各有去处：状态声明（"不是模型实现 / P0 未实现 / 未经校准"）与定稿直链进前置引用块第 1 条，网页版直链进第 4 条，口径边界与文件表不再重复——正文本身就是报告，第二份摘要只会制造第二个真值源。
- 维护链：改 `_report_build.py` → 重跑步骤 2 → `cp` 成 `index.html` → 重跑步骤 4。**不要手改 `README.md` 正文数字**。

## 10. 第二轮发布与线上逐字节验收（2026-10-16 01:35）

- 提交 `db7dd68`（17 个文件变更）已推 `origin/main`，快进 `b993e80..db7dd68`，非强推。仓库现 5 个 commit：`9d397ee`→`1a2e5fe`→`810fff5`→`b993e80`→`db7dd68`；受版本控制文件 13 → **26 个**（`git ls-files` 实测：新增 `_readme_build.py` 1 个 + `assets/` 12 个；`README.md` 原已跟踪，故只算覆盖不算新增）。
- **contents API 原始字节**（`Accept: application/vnd.github.raw+json`，带 `?ref=db7dd68`，不走 raw.githubusercontent 的 CDN 缓存）：`index.html` 50,847 B / `5f1f03b6`、`README.md` 22,265 B / `8b8dbb37`、`_readme_build.py` 7,888 B / `c6149345`、`assets/fig6.png` 104,043 B / `f4731b01`、`assets/fig1.png` 24,174 B / `c40b8d20`、定稿快照 38,433 B / `69e78e09` —— 六条与本地工作区逐字节一致（`fig6.png` 另做了 `cmp` 全文件比对，rc=0）。
- **Pages 首页已随之更新**：<https://rainchai455-cy.github.io/ww3prediction/> = 200、50,847 B、`5f1f03b6`（不再是首轮的 `08acf514…`）；定稿直链 200 / 38,433 B / `69e78e09`；`assets/fig6.png` 200 / 104,043 B / `f4731b01`。
- **仓库首页确实渲染了报告正文**（`curl https://github.com/rainchai455-cy/ww3prediction` 页面 HTML 352,821 B）：6 个 `assets/figN.png` 引用全部出现在 `<img>` 里；探针串命中次数——"代理触发比例" 6、"不可识别" 4、"4811" 5、"17.07%" 9、`Wang &amp; Ruggiero` 1、"净利息" 4、"$1T" 3。即 Markdown 管线没剥掉表格与图，实体也没丢。
- 一条计数口径的更正：本条初稿写"14 个 `<table>`、21 个 `<h2>`"，那是**整页** grep 值，含 GitHub 自己的文件列表 chrome。README 自身的量按 `grep -c` 实测是 **13 张表 / 8 个 H2 / 1 个 H1 / 1 个 H3 / 6 处图片引用**（见 §9 行内的 76 行表格计数）。引用时按 README 口径，不要把整页计数当报告结构。
- 本文件（`MANIFEST.md`）自身不参与逐字节记录：每追加一轮记录它就变哈希，把它写进表里等于制造一条必然过期的断言。

---

## 11. §10 并入审计报告后，公开站的实际状态（2026-10-16 01:50）

- **本轮改动分两步测得，两次都对本文件之外零影响**。第一步：把 §1 的 `section10_draft_asis.md`、`pending_patch.md` 两行注记与 §6 的"§10 仍未合并"改成"已合并"，`git diff --stat` = `MANIFEST.md | 6 +++---`（**3 insertions / 3 deletions**）。第二步：追加本节本身，追加后即时测得 diff = **15 insertions / 3 deletions**（= 第一步的 3/3 + 本节新增 12 行；本节随后又补了两条记录，所以这个数不是最终提交数）。两步里 `index.html`、`README.md`、`_report_build.py`、`_readme_build.py`、`assets/` 12 个与 `us_debt/` **一个字节都没动**，`git status --short` 始终只列出 `M MANIFEST.md`；发布物哈希不变：`index.html` 50,847 B / `5f1f03b6…`、`README.md` 22,265 B / `8b8dbb37…`。
- **合并没有让公开站与审计报告出现数字分歧**：卡 8 的收益率数值是 `_report_build.py` 从 `_tyc2026.csv` 现算的，落稿时写的就是否证口径，而不是他方草稿里的被否证值。在已发布的 `index.html`（`README.md` 同源，同样命中）里实测：
  - 原始字节 `grep -o` 计数——`3.96%` 2 处、`4.14%` 2 处、`避险` 5 处、`达利欧` 1 处；逐处看过上下文，这四处都是**在否证句或出处门表里**出现（"3.96% → 4.39%（冲突后）｜起点值不在序列里（全年最低 3.97%）；端点非唯一"），不是被当作观测值引用。
  - 去标签、并空白后的正文里，下列句子各命中 1 次：`各出现 0 次`（完整句："被当作起点的 3.96% 与 4.14% 在全年序列里 各出现 0 次"）、`涨幅 40–45bp 的上行有 19 次`、`最大 30 日升幅 +54bp`、`至 03/26 为 +45bp`、`占该段 62%`、`该窗口对避险机制不可识别`、`无源，不得作直接引语`。注意 P2 的三段配对（+42/+45）在站里是分开写的，没有混用成一个终点。
  - 命中 **0 次**：`美债收益率不再因地缘冲突而下降`。这就是 §10.8 里 P6 作废的同一依据，在站侧再验一遍。
- 因此**不重建 HTML、不重跑 README 管线**：P1–P3 纠正的对象是他方草稿文件，公开站从未登过那三个错值；P6 要改的措辞在站里不存在。合并后的审计报告本身仍只在 `<upstream>/audit/`，不上传本仓库（三方对账文档，公开站只放报告与其可复现依赖）。
- 第二轮里唯一牵到发布物的一条，如实说明：站侧 `index.html`／`README.md` 的卡 8 写"从局部低点起 ≤30 日、涨幅 40–45bp 的上行有 19 次"。复算发现 **19 是 `check_fiscal_claims.py:39` 浮点判据的值**——`0.40 ≤ Δ ≤ 0.45` 会漏掉 3 个尾数为 `0.4500000000000002` 的恰 45 bp 窗口（08/26→09/23、09/09→10/02、09/09→10/07），名义含端点应为 **22 次**；只设 ≥40 bp 下限、不设上限则是 **50 次**（其中 28 个 >45 bp）。三口径已并列写进 `<upstream>/audit/independent_gate_report_2026-10-15.md` 的 10.2 与 §10.8.1。**发布物仍未重建**：19 属偏保守方向（只低估"非唯一"，不夸大），不可识别的结论不依赖这个数；脚本本身也没改（它是我方全部引用值的落盘凭据，改它等于换证据）。若要把页面也改成三口径并列，需另下指令并重跑 `_report_build.py` → `cp` 成 `index.html` → `_readme_build.py`。
- 一条自身操作更正，如实登记：本轮原先想用 `printf` 追加本节，双引号里的反引号被 bash 当命令替换执行了，PATH 上的 `/d/bin/README.md`、`trng` 因此被当脚本跑了一遍，并在仓库根目录留下 3 个未跟踪文件（`secret.bin` 32 B、`trng` 0 B、`⚠️` 0 B，mtime 01:50:51/01:50:55）。已 `rm -f` 删除并复验：`git status --short` 回到只有 `M MANIFEST.md`，`git ls-files` 仍 26 个，§1 表格里受控文件逐字节核对 **checked=10 bad=3**，三条 MISSING 恰是开头映射说明里已声明的三个（`ww3_final_simulation_report_2026-10-16.html` 以 `index.html` 名发布 + 两个未发布的 `us_debt/` 内部件）。教训：含反引号的中文段落一律走 Edit，不走 shell。
- **推送与线上逐字节验收**（数字绑定到提交 `1ce11a4`，本文件在 `1ce11a4` 之后又被这条记录改动，故不要把下面的哈希当"最新版"）：快进推送 `3421325..1ce11a4`，非强推，`git status -sb` 显示 `main...origin/main` 无分叉。contents API（`Accept: application/vnd.github.raw+json`，`?ref=1ce11a4`）取回字节后本地复验：`index.html` 50,847 B / `5f1f03b69d10a4f4452b5876992eb471cb80775f7f4503702b92581e0e3bf688`、`README.md` 22,265 B / `8b8dbb3763bf74dbc0082f64cdbc2feb30a8adb24473b414c4d72691fe79b7e3` 这两条做了 `cmp` 全文件比对（rc=0）；`MANIFEST.md` 当时取回 24,789 B / `c41e6b2c8901fc2c731ae8a090252ac0fb0bf328e223a9b35cc5697fdd9cf111`，与本地哈希相等，其后本条记录又继续增长过本文件的哈希与字节数——所以这里刻意不写"最新版 MANIFEST 的大小"：每次追加都会改自己的哈希，任何自记数字一落地就过期。引用 `MANIFEST.md` 必须带 ref。Pages 首页仍 200 / 50,847 B / `5f1f03b6…` ⇒ **报告首页一个字节都没因本次审计合并而变化**，这正是上面"无需重建"结论的线上佐证。
