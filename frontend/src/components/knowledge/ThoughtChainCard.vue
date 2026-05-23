<template>
  <el-card class="thought-chain-card" shadow="hover">
    <div class="card-header">
      <div class="problem">{{ chain.problem }}</div>
      <el-tag size="small" :type="chain.source === 'auto_extract' ? 'success' : 'info'">
        {{ chain.source === 'auto_extract' ? '自动提取' : '手动录入' }}
      </el-tag>
    </div>

    <div class="chain-steps">
      <div v-for="(step, idx) in chain.thought_chain" :key="idx" class="step">
        <span class="step-num">{{ idx + 1 }}</span>
        <span class="step-text">{{ step.content }}</span>
      </div>
    </div>

    <div class="card-footer">
      <div class="tags">
        <el-tag v-for="tag in chain.tags" :key="tag" size="small" type="info" class="tag">{{ tag }}</el-tag>
      </div>
      <div class="meta">
        <span v-if="chain.related_issue_ids.length" class="related">
          关联问题: {{ chain.related_issue_ids.map((id) => `#${id}`).join(', ') }}
        </span>
        <span class="time">{{ formatTime(chain.created_at) }}</span>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import type { ThoughtChain } from '@/types/knowledge'

defineProps<{ chain: ThoughtChain }>()

const formatTime = (time: string) => {
  return new Date(time).toLocaleString('zh-CN')
}
</script>

<style scoped>
.thought-chain-card {
  transition: transform 0.2s;
}

.thought-chain-card:hover {
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.problem {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
  flex: 1;
  margin-right: 8px;
}

.chain-steps {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 12px;
  padding-left: 4px;
}

.step {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 13px;
  color: #606266;
}

.step-num {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #e4e7ed;
  color: #606266;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 600;
  flex-shrink: 0;
}

.step-text {
  line-height: 20px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding-top: 12px;
  border-top: 1px solid #ebeef5;
}

.tags {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
  font-size: 12px;
  color: #909399;
}

.related {
  color: #409eff;
}
</style>
