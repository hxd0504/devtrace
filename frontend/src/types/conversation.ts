export type MessageRole = 'user' | 'assistant' | 'system'
export type MessageType = 'text' | 'execution_result' | 'knowledge_extract' | 'system_notify'
export type ConversationSource = 'devtrace' | 'chatgpt_web' | 'manual_import'

export interface Conversation {
  id: number
  workspace_id: number
  title: string | null
  source: ConversationSource
  created_by: number
  created_at: string
  updated_at: string
}

export interface ConversationCreate {
  workspace_id: number
  title?: string
  source?: ConversationSource
}

export interface Message {
  id: number
  conversation_id: number
  role: MessageRole
  content: string
  message_type: MessageType
  metadata: Record<string, unknown>
  created_at: string
}

export interface MessageCreate {
  role: MessageRole
  content: string
  message_type?: MessageType
  metadata?: Record<string, unknown>
}
