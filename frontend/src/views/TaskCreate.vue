<template>
  <AppLayout>
    <div class="task-create-page">
      <!-- 顶部标题 -->
      <div class="page-header">
        <div class="header-left">
          <el-button :icon="ArrowLeft" @click="goBack">返回</el-button>
          <h2>创建任务</h2>
        </div>
        <el-tag type="success" effect="dark">AI 智能创建</el-tag>
      </div>

      <!-- 意图输入区 -->
      <el-card class="intent-card" shadow="hover">
        <div class="intent-input">
          <el-input
            v-model="intent"
            type="textarea"
            :rows="3"
            placeholder="输入一句任务意图，例如：修复 Docker 镜像拉取超时问题"
            :disabled="generating"
          />
          <div class="intent-actions">
            <el-button type="primary" :loading="generating" @click="generateDraft">
              <el-icon><MagicStick /></el-icon>
              生成任务草稿
            </el-button>
            <span class="hint">系统将结合当前问题、对话和证据自动生成任务草稿</span>
          </div>
        </div>
      </el-card>

      <!-- 主内容区：左右分栏 -->
      <div class="main-content" v-if="draft">
        <!-- 左侧：上下文来源 -->
        <div class="context-panel">
          <el-card shadow="never">
            <template #header>
              <div class="card-header">
                <el-icon><Connection /></el-icon>
                <span>上下文来源</span>
              </div>
            </template>

            <!-- 当前 Issue -->
            <div class="context-section">
              <h4>当前 Issue</h4>
              <div class="issue-info" v-if="currentIssue">
                <el-tag :type="getStatusType(currentIssue.status)" size="small">
                  {{ getStatusLabel(currentIssue.status) }}
                </el-tag>
                <p class="issue-title">{{ currentIssue.title }}</p>
                <p class="issue-desc">{{ currentIssue.description || '暂无描述' }}</p>
              </div>
              <el-empty v-else description="无 Issue 信息" :image-size="60" />
            </div>

            <el-divider />

            <!-- 相关文件 -->
            <div class="context-section">
              <h4>相关文件</h4>
              <div v-if="currentIssue?.related_files?.length" class="file-list">
                <div v-for="(file, idx) in currentIssue.related_files" :key="idx" class="file-item">
                  <el-icon><Document /></el-icon>
                  <span>{{ file.name }}</span>
                  <el-tag size="small" type="info">{{ file.path }}</el-tag>
                </div>
              </div>
              <el-empty v-else description="暂无相关文件" :image-size="60" />
            </div>

            <el-divider />

            <!-- 证据片段 -->
            <div class="context-section">
              <h4>证据片段</h4>
              <div v-if="currentIssue?.evidence_note" class="evidence-content">
                <el-text type="info">{{ currentIssue.evidence_note }}</el-text>
              </div>
              <el-empty v-else description="暂无证据" :image-size="60" />
            </div>
          </el-card>
        </div>

        <!-- 右侧：AI 生成的草稿 -->
        <div class="draft-panel">
          <el-card shadow="never">
            <template #header>
              <div class="card-header">
                <div class="header-left">
                  <el-icon><MagicStick /></el-icon>
                  <span>AI 生成的任务草稿</span>
                </div>
                <el-tag type="success" size="small">AI 推荐</el-tag>
              </div>
            </template>

            <el-form :model="draft" label-width="100px" label-position="top">
              <!-- 任务标题 -->
              <el-form-item>
                <template #label>
                  <div class="label-with-tag">
                    <span>任务标题</span>
                    <el-tag type="success" size="small">AI 生成</el-tag>
                  </div>
                </template>
                <el-input v-model="draft.title" />
              </el-form-item>

              <!-- 任务描述 -->
              <el-form-item>
                <template #label>
                  <div class="label-with-tag">
                    <span>任务描述</span>
                    <el-tag type="success" size="small">AI 生成</el-tag>
                  </div>
                </template>
                <el-input v-model="draft.description" type="textarea" :rows="4" />
              </el-form-item>

              <!-- 执行信息行 -->
              <el-row :gutter="16">
                <el-col :span="8">
                  <el-form-item>
                    <template #label>
                      <div class="label-with-tag">
                        <span>执行类型</span>
                        <el-tag type="warning" size="small">AI 推断</el-tag>
                      </div>
                    </template>
                    <el-select v-model="draft.executor_type" style="width: 100%">
                      <el-option label="人工" value="human" />
                      <el-option label="AI窗口" value="ai_window" />
                      <el-option label="角色" value="role" />
                      <el-option label="工具" value="tool" />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="8">
                  <el-form-item>
                    <template #label>
                      <div class="label-with-tag">
                        <span>执行体</span>
                        <el-tag type="warning" size="small">推荐</el-tag>
                      </div>
                    </template>
                    <el-select v-model="draft.executor_name" style="width: 100%">
                      <el-option
                        v-for="exec in executorOptions"
                        :key="exec.name"
                        :label="exec.name"
                        :value="exec.name"
                      >
                        <div class="executor-option">
                          <span>{{ exec.name }}</span>
                          <el-tag size="small" :type="exec.type === 'ai_window' ? 'primary' : 'info'">
                            {{ exec.type === 'ai_window' ? 'AI' : '人工' }}
                          </el-tag>
                          <span class="score">匹配度 {{ (exec.score * 100).toFixed(0) }}%</span>
                        </div>
                      </el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="8">
                  <el-form-item>
                    <template #label>
                      <span>负责人</span>
                    </template>
                    <el-select v-model="draft.owner_name" style="width: 100%">
                      <el-option label="admin" value="admin" />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>

              <!-- 推荐理由 -->
              <el-form-item>
                <template #label>
                  <div class="label-with-tag">
                    <span>推荐理由</span>
                    <el-tag type="info" size="small">AI 分析</el-tag>
                  </div>
                </template>
                <el-input v-model="draft.recommend_reason" type="textarea" :rows="2" disabled />
              </el-form-item>

              <!-- 证据与验收 -->
              <el-row :gutter="16">
                <el-col :span="12">
                  <el-form-item>
                    <template #label>
                      <div class="label-with-tag">
                        <span>证据摘要</span>
                        <el-tag type="success" size="small">AI 生成</el-tag>
                      </div>
                    </template>
                    <el-input v-model="draft.evidence_summary" type="textarea" :rows="3" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item>
                    <template #label>
                      <div class="label-with-tag">
                        <span>验收标准</span>
                        <el-tag type="success" size="small">AI 生成</el-tag>
                      </div>
                    </template>
                    <el-input v-model="draft.acceptance_criteria" type="textarea" :rows="3" />
                  </el-form-item>
                </el-col>
              </el-row>

              <!-- 风险等级 -->
              <el-form-item>
                <template #label>
                  <div class="label-with-tag">
                    <span>风险等级</span>
                    <el-tag type="warning" size="small">AI 评估</el-tag>
                  </div>
                </template>
                <el-radio-group v-model="draft.risk_level">
                  <el-radio-button value="low">
                    <el-tag type="success" size="small">低风险</el-tag>
                  </el-radio-button>
                  <el-radio-button value="medium">
                    <el-tag type="warning" size="small">中风险</el-tag>
                  </el-radio-button>
                  <el-radio-button value="high">
                    <el-tag type="danger" size="small">高风险</el-tag>
                  </el-radio-button>
                </el-radio-group>
              </el-form-item>

              <!-- 高级设置折叠区 -->
              <el-collapse v-model="advancedOpen">
                <el-collapse-item title="高级设置" name="advanced">
                  <el-form-item label="执行备注">
                    <el-input v-model="draft.executor_note" type="textarea" :rows="2" placeholder="可选：补充执行说明" />
                  </el-form-item>
                  <el-form-item label="证据来源">
                    <el-input v-model="draft.evidence_source" placeholder="可选：证据来源路径或链接" />
                  </el-form-item>
                  <el-form-item label="标签">
                    <el-select v-model="draft.tags" multiple filterable allow-create placeholder="可选：添加标签">
                      <el-option v-for="tag in draft.tags" :key="tag" :label="tag" :value="tag" />
                    </el-select>
                  </el-form-item>
                </el-collapse-item>
              </el-collapse>
            </el-form>

            <!-- 操作按钮 -->
            <div class="draft-actions">
              <el-button @click="resetDraft">重新生成</el-button>
              <el-button type="primary" :loading="creating" @click="handleCreate">
                <el-icon><Check /></el-icon>
                创建任务
              </el-button>
              <el-button type="success" :loading="creating" @click="handleCreateAndDispatch">
                <el-icon><Promotion /></el-icon>
                创建并下发
              </el-button>
            </div>
          </el-card>
        </div>
      </div>

      <!-- 空状态：未生成草稿 -->
      <el-empty v-else-if="!generating" description="输入任务意图后生成草稿" :image-size="120">
        <template #image>
          <el-icon :size="80" color="#c0c4cc"><MagicStick /></el-icon>
        </template>
      </el-empty>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, MagicStick, Connection, Document, Check, Promotion } from '@element-plus/icons-vue'
