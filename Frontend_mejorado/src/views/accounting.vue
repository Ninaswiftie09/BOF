<template>
  <div class="contabilidad-container">
    <router-link to="/" class="back-button">Regresar a Inicio</router-link>
    <div class="upper-rectangle"></div>

    <div class="header-rectangle">
      <h2 class="header-title">SISTEMA DE CONTABILIDAD</h2>
    </div>

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
export default {
  name: 'AccountingView',
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
.upper-rectangle {
  background-color: var(--color-primary);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  padding: 20px;
  text-align: center;
  z-index: 1000;
  margin-bottom: 10px;
}
.header-rectangle {
  background-color: var(--color-primary);
  border-radius: 8px;
  padding: 20px;
  margin-top: 10px;
  margin-bottom: 20px;
  text-align: center;
}
.header-title {
  color: #fff;
  margin: 0;
  text-transform: uppercase;
}
.summary-section {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 30px;
}
.summary-card {
  flex: 1 1 200px;
  background-color: var(--color-quaternary);
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  transition: background-color 0.3s;
}
.summary-card:hover {
  background-color: var(--color-tertiary);
}
.summary-card h3 {
  margin: 0;
  text-transform: uppercase;
  color: var(--color-primary);
}
.summary-card p {
  font-size: 1.5rem;
  margin-top: 10px;
  color: var(--color-primary);
  font-weight: bold;
}
.actions-row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 30px;
}
.action-box {
  flex: 1 1 200px;
  background-color: var(--color-quaternary);
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: background-color 0.3s;
}
.action-box:hover {
  background-color: var(--color-tertiary);
}
.operations-section {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
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
.operations-table th {
  background-color: var(--color-primary);
  color: #fff;
  text-transform: uppercase;
}
.operations-table tr:nth-child(even) {
  background-color: var(--color-quaternary);
}
.operations-table tr:hover {
  background-color: #8cafdc;
}
.btn-view {
  background-color: var(--color-secondary);
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  text-transform: uppercase;
  transition: background-color 0.3s;
}
.btn-view:hover {
  background-color: var(--color-tertiary);
}
</style>
