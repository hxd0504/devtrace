"""DevTrace 端到端冒烟测试（14 步）"""

import sys
import requests

BASE = "http://localhost:8002"
token = None
workspace_id = None
issue_id = None
issue_version = None
task_id = None
task_version = None


def auth_header():
    return {"Authorization": f"Bearer {token}"}


def fail(msg):
    print(f"[FAIL] {msg}")
    sys.exit(1)


def step(n, desc):
    print(f"\n--- Step {n}: {desc} ---")


# Step 1: 登录
step(1, "POST /api/v1/auth/login")
r = requests.post(f"{BASE}/api/v1/auth/login", json={"username": "admin", "password": "admin123"})
if r.status_code != 200:
    fail(f"登录失败: {r.status_code} {r.text}")
token = r.json()["access_token"]
print(f"[PASS] 获取 token: {token[:20]}...")

# Step 2: 获取当前用户
step(2, "GET /api/v1/auth/me")
r = requests.get(f"{BASE}/api/v1/auth/me", headers=auth_header())
if r.status_code != 200 or r.json().get("username") != "admin":
    fail(f"获取用户失败: {r.status_code} {r.text}")
print(f"[PASS] username={r.json()['username']}")

# Step 3: 创建工作空间
step(3, "POST /api/v1/workspaces")
r = requests.post(f"{BASE}/api/v1/workspaces", headers=auth_header(), json={"name": "smoke-test-ws"})
if r.status_code != 201:
    fail(f"创建工作空间失败: {r.status_code} {r.text}")
workspace_id = r.json()["id"]
print(f"[PASS] workspace_id={workspace_id}")

# Step 4: 创建问题
step(4, f"POST /api/v1/workspaces/{workspace_id}/issues")
r = requests.post(
    f"{BASE}/api/v1/workspaces/{workspace_id}/issues",
    headers=auth_header(),
    json={"title": "smoke-test-issue", "description": "冒烟测试问题"},
)
if r.status_code != 201:
    fail(f"创建问题失败: {r.status_code} {r.text}")
data = r.json()
issue_id = data["id"]
issue_version = data["version"]
if data["status"] != "open":
    fail(f"问题状态应为 open，实际为 {data['status']}")
print(f"[PASS] issue_id={issue_id}, status={data['status']}")

# Step 5: 问题状态 open → in_progress
step(5, f"PUT .../issues/{issue_id}/status (open→in_progress)")
r = requests.put(
    f"{BASE}/api/v1/workspaces/{workspace_id}/issues/{issue_id}/status",
    headers=auth_header(),
    json={"status": "in_progress", "version": issue_version},
)
if r.status_code != 200:
    fail(f"状态变更失败: {r.status_code} {r.text}")
data = r.json()
issue_version = data["version"]
if data["status"] != "in_progress":
    fail(f"状态应为 in_progress，实际为 {data['status']}")
print(f"[PASS] status={data['status']}, version={issue_version}")

# Step 6: 创建任务
step(6, f"POST .../issues/{issue_id}/tasks")
r = requests.post(
    f"{BASE}/api/v1/workspaces/{workspace_id}/issues/{issue_id}/tasks",
    headers=auth_header(),
    json={"title": "smoke-test-task", "description": "冒烟测试任务"},
)
if r.status_code != 201:
    fail(f"创建任务失败: {r.status_code} {r.text}")
data = r.json()
task_id = data["id"]
task_version = data["version"]
if data["status"] != "todo":
    fail(f"任务状态应为 todo，实际为 {data['status']}")
print(f"[PASS] task_id={task_id}, status={data['status']}")

# Step 7: 任务状态 todo → doing
step(7, f"PUT .../tasks/{task_id}/status (todo→doing)")
r = requests.put(
    f"{BASE}/api/v1/workspaces/{workspace_id}/issues/{issue_id}/tasks/{task_id}/status",
    headers=auth_header(),
    json={"status": "doing", "version": task_version},
)
if r.status_code != 200:
    fail(f"任务状态变更失败: {r.status_code} {r.text}")
data = r.json()
task_version = data["version"]
if data["status"] != "doing":
    fail(f"状态应为 doing，实际为 {data['status']}")
