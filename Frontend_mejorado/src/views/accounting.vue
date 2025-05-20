<template>
  <div class="contabilidad-container">
    <!-- Header tipo barra -->
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
        <p>Q64,000</p>
      </div>
      <div class="summary-card">
        <h3>GASTOS</h3>
        <p>Q64,000</p>
      </div>
      <div class="summary-card">
        <h3>BALANCE</h3>
        <p>Q64,000</p>
      </div>
      <div class="summary-card">
        <h3>OPERACIONES</h3>
        <p>64</p>
      </div>
    </div>

    <div class="actions-row">
      <div class="action-box" @click="viewIncomeChart">
        <h3>GRÁFICA INGRESOS</h3>
        <p>Analiza la evolución de los ingresos</p>
      </div>
      <div class="action-box" @click="viewExpensesChart">
        <h3>GRÁFICA GASTOS</h3>
        <p>Analiza la evolución de los gastos</p>
      </div>
      <div class="action-box" @click="viewBalanceChart">
        <h3>GRÁFICA BALANCE</h3>
        <p>Consulta el Balance General</p>
      </div>
      <div class="action-box" @click="closeAccounting">
        <h3>CIERRES CONTABLES</h3>
        <p>Registra y Analiza todos los Cierres Contables</p>
      </div>
    </div>

    <div class="operations-section">
      <h2 class="section-title">OPERACIONES RECIENTES</h2>
      <table class="operations-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>DESCRIPCIÓN</th>
            <th>MONTO</th>
            <th>FECHA</th>
            <th>ACCIÓN</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="op in operations" :key="op.id">
            <td>{{ op.id }}</td>
            <td>{{ op.description }}</td>
            <td>{{ op.amount }}</td>
            <td>{{ op.date }}</td>
            <td><button class="btn-view" @click="viewOperation(op)">VER</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'

export default {
  name: 'AccountingView',
  setup() {
    const router = useRouter()
    const goHome = () => {
      router.push({ name: 'home' }) // Asegúrate que tu ruta de inicio se llama "home"
    }
    return { goHome }
  },
  data() {
    return {
      operations: [
        { id: 1, description: 'Venta de producto', amount: 'Q64,000', date: '2023-04-09' },
        { id: 2, description: 'Compra de insumos', amount: 'Q64,000', date: '2023-04-09' },
        { id: 3, description: 'Pago de servicios', amount: 'Q64,000', date: '2023-04-09' },
        { id: 4, description: 'Venta de producto', amount: 'Q64,000', date: '2023-04-09' },
        { id: 5, description: 'Compra de equipo', amount: 'Q64,000', date: '2023-04-09' }
      ]
    }
  },
  methods: {
    viewIncomeChart() {
      console.log('VER GRÁFICA DE INGRESOS')
    },
    viewExpensesChart() {
      console.log('VER GRÁFICA DE GASTOS')
    },
    viewBalanceChart() {
      console.log('VER GRÁFICA DE BALANCE')
    },
    closeAccounting() {
      console.log('CIERRES CONTABLES')
    },
    viewOperation(op) {
      console.log('VER OPERACIÓN:', op)
    }
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

/* Header reutilizado */
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

/* Secciones de contenido */
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
}
.summary-card:hover {
  background-color: var(--color-senary);
}
.summary-card h3 {
  margin: 0;
  text-transform: uppercase;
  color: var(--colo-texto-blanco);
}
.summary-card p {
  font-size: 1.5rem;
  margin-top: 10px;
  color: var(--colo-texto-blanco);
  font-weight: bold;
}
.actions-row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 30px;
  color: var(--colo-texto-blanco);
}
.actions-row h3 {
  margin: 0;
  text-transform: uppercase;
  color: var(--colo-texto-blanco);
}
.action-box {
  flex: 1 1 200px;
  background-color: var(--color-primary);
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: background-color 0.3s;
}
.action-box:hover {
  background-color: var(--color-senary);
}
.operations-section {
  background-color: #1e293b;
  border-radius: 8px;
  padding: 20px;
  color: var(--colo-texto-blanco);
}
.operations-table th {
  background-color: var(--color-primary);
  color: var(--colo-texto-blanco);
  text-transform: uppercase;
}
.operations-table td {
  color: var(--colo-texto-blanco);
}
.section-title {
  margin-bottom: 20px;
  text-transform: uppercase;
  color: var(--color-primary);
  text-align: center;
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
.operations-table tr:nth-child(even) {
  background-color: var(--color-quaternary);
}
.operations-table tr:hover {
  background-color: #2B5CA8;
}
.btn-view {
  background-color: var(--color-senary);
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  text-transform: uppercase;
  transition: background-color 0.3s;
}
.btn-view:hover {
  background-color: var(--color-primary);
}
</style>
