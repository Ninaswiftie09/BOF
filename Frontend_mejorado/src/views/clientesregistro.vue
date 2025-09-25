<template>
  <div class="crm-home page">
    <NavBar title="CLIENTES">
      <template #actions>
        <input v-model="search" class="input--white" placeholder="Buscar clientes…" />
      </template>
    </NavBar>

    <div class="body-wrapper container">
      <section class="module">
        <!-- Tabla reutilizable (sin 'Contacto') -->
        <Tablas
          :columns="columns"
          :rows="filteredClientes"
          :center="true"
          :searchable="false"
          :actions="{ edit:true, delete:true }"
          @edit="editCliente"
          @delete="(row) => deleteCliente(row.id)"
        />

        <div class="footer-actions" style="justify-content:flex-end">
          <button class="btn" @click="open('clientes')">Agregar Cliente</button>
        </div>
      </section>
    </div>

    <!-- Modal Clientes (compacto + oscuro) -->
    <div v-if="modal.visible && modal.type==='clientes'" class="modal-overlay" @click.self="close">
      <div class="modal-content modal--compact">
        <h3>{{ clienteForm.id ? 'Editar Cliente' : 'Nuevo Cliente' }}</h3>

        <form class="form-vertical" @submit.prevent="saveCliente">
          <div class="form-field">
            <label>Nombre</label>
            <input class="input--dark" v-model="clienteForm.nombre" required />
          </div>

          <div class="form-field">
            <label>NIT</label>
            <input class="input--dark" v-model="clienteForm.nit" />
          </div>

          <div class="form-field">
            <label>Dirección</label>
            <input class="input--dark" v-model="clienteForm.direccion" />
          </div>

          <div class="form-field">
            <label>Dirección Entrega</label>
            <input class="input--dark" v-model="clienteForm.direccion_entrega" />
          </div>

          <div class="form-field">
            <label>Teléfono</label>
            <input class="input--dark" v-model="clienteForm.telefono" />
          </div>

          <div class="form-field">
            <label>E-mail</label>
            <input class="input--dark" type="email" v-model="clienteForm.email" />
          </div>

          <div class="modal-actions">
            <button type="submit" class="btn">Guardar</button>
            <button type="button" class="btn btn--muted" @click="close">Cancelar</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal búsqueda (opcional, igual que antes) -->
    <div v-if="modal.visible && modal.type === 'buscar'" class="modal-overlay" @click.self="close">
      <div class="modal-content modal--compact">
        <h3>Buscar Cliente para Modificar o Eliminar</h3>

        <input
          v-model="modal.searchTerm"
          @input="searchClientsInModal"
          class="input--dark"
          placeholder="Escribe un nombre para buscar..."
        />

        <div class="table-wrapper" style="margin-top:10px">
          <table class="table dark-table table--center">
            <tbody>
              <tr v-for="cliente in modal.searchResults" :key="cliente.id">
                <td style="text-align:left">{{ cliente.nombre }}</td>
                <td class="table-actions" style="display:flex; gap:.5rem">
                  <button class="btn btn--muted" @click="editCliente(cliente)">✎</button>
                  <button class="btn btn--danger" @click="deleteCliente(cliente.id)">✕</button>
                </td>
              </tr>
              <tr v-if="modal.searchResults.length===0 && modal.searchTerm">
                <td class="muted" colspan="2">No se encontraron clientes.</td>
              </tr>
              <tr v-else-if="!modal.searchTerm">
                <td class="muted" colspan="2">Comienza a escribir para ver los resultados.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="modal-actions">
          <button type="button" class="btn btn--muted" @click="close">Cerrar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import Tablas from '@/components/Reutilizacion/Tablas.vue'
import { apiFetch } from '@/utils/api'
import { bus } from '@/event-bus'

const router = useRouter()
const go = path => router.push(path)

/* columnas de la tabla (SIN 'Contacto') */
const columns = [
  { key: 'codigo_cliente', label: 'Código' },
  { key: 'nombre',         label: 'Nombre' },
  { key: 'telefono',       label: 'Teléfono' },
  { key: 'nit',            label: 'NIT' },
]

/* UI & estado */
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

/* FORMULARIO CLIENTES (SIN 'contacto') */
const clienteForm = reactive({
  id: null,
  codigo_cliente: '',
  estado: true,
  nombre: '',
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
  for (const [k,v] of Object.entries(sample)) {
    if (typeof v === 'string' && !isNaN(Date.parse(v)) && /fecha|date|crea|alta|reg/i.test(k)) return k
  }
  return null
}

function emitirKpiClientesNuevos() {
  const list = clientes.value || []
  const field = pickDateField(list[0])
  const start = new Date(); start.setDate(1); start.setHours(0,0,0,0)
  const end = new Date(start); end.setMonth(start.getMonth()+1)
  let nuevosMes
  if (!field) {
    nuevosMes = list.length
  } else {
    nuevosMes = list.filter(c => {
      const t = Date.parse(c[field])
      return !isNaN(t) && t >= +start && t < +end
    }).length
  }
  bus.emit('clientes-actualizados', { nuevosMes })
}

/* ===== FETCH ===== */
async function fetchClientes () {
  try {
    const data = await apiFetch('/api/clientes/')
    clientes.value = Array.isArray(data) ? data : (Array.isArray(data?.results) ? data.results : [])
    emitirKpiClientesNuevos()
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
    /* contacto eliminado */
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

/* ===== EDITAR / ELIMINAR ===== */
function editCliente (cliente) {
  // si el backend sigue mandando 'contacto', se ignora al no existir en el form
  const { id, codigo_cliente, estado, nombre, nit, direccion, direccion_entrega, telefono, email, cartera } = cliente
  Object.assign(clienteForm, { id, codigo_cliente, estado, nombre, nit, direccion, direccion_entrega, telefono, email, cartera })
  modal.type = 'clientes'
  modal.visible = true
}

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

/* ===== FILTROS (sin 'contacto') ===== */
const filteredClientes = computed(() =>
  clientes.value.filter(c =>
    [c.codigo_cliente, c.nombre, c.telefono, c.nit]
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

<style scoped>
.crm-home{
  min-height:100vh;
  background:#0a0f2c;
  display:flex; flex-direction:column;
  font-family:'Segoe UI',sans-serif; color:#fff;
}
.body-wrapper{ padding: 2rem; display:flex; flex-direction:column; gap:2rem; }
</style>
