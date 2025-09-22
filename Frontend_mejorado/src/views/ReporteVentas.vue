<template>
  <div class="reporte-ventas">
    <!-- NavBar unificado -->
    <NavBar title="REPORTE DE VENTAS" />

    <main class="main-content">
      <!-- FILTROS -->
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
          <button class="btn btn--primary" @click="filtrarDatos" :disabled="cargando">Filtrar</button>
          <button class="btn btn--muted" @click="resetFiltros" :disabled="cargando">Limpiar</button>
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

        <!-- se agrega un color -->
        <div v-if="errorMsg" class="no-data" style="color:#fca5a5">{{ errorMsg }}</div>

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
import Chart from 'chart.js/auto'
import NavBar from '@/components/NavBar.vue'
import { apiFetch } from '@/utils/api'

export default {
  components: { NavBar },
  data() {
    return {
      // filtros/fechas
      fechaInicio: '',
      fechaFin: '',
      filtroFechaInicio: '',
      filtroFechaFin: '',
      // KPI/tabla
      totalVentas: 0,
      numeroFacturas: 0,
      ventas: [],
      // ui
      cargando: false,
      errorMsg: '',
      paginaActual: 1,
      totalPaginas: 1,
      // charts
      evolucionChartInstance: null,
      productosChartInstance: null,
      metodosPagoChartInstance: null,
    }
  },

  mounted() {
    // Rango: mes actual por defecto
    const hoy = new Date()
    const primerDia = new Date(hoy.getFullYear(), hoy.getMonth(), 1)
    const ultimoDia = new Date(hoy.getFullYear(), hoy.getMonth() + 1, 0)
    const fmt = (f) =>
      `${f.getFullYear()}-${String(f.getMonth() + 1).padStart(2, '0')}-${String(f.getDate()).padStart(2, '0')}`
    this.filtroFechaInicio = fmt(primerDia)
    this.filtroFechaFin = fmt(ultimoDia)
    this.filtrarDatos()
  },

  beforeUnmount() {
    this.evolucionChartInstance?.destroy?.()
    this.productosChartInstance?.destroy?.()
    this.metodosPagoChartInstance?.destroy?.()
  },

  methods: {
    formatearFecha(fecha) {
      if (!fecha) return ''
      return new Date(fecha).toLocaleDateString('es-GT')
    },

    async filtrarDatos() {
      this.errorMsg = ''
      this.fechaInicio = this.filtroFechaInicio
      this.fechaFin = this.filtroFechaFin
      if (!this.fechaInicio || !this.fechaFin) {
        this.errorMsg = 'Por favor, seleccioná ambas fechas.'
        return
      }
      await Promise.all([
        this.cargarVentas(),
        this.cargarEvolucionVentas(),
        this.cargarProductosMasVendidos(),
        this.cargarMetodosPago()
      ])
    },

    async cargarVentas() {
      this.cargando = true
      this.errorMsg = ''
      try {
        const data = await apiFetch(
          `/api/ventas/por-fecha/?fecha_inicio=${this.fechaInicio}&fecha_fin=${this.fechaFin}`
        )
        this.totalVentas = data.total_ventas ?? 0
        this.numeroFacturas = data.numero_facturas ?? 0
        this.ventas = data.ventas ?? []
        // si luego hay paginación real, aquí se calculan paginaActual/totalPaginas
      } catch (err) {
        console.error('Error al obtener las ventas:', err)
        this.errorMsg = 'No se pudieron cargar las ventas.'
      } finally {
        this.cargando = false
      }
    },

    async cargarEvolucionVentas() {
      try {
        const data = await apiFetch(
          `/api/ventas/evolucion/?fecha_inicio=${this.fechaInicio}&fecha_fin=${this.fechaFin}`
        )
        this.renderEvolucionChart(data || [])
      } catch (error) {
        console.error('Error al cargar evolución de ventas:', error)
      }
    },

    async cargarProductosMasVendidos() {
      try {
        const data = await apiFetch('/api/ventas/productos-mas-vendidos/')
        this.renderProductosChart(data || [])
      } catch (error) {
        console.error('Error al cargar productos más vendidos:', error)
      }
    },

    async cargarMetodosPago() {
      try {
        const data = await apiFetch('/api/ventas/metodos-pago/')
        this.renderMetodosPagoChart(data || [])
      } catch (error) {
        console.error('Error al cargar métodos de pago:', error)
      }
    },

    renderEvolucionChart(data) {
      this.evolucionChartInstance?.destroy?.()
      const ctx = document.getElementById('evolucionVentasChart')?.getContext('2d')
      if (!ctx) return
      this.evolucionChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.map((item) => this.formatearFecha(item.dia)),
          datasets: [
            {
              label: 'Total de Ventas por Día',
              data: data.map((item) => item.total),
              /*color en script*/
              borderColor: '#2AA68F',
              backgroundColor: 'rgba(42, 166, 143, 0.2)',
              tension: 0.1,
              fill: true
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            /*color en script*/
            y: { ticks: { color: '#FFF' } },
            x: { ticks: { color: '#FFF' } }
          },
          /*color en script*/
          plugins: { legend: { labels: { color: '#FFF' } } }
        }
      })
    },

    renderProductosChart(data) {
      this.productosChartInstance?.destroy?.()
      const ctx = document.getElementById('productosMasVendidosChart')?.getContext('2d')
      if (!ctx) return
      this.productosChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.map((item) => item.producto__nombre),
          datasets: [
            {
              label: 'Cantidad Vendida',
              data: data.map((item) => item.total_vendido),
              /*color en script*/
              backgroundColor: ['#2B5CA8', '#374666', '#83A4CC', '#C9E8F5', '#84C8C0']
            }
          ]
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
      this.metodosPagoChartInstance?.destroy?.()
      const ctx = document.getElementById('metodosPagoChart')?.getContext('2d')
      if (!ctx) return
      this.metodosPagoChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: data.map((item) => item.metodo_pago),
          datasets: [
            {
              data: data.map((item) => item.cantidad),
              /*color en script*/
              backgroundColor: ['#839A2D', '#2AA68F', '#2B5CA8', '#C9E8F5']
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { labels: { color: '#FFF' } } }
        }
      })
    },

    // paginación futura (placeholder)
    cambiarPagina(nueva) { this.paginaActual = nueva },

    resetFiltros() {
      const hoy = new Date()
      const primerDia = new Date(hoy.getFullYear(), hoy.getMonth(), 1)
      const ultimoDia = new Date(hoy.getFullYear(), hoy.getMonth() + 1, 0)
      const fmt = (f) =>
        `${f.getFullYear()}-${String(f.getMonth() + 1).padStart(2, '0')}-${String(f.getDate()).padStart(2, '0')}`
      this.filtroFechaInicio = fmt(primerDia)
      this.filtroFechaFin = fmt(ultimoDia)
      this.filtrarDatos()
    }
  }
}
</script>

