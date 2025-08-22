<template>
  <div class="reporte-ventas">
    <!-- NavBar unificado (solo barra) -->
    <NavBar title="REPORTE DE VENTAS" />

    <main class="main-content">
      <!-- FILTROS (debajo del NavBar) -->
      <div class="filtros-container">
        <div class="filtro">
          <label for="fecha-inicio">Desde</label>
          <input type="date" id="fecha-inicio" v-model="filtroFechaInicio" />
        </div>
        <div class="filtro">
          <label for="fecha-fin">Hasta</label>
          <input type="date" id="fecha-fin" v-model="filtroFechaFin" />
        </div>
        <div class="filtro-actions">
          <button class="btn btn--primary" @click="filtrarDatos">Filtrar</button>
          <button class="btn btn--muted" @click="resetFiltros">Limpiar</button>
        </div>
      </div>

      <!-- KPIs -->
      <div class="kpi-container">
        <div class="kpi-card principal">
          <h3>Total de Ventas</h3>
          <p class="valor">Q{{ totalVentas }}</p>
          <p class="descripcion">Solo ventas</p>
        </div>
        <div class="kpi-card principal">
          <h3>Número de Facturas</h3>
          <p class="valor">{{ numeroFacturas }}</p>
          <p class="descripcion">Tickets de venta emitidos</p>
        </div>
      </div>

      <!-- Gráficas -->
      <div class="chart-container">
        <h2>Evolución de Ventas</h2>
        <div class="chart-placeholder">
          <canvas id="evolucionVentasChart"></canvas>
        </div>
      </div>

      <div class="chart-container">
        <h2>Productos más vendidos</h2>
        <div class="chart-placeholder">
          <canvas id="productosMasVendidosChart"></canvas>
        </div>
      </div>

      <div class="chart-container">
        <h2>Métodos de pago utilizados</h2>
        <div class="chart-placeholder shorter">
          <canvas id="metodosPagoChart"></canvas>
        </div>
      </div>

      <!-- Tabla -->
      <div class="table-container">
        <h2>Tabla de Ventas Detalladas</h2>
        <table v-if="ventas.length" class="dark-table">
          <thead>
            <tr>
              <th>ID Venta</th>
              <th>Producto</th>
              <th>Cliente</th>
              <th>Cantidad</th>
              <th>Precio Unitario</th>
              <th>Total</th>
              <th>Método Pago</th>
              <th>Fecha</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="venta in ventas" :key="venta.id">
              <tr v-for="(detalle, i) in venta.detalles" :key="`${venta.id}-${i}`">
                <td>{{ venta.id }}</td>
                <td>{{ detalle.producto.nombre }}</td>
                <td>{{ venta.cliente_id || 'No registrado' }}</td>
                <td>{{ detalle.cantidad }}</td>
                <td>Q{{ detalle.precio_unitario }}</td>
                <td>Q{{ detalle.subtotal }}</td>
                <td>{{ venta.metodo_pago }}</td>
                <td>{{ formatearFecha(venta.fecha) }}</td>
              </tr>
            </template>
          </tbody>
        </table>

        <div v-else-if="cargando" class="loading">
          <div class="spinner"></div>
          <p>Cargando ventas...</p>
        </div>
        <p v-else class="no-data">No se encontraron ventas para el periodo seleccionado</p>

        <div class="pagination">
          <button :disabled="paginaActual === 1" @click="cambiarPagina(paginaActual - 1)">
            « Anterior
          </button>
          <span>Página {{ paginaActual }} de {{ totalPaginas }}</span>
          <button :disabled="paginaActual === totalPaginas" @click="cambiarPagina(paginaActual + 1)">
            Siguiente »
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios'
import Chart from 'chart.js/auto'
import NavBar from '@/components/NavBar.vue'

