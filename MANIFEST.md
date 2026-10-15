# WW3 最终报告交付目录（release_2026-10-15）

建立时间 2026-10-16 00:04。本目录是自包含的**报告 + 执行依赖**快照，不是模型实现目录。里面没有任何代码通过 P0；`label_status` 三态仍未实现。〔后半句自 2026-10-16 03:40 起过期：三态标签已在上游 `<upstream>/www3v0.3/ww3_risk_model_v0_3.ipynb`（70,612 B / `d8c53ee6…`）实现并通过 `ww3_task_priority_v1.md` §1 六条判据，见 §13。前半句仍成立：本仓库不含 notebook，站内发布件字节未变。〕

> **本仓库（公开站）与本地交付目录的映射**：本文件是从交付目录带过来的记录，表中路径按交付目录写。三处差异：① `index.html` = 表中的 `ww3_final_simulation_report_2026-10-16.html`（同字节、同哈希 `9bc1fb1b…` / 51,618 B；2026-10-16 02:47 按指令重建后生效，重建前为 50,847 B / `5f1f03b6…`，见 §12）；② 表中 `us_debt/section10_draft_asis.md` 与 `us_debt/pending_patch.md` 未随本仓库发布（内部评审过程），其余文件逐字节一致；③ 本仓库另有**公开站专属产物**，不在下表：`README.md`、`_readme_build.py`、`assets/fig1..6.svg|png`（12 个文件）、`.nojekyll`、`.gitattributes`——详见 §8。文中 `<upstream>/` 指本地未发布的上游目录。

## 1. 目录内容

