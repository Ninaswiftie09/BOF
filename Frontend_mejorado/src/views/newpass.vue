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

<script setup>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { BASE_URL } from '@/config';

const pasoActual = ref(1);
const codigo = ref('');
const nuevaContrasena = ref('');
const confirmarContrasena = ref('');
const message = ref('');
const messageType = ref('');

const router = useRouter();
const route = useRoute();
const email = route.query.email || '';  // Email viene desde forgotpass.vue

async function handleVerificarCodigo() {
  message.value = '';

  if (!codigo.value) {
    message.value = 'Por favor, ingresa el código.';
    messageType.value = 'error';
    return;
  }

  // ⚠️ no hacemos nada más aquí,
  // solo pasamos al siguiente paso
  pasoActual.value = 2;
  message.value = '';
}

async function handleNuevaContrasena() {
  message.value = '';

  if (nuevaContrasena.value !== confirmarContrasena.value) {
    message.value = 'Las contraseñas no coinciden.';
    messageType.value = 'error';
    return;
  }

  try {
    const response = await fetch(`${BASE_URL}/api/auth/verify-reset/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email,
        code: codigo.value,
        new_password: nuevaContrasena.value
      })
    });

    const result = await response.json();

    if (response.ok) {
      message.value = 'Contraseña cambiada con éxito. Redirigiendo...';
      messageType.value = 'success';
      setTimeout(() => router.push('/login'), 2000);
    } else {
      message.value = result.message || 'Error al cambiar contraseña.';
      messageType.value = 'error';
    }
  } catch (error) {
    message.value = 'Error de red.';
    messageType.value = 'error';
  }
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