<template>
  <div class="contabilidad-container">
    <header class="top-bar">
      <img
        src="@/assets/logo_bof_blanco.png"
        alt="Logo del cliente"
        class="logo"
        @click="goHome"
      />
      <h1>SISTEMA DE CONTABILIDAD</h1>
      <button class="avatar-btn"></button>
    </header>

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
      <div class="section-header" style="display: flex; justify-content: space-between; align-items: center;">
        <h2 class="section-title">OPERACIONES RECIENTES</h2>
        <button class="btn-add" @click="showForm = !showForm">
          {{ showForm ? 'CANCELAR' : 'AGREGAR MOVIMIENTO' }}
        </button>
      </div>

      <div v-if="showForm" class="operation-form" style="margin-bottom: 20px;">
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
          <tr v-for="op in operations" :key="op.id">
            <td>{{ op.id }}</td>
            <td>{{ op.tipo === 'ingreso' ? 'Ingreso' : 'Egreso' }}</td>
            <td>{{ op.concepto }}</td>
            <td>Q{{ op.monto.toLocaleString() }}</td>
            <td>{{ op.fecha }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { apiFetch } from '../utils/api'


export default {
  name: 'AccountingView',
  setup() {
    const router = useRouter()
    const goHome = () => {
      router.push({ name: 'home' })
    }
    return { goHome }
  },
  data() {
    return {
      operations: [],
      summary: {
        ingresos: 0,
        egresos: 0,
        balance: 0,
        total: 0,
      },
      showForm: false,
      newOperation: {
        tipo: 'ingreso',
        monto: '',
        concepto: ''
      }
    }
  },
  methods: {
    async fetchOperations() {
      try {
        const data = await apiFetch('/api/operaciones/')
        this.operations = data

        this.calculateSummary()
      } catch (error) {
        console.error('Error cargando operaciones:', error)
      }
    },
    calculateSummary() {
      let ingresos = 0
      let egresos = 0
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
        alert('Completa todos los campos')
        return
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
  mounted() {
    this.fetchOperations()
  }
}
</script>

<style scoped>
.contabilidad-container {
  margin: 20px;
  padding: 20px;
  min-height: 100vh;
  background-color: var(--color-octonary);
  padding-top: 120px;
}

.top-bar {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 0.75rem 2rem;
  background: #1e293b;
  justify-content: space-between;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}
.logo {
  width: 150px;
  height: auto;
  cursor: pointer;
}
h1 {
  font-family: 'Segoe UI', sans-serif;
  color: #ffffff;
  font-size: 2rem;
  flex-grow: 1;
  text-align: center;
}
.avatar-btn {
  width: 40px;
  height: 40px;
  background-color: transparent;
  border: none;
  cursor: pointer;
}

.summary-section {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 30px;
}
.summary-card {
  flex: 1 1 200px;
  background-color: var(--color-primary);
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  transition: background-color 0.3s;
  color: var(--colo-texto-blanco);
}
.summary-card:hover {
  background-color: var(--color-senary);
}
.summary-card h3 {
  margin: 0;
  text-transform: uppercase;
  color: #ffffff;
}
.summary-card p {
  font-size: 1.5rem;
  margin-top: 10px;
  font-weight: bold;
  color: var(--colo-texto-blanco);
}

.operations-section {
  background-color: #1e293b;
  border-radius: 8px;
  padding: 20px;
  color: var(--colo-texto-blanco);
}
.section-title {
  margin-bottom: 20px;
  text-transform: uppercase;
  color: #ffffff;
  text-align: center;
}

.btn-add {
  background-color: #1e293b;
  color: white;
  border: 2px solid white;
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}
.btn-add:hover {
  background-color: #334155;
}

.operation-form {
  background-color: #f9fafb;
  padding: 20px;
  border-radius: 10px;
  color: #1e293b;
  box-shadow: 0 0 10px rgba(0,0,0,0.05);
}
.operation-form h3 {
  margin-bottom: 16px;
  text-align: center;
  color: #1e293b;
}
.form-group {
  margin-bottom: 15px;
}
.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 6px;
  color: #1e293b;
}
.form-group select,
.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #cbd5e1;
  font-size: 1rem;
  font-family: inherit;
}

.btn-submit {
  background-color: #1e293b;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  text-transform: uppercase;
  transition: background-color 0.3s;
  margin-top: 10px;
  width: 100%;
}
.btn-submit:hover {
  background-color: #334155;
}

.operations-table {
  width: 100%;
  border-collapse: collapse;
}
.operations-table th,
.operations-table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}
.operations-table th {
  background-color: var(--color-primary);
  color: #ffffff;
  text-transform: uppercase;
}
.operations-table tr:nth-child(even) {
  background-color: var(--color-quaternary);
  color: #003366;
}
.operations-table tr:nth-child(odd) {
  background-color: #1e293b;
  color: #ffffff;
}
.operations-table tr:hover {
  background-color: #2B5CA8;
  color: #ffffff;
}

.btn-view {
  background-color: var(--color-primary);
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  text-transform: uppercase;
  transition: background-color 0.3s;
}
.btn-view:hover {
  background-color: var(--color-senary);
}

</style>


