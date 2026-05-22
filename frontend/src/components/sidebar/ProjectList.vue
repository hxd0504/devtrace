<template>
  <div class="project-list">
    <div class="section-header">
      <span>项目空间</span>
      <el-button :icon="Plus" circle size="small" @click="showCreate = true" />
    </div>
    <div class="list-content">
      <div
        v-for="ws in workspaces"
        :key="ws.id"
        class="project-item"
        :class="{ active: selectedId === ws.id }"
        @click="selectWorkspace(ws)"
      >
        <el-icon><Folder /></el-icon>
        <span class="name">{{ ws.name }}</span>
      </div>
      <div v-if="workspaces.length === 0" class="empty-hint">暂无项目</div>
    </div>

    <!-- 创建项目弹窗 -->
    <el-dialog v-model="showCreate" title="创建项目空间" width="400px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="form.name" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="2" placeholder="选填" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreate = false">取消</el-button>
        <el-button type="primary" @click="handleCreate">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Plus, Folder } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { workspaceApi } from '@/api/workspace'
import type { Workspace } from '@/types/workspace'

const emit = defineEmits<{
  select: [workspace: Workspace]
}>()

const workspaces = ref<Workspace[]>([])
const selectedId = ref<number | null>(null)
const showCreate = ref(false)
const form = reactive({ name: '', description: '' })

const loadWorkspaces = async () => {
  try {
    const res = await workspaceApi.list()
    workspaces.value = res.items
  } catch {
    ElMessage.error('加载项目列表失败')
  }
}

const selectWorkspace = (ws: Workspace) => {
  selectedId.value = ws.id
  emit('select', ws)
}

const handleCreate = async () => {
  if (!form.name.trim()) {
    ElMessage.warning('请输入项目名称')
    return
  }
  try {
    await workspaceApi.create({ name: form.name, description: form.description || undefined })
    ElMessage.success('创建成功')
    showCreate.value = false
    form.name = ''
    form.description = ''
    await loadWorkspaces()
  } catch {
    ElMessage.error('创建失败')
  }
}

onMounted(loadWorkspaces)
</script>

<style scoped>
.project-list {
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

.project-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  cursor: pointer;
  font-size: 13px;
  transition: background 0.2s;
}

.project-item:hover {
  background: #313244;
}

.project-item.active {
  background: #45475a;
  color: #89b4fa;
}

.name {
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
