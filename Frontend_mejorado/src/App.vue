<script setup>
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'

onMounted(() => {
  const baseURL = import.meta.env.DEV ? '/api' : ''
  
  fetch(`${baseURL}/ping/`)
    .then(res => res.json())
    .then(data => console.log('Respuesta del backend:', data))
    .catch(err => console.error('Error al hacer ping:', err))
})
</script>

<template>
  <div>
    <RouterView />
  </div>
</template>

<style>
</style>
