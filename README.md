# DevTrace - AI辅助研发的项目记忆与智能体调度平台

DevTrace 是面向 AI 辅助研发流程的项目记忆与智能体调度平台，包含两大核心板块：**项目记忆中心**（问题归档、历史坑检索、可复用解法、对话导入、RAG 召回）和 **智能体调度中心**（任务草稿生成、执行体推荐、调度记录、执行提示词、结果回填）。

## 核心功能

### 问题管理
- 创建和管理项目问题
- 问题状态流转：open → in_progress → resolved → archived
- 问题归档时记录根因分析、解决方案和复盘信息

### 任务管理
- 为问题创建子任务
- 任务状态流转：todo → doing → done
- 任务与问题关联

### AI 智能创建任务（V1.1）
- 用户输入一句任务意图
- AI 自动生成任务草稿（标题、描述、执行类型、执行体、验收标准、风险等级）
- 用户确认或微调后创建
- 支持执行体推荐和匹配度评分

### 执行体调度
- 支持多种执行体类型：人工、AI窗口、角色、工具
- 记录执行提示词和执行结果
- 调度规则快照和调度原因记录

### 处理记录
- 自动记录操作日志
- 支持添加备注
- 完整的活动时间线

## 技术栈

### 后端
- **框架**: FastAPI
- **数据库**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **迁移**: Alembic
- **认证**: JWT

### 前端
- **框架**: Vue 3 + TypeScript
- **UI**: Element Plus
- **状态管理**: Pinia
- **HTTP客户端**: Axios

### 部署
- **容器化**: Docker + Docker Compose
- **反向代理**: Nginx

## 快速开始

### 前提条件
- Docker Desktop

### 启动服务

```bash
# 克隆项目
git clone <your-repo-url>
cd devtrace

# 复制环境变量
cp .env.example .env

# 启动所有服务
docker compose up -d

# 查看日志
docker compose logs -f
```

### 访问地址

- 前端: http://localhost
- 后端API: http://localhost:8000
- Swagger文档: http://localhost:8000/docs

### 默认账号

- 用户名: `admin`
- 密码: 见种子数据脚本或自行设置

## 项目结构

```
devtrace/
├── backend/                # 后端服务
│   ├── app/
│   │   ├── models/        # 数据模型
│   │   ├── routers/       # API路由
│   │   ├── schemas/       # Pydantic Schema
│   │   ├── services/      # 业务逻辑
│   │   └── utils/         # 工具函数
│   ├── alembic/           # 数据库迁移
│   └── scripts/           # 种子数据脚本
├── frontend/              # 前端服务
│   └── src/
│       ├── api/           # API调用
│       ├── views/         # 页面组件
│       ├── types/         # TypeScript类型
│       ├── stores/        # Pinia状态
│       ├── stores/        # Pinia 状态管理
│       └── layouts/       # 布局组件
├── docs/                  # 文档
└── handoff_logs/          # 交接日志
```

## API 接口

### 认证
- `POST /api/v1/auth/login` - 用户登录
- `GET /api/v1/auth/me` - 获取当前用户

### 项目空间
- `GET /api/v1/workspaces` - 获取项目列表
- `POST /api/v1/workspaces` - 创建项目
- `GET /api/v1/workspaces/:id` - 获取项目详情

### 问题
- `GET /api/v1/workspaces/:wid/issues` - 获取问题列表
- `POST /api/v1/workspaces/:wid/issues` - 创建问题
- `GET /api/v1/workspaces/:wid/issues/:id` - 获取问题详情
- `PUT /api/v1/workspaces/:wid/issues/:id` - 更新问题
- `PUT /api/v1/workspaces/:wid/issues/:id/status` - 更新问题状态
- `POST /api/v1/workspaces/:wid/issues/:id/archive` - 归档问题

### 任务
- `GET /api/v1/workspaces/:wid/issues/:id/tasks` - 获取任务列表
- `POST /api/v1/workspaces/:wid/issues/:id/tasks` - 创建任务
- `PUT /api/v1/workspaces/:wid/issues/:id/tasks/:tid` - 更新任务
- `PUT /api/v1/workspaces/:wid/issues/:id/tasks/:tid/status` - 更新任务状态

### AI 智能创建（V1.1）
- `POST /api/v1/tasks/draft` - AI 生成任务草稿
- `GET /api/v1/executors` - 获取执行体推荐列表

## 开发说明

### 本地开发

```bash
# 后端
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload

# 前端
cd frontend
npm install
npm run dev
```

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| POSTGRES_USER | 数据库用户 | devtrace |
| POSTGRES_PASSWORD | 数据库密码 | 需要设置 |
| POSTGRES_DB | 数据库名 | devtrace |
| DATABASE_URL | 数据库连接串 | 自动生成 |
| SECRET_KEY | JWT密钥 | 需要设置 |
| ADMIN_PASSWORD | 管理员密码 | 需要设置 |

### 数据库迁移

```bash
# 创建迁移
docker compose exec backend bash -c "cd /app && PYTHONPATH=/app alembic revision --autogenerate -m '描述'"

# 执行迁移
docker compose exec backend bash -c "cd /app && PYTHONPATH=/app alembic upgrade head"
```

### 种子数据

```bash
# 开发环境种子数据
docker compose exec backend bash -c "cd /app && PYTHONPATH=/app python -m scripts.dev_seed"

# 演示种子数据
docker compose exec backend bash -c "cd /app && PYTHONPATH=/app python -m scripts.demo_seed"
```

## 版本规划

- **V1**: 核心功能闭环（问题、任务、状态流转、归档）— 已完成
- **V1.1**: AI 智能创建任务、执行体推荐 — 已完成
- **V2**: 对话、调度、知识沉淀 — 已完成（原型）
- **稳定化阶段**: 当前阶段，修复已知问题，完善数据库迁移和测试

## License

MIT
