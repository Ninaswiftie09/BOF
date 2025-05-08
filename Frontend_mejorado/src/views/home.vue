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
        <div class="view-name"> HOME</div>
        <input class="search" placeholder="Buscar elementos exactos" />
        <div class="user-circle"></div>
      </header>

      <section class="content">
        <div class="chart-area">
          <canvas id="myPieChart"></canvas>
        </div>

        <div class="side-panels">
          <div class="panel"> Calendario</div>
          <div class="panel"> Gráfica del mejor mes</div>
          <div class="panel"> Algún otro apartado</div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import Chart from 'chart.js/auto'

// Importación de íconos SVG para menu flotante
import IconCalculadora from '@/components/icons/IconCalculadora.vue'
import IconClientes from '@/components/icons/IconClientes.vue'
import IconFacturas from '@/components/icons/IconFacturas.vue'
import IconContabilidad from '@/components/icons/IconContabilidad.vue'
import IconInventario from '@/components/icons/IconInventario.vue'
import IconReporteVentas from '@/components/icons/IconRVentas.vue'


// Lista de elementos de navegación
const navItems = [
  { label: 'Clientes', icon: IconClientes, route: '/clientes' },
  { label: 'Facturas', icon: IconFacturas, route: '/billpage' },
  { label: 'contabilidad', icon: IconContabilidad, route: '/accounting' },
  { label: 'Calculadora', icon: IconCalculadora, route: '/calculadora' },
  { label: 'Inventario', icon: IconInventario, route: '/mi_inventario' },
  { label: 'Reporte de ventas', icon: IconReporteVentas, route: '/ReporteVentas' }
]

onMounted(() => {
  const ctx = document.getElementById('myPieChart').getContext('2d')
  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Libro de Matemáticas', 'Cuaderno de Dibujo', 'Marcadores', 'Pinturas', 'Tijeras'],
      datasets: [{
        data: [5, 15, 4, 10, 6],
        backgroundColor: ['#839A2D', '#2AA68F', '#84C8C0', '#C9E8F5', '#2B5CA8'],
        borderColor: '#fff',
        borderWidth: 1
      }]
    },
    options: {
      plugins: {
        legend: {
          position: 'top'
        },
        title: {
          display: true,
          text: 'Inventario'
        }
      }
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

.logo {
  width: 250px;
  height: 150px;
  margin-bottom: 1rem;
}

.nav-links {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
  color: white;
  text-decoration: none;
}

.nav-item:hover,
.router-link-exact-active {
  background-color: #334155;
}

.icon-circle {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.topbar {
  background-color: #1e293b;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.view-name {
  font-size: 1.25rem;
  font-weight: bold;
}

.search {
  padding: 0.5rem;
  border-radius: 8px;
  border: none;
  width: 250px;
}

.user-circle {
  width: 36px;
  height: 36px;
  background-color: white;
  border-radius: 50%;
}

.content {
  display: flex;
  padding: 2rem;
  gap: 2rem;
}

.chart-area {
  flex: 2;
  background-color: #1e293b;
  padding: 2rem;
  border-radius: 16px;
}

.side-panels {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.panel {
  background-color: #334155;
  padding: 1rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 500;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
