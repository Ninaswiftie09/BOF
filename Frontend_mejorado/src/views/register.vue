<template>
  <div class="register-page">
    <!-- Barra unificada -->
    <NavBar title="REGISTRO DE USUARIO" />

    <!-- Contenido -->
    <div class="background">
      <div class="register-container">
        <h1>Registro de Usuario</h1>

        <form @submit.prevent="handleSubmit" novalidate>
          <div class="input-group">
            <label for="first-name">Nombre</label>
            <input
              type="text"
              id="first-name"
              v-model.trim="firstName"
              placeholder="Ingresa tu nombre"
              required
            />
          </div>

          <div class="input-group">
            <label for="last-name">Apellido</label>
            <input
              type="text"
              id="last-name"
              v-model.trim="lastName"
              placeholder="Ingresa tu apellido"
              required
            />
          </div>

          <div class="input-group">
            <label for="email">Correo electrónico</label>
            <input
              type="email"
              id="email"
              v-model.trim="email"
              placeholder="Ingresa tu correo electrónico"
              required
            />
          </div>

          <div class="input-group">
            <label for="position">Cargo</label>
            <select id="position" v-model="position" required>
              <option value="admin">Administrador</option>
              <option value="Empleado">Empleado</option>
            </select>
          </div>

          <button type="submit" :disabled="loading">
            {{ loading ? 'Registrando…' : 'Registrarse' }}
          </button>

          <p v-if="message" class="feedback" :class="messageType">{{ message }}</p>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import { apiFetch } from '@/utils/api'

export default {
  name: 'RegisterUserView',
  components: { NavBar },
  data() {
    return {
      firstName: '',
      lastName: '',
      email: '',
      position: 'admin',
      loading: false,
      message: '',
      messageType: '' // 'success' | 'error'
    }
  },
  methods: {
    async handleSubmit() {
      this.message = ''
      this.messageType = ''
      if (!this.firstName || !this.lastName || !this.email) {
        this.message = 'Completa todos los campos.'
        this.messageType = 'error'
        return
      }
      this.loading = true
      try {
        const payload = {
          first_name: this.firstName,
          last_name: this.lastName,
          email: this.email,
          // Backend actual usa estos textos:
          role: this.position === 'admin' ? 'Administrador' : 'Empleado'
        }

        const res = await apiFetch('/api/register/', 'POST', payload)

        this.message = res?.message || 'Usuario creado exitosamente'
        this.messageType = 'success'
        // Limpia el formulario
        this.firstName = ''
        this.lastName = ''
        this.email = ''
        this.position = 'admin'
        // Redirige al login
        this.$router.push('/login')
      } catch (err) {
        console.error('Error al registrar usuario:', err)
        this.message = err?.message || 'Error al crear usuario'
        this.messageType = 'error'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.register-page{
  background: var(--color-octonary); /*fondo pantalla detras de imagen*/
  min-height: 100vh;
}

.background {
  background-image: url('@/assets/images/re.jpg'); /*imagen*/
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  min-height: calc(100vh - 120px);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 24px 16px;
}

.register-container {
  width: 100%;
  max-width: 400px;
  padding: 30px;
  background: rgba(255, 255, 255, 0.85); /*fondo ficha "registro usuario" */
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.1); /*borde ficha "registro usuario" */
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25); /*sombreado debajo ficha*/
}

h1 {
  font-family: 'Archivo Black', sans-serif;
  color: var(--colo-texto-negro); /*titulo "resgistro usuario" */
  text-align: center;
  margin-bottom: 20px;
}

.input-group { margin-bottom: 15px; }

.input-group label {
  font-family: 'Kollektif', sans-serif;
  color: var(--colo-texto-negro); /*texto campos*/
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}

.input-group input,
.input-group select {
  width: 100%;
  padding: 10px;
  font-family: 'Kollektif', sans-serif;
  font-size: 16px;
  color: var(--colo-texto-negro); /*texto ingresado input campos*/
  background-color: var(--color-septenary); /*fondo input campos*/
  border: 1px solid var(--color-quinary); /*borde input campos*/
  border-radius: 6px;
}

button {
  background-color: var(--color-secondary); /*fondo boton "registrarse" */
  color: white; /*texto "registrarse" */
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  font-family: 'Kollektif', sans-serif;
  width: 100%;
  border-radius: 8px;
  transition: opacity .2s ease;
}

button[disabled] { opacity: .7; cursor: not-allowed; }
button:hover:not([disabled]) { background-color: var(--color-quaternary); } /*fondo boton "registrarse" cursor arriba */

.feedback {
  margin-top: 12px;
  text-align: center;
  font-family: 'Kollektif', sans-serif;
  font-weight: bold;
}
.feedback.success { color: #0b8f4d; } /*nunca se ve*/
.feedback.error { color: #b00020; } /*mensaje error*/
</style>
