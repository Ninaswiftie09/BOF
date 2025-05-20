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

    <!-- Acciones a la derecha -->
    <div class="ml-auto flex items-center">
      <button class = "avatar-btn">
        <img
          :src="profileImg"
          class="avatar-img"
        />
      </button>
    </div>

  </header>
</template>

<script setup>
defineProps({
  title: { type: String, required: true }
})

import profileImage from '@/assets/profileImg.png'
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
  height:80px;
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

/* ====== Foto de Perfil ====== */
.avatar-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: var(--color-novenary);
  overflow: hidden;
  border: none;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}


.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 5rem;
}


</style>
