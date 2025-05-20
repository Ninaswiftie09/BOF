<script setup>
import { useRouter } from 'vue-router'
import NavBar        from '@/components/NavBar.vue'

const router = useRouter()
const go = path => router.push(path)
</script>

<template>
  <!-- CHANGE: envolvemos todo en un div para que las clases .crm-home existan -->
  <div class="crm-home">

    <!-- Barra superior -->
    <NavBar title="CLIENTES Y PROVEEDORES">
    </NavBar>

    <!-- Tarjetas -->
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
  background:#0a0f2c;
  display:flex; flex-direction:column;
}

/* Tarjetas */
.cards-wrapper{
  flex:1;display:flex;justify-content:center;align-items:center;
  gap:3rem;flex-wrap:wrap;padding:2rem;
}
.big-card{
  width:400px;height:440px;
  background:rgba(255,255,255,.08);
  border:2px solid rgba(255,255,255,.15);
  border-radius:18px;cursor:pointer;
  backdrop-filter:blur(4px);
  box-shadow:0 4px 20px rgba(0,0,0,.25);
  display:flex;justify-content:center;align-items:center;
  transition:background .2s , transform .2s;
  font-family:'Segoe UI',sans-serif;font-size:1.4rem;color:#fff;
}
.big-card:hover{
  background:rgba(0,0,0,.25);
  transform:translateY(-6px) scale(1.03);
}
.big-card span{pointer-events:none;}

@media (max-width:600px){
  .big-card{width:180px;height:220px;font-size:1.2rem;}
  .cards-wrapper{gap:1.5rem;}
}
</style>

