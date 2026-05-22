<template>
  <AppLayout>
    <div class="issue-detail">
      <div class="header">
        <div>
          <h2>{{ issue?.title }}</h2>
          <el-tag :type="getStatusType(issue?.status || 'open')" size="large">
            {{ getStatusLabel(issue?.status || 'open') }}
          </el-tag>
        </div>
        <div class="actions">
          <el-button @click="showEditDialog = true" :disabled="issue?.status === 'archived'">
            编辑
          </el-button>
          <el-button
            v-for="status in availableTransitions"
            :key="status"
            :type="status === 'archived' ? 'danger' : 'primary'"
            @click="handleStatusChange(status)"
          >
            {{ getTransitionLabel(status) }}
          </el-button>
        </div>
      </div>

      <el-divider />

      <el-descriptions :column="2" border>
        <el-descriptions-item label="ID">{{ issue?.id }}</el-descriptions-item>
        <el-descriptions-item label="负责人">{{ issue?.assignee_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="执行体">{{ issue?.executor_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="执行类型">{{ issue?.executor_type || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间" :span="2">{{ formatTime(issue?.created_at || '') }}</el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">{{ issue?.description || '暂无描述' }}</el-descriptions-item>
        <el-descriptions-item v-if="issue?.executor_note" label="执行备注" :span="2">
          {{ issue.executor_note }}
        </el-descriptions-item>
        <el-descriptions-item v-if="issue?.evidence_note" label="证据说明" :span="2">
          {{ issue.evidence_note }}
        </el-descriptions-item>
      </el-descriptions>

      <!-- 归档信息 -->
      <template v-if="issue?.status === 'archived'">
        <el-divider>归档信息</el-divider>
        <el-descriptions :column="1" border>
          <el-descriptions-item label="根因分析">{{ issue.root_cause }}</el-descriptions-item>
          <el-descriptions-item label="已尝试方案">{{ issue.failed_attempts }}</el-descriptions-item>
          <el-descriptions-item label="最终解决方案">{{ issue.final_solution }}</el-descriptions-item>
          <el-descriptions-item label="是否可复用">
            <el-tag :type="issue.reusable ? 'success' : 'info'">
              {{ issue.reusable ? '是' : '否' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item v-if="issue.tags?.length" label="标签">
            <el-tag v-for="tag in issue.tags" :key="tag" style="margin-right: 8px">
              {{ tag }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>
      </template>

      <!-- 任务列表 -->
      <el-divider>
        <div class="divider-header">
          <span>任务列表</span>
          <el-button size="small" type="primary" @click="goToCreateTask" :disabled="issue?.status === 'archived'">
            添加任务
          </el-button>
        </div>
      </el-divider>

      <el-table :data="tasks" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="标题" min-width="200" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getTaskStatusType(row.status)">
              {{ getTaskStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="owner_name" label="负责人" width="120" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button
              v-for="status in getTaskTransitions(row.status)"
              :key="status"
              size="small"
              @click="handleTaskStatusChange(row, status)"
            >
              {{ getTaskTransitionLabel(status) }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 处理记录 -->
      <el-divider>
        <div class="divider-header">
          <span>处理记录</span>
          <el-button size="small" @click="showNoteDialog = true" :disabled="issue?.status === 'archived'">
            添加备注
          </el-button>
        </div>
      </el-divider>

      <el-timeline>
        <el-timeline-item
          v-for="(log, index) in issue?.activity_log || []"
          :key="index"
          :timestamp="formatTime(log.timestamp)"
          :type="getLogType(log.action)"
        >
          <p>
            <strong>{{ log.username }}</strong>
            {{ getLogAction(log.action) }}
            <span v-if="log.details">：{{ log.details }}</span>
          </p>
        </el-timeline-item>
      </el-timeline>
    </div>

    <!-- 编辑问题弹窗 -->
    <el-dialog v-model="showEditDialog" title="编辑问题" width="600px">
      <el-form ref="editFormRef" :model="editForm" label-width="100px">
        <el-form-item label="标题" prop="title" :rules="[{ required: true, message: '请输入标题' }]">
          <el-input v-model="editForm.title" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="editForm.description" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="负责人">
          <el-input v-model="editForm.assignee_name" />
        </el-form-item>
        <el-form-item label="执行体">
          <el-input v-model="editForm.executor_name" />
        </el-form-item>
        <el-form-item label="执行类型">
          <el-select v-model="editForm.executor_type" clearable>
            <el-option label="人工" value="human" />
            <el-option label="AI窗口" value="ai_window" />
            <el-option label="角色" value="role" />
            <el-option label="工具" value="tool" />
          </el-select>
        </el-form-item>
        <el-form-item label="执行备注">
          <el-input v-model="editForm.executor_note" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="证据说明">
          <el-input v-model="editForm.evidence_note" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>

    <!-- 添加备注弹窗 -->
    <el-dialog v-model="showNoteDialog" title="添加备注" width="500px">
      <el-input
        v-model="noteContent"
        type="textarea"
        :rows="4"
        placeholder="请输入备注内容"
      />
      <template #footer>
        <el-button @click="showNoteDialog = false">取消</el-button>
        <el-button type="primary" :loading="addingNote" @click="handleAddNote">提交</el-button>
      </template>
    </el-dialog>

    <!-- 归档弹窗 -->
    <el-dialog v-model="showArchiveDialog" title="归档问题" width="600px">
      <el-form ref="archiveFormRef" :model="archiveForm" :rules="archiveRules" label-width="120px">
        <el-form-item label="根因分析" prop="root_cause">
          <el-input v-model="archiveForm.root_cause" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="已尝试方案" prop="failed_attempts">
          <el-input v-model="archiveForm.failed_attempts" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="最终解决方案" prop="final_solution">
          <el-input v-model="archiveForm.final_solution" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="是否可复用" prop="reusable">
          <el-switch v-model="archiveForm.reusable" />
        </el-form-item>
        <el-form-item label="标签">
          <el-input v-model="archiveForm.tagsInput" placeholder="多个标签用逗号分隔" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showArchiveDialog = false">取消</el-button>
        <el-button type="primary" :loading="archiving" @click="handleArchive">确认归档</el-button>
      </template>
    </el-dialog>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import AppLayout from '@/layouts/AppLayout.vue'
import { issueApi } from '@/api/issue'
import { taskApi } from '@/api/task'
import type { Issue, IssueStatus } from '@/types/issue'
import type { Task, TaskStatus } from '@/types/task'
import {
  getIssueTransitions,
  getTaskTransitions as getTaskTransitionsUtil,
  ISSUE_STATUS_LABELS,
  ISSUE_STATUS_TYPES,
  TASK_STATUS_LABELS,
  TASK_STATUS_TYPES,
  ISSUE_TRANSITION_LABELS,
  TASK_TRANSITION_LABELS,
} from '@/utils/state_machine'

const router = useRouter()
const route = useRoute()
const workspaceId = Number(route.params.wid)
const issueId = Number(route.params.id)

const issue = ref<Issue | null>(null)
const tasks = ref<Task[]>([])
const showEditDialog = ref(false)
const showNoteDialog = ref(false)
const showArchiveDialog = ref(false)
const saving = ref(false)
const addingNote = ref(false)
const archiving = ref(false)
const noteContent = ref('')
const editFormRef = ref<FormInstance>()
const archiveFormRef = ref<FormInstance>()

const editForm = reactive({
  title: '',
  description: '',
  assignee_name: '',
  executor_name: '',
  executor_type: null as 'human' | 'ai_window' | 'role' | 'tool' | null,
  executor_note: '',
  evidence_note: '',
})

const archiveForm = reactive({
  root_cause: '',
  failed_attempts: '',
  final_solution: '',
  reusable: false,
  tagsInput: '',
})

const archiveRules: FormRules = {
  root_cause: [{ required: true, message: '请输入根因分析', trigger: 'blur' }],
  failed_attempts: [{ required: true, message: '请输入已尝试方案', trigger: 'blur' }],
  final_solution: [{ required: true, message: '请输入最终解决方案', trigger: 'blur' }],
}

const availableTransitions = computed(() => {
  if (!issue.value) return []
  return getIssueTransitions(issue.value.status)
})

const getStatusType = (status: IssueStatus) => {
  return ISSUE_STATUS_TYPES[status] || ''
}

const getStatusLabel = (status: IssueStatus) => {
  return ISSUE_STATUS_LABELS[status] || status
}

const getTaskStatusType = (status: TaskStatus) => {
  return TASK_STATUS_TYPES[status] || ''
}

const getTaskStatusLabel = (status: TaskStatus) => {
  return TASK_STATUS_LABELS[status] || status
}

const getTaskTransitions = (status: TaskStatus) => {
  return getTaskTransitionsUtil(status)
}

const getTransitionLabel = (status: IssueStatus) => {
  return ISSUE_TRANSITION_LABELS[status] || status
}

const getTaskTransitionLabel = (status: TaskStatus) => {
  return TASK_TRANSITION_LABELS[status] || status
}

const getLogType = (action: string) => {
  const map: Record<string, string> = {
    created: 'primary',
    status_change: 'warning',
    note: 'info',
    archived: 'success',
  }
  return map[action] || ''
}

const getLogAction = (action: string) => {
  const map: Record<string, string> = {
    created: '创建了问题',
    status_change: '变更了状态',
    note: '添加了备注',
    archived: '归档了问题',
  }
  return map[action] || action
}

const formatTime = (time: string) => {
  return new Date(time).toLocaleString('zh-CN')
}

const loadData = async () => {
  try {
    const [issueData, tasksData] = await Promise.all([
      issueApi.get(workspaceId, issueId),
      taskApi.list(workspaceId, issueId),
    ])
    issue.value = issueData
    tasks.value = tasksData
    // 填充编辑表单
    editForm.title = issueData.title
    editForm.description = issueData.description || ''
    editForm.assignee_name = issueData.assignee_name || ''
    editForm.executor_name = issueData.executor_name || ''
    editForm.executor_type = issueData.executor_type || null
    editForm.executor_note = issueData.executor_note || ''
    editForm.evidence_note = issueData.evidence_note || ''
  } catch (e: any) {
    ElMessage.error('加载数据失败')
  }
}

const handleStatusChange = async (targetStatus: IssueStatus) => {
  if (targetStatus === 'archived') {
    showArchiveDialog.value = true
    return
  }

  try {
    await ElMessageBox.confirm(`确定要将状态变更为 ${getStatusLabel(targetStatus)} 吗？`, '确认')
    await issueApi.changeStatus(workspaceId, issueId, {
      status: targetStatus,
      version: issue.value!.version,
    })
    ElMessage.success('状态变更成功')
    await loadData()
  } catch (e: any) {
    if (e !== 'cancel') {
      ElMessage.error(e.response?.data?.detail || '状态变更失败')
    }
  }
}

const handleSave = async () => {
  if (!editFormRef.value) return

  saving.value = true
  try {
    await issueApi.update(workspaceId, issueId, {
      ...editForm,
      executor_type: editForm.executor_type ?? undefined,
      version: issue.value!.version,
    })
    ElMessage.success('保存成功')
    showEditDialog.value = false
    await loadData()
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '保存失败')
  } finally {
    saving.value = false
  }
}

const handleAddNote = async () => {
  if (!noteContent.value.trim()) {
    ElMessage.warning('请输入备注内容')
    return
  }

  addingNote.value = true
  try {
    await issueApi.addNote(workspaceId, issueId, noteContent.value)
    ElMessage.success('备注添加成功')
    showNoteDialog.value = false
    noteContent.value = ''
    await loadData()
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '添加备注失败')
  } finally {
    addingNote.value = false
  }
}

const handleArchive = async () => {
  if (!archiveFormRef.value) return

  await archiveFormRef.value.validate(async (valid) => {
    if (!valid) return

    archiving.value = true
    try {
      await issueApi.archive(workspaceId, issueId, {
        root_cause: archiveForm.root_cause,
        failed_attempts: archiveForm.failed_attempts,
        final_solution: archiveForm.final_solution,
        reusable: archiveForm.reusable,
        tags: archiveForm.tagsInput ? archiveForm.tagsInput.split(',').map(t => t.trim()) : [],
        version: issue.value!.version,
      })
      ElMessage.success('归档成功')
      showArchiveDialog.value = false
      await loadData()
    } catch (e: any) {
      ElMessage.error(e.response?.data?.detail || '归档失败')
    } finally {
      archiving.value = false
    }
  })
}

const handleTaskStatusChange = async (task: Task, targetStatus: TaskStatus) => {
  try {
    await taskApi.changeStatus(workspaceId, issueId, task.id, {
      status: targetStatus,
      version: task.version,
    })
    ElMessage.success('任务状态变更成功')
    await loadData()
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '状态变更失败')
  }
}

const goToCreateTask = () => {
  router.push(`/workspace/${workspaceId}/issue/${issueId}/task/create`)
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.issue-detail {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.header h2 {
  margin: 0 0 8px 0;
}

.actions {
  display: flex;
  gap: 8px;
}

.divider-header {
  display: flex;
  align-items: center;
  gap: 16px;
}
</style>
