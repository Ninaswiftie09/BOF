<template>
    <div class="clientes-container">
      <h1>Clientes</h1>
      <router-link to="/" class="back-button">Regresar</router-link>
  
      <table>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Apellidos</th>
            <th>telefono</th>
            <th>CUI</th>
            <th>NIT</th>
            <th>fecha de entrega</th>

          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Abner Gabriel</td>
            <td>Mejicanos Hernandez</td>
            <td>36902623</td>
            <td>3729283343</td>
            <td>8515948</td>
            <td>12/Marzo/2026</td>

          
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <style scoped>
  .inventory-container {
    padding: 40px;
    background-color: var(--color-octonary);
    min-height: 100vh;
  }
  
  h1 {
    font-size: 36px;
    font-weight: bold;
    color: var(--color-primary);
    margin-bottom: 30px;
  }
  
  .back-button {
    background-color: var(--color-secondary);
    color: white;
    padding: 10px 20px;
    border-radius: 10px;
    font-weight: bold;
    text-decoration: none;
    float: right;
    margin-top: -60px;
  }
  
  .back-button:hover {
    background-color: var(--color-tertiary);
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    background-color: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 0 10px rgba(0,0,0,0.05);
  }
  
  th {
    background-color: var(--color-secondary);
    color: white;
    font-weight: bold;
    padding: 16px;
    font-size: 18px;
  }
  
  td {
    text-align: center;
    padding: 12px;
    font-size: 16px;
    color: var(--color-senary);
  }
  
  tr:nth-child(even) {
    background-color: #f9f9f9;
  }
  
  .en-escasez {
    background-color: #fff2f2;
    color: #b00020;
    font-weight: bold;
  }
  </style>
  