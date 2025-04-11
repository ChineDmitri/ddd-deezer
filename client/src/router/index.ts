import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { isAuthenticated, getCurrentUser } from '@/services/authService'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/map',
      name: 'map',
      component: () => import('../views/MapView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/admin-ui',
      name: 'admin',
      component: () => import('../views/AdminView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
    },
  ],
})

// Navigation guard to redirect unauthenticated users to home page
router.beforeEach((to, from, next) => {
  // Check if the route requires authentication
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    // Check if user is authenticated
    if (!isAuthenticated()) {
      // If not authenticated, redirect to home page
      next({
        path: '/',
        query: { authRequired: 'true' },
      })
    } 
    // Check if route requires admin role
    else if (to.matched.some((record) => record.meta.requiresAdmin)) {
      const user = getCurrentUser()
      if (user?.role !== 'admin') {
        // User is not an admin, redirect to home
        next({
          path: '/',
          query: { accessDenied: 'true' },
        })
      } else {
        // User is an admin, proceed
        next()
      }
    }
    else {
      // User is authenticated, proceed to requested page
      next()
    }
  } else {
    // Route doesn't require authentication, proceed
    next()
  }
})

export default router
