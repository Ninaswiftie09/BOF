<template>
  <div class="inventory-container">
    <!-- Header unificado (como en Clientes) -->
    <NavBar title="PEDIDOS">
      <template #actions>
        <input
          v-model="tablaQuery"
          class="nav-search"
          placeholder="Buscar pedidos…"
        />
      </template>
    </NavBar>

    <section class="module">
      <h2 class="module-title">Historial de pedidos</h2>

      <table>
        <thead>
          <tr>
            <th v-for="h in headers" :key="h">{{ h }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in filasMostradas" :key="row.key">
            <td>{{ row.cliente_nombre }}</td>
            <td>{{ formatFecha(row.fecha) }}</td>
            <td>{{ row.metodo_pago }}</td>
            <td>{{ row.producto }}</td>
            <td>Q{{ toMoney(row.precio_unitario) }}</td>
            <td>Q{{ toMoney(row.subtotal) }}</td>
            <td>Q{{ toMoney(row.total) }}</td>
            <td>
              <div class="flex-gap">
                <button class="mini-btn sky" @click="abrirFormulario('editar', row)">Editar</button>
                <button class="mini-btn danger" @click="abrirFormulario('eliminar', row)">Eliminar</button>
              </div>
            </td>
          </tr>

          <tr v-if="!cargando && !filas.length">
            <!-- color en template -->
            <td colspan="8" style="text-align:center; padding:16px; color:#6b7280">
              Sin pedidos aún
            </td>
          </tr>
          <tr v-if="cargando">
            <!-- color en template -->
            <td colspan="8" style="text-align:center; padding:16px; color:#6b7280">
              Cargando…
            </td>
          </tr>
        </tbody>
      </table>

      <div class="button-row">
        <button @click="abrirFormulario('agregar')">Agregar pedido</button>
        <button @click="toggleVerTodos">{{ verTodos ? 'Ocultar' : 'Ver Todos' }}</button>
      </div>
    </section>

    <!-- Modal -->
    <div v-if="formVisible" class="modal-overlay">
      <div class="modal-content large-modal">
        <h3 v-if="accion==='agregar'">Agregar nueva orden</h3>
        <h3 v-else-if="accion==='editar'">Editar orden #{{ formData.id }}</h3>
        <h3 v-else>Eliminar orden #{{ formData.id }}</h3>

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

          <h4 class="detalle-titulo">Detalles de la orden</h4>

          <!-- Encabezados de la “tabla” de detalles -->
          <div class="detalle-grid detalle-header">
            <span>Uniforme (ID)</span>
            <span>Cantidad</span>
            <span>Precio unitario</span>
            <span>Total</span>
            <span></span>
          </div>

          <!-- Filas editables -->
          <div v-for="(d, i) in formData.detalles" :key="i" class="detalle-grid">
            <div>
              <input
                type="number"
                min="1"
                v-model.number="d.producto"
                placeholder="ID de uniforme"
                @change="onUniformeChange(i)"
              />
              <small v-if="d.nombre" class="detalle-nombre">→ {{ d.nombre }}</small>
            </div>
            <input type="number" min="1" v-model.number="d.cantidad" @input="recalcularTotales" />
            <input type="number" step="0.01" min="0" v-model.number="d.precio_unitario" @input="recalcularTotales" />
            <div class="cell-total">Q{{ toMoney((d.cantidad || 0) * (d.precio_unitario || 0)) }}</div>
            <button type="button" class="mini-btn danger" @click="quitarDetalle(i)">Quitar</button>
          </div>

          <button type="button" class="mini-btn" @click="agregarDetalle">+ Agregar línea</button>

          <div class="totales">
            <div class="total-row"><span>Subtotal:</span><strong>Q{{ toMoney(subtotal) }}</strong></div>
            <div class="total-row total-final"><span>Total:</span><strong>Q{{ toMoney(formData.precio_total) }}</strong></div>
          </div>

          <div class="buttons-row">
            <button type="submit" class="btn-primary">{{ accion==='agregar' ? 'Guardar' : 'Actualizar' }}</button>
            <button type="button" class="btn-cancel" @click="cerrarFormulario">Cancelar</button>
          </div>
        </form>

        <div v-else class="form-vertical">
          <p>¿Seguro que deseas eliminar la orden <strong>#{{ formData.id }}</strong>?</p>
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
import { useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import { apiFetch } from '@/utils/api'

// --- Endpoints existentes ---
const CLIENTES_A    = `/api/cliente/clientes/`
const CLIENTES_B    = `/api/clientes/`
const ORDENES_HIST  = `/api/ordenes/historial/`
const ORDEN_ITEM    = id => `/api/ordenes/${id}/`
const ORDENES_LIST  = `/api/ordenes/`
const UNIFORME_SHOW = id => `/api/uniformes/${id}/`
const UNIFORME_LIST = `/api/uniformes/`

export default {
  components: { NavBar },
  setup(){
    const router = useRouter()
    const goHome = () => router.push({ name:'home' })
    return { goHome }
  },
  data(){
    return {
      headers: ['Cliente','Fecha','Método de pago','Producto','Precio unitario','Subtotal','Total','Acciones'],
      filas: [],
      verTodos: false,
      cargando: false,

      tablaQuery: '',

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
      uniformesCache: {}, // { [id]: { nombre: string } }
    }
  },
  computed: {
    filasFiltradas(){
      const q = this.tablaQuery.trim().toLowerCase()
      if(!q) return this.filas
      return this.filas.filter(r => {
        const cliente  = (r.cliente_nombre || '').toLowerCase()
        const fecha    = this.formatFecha(r.fecha).toLowerCase()
        const metodo   = (r.metodo_pago || '').toLowerCase()
        const producto = (r.producto || '').toLowerCase()
        const pu       = String(r.precio_unitario || '').toLowerCase()
        const sub      = String(r.subtotal || '').toLowerCase()
        const tot      = String(r.total || '').toLowerCase()
        return cliente.includes(q) || fecha.includes(q) || metodo.includes(q) ||
               producto.includes(q) || pu.includes(q) || sub.includes(q) || tot.includes(q)
      })
    },
    filasMostradas(){ return this.verTodos ? this.filasFiltradas : this.filasFiltradas.slice(0,10) },
    subtotal(){
      return this.formData.detalles.reduce(
        (acc, d)=> acc + (Number(d.cantidad)||0) * (Number(d.precio_unitario)||0), 0
      )
    }
  },
  watch:{ subtotal(v){ this.formData.precio_total = v } },
  async mounted(){
    await this.cargarClientes()
    await this.cargarFilas()
  },
  methods: {
    // ============== Utils ==============
    toMoney(n){ const v = Number(n||0); return v.toLocaleString('es-MX',{minimumFractionDigits:2,maximumFractionDigits:2}) },
    formatFecha(iso){ if(!iso) return ''; const d = new Date(iso); return d.toLocaleDateString('es-MX',{year:'numeric',month:'short',day:'2-digit'}) },
    toggleVerTodos(){ this.verTodos = !this.verTodos },

    // ⬇️ Unificamos sobre apiFetch (ya maneja CSRF + credentials + errores)
    async req(url, method='GET', data){
      return await apiFetch(url, method, data)
    },
    async safeGet(url){
      try { return await apiFetch(url, 'GET') } catch { return null }
    },

    // ============== Carga de datos ==============
    async cargarClientes(){
      let data = await this.safeGet(CLIENTES_A)
      if(!data) data = await this.safeGet(CLIENTES_B)
      this.clientes = Array.isArray(data) ? data : (data?.results || [])
      this.clientesMap = Object.fromEntries((this.clientes||[]).map(c => [c.id, c.nombre]))
    },

    async cargarFilas(){
      this.cargando = true
      const rows=[]
      let k=1
      const hist = await this.safeGet(ORDENES_HIST)
      const list = Array.isArray(hist) ? hist : (hist?.results || [])
      for(const o of list){
        const mp = this.leerMetodoPago(o.id)
        const detalles = Array.isArray(o.detalles) ? o.detalles : []
        for(const d of detalles){
          const pu = Number(d.precio || 0)
          const sub = Number((Number(d.cantidad||0) * pu) - Number(d.descuento || 0))
          rows.push({
            key: `orden-${o.id}-${d.id || k++}`,
            id: o.id,
            cliente_nombre: o.cliente || '—',
            fecha: o.fecha,
            metodo_pago: mp,
            producto: d.producto,
            precio_unitario: pu,
            subtotal: sub,
            total: Number(o.total || 0)
          })
        }
      }
      this.filas = rows.sort((a,b)=> (new Date(b.fecha||0))-(new Date(a.fecha||0)))
      this.cargando=false
    },

    // Método de pago “sidecar”
    mpKey(id){ return `mp_orden_${id}` },
    leerMetodoPago(id){ return localStorage.getItem(this.mpKey(id)) || 'efectivo' },
    guardarMetodoPago(id, metodo){ localStorage.setItem(this.mpKey(id), metodo || 'efectivo') },
    borrarMetodoPago(id){ localStorage.removeItem(this.mpKey(id)) },

    // ============== Modal ==============
    abrirFormulario(accion, row=null){
      this.accion = accion
      this.formVisible = true

      if(accion==='agregar'){
        this.formData = {
          id: null,
          cliente: '',
          fecha: new Date().toISOString().slice(0,10),
          metodo_pago: 'efectivo',
          detalles: [{ producto:null, nombre:null, cantidad:1, precio_unitario:0 }],
          precio_total: 0
        }
        return
      }

      if(!row) return

      if(accion==='editar'){
        this.formData = {
          id: row.id,
          cliente: 0,
          fecha: (row.fecha||'').slice(0,10),
          metodo_pago: this.leerMetodoPago(row.id),
          detalles: [],
          precio_total: Number(row.total || 0)
        }
        this.cargarOrden(row.id)
      }

      if(accion==='eliminar'){
        this.formData = { id: row.id }
      }
    },
    cerrarFormulario(){ this.formVisible=false },

    async cargarOrden(id){
      try{
        const data = await this.req(ORDEN_ITEM(id),'GET')
        const dets = Array.isArray(data.detalles) ? data.detalles : []
        this.formData.detalles = dets.map(d => ({
          producto: null,
          nombre: d.producto || null,
          cantidad: Number(d.cantidad || 1),
          precio_unitario: Number(d.precio || 0),
        }))
        this.recalcularTotales()
      }catch(e){
        console.warn('No se pudo cargar la orden', e)
        this.formData.detalles = [{ producto:null, nombre:null, cantidad:1, precio_unitario:0 }]
      }
    },

    agregarDetalle(){
      if(!Array.isArray(this.formData.detalles)) this.formData.detalles=[]
      this.formData.detalles.push({ producto:null, nombre:null, cantidad:1, precio_unitario:0 })
    },
    quitarDetalle(i){
      if(Array.isArray(this.formData.detalles)) this.formData.detalles.splice(i,1)
      this.recalcularTotales()
    },
    recalcularTotales(){ this.formData.detalles=[...this.formData.detalles] },

    // ======= Lookup SOLO UNIFORMES, mostrando SOLO el 'tipo' =======
    async onUniformeChange(index){
      const d = this.formData.detalles[index]
      if(!d || !d.producto) return

      if(this.uniformesCache[d.producto]){
        d.nombre = this.uniformesCache[d.producto].nombre
        this.recalcularTotales()
        return
      }

      let info = await this.fetchUniforme(d.producto) || await this.fetchUniformeDesdeLista(d.producto)
      const nombre = info?.nombre ?? `Uniforme #${d.producto}`
      this.uniformesCache[d.producto] = { nombre }
      d.nombre = nombre
      this.recalcularTotales()
    },
    async fetchUniforme(id){
      try{
        const u = await this.req(UNIFORME_SHOW(id),'GET')
        return { nombre: u?.tipo || `Uniforme #${id}` }
      }catch(_){ return null }
    },
    async fetchUniformeDesdeLista(id){
      try{
        const list = await this.req(UNIFORME_LIST,'GET')
        const arr = Array.isArray(list) ? list : (list?.results || [])
        const u = arr.find(x => String(x.id)===String(id))
        return u ? { nombre: u.tipo || `Uniforme #${id}` } : null
      }catch(_){ return null }
    },

    // ============== Guardar / Eliminar ==============
    async submitFormulario(){
      try{
        if(this.accion==='eliminar'){
          if(!this.formData.id){ alert('Sin ID'); return }
          await this.req(ORDEN_ITEM(this.formData.id),'DELETE')
          this.borrarMetodoPago(this.formData.id)
          this.formVisible=false
          await this.cargarFilas()
          return
        }

        // construir payload Orden (producto es TEXTO; usamos el 'nombre' detectado)
        const detalles = (this.formData.detalles||[]).filter(d => (d.nombre || d.producto) && d.cantidad>0)
        if(detalles.length===0){ alert('Agrega al menos un detalle.'); return }

        const clienteNombre = this.clientesMap[this.formData.cliente] || '—'
        const payload = {
          cliente: clienteNombre,
          fecha: this.formData.fecha,
          total: Number(this.subtotal.toFixed(2)),
          detalles: await Promise.all(detalles.map(async d => {
            let nombre = d.nombre
            if(!nombre && d.producto){
              const info = await this.fetchUniforme(d.producto) || await this.fetchUniformeDesdeLista(d.producto)
              nombre = info?.nombre || `Uniforme #${d.producto}`
            }
            return {
              producto: String(nombre || 'Uniforme'),
              talla: '-', color: '-', tela: '-', bordado: '-',
              cantidad: Number(d.cantidad),
              precio: Number((+d.precio_unitario || 0).toFixed(2)),
              descuento: 0
            }
          }))
        }

        if(this.accion==='editar' && this.formData.id){
          await this.req(ORDEN_ITEM(this.formData.id),'PUT', payload)
          this.guardarMetodoPago(this.formData.id, this.formData.metodo_pago)
        }else{
          const created = await this.req(ORDENES_LIST,'POST', payload)
          if(created?.id) this.guardarMetodoPago(created.id, this.formData.metodo_pago)
        }

        this.formVisible=false
        await this.cargarFilas()
      }catch(e){
        console.error('Error guardando/eliminando:', e)
        alert('No se pudo completar la acción. Revisa los datos e intenta de nuevo.')
      }
    }
  }
}
</script>

<style scoped>
.inventory-container{
  min-height: 100vh;
  background-color: var(--color-octonary); /*fondo pagina "pedidos" */
  display:flex; flex-direction:column;
  font-family: 'Segoe UI', sans-serif;
  color: var(--color-senary); /*texto formulario de agregar pedido: Q0.00 , subtotal: Q0.00, total: Q0.00 */
}

/* === Módulo === */
.module{
  background:#0d1130; /*fondo tarjeta "historial pedidos" */
  border:2px solid #1e2236; /*borde tarjeta "historial de pedidos" */
  border-radius:16px;
  padding:1.5rem;
  margin: 20px;
}
.module-title{
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color:#fff; /*titulo "historial de pedidos" */
  text-transform: uppercase;
}

/*no cambia nada si se elimina */
.nav-search{
  width: 320px; max-width: 40vw;
  padding: .5rem .75rem;
  border-radius: 10px;
  border: 1px solid #cbd5e1; /*nada*/
  background: #fff; /*nada*/
  color:#000; /*nada*/
  font-size: .95rem;
}
/*no cambia nada si se elimina */
.nav-search:focus{ outline:none;
  box-shadow:0 0 0 3px rgba(99,102,241,.25); /*nada*/
  border-color:#6366f1; /*nada*/
}

/* Tabla */
table{
  width:100%; border-collapse:collapse;
  background:#fff; /*color1 intercalado de filas de tablas*/
  border-radius:12px; overflow:hidden;
  box-shadow:0 0 10px rgba(0,0,0,.05); /*sombreado tabla "historial pedido" */
  margin-bottom:10px;
}
th{
  background: var(--color-senary); /*fondo encabezado de tabla*/
  color:#fff; /*texto encabezados tabla historial pedido*/
  font-weight:bold; padding:16px; font-size:16px;
}
td{
  text-align:center; padding:12px; font-size:15px;
  color: var(--color-senary); /*texto pedidos tabla*/
}
tr:nth-child(even){ background:#f9f9f9; } /*color2 intercalado de filas de tablas*/

/* Botonera inferior */
.button-row{ display:flex; flex-wrap:wrap; gap:10px; margin:10px 0 0; }
.button-row button{
  background: var(--color-senary); /*fondo botones "agregar pedido, ver todos/ocultar" */
  color:#fff; /*texto botones "agregar pedido, ver todos/ocultar"*/
  padding:10px 14px; border:none; border-radius:8px; font-weight:bold; cursor:pointer;
  transition: background-color .3s; /*asdf*/
}
.button-row button:hover{ background: var(--color-tertiary); } /*fondo botones "agregar pedido, ver todos/ocultar cursor arriba" */

/* Botones pequeños */
.mini-btn{
  background:#334155; /*fondo boton "+ agregar linea" */
  color:#fff; /*texto botones "editar, eliminar" en formulario "+ agregar linea, quitar" */
  padding:6px 10px; border:none; border-radius:6px; font-size:12px; cursor:pointer;
}
.mini-btn.sky{ background:#0284c7; } /*fondo boton accion "Editar"*/
.mini-btn.danger{ background:#e11d48; } /*fondo boton accion "eliminar" */
.flex-gap{ display:flex; gap:8px; justify-content:center; }

/* Modal */
.modal-overlay{
  position:fixed; inset:0;
  background:rgba(0,0,0,.5); /*fondo pantalla completa formulario "agregar nueva orden"*/
  display:flex; align-items:center; justify-content:center; z-index:9999;
}
.modal-content{
  background:#fff; /*fondo tarjeta formulario "agregar nueva orden" y fondo boton "cancelar"*/
  padding:25px 30px; border-radius:12px;
  box-shadow:0 8px 20px rgba(0,0,0,.3); /*sombreado tarjeta formulario "agregar nueva orden" */
  width:90%; max-width: 520px; max-height:90vh; overflow-y:auto; position:relative; }
.large-modal{ max-width: 980px; }

/* ===== Formularios dentro del modal ===== */
.form-vertical label{
  font-weight: 600;
  margin-top: 12px;
  margin-bottom: 5px;
  display: block;
  color: #1e293b; /*titulo campos "cliente, fecha, metodo de pago"*/
  font-size: 0.9rem;
}
.form-vertical input,
.form-vertical textarea,
.form-vertical select{
  width:100%;
  padding:8px 10px;
  border-radius:6px;
  border:1px solid #cbd5e1; /*borde input campos "cliente, fecha, metodo de pago"*/
  font-size:15px;
  background:#fff; /*fondo input campos "cliente, fecha, metodo de pago" */
  color:#0f172a; /*texto ingresado en input campos "cliente, fecha, metodo de pago" y en tabla "uniforme, cantidad, precio unitario"*/
}

.detalle-titulo{
  margin-top:18px;
  color:#1e293b; /*titulo "detalles de la orden" */
  font-weight:700;
}
.detalle-grid{ display:grid; grid-template-columns: 3fr 1fr 1fr 1fr auto; align-items:center; gap:10px; margin-top:10px; }
.detalle-header{
  font-weight:700;
  background-color: var(--color-senary); /*fondo encabezados tabla formulario "uniforme, cantidad, precio unitario, total"*/
  color:#fff; /*texto encabezados tabla formulario "uniforme, cantidad, precio unitario, total"*/
  padding:8px 6px;
  border-radius:6px;
}
.detalle-header span{ text-align:center; }
.detalle-nombre{
  color:#64748b; /*texto "→Overol de Trabajo" es el nombre del producto */
  display:block; margin-top:2px;
}

.cell-total{ text-align:right; padding-right:8px; }

.totales{ margin-top: 16px; display:flex; flex-direction:column; gap:8px; align-items:flex-end; }
.total-row{ display:flex; gap:16px; align-items:center; }
.total-final{ font-size: 18px; }

.buttons-row{ margin-top: 20px; display:flex; gap:15px; justify-content:flex-end; }
.btn-primary{
  background: var(--color-senary); /*fondo boton "guardar" en formulario "agregar nueva orden" */
  color:#fff; /*texto boton "guardar" */
  padding:10px 22px; border-radius:8px; border:none; font-weight:600; cursor:pointer;
  transition: background-color .3s; /*nada*/
}
.btn-primary:hover{ background: var(--color-tertiary); } /*fondo boton "guardar" cursor arriba */
.btn-cancel{
  background:transparent;
  color:#555; /*texto "cancelar" en formulario */
  padding:10px 22px; border-radius:8px;
  border:1px solid #aaa; /*borde boton "cancelar" en formulario */
  cursor:pointer; font-weight:600;
  transition: background-color .3s;
}
.btn-cancel:hover{ background:#eee; } /*fondo boton "cancelar" cursor arriba */
</style>
