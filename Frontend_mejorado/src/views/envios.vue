<template>
  <div class="page">
    <NavBar title="PEDIDOS">
      <template #actions>
        <input v-model="tablaQuery" class="input input--white" placeholder="Buscar pedidos…" />
      </template>
    </NavBar>

    <div class="container">
      <section class="module">
        <h2 class="section-title">Historial de pedidos</h2>

        <!-- Tabla principal (limitada a 6) -->
        <TablaBase
          class="table--center"
          :columns="columns"
          :rows="filasMostradas"
          row-key="key"
          :actions="{ edit:true, delete:true }"
          :searchable="true"
          v-model:search="tablaQuery"
          :useLocalFilter="false"
          :showAddButton="false"
          addLabel="Agregar pedido"
          :show-see-all="false"
          :auto-limit="6"
          @add="abrirFormulario('agregar')"
          @edit="(row)=>abrirFormulario('editar', row)"
          @delete="(row)=>abrirFormulario('eliminar', row)"
        />

        <!-- Pie con los botones (a la derecha) -->
        <div class="footer-actions">
          <button class="btn" @click="abrirFormulario('agregar')">Agregar pedido</button>
          <button class="btn btn--muted" @click="abrirVerTodos">Ver Todos</button>
        </div>
      </section>
    </div>

    <!-- Modal CRUD -->
    <div v-if="formVisible" class="modal-overlay" @click.self="cerrarFormulario">
      <div class="modal-window" :class="{'modal--wide': accion!=='eliminar'}">
        <h3 v-if="accion==='agregar'">Agregar nueva orden</h3>
        <h3 v-else-if="accion==='editar'">Editar orden #{{ formData.id }}</h3>
        <h3 v-else>Eliminar orden #{{ formData.id }}</h3>

        <!-- AGREGAR / EDITAR -->
        <form v-if="accion!=='eliminar'" class="form-vertical" @submit.prevent="submitFormulario">
          <div class="form-field">
            <label>Cliente</label>
            <div class="select-wrap">
              <select v-model.number="formData.cliente" class="select--dark" required>
                <option :value="''" disabled>Selecciona un cliente</option>
                <option v-for="c in clientes" :key="c.id" :value="c.id">{{ c.nombre }}</option>
              </select>
            </div>
          </div>

          <div class="form-field">
            <label>Fecha</label>
            <input type="date" v-model="formData.fecha" class="input--dark" />
          </div>

          <div class="form-field">
            <label>Método de pago</label>
            <div class="select-wrap">
              <select v-model="formData.metodo_pago" class="select--dark" required>
                <option value="efectivo">Efectivo</option>
                <option value="transferencia">Transferencia</option>
                <option value="tarjeta">Tarjeta</option>
                <option value="otro">Otro</option>
              </select>
            </div>
          </div>

          <h4 class="detalle-title">Detalles de la orden</h4>

          <!-- Encabezados de detalles -->
          <div class="detalle-grid-doble detalle-header">
            <span>ID</span>
            <span>Producto</span>
            <span>Cantidad</span>
            <span>Precio unitario</span>
            <span>Total</span>
            <span></span>
          </div>

          <!-- Filas de detalle -->
          <div v-for="(d, i) in formData.detalles" :key="i" class="detalle-grid-doble">
            <!-- Campo ID -->
            <div class="select-wrap">
              <input
                type="number"
                min="1"
                v-model.number="d.producto"
                class="input--dark"
                placeholder="ID"
                @input="onIdChange(i)"
              />
            </div>

            <!-- Campo Producto (Select con búsqueda) -->
            <div class="select-wrap">
              <select 
                v-model.number="d.producto" 
                class="select--dark"
                @change="onProductoSelectChange(i)"
              >
                <option :value="null" disabled>Selecciona un producto</option>
              <option v-for="u in uniformesFiltrados(d.searchQuery)" :key="u.id" :value="u.id">
              {{ u.tipo }} - Stock: {{ u.stock }}
              </option>  
              </select>
            </div>

            <input type="number" min="1" v-model.number="d.cantidad" class="input--dark" @input="recalcularTotales" />
            <input type="number" step="0.01" min="0" v-model.number="d.precio_unitario" class="input--dark" @input="recalcularTotales" />

            <div class="cell-total">Q{{ toMoney((d.cantidad || 0) * (d.precio_unitario || 0)) }}</div>

            <button type="button" class="mini-btn danger" @click="quitarDetalle(i)">Quitar</button>
          </div>

          <button type="button" class="mini-btn" @click="agregarDetalle">+ Agregar línea</button>

          <div class="totales">
            <div class="total-row"><span>Subtotal:</span><strong>Q{{ toMoney(subtotal) }}</strong></div>
            <div class="total-row total-final"><span>Total:</span><strong>Q{{ toMoney(formData.precio_total) }}</strong></div>
          </div>

          <div class="modal-actions">
            <button type="submit" class="btn"> {{ accion==='agregar' ? 'Guardar' : 'Actualizar' }} </button>
            <button type="button" class="btn secondary" @click="cerrarFormulario">Cancelar</button>
          </div>
        </form>

        <!-- ELIMINAR -->
        <div v-else class="form-vertical">
          <p>¿Seguro que deseas eliminar la orden <strong>#{{ formData.id }}</strong>?</p>
          <div class="modal-actions">
            <button class="btn btn--danger" @click="submitFormulario">Eliminar</button>
            <button class="btn secondary" @click="cerrarFormulario">Cancelar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal VER TODOS (lista completa) -->
    <div v-if="verTodosVisible" class="modal-overlay" @click.self="cerrarVerTodos">
      <div class="modal-window modal--wide">
        <button class="close-btn-top" @click="cerrarVerTodos">✕</button>
        <h3>Pedidos - Lista Completa</h3>
        <div class="table-wrapper">
          <table class="table dark-table table--center">
            <thead>
              <tr>
                <th v-for="c in columns" :key="c.key">{{ c.label }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="r in filasFiltradas" :key="r.key">
                <td>{{ r.cliente_nombre }}</td>
                <td>{{ r.fecha_fmt }}</td>
                <td>{{ r.metodo_pago }}</td>
                <td>{{ r.producto }}</td>
                <td style="text-align:right;">{{ r.precio_unitario_fmt }}</td>
                <td style="text-align:right;">{{ r.subtotal_fmt }}</td>
                <td style="text-align:right;">{{ r.total_fmt }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="modal-actions">
          <button class="btn secondary" @click="cerrarVerTodos">Cerrar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import TablaBase from '@/components/Reutilizacion/Tablas.vue'

// Clientes
const CLIENTES_A = `/api/clientes/`
const CLIENTES_B = `/api/clientes/`

// Ventas 
const ORDENES_LIST = `/api/ventas/crear/`
const ORDEN_EDITAR = id => `/api/ventas/editar/${id}/`
const ORDEN_ELIMINAR = id => `/api/ventas/eliminar/${id}/`
const ORDEN_RECIBO = id => `/api/ventas/${id}/recibo/`
const ORDENES_HIST = `/api/ventas/detalles/`

// Inventario 
const UNIFORME_SHOW = id => `/api/uniformes/${id}/`
const UNIFORME_LIST = `/api/uniformes/`

export default {
  components: { NavBar, TablaBase },
  setup() {
    const router = useRouter()
    const goHome = () => router.push({ name: 'home' })
    return { goHome }
  },
  data() {
    return {
      tablaQuery: '',
      verTodosVisible: false,
      cargando: false,
      columns: [
        { key: 'cliente_nombre', label: 'Cliente' },
        { key: 'fecha_fmt', label: 'Fecha' },
        { key: 'metodo_pago', label: 'Método de pago' },
        { key: 'producto', label: 'Producto' },
        { key: 'precio_unitario_fmt', label: 'Precio unitario', align: 'right' },
        { key: 'subtotal_fmt', label: 'Subtotal', align: 'right' },
        { key: 'total_fmt', label: 'Total', align: 'right' }
      ],
      filas: [],
      formVisible: false,
      accion: 'agregar',
      formData: {
        id: null,
        cliente: '',
        fecha: '',
        metodo_pago: 'efectivo',
        detalles: [],
        precio_total: 0
      },
      clientes: [],
      clientesMap: {},
      uniformesCache: {},
      todosUniformes: []
    }
  },
  computed: {
    filasFiltradas() {
      const q = this.tablaQuery.trim().toLowerCase()
      if (!q) return this.filas
      return this.filas.filter(r =>
        [r.cliente_nombre, r.fecha_fmt, r.metodo_pago, r.producto,
        r.precio_unitario_fmt, r.subtotal_fmt, r.total_fmt]
          .some(v => (v || '').toString().toLowerCase().includes(q))
      )
    },
    filasMostradas() { return this.filasFiltradas },
    subtotal() {
      return (this.formData.detalles || []).reduce(
        (acc, d) => acc + (Number(d.cantidad) || 0) * (Number(d.precio_unitario) || 0), 0
      )
    }
  },
  watch: { subtotal(v) { this.formData.precio_total = v } },
  async mounted() {
    await this.cargarClientes()
    await this.cargarTodosUniformes()
    await this.cargarFilas()
  },
  methods: {
    toMoney(n) { const v = Number(n || 0); return v.toLocaleString('es-MX', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) },
    formatFecha(iso) { if (!iso) return ''; const d = new Date(iso); return d.toLocaleDateString('es-MX', { year: 'numeric', month: 'short', day: '2-digit' }) },

    getCSRF() {
      const name = 'csrftoken'; const cookies = document.cookie?.split(';') || []
      for (const c of cookies) { const t = c.trim(); if (t.startsWith(name + '=')) return decodeURIComponent(t.slice(name.length + 1)) }
      return null
    },
    
    async req(url, method = 'GET', data) {
      const opts = { method, credentials: 'include', headers: {} }
      if (method !== 'GET' && method !== 'HEAD') {
        opts.headers['Content-Type'] = 'application/json'
        const csrf = this.getCSRF()
        if (csrf) opts.headers['X-CSRFToken'] = csrf
        if (data !== undefined) opts.body = JSON.stringify(data)
      }
      
      const r = await fetch(url, opts)
      
      // Manejo especial para DELETE (puede retornar 204 o 500 pero funciona)
      if (method === 'DELETE' && (r.status === 204 || r.status === 500)) {
        return null
      }
      
      if (!r.ok) {
        const txt = await r.text().catch(() => '')
        throw new Error(`${r.status} ${r.statusText} - ${txt}`)
      }
      
      const ct = r.headers.get('content-type') || ''
      return ct.includes('application/json') ? r.json() : null
    },
    
    async safeGet(url) { try { return await this.req(url, 'GET') } catch (_) { return null } },

    mpKey(id) { return `mp_orden_${id}` },
    leerMetodoPago(id) { return localStorage.getItem(this.mpKey(id)) || 'efectivo' },
    guardarMetodoPago(id, metodo) { localStorage.setItem(this.mpKey(id), metodo || 'efectivo') },
    borrarMetodoPago(id) { localStorage.removeItem(this.mpKey(id)) },

    async cargarClientes() {
      let data = await this.safeGet(CLIENTES_A)
      if (!data) data = await this.safeGet(CLIENTES_B)
      this.clientes = Array.isArray(data) ? data : (data?.results || [])
      this.clientesMap = Object.fromEntries((this.clientes || []).map(c => [c.id, c.nombre]))
    },

    async cargarTodosUniformes() {
      try {
        const data = await this.req(UNIFORME_LIST, 'GET')
        this.todosUniformes = Array.isArray(data) ? data : (data?.results || [])
      } catch (e) {
        console.warn('No se pudieron cargar los uniformes', e)
        this.todosUniformes = []
      }
    },

    uniformesFiltrados(query) {
      return this.todosUniformes
    },

    onIdChange(index) {
      const d = this.formData.detalles[index]
      const id = d.producto
      
      if (!id) {
        d.nombre = null
        return
      }

      const uniforme = this.todosUniformes.find(u => u.id === id)
      if (uniforme) {
        d.nombre = `${uniforme.tipo} - ${uniforme.talla} - ${uniforme.color}`
        this.uniformesCache[id] = { nombre: d.nombre }
      } else {
        d.nombre = null
      }
      
      this.recalcularTotales()
    },

    onProductoSelectChange(index) {
      const d = this.formData.detalles[index]
      const id = d.producto
      
      if (!id) return

      const uniforme = this.todosUniformes.find(u => u.id === id)
      if (uniforme) {
        d.nombre = `${uniforme.tipo} - ${uniforme.talla} - ${uniforme.color}`
        this.uniformesCache[id] = { nombre: d.nombre }
      }
      
      this.recalcularTotales()
    },

    async cargarFilas() {
      this.cargando = true
      const rows = []
      let k = 1

      const hist = await this.safeGet(ORDENES_HIST)
      const list = Array.isArray(hist) ? hist : (hist?.results || [])

      for (const o of list) {
        const mp = this.leerMetodoPago(o.id)
        const detalles = Array.isArray(o.detalles) ? o.detalles : []

        const clienteNombre =
          typeof o.cliente === 'number'
            ? this.clientesMap[o.cliente] || `Cliente #${o.cliente}`
            : o.cliente || '—'

        for (const d of detalles) {
          let productoNombre = '—'
          if (typeof d.producto === 'object' && d.producto !== null) {
            productoNombre = d.producto.nombre || d.producto.tipo || `Uniforme #${d.producto.id || ''}`
          } else {
            productoNombre = d.producto || '—'
          }

          const pu = Number(d.precio_unitario ?? d.precio ?? 0)
          const sub = Number((Number(d.cantidad || 0) * pu) - Number(d.descuento || 0))

          const row = {
            key: `orden-${o.id}-${d.id || k++}`,
            id: o.id,
            cliente_nombre: clienteNombre,
            fecha: o.fecha,
            metodo_pago: mp,
            producto: productoNombre,
            precio_unitario: pu,
            subtotal: sub,
            total: Number(o.total || 0)
          }

          row.fecha_fmt = this.formatFecha(row.fecha)
          row.precio_unitario_fmt = `Q${this.toMoney(row.precio_unitario)}`
          row.subtotal_fmt = `Q${this.toMoney(row.subtotal)}`
          row.total_fmt = `Q${this.toMoney(row.total)}`
          rows.push(row)
        }
      }

      this.filas = rows.sort((a, b) => (new Date(b.fecha || 0)) - (new Date(a.fecha || 0)))
      this.cargando = false
    },

    abrirFormulario(accion, row = null) {
      this.accion = accion
      this.formVisible = true

      if (accion === 'agregar') {
        this.formData = {
          id: null,
          cliente: '',
          fecha: new Date().toISOString().slice(0, 10),
          metodo_pago: 'efectivo',
          detalles: [{ 
            producto: null, 
            nombre: null, 
            cantidad: 1, 
            precio_unitario: 0,
            searchQuery: ''
          }],
          precio_total: 0
        }
        return
      }

      if (!row) return

      if (accion === 'editar') {
        this.formData = {
          id: row.id,
          cliente: 0,
          fecha: (row.fecha || '').slice(0, 10),
          metodo_pago: this.leerMetodoPago(row.id),
          detalles: [],
          precio_total: Number(row.total || 0)
        }
        this.cargarOrden(row.id)
      }

      if (accion === 'eliminar') {
        this.formData = { id: row.id }
      }
    },
    cerrarFormulario() { this.formVisible = false },

    async cargarOrden(id) {
      try {
        const data = await this.req(ORDEN_RECIBO(id), 'GET')
        const dets = Array.isArray(data.detalles) ? data.detalles : []
        
        this.formData.detalles = dets.map(d => {
          let productoId = null
          let productoNombre = null
          
          if (typeof d.producto === 'object' && d.producto !== null) {
            productoId = d.producto.id
            productoNombre = d.producto.tipo || d.producto.nombre || `Uniforme #${d.producto.id}`
          } else if (typeof d.producto === 'number') {
            productoId = d.producto
            productoNombre = `Uniforme #${d.producto}`
          }
          
          return {
            id: d.id,
            producto: productoId,
            nombre: productoNombre,
            cantidad: Number(d.cantidad || 1),
            precio_unitario: Number(d.precio_unitario || d.precio || 0),
            searchQuery: ''
          }
        })
        
        this.formData.cliente = data.cliente?.id || data.cliente || ''
        this.recalcularTotales()
      } catch (e) {
        console.warn('No se pudo cargar la orden', e)
        this.formData.detalles = [{ 
          producto: null, 
          nombre: null, 
          cantidad: 1, 
          precio_unitario: 0,
          searchQuery: ''
        }]
      }
    },

    agregarDetalle() {
      if (!Array.isArray(this.formData.detalles)) this.formData.detalles = []
      this.formData.detalles.push({ 
        producto: null, 
        nombre: null, 
        cantidad: 1, 
        precio_unitario: 0,
        searchQuery: ''
      })
    },
    quitarDetalle(i) {
      if (Array.isArray(this.formData.detalles)) this.formData.detalles.splice(i, 1)
      this.recalcularTotales()
    },
    recalcularTotales() { this.formData.detalles = [...this.formData.detalles] },

    abrirVerTodos() { this.verTodosVisible = true },
    cerrarVerTodos() { this.verTodosVisible = false },

    async submitFormulario() {
      try {
        if (this.accion === 'eliminar') {
          if (!this.formData.id) { alert('Sin ID'); return }
          await this.req(ORDEN_ELIMINAR(this.formData.id), 'DELETE')
          this.borrarMetodoPago(this.formData.id)
          this.formVisible = false
          await this.cargarFilas()
          return
        }

        if (!this.formData.cliente) {
          alert('Selecciona un cliente')
          return
        }

        const detalles = (this.formData.detalles || []).filter(
          d => d.producto && d.cantidad > 0
        )
        
        if (detalles.length === 0) {
          alert('Agrega al menos un detalle con un uniforme válido.')
          return
        }

        const payload = {
          cliente: this.formData.cliente,
          fecha: this.formData.fecha,
          metodo_pago: this.formData.metodo_pago,
          estado: 'completada',
          detalles: detalles.map(d => {
            const detalle = {
              producto: Number(d.producto),
              cantidad: Number(d.cantidad),
              precio_unitario: Number((+d.precio_unitario || 0).toFixed(2))
            }
            
            if (this.accion === 'editar' && d.id) {
              detalle.id = d.id
            }
            
            return detalle
          })
        }

        if (this.accion === 'editar' && this.formData.id) {
          await this.req(ORDEN_EDITAR(this.formData.id), 'PUT', payload)
          this.guardarMetodoPago(this.formData.id, this.formData.metodo_pago)
        } else {
          const created = await this.req(ORDENES_LIST, 'POST', payload)
          if (created?.id)
            this.guardarMetodoPago(created.id, this.formData.metodo_pago)
        }

        this.formVisible = false
        await this.cargarFilas()
      } catch (e) {
        console.error('Error:', e)
        alert('Ocurrió un error. Por favor verifica los datos e intenta nuevamente.')
      }
    }
  }
}
</script>

<style scoped>
.page{ min-height:100vh; background:var(--color-octonary); color:#fff; }
.container{ padding: 24px; }
.module{ background:#0d1130; border:2px solid #1e2236; border-radius:16px; padding:16px; }
.section-title{ color:#fff; margin:0 0 12px 0; }

.detalle-title{ margin-top:18px; font-weight:700; }

.detalle-grid-doble{ 
  display:grid; 
  grid-template-columns: 80px 2fr 1fr 1fr 1fr auto; 
  align-items:center; 
  gap:10px; 
  margin-top:10px; 
}

.detalle-header{ font-weight:700; background:var(--color-senary); color:#fff; padding:8px 6px; border-radius:6px; }
.detalle-header span{ text-align:center; }
.detalle-nombre{ color:#10b981; display:block; margin-top:4px; font-weight:500; }
.cell-total{ text-align:right; padding-right:8px; }

.totales{ margin-top:14px; display:flex; flex-direction:column; gap:6px; align-items:flex-end; }
.total-row{ display:flex; gap:16px; align-items:center; }
.total-final{ font-size:18px; }

.modal-window{ background:#1e293b; color:#fff; padding:20px; border-radius:14px; min-width:560px; max-width:90%; max-height:90vh; overflow:auto; position:relative; }
.modal--wide{ min-width:860px; }
.modal-actions{ display:flex; justify-content:flex-end; gap:10px; margin-top:12px; }
.close-btn-top{ position:absolute; top:10px; right:15px; background:transparent; border:none; font-size:22px; cursor:pointer; font-weight:bold; color:#fff; }
.table-wrapper{ max-height:70vh; overflow:auto; }

.footer-actions{ display:flex; justify-content:flex-end; gap:10px; margin-top:10px; }
</style>