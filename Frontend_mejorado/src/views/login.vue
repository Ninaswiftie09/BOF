<template>
  <div class="background">
    <div class="login-container">
      <h1>Inicio de sesión</h1>

      <form @submit.prevent="handleSubmit">
        <div class="input-group">
          <label for="email">Correo electrónico</label>
          <input
            type="email"
            id="email"
            v-model.trim="email"
            placeholder="Ingresa tu correo electrónico"
            required
            autocomplete="username"
          />
        </div>

        <div class="input-group">
          <label for="password">Contraseña</label>
          <div class="password-field">
            <input
              :type="showPass ? 'text' : 'password'"
              id="password"
              v-model="password"
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
              <!-- 👁️ ver -->
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
              <!-- 🚫👁️ ocultar -->
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

        <button type="submit" :disabled="loading">
          {{ loading ? 'Ingresando…' : 'Iniciar sesión' }}
        </button>

        <div class="forgot-password">
          <router-link to="/forgotpass">¿Olvidaste tu contraseña?</router-link>
        </div>
      </form>

      <div v-if="message" class="msg" :class="messageType">
        <p>{{ message }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { apiFetch } from '@/utils/api' // si no tienes alias "@", usa: '../utils/api'

const LOGIN_URL = '/api/login/' // cambia solo esta ruta si tu backend usa otra

export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
      showPass: false,
      loading: false,
      message: '',
      messageType: '', // 'error' | 'success'
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

        if (data && data.user) {
          sessionStorage.setItem('user', JSON.stringify(data.user))
        }
        sessionStorage.setItem('isLoggedIn', 'true')

        this.messageType = 'success'
        this.message = '¡Bienvenida! Inicio de sesión exitoso.'
        const next = this.$route?.query?.next || '/home'
        this.$router.replace(next)
      } catch (err) {
        this.messageType = 'error'
        this.message = err?.message || 'No se pudo iniciar sesión.'
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

.login-container {
  width: 100%;
  max-width: 400px;
  padding: 30px;
  background: rgba(255, 255, 255, 0.1); /* fondo tarjeta login */
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.3); /* borde tarjeta login */
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25); /* sombreado tarjeta login */
}

h1 {
  font-family: 'Archivo Black', sans-serif;
  color: var(--colo-texto-negro); /* texto Inicio sesion */
  text-align: center;
  margin-bottom: 20px;
}

.input-group { margin-bottom: 15px; }

.input-group label {
  font-family: 'Kollektif', sans-serif;
  color: var(--colo-texto-negro); /* texto correo y contrasenna */
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}

.input-group input {
  width: 100%;
  padding: 10px;
  font-family: 'Kollektif', sans-serif;
  font-size: 16px;
  color: var(--colo-texto-negro); /* color texto ingresado */
  background-color: var(--color-septenary); /* fondo input */
  border: 1px solid var(--color-quinary); /* borde input */
  border-radius: 4px;
}

.password-field {
  position: relative;
}

.password-field input {
  padding-right: 52px; /* más espacio para el ojito más grande */
}

.toggle-pass {
  position: absolute;
  right: 6px;
  top: 50%;
  transform: translateY(-50%);
  border: none;
  background: transparent;
  cursor: pointer;
  padding: 6px;         /* área clic cómoda */
  width: 36px;          /* objetivo táctil ~36px */
  height: 36px;
  line-height: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--colo-texto-negro);
}

.toggle-pass:hover {
  opacity: 0.9;
}

.toggle-pass:focus-visible {
  outline: 2px solid var(--color-quinary);
  border-radius: 6px;
}

button {
  background-color: var(--color-secondary); /* fondo boton iniciar sesion */
  color: #fff; /* texto boton iniciar sesion */
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  font-family: 'Kollektif', sans-serif;
  width: 100%;
  transition: background-color .2s ease;
}

button[disabled] { opacity: .7; cursor: not-allowed; }

button:hover:not([disabled]) {
  background-color: var(--color-quaternary); /* color con cursor arriba */
}

.forgot-password { text-align: center; margin-top: 10px; }

.forgot-password a {
  font-family: 'Kollektif', sans-serif;
  color: var(--color-quinary);
  text-decoration: none;
}

.forgot-password a:hover {
  color: var(--colo-texto-negro);
}

.msg {
  margin-top: 16px;
  text-align: center;
  font-family: 'Kollektif', sans-serif;
  font-weight: bold;
}

.msg.success {
  color: #0f5132;
  background: #d1e7dd;
  border: 1px solid #badbcc;
  padding: 8px;
  border-radius: 8px;
}

.msg.error {
  color: #842029; /* texto cuadro error */
  background: #f8d7da; /* fondo cuadro error */
  border: 1px solid #f5c2c7; /* borde cuadro error */
  padding: 8px;
  border-radius: 8px;
}
</style>
