# DevTrace 开发工作流程

## 分支策略

- `main`: 主分支，由主窗口管理，所有代码最终合并到这里
- `backend`: 后端开发分支，后端窗口使用
- `frontend`: 前端开发分支，前端窗口使用

## 工作流程

### 后端窗口
1. 从 `main` 分支创建功能分支：`git checkout -b backend/feature-name`
2. 在功能分支上开发
3. 完成后提交 PR 到 `backend` 分支
4. 等待主窗口审核合并

### 前端窗口
1. 从 `main` 分支创建功能分支：`git checkout -b frontend/feature-name`
2. 在功能分支上开发
3. 完成后提交 PR 到 `frontend` 分支
4. 等待主窗口审核合并

### 主窗口
1. 审核后端和前端的 PR
2. 合并到对应的开发分支
3. 定期将开发分支合并到 `main`

## 代码规范

### 后端 (Python/FastAPI)
- 使用同步 SQLAlchemy + psycopg2-binary
- JSONB 字段使用 MutableList.as_mutable(JSONB) + default=list
- Pydantic Schema 使用 Field(default_factory=list)
- 所有查询都过滤 owner_id
- API 路径使用 {workspace_id} 风格

### 前端 (Vue3/TypeScript)
- 使用 Vue3 + TypeScript + Element Plus
- 页面通过 src/api 调用，不直接写 axios
- TypeScript 类型与后端 Schema 一致
- 组件名使用 Workspace，不使用 Project

## 环境变量

必须在 `.env` 文件中设置：
- `POSTGRES_USER`: 数据库用户
- `POSTGRES_PASSWORD`: 数据库密码
- `SECRET_KEY`: JWT 密钥
- `ADMIN_PASSWORD`: 管理员密码

## 启动命令

```bash
# 启动所有服务
docker compose up -d

# 查看日志
docker compose logs -f

# 执行数据库迁移
docker compose exec backend bash -c "cd /app && PYTHONPATH=/app alembic upgrade head"

# 执行种子数据
docker compose exec backend bash -c "cd /app && PYTHONPATH=/app python -m scripts.dev_seed"
```
