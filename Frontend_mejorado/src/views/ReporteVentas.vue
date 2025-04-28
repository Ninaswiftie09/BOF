<template>
  <div class="reporte-ventas">
    <div class="header-container">
      <router-link to="/" class="back-button">← Regresar a Inicio</router-link>
      <h1>Reporte de Ventas</h1>
    </div>
    
    <div class="filtros-container">
      <div class="filtro">
        <label for="fecha-inicio">Desde:</label>
        <input type="date" id="fecha-inicio" v-model="filtroFechaInicio">
      </div>
      <div class="filtro">
        <label for="fecha-fin">Hasta:</label>
        <input type="date" id="fecha-fin" v-model="filtroFechaFin">
      </div>
      <button class="btn-filtrar" @click="filtrarDatos">Filtrar</button>
      <button class="btn-reset" @click="resetFiltros">Limpiar</button>
    </div>

      // comentariosprueba
    <!-- Sección 1:  -->
    <div class="kpi-container">
      <div class="kpi-card principal">
        <h3>Total de Ventas</h3>
        <p class="valor">Q{{ totalVentas }}</p>
        <p class="descripcion">Solo ventas (sin gastos ni balances)</p>
      </div>
      <div class="kpi-card principal">
        <h3>Número de Facturas</h3>
        <p class="valor">{{ numeroFacturas }}</p>
        <p class="descripcion">Tickets de venta emitidos</p>
      </div>
    </div>
    
    <!-- Sección 2: Gráfica de evolución de ventas -->
    <div class="chart-container">
      <h2>Evolución de Ventas</h2>
      <div class="chart-placeholder">
        <!-- Integrar las gráficas de línea o barras -->
        <div class="chart-overlay">Gráfica de evolución de ventas por días, semanas o meses</div>
      </div>
    </div>
    
    <!-- Sección 3: Productos más vendidos -->
    <div class="chart-container">
      <h2>Productos más vendidos</h2>
      <div class="chart-placeholder">
        <!-- integrar las gráficas de barras horizontales -->
        <div class="chart-overlay">Top 5 o 10 productos más vendidos</div>
      </div>
    </div>
    
    <!-- Sección 4: Métodos de pago -->
    <div class="chart-container">
      <h2>Métodos de pago utilizados</h2>
      <div class="chart-placeholder shorter">
        <!-- agregar aca gráfica de pastel -->
        <div class="chart-overlay">Distribución de pagos (efectivo, tarjeta, transferencia)</div>
      </div>
    </div>
    
    <!-- Sección 5: Tabla de Ventas Detalladas -->
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
          <tr v-for="venta in ventas" :key="venta.id">
            <td>{{ venta.id }}</td>
            <td>{{ venta.producto }}</td>
            <td>{{ venta.cliente || 'No registrado' }}</td>
            <td>{{ venta.cantidad }}</td>
            <td>Q{{ venta.precio_unitario }}</td>
            <td>Q{{ venta.total }}</td>
            <td>{{ venta.metodo_pago || 'Efectivo' }}</td>
            <td>{{ formatearFecha(venta.fecha) }}</td>
          </tr>
        </tbody>
      </table>
      <div v-else-if="cargando" class="loading">
        <div class="spinner"></div>
        <p>Cargando ventas...</p>
      </div>
      <p v-else class="no-data">No se encontraron ventas para el periodo seleccionado</p>
      
      <div class="pagination">
        <button :disabled="paginaActual === 1" @click="cambiarPagina(paginaActual - 1)">&laquo; Anterior</button>
        <span>Página {{ paginaActual }} de {{ totalPaginas }}</span>
        <button :disabled="paginaActual === totalPaginas" @click="cambiarPagina(paginaActual + 1)">Siguiente &raquo;</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReporteVentas',
  data() {
    return {
      // Datos que serán proporcionados por el backend
      ventas: [],
      cargando: true,
      filtroFechaInicio: '',
      filtroFechaFin: '',
      paginaActual: 1,
      totalPaginas: 1,
      
      // Datos  (estos deberán ser calculados por el backend)
        // Comentario de prueba commit 
      
      totalVentas: '0.00',
      numeroFacturas: 0
    };
  },
  methods: {
    // Método para formatear fechas (frontend)
    formatearFecha(fecha) {
      return new Date(fecha).toLocaleDateString();
    },
    
    // BACKEND: Implementar lógica de filtrado de datos por fechas
    filtrarDatos() {
      console.log('Filtrando datos:', this.filtroFechaInicio, this.filtroFechaFin);
      // Aquí el backend debe implementar la petición a la API con los filtros
    },
    
    // BACKEND: Implementar reinicio de filtros
    resetFiltros() {
      this.filtroFechaInicio = '';
      this.filtroFechaFin = '';
      // Aquí  recargar los datos originales
    },
    
    // BACKEND: Implementar paginación
    cambiarPagina(pagina) {
      this.paginaActual = pagina;
      // implementar la petición para la página específica
    }
  },
  mounted() {
    // BACKEND: Implementar carga inicial de datos
    // Por ahora es data quemada 
    setTimeout(() => {
      this.ventas = [
        {
          id: 1,
          producto: 'Camisa deportiva',
          cliente: 'Juan Pérez',
          cantidad: 2,
          precio_unitario: 150.00,
          total: 300.00,
          metodo_pago: 'Efectivo',
          fecha: '2025-04-20'
        },
        {
          id: 2,
          producto: 'Pantalón formal',
          cliente: 'María López',
          cantidad: 1,
          precio_unitario: 250.00,
          total: 250.00,
          metodo_pago: 'Tarjeta',
          fecha: '2025-04-21'
        }
      ];
      
      this.totalVentas = '550.00';
      this.numeroFacturas = 2;
      this.cargando = false;
    }, 1000);
  }
}
</script>

