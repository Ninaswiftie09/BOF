/* clientesregistro.vue */
<script setup>
import { reactive, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import { onMounted } from 'vue'
import { apiFetch } from '../utils/api'

const router = useRouter()
const go = path => router.push(path)

const search = ref('')
const modal = reactive({ visible: false, type: '', searchTerm: '', searchResults: [] })
const open = t => {
  modal.type = t;
  modal.visible = true;
  if (t === 'buscar') {
    modal.searchTerm = '';
    modal.searchResults = [];
  }
}
const close = () => { modal.visible = false; resetForm();  }

/* FORMULARIO CLIENTES */
const clienteForm = reactive({
  id: null,
  codigo_cliente: '',
  estado: true,
  nombre: '',
  contacto: '', /*eliminar contacto*/
  nit: '',
  direccion: '',
  direccion_entrega: '',
  telefono: '',
  email: '',
  cartera: 0,
})
const clientes = ref([])

/* FUNCIÓN FETCH */
async function fetchClientes() {
  try {
    const data = await apiFetch('/api/clientes/')
    clientes.value = data
  } catch (error) {
    console.error('Error al obtener clientes:', error)
  }
}

onMounted(() => {
  fetchClientes()
})


function resetForm() {
  Object.assign(clienteForm, {
    id: null,
    codigo_cliente: '',
    estado: true,
    nombre: '',
    contacto: '', /*eliminar contacto*/
    nit: '',
    direccion: '',
    direccion_entrega: '',
    telefono: '',
    email: '',
    cartera: 0
  })
}

/* GUARDAR CLIENTE */
async function saveCliente() {
  if (!clienteForm.nombre) return alert('El nombre es requerido')

  const isUpdating = !!clienteForm.id;
  const method = isUpdating ? 'PUT' : 'POST'
  const url = isUpdating
    ? `/api/clientes/${clienteForm.id}/`
    : `/api/clientes/`

  const payload = { 
    nombre: clienteForm.nombre,
    contacto: clienteForm.contacto,
    nit: clienteForm.nit,
    direccion: clienteForm.direccion,
    direccion_entrega: clienteForm.direccion_entrega,
    telefono: clienteForm.telefono,
    email: clienteForm.email,
    cartera: clienteForm.cartera,
    estado: clienteForm.estado,
  };

  delete payload.id;
  delete payload.codigo_cliente;

  try {
    await apiFetch(url, method, payload)
    await fetchClientes()
    close()
  } catch (err) {
    console.error('Error al guardar cliente:', err);
    alert('Hubo un error al guardar el cliente.');
  }
}

/* EDITAR CLIENTE */
function editCliente(cliente) {
  Object.assign(clienteForm, { ...cliente, id: cliente.id })
  modal.type = 'clientes'
  modal.visible = true
}

/* ELIMINAR CLIENTE */
async function deleteCliente(id) {
  if (!confirm(`¿Seguro que deseas eliminar al cliente con ID ${id}?`)) return

  try {
    await apiFetch(`/api/clientes/${id}/`, 'DELETE')
    await fetchClientes()
    close()
  } catch (err) {
    console.error('Error al eliminar cliente:', err)
    alert('Error al eliminar el cliente')
  }
}

/* FILTRO DE BÚSQUEDA */
const filteredClientes = computed(() =>
  clientes.value.filter(c =>
    [c.codigo_cliente, c.nombre, c.contacto]  /*eliminar contacto*/
      .some(v => v?.toString().toLowerCase().includes(search.value.toLowerCase()))
  )
)

/* FILTRO DE BÚSQUEDA POR NOMBRE */
function searchClientsInModal() {
  if (!modal.searchTerm) {
    modal.searchResults = [];
    return;
  }
  modal.searchResults = clientes.value.filter(c =>
    c.nombre.toLowerCase().includes(modal.searchTerm.toLowerCase())
  );
}



</script>

<template>
  <div class="crm-home">
    <NavBar title="CLIENTES">
      <template #actions>
        <input v-model="search" class="search" placeholder="Buscar clientes…" />
        <button class="avatar-btn"></button>
      </template>
    </NavBar>

    <div class="body-wrapper">
      
      <!-- Tabla de clientes -->
      <section class="module">
        <div class="search-wrapper">
          <input v-model="search" class="search-clientes" placeholder="Buscar clientes…" />
        </div>

        <table>
          <thead>
            <tr>
              <th>Código</th>
              <th>Nombre</th>
              <th>Contacto</th> <!-- eliminar contacto -->
              <th>Teléfono</th>
              <th>NIT</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in filteredClientes" :key="c.codigo_cliente">
              <td>{{ c.codigo_cliente }}</td>
              <td>{{ c.nombre }}</td>
              <td>{{ c.contacto }}</td> <!-- eliminar contacto -->
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

      <!-- Tarjetas de acción -->
      <div class="add-button-wrapper">
        <button class="add-button" @click="open('clientes')">Agregar Cliente</button>
      </div>

    </div>

    <!-- Modal de Clientes -->
    <div v-if="modal.visible && modal.type==='clientes'" class="modal-overlay" @click.self="close">
      <div class="modal-window">
        <h3>{{ clienteForm.id ? 'Editar Cliente' : 'Nuevo Cliente' }}</h3>
        <form class="modal-form grid-two" @submit.prevent="saveCliente">
          <label>Nombre<input v-model="clienteForm.nombre" required/></label>
          <label>Contacto<input v-model="clienteForm.contacto"/></label>  <!-- eliminar contacto -->
          <label>NIT<input v-model="clienteForm.nit"/></label>
          <label>Dirección<input v-model="clienteForm.direccion"/></label>
          <label>Dirección Entrega<input v-model="clienteForm.direccionEntrega"/></label>
          <label>Teléfono<input v-model="clienteForm.telefono"/></label>
          <label>E-mail<input type="email" v-model="clienteForm.email"/></label>
          <div class="actions">
            <button type="submit" class="save-big">Guardar</button>
            <button type="button" class="cancel-btn" @click="close">Cancelar</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal de busqueda por nombre -->
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
.crm-home{
  min-height:100vh;
  background:#0a0f2c;
  display:flex;
  flex-direction:column;
  font-family:'Segoe UI',sans-serif;
  color: #fff;
}

.body-wrapper{
  padding: 5rem 2rem;
  display:flex;
  flex-direction:column;
  gap:2rem;
}

.avatar-btn{
  width:36px;
  height:36px;
  border-radius:50%;
  background:#fff;
  border:none;
  cursor:pointer
}

.module{
  background:#0d1130;
  border:2px solid #1e2236;
  border-radius:16px;
  padding:1.5rem;
}
.cards-module{
  justify-content:center;
  display:flex
}


/* TABLA CLIENTES */
table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 4px; /* Espacio vertical entre filas */
  min-width: 800px;
}
th {
  background-color: transparent;
  padding: 12px 16px;
  color: #fff; /* Texto de encabezado gris */
  font-size: 0.9rem;
  text-align: left;
  border-bottom: 2px solid #334155; /* Línea inferior */
}
td {
  padding: 16px;
  background-color: #1e293b; /* Fondo oscuro para las filas */
  color: #ffffff;
  text-align: left;
  vertical-align: middle;
  border: none;
}
/* Estilo para la fila de "No hay resultados" */
tr[v-if="filteredClientes.length===0"] td {
  background-color: transparent;
  text-align: center;
  padding: 2rem;
  font-style: italic;
  color: #94a3b8;
}




