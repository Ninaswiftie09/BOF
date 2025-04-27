<template>
  <div class="container">
    <header class="header">
      <div class="menu">☰</div>
      <div><a href="#" class="profile-link">Perfil del Usuario</a></div>
    </header>

    <div class="content">
      <div class="left">
        <h2 class="title">
          Inventario
          <router-link class="view-link" to="/mi_inventario">(Ver mi inventario)</router-link>
        </h2>
        <canvas id="myPieChart"></canvas>
      </div>

      <div class="right">
        <router-link class="division" to="/clientes"><h3>Clientes</h3></router-link>
        <router-link class="division" to="/billpage"><h3>Facturas</h3></router-link>
        <router-link class="division" to="/ReporteVentas"><h3>Reportes de Ventas</h3></router-link>
        <router-link class="division" to="/calculadora"><h3>Calculadora de Materia Prima</h3></router-link>
        <router-link class="division" to="/accounting"><h3>Contabilidad</h3></router-link>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  name: 'HomeView',
  mounted() {
    const ctx = document.getElementById('myPieChart').getContext('2d');
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
            position: 'top',
            labels: {
              color: '#374666',
              font: {
                family: 'Kollektif'
              }
            }
          },
          title: {
            display: true,
            text: 'Inventario',
            color: '#839A2D',
            font: {
              size: 18,
              family: 'Archivo Black'
            }
          }
        }
      }
    });
  }
};
</script>

<style scoped>
.container {
  background-color: var(--color-novenary);
  padding: 20px;
  font-family: 'Kollektif', sans-serif;
  height: 100vh;

  /* Agregado para compensar el header fijo */
  padding-top: 70px;
}

.header {
  background-color: var(--color-senary);
  color: white;
  padding: 10px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;

  /* 🔒 Fijar la barra en la parte superior */
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
}

.profile-link {
  text-decoration: none;
  color: white;
  font-weight: bold;
  margin-right: 25px;
}

.content {
  display: flex;
  margin-top: 20px;
  height: 90%;
}

.left {
  width: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.right {
  width: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 10px;
}

.title {
  color: var(--color-primary);
}

.view-link {
  font-size: 14px;
  margin-left: 10px;
  color: var(--color-tertiary);
  font-weight: bold;
  text-decoration: none;
}

canvas {
  width: 500px !important;
  height: 500px !important;
}

.division {
  background-color: var(--color-quaternary);
  color: var(--color-senary);
  padding: 15px;
  text-align: center;
  border-radius: 10px;
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.3s;
}

.division:hover {
  background-color: var(--color-secondary);
}
</style>
