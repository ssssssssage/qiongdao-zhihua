# 上游 PPO-GNN 项目与琼岛智划展示系统一致性审计

本报告用于核对项目 B（琼岛智划展示系统）对项目 A（学长原始 DRL urban planning 项目）的算法底座、数据含义、图例、输出结果和技术表述是否准确。审计目标不是要求项目 B 照抄项目 A，而是避免参赛材料出现不真实、不可复现或容易被评委质疑的表述。

## 一、审计结论摘要

项目 A 是一个完整的研究型深度强化学习城市规划项目，包含 PPO 训练、SGNN/GNN 图状态编码、规划环境、奖励函数、训练入口、推理入口和最终 GeoJSON 规划结果。

项目 B 当前更准确地说是一个 **展示端与解释端系统**：它读取项目 A 离线生成或派生的规划结果图片和统计 CSV，再叠加自然语言需求解析、多角色诉求模拟、本地政策文本检索解释和 Markdown 报告生成。项目 B 当前没有把项目 A 的 PPO/SGNN 训练与推理流程完整集成到展示系统中，也不应被表述为比赛现场实时训练或实时生成新规划图。

最需要立刻修正的是：明文 API Key、0 字节/无效数据文件、图例颜色与项目 A `city_config.py` 不一致，以及“PPO-GNN 规划引擎”“RAG政策解释”“多Agent协同”等表述过强的问题。

## 二、项目 A 原始能力摘要

项目 A 的核心能力如下：

| 能力 | 项目 A 中的位置 | 审计判断 |
|---|---|---|
| PPO 训练入口 | `urban_planning/train.py` | 存在真实训练入口 |
| 推理/评估入口 | `urban_planning/eval.py` | 存在真实推理与基线评估入口 |
| PPO Agent | `urban_planning/agents/urban_planning_agent.py`、`khrylib/rl/agents/agent_ppo.py` | 存在 PPO 更新、采样、优势估计和 checkpoint 保存 |
| SGNN/GNN 状态编码 | `urban_planning/models/state_encoder.py` | 存在图节点、边、mask、GCN 聚合和 attention |
| 环境与 step 逻辑 | `urban_planning/envs/city.py` | 存在 land use / road 阶段、动作、奖励、done 逻辑 |
| 图结构建模 | `urban_planning/envs/plan_client.py` | 使用空间邻接生成 graph features |
| 奖励函数 | `city.py`、`plan_client.py` | 包含 life circle、greenness、road network、concept 等 |
| 输入数据 | `urban_planning/cfg/test_data/...` | `init_plan.pickle` + `objectives.yaml` |
| 最终输出 | `results/dhm.geojson`、`results/hlg.geojson` | A 提供 HLG/DHM 最终 GeoJSON 规划结果 |

需要注意：项目 A 的 HLG/DHM 真实场景配置里 `skip_road: true`、`road_network_weight: 0.0`，因此不能把当前 HLG/DHM 结果说成“同时完成用地与道路 PPO 联合优化”。更准确说法是：A 的框架支持用地与道路规划，但当前 HLG/DHM 配置主要展示 land-use 规划结果，路网部分更多来自已有道路/边界或结果数据。

## 三、项目 B 新增能力摘要

项目 B 的新增能力主要在展示与解释层：

| 能力 | 项目 B 中的位置 | 审计判断 |
|---|---|---|
| Streamlit 展示端 | `app/streamlit_app.py` | 展示页面、图表、交互入口 |
| 自然语言需求解析 | `parse_user_need`、`call_deepseek_parser` | DeepSeek 调用失败时回退到规则解析 |
| 多Agent协同分析 | `build_rule_agent_logs`、`generate_agent_logs` | 文本模拟居民/政府/商业/协调器观点 |
| 本地政策检索 | `load_policy_documents`、`retrieve_policy_chunks` | 基于本地 txt 和关键词打分的轻量级检索 |
| 政策解释生成 | `generate_policy_explanation` | LLM 或规则模板生成解释 |
| 规划结果展示 | `outputs/*.png`、`data/*_summary.csv` | 读取离线图片和统计 CSV |
| 报告生成 | `build_report` | 生成可下载 Markdown 报告 |
| 资产生成脚本 | `generate_assets.py` | 从 A 的 `results/*.geojson` 派生 PNG 和 CSV |