<style scoped>
.reporte-ventas{
  background: var(--color-octonary); /*fondo pantalla reporteventas*/
  color: #fff; /*texto "pagina 1 de 1" */
  min-height: 100vh;
  font-family: 'Kollektif', sans-serif;
}

.main-content{
  padding: 20px;
  display: grid;
  gap: 20px;
}

/* FILTROS */
.filtros-container{
  display: flex; flex-wrap: wrap; gap: 14px 20px;
  align-items: end;
  background: #1e293b; /*fondo cuadro filtros*/
  border: 1px solid #223043; /*borde cuadro filtros*/
  border-radius: 12px;
  padding: 14px 16px;
}
.filtro{ display:flex; flex-direction:column; gap:6px; min-width: 220px; }
.filtro label{
  font-weight: 800;
  color: #fff; /*texto filtro "desde, hasta" */
}
.filtro input{
  padding: 10px 12px; border-radius: 10px;
  border: 1px solid #334155; /*borde input filtro fecha*/
  background: #0b1326; /*fondo input filtro fecha*/
  color: #fff; /*texto input filtro fecha*/
  outline: none;
}
.filtro input:focus{
  border-color: var(--color-quinary); /*borde interior input filtro fecha seleccionado*/
  box-shadow: 0 0 0 3px rgba(43,92,168,.25); /*borde exterior input filtro fecha seleccionado*/
}
.filtro-actions{ display:flex; gap:10px; margin-left: auto; }
.btn{ padding:10px 14px; border-radius:10px; font-weight:800; border:none; cursor:pointer; }
.btn--primary{
  background: var(--color-quinary); /*fondo boton "filtrar" */
  color:#fff; /*texto "filtrar" */
}
.btn--muted{
  background: #334155; /*fondo boton "limpiar" */
  color:#fff; /*texto "limpiar"*/
}

