# 工程目录与迁移说明

本次把业务源码统一归入 `financial_reports/`，其余资源按脚本、实验、样例、文档和测试分类。没有移除原有代码功能或数据文件；64 个原文件均有保留位置，10 个 Python 文件同步调整了包引用并去掉旧的 `sys.path` 路径注入。Python 模块入口统一从仓库根目录使用 `python -m ...` 运行。

## 文件夹职责

| 文件夹 | 内容 |
| --- | --- |
| `financial_reports/generators/` | 三种公司研报生成器 |
| `financial_reports/agents/` | 数据分析智能体及其配置、执行器和提示词 |
| `financial_reports/collectors/` | 财务数据、公司资料、股权与竞争对手工具 |
| `financial_reports/workflows/` | 行业、宏观研究示例 |
| `financial_reports/backend/` | 后端工具包、配置和专用提示词 |
| `financial_reports/services/`、`financial_reports/config/` | 独立 LLM 封装和环境配置 |
| `financial_reports/templates/` | 通用分析、结构和内容提示词 |
| `financial_reports/vendor/` | 原工程内置 PocketFlow 源码 |
| `scripts/crawlers/` | 可通过 Python 模块运行的年报爬虫 |
| `notebooks/` | 爬虫与数据处理 Notebook |
| `examples/` | 后端工具加载示例 |
| `data/samples/` | 历史搜索样本，独立于运行时缓存 |
| `docs/references/` | 原始 Word 参考文档 |
| `docs/history/` | 首次补全记录及其 SHA-256 清单 |
| `tests/` | 无需外部服务的目录、模块引用与基础行为检查 |

原有后端模板与通用模板虽有相同内容，仍各自保留，避免整理时丢失来源文件。原有运行时数据与输出位置保持脚本中的设置；本次没有改变研究参数或研报算法。

## 运行与导入迁移

```bash
python -m financial_reports.generators.integrated_research_report_generator
python -m financial_reports.workflows.industry_workflow
python -m scripts.crawlers.scrape
```

```python
from financial_reports.agents.data_analysis_agent import quick_analysis, LLMConfig
from financial_reports.generators.integrated_research_report_generator import IntegratedResearchReportGenerator
from financial_reports.collectors.get_financial_statements import get_all_financial_statements
from financial_reports.vendor.pocketflow import Node, Flow
```

旧的 `from data_analysis_agent ...`、`from utils ...` 和 `from Backend ...` 外部调用需改为新包名。根目录原有 `main.py` 是工具加载示例，现放在 `examples/backend_imports.py`；`data/scrape` 增加 `.py` 扩展名，放在 `scripts/crawlers/scrape.py`。运行前安装依赖并填写根目录 `.env`。

## README 更新

中英文 README 使用相同的真实目录树，列出研报、智能体、采集、工作流、后端、模板、爬虫及资源。Mermaid 架构图展示当前模块职责与依赖，独立工作流和后端工具与公司研报编排分别呈现。删除了旧说明中不存在的 `--ticker` 参数、`generate_report` 接口、工作流 `add_node` 用法，以及尚未随仓库提供的数据文件示例。

## 检查范围

离线检查编译全部 Python 源码和 Notebook 代码单元，解析内部绝对/相对模块引用，实际导入独立提示词模块，并运行内置 PocketFlow 的两节点工作流。迁移核对覆盖原有全部文件，并比较 Python 语法树，确认源码变更只涉及包引用与旧路径注入的移除。另检查 README 的本地链接、目录树条目与代码块。

这些检查不执行外部 API、Ollama 服务、财务数据下载或完整研报生成。保留的历史清单描述首次补全时的原路径；本次清单同时提供新旧路径和整理后的文件摘要。

## 全部原文件对应关系

详见 [JSON 迁移清单](reorganization-manifest.json)。

