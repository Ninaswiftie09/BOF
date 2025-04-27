<template>
    <div class="background">
      <div class="register-container">
        <h1>Registro de Usuario</h1>
        <form @submit.prevent="handleSubmit">
          <div class="input-group">
            <label for="first-name">Nombre</label>
            <input 
              type="text" 
              id="first-name" 
              v-model="firstName" 
              placeholder="Ingresa tu nombre"
              required
            />
          </div>
  
          <div class="input-group">
            <label for="last-name">Apellido</label>
            <input 
              type="text" 
              id="last-name" 
              v-model="lastName" 
              placeholder="Ingresa tu apellido"
              required
            />
          </div>
  
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
  
          <div class="input-group">
            <label for="position">Cargo</label>
            <select id="position" v-model="position" required>
              <option value="admin">Administrador</option>
              <option value="Empleado">Empleado</option>
            </select>
          </div>
  
          <button type="submit">Registrarse</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "RegisterUserView",  
    data() {
      return {
        firstName: "",
        lastName: "",
        email: "",
        password: "", 
        position: "admin"
      };
    },
    methods: {
      async handleSubmit() {
        const registerData = {
          first_name: this.firstName,
          last_name: this.lastName,
          email: this.email,
          password: this.password,  
          role: this.position === "admin" ? "Administrador" : "Empleado"
        };
  
        try {
          const response = await fetch('http://localhost:8000/api/register/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(registerData)
          });
  
          const result = await response.json();
  
          if (response.ok) {
            alert('Usuario creado exitosamente');
            this.$router.push('/login')
          } else {
            alert(result.message || 'Error al crear usuario');
          }
        } catch (error) {
          console.error("Error al registrar usuario:", error);
          alert('Hubo un problema al enviar la solicitud');
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .background {
    background-color: white;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .register-container {
    width: 100%;
    max-width: 400px;
    padding: 30px;
    background: rgba(255, 255, 255, 0.8);
    border-radius: 12px;
    border: 1px solid rgba(0, 0, 0, 0.1);
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
  
  .input-group input,
  .input-group select {
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
  </style>
  