| 路径 | 字节 | sha256 | 角色 |
|---|---|---|---|
| `ww3_final_simulation_report_2026-10-15.html` | 38,433 | `69e78e0965460389b7d3246b3f5778dc8fe2c8f6f7e279e4eb76fc9388664202` | **定稿快照**（与 `<upstream>/` 同名文件逐字节一致，本目录内不参与被覆盖） |
| `_report_sim.py` | 5,102 | `adc9364f6d21b9d14e982e44d2e4c78feace96cf88ea3d191391a8a2df2eef8b` | 蒙特卡洛驱动（27 个 run，同批种子） |
| `_report_build.py` | 50,537 | `0c3bd8a687bea427e734ebf00abd215a5349869f47047c8929545bb6e3a5d105` | 图表/正文构建（纯 SVG，无绘图库依赖）。**本目录版含卡 8「美债补充项」，与原工作区脚本不再等价**（见 §3）。本版修掉了 5/6 张图的 `font-family` 非法引号（见 §4）；02:18 那轮改了窗口三口径计数、`EL` 增量单位、弹性标"对数"（见 §12）；**03:54 那轮只改 P0 状态文字**（卡 6 标题/副题、tag 待办→已闭合、图内 `N=3,518` 标签改等宽"旧实现"、任务表 P0 列、页尾升级前提），六组对账数字与其余五幅图未变（见 §14）。**这棵树是自包含的**：03:56 用本仓库这份脚本 + 本仓库 `us_debt/evidence/_tyc2026.csv` 重跑，产物与 `index.html` 归一化生成时间戳后逐字符相同（各 52,037 字节）。改前 `50,049 B / 62357533…` |
| `ww3_final_simulation_report_2026-10-16.html` | 52,106 | `5517b3058d1600adf092243bef86f5fa4f83ba9e8d13dc0befdbe1b11ca98fd2` | **当前版报告（8 卡 / 6 图）**，= 上面 build 脚本跑出的产物；含卡 8。本仓库内同一份字节以 `index.html` 发布（改前 `9bc1fb1b…` / 51,618 B，备份 `<upstream>/release_2026-10-15/_prerebuild_backup_2026-10-16/site_index_before_p0.html`） |
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
- **当前版（含卡 8）实测**：`_report_build.py` `d850d072…` 跑步骤 2 → `output/ww3_final_simulation_report_2026-10-16.html` 50,847 B / 39,740 字符 / 8 张卡 / 6 幅内联 SVG；根目录副本与 `output/` 那份同哈希 `08acf514…`。卡 8 的 18 个探针串全部命中（19 次、+54bp、5.19%、不可识别、65.7%、92.0%、1.70、1.95、2.67、×1.212、4811、3.60 个数量级、三次出现、indeterminate_resolution、+42bp、+58bp、Lemke、403）。**其后**修 `font-family` 合法性（`784c9b8a…`）重跑步骤 2：产物仍 50,847 B / 8 卡 / 6 图，哈希变为 `5f1f03b6…`，18 个探针串复测仍全部命中，定稿快照未被写。**第三次重跑（02:47，指令"改，更新并重跑流水线"）后本节的 50,847／`5f1f03b6…` 均已过期**：现为 51,618 B / 40,218 字符 / `9bc1fb1b…`，逐条改动与探针见 §12。
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
- §10 **已于 2026-10-16 合并进审计报告**（该报告不在本仓库，位于 `<upstream>/audit/independent_gate_report_2026-10-15.md`）：195 行 → 271 行 → 291 行 →（第三轮 02:18–02:26：三口径整数基点复核、发布件单位错更正、新增 §10.4 末与 §10.8.2）**314 行 / 56,103 B / sha256 前缀 `e7832cc02ece`**（完整 64 位以该文件当场 `sha256sum` 为准，本文件只记前缀以免抄错）〔03:38 起为 **350 行 / 63,316 B / `9e61bcd9…`**：P0 实施轮追加 §11 并在三处加过期括注，前 153 行锚点复验仍为 `87575855…f404c6`；见 §13〕；**纯追加**（末尾 `---` + 新 §10），前 153 行锚点复验仍为 `87575855…f404c6`，合并前备份 `<upstream>/audit/_premerge_backup_independent_gate_report_2026-10-16.md`（`7cc00a69…`）。执行 P1–P5、P7，**P6 作废**（目标措辞在两份 HTML 报告里各 0 处命中），依据与我方两处数字更正记在新 §10.8。第二轮（02:05）审计了他方 `1/` 目录的自建补丁，记在 §10.8.1：他们两处数字口径写错（19 次的判据区间、对数弹性写成 2.0–2.75）、P6 那条 0 命中指令再次出现、P7 缺项；**我方 10.2 犯过同一处 19/≥40 的错并已就地改正**，同时查出核对用的脚本判据有浮点边界（名义含端点应为 22 次），记录改为并列 19／22／50 三口径，脚本本身未动。〔**本条的 19／22／50 已被第三轮推翻为 19／23／51**：那一轮的下限仍用浮点比较，漏掉名义 +40 bp 的 09/04→09/24；整数基点独立复核见 `<upstream>/_work/verify_ep.py` 与 §10.8.2。〕本目录 `us_debt/` 里放的是**副本**（他方原样快照 + 我方审计记录 + 补丁指令原件），真值源是那份审计报告；`<upstream>/ww3_section10_append_draft_2026-10-15.md`（`1a58f30c…`，56 行）未被改动，他方的补丁也**没有**被应用到任何地方（避免第三份 §10）。
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
| `_readme_build.py` | 8,028 | `dc339c3c9d39faf045c5ab1b9ca3a3ad9f2583b9fd2ecafc667cf69532735a36` | HTML→Markdown 转换器（纯标准库 + 系统 `magick`）。输入 `index.html`，输出 `README.md` + `assets/figN.svg/png`。2026-10-16 03:54 只改了第 215 行那条前置引用块的口径（P0 已落地 / P1-b、P1-c 未完成 ⇒ 数字仍未校准），7,888 → **8,028**；旧版已备份为 `_prerebuild_backup_2026-10-16/_readme_build_before_p0.py`（`c6149345…`，用 `git show HEAD:` 取回，不是我编辑后的文件） |
| `README.md` | 23,594 | `1e9b58f01840490b3678e0f2a111c10b7a834573fe772b7d8bebc7ee833ee4d5` | 由上者生成，212 行：1 个 H1 + 8 个 H2（卡标题带原标签前缀，如 `## L3 先验 ｜ 1. …`）+ 1 个 H3、**13 张 Markdown 表 / 76 行非分隔表行**（KPI 也转成表）、6 处 `![图 N](assets/figN.png)`、23 条引用块（原 note/alert + 4 条前置说明）、10 个标题。2026-10-16 02:26 重跑后字节数 22,265 → 23,002，03:54 那轮 → **23,594**；两轮的行/标题/表/图/引用块**逐项计数全部不变**（本轮 `git diff HEAD~1 -- README.md` = 8 对行，纯状态文字） |
| `assets/fig1..6.svg` | 2,919 / 1,846 / 2,685 / 3,014 / 6,363 / 5,881 | `d177d0b1` `931b3841` `474281ec` `a59e249d` `f2e18e31` `49da5e2c` | 从 HTML 里原样抽出的 SVG，仅把 `width="100%"` 替换成显式 `width`/`height`（前插会产生重复属性 ⇒ 非法 XML）。**这 6 个哈希才是图的稳定身份**：重跑步骤 4 不变。03:54 轮只有 fig2 变（`50d7e2c8` → `931b3841`），字节数 1,846 **不变**：改动是一个 `<text>` 的等宽替换（"P0 前的行为"→"旧实现"，x=242、y=159.9、font-size 13.5、text-anchor=end 均不变）；用等宽是因为 `text-anchor="end"` 的文字变长会向左溢出画布、把 "N=" 裁掉（我渲图亲眼看到才换的） |
| `assets/fig1..6.png` | 24,174 / 15,578 / 39,175 / 33,597 / 54,509 / 104,043 | `e8f8f74d` `bf2af8f2` `affbc886` `a45d2cb3` `dabc8758` `b5ab0b1a` | `magick -density 144`，尺寸 1635×375 / ×375 / ×450 / ×477 / ×546 / ×525，合计 271,076 B（02:26 轮为 271,085，差 9 B 全在 fig2 的那处标签）。**PNG 内嵌 tIME 文本块，每次重栅格化哈希都会变** ⇒ 上列哈希只对应 2026-10-16 03:54 这次重跑（旧值 `87dd5c9d e7cf44af a6b32823 8fd5edfe f3834ebc 8954ec4c`），不能当幂等性检验；幂等只看 `README.md`。**像素身份已直接验过**：本轮 6 张图与 `git show HEAD~1:assets/figN.png` 的旧图逐张 `magick … -depth 8 rgb:-` 比摘要 ⇒ **fig1/3/4/5/6 五张完全相同**（宽高、字节数也相同，纯 tIME 漂移），只有 **fig2 因上面那一处标签文字而变**；即本轮除 fig2 那一行标签外没有任何视觉/裁切变化。 |

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
- 第二轮里唯一牵到发布物的一条，如实说明：站侧 `index.html`／`README.md` 的卡 8 写"从局部低点起 ≤30 日、涨幅 40–45bp 的上行有 19 次"。复算发现 **19 是 `check_fiscal_claims.py:39` 浮点判据的值**——`0.40 ≤ Δ ≤ 0.45` 会漏掉 3 个尾数为 `0.4500000000000002` 的恰 45 bp 窗口（08/26→09/23、09/09→10/02、09/09→10/07），名义含端点应为 **22 次**（该值已作废：见 §12，整数基点复核给 **23**）；只设 ≥40 bp 下限、不设上限则是 **50 次**（同样作废，正确值 **51**；两者差的都是 09/04→09/24 那个名义 +40 bp 窗口）（其中 28 个 >45 bp 不变）。三口径已并列写进 `<upstream>/audit/independent_gate_report_2026-10-15.md` 的 10.2 与 §10.8.1。〔**该状态已被 §12 取代**：02:18 用户下指令"改，更新并重跑流水线"，页面已改成三口径并列并重跑全链，`index.html` 由 `5f1f03b6…`/50,847 B 变为 `9bc1fb1b…`/51,618 B。脚本 `check_fiscal_claims.py` 依旧未改。〕
- 一条自身操作更正，如实登记：本轮原先想用 `printf` 追加本节，双引号里的反引号被 bash 当命令替换执行了，PATH 上的 `/d/bin/README.md`、`trng` 因此被当脚本跑了一遍，并在仓库根目录留下 3 个未跟踪文件（`secret.bin` 32 B、`trng` 0 B、`⚠️` 0 B，mtime 01:50:51/01:50:55）。已 `rm -f` 删除并复验：`git status --short` 回到只有 `M MANIFEST.md`，`git ls-files` 仍 26 个，§1 表格里受控文件逐字节核对 **checked=10 bad=3**，三条 MISSING 恰是开头映射说明里已声明的三个（`ww3_final_simulation_report_2026-10-16.html` 以 `index.html` 名发布 + 两个未发布的 `us_debt/` 内部件）。教训：含反引号的中文段落一律走 Edit，不走 shell。
- **推送与线上逐字节验收**（数字绑定到提交 `1ce11a4`，本文件在 `1ce11a4` 之后又被这条记录改动，故不要把下面的哈希当"最新版"）：快进推送 `3421325..1ce11a4`，非强推，`git status -sb` 显示 `main...origin/main` 无分叉。contents API（`Accept: application/vnd.github.raw+json`，`?ref=1ce11a4`）取回字节后本地复验：`index.html` 50,847 B / `5f1f03b69d10a4f4452b5876992eb471cb80775f7f4503702b92581e0e3bf688`、`README.md` 22,265 B / `8b8dbb3763bf74dbc0082f64cdbc2feb30a8adb24473b414c4d72691fe79b7e3` 这两条做了 `cmp` 全文件比对（rc=0）；`MANIFEST.md` 当时取回 24,789 B / `c41e6b2c8901fc2c731ae8a090252ac0fb0bf328e223a9b35cc5697fdd9cf111`，与本地哈希相等，其后本条记录又继续增长过本文件的哈希与字节数——所以这里刻意不写"最新版 MANIFEST 的大小"：每次追加都会改自己的哈希，任何自记数字一落地就过期。引用 `MANIFEST.md` 必须带 ref。Pages 首页仍 200 / 50,847 B / `5f1f03b6…` ⇒ **报告首页一个字节都没因本次审计合并而变化**，这正是上面"无需重建"结论的线上佐证。