因此，项目 B 应被定位为：**基于上游 DRL/PPO-SGNN 离线规划结果的海南场景化展示、解释和报告生成系统**。

## 四、两个项目的对应关系

| 项目 A 原始能力 | 项目 B 对应内容 | 一致性判断 | 建议表述 |
|---|---|---|---|
| PPO/SGNN 算法训练 | B 无完整训练集成 | 部分继承，主要是结果展示 | “参考/基于上游 PPO-SGNN 离线规划结果” |
| 初始地块、道路、交叉点、objectives | B 页面用户文本与场景权重 | 数据入口不同 | “展示端文本输入用于解释，不直接驱动 PPO 训练” |
| HLG/DHM GeoJSON 最终结果 | B 的 PNG/CSV | 派生关系成立 | “从上游 GeoJSON 派生展示图和统计表” |
| city_config type 定义 | B 的图例表 | 类型基本对，颜色不对 | “type 含义来自 A，颜色为展示端配色/或按 A 修正” |
| life circle / greenness 奖励 | B 的生活圈、绿地解释 | 概念相关，但不是实时评分 | “用于解释规划目标，不代表现场重新计算 PPO reward” |
| Road network reward | B 文案写交通连通 | 对 HLG/DHM 结果偏强 | “框架支持交通连通评价；当前展示结果以离线结果说明为主” |
| 无海南场景数据 | B 的海南自贸港/三亚场景 | B 新增解释层 | “海南场景化应用展示，不声称底层训练数据来自海南” |

## 五、需要修正的代码、文案、图例、报告描述

### 1. 必须修正的代码与文件问题

| 文件/目录 | 当前问题 | 风险 | 建议修正 |
|---|---|---|---|
| `app/import requests.swift` | 第 3 行存在明文 `sk-...` API Key | 严重安全风险，比赛材料泄露密钥 | 立即撤销该密钥；删除该文件或改为环境变量读取 |
| `data/dhm.geojson` | 0 字节 | 无效 GeoJSON，容易被质疑数据真实性 | 从 A 的 `results/dhm.geojson` 复制有效文件，或删除并说明页面不读取它 |
| `data/hlg.geojson` | 0 字节 | 无效 GeoJSON | 同上 |
| `outputs/report_demo.md` | 0 字节 | 报告样例为空 | 补充真实样例或删除无效文件 |
| `docs/说明书.docx` | 0 字节，Word 结构损坏 | 材料完整度风险 | 重新生成有效说明书，或不要提交该文件 |
| `docs/~$解说.docx` | Word 临时锁文件 | 材料不整洁 | 删除临时文件 |
| `engine_original/` | 空目录 | 不能证明算法集成 | 补充说明“上游项目独立存放”，或放置 README 指向 A 的路径与来源 |
| `test_deepseek_api.py` | 默认 Base URL/Model 与 `streamlit_app.py`、`AI_TASK.md` 不一致 | 调试与展示说明不一致 | 统一默认 URL 和模型，或说明只是旧测试脚本 |

### 2. 必须修正的图例问题

项目 A 的真实 type 映射来自 `urban_planning/envs/city_config.py`：

