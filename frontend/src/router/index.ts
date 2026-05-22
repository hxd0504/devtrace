import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', name: 'Login', component: () => import('@/views/Login.vue') },
    { path: '/', redirect: '/workspaces' },
    { path: '/workspaces', name: 'WorkspaceList', component: () => import('@/views/WorkspaceList.vue'), meta: { requiresAuth: true } },
    { path: '/workspace/:id', name: 'WorkspaceDetail', component: () => import('@/views/WorkspaceDetail.vue'), meta: { requiresAuth: true } },
    { path: '/workspace/:id/issue/create', name: 'IssueCreate', component: () => import('@/views/IssueCreate.vue'), meta: { requiresAuth: true } },
    { path: '/workspace/:wid/issue/:id', name: 'IssueDetail', component: () => import('@/views/IssueDetail.vue'), meta: { requiresAuth: true } },
    { path: '/workspace/:wid/issue/:id/task/create', name: 'TaskCreate', component: () => import('@/views/TaskCreate.vue'), meta: { requiresAuth: true } },
  ],
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()

  // 已登录用户不允许访问登录页
  if (to.path === '/login' && authStore.token) {
    return '/workspaces'
  }

  // 未登录用户访问需认证页面
  if (to.meta.requiresAuth && !authStore.token) {
    return '/login'
  }

  // 有 token 但无 user 信息，自动获取用户信息
  if (authStore.token && !authStore.user) {
    try {
      await authStore.fetchMe()
    } catch {
      authStore.logout()
      return '/login'
    }
  }
})

export default router
