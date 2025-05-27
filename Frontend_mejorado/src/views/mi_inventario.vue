<template>
  <div class="inventory-container">
    <!-- Encabezado unificado -->
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
            <th v-for="col in columnasPorTipo[tipo]" :key="col">{{ col }}</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(item, index) in mostrarLimitado(tipo) ? items.slice(0, 6) : items"
            :key="index"
            :class="{ 'en-escasez': item.stock < 6 }"
          >
            <template v-if="tipo === 'Telas'">
              <td>{{ item.id }}</td><td>{{ item.nombre }}</td><td>{{ item.tipo }}</td>
              <td>{{ item.composicion }}</td><td>{{ item.color }}</td>
              <td>{{ item.codigo }}</td><td>{{ item.stock }}</td><td>{{ item.descripcion }}</td>
            </template>
            <template v-else-if="tipo === 'Hilos'">
              <td>{{ item.id }}</td><td>{{ item.nombre }}</td><td>{{ item.material }}</td>
              <td>{{ item.codigo_color }}</td><td>{{ item.color }}</td>
              <td>{{ item.codigo }}</td><td>{{ item.stock }}</td><td>{{ item.descripcion }}</td>
            </template>
            <template v-else-if="tipo === 'Uniformes'">
              <td>{{ item.id }}</td><td>{{ item.tipo }}</td><td>{{ item.talla }}</td>
              <td>{{ item.color }}</td><td>{{ item.stock }}</td><td>{{ item.material_nombre }}</td>
            </template>
          </tr>
        </tbody>
      </table>

      <div class="button-row">
        <button @click="abrirFormulario('agregar', tipo)">Agregar producto</button>
        <button @click="abrirFormulario('eliminar', tipo)">Eliminar Producto</button>
        <button @click="abrirFormulario('editar', tipo)">Editar Producto</button>
        <button @click="toggleVistaCompleta(tipo)">{{ mostrarLimitado(tipo) ? 'Ver Todos' : 'Ver Menos' }}</button>
      </div>

      <!-- Formulario Modal -->
      <div v-if="formVisible && tipoFormulario === tipo" class="formulario">
        <h3 v-if="accion === 'agregar'">Agregar nuevo {{ tipo }}</h3>
        <h3 v-else-if="accion === 'editar'">Editar {{ tipo }}</h3>
        <h3 v-else-if="accion === 'eliminar'">Eliminar {{ tipo }}</h3>

        <form @submit.prevent="submitFormulario" class="form-vertical">
          <div v-if="accion !== 'agregar'">
            <label>ID del producto:</label>
            <input v-model.number="formData.id" type="number" min="1" required />
          </div>

          <div v-if="accion !== 'eliminar'">
            <div v-if="tipo === 'Telas'">
              <input v-model="formData.nombre" placeholder="Nombre" />
              <input v-model="formData.tipo" placeholder="Tipo" />
              <input v-model="formData.composicion" placeholder="Composición" />
              <input v-model="formData.color" placeholder="Color" />
              <input v-model="formData.codigo" placeholder="Código" />
              <input v-model.number="formData.stock" type="number" />
              <textarea v-model="formData.descripcion" placeholder="Descripción"></textarea>
            </div>

            <div v-else-if="tipo === 'Hilos'">
              <input v-model="formData.nombre" placeholder="Nombre" />
              <input v-model="formData.material" placeholder="Material" />
              <input v-model="formData.codigo_color" placeholder="Código de color" />
              <input v-model="formData.color" placeholder="Color" />
              <input v-model="formData.codigo" placeholder="Código" />
              <input v-model.number="formData.stock" type="number" />
              <textarea v-model="formData.descripcion" placeholder="Descripción"></textarea>
            </div>

            <div v-else-if="tipo === 'Uniformes'">
              <input v-model="formData.tipo" placeholder="Tipo" />
              <input v-model="formData.talla" placeholder="Talla" />
              <input v-model="formData.color" placeholder="Color" />
              <input v-model.number="formData.material" placeholder="ID de Tela relacionada" />
              <input v-model.number="formData.stock" type="number" />
            </div>
          </div>

          <div class="buttons-row">
            <button type="submit" class="btn-primary">
              {{ accion === 'agregar' ? 'Guardar' : accion === 'editar' ? 'Actualizar' : 'Eliminar' }}
            </button>
            <button type="button" class="btn-cancel" @click="cerrarFormulario">Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    const goHome = () => router.push({ name: 'home' });
    return { goHome };
  },
  data() {
    return {
      vistaExtendida: {},
      inventarios: { Telas: [], Hilos: [], Uniformes: [] },
      columnasPorTipo: {
        Telas: ["id", "Nombre", "Tipo", "Composición", "Color", "Código", "Stock", "Descripción"],
        Hilos: ["id", "Nombre", "Material", "Código Color", "Color", "Código", "Stock", "Descripción"],
        Uniformes: ["id", "Tipo", "Talla", "Color", "Stock", "Material (tela)"]
      },
      formVisible: false,
      tipoFormulario: '',
      accion: '',
      formData: {},
    };
  },
  mounted() {
    this.obtenerInventario("Telas", "telas");
    this.obtenerInventario("Hilos", "hilos");
    this.obtenerInventario("Uniformes", "uniformes");
  },
  methods: {
    mostrarLimitado(tipo) {
      return !this.vistaExtendida[tipo];
    },
    toggleVistaCompleta(tipo) {
      this.$set(this.vistaExtendida, tipo, !this.vistaExtendida[tipo]);
    },
    abrirFormulario(accion, tipo) {
      this.accion = accion;
      this.tipoFormulario = tipo;
      this.formVisible = true;
      this.formData = {};
    },
    cerrarFormulario() {
      this.formVisible = false;
      this.formData = {};
    },
    async submitFormulario() {
      try {
        const base = 'http://localhost:8000/api';
        let url = '', method = '';

        const tipo = this.tipoFormulario.slice(0, -1).toLowerCase();

        if (this.accion === 'agregar') {
          url = `${base}/inventario/agregar-nuevo-${tipo}/`;
          method = 'POST';
        } else if (this.accion === 'editar') {
          url = `${base}/inventario/editar-${tipo}/${this.formData.id}/`;
          method = 'PUT';
        } else if (this.accion === 'eliminar') {
          url = `${base}/inventario/eliminar-${tipo}/${this.formData.id}/`;
          method = 'DELETE';
        }

        const res = await fetch(url, {
          method,
          headers: { 'Content-Type': 'application/json' },
          body: method !== 'DELETE' ? JSON.stringify(this.formData) : null,
        });

        if (!res.ok) {
          const err = await res.json();
          alert('Error: ' + (err.error || 'Desconocido'));
          return;
        }

        alert(`${this.accion} exitoso`);
        this.cerrarFormulario();
        this.obtenerInventario(this.tipoFormulario, this.tipoFormulario.toLowerCase());
      } catch (e) {
        alert('Error al conectar con el servidor');
        console.error(e);
      }
    },
    async obtenerInventario(tipo, endpoint) {
      try {
        const res = await fetch(`http://localhost:8000/api/${endpoint}/`);
        const data = await res.json();
        const items = data.map(item => tipo === 'Uniformes' ? { ...item, material_nombre: item.material_nombre || 'N/A' } : item);
        this.inventarios[tipo] = items;
      } catch (e) {
        console.error(`Error obteniendo ${tipo}:`, e);
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
  background: white;
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
  font-size: 22px;
  cursor: pointer;
  font-weight: bold;
  color: #333;
}

.formulario button:hover {
  opacity: 0.9;
}

</style>
