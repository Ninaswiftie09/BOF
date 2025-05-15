<script setup>
import { reactive, ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

// Método para redirigir al home
function goHome() {
  router.push({ name: 'home' })
}

const API = 'http://localhost:8000/api'

// Estado de modales
const modal = reactive({ visible: false, type: '' })
// Proveedor seleccionado para historial
const currentProveedor = ref(null)

// Datos traídos del backend
const proveedores = ref([])
const compras = ref([])

// Barras de búsqueda
const searchQuery = ref('')
const searchReportQuery = ref('')

// Formularios reactivos
const proveedorForm = reactive({
  nombre: '',
  correo: '',
  telefono: '',
  direccion: ''
})
const compraForm = reactive({
  proveedor: '',
  descripcion: '',
  monto: ''
})

// Computed para filtrar tablas
const filteredProveedores = computed(() =>
  proveedores.value.filter(p =>
    p.nombre.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
)
const filteredCompras = computed(() =>
  compras.value.filter(c =>
    String(c.proveedor).includes(searchReportQuery.value)
  )
)

// Mostrar/ocultar modales y capturar proveedor para historial
function open(type, prov = null) {
  modal.type = type
  modal.visible = true
  if (type === 'historial' && prov) {
    currentProveedor.value = prov
  }
}
function close() {
  modal.visible = false
}

// Peticiones al API
async function fetchProveedores() {
  try {
    const params = searchQuery.value ? { search: searchQuery.value } : {}
    proveedores.value = (await axios.get(`${API}/proveedores/`, { params })).data
  } catch (e) {
    console.error('Error cargando proveedores', e)
  }
}
async function fetchCompras() {
  try {
    compras.value = (await axios.get(`${API}/compras/`)).data
  } catch (e) {
    console.error('Error cargando compras', e)
  }
}

// Guardar nuevo proveedor
async function saveProveedor() {
  if (!proveedorForm.nombre) return alert('El nombre es obligatorio')
  try {
    await axios.post(`${API}/proveedores/`, proveedorForm)
    close()
    Object.keys(proveedorForm).forEach(k => (proveedorForm[k] = ''))
    await fetchProveedores()
  } catch (e) {
    console.error('Error guardando proveedor', e)
    alert(e.response?.data?.nombre || 'No se pudo crear proveedor')
  }
}

// Guardar nueva compra
async function saveCompra() {
  if (!compraForm.proveedor || !compraForm.descripcion || !compraForm.monto)
    return alert('Todos los campos de compra son obligatorios')
  try {
    await axios.post(`${API}/compras/`, compraForm)
    close()
    Object.keys(compraForm).forEach(k => (compraForm[k] = ''))
    await Promise.all([fetchProveedores(), fetchCompras()])
  } catch (e) {
    console.error('Error guardando compra', e)
    alert('No se pudo crear compra')
  }
}

// Al montar, cargamos datos
onMounted(() => {
  fetchProveedores()
  fetchCompras()
})
</script>





<template>
  <div class="crm-home">
    <header class="top-bar">
      <!-- Logo con redirección al Home -->
      <img
        src="@/assets/logo_bof_blanco.png"
        alt="Logo del cliente"
        class="logo"
        @click="goHome"
      />
      <h1>PROVEEDORES</h1>
      <button class="avatar-btn"></button>
    </header>

    <div class="section-container">
      <!-- Sección de Actualización de Proveedores -->
      <div class="update-section">
        <h2>ACTUALIZACIÓN</h2>
        <div class="search-wrapper">
          <input
            v-model="searchQuery"
            class="search"
            placeholder="Buscar proveedores..."
          />
        </div>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Correo</th>
                <th>Teléfono</th>
                <th>Dirección</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="prov in filteredProveedores" :key="prov.id">
                <td>{{ prov.id }}</td>
                <td>{{ prov.nombre }}</td>
                <td>{{ prov.correo }}</td>
                <td>{{ prov.telefono }}</td>
                <td>{{ prov.direccion }}</td>
                <td>
                  <button @click="open('historial', prov)">Ver Historial</button>
                </td>
              </tr>
              <tr v-if="filteredProveedores.length === 0">
                <td colspan="6" class="text-center py-4">No hay proveedores.</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="new-order-wrapper">
          <button class="new-order-btn" @click="open('proveedor')">
            AGREGAR PROVEEDOR
          </button>
        </div>
      </div>

      <!-- Sección de Reportes de Compras -->
      <div class="report-section">
        <h2>REPORTES</h2>
        <div class="search-wrapper">
          <input
            v-model="searchReportQuery"
            class="search"
            placeholder="Buscar historial de compras..."
          />
        </div>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Proveedor</th>
                <th>Fecha</th>
                <th>Monto</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="comp in filteredCompras" :key="comp.id">
                <td>{{ comp.id }}</td>
                <td>{{ comp.proveedor }}</td>
                <td>{{ comp.fecha }}</td>
                <td>{{ comp.monto }}</td>
              </tr>
              <tr v-if="filteredCompras.length === 0">
                <td colspan="4" class="text-center py-4">No hay compras.</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="new-order-wrapper">
          <button class="new-order-btn" @click="open('compra')">
            NUEVA COMPRA
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Nuevo Proveedor -->
    <div
      v-if="modal.visible && modal.type === 'proveedor'"
      class="modal-overlay"
      @click.self="close"
    >
      <div class="modal-window">
        <h3>Nuevo Proveedor</h3>
        <form class="modal-form grid-two" @submit.prevent="saveProveedor">
          <label>Nombre
            <input v-model="proveedorForm.nombre" required />
          </label>
          <label>Correo
            <input v-model="proveedorForm.correo" type="email" />
          </label>
          <label>Teléfono
            <input v-model="proveedorForm.telefono" />
          </label>
          <label>Dirección
            <input v-model="proveedorForm.direccion" />
          </label>
          <button class="save-big" type="submit">Guardar</button>
          <button class="cancel-btn" type="button" @click="close">
            Cancelar
          </button>
        </form>
      </div>
    </div>

    <!-- Modal Nueva Compra -->
    <div
      v-if="modal.visible && modal.type === 'compra'"
      class="modal-overlay"
      @click.self="close"
    >
      <div class="modal-window">
        <h3>Nueva Compra</h3>
        <form class="modal-form grid-two" @submit.prevent="saveCompra">
          <label>Proveedor
            <select v-model="compraForm.proveedor" required>
              <option disabled value="">Selecciona un proveedor</option>
              <option v-for="p in proveedores" :key="p.id" :value="p.id">
                {{ p.nombre }}
              </option>
            </select>
          </label>
          <label>Descripción
            <input v-model="compraForm.descripcion" required />
          </label>
          <label>Monto
            <input
              type="number"
              step="0.01"
              v-model="compraForm.monto"
              required
            />
          </label>
          <button class="save-big" type="submit">Guardar</button>
          <button class="cancel-btn" type="button" @click="close">
            Cancelar
          </button>
        </form>
      </div>
    </div>

    <!-- Modal Historial de Compras -->
    <div
      v-if="modal.visible && modal.type === 'historial'"
      class="modal-overlay"
      @click.self="close"
    >
      <div class="modal-window">
        <h3>Historial de Compras de {{ currentProveedor.nombre }}</h3>
        <div class="table-wrapper" style="max-height:60vh; overflow:auto;">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Fecha</th>
                <th>Descripción</th>
                <th>Monto</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="c in compras.filter(x => x.proveedor === currentProveedor.id)"
                :key="c.id"
              >
                <td>{{ c.id }}</td>
                <td>{{ c.fecha }}</td>
                <td>{{ c.descripcion }}</td>
                <td>{{ c.monto }}</td>
              </tr>
              <tr
                v-if="!compras.some(x => x.proveedor === currentProveedor.id)"
              >
                <td colspan="4" class="text-center py-4">
                  Sin compras para este proveedor.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <button class="save-big" @click="close">Cerrar</button>
      </div>
    </div>
  </div>
</template>



<style scoped>
* { color: #fff }
.crm-home {
  min-height: 100vh;
  background: #0a0f2c;
  display: flex;
  flex-direction: column;
  font-family: 'Segoe UI', sans-serif;
}
.top-bar {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 0.75rem 2rem;
  background: #1e293b;
  justify-content: space-between;
}
h1 {
  font-family: 'Segoe UI', sans-serif;
  color: #ffffff;
  font-size: 2rem;
  flex-grow: 1;
  text-align: center;
}
.logo {
  width: 150px;
  height: auto;
  cursor: pointer;
}
.search-wrapper {
  padding: 1rem 2rem;
}
.search {
  padding: 0.6rem 1rem;
  border-radius: 6px;
  border: none;
  background: #fff;
  color: #000;
  width: 100%;
}
.new-order-wrapper {
  display: flex;
  justify-content: flex-end;
  padding: 1.5rem 2rem;
}
.new-order-btn {
  background: #1d4ed8;
  border: none;
  color: #fff;
  border-radius: 12px;
  padding: 0.7rem 1.6rem;
  font-weight: 600;
  cursor: pointer;
}
.section-container {
  display: flex;
  justify-content: space-between;
  padding: 2rem;
}
.update-section,
.report-section {
  width: 48%;
  padding: 2rem;
  background-color: #101222;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}
.table-wrapper {
  max-height: 60vh;
  overflow: auto;
  padding: 1rem;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th,
td {
  padding: 0.4rem 0.6rem;
  border-bottom: 1px solid #2c3148;
}
thead {
  position: sticky;
  top: 0;
  background: #1e2236;
}
button {
  padding: 0.5rem 1rem;
  margin-top: 1rem;
}
/* Modal Styling */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}
.modal-window {
  background: #1e2236;
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
.modal-window h3 {
  margin: 0;
  font-size: 1.2rem;
  text-align: center;
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
  color: #fff;
}
.save-big {
  grid-column: 1 / -1;
  padding: 0.6rem 1rem;
  border: none;
  border-radius: 8px;
  background: #2563eb;
  font-weight: 600;
  cursor: pointer;
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
