<template>
  <div class="ai-tag-panel">
    <div class="section-header">
      <span>AI 标签</span>
    </div>
    <div class="list-content">
      <div v-for="tag in tags" :key="tag.id" class="ai-tag-item">
        <div class="ai-name">{{ tag.ai_tool }}</div>
        <div class="stats">
          <div class="stat-row">
            <span class="stat-label">速度</span>
            <ProgressBar :value="(tag.stats.speed as number) || 0" />
          </div>
          <div class="stat-row">
            <span class="stat-label">质量</span>
            <ProgressBar :value="(tag.stats.quality as number) || 0" />
          </div>
          <div class="stat-row">
            <span class="stat-label">稳定</span>
            <ProgressBar :value="(tag.stats.stability as number) || 0" />
          </div>
        </div>
        <div class="specialties">
          <el-tag
            v-for="s in (tag.tags.specialty as string[] || [])"
            :key="s"
            size="small"
            type="info"
            class="specialty-tag"
          >{{ s }}</el-tag>
        </div>
      </div>
      <div v-if="tags.length === 0" class="empty-hint">暂无 AI 数据</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { dispatchApi } from '@/api/dispatch'
import ProgressBar from './ProgressBar.vue'
import type { AITag } from '@/types/dispatch'

const props = defineProps<{ workspaceId: number }>()

const tags = ref<AITag[]>([])

const loadTags = async () => {
  try {
    tags.value = await dispatchApi.getAITags(props.workspaceId)
  } catch {
    // ignore
  }
}

watch(() => props.workspaceId, loadTags)
onMounted(loadTags)
</script>

<style scoped>
.ai-tag-panel {
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
  max-height: 300px;
  overflow-y: auto;
}

.ai-tag-item {
  padding: 10px 16px;
  border-bottom: 1px solid #313244;
}

.ai-tag-item:last-child {
  border-bottom: none;
}

.ai-name {
  font-size: 13px;
  font-weight: 600;
  color: #cdd6f4;
  margin-bottom: 6px;
}

.stats {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stat-label {
  font-size: 11px;
  color: #6c7086;
  width: 28px;
}

.specialties {
  display: flex;
  gap: 4px;
  margin-top: 6px;
  flex-wrap: wrap;
}

.specialty-tag {
  font-size: 11px;
}

.empty-hint {
  padding: 8px 16px;
  font-size: 12px;
  color: #585b70;
}
</style>