.edit-btn, .remove-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
}
.edit-btn { color: #60a5fa; }
.remove-btn { color: #e74c3c; }
.edit-btn:hover { color: #93c5fd; }
.remove-btn:hover { color: #f87171; }


.cards-container{
  display:flex;
  gap:3rem;
  flex-wrap:wrap;
  justify-content:center;
  padding:0
}
.big-card{
  width:340px;
  min-height:150px;
  background:#101222;
  border:2px solid #1e2236;
  border-radius:18px;
  padding:1.5rem;
  display:flex;
  flex-direction:column;
  gap:1rem
}
.big-card h2{
  margin:0;
  font-size:1.1rem;
  letter-spacing:.5px;
  border-bottom:1px solid #2c3148;
  padding-bottom:.5rem;
  color:#fff
}
.big-card ul{
  list-style:none;
  margin: 0;
  padding: 0;
  display:flex;
  flex-direction:column;
  gap:.8rem
}
.big-card li{
  cursor:pointer;
  padding:.4rem .2rem;
  border-radius:6px
}
.big-card li:hover{ background:#1e2236 }

.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.6);display:flex;justify-content:center;align-items:center;z-index:2000}
.modal-window{background:#1e293b;padding:2rem;border-radius:14px;min-width:600px;max-width:90%;max-height:90vh;overflow:auto;display:flex;flex-direction:column;gap:1rem}
.modal-form{display:flex;flex-direction:column;gap:.8rem}
.grid-two{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
.modal-form label{display:flex;flex-direction:column;font-size:.9rem;gap:.25rem}
.modal-form input{padding:.45rem .6rem;border:none;border-radius:6px;background:#111827;color:#fff}
.actions{display:flex;gap:.6rem;justify-content:center; grid-column: 1 / -1;}
.cancel-btn{padding:.6rem 1.4rem;border:none;border-radius:8px;background:#9ca3af;color:#1e293b;font-weight:600;cursor:pointer}
.save-big{padding:.6rem 1.4rem;border:none;border-radius:8px;background:#2563eb;font-weight:600;cursor:pointer;color:#fff}


.remove-btn-modal { 
  background-color: #e74c3c; 
}
.remove-btn-modal:hover { 
  background-color: #ff6b6b; 
}

.search-in-modal {
  width: 100%;
  padding: .6rem .8rem;
  border-radius: 6px;
  border: 1px solid #334155;
  background: #111827;
  color: #fff;
  font-size: 1rem;
  margin-bottom: 1rem;
}
.search-results-container {
  min-height: 200px;
  max-height: 40vh;
  overflow-y: auto;
  background: #0d1130;
  border-radius: 8px;
  padding: 1rem;
}
.results-table {
  width: 100%;
  border-collapse: collapse;
}
.results-table tr {
  border-bottom: 1px solid #2c3148;
}
.results-table tr:last-child {
  border-bottom: none;
}
.results-table td {
  padding: .75rem;
}
.results-table td:last-child {
  text-align: right;
}
.search-results-container p {
  color: #94a3b8;
  text-align: center;
  margin-top: 2rem;
}

/* barra de búsqueda*/
.search-wrapper {
  margin-bottom: 1rem;
}
.search-clientes {
  max-width: 300px;
  width: 100%;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  background: #fff;
  color: #000;
  font-size: 0.8rem;
}

/* Boton agregar clientes */
.add-button-wrapper {
  display: flex;
  justify-content: flex-end; 
  padding: 0 1.5rem;
}
.add-button {
  background: #374666;
  color: white;
  border: none;
  padding: .7rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}
.add-button:hover {
  background: #4a5568;
}

</style>