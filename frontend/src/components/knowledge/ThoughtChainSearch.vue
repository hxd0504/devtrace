<template>
  <div class="thought-chain-search">
    <el-input
      v-model="query"
      placeholder="搜索思维链..."
      clearable
      :prefix-icon="Search"
      @keyup.enter="handleSearch"
      @clear="handleClear"
      style="width: 240px"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'

defineProps<{ workspaceId: number }>()

const emit = defineEmits<{
  search: [query: string]
}>()

const query = ref('')

const handleSearch = () => {
  emit('search', query.value)
}

const handleClear = () => {
  emit('search', '')
}
</script>

<style scoped>
.thought-chain-search {
  display: inline-flex;
}
</style>
