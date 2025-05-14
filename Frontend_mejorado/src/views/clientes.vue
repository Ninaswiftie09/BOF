<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

// Función de navegación
function go (path) {
  router.push(path) // Redirige a la ruta que recibe como argumento
}
</script>

<template>
  <div class="crm-home">

    <!-- Barra superior -->
    <header class="top-bar">
      <!-- Logo como botón, redirigiendo al Home -->
      <img src="@/assets/logo_bof_blanco.png" alt="Logo del cliente" class="logo" @click="go('/home')"/>

      <h1>CLIENTES Y PROVEEDORES</h1>

      <!-- Botón de avatar -->
      <button class="avatar-btn"></button>
    </header>

    <!-- Contenedor central -->
    <main class="cards-wrapper">
      <button class="big-card" @click="go('/clientesregistro')">
        <span>CLIENTES</span>
      </button>
      <button class="big-card" @click="go('/proveedores')">
        <span>PROVEEDORES</span>
      </button>
    </main>

  </div>
</template>

<style scoped>
.crm-home{
  min-height:100vh;
  background: #0a0f2c;
  display:flex;
  flex-direction:column;
}

/* Top Bar */
.top-bar{
  display:flex;
  align-items:center;
  justify-content: space-between;
  gap:1.5rem;
  padding:.75rem 2rem;
  background: #1e293b;
  color:var(--color-novenary);
  position: relative; /* Para que el logo y texto se ubiquen bien */
}

.logo {
  width: 250px;
  height: 150px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.05); /* Efecto de hover en el logo */
}

/* Centrado y tamaño del texto */
h1 {
  font-family:'Segoe UI', sans-serif;
  color:#ffffff;
  letter-spacing:.5px;
  font-size: 2rem; /* Aumenté el tamaño de la letra */
  flex-grow: 1; /* Asegura que el texto ocupe el espacio y se centre */
  text-align: center; /* Centrado del texto */
}

/* Barra de búsqueda eliminada */

/* Avatar Button */
.avatar-btn{
  width:36px; height:36px;
  border-radius:50%;
  background:var(--color-novenary);
  border:none; cursor:pointer;
}

/* Tarjetas */
.cards-wrapper{
  flex:1; display:flex; justify-content:center; align-items:center;
  gap:3rem; flex-wrap:wrap; padding:2rem;
}

.big-card{
  width:400px;
  height:440px;
  background:rgba(255,255,255,.08);  /* Para la transparencia */
  border:2px solid rgba(255,255,255,.15);
  border-radius:18px; cursor:pointer;
  backdrop-filter:blur(4px);
  box-shadow:0 4px 20px rgba(0,0,0,.25);
  display:flex; justify-content:center; align-items:center;
  transition:background .2s , transform .2s;

  font-family:'Segoe UI', sans-serif;
  font-size:1.4rem; color:#fff;
}

.big-card:hover{
  background:rgba(0,0,0,.25);                    /* Para oscurecer cuando mi cursor está arriba */
  transform:translateY(-6px) scale(1.03);
}

.big-card span{ pointer-events:none; }

@media (max-width:600px){
  .big-card{ width:180px; height:220px; font-size:1.2rem; }
  .cards-wrapper{ gap:1.5rem; }
}
</style>
