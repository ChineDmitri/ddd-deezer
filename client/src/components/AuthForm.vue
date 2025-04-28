<script setup lang="ts">
import { defineProps, defineEmits, ref, computed } from 'vue';
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
const firstName = ref('');
const lastName = ref('');
const birthDate = ref('');
const favoriteGenres = ref([]);
const userRole = ref('listener'); // Default role is listener

// Form state
const isSubmitting = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const formErrors = ref({}); // Pour stocker les erreurs par champ

const hasVisibleFieldErrors = computed(() => {
  // Vérifie si des erreurs de champ sont déjà visibles
  return Object.keys(formErrors.value).some(field =>
    document.querySelector(`[data-field="${field}"] .field-error`) !== null
  );
});

const shouldShowGlobalError = computed(() => {
  return errorMessage.value || (Object.keys(formErrors.value).length > 0 && !hasVisibleFieldErrors.value);
});

const globalErrorMessage = computed(() => {
  if (errorMessage.value) {
    return errorMessage.value;
  }

  if (Object.keys(formErrors.value).length > 0) {
    return Object.values(formErrors.value)[0] || 'Please correct the errors in the form.';
  }

  return '';
});

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
  firstName.value = '';
  lastName.value = '';
  birthDate.value = '';
  favoriteGenres.value = [];
  userRole.value = 'listener';
  errorMessage.value = '';
  successMessage.value = '';
  formErrors.value = {};
};

const validateForm = () => {
  // Reset error message
  errorMessage.value = '';
  formErrors.value = {};

  // Login validation
  if (props.authMode === 'login') {
    if (!username.value) {
      formErrors.value.username = 'Username is required';
      return false;
    }

    if (!password.value) {
      formErrors.value.password = 'Password is required';
      return false;
    }

    return true;
  }

  // Registration validation
  let isValid = true;

  if (!username.value) {
    formErrors.value.username = 'Username is required';
    isValid = false;
  }

  if (!email.value) {
    formErrors.value.email = 'Email is required';
    isValid = false;
  } else if (!validateEmail(email.value)) {
    formErrors.value.email = 'Please enter a valid email address';
    isValid = false;
  }

  if (!password.value) {
    formErrors.value.password = 'Password is required';
    isValid = false;
  } else if (password.value.length < 8) {
    formErrors.value.password = 'Password must be at least 8 characters';
    isValid = false;
  }

  if (password.value !== confirmPassword.value) {
    formErrors.value.confirmPassword = 'Passwords do not match';
    isValid = false;
  }

  return isValid;
};

// Fonction de validation d'email
const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
};

const handleRegister = async () => {
  isSubmitting.value = true;
  errorMessage.value = '';
  formErrors.value = {};

  try {
    if (password.value !== confirmPassword.value) {
      formErrors.value.confirmPassword = 'Passwords do not match';
      throw new Error('Passwords do not match.');
    }

    // Formater la date correctement (YYYY-MM-DD)
    let formattedDate = birthDate.value;
    if (birthDate.value) {
      // S'assurer que la date est au format YYYY-MM-DD
      const dateObj = new Date(birthDate.value);
      if (!isNaN(dateObj.getTime())) {
        formattedDate = dateObj.toISOString().split('T')[0]; // Format YYYY-MM-DD
      }
    }

    const user = await registerUser({
      username: username.value,
      password: password.value,
      email: email.value,
      first_name: firstName.value,
      last_name: lastName.value,
      birth_date: formattedDate,
      role: userRole.value,
      favorite_genres: favoriteGenres.value
    });

    const credentials = {
      username: username.value,
      password: password.value
    };

    const { profile } = await completeLoginProcess(credentials);

    successMessage.value = 'Account created successfully!';
    emit('authSuccess', profile);
    resetForm();
  } catch (error) {
    console.error('Error during registration:', error);

    // Traiter les erreurs renvoyées par l'API
    if (error.response && error.response.data) {
      const apiErrors = error.response.data;

      // Traitement amélioré des erreurs d'API
      for (const field in apiErrors) {
        if (Array.isArray(apiErrors[field])) {
          // Personnalisation des messages d'erreur selon le champ
          const errorMessage = apiErrors[field].join(', ');

          // Transformer les messages d'erreur bruts en messages plus conviviaux
          if (field === 'username') {
            if (errorMessage.includes('already exists')) {
              formErrors.value[field] = 'This username is already taken. Please choose another one.';
            } else if (errorMessage.includes('valid username')) {
              formErrors.value[field] = 'Username can only contain letters, numbers, and @/./+/-/_ characters.';
            } else {
              formErrors.value[field] = errorMessage;
            }
          }
          else if (field === 'email') {
            if (errorMessage.includes('valid email')) {
              formErrors.value[field] = 'Please enter a valid email address.';
            } else if (errorMessage.includes('already exists')) {
              formErrors.value[field] = 'This email is already registered. Please use another one.';
            } else {
              formErrors.value[field] = errorMessage;
            }
          }
          else if (field === 'birth_date') {
            if (errorMessage.includes('wrong format')) {
              formErrors.value[field] = 'Please enter a valid date in YYYY-MM-DD format.';
            } else {
              formErrors.value[field] = errorMessage;
            }
          }
          else {
            formErrors.value[field] = errorMessage;
          }
        }
      }

      // Créer un message d'erreur global résumé
      const errorFields = Object.keys(apiErrors);
      if (errorFields.length > 0) {
        // Message d'erreur global plus convivial
        errorMessage.value = 'Please correct the highlighted fields and try again.';
      } else {
        errorMessage.value = error.message || 'Error during registration. Please try again.';
      }
    } else {
      errorMessage.value = error.message || 'Error during registration. Please try again.';
    }
  } finally {
    isSubmitting.value = false;
  }
};

