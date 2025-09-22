<template>
  <div class="contabilidad-container">
    <!-- Header unificado (igual al de Clientes) -->
    <NavBar title="SISTEMA DE CONTABILIDAD">
      <template #actions>
        <input v-model="search" class="nav-search" placeholder="Buscar operaciones…" />
      </template>
    </NavBar>

    <div class="summary-section">
      <div class="summary-card">
        <h3>INGRESOS</h3>
        <p>Q{{ summary.ingresos.toLocaleString() }}</p>
      </div>
      <div class="summary-card">
        <h3>GASTOS</h3>
        <p>Q{{ summary.egresos.toLocaleString() }}</p>
      </div>
      <div class="summary-card">
        <h3>BALANCE</h3>
        <p>Q{{ summary.balance.toLocaleString() }}</p>
      </div>
      <div class="summary-card">
        <h3>OPERACIONES</h3>
        <p>{{ summary.total }}</p>
      </div>
    </div>

    <div class="operations-section">
      <div class="section-header">
        <h2 class="section-title">OPERACIONES RECIENTES</h2>
        <button class="btn-add" @click="showForm = !showForm">
          {{ showForm ? 'CANCELAR' : 'AGREGAR MOVIMIENTO' }}
        </button>
      </div>

      <div v-if="showForm" class="operation-form">
        <h3>NUEVA OPERACIÓN</h3>
        <form @submit.prevent="addOperation">
          <div class="form-group">
            <label>Tipo:</label>
            <select v-model="newOperation.tipo" required>
              <option value="ingreso">Ingreso</option>
              <option value="egreso">Egreso</option>
            </select>
          </div>
          <div class="form-group">
            <label>Monto (Q):</label>
            <input type="number" step="0.01" min="0.01" v-model.number="newOperation.monto" required />
          </div>
          <div class="form-group">
            <label>Concepto:</label>
            <textarea v-model="newOperation.concepto" maxlength="250" required></textarea>
          </div>
          <button type="submit" class="btn-submit">GUARDAR</button>
        </form>
      </div>

      <table class="operations-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>TIPO</th>
            <th>CONCEPTO</th>
            <th>MONTO</th>
            <th>FECHA</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="op in filteredOperations" :key="op.id">
            <td>{{ op.id }}</td>
            <td>{{ op.tipo === 'ingreso' ? 'Ingreso' : 'Egreso' }}</td>
            <td>{{ op.concepto }}</td>
            <td>Q{{ Number(op.monto).toLocaleString() }}</td>
            <td>{{ op.fecha }}</td>
          </tr>
          <tr v-if="filteredOperations.length === 0">
            <td colspan="5">No hay operaciones que coincidan con la búsqueda</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { apiFetch } from '../utils/api'
import NavBar from '@/components/NavBar.vue'

export default {
  name: 'AccountingView',
  components: { NavBar },
  setup() {
    const router = useRouter()
    const goHome = () => router.push({ name: 'home' })
    return { goHome }
  },
  data() {
    return {
      operations: [],
      summary: { ingresos: 0, egresos: 0, balance: 0, total: 0 },
      showForm: false,
      newOperation: { tipo: 'ingreso', monto: '', concepto: '' },
      search: '' // <-- para el buscador del header
    }
  },
  computed: {
    filteredOperations() {
      const q = this.search.trim().toLowerCase()
      if (!q) return this.operations
      return this.operations.filter(op => {
        const monto = Number(op.monto)?.toString() ?? ''
        return [
          op.tipo === 'ingreso' ? 'ingreso' : 'egreso',
          op.concepto ?? '',
          op.fecha ?? '',
          monto
        ].some(v => v.toString().toLowerCase().includes(q))
      })
    }
  },
  methods: {
    async fetchOperations() {
      try {
        const data = await apiFetch('/api/operaciones/')
        this.operations = Array.isArray(data) ? data : (data?.results || [])
        this.calculateSummary()
      } catch (error) {
        console.error('Error cargando operaciones:', error)
      }
    },
    calculateSummary() {
      let ingresos = 0, egresos = 0
      this.operations.forEach(op => {
        if (op.tipo === 'ingreso') ingresos += Number(op.monto)
        else if (op.tipo === 'egreso') egresos += Number(op.monto)
      })
      this.summary.ingresos = ingresos
      this.summary.egresos = egresos
      this.summary.balance = ingresos - egresos
      this.summary.total = this.operations.length
    },
    async addOperation() {
      if (!this.newOperation.monto || !this.newOperation.concepto.trim()) {
        alert('Completa todos los campos'); return
      }
      try {
        const payload = {
          tipo: this.newOperation.tipo,
          monto: parseFloat(this.newOperation.monto),
          concepto: this.newOperation.concepto,
          fecha: new Date().toISOString().slice(0, 10),
        }
        const data = await apiFetch('/api/operaciones/', 'POST', payload)
        this.operations.push(data)
        this.calculateSummary()
        this.showForm = false
        this.newOperation = { tipo: 'ingreso', monto: '', concepto: '' }
      } catch (error) {
        console.error('Error agregando operación:', error)
        alert('Error al agregar la operación')
      }
    },
  },
  mounted() { this.fetchOperations() }
}
</script>

