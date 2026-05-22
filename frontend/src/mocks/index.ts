import { mockAuthApi } from './auth'
import { mockWorkspaceApi } from './workspace'
import { mockIssueApi } from './issue'
import { mockTaskApi } from './task'
import { mockConversationApi } from './conversation'
import { mockDispatchApi } from './dispatch'
import { mockKnowledgeApi } from './knowledge'
import { mockImportApi } from './import'
import { authApi } from '@/api/auth'
import { workspaceApi } from '@/api/workspace'
import { issueApi } from '@/api/issue'
import { taskApi } from '@/api/task'
import { conversationApi } from '@/api/conversation'
import { dispatchApi } from '@/api/dispatch'
import { knowledgeApi } from '@/api/knowledge'
import { importApi } from '@/api/import'

const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true'

export const api = USE_MOCK
  ? {
      auth: mockAuthApi,
      workspace: mockWorkspaceApi,
      issue: mockIssueApi,
      task: mockTaskApi,
      conversation: mockConversationApi,
      dispatch: mockDispatchApi,
      knowledge: mockKnowledgeApi,
      import: mockImportApi,
    }
  : {
      auth: authApi,
      workspace: workspaceApi,
      issue: issueApi,
      task: taskApi,
      conversation: conversationApi,
      dispatch: dispatchApi,
      knowledge: knowledgeApi,
      import: importApi,
    }
