<template>
  <div class="dashboard-container">
    <aside class="sidebar">
      <div class="logo">LOGO</div>
      <nav class="nav-links">
        <div class="nav-item" v-for="item in navItems" :key="item.label">
          <div class="icon-circle">
            <img :src="item.icon" alt="icon" />
          </div>
          <span>{{ item.label }}</span>
        </div>
      </nav>
    </aside>

    <main class="main-area">
      <header class="topbar">
        <div class="view-name">NOMBRE VISTA</div>
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
const navItems = [
  { label: 'Clientes', icon: '/icons/clientes.svg' },
  { label: 'Facturas', icon: '/icons/facturas.svg' },
  { label: 'Reportes', icon: '/icons/reportes.svg' },
  { label: 'Calculadora', icon: '/icons/calculadora.svg' },
  { label: 'Inventario', icon: '/icons/inventario.svg' }
]
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
  font-size: 1.5rem;
  font-weight: bold;
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
}

.nav-item:hover {
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

.icon-circle img {
  width: 20px;
  height: 20px;
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