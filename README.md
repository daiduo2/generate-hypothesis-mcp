# Generate Hypothesis MCP

**AstroInsight Research Assistant** 是一个强大的基于MCP协议的AI研究论文生成工具，专为科研工作者和学术研究人员设计。该工具通过集成多个AI模型和学术数据源，实现从关键词搜索到完整研究假设生成的全自动化流程，显著提升学术研究效率。

## 工具简介

本MCP工具是专业的**AI驱动研究助手**，核心功能包括智能论文检索、事实信息提取、研究假设生成、技术方案优化等完整研究流程。采用多智能体协作架构，支持DeepSeek、Qwen等多个前沿AI模型协同工作，为研究人员提供从文献调研到创新想法生成的一站式解决方案。工具遵循MCP标准协议，可无缝集成到各类AI开发环境中，是提升学术研究效率的强大助手。

## 核心功能特色

🔍 **智能论文检索** - 基于关键词自动搜索ArXiv等学术数据库，精准定位相关研究文献  
📊 **事实信息提取** - 运用先进的NLP技术从学术论文中提取核心概念、研究方法和关键发现  
💡 **研究假设生成** - 基于提取的事实信息，智能生成具有创新性的研究假设和思路  
⚡ **技术方案优化** - 对初步研究想法进行技术层面的深度优化和可行性分析  
🤖 **多智能体协作** - 采用MoA (Mixture of Agents) 架构，多个AI模型协同工作提升输出质量  
👥 **人机协作模式** - 支持研究人员参与指导，实现AI辅助的个性化研究流程

## 技术架构亮点

🏗️ **MCP协议标准** - 基于FastMCP框架构建，完全兼容Model Context Protocol标准，确保与各类AI客户端的无缝集成  
🧠 **多模型融合** - 深度集成DeepSeek、Qwen等前沿大语言模型，通过模型互补实现更高质量的研究输出  
⚙️ **异步任务引擎** - 采用多线程异步处理架构，支持长时间运行的复杂研究任务，提供实时进度监控  
📈 **智能状态管理** - 内置任务状态跟踪系统，支持任务暂停、恢复和结果持久化存储  
🔄 **流水线处理** - 将研究流程分解为多个独立模块，支持灵活的工作流定制和优化

## MCP工具接口

本工具提供三个核心MCP工具函数，可通过任何支持MCP协议的AI客户端调用：

### `generate_research_paper`
- **功能**: 启动完整的研究论文生成流程
- **参数**: `keyword`(研究关键词), `search_paper_num`(检索论文数量1-20)
- **返回**: 任务ID和初始状态信息

### `get_task_status` 
- **功能**: 查询任务执行状态和进度
- **参数**: `task_id`(任务唯一标识符)
- **返回**: 详细的任务状态、进度百分比和结果信息

### `list_active_tasks`
- **功能**: 列出所有活跃任务的概览信息  
- **参数**: 无
- **返回**: 当前所有运行中和最近完成的任务列表

## 安装和使用

### 环境要求

- Python 3.8+
- 相关依赖包（见requirements.txt）

### 配置

1. 复制环境变量模板：
```bash
cp .env.example .env
```

2. 配置API密钥：
```
DEEPSEEK_API_TOKEN=your_deepseek_token
QWEN_API_TOKEN=your_qwen_token
MINERU_API_TOKEN=your_mineru_token
```

### 启动服务

```bash
python astroinsight_optimized_fastmcp.py
```

### MCP工具使用

该项目提供以下MCP工具：

1. **generate_research_paper**: 生成研究论文
2. **get_task_status**: 获取任务状态
3. **list_active_tasks**: 列出活跃任务

## 项目结构

```
├── app/                    # 应用核心代码
│   ├── api/               # API接口
│   ├── core/              # 核心功能模块
│   ├── task/              # 任务处理
│   └── utils/             # 工具函数
├── astroinsight_optimized_fastmcp.py  # MCP服务器主文件
├── main.py                # 主要业务逻辑
├── requirements.txt       # 依赖包列表
└── README.md             # 项目说明

```

## 开发规范

### Git提交规范

- `feat`: 增加新功能
- `fix`: 修复问题/BUG
- `style`: 代码风格相关无影响运行结果的
- `perf`: 优化/性能提升
- `refactor`: 重构
- `revert`: 撤销修改
- `test`: 测试相关
- `docs`: 文档/注释
- `chore`: 依赖更新/脚手架配置修改等

### 编码规范

- Python文件编码为 `utf-8`
- 遵循PEP 8代码风格
- 添加必要的函数和类注释

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 联系方式

如有问题或建议，请通过GitHub Issues联系我们。