<template>
  <div class="page-container">
    <NavBar title="REPORTE DE VENTAS" />

    <main class="page-content">
      <!-- FILTROS -->
      <section class="filters-container">
        <div class="filter-group">
          <label for="fecha-inicio">Desde</label>
          <input type="date" id="fecha-inicio" class="input-dark" v-model="filtroFechaInicio" />
        </div>
        <div class="filter-group">
          <label for="fecha-fin">Hasta</label>
          <input type="date" id="fecha-fin" class="input-dark" v-model="filtroFechaFin" />
        </div>
        <div class="flex-group" style="margin-left: auto;">
          <button class="btn btn-secondary" @click="resetFiltros" :disabled="cargando">Limpiar</button>
          <button class="btn btn-primary" @click="filtrarDatos" :disabled="cargando">Filtrar</button>
        </div>
      </section>

      <!-- KPIs -->
      <section class="summary-grid">
        <div class="summary-card">
          <h3>Total de Ventas</h3>
          <p class="valor">Q{{ totalVentas.toLocaleString() }}</p>
        </div>
        <div class="summary-card">
          <h3>Número de Facturas</h3>
          <p class="valor">{{ numeroFacturas }}</p>
        </div>
      </section>

      <!-- Gráficas -->
      <div class="chart-grid">
        <div class="chart-container">
          <h2 class="module-title">Evolución de Ventas</h2>
          <div class="chart-placeholder">
            <canvas id="evolucionVentasChart"></canvas>
          </div>
        </div>

        <div class="chart-container">
          <h2 class="module-title">Productos más vendidos</h2>
          <div class="chart-placeholder">
            <canvas id="productosMasVendidosChart"></canvas>
          </div>
        </div>
        
        <div class="chart-container">
          <h2 class="module-title">Métodos de pago utilizados</h2>
          <div class="chart-placeholder">
            <canvas id="metodosPagoChart"></canvas>
          </div>
        </div>
      </div>
<<<<<<< Updated upstream

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

=======
      
      <!-- Tabla -->
      <section class="module">
        <h2 class="module-title" style="margin-bottom: 1rem;">Tabla de Ventas Detalladas</h2>
        <div class="table-wrapper">
          <div v-if="errorMsg" class="message error-dark">{{ errorMsg }}</div>

          <table v-if="ventas.length" class="table">
            <thead>
              <tr>
                <th>ID Venta</th>
                <th>Producto</th>
                <th>Cliente</th>
                <th>Cantidad</th>
                <th>Precio U.</th>
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
                  <td>{{ venta.cliente_id || 'N/A' }}</td>
                  <td>{{ detalle.cantidad }}</td>
                  <td>Q{{ detalle.precio_unitario }}</td>
                  <td>Q{{ detalle.subtotal }}</td>
                  <td>{{ venta.metodo_pago }}</td>
                  <td>{{ formatearFecha(venta.fecha) }}</td>
                </tr>
              </template>
            </tbody>
          </table>

          <div v-else-if="cargando" class="loading-state">
            Cargando ventas...
          </div>
          <p v-else class="muted-text" style="text-align: center; padding: 2rem;">
            No se encontraron ventas para el periodo seleccionado
          </p>
        </div>
      </section>
>>>>>>> Stashed changes
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import Chart from 'chart.js/auto';
import NavBar from '@/components/NavBar.vue';
import { apiFetch } from '@/utils/api';

const filtroFechaInicio = ref('');
const filtroFechaFin = ref('');
const totalVentas = ref(0);
const numeroFacturas = ref(0);
const ventas = ref([]);
const cargando = ref(false);
const errorMsg = ref('');

let evolucionChartInstance = null;
let productosChartInstance = null;
let metodosPagoChartInstance = null;

// --- Helper para obtener variables CSS ---
const getCssVar = (varName) => getComputedStyle(document.documentElement).getPropertyValue(varName).trim();

const formatearFecha = (fecha) => {
  if (!fecha) return '';
  return new Date(fecha).toLocaleDateString('es-GT');
};

<<<<<<< Updated upstream
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
          labels: data.map((item) => item.categoria),
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
=======
const filtrarDatos = async () => {
  errorMsg.value = '';
  if (!filtroFechaInicio.value || !filtroFechaFin.value) {
    errorMsg.value = 'Por favor, seleccione ambas fechas.';
    return;
>>>>>>> Stashed changes
  }
  await Promise.all([
    cargarVentas(),
    cargarEvolucionVentas(),
    cargarProductosMasVendidos(),
    cargarMetodosPago()
  ]);
};

