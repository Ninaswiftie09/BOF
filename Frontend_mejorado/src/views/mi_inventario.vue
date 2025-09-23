<template>
  <div class="inventory-container">
    <!-- Header unificado (sin modificar el componente) -->
    <NavBar title="INVENTARIO">
      <template #actions>
        <input v-model="search" class="nav-search" placeholder="Buscar en inventario…" />
      </template>
    </NavBar>

    <!-- 👇 todo el contenido va aquí, con padding -->
    <div class="page-body">
      <div
        v-for="(items, tipo) in inventarios"
        :key="tipo"
        class="inventory-section"
      >
        <h2>{{ titulosVisibles[tipo] || tipo }}</h2>

        <table>
          <thead>
            <tr>
              <th v-for="col in columnasPorTipo[tipo]" :key="col">{{ col }}</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(item, index) in itemsToRender(tipo)"
              :key="index"
              :class="{ 'en-escasez': item.stock < 6 }"
            >
              <!-- Telas -->
              <template v-if="tipo === 'Telas'">
                <td>{{ item.id }}</td><td>{{ item.nombre }}</td><td>{{ item.tipo }}</td>
                <td>{{ item.composicion }}</td><td>{{ item.color }}</td>
                <td>{{ item.codigo }}</td><td>{{ item.stock }}</td><td>{{ item.descripcion }}</td>
              </template>

              <!-- Hilos -->
              <template v-else-if="tipo === 'Hilos'">
                <td>{{ item.id }}</td><td>{{ item.nombre }}</td><td>{{ item.material }}</td>
                <td>{{ item.codigo_color }}</td><td>{{ item.color }}</td>
                <td>{{ item.codigo }}</td><td>{{ item.stock }}</td><td>{{ item.descripcion }}</td>
              </template>

              <!-- Uniformes (Productos) -->
              <template v-else-if="tipo === 'Uniformes'">
                <td>{{ item.id }}</td><td>{{ item.tipo }}</td><td>{{ item.talla }}</td>
                <td>{{ item.color }}</td><td>{{ item.stock }}</td>
                <td>{{ item.categoria_nombre || 'N/A' }}</td>
                <td>{{ item.material_nombre || 'N/A' }}</td>
              </template>

              <!-- Categorías -->
              <template v-else-if="tipo === 'Categorias'">
                <td>{{ item.id }}</td>
                <td>{{ item.nombre }}</td>
              </template>
            </tr>
          </tbody>
        </table>

        <div class="button-row">
          <button @click="abrirFormulario('agregar', tipo)">Agregar producto</button>
          <button @click="abrirFormulario('eliminar', tipo)">Eliminar Producto</button>
          <button @click="abrirFormulario('editar', tipo)">Editar Producto</button>
          <button @click="abrirVerTodos(tipo)">{{ vistaExtendida[tipo] ? 'Ocultar' : 'Ver Todos' }}</button>
        </div>
      </div>
    </div>

    <!-- Modal Formulario -->
    <div v-if="formVisible" class="modal-overlay">
      <div class="modal-content">
        <h3 v-if="accion === 'agregar'">Agregar nuevo {{ titulosVisibles[tipoFormulario] || tipoFormulario }}</h3>
        <h3 v-else-if="accion === 'editar'">Editar {{ titulosVisibles[tipoFormulario] || tipoFormulario }}</h3>
        <h3 v-else-if="accion === 'eliminar'">Eliminar {{ titulosVisibles[tipoFormulario] || tipoFormulario }}</h3>

        <form @submit.prevent="submitFormulario" class="form-vertical">
          <!-- Selección de producto para edición -->
          <div v-if="accion === 'editar'">
            <label>Seleccionar producto:</label>
            <select v-model.number="seleccionId" @change="autoCompletarProducto">
              <option :value="null" disabled>Seleccione un producto</option>
              <option v-for="item in inventarios[tipoFormulario]" :key="item.id" :value="item.id">
                {{ formatearProducto(item) }}
              </option>
            </select>
            <label>O ID del producto:</label>
            <input v-model.number="formData.id" type="number" min="1" @change="autoCompletarProducto" required />
          </div>

          <!-- ID cuando es eliminación -->
          <div v-else-if="accion === 'eliminar'">
            <label>ID del producto:</label>
            <input v-model.number="formData.id" type="number" min="1" required />
          </div>

          <!-- Campos cuando no es eliminar -->
          <div v-if="accion !== 'eliminar'">
            <!-- TELAS -->
            <div v-if="tipoFormulario === 'Telas'">
              <label>Nombre</label><input v-model="formData.nombre" placeholder="Nombre" />
              <label>Tipo</label><input v-model="formData.tipo" placeholder="Tipo" />
              <label>Composición</label><input v-model="formData.composicion" placeholder="Composición" />
              <label>Color</label><input v-model="formData.color" placeholder="Color" />
              <label>Código</label><input v-model="formData.codigo" placeholder="Código" />
              <label>Stock</label><input v-model.number="formData.stock" type="number" />
              <label>Descripción</label><textarea v-model="formData.descripcion" placeholder="Descripción"></textarea>
            </div>

            <!-- HILOS -->
            <div v-else-if="tipoFormulario === 'Hilos'">
              <label>Nombre</label><input v-model="formData.nombre" placeholder="Nombre" />
              <label>Material</label><input v-model="formData.material" placeholder="Material" />
              <label>Código de color</label><input v-model="formData.codigo_color" placeholder="Código de color" />
              <label>Color</label><input v-model="formData.color" placeholder="Color" />
              <label>Código</label><input v-model="formData.codigo" placeholder="Código" />
              <label>Stock</label><input v-model.number="formData.stock" type="number" />
              <label>Descripción</label><textarea v-model="formData.descripcion" placeholder="Descripción"></textarea>
            </div>

            <!-- UNIFORMES (Productos) -->
            <div v-else-if="tipoFormulario === 'Uniformes'">
              <label>Tipo</label><input v-model="formData.tipo" placeholder="Tipo" />
              <label>Talla</label><input v-model="formData.talla" placeholder="Talla" />
              <label>Color</label><input v-model="formData.color" placeholder="Color" />
              <label>ID de Tela relacionada</label><input v-model.number="formData.material" />
              <label>Stock</label><input v-model.number="formData.stock" type="number" />
              <label>Tipo de categoría</label>
              <select v-model.number="formData.categoria">
                <option :value="null" disabled>Seleccione una categoría</option>
                <option v-for="c in categoriasOptions" :key="c.id" :value="c.id">{{ c.nombre }}</option>
              </select>
            </div>

            <!-- CATEGORÍAS -->
            <div v-else-if="tipoFormulario === 'Categorias'">
              <label>Nombre</label>
              <input v-model="formData.nombre" placeholder="Nombre de la categoría" required />
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

    <!-- Modal Ver Todos -->
    <div v-if="verTodosVisible" class="modal-overlay">
      <div class="modal-content full-table-modal">
        <button class="close-btn-top" @click="cerrarVerTodos">✕</button>
        <h3>{{ titulosVisibles[tipoVerTodos] || tipoVerTodos }} - Lista Completa</h3>
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
                <td>{{ item.color }}</td><td>{{ item.stock }}</td>
                <td>{{ item.categoria_nombre || 'N/A' }}</td>
                <td>{{ item.material_nombre || 'N/A' }}</td>
              </template>
              <template v-else-if="tipoVerTodos === 'Categorias'">
                <td>{{ item.id }}</td><td>{{ item.nombre }}</td>
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
import { useRouter } from 'vue-router'
import { bus } from '@/event-bus'
import NavBar from '@/components/NavBar.vue'
import { apiFetch } from '@/utils/api'

