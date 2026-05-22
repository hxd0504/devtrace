import type { Conversation } from '@/types/conversation'

let nextId = 100

export const mockImportApi = {
  importChatGPT(data: { url?: string; content: string }): Promise<Conversation> {
    const conv: Conversation = {
      id: nextId++,
      workspace_id: 1,
      title: `ChatGPT 导入 - ${new Date().toLocaleDateString('zh-CN')}`,
      source: 'chatgpt_web',
      created_by: 1,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    }
    return Promise.resolve(conv)
  },
  importManual(data: { title: string; content: string }): Promise<Conversation> {
    const conv: Conversation = {
      id: nextId++,
      workspace_id: 1,
      title: data.title,
      source: 'manual_import',
      created_by: 1,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    }
    return Promise.resolve(conv)
  },
}