export default {
  components: { NavBar },
  data() {
    return {
      fechaInicio: '',
      fechaFin: '',
      filtroFechaInicio: '',
      filtroFechaFin: '',
      totalVentas: 0,
      numeroFacturas: 0,
      ventas: [],
      cargando: false,
      paginaActual: 1,
      totalPaginas: 1,
      evolucionChartInstance: null,
      productosChartInstance: null,
      metodosPagoChartInstance: null,
    }
  },
  methods: {
    formatearFecha(fecha) {
      if (!fecha) return ''
      return new Date(fecha).toLocaleDateString('es-GT')
    },

    filtrarDatos() {
      this.fechaInicio = this.filtroFechaInicio
      this.fechaFin = this.filtroFechaFin
      if (this.fechaInicio && this.fechaFin) {
        this.cargarVentas()
        this.cargarEvolucionVentas()
        this.cargarProductosMasVendidos()
        this.cargarMetodosPago()
      } else {
        alert('Por favor, seleccioná ambas fechas.')
      }
    },

    async cargarVentas() {
      this.cargando = true
      try {
        const response = await axios.get('http://localhost:8000/api/ventas/por-fecha/', {
          params: { fecha_inicio: this.fechaInicio, fecha_fin: this.fechaFin },
        })
        this.totalVentas = response.data.total_ventas
        this.numeroFacturas = response.data.numero_facturas
        this.ventas = response.data.ventas
        // si tu API devuelve paginación, actualiza aquí paginaActual/totalPaginas
      } catch (error) {
        console.error('Error al obtener las ventas:', error)
      } finally {
        this.cargando = false
      }
    },

    async cargarEvolucionVentas() {
      try {
        const res = await axios.get('/api/ventas/evolucion/', {
          params: { fecha_inicio: this.fechaInicio, fecha_fin: this.fechaFin },
        })
        this.renderEvolucionChart(res.data)
      } catch (error) {
        console.error('Error al cargar evolución de ventas:', error)
      }
    },

    async cargarProductosMasVendidos() {
      try {
        const res = await axios.get('/api/ventas/productos-mas-vendidos/')
        this.renderProductosChart(res.data)
      } catch (error) {
        console.error('Error al cargar productos más vendidos:', error)
      }
    },

    async cargarMetodosPago() {
      try {
        const res = await axios.get('/api/ventas/metodos-pago/')
        this.renderMetodosPagoChart(res.data)
      } catch (error) {
        console.error('Error al cargar métodos de pago:', error)
      }
    },

    renderEvolucionChart(data) {
      if (this.evolucionChartInstance) this.evolucionChartInstance.destroy()
      const ctx = document.getElementById('evolucionVentasChart')?.getContext('2d')
      if (!ctx) return
      this.evolucionChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.map(item => this.formatearFecha(item.dia)),
          datasets: [{
            label: 'Total de Ventas por Día',
            data: data.map(item => item.total),
            borderColor: '#2AA68F',
            backgroundColor: 'rgba(42, 166, 143, 0.2)',
            tension: 0.1,
            fill: true,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: { ticks: { color: '#FFF' } },
            x: { ticks: { color: '#FFF' } }
          },
          plugins: { legend: { labels: { color: '#FFF' } } }
        }
      })
    },

    renderProductosChart(data) {
      if (this.productosChartInstance) this.productosChartInstance.destroy()
      const ctx = document.getElementById('productosMasVendidosChart')?.getContext('2d')
      if (!ctx) return
      this.productosChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.map(item => item.producto__nombre),
          datasets: [{
            label: 'Cantidad Vendida',
            data: data.map(item => item.total_vendido),
            backgroundColor: ['#2B5CA8', '#374666', '#83A4CC', '#C9E8F5', '#84C8C0'],
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'y',
          scales: {
            y: { ticks: { color: '#FFF' } },
            x: { ticks: { color: '#FFF' } }
          },
          plugins: { legend: { labels: { color: '#FFF' } } }
        }
      })
    },

    renderMetodosPagoChart(data) {
      if (this.metodosPagoChartInstance) this.metodosPagoChartInstance.destroy()
      const ctx = document.getElementById('metodosPagoChart')?.getContext('2d')
      if (!ctx) return
      this.metodosPagoChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: data.map(item => item.metodo_pago),
          datasets: [{
            data: data.map(item => item.cantidad),
            backgroundColor: ['#839A2D', '#2AA68F', '#2B5CA8', '#C9E8F5'],
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { labels: { color: '#FFF' } } }
        }
      })
    },

    // si luego activas paginación real:
    cambiarPagina(nueva) { this.paginaActual = nueva }
    // y calcula totalPaginas según tu backend
  }
}
</script>

