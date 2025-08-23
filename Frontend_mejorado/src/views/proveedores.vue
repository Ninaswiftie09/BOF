<template>
  <div class="page">
    <NavBar title="PROVEEDORES" />

    <div class="container">
      <section class="module">
        <input
          v-model="searchQuery"
          class="input input--white"
          placeholder="Buscar proveedores…"
        />

        <div class="table-wrapper">
          <table class="table">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Correo</th>
                <th>Teléfono</th>
                <th>Dirección</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="prov in filteredProveedores" :key="prov.id">
                <td>{{ prov.nombre }}</td>
                <td>{{ prov.correo }}</td>
                <td>{{ prov.telefono }}</td>
                <td>{{ prov.direccion }}</td>
                <td class="table-actions">
                  <button class="icon-btn" @click="open('proveedor', prov)">✎</button>
                  <button class="icon-btn danger" @click="eliminarProveedor(prov.id)">✕</button>
                </td>
              </tr>
              <tr v-if="filteredProveedores.length === 0">
                <td colspan="5" style="text-align:center;">No se encontraron proveedores</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <div class="footer-actions">
        <button class="btn" @click="open('proveedor')">Agregar Proveedores</button>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="modal.visible && modal.type === 'proveedor'" class="modal-overlay" @click.self="close">
      <div class="modal-window">
        <h3>{{ currentProveedor ? 'Editar Proveedor' : 'Nuevo Proveedor' }}</h3>
        <form class="grid-two" @submit.prevent="saveProveedor">
          <label>Nombre<input v-model="proveedorForm.nombre" required /></label>
          <label>Correo<input v-model="proveedorForm.correo" type="email" /></label>
          <label>Teléfono<input v-model="proveedorForm.telefono" /></label>
          <label>Dirección<input v-model="proveedorForm.direccion" /></label>

          <div class="modal-actions">
            <button class="btn" type="submit">Guardar</button>
            <button class="btn secondary" type="button" @click="close">Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from 'vue'
import axios from 'axios'
import NavBar from '@/components/NavBar.vue'

const API = '/api'

const modal = reactive({ visible: false, type: '' })
const currentProveedor = ref(null)
const proveedores = ref([])
const searchQuery = ref('')

const proveedorForm = reactive({ nombre: '', correo: '', telefono: '', direccion: '' })

const filteredProveedores = computed(() =>
  proveedores.value.filter(p =>
    (p.nombre || '').toLowerCase().includes(searchQuery.value.toLowerCase())
  )
)

function open(type, prov = null) {
  modal.type = type
  modal.visible = true
  if (type === 'proveedor') {
    if (prov) {
      Object.assign(proveedorForm, prov)
      currentProveedor.value = prov
    } else {
      Object.assign(proveedorForm, { nombre: '', correo: '', telefono: '', direccion: '', nit: '' })
      currentProveedor.value = null
    }
  }
}
function close() { modal.visible = false }

async function fetchProveedores() {
  try {
    proveedores.value = (await axios.get(`${API}/proveedores/`)).data
  } catch (e) { console.error('Error cargando proveedores', e) }
}

async function eliminarProveedor(id) {
  if (!confirm('¿Estás segura de que quieres eliminar este proveedor?')) return
  try {
    await axios.delete(`${API}/proveedores/${id}/`)
    await fetchProveedores()
  } catch (e) {
    console.error('Error al eliminar proveedor:', e)
    alert('No se pudo eliminar el proveedor')
  }
}

async function saveProveedor() {
  if (!proveedorForm.nombre) return alert('El nombre es obligatorio')
  const data = { ...proveedorForm }
  try {
    if (currentProveedor.value) {
      await axios.put(`${API}/proveedores/${currentProveedor.value.id}/`, data)
    } else {
      await axios.post(`${API}/proveedores/`, data)
    }
    close()
    Object.assign(proveedorForm, { nombre: '', correo: '', telefono: '', direccion: '', nit: '' })
    await fetchProveedores()
  } catch (e) {
    console.error('🔴 Error guardando proveedor:', e.response?.data || e)
    alert(e.response?.data?.nombre || 'No se pudo guardar proveedor')
  }
}

onMounted(fetchProveedores)
</script>
