<template>
  <div class="page-container proveedores-view">
    <header class="top-bar">
      <img src="@/assets/logo_bof_blanco.png" alt="Logo del cliente" class="logo" @click="goHome" />
      <h1 class="title">PROVEEDORES</h1>
      <button class="avatar-btn">
        <img src="@/assets/profileImg.png" class="avatar-img" />
      </button>
    </header>

    <div class="body-wrapper">
      <section class="module">
        <input v-model="searchQuery" class="search" placeholder="Buscar proveedores…" />
        <table>
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
      <td>
        <button class="btn-action edit" @click="open('proveedor', prov)">✏️</button>
        <button class="btn-action delete" @click="eliminarProveedor(prov.id)">🗑️</button>
      </td>
    </tr>
    <tr v-if="filteredProveedores.length === 0">
      <td colspan="5" style="text-align: center;">No se encontraron proveedores</td>
    </tr>
  </tbody>
</table>

      </section>

      <section class="module cards-module">
        <div class="cards-container">
          <section class="big-card">
            <h2>ACTUALIZACIÓN</h2>
            <ul>
              <li @click="open('proveedor')">Agregar proveedor</li>
            </ul>
          </section>
        </div>
      </section>
    </div>

    <!-- MODAL: Nuevo proveedor -->
    <div v-if="modal.visible && modal.type === 'proveedor'" class="modal-overlay" @click.self="close">
      <div class="modal-window">
        <h3>Nuevo Proveedor</h3>
        <form class="modal-form grid-two" @submit.prevent="saveProveedor">
          <label>Nombre<input v-model="proveedorForm.nombre" required /></label>
          <label>Correo<input v-model="proveedorForm.correo" type="email" /></label>
          <label>Teléfono<input v-model="proveedorForm.telefono" /></label>
          <label>Dirección<input v-model="proveedorForm.direccion" /></label>

          <button class="save-big" type="submit">Guardar</button>
          <button class="cancel-btn" type="button" @click="close">Cancelar</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
function goHome() { router.push({ name: 'home' }) }

const API = '/api'

const modal = reactive({ visible: false, type: '' })
const currentProveedor = ref(null)

const proveedores = ref([])
const searchQuery = ref('')
const proveedorForm = reactive({ nombre: '', correo: '', telefono: '', direccion: ''})

const filteredProveedores = computed(() =>
  proveedores.value.filter(p =>
    p.nombre.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
)

function open(type, prov = null) {
  modal.type = type
  modal.visible = true
  if (type === 'proveedor') {
    if (prov) {
      // Editar: llena el formulario
      Object.assign(proveedorForm, prov)
      currentProveedor.value = prov
    } else {
      // Agregar: limpia el formulario
      Object.assign(proveedorForm, { nombre: '', correo: '', telefono: '', direccion: '' })
      currentProveedor.value = null
    }
  }
}

function close() {
  modal.visible = false
}

async function fetchProveedores() {
  try {
    const params = searchQuery.value ? { search: searchQuery.value } : {}
    proveedores.value = (await axios.get(`${API}/proveedores/`, { params })).data
  } catch (e) {
    console.error('Error cargando proveedores', e)
  }
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
  const proveedorData = { ...proveedorForm }

  try {
    if (currentProveedor.value) {
      // EDITAR
      await axios.put(`${API}/proveedores/${currentProveedor.value.id}/`, proveedorData)
    } else {
      // NUEVO
      await axios.post(`${API}/proveedores/`, proveedorData)
    }
    close()
    Object.assign(proveedorForm, { nombre: '', correo: '', telefono: '', direccion: '' })
    await fetchProveedores()
  } catch (e) {
    console.error('🔴 Error guardando proveedor:', e.response?.data || e)
    alert(e.response?.data?.nombre || 'No se pudo guardar proveedor')
  }
}

onMounted(() => {
  fetchProveedores()
})
</script>

<style scoped>
.btn-action {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  margin-right: 0.3rem;
  padding: 0.3rem;
  border-radius: 4px;
}

.btn-action.edit:hover {
  background-color: #2563eb;
  color: white;
}

.btn-action.delete:hover {
  background-color: #dc2626;
  color: white;
}


.body-wrapper {
  padding: 1rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.module {
  background: #0d1130;
  border: 2px solid #1e2236;
  border-radius: 16px;
  padding: 1.5rem;
}

.cards-module {
  display: flex;
  justify-content: center;
}

.cards-container {
  display: flex;
  flex-wrap: wrap;
  gap: 3rem;
  justify-content: center;
}

.big-card {
  width: 340px;
  min-height: 300px;
  background: #101222;
  border: 2px solid #1e2236;
  border-radius: 18px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.big-card h2 {
  margin: 0;
  font-size: 1.1rem;
  border-bottom: 1px solid #2c3148;
  padding-bottom: 0.5rem;
}

.big-card ul {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.big-card li {
  cursor: pointer;
  padding: 0.4rem 0.2rem;
  border-radius: 6px;
}

.big-card li:hover {
  background: #1e2236;
}

.search {
  max-width: 300px;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  border: none;
  background: white;
  color: black;
  margin-bottom: 1rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.8rem;
}

th, td {
  padding: 0.4rem 0.6rem;
  border-bottom: 1px solid #2c3148;
}

thead {
  background: #1e2236;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.modal-window {
  background: #1e293b;
  padding: 2rem;
  border-radius: 14px;
  min-width: 600px;
  max-width: 90%;
  max-height: 90vh;
  overflow: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.grid-two {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 0.8rem;
}

.modal-form label {
  display: flex;
  flex-direction: column;
  font-size: 0.9rem;
  gap: 0.25rem;
}

.modal-form input,
.modal-form select {
  padding: 0.45rem 0.6rem;
  border: none;
  border-radius: 6px;
  background: #111827;
  color: white;
}

.save-big {
  grid-column: 1 / -1;
  padding: 0.6rem 1rem;
  border: none;
  border-radius: 8px;
  background: #2563eb;
  font-weight: 600;
  cursor: pointer;
  color: white;
}

.cancel-btn {
  align-self: center;
  padding: 0.4rem 1.4rem;
  border: none;
  border-radius: 8px;
  background: #9ca3af;
  color: #1e2236;
  font-weight: 600;
  cursor: pointer;
}

.cancel-btn:hover {
  background: #d1d5db;
}
</style>
