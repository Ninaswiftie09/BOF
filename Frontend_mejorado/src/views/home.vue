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
        <!-- Pie -->
        <div class="chart-area">
          <canvas id="myPieChart"></canvas>
        </div>

        <!-- Widgets derecha -->
        <div class="side-panels">
          <!-- Calendario -->
          <div class="panel panel--calendar">
            <v-calendar
              is-inline
              :is-dark="true"
              color="gray"
              :attributes="calendarAttrs"
              :month-format="{ month: 'long', year: 'numeric' }"
            />
          </div>

          <!-- Ventas por mes -->
          <div class="panel">
            <canvas id="bestMonthChart"></canvas>
          </div>

          <!-- Clientes nuevos -->
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
import { bus } from '@/event-bus'
import { BASE_URL } from '@/config'

import IconClientes from '@/components/icons/IconClientes.vue'
import IconFacturas from '@/components/icons/IconFacturas.vue'
import IconContabilidad from '@/components/icons/IconContabilidad.vue'
import IconInventario from '@/components/icons/IconInventario.vue'
import IconReporteVentas from '@/components/icons/IconRVentas.vue'
import IconUser from '@/components/icons/IconUser.vue'

/* --------- Estado --------- */
const MONTHS = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']

const inventarioData = ref({ Telas: 0, Hilos: 0, Uniformes: 0 })
const ventasPorMes = ref(MONTHS.reduce((acc, m) => (acc[m] = 0, acc), {}))

const navItems = [
  { label: 'Clientes y Proveedores', icon: IconClientes, route: '/clientes' },
  { label: 'Facturas', icon: IconFacturas, route: '/billpage' },
  { label: 'Contabilidad', icon: IconContabilidad, route: '/accounting' },
  { label: 'Inventario', icon: IconInventario, route: '/mi_inventario' },
  { label: 'Reporte de ventas', icon: IconReporteVentas, route: '/ReporteVentas' },
  { label: 'Gestión de Usuarios', icon: IconUser, route: '/register' },
  { label: 'Pedidos', icon: IconUser, route: '/envios' }
]

const calendarAttrs = ref([{ key: 'hoy', highlight: true, dates: new Date() }])

/* --------- Charts refs --------- */
let pieChart = null
let barChart = null

/* --------- Fetch inventario (pie) --------- */
async function fetchInventarioData () {
  const endpoints = [
    { key: 'Telas', path: '/api/telas/' },
    { key: 'Hilos', path: '/api/hilos/' },
    { key: 'Uniformes', path: '/api/uniformes/' }
  ]
  try {
    const resps = await Promise.all(endpoints.map(e => fetch(`${BASE_URL}${e.path}`)))
    const datasets = await Promise.all(resps.map(r => r.json()))
    datasets.forEach((data, i) => {
      const key = endpoints[i].key
      inventarioData.value[key] = Array.isArray(data)
        ? data.reduce((sum, it) => sum + (Number(it.stock) || 0), 0)
        : 0
    })
  } catch (err) { console.error('Error cargando inventario:', err) }
}

/* --------- Fetch ventas (barras) --------- */
async function fetchVentasMensuales () {
  try {
    const res = await fetch(`${BASE_URL}/api/ventas/evolucion/`)
    const data = await res.json()

    MONTHS.forEach(m => (ventasPorMes.value[m] = 0))

    data.forEach(v => {
      const fecha = new Date(v.dia)
      const m = fecha.toLocaleString('es-ES', { month: 'short' }) // "jul"
      const key = m.charAt(0).toUpperCase() + m.slice(1)          // "Jul"
      if (key in ventasPorMes.value) ventasPorMes.value[key] += Number(v.total) || 0
    })
  } catch (e) { console.error('Error al cargar ventas reales:', e) }
}

/* --------- Render pie --------- */
function renderPieChart () {
  const ctx = document.getElementById('myPieChart')?.getContext('2d')
  if (!ctx) return
  if (pieChart) pieChart.destroy()

  pieChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Telas', 'Hilos', 'Uniformes'],
      datasets: [{
        data: [inventarioData.value.Telas, inventarioData.value.Hilos, inventarioData.value.Uniformes],
        backgroundColor: ['#839A2D', '#2AA68F', '#2B5CA8'],
        borderColor: '#ffffff',
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
}

/* --------- Render barras --------- */
function renderBarChart () {
  const ctx = document.getElementById('bestMonthChart')?.getContext('2d')
  if (!ctx) return
  if (barChart) barChart.destroy()

  const labels = MONTHS
  const values = labels.map(m => ventasPorMes.value[m])
  const currentIdx = new Date().getMonth() // 0-11

  barChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Ventas',
        data: values,
        backgroundColor: (c) => c.dataIndex === currentIdx ? '#2B5CA8' : '#84C8C0',
        borderColor: '#fff',
        borderWidth: 1
      }]
    },
    options: {
      maintainAspectRatio: false,
      plugins: {
        title: { display: true, text: 'Ventas por mes' },
        tooltip: {
          callbacks: {
            label: (ctx) => {
              const v = Number(ctx.parsed.y || 0)
              return ` ${v.toLocaleString('es-CL', { style: 'currency', currency: 'CLP' })}`
            }
          }
        }
      },
      scales: {
        y: { beginAtZero: true, ticks: { callback: v => Number(v).toLocaleString('es-CL') } }
      }
    }
  })
}