| type | A 中英文名 | 中文含义 | A 原始颜色 |
|---|---|---|---|
| 0 | outside | 外部区域 | black |
| 1 | feasible | 可规划/剩余可建设空间 | white |
| 2 | road | 道路 | red |
| 3 | boundary | 边界 | lightgreen |
| 4 | residential | 居住用地 | yellow |
| 5 | business | 商业用地 | fuchsia |
| 6 | office | 办公用地 | gold |
| 7 | green_l | 大型绿地 | green |
| 8 | green_s | 小型绿地/剩余绿地 | lightgreen |
| 9 | school | 学校 | darkorange |
| 10 | hospital_l | 大型医院 | blue |
| 11 | hospital_s | 小型医院/社区医疗 | cyan |
| 12 | recreation | 休闲娱乐 | lavender |
| 13 | intersection | 道路交叉点/路网节点 | A 中为独立常量，未进入 `TYPE_COLOR_MAP` |

B 当前 `LAND_USE_LEGEND` 的中文类型基本正确，尤其 **type=4 是居住用地，不是绿地**。但 B 当前颜色不符合 A 的 `TYPE_COLOR_MAP`。例如：

| type | B 当前颜色 | A 真实颜色 | 需要修正 |
|---|---|---|---|
| 1 | 蓝色 | white | 改为白色，或注明展示端重绘配色 |
| 2 | 蓝色 | red | 改为红色 |
| 4 | 绿色 | yellow | 改为黄色；不要让评委误以为 type=4 是绿地 |
| 5 | 红色 | fuchsia | 改为紫红色/洋红 |
| 6 | 紫色 | gold | 改为金色 |
| 7 | 棕色 | green | 改为绿色 |
| 8 | 棕色 | lightgreen | 改为浅绿色 |
| 9 | 粉色 | darkorange | 改为深橙 |
| 10 | 灰色 | blue | 改为蓝色 |
| 11 | 黄绿色 | cyan | 改为青色 |
| 12 | 青色 | lavender | 改为淡紫色 |

`generate_assets.py` 当前使用 GeoPandas 默认 categorical 配色，未使用 A 的 `TYPE_COLOR_MAP`。如果页面继续声称“正式映射依据来自 city_config.py”，则必须同步修改 `generate_assets.py` 和 `streamlit_app.py` 中的图例色值。否则应改成：“type 含义来自上游 `city_config.py`，当前颜色为展示端重绘配色，仅用于区分类型。”

### 3. 必须修正的页面文案

以下页面文案建议降级为更严谨表达：

| 当前说法 | 风险 | 建议改法 |
|---|---|---|
| “PPO-GNN 规划引擎” | 暗示 B 内置完整训练/推理引擎 | “上游 PPO-SGNN 离线规划结果展示” |
| “PPO-GNN深度强化学习规划引擎” | 容易被追问现场训练和模型权重 | “参考上游 DRL/PPO-SGNN 算法底座，展示端读取离线生成结果” |
| “AI + PPO-GNN” | 可保留但偏营销 | “AI 解释 + PPO-SGNN 离线结果” |
| “多Agent协同分析机制” | 暗示多 agent 真正参与空间优化 | “多角色诉求模拟与协调解释” |
| “RAG政策知识库” | 当前只是本地 txt 关键词检索，非向量库/实时权威库 | “轻量级本地政策文本检索增强解释” |
| “15分钟生活圈优化方案” | B 未重新计算完整生活圈优化 | “围绕 15 分钟生活圈目标的解释与展示方案” |
| “面向海南自贸港社区治理” | 可说，但底层空间数据不是海南 | “面向海南自贸港语境的展示与政策解释适配” |

### 4. 必须修正的报告描述

`build_report()` 中的报告描述应避免把展示端解释权重写成 PPO 训练奖励。建议修正方向：

