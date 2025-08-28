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
      if (!this.email) {
        this.success = false;
        this.message = "Por favor ingresa tu correo.";
        return;
      }

      try {
        const data = await apiFetch('/api/forgot-password/', 'POST', { email: this.email })
        this.success = true
        this.message = data?.message || "Revisa tu correo para obtener la nueva contraseña."
      } catch (error) {
        console.error("Error:", error)
        this.success = false
        this.message = error?.message || "Error al conectar con el servidor."
      }
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
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.forgotpass-container {
  width: 100%;
  max-width: 400px;
  padding: 30px;
  background: rgba(255, 255, 255, 0.85);
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
}

h1 {
  font-family: 'Archivo Black', sans-serif;
  color: var(--colo-texto-negro);
  text-align: center;
  margin-bottom: 20px;
}

.input-group { margin-bottom: 15px; }

.input-group label {
  font-family: 'Kollektif', sans-serif;
  color: var(--colo-texto-negro);
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}

.input-group input {
  width: 100%;
  padding: 10px;
  font-family: 'Kollektif', sans-serif;
  font-size: 16px;
  color: var(--colo-texto-negro);
  background-color: var(--color-septenary);
  border: 1px solid var(--color-quinary);
  border-radius: 4px;
}

button {
  background-color: var(--color-secondary);
  color: white;
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  font-family: 'Kollektif', sans-serif;
  width: 100%;
}

button:hover { background-color: var(--color-quaternary); }

.back-to-login { text-align: center; margin-top: 10px; }

.back-to-login a {
  font-family: 'Kollektif', sans-serif;
  color: var(--color-quinary);
  text-decoration: none;
}

.back-to-login a:hover { color: var(--colo-texto-negro); }
</style>