import AppLayout from '@/layouts/AppLayout.vue'
import { issueApi } from '@/api/issue'
import { taskApi } from '@/api/task'
import type { Issue } from '@/types/issue'
import type { ExecutorRecommend, RiskLevel, TaskDraftResponse } from '@/types/task'

const router = useRouter()
const route = useRoute()
const workspaceId = Number(route.params.wid)
const issueId = Number(route.params.id)

const intent = ref('')
const generating = ref(false)
const creating = ref(false)
const advancedOpen = ref([])
const currentIssue = ref<Issue | null>(null)

interface DraftForm extends TaskDraftResponse {
  executor_note: string
  evidence_source: string
  recommend_reason: string
}

const draft = ref<DraftForm | null>(null)

const executorOptions = ref<ExecutorRecommend[]>([
  { name: 'Claude Code 窗口A', type: 'ai_window', score: 0.95 },
  { name: 'MiMo', type: 'ai_window', score: 0.88 },
  { name: 'admin', type: 'human', score: 0.70 },
])

// 加载 Issue 上下文
onMounted(async () => {
  try {
    currentIssue.value = await issueApi.get(workspaceId, issueId)
  } catch (e) {
    console.error('加载 Issue 失败', e)
  }
})

// Mock AI 生成草稿
const generateDraft = async () => {
  if (!intent.value.trim()) {
    ElMessage.warning('请输入任务意图')
    return
  }

  generating.value = true
  try {
    // V1.1 先用 Mock，后续接入真实 AI
    await new Promise(resolve => setTimeout(resolve, 800))

    draft.value = {
      title: intent.value,
      description: `基于任务意图「${intent.value}」自动生成的任务描述。\n\n当前 Issue：${currentIssue.value?.title || '无'}\n需要结合上下文进行具体分析和处理。`,
      executor_type: 'ai_window',
      executor_name: 'Claude Code 窗口A',
      owner_name: 'admin',
      evidence_summary: currentIssue.value?.evidence_note || '暂无证据摘要',
      acceptance_criteria: `1. 完成「${intent.value}」的核心功能\n2. 通过基本测试验证\n3. 更新相关文档`,
      risk_level: 'medium' as RiskLevel,
      tags: ['AI生成', '待验证'],
      executor_note: '',
      evidence_source: '',
      recommend_reason: `基于当前 Issue 上下文和任务复杂度分析，推荐使用 AI 窗口执行。该任务涉及技术调试和配置优化，适合 AI 辅助完成。`,
    }
  } catch (e) {
    ElMessage.error('生成草稿失败')
  } finally {
    generating.value = false
  }
}

