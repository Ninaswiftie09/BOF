<template>
  <div class="inventory-container">
    <!-- Top Bar -->
    <header class="top-bar">
      <img src="@/assets/logo_bof_blanco.png" alt="Logo del cliente" class="logo" @click="goHome" />
      <h1>PEDIDOS</h1>
    </header>

    <!-- Tabla principal -->
    <section class="inventory-section">
      <h2>Historial de pedidos</h2>

      <!-- Buscador arriba -->
      <div class="table-toolbar">
        <input
          v-model="tablaQuery"
          class="top-search"
          placeholder="Buscar por id, cliente, fecha o total…"
        />
      </div>

      <table>
        <thead>
          <tr>
            <th v-for="h in headers" :key="h">{{ h }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in pedidosMostrados" :key="p.id">
            <td>{{ p.id }}</td>
            <td>{{ p.cliente_nombre }}</td>
            <td>{{ formatFecha(p.fecha) }}</td>
            <td>{{ p.metodo_pago || '—' }}</td>
            <td>{{ p.estado || '—' }}</td>
            <td>Q{{ toMoney(p.total) }}</td>
            <td>
              <div class="flex-gap">
                <button class="mini-btn sky" @click="abrirFormulario('editar', p)">Editar</button>
                <button class="mini-btn danger" @click="abrirFormulario('eliminar', p)">Eliminar</button>
              </div>
            </td>
          </tr>
          <tr v-if="!cargando && !pedidos.length">
            <td colspan="7" style="text-align:center; padding:16px; color:#6b7280">Sin pedidos aún</td>
          </tr>
          <tr v-if="cargando">
            <td colspan="7" style="text-align:center; padding:16px; color:#6b7280">Cargando…</td>
          </tr>
        </tbody>
      </table>

      <!-- Botones inferiores -->
      <div class="button-row">
        <button @click="abrirFormulario('agregar')">Agregar pedido</button>
        <button @click="toggleVerTodos">{{ verTodos ? 'Ocultar' : 'Ver Todos' }}</button>
      </div>
    </section>

    <!-- Modal Agregar / Editar / Eliminar -->
    <div v-if="formVisible" class="modal-overlay">
      <div class="modal-content large-modal">
        <h3 v-if="accion==='agregar'">Agregar nuevo pedido</h3>
        <h3 v-else-if="accion==='editar'">Editar pedido #{{ formData.id }}</h3>
        <h3 v-else>Eliminar pedido #{{ formData.id }}</h3>

        <form v-if="accion!=='eliminar'" class="form-vertical" @submit.prevent="submitFormulario">
          <label>Cliente</label>
          <select v-model.number="formData.cliente" required>
            <option :value="''" disabled>Selecciona un cliente</option>
            <option v-for="c in clientes" :key="c.id" :value="c.id">{{ c.nombre }}</option>
          </select>

          <label>Fecha</label>
          <input type="date" v-model="formData.fecha" />

          <label>Método de pago</label>
          <select v-model="formData.metodo_pago" required>
            <option value="efectivo">Efectivo</option>
            <option value="transferencia">Transferencia</option>
            <option value="tarjeta">Tarjeta</option>
            <option value="otro">Otro</option>
          </select>

          <label>Estado</label>
          <select v-model="formData.estado" required>
            <option value="pendiente">Pendiente</option>
            <option value="completada">Completada</option>
            <option value="anulada">Anulada</option>
          </select>

          <!-- Detalles -->
          <h4 style="margin-top:18px">Detalles del pedido</h4>
          <div class="detalle-grid detalle-header">
            <span>Producto (ID)</span>
            <span>Cantidad</span>
            <span>Precio unitario</span>
            <span>Total</span>
            <span></span>
          </div>

          <div v-for="(d, i) in formData.detalles" :key="i" class="detalle-grid">
            <input
              type="number"
              min="1"
              v-model.number="d.producto"
              placeholder="ID de producto"
              @change="onProductoChange(i)"
            />
            <input type="number" min="1" v-model.number="d.cantidad" @input="recalcularTotales" />
            <input type="number" step="0.01" min="0" v-model.number="d.precio_unitario" @input="recalcularTotales" />
            <div class="cell-total">
              ${{ toMoney((d.cantidad || 0) * (d.precio_unitario || 0)) }}
            </div>
            <button type="button" class="mini-btn danger" @click="quitarDetalle(i)">Quitar</button>
          </div>

          <button type="button" class="mini-btn" @click="agregarDetalle">+ Agregar línea</button>

          <div class="totales">
            <div class="total-row"><span>Subtotal:</span><strong>${{ toMoney(subtotal) }}</strong></div>
            <div class="total-row total-final"><span>Total:</span><strong>${{ toMoney(formData.precio_total) }}</strong></div>
          </div>

          <div class="buttons-row">
            <button type="submit" class="btn-primary">{{ accion==='agregar' ? 'Guardar' : 'Actualizar' }}</button>
            <button type="button" class="btn-cancel" @click="cerrarFormulario">Cancelar</button>
          </div>
        </form>

        <div v-else class="form-vertical">
          <p>¿Seguro que deseas eliminar el pedido <strong>#{{ formData.id }}</strong>?</p>
          <div class="buttons-row">
            <button class="btn-primary" @click="submitFormulario">Eliminar</button>
            <button class="btn-cancel" @click="cerrarFormulario">Cancelar</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import { BASE_URL } from '@/config'
import { useRouter } from 'vue-router'

// 👉 Cambia esto si tu lookup de producto NO es /api/productos/:id/
const PRODUCTS_ENDPOINT = `${BASE_URL}/api/productos/` // termina en '/'

export default {
  setup(){
    const router = useRouter()
    const goHome = () => router.push({ name:'home' })
    return { goHome }
  },
  data(){
    return {
      headers: ['id','Cliente','Fecha','Método','Estado','Total','Acciones'],
      pedidos: [],
      verTodos: false,
      cargando: false,

      // buscador
      tablaQuery: '',

      // modal principal
      formVisible: false,
      accion: 'agregar', // agregar | editar | eliminar
      formData: {
        id: null,
        cliente: '',          // cliente_id
        fecha: '',
        metodo_pago: 'efectivo',
        estado: 'pendiente',
        detalles: [],         // { producto, cantidad, precio_unitario }
        precio_total: 0       // mostrado; backend calcula 'total' real
      },

      clientes: [],
      // cache simple de productos {id: {precio_unitario: ...}}
      productosCache: {}
    }
  },
  computed: {
    // filtro por id, cliente, fecha formateada y total
    pedidosFiltradosTabla(){
      const q = this.tablaQuery.trim().toLowerCase()
      if(!q) return this.pedidos
      return this.pedidos.filter(p => {
        const id = String(p.id)
        const cliente = (p.cliente_nombre || '').toLowerCase()
        const fechaStr = this.formatFecha(p.fecha).toLowerCase()
        const totalStr = this.toMoney(p.total).toLowerCase()
        return id.includes(q) || cliente.includes(q) || fechaStr.includes(q) || totalStr.includes(q)
      })
    },
    pedidosMostrados(){
      const base = this.pedidosFiltradosTabla
      return this.verTodos ? base : base.slice(0,6)
    },
    subtotal(){
      return this.formData.detalles.reduce(
        (acc, d)=> acc + (Number(d.cantidad)||0) * (Number(d.precio_unitario)||0), 0
      )
    }
  },
  watch: {
    subtotal(val){ this.formData.precio_total = val }
  },
  mounted(){
    this.cargarPedidos()
    this.cargarClientes()
  },
  methods: {
    // utilidades
    toMoney(n){
      const v = Number(n||0)
      return v.toLocaleString('es-MX', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    },
    formatFecha(iso){
      if(!iso) return ''
      const d = new Date(iso)
      return d.toLocaleDateString('es-MX', { year:'numeric', month:'short', day:'2-digit' })
    },
    getCookie(name){
      let cookieValue = null
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';')
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim()
          if (cookie.startsWith(name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
            break
          }
        }
      }
      return cookieValue
    },

    // UI
    toggleVerTodos(){ this.verTodos = !this.verTodos },
    abrirFormulario(accion, pedido=null){
      this.accion = accion
      this.formVisible = true
      if(accion==='agregar'){
        this.formData = {
          id: null,
          cliente: '',
          fecha: new Date().toISOString().slice(0,10),
          metodo_pago: 'efectivo',
          estado: 'pendiente',
          detalles: [{ producto: null, cantidad: 1, precio_unitario: 0 }],
          precio_total: 0
        }
      } else if(accion==='editar' && pedido){
        // Precargar desde la fila (no tenemos GET detalle estándar)
        this.formData = {
          id: pedido.id,
          cliente: pedido.cliente_id || '',
          fecha: (pedido.fecha || '').slice(0,10),
          metodo_pago: pedido.metodo_pago || 'efectivo',
          estado: pedido.estado || 'pendiente',
          detalles: [], // sin endpoint detalle, el usuario vuelve a ingresar líneas
          precio_total: pedido.total || 0
        }
      } else if(accion==='eliminar' && pedido){
        this.formData = { id: pedido.id }
      }
    },
    cerrarFormulario(){ this.formVisible = false },

    agregarDetalle(){
      if(!Array.isArray(this.formData.detalles)) this.formData.detalles = []
      this.formData.detalles.push({ producto:null, cantidad:1, precio_unitario:0 })
    },
    quitarDetalle(i){
      if(Array.isArray(this.formData.detalles)) this.formData.detalles.splice(i,1)
      this.recalcularTotales()
    },
    recalcularTotales(){
      // dispara el watcher de subtotal al mutar el array
      this.formData.detalles = [...this.formData.detalles]
    },

    async onProductoChange(index){
      const d = this.formData.detalles[index]
      if(!d || !d.producto) return
      try{
        // cache
        if(this.productosCache[d.producto]){
          d.precio_unitario = Number(this.productosCache[d.producto].precio_unitario) || 0
          this.recalcularTotales()
          return
        }
        // 👉 Ajusta si tu endpoint de productos es otro:
        const r = await fetch(`${PRODUCTS_ENDPOINT}${d.producto}/`)
        if(!r.ok) throw new Error('Producto no encontrado')
        const prod = await r.json()
        // intenta varias claves comunes
        const precio = Number(
          prod.precio_unitario ?? prod.precio ?? prod.costo ?? prod.price ?? 0
        )
        this.productosCache[d.producto] = { precio_unitario: precio }
        d.precio_unitario = precio || 0
        this.recalcularTotales()
      }catch(e){
        console.warn('No se pudo obtener precio del producto', d.producto, e)
      }
    },

    // API
    async cargarClientes(){
      try{
        const r = await fetch(`${BASE_URL}/api/clientes/`)
        this.clientes = await r.json()
      }catch(e){ console.error('Error clientes', e) }
    },
    async cargarPedidos(){
      this.cargando = true
      this.pedidos = []
      // Intentamos varias fuentes de lista
      const fuentes = [
        `${BASE_URL}/api/ventas/`,
        `${BASE_URL}/api/ordenes/historial/`,
        `${BASE_URL}/api/ventas/detalles/`,
      ]
      for (const url of fuentes){
        try{
          const r = await fetch(url)
          if(!r.ok) continue
          const data = await r.json()
          const arr = Array.isArray(data) ? data : (Array.isArray(data.results) ? data.results : [])
          if(!arr.length) continue
          this.pedidos = arr.map(p => ({
            id: p.id ?? p.pedido_id ?? p.venta_id ?? p.pk,
            cliente_nombre: p.cliente_nombre ?? p.cliente?.nombre ?? '—',
            fecha: p.fecha ?? p.created_at ?? p.fecha_venta,
            metodo_pago: p.metodo_pago ?? p.payment_method ?? '—',
            estado: p.estado ?? p.status ?? '—',
            total: p.total ?? p.precio_total ?? p.monto_total ?? 0,
            cliente_id: p.cliente_id ?? p.cliente?.id
          })).filter(p => p.id != null)
          if(this.pedidos.length) break
        }catch(e){
          // prueba la siguiente fuente
        }
      }
      this.cargando = false
    },

    async submitFormulario(){
      try{
        const csrftoken = this.getCookie('csrftoken')
        const createUrl = `${BASE_URL}/api/ventas/crear/`
        const updateUrl = (id) => `${BASE_URL}/api/ventas/editar/${id}/`
        const deleteUrl = (id) => `${BASE_URL}/api/ventas/eliminar/${id}/`

        let url = createUrl
        let method = 'POST'
        let body = null

        if (this.accion === 'agregar' || this.accion === 'editar') {
          body = JSON.stringify({
            fecha: this.formData.fecha,
            cliente_id: this.formData.cliente,
            metodo_pago: this.formData.metodo_pago,
            estado: this.formData.estado,
            detalles: (this.formData.detalles || []).map(d => ({
              producto: d.producto,
              cantidad: d.cantidad,
              precio_unitario: Number(d.precio_unitario).toFixed(2)
            }))
          })
        }
        if (this.accion === 'editar') {
          url = updateUrl(this.formData.id)
          method = 'PUT'
        } else if (this.accion === 'eliminar') {
          url = deleteUrl(this.formData.id)
          method = 'DELETE'
        }

        const res = await fetch(url, {
          method,
          credentials: 'include',
          headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
          body: method === 'DELETE' ? null : body
        })

        if(!res.ok){
          const err = await res.json().catch(()=>({error:'Error desconocido'}))
          alert('Error: ' + (err.error || res.statusText))
          return
        }

        this.formVisible = false
        await this.cargarPedidos()
      } catch (e) {
        console.error(e)
        alert('Error en la conexión con el servidor')
      }
    }
  }
}
</script>

