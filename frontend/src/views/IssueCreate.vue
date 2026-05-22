<template>
  <AppLayout>
    <div class="issue-create">
      <h2>创建问题</h2>
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
      >
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入问题标题" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="4"
            placeholder="请输入问题描述（选填）"
          />
        </el-form-item>
        <el-form-item label="负责人" prop="assignee_name">
          <el-input v-model="form.assignee_name" placeholder="请输入负责人（选填）" />
        </el-form-item>
        <el-divider>执行信息</el-divider>
        <el-form-item label="执行体" prop="executor_name">
          <el-input v-model="form.executor_name" placeholder="请输入执行体名称（选填）" />
        </el-form-item>
        <el-form-item label="执行类型" prop="executor_type">
          <el-select v-model="form.executor_type" placeholder="请选择执行类型（选填）" clearable>
            <el-option label="人工" value="human" />
            <el-option label="AI窗口" value="ai_window" />
            <el-option label="角色" value="role" />
            <el-option label="工具" value="tool" />
          </el-select>
        </el-form-item>
        <el-form-item label="执行备注" prop="executor_note">
          <el-input
            v-model="form.executor_note"
            type="textarea"
            :rows="2"
            placeholder="请输入执行备注（选填）"
          />
        </el-form-item>
        <el-divider>证据信息</el-divider>
        <el-form-item label="证据说明" prop="evidence_note">
          <el-input
            v-model="form.evidence_note"
            type="textarea"
            :rows="3"
            placeholder="请输入证据说明（选填）"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleCreate">
            创建
          </el-button>
          <el-button @click="goBack">取消</el-button>
        </el-form-item>
      </el-form>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import AppLayout from '@/layouts/AppLayout.vue'
import { issueApi } from '@/api/issue'

const router = useRouter()
const route = useRoute()
const workspaceId = Number(route.params.id)

const formRef = ref<FormInstance>()
const loading = ref(false)

const form = reactive({
  title: '',
  description: '',
  assignee_name: '',
  executor_name: '',
  executor_type: null as 'human' | 'ai_window' | 'role' | 'tool' | null,
  executor_note: '',
  evidence_note: '',
})

const rules: FormRules = {
  title: [
    { required: true, message: '请输入问题标题', trigger: 'blur' },
    { max: 200, message: '标题最多200个字符', trigger: 'blur' },
  ],
}

const handleCreate = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    loading.value = true
    try {
      await issueApi.create(workspaceId, {
        title: form.title,
        description: form.description || undefined,
        assignee_name: form.assignee_name || undefined,
        executor_name: form.executor_name || undefined,
        executor_type: form.executor_type || undefined,
        executor_note: form.executor_note || undefined,
        evidence_note: form.evidence_note || undefined,
      })
      ElMessage.success('问题创建成功')
      router.push(`/workspace/${workspaceId}`)
    } catch (e: any) {
      ElMessage.error(e.response?.data?.detail || '创建失败')
    } finally {
      loading.value = false
    }
  })
}

const goBack = () => {
  router.push(`/workspace/${workspaceId}`)
}
</script>

<style scoped>
.issue-create {
  padding: 20px;
  max-width: 800px;
}

.issue-create h2 {
  margin-bottom: 20px;
}
</style>
