# Mock 接口清单

> 日期：2026-05-25
> 阶段：稳定化阶段

---

## 仍为 Mock 实现的接口

### 1. `services/ai.py` — 完全 Mock

| 函数 | 接口 | 类型 | 说明 |
|------|------|------|------|
| `generate_task_draft()` | POST /api/v1/ai/task-draft | Mock | 根据意图关键词返回固定模板的任务草稿 |
| `get_executor_recommendations()` | GET /api/v1/ai/executor-recommendations | Mock | 返回静态的执行体推荐列表 |

**当前行为**：
- `generate_task_draft()`: 根据意图中的关键词（docker/api/数据库等）返回预设的标题、标签和风险等级
- `get_executor_recommendations()`: 返回固定的 4 个执行体推荐，评分硬编码

**需要接入**：真实 LLM API（如 Claude API）进行意图理解和任务生成

---

### 2. `services/knowledge.py` — 部分 Mock

| 函数 | 接口 | 类型 | 说明 |
|------|------|------|------|
| `extract_knowledge_from_conversation()` | POST /api/v1/knowledge/extract | Mock | 从对话中提取思维链，当前为简单截取 |

**当前行为**：
- 取对话标题或第一条消息前 100 字符作为"问题"
- 取前 5 条消息的前 200 字符作为"思维链步骤"
- 标签固定为 `["auto_extract"]`

**需要接入**：真实 LLM API 进行语义分析和知识提取

---

## 规则引擎实现（可接受）

### 3. `services/dispatch.py` — 规则引擎

| 函数 | 接口 | 类型 | 说明 |
|------|------|------|------|
| `dispatch_task()` | POST /api/v1/dispatch | 规则引擎 | 根据任务类型匹配 AI 工具 |
| `get_ai_tags()` | GET /api/v1/ai-tags | 数据库查询 | 正常实现 |
| `update_ai_tag()` | PUT /api/v1/ai-tags/{tool} | 数据库操作 | 正常实现 |

**当前行为**：
- 使用 `DISPATCH_RULES` 字典进行任务类型到 AI 工具的映射
- 支持 6 种任务类型：backend, frontend, test, docs, design, debug
- 生成结构化的执行提示词模板

**评估**：规则引擎在当前阶段可接受，后续可升级为基于历史数据的智能推荐

---

## 总结

| 状态 | 数量 | 说明 |
|------|------|------|
| 完全 Mock | 2 | ai.py 的两个函数 |
| 部分 Mock | 1 | knowledge.py 的知识提取 |
| 规则引擎 | 1 | dispatch.py 的调度逻辑 |
| 正常实现 | 6 | 其他所有服务 |

**优先级建议**：
1. 接入 LLM 实现 `generate_task_draft()` — 影响任务创建流程
2. 接入 LLM 实现 `extract_knowledge_from_conversation()` — 影响知识沉淀功能
3. `get_executor_recommendations()` 可基于历史调度数据优化
