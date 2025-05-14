<template>
  <div class="inventory-container">
    <h1>Inventario</h1>
    <router-link to="/" class="back-button">Regresar</router-link>

    <div v-for="(items, tipo) in inventarios" :key="tipo" class="inventory-section">
      <h2>{{ tipo }}</h2>
      <table>
        <thead>
          <tr>
            <th>Material</th>
            <th>Descripción</th>
            <th>Cantidad</th>
            <th>En Escasez</th>
            <th>Usados</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(item, index) in mostrarLimitado(tipo) ? items.slice(0, 6) : items"
            :key="index"
            :class="{ 'en-escasez': item.cantidad < 6 }"
          >
            <td>{{ item.material }}</td>
            <td>{{ item.descripcion }}</td>
            <td>{{ item.cantidad }}</td>
            <td>{{ item.cantidad < 6 ? 'Sí' : 'No' }}</td>
            <td>{{ item.usados }}</td>
          </tr>
        </tbody>
      </table>

      <div class="button-row">
        <button @click="agregarStock(tipo)">Agregar Stock</button>
        <button @click="sacarStock(tipo)">Sacar Stock</button>
        <button @click="agregarProducto(tipo)">Agregar Nuevo Producto</button>
        <button @click="toggleVistaCompleta(tipo)">
          {{ mostrarLimitado(tipo) ? 'Ver Todos' : 'Ver Menos' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      vistaExtendida: {},
      inventarios: {
        Telas: [
          { material: 'Telas blancas', descripcion: 'Tela de algodón', cantidad: 15, usados: 50 },
          { material: 'Telas verdes', descripcion: 'Tela poliéster', cantidad: 4, usados: 15 },
          { material: 'Telas negras', descripcion: 'Tela licra', cantidad: 10, usados: 30 },
          { material: 'Telas rojas', descripcion: 'Tela sintética', cantidad: 6, usados: 5 },
          { material: 'Telas cafés', descripcion: 'Tela de lino', cantidad: 11, usados: 10 },
          { material: 'Telas azules', descripcion: 'Tela denim', cantidad: 3, usados: 8 },
          { material: 'Telas grises', descripcion: 'Tela mezclilla', cantidad: 7, usados: 6 },
        ],
        Hilos: [
          { material: 'Hilo blanco', descripcion: 'Hilo algodón', cantidad: 12, usados: 30 },
          { material: 'Hilo rojo', descripcion: 'Hilo sintético', cantidad: 3, usados: 10 },
          { material: 'Hilo negro', descripcion: 'Hilo grueso', cantidad: 6, usados: 25 },
          { material: 'Hilo azul', descripcion: 'Hilo de poliéster', cantidad: 5, usados: 18 },
          { material: 'Hilo gris', descripcion: 'Hilo licra', cantidad: 7, usados: 11 },
          { material: 'Hilo verde', descripcion: 'Hilo lino', cantidad: 8, usados: 9 },
          { material: 'Hilo marrón', descripcion: 'Hilo elástico', cantidad: 2, usados: 7 },
        ],
        Uniformes: [
          { material: 'Uniforme escolar', descripcion: 'Niño/a primaria', cantidad: 8, usados: 20 },
          { material: 'Uniforme médico', descripcion: 'Scrub clínico', cantidad: 2, usados: 5 },
          { material: 'Uniforme policía', descripcion: 'Oficial urbano', cantidad: 10, usados: 12 },
          { material: 'Uniforme chef', descripcion: 'Cocina profesional', cantidad: 4, usados: 3 },
          { material: 'Uniforme empresa', descripcion: 'Oficina/industrial', cantidad: 6, usados: 14 },
          { material: 'Uniforme militar', descripcion: 'Camuflaje', cantidad: 9, usados: 11 },
          { material: 'Uniforme seguridad', descripcion: 'Privada', cantidad: 5, usados: 6 },
        ],
      },
    }
  },
  methods: {
    mostrarLimitado(tipo) {
      return !this.vistaExtendida[tipo];
    },
    toggleVistaCompleta(tipo) {
      this.$set(this.vistaExtendida, tipo, !this.vistaExtendida[tipo]);
    },
    agregarStock(tipo) {
      alert(`Agregar stock a: ${tipo}`);
    },
    sacarStock(tipo) {
      alert(`Sacar stock de: ${tipo}`);
    },
    agregarProducto(tipo) {
      alert(`Agregar nuevo producto a: ${tipo}`);
    }
  }
}
</script>

<style scoped>
.inventory-container {
  padding: 40px;
  background-color: var(--color-octonary);
  min-height: 100vh;
}

h1 {
  font-size: 36px;
  font-weight: bold;
  color: var(--colo-texto-blanco);
  margin-bottom: 30px;
}

h2 {
  color: var(--colo-texto-blanco);
  margin-top: 40px;
  margin-bottom: 10px;
}

.back-button {
  background-color: var(--color-senary);
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
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
  margin-bottom: 10px;
}

th {
  background-color: var(--color-senary);
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

.button-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 40px;
}

.button-row button {
  background-color: var(--color-senary);
  color: white;
  padding: 10px 14px;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

.button-row button:hover {
  background-color: var(--color-tertiary);
}
</style>