## 12. 第三轮：页面按指令重建、三口径上线（2026-10-16 02:18–02:47，含站内复现与线上验收）

- 指令原文：**"改，更新并重跑流水线"**。这是本站第一次因审计轮次而**改写发布件**——前两轮都只改记录、页面字节不动。
- 链路与产物（全部实测，非推断）：`<upstream>/release_2026-10-15/_report_build.py`（现 50,049 B / `62357533…`，改前 `784c9b8a…`）跑步骤 2 → `output/ww3_final_simulation_report_2026-10-16.html` 51,618 B / 40,218 字符 / 8 卡 / 6 图 → 覆盖 release 根目录同名副本 → `cp` 成仓库 `index.html`（三份 `cmp` 逐字节相同，均 `9bc1fb1b…`）→ 本仓库 `_readme_build.py`（`c6149345…`，脚本未改）→ `README.md` 23,002 B / `c394f72c…` + `assets/fig1..6.svg/png`。
- 内容改动 = 一处口径并列 + 两处纠错：① 卡 8 的非唯一性从单一"19 次"改为 **19／23／51 三口径并列**，并把被浮点判据判假的 4 个窗口连尾数一起列出（3 个 `0.4500000000000002` 在 45bp 上端、1 个 `0.39999999999999947` 在 40bp 下端）；② KPI 位从 `19 次` 改为 `23／51 次`，19 降为注脚；③ 量级链从 `+$4000–5500B` 改为 **+$40–55B**。第③条是**我方发布件的 100 倍单位错**（把本金基数标成利息增量），不是他方草稿的错；发现过程、推导与复现记在 `<upstream>/audit/independent_gate_report_2026-10-15.md` §10.4 末与 §10.8.2。
- **三口径就此锁定 19／23／51**：本文件 §11 与审计报告先前记的 22／50 **作废**——那次人工点数在 ≥40bp 的下限处仍用浮点比较，恰好漏掉 09/04→09/24（名义 +40bp）。复核用 `_work/verify_ep.py`（2,653 B / `8b47188a…`，整数基点、纯标准库、同一份 CSV、同一条局部低点规则），与 build 脚本（浮点+容差）是两条实现，逐点一致；`>45bp` 仍是 28 个，最大 30 日升幅仍是 +54bp，不加局部低点过滤则 ≥40bp 有 63 个。
- 自检（交付前自己看过，不是让用户验收）：六幅 `fig*.svg` 哈希**不变**（本轮未动图内文字，故 SVG 身份不变）；六幅 `fig*.png` 的 24 位 RGB 像素摘要、宽高、文件字节数与旧图**逐项相同**，只有 tIME 块变 ⇒ 无排版位移、无裁切、无新增图形。文字探针：`$4000`、`2.0–2.75` 在 `index.html` 与 `README.md` 各 **0** 命中；`19 次` 各剩 1 处；`23 次`、`51 次`、`+$40–55B`、`个端点恰在`、`0.39999999999999947` 各命中；`4 个端点` 整串在原始字节 0 命中是 `<b>4</b>` 把句子里切了，去标签版命中 1 处。改前的三份 `5f1f03b6…` 字节已备份在 `<upstream>/release_2026-10-15/_prerebuild_backup_2026-10-16/`。
- 未动的东西：模型代码与 notebook、`_report_data.json`、`us_debt/evidence/_tyc2026.csv`、`us_debt/check_fiscal_claims.py`（脚本打印的 19 仍可复现，它是我方引用值的落盘凭据）、10-15 定稿快照、`ww3_terminal_layer_gate_freeze_v1.md`、`ww3_task_priority_v1.md`、根目录 §10 草稿、`1/` 里那份他方补丁（仍未应用）。**不新增参数、不改终端层定义、不重跑模拟；P0 仍未实现。**〔本轮（第三轮）确实没动 notebook，此句作为当轮记录保留；**下一轮（§13）动了 notebook 并落地 P0**，但仍未新增参数、未改终端定义、未重跑模拟。〕
- 口径不变：卡 8 仍是**先验假设展示件**，不进三项正式摘要；报告输出仍是**代理触发比例**，不得说成"真实 WW3 的五年概率"；引用美债／财政结论时以 `<upstream>/audit/` §10 为准，不得把卡 8 当模型输入或已估计量。
- **站树自身可复现（本轮补做，发现并修了一条断链）**：本仓库跟踪的 `_report_build.py` 此前停在 `784c9b8a…` / 48,554 B，而 `index.html` 已由 `62357533…` 生成 ⇒ 站内"报告 + 可复现依赖"名不副实。已把 release 那份同步进来（现 50,049 B / `62357533…`），并在**站树内**重跑一次验证：产物 51,618 B / 40,218 字符，与 `index.html` 在归一化 `<div class="head">` 里的"生成于 …"之后**逐字符相同**（归一化后各 40,201 字符，唯一差异是 02:47 vs 02:26 这个时间戳本身；未归一化时字节数相同但哈希不同）。站树的 `us_debt/evidence/_tyc2026.csv`、`_report_data.json`、`us_debt/check_fiscal_claims.py` 与 release 树 `cmp` 逐字节相同。临时 `output/` 已删（跑前该目录不存在，`git status --short` 复干净）。⇒ 从此线上首页可只凭本仓库重算。
- **线上逐字节验收（数字绑定到提交 `7b26cfb`；本文件在那次提交里是 31,637 B，之后又被这两条改动 ⇒ 引用 `MANIFEST.md` 必须带 ref）**：走 contents API（`Accept: application/vnd.github.raw+json` + `?ref=7b26cfb1f978e1998ccd63514ecbcf9b1a84ff36`，不用 raw.githubusercontent 的 CDN 缓存）：`index.html` 51,618、`README.md` 23,002、`MANIFEST.md` 31,637、`assets/fig1.png` 24,174 四件 `cmp` 与本地**逐字节相同**；随后把 12 件 `assets/*` 全部取回放比，**identical=12 / differ=0**。Pages 首页 <https://rainchai455-cy.github.io/ww3prediction/> = HTTP 200 / 51,618 B / `9bc1fb1b`，与本地 `index.html` `cmp` 相同；线上页面内 `23 次` 命中 1 处、`$4000` **0 命中**。定稿直链 `…/ww3_final_simulation_report_2026-10-15.html` = 200 / 38,433 B / `69e78e09`，**未被本轮改动**。
- 一条自身操作更正：本轮先试 `git credential fill` 取 token 再打 API，那条命令卡在鉴权上（超时转后台，已终止）。公开仓的 contents API 匿名就能取原始字节，60 次/小时的限额足够这种十几次验收 ⇒ 以后验收线上字节直接匿名打，不去碰缓存凭据。
- **02:47 之后的收尾（03:00–03:04，只改记录、不改发布件）**：`index.html`／`README.md`／`assets/` 12 件／`_report_build.py`／`_readme_build.py` 一字节未再动；改的只有本文件（开头映射里 `index.html` 的哈希、§4"当前版实测"的过期标注、§6 审计报告版本引用与 19／22／50 的作废标注）和 `<upstream>/audit/independent_gate_report_2026-10-15.md` §10.8.2（补上 `f5fe17d` 那四件的线上验收）。审计报告因此由 55,893 B / `f52c6b11…` 变为 **314 行 / 56,103 B / sha256 前缀 `e7832cc02ece`**，前 153 行锚点复验仍为 `87575855…f404c6`。本文件自己的字节数**不在本文件内登记**（自指：再改一次就失效），需要时对站内 `MANIFEST.md` 当场 `stat`／`sha256sum`；引用站内 `MANIFEST.md` 一律带 ref。


