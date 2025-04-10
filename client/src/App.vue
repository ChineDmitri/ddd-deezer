<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue'

const showAuthForm = ref(false)
const authMode = ref('login') // 'login' or 'register'

const toggleAuthForm = () => {
  showAuthForm.value = !showAuthForm.value
}

const switchAuthMode = () => {
  authMode.value = authMode.value === 'login' ? 'register' : 'login'
}
</script>

<template>
  <div class="app-container">
    <header>
      <div class="logo-container">
        <img alt="Music logo" class="logo" src="@/assets/logo.svg" width="50" height="50" />
        <h1>Recommendation Music</h1>
      </div>

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
        <RouterLink to="/map">Regions</RouterLink>
        <RouterLink to="/recommendations">For You</RouterLink>
        <button @click="toggleAuthForm" class="auth-button">
          {{ showAuthForm ? 'Close' : 'Login' }}
        </button>
      </nav>
    </header>

    <main>
      <div class="content-container">
        <!-- Authentication form -->
        <div v-if="showAuthForm" class="auth-form-container">
          <div class="auth-form">
            <h2>{{ authMode === 'login' ? 'Login' : 'Create Account' }}</h2>

            <form @submit.prevent>
              <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" placeholder="Your email">
              </div>

              <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" placeholder="Your password">
              </div>

              <div v-if="authMode === 'register'" class="form-group">
                <label for="confirmPassword">Confirm Password</label>
                <input type="password" id="confirmPassword" placeholder="Confirm password">
              </div>

              <button type="submit" class="submit-button">
                {{ authMode === 'login' ? 'Login' : 'Create Account' }}
              </button>
            </form>

            <div class="auth-switch">
              <span v-if="authMode === 'login'">
                Don't have an account?
                <button @click="switchAuthMode" class="text-button">Create Account</button>
              </span>
              <span v-else>
                Already have an account?
                <button @click="switchAuthMode" class="text-button">Login</button>
              </span>
            </div>
          </div>
        </div>

        <!-- Main content -->
        <RouterView />
      </div>
    </main>

    <footer>
      <div class="footer-content">
        <p>&copy; 2025 DDD Music Recommendation Project</p>
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
  --container-width: 1200px;
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
  flex: 1;
  padding: 2rem;
  display: flex;
  justify-content: center;
  position: relative;
  z-index: 1;
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

/* Authentication Styles */
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

.auth-form-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.auth-form {
  background-color: var(--secondary-color);
  border-radius: var(--border-radius);
  padding: 2rem;
  width: 90%;
  max-width: 400px;
  box-shadow: var(--box-shadow);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.auth-form h2 {
  color: var(--primary-color);
  margin-bottom: 1.5rem;
  text-align: center;
}

.form-group {
  margin-bottom: 1.2rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--accent-color);
  font-size: 0.9rem;
}

.form-group input {
  width: 100%;
  padding: 0.8rem;
  border-radius: var(--border-radius);
  border: 1px solid rgba(255, 255, 255, 0.2);
  background-color: rgba(255, 255, 255, 0.1);
  color: var(--text-color);
  font-size: 1rem;
}

.form-group input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(29, 185, 84, 0.2);
}

.submit-button {
  width: 100%;
  background-color: var(--primary-color);
  color: var(--secondary-color);
  border: none;
  border-radius: var(--border-radius);
  padding: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 0.5rem;
  font-size: 1rem;
}

.submit-button:hover {
  background-color: var(--hover-color);
}

.auth-switch {
  margin-top: 1.5rem;
  text-align: center;
  color: var(--accent-color);
  font-size: 0.9rem;
}

.text-button {
  background: none;
  border: none;
  color: var(--primary-color);
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  padding: 0;
  margin-left: 0.3rem;
}

.text-button:hover {
  text-decoration: underline;
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

  .auth-button {
    margin-top: 0.5rem;
  }

  .footer-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
}
</style>