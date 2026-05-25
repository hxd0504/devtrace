<template>
  <div class="chat-window">
    <!-- 顶部标题栏 -->
    <div class="chat-header">
      <div class="header-left">
        <h3 v-if="conversation">{{ conversation.title || '新对话' }}</h3>
        <h3 v-else>DevTrace AI 指挥中心</h3>
        <el-tag v-if="conversation" size="small" type="info">{{ conversation.source }}</el-tag>
      </div>
      <div class="header-actions">
        <el-button size="small" :icon="Refresh" @click="loadMessages" />
        <el-dropdown @command="handleCommand">
          <el-button size="small" :icon="MoreFilled" />
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="extract">提取知识</el-dropdown-item>
              <el-dropdown-item command="import">导入对话</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <!-- 消息列表 -->
    <div class="message-list" ref="messageListRef">
      <div v-if="!conversation" class="welcome-screen">
        <el-icon :size="64" color="#c0c4cc"><ChatDotRound /></el-icon>
        <h2>开始新对话</h2>
        <p>输入指令，AI 将自动分析并推荐执行方案</p>
        <div class="quick-actions">
          <el-button @click="quickAction('帮我分析当前项目结构')">分析项目结构</el-button>
          <el-button @click="quickAction('帮我实现用户登录功能')">实现登录功能</el-button>
          <el-button @click="quickAction('Docker 镜像拉取失败怎么解决？')">Docker 问题排查</el-button>
        </div>
      </div>
      <template v-else>
        <MessageBubble
          v-for="msg in messages"
          :key="msg.id"
          :message="msg"
        />
        <div v-if="sending" class="typing-indicator">
          <span></span><span></span><span></span>
        </div>
      </template>
    </div>

    <!-- 输入框 -->
    <MessageInput
      :disabled="!conversation"
      :loading="sending"
      @send="handleSend"
    />

    <!-- 调度弹窗 -->
    <DispatchDialog
      v-if="showDispatch"
      :task-id="dispatchTaskId"
      @close="showDispatch = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ChatDotRound, Refresh, MoreFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import MessageBubble from './MessageBubble.vue'
import MessageInput from './MessageInput.vue'
import DispatchDialog from '@/components/dispatch/DispatchDialog.vue'
import { conversationApi } from '@/api/conversation'
import { knowledgeApi } from '@/api/knowledge'
import type { Conversation, Message } from '@/types/conversation'

const props = defineProps<{ conversationId?: string | number }>()

const route = useRoute()
const router = useRouter()

const conversation = ref<Conversation | null>(null)
const messages = ref<Message[]>([])
const sending = ref(false)
const messageListRef = ref<HTMLElement>()
const showDispatch = ref(false)
const dispatchTaskId = ref(0)

const convId = () => {
  const id = props.conversationId || route.params.conversationId
  return id ? Number(id) : null
}

const loadMessages = async () => {
  const id = convId()
  if (!id) {
    conversation.value = null
    messages.value = []
    return
  }
  try {
    conversation.value = await conversationApi.get(id)
    messages.value = await conversationApi.getMessages(id)
    await nextTick()
    scrollToBottom()
  } catch {
    ElMessage.error('加载对话失败')
  }
}

const scrollToBottom = () => {
  if (messageListRef.value) {
    messageListRef.value.scrollTop = messageListRef.value.scrollHeight
  }
}

const handleSend = async (content: string) => {
  const id = convId()
  if (!id) {
    // 没有对话时，先创建对话
    try {
      const conv = await conversationApi.create({
        workspace_id: 1,
        title: content.slice(0, 50),
      })
      router.push(`/chat/${conv.id}`)
      // 创建后在 watch 中会自动加载
      return
    } catch {
      ElMessage.error('创建对话失败')
      return
    }
  }

  sending.value = true
  try {
    await conversationApi.sendMessage(id, { role: 'user', content })
    // 重新加载消息（mock 中会自动添加 AI 回复）
    await loadMessages()
  } catch {
    ElMessage.error('发送失败')
  } finally {
    sending.value = false
  }
}

const quickAction = (text: string) => {
  handleSend(text)
}

const handleCommand = async (cmd: string) => {
  if (cmd === 'extract') {
    const id = convId()
    if (!id) return
    try {
      await knowledgeApi.extract(id)
      ElMessage.success('知识提取完成')
    } catch {
      ElMessage.error('提取失败')
    }
  } else if (cmd === 'import') {
    // 打开导入对话框（后续实现）
    ElMessage.info('导入功能开发中')
  }
}

watch(() => props.conversationId || route.params.conversationId, loadMessages, { immediate: true })
</script>

<style scoped>
.chat-window {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: #fff;
  border-bottom: 1px solid #ebeef5;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-left h3 {
  margin: 0;
  font-size: 16px;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.welcome-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #909399;
}

.welcome-screen h2 {
  margin: 16px 0 8px;
  color: #303133;
}

.quick-actions {
  display: flex;
  gap: 8px;
  margin-top: 20px;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 12px 16px;
  width: fit-content;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #c0c4cc;
  animation: bounce 1.4s infinite ease-in-out both;
}

.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}
</style>
