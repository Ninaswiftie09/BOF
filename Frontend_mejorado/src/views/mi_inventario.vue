<template>
  <div class="inventory-container">
    <!-- HEADER unificado -->
    <header class="top-bar">
      <img
        src="@/assets/logo_bof_blanco.png"
        alt="Logo del cliente"
        class="logo"
        @click="goHome"
      />
      <h1>INVENTARIO</h1>
      <button class="avatar-btn"></button>
    </header>

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

      <!-- Formularios por tipo -->
      <div v-if="formVisible && tipoFormulario === tipo" class="formulario">
        <h3>Agregar nuevo {{ tipo }}</h3>

        <div v-if="tipo === 'Telas'">
          <input v-model="nuevoProducto.nombre" placeholder="Nombre">
          <input v-model="nuevoProducto.tipo" placeholder="Tipo">
          <input v-model="nuevoProducto.composicion" placeholder="Composición">
          <input v-model="nuevoProducto.color" placeholder="Color">
          <input v-model="nuevoProducto.codigo" placeholder="Código">
          <input v-model.number="nuevoProducto.stock" type="number" placeholder="Stock">
          <textarea v-model="nuevoProducto.descripcion" placeholder="Descripción"></textarea>
          <button @click="enviarNuevo('telas')">Guardar</button>
        </div>

        <div v-else-if="tipo === 'Hilos'">
          <input v-model="nuevoProducto.nombre" placeholder="Nombre">
          <input v-model="nuevoProducto.material" placeholder="Material">
          <input v-model="nuevoProducto.codigo_color" placeholder="Código de color">
          <input v-model="nuevoProducto.color" placeholder="Color">
          <input v-model="nuevoProducto.codigo" placeholder="Código">
          <input v-model.number="nuevoProducto.stock" type="number" placeholder="Stock">
          <textarea v-model="nuevoProducto.descripcion" placeholder="Descripción"></textarea>
          <button @click="enviarNuevo('hilos')">Guardar</button>
        </div>

        <div v-else-if="tipo === 'Uniformes'">
          <input v-model="nuevoProducto.tipo" placeholder="Tipo">
          <input v-model="nuevoProducto.talla" placeholder="Talla">
          <input v-model="nuevoProducto.color" placeholder="Color">
          <input v-model.number="nuevoProducto.material" placeholder="ID de Tela relacionada">
          <input v-model.number="nuevoProducto.stock" type="number" placeholder="Stock">
          <button @click="enviarNuevo('uniformes')">Guardar</button>
        </div>

        <button @click="formVisible = false">Cancelar</button>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'

export default {
  setup() {
    const router = useRouter()
    const goHome = () => {
      router.push({ name: 'home' })
    }
    return { goHome }
  },
  data() {
    return {
      vistaExtendida: {},
      formVisible: false,
      tipoFormulario: '',
      inventarios: {
        Telas: [],
        Hilos: [],
        Uniformes: []
      },
      nuevoProducto: {}
    };
  },
  mounted() {
    this.obtenerInventario('Telas', 'telas');
    this.obtenerInventario('Hilos', 'hilos');
    this.obtenerInventario('Uniformes', 'uniformes');
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
      this.tipoFormulario = tipo;
      this.formVisible = true;
      this.nuevoProducto = {};
    },
    async obtenerInventario(tipo, endpoint) {
      try {
        const res = await fetch(`http://localhost:8000/api/${endpoint}/`);
        const data = await res.json();
        const items = data.map(item => ({
          material: item.nombre || item.tipo || 'Sin nombre',
          descripcion: item.descripcion || '—',
          cantidad: item.stock || 0,
          usados: item.usados || 0
        }));
        this.inventarios[tipo] = items;
      } catch (error) {
        console.error(`Error al obtener ${tipo}:`, error);
      }
    },
    async enviarNuevo(endpoint) {
      try {
        const res = await fetch(`http://localhost:8000/api/${endpoint}/nuevo/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.nuevoProducto)
        });

        const result = await res.json();

        if (!res.ok) {
          alert('Error: ' + (result.error || 'Error al guardar'));
          return;
        }

        alert(`${this.tipoFormulario.slice(0, -1)} agregado correctamente`);
        this.formVisible = false;
        this.obtenerInventario(this.tipoFormulario, endpoint);
      } catch (error) {
        alert('Error de red');
        console.error(error);
      }
    }
  }
};
</script>

<style scoped>
.inventory-container {
  padding: 40px;
  background-color: var(--color-octonary);
  min-height: 100vh;
  padding-top: 120px; /* espacio para el header fijo */
}

/* HEADER UNIFICADO */
.top-bar {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 0.75rem 2rem;
  background: #1e293b;
  justify-content: space-between;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}
.logo {
  width: 150px;
  height: auto;
  cursor: pointer;
}
h1 {
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

/* CONTENIDO */
h2 {
  color: var(--colo-texto-blanco);
  margin-top: 40px;
  margin-bottom: 10px;
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
  margin-bottom: 20px;
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
.formulario {
  background: var(--colo-texto-blanco);
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 30px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}
.formulario input,
.formulario textarea {
  display: block;
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
  border-radius: 6px;
  border: 1px solid #ccc;
}
.formulario button {
  background-color: var(--color-senary);
  color: var(--colo-texto-blanco);
  padding: 10px 20px;
  font-weight: bold;
  border: none;
  border-radius: 6px;
  margin-right: 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.formulario button:hover {
  opacity: 0.9;
}
</style>
