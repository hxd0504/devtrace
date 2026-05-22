import type { IssueStatus } from '@/types/issue'
import type { TaskStatus } from '@/types/task'

export const ISSUE_TRANSITIONS: Record<IssueStatus, IssueStatus[]> = {
  open: ['in_progress'],
  in_progress: ['resolved', 'open'],
  resolved: ['archived', 'in_progress'],
  archived: [],
}

export const TASK_TRANSITIONS: Record<TaskStatus, TaskStatus[]> = {
  todo: ['doing'],
  doing: ['done', 'todo'],
  done: ['doing'],
}

export function canTransitionIssue(current: IssueStatus, target: IssueStatus): boolean {
  return ISSUE_TRANSITIONS[current]?.includes(target) || false
}

export function canTransitionTask(current: TaskStatus, target: TaskStatus): boolean {
  return TASK_TRANSITIONS[current]?.includes(target) || false
}

export function getIssueTransitions(status: IssueStatus): IssueStatus[] {
  return ISSUE_TRANSITIONS[status] || []
}

export function getTaskTransitions(status: TaskStatus): TaskStatus[] {
  return TASK_TRANSITIONS[status] || []
}

export const ISSUE_STATUS_LABELS: Record<IssueStatus, string> = {
  open: '待处理',
  in_progress: '进行中',
  resolved: '已解决',
  archived: '已归档',
}

export const ISSUE_STATUS_TYPES: Record<IssueStatus, string> = {
  open: 'info',
  in_progress: 'warning',
  resolved: 'success',
  archived: '',
}

export const TASK_STATUS_LABELS: Record<TaskStatus, string> = {
  todo: '待办',
  doing: '进行中',
  done: '已完成',
}

export const TASK_STATUS_TYPES: Record<TaskStatus, string> = {
  todo: 'info',
  doing: 'warning',
  done: 'success',
}

export const ISSUE_TRANSITION_LABELS: Record<IssueStatus, string> = {
  open: '重新打开',
  in_progress: '开始处理',
  resolved: '标记解决',
  archived: '归档',
}

export const TASK_TRANSITION_LABELS: Record<TaskStatus, string> = {
  todo: '待办',
  doing: '开始',
  done: '完成',
}
