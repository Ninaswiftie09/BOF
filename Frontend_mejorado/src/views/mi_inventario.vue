<template>
  <div class="inventory-container">
    <!-- Encabezado modernizado -->
    <header class="top-bar">
      <img
        src="@/assets/logo_bof_blanco.png"
        alt="Logo del cliente"
        class="logo"
        @click="goHome"
      />
      <h1>INVENTARIO</h1>
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
        <button @click="abrirVerTodos(tipo)">Ver Todos</button>
      </div>
    </div>
    

    <div v-if="formVisible" class="modal-overlay">
      <div class="modal-content">
        <h3 v-if="accion === 'agregar'">Agregar nuevo {{ tipoFormulario }}</h3>
        <h3 v-else-if="accion === 'editar'">Editar {{ tipoFormulario }}</h3>
        <h3 v-else-if="accion === 'eliminar'">Eliminar {{ tipoFormulario }}</h3>

        <form @submit.prevent="submitFormulario" class="form-vertical">
          <div v-if="accion !== 'agregar'">
            <label>ID del producto:</label>
            <input v-model.number="formData.id" type="number" min="1" required />
          </div>

          <div v-if="accion !== 'eliminar'">
            <div v-if="tipoFormulario === 'Telas'">
              <label>Nombre</label>
              <input v-model="formData.nombre" placeholder="Nombre" />
              <label>Tipo</label>
              <input v-model="formData.tipo" placeholder="Tipo" />
              <label>Composición</label>
              <input v-model="formData.composicion" placeholder="Composición" />
              <label>Color</label>
              <input v-model="formData.color" placeholder="Color" />
              <label>Código</label>
              <input v-model="formData.codigo" placeholder="Código" />
              <label>Stock</label>
              <input v-model.number="formData.stock" type="number" />
              <label>Descripción</label>
              <textarea v-model="formData.descripcion" placeholder="Descripción"></textarea>
            </div>
            <div v-if="tipoFormulario === 'Hilos'">
              <label>Nombre</label>
              <input v-model="formData.nombre" placeholder="Nombre" />
              <label>Material</label>
              <input v-model="formData.material" placeholder="Material" />
              <label>Código de color</label>
              <input v-model="formData.codigo_color" placeholder="Código de color" />
              <label>Color</label>
              <input v-model="formData.color" placeholder="Color" />
              <label>Código</label>
              <input v-model="formData.codigo" placeholder="Código" />
              <label>Stock</label>
              <input v-model.number="formData.stock" type="number" />
              <label>Descripción</label>
              <textarea v-model="formData.descripcion" placeholder="Descripción"></textarea>
            </div>
            <div v-if="tipoFormulario === 'Uniformes'">
              <label>Tipo</label>
              <input v-model="formData.tipo" placeholder="Tipo" />
              <label>Talla</label>
              <input v-model="formData.talla" placeholder="Talla" />
              <label>Color</label>
              <input v-model="formData.color" placeholder="Color" />
              <label>ID de Tela relacionada</label>
              <input v-model.number="formData.material" />
              <label>Stock</label>
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

    <div v-if="verTodosVisible" class="modal-overlay">
      <div class="modal-content full-table-modal">
        <button class="close-btn-top" @click="cerrarVerTodos">✕</button>
        <h3>{{ tipoVerTodos }} - Lista Completa</h3>
        <table>
          <thead>
            <tr>
              <th v-for="col in columnasPorTipo[tipoVerTodos]" :key="col">{{ col }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in inventarios[tipoVerTodos]" :key="item.id">
              <template v-if="tipoVerTodos === 'Telas'">
                <td>{{ item.id }}</td><td>{{ item.nombre }}</td><td>{{ item.tipo }}</td>
                <td>{{ item.composicion }}</td><td>{{ item.color }}</td>
                <td>{{ item.codigo }}</td><td>{{ item.stock }}</td><td>{{ item.descripcion }}</td>
              </template>
              <template v-else-if="tipoVerTodos === 'Hilos'">
                <td>{{ item.id }}</td><td>{{ item.nombre }}</td><td>{{ item.material }}</td>
                <td>{{ item.codigo_color }}</td><td>{{ item.color }}</td>
                <td>{{ item.codigo }}</td><td>{{ item.stock }}</td><td>{{ item.descripcion }}</td>
              </template>
              <template v-else-if="tipoVerTodos === 'Uniformes'">
                <td>{{ item.id }}</td><td>{{ item.tipo }}</td><td>{{ item.talla }}</td>
                <td>{{ item.color }}</td><td>{{ item.stock }}</td><td>{{ item.material_nombre }}</td>
              </template>
            </tr>
          </tbody>
        </table>
        <button class="btn-cancel" @click="cerrarVerTodos">Cerrar</button>
      </div>
    </div>
  </div>
</template>


<script>
import { BASE_URL } from '@/config';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    const goHome = () => {
      router.push({ name: 'home' });
    };
    return { goHome };
  },
  data() {
    return {
      vistaExtendida: {},
      inventarios: {
        Telas: [],
        Hilos: [],
        Uniformes: []
      },
      columnasPorTipo: {
        Telas: ["id", "Nombre", "Tipo", "Composición", "Color", "Código", "Stock", "Descripción"],
        Hilos: ["id", "Nombre", "Material", "Código Color", "Color", "Código", "Stock", "Descripción"],
        Uniformes: ["id", "Tipo", "Talla", "Color", "Stock", "Material (tela)"]
      },
      formVisible: false,
      tipoFormulario: '',
      accion: '',
      formData: {},
      verTodosVisible: false,
      tipoVerTodos: ''
    };
  },
  mounted() {
    this.obtenerInventario("Telas");
    this.obtenerInventario("Hilos");
    this.obtenerInventario("Uniformes");

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
    abrirVerTodos(tipo) {
      this.tipoVerTodos = tipo;
      this.verTodosVisible = true;
    },
    cerrarVerTodos() {
      this.verTodosVisible = false;
      this.tipoVerTodos = '';
    },
    async submitFormulario() {
      try {
        const tipo = this.tipoFormulario.slice(0, -1).toLowerCase();
        const urlBase = `${BASE_URL}/api/`;
        let url = '';
        let method = '';

        if (this.accion === 'agregar') {
          url = `${urlBase}/inventario/agregar-nuevo-${tipo}/`;
          method = 'POST';
        } else if (this.accion === 'editar') {
          if (!this.formData.id) return alert('Debe especificar el ID');
          url = `${urlBase}/inventario/editar-${tipo}/${this.formData.id}/`;
          method = 'PUT';
        } else if (this.accion === 'eliminar') {
          if (!this.formData.id) return alert('Debe especificar el ID');
          url = `${urlBase}/inventario/eliminar-${tipo}/${this.formData.id}/`;
          method = 'DELETE';
        }

        // Función para obtener el token CSRF
        function getCookie(name) {
          let cookieValue = null;
          if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
              const cookie = cookies[i].trim();
              // Coincide con el nombre
              if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
              }
            }
          }
          return cookieValue;
        }


        const res = await fetch(url, {
          method,
          credentials: 'include',  
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // token CSRF
          },
          body: method !== 'DELETE' ? JSON.stringify(this.formData) : null
        });


        if (!res.ok) {
          const err = await res.json();
          return alert('Error: ' + (err.error || 'Desconocido'));
        }

        alert(`${this.accion} completado con éxito`);
        this.cerrarFormulario();
        this.obtenerInventario(this.tipoFormulario, this.tipoFormulario.toLowerCase());

      } catch (error) {
        alert('Error en la conexión con el servidor');
        console.error(error);
      }
    },
    async obtenerInventario(tipo, endpoint) {
      try {
        const res = await fetch(`${BASE_URL}/api/${tipo.toLowerCase()}/`);
        const data = await res.json();
        this.inventarios[tipo] = data.map(item =>
          tipo === "Uniformes" ? { ...item, material_nombre: item.material_nombre || "N/A" } : item
        );
      } catch (error) {
        console.error(`Error al obtener ${tipo}:`, error);
      }
    }

  }
};
</script>

