import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAuthStore } from './auth'

export const useCatalogsStore = defineStore('catalogs', () => {
  const authStore = useAuthStore()

  // State
  const telas = ref([])
  const materiales = ref([])
  const loading = ref(false)
  const lastFetch = ref({
    telas: null,
    materiales: null
  })

  // Cache expiration time (5 minutos)
  const CACHE_TIME = 5 * 60 * 1000

  // Getters
  const telasOptions = computed(() => 
    telas.value.map(t => ({
      id: t.id,
      label: t.nombre,
      ...t
    }))
  )

  const materialesOptions = computed(() => 
    materiales.value.map(m => ({
      id: m.id,
      label: m.nombre,
      ...m
    }))
  )

  // Helper: Verificar si el cache es válido
  function isCacheValid(catalogType) {
    const lastTime = lastFetch.value[catalogType]
    if (!lastTime) return false
    return (Date.now() - lastTime) < CACHE_TIME
  }

  // Actions: Cargar telas
  async function fetchTelas(forceRefresh = false) {
    if (!forceRefresh && isCacheValid('telas') && telas.value.length > 0) {
      return telas.value
    }

    loading.value = true
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/telas/`, {
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error('Error al cargar telas')
      }

      const data = await response.json()
      telas.value = data
      lastFetch.value.telas = Date.now()
      return data
    } catch (error) {
      console.error('Error cargando telas:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // Actions: Cargar materiales
  async function fetchMateriales(forceRefresh = false) {
    if (!forceRefresh && isCacheValid('materiales') && materiales.value.length > 0) {
      return materiales.value
    }

    loading.value = true
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/materiales/`, {
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error('Error al cargar materiales')
      }

      const data = await response.json()
      materiales.value = data
      lastFetch.value.materiales = Date.now()
      return data
    } catch (error) {
      console.error('Error cargando materiales:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // Actions: Cargar ambos catálogos
  async function fetchAll(forceRefresh = false) {
    await Promise.all([
      fetchTelas(forceRefresh),
      fetchMateriales(forceRefresh)
    ])
  }

  // Actions: Buscar tela por ID
  function getTelaById(id) {
    return telas.value.find(t => t.id === id)
  }

  // Actions: Buscar material por ID
  function getMaterialById(id) {
    return materiales.value.find(m => m.id === id)
  }

  // Actions: Limpiar cache
  function clearCache() {
    telas.value = []
    materiales.value = []
    lastFetch.value = {
      telas: null,
      materiales: null
    }
  }

  // Actions: Agregar/actualizar item en cache
  function updateTelaInCache(tela) {
    const index = telas.value.findIndex(t => t.id === tela.id)
    if (index !== -1) {
      telas.value[index] = tela
    } else {
      telas.value.push(tela)
    }
  }

  function updateMaterialInCache(material) {
    const index = materiales.value.findIndex(m => m.id === material.id)
    if (index !== -1) {
      materiales.value[index] = material
    } else {
      materiales.value.push(material)
    }
  }

  // Actions: Eliminar item del cache
  function removeTelaFromCache(id) {
    telas.value = telas.value.filter(t => t.id !== id)
  }

  function removeMaterialFromCache(id) {
    materiales.value = materiales.value.filter(m => m.id !== id)
  }

  return {
    // State
    telas,
    materiales,
    loading,
    // Getters
    telasOptions,
    materialesOptions,
    // Actions
    fetchTelas,
    fetchMateriales,
    fetchAll,
    getTelaById,
    getMaterialById,
    clearCache,
    updateTelaInCache,
    updateMaterialInCache,
    removeTelaFromCache,
    removeMaterialFromCache
  }
})