## 13. P0 实施轮对本站快照的影响：发布件零改动，站内三句状态文字过期（2026-10-16 03:20–03:45）〔2026-10-16 03:54 起本节的"发布件零改动"只对本节所记的 03:20–03:45 窗口成立：随后一轮按指令"同意默认口径，剩下的事项都推进"重建并提交了页面与 README，全部新哈希见 §14〕

- **指令与范围**："推进 P0 任务：完成三态标签（确认发生／确认未发生／证据不足）的实现，这是报告升级的前提。"＝首次授权改模型代码，范围只到 `<upstream>/www3v0.3/ww3_risk_model_v0_3.ipynb` 的 cell 6／7／9。**没有**授权重跑发布流水线、重打包 zip、或再推一次 GitHub，本轮因此一件发布件都没动。〔下一轮（03:54，§14）拿到了这三项授权，本条只描述 P0 那一轮当时的范围〕
- **notebook 实测**：`www3v0.3/ww3_risk_model_v0_3.ipynb` 与 bundle 同名副本 **70,612 B / `d8c53ee6…`**、`cmp` 逐字节相同；改前备份 `*.ipynb.pre-p0.bak` = 46,528 B / `e8fcdb29…`。验收：`_work/verify_p0.py` 从 notebook 读出 cell 7／9／11 源码执行，**`8/8 checks pass`**（`_work/p0_acceptance_output.txt`），三条 PASS 串齐（`7 pair-aware label tests` / `P0 three-state label tests U8-U13` / `as-of feature availability test`），`ww3_task_priority_v1.md` §1 表格的 17.07%／0.42%／**40.2×** 由代码复现。细节在 `<upstream>/audit/independent_gate_report_2026-10-15.md` §11。
- **发布件逐字节未变（本轮末实测）**：`index.html` 51,618 B / `9bc1fb1b…`、`README.md` 23,002 B / `c394f72c…`、`_report_build.py` 50,049 B / `62357533…`、`_readme_build.py` 7,888 B、`assets/` 12 件、定稿 `ww3_final_simulation_report_2026-10-15.html` 38,433 B / `69e78e09…`。⇒ 线上 Pages 与 `?ref=f70b84c` 的验收数字全部照旧有效，本轮不产生新的线上验收义务。
- **站内过期的句子（三处，改它们＝重建＋覆盖线上件）**：① `README.md` 第 3 行前置引用块"`label_status` 三态（P0）未实现"；② `README.md` 第 129 行"标签三态未实现：classifier 里的 `_as_bool` 与 `.fillna(False)` 把『证据不足』实现成『确认未发生』"；③ `README.md` 第 205 行任务表 P0 状态列"未实现"。三者都由 `_readme_build.py:215`／`_report_build.py:396`／`_report_build.py:596` 生成 ⇒ 更正要走脚本重生成，不手改 HTML/MD。本文件（`MANIFEST.md`）第 3 行与 §12 末条已按"就地加括注、原文保留"处理。〔2026-10-16 03:54：这三句已按本条指明的路径（改 `_readme_build.py:215`／`_report_build.py:396`／`:596` 后重跑流水线，不手改 HTML/MD）重生成并抹除；本轮 `grep -c 未实现` 在 `index.html` 与 `README.md` 均为 **0**，见 §14〕
- **结论不因此变化**：报告的停止条件写的是"P0 **与** P1-b **与** P1-c 完成前不升级为现实风险预测"。本轮只落地 P0 这一条，P1-b（时间外验证）与 P1-c（当前起点证据审核）未完成 ⇒ 页面"不升级"的判定照旧；`positive_windows = 4` 全来自合成用例，**历史可核验正例仍为 0**。
- **站仓 git 状态**：本轮只追加了本文件这一处站内改动（§13 + 三条括注），`index.html`／`README.md`／`assets/`／两份 build 脚本未动。**HEAD 仍 `f70b84c`，工作树因此为脏**（1 个文件 modified、未提交、未推送）——提交与推送属"影响他可见的共享状态"，等他点头再做；他要的默认动作应是"记录提交 + 站内状态文字重生成 + 一次发布"三件一起做，因为只提交本文件会让 `README.md` 的"未实现"继续挂在首页上。〔2026-10-16 03:54–04:10：三件一起做的那条路已走通，见 §14〕