const cargarVentas = async () => {
  cargando.value = true;
  errorMsg.value = '';
  try {
    const data = await apiFetch(`/api/ventas/por-fecha/?fecha_inicio=${filtroFechaInicio.value}&fecha_fin=${filtroFechaFin.value}`);
    totalVentas.value = data.total_ventas ?? 0;
    numeroFacturas.value = data.numero_facturas ?? 0;
    ventas.value = data.ventas ?? [];
  } catch (err) {
    console.error('Error al obtener las ventas:', err);
    errorMsg.value = 'No se pudieron cargar las ventas.';
  } finally {
    cargando.value = false;
  }
};

const cargarEvolucionVentas = async () => {
  try {
    const data = await apiFetch(`/api/ventas/evolucion/?fecha_inicio=${filtroFechaInicio.value}&fecha_fin=${filtroFechaFin.value}`);
    renderEvolucionChart(data || []);
  } catch (error) { console.error('Error al cargar evolución de ventas:', error); }
};

const cargarProductosMasVendidos = async () => {
  try {
    const data = await apiFetch(`/api/ventas/productos-mas-vendidos/?fecha_inicio=${filtroFechaInicio.value}&fecha_fin=${filtroFechaFin.value}`);
    renderProductosChart(data || []);
  } catch (error) { 
    console.error('Error al cargar productos más vendidos:', error); 
    renderProductosChart([]); 
  }
};

const cargarMetodosPago = async () => {
  try {
    const data = await apiFetch('/api/ventas/metodos-pago/');
    renderMetodosPagoChart(data || []);
  } catch (error) { console.error('Error al cargar métodos de pago:', error); }
};

// --- Métodos para renderizar las gráficas ---
const renderEvolucionChart = (data) => {
  evolucionChartInstance?.destroy?.();
  const ctx = document.getElementById('evolucionVentasChart')?.getContext('2d');
  if (!ctx) return;

  const textColor = getCssVar('--color-text-light-primary');
  const primaryColor = getCssVar('--color-action-primary');
  const primaryColorTransparent = 'rgba(43, 92, 168, 0.2)'; // Versión transparente de --color-action-primary

  evolucionChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.map((item) => formatearFecha(item.dia)),
      datasets: [{
        label: 'Total de Ventas por Día',
        data: data.map((item) => item.total),
        borderColor: primaryColor,
        backgroundColor: primaryColorTransparent,
        tension: 0.1,
        fill: true
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { ticks: { color: textColor } },
        x: { ticks: { color: textColor } }
      },
      plugins: { legend: { labels: { color: textColor } } }
    }
  });
};

const renderProductosChart = (data) => {
  productosChartInstance?.destroy?.();
  const ctx = document.getElementById('productosMasVendidosChart')?.getContext('2d');
  if (!ctx) return;

  const textColor = getCssVar('--color-text-light-primary');

  productosChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.map((item) => item.producto__nombre),
      datasets: [{
        label: 'Cantidad Vendida',
        data: data.map((item) => item.total_vendido),
        backgroundColor: [
          getCssVar('--color-action-primary'),
          getCssVar('--color-action-secondary'),
          getCssVar('--color-icon-edit'),
          getCssVar('--navbar-background'),
          getCssVar('--color-action-danger'),
        ]
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      scales: {
        y: { ticks: { color: textColor } },
        x: { ticks: { color: textColor } }
      },
      plugins: { legend: { labels: { color: textColor } } }
    }
  });
};

const renderMetodosPagoChart = (data) => {
  metodosPagoChartInstance?.destroy?.();
  const ctx = document.getElementById('metodosPagoChart')?.getContext('2d');
  if (!ctx) return;

  const textColor = getCssVar('--color-text-light-primary');

  metodosPagoChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: data.map((item) => item.metodo_pago),
      datasets: [{
        data: data.map((item) => item.cantidad),
        backgroundColor: [
          getCssVar('--color-action-primary'),
          getCssVar('--color-action-secondary'),
          getCssVar('--color-icon-edit'),
          getCssVar('--color-action-danger'),
        ]
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: 'top', labels: { color: textColor } } }
    }
  });
};

const resetFiltros = () => {
  const hoy = new Date();
  const primerDia = new Date(hoy.getFullYear(), hoy.getMonth(), 1);
  const ultimoDia = new Date(hoy.getFullYear(), hoy.getMonth() + 1, 0);
  const fmt = (f) => f.toISOString().slice(0, 10);
  filtroFechaInicio.value = fmt(primerDia);
  filtroFechaFin.value = fmt(ultimoDia);
  filtrarDatos();
};

onMounted(() => {
  resetFiltros();
});

onBeforeUnmount(() => {
  evolucionChartInstance?.destroy?.();
  productosChartInstance?.destroy?.();
  metodosPagoChartInstance?.destroy?.();
});
</script>

<style scoped>
.page-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.chart-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: var(--spacing-xl);
  margin-bottom: var(--spacing-xl);
}

.loading-state {
  text-align: center;
  padding: 2rem;
  color: var(--color-text-light-secondary);
}
</style>