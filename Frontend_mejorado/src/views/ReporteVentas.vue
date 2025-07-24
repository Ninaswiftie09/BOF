<template>
  <div class="reporte-ventas">
    <!-- HEADER unificado -->
    <header class="top-bar">
      <img
        src="@/assets/logo_bof_blanco.png"
        alt="Logo del cliente"
        class="logo"
        @click="goHome"
      />
      <h1>REPORTE DE VENTAS</h1>
      <button class="avatar-btn"></button>
    </header>

    <!-- FILTROS -->
    <div class="filtros-container">
      <div class="filtro">
        <label for="fecha-inicio">Desde:</label>
        <input type="date" id="fecha-inicio" v-model="filtroFechaInicio" />
      </div>
      <div class="filtro">
        <label for="fecha-fin">Hasta:</label>
        <input type="date" id="fecha-fin" v-model="filtroFechaFin" />
      </div>
      <button class="btn-filtrar" @click="filtrarDatos">Filtrar</button>
      <button class="btn-reset" @click="resetFiltros">Limpiar</button>
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
        <div class="chart-overlay">Gráfica de evolución de ventas por días, semanas o meses</div>
      </div>
    </div>

    <div class="chart-container">
      <h2>Productos más vendidos</h2>
      <div class="chart-placeholder">
        <div class="chart-overlay">Top 5 o 10 productos más vendidos</div>
      </div>
    </div>

    <div class="chart-container">
      <h2>Métodos de pago utilizados</h2>
      <div class="chart-placeholder shorter">
        <div class="chart-overlay">Distribución de pagos (efectivo, tarjeta, transferencia)</div>
      </div>
    </div>

    <!-- Tabla -->
    <div class="table-container">
      <h2>Tabla de Ventas Detalladas</h2>
      <table v-if="ventas.length">
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
          &laquo; Anterior
        </button>
        <span>Página {{ paginaActual }} de {{ totalPaginas }}</span>
        <button :disabled="paginaActual === totalPaginas" @click="cambiarPagina(paginaActual + 1)">
          Siguiente &raquo;
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
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
    };
  },
  methods: {
    formatearFecha(fecha) {
      if (!fecha) return '';
      return new Date(fecha).toLocaleDateString('es-GT');
    },

    filtrarDatos() {
      this.fechaInicio = this.filtroFechaInicio;
      this.fechaFin = this.filtroFechaFin;

      if (this.fechaInicio && this.fechaFin) {
        this.cargarVentas();
      } else {
        alert('Por favor, seleccioná ambas fechas.');
      }
    },

    async cargarVentas() {
      this.cargando = true;
      try {
        const response = await axios.get('http://localhost:8000/api/ventas/por-fecha/', {

          params: {
            fecha_inicio: this.fechaInicio,
            fecha_fin: this.fechaFin,
          },
        });
        this.totalVentas = response.data.total_ventas;
        this.numeroFacturas = response.data.numero_facturas;
        this.ventas = response.data.ventas;
      } catch (error) {
        console.error('Error al obtener las ventas:', error);
      } finally {
        this.cargando = false;
      }
    },

    resetFiltros() {
      this.filtroFechaInicio = '';
      this.filtroFechaFin = '';
      this.fechaInicio = '';
      this.fechaFin = '';
      this.totalVentas = 0;
      this.numeroFacturas = 0;
      this.ventas = [];
    }
  }
};
</script>



<style scoped>
/* Header unificado */
.top-bar {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 0.75rem 2rem;
  background: #1e293b;
  justify-content: space-between;
  position: relative;
  top: 0;
  left: 0;
  z-index: 1000;
}
.logo {
  width: 150px;
  height: auto;
  cursor: pointer;
}
.top-bar h1 {
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

/* Página general */
.reporte-ventas {
  background-color: #0a0f2c; /* fondo oscuro */
  color: #ffffff; /* texto claro */
  padding: 20px;
  padding-top: 120px; /* espacio para header */
  font-family: 'Kollektif', sans-serif;
  min-height: 100vh;
}

/* Filtros */
.filtros-container {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
  flex-wrap: wrap;
  background-color: #1e293b;
  padding: 15px;
  border-radius: 8px;
}
.filtro label {
  margin-bottom: 5px;
  font-weight: bold;
  color: #ffffff;
}
.filtro input {
  padding: 8px;
  border-radius: 4px;
  border: none;
  background-color: #ffffff;
  color: #000000;
}
.btn-filtrar, .btn-reset {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  margin-top: auto;
}
.btn-filtrar {
  background-color: #2aa68f;
  color: #fff;
}
.btn-reset {
  background-color: #839a2d;
  color: #fff;
}

/* KPI */
.kpi-container {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  margin-bottom: 30px;
}
.kpi-card {
  background-color: #1e2236;
  padding: 20px;
  border-radius: 8px;
}
.kpi-card.principal {
  flex: 1;
  min-width: 250px;
}
.kpi-card h3 {
  margin: 0;
  color: #2b5ca8;
}
.kpi-card .valor {
  font-size: 2rem;
  font-weight: bold;
  color: #ffffff;
}
.kpi-card .descripcion {
  font-size: 0.9rem;
  color: #ccc;
}

/* Chart */
.chart-container {
  background-color: #1e2236;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}
.chart-placeholder {
  background-color: #2c3148;
  border-radius: 6px;
  height: 250px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.chart-placeholder.shorter {
  height: 180px;
}
.chart-overlay {
  color: #ccc;
  font-style: italic;
}

/* Tabla */
.table-container {
  background-color: #1e2236;
  padding: 20px;
  border-radius: 8px;
  overflow-x: auto;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  padding: 10px;
  border: 1px solid #2c3148;
  color: #ffffff;
}
th {
  background-color: #2aa68f;
}
tr:nth-child(even) {
  background-color: #2b2f40;
}
tr:hover {
  background-color: #3c4c6e;
}

/* Paginación */
.pagination {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
}
.pagination button {
  background-color: #2aa68f;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}
.pagination button:disabled {
  background-color: #666;
  cursor: not-allowed;
}
</style>
