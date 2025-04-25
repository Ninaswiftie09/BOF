<template>
  <div class="inventory-container">
    <h1>Inventario</h1>
    <router-link to="/" class="back-button">Regresar</router-link>

    <table>
      <thead>
        <tr>
          <th>Materiales</th>
          <th>Cantidad</th>
          <th>En Escasez</th>
          <th>Usados</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Telas blancas</td>
          <td>15</td>
          <td>No</td>
          <td>50</td>
        </tr>
        <tr class="en-escasez">
          <td>Telas verdes</td>
          <td>4</td>
          <td>Sí</td>
          <td>15</td>
        </tr>
        <tr>
          <td>Telas negras</td>
          <td>10</td>
          <td>No</td>
          <td>30</td>
        </tr>
        <tr class="en-escasez">
          <td>Telas rojas</td>
          <td>6</td>
          <td>Sí</td>
          <td>5</td>
        </tr>
        <tr>
          <td>Telas cafés</td>
          <td>11</td>
          <td>No</td>
          <td>10</td>
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