const handleLogin = async () => {
  isSubmitting.value = true;
  errorMessage.value = '';
  formErrors.value = {};

  try {
    const { profile } = await completeLoginProcess({
      username: username.value,
      password: password.value
    });

    successMessage.value = 'Login successful!';
    emit('authSuccess', profile);
    resetForm();
  } catch (error) {
    console.error('Error during login:', error);

    // Traiter les erreurs de login
    if (error.response && error.response.data) {
      // Pour les erreurs d'API spécifiques aux champs
      const apiErrors = error.response.data;

      if (apiErrors.non_field_errors) {
        errorMessage.value = apiErrors.non_field_errors.join(', ');
      } else if (apiErrors.detail) {
        errorMessage.value = apiErrors.detail;
      } else {
        errorMessage.value = 'Invalid credentials. Please try again.';
      }
    } else {
      errorMessage.value = error.message || 'Invalid credentials. Please try again.';
    }
  } finally {
    isSubmitting.value = false;
  }
};

const handleSubmit = async () => {
  if (!validateForm()) {
    return;
  }

  if (props.authMode === 'register') {
    await handleRegister();
  } else {
    await handleLogin();
  }
};
</script>

<template>
  <div v-if="showAuthForm" class="auth-form-overlay">
    <div class="auth-form-container">
      <div class="auth-form-header">
        <h2>{{ authMode === 'login' ? 'Login' : 'Create Account' }}</h2>
        <button @click="$emit('close')" class="close-button">&times;</button>
      </div>

      <div v-if="shouldShowGlobalError" class="error-message">
        {{ globalErrorMessage }}
      </div>

      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>

      <form @submit.prevent="handleSubmit">
        <!-- Login form - maintenir en une colonne -->
        <div v-if="authMode === 'login'">
          <div class="form-group" :class="{ 'has-error': formErrors.username }">
            <label for="username">Username</label>
            <input type="text" id="username" v-model="username" placeholder="Your username" :disabled="isSubmitting"
              autofocus>
            <div v-if="formErrors.username" class="field-error">{{ formErrors.username }}</div>
          </div>

          <div class="form-group" :class="{ 'has-error': formErrors.password }">
            <label for="password">Password</label>
            <input type="password" id="password" v-model="password" placeholder="Your password"
              :disabled="isSubmitting">
            <div v-if="formErrors.password" class="field-error">{{ formErrors.password }}</div>
          </div>
        </div>

        <!-- Registration form - réorganisé en deux colonnes -->
        <div v-else class="register-form-grid">
          <!-- Première colonne -->
          <div class="form-column">
            <div class="form-group" :class="{ 'has-error': formErrors.username }">
              <label for="username">Username*</label>
              <input type="text" id="username" v-model="username" placeholder="Your username" :disabled="isSubmitting"
                autofocus>
              <div v-if="formErrors.username" class="field-error">{{ formErrors.username }}</div>
            </div>

            <div class="form-group" :class="{ 'has-error': formErrors.email }">
              <label for="email">Email*</label>
              <input type="email" id="email" v-model="email" placeholder="Your email" :disabled="isSubmitting">
              <div v-if="formErrors.email" class="field-error">{{ formErrors.email }}</div>
            </div>

            <div class="form-group" :class="{ 'has-error': formErrors.password }">
              <label for="password">Password*</label>
              <input type="password" id="password" v-model="password" placeholder="Your password"
                :disabled="isSubmitting">
              <div v-if="formErrors.password" class="field-error">{{ formErrors.password }}</div>
            </div>

            <div class="form-group" :class="{ 'has-error': formErrors.confirmPassword }">
              <label for="confirmPassword">Confirm Password*</label>
              <input type="password" id="confirmPassword" v-model="confirmPassword" placeholder="Confirm password"
                :disabled="isSubmitting">
              <div v-if="formErrors.confirmPassword" class="field-error">{{ formErrors.confirmPassword }}</div>
            </div>

            <!-- Radio buttons for user role -->
            <div class="form-group role-selection">
              <label>User Role*</label>
              <div class="radio-group">
                <label class="radio-label">
                  <input type="radio" name="userRole" value="listener" v-model="userRole" :disabled="isSubmitting">
                  <span>Listener</span>
                </label>
                <label class="radio-label">
                  <input type="radio" name="userRole" value="artist" v-model="userRole" :disabled="isSubmitting">
                  <span>Artist</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Deuxième colonne -->
          <div class="form-column">
            <div class="form-group" :class="{ 'has-error': formErrors.firstName }">
              <label for="firstName">First Name</label>
              <input type="text" id="firstName" v-model="firstName" placeholder="Your first name"
                :disabled="isSubmitting">
              <div v-if="formErrors.firstName" class="field-error">{{ formErrors.firstName }}</div>
            </div>

            <div class="form-group" :class="{ 'has-error': formErrors.lastName }">
              <label for="lastName">Last Name</label>
              <input type="text" id="lastName" v-model="lastName" placeholder="Your last name" :disabled="isSubmitting">
              <div v-if="formErrors.lastName" class="field-error">{{ formErrors.lastName }}</div>
            </div>

            <div class="form-group" :class="{ 'has-error': formErrors.birth_date }">
              <label for="birthDate">Birth Date</label>
              <input type="date" id="birthDate" v-model="birthDate" :disabled="isSubmitting">
              <div v-if="formErrors.birth_date" class="field-error">{{ formErrors.birth_date }}</div>
            </div>

            <div class="form-group" :class="{ 'has-error': formErrors.favoriteGenres }">
              <label for="favoriteGenres">Favorite Genres</label>
              <input type="text" id="favoriteGenres" v-model="favoriteGenres" placeholder="Rock, Pop, Jazz..."
                :disabled="isSubmitting">
              <div v-if="formErrors.favoriteGenres" class="field-error">{{ formErrors.favoriteGenres }}</div>
            </div>
          </div>
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
.auth-form-overlay {
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

.auth-form-container {
  background-color: var(--secondary-color);
  border-radius: var(--border-radius);
  padding: 2rem;
  width: 90%;
  max-width: 600px;
  /* Augmenter pour accommoder le layout en colonnes */
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
  white-space: pre-line;
  /* Respecter les sauts de ligne */
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

/* Ajout des styles pour la mise en page en deux colonnes */
.register-form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-column {
  display: flex;
  flex-direction: column;
}

/* Réduire légèrement les marges des éléments de formulaire pour les colonnes */
.register-form-grid .form-group {
  margin-bottom: 0.8rem;
}

/* Ajout d'un style pour les champs requis */
.register-form-grid label::after {
  content: '*';
  color: var(--primary-color);
  margin-left: 2px;
}

/* Mais enlever l'astérisque pour les champs facultatifs */
.register-form-grid .form-group:nth-child(n+5) label::after {
  content: '';
}

/* Styles pour les erreurs de champ */
.has-error input {
  border-color: #ff3b30;
  background-color: rgba(255, 59, 48, 0.05);
}

.field-error {
  color: #ff3b30;
  font-size: 0.8rem;
  margin-top: 0.3rem;
  font-weight: 500;
}

/* Styles améliorés pour les boutons radio */
.role-selection {
  margin-top: 0.5rem;
}

.radio-group {
  display: flex;
  gap: 1.5rem;
  margin-top: 0.5rem;
  padding: 0.5rem 0;
}

.radio-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
  position: relative;
  padding-left: 28px;
  margin-bottom: 0;
}

/* Cacher le bouton radio natif */
.radio-label input {
  position: absolute;
  opacity: 0;
  height: 0;
  width: 0;
  cursor: pointer;
}

/* Créer un radio personnalisé */
.radio-label:before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  height: 18px;
  width: 18px;
  background-color: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  transition: all 0.2s ease;
}