<style scoped>
.logo { width: 100px; height: auto; cursor: pointer; }
.inventory-container { padding: 40px; background-color: var(--color-octonary); min-height: 100vh; }
.top-bar { display:flex; align-items:center; justify-content:space-between; background:#1e293b; padding: .75rem 2rem; position:fixed; top:0; left:0; right:0; height:60px; z-index:1000; box-shadow: 0 2px 5px rgba(0,0,0,.1);} 
h1 { flex-grow: 1; text-align:center; color:#fff; font-size:1.8rem; font-weight:bold; margin:0; }
h2 { color: var(--colo-texto-blanco); margin-top: 80px; margin-bottom: 10px; }
.inventory-section { margin-top:10px; }

/* Buscador */
.table-toolbar { display:flex; justify-content:flex-end; margin:10px 0 14px; }
.top-search { width:320px; max-width:100%; padding:10px 12px; border-radius:10px; border:1px solid #cbd5e1; font-size:15px; }
.top-search:focus { outline:none; box-shadow:0 0 0 3px rgba(99,102,241,.25); border-color:#6366f1; }

/* Tabla */
table { width:100%; border-collapse:collapse; background:#fff; border-radius:12px; overflow:hidden; box-shadow:0 0 10px rgba(0,0,0,.05); margin-bottom:10px; }
th { background: var(--color-senary); color:#fff; font-weight:bold; padding:16px; font-size:18px; }
td { text-align:center; padding:12px; font-size:16px; color: var(--color-senary); }
tr:nth-child(even){ background:#f9f9f9; }

.button-row { display:flex; flex-wrap:wrap; gap:10px; margin: 10px 0 20px; }
.button-row button { background: var(--color-senary); color:#fff; padding:10px 14px; border:none; border-radius:8px; font-weight:bold; cursor:pointer; transition: background-color .3s; }
.button-row button:hover { background: var(--color-tertiary); }
.mini-btn { background: #334155; color:#fff; padding:6px 10px; border:none; border-radius:6px; font-size:12px; cursor:pointer; }
.mini-btn.sky { background:#0284c7; }
.mini-btn.danger { background:#e11d48; }
.flex-gap { display:flex; gap:8px; justify-content:center; }

/* Modales */
.modal-overlay { position:fixed; inset:0; background:rgba(0,0,0,.5); display:flex; align-items:center; justify-content:center; z-index:9999; }
.modal-content { background:#fff; padding:25px 30px; border-radius:12px; box-shadow:0 8px 20px rgba(0,0,0,.3); width:90%; max-width: 520px; max-height:90vh; overflow-y:auto; position:relative; }
.large-modal { max-width: 980px; }
.close-btn-top { position:absolute; top:10px; right:15px; background:transparent; border:none; font-size:22px; cursor:pointer; font-weight:bold; color:#333; }
.close-btn-top:hover { color:#b00020; }

.form-vertical label { font-weight:600; margin-top:12px; margin-bottom:5px; display:block; }
.form-vertical input, .form-vertical textarea, .form-vertical select { width:100%; padding:8px 10px; border-radius:6px; border:1px solid #ccc; font-size:15px; resize:vertical; }

.detalle-grid { display:grid; grid-template-columns: 3fr 1fr 1fr 1fr auto; align-items:center; gap:10px; margin-top:10px; }
.detalle-header { font-weight:700; color:#334155; }
.cell-total { text-align:right; padding-right:8px; }

.totales { margin-top: 16px; display:flex; flex-direction:column; gap:8px; align-items:flex-end; }
.total-row { display:flex; gap:16px; align-items:center; }
.total-final { font-size: 18px; }

.buttons-row { margin-top: 20px; display:flex; gap:15px; justify-content:flex-end; }
.btn-primary { background: var(--color-senary); color: var(--colo-texto-blanco); padding:10px 22px; border-radius:8px; border:none; font-weight:600; cursor:pointer; transition: background-color .3s; }
.btn-primary:hover { background: var(--color-tertiary); }
.btn-cancel { background:transparent; color:#555; padding:10px 22px; border-radius:8px; border:1px solid #aaa; cursor:pointer; font-weight:600; transition: background-color .3s; }
.btn-cancel:hover { background:#eee; }
</style>
