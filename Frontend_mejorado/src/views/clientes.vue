<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

function go (path) {
  router.push(path)
}
</script>

<template>
  <div class="crm-home">

    <!-- Barra superior (idéntica a Home) -->
    <header class="top-bar">
      
      <h1>CLIENTES</h1>

      <input placeholder="Buscar elementos exactos" class="search"/>

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


/* Top Bar*/
.top-bar{
  display:flex;
  align-items:center;
  justify-content: space-between;
  gap:1.5rem;
  padding:.75rem 2rem;
  background: #1e293b;
  color:var(--color-novenary);
}


h1{
  font-family:'Segoe UI', sans-serif;
  color:#ffffff;
  letter-spacing:.5px;
  }

.search{
  flex:1 1 420px;
  max-width:420px;
  margin:0 auto;
  padding:.4rem .8rem;
  border-radius:6px;
  border:none;
  background:var(--color-novenary);
  color:var(--color-senary);
}
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