const resetDraft = () => {
  draft.value = null
  intent.value = ''
}

const handleCreate = async () => {
  if (!draft.value) return

  creating.value = true
  try {
    await taskApi.create(workspaceId, issueId, {
      title: draft.value.title,
      description: draft.value.description || undefined,
      owner_name: draft.value.owner_name || undefined,
      executor_name: draft.value.executor_name || undefined,
      executor_type: draft.value.executor_type || undefined,
      executor_note: draft.value.executor_note || undefined,
      evidence_source: draft.value.evidence_source || undefined,
      evidence_summary: draft.value.evidence_summary || undefined,
      acceptance_criteria: draft.value.acceptance_criteria || undefined,
      risk_level: draft.value.risk_level || undefined,
      tags: draft.value.tags,
    })
    ElMessage.success('任务创建成功')
    router.push(`/workspace/${workspaceId}/issue/${issueId}`)
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '创建失败')
  } finally {
    creating.value = false
  }
}

const handleCreateAndDispatch = async () => {
  // V1.1 先创建，后续实现下发逻辑
  await handleCreate()
}

const goBack = () => {
  router.push(`/workspace/${workspaceId}/issue/${issueId}`)
}

const getStatusType = (status: string) => {
  const map: Record<string, string> = { open: 'info', in_progress: 'warning', resolved: 'success', archived: 'danger' }
  return map[status] || 'info'
}

const getStatusLabel = (status: string) => {
  const map: Record<string, string> = { open: '待处理', in_progress: '处理中', resolved: '已解决', archived: '已归档' }
  return map[status] || status
}
</script>

<style scoped>
.task-create-page {
  padding: 20px;
  max-width: 1100px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-left h2 {
  margin: 0;
}

.intent-card {
  margin-bottom: 20px;
}

.intent-input {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.intent-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.hint {
  color: #909399;
  font-size: 13px;
}

.main-content {
  display: flex;
  gap: 20px;
}

.context-panel {
  width: 360px;
  flex-shrink: 0;
}

.draft-panel {
  flex: 1;
  min-width: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header .header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.context-section {
  margin-bottom: 16px;
}

.context-section h4 {
  margin: 0 0 8px 0;
  color: #606266;
  font-size: 14px;
}

.issue-title {
  font-weight: 600;
  margin: 8px 0 4px 0;
}

.issue-desc {
  color: #909399;
  font-size: 13px;
  margin: 0;
}

.file-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.evidence-content {
  background: #f5f7fa;
  padding: 8px 12px;
  border-radius: 4px;
}

.label-with-tag {
  display: flex;
  align-items: center;
  gap: 8px;
}

.executor-option {
  display: flex;
  align-items: center;
  gap: 8px;
}

.score {
  color: #67c23a;
  font-size: 12px;
  margin-left: auto;
}

.draft-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

:deep(.el-collapse-item__header) {
  font-size: 14px;
  color: #409eff;
}
</style>
