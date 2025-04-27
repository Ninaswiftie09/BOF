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
            v-model="email" 
            placeholder="Ingresa tu correo electrónico"
            required
          />
        </div>

        <div class="input-group">
          <label for="password">Contraseña</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            placeholder="Ingresa tu contraseña"
            required
          />
        </div>

        <button type="submit">Iniciar sesión</button>

        <div class="forgot-password">
          <router-link to="/forgotpass">¿Olvidaste tu contraseña?</router-link>
        </div>

        <div class="create-account">
          <p>¿No tienes cuenta? <router-link to="/register">Crear cuenta</router-link></p>
        </div>
        
      </form>

      <div v-if="message" class="success-message">
        <p>{{ message }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LoginView", 
  data() {
    return {
      email: "",
      password: "",
      message: "" 
    };
  },
  methods: {
  async handleSubmit() {
    const loginData = {
      email: this.email,
      password: this.password
    };

    try {
      const response = await fetch('http://localhost:8000/api/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(loginData)
      });

      if (response.ok) {
        const data = await response.json();
        console.log("Respuesta del servidor:", data);

        this.message = "¡Bienvenido! Inicio de sesión exitoso.";
        this.messageType = "success";
        
        this.email = ''; 
        this.password = '';
        
        this.$router.push('/home'); 

      } else {
        const data = await response.json();
        this.message = data.message || 'Credenciales incorrectas. Intenta de nuevo.';
        this.messageType = "error";
      }
    } catch (error) {
      console.error("Error de login:", error);
      this.message = 'Error al conectar con el servidor. Intenta nuevamente más tarde.';
      this.messageType = "error";
    }
  }
}

};
</script>

<style scoped>
.background {
  background-image: url('@/assets/images/fondo.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.login-container {
  width: 100%;
  max-width: 400px;
  padding: 30px;
  background: rgba(255, 255, 255, 0.1); 
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
}

h1 {
  font-family: 'Archivo Black', sans-serif;
  color: var(--color-primary);
  text-align: center;
  margin-bottom: 20px;
}

.input-group {
  margin-bottom: 15px;
}

.input-group label {
  font-family: 'Kollektif', sans-serif;
  color: var(--color-primary);
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}

.input-group input {
  width: 100%;
  padding: 10px;
  font-family: 'Kollektif', sans-serif;
  font-size: 16px;
  color: var(--color-primary);
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

button:hover {
  background-color: var(--color-quaternary);
}

.forgot-password {
  text-align: center;
  margin-top: 10px;
}

.forgot-password a {
  font-family: 'Kollektif', sans-serif;
  color: var(--color-quinary);
  text-decoration: none;
}

.forgot-password a:hover {
  color: var(--color-primary);
}

.create-account {
  text-align: center;
  margin-top: 10px;
}

.create-account a {
  font-family: 'Kollektif', sans-serif;
  color: var(--color-quinary);
  text-decoration: none;
}

.create-account a:hover {
  color: var(--color-primary);
}

.success-message {
  margin-top: 20px;
  text-align: center;
  font-family: 'Kollektif', sans-serif;
  color: rgb(0, 0, 0);
  font-weight: bold;
}
</style>
