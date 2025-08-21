<!-- src/components/NavBar.vue -->
<template>
  <header class="top-bar nav-gap">
    <!-- Logo clicable a /home -->
    <img
      src="@/assets/logo_bof_blanco.png"
      alt="Logo BOF"
      class="logo"
      @click="$router.push('/home')"
    />

    <!-- Título -->
    <h1 class="title">{{ title }}</h1>

    <!-- Acciones a la derecha: SOLO en Home -->
    <div class="actions" v-if="isHome">
      <button class="avatar-btn" aria-label="Perfil">
        <img :src="finalProfileImg" alt="Perfil" class="avatar-img" />
      </button>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import profileImage from '@/assets/profileImg.png'

const props = defineProps({
  title: { type: String, required: true },
  profileImg: { type: String, default: '' }
})

const route = useRoute()
/* */
const isHome = computed(() => route.name === 'home' || route.path === '/home')
const finalProfileImg = computed(() => props.profileImg || profileImage)
</script>

<style scoped>
.top-bar{
  display:flex; align-items:center; gap:1.5rem;
  padding:.75rem 2rem; background:#1e293b;
}

/* Logo */
.logo{ height:80px; width:auto; cursor:pointer; }

/* Título */
.title{
  font-family:'Segoe UI',sans-serif;
  font-size:2rem; font-weight:700; color:#ffffff; letter-spacing:.5px;
  margin-right:auto;
}


.actions{ margin-left:auto; display:flex; align-items:center; gap:.75rem; }

/* Avatar/círculo blanco (solo en Home por v-if) */
.avatar-btn{
  width:36px; height:36px; border-radius:50%;
  background: var(--color-novenary);
  overflow:hidden; border:none; padding:0;
  display:flex; align-items:center; justify-content:center; cursor:pointer;
}
.avatar-img{ width:100%; height:100%; object-fit:cover; }
</style>
