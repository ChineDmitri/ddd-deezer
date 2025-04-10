/**
 * Service for authentication operations
 */

const API_BASE_URL = 'http://127.0.0.1:8000/api'

interface RegisterCredentials {
  username: string
  email: string
  password: string
}

interface LoginCredentials {
  username: string
  password: string
}

interface LoginResponse {
  refresh: string
  access: string
}

interface UserProfile {
  username: string
  email: string
  first_name: string
  last_name: string
  birth_date: string | null
  role: string
}

/**
 * Register a new user
 * @param credentials User registration data
 * @returns The created user profile
 */
export async function registerUser(credentials: RegisterCredentials): Promise<UserProfile> {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    })

    if (!response.ok) {
      // If response is not 2xx, attempt to parse error message
      const errorData = await response.json().catch(() => null)
      throw new Error(
        errorData
          ? JSON.stringify(errorData)
          : `Registration failed with status: ${response.status}`,
      )
    }

    const userData: UserProfile = await response.json()
    return userData
  } catch (error) {
    console.error('Registration error:', error)
    throw error
  }
}

/**
 * Login a user
 * @param credentials User login credentials
 * @returns Authentication tokens
 */
export async function loginUser(credentials: LoginCredentials): Promise<LoginResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    })

    if (!response.ok) {
      // If response is not 2xx, attempt to parse error message
      const errorData = await response.json().catch(() => null)
      throw new Error(
        errorData ? JSON.stringify(errorData) : `Login failed with status: ${response.status}`,
      )
    }

    const tokens: LoginResponse = await response.json()
    return tokens
  } catch (error) {
    console.error('Login error:', error)
    throw error
  }
}

/**
 * Get user profile using the authentication token
 * @param token Access token
 * @returns User profile
 */
export async function getUserProfile(token: string): Promise<UserProfile> {
  try {
    const response = await fetch(`${API_BASE_URL}/users/me/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (!response.ok) {
      throw new Error(`Failed to get user profile: ${response.status}`)
    }

    const userData: UserProfile = await response.json()
    return userData
  } catch (error) {
    console.error('Error fetching user profile:', error)
    throw error
  }
}

/**
 * Store user authentication data in localStorage
 * @param tokens Authentication tokens
 * @param user User profile
 */
export function storeAuthData(tokens: LoginResponse, user: UserProfile): void {
  localStorage.setItem('accessToken', tokens.access)
  localStorage.setItem('refreshToken', tokens.refresh)
  localStorage.setItem('user', JSON.stringify(user))
}

/**
 * Get access token from storage
 * @returns Access token or null if not found
 */
export function getAccessToken(): string | null {
  return localStorage.getItem('accessToken')
}

/**
 * Check if user is authenticated
 * @returns Boolean indicating if user is authenticated
 */
export function isAuthenticated(): boolean {
  return localStorage.getItem('accessToken') !== null
}

/**
 * Get current user profile
 * @returns User profile or null if not authenticated
 */
export function getCurrentUser(): UserProfile | null {
  const userJson = localStorage.getItem('user')
  return userJson ? JSON.parse(userJson) : null
}

/**
 * Logout current user
 */
export function logout(): void {
  localStorage.removeItem('accessToken')
  localStorage.removeItem('refreshToken')
  localStorage.removeItem('user')
}
