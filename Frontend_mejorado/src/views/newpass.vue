<template>
  <div class="background">
    <div class="auth-card">
      
      <!-- VERIFICAR CÓDIGO -->
      <div v-if="pasoActual === 1">
        <h1>Verificar Código</h1>
        <form @submit.prevent="handleVerificarCodigo">
          <div class="form-field">
            <label for="codigo" class="form-label">Código de Verificación</label>
            <input
              type="text"
              id="codigo"
              v-model.trim="codigo"
              class="input--auth"
              placeholder="Ingresa el código que recibiste"
              required
            />
          </div>

          <button type="submit" class="btn btn-primary">Verificar</button>
        </form>
      </div>

      <!-- PASO 2: NUEVA CONTRASEÑA -->
      <div v-if="pasoActual === 2">
        <h1>Establecer Nueva Contraseña</h1>
        <form @submit.prevent="handleNuevaContrasena">
          <div class="form-field">
            <label for="password" class="form-label">Nueva Contraseña</label>
            <input
              type="password"
              id="password"
              v-model="nuevaContrasena"
              class="input--auth"
              placeholder="Ingresa tu nueva contraseña"
              required
            />
          </div>
          
          <div class="form-field">
            <label for="confirm-password" class="form-label">Confirmar Contraseña</label>
            <input
              type="password"
              id="confirm-password"
              v-model="confirmarContrasena"
              class="input--auth"
              placeholder="Vuelve a escribir la contraseña"
              required
            />
          </div>

          <button type="submit" class="btn btn-primary">Guardar Contraseña</button>
        </form>
      </div>

      <!-- Mensaje de feedback -->
      <div v-if="message" class="feedback" :class="messageType">
        {{ message }}
      </div>
      
      <router-link to="/login" class="auth-link">Volver al inicio de sesión</router-link>

    </div>
  </div>
</template>

<script>
import { BASE_URL } from '@/config';

export default {
  name: 'NewPassView',
  data() {
    return {
      email: this.$route.query.email || "",  // se recibe por query desde forgotpass.vue
      code: "",
      newPassword: ""
    };
  },
  methods: {
    async handleSubmit() {
      if (!this.email || !this.code || !this.newPassword) {
        alert("Por favor, completa todos los campos.");
        return;
      }

      try {
        const response = await fetch(`${BASE_URL}/auth/reset-password/`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: this.email,
            code: this.code,
            new_password: this.newPassword
          })
        });

        const data = await response.json();

        if (response.ok) {
          alert("Contraseña restablecida con éxito. Ahora puedes iniciar sesión.");
          this.$router.push({ name: "Login" }); // Asegúrate de que exista esta ruta
        } else {
          alert(data.message || "Error al restablecer la contraseña.");
        }
      } catch (error) {
        console.error(error);
        alert("Ocurrió un error. Inténtalo de nuevo más tarde.");
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
  min-height: 100vh;
  display: grid;
  place-items: center;
}

.form-field + .form-field,
.form-field + .btn {
  margin-top: 1rem;
}

.feedback {
  margin-top: 1rem;
  text-align: center;
  font-weight: bold;
}
.feedback.success {
  color: #a7f3d0;
}
.feedback.error {
  color: #fca5a5;
}
</style>