/* KPIs */
.kpi-container{ display:flex; gap:20px; flex-wrap: wrap; }
.kpi-card{
  background:#1e2236; /*fondo tarjetas "total ventas, numero facturas"*/
  padding:20px; border-radius:12px;
  border:1px solid #223043; /*borde tarjetas "total ventas, numero facturas"*/
}
.kpi-card.principal{ flex:1; min-width:260px; }
.kpi-card h3{
  margin:0;
  color: var(--color-quinary); /*titulo tarjetas "total ventas, numero facturas"*/
}
.kpi-card .valor{
  font-size:2rem; font-weight:800;
  color:#fff; /*numeros tarjetas "total ventas, numero facturas"*/
}
.kpi-card .descripcion{
  font-size:.9rem;
  color:#cbd5e1; /*subtexto tarjetas "total ventas, numero facturas"*/
}

/* Charts */
.chart-container{
  background:#1e2236; /*fondo tarjetas con graficas "evolucion ventas, productos vendidos, metodos pago"*/
  padding:20px; border-radius:12px;
  border:1px solid #223043; /*borde tarjetas con graficas "evolucion ventas, productos vendidos, metodos pago"*/
}
.chart-container h2{ margin-top:0; color:#fff; } /*titulos graficas "evolucion ventas, productos vendidos, metodos pago" */
.chart-placeholder{
  background:#2c3148; /*fondo de graficas*/
  border-radius:10px; height:280px;
  display:flex; align-items:center; justify-content:center; overflow:hidden;
}
.chart-placeholder.shorter{ height:200px; }
.chart-placeholder canvas{ width:100% !important; height:100% !important; }

/* Tabla */
.table-container{
  background:#1e2236; /*fondo ficha "tabla de ventas detalladas" */
  padding:20px; border-radius:12px;
  border:1px solid #223043; /*borde ficha "tabla de ventas detalladas" */
  overflow-x:auto;
}
table{ width:100%; border-collapse: collapse; }
th, td{
  padding:12px;
  border:1px solid #2c3148; /*opciones bordes tabla "tabla de ventas detalladas" */
}
th{
  background: var(--color-senary); /*nada*/
  color:#fff; /*nada*/
  text-align:left;
}
tr:nth-child(even){ background:#2b2f40; } /*nada*/
tr:nth-child(odd){ background:#1f2336; } /*asdf*/
tr:hover{ background:#3c4c6e; } /*nada*/

/* Paginación */
.pagination{
  display:flex; justify-content:center; gap:12px; margin-top:16px; align-items:center;
}
.pagination button{
  background: var(--color-quinary); /*nada*/
  color:#fff; /*texto botones "anterior/siguiente"*/
  border:none;
  padding:8px 14px; border-radius:8px; cursor:pointer;
}
.pagination button:disabled{ background:#475569; /*fondo botones "anterior/siguiente" */
  cursor:not-allowed;
}

.loading{ display:grid; place-items:center; gap:8px; padding:20px; }
.spinner{
  width:28px; height:28px; border-radius:50%;
  border:3px solid rgba(255,255,255,.25); /*nada*/
  border-top-color:#fff; /*nada*/
  animation: spin 1s linear infinite;
}
@keyframes spin{ to { transform: rotate(360deg); } }

.no-data{
  color:#cbd5e1; /*nada*/
  text-align:center;
  }
</style>
