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
    <div
      v-if="modal.visible && modal.type === 'proveedor'"
      class="modal-overlay"
      @click.self="close"
    >
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
.page{ min-height:100vh; background:var(--color-octonary); color:#fff; }
.container{ max-width:1100px; margin:0 auto; padding:20px; }
.module{
  background:#0d1130; border:2px solid #1e2236; border-radius:16px; padding:16px;
}
.input{ width:100%; max-width:360px; padding:10px 12px; border-radius:10px; border:1px solid #cbd5e1; }
.input--white{ background:#fff; color:#000; }

.table-wrapper{ overflow:auto; margin-top:12px; }
.table{ width:100%; border-collapse:collapse; min-width:720px; background:#111827; }
.table thead th{
  text-align:left; background:var(--color-senary); color:#fff; padding:12px; position:sticky; top:0;
}
.table td{ padding:12px; border-top:1px solid #263043; color:#e5e7eb; }
.table-actions{ display:flex; gap:8px; }

.icon-btn{
  background:#334155; color:#fff; border:none; padding:6px 10px; border-radius:6px; cursor:pointer;
}
.icon-btn:hover{ background:#3b4b63 }
.icon-btn.danger{ background:#e11d48 }
.icon-btn.danger:hover{ background:#be123c }

.footer-actions{ display:flex; justify-content:flex-end; margin-top:14px; }
.btn{
  background: var(--color-senary); color:#fff; border:none; border-radius:10px; padding:10px 16px; cursor:pointer; font-weight:700;
}
.btn.secondary{ background:#6b7280 }
.btn:hover{ background: var(--color-tertiary); }

/* Modal */
.modal-overlay{ position:fixed; inset:0; background:rgba(0,0,0,.6); display:flex; align-items:center; justify-content:center; z-index:50; }
.modal-window{
  background:#1e293b; padding:20px; border-radius:14px; min-width:560px; max-width:90%; color:#fff;
}
.grid-two{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }
.grid-two label{ display:flex; flex-direction:column; gap:6px; font-size:.9rem; }
.grid-two input{
  padding:10px; border-radius:8px; border:1px solid #334155; background:#111827; color:#fff;
}
.modal-actions{ grid-column:1 / -1; display:flex; gap:10px; justify-content:flex-end; margin-top:6px; }

@media (max-width:700px){
  .modal-window{ min-width:unset; }
  .grid-two{ grid-template-columns:1fr; }
}
</style>
