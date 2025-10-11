import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // State
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const role = ref(localStorage.getItem('role') || null)

  // Getters
  const isAuthenticated = computed(() => !!token.value)
const isAdmin = computed(() => role.value === 'admin')
  const isEmpleado = computed(() => role.value === 'empleado')
  const userName = computed(() => user.value?.nombre || user.value?.email || 'Usuario')

  // Actions
  function setAuth(authData) {
    token.value = authData.token
    user.value = authData.user
    role.value = authData.role || authData.user?.role || authData.user?.rol

    // Persistir en localStorage
    localStorage.setItem('token', authData.token)
    localStorage.setItem('user', JSON.stringify(authData.user))
    localStorage.setItem('role', role.value)
  }

  function logout() {
    token.value = null
    user.value = null
    role.value = null

    // Limpiar localStorage
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('role')
  }

  function updateUser(userData) {
    user.value = { ...user.value, ...userData }
    localStorage.setItem('user', JSON.stringify(user.value))
  }

  return {
    // State
    token,
    user,
    role,
    // Getters
    isAuthenticated,
    isAdmin,
    isEmpleado,
    userName,
    // Actions
    setAuth,
    logout,
    updateUser
  }
})