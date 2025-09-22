<template>
  <div class="background">
    <div class="login-container">
      <h1>Inicio de sesión</h1>

      <form @submit.prevent="handleSubmit">
        <div class="input-group">
          <label for="email">Correo electrónico</label>
          <input
            type="texto"
            id="email"
            v-model.trim="email"
            placeholder="Ingresa tu correo electrónico"
            required
            autocomplete="username"
          />
        </div>

        <div class="input-group">
          <label for="password">Contraseña</label>
          <input
            :type="showPass ? 'text' : 'password'"
            id="password"
            v-model="password"
            placeholder="Ingresa tu contraseña"
            required
            autocomplete="current-password"
          />
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
import { apiFetch } from '@/utils/api'

export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
      showPass: false,
      loading: false,
      message: '',
      messageType: '' // 'success' | 'error'
    }
  },
  methods: {
    async handleSubmit() {
      this.message = ''
      this.messageType = ''
      this.loading = true
      try {
        const payload = { email: this.email, password: this.password }
        // POST /api/login/ (usa apiFetch → incluye BASE_URL, credenciales y CSRF)
        const data = await apiFetch('/api/login/', 'POST', payload)

        // Marca sesión en el navegador (si usas guard en router)
        sessionStorage.setItem('isLoggedIn', 'true')
        // Puedes guardar info de usuario si el backend la devuelve:
        if (data && data.user) {
          sessionStorage.setItem('user', JSON.stringify(data.user))
        }

        this.message = '¡Bienvenido! Inicio de sesión exitoso.'
        this.messageType = 'success'
        this.email = ''
        this.password = ''

        const next = this.$route.query.next || '/home'
        this.$router.replace(next)
      } catch (err) {
        // Intenta extraer mensaje legible si vino JSON
        let msg = 'Credenciales incorrectas o error al iniciar sesión.'
        try {
          const parsed = JSON.parse(err.message)
          msg = parsed.message || parsed.detail || msg
        } catch (_) {
          if (err?.message) msg = err.message
        }
        this.message = msg
        this.messageType = 'error'
      } finally {
        this.loading = false
      }
    }
  }
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
  background: rgba(255, 255, 255, 0.1); /*fondo tarjeta login*/
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.3); /*borde tarjeta login*/
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25); /*sombreado tarjeta login*/
}

h1 {
  font-family: 'Archivo Black', sans-serif;
  color: var(--colo-texto-negro); /*texto Inicio sesion*/
  text-align: center;
  margin-bottom: 20px;
}

.input-group { margin-bottom: 15px; }
.input-group label {
  font-family: 'Kollektif', sans-serif;
  color: var(--colo-texto-negro); /*texto correo y contrasenna*/
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}
.input-group input {
  width: 100%;
  padding: 10px;
  font-family: 'Kollektif', sans-serif;
  font-size: 16px;
  color: var(--colo-texto-negro); /*color texto ingresado*/
  background-color: var(--color-septenary); /*fondo input correo y contrasenna*/
  border: 1px solid var(--color-quinary); /*borde input correo y contrasenna*/
  border-radius: 4px;
}

button {
  background-color: var(--color-secondary); /*fondo boton iniciar sesion*/
  color: #fff; /*texto boton iniciar sesion*/
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  font-family: 'Kollektif', sans-serif;
  width: 100%;
  transition: background-color .2s ease;
}
button[disabled] { opacity: .7; cursor: not-allowed; }
button:hover:not([disabled]) {
  background-color: var(--color-quaternary); /*color con cursor arriba*/
}

.forgot-password { text-align: center; margin-top: 10px; }
.forgot-password a {
  font-family: 'Kollektif', sans-serif;
  color: var(--color-quinary); /*nada*/
  text-decoration: none;
}
.forgot-password a:hover {
  color: var(--colo-texto-negro); /*nada*/
}

.msg {
  margin-top: 16px;
  text-align: center;
  font-family: 'Kollektif', sans-serif;
  font-weight: bold;
}

.msg.success {
  color: #0f5132; /*nunca se ve*/
  background: #d1e7dd; /*nunca se ve*/
  border: 1px solid #badbcc; /*nunca se ve*/
  padding: 8px;
  border-radius: 8px;
}

.msg.error {
  color: #842029; /*texto cuadro error*/
  background: #f8d7da; /*fondo cuadro error*/
  border: 1px solid #f5c2c7; /*borde cuadro error*/
  padding: 8px;
  border-radius: 8px; }
</style>
