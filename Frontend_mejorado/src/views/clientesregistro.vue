<script setup>
import { reactive, ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'

const router = useRouter()
const go = path => router.push(path)

const search = ref('')
const modal = reactive({ visible:false, type:'' })
const open = t => { modal.type = t; modal.visible = true }
const close = () => { modal.visible = false }

const clienteForm = reactive({
  codigo:'', estado:'Activo', nombre:'', contacto:'', nit:'',
  direccion:'', direccionEntrega:'', telefono:'', email:'', cartera:0
})
const clientes = ref([])

function saveCliente () {
  if (!clienteForm.codigo || !clienteForm.nombre) return alert('Código y nombre')
  clientes.value.push({ ...clienteForm })
  Object.keys(clienteForm).forEach(k =>
    clienteForm[k] = k==='estado' ? 'Activo' : (typeof clienteForm[k]==='number' ? 0 : '')
  )
  close()
}

/* FILTRO DE BÚSQUEDA */
const filteredClientes = computed(() =>
  clientes.value.filter(c =>
    [c.codigo, c.nombre, c.contacto]
      .some(v => v?.toLowerCase().includes(search.value.toLowerCase()))
  )
)

/* NUEVA ORDEN */
const orderHeader = reactive({ cliente:'', fecha:'' })
const orderLines  = ref([
  { producto:'', talla:'', color:'', tela:'', bordado:'', cantidad:1, precio:0, descuento:0 }
])
const addLine    = () => orderLines.value.push({ producto:'', talla:'', color:'', tela:'', bordado:'', cantidad:1, precio:0, descuento:0 })
const removeLine = i => orderLines.value.splice(i,1)
const lineTotal  = l => (l.precio*l.cantidad) - l.descuento
const grandTotal = computed(()=> orderLines.value.reduce((s,l)=>s+lineTotal(l),0))

function saveOrder(){
  pedidos.value.push({ id:Date.now(), cliente:orderHeader.cliente, monto:grandTotal.value, fecha:orderHeader.fecha, estado:'pendiente' })
  orderHeader.cliente = ''; orderHeader.fecha = ''
  orderLines.value = [{ producto:'', talla:'', color:'', tela:'', bordado:'', cantidad:1, precio:0, descuento:0 }]
  close()
}

const pedidos  = ref([])
const pagadas  = ref([])
const porPagar = ref([])
</script>

<template>
  <div class="crm-home">
    <NavBar title="CLIENTES">
      <template #actions>
        <input v-model="search" class="search" placeholder="Buscar clientes…" />
        <button class="avatar-btn"></button>
      </template>
    </NavBar>

    <div class="new-order-wrapper">
      <button class="new-order-btn" @click="open('orden')">NUEVA ORDEN</button>
    </div>

    <div class="body-wrapper">
      <!-- módulo 1 : Tabla de clientes -->
      <section class="module">
        <table>
          <thead>
            <tr><th>Código</th><th>Nombre</th><th>Contacto</th><th>Acciones</th></tr>
          </thead>
          <tbody>
            <tr v-for="c in filteredClientes" :key="c.codigo">
              <td>{{ c.codigo }}</td>
              <td>{{ c.nombre }}</td>
              <td>{{ c.contacto }}</td>
              <td><button @click="open('historial')">Ver pedidos pasados</button></td>
            </tr>
            <tr v-if="filteredClientes.length===0"><td colspan="4">&nbsp;</td></tr>
          </tbody>
        </table>
      </section>

      <!-- módulo 2 : Tarjetas -->
      <section class="module cards-module">
        <div class="cards-container">
          <section class="big-card">
            <h2>ACTUALIZACIÓN</h2>
            <ul><li @click="open('clientes')">Clientes</li></ul>
          </section>
          <section class="big-card">
            <h2>REPORTES</h2>
            <ul>
              <li @click="open('historial')">Historial de pedidos</li>
              <li @click="open('pagar')">Cuentas a pagar</li>
              <li @click="open('pagadas')">Cuentas pagadas</li>
            </ul>
          </section>
        </div>
      </section>
    </div>

    <div v-if="modal.visible" class="modal-overlay" @click.self="close">
      <div class="modal-window">

        <!-- Clientes -->
        <template v-if="modal.type==='clientes'">
          <h3>Clientes</h3>
          <form class="modal-form grid-two" @submit.prevent="saveCliente">
            <label>Código<input v-model="clienteForm.codigo" required/></label>
            <label>Estado<select v-model="clienteForm.estado"><option>Activo</option><option>Inactivo</option></select></label>
            <label>Nombre<input v-model="clienteForm.nombre" required/></label>
            <label>Contacto<input v-model="clienteForm.contacto"/></label>
            <label>NIT<input v-model="clienteForm.nit"/></label>
            <label>Dirección<input v-model="clienteForm.direccion"/></label>
            <label>Entrega<input v-model="clienteForm.direccionEntrega"/></label>
            <label>Teléfono<input v-model="clienteForm.telefono"/></label>
            <label>E-mail<input type="email" v-model="clienteForm.email"/></label>
            <label>Cartera<input type="number" v-model.number="clienteForm.cartera" min="0"/></label>
            <button type="submit" class="save-big">Guardar</button>
            <button type="button" class="cancel-btn" @click="close">Cancelar</button>
          </form>
        </template>

        <!-- Historial / Pagar / Pagadas -->
        <template v-else-if="['historial','pagar','pagadas'].includes(modal.type)">
          <h3>{{ {historial:'Historial de pedidos',pagar:'Cuentas a pagar',pagadas:'Cuentas pagadas'}[modal.type] }}</h3>
          <div class="table-wrapper">
            <table>
              <thead>
                <tr v-if="modal.type==='historial'">
                  <th>Id</th><th>Cliente</th><th>Monto</th><th>Fecha ven.</th><th>Estado</th>
                </tr>
                <tr v-else>
                  <th>Id</th><th>Id pedido</th><th>Cliente</th><th>Fecha pago</th><th>Monto</th>
                </tr>
              </thead>
              <tbody>
                <template v-if="modal.type==='historial'">
                  <tr v-for="p in pedidos" :key="p.id">
                    <td>{{p.id}}</td><td>{{p.cliente}}</td><td>{{p.monto}}</td><td>{{p.fecha}}</td><td>{{p.estado}}</td>
                  </tr>
                </template>
                <template v-else-if="modal.type==='pagadas'">
                  <tr v-for="(p,i) in pagadas" :key="i">
                    <td>{{p.id}}</td><td>{{p.idPedido}}</td><td>{{p.cliente}}</td><td>{{p.fecha}}</td><td>{{p.monto}}</td>
                  </tr>
                </template>
                <template v-else>
                  <tr v-for="(p,i) in porPagar" :key="i">
                    <td>{{p.id}}</td><td>{{p.idPedido}}</td><td>{{p.cliente}}</td><td>{{p.fecha}}</td><td>{{p.monto}}</td>
                  </tr>
                </template>
                <tr v-if="(modal.type==='historial' ? pedidos : modal.type==='pagadas' ? pagadas : porPagar).length===0">
                  <td :colspan="modal.type==='historial'?5:5">&nbsp;</td>
                </tr>
              </tbody>
            </table>
          </div>
          <button class="cancel-btn" @click="close">Cerrar</button>
        </template>

        <!-- Nueva Orden -->
        <template v-else-if="modal.type==='orden'">
          <h3>Nueva orden</h3>
          <div class="grid-two mb-3">
            <label>Cliente
              <select v-model="orderHeader.cliente">
                <option v-for="c in clientes" :key="c.codigo" :value="c.nombre">{{c.nombre}}</option>
              </select>
            </label>
            <label>Fecha<input type="date" v-model="orderHeader.fecha"/></label>
          </div>
          <table class="order-table">
            <thead>
              <tr>
                <th>Producto</th><th>Talla</th><th>Color</th><th>Tela</th><th>Bordado</th>
                <th>Cant.</th><th>Precio</th><th>Desc.</th><th>Total</th><th>Eliminar</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(l,i) in orderLines" :key="i">
                <td><input v-model="l.producto"/></td>
                <td><input v-model="l.talla"/></td>
                <td><input v-model="l.color"/></td>
                <td><input v-model="l.tela"/></td>
                <td><input v-model="l.bordado"/></td>
                <td><input type="number" min="1" v-model.number="l.cantidad"/></td>
                <td><input type="number" min="0" v-model.number="l.precio"/></td>
                <td><input type="number" min="0" v-model.number="l.descuento"/></td>
                <td>{{ lineTotal(l) }}</td>
                <td><button class="remove-btn" @click="removeLine(i)">✕</button></td>
              </tr>
              <tr><td colspan="10">&nbsp;</td></tr>
            </tbody>
          </table>
          <button class="add-line" @click="addLine">+ Agregar otro producto</button>
          <div class="grand-total">TOTAL: {{ grandTotal }}</div>
          <div class="actions">
            <button class="cancel-btn" @click="close">Cancelar</button>
            <button class="save-big" @click="saveOrder">Guardar</button>
          </div>
        </template>

      </div>
    </div>

  </div>
</template>

<style scoped>
*{color:#fff}
.crm-home{min-height:100vh;background:#0a0f2c;display:flex;flex-direction:column;font-family:'Segoe UI',sans-serif}

.search{flex:1 1 300px;max-width:300px;margin-right:1rem;padding:.4rem .8rem;border-radius:6px;border:none;background:#fff;color:#000}
.avatar-btn{width:36px;height:36px;border-radius:50%;background:#fff;border:none;cursor:pointer}

.new-order-wrapper{display:flex;justify-content:flex-end;padding:1.5rem 2rem}
.new-order-btn{background:#1d4ed8;border:none;color:#fff;border-radius:12px;padding:.7rem 1.6rem;font-weight:600;cursor:pointer}
.new-order-btn:hover{transform:translateY(-2px)}

.body-wrapper{display:flex;flex-direction:column;gap:2rem;padding:1rem 2rem}
.module{background:#0d1130;border:2px solid #1e2236;border-radius:16px;padding:1.5rem}
.cards-module{justify-content:center;display:flex}

.cards-container{display:flex;gap:3rem;flex-wrap:wrap;justify-content:center;padding:0}
.big-card{width:340px;min-height:360px;background:#101222;border:2px solid #1e2236;border-radius:18px;padding:1.5rem;display:flex;flex-direction:column;gap:1rem}
.big-card h2{margin:0;font-size:1.1rem;letter-spacing:.5px;border-bottom:1px solid #2c3148;padding-bottom:.5rem;color:#fff}
.big-card ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:.8rem}
.big-card li{cursor:pointer;padding:.4rem .2rem;border-radius:6px}
.big-card li:hover{background:#1e2236}

.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.6);display:flex;justify-content:center;align-items:center;z-index:2000}
.modal-window{background:#1e293b;padding:2rem;border-radius:14px;min-width:600px;max-width:90%;max-height:90vh;overflow:auto;display:flex;flex-direction:column;gap:1rem}

.modal-form{display:flex;flex-direction:column;gap:.8rem}
.grid-two{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:.8rem}
.modal-form label{display:flex;flex-direction:column;font-size:.9rem;gap:.25rem}
.modal-form input,.modal-form select{padding:.45rem .6rem;border:none;border-radius:6px;background:#111827;color:#fff}

.table-wrapper{max-height:60vh;overflow:auto;margin-bottom:1rem}
.table-wrapper table{width:100%;border-collapse:collapse;font-size:.8rem}
.table-wrapper th,.table-wrapper td{padding:.4rem .6rem;border-bottom:1px solid #2c3148}
.table-wrapper thead{position:sticky;top:0;background:#1e293b}

.order-table{width:100%;border-collapse:collapse;margin-bottom:1rem;font-size:.8rem}
.order-table th,.order-table td{border:1px solid #2c3148;padding:.3rem .4rem;text-align:center}
.remove-btn{background:transparent;border:none;color:#e74c3c;cursor:pointer}
.add-line{background:#059669;border:none;color:#fff;border-radius:8px;padding:.4rem 1rem;cursor:pointer;margin-bottom:.6rem}
.grand-total{text-align:right;font-weight:700;margin-bottom:.4rem}
.actions{display:flex;gap:.6rem;justify-content:center}
.cancel-btn{align-self:center;padding:.4rem 1.4rem;border:none;border-radius:8px;background:#9ca3af;color:#1e293b;font-weight:600;cursor:pointer}
.cancel-btn:hover{background:#d1d5db}
.save-big{padding:.6rem 1rem;border:none;border-radius:8px;background:#2563eb;font-weight:600;cursor:pointer;color:#fff}
</style>
