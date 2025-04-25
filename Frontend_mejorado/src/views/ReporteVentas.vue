<template>
    <div class="reporte-ventas">
      <router-link to="/" class="back-button">Regresar a Inicio</router-link>

      <h1>Reporte de Ventas</h1>
      <table v-if="ventas.length">
        <thead>
          <tr>
            <th>ID Venta</th>
            <th>Producto</th>
            <th>Cantidad</th>
            <th>Precio Unitario</th>
            <th>Total</th>
            <th>Fecha</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="venta in ventas" :key="venta.id">
            <td>{{ venta.id }}</td>
            <td>{{ venta.producto }}</td>
            <td>{{ venta.cantidad }}</td>
            <td>Q{{ venta.precio_unitario }}</td>
            <td>Q{{ venta.total }}</td>
            <td>{{ venta.fecha }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else>Cargando ventas...</p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ReporteVentas',
    data() {
      return {
        ventas: []
      };
    },
    mounted() {
      fetch('http://localhost:8000/api/ventas/')
        .then(response => response.json())
        .then(data => {
          this.ventas = data;
        })
        .catch(error => {
          console.error('Error al cargar las ventas:', error);
        });
    }
  }
  </script>
  
  <style scoped>
  .reporte-ventas {
    padding: 30px;
    font-family: "Segoe UI", sans-serif;
    background-color: #0D1B2A;
    color: #E0E1DD;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
    background-color: #1B263B;
  }
  
  th, td {
    padding: 10px;
    border: 1px solid #778DA9;
    text-align: left;
  }
  
  th {
    background-color: #415A77;
  }
  </style>
  