## 14. 第四轮：状态行重生成、bundle 重打包、他方文档括注 ⇒ 三件一起做（2026-10-16 03:45–04:10）

- **指令**："同意默认口径，剩下的事项都推进"。默认口径＝`negative` 定义为 `coverage_verified_days > 0`（其余两态由 cell 7 的三值辅助函数 `_tri`／`_as_tribool` 给出）。三项＝① 重生成发布状态行并提交推送，② 重打包 `www3v0.3/ww3_risk_model_v0_3_bundle.zip`，③ 更正他方 V0.3 文档里三句"未实现"。冻结文件 `ww3_terminal_layer_gate_freeze_v1.md` 与 `ww3_task_priority_v1.md` 不在清单内，未动。

- **① 构建脚本改动（只改状态文字，不改任何数字）**：`_report_build.py` 六处——卡 6 标题改为"6. 可靠性缺口 P0 已闭合（2026-10-16）：不可核验暴露不再进负例分母"、副标题点名 notebook cell 7／`d8c53ee6…`／"修复前后对照，不是现存缺陷"、标签 `tag="已闭合"`、KPI 子串 `N=3,518（P0 前的行为）`、图 2 图例 `N=3,518（旧实现：缺失折成负例）`、任务表 P0 行"已实现（2026-10-16，六条判据 8/8 实测通过）"，停止块重写为"P0 … 已于 2026-10-16 完成并通过 §1 六条判据（8/8）；但在 P1-c 与 P1-b 完成之前 … 仍不升级为现实风险预测。历史可核验终端正例仍为 0。" 脚本 50,049 → **50,537 B / `0c3bd8a687bea427e734ebf00abd215a5349869f47047c8929545bb6e3a5d105`**；发布目录与站树两份 `cmp` 逐字节相同。`_readme_build.py` 只改第 215 行前置引用块 ⇒ 7,888 → **8,028 B / `dc339c3c…`**（§9 表已更新）。

