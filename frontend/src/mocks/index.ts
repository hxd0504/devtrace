import { mockAuthApi } from './auth'
import { mockWorkspaceApi } from './workspace'
import { mockIssueApi } from './issue'
import { mockTaskApi } from './task'
import { authApi } from '@/api/auth'
import { workspaceApi } from '@/api/workspace'
import { issueApi } from '@/api/issue'
import { taskApi } from '@/api/task'

const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true'

export const api = USE_MOCK
  ? { auth: mockAuthApi, workspace: mockWorkspaceApi, issue: mockIssueApi, task: mockTaskApi }
  : { auth: authApi, workspace: workspaceApi, issue: issueApi, task: taskApi }