<style scoped>
.reporte-ventas{
  background: var(--color-octonary);
  color: #fff;
  min-height: 100vh;
  font-family: 'Kollektif', sans-serif;
}

/* Contenido general (NavBar no es fijo, así que no hace falta padding-top) */
.main-content{
  padding: 20px;
  display: grid;
  gap: 20px;
}

/* FILTROS */
.filtros-container{
  display: flex; flex-wrap: wrap; gap: 14px 20px;
  align-items: end;
  background: #1e293b; border: 1px solid #223043; border-radius: 12px;
  padding: 14px 16px;
}
.filtro{ display:flex; flex-direction:column; gap:6px; min-width: 220px; }
.filtro label{ font-weight: 800; color: #fff; }
.filtro input{
  padding: 10px 12px; border-radius: 10px; border: 1px solid #334155;
  background: #0b1326; color: #fff; outline: none;
}
.filtro input:focus{ border-color: var(--color-quinary); box-shadow: 0 0 0 3px rgba(43,92,168,.25); }
.filtro-actions{ display:flex; gap:10px; margin-left: auto; }
.btn{ padding:10px 14px; border-radius:10px; font-weight:800; border:none; cursor:pointer; }
.btn--primary{ background: var(--color-quinary); color:#fff; }
.btn--muted{ background: #334155; color:#fff; }

/* KPIs */
.kpi-container{ display:flex; gap:20px; flex-wrap: wrap; }
.kpi-card{
  background:#1e2236; padding:20px; border-radius:12px; border:1px solid #223043;
}
.kpi-card.principal{ flex:1; min-width:260px; }
.kpi-card h3{ margin:0; color: var(--color-quinary); }
.kpi-card .valor{ font-size:2rem; font-weight:800; color:#fff; }
.kpi-card .descripcion{ font-size:.9rem; color:#cbd5e1; }

/* Charts */
.chart-container{
  background:#1e2236; padding:20px; border-radius:12px; border:1px solid #223043;
}
.chart-container h2{ margin-top:0; color:#fff; }
.chart-placeholder{
  background:#2c3148; border-radius:10px; height:280px;
  display:flex; align-items:center; justify-content:center; overflow:hidden;
}
.chart-placeholder.shorter{ height:200px; }
.chart-placeholder canvas{ width:100% !important; height:100% !important; }

/* Tabla */
.table-container{
  background:#1e2236; padding:20px; border-radius:12px; border:1px solid #223043; overflow-x:auto;
}
table{ width:100%; border-collapse: collapse; }
th, td{ padding:12px; border:1px solid #2c3148; }
th{ background: var(--color-senary); color:#fff; text-align:left; }
tr:nth-child(even){ background:#2b2f40; }
tr:nth-child(odd){ background:#1f2336; }
tr:hover{ background:#3c4c6e; }

/* Paginación */
.pagination{
  display:flex; justify-content:center; gap:12px; margin-top:16px; align-items:center;
}
.pagination button{
  background: var(--color-quinary); color:#fff; border:none;
  padding:8px 14px; border-radius:8px; cursor:pointer;
}
.pagination button:disabled{ background:#475569; cursor:not-allowed; }

.loading{ display:grid; place-items:center; gap:8px; padding:20px; }
.spinner{
  width:28px; height:28px; border-radius:50%;
  border:3px solid rgba(255,255,255,.25); border-top-color:#fff; animation: spin 1s linear infinite;
}
@keyframes spin{ to { transform: rotate(360deg); } }

.no-data{ color:#cbd5e1; text-align:center; }
</style>
