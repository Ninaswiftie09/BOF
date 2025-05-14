<script setup>
import { reactive, ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Método para redirigir al home
function goHome() {
  router.push({ name: 'home' }) // Redirige directamente al home
}

const open = t => { 
  modal.type = t;  // Cambia el tipo de modal (proveedor o compra)
  modal.visible = true; // Muestra el modal
}
const close = () => { 
  modal.visible = false; // Cierra el modal
}

const modal = reactive({ visible: false, type: '' })

const proveedorForm = reactive({
  id: '', nombre: '', contacto: '', nit: '', telefono: '',
  email: '', direccion: '', fecha_registro: ''
})

const proveedores = ref([])

const compraForm = reactive({
  proveedor_id: '', fecha_compra: '', metodo_pago: '', monto_total: 0
})

const compras = ref([])

const detalleCompraForm = reactive({
  compra_id: '', nombre_producto: '', cantidad: 0, precio_unitario: 0, subtotal: 0
})

const detalleCompra = ref([])

const searchQuery = ref('')  // Barra de búsqueda para proveedores
const searchReportQuery = ref('')  // Barra de búsqueda para el historial de compras

// Método para filtrar los proveedores utilizando computed
const filteredProveedores = computed(() => {
  return proveedores.value.filter(p => p.nombre.toLowerCase().includes(searchQuery.value.toLowerCase()))
})

// Método para filtrar las compras utilizando computed
const filteredCompras = computed(() => {
  return compras.value.filter(c => c.proveedor_id.toLowerCase().includes(searchReportQuery.value.toLowerCase()))
})

function saveProveedor() {
  if (!proveedorForm.id || !proveedorForm.nombre) return alert('ID y nombre son obligatorios');
  proveedores.value.push({ ...proveedorForm });
  Object.keys(proveedorForm).forEach(k => proveedorForm[k] = '');  // Limpiar formulario
  close();
}

function saveCompra() {
  compras.value.push({
    id: Date.now(),
    proveedor_id: compraForm.proveedor_id,
    fecha_compra: compraForm.fecha_compra,
    metodo_pago: compraForm.metodo_pago,
    monto_total: compraForm.monto_total
  });
  Object.keys(compraForm).forEach(k => compraForm[k] = '');  // Limpiar formulario
  close();
}

function saveDetalleCompra() {
  detalleCompra.value.push({
    id: Date.now(),
    compra_id: detalleCompraForm.compra_id,
    nombre_producto: detalleCompraForm.nombre_producto,
    cantidad: detalleCompraForm.cantidad,
    precio_unitario: detalleCompraForm.precio_unitario,
    subtotal: detalleCompraForm.subtotal
  });
  Object.keys(detalleCompraForm).forEach(k => detalleCompraForm[k] = '');  // Limpiar formulario
  close();
}
</script>

<template>
  <div class="crm-home">
    <header class="top-bar">
      <!-- Logo con redirección al Home -->
      <img src="@/assets/logo_bof_blanco.png" alt="Logo del cliente" class="logo" @click="goHome"/>
      <h1>PROVEEDORES</h1>
      <button class="avatar-btn"></button>
    </header>

    <!-- Apartados de Actualización y Reportes -->
    <div class="section-container">
      <div class="update-section">
        <h2>ACTUALIZACIÓN</h2>
        <!-- Barra de búsqueda para proveedores -->
        <div class="search-wrapper">
          <input v-model="searchQuery" class="search" placeholder="Buscar proveedores..." />
        </div>
        <!-- Tabla de Proveedores y Nuevo Proveedor -->
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Contacto</th>
                <th>NIT</th>
                <th>Teléfono</th>
                <th>Email</th>
                <th>Dirección</th>
                <th>Fecha Registro</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(proveedor, index) in filteredProveedores" :key="index">
                <td>{{ proveedor.id }}</td>
                <td>{{ proveedor.nombre }}</td>
                <td>{{ proveedor.contacto }}</td>
                <td>{{ proveedor.nit }}</td>
                <td>{{ proveedor.telefono }}</td>
                <td>{{ proveedor.email }}</td>
                <td>{{ proveedor.direccion }}</td>
                <td>{{ proveedor.fecha_registro }}</td>
                <td>
                  <button @click="open('historial')">Ver Historial</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <!-- Botón de Agregar Proveedor -->
        <div class="new-order-wrapper">
          <button class="new-order-btn" @click="open('proveedor')">AGREGAR PROVEEDOR</button>
        </div>
      </div>

      <div class="report-section">
        <h2>REPORTES</h2>
        <!-- Barra de búsqueda para historial de compras -->
        <div class="search-wrapper">
          <input v-model="searchReportQuery" class="search" placeholder="Buscar historial de compras..." />
        </div>
        <!-- Historial de Compras -->
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Id</th><th>Proveedor</th><th>Fecha de Compra</th><th>Metodo de Pago</th><th>Monto Total</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(compra, index) in filteredCompras" :key="index">
                <td>{{ compra.id }}</td>
                <td>{{ compra.proveedor_id }}</td>
                <td>{{ compra.fecha_compra }}</td>
                <td>{{ compra.metodo_pago }}</td>
                <td>{{ compra.monto_total }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <!-- Mover el botón de Nueva Compra aquí -->
        <div class="new-order-wrapper">
          <button class="new-order-btn" @click="open('compra')">NUEVA COMPRA</button>
        </div>
      </div>
    </div>

    <!-- Modal de Nuevo Proveedor -->
    <div v-if="modal.visible && modal.type === 'proveedor'" class="modal-overlay" @click.self="close">
      <div class="modal-window">
        <h3>Nuevo Proveedor</h3>
        <form class="modal-form grid-two" @submit.prevent="saveProveedor">
          <label>ID
            <input v-model="proveedorForm.id" />
          </label>
          <label>Nombre
            <input v-model="proveedorForm.nombre" />
          </label>
          <label>Contacto
            <input v-model="proveedorForm.contacto" />
          </label>
          <label>NIT
            <input v-model="proveedorForm.nit" />
          </label>
          <label>Teléfono
            <input v-model="proveedorForm.telefono" />
          </label>
          <label>Email
            <input v-model="proveedorForm.email" />
          </label>
          <label>Dirección
            <input v-model="proveedorForm.direccion" />
          </label>
          <label>Fecha Registro
            <input type="date" v-model="proveedorForm.fecha_registro" />
          </label>
          <button class="save-big" type="submit">Guardar</button>
          <button class="cancel-btn" type="button" @click="close">Cancelar</button>
        </form>
      </div>
    </div>

    <!-- Modal de Nueva Compra -->
    <div v-if="modal.visible && modal.type === 'compra'" class="modal-overlay" @click.self="close">
      <div class="modal-window">
        <h3>Nueva Compra</h3>
        <form class="modal-form grid-two" @submit.prevent="saveCompra">
          <label>Proveedor
            <select v-model="compraForm.proveedor_id">
              <option v-for="p in proveedores" :key="p.id" :value="p.id">{{p.nombre}}</option>
            </select>
          </label>
          <label>Fecha de Compra <input type="date" v-model="compraForm.fecha_compra" /></label>
          <label>Metodo de Pago
            <input v-model="compraForm.metodo_pago" />
          </label>
          <label>Monto Total
            <input type="number" min="0" v-model.number="compraForm.monto_total" />
          </label>
          <button class="save-big" type="submit">Guardar</button>
          <button class="cancel-btn" type="button" @click="close">Cancelar</button>
        </form>
      </div>
    </div>

    <!-- Modal de Detalle de Compra -->
    <div v-if="modal.visible && modal.type === 'detalleCompra'" class="modal-overlay" @click.self="close">
      <div class="modal-window">
        <h3>Detalle de Compra</h3>
        <form class="modal-form grid-two" @submit.prevent="saveDetalleCompra">
          <label>Compra ID
            <input v-model="detalleCompraForm.compra_id" />
          </label>
          <label>Nombre del Producto
            <input v-model="detalleCompraForm.nombre_producto" />
          </label>
          <label>Cantidad
            <input type="number" v-model="detalleCompraForm.cantidad" />
          </label>
          <label>Precio Unitario
            <input type="number" v-model="detalleCompraForm.precio_unitario" />
          </label>
          <label>Subtotal
            <input type="number" v-model="detalleCompraForm.subtotal" />
          </label>
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
  padding:.6rem 1rem;
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

.section-container {
  display: flex;
  justify-content: space-between;
  padding: 2rem;
}

.update-section, .report-section {
  width: 48%;
  padding: 2rem;
  background-color: #1e293b;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

.update-section {
  background-color: #101222;
}

.report-section {
  background-color: #101222;
}

.table-wrapper {
  max-height:60vh;
  overflow:auto;
  padding: 1rem;
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
  gap: .8rem;
}

.grid-two {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: .8rem;
}

.modal-form label {
  display: flex;
  flex-direction: column;
  font-size: .9rem;
  gap: .25rem;
}

.modal-form input,
.modal-form select {
  padding: .45rem .6rem;
  border: none;
  border-radius: 6px;
  background: #111827;
  color: #fff;
}

.save-big {
  grid-column: 1 / -1;
  padding: .6rem 1rem;
  border: none;
  border-radius: 8px;
  background: #2563eb;
  font-weight: 600;
  cursor: pointer;
}

.cancel-btn {
  align-self: center;
  padding: .4rem 1.4rem;
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
