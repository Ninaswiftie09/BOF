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
          <div class="panel">Calendario</div>
          <div class="panel">Gráfica del mejor mes</div>
          <div class="panel">Algún otro apartado</div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import Chart from 'chart.js/auto'

import IconClientes from '@/components/icons/IconClientes.vue'
import IconFacturas from '@/components/icons/IconFacturas.vue'
import IconContabilidad from '@/components/icons/IconContabilidad.vue'
import IconInventario from '@/components/icons/IconInventario.vue'
import IconReporteVentas from '@/components/icons/IconRVentas.vue'

const navItems = [
  { label: 'Clientes y Proveedores', icon: IconClientes, route: '/clientes' },
  { label: 'Facturas', icon: IconFacturas, route: '/billpage' },
  { label: 'Contabilidad', icon: IconContabilidad, route: '/accounting' },
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
      maintainAspectRatio: false,    // permite estirar la gráfica
      plugins: {
        legend: { position: 'top' },
        title: { display: true, text: 'Inventario' }
      }
    }
  })
})
</script>

<style scoped>
.dashboard-container {
  display: flex;
  height: 100vh;        /* ocupa toda la ventana */
  overflow: hidden;     /* nada de scroll global */
  background: #0a0f2c;
  color: white;
  font-family: 'Segoe UI', sans-serif;
}

/* Sidebar igual que antes */
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
.nav-links { width: 100%; display: flex; flex-direction: column; gap: 1rem; }
.nav-item {
  display: flex; align-items: center; gap: 0.5rem;
  padding: 0.5rem; border-radius: 8px; cursor: pointer;
  transition: background 0.2s; color: white; text-decoration: none;
}
.nav-item:hover,
.router-link-exact-active { background-color: #334155; }
.icon-circle {
  width: 36px; height: 36px; border-radius: 50%;
  background-color: #64748b; display: flex;
  align-items: center; justify-content: center;
}

/* Main area */
.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;      /* quita scroll interno */
}

/* Header fijo */
.topbar {
  flex: 0 0 60px;        /* altura fija */
  background-color: #1e293b;
  display: flex; justify-content: space-between;
  align-items: center; padding: 0 1rem;
}
.view-name { font-size: 1.25rem; font-weight: bold; }
.user-circle {
  width: 36px; height: 36px;
  background-color: white; border-radius: 50%;
}

/* Content toma todo lo restante */
.content {
  flex: 1;               /* ocupa todo lo que deje el header */
  display: flex;
  gap: 1rem;
  padding: 1rem;
  overflow: hidden;      /* nada de scroll interno */
  align-items: stretch;  /* forzar mismo alto a children */
}

/* Gráfica ocupa 2/3 del ancho y todo el alto */
.chart-area {
  flex: 2;
  background-color: #1e293b;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
/* Canvas estira para llenar container */
.chart-area canvas {
  width: 100% !important;
  height: 100% !important;
}

/* Paneles laterales ocupan 1/3 del ancho, divididos en tres bloques iguales */
.side-panels {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  overflow: hidden;
}
.panel {
  flex: 1;               /* cada una igual altura */
  background-color: #334155;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  font-size: 1rem;
}
</style>
