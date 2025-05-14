<script setup>
import { reactive, ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const open = t => { modal.type = t; modal.visible = true }
const close = () => { modal.visible = false }

const modal = reactive({ visible: false, type: '' })

const proveedorForm = reactive({
  codigo: '', estado: 'Activo', nombre: '', contacto: '', nit: '',
  direccion: '', telefono: '', email: ''
})

const proveedores = ref([])

const compraForm = reactive({
  proveedor: '', fecha: '', insumos: '', costo: 0
})

const compras = ref([])

const searchQuery = ref('')  // Barra de búsqueda

// Método para filtrar los proveedores utilizando computed
const filteredProveedores = computed(() => {
  return proveedores.value.filter(p => p.nombre.toLowerCase().includes(searchQuery.value.toLowerCase()))
})

function saveProveedor() {
  if (!proveedorForm.codigo || !proveedorForm.nombre) return alert('Código y nombre')
  proveedores.value.push({ ...proveedorForm })
  Object.keys(proveedorForm).forEach(k => proveedorForm[k] = k === 'estado' ? 'Activo' : '')
  close()
}

function saveCompra() {
  compras.value.push({ id: Date.now(), proveedor: compraForm.proveedor, costo: compraForm.costo, fecha: compraForm.fecha })
  Object.keys(compraForm).forEach(k => compraForm[k] = '')
  close()
}
</script>

<template>
  <div class="crm-home">
    <header class="top-bar">
      <!-- Logo con redirección al Home -->
      <img src="@/assets/logo_bof_blanco.png" alt="Logo del cliente" class="logo" @click="router.push('/')"/>
      <h1>PROVEEDORES</h1>
      <button class="avatar-btn"></button>
    </header>

    <!-- Barra de búsqueda -->
    <div class="search-wrapper">
      <input v-model="searchQuery" class="search" placeholder="Buscar proveedores..." />
    </div>

    <!-- Botón para abrir el modal de Nueva Compra -->
    <div class="new-order-wrapper">
      <button class="new-order-btn" @click="open('compra')">NUEVA COMPRA</button>
    </div>

    <!-- Tabla de Proveedores -->
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Código</th>
            <th>Nombre</th>
            <th>Contacto</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(proveedor, index) in filteredProveedores" :key="index">
            <td>{{ proveedor.codigo }}</td>
            <td>{{ proveedor.nombre }}</td>
            <td>{{ proveedor.contacto }}</td>
            <td>{{ proveedor.estado }}</td>
            <td>
              <button @click="open('historial')">Ver Historial</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal de Nueva Compra -->
    <div v-if="modal.visible && modal.type === 'compra'" class="modal-overlay" @click.self="close">
      <div class="modal-window">
        <h3>Nueva Compra</h3>
        <form class="modal-form grid-two" @submit.prevent="saveCompra">
          <label>Proveedor
            <select v-model="compraForm.proveedor">
              <option v-for="p in proveedores" :key="p.codigo" :value="p.nombre">{{p.nombre}}</option>
            </select>
          </label>
          <label>Fecha <input type="date" v-model="compraForm.fecha" /></label>
          <label>Insumos adquiridos <input v-model="compraForm.insumos" /></label>
          <label>Costo total <input type="number" min="0" v-model.number="compraForm.costo" /></label>
          <button class="save-big" type="submit">Guardar</button>
          <button class="cancel-btn" type="button" @click="close">Cancelar</button>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
*{color:#fff}
.crm-home{min-height:100vh;background:#0a0f2c;display:flex;flex-direction:column;font-family:'Segoe UI',sans-serif}
.top-bar{display:flex;align-items:center;gap:1.5rem;padding:.75rem 2rem;background:#1e293b;justify-content:space-between;align-items:center}
h1{font-family:'Segoe UI', sans-serif;color:#ffffff;font-size:2rem;flex-grow: 1;text-align:center}

.logo {
  width: 150px; /* Limitar el tamaño del logo */
  height: auto; /* Mantener proporciones */
  cursor: pointer;
}

.search-wrapper {
  padding: 1rem 2rem;
}

.search {
  padding:.4rem .8rem;
  border-radius:6px;
  border:none;
  background:#fff;
  color:#000;
  width: 100%;
}

.new-order-wrapper {
  display: flex;
  justify-content: flex-end;
  padding: 1.5rem 2rem;
}

.new-order-btn {
  background:#1d4ed8;
  border:none;
  color:#fff;
  border-radius:12px;
  padding:.7rem 1.6rem;
  font-weight:600;
  cursor:pointer;
}

.table-wrapper {
  max-height:60vh;
  overflow:auto;
  padding: 2rem;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding:.4rem .6rem;
  border-bottom:1px solid #2c3148;
}

thead {
  position:sticky;
  top:0;
  background:#1e2236;
}

button {
  padding: .5rem 1rem;
  margin-top: 1rem;
}
</style>
