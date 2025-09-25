<template>
  <div class="inventory-container page">
    <!-- Header -->
    <NavBar title="INVENTARIO">
      <template #actions>
        <input v-model="search" class="input--white" placeholder="Buscar en inventario…" />
      </template>
    </NavBar>

    <div class="container">
      <div
        v-for="(items, tipo) in inventarios"
        :key="tipo"
        class="inventory-section module"
      >
        <h2>{{ titulosVisibles[tipo] || tipo }}</h2>

        <!-- Tabla reutilizable (centrada, con buscador por tabla) -->
        <Tablas
          :columns="columnsByTipo[tipo]"
          :rows="itemsToRender(tipo)"
          v-model:search="searchLocal[tipo]"
          :searchable="true"
          :searchTheme="'dark'"
          :useLocalFilter="false"
          :center="true"
          :actions="{ edit:false, delete:false }"
          :showAddButton="false"
          :maxVisible="null"
        />

        <!-- Botonera -->
        <div class="footer-actions" style="gap:10px; flex-wrap:wrap">
          <button class="btn" @click="abrirFormulario('agregar', tipo)">Agregar producto</button>
          <button class="btn btn--danger" @click="abrirFormulario('eliminar', tipo)">Eliminar Producto</button>
          <button class="btn btn--muted" @click="abrirFormulario('editar', tipo)">Editar Producto</button>
          <button class="btn" @click="abrirVerTodos(tipo)">Ver Todos</button>
        </div>
      </div>
    </div>

    <!-- ============== Modal Formulario (compacto + oscuro) ============== -->
    <div v-if="formVisible" class="modal-overlay">
      <div class="modal-content modal--compact">
        <h3 v-if="accion === 'agregar'">Agregar nuevo {{ titulosVisibles[tipoFormulario] || tipoFormulario }}</h3>
        <h3 v-else-if="accion === 'editar'">Editar {{ titulosVisibles[tipoFormulario] || tipoFormulario }}</h3>
        <h3 v-else-if="accion === 'eliminar'">Eliminar {{ titulosVisibles[tipoFormulario] || tipoFormulario }}</h3>

        <form @submit.prevent="submitFormulario" class="form-vertical">
          <!-- Selección de producto para edición -->
          <template v-if="accion === 'editar'">
            <label>Seleccionar producto:</label>
            <div class="select-wrap">
              <select class="select--dark" v-model.number="seleccionId" @change="autoCompletarProducto">
                <option :value="null" disabled>Seleccione un producto</option>
                <option v-for="item in inventarios[tipoFormulario]" :key="item.id" :value="item.id">
                  {{ formatearProducto(item) }}
                </option>
              </select>
            </div>

            <label>O ID del producto:</label>
            <input class="input--dark" v-model.number="formData.id" type="number" min="1" @change="autoCompletarProducto" required />
          </template>

          <!-- ID cuando es eliminación -->
          <template v-else-if="accion === 'eliminar'">
            <label>ID del producto:</label>
            <input class="input--dark" v-model.number="formData.id" type="number" min="1" required />
          </template>

          <!-- Campos cuando no es eliminar -->
          <template v-if="accion !== 'eliminar'">
            <!-- TELAS -->
            <template v-if="tipoFormulario === 'Telas'">
              <div class="form-field">
                <label>Nombre</label>
                <input class="input--dark" v-model="formData.nombre" placeholder="Nombre" />
              </div>
              <div class="form-field">
                <label>Tipo</label>
                <input class="input--dark" v-model="formData.tipo" placeholder="Tipo" />
              </div>
              <div class="form-field">
                <label>Composición</label>
                <input class="input--dark" v-model="formData.composicion" placeholder="Composición" />
              </div>
              <div class="form-field">
                <label>Color</label>
                <input class="input--dark" v-model="formData.color" placeholder="Color" />
              </div>
              <div class="form-field">
                <label>Código</label>
                <input class="input--dark" v-model="formData.codigo" placeholder="Código" />
              </div>
              <div class="form-field">
                <label>Stock</label>
                <input class="input--dark" v-model.number="formData.stock" type="number" />
              </div>
              <div class="form-field">
                <label>Descripción</label>
                <textarea class="input--dark" v-model="formData.descripcion" placeholder="Descripción"></textarea>
              </div>
            </template>

            <!-- HILOS -->
            <template v-else-if="tipoFormulario === 'Hilos'">
              <div class="form-field">
                <label>Nombre</label>
                <input class="input--dark" v-model="formData.nombre" placeholder="Nombre" />
              </div>
              <div class="form-field">
                <label>Material</label>
                <input class="input--dark" v-model="formData.material" placeholder="Material" />
              </div>
              <div class="form-field">
                <label>Código de color</label>
                <input class="input--dark" v-model="formData.codigo_color" placeholder="Código de color" />
              </div>
              <div class="form-field">
                <label>Color</label>
                <input class="input--dark" v-model="formData.color" placeholder="Color" />
              </div>
              <div class="form-field">
                <label>Código</label>
                <input class="input--dark" v-model="formData.codigo" placeholder="Código" />
              </div>
              <div class="form-field">
                <label>Stock</label>
                <input class="input--dark" v-model.number="formData.stock" type="number" />
              </div>
              <div class="form-field">
                <label>Descripción</label>
                <textarea class="input--dark" v-model="formData.descripcion" placeholder="Descripción"></textarea>
              </div>
            </template>

            <!-- UNIFORMES (Productos) -->
            <template v-else-if="tipoFormulario === 'Uniformes'">
              <div class="form-field">
                <label>Tipo</label>
                <input class="input--dark" v-model="formData.tipo" placeholder="Tipo" />
              </div>
              <div class="form-field">
                <label>Talla</label>
                <input class="input--dark" v-model="formData.talla" placeholder="Talla" />
              </div>
              <div class="form-field">
                <label>Color</label>
                <input class="input--dark" v-model="formData.color" placeholder="Color" />
              </div>
              <div class="form-field">
                <label>ID de Tela relacionada</label>
                <input class="input--dark" v-model.number="formData.material" />
              </div>
              <div class="form-field">
                <label>Stock</label>
                <input class="input--dark" v-model.number="formData.stock" type="number" />
              </div>
              <div class="form-field">
                <label>Tipo de categoría</label>
                <div class="select-wrap">
                  <select class="select--dark" v-model.number="formData.categoria">
                    <option :value="null" disabled>Seleccione una categoría</option>
                    <option v-for="c in categoriasOptions" :key="c.id" :value="c.id">{{ c.nombre }}</option>
                  </select>
                </div>
              </div>
            </template>

            <!-- CATEGORÍAS -->
            <template v-else-if="tipoFormulario === 'Categorias'">
              <div class="form-field">
                <label>Nombre</label>
                <input class="input--dark" v-model="formData.nombre" placeholder="Nombre de la categoría" required />
              </div>
            </template>
          </template>

          <div class="modal-actions">
            <button type="submit" class="btn">
              {{ accion === 'agregar' ? 'Guardar' : accion === 'editar' ? 'Actualizar' : 'Eliminar' }}
            </button>
            <button type="button" class="btn btn--muted" @click="cerrarFormulario">Cancelar</button>
          </div>
        </form>
      </div>
    </div>

    <!-- ================= Modal Ver Todos (ancho) ================= -->
    <div v-if="verTodosVisible" class="modal-overlay">
      <div class="modal-content modal--wide full-table-modal">
        <button class="close-btn-top" @click="cerrarVerTodos">✕</button>
        <h3>{{ titulosVisibles[tipoVerTodos] || tipoVerTodos }} - Lista Completa</h3>

        <div class="table-wrapper">
          <table class="table dark-table table--center">
            <thead>
              <tr>
                <th v-for="col in (columnsByTipo[tipoVerTodos] || [])" :key="col.key">{{ col.label }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in inventarios[tipoVerTodos]" :key="item.id">
                <template v-for="col in (columnsByTipo[tipoVerTodos] || [])" :key="col.key">
                  <td>
                    {{
                      item[col.key] ??
                      (col.key==='categoria_nombre' ? 'N/A' :
                       col.key==='material_nombre'  ? 'N/A' : '')
                    }}
                  </td>
                </template>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="footer-actions">
          <button class="btn btn--muted" @click="cerrarVerTodos">Cerrar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { bus } from '@/event-bus'
import NavBar from '@/components/NavBar.vue'
import Tablas from '@/components/Reutilizacion/Tablas.vue'
import { apiFetch } from '@/utils/api'

export default {
  components: { NavBar, Tablas },
  setup() {
    const router = useRouter()
    const goHome = () => router.push({ name: 'home' })
    return { goHome }
  },
  data() {
    return {
      search: '',
      inventarios: { Telas: [], Hilos: [], Uniformes: [], Categorias: [] },
      titulosVisibles: { Telas:'Telas', Hilos:'Hilos', Uniformes:'Productos', Categorias:'Categorías' },

      columnsByTipo: {
        Telas: [
          { key:'id', label:'id' },
          { key:'nombre', label:'Nombre' },
          { key:'tipo', label:'Tipo' },
          { key:'composicion', label:'Composición' },
          { key:'color', label:'Color' },
          { key:'codigo', label:'Código' },
          { key:'stock', label:'Stock' },
          { key:'descripcion', label:'Descripción' },
        ],
        Hilos: [
          { key:'id', label:'id' },
          { key:'nombre', label:'Nombre' },
          { key:'material', label:'Material' },
          { key:'codigo_color', label:'Código Color' },
          { key:'color', label:'Color' },
          { key:'codigo', label:'Código' },
          { key:'stock', label:'Stock' },
          { key:'descripcion', label:'Descripción' },
        ],
        Uniformes: [
          { key:'id', label:'id' },
          { key:'tipo', label:'Tipo' },
          { key:'talla', label:'Talla' },
          { key:'color', label:'Color' },
          { key:'stock', label:'Stock' },
          { key:'categoria_nombre', label:'Categoría' },
          { key:'material_nombre', label:'Material (tela)' },
        ],
        Categorias: [
          { key:'id', label:'id' },
          { key:'nombre', label:'Nombre' },
        ],
      },

      /* búsqueda local por tabla */
      searchLocal: { Telas:'', Hilos:'', Uniformes:'', Categorias:'' },

      formVisible:false, tipoFormulario:'', accion:'', formData:{},
      verTodosVisible:false, tipoVerTodos:'', categoriasOptions:[], seleccionId:null
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
    /* Búsqueda global del header */
    filteredByType(tipo){
      const q = this.search.trim().toLowerCase()
      const arr = this.inventarios[tipo] || []
      if (!q) return arr
      return arr.filter(obj =>
        Object.values(obj).some(v => (v ?? '').toString().toLowerCase().includes(q))
      )
    },

    /* Búsqueda local por tabla + límite 6 (siempre) */
    itemsToRender(tipo){
      let arr = this.filteredByType(tipo)
      const needle = (this.searchLocal[tipo] || '').trim().toLowerCase()
      if (needle) {
        const keys = (this.columnsByTipo[tipo] || []).map(c => c.key)
        arr = arr.filter(r => keys.some(k => String(r?.[k] ?? '').toLowerCase().includes(needle)))
      }
      return arr.slice(0, 6)
    },

    abrirFormulario(accion, tipo){
      this.accion = accion
      this.tipoFormulario = tipo
      this.formVisible = true
      this.formData = {}
      this.seleccionId = null
      if (tipo==='Uniformes' || tipo==='Categorias') this.cargarCategorias()
    },
    cerrarFormulario(){ this.formVisible=false; this.formData={}; this.seleccionId=null },

    abrirVerTodos(tipo){
      this.tipoVerTodos = tipo
      this.verTodosVisible = true
    },
    cerrarVerTodos(){
      this.verTodosVisible = false
      this.tipoVerTodos = ''
    },

    formatearProducto(item){
      return this.tipoFormulario==='Uniformes'
        ? `${item.id} - ${item.tipo} ${item.talla}`
        : `${item.id} - ${item.nombre || item.tipo}`
    },
    autoCompletarProducto(){
      const id = this.seleccionId || this.formData.id
      if(!id) return
      const lista = this.inventarios[this.tipoFormulario] || []
      const item = lista.find(p => p.id === id)
      if(!item){ this.formData = { id }; this.seleccionId = null; return }

      if(this.tipoFormulario==='Telas'){
        const {id:i,nombre,tipo,composicion,color,codigo,stock,descripcion}=item
        this.formData = {id:i,nombre,tipo,composicion,color,codigo,stock,descripcion}
      } else if(this.tipoFormulario==='Hilos'){
        const {id:i,nombre,material,codigo_color,color,codigo,stock,descripcion}=item
        this.formData = {id:i,nombre,material,codigo_color,color,codigo,stock,descripcion}
      } else if(this.tipoFormulario==='Uniformes'){
        const {id:i,tipo,talla,color,stock,material,categoria}=item
        this.formData = {id:i,tipo,talla,color,stock,material,categoria}
      } else if(this.tipoFormulario==='Categorias'){
        const {id:i,nombre}=item
        this.formData = {id:i,nombre}
      } else {
        this.formData = { ...item }
      }
      this.seleccionId = id
    },

    async submitFormulario(){
      try{
        const tipo = this.tipoFormulario.slice(0,-1).toLowerCase()
        const agregar = {
          tela:'inventario/agregar-nueva-tela',
          hilo:'inventario/agregar-nuevo-hilo',
          uniforme:'inventario/agregar-nuevo-uniforme',
          categoria:'inventario/agregar-nueva-categoria'
        }

        let url = '', method = '', payload = null

        if (this.accion === 'agregar') {
          url = `/api/${agregar[tipo]}/`
          method = 'POST'
          payload = this.formData
        } else if (this.accion === 'editar') {
          if (!this.formData.id) return alert('Debe especificar el ID')
          const base = (tipo === 'categoria') ? 'editar-categoria' : `editar-${tipo}`
          url = `/api/inventario/${base}/${this.formData.id}/`
          method = 'PUT'
          payload = this.formData
        } else if (this.accion === 'eliminar') {
          if (!this.formData.id) return alert('Debe especificar el ID')
          const base = (tipo === 'categoria') ? 'eliminar-categoria' : `eliminar-${tipo}`
          url = `/api/inventario/${base}/${this.formData.id}/`
          method = 'DELETE'
        }

        await apiFetch(url, method, payload)

        alert(`${this.accion} completado con éxito`)
        bus?.emit?.('inventario-actualizado')
        this.cerrarFormulario()
        await this.obtenerInventario(this.tipoFormulario)
        if(this.tipoFormulario==='Categorias') await this.cargarCategorias()
      } catch (e) {
        console.error(e)
        alert('Error en la operación. Revisa los datos e intenta nuevamente.')
      }
    },

    async obtenerInventario(tipo){
      try{
        const data = await apiFetch(`/api/${tipo.toLowerCase()}/`)
        this.inventarios[tipo] = (Array.isArray(data) ? data : []).map(item =>
          tipo==='Uniformes'
            ? { ...item, material_nombre:item.material_nombre||'N/A', categoria_nombre:item.categoria_nombre||'N/A' }
            : item
        )
      }catch(e){ console.error(`Error al obtener ${tipo}:`, e) }
    },

    async cargarCategorias(){
      try{
        this.categoriasOptions = await apiFetch('/api/categorias/')
      } catch(e){ console.error('Error cargando categorías', e) }
    }
  }
}
</script>

<style scoped>
.inventory-container{
  min-height:100vh;
  display:flex; flex-direction:column;
}
.close-btn-top{
  position:absolute; top:10px; left:10px;
  background:#2B5CA8; border:none; color:#fff;
  width:40px; height:40px; border-radius:10px;
  cursor:pointer; font-size:18px; font-weight:800;
}
</style>