export default {
  components: { NavBar },
  setup() {
    const router = useRouter()
    const goHome = () => router.push({ name: 'home' })
    return { goHome }
  },
  data() {
    return {
      search: '',
      vistaExtendida: {},
      inventarios: { Telas: [], Hilos: [], Uniformes: [], Categorias: [] },
      titulosVisibles: { Telas: 'Telas', Hilos: 'Hilos', Uniformes: 'Productos', Categorias: 'Categorías' },
      columnasPorTipo: {
        Telas:      ['id','Nombre','Tipo','Composición','Color','Código','Stock','Descripción'],
        Hilos:      ['id','Nombre','Material','Código Color','Color','Código','Stock','Descripción'],
        Uniformes:  ['id','Tipo','Talla','Color','Stock','Categoría','Material (tela)'],
        Categorias: ['id','Nombre'],
      },
      formVisible: false, tipoFormulario: '', accion: '', formData: {},
      verTodosVisible: false, tipoVerTodos: '', categoriasOptions: [], seleccionId: null,
    }
  },
  mounted() {
    this.obtenerInventario('Telas')
    this.obtenerInventario('Hilos')
    this.obtenerInventario('Uniformes')
    this.obtenerInventario('Categorias')
    this.cargarCategorias()

    bus?.on?.('inventario-actualizado', () => {
      this.obtenerInventario('Telas')
      this.obtenerInventario('Hilos')
      this.obtenerInventario('Uniformes')
      this.obtenerInventario('Categorias')
      this.cargarCategorias()
    })
  },
  methods: {
    /* --- Header search helpers --- */
    filteredByType(tipo) {
      const q = this.search.trim().toLowerCase()
      const arr = this.inventarios[tipo] || []
      if (!q) return arr
      return arr.filter(obj =>
        Object.values(obj).some(v => (v ?? '').toString().toLowerCase().includes(q))
      )
    },
    itemsToRender(tipo) {
      const arr = this.filteredByType(tipo)
      return this.mostrarLimitado(tipo) ? arr.slice(0, 6) : arr
    },

    mostrarLimitado(tipo) { return !this.vistaExtendida[tipo] },
    toggleVistaCompleta(tipo) {
      this.vistaExtendida = { ...this.vistaExtendida, [tipo]: !this.vistaExtendida[tipo] }
    },

    abrirFormulario(accion, tipo) {
      this.accion = accion
      this.tipoFormulario = tipo
      this.formVisible = true
      this.formData = {}
      this.seleccionId = null
      if (tipo === 'Uniformes' || tipo === 'Categorias') this.cargarCategorias()
    },
    cerrarFormulario() { this.formVisible = false; this.formData = {}; this.seleccionId = null },

    abrirVerTodos(tipo) { this.tipoVerTodos = tipo; this.verTodosVisible = true; this.toggleVistaCompleta(tipo) },
    cerrarVerTodos() { this.verTodosVisible = false; this.tipoVerTodos = '' },

    formatearProducto(item) {
      return this.tipoFormulario === 'Uniformes'
        ? `${item.id} - ${item.tipo} ${item.talla}`
        : `${item.id} - ${item.nombre || item.tipo}`
    },

    autoCompletarProducto() {
      const id = this.seleccionId || this.formData.id
      if (!id) return
      const lista = this.inventarios[this.tipoFormulario] || []
      const item = lista.find(p => p.id === id)
      if (!item) { this.formData = { id }; this.seleccionId = null; return }

      if (this.tipoFormulario === 'Telas') {
        const { id: i, nombre, tipo, composicion, color, codigo, stock, descripcion } = item
        this.formData = { id: i, nombre, tipo, composicion, color, codigo, stock, descripcion }
      } else if (this.tipoFormulario === 'Hilos') {
        const { id: i, nombre, material, codigo_color, color, codigo, stock, descripcion } = item
        this.formData = { id: i, nombre, material, codigo_color, color, codigo, stock, descripcion }
      } else if (this.tipoFormulario === 'Uniformes') {
        const { id: i, tipo, talla, color, stock, material, categoria } = item
        this.formData = { id: i, tipo, talla, color, stock, material, categoria }
      } else if (this.tipoFormulario === 'Categorias') {
        const { id: i, nombre } = item
        this.formData = { id: i, nombre }
      } else {
        this.formData = { ...item }
      }
      this.seleccionId = id
    },

    /* === FIX ENDPOINTS: crear/editar/eliminar === */
    async submitFormulario() {
      try {
        const tipo = this.tipoFormulario.slice(0, -1).toLowerCase() // Telas->tela, etc.

        // Crear: colecciones base (DRF) excepto categoría que tiene endpoint especial
        const crear = {
          tela: '/api/telas/',
          hilo: '/api/hilos/',
          uniforme: '/api/uniformes/',
          categoria: '/api/inventario/agregar-nueva-categoria/',
        }

        let url = '', method = '', payload = null

        if (this.accion === 'agregar') {
          url = crear[tipo]
          method = 'POST'
          payload = this.formData
        } else if (this.accion === 'editar') {
          if (!this.formData.id) { alert('Debe especificar el ID'); return }
          const base = (tipo === 'categoria') ? 'editar-categoria' : `editar-${tipo}`
          url = `/api/inventario/${base}/${this.formData.id}/`
          method = 'PUT'
          payload = this.formData
        } else if (this.accion === 'eliminar') {
          if (!this.formData.id) { alert('Debe especificar el ID'); return }
          const base = (tipo === 'categoria') ? 'eliminar-categoria' : `eliminar-${tipo}`
          url = `/api/inventario/${base}/${this.formData.id}/`
          method = 'DELETE'
        } else {
          alert('Acción desconocida'); return
        }

        await apiFetch(url, method, payload)

        alert(`${this.accion} completado con éxito`)
        bus?.emit?.('inventario-actualizado')
        this.cerrarFormulario()
        await this.obtenerInventario(this.tipoFormulario)
        if (this.tipoFormulario === 'Categorias') await this.cargarCategorias()
      } catch (e) {
        console.error(e)
        alert('Error en la operación. Revisa los datos e intenta nuevamente.')
      }
    },

    async obtenerInventario(tipo) {
      try {
        // Telas/Hilos/Uniformes: /api/{colección}/  |  Categorias: /api/categorias/
        const path = (tipo === 'Categorias') ? '/api/categorias/' : `/api/${tipo.toLowerCase()}/`
        const data = await apiFetch(path)
        this.inventarios[tipo] = (Array.isArray(data) ? data : []).map(item =>
          tipo === 'Uniformes'
            ? { ...item, material_nombre: item.material_nombre || 'N/A', categoria_nombre: item.categoria_nombre || 'N/A' }
            : item
        )
      } catch (e) {
        console.error(`Error al obtener ${tipo}:`, e)
      }
    },

    async cargarCategorias() {
      try {
        this.categoriasOptions = await apiFetch('/api/categorias/')
      } catch (e) {
        console.error('Error cargando categorías', e)
      }
    },
  }
}
</script>