print(f"[PASS] status={data['status']}, version={task_version}")

# Step 8: 添加任务备注
step(8, f"POST .../tasks/{task_id}/notes")
r = requests.post(
    f"{BASE}/api/v1/workspaces/{workspace_id}/issues/{issue_id}/tasks/{task_id}/notes",
    headers=auth_header(),
    json={"details": "冒烟测试备注"},
)
if r.status_code != 200:
    fail(f"添加备注失败: {r.status_code} {r.text}")
data = r.json()
if data["version"] <= task_version:
    fail(f"版本应递增，原 {task_version}，现 {data['version']}")
task_version = data["version"]
print(f"[PASS] version={task_version}")

# Step 9: 问题状态 in_progress → resolved
step(9, f"PUT .../issues/{issue_id}/status (in_progress→resolved)")
r = requests.put(
    f"{BASE}/api/v1/workspaces/{workspace_id}/issues/{issue_id}/status",
    headers=auth_header(),
    json={"status": "resolved", "version": issue_version},
)
if r.status_code != 200:
    fail(f"状态变更失败: {r.status_code} {r.text}")
data = r.json()
issue_version = data["version"]
if data["status"] != "resolved":
    fail(f"状态应为 resolved，实际为 {data['status']}")
print(f"[PASS] status={data['status']}, version={issue_version}")

# Step 10: 归档问题
step(10, f"POST .../issues/{issue_id}/archive")
r = requests.post(
    f"{BASE}/api/v1/workspaces/{workspace_id}/issues/{issue_id}/archive",
    headers=auth_header(),
    json={
        "root_cause": "冒烟测试根因",
        "failed_attempts": "无",
        "final_solution": "冒烟测试解决方案",
        "reusable": True,
        "tags": ["smoke"],
        "version": issue_version,
    },
)
if r.status_code != 200:
    fail(f"归档失败: {r.status_code} {r.text}")
data = r.json()
if data["status"] != "archived":
    fail(f"状态应为 archived，实际为 {data['status']}")
print(f"[PASS] status={data['status']}")

# Step 11: 创建对话
step(11, "POST /api/v1/conversations")
r = requests.post(
    f"{BASE}/api/v1/conversations",
    headers=auth_header(),
    json={"workspace_id": workspace_id, "title": "smoke-test-conv"},
)
if r.status_code != 201:
    fail(f"创建对话失败: {r.status_code} {r.text}")
conv_id = r.json()["id"]
print(f"[PASS] conversation_id={conv_id}")

# Step 12: 发送消息
step(12, f"POST .../conversations/{conv_id}/messages")
r = requests.post(
    f"{BASE}/api/v1/conversations/{conv_id}/messages",
    headers=auth_header(),
    json={"role": "user", "content": "冒烟测试消息"},
)
if r.status_code != 201:
    fail(f"发送消息失败: {r.status_code} {r.text}")
data = r.json()
if data["role"] != "user":
    fail(f"role 应为 user，实际为 {data['role']}")
print(f"[PASS] message_id={data['id']}, role={data['role']}")

# Step 13: 调度任务
step(13, "POST /api/v1/dispatch")
r = requests.post(
    f"{BASE}/api/v1/dispatch",
    headers=auth_header(),
    json={"task_id": task_id, "task_type": "code_review"},
)
if r.status_code != 201:
    fail(f"调度失败: {r.status_code} {r.text}")
data = r.json()
print(f"[PASS] ai_tool={data['ai_tool']}")

# Step 14: 手动导入对话
step(14, "POST /api/v1/import/manual")
r = requests.post(
    f"{BASE}/api/v1/import/manual",
    headers=auth_header(),
    json={"title": "smoke-test-import", "content": "用户: 测试导入\n助手: 收到", "workspace_id": workspace_id},
)
if r.status_code != 201:
    fail(f"导入失败: {r.status_code} {r.text}")
print(f"[PASS] conversation_id={r.json()['id']}")

print("\n" + "=" * 40)
print("全部 14 步 [PASS]，冒烟测试通过！")
print("=" * 40)
