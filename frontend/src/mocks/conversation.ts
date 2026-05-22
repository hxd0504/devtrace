import type { Conversation, Message } from '@/types/conversation'

const mockConversations: Conversation[] = [
  {
    id: 1,
    workspace_id: 1,
    title: '用户登录功能开发',
    source: 'devtrace',
    created_by: 1,
    created_at: '2026-05-22T10:00:00Z',
    updated_at: '2026-05-22T10:00:00Z',
  },
  {
    id: 2,
    workspace_id: 1,
    title: 'Docker 镜像构建问题',
    source: 'devtrace',
    created_by: 1,
    created_at: '2026-05-22T09:00:00Z',
    updated_at: '2026-05-22T09:30:00Z',
  },
]

const mockMessages: Record<number, Message[]> = {
  1: [
    {
      id: 1,
      conversation_id: 1,
      role: 'user',
      content: '帮我实现用户登录功能',
      message_type: 'text',
      metadata: {},
      created_at: '2026-05-22T10:00:00Z',
    },
    {
      id: 2,
      conversation_id: 1,
      role: 'assistant',
      content: '好的，我来分析需求。用户登录功能需要以下组件：\n1. 登录表单（用户名+密码）\n2. JWT 认证逻辑\n3. 路由守卫\n4. 用户状态管理',
      message_type: 'text',
      metadata: {},
      created_at: '2026-05-22T10:00:05Z',
    },
    {
      id: 3,
      conversation_id: 1,
      role: 'system',
      content: 'Claude Code 已开始执行登录模块代码生成',
      message_type: 'system_notify',
      metadata: { ai_tool: 'Claude Code' },
      created_at: '2026-05-22T10:00:10Z',
    },
    {
      id: 4,
      conversation_id: 1,
      role: 'assistant',
      content: '执行完成。已生成 Login.vue、auth store、API 接口。文件已写入项目目录。',
      message_type: 'execution_result',
      metadata: { files_created: ['Login.vue', 'auth.ts', 'authApi.ts'] },
      created_at: '2026-05-22T10:01:00Z',
    },
  ],
  2: [
    {
      id: 5,
      conversation_id: 2,
      role: 'user',
      content: 'Docker 镜像拉取超时怎么解决？',
      message_type: 'text',
      metadata: {},
      created_at: '2026-05-22T09:00:00Z',
    },
    {
      id: 6,
      conversation_id: 2,
      role: 'assistant',
      content: '常见原因：\n1. 网络问题 - 检查服务器网络连通性\n2. 镜像源配置 - 配置国内镜像源\n3. 代理设置 - 检查 HTTP_PROXY 环境变量',
      message_type: 'text',
      metadata: {},
      created_at: '2026-05-22T09:00:05Z',
    },
    {
      id: 7,
      conversation_id: 2,
      role: 'assistant',
      content: '知识提取：Docker 镜像拉取失败排查思路 → 已保存到知识库',
      message_type: 'knowledge_extract',
      metadata: { thought_chain_id: 1 },
      created_at: '2026-05-22T09:30:00Z',
    },
  ],
}

let nextId = 3
let nextMsgId = 8

export const mockConversationApi = {
  list(workspaceId: number): Promise<Conversation[]> {
    return Promise.resolve(mockConversations.filter((c) => c.workspace_id === workspaceId))
  },
  get(id: number): Promise<Conversation> {
    const conv = mockConversations.find((c) => c.id === id)
    if (!conv) return Promise.reject(new Error('Conversation not found'))
    return Promise.resolve(conv)
  },
  create(data: { workspace_id: number; title?: string }): Promise<Conversation> {
    const conv: Conversation = {
      id: nextId++,
      workspace_id: data.workspace_id,
      title: data.title || null,
      source: 'devtrace',
      created_by: 1,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    }
    mockConversations.push(conv)
    mockMessages[conv.id] = []
    return Promise.resolve(conv)
  },
  getMessages(conversationId: number): Promise<Message[]> {
    return Promise.resolve(mockMessages[conversationId] || [])
  },
  sendMessage(conversationId: number, data: { role: string; content: string; message_type?: string }): Promise<Message> {
    const msg: Message = {
      id: nextMsgId++,
      conversation_id: conversationId,
      role: data.role as Message['role'],
      content: data.content,
      message_type: (data.message_type as Message['message_type']) || 'text',
      metadata: {},
      created_at: new Date().toISOString(),
    }
    if (!mockMessages[conversationId]) mockMessages[conversationId] = []
    mockMessages[conversationId].push(msg)

    // 模拟 AI 自动回复
    if (data.role === 'user') {
      const aiReply: Message = {
        id: nextMsgId++,
        conversation_id: conversationId,
        role: 'assistant',
        content: `收到你的消息：「${data.content}」\n\n我来分析一下这个问题...`,
        message_type: 'text',
        metadata: {},
        created_at: new Date(Date.now() + 1000).toISOString(),
      }
      mockMessages[conversationId].push(aiReply)
    }

    return Promise.resolve(msg)
  },
}