| 报告位置 | 当前风险 | 建议写法 |
|---|---|---|
| “PPO-GNN离线规划流程说明” | “医疗、教育、商业、交通”等目标被写成底层奖励，和 A 的真实 reward 不完全一致 | “上游 reward 主要包含 life circle、greenness、road network、concept 等；展示端将其转译为医疗、教育、商业、绿地、交通等解释维度” |
| “输出结果：指标权重与方案解释” | 容易混淆算法输出和展示端生成内容 | “算法输出为空间规划结果；指标权重与方案解释由展示端生成” |
| “多Agent协同分析” | 容易被误解为多智能体强化学习 | “LLM/规则驱动的多角色诉求模拟，不参与 PPO 动作选择” |
| “RAG政策与合规解释” | 当前政策文本为本地摘要 | “基于本地政策摘要文本的检索增强解释，非实时政策数据库” |
| “Linux / WSL2 端用于强化学习训练” | 如果 B 未附训练脚本/权重，表述偏强 | “上游算法训练可在 Linux/WSL2 环境复现；当前仓库展示端不执行训练” |

## 六、数据文件有效性审计

| 文件 | 状态 | 判断 |
|---|---|---|
| `outputs/dhm_result_clean.png` | 有效 PNG | 可展示 |
| `outputs/hlg_result_clean.png` | 有效 PNG | 可展示 |
| `data/dhm_summary.csv` | 有效 CSV，13 行 | 与 A 的 DHM GeoJSON 类型统计匹配 |
| `data/hlg_summary.csv` | 有效 CSV，13 行 | 与 A 的 HLG GeoJSON 类型统计匹配 |
| `data/dhm.geojson` | 0 字节 | 无效 |
| `data/hlg.geojson` | 0 字节 | 无效 |
| `outputs/report_demo.md` | 0 字节 | 无效样例 |
| `docs/说明书.docx` | 0 字节/损坏 | 无效材料 |

项目 B 页面目前主要读取 PNG 和 CSV，因此页面展示本身可运行；但提交材料中出现 0 字节 GeoJSON 和损坏 DOCX，会直接损害数据真实性和材料完整度。

## 七、功能表述可用性判断

| 表述 | 是否建议使用 | 推荐边界 |
|---|---|---|
| PPO-GNN 规划引擎 | 谨慎使用 | 改为“上游 PPO-SGNN 离线规划算法底座” |
| 深度强化学习规划引擎 | 可以说，但需限定 | “上游项目包含 DRL 训练与推理；本展示端读取离线结果” |
| 多Agent协同 | 可以说，但需降级 | “多角色诉求模拟与协调解释” |
| RAG政策解释 | 可以说，但需限定 | “本地政策文本检索增强解释” |
| 15分钟生活圈 | 可以说 | “围绕 15 分钟生活圈目标进行解释与展示” |
| 自动生成规划报告 | 可以说 | 当前确实能生成 Markdown 报告 |
| 面向海南自贸港社区治理 | 可以说 | 说明是展示场景和政策语境适配，不是底层训练数据来源 |

## 八、参赛风险清单

### 1. 原创性边界

风险：项目 A 是上游研究项目，B 若直接称“自主研发 PPO-GNN 引擎”会被质疑原创性。

建议：明确写成“算法底座参考/复用上游开源 DRL urban planning 项目；本项目原创工作集中在海南场景化展示、自然语言交互、多角色诉求解释、本地政策检索和报告生成。”

### 2. 算法真实性

风险：B 仓库未集成完整训练/推理流程，`engine_original` 为空。

建议：不要说“现场训练”“现场推理生成图”。答辩时主动说明“展示端读取离线结果，保证稳定演示；上游算法可单独复现。”

### 3. 数据真实性

风险：B 的 GeoJSON 是 0 字节；PNG/CSV 是有效派生物，但需要说明来源。

建议：补齐有效 GeoJSON 或删除无效文件；README 说明 PNG/CSV 由 `generate_assets.py` 从 A 的 `results/*.geojson` 派生。

### 4. RAG 真实性

风险：当前不是向量数据库，也不是联网权威政策库，而是本地 txt + 关键词评分 + LLM/模板。

建议：称为“轻量级 RAG”或“本地政策文本检索增强解释”，并列出本地政策文件。

### 5. 移动应用形态

风险：当前是 Streamlit Web，不是原生 App。`app/import requests.swift` 文件名反而会造成误解。

