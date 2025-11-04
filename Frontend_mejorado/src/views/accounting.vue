<template>
  <div class="contabilidad-container">
    <NavBar title="SISTEMA DE CONTABILIDAD">
      <template #actions>
        <input v-model="search" class="input--white" placeholder="Buscar operaciones…" />
      </template>
    </NavBar>

    <!-- Resumen -->
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

    <!-- Tabla principal -->
    <div class="operations-section">
      <div class="section-header">
        <h2 class="section-title">OPERACIONES RECIENTES</h2>
        <div class="section-buttons">
          <button class="btn" @click="openNew">AGREGAR MOVIMIENTO</button>
          <button class="btn btn--muted" @click="abrirVerTodos">VER TODO</button>
        </div>
      </div>

      <Tablas
        :columns="columns"
        :rows="tableRows.slice(0,6)"
        :center="true"
        :searchable="false"
        :actions="{ edit:false, delete:false }"
      />
    </div>

    <!-- Modal: nueva operación -->
    <div v-if="modalOpen" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content modal--compact">
        <h3>NUEVA OPERACIÓN</h3>
        <form class="form-vertical" @submit.prevent="addOperation">
          <div class="form-field">
            <label>Tipo</label>
            <div class="select-wrap">
              <select class="select--dark" v-model="newOperation.tipo" required>
                <option value="ingreso">Ingreso</option>
                <option value="egreso">Egreso</option>
              </select>
            </div>
          </div>

          <div class="form-field">
            <label>Monto (Q)</label>
            <input class="input--dark" type="number" step="0.01" min="0.01" v-model.number="newOperation.monto" required />
          </div>

          <div class="form-field">
            <label>Concepto</label>
            <textarea class="input--dark" v-model="newOperation.concepto" maxlength="250" required></textarea>
          </div>

          <div class="modal-actions">
            <button type="submit" class="btn">Guardar</button>
            <button type="button" class="btn btn--muted" @click="closeModal">Cancelar</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal: Ver Todo -->
    <div v-if="verTodosVisible" class="modal-overlay" @click.self="cerrarVerTodos">
      <div class="modal-content modal--wide full-table-modal">
        <button class="close-btn-top" @click="cerrarVerTodos">✕</button>
        <h3>OPERACIONES - LISTA COMPLETA</h3>
        <div class="table-wrapper">
          <table class="table dark-table table--center">
            <thead>
              <tr>
                <th v-for="col in columns" :key="col.key">{{ col.label }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in tableRows" :key="row.id">
                <td>{{ row.id }}</td>
                <td>{{ row.tipo }}</td>
                <td>{{ row.concepto }}</td>
                <td>{{ row.monto }}</td>
                <td>{{ row.fecha }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="modal-actions">
          <button class="btn btn--muted" @click="cerrarVerTodos">Cerrar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { apiFetch } from '@/utils/api'
import NavBar from '@/components/NavBar.vue'
import Tablas from '@/components/Reutilizacion/Tablas.vue'

export default {
  name: 'AccountingView',
  components: { NavBar, Tablas },
  setup() {
    const router = useRouter()
    const goHome = () => router.push({ name: 'home' })
    return { goHome }
  },
  data() {
    return {
      operations: [],
      summary: { ingresos: 0, egresos: 0, balance: 0, total: 0 },
      search: '',
      modalOpen: false,
      verTodosVisible: false,
      newOperation: { tipo: 'ingreso', monto: '', concepto: '' },
      columns: [
        { key: 'id', label: 'ID' },
        { key: 'tipo', label: 'TIPO' },
        { key: 'concepto', label: 'CONCEPTO' },
        { key: 'monto', label: 'MONTO' },
        { key: 'fecha', label: 'FECHA' },
      ],
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
    },
    tableRows() {
      return this.filteredOperations.map(op => ({
        id: op.id,
        tipo: op.tipo === 'ingreso' ? 'Ingreso' : 'Egreso',
        concepto: op.concepto,
        monto: `Q${Number(op.monto).toLocaleString()}`,
        fecha: op.fecha,
      }))
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
    openNew() { this.modalOpen = true },
    closeModal() { this.modalOpen = false },
    abrirVerTodos() { this.verTodosVisible = true },
    cerrarVerTodos() { this.verTodosVisible = false },
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
        this.closeModal()
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
.contabilidad-container{
  min-height:100vh;
  background:#0a0f2c;
  color:#fff;
  display:flex;
  flex-direction:column;
  font-family:'Segoe UI',sans-serif;
  padding-bottom: 2rem;
}

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
}
.summary-card h3{ margin:0; text-transform:uppercase; }
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
.section-buttons{
  display:flex; gap:10px;
}
.btn{ font-weight:700; }

.close-btn-top{
  position:absolute; top:10px; right:15px;
  background:transparent; border:none; font-size:22px;
  cursor:pointer; font-weight:bold; color:#fff;
}
.table-wrapper{ max-height:70vh; overflow:auto; }
</style>