- **① 产物**：`index.html` 51,618 → **52,106 B / `5517b3058d1600adf092243bef86f5fa4f83ba9e8d13dc0befdbe1b11ca98fd2`**（改前一份已存 `_prerebuild_backup_2026-10-16/site_index_before_p0.html`）；`README.md` 23,002 → **23,594 B / `1e9b58f0…`**（改前存 `README_before_p0.md`）。`git diff --stat HEAD~1 -- README.md index.html assets/`：**9 个文件变化、14 增 14 删**——README 8 对行、`index.html` 5 对行、`assets/fig2.svg` 1 对行，六张 PNG 只有 fig2 的字节数变（15,587 → 15,578）；整个 `49a6a23` 是 12 件 / 38 增 28 删，多出的两对文件是两份构建脚本本身。

- **数字没动的证据（同一条 stderr 逐字节一致）**：重跑 `_report_build.py` 的自检行仍是 `ceiling=17.07% fold=0.425% r3=9.21 rp21=5.72 rrho=6.13 spread=1.095`、`EP … = 19/23/51/28/4`、`EL inc=[40,55]B … ord=3.5986`；`check_fiscal_claims.py` 未重跑（其依赖 `us_debt/evidence/_tyc2026.csv` 与卡 8 计算逻辑均未被本轮触碰），原样输出 `check_output_2026-10-16.txt` 继续有效。另：`grep -c '未实现'` 在 `index.html` 与 `README.md` 均为 **0**，`grep -c '\$4000'` 亦为 0（防串位）。