建议：不要称“移动应用”；可以称“Web 展示系统”或“可在移动浏览器访问的 Web 原型”。

### 6. 安全风险

风险：明文 API Key 是最高优先级安全问题。

建议：撤销泄露密钥、删除明文文件、统一使用环境变量，并在提交前全仓搜索 `sk-`、`api_key = "`、`Bearer`。

### 7. 材料完整度

风险：0 字节文件、损坏 DOCX、空目录会被认为项目整理不完整。

建议：提交前清理临时文件，补充 README、说明书、架构图、数据来源说明、上游引用和许可证说明。

## 九、答辩中可以放心说的表述

可以使用以下表述：

- “底层算法参考上游 DRL urban planning 项目，该项目包含 PPO、SGNN 图状态编码、规划环境和奖励函数。”
- “当前参赛系统是展示端与解释端，读取上游离线生成的规划结果图和统计表，不在比赛现场训练模型。”
- “type 含义来自上游 `city_config.py`，其中 type=4 是居住用地，type=7/type=8 才是绿地。”
- “多Agent模块用于模拟居民、政府、产业运营方等多方诉求，帮助解释方案取舍。”
- “政策解释模块基于本地政策文本做检索增强，并在 API 不可用时回退到规则模板。”
- “自动报告生成是展示端能力，可把场景解析、规划图说明、多角色分析和政策解释整合成 Markdown 报告。”

## 十、答辩中不建议说的表述

不建议使用以下表述：

- “我们现场实时训练 PPO-GNN。”
- “用户输入后系统现场推理生成新的规划图。”
- “项目 B 已完整集成上游 PPO-GNN 训练引擎。”
- “底层训练数据来自海南真实社区。”
- “RAG 接入了权威实时政策数据库。”
- “多Agent共同求解空间规划方案。”
- “这是一个原生移动应用。”
- “HLG/DHM 结果完成了用地和道路的联合 PPO 优化。”

## 十一、建议写入 README / 说明书 / PPT 的技术架构描述

推荐写法：

> 琼岛智划采用“离线算法层 + 展示解释层”架构。离线算法层参考上游 DRL urban planning 项目，在 Linux/WSL2 环境中基于初始空间地块、道路、交叉点和规划目标文件，使用 PPO 与 SGNN 图状态编码生成社区用地规划结果。展示解释层基于 Streamlit 读取已生成的 GeoJSON 派生图片和统计 CSV，结合用户自然语言需求解析、多角色诉求模拟、本地政策文本检索增强解释，生成可视化页面和 Markdown 规划分析报告。当前版本不进行现场模型训练；海南自贸港与三亚场景属于展示端场景化解释与政策适配。

## 十二、推荐修正优先级

### P0：提交前必须处理

1. 撤销并移除明文 API Key。
2. 修正或删除 0 字节 GeoJSON、空报告、损坏 DOCX。
3. 修正图例颜色，或明确“颜色为展示端配色”。
4. README/PPT 明确“展示端读取离线生成结果，不现场训练”。

### P1：强烈建议处理

1. 补充有效 README，说明上游来源、派生数据、展示端新增能力。
2. 统一 `test_deepseek_api.py`、`AI_TASK.md`、`streamlit_app.py` 中的默认 API Base URL 和模型名。
3. 把“多Agent协同”改成“多角色诉求模拟与协调解释”。
4. 把“RAG政策解释”改成“轻量级本地政策文本检索增强解释”。
5. 在报告模板中区分“算法输出”和“展示端解释输出”。

### P2：后续增强

1. 在 B 中补充一个只读的 `engine_original/README.md`，说明上游项目路径、引用论文、许可证和复现命令。
2. 增加数据校验脚本，自动检查 0 字节、无效 GeoJSON、无效 CSV、无效 PNG。
3. 增加“技术边界说明”页面，主动说明展示端不现场训练。
4. 若时间允许，接入真正的上游推理脚本或保存模型权重，让“离线推理”可在本地复现。
