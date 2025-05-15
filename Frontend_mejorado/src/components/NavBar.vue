<!-- src/components/NavBar.vue -->
<template>
  <header class="top-bar nav-gap">

    <!-- Logo clicable a /home -->
    <img
      src="@/assets/logo_bof_blanco.png"
      alt="Logo BOF"
      class="logo"
      @click="$router.push('/home')" />

    <!-- Título -->
    <h1 class="title">{{ title }}</h1>

    <!-- Acciones a la derecha (avatar, switch, etc.) -->
    <div class="ml-auto flex items-center">
      <slot name="actions" />
    </div>

  </header>
</template>

<script setup>
defineProps({
  title: { type: String, required: true }
})
</script>

<style scoped>
.top-bar{
  display:flex;
  align-items:center;
  gap:1.5rem;
  padding:.75rem 2rem;
  background:#1e293b;
}

/* ====== logo añadido ====== */
.logo{
  height:80px;          /* grosor similar a la barra */
  width:auto;
  cursor:pointer;
  
}

/* ====== título ====== */
.title{
  font-family:'Segoe UI',sans-serif;
  font-size:2rem;
  font-weight:700;
  color:#ffffff;
  letter-spacing:.5px;
  
}



</style>
