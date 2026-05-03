# 琼岛智划 AI 协作开发任务板

## 项目名称
琼岛智划：面向海南自贸港的多智能体协同社区规划系统

## 当前项目路径
D:\琼岛智划_project

## 当前状态
- Streamlit 前端已经可以打开
- DeepSeek API 已经通过 test_deepseek_api.py 测试成功
- 使用的中转 API 地址为：https://api.sydney-ai.com/v1
- 可用模型为：deepseek-chat
- 当前核心文件：app/streamlit_app.py

## 项目目标
把当前静态演示项目升级为真正的 AI 驱动系统：

用户输入自然语言社区规划需求
↓
DeepSeek 解析为结构化 JSON
↓
系统生成规划指标、推荐方案和解释
↓
多 Agent 模拟居民、政府、商业三方观点
↓
Streamlit 页面展示结果、日志和政策解释

## 开发约束
1. 不要删除现有页面功能。
2. 不要删除图片展示、指标表、多Agent日志、政策解释模块。
3. 不要把 API Key 写死进代码。
4. API Key 必须从环境变量 DEEPSEEK_API_KEY 读取。
5. Base URL 从环境变量 DEEPSEEK_BASE_URL 读取，默认 https://api.sydney-ai.com/v1。
6. Model 从环境变量 DEEPSEEK_MODEL 读取，默认 deepseek-chat。
7. Streamlit 必须用以下命令运行：
   python -m streamlit run app\streamlit_app.py
8. 每次修改尽量只改一个功能。
9. 修改完成后必须说明改了哪些文件、哪些函数。
10. 如果 API 调用失败，页面不能崩溃，必须回退到规则解析。

## 当前第一阶段任务
把 DeepSeek API 正式接入 streamlit_app.py 中的需求解析函数。