<template>
  <div class="page-container">
    <NavBar title="PROVEEDORES">
    </NavBar>

    <div class="page-content">
      <section class="module">

        <div class="toolbar">
          <input
            v-model="searchQuery"
            class="input-dark"
            placeholder="Buscar proveedores…"
            style="max-width: 300px;"
          />
        </div>
        
        <div class="table-wrapper">
          <table class="table">
            <thead>
              <tr>
                <th v-for="col in columns" :key="col.key">{{ col.label }}</th>
                <th style="width:140px; text-align: right;">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="proveedor in filteredProveedores" :key="proveedor.id">
                <td v-for="col in columns" :key="col.key">
                  {{ proveedor[col.key] }}
                </td>
                <td class="actions" style="justify-content: flex-end;">
                  <button class="icon-btn edit" title="Editar" @click="open('proveedor', proveedor)">✎</button>
                  <button class="icon-btn delete" title="Eliminar" @click="eliminarProveedor(proveedor.id)">✕</button>
                </td>
              </tr>
              <tr v-if="filteredProveedores.length === 0">
                <td :colspan="columns.length + 1" class="muted-text" style="text-align:center; padding: 1.2rem 0;">
                  No hay proveedores para mostrar
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="footer-actions">
          <button class="btn btn-primary" @click="open('proveedor')">Agregar Proveedor</button>
        </div>
      </section>
    </div>

    <!-- Modal: nuevo/editar proveedor -->
    <div v-if="modal.visible && modal.type === 'proveedor'" class="modal-overlay" @click.self="close">
      <div class="modal-content-dark">
        <h3>{{ currentProveedor ? 'Editar Proveedor' : 'Nuevo Proveedor' }}</h3>

        <form @submit.prevent="saveProveedor">
          <div class="form-group">
            <label for="nombre" class="form-label">Nombre</label>
            <input id="nombre" class="form-input" v-model="proveedorForm.nombre" required />
          </div>

          <div class="form-group">
            <label for="correo" class="form-label">Correo</label>
            <input id="correo" class="form-input" v-model="proveedorForm.correo" type="email" />
          </div>

          <div class="form-group">
            <label for="telefono" class="form-label">Teléfono</label>
            <input id="telefono" class="form-input" v-model="proveedorForm.telefono" />
          </div>

          <div class="form-group">
            <label for="direccion" class="form-label">Dirección</label>
            <input id="direccion" class="form-input" v-model="proveedorForm.direccion" />
          </div>

          <div class="modal-actions">
            <button type="button" class="btn btn-secondary" @click="close">Cancelar</button>
            <button type="submit" class="btn btn-primary">Guardar</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from 'vue'
import NavBar from '@/components/NavBar.vue'
import { apiFetch } from '@/utils/api'

/* UI / estado */
const modal = reactive({ visible: false, type: '' })
const currentProveedor = ref(null)
const proveedores = ref([])
const searchQuery = ref('')

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
.page-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.footer-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: var(--spacing-lg);
}

.form-group + .form-group {
  margin-top: var(--spacing-md);
}

.toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: var(--spacing-lg);
}

</style>