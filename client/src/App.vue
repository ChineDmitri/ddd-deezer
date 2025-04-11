<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { ref, onMounted, computed } from 'vue'
import AuthForm from '@/components/AuthForm.vue'
import { isAuthenticated, getCurrentUser, logout } from '@/services/authService'
import { useRouter } from 'vue-router'

const router = useRouter()
const showAuthForm = ref(false)
const authMode = ref('login') // 'login' or 'register'
const isLoggedIn = ref(false)
const currentUser = ref(null)

// Add isAdmin computed property
const isAdmin = computed(() => {
  return currentUser.value?.role === 'admin'
})

// Check if user is already logged in on component mount
onMounted(() => {
  isLoggedIn.value = isAuthenticated()
  if (isLoggedIn.value) {
    currentUser.value = getCurrentUser()
  }
})

const toggleAuthForm = () => {
  showAuthForm.value = !showAuthForm.value
}

const switchAuthMode = () => {
  authMode.value = authMode.value === 'login' ? 'register' : 'login'
}

// Fix the handleAuthSuccess function to close the form after successful login
const handleAuthSuccess = (user) => {
  isLoggedIn.value = true
  currentUser.value = user
  showAuthForm.value = false  // Changed from true to false to close the form
}

const handleLogout = () => {
  logout()
  isLoggedIn.value = false
  currentUser.value = null
  router.push('/')
}

const formatDate = (date) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(date).toLocaleDateString(undefined, options)
}
</script>

<template>
  <div class="app-container">
    <header>
      <div class="logo-container">
        <img alt="Music logo" class="logo" src="@/assets/logo.svg" width="50" height="50" />
        <h1>MixMatch</h1>
      </div>

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/map">Regions</RouterLink>
        <RouterLink v-if="isAdmin" to="/admin-ui">Espace Direction</RouterLink>

        <div v-if="isLoggedIn" class="user-menu">
          <div class="user-profile-container">
            <span class="username">{{ currentUser?.username }}</span>
            <div class="user-tooltip">
              <div class="tooltip-header">
                <strong>{{ currentUser?.username }}</strong>
                <span class="user-role">{{ currentUser?.role }}</span>
              </div>
              <div class="tooltip-content">
                <p v-if="currentUser?.email"><strong>Email:</strong> {{ currentUser?.email }}</p>
                <p v-if="currentUser?.first_name || currentUser?.last_name">
                  <strong>Name:</strong> {{ (currentUser?.first_name || '') + ' ' + (currentUser?.last_name || '') }}
                </p>
                <p v-if="currentUser?.birth_date">
                  <strong>Birth Date:</strong> {{ formatDate(currentUser?.birth_date) }}
                </p>
                <p v-if="currentUser?.favorite_genres">
                  <strong>Favorite Genres:</strong> {{ currentUser?.favorite_genres || 'None specified' }}
                </p>
              </div>
            </div>
          </div>
          <button @click="handleLogout" class="auth-button logout-button">Logout</button>
        </div>
        <button v-else @click="toggleAuthForm" class="auth-button">
          {{ showAuthForm ? 'Close' : 'Login' }}
        </button>
      </nav>
    </header>

    <main>
      <div class="content-container">
        <!-- Utilisation du composant AuthForm -->
        <AuthForm :showAuthForm="showAuthForm" :authMode="authMode" @close="toggleAuthForm" @switchMode="switchAuthMode"
          @authSuccess="handleAuthSuccess" />

        <!-- Main content -->
        <RouterView />
      </div>
    </main>

    <footer>
      <div class="footer-content">
        <p>&copy; 2025 MixMatch - Project DDD</p>
        <div class="social-links">
          <a href="#" class="social-link">Instagram</a>
          <a href="#" class="social-link">Twitter</a>
          <a href="#" class="social-link">GitHub</a>
        </div>
      </div>
    </footer>
  </div>
</template>


