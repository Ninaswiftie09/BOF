<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  const baseURL = import.meta.env.DEV ? '/api' : ''
  
  fetch(`${baseURL}/ping/`)
    .then(res => res.json())
    .then(data => console.log('Respuesta del backend:', data))
    .catch(err => console.error('Error al hacer ping:', err))
})
</script>

<template>
  <h1>Frontend conectado al Backend 🎉</h1>
</template>