/* --------- Mount --------- */
onMounted(async () => {
  await fetchInventarioData()
  await fetchVentasMensuales()
  renderPieChart()
  renderBarChart()
})

/* --------- Eventos para refrescar --------- */
bus.on('inventario-actualizado', async () => {
  await fetchInventarioData()
  if (pieChart) {
    pieChart.data.datasets[0].data = [
      inventarioData.value.Telas,
      inventarioData.value.Hilos,
      inventarioData.value.Uniformes
    ]
    pieChart.update()
  } else { renderPieChart() }
})

bus.on('ventas-actualizadas', async () => {
  await fetchVentasMensuales()
  if (barChart) {
    const labels = MONTHS
    barChart.data.labels = labels
    barChart.data.datasets[0].data = labels.map(m => ventasPorMes.value[m])
    barChart.update()
  } else { renderBarChart() }
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

/* Sidebar */
.sidebar {
  width: 240px;
  background-color: #1e293b;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
}
.logo { width: 180px; height: auto; margin-bottom: 1rem; transition: transform .3s ease-in-out; }
.logo:hover { transform: scale(1.05); }
.nav-links { width: 100%; display: flex; flex-direction: column; gap: .5rem; flex-grow: 1; justify-content: center; }
.nav-item { display: flex; align-items: center; gap: .75rem; padding: .6rem; border-radius: 8px; cursor: pointer; transition: background .3s, transform .3s; color: white; text-decoration: none; }
.nav-item:hover { background-color: #334155; transform: translateX(4px); }
.router-link-exact-active { background-color: #334155; }
.icon-circle { width: 44px; height: 44px; border-radius: 50%; background-color: #64748b; display: flex; align-items: center; justify-content: center; transition: transform .3s; }
.nav-item:hover .icon-circle { transform: scale(1.15); }

/* Main */
.main-area { flex: 1; display: flex; flex-direction: column; }
.topbar { background-color: #1e293b; padding: 1rem; display: flex; justify-content: space-between; align-items: center; }
.view-name { font-size: 1.25rem; font-weight: bold; }
.user-circle { width: 36px; height: 36px; background-color: white; border-radius: 50%; }

.content { display: flex; flex: 1; padding: 1rem; gap: 1rem; overflow: hidden; }

/* Pie */
.chart-area {
  flex: 2;
  background-color: #1e293b;
  border-radius: 16px;
  display: flex; align-items: center; justify-content: center;
}
.chart-area canvas { width: 100% !important; height: 100% !important; }

/* Widgets derecha */
.side-panels{
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  min-height: 0; /* permite que se repartan en columna sin cortar */
}
.panel{
  background-color: #334155;
  border-radius: 12px;
  padding: 1rem;
  display: flex; align-items: center; justify-content: center;
  position: relative;
  min-height: 0;
  overflow: visible; /* no cortar hijos (calendario) */
}

/* Proporciones: calendario más alto para que no se recorte */
.side-panels .panel:nth-child(1){ flex: 0.90; } /* Calendario */
.side-panels .panel:nth-child(2){ flex: 0.90; } /* Ventas por mes */
.side-panels .panel:nth-child(3){ flex: 0.75; } /* Clientes nuevos */

/* Calendario ocupa el panel completo */
.panel--calendar{
  align-items: stretch; /* estira el v-calendar */
  padding: .75rem;
}
.panel--calendar :deep(.vc-container){
  width: 100%;
  height: 80%;
  background: transparent;
  box-shadow: none;
  border: 0;
  border-radius: 10px;
}
.panel--calendar :deep(.vc-pane){ background: transparent; box-shadow: none; }
.panel--calendar :deep(.vc-header){ position: static; }
.panel--calendar { padding: 0.5rem; }                 /* un poco menos de padding */
.panel--calendar :deep(.vc-container) {
  transform: scale(0.85);                             /* << tamaño del calendario */
  transform-origin: top center;                       /* ancla el escalado arriba */
}
/* Canvas ocupa todo el panel */
.panel canvas{ width:100% !important; height:100% !important; }

/* KPI */
.kpi{ text-align:center; width:100%; }
.kpi h3{ margin:0 0 .25rem 0; }
.kpi .value{ font-size:2rem; margin:.5rem 0; color:#2AA68F; }
.kpi small{ color:#cbd5e1; }

/* Responsive: si la pantalla es bajita, seguimos dando aire al calendario */
@media (max-height: 850px){
  .side-panels .panel:nth-child(1){ flex: 1.10; }
  .side-panels .panel:nth-child(2){ flex: 0.85; }
  .side-panels .panel:nth-child(3){ flex: 0.70; }
}
@media (max-height: 780px){
  .side-panels .panel:nth-child(1){ flex: 1.05; }
  .side-panels .panel:nth-child(2){ flex: 0.80; }
  .side-panels .panel:nth-child(3){ flex: 0.70; }
}
</style>