<style scoped>
/* === Fondo y layout general (igual estilo oscuro que en otras vistas) === */
.contabilidad-container{
  min-height:100vh;
  background:#0a0f2c; /*fondo de pantalla contabilidad*/
  color:#fff; /*nada*/
  display:flex;
  flex-direction:column;
  font-family:'Segoe UI',sans-serif;
  padding-bottom: 2rem;
}

/* === Input del header: MISMO estilo que en Clientes === */
/*no cambia nada si se elimina*/
.nav-search{
  width: 280px; max-width: 40vw;
  padding: .5rem .75rem;
  border-radius: 10px;
  border: 1px solid #cbd5e1; /*nada*/
  background: #fff; /*nada*/
  color:#000; /*nada*/
  font-size: .9rem;
}
/*no cambia nada si se elimina*/
.nav-search:focus{
  outline: none;
  box-shadow: 0 0 0 3px rgba(99,102,241,.25); /*nada*/
  border-color:#6366f1; /*nada*/
}

/* === Secciones internas === */
.summary-section{
  display:flex; flex-wrap:wrap; gap:20px;
  margin: 2rem; margin-bottom:30px;
}
.summary-card{
  flex:1 1 200px;
  background:#0d1130; /*fondo tarjetas "ingresos, gastos, balance, operaciones"*/
  border:2px solid #1e2236; /*borde tarjetas "ingresos, gastos, balance, operaciones"*/
  border-radius:16px;
  padding:20px; text-align:center;
  color:#fff; /*numeros resultantes tarjetas "ingresos, gastos, balance, operaciones"*/
  transition: background-color .3s; /*nada*/
}
.summary-card:hover{ background:#10163a; } /*fondo tarjetas "ingresos, gastos, balance, operaciones" con cursor arriba*/
.summary-card h3{
  margin:0; text-transform:uppercase;
  color:#fff; /*titulo tarjetas "ingresos, gastos, balance, operaciones"*/
}
.summary-card p{ font-size:1.5rem; margin-top:10px; font-weight:bold; }

.operations-section{
  background:#0d1130; /*fondo tabla "operaciones recientes" */
  border:2px solid #1e2236; /*borde tabla "operaciones recientes" */
  border-radius:16px;
  padding:20px; color:#fff; /*nada*/
  margin: 0 2rem;
}
.section-header{
  display:flex; justify-content:space-between; align-items:center;
  margin-bottom: 16px;
}
.section-title{
  margin:0; text-transform:uppercase;
  color:#fff; /*titulo "operaciones recientes" de tabla */
  text-align:center;
}

.btn-add{
  background:#141a3d; /*fondo boton "agregar movimiento"/"cancelar" de tabla */
  color:#dbeafe; /*texto  boton "agregar movimiento"/"cancelar" de tabla */
  border:1px solid #263268; /*borde boton "agregar movimiento"/"cancelar" */
  padding:10px 16px; border-radius:10px; font-weight:700; cursor:pointer;
  transition: background-color .2s, transform .05s;
}
.btn-add:hover{ background:#1b2354; } /*fondo boton "agregar movimiento"/"cancelar" cursor arriba*/
.btn-add:active{ transform: translateY(1px); }

.operation-form{
  background:#f9fafb; /*fondo tarjeta "nueva operacion" */
  padding:20px; border-radius:12px;
  color:#1e293b; /*nada*/
  box-shadow:0 6px 18px rgba(0,0,0,.15); /*sombreado abajo tarjeta "nueva operacion" */
  margin-bottom:20px;
}
.operation-form h3{
  margin-bottom:16px; text-align:center;
  color:#1e293b; /*titulo "nueva operacion" */
}
.form-group{ margin-bottom:15px; }
.form-group label{
  display:block; font-weight:700; margin-bottom:6px;
  color:#1e293b; /*texto campo inputs tarjeta "nueva operacion" */
}
.form-group select, .form-group input, .form-group textarea{
  width:100%; padding:10px; border-radius:8px;
  border:1px solid #cbd5e1; /*borde inputs tarjeta "nueva operacion" */
  font-size:1rem; font-family:inherit;
}

/* Tabla */
.operations-table{ width:100%; border-collapse:separate; border-spacing:0 4px; }
.operations-table th{
  background:transparent; padding:12px 16px;
  color:#fff; /*titulo encabezado tabla "id, tipo, concepto..." */
  font-size:.9rem; text-align:center;
  border-bottom:2px solid #334155; /*color linea separadora entre encabezado y tabla */
}
.operations-table td{
  padding:12px 16px; text-align:center; border:none;
}
.operations-table tbody tr{
  background:#1e293b; /*color1 lineas intercalado en tabla*/
  color:#fff; /*todo texto operaciones en tabla */
}
.operations-table tbody tr:nth-child(even){
  background:#162132; /*color2 lineas intercalado en tabla*/
}
.operations-table tbody tr:hover{
  background:#2b3a55; /*color lineas en tabla cursor arriba*/
}
</style>
