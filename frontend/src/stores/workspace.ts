import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useWorkspaceStore = defineStore('workspace', () => {
  const currentWorkspaceId = ref(1)

  function setWorkspace(id: number) {
    currentWorkspaceId.value = id
  }

  return { currentWorkspaceId, setWorkspace }
})
