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
            <button type="submit" class="btn">Guardar</button>
            <button type="button" class="btn secondary" @click="close">Cancelar</button>
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

const modal = reactive({ visible: false, type: '' })
const currentProveedor = ref(null)
const proveedores = ref([])
const searchQuery = ref('')

const proveedorForm = reactive({ id: null, nombre: '', correo: '', telefono: '', direccion: '' })

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

async function fetchProveedores() {
  try {
    proveedores.value = await apiFetch('/api/proveedores/')
  } catch (e) {
    console.error('Error cargando proveedores', e)
    proveedores.value = []
  }
}

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
.page{
  min-height:100vh;
  background:var(--color-octonary); /*fondo pantalla proveedores*/
  color:#fff; /*nada*/
}

.container{ max-width:1100px; margin:0 auto; padding:20px; }
.module{
  background:#0d1130; /*fondo tarjeta proveedores*/
  border:2px solid #1e2236; /*borde tarjeta proveedores*/
  border-radius:16px; padding:16px;
}
.input{
  width:100%; max-width:360px; padding:10px 12px; border-radius:10px;
  border:1px solid #cbd5e1; /*borde input buscador proveedores*/
}
.input--white{
  background:#fff; /*fondo input buscador proveedores*/
  color:#000; /*color texto input buscador proveedores*/
}

.table-wrapper{ overflow:auto; margin-top:12px; }
.table{
  width:100%; border-collapse:collapse; min-width:720px;
  background:#111827; /*todos los bordes de tabla*/
}
.table thead th{
  text-align:left;
  background:var(--color-senary); /*fondo encabezados*/
  color:#fff; /*texto encabezados*/
  padding:12px; position:sticky; top:0;
}
.table td{
  padding:12px;
  border-top:1px solid #263043; /*lineas separadoras entre proveedores tabla*/
  color:#e5e7eb; /*texto de proveedores guardados tabla*/
}
.table-actions{ display:flex; gap:8px; }

.edit-btn,.remove-btn{ background:transparent; border:none; cursor:pointer; font-size:1.1rem; }
.edit-btn{
  color:#60a5fa; /*color icono editar*/
}
.remove-btn{
  color:#e74c3c; /*color icono eliminar*/
}

.edit-btn:hover{
  color:#93c5fd; /*color icono editar cursor arriba*/
}
.remove-btn:hover{
color:#f87171; /*color icono eliminar cursor arriba*/
}


.footer-actions{ display:flex; justify-content:flex-end; margin-top:14px; }
.btn{
  background: var(--color-senary); /*fondo boton "agregar proveedores" y "guardar" en formulario*/
  color:#fff; /*texto boton "agregar proveedores" y "guardar" en formulario*/
  border:none; border-radius:10px; padding:10px 16px; cursor:pointer; font-weight:700;
}
.btn.secondary{ background:#6b7280 } /*fondo boton "cancelar" formulario*/
.btn:hover{ background: var(--color-tertiary); } /*fondo de botones "agregar proveedores", "guardar" y "cancelar" cursor arriba*/

/* Modal */
.modal-overlay{
  position:fixed; inset:0;
  background:rgba(0,0,0,.6); /*fondo pantalla completa formulario*/
  display:flex; align-items:center; justify-content:center; z-index:50;
}
.modal-window{
  background:#1e293b; /*fondo tarjeta formulario nuevo proveedor*/
  padding:20px; border-radius:14px; min-width:560px; max-width:90%;
  color:#fff; /*texto campo formulario nuevo proveedor*/
}
.grid-two{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }
.grid-two label{ display:flex; flex-direction:column; gap:6px; font-size:.9rem; }
.grid-two input{
  padding:10px; border-radius:8px;
  border:1px solid #334155; /*borde inputs formulario*/
  background:#111827; /*fondo inputs formulario*/
  color:#fff; /*texto ingresado input formulario*/
}
.modal-actions{ grid-column:1 / -1; display:flex; gap:10px; justify-content:flex-end; margin-top:6px; }

@media (max-width:700px){
  .modal-window{ min-width:unset; }
  .grid-two{ grid-template-columns:1fr; }
}
</style>
