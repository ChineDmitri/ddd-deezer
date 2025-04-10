import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { isAuthenticated } from '@/services/authService'

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
        // Optional: Add a query parameter to indicate authentication is required
        query: { authRequired: 'true' },
      })
    } else {
      // User is authenticated, proceed to requested page
      next()
    }
  } else {
    // Route doesn't require authentication, proceed
    next()
  }
})

export default router
