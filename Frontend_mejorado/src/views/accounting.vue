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
  background:#0a0f2c;
  color:#fff;
  display:flex;
  flex-direction:column;
  font-family:'Segoe UI',sans-serif;
  padding-bottom: 2rem;
}

/* === Input del header: MISMO estilo que en Clientes === */
.nav-search{
  width: 280px; max-width: 40vw;
  padding: .5rem .75rem;
  border-radius: 10px;
  border: 1px solid #cbd5e1;
  background: #fff; color:#000;
  font-size: .9rem;
}
.nav-search:focus{
  outline: none;
  box-shadow: 0 0 0 3px rgba(99,102,241,.25);
  border-color:#6366f1;
}

/* === Secciones internas === */
.summary-section{
  display:flex; flex-wrap:wrap; gap:20px;
  margin: 2rem; margin-bottom:30px;
}
.summary-card{
  flex:1 1 200px;
  background:#0d1130;
  border:2px solid #1e2236;
  border-radius:16px;
  padding:20px; text-align:center;
  color:#fff;
  transition: background-color .3s;
}
.summary-card:hover{ background:#10163a; }
.summary-card h3{ margin:0; text-transform:uppercase; color:#fff; }
.summary-card p{ font-size:1.5rem; margin-top:10px; font-weight:bold; }

.operations-section{
  background:#0d1130;
  border:2px solid #1e2236;
  border-radius:16px;
  padding:20px; color:#fff;
  margin: 0 2rem;
}
.section-header{
  display:flex; justify-content:space-between; align-items:center;
  margin-bottom: 16px;
}
.section-title{ margin:0; text-transform:uppercase; color:#fff; text-align:center; }

.btn-add{
  background:#141a3d; color:#dbeafe; border:1px solid #263268;
  padding:10px 16px; border-radius:10px; font-weight:700; cursor:pointer;
  transition: background-color .2s, transform .05s;
}
.btn-add:hover{ background:#1b2354; }
.btn-add:active{ transform: translateY(1px); }

.operation-form{
  background:#f9fafb; padding:20px; border-radius:12px; color:#1e293b;
  box-shadow:0 6px 18px rgba(0,0,0,.15);
  margin-bottom:20px;
}
.operation-form h3{ margin-bottom:16px; text-align:center; color:#1e293b; }
.form-group{ margin-bottom:15px; }
.form-group label{ display:block; font-weight:700; margin-bottom:6px; color:#1e293b; }
.form-group select, .form-group input, .form-group textarea{
  width:100%; padding:10px; border-radius:8px; border:1px solid #cbd5e1; font-size:1rem; font-family:inherit;
}

/* Tabla */
.operations-table{ width:100%; border-collapse:separate; border-spacing:0 4px; }
.operations-table th{
  background:transparent; padding:12px 16px; color:#fff;
  font-size:.9rem; text-align:center; border-bottom:2px solid #334155;
}
.operations-table td{
  padding:12px 16px; text-align:center; border:none;
}
.operations-table tbody tr{
  background:#1e293b; color:#fff;
}
.operations-table tbody tr:nth-child(even){
  background:#162132;
}
.operations-table tbody tr:hover{
  background:#2b3a55;
}
</style>
