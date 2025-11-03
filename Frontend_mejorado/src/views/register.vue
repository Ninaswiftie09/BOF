<template>
  <div class="page-container">
    <NavBar title="REGISTRO DE USUARIO" />

    <div class="background">
      <div class="auth-card">
        <h1>Registro de Usuario</h1>

        <form @submit.prevent="handleSubmit" novalidate>
          <div class="form-group">
            <label for="first-name" class="form-label">Nombre</label>
            <input
              type="text"
              id="first-name"
              class="form-input"
              v-model.trim="firstName"
              placeholder="Ingresa el nombre"
              required
            />
          </div>

          <div class="form-group">
            <label for="last-name" class="form-label">Apellido</label>
            <input
              type="text"
              id="last-name"
              class="form-input"
              v-model.trim="lastName"
              placeholder="Ingresa el apellido"
              required
            />
          </div>

          <div class="form-group">
            <label for="email" class="form-label">Correo electrónico</label>
            <input
              type="email"
              id="email"
              class="form-input"
              v-model.trim="email"
              placeholder="Ingresa el correo electrónico"
              required
            />
          </div>

          <div class="form-group">
            <label for="position" class="form-label">Cargo</label>
            <select id="position" class="form-input" v-model="position" required>
              <option value="admin">Administrador</option>
              <option value="Empleado">Empleado</option>
            </select>
          </div>

          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Registrando…' : 'Registrarse' }}
          </button>

          <div v-if="message" class="message" :class="messageType === 'success' ? 'success-dark' : 'error-dark'">
            {{ message }}
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import NavBar from '@/components/NavBar.vue';
import { apiFetch } from '@/utils/api';

const router = useRouter();

const firstName = ref('');
const lastName = ref('');
const email = ref('');
const position = ref('admin');
const loading = ref(false);
const message = ref('');
const messageType = ref('');

const handleSubmit = async () => {
  message.value = '';
  messageType.value = '';
  if (!firstName.value || !lastName.value || !email.value) {
    message.value = 'Completa todos los campos.';
    messageType.value = 'error';
    return;
  }
  loading.value = true;
  try {
    const payload = {
      first_name: firstName.value,
      last_name: lastName.value,
      email: email.value,
      role: position.value === 'admin' ? 'Administrador' : 'Empleado'
    };

    const res = await apiFetch('/api/register/', 'POST', payload);

    message.value = res?.message || 'Usuario creado exitosamente. Redirigiendo...';
    messageType.value = 'success';
    
    setTimeout(() => {
      firstName.value = '';
      lastName.value = '';
      email.value = '';
      position.value = 'admin';
      router.push('/login');
    }, 2000);

  } catch (err) {
    console.error('Error al registrar usuario:', err);
    message.value = err?.message || 'Error al crear el usuario. Verifique los datos.';
    messageType.value = 'error';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.page-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.background {
  background-image: url('@/assets/images/re.jpg');
  background-size: cover;
  background-position: center;
  flex-grow: 1;
  display: grid;
  place-items: center;
  padding: var(--spacing-lg);
}

.form-group + .form-group,
.form-group + .btn {
  margin-top: var(--spacing-md);
}

.message {
  margin-top: var(--spacing-md);
}
</style>