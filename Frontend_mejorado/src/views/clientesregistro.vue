<template>
  <div class="page-container">
    <NavBar title="CLIENTES">
      <template #actions>
        <input v-model="search" class="input-dark" placeholder="Buscar clientes…" style="max-width: 300px;" />
      </template>
    </NavBar>

    <div class="page-content">
      <section class="module">
        
        <!-- Reemplazo del componente Tablas.vue -->
        <div class="table-wrapper">
          <table class="table">
            <thead>
              <tr>
                <th v-for="col in columns" :key="col.key">{{ col.label }}</th>
                <th style="width:140px; text-align: right;">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="cliente in filteredClientes" :key="cliente.id">
                <td v-for="col in columns" :key="col.key">
                  {{ cliente[col.key] }}
                </td>
                <td class="actions" style="justify-content: flex-end;">
                  <button class="icon-btn edit" title="Editar" @click="editCliente(cliente)">✎</button>
                  <button class="icon-btn delete" title="Eliminar" @click="deleteCliente(cliente.id)">✕</button>
                </td>
              </tr>
              <tr v-if="filteredClientes.length === 0">
                <td :colspan="columns.length + 1" class="muted-text" style="text-align:center; padding: 1.2rem 0;">
                  No hay datos para mostrar
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="footer-actions">
          <button class="btn btn-primary" @click="open('clientes')">Agregar Cliente</button>
        </div>
      </section>
    </div>

    <!-- Modal Clientes (Agregar/Editar) -->
    <div v-if="modal.visible && modal.type==='clientes'" class="modal-overlay" @click.self="close">
      <div class="modal-content-dark">
        <h3>{{ clienteForm.id ? 'Editar Cliente' : 'Nuevo Cliente' }}</h3>

        <form @submit.prevent="saveCliente" class="form-grid">
          <div class="form-group">
            <label for="nombre" class="form-label">Nombre</label>
            <input id="nombre" class="form-input" v-model="clienteForm.nombre" required />
          </div>

          <div class="form-group">
            <label for="nit" class="form-label">NIT</label>
            <input id="nit" class="form-input" v-model="clienteForm.nit" />
          </div>

          <div class="form-group">
            <label for="direccion" class="form-label">Dirección</label>
            <input id="direccion" class="form-input" v-model="clienteForm.direccion" />
          </div>

          <div class="form-group">
            <label for="entrega" class="form-label">Dirección Entrega</label>
            <input id="entrega" class="form-input" v-model="clienteForm.direccion_entrega" />
          </div>

          <div class="form-group">
            <label for="telefono" class="form-label">Teléfono</label>
            <input id="telefono" class="form-input" v-model="clienteForm.telefono" />
          </div>

          <div class="form-group">
            <label for="email" class="form-label">E-mail</label>
            <input id="email" class="form-input" type="email" v-model="clienteForm.email" />
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
import { useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
// Ya no importamos Tablas.vue
import { apiFetch } from '@/utils/api'
import { bus } from '@/event-bus'

const router = useRouter()
const go = path => router.push(path)

const columns = [
  { key: 'codigo_cliente', label: 'Código' },
  { key: 'nombre',         label: 'Nombre' },
  { key: 'telefono',       label: 'Teléfono' },
  { key: 'nit',            label: 'NIT' },
]

const search = ref('')
const modal = reactive({ visible: false, type: '' })
const open = t => {
  modal.type = t
  modal.visible = true
}
const close = () => { modal.visible = false; resetForm() }

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

function pickDateField(sample) {
  if (!sample) return null
  const preferred = ['created_at','fecha_registro','creado','fecha_creacion','fecha','fecha_alta','f_creacion','created','createdAt']
  for (const k of preferred) if (sample[k] && !isNaN(Date.parse(sample[k]))) return k
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
  let nuevosMes = field
    ? list.filter(c => { const t = Date.parse(c[field]); return !isNaN(t) && t >= +start && t < +end }).length
    : list.length
  bus.emit('clientes-actualizados', { nuevosMes })
}

async function fetchClientes () {
  try {
    const data = await apiFetch('/api/clientes/')
    clientes.value = Array.isArray(data) ? data : (Array.isArray(data?.results) ? data.results : [])
    emitirKpiClientesNuevos()
  } catch (e) { console.error('Error al obtener clientes:', e) }
}
onMounted(fetchClientes)

function resetForm () {
  Object.assign(clienteForm, { id: null, codigo_cliente: '', estado: true, nombre: '', nit: '', direccion: '', direccion_entrega: '', telefono: '', email: '', cartera: 0 })
}

async function saveCliente () {
  if (!clienteForm.nombre) return alert('El nombre es requerido')
  const isUpdating = !!clienteForm.id
  const method = isUpdating ? 'PUT' : 'POST'
  const url = isUpdating ? `/api/clientes/${clienteForm.id}/` : `/api/clientes/`
  const payload = {
    nombre: clienteForm.nombre,
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
  } catch (err) { console.error('Error al guardar cliente:', err); alert('Hubo un error al guardar el cliente.') }
}

function editCliente (cliente) {
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
  } catch (err) { console.error('Error al eliminar cliente:', err); alert('Error al eliminar el cliente') }
}

const filteredClientes = computed(() =>
  clientes.value.filter(c =>
    [c.codigo_cliente, c.nombre, c.telefono, c.nit]
      .some(v => v?.toString().toLowerCase().includes(search.value.toLowerCase()))
  )
)
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

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
}

.modal-actions {
  grid-column: 1 / -1;
}
</style>