<style>
:root {
  --primary-color: #1db954;
  --secondary-color: #191414;
  --text-color: #ffffff;
  --accent-color: #b3b3b3;
  --hover-color: #1ed760;
  --border-radius: 8px;
  --box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  --glassmorphism-bg: rgba(25, 20, 20, 0.7);
  --glassmorphism-blur: 10px;
  --container-width: 80vw;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Inter', 'Roboto', sans-serif;
  color: var(--text-color);
  line-height: 1.6;
  background: url('@/assets/bg_main.jpg') no-repeat center center fixed;
  background-size: cover;
  min-height: 100vh;
  margin: 0;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: var(--container-width);
  margin: 0 auto;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
  background-color: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(5px);
}

header {
  background-color: var(--glassmorphism-bg);
  backdrop-filter: blur(var(--glassmorphism-blur));
  -webkit-backdrop-filter: blur(var(--glassmorphism-blur));
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo-container h1 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-color);
  text-shadow: 0 0 15px rgba(29, 185, 84, 0.5);
}

.logo {
  filter: drop-shadow(0 0 8px rgba(29, 185, 84, 0.6));
}

nav {
  display: flex;
  gap: 1.8rem;
  align-items: center;
}

nav a {
  text-decoration: none;
  color: var(--accent-color);
  font-weight: 600;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  transition: all 0.3s ease;
  position: relative;
  padding: 0.5rem 0;
}

nav a:hover {
  color: var(--primary-color);
  transform: translateY(-2px);
}

nav a::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background-color: var(--primary-color);
  transition: width 0.3s ease;
}

nav a:hover::before {
  width: 100%;
}

nav a.router-link-active {
  color: var(--primary-color);
  font-weight: 700;
}

nav a.router-link-active::before {
  width: 100%;
  background-color: var(--primary-color);
}

main {
  width: 100%;
  flex: 1;
  padding: 2rem;
  display: flex;
  justify-content: center;
  position: relative;
  z-index: 1;
  margin: 0 auto;
}

.content-container {
  width: 80vw;
  max-width: var(--container-width);
  margin: 0 auto;
  position: relative;
}

main::before {
  content: "";
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: -1;
  pointer-events: none;
}

.content-container {
  width: 100%;
  max-width: var(--container-width);
  margin: 0 auto;
  position: relative;
}

footer {
  background-color: var(--glassmorphism-bg);
  backdrop-filter: blur(var(--glassmorphism-blur));
  -webkit-backdrop-filter: blur(var(--glassmorphism-blur));
  padding: 1.2rem 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-content {
  max-width: var(--container-width);
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.social-links {
  display: flex;
  gap: 1.5rem;
}

.social-link {
  color: var(--accent-color);
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.3s ease;
}

.social-link:hover {
  color: var(--primary-color);
}

.auth-button {
  background-color: var(--primary-color);
  color: var(--secondary-color);
  border: none;
  border-radius: var(--border-radius);
  padding: 0.5rem 1.2rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.auth-button:hover {
  background-color: var(--hover-color);
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  header {
    flex-direction: column;
    padding: 1rem;
  }

  .logo-container {
    margin-bottom: 1rem;
  }

  nav {
    width: 100%;
    justify-content: space-around;
    gap: 0.8rem;
    flex-wrap: wrap;
  }

  nav a {
    font-size: 0.8rem;
  }

  .footer-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.username {
  color: var(--primary-color);
  font-weight: 600;
  font-size: 0.95rem;
}

.logout-button {
  background-color: transparent;
  border: 1px solid var(--primary-color);
  color: var(--primary-color);
}

.logout-button:hover {
  background-color: rgba(29, 185, 84, 0.1);
}

.user-profile-container {
  position: relative;
}

.user-tooltip {
  position: absolute;
  top: 100%;
  left: 0;
  background-color: var(--secondary-color);
  color: var(--text-color);
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  padding: 1rem;
  display: none;
  z-index: 10;
}

.user-profile-container:hover .user-tooltip {
  display: block;
}

.tooltip-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.tooltip-header strong {
  font-size: 1rem;
}

.tooltip-header .user-role {
  font-size: 0.85rem;
  color: var(--accent-color);
}

.tooltip-content p {
  margin: 0.3rem 0;
}
</style>