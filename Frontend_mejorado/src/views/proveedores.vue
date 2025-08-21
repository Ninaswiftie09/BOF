<template>
  <div class="crm-home">
    <!-- Header unificado -->
    <NavBar title="PROVEEDORES" />

    <div class="body-wrapper">
      <section class="module">
        <input v-model="searchQuery" class="search input" placeholder="Buscar proveedores…" />

        <div class="table-wrapper">
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
                  <button class="edit-btn" @click="open('proveedor', prov)">✎</button>
                  <button class="remove-btn" @click="eliminarProveedor(prov.id)">✕</button>
                </td>
              </tr>
              <tr v-if="filteredProveedores.length === 0">
                <td colspan="5" style="text-align:center;">No se encontraron proveedores</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <div class="add-button-wrapper">
        <button class="add-button btn" @click="open('proveedor')">Agregar Proveedores</button>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="modal.visible && modal.type === 'proveedor'" class="modal-overlay" @click.self="close">
      <div class="modal-window">
        <h3>{{ currentProveedor ? 'Editar Proveedor' : 'Nuevo Proveedor' }}</h3>
        <form class="modal-form grid-two" @submit.prevent="saveProveedor">
          <label>Nombre<input v-model="proveedorForm.nombre" required /></label>
          <label>Correo<input v-model="proveedorForm.correo" type="email" /></label>
          <label>Teléfono<input v-model="proveedorForm.telefono" /></label>
          <label>Dirección<input v-model="proveedorForm.direccion" /></label>

          <button class="save-big btn" type="submit">Guardar</button>
          <button class="cancel-btn btn secondary" type="button" @click="close">Cancelar</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import NavBar from '@/components/NavBar.vue'

const router = useRouter()
const goHome = () => router.push({ name: 'home' })

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
      await axios.put(`${API}/proveedores/${currentProveedor.value.id}/`, proveedorData)
    } else {
      await axios.post(`${API}/proveedores/`, proveedorData)
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

<style scoped>
/*  paleta global */
.crm-home{
  background: var(--color-octonary);
  min-height: 100vh;
  display: flex; flex-direction: column;
  color: var(--color-novenary);
  font-family: 'Kollektif', sans-serif;
}

.body-wrapper { padding: 1rem 2rem; display: flex; flex-direction: column; gap: 2rem; }

.module{
  background: #0d1130;
  border: 2px solid #1e2236;
  border-radius: 16px;
  padding: 1.5rem;
  display: flex; flex-direction: column; gap: 1rem;
}


.search{ max-width: 300px; }

/* Tabla */
.table-wrapper { max-height: 60vh; overflow: auto; margin-bottom: 1rem; }
table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 4px;
  min-width: 800px;
}
th {
  background: transparent;
  padding: 12px 16px;
  color: var(--color-novenary);
  font-size: .9rem;
  text-align: left;
  border-bottom: 2px solid var(--color-senary);
}
td {
  padding: 16px;
  background: var(--color-primary);
  color: var(--color-novenary);
  text-align: left;
  vertical-align: middle;
  border: none;
}

/* Acciones */
.edit-btn, .remove-btn {
  background: transparent; border: none; cursor: pointer; font-size: 1.1rem;
}
.edit-btn { color: #60a5fa; }
.remove-btn { color: #e74c3c; }
.edit-btn:hover { color: #93c5fd; }
.remove-btn:hover { color: #f87171; }

/* Footer */
.add-button-wrapper { display: flex; justify-content: flex-end; padding: 0 1.5rem; }
.add-button { background: var(--color-senary); }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.6); display: flex; justify-content: center; align-items: center; z-index: 2000; }
.modal-window {
  background: var(--color-primary);
  padding: 2rem; border-radius: 14px;
  min-width: 600px; max-width: 90%; max-height: 90vh; overflow: auto;
  display: flex; flex-direction: column; gap: 1rem;
}
.modal-form { display: flex; flex-direction: column; gap: .8rem; }
.grid-two { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: .8rem; }
.modal-form label { display: flex; flex-direction: column; font-size: .9rem; gap: .25rem; }
.modal-form input, .modal-form select { /*  */ }
.save-big { grid-column: 1 / -1; }
.cancel-btn { background: var(--color-septenary); color: var(--color-primary); }
.cancel-btn:hover { filter: brightness(1.1); }
</style>
