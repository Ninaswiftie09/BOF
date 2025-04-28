<script setup>
import { reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const open   = t => { modal.type = t; modal.visible = true }
const close  = () => { modal.visible = false }

const modal = reactive({ visible:false, type:'' })

const proveedorForm = reactive({
  codigo:'', estado:'Activo', nombre:'', contacto:'', nit:'',
  direccion:'', telefono:'', email:''
})
const proveedores = ref([])

const compraForm = reactive({
  proveedor:'', fecha:'', insumos:'', costo:0
})
const compras   = ref([])
const pagadas   = ref([])
const porPagar  = ref([])

function saveProveedor () {
  if (!proveedorForm.codigo || !proveedorForm.nombre) return alert('Código y nombre')
  proveedores.value.push({ ...proveedorForm })
  Object.keys(proveedorForm).forEach(k=>proveedorForm[k]=k==='estado'?'Activo':'')
  close()
}
function saveCompra () {
  compras.value.push({ id:Date.now(), proveedor:compraForm.proveedor, costo:compraForm.costo, fecha:compraForm.fecha })
  Object.keys(compraForm).forEach(k=>compraForm[k]='')
  close()
}
</script>

<template>
  <div class="crm-home">
    <header class="top-bar">
      <h1>PROVEEDORES</h1>
      <input class="search" placeholder="Buscar elementos exactos" />
      <button class="avatar-btn"></button>
    </header>

    <div class="new-order-wrapper">
      <button class="new-order-btn" @click="open('compra')">NUEVA COMPRA</button>
    </div>

    <main class="cards-container">
      <section class="big-card">
        <h2>ACTUALIZACIÓN</h2>
        <ul><li @click="open('proveedor')">Proveedores</li></ul>
      </section>

      <section class="big-card">
        <h2>REPORTES</h2>
        <ul>
          <li @click="open('historial')">Historial de compras</li>
          <li @click="open('pagar')">Saldos a pagar</li>
          <li @click="open('pagados')">Saldos pagados</li>
        </ul>
      </section>
    </main>

    <div v-if="modal.visible" class="modal-overlay" @click.self="close">
      <div class="modal-window">
        <template v-if="modal.type==='proveedor'">
          <h3>Proveedores</h3>
          <form class="modal-form grid-two" @submit.prevent="saveProveedor">
            <label>Código <input v-model="proveedorForm.codigo" required /></label>
            <label>Estado
              <select v-model="proveedorForm.estado"><option>Activo</option><option>Inactivo</option></select>
            </label>
            <label>Nombre <input v-model="proveedorForm.nombre" required /></label>
            <label>Contacto <input v-model="proveedorForm.contacto" /></label>
            <label>NIT <input v-model="proveedorForm.nit" /></label>
            <label>Dirección <input v-model="proveedorForm.direccion" /></label>
            <label>Teléfono <input v-model="proveedorForm.telefono" /></label>
            <label>E-mail <input v-model="proveedorForm.email" type="email" /></label>
            <button class="save-big" type="submit">Guardar</button>
            <button class="cancel-btn" type="button" @click="close">Cancelar</button>
          </form>
        </template>

        <template v-else-if="['historial','pagar','pagados'].includes(modal.type)">
          <h3>{{ {historial:'Historial de compras',pagar:'Saldos a pagar',pagados:'Saldos pagados'}[modal.type] }}</h3>
          <div class="table-wrapper">
            <table>
              <thead>
                <tr v-if="modal.type==='historial'">
                  <th>Id</th><th>Proveedor</th><th>Costo</th><th>Fecha</th>
                </tr>
                <tr v-else>
                  <th>Id</th><th>Id compra</th><th>Proveedor</th><th>Fecha pago</th><th>Monto</th>
                </tr>
              </thead>
              <tbody>
                <template v-if="modal.type==='historial'">
                  <tr v-for="c in compras" :key="c.id"><td>{{c.id}}</td><td>{{c.proveedor}}</td><td>{{c.costo}}</td><td>{{c.fecha}}</td></tr>
                </template>
                <template v-else-if="modal.type==='pagados'">
                  <tr v-for="(p,i) in pagadas" :key="i"><td>{{p.id}}</td><td>{{p.idCompra}}</td><td>{{p.proveedor}}</td><td>{{p.fecha}}</td><td>{{p.monto}}</td></tr>
                </template>
                <template v-else>
                  <tr v-for="(p,i) in porPagar" :key="i"><td>{{p.id}}</td><td>{{p.idCompra}}</td><td>{{p.proveedor}}</td><td>{{p.fecha}}</td><td>{{p.monto}}</td></tr>
                </template>
              </tbody>
            </table>
          </div>
          <button class="cancel-btn" @click="close">Cerrar</button>
        </template>

        <template v-else-if="modal.type==='compra'">
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
.search{flex:1 1 420px;max-width:420px;margin:0 auto;padding:.4rem .8rem;border-radius:6px;border:none;background:#fff;color:#000}
.search::placeholder{color:#555}
.avatar-btn{width:36px;height:36px;border-radius:50%;background:#fff;border:none;cursor:pointer}
.new-order-wrapper{display:flex;justify-content:flex-end;padding:1.5rem 2rem}
.new-order-btn{background:#1d4ed8;border:none;color:#fff;border-radius:12px;padding:.7rem 1.6rem;font-weight:600;cursor:pointer}
.new-order-btn:hover{transform:translateY(-2px)}

.cards-container{flex:1;display:flex;gap:3rem;flex-wrap:wrap;justify-content:center;padding:1rem 2rem 4rem}
.big-card{width:340px;min-height:360px;background:#101222;border:2px solid #1e2236;border-radius:18px;padding:1.5rem;display:flex;flex-direction:column;gap:1rem}
.big-card h2{margin:0;font-size:1.1rem;border-bottom:1px solid #2c3148;padding-bottom:.5rem;color:#fff}
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

.save-big{grid-column:1/-1;padding:.6rem 1rem;border:none;border-radius:8px;background:#2563eb;font-weight:600;cursor:pointer}
.cancel-btn{align-self:center;padding:.4rem 1.4rem;border:none;border-radius:8px;background:#9ca3af;color:#1e2236;font-weight:600;cursor:pointer}
.cancel-btn:hover{background:#d1d5db}

.table-wrapper{max-height:60vh;overflow:auto}
table{width:100%;border-collapse:collapse;font-size:.8rem}
th,td{padding:.4rem .6rem;border-bottom:1px solid #2c3148}
thead{position:sticky;top:0;background:#1e2236}
</style>

