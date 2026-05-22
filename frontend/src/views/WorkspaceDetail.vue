<template>
  <AppLayout>
    <div class="workspace-detail">
      <div class="header">
        <div>
          <h2>{{ workspace?.name }}</h2>
          <p class="description">{{ workspace?.description || '暂无描述' }}</p>
        </div>
        <el-button type="primary" @click="goToCreateIssue">
          创建问题
        </el-button>
      </div>

      <el-divider />

      <div class="filter-bar">
        <span>状态筛选：</span>
        <el-select v-model="statusFilter" placeholder="全部状态" clearable>
          <el-option label="待处理" value="open" />
          <el-option label="进行中" value="in_progress" />
          <el-option label="已解决" value="resolved" />
          <el-option label="已归档" value="archived" />
        </el-select>
      </div>

      <el-table :data="filteredIssues" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="标题" min-width="200">
          <template #default="{ row }">
            <el-link type="primary" @click="goToIssueDetail(row.id)">
              {{ row.title }}
            </el-link>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="assignee_name" label="负责人" width="120" />
        <el-table-column prop="executor_name" label="执行体" width="120" />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="filteredIssues.length === 0" description="暂无问题" />
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import AppLayout from '@/layouts/AppLayout.vue'
import { workspaceApi } from '@/api/workspace'
import { issueApi } from '@/api/issue'
import type { Workspace } from '@/types/workspace'
import type { Issue, IssueStatus } from '@/types/issue'

const router = useRouter()
const route = useRoute()
const workspaceId = Number(route.params.id)

const workspace = ref<Workspace | null>(null)
const issues = ref<Issue[]>([])
const statusFilter = ref<IssueStatus | ''>('')

const filteredIssues = computed(() => {
  if (!statusFilter.value) return issues.value
  return issues.value.filter((issue) => issue.status === statusFilter.value)
})

const getStatusType = (status: IssueStatus) => {
  const map: Record<IssueStatus, string> = {
    open: 'info',
    in_progress: 'warning',
    resolved: 'success',
    archived: '',
  }
  return map[status] || ''
}

const getStatusLabel = (status: IssueStatus) => {
  const map: Record<IssueStatus, string> = {
    open: '待处理',
    in_progress: '进行中',
    resolved: '已解决',
    archived: '已归档',
  }
  return map[status] || status
}

const formatTime = (time: string) => {
  return new Date(time).toLocaleString('zh-CN')
}

const loadData = async () => {
  try {
    const [workspaceData, issuesData] = await Promise.all([
      workspaceApi.get(workspaceId),
      issueApi.list(workspaceId),
    ])
    workspace.value = workspaceData
    issues.value = issuesData
  } catch (e: any) {
    ElMessage.error('加载数据失败')
  }
}

const goToCreateIssue = () => {
  router.push(`/workspace/${workspaceId}/issue/create`)
}

const goToIssueDetail = (issueId: number) => {
  router.push(`/workspace/${workspaceId}/issue/${issueId}`)
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.workspace-detail {
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

.description {
  color: #666;
  margin: 0;
}

.filter-bar {
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