<style scoped>
/* === Fondo y layout general === */
.inventory-container{
  min-height:100vh;
  background:#0a0f2c; /*fondo pantalla inventario*/
  color:#fff; /*nada*/
  display:flex;
  flex-direction:column;
  font-family:'Segoe UI',sans-serif;
}

/* Padding del contenido, NO del header */
.page-body{
  padding: 40px;
}

/*no cambia nada si se elimina*/
.nav-search{
  width: 280px; max-width: 40vw;
  padding: .5rem .75rem;
  border-radius: 10px;
  border: 1px solid #cbd5e1; /*nada*/
  background: #fff; /*nada*/
  color:#000; /*nada*/
  font-size: .9rem;
}
/*no cambia nada si se elimina*/
.nav-search:focus{
  outline: none;
  box-shadow: 0 0 0 3px rgba(99,102,241,.25); /*nada*/
  border-color:#6366f1; /*nada*/
}

h2{
  color: #fff; /*titulo de tablas "telas, hilos, productos, categorias" */
  margin-top: 40px;
  margin-bottom: 10px;
}

/* ===== Tabla y estados ===== */
table{
  width: 100%;
  border-collapse: collapse;
  background-color: white; /*color1 fila intercalado en tablas*/
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 0 10px rgba(0,0,0,0.05); /*sombreado abajo de tablas "telas, hilos, productos, categorias" */
  margin-bottom: 10px;
}
th{
  background-color: var(--color-senary); /*color fondo encabezados tablas*/
  color: white; /*color texto encabezados tablas*/
  font-weight: bold;
  padding: 16px;
  font-size: 18px;
}
td{
  text-align: center;
  padding: 12px;
  font-size: 16px;
  color: var(--color-senary); /*todo texto filas resultado de tablas*/
}
tr:nth-child(even){ background-color: #f9f9f9; } /*color2 fila intercalado en tablas*/

/*no probado aun*/
.en-escasez{
  background-color: #fff2f2; /*asdf*/
  color: #b00020; /*asdf*/
  font-weight: bold;
}

/* ===== Botonera ===== */
.button-row{
  display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px;
}
.button-row button{
  background-color: var(--color-senary); /*fondo botones opciones "agregar, eliminar, editar producto, y ocultar/ ver todos" */
  color: white; /*texto botones opciones "agregar, eliminar, editar producto, y ocultar/ver todos" */
  padding: 10px 14px; border: none; border-radius: 8px;
  font-weight: bold; cursor: pointer;
  transition: background-color 0.3s; /*nada*/
}
.button-row button:hover{ background-color: var(--color-tertiary); } /*fondo botones opciones con cursor arriba*/

/* ===== Modales ===== */
.modal-overlay{
  position: fixed; inset:0; background-color: rgba(0,0,0,0.5); /*fondo pantalla completa opciones "agregar" */
  display:flex; align-items:center; justify-content:center; z-index: 9999;
}
.modal-content{
  background: white; /*fondo tarjeta formulario "agregar nuevo" y fondo boton "cancelar", excepto ocultar/ver todos*/
  padding: 25px 30px; border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.3); /*sombreado debajo tarjeta formulario*/
  max-width: 450px; width: 90%; max-height: 90vh; overflow-y:auto;
}