<style scoped>
.logo {
  width: 100px;
  height: auto;
  cursor: pointer;
}

.inventory-container {
  padding: 40px;
  background-color: var(--color-octonary);
  min-height: 100vh;
}

h1 {
  flex-grow: 1;
  text-align: center;
  color: #ffffff;
  font-size: 1.8rem;
  font-weight: bold;
  margin: 0;
}

h2 {
  color: var(--colo-texto-blanco);
  margin-top: 40px;
  margin-bottom: 10px;
}

.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #1e293b; /* Azul oscuro */
  padding: 0.75rem 2rem;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  z-index: 1000;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
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

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.modal-content {
  background: white;
  padding: 25px 30px;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.3);
  max-width: 450px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.form-vertical label {
  font-weight: 600;
  margin-top: 12px;
  margin-bottom: 5px;
  display: block;
}

.form-vertical input,
.form-vertical textarea {
  width: 100%;
  padding: 8px 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 15px;
  resize: vertical;
}

.buttons-row {
  margin-top: 20px;
  display: flex;
  gap: 15px;
  justify-content: flex-end;
}

.btn-primary {
  background-color: var(--color-senary);
  color: var(--colo-texto-blanco);
  padding: 10px 22px;
  border-radius: 8px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-primary:hover {
  background-color: var(--color-tertiary);
}

.btn-cancel {
  background: transparent;
  color: #555;
  padding: 10px 22px;
  border-radius: 8px;
  border: 1px solid #aaa;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s ease;
}

.btn-cancel:hover {
  background-color: #eee;
}
.full-table-modal {
  background: white;
  padding: 25px 30px;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.3);
  max-width: 90vw; 
  width: 90vw;
  max-height: 90vh;
  overflow-y: auto;
  position: relative; 
}
.close-btn-top {
  position: absolute;
  top: 10px;
  right: 15px;
  background: transparent;
  border: none;
  font-size: 22px;
  cursor: pointer;
  font-weight: bold;
  color: #333;
}

.close-btn-top:hover {
  color: #b00020;
}


</style>
