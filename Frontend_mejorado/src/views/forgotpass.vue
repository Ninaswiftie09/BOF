<template>
  <div class="background">
    <div class="forgotpass-container">
      <h1>Recuperar Contraseña</h1>
      <form @submit.prevent="handleSubmit">
        <div class="input-group">
          <label for="email">Correo electrónico</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            placeholder="Ingresa tu correo electrónico"
            required
          />
        </div>

        <button type="submit">Recuperar Contraseña</button>

        <div class="back-to-login">
          <a href="#">Volver al inicio de sesión</a>
        </div>

        <!-- color -->
        <div v-if="message" :style="{ color: success ? 'green' : 'red', marginTop: '10px' }">  
          {{ message }}
        </div>

      </form>
    </div>
  </div>
</template>

<script>
import { apiFetch } from '@/utils/api'

export default {
  name: "ForgotPasswordView",  
  data() {
    return {
      email: "",
      message: "",
      success: false
    };
  },
  methods: {
    async handleSubmit() {
  fetch(`${BASE_URL}/auth/send-code/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: this.email })
  })
    .then(res => res.json())
    .then(data => {
      alert('Código enviado a tu correo');
      this.$router.push({ name: 'NewPassView', query: { email: this.email } });
    })
    .catch(err => {
      console.error(err);
      alert('Error al enviar código');
    });
    }
  }
};
</script>
<style scoped>
.background {
  background-image: url('@/assets/images/re.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.forgotpass-container {
  width: 100%;
  max-width: 400px;
  padding: 2rem;
  background-color: rgba(13, 17, 48, 0.75); /* Fondo azul oscuro semitransparente */
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2); /* Borde blanco sutil */
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

h1 {
  font-family: 'Archivo Black', sans-serif;
  color: var(--color-text-light-primary); /* Texto blanco */
  text-align: center;
  margin-bottom: 1.5rem;
}

.input-group {
  margin-bottom: 1rem;
}

.input-group label {
  font-family: 'Kollektif', sans-serif;
  color: var(--color-text-light-secondary); /* Texto gris claro */
  font-weight: normal;
  display: block;
  margin-bottom: 6px;
}

.input-group input {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  background-color: rgba(0, 0, 0, 0.3); /* Fondo negro semitransparente */
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: var(--color-text-light-primary); /* Texto blanco */
  font-size: 1rem;
}

button {
  background-color: var(--color-action-primary); /* Botón azul */
  color: var(--color-text-light-primary); /* Texto blanco */
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-family: 'Kollektif', sans-serif;
  width: 100%;
  transition: filter .15s ease, transform .05s ease;
}

button:hover:not([disabled]) {
  filter: brightness(1.08);
}

button:active {
  transform: translateY(1px);
}

button[disabled] {
  opacity: 0.7;
  cursor: not-allowed;
}

.back-to-login {
  text-align: center;
  margin-top: 1rem;
}

.back-to-login a {
  font-family: 'Kollektif', sans-serif;
  color: var(--color-text-light-secondary); /* Enlace gris claro */
  text-decoration: none;
  font-size: 0.9rem;
}

.back-to-login a:hover {
  text-decoration: underline;
}
</style>