.form-vertical label{ font-weight: 600; margin: 12px 0 5px; display:block; }
.form-vertical input,
.form-vertical textarea,
.form-vertical select{
  width: 100%; padding: 8px 10px; border-radius: 6px;
  border: 1px solid #ccc; /*borde input formularios*/
  font-size: 15px;
}
.buttons-row{ margin-top: 20px; display:flex; gap: 15px; justify-content: flex-end; }
.btn-primary{
  background-color: var(--color-senary); /*fondo boton "guardar" formulario opciones*/
  color: var(--colo-texto-blanco); /*texto "guardar" formulario opciones*/
  padding: 10px 22px; border-radius: 8px; border:none; font-weight:600; cursor:pointer;
  transition: background-color .3s ease; /*nada*/
}
.btn-primary:hover{ background-color: var(--color-tertiary); } /*fondo boton "guardar" cursor arriba*/
.btn-cancel{
  background: transparent;
  color:#555; /*texto "cancelar" en opciones y ocultar/ver todos*/
  padding:10px 22px; border-radius: 8px;
  border: 1px solid #aaa; /*borde boton "cancelar" en opciones y ocultar/ver todos*/
  cursor:pointer; font-weight:600; transition: background-color .3s ease;
}
.btn-cancel:hover{ background-color:#eee; } /*fondo boton "cancelar" cursor arriba*/

/* Modal de “ver todos” */
.full-table-modal{
  background:white; /*fondo tarjeta*/
  padding:25px 30px; border-radius:12px;
  box-shadow:0 8px 20px rgba(0,0,0,0.3); /*sombreado tarjeta en "ocultar" */
  max-width:90vw; width:90vw; max-height:90vh; overflow-y:auto; position:relative;
}
.close-btn-top{
  position:absolute; top:10px; right:15px; background:transparent; border:none; font-size:22px; cursor:pointer; font-weight:bold;
  color:#333; /*color simbolo x en ocultar/ver todos*/
}
.close-btn-top:hover{ color:#b00020; } /*color simbolo x en ocultar/ver todos cursor arriba*/
</style>
