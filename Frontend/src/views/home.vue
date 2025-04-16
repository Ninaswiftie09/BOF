<template>
    <div class="container">
      <header class="header">
        <div class="menu">☰</div>
        <div><a href="#" class="profile-link">Perfil del Usuario</a></div>
      </header>
  
      <div class="content">
        <div class="left">
          <h2 class="title">
            Inventario <span class="view-link">(Ver mi inventario)</span>
          </h2>
          <canvas id="myPieChart"></canvas>
        </div>
  
        <div class="right">
          <div class="division"><h3><a href="#">Clientes</a></h3></div>
          <div class="division"><h3><a href="#">Facturas</a></h3></div>
          <div class="division"><h3><a href="#">Reportes de Ventas</a></h3></div>
          <div class="division"><h3><a href="#">Calculadora de Materia Prima</a></h3></div>
          <div class="division"><h3><a href="#">Contabilidad</a></h3></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Chart from 'chart.js/auto';
  
  export default {
    name: 'HomeDashboard',
    mounted() {
      const ctx = document.getElementById('myPieChart').getContext('2d');
      new Chart(ctx, {
        type: 'pie',
        data: {
          labels: [
            'Telas blancas',
            'Telas verdes',
            'Telas negras',
            'Telas rojas',
            'Telas negras'
          ],
          datasets: [{
            data: [15, 4, 10, 6, 11],
            backgroundColor: [
              '#839A2D', // primario
              '#2AA68F', // secundario
              '#84C8C0', // terciario
              '#C9E8F5', // cuaternario
              '#2B5CA8',  // quinario
            ],
            borderColor: '#374666',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
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
   font-family: 'Kollektif', sans-serif;
   background-color: #b1d1eb;
   color: #374666;
   height: 100vh;
   overflow: hidden;
   display: flex;
   flex-direction: column;
 }
 
 .header {
   background-color: #3B3536;
   color: white;
   padding: 10px 20px;
   display: flex;
   justify-content: space-between;
   align-items: center;
 }
 
 .menu {
   font-size: 24px;
   cursor: pointer;
 }
 
 .profile-link {
   text-decoration: none;
   color: #F3F0EB;
   font-weight: bold;
 }
 
 .content {
   display: flex;
   flex-direction: row;
   height: calc(100% - 60px);
 }
 
 .left {
   width: 60%;
   padding: 20px;
   display: flex;
   flex-direction: column;
   align-items: center;
   justify-content: center;
 }
 
 .right {
   width: 40%;
   padding: 20px;
   display: flex;
   flex-direction: column;
   gap: 15px;
   justify-content: center;
 }
 
 .title {
   font-family: 'Archivo Black', sans-serif;
   color: #839A2D;
 }
 
 .view-link {
   color: #2AA68F;
   font-size: 14px;
   font-weight: bold;
 }
 
 canvas {
   width: 500px !important;
   height: 500px !important;
   max-width: 100%;
   max-height: 100%;
 }
 
 .division {
   background-color: #cbdfef;
   padding: 14px;
   border-radius: 10px;
   text-align: center;
   min-width: 200px;
 }
 
 .division h3 a {
   text-decoration: none;
   color: #374666;
   font-weight: bold;
 }
 </style>
 