| 整理前 | 整理后 |
| --- | --- |
| `.env.example` | `.env.example` |
| `.gitattributes` | `.gitattributes` |
| `.gitignore` | `.gitignore` |
| `Backend/__init__.py` | `financial_reports/backend/__init__.py` |
| `Backend/config/__init__.py` | `financial_reports/backend/config/__init__.py` |
| `Backend/config/config.py` | `financial_reports/backend/config/config.py` |
| `Backend/config/prompt_companyorshare.py` | `financial_reports/backend/templates/prompt_companyorshare.py` |
| `Backend/config/prompt_industry.py` | `financial_reports/backend/templates/prompt_industry.py` |
| `Backend/config/prompt_macro.py` | `financial_reports/backend/templates/prompt_macro.py` |
| `Backend/main.py` | `financial_reports/backend/main.py` |
| `Backend/utils/LLMRequest.py` | `financial_reports/backend/utils/LLMRequest.py` |
| `Backend/utils/RAG.py` | `financial_reports/backend/utils/RAG.py` |
| `Backend/utils/__init__.py` | `financial_reports/backend/utils/__init__.py` |
| `Backend/utils/drawGraph.py` | `financial_reports/backend/utils/drawGraph.py` |
| `LICENSE` | `LICENSE` |
| `README.md` | `README.md` |
| `README.zh-CN.md` | `README.zh-CN.md` |
| `Scrape.ipynb` | `notebooks/Scrape.ipynb` |
| `__init__.py` | `financial_reports/__init__.py` |
| `config.py` | `financial_reports/config/deepseek.py` |
| `content_companyorshare.py` | `financial_reports/templates/content/content_companyorshare.py` |
| `content_industry.py` | `financial_reports/templates/content/content_industry.py` |
| `content_macro.py` | `financial_reports/templates/content/content_macro.py` |
| `data/__init__.py` | `scripts/crawlers/__init__.py` |
| `data/scrape` | `scripts/crawlers/scrape.py` |
| `data_analysis_agent/.env.example` | `financial_reports/agents/data_analysis_agent/.env.example` |
| `data_analysis_agent/.gitignore` | `financial_reports/agents/data_analysis_agent/.gitignore` |
| `data_analysis_agent/README.md` | `financial_reports/agents/data_analysis_agent/README.md` |
| `data_analysis_agent/__init__.py` | `financial_reports/agents/data_analysis_agent/__init__.py` |
| `data_analysis_agent/config/__init__.py` | `financial_reports/agents/data_analysis_agent/config/__init__.py` |
| `data_analysis_agent/config/llm_config.py` | `financial_reports/agents/data_analysis_agent/config/llm_config.py` |
| `data_analysis_agent/data_analysis_agent.py` | `financial_reports/agents/data_analysis_agent/data_analysis_agent.py` |
| `data_analysis_agent/prompts.py` | `financial_reports/agents/data_analysis_agent/prompts.py` |
| `data_analysis_agent/utils/__init__.py` | `financial_reports/agents/data_analysis_agent/utils/__init__.py` |
| `data_analysis_agent/utils/code_executor.py` | `financial_reports/agents/data_analysis_agent/utils/code_executor.py` |
| `data_analysis_agent/utils/create_session_dir.py` | `financial_reports/agents/data_analysis_agent/utils/create_session_dir.py` |
| `data_analysis_agent/utils/extract_code.py` | `financial_reports/agents/data_analysis_agent/utils/extract_code.py` |
| `data_analysis_agent/utils/fallback_openai_client.py` | `financial_reports/agents/data_analysis_agent/utils/fallback_openai_client.py` |
| `data_analysis_agent/utils/format_execution_result.py` | `financial_reports/agents/data_analysis_agent/utils/format_execution_result.py` |
| `data_analysis_agent/utils/llm_helper.py` | `financial_reports/agents/data_analysis_agent/utils/llm_helper.py` |
| `docs/LOCAL_INTEGRATION.md` | `docs/history/LOCAL_INTEGRATION.md` |
| `docs/local-integration-manifest.json` | `docs/history/local-integration-manifest.json` |
| `in_depth_research_report_generator.py` | `financial_reports/generators/in_depth_research_report_generator.py` |
| `industry_info/all_search_results.json` | `data/samples/industry/all_search_results.json` |
| `industry_workflow.py` | `financial_reports/workflows/industry_workflow.py` |
| `integrated_research_report_generator.py` | `financial_reports/generators/integrated_research_report_generator.py` |
| `llm.py` | `financial_reports/services/llm.py` |
| `macro_workflow.py` | `financial_reports/workflows/macro_workflow.py` |
| `main.py` | `examples/backend_imports.py` |
| `pocketflow/__init__.py` | `financial_reports/vendor/pocketflow/__init__.py` |
| `prompt_companyorshare.py` | `financial_reports/templates/structure/prompt_companyorshare.py` |
| `prompt_industry.py` | `financial_reports/templates/structure/prompt_industry.py` |
| `prompt_macro.py` | `financial_reports/templates/structure/prompt_macro.py` |
| `prompts.py` | `financial_reports/templates/analysis/prompts.py` |
| `requirements.txt` | `requirements.txt` |
| `research_report_generator.py` | `financial_reports/generators/research_report_generator.py` |
| `utils/get_base_info.py` | `financial_reports/collectors/get_base_info.py` |
| `utils/get_company_info.py` | `financial_reports/collectors/get_company_info.py` |
| `utils/get_financial_statements.py` | `financial_reports/collectors/get_financial_statements.py` |
| `utils/get_shareholder_info.py` | `financial_reports/collectors/get_shareholder_info.py` |
| `utils/get_stock_intro.py` | `financial_reports/collectors/get_stock_intro.py` |
| `utils/identify_competitors.py` | `financial_reports/collectors/identify_competitors.py` |
| `utils/search_info.py` | `financial_reports/collectors/search_info.py` |
| `公司研报 需要.docx` | `docs/references/公司研报 需要.docx` |
