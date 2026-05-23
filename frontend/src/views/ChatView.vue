<template>
  <V2Layout>
    <template #header-action>
      <el-button :icon="Plus" circle size="small" @click="createConversation" />
    </template>

    <template #sidebar-extra>
      <ProjectList />
      <IssueList v-if="currentWorkspaceId" :workspace-id="currentWorkspaceId" />
      <AITagPanel v-if="currentWorkspaceId" :workspace-id="currentWorkspaceId" />
    </template>

    <router-view />
  </V2Layout>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { Plus } from '@element-plus/icons-vue'
import { useWorkspaceStore } from '@/stores/workspace'
import V2Layout from '@/layouts/V2Layout.vue'
import ProjectList from '@/components/sidebar/ProjectList.vue'
import IssueList from '@/components/sidebar/IssueList.vue'
import AITagPanel from '@/components/dispatch/AITagPanel.vue'

const router = useRouter()
const workspaceStore = useWorkspaceStore()

const currentWorkspaceId = computed(() => workspaceStore.currentWorkspaceId)

const createConversation = () => {
  router.push('/chat')
}
</script>
