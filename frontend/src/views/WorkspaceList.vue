<template>
  <AppLayout>
    <div class="workspace-list">
      <div class="header">
        <h2>项目空间</h2>
        <el-button type="primary" @click="showCreateDialog = true">
          创建项目
        </el-button>
      </div>

      <el-row :gutter="16">
        <el-col
          v-for="workspace in workspaces"
          :key="workspace.id"
          :xs="24"
          :sm="12"
          :md="8"
          :lg="6"
        >
          <el-card
            class="workspace-card"
            shadow="hover"
            @click="goToDetail(workspace.id)"
          >
            <template #header>
              <div class="card-header">
                <span>{{ workspace.name }}</span>
              </div>
            </template>
            <div class="card-body">
              <p class="description">{{ workspace.description || '暂无描述' }}</p>
              <p class="time">
                创建时间: {{ formatTime(workspace.created_at) }}
              </p>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-empty v-if="workspaces.length === 0" description="暂无项目" />
    </div>

    <!-- 创建项目弹窗 -->
    <el-dialog
      v-model="showCreateDialog"
      title="创建项目"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="项目描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入项目描述（选填）"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" :loading="creating" @click="handleCreate">
          创建
        </el-button>
      </template>
    </el-dialog>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import AppLayout from '@/layouts/AppLayout.vue'
import { workspaceApi } from '@/api/workspace'
import type { Workspace } from '@/types/workspace'

const router = useRouter()
const workspaces = ref<Workspace[]>([])
const showCreateDialog = ref(false)
const creating = ref(false)
const formRef = ref<FormInstance>()

const form = reactive({
  name: '',
  description: '',
})

const rules: FormRules = {
  name: [
    { required: true, message: '请输入项目名称', trigger: 'blur' },
    { max: 100, message: '项目名称最多100个字符', trigger: 'blur' },
  ],
}

const formatTime = (time: string) => {
  return new Date(time).toLocaleString('zh-CN')
}

const loadWorkspaces = async () => {
  try {
    const res = await workspaceApi.list()
    workspaces.value = res.items
  } catch (e: any) {
    ElMessage.error('加载项目列表失败')
  }
}

const goToDetail = (id: number) => {
  router.push(`/workspace/${id}`)
}

const handleCreate = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    creating.value = true
    try {
      await workspaceApi.create({
        name: form.name,
        description: form.description || undefined,
      })
      ElMessage.success('项目创建成功')
      showCreateDialog.value = false
      form.name = ''
      form.description = ''
      await loadWorkspaces()
    } catch (e: any) {
      ElMessage.error(e.response?.data?.detail || '创建失败')
    } finally {
      creating.value = false
    }
  })
}

onMounted(() => {
  loadWorkspaces()
})
</script>

<style scoped>
.workspace-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h2 {
  margin: 0;
}

.workspace-card {
  margin-bottom: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.workspace-card:hover {
  transform: translateY(-4px);
}

.card-header {
  font-weight: bold;
  font-size: 16px;
}

.card-body {
  min-height: 80px;
}

.description {
  color: #666;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.time {
  color: #999;
  font-size: 12px;
  margin: 0;
}
</style>
