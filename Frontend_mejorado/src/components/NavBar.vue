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
/* Este bloque scoped se queda, pero con los valores referenciando a NuevoStyles.css */

.top-bar {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--spacing-md); /* Usando variable global */
  padding: var(--spacing-sm) var(--spacing-xl); /* Usando variables globales */
  background: var(--navbar-background); /* Usando variable global */
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  min-height: clamp(64px, 9vw, 100px);
}

.logo {
  height: clamp(56px, 8vw, 96px);
  width: auto;
  cursor: pointer;
}

.title-wrap {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}
.title {
  margin: 0;
  /* Usando la fuente global para títulos (Archivo Black) o si prefieres Kollektif para títulos de navbar, tendrías que sobrescribir explícitamente aquí o hacer una nueva variable. Por defecto, h1 usa Archivo Black */
  font-family: 'Archivo Black', sans-serif; /* Mantenido aquí si quieres que el título de la navbar sea distinto del h1 global */
  font-weight: var(--font-weight-bold); /* Usando variable global */
  letter-spacing: 0.3px;
  font-size: clamp(22px, 2.4vw, 34px);
  color: var(--color-text-light-primary); /* Usando variable global */
  text-align: center;
}

.actions {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: var(--spacing-sm); /* Usando variable global */
}

.avatar-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--color-text-light-primary); /* Si el fondo del avatar es blanco como antes */
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
</style>