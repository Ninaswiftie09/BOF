<script setup>
import { reactive, ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
function goHome() { router.push({ name: 'home' }) }

const API = 'http://localhost:8000/api'

const modal = reactive({ visible: false, type: '' })
const currentProveedor = ref(null)

const proveedores = ref([])
const compras = ref([])

const searchQuery = ref('')
const searchReportQuery = ref('')

const proveedorForm = reactive({ nombre: '', correo: '', telefono: '', direccion: '' })
const compraForm = reactive({ proveedor: '', descripcion: '', monto: '' })

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

function open(type, prov = null) {
  modal.type = type
  modal.visible = true
  if (type === 'historial' && prov) currentProveedor.value = prov
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
async function fetchCompras() {
  try {
    compras.value = (await axios.get(`${API}/compras/`)).data
  } catch (e) {
    console.error('Error cargando compras', e)
  }
}

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

onMounted(() => {
  fetchProveedores()
  fetchCompras()
})
</script>

<template>
  <div class="crm-home">
    <header class="top-bar">
      <img src="@/assets/logo_bof_blanco.png" alt="Logo del cliente" class="logo" @click="goHome" />
      <h1>PROVEEDORES</h1>
      <button class="avatar-btn"></button>
    </header>

    <div class="new-order-wrapper">
      <button class="new-order-btn" @click="open('compra')">NUEVA COMPRA</button>
    </div>

    <div class="body-wrapper">
      <section class="module">
        <input v-model="searchQuery" class="search" placeholder="Buscar proveedores…" />
        <table>
          <thead>
            <tr><th>ID</th><th>Nombre</th><th>Correo</th><th>Teléfono</th><th>Dirección</th><th>Acciones</th></tr>
          </thead>
          <tbody>
            <tr v-for="prov in filteredProveedores" :key="prov.id">
              <td>{{ prov.id }}</td>
              <td>{{ prov.nombre }}</td>
              <td>{{ prov.correo }}</td>
              <td>{{ prov.telefono }}</td>
              <td>{{ prov.direccion }}</td>
              <td><button @click="open('historial', prov)">Ver historial</button></td>
            </tr>
            <tr v-if="filteredProveedores.length === 0">
              <td colspan="6">&nbsp;</td>
            </tr>
          </tbody>
        </table>
      </section>

      <section class="module cards-module">
        <div class="cards-container">
          <section class="big-card">
            <h2>ACTUALIZACIÓN</h2>
            <ul><li @click="open('proveedor')">Agregar proveedor</li></ul>
          </section>
          <section class="big-card">
            <h2>REPORTES</h2>
            <ul>
              <li @click="open('historial')">Historial de compras</li>
            </ul>
          </section>
        </div>
      </section>
    </div>

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

    <div v-if="modal.visible && modal.type === 'compra'" class="modal-overlay" @click.self="close">
      <div class="modal-window">
        <h3>Nueva Compra</h3>
        <form class="modal-form grid-two" @submit.prevent="saveCompra">
          <label>Proveedor
            <select v-model="compraForm.proveedor" required>
              <option disabled value="">Selecciona un proveedor</option>
              <option v-for="p in proveedores" :key="p.id" :value="p.id">{{ p.nombre }}</option>
            </select>
          </label>
          <label>Descripción<input v-model="compraForm.descripcion" required /></label>
          <label>Monto<input type="number" step="0.01" v-model="compraForm.monto" required /></label>
          <button class="save-big" type="submit">Guardar</button>
          <button class="cancel-btn" type="button" @click="close">Cancelar</button>
        </form>
      </div>
    </div>

    <div v-if="modal.visible && modal.type === 'historial'" class="modal-overlay" @click.self="close">
      <div class="modal-window">
        <h3>Historial de Compras de {{ currentProveedor.nombre }}</h3>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr><th>ID</th><th>Fecha</th><th>Descripción</th><th>Monto</th></tr>
            </thead>
            <tbody>
              <tr v-for="c in compras.filter(x => x.proveedor === currentProveedor.id)" :key="c.id">
                <td>{{ c.id }}</td><td>{{ c.fecha }}</td><td>{{ c.descripcion }}</td><td>{{ c.monto }}</td>
              </tr>
              <tr v-if="!compras.some(x => x.proveedor === currentProveedor.id)">
                <td colspan="4" class="text-center py-4">Sin compras para este proveedor.</td>
              </tr>
            </tbody>
          </table>
        </div>
        <button class="cancel-btn" @click="close">Cerrar</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Segoe+UI&display=swap');
* { color: #fff; box-sizing: border-box; }
body, html { margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; }

.crm-home { background: #0a0f2c; min-height: 100vh; display: flex; flex-direction: column; }
.top-bar { display: flex; align-items: center; justify-content: space-between; background: #1e293b; padding: 0.75rem 2rem; }
.logo { width: 150px; cursor: pointer; }
h1 { flex-grow: 1; text-align: center; font-size: 2rem; color: white; }
.avatar-btn { width: 36px; height: 36px; border-radius: 50%; background: white; border: none; cursor: pointer; }

.new-order-wrapper { display: flex; justify-content: flex-end; padding: 1.5rem 2rem; }
.new-order-btn { background: #1d4ed8; color: white; border: none; padding: 0.7rem 1.6rem; font-weight: 600; border-radius: 12px; cursor: pointer; }
.new-order-btn:hover { transform: translateY(-2px); }

.body-wrapper { padding: 1rem 2rem; display: flex; flex-direction: column; gap: 2rem; }
.module { background: #0d1130; border: 2px solid #1e2236; border-radius: 16px; padding: 1.5rem; }
.cards-module { display: flex; justify-content: center; }
.cards-container { display: flex; flex-wrap: wrap; gap: 3rem; justify-content: center; }
.big-card { width: 340px; min-height: 300px; background: #101222; border: 2px solid #1e2236; border-radius: 18px; padding: 1.5rem; display: flex; flex-direction: column; gap: 1rem; }
.big-card h2 { margin: 0; font-size: 1.1rem; border-bottom: 1px solid #2c3148; padding-bottom: 0.5rem; }
.big-card ul { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 0.8rem; }
.big-card li { cursor: pointer; padding: 0.4rem 0.2rem; border-radius: 6px; }
.big-card li:hover { background: #1e2236; }

.search { max-width: 300px; padding: 0.4rem 0.8rem; border-radius: 6px; border: none; background: white; color: black; margin-bottom: 1rem; }
.table-wrapper { max-height: 60vh; overflow: auto; margin-bottom: 1rem; }
table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
th, td { padding: 0.4rem 0.6rem; border-bottom: 1px solid #2c3148; }
thead { position: sticky; top: 0; background: #1e2236; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); display: flex; justify-content: center; align-items: center; z-index: 2000; }
.modal-window { background: #1e293b; padding: 2rem; border-radius: 14px; min-width: 600px; max-width: 90%; max-height: 90vh; overflow: auto; display: flex; flex-direction: column; gap: 1rem; }
.modal-form { display: flex; flex-direction: column; gap: 0.8rem; }
.grid-two { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 0.8rem; }
.modal-form label { display: flex; flex-direction: column; font-size: 0.9rem; gap: 0.25rem; }
.modal-form input, .modal-form select { padding: 0.45rem 0.6rem; border: none; border-radius: 6px; background: #111827; color: white; }
.save-big { grid-column: 1 / -1; padding: 0.6rem 1rem; border: none; border-radius: 8px; background: #2563eb; font-weight: 600; cursor: pointer; color: white; }
.cancel-btn { align-self: center; padding: 0.4rem 1.4rem; border: none; border-radius: 8px; background: #9ca3af; color: #1e2236; font-weight: 600; cursor: pointer; }
.cancel-btn:hover { background: #d1d5db; }
</style>
