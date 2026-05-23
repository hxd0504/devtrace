<template>
  <div class="knowledge-panel">
    <div class="panel-header">
      <h2>知识库</h2>
      <div class="header-actions">
        <ThoughtChainSearch :workspace-id="workspaceId" @search="handleSearch" />
        <el-button type="primary" :icon="Plus" @click="showCreate = true">新建思维链</el-button>
      </div>
    </div>

    <div class="panel-content">
      <ThoughtChainCard
        v-for="chain in chains"
        :key="chain.id"
        :chain="chain"
      />
      <el-empty v-if="chains.length === 0" description="暂无思维链数据" />
    </div>

    <!-- 新建弹窗 -->
    <el-dialog v-model="showCreate" title="新建思维链" width="600px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="问题">
          <el-input v-model="form.problem" placeholder="描述遇到的问题" />
        </el-form-item>
        <el-form-item label="思维链">
          <div v-for="(step, idx) in form.thought_chain" :key="idx" class="step-input">
            <span class="step-num">{{ idx + 1 }}.</span>
            <el-input v-model="step.content" placeholder="输入思考步骤" />
            <el-button :icon="Delete" circle size="small" @click="removeStep(idx)" />
          </div>
          <el-button size="small" @click="addStep">添加步骤</el-button>
        </el-form-item>
        <el-form-item label="标签">
          <el-select v-model="form.tags" multiple filterable allow-create placeholder="添加标签">
            <el-option v-for="tag in form.tags" :key="tag" :label="tag" :value="tag" />
          </el-select>
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
import { Plus, Delete } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import ThoughtChainCard from './ThoughtChainCard.vue'
import ThoughtChainSearch from './ThoughtChainSearch.vue'
import { knowledgeApi } from '@/api/knowledge'
import type { ThoughtChain, ThoughtStep } from '@/types/knowledge'

const props = defineProps<{ workspaceId: number }>()

const chains = ref<ThoughtChain[]>([])
const showCreate = ref(false)
const form = reactive({
  problem: '',
  thought_chain: [{ content: '' }] as ThoughtStep[],
  tags: [] as string[],
})

const loadChains = async () => {
  try {
    chains.value = await knowledgeApi.list(props.workspaceId)
  } catch {
    // ignore
  }
}

const handleSearch = async (query: string) => {
  if (!query.trim()) {
    await loadChains()
    return
  }
  try {
    chains.value = await knowledgeApi.search(props.workspaceId, query)
  } catch {
    // ignore
  }
}

const addStep = () => {
  form.thought_chain.push({ content: '' })
}

const removeStep = (idx: number) => {
  form.thought_chain.splice(idx, 1)
}

const handleCreate = async () => {
  if (!form.problem.trim()) {
    ElMessage.warning('请输入问题描述')
    return
  }
  const validSteps = form.thought_chain.filter((s) => s.content.trim())
  if (validSteps.length === 0) {
    ElMessage.warning('请至少添加一个思维步骤')
    return
  }
  try {
    await knowledgeApi.create({
      workspace_id: props.workspaceId,
      problem: form.problem,
      thought_chain: validSteps,
      tags: form.tags.length ? form.tags : undefined,
      source: 'manual',
    })
    ElMessage.success('创建成功')
    showCreate.value = false
    form.problem = ''
    form.thought_chain = [{ content: '' }]
    form.tags = []
    await loadChains()
  } catch {
    ElMessage.error('创建失败')
  }
}

onMounted(loadChains)
</script>

<style scoped>
.knowledge-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  background: #fff;
  border-bottom: 1px solid #ebeef5;
}

.panel-header h2 {
  margin: 0;
  font-size: 20px;
}

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.panel-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.step-input {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.step-num {
  font-weight: 600;
  color: #909399;
  width: 20px;
}
</style>
