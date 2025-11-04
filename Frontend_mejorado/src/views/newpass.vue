<template>
  <div class="background">
    <div class="auth-card">

      <!-- PASO 1: VERIFICAR CÓDIGO -->
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

      <!-- PASO 2: NUEVA CONTRASEÑA -->
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
          <div class="password-requirements">
            La contraseña debe tener al menos 6 caracteres, incluyendo mayúsculas, minúsculas, números y símbolos.
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
import { useRouter, useRoute } from 'vue-router';
import { apiFetch } from '@/utils/api';

const pasoActual = ref(1);
const codigo = ref('');
const nuevaContrasena = ref('');
const confirmarContrasena = ref('');
const message = ref('');
const messageType = ref('');

const router = useRouter();
const route = useRoute();
const email = route.query.email || '';

function handleVerificarCodigo() {
  message.value = '';
  if (!codigo.value) {
    message.value = 'Por favor, ingresa el código.';
    messageType.value = 'error';
    return;
  }
  pasoActual.value = 2;
}

async function handleNuevaContrasena() {
  message.value = '';
  if (nuevaContrasena.value !== confirmarContrasena.value) {
    message.value = 'Las contraseñas no coinciden.';
    messageType.value = 'error';
    return;
  }

  try {
    const payload = {
      email,
      code: codigo.value,
      new_password: nuevaContrasena.value
    };
    
    const result = await apiFetch('/api/auth/verify-reset/', 'POST', payload);

    message.value = 'Contraseña cambiada con éxito. Redirigiendo...';
    messageType.value = 'success';
    setTimeout(() => router.push('/login'), 2000);

  } catch (err) {
    message.value = err?.message || 'Error al cambiar la contraseña. El código puede ser incorrecto.';
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
.form-group + .form-group,
.form-group + button {
  margin-top: var(--spacing-md);
}

.password-requirements {
  font-size: 0.8rem;
  color: var(--color-text-light-secondary);
  text-align: center;
  margin: var(--spacing-sm) 0 var(--spacing-md) 0;
  line-height: 1.4;
}

.message {
  margin-top: var(--spacing-md);
}
</style>