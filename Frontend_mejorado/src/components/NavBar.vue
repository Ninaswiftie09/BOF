<!-- src/components/NavBar.vue -->
<template>
  <header class="top-bar" role="banner">
    <!-- Logo (click a /home) -->
    <img
      src="@/assets/logo_bof_blanco.png"
      alt="Logo BOF"
      class="logo"
      @click="$router.push('/home')"
    />

    <!-- Título centrado absoluto -->
    <div class="title-wrap">
      <h1 class="title">{{ title }}</h1>
    </div>

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
const isHome = computed(() => route.name === 'home' || route.path === '/home')
const finalProfileImg = computed(() => props.profileImg || profileImage)
</script>

<style scoped>
/* Barra NO fija: sin position sticky/fixed */
.top-bar{
  position: relative;
  display:flex; align-items:center;
  gap:1rem;
  padding: .75rem 2rem;
  background: var(--color-primary);
  border-bottom: 1px solid rgba(255,255,255,.06);
  min-height: clamp(64px, 9vw, 100px); /* altura cómoda para logo grande */
}

/* Logo más grande y responsive */
.logo{
  height: clamp(56px, 8vw, 96px);
  width:auto; cursor:pointer;
}

/* Título centrado “real”  */
.title-wrap{
  position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
  pointer-events:none; /* deja clicables logo/acciones debajo si se solapa */
}
.title{
  margin:0;
  font-family:'Segoe UI',sans-serif;
  font-weight:800;
  letter-spacing:.3px;
  font-size: clamp(22px, 2.4vw, 34px);
  color: var(--color-novenary);
  text-align:center;
}

/* Acciones a la derecha */
.actions{ margin-left:auto; display:flex; align-items:center; gap:.75rem; }

/* Avatar/círculo (solo en Home por v-if) */
.avatar-btn{
  width:36px; height:36px; border-radius:50%;
  background: var(--color-novenary);
  overflow:hidden; border:none; padding:0;
  display:flex; align-items:center; justify-content:center; cursor:pointer;
}
.avatar-img{ width:100%; height:100%; object-fit:cover; }
</style>