/* Indicateur du radio sélectionné (le cercle intérieur) */
.radio-label:after {
  content: "";
  position: absolute;
  display: none;
  left: 6px;
  top: 50%;
  transform: translateY(-50%);
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--primary-color);
  transition: all 0.2s ease;
}

/* Afficher l'indicateur quand checked */
.radio-label input:checked~:after {
  display: block;
}

/* Style quand le radio est sélectionné */
.radio-label input:checked~:before {
  border-color: var(--primary-color);
  background-color: rgba(29, 185, 84, 0.1);
}

/* Style au survol */
.radio-label:hover:before {
  border-color: var(--primary-color);
}

/* État coché : input checked + span ::before */
.radio-label input[type="radio"]:checked+span::before {
  border-color: var(--primary-color);
}

.radio-label span {
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--text-color);
  transition: color 0.2s ease;
}

/* Style quand checked pour le texte */
.radio-label input:checked+span {
  color: var(--primary-color);
  font-weight: 600;
}

/* Style disabled */
.radio-label input:disabled+span {
  opacity: 0.6;
  cursor: not-allowed;
}

.radio-label input:disabled~:before {
  background-color: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  cursor: not-allowed;
}

/* Ajuster l'espacement des éléments de formulaire */
.register-form-grid .form-group {
  margin-bottom: 1rem;
}

/* Media query pour revenir à une colonne sur petit écran */
@media (max-width: 640px) {
  .register-form-grid {
    grid-template-columns: 1fr;
    gap: 0;
  }

  .auth-form-container {
    max-width: 400px;
  }

  /* Ajuster l'espacement des éléments de formulaire sur mobile */
  .register-form-grid .form-group {
    margin-bottom: 1.2rem;
  }
}
</style>