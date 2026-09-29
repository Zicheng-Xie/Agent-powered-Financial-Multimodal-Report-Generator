# 数据分析智能体

模块位置：`financial_reports.agents.data_analysis_agent`。

该模块使用大模型进行多轮数据分析，通过 IPython 执行生成的 Python 代码，保存分析结果和图表。其公共接口包括 `DataAnalysisAgent`、`LLMConfig`、`CodeExecutor`、`create_agent` 和 `quick_analysis`。

[仓库说明](../../../README.zh-CN.md) · [许可证](../../../LICENSE)

## 模块结构

```text
financial_reports/agents/data_analysis_agent/
├── config/
│   └── llm_config.py
├── utils/
│   ├── code_executor.py
│   ├── create_session_dir.py
│   ├── extract_code.py
│   ├── fallback_openai_client.py
│   ├── format_execution_result.py
│   └── llm_helper.py
├── data_analysis_agent.py
├── prompts.py
├── __init__.py
├── .env.example
├── .gitignore
└── README.md
```

## 使用

在仓库根目录安装 `requirements.txt` 中的依赖，并配置根目录 `.env` 的 `OPENAI_API_KEY`、`OPENAI_BASE_URL` 和 `OPENAI_MODEL`。

```python
from financial_reports.agents.data_analysis_agent import quick_analysis, LLMConfig

result = quick_analysis(
    query="分析收入、利润和现金流的变化，并生成趋势图。",
    files=["path/to/financial_statements.csv"],
    llm_config=LLMConfig(),
    output_dir="outputs",
    max_rounds=10,
    absolute_path=True,
)
print(result.get("final_report", ""))
```

运行时会在指定输出目录下创建会话子目录，保存图表与 Markdown 分析报告；这些内容不作为源码提交。完整公司研报的编排及 Word 转换由 `financial_reports/generators/` 中的生成器负责。

`utils/llm_helper.py` 封装同步/异步调用，`utils/fallback_openai_client.py` 提供可选的备用接口配置，`utils/code_executor.py` 提供 IPython 执行与结果捕获。文件路径、API 配置及外部依赖需要在实际使用环境中准备。

目录迁移后，请使用上述完整包名导入，并从仓库根目录运行 Python。原有接口参数保持不变。