<style scoped>
.reporte-ventas {
  padding: 20px;
  font-family: 'Kollektif', sans-serif;
  background-color: var(--color-octonary); /* B1D1EB - azul claro */
  color: var(--color-senary); /* 374666 - azul oscuro para texto */
  min-height: 100vh;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.back-button {
  padding: 8px 16px;
  background-color: var(--color-secondary); /* 2AA68F - verde turquesa */
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s;
  font-family: 'Kollektif', sans-serif;
}

.back-button:hover {
  background-color: var(--color-quaternary); /* C9E8F5 - celeste claro */
  color: var(--color-senary);
}

h1 {
  margin: 0;
  color: var(--color-primary); /* 839A2D - verde oliva */
  font-family: 'Archivo Black', sans-serif;
}

h2 {
  color: var(--color-primary);
  border-bottom: 1px solid var(--color-secondary);
  padding-bottom: 8px;
  margin-top: 30px;
  font-family: 'Archivo Black', sans-serif;
}

.filtros-container {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
  flex-wrap: wrap;
  background-color: var(--color-novenary); /* blanco */
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.filtro {
  display: flex;
  flex-direction: column;
}

.filtro label {
  margin-bottom: 5px;
  color: var(--color-senary);
  font-weight: bold;
}

.filtro input {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid var(--color-septenary);
  background-color: var(--color-novenary);
  color: var(--color-senary);
}

.btn-filtrar, .btn-reset {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  align-self: flex-end;
  margin-top: auto;
  font-family: 'Kollektif', sans-serif;
}

.btn-filtrar {
  background-color: var(--color-secondary);
  color: white;
}

.btn-reset {
  background-color: var(--color-tertiary);
  color: var(--color-senary);
}

/* KPIs */
.kpi-container {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.kpi-card {
  background-color: var(--color-novenary);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.kpi-card.principal {
  flex: 1;
  min-width: 250px;
  border-left: 4px solid var(--color-primary);
}

.kpi-card h3 {
  margin-top: 0;
  color: var(--color-quinary); /* 2B5CA8 - azul fuerte */
  font-size: 1rem;
  font-family: 'Archivo Black', sans-serif;
}

.kpi-card .valor {
  font-size: 2rem;
  font-weight: bold;
  margin: 10px 0;
  color: var(--color-primary);
}

.kpi-card .descripcion {
  font-size: 0.8rem;
  color: var(--color-senary);
  margin: 0;
}

/* Charts */
.chart-container {
  background-color: var(--color-novenary);
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chart-placeholder {
  height: 300px;
  background-color: var(--color-quaternary);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.chart-placeholder.shorter {
  height: 200px;
}

.chart-overlay {
  color: var(--color-senary);
  text-align: center;
  font-style: italic;
}

/* Table */
.table-container {
  background-color: var(--color-novenary);
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  overflow-x: auto;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 10px;
  border: 1px solid var(--color-octonary);
  text-align: left;
}

th {
  background-color: var(--color-secondary);
  position: sticky;
  top: 0;
  color: white;
  font-family: 'Archivo Black', sans-serif;
  font-weight: normal;
}

tr:nth-child(even) {
  background-color: var(--color-quaternary);
}

tr:hover {
  background-color: var(--color-tertiary);
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 40px 0;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top: 4px solid var(--color-secondary);
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

.no-data {
  text-align: center;
  margin: 40px 0;
  color: var(--color-senary);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 20px;
}

.pagination button {
  padding: 8px 16px;
  background-color: var(--color-secondary);
  border: none;
  border-radius: 4px;
  color: white;
  cursor: pointer;
  font-family: 'Kollektif', sans-serif;
}

.pagination button:disabled {
  background-color: var(--color-septenary);
  cursor: not-allowed;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Media queries para responsividad */
@media (max-width: 768px) {
  .header-container {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .back-button {
    margin-bottom: 10px;
  }
  
  .kpi-container {
    flex-direction: column;
  }
  
  .kpi-card {
    min-width: 100%;
  }
  
  th, td {
    padding: 8px 5px;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .filtros-container {
    flex-direction: column;
  }
  
  .filtro {
    width: 100%;
  }
  
  .btn-filtrar, .btn-reset {
    width: 100%;
    margin-top: 10px;
  }
  
  th, td {
    padding: 6px 3px;
    font-size: 0.8rem;
  }
  
  .pagination {
    flex-direction: column;
    gap: 5px;
  }
  
  .chart-placeholder {
    height: 200px;
  }
}
</style>


