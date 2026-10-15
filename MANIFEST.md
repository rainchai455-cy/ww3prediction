# WW3 最终报告交付目录（release_2026-10-15）

建立时间 2026-10-16 00:04。本目录是自包含的**报告 + 执行依赖**快照，不是模型实现目录。里面没有任何代码通过 P0；`label_status` 三态仍未实现。

> **本仓库（公开站）与本地交付目录的映射**：本文件是从交付目录带过来的记录，表中路径按交付目录写。两处差异：① `index.html` = 表中的 `ww3_final_simulation_report_2026-10-16.html`（同字节、同哈希 `08acf514…`）；② 表中 `us_debt/section10_draft_asis.md` 与 `us_debt/pending_patch.md` 未随本仓库发布（内部评审过程），其余 9 个文件逐字节一致。文中 `<upstream>/` 指本地未发布的上游目录。

## 1. 目录内容

| 路径 | 字节 | sha256 | 角色 |
|---|---|---|---|
| `ww3_final_simulation_report_2026-10-15.html` | 38,433 | `69e78e0965460389b7d3246b3f5778dc8fe2c8f6f7e279e4eb76fc9388664202` | **定稿快照**（与 `<upstream>/` 同名文件逐字节一致，本目录内不参与被覆盖） |
| `_report_sim.py` | 5,102 | `adc9364f6d21b9d14e982e44d2e4c78feace96cf88ea3d191391a8a2df2eef8b` | 蒙特卡洛驱动（27 个 run，同批种子） |
| `_report_build.py` | 48,594 | `d850d072f16ff1a184dd3b4fe9ad7d046ce9a04644293d424915aee5f5710be9` | 图表/正文构建（纯 SVG，无绘图库依赖）。**本目录版含卡 8「美债补充项」163 行，与原工作区脚本不再等价**（见 §3） |
| `ww3_final_simulation_report_2026-10-16.html` | 50,847 | `08acf514022930739e683ab56533177e6ac8313c6a15887769754610efa7aa5a` | **当前版报告（8 卡 / 6 图）**，= 上面 build 脚本跑出的产物；含卡 8 |
| `_report_data.json` | 6,581 | `910c9309f71ac480bbd3973adec9e702767c076769ba5b32b22737acca4d5ed0` | 唯一中间数据：全部结果 + 每个 run 的种子 + 代理暴露率 |
| `us_debt/evidence/_tyc2026.csv` | 16,067 | `bec74a6c0f118755eee4855ab6dc4fa924e6c08b6361e23b6c2e2590f2cb271c` | 一手证据（Treasury 日度曲线 2026，197 观测）。不是 `_report_sim.py` 的依赖，但**是 `_report_build.py` 卡 8 的构建期依赖**：缺文件即 `SystemExit`，卡内每个收益率数字都由它现算 |
| `us_debt/check_fiscal_claims.py` | 3,189 | `8392f5e50fbab5855450ae14703bd0b106cf9f4b820ad7062a291013fbb57c13` | 美债部分唯一可执行核验：从上面那个 CSV 重算正文每个数字（纯标准库，无 numpy、无网络） |
| `us_debt/evidence/check_output_2026-10-16.txt` | 1,242 | `0613e5bad9fcad368d4bf0815652af6a595f1b2146f0ef1b88a3ec1ea4252c5a` | 上述脚本上次运行的原样输出（21 行），供离线对账 |
| `us_debt/audit_findings.md` | 9,472 | `dfe2166c0cdc594c9777158f3b51f1c14a132e8c3e8aac33b18a91fefd84bee7` | 美债模块审计记录（出处门 7 项、不可识别判定、90% 分母、量级检验、三条阻塞、顺序表；71 行） |
| `us_debt/section10_draft_asis.md` | 7,640 | `1a58f30cc0391d9c16335302d7b7298e394bc82a7c74b0eec632fe0c9d1eef17` | 他方 §10 草稿的**原样快照**（未改一字），含 2 处待改，见 `pending_patch.md` P1–P3 |
| `us_debt/pending_patch.md` | 4,636 | `2716b8c62e3df6d4934e713723107ea0aba6cda8e716f90fac980c5f6645bbd3` | 7 条定点补丁（3 必改 + 4 建议），**尚未执行** |
| `output/`（重建后生成） | — | — | 你自己重跑时报告的落点；刻意与定稿分开，避免覆盖 |

依赖闭包：`numpy`（仅 `_report_sim.py`）+ 标准库（math/json/time/os/csv/html/datetime）。**无 matplotlib、无 pandas、无网络访问、无 notebook 参与**；全部图形是构建脚本自己拼的内联 SVG，产物是单文件 HTML（除 SVG 命名空间 URL 外无任何外部引用，可直接作静态首页）。

## 2. 复现命令（实测环境）

```
解释器  D:\OCR\PaddleOCR\.venv\Scripts\python.exe   python 3.12.10 / numpy 2.3.5
步骤 1  <python> _report_sim.py      # 约 158 s，覆写本目录 _report_data.json
步骤 2  <python> _report_build.py    # 秒级，读 _report_data.json + us_debt\evidence\_tyc2026.csv，写 output\ww3_final_simulation_report_2026-10-16.html，不碰 10-15 定稿快照
步骤 3  <python> us_debt\check_fiscal_claims.py   # 秒级，只读 us_debt\evidence\_tyc2026.csv，重算美债部分全部数字，不写文件
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
- **当前版（含卡 8）实测**：`_report_build.py` `d850d072…` 跑步骤 2 → `output/ww3_final_simulation_report_2026-10-16.html` 50,847 B / 39,740 字符 / 8 张卡 / 6 幅内联 SVG；根目录副本与 `output/` 那份同哈希 `08acf514…`。卡 8 的 18 个探针串全部命中（19 次、+54bp、5.19%、不可识别、65.7%、92.0%、1.70、1.95、2.67、×1.212、4811、3.60 个数量级、三次出现、indeterminate_resolution、+42bp、+58bp、Lemke、403）。
- **界面自检**：headless Edge 1180×9500 截图，`-trim` 内容边界 1120×7138+30+26；卡 8 区域逐块目视过。修掉的三处排版缺陷：①右上 "10/05 峰 5.31%" 原先越出画布被裁；②橙色 "4.39%（03/20、03/24、05/01 三次出现）" 长标签压在折线上，改为 "4.39%（三次出现）"，三个日期改由正文注 ② 承载（`AT439` 现算）；③ 5 个 KPI 原先 4+1 换行、第 5 个被拉成整行，改内联 `flex:1 1 186px` 后单行等宽（页高 7229→7138）。
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
- §10 仍未合并进审计报告：`audit/independent_gate_report_2026-10-15.md` 仍 195 行、前 153 行锚点 `87575855…f404c6` 未变。本目录 `us_debt/` 里放的是**副本**（他方原样快照 + 我方审计记录 + 未执行补丁），原仓库根目录的 `ww3_section10_append_draft_2026-10-15.md` 未被本目录操作改动。
- `ww3_risk_model_v0_3_bundle.zip`（未重打包，与 bundle 目录不一致；重打包=覆盖既有产物，需另下指令）。

## 7. 已知未修项（沿用他 V0.3 工作单，本目录不掩盖）

- 报告正文写"六个"标签测试，代码实为 7 个（`PASS: 7 pair-aware label tests`）。
- 终端窗口上限代码 `>89` 天 vs 文档 `≤90` 天。
- `_as_bool` / `.fillna(False)` 仍把"证据不足"折成负例；`raise ValueError` 路径不产出状态。
