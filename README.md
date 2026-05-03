# 琼岛智划

**面向海南自贸港社区治理的 AI 多智能体协同规划展示系统**

## 1. 项目简介

琼岛智划是一个面向海南自贸港、三亚滨海社区、候鸟老人、年轻家庭、游客短租等社区治理与规划展示场景的 AI 辅助系统。系统支持用户用自然语言描述社区规划诉求，并结合场景识别、指标权重、规划结果图、政策证据链和多Agent解释，形成可展示、可下载的规划分析结果。

本项目主要用于参赛展示和原型验证，重点呈现“离线空间规划结果”与“在线智能解释能力”的结合方式，帮助评委和使用者理解不同社区场景下的公共服务配置、空间治理重点和合规解释逻辑。

## 2. 系统定位

本系统采用 **“离线规划引擎 + 在线智能解释”** 架构。

展示端读取上游 PPO/SGNN 项目离线生成的规划结果图、GeoJSON 和统计表，不进行现场训练，也不实时生成新的 PPO/SGNN 规划结果。用户输入主要用于场景识别、需求解析、政策解释、多Agent分析和报告生成，不直接改变底层空间规划结果。

## 3. 技术架构

- **离线算法层**：参考上游 DRL urban planning 项目，包含 PPO、SGNN/GNN 状态编码、规划环境、奖励函数和离线规划结果。上游结果通过 GeoJSON、PNG 和 CSV 进入展示端。
- **在线交互层**：基于 Streamlit 页面，支持自然语言输入、候鸟老人友好模式、年轻家庭模式、游客短租模式三类场景选择，以及规划结果可视化浏览。
- **智能解释层**：使用 DeepSeek/规则兜底进行需求解析，结合多Agent解释模块和轻量级本地政策 RAG，生成包含政策名称、发布机构、年份/时间、命中片段和支撑方向的政策证据链、合规解释和多方诉求协调建议。
- **成果输出层**：展示静态规划图、动态 GeoJSON 渲染、空间统计表，并支持 Markdown / Word 规划分析报告导出。

## 4. 核心功能

- 自然语言需求解析
- 三类社区规划场景识别
- 指标权重分析
- 静态规划结果图展示
- 动态 GeoJSON 渲染与场景重点类型高亮
- PPO/SGNN 离线规划流程说明
- 多Agent协同分析
- 轻量级 RAG 政策证据链与合规解释
- Markdown 和 Word 报告导出

## 5. 目录结构

```text
D:\琼岛智划_project
├─ app/
│  └─ streamlit_app.py          # Streamlit 展示端主程序
├─ data/
│  ├─ dhm.geojson               # 上游离线规划结果 GeoJSON
│  ├─ hlg.geojson               # 上游离线规划结果 GeoJSON
│  ├─ dhm_summary.csv           # DHM 空间统计表
│  └─ hlg_summary.csv           # HLG 空间统计表
├─ outputs/
│  ├─ dhm_result_clean.png      # DHM 静态规划结果图
│  └─ hlg_result_clean.png      # HLG 静态规划结果图
├─ policy/
│  └─ *.txt                     # 参赛演示用政策摘要知识库
├─ docs/
│  └─ UPSTREAM_ALIGNMENT_AUDIT.md # 上游一致性审计材料
├─ engine_original/             # 上游算法项目相关材料或备份
├─ generate_assets.py           # 离线结果派生图片/统计表脚本
├─ requirements.txt             # Python 依赖列表
├─ README.md                    # 项目交付说明
└─ 运行说明.md                  # 面向演示运行的简明步骤
```

目录说明：

- `app/`：存放 Streamlit 展示端主程序。
- `data/`：存放离线 GeoJSON 和空间统计 CSV。
- `outputs/`：存放静态规划结果 PNG。
- `policy/`：存放参赛演示用政策摘要和政策来源索引，用于轻量级 RAG 检索；证据链会展示政策名称、发布机构、年份/时间、命中片段和支撑方向，但不代表完整政策原文。
- `docs/`：存放审计报告、说明材料等文档。
- `engine_original/`：用于保留或说明上游算法项目相关材料。
- `generate_assets.py`：用于离线派生展示图和统计表的脚本。
- `requirements.txt`：项目运行依赖。

## 6. 运行环境

建议环境：

- Python 3.10+
- Windows + VS Code + PowerShell
- Streamlit

## 7. 安装依赖

```powershell
pip install -r requirements.txt
```

## 8. 启动方式

PowerShell 示例：

```powershell
cd D:\琼岛智划_project
$env:DEEPSEEK_API_KEY="你的APIKey"
$env:DEEPSEEK_BASE_URL="https://api.sydney-ai.com/v1"
$env:DEEPSEEK_MODEL="deepseek-chat"
python -m streamlit run app\streamlit_app.py --server.port 8502
```

注意：请使用自己的 API Key，不要在代码、文档或截图材料中写入真实密钥。

## 9. 演示输入示例

候鸟老人：

```text
这个社区候鸟老人较多，希望医院、菜市场、公园都近一点，路上有休息座椅，过马路少。
```

年轻家庭：

```text
这个片区年轻家庭较多，希望孩子上学方便，周边有运动空间，同时居住环境安静。
```

游客短租：

```text
我是来三亚旅游的，喜欢大海，希望民宿、景点、免税店和公交接驳都方便，夜间出行安全。
```

## 10. 输出成果

系统支持：

- 页面交互展示
- 动态 GeoJSON 图
- 空间统计表
- 政策证据链
- Markdown 报告
- Word 报告

## 11. 真实性说明

- 当前系统不进行现场 PPO/SGNN 训练。
- 当前系统不实时生成新的底层空间规划结果。
- DeepSeek、多Agent、RAG 用于在线解释、合规辅助和报告生成。
- 海南自贸港和三亚场景属于展示端场景化适配。
- 上游算法结果通过离线 GeoJSON、PNG 和 CSV 形式进入展示端。
- `policy` 目录为参赛演示用政策摘要知识库和来源索引，不代表完整政策原文；若无法确定精确条号，系统仅使用“相关要求/政策摘要”表达，不编造法规条号。

## 12. 后续优化方向

- 接入更多真实社区数据
- 政策 RAG 向向量检索升级
- 移动端 PWA / WebView 包装
- 增加优化前后对比
- 增加交互式地图图层

## 移动应用形态说明

本作品当前采用 Web App 原型实现，可在电脑浏览器、平板和手机浏览器中访问。当前版本重点展示移动应用的核心交互流程，包括自然语言需求输入、场景识别、规划结果展示、动态 GeoJSON 渲染、多Agent解释、政策证据链和报告导出。

后续可通过 Android WebView 或 PWA 方式封装为移动端 App。当前版本不声称已经是完整原生 Android / iOS App。

## Streamlit Cloud 部署说明

本项目可部署到 Streamlit Community Cloud，入口文件为：

```text
app/streamlit_app.py
```

部署步骤：

1. 进入 Streamlit Community Cloud。
2. 选择 GitHub 仓库 `qiongdao-zhihua`。
3. Branch 填写：

```text
main
```

4. Main file path 填写：

```text
app/streamlit_app.py
```

5. 在 Advanced settings / Secrets 中填写：

```toml
DEEPSEEK_API_KEY = "你的APIKey"
DEEPSEEK_BASE_URL = "https://api.sydney-ai.com/v1"
DEEPSEEK_MODEL = "deepseek-chat"
```

注意：不要在 GitHub 仓库、README、代码或截图中写入真实 API Key。若未配置 DeepSeek Key，系统仍可通过规则解析兜底运行。
