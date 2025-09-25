<template>
  <div class="page">
    <NavBar title="PROVEEDORES">
      <template #actions>
        <input
          v-model="searchQuery"
          class="input--white"
          placeholder="Buscar proveedores…"
        />
      </template>
    </NavBar>

    <div class="container">
      <section class="module">
        <Tablas
          :columns="columns"
          :rows="filteredProveedores"
          :center="true"
          :searchable="false"                    
          :actions="{ edit:true, delete:true }"
          @edit="(row) => open('proveedor', row)"
          @delete="(row) => eliminarProveedor(row.id)"
        />

        <div class="footer-actions" style="justify-content:flex-end; gap:.5rem">
          <button class="btn" @click="open('proveedor')">Agregar Proveedores</button>
        </div>
      </section>
    </div>

    <!-- Modal: nuevo/editar proveedor -->
    <div v-if="modal.visible && modal.type === 'proveedor'" class="modal-overlay" @click.self="close">
      <div class="modal-content modal--compact">
        <h3>{{ currentProveedor ? 'Editar Proveedor' : 'Nuevo Proveedor' }}</h3>

        <form class="form-vertical" @submit.prevent="saveProveedor">
          <div class="form-field">
            <label>Nombre</label>
            <input class="input--dark" v-model="proveedorForm.nombre" required />
          </div>

          <div class="form-field">
            <label>Correo</label>
            <input class="input--dark" v-model="proveedorForm.correo" type="email" />
          </div>

          <div class="form-field">
            <label>Teléfono</label>
            <input class="input--dark" v-model="proveedorForm.telefono" />
          </div>

          <div class="form-field">
            <label>Dirección</label>
            <input class="input--dark" v-model="proveedorForm.direccion" />
          </div>

          <div class="modal-actions">
            <button type="submit" class="btn">Guardar</button>
            <button type="button" class="btn btn--muted" @click="close">Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from 'vue'
import NavBar from '@/components/NavBar.vue'
import Tablas from '@/components/Reutilizacion/Tablas.vue'
import { apiFetch } from '@/utils/api'

/* UI / estado */
const modal = reactive({ visible: false, type: '' })
const currentProveedor = ref(null)
const proveedores = ref([])
const searchQuery = ref('')

/* Columnas que se muestran en la tabla */
const columns = [
  { key: 'nombre',    label: 'Nombre' },
  { key: 'correo',    label: 'Correo' },
  { key: 'telefono',  label: 'Teléfono' },
  { key: 'direccion', label: 'Dirección' },
]

/* Form */
const proveedorForm = reactive({ id: null, nombre: '', correo: '', telefono: '', direccion: '' })

/* Filtro (header) */
const filteredProveedores = computed(() => {
  const q = (searchQuery.value || '').trim().toLowerCase()
  if (!q) return proveedores.value
  return proveedores.value.filter(p =>
    ['nombre','correo','telefono','direccion'].some(k =>
      String(p?.[k] ?? '').toLowerCase().includes(q)
    )
  )
})

/* Abrir/Cerrar modal */
function open(type, prov = null) {
  modal.type = type
  modal.visible = true
  if (type === 'proveedor') {
    if (prov) {
      Object.assign(proveedorForm, {
        id: prov.id ?? null,
        nombre: prov.nombre ?? '',
        correo: prov.correo ?? '',
        telefono: prov.telefono ?? '',
        direccion: prov.direccion ?? ''
      })
      currentProveedor.value = { id: prov.id }
    } else {
      Object.assign(proveedorForm, { id: null, nombre: '', correo: '', telefono: '', direccion: '' })
      currentProveedor.value = null
    }
  }
}
function close() { modal.visible = false }

/* Fetch */
async function fetchProveedores() {
  try {
    proveedores.value = await apiFetch('/api/proveedores/')
  } catch (e) {
    console.error('Error cargando proveedores', e)
    proveedores.value = []
  }
}

/* Eliminar */
async function eliminarProveedor(id) {
  if (!confirm('¿Estás segura de que quieres eliminar este proveedor?')) return
  try {
    await apiFetch(`/api/proveedores/${id}/`, 'DELETE')
    await fetchProveedores()
  } catch (e) {
    console.error('Error al eliminar proveedor:', e)
    alert('No se pudo eliminar el proveedor')
  }
}

/* Guardar (crear/actualizar) */
async function saveProveedor() {
  if (!proveedorForm.nombre) return alert('El nombre es obligatorio')
  const data = {
    nombre: proveedorForm.nombre,
    correo: proveedorForm.correo,
    telefono: proveedorForm.telefono,
    direccion: proveedorForm.direccion
  }
  try {
    if (currentProveedor.value?.id) {
      await apiFetch(`/api/proveedores/${currentProveedor.value.id}/`, 'PUT', data)
    } else {
      await apiFetch('/api/proveedores/', 'POST', data)
    }
    close()
    Object.assign(proveedorForm, { id: null, nombre: '', correo: '', telefono: '', direccion: '' })
    await fetchProveedores()
  } catch (e) {
    console.error('🔴 Error guardando proveedor:', e)
    alert('No se pudo guardar el proveedor')
  }
}

onMounted(fetchProveedores)
</script>

<style scoped>
.page{ min-height:100vh; background:var(--color-octonary); color:#fff; }
.container{ max-width:1100px; margin:0 auto; padding:20px; }
.module{ background:#0d1130; border:2px solid #1e2236; border-radius:16px; padding:16px; }
</style>
