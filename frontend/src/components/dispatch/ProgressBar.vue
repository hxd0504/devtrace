<template>
  <div class="progress-bar">
    <div class="bar-track">
      <div class="bar-fill" :style="{ width: `${percent}%` }" :class="level" />
    </div>
    <span class="bar-label">{{ label }}</span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ value: number }>()

const percent = computed(() => Math.round(props.value * 100))

const level = computed(() => {
  if (percent.value >= 80) return 'high'
  if (percent.value >= 50) return 'medium'
  return 'low'
})

const label = computed(() => {
  if (percent.value >= 80) return '高'
  if (percent.value >= 50) return '中'
  return '低'
})
</script>

<style scoped>
.progress-bar {
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1;
}

.bar-track {
  flex: 1;
  height: 6px;
  background: #313244;
  border-radius: 3px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.3s;
}

.bar-fill.high {
  background: #a6e3a1;
}

.bar-fill.medium {
  background: #f9e2af;
}

.bar-fill.low {
  background: #f38ba8;
}

.bar-label {
  font-size: 11px;
  color: #6c7086;
  width: 16px;
  text-align: right;
}
</style>