- **一处自查拦下的缺陷（已修）**：图 2 图例最初改成"P0 前的实现"，`text-anchor="end"` 让文字向左长出一格，把同一行的 `N=` 裁到画布外；我自行渲染并看了裁片才发现，换成等宽的"旧实现"后 fig2.svg 字节数 1,846 **不变**。fig1/3/4/5/6 五张 PNG 与改前 `magick … -depth 8 rgb:-` 摘要完全相同 ⇒ 除 fig2 那一行标签外零视觉变化（身份见 §9 表）。

- **站内复现**：在站树重跑 `_report_build.py`，产物与发布目录那份经时间戳归一后各 **52,037 B** 且逐字节相同 ⇒ 站树携带的构建脚本与它发布的这份 `index.html` 同源（第三轮的依赖链教训）。

- **② bundle zip**：`_work/repack_bundle.py`（`zipfile` + `time.localtime`，本机 venv 的 `os` 无 `localtime`；固定 11 个文件名顺序、`external_attr=0o644<<16`；先断言 `*.ipynb.pre-p0.bak` 存在、且目录内非 .bak 文件集合与压缩包内集合相等再压）。旧 25,894 B / `210c3e67…` 保留为 `.zip.pre-p0.bak`；新 **35,058 B / `22d5e03928f26c676619e239f78b717a06cf3b020f068a67d7d5fc6e01e8dba5`**，解包后 11/11 件与目录 `cmp` 相同。

- **③ 他方文档括注（原文保留、只在句尾加〔〕）**：`README_ww3_model_v0_2.md:34` → 4,142 B / `4c491e9d…`；`www3v0.3/ww3_audit_decisions_v0_3.md:36` 与其 bundle 副本 → 两份各 5,254 B / `5b5bc55b…`（`cmp` 相同）；`bundle/README_ww3_model_v0_3.md:51` → 6,929 B。

- **git**：站内 12 件改动已提交为 **`49a6a23`**（"P0 已落地：重生成状态行（六条判据 8/8），数字与其余五图未变"，38 增 28 删）；本文件（§14 + §9 表更新 + 括注）作为紧随其后的第二个提交一起推送，该 commit id 无法写进本文件自己那一节，记在 `<upstream>/release_2026-10-15/MANIFEST.md` §10。推送后的线上验收走匿名 contents API（`Accept: application/vnd.github.raw+json`、带 `?ref=`），不触碰缓存凭据。

- **口径不变项**：`positive_windows = 4` 全部来自合成用例，历史可核验终端正例仍为 **0**；页面"不升级为现实风险预测"的判定因 P1-b／P1-c 未完成而照旧（§13 末条结论未变）。
