<template>
  <div class="background">
    <div class="auth-card">
      <h1>Inicio de sesión</h1>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="email" class="form-label">Correo electrónico</label>
          <input
            type="text"
            id="email"
            v-model.trim="email"
            class="form-input"
            placeholder="Ingresa tu correo"
            required
            autocomplete="username"
          />
        </div>

        <div class="form-group">
          <label for="password" class="form-label">Contraseña</label>
          <div class="password-field">
            <input
              :type="showPass ? 'text' : 'password'"
              id="password"
              v-model="password"
              class="form-input"
              placeholder="Ingresa tu contraseña"
              required
              autocomplete="current-password"
            />
            <button
              type="button"
              class="toggle-pass"
              @click="toggleShowPass"
              :aria-label="showPass ? 'Ocultar contraseña' : 'Mostrar contraseña'"
              :title="showPass ? 'Ocultar' : 'Mostrar'"
            >
              <!-- ver -->
              <svg
                v-if="!showPass"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                width="26"
                height="26"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                aria-hidden="true"
              >
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
              <!-- ocultar -->
              <svg
                v-else
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                width="26"
                height="26"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                aria-hidden="true"
              >
                <path d="M17.94 17.94A10.94 10.94 0 0 1 12 20C5 20 1 12 1 12a21.8 21.8 0 0 1 5.06-6.94"/>
                <path d="M10.58 10.58a3 3 0 0 0 4.24 4.24"/>
                <path d="M12 6a10.94 10.94 0 0 1 7.94 5.06 21.8 21.8 0 0 1-2.29 3.12"/>
                <line x1="1" y1="1" x2="23" y2="23"/>
              </svg>
            </button>
          </div>
        </div>

        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ loading ? 'Ingresando…' : 'Iniciar sesión' }}
        </button>

        <router-link to="/forgotpass" class="auth-link">¿Olvidaste tu contraseña?</router-link>
      </form>

      <div v-if="message" class="message" :class="messageType === 'success' ? 'success-dark' : 'error-dark'">
        <p>{{ message }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { apiFetch } from '@/utils/api'
import { useAuthStore } from '@/stores/auth'
import { useCatalogsStore } from '@/stores/catalogs'

const LOGIN_URL = '/api/login/'

export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
      showPass: false,
      loading: false,
      message: '',
      messageType: '',
    }
  },
  methods: {
    async handleSubmit() {
      this.message = ''
      this.messageType = ''

      const email = this.email?.trim()
      const password = this.password?.trim()
      if (!email || !password) {
        this.messageType = 'error'
        this.message = 'Ingresa tu correo y contraseña.'
        return
      }

      this.loading = true
      try {
        const payload = { email, password }
        const data = await apiFetch(LOGIN_URL, 'POST', payload)

        sessionStorage.setItem('isLoggedIn', 'true')

        const userResponse = await fetch('/api/me/', { 
          credentials: 'include' 
        })
        
        if (!userResponse.ok) {
          throw new Error('No se pudieron obtener los datos del usuario')
        }
        
        const userData = await userResponse.json()
        console.log('📦 Datos de /api/me/:', userData)

        const authStore = useAuthStore()
        const catalogsStore = useCatalogsStore()

        authStore.setAuth({
          token: 'session-cookie',
          user: {
            id: userData.id,
            email: userData.email,
            nombre: userData.first_name,
            rol: userData.role 
          },
          role: userData.role
        })

        catalogsStore.fetchAll().catch(err => {
          console.warn('No se pudieron cargar catálogos:', err)
        })

        this.messageType = 'success'
        this.message = '¡Bienvenida! Inicio de sesión exitoso.'
        
        const next = this.$route?.query?.next || '/home'
        this.$router.replace(next)
      } catch (err) {
        let msg = 'Credenciales incorrectas o error al iniciar sesión.'
        try {
          const parsed = JSON.parse(err.message)
          msg = parsed.message || parsed.detail || msg
        } catch (_) {
          if (err?.message) msg = err.message
        }
        this.message = msg
        this.messageType = 'error'
        console.error('Error en login:', err)
      } finally {
        this.loading = false
      }
    },
    toggleShowPass() {
      this.showPass = !this.showPass
    },
  },
}
</script>

<style scoped>
.background {
  background-image: url('@/assets/images/fondo.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  min-height: 100vh;
  display: grid;
  place-items: center;
  overflow: hidden;
}

.form-group + .form-group {
  margin-top: var(--spacing-md);
}

.password-field {
  position: relative;
}

.password-field .form-input {
  padding-right: 52px;
}

.toggle-pass {
  position: absolute;
  right: var(--spacing-xs);
  top: 50%;
  transform: translateY(-50%);
  border: none;
  background: transparent;
  cursor: pointer;
  padding: var(--spacing-xxs);
  width: 36px;
  height: 36px;
  line-height: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-light-secondary);
  transition: color 0.2s ease;
}

.toggle-pass:hover {
  color: var(--color-text-light-primary);
  opacity: 1;
}

.toggle-pass:focus-visible {
  outline: 2px solid var(--color-action-primary);
  border-radius: 6px;
}
</style>