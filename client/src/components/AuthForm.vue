<script setup lang="ts">
import { defineProps, defineEmits, ref } from 'vue';
import { registerUser, loginUser, storeAuthData, completeLoginProcess, getDetailedUserProfile } from '@/services/authService';

const props = defineProps({
  showAuthForm: Boolean,
  authMode: String
});

const emit = defineEmits(['close', 'switchMode', 'authSuccess']);

// Form data
const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');

// Form state
const isSubmitting = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const closeForm = () => {
  emit('close');
  // Reset form
  resetForm();
};

const switchMode = () => {
  // Reset form and error message when switching modes
  resetForm();
  emit('switchMode');
};

const resetForm = () => {
  username.value = '';
  email.value = '';
  password.value = '';
  confirmPassword.value = '';
  errorMessage.value = '';
  successMessage.value = '';
};

const validateForm = () => {
  // Reset error message
  errorMessage.value = '';

  // Login validation
  if (props.authMode === 'login') {
    if (!username.value) {
      errorMessage.value = 'Username is required';
      return false;
    }

    if (!password.value) {
      errorMessage.value = 'Password is required';
      return false;
    }

    return true;
  }

  // Registration validation
  if (!username.value) {
    errorMessage.value = 'Username is required';
    return false;
  }

  if (!email.value) {
    errorMessage.value = 'Email is required';
    return false;
  }

  if (!password.value) {
    errorMessage.value = 'Password is required';
    return false;
  }

  if (password.value.length < 8) {
    errorMessage.value = 'Password must be at least 8 characters';
    return false;
  }

  if (password.value !== confirmPassword.value) {
    errorMessage.value = 'Passwords do not match';
    return false;
  }

  return true;
};

const handleSubmit = async () => {
  if (!validateForm()) {
    return;
  }

  isSubmitting.value = true;

  try {
    if (props.authMode === 'register') {
      // Register new user
      const user = await registerUser({
        username: username.value,
        email: email.value,
        password: password.value
      });

      // After registration, use completeLoginProcess to login and fetch user profile
      const { tokens, profile } = await completeLoginProcess({
        username: username.value,
        password: password.value
      });

      successMessage.value = 'Account created successfully!';

      // Pour l'inscription
      setTimeout(() => {
        emit('authSuccess', profile);
        closeForm();
      }, 1500);
    } else {
      // Login user and fetch complete profile in one step
      const { tokens, profile } = await completeLoginProcess({
        username: username.value,
        password: password.value
      });

      successMessage.value = 'Login successful!';

      // Pour la connexion
      setTimeout(() => {
        emit('authSuccess', profile);
        closeForm();
      }, 1000);
    }
  } catch (error) {
    if (error instanceof Error) {
      errorMessage.value = error.message;
      // Try to parse error message if it's JSON
      try {
        const parsedError = JSON.parse(error.message);
        errorMessage.value = Object.values(parsedError).flat().join(', ');
      } catch {
        // Use error message as is if it's not JSON
        errorMessage.value = error.message;
      }
    } else {
      errorMessage.value = 'An unknown error occurred';
    }
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<template>
  <div v-if="showAuthForm" class="auth-form-container">
    <div class="auth-form">
      <div class="auth-form-header">
        <h2>{{ authMode === 'login' ? 'Login' : 'Create Account' }}</h2>
        <button class="close-button" @click="closeForm">×</button>
      </div>

      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="username">Username</label>
          <input type="text" id="username" v-model="username" placeholder="Your username" :disabled="isSubmitting"
            autofocus>
        </div>

        <div v-if="authMode === 'register'" class="form-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="email" placeholder="Your email" :disabled="isSubmitting">
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" placeholder="Your password" :disabled="isSubmitting">
        </div>

        <div v-if="authMode === 'register'" class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <input type="password" id="confirmPassword" v-model="confirmPassword" placeholder="Confirm password"
            :disabled="isSubmitting">
        </div>

        <button type="submit" class="submit-button" :disabled="isSubmitting">
          <span v-if="isSubmitting" class="spinner"></span>
          {{ authMode === 'login' ? 'Login' : 'Create Account' }}
        </button>
      </form>

      <div class="auth-switch">
        <span v-if="authMode === 'login'">
          Don't have an account?
          <button @click="switchMode" class="text-button" :disabled="isSubmitting">Create Account</button>
        </span>
        <span v-else>
          Already have an account?
          <button @click="switchMode" class="text-button" :disabled="isSubmitting">Login</button>
        </span>
      </div>
    </div>
  </div>
</template>

<style>
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

.auth-form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.auth-form h2 {
  color: var(--primary-color);
  margin: 0;
  text-align: center;
  flex-grow: 1;
}

.close-button {
  background: none;
  border: none;
  color: var(--accent-color);
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.close-button:hover {
  color: var(--text-color);
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
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.submit-button:hover {
  background-color: var(--hover-color);
}

.submit-button:disabled {
  background-color: var(--accent-color);
  cursor: not-allowed;
  opacity: 0.7;
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

.text-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-message {
  background-color: rgba(255, 59, 48, 0.2);
  color: #ff3b30;
  padding: 0.8rem;
  border-radius: var(--border-radius);
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.success-message {
  background-color: rgba(52, 199, 89, 0.2);
  color: #34c759;
  padding: 0.8rem;
  border-radius: var(--border-radius);
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid var(--secondary-color);
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 8px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>