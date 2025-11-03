<template>
  <div class="background">
    <div class="auth-card">

    <!-- VERIFICAR CÓDIGO -->
      <div v-if="pasoActual === 1">
        <h1>Verificar Código</h1>
        <form @submit.prevent="handleVerificarCodigo">
          <div class="form-group">
            <label for="codigo" class="form-label">Código de Verificación</label>
            <input
              type="text"
              id="codigo"
              v-model.trim="codigo"
              class="form-input"
              placeholder="Ingresa el código que recibiste"
              required
            />
          </div>

          <button type="submit" class="btn btn-primary">Verificar</button>
        </form>
      </div>

      <!-- NUEVA CONTRASEÑA -->
      <div v-if="pasoActual === 2">
        <h1>Establecer Nueva Contraseña</h1>
        <form @submit.prevent="handleNuevaContrasena">
          <div class="form-group">
            <label for="password" class="form-label">Nueva Contraseña</label>
            <input
              type="password"
              id="password"
              v-model="nuevaContrasena"
              class="form-input"
              placeholder="Ingresa tu nueva contraseña"
              required
            />
          </div>

          <div class="form-group">
            <label for="confirm-password" class="form-label">Confirmar Contraseña</label>
            <input
              type="password"
              id="confirm-password"
              v-model="confirmarContrasena"
              class="form-input"
              placeholder="Vuelve a escribir la contraseña"
              required
            />
          </div>

          <button type="submit" class="btn btn-primary">Guardar Contraseña</button>
        </form>
      </div>

      <!-- Mensaje de feedback -->
      <div v-if="message" class="message" :class="messageType === 'success' ? 'success-dark' : 'error-dark'">
        {{ message }}
      </div>

      <router-link to="/login" class="auth-link">Volver al inicio de sesión</router-link>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

// --- Estado Mínimo para la Interfaz ---
const pasoActual = ref(1);
const codigo = ref('');
const nuevaContrasena = ref('');
const confirmarContrasena = ref('');
const message = ref('');
const messageType = ref('');

const router = useRouter();

// --- Lógica Mínima para Probar el Flujo ---

function handleVerificarCodigo() {
  message.value = '';
  if (!codigo.value) {
    message.value = 'Por favor, ingresa el código.';
    messageType.value = 'error';
    return;
  }

  // Simulacion
  console.log('Simulando verificación del código:', codigo.value);
  message.value = 'Código verificado.';
  messageType.value = 'success';

  // Pasa luego de 1 seg
  setTimeout(() => {
    pasoActual.value = 2;
    message.value = '';
  }, 1000);
}

function handleNuevaContrasena() {
  message.value = '';
  if (nuevaContrasena.value !== confirmarContrasena.value) {
    message.value = 'Las contraseñas no coinciden.';
    messageType.value = 'error';
    return;
  }

  // SIMULACIÓN: Siempre funciona.
  console.log('Simulando cambio de contraseña...');
  message.value = 'Contraseña cambiada con éxito.';
  messageType.value = 'success';

  setTimeout(() => {
    router.push('/login');
  }, 2000);
}
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

.form-group + .form-group,
.form-group + .btn {
  margin-top: var(--spacing-md);
}

</style>