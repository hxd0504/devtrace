<template>
  <V2Layout>
    <template #sidebar-extra>
      <ProjectList />
    </template>

    <KnowledgePanel :workspace-id="currentWorkspaceId" />
  </V2Layout>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useWorkspaceStore } from '@/stores/workspace'
import V2Layout from '@/layouts/V2Layout.vue'
import ProjectList from '@/components/sidebar/ProjectList.vue'
import KnowledgePanel from '@/components/knowledge/KnowledgePanel.vue'

const workspaceStore = useWorkspaceStore()
const currentWorkspaceId = computed(() => workspaceStore.currentWorkspaceId)
</script>
