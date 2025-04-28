<script setup>
import { reactive, ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const go = path => router.push(path)

const modal = reactive({ visible:false, type:'' })
const open  = t => { modal.type = t; modal.visible = true }
const close = () => { modal.visible = false }

const cartera = reactive({ exterior:false, moneda:'GTQ', interes:0 })

const clienteForm = reactive({
  codigo:'', estado:'Activo', nombre:'', contacto:'', nit:'',
  direccion:'', direccionEntrega:'', telefono:'', email:'', cartera:0
})
const clientes = ref([])

const ordenForm = reactive({
  cliente:'', fecha:'', cantidad:1, productos:'', descripcion:'', precioUnit:0, total:0
})
watch(() => ordenForm.precioUnit, val => ordenForm.total = (+val||0)*(+ordenForm.cantidad||1))
watch(() => ordenForm.cantidad,  val => ordenForm.total = (+val||0)*(+ordenForm.precioUnit||0))

const pedidos  = ref([])
const pagadas  = ref([])
const porPagar = ref([])

function saveCartera () { alert('Cartera modificada'); close() }
function saveCliente () {
  if (!clienteForm.codigo || !clienteForm.nombre) return alert('Código y nombre')
  clientes.value.push({ ...clienteForm })
  Object.keys(clienteForm).forEach(k=>clienteForm[k]=k==='estado'?'Activo':(typeof clienteForm[k]==='number'?0:''))
  close()
}
function saveOrden () {
  pedidos.value.push({ id:Date.now(), cliente:ordenForm.cliente, monto:ordenForm.total, fecha:ordenForm.fecha, estado:'pendiente' })
  Object.keys(ordenForm).forEach(k=>ordenForm[k]=k==='cantidad'?1:0)
  close()
}
</script>

<template>
  <div class="crm-home">
    <header class="top-bar">
      <h1>CLIENTES</h1>
      <input class="search" placeholder="Buscar elementos exactos" />
      <button class="avatar-btn"></button>
    </header>

    <div class="new-order-wrapper">
      <button class="new-order-btn" @click="open('orden')">NUEVA ORDEN</button>
    </div>

    <main class="cards-container">
      <section class="big-card">
        <h2>ACTUALIZACIÓN</h2>
        <ul>
          <li @click="open('cartera')">Cartera Crédito</li>
          <li @click="open('clientes')">Clientes</li>
        </ul>
      </section>

      <section class="big-card">
        <h2>REPORTES</h2>
        <ul>
          <li @click="open('historial')">Historial de pedidos</li>
          <li @click="open('pagar')">Cuentas a pagar</li>
          <li @click="open('pagadas')">Cuentas pagadas</li>
        </ul>
      </section>
    </main>

    <div v-if="modal.visible" class="modal-overlay" @click.self="close">
      <div class="modal-window">
        <template v-if="modal.type==='cartera'">
          <h3>Cartera Crédito</h3>
          <form class="modal-form" @submit.prevent="saveCartera">
            <label>Cliente exterior <input type="checkbox" v-model="cartera.exterior" /></label>
            <label>Moneda
              <select v-model="cartera.moneda">
                <option value="GTQ">Quetzales</option>
                <option value="USD">Dólares</option>
              </select>
            </label>
            <label>Interés <input v-model.number="cartera.interes" placeholder="Q0.00" /></label>
            <div class="actions">
              <button type="submit">Modificar</button>
              <button @click="alert('Eliminar…')">Eliminar</button>
            </div>
            <button class="cancel-btn" @click="close">Cancelar</button>
          </form>
        </template>

        <template v-else-if="modal.type==='clientes'">
          <h3>Clientes</h3>
          <form class="modal-form grid-two" @submit.prevent="saveCliente">
            <label>Código <input v-model="clienteForm.codigo" required /></label>
            <label>Estado
              <select v-model="clienteForm.estado"><option>Activo</option><option>Inactivo</option></select>
            </label>
            <label>Nombre <input v-model="clienteForm.nombre" required /></label>
            <label>Contacto <input v-model="clienteForm.contacto" /></label>
            <label>NIT <input v-model="clienteForm.nit" /></label>
            <label>Dirección <input v-model="clienteForm.direccion" /></label>
            <label>Dirección Entrega <input v-model="clienteForm.direccionEntrega" /></label>
            <label>Teléfono <input v-model="clienteForm.telefono" /></label>
            <label>E-mail <input v-model="clienteForm.email" type="email" /></label>
            <label>Cartera <input v-model.number="clienteForm.cartera" type="number" min="0" /></label>
            <button type="submit" class="save-big">Guardar</button>
            <button class="cancel-btn" type="button" @click="close">Cancelar</button>
          </form>
        </template>

        <template v-else-if="['historial','pagar','pagadas'].includes(modal.type)">
          <h3>{{ {historial:'Historial de pedidos',pagar:'Cuentas a pagar',pagadas:'Cuentas pagadas'}[modal.type] }}</h3>
          <div class="table-wrapper">
            <table>
              <thead>
                <tr v-if="modal.type==='historial'">
                  <th>Id</th><th>Cliente</th><th>Monto</th><th>Fecha ven.</th><th>Pago</th>
                </tr>
                <tr v-else>
                  <th>Id</th><th>Id pedido</th><th>Cliente</th><th>Fecha pago</th><th>Monto</th>
                </tr>
              </thead>
              <tbody>
                <template v-if="modal.type==='historial'">
                  <tr v-for="p in pedidos" :key="p.id"><td>{{p.id}}</td><td>{{p.cliente}}</td><td>{{p.monto}}</td><td>{{p.fecha}}</td><td>{{p.estado}}</td></tr>
                </template>
                <template v-else-if="modal.type==='pagadas'">
                  <tr v-for="(p,i) in pagadas" :key="i"><td>{{p.id}}</td><td>{{p.idPedido}}</td><td>{{p.cliente}}</td><td>{{p.fecha}}</td><td>{{p.monto}}</td></tr>
                </template>
                <template v-else>
                  <tr v-for="(p,i) in porPagar" :key="i"><td>{{p.id}}</td><td>{{p.idPedido}}</td><td>{{p.cliente}}</td><td>{{p.fecha}}</td><td>{{p.monto}}</td></tr>
                </template>
              </tbody>
            </table>
          </div>
          <button class="cancel-btn" @click="close">Cerrar</button>
        </template>

        <template v-else-if="modal.type==='orden'">
          <h3>Nueva Orden</h3>
          <form class="modal-form grid-two" @submit.prevent="saveOrden">
            <label>Cliente
              <select v-model="ordenForm.cliente">
                <option v-for="c in clientes" :key="c.codigo" :value="c.nombre">{{c.nombre}}</option>
              </select>
            </label>
            <label>Fecha <input type="date" v-model="ordenForm.fecha" /></label>
            <label>Cantidad <input type="number" min="1" v-model.number="ordenForm.cantidad" /></label>
            <label>Productos solicitados <input v-model="ordenForm.productos" /></label>
            <label>Descripción <input v-model="ordenForm.descripcion" /></label>
            <label>Precio unitario <input type="number" min="0" v-model.number="ordenForm.precioUnit" /></label>
            <label>Precio total <input type="number" readonly :value="ordenForm.total" /></label>
            <button type="submit" class="save-big">Guardar</button>
            <button class="cancel-btn" type="button" @click="close">Cancelar</button>
          </form>
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped>
*{color:#fff}
.crm-home{min-height:100vh;background:#0a0f2c;display:flex;flex-direction:column;font-family:'Segoe UI',sans-serif}
.top-bar{display:flex;align-items:center;gap:1.5rem;padding:.75rem 2rem;background:#1e293b}
h1{font-weight:600}
.search{flex:1 1 420px;max-width:420px;margin:0 auto;padding:.4rem .8rem;border-radius:6px;border:none;background:#ffffff;color:#000}
.search::placeholder{color:#555}
.avatar-btn{width:36px;height:36px;border-radius:50%;background:#ffffff;border:none;cursor:pointer}
.new-order-wrapper{display:flex;justify-content:flex-end;padding:1.5rem 2rem}
.new-order-btn{background:#1d4ed8;border:none;color:#fff;border-radius:12px;padding:.7rem 1.6rem;font-weight:600;cursor:pointer}
.new-order-btn:hover{transform:translateY(-2px)}

.cards-container{flex:1;display:flex;gap:3rem;flex-wrap:wrap;justify-content:center;padding:1rem 2rem 4rem}
.big-card{width:340px;min-height:360px;background:#101222;border:2px solid #1e2236;border-radius:18px;padding:1.5rem;display:flex;flex-direction:column;gap:1rem}
.big-card h2{margin:0;font-size:1.1rem;letter-spacing:.5px;border-bottom:1px solid #2c3148;padding-bottom:.5rem;color:#ffffff}
.big-card ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:.8rem}
.big-card li{cursor:pointer;padding:.4rem .2rem;border-radius:6px}
.big-card li:hover{background:#1e2236}

.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.6);display:flex;justify-content:center;align-items:center;z-index:2000}
.modal-window{background:#1e2236;padding:2rem;border-radius:14px;min-width:600px;max-width:90%;max-height:90vh;overflow:auto;display:flex;flex-direction:column;gap:1rem}
.modal-window h3{margin:0;font-size:1.2rem;text-align:center}
.modal-form{display:flex;flex-direction:column;gap:.8rem}
.grid-two{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:.8rem}
.modal-form label{display:flex;flex-direction:column;font-size:.9rem;gap:.25rem}
.modal-form input,.modal-form select{padding:.45rem .6rem;border:none;border-radius:6px;background:#111827;color:#fff}
.actions{display:flex;gap:.6rem;justify-content:center}
.actions button{padding:.5rem 1rem;border:none;border-radius:8px;background:#334155;cursor:pointer}
.actions button:hover{background:#475569}
.cancel-btn{align-self:center;padding:.4rem 1.4rem;border:none;border-radius:8px;background:#9ca3af;color:#1e2236;font-weight:600;cursor:pointer}
.cancel-btn:hover{background:#d1d5db}
.save-big{grid-column:1/-1;padding:.6rem 1rem;border:none;border-radius:8px;background:#2563eb;font-weight:600;cursor:pointer}
.table-wrapper{max-height:60vh;overflow:auto}
table{width:100%;border-collapse:collapse;font-size:.8rem}
th,td{padding:.4rem .6rem;border-bottom:1px solid #2c3148}
thead{position:sticky;top:0;background:#1e2236}
</style>
