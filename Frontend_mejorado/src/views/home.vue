<template>
  <div class="dashboard-container">
    <aside class="sidebar">
      <img src="@/assets/logo_bof_blanco.png" alt="logo del cliente" class="logo" />
      <nav class="nav-links">
        <router-link
          v-for="item in navItems"
          :key="item.label"
          :to="item.route"
          class="nav-item"
        >
          <div class="icon-circle">
            <component v-if="item.icon" :is="item.icon" />
            <span v-else>🔸</span>
          </div>
          <span>{{ item.label }}</span>
        </router-link>
      </nav>
    </aside>

    <main class="main-area">
      <header class="topbar">
        <div class="view-name">HOME</div>
        <div class="user-circle"></div>
      </header>

      <section class="content">
        <div class="chart-area">
          <canvas id="myPieChart"></canvas>
        </div>

        <div class="side-panels">
          <!-- Calendario -->
          <div class="panel">
            <v-calendar
              is-inline
              :is-dark="true"
              color="gray"
              :attributes="calendarAttrs"
              :month-format="{ month: 'long', year: 'numeric' }"
            />
          </div>

          <!-- Gráfica de barras simulada: Ventas por mes -->
          <div class="panel">
            <canvas id="bestMonthChart"></canvas>
          </div>

          <!-- clientes nuevos -->
          <div class="panel">
            <div class="kpi">
              <h3>Clientes nuevos</h3>
              <p class="value">45</p>
              <small>en el mes</small>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import Chart from 'chart.js/auto'

import IconClientes from '@/components/icons/IconClientes.vue'
import IconFacturas from '@/components/icons/IconFacturas.vue'
import IconContabilidad from '@/components/icons/IconContabilidad.vue'
import IconInventario from '@/components/icons/IconInventario.vue'
import IconReporteVentas from '@/components/icons/IconRVentas.vue'
import IconUser from '@/components/icons/IconUser.vue' 




const inventarioData = ref({
  Telas: 0,
  Hilos: 0,
  Uniformes: 0
})

const ventasPorMes = ref({
  Ene: 0, Feb: 0, Mar: 0, Abr: 0, May: 0, Jun: 0,
  Jul: 0, Ago: 0, Sep: 0, Oct: 0, Nov: 0, Dic: 0
})

// Navegación
const navItems = [
  { label: 'Clientes y Proveedores', icon: IconClientes, route: '/clientes' },
  { label: 'Facturas', icon: IconFacturas, route: '/billpage' },
  { label: 'Contabilidad', icon: IconContabilidad, route: '/accounting' },
  { label: 'Inventario', icon: IconInventario, route: '/mi_inventario' },
  { label: 'Reporte de ventas', icon: IconReporteVentas, route: '/ReporteVentas' },
  { label: 'Gestión de Usuarios', icon: IconUser, route: '/register' }

]

// Atributos para V-Calendar (resalta hoy)
const calendarAttrs = ref([
  { key: 'hoy', highlight: true, dates: new Date() }
])

//
async function fetchInventarioData() {
  const tipos = ['telas', 'hilos', 'uniformes']
  for (const tipo of tipos) {
    try {
      const res = await fetch(`https://abriluniformes.shop/api/${tipo}/`)
      const data = await res.json()
      inventarioData.value[tipo.charAt(0).toUpperCase() + tipo.slice(1)] = data.reduce(
        (total, item) => total + (item.stock || 0),
        0
      )
    } catch (err) {
      console.error(`Error cargando ${tipo}:`, err)
    }
  }
}

// 
async function fetchVentasMensuales() {
  try {
    const res = await fetch('https://abriluniformes.shop/api/ventas/')
    const data = await res.json()

    // Reset
    Object.keys(ventasPorMes.value).forEach(m => ventasPorMes.value[m] = 0)

    data.forEach(v => {
      const fecha = new Date(v.fecha)
      const mes = fecha.toLocaleString('es-ES', { month: 'short' }) 
      const clave = mes.charAt(0).toUpperCase() + mes.slice(1) 

      if (ventasPorMes.value[clave] !== undefined) {
        ventasPorMes.value[clave] += parseFloat(v.total)
      }
    })

  } catch (error) {
    console.error('Error cargando ventas:', error)
  }
}

onMounted(async () => {
  await fetchInventarioData()
  await fetchVentasMensuales()


  // Pie Chart: Inventario real
  const pieCtx = document.getElementById('myPieChart').getContext('2d')
  new Chart(pieCtx, {
    type: 'pie',
    data: {
      labels: ['Telas', 'Hilos', 'Uniformes'],
      datasets: [{
        data: [
          inventarioData.value.Telas,
          inventarioData.value.Hilos,
          inventarioData.value.Uniformes
        ],
        backgroundColor: ['#839A2D', '#2AA68F', '#2B5CA8'],
        borderColor: '#fff',
        borderWidth: 1
      }]
    },
    options: {
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top' },
        title: { display: true, text: 'Inventario' }
      }
    }
  })

 const barCtx = document.getElementById('bestMonthChart').getContext('2d')
  new Chart(barCtx, {
    type: 'bar',
    data: {
      labels: Object.keys(ventasPorMes.value).slice(0, 6), // Ene-Jun
      datasets: [{
        label: 'Ventas',
        data: Object.values(ventasPorMes.value).slice(0, 6),
        backgroundColor: context => context.dataIndex === 4 ? '#2AA68F' : '#84C8C0',
        borderColor: '#fff',
        borderWidth: 1
      }]
    },
    options: {
      maintainAspectRatio: false,
      plugins: {
        title: { display: true, text: 'Ventas por mes' }
      },
      scales: { y: { beginAtZero: true } }
    }
  })
})

</script>

<style scoped>
.dashboard-container {
  display: flex;
  height: 100vh;
  background: #0a0f2c;
  color: white;
  font-family: 'Segoe UI', sans-serif;
}

.sidebar {
  width: 240px;
  background-color: #1e293b;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.logo { width: 250px; height: 150px; margin-bottom: 1rem; }

.nav-links { width: 100%; display: flex; flex-direction: column; gap: 1rem; }
.nav-item { display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem; border-radius: 8px;
            cursor: pointer; transition: background 0.2s; color: white; text-decoration: none; }
.nav-item:hover, .router-link-exact-active { background-color: #334155; }
.icon-circle { width: 36px; height: 36px; border-radius: 50%; background-color: #64748b;
               display: flex; align-items: center; justify-content: center; }

.main-area { flex: 1; display: flex; flex-direction: column; }
.topbar { background-color: #1e293b; padding: 1rem; display: flex;
         justify-content: space-between; align-items: center; }
.view-name { font-size: 1.25rem; font-weight: bold; }
.user-circle { width: 36px; height: 36px; background-color: white; border-radius: 50%; }

.content { display: flex; flex: 1; padding: 1rem; gap: 1rem; overflow: hidden; }
.chart-area { flex: 2; background-color: #1e293b; border-radius: 16px;
              display: flex; align-items: center; justify-content: center; }
.chart-area canvas { width: 100% !important; height: 100% !important; }

.side-panels { flex: 1; display: flex; flex-direction: column; gap: 1rem; overflow: hidden; }
.panel { background-color: #334155; border-radius: 12px; padding: 1rem;
         display: flex; align-items: center; justify-content: center; position: relative; }

/* Ajuste general para canvases en paneles */
.panel canvas { width: 100% !important; height: 100% !important; }

/* Estilos de KPI simple */
.kpi { text-align: center; }
.kpi .value { font-size: 2rem; margin: 0.5rem 0; color: #2AA68F; }
.kpi small { color: #cbd5e1; }
</style>
