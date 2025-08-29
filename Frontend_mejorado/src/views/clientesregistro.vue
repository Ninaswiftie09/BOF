<script setup>
import { reactive, ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import { apiFetch } from '@/utils/api'
import { bus } from '@/event-bus' // <-- para emitir el KPI al Home

const router = useRouter()
const go = path => router.push(path)

const search = ref('')
const modal = reactive({ visible: false, type: '', searchTerm: '', searchResults: [] })
const open = t => {
  modal.type = t
  modal.visible = true
  if (t === 'buscar') {
    modal.searchTerm = ''
    modal.searchResults = []
  }
}
const close = () => { modal.visible = false; resetForm() }

/* FORMULARIO CLIENTES */
const clienteForm = reactive({
  id: null,
  codigo_cliente: '',
  estado: true,
  nombre: '',
  contacto: '', 
  nit: '',
  direccion: '',
  direccion_entrega: '',
  telefono: '',
  email: '',
  cartera: 0,
})
const clientes = ref([])

/* ===== Helpers para fecha + KPI ===== */
function pickDateField(sample) {
  if (!sample) return null
  const preferred = [
    'created_at','fecha_registro','creado','fecha_creacion',
    'fecha','fecha_alta','f_creacion','created','createdAt'
  ]
  for (const k of preferred) {
    if (sample[k] && !isNaN(Date.parse(sample[k]))) return k
  }
  // Heurística por si el backend se llama “Juan”
  for (const [k,v] of Object.entries(sample)) {
    if (typeof v === 'string' && !isNaN(Date.parse(v)) && /fecha|date|crea|alta|reg/i.test(k)) return k
  }
  return null
}

function emitirKpiClientesNuevos() {
  const list = clientes.value || []
  const field = pickDateField(list[0])

  // Rango del mes actual (local)
  const start = new Date(); start.setDate(1); start.setHours(0,0,0,0)
  const end = new Date(start); end.setMonth(start.getMonth()+1)

  let nuevosMes
  if (!field) {
    nuevosMes = list.length // fallback: total
    console.warn('[KPI] No se encontró campo de fecha; usando total de clientes:', nuevosMes)
  } else {
    nuevosMes = list.filter(c => {
      const t = Date.parse(c[field])
      return !isNaN(t) && t >= +start && t < +end
    }).length
    console.debug('[KPI] Campo de fecha usado:', field, '-> nuevosMes:', nuevosMes)
  }

  bus.emit('clientes-actualizados', { nuevosMes })
}

/* ===== FETCH ===== */
async function fetchClientes () {
  try {
    const data = await apiFetch('/api/clientes/')
    // Soporta lista directa o DRF paginado
    clientes.value = Array.isArray(data) ? data : (Array.isArray(data?.results) ? data.results : [])
    emitirKpiClientesNuevos() // emite KPI tras cargar
  } catch (e) {
    console.error('Error al obtener clientes:', e)
  }
}

onMounted(fetchClientes)

function resetForm () {
  Object.assign(clienteForm, {
    id: null,
    codigo_cliente: '',
    estado: true,
    nombre: '',
    contacto: '',
    nit: '',
    direccion: '',
    direccion_entrega: '',
    telefono: '',
    email: '',
    cartera: 0
  })
}

/* ===== GUARDAR ===== */
async function saveCliente () {
  if (!clienteForm.nombre) return alert('El nombre es requerido')

  const isUpdating = !!clienteForm.id
  const method = isUpdating ? 'PUT' : 'POST'
  const url = isUpdating ? `/api/clientes/${clienteForm.id}/` : `/api/clientes/`

  const payload = {
    nombre: clienteForm.nombre,
    contacto: clienteForm.contacto,
    nit: clienteForm.nit,
    direccion: clienteForm.direccion,
    direccion_entrega: clienteForm.direccion_entrega,
    telefono: clienteForm.telefono,
    email: clienteForm.email,
    cartera: clienteForm.cartera,
    estado: clienteForm.estado
  }

  try {
    await apiFetch(url, method, payload)
    await fetchClientes()
    emitirKpiClientesNuevos()
    close()
  } catch (err) {
    console.error('Error al guardar cliente:', err)
    alert('Hubo un error al guardar el cliente.')
  }
}

/* ===== EDITAR ===== */
function editCliente (cliente) {
  Object.assign(clienteForm, { ...cliente, id: cliente.id })
  modal.type = 'clientes'
  modal.visible = true
}

/* ===== ELIMINAR ===== */
async function deleteCliente (id) {
  if (!confirm(`¿Seguro que deseas eliminar al cliente con ID ${id}?`)) return
  try {
    await apiFetch(`/api/clientes/${id}/`, 'DELETE')
    await fetchClientes()
    emitirKpiClientesNuevos()
    close()
  } catch (err) {
    console.error('Error al eliminar cliente:', err)
    alert('Error al eliminar el cliente')
  }
}

/* ===== FILTROS ===== */
const filteredClientes = computed(() =>
  clientes.value.filter(c =>
    [c.codigo_cliente, c.nombre, c.contacto]
      .some(v => v?.toString().toLowerCase().includes(search.value.toLowerCase()))
  )
)

function searchClientsInModal () {
  if (!modal.searchTerm) { modal.searchResults = []; return }
  modal.searchResults = clientes.value.filter(c =>
    (c.nombre || '').toLowerCase().includes(modal.searchTerm.toLowerCase())
  )
}
</script>

<template>
  <div class="crm-home">
    <NavBar title="CLIENTES">
      <template #actions>
        <input v-model="search" class="nav-search" placeholder="Buscar clientes…" />
      </template>
    </NavBar>

    <div class="body-wrapper">
      <section class="module">
        <div class="search-wrapper">
          <input v-model="search" class="search-clientes" placeholder="Buscar clientes…" />
        </div>

        <table>
          <thead>
            <tr>
              <th>Código</th>
              <th>Nombre</th>
              <th>Contacto</th>
              <th>Teléfono</th>
              <th>NIT</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in filteredClientes" :key="c.id">
              <td>{{ c.codigo_cliente }}</td>
              <td>{{ c.nombre }}</td>
              <td>{{ c.contacto }}</td>
              <td>{{ c.telefono }}</td>
              <td>{{ c.nit }}</td>
              <td>
                <button class="edit-btn" @click="editCliente(c)">✎</button>
                <button class="remove-btn" @click="deleteCliente(c.id)">✕</button>
              </td>
            </tr>
            <tr v-if="filteredClientes.length===0">
              <td colspan="6">No hay clientes registrados</td>
            </tr>
          </tbody>
        </table>
      </section>

      <div class="add-button-wrapper">
        <button class="add-button" @click="open('clientes')">Agregar Cliente</button>
      </div>
    </div>

    <!-- Modal Clientes -->
    <div v-if="modal.visible && modal.type==='clientes'" class="modal-overlay" @click.self="close">
      <div class="modal-window">
        <h3>{{ clienteForm.id ? 'Editar Cliente' : 'Nuevo Cliente' }}</h3>
        <form class="modal-form grid-two" @submit.prevent="saveCliente">
          <label>Nombre<input v-model="clienteForm.nombre" required/></label>
          <label>Contacto<input v-model="clienteForm.contacto"/></label>
          <label>NIT<input v-model="clienteForm.nit"/></label>
          <label>Dirección<input v-model="clienteForm.direccion"/></label>
          <label>Dirección Entrega<input v-model="clienteForm.direccion_entrega"/></label>
          <label>Teléfono<input v-model="clienteForm.telefono"/></label>
          <label>E-mail<input type="email" v-model="clienteForm.email"/></label>
          <div class="actions">
            <button type="submit" class="save-big">Guardar</button>
            <button type="button" class="cancel-btn" @click="close">Cancelar</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal búsqueda -->
    <div v-if="modal.visible && modal.type === 'buscar'" class="modal-overlay" @click.self="close">
      <div class="modal-window">
        <h3>Buscar Cliente para Modificar o Eliminar</h3>
        <input
          v-model="modal.searchTerm"
          @input="searchClientsInModal"
          class="search-in-modal"
          placeholder="Escribe un nombre para buscar..."
        />
        <div class="search-results-container">
          <table v-if="modal.searchResults.length > 0" class="results-table">
            <tbody>
              <tr v-for="cliente in modal.searchResults" :key="cliente.id">
                <td>{{ cliente.nombre }}</td>
                <td>
                  <button class="edit-btn" @click="editCliente(cliente)">✎</button>
                  <button class="remove-btn" @click="deleteCliente(cliente.id)">✕</button>
                </td>
              </tr>
            </tbody>
          </table>
          <p v-else-if="modal.searchTerm">No se encontraron clientes.</p>
          <p v-else>Comienza a escribir para ver los resultados.</p>
        </div>
        <div class="actions">
          <button type="button" class="cancel-btn" @click="close">Cerrar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* (tus estilos originales) */
.crm-home{
  min-height:100vh;
  background:#0a0f2c;
  display:flex; flex-direction:column;
  font-family:'Segoe UI',sans-serif; color:#fff;
}
.body-wrapper{
  padding: 2rem;
  display:flex; flex-direction:column; gap:2rem;
}
.nav-search{
  width: 280px; max-width: 40vw;
  padding: .5rem .75rem;
  border-radius: 10px;
  border: 1px solid #cbd5e1;
  background: #fff; color:#000;
  font-size: .9rem;
}
.nav-search:focus{ outline: none; box-shadow: 0 0 0 3px rgba(99,102,241,.25); border-color:#6366f1; }
.module{
  background:#0d1130;
  border:2px solid #1e2236;
  border-radius:16px;
  padding:1.5rem;
}
table{ width:100%; border-collapse:separate; border-spacing:0 4px; min-width:800px; }
th{
  background:transparent; padding:12px 16px; color:#fff;
  font-size:.9rem; text-align:left; border-bottom:2px solid #334155;
}
td{
  padding:16px; background:#1e293b; color:#fff; text-align:left;
  vertical-align:middle; border:none;
}
tr[v-if="filteredClientes.length===0"] td{
  background:transparent; text-align:center; padding:2rem; font-style:italic; color:#94a3b8;
}
.edit-btn,.remove-btn{ background:transparent; border:none; cursor:pointer; font-size:1.1rem; }
.edit-btn{ color:#60a5fa; } .remove-btn{ color:#e74c3c; }
.edit-btn:hover{ color:#93c5fd; } .remove-btn:hover{ color:#f87171; }
.modal-overlay{ position:fixed; inset:0; background:rgba(0,0,0,.6); display:flex; justify-content:center; align-items:center; z-index:2000; }
.modal-window{ background:#1e293b; padding:2rem; border-radius:14px; min-width:600px; max-width:90%; max-height:90vh; overflow:auto; display:flex; flex-direction:column; gap:1rem; }
.modal-form{ display:flex; flex-direction:column; gap:.8rem; }
.grid-two{ display:grid; grid-template-columns:1fr 1fr; gap:1rem; }
.modal-form label{ display:flex; flex-direction:column; font-size:.9rem; gap:.25rem; }
.modal-form input{ padding:.45rem .6rem; border:none; border-radius:6px; background:#111827; color:#fff; }
.actions{ display:flex; gap:.6rem; justify-content:center; grid-column:1 / -1; }
.cancel-btn{ padding:.6rem 1.4rem; border:none; border-radius:8px; background:#9ca3af; color:#1e293b; font-weight:600; cursor:pointer; }
.save-big{ padding:.6rem 1.4rem; border:none; border-radius:8px; background:#2563eb; font-weight:600; cursor:pointer; color:#fff; }
.search-in-modal{
  width:100%; padding:.6rem .8rem; border-radius:6px; border:1px solid #334155;
  background:#111827; color:#fff; font-size:1rem; margin-bottom:1rem;
}
.search-results-container{ min-height:200px; max-height:40vh; overflow-y:auto; background:#0d1130; border-radius:8px; padding:1rem; }
.results-table{ width:100%; border-collapse:collapse; }
.results-table tr{ border-bottom:1px solid #2c3148; }
.results-table tr:last-child{ border-bottom:none; }
.results-table td{ padding:.75rem; }
.results-table td:last-child{ text-align:right; }
.search-results-container p{ color:#94a3b8; text-align:center; margin-top:2rem; }
.search-wrapper{ margin-bottom:1rem; }
.search-clientes{
  max-width:300px; width:100%;
  padding:.4rem .8rem; border-radius:6px; background:#fff; color:#000; font-size:.8rem;
}
.add-button-wrapper{ display:flex; justify-content:flex-end; padding:0 1.5rem; }
.add-button{
  background:#374666; color:#fff; border:none; padding:.7rem 1.5rem; font-size:1rem;
  font-weight:600; border-radius:8px; cursor:pointer; transition: background-color .2s;
}
.add-button:hover{ background:#4a5568; }
</style>
