<template>
  <div class="issue-list">
    <div class="section-header">
      <span>问题列表</span>
      <el-tag size="small" type="info">{{ issues.length }}</el-tag>
    </div>
    <div class="list-content">
      <div
        v-for="issue in issues"
        :key="issue.id"
        class="issue-item"
        @click="goToIssue(issue)"
      >
        <el-tag :type="statusType(issue.status)" size="small" class="status-tag">
          {{ statusLabel(issue.status) }}
        </el-tag>
        <span class="title">{{ issue.title }}</span>
      </div>
      <div v-if="issues.length === 0" class="empty-hint">暂无问题</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { issueApi } from '@/api/issue'
import type { Issue, IssueStatus } from '@/types/issue'

const props = defineProps<{ workspaceId: number }>()

const router = useRouter()
const issues = ref<Issue[]>([])

const statusType = (status: IssueStatus) => {
  const map: Record<IssueStatus, string> = { open: 'info', in_progress: 'warning', resolved: 'success', archived: '' }
  return map[status] || ''
}

const statusLabel = (status: IssueStatus) => {
  const map: Record<IssueStatus, string> = { open: '待处理', in_progress: '进行中', resolved: '已解决', archived: '已归档' }
  return map[status] || status
}

const loadIssues = async () => {
  try {
    issues.value = await issueApi.list(props.workspaceId)
  } catch {
    // ignore
  }
}

const goToIssue = (issue: Issue) => {
  router.push(`/workspace/${props.workspaceId}/issue/${issue.id}`)
}

watch(() => props.workspaceId, loadIssues)
onMounted(loadIssues)
</script>

<style scoped>
.issue-list {
  border-bottom: 1px solid #313244;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  font-size: 12px;
  color: #6c7086;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.list-content {
  max-height: 200px;
  overflow-y: auto;
}

.issue-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 16px;
  cursor: pointer;
  font-size: 13px;
  transition: background 0.2s;
}

.issue-item:hover {
  background: #313244;
}

.status-tag {
  flex-shrink: 0;
}

.title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.empty-hint {
  padding: 8px 16px;
  font-size: 12px;
  color: #585b70;
}
</style>
