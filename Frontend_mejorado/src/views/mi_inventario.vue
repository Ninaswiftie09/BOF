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

        <!-- Tabla reutilizable -->
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

    <!-- ============== Modal Formulario  ============== -->
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
              <div class="form-field" v-for="f in ['nombre','tipo','composicion','color','codigo','stock','descripcion']" :key="f">
                <label>{{ f.charAt(0).toUpperCase() + f.slice(1) }}</label>
                <input
                  v-if="f!=='descripcion'"
                  class="input--dark"
                  v-model="formData[f]"
                  :placeholder="f.charAt(0).toUpperCase() + f.slice(1)"
                />
                <textarea
                  v-else
                  class="input--dark"
                  v-model="formData[f]"
                  placeholder="Descripción"
                ></textarea>
              </div>
            </template>

            <!-- HILOS -->
            <template v-else-if="tipoFormulario === 'Hilos'">
              <div class="form-field">
                <label>Nombre</label>
                <input class="input--dark" v-model="formData.nombre" />
              </div>
              <div class="form-field">
                <label>Material</label>
                <input class="input--dark" v-model="formData.material" />
              </div>
              <div class="form-field">
                <label>Código de color</label>
                <input class="input--dark" v-model="formData.codigo_color" />
              </div>
              <div class="form-field">
                <label>Color</label>
                <input class="input--dark" v-model="formData.color" />
              </div>
              <div class="form-field">
                <label>Código</label>
                <input class="input--dark" v-model="formData.codigo" />
              </div>
              <div class="form-field">
                <label>Stock</label>
                <input class="input--dark" type="number" v-model.number="formData.stock" />
              </div>
              <div class="form-field">
                <label>Descripción</label>
                <textarea class="input--dark" v-model="formData.descripcion"></textarea>
              </div>
            </template>

            <!-- UNIFORMES -->
            <template v-else-if="tipoFormulario === 'Uniformes'">
              <div class="form-field">
                <label>Tipo</label>
                <input class="input--dark" v-model="formData.tipo" />
              </div>
              <div class="form-field">
                <label>Talla</label>
                <input class="input--dark" v-model="formData.talla" />
              </div>
              <div class="form-field">
                <label>Color</label>
                <input class="input--dark" v-model="formData.color" />
              </div>
              <div class="form-field">
                <label>ID de Tela relacionada</label>
                <input class="input--dark" type="number" v-model.number="formData.material" />
              </div>
              <div class="form-field">
                <label>Stock</label>
                <input class="input--dark" type="number" v-model.number="formData.stock" />
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

    <!-- Modal Ver Todos -->
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
                  <td>{{ item[col.key] ?? (col.key==='categoria_nombre' ? 'N/A' : col.key==='material_nombre' ? 'N/A' : '') }}</td>
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
        Telas:[{key:'id',label:'id'},{key:'nombre',label:'Nombre'},{key:'tipo',label:'Tipo'},{key:'composicion',label:'Composición'},{key:'color',label:'Color'},{key:'codigo',label:'Código'},{key:'stock',label:'Stock'},{key:'descripcion',label:'Descripción'}],
        Hilos:[{key:'id',label:'id'},{key:'nombre',label:'Nombre'},{key:'material',label:'Material'},{key:'codigo_color',label:'Código Color'},{key:'color',label:'Color'},{key:'codigo',label:'Código'},{key:'stock',label:'Stock'},{key:'descripcion',label:'Descripción'}],
        Uniformes:[{key:'id',label:'id'},{key:'tipo',label:'Tipo'},{key:'talla',label:'Talla'},{key:'color',label:'Color'},{key:'stock',label:'Stock'},{key:'categoria_nombre',label:'Categoría'},{key:'material_nombre',label:'Material (tela)'}],
        Categorias:[{key:'id',label:'id'},{key:'nombre',label:'Nombre'}],
      },
      searchLocal: { Telas:'', Hilos:'', Uniformes:'', Categorias:'' },
      formVisible:false, tipoFormulario:'', accion:'', formData:{},
      verTodosVisible:false, tipoVerTodos:'', categoriasOptions:[], seleccionId:null
    }
  },
  mounted() {
    ['Telas','Hilos','Uniformes','Categorias'].forEach(t => this.obtenerInventario(t))
    this.cargarCategorias()
    bus?.on?.('inventario-actualizado', () => {
      ['Telas','Hilos','Uniformes','Categorias'].forEach(t => this.obtenerInventario(t))
      this.cargarCategorias()
    })
  },
  methods: {
    filteredByType(tipo){
      const q=this.search.trim().toLowerCase()
      const arr=this.inventarios[tipo]||[]
      if(!q)return arr
      return arr.filter(obj=>Object.values(obj).some(v=>(v??'').toString().toLowerCase().includes(q)))
    },
    itemsToRender(tipo){
      let arr=this.filteredByType(tipo)
      const needle=(this.searchLocal[tipo]||'').trim().toLowerCase()
      if(needle){
        const keys=(this.columnsByTipo[tipo]||[]).map(c=>c.key)
        arr=arr.filter(r=>keys.some(k=>String(r?.[k]??'').toLowerCase().includes(needle)))
      }
      return arr.slice(0,6)
    },
    abrirFormulario(accion,tipo){
      this.accion=accion;this.tipoFormulario=tipo;this.formVisible=true;this.formData={};this.seleccionId=null
      if(tipo==='Uniformes'||tipo==='Categorias')this.cargarCategorias()
    },
    cerrarFormulario(){this.formVisible=false;this.formData={};this.seleccionId=null},
    abrirVerTodos(tipo){this.tipoVerTodos=tipo;this.verTodosVisible=true},
    cerrarVerTodos(){this.verTodosVisible=false;this.tipoVerTodos=''},
    formatearProducto(item){return this.tipoFormulario==='Uniformes'?`${item.id} - ${item.tipo} ${item.talla}`:`${item.id} - ${item.nombre||item.tipo}`},
    autoCompletarProducto(){
      const id=this.seleccionId
      if(!id)return
      const lista=this.inventarios[this.tipoFormulario]||[]
      const item=lista.find(p=>p.id===id)
      if(!item)return
      if(this.tipoFormulario==='Telas'||this.tipoFormulario==='Hilos'||this.tipoFormulario==='Categorias'||this.tipoFormulario==='Uniformes')
        this.formData={...item}
    },
    async safeApiFetch(url, method='GET', payload){
      try{
        return await apiFetch(url,method,payload)
      }catch(err){
        // Manejo especial de error DELETE
        if(method==='DELETE' && (err.message?.includes('Failed to fetch') || err.message?.includes('ERR_CONTENT_LENGTH_MISMATCH'))){
          console.warn('DELETE inconsistente, se asume éxito')
          return null
        }
        throw err
      }
    },
    async submitFormulario(){
      try{
        const tipo=this.tipoFormulario.slice(0,-1).toLowerCase()
        const plural={tela:'telas',hilo:'hilos',uniforme:'uniformes'}[tipo]
        let url='',method='',payload=null

        if(this.accion==='agregar'){
          if(tipo==='categoria'){url='/api/inventario/agregar-nueva-categoria/';method='POST';payload=this.formData}
          else if(tipo==='uniforme'){
            const f=this.formData
            payload={tipo:f.tipo,talla:f.talla,color:f.color,stock:Number(f.stock||0),material:Number(f.material),categoria:Number(f.categoria)}
            url='/api/uniformes/';method='POST'
          }else{url=`/api/${plural}/`;method='POST';payload=this.formData}
        }else if(this.accion==='editar'){
          if(!this.formData.id)return alert('Debe especificar el ID')
          if(tipo==='categoria'){url=`/api/inventario/editar-categoria/${this.formData.id}/`;method='PUT';payload=this.formData}
          else if(tipo==='uniforme'){
            const f=this.formData
            payload={tipo:f.tipo,talla:f.talla,color:f.color,stock:Number(f.stock||0),material:Number(f.material),categoria:Number(f.categoria)}
            url=`/api/uniformes/${this.formData.id}/`;method='PUT'
          }else{url=`/api/${plural}/${this.formData.id}/`;method='PUT';payload=this.formData}
        }else if(this.accion==='eliminar'){
          if(!this.formData.id)return alert('Debe especificar el ID')
          if(tipo==='categoria'){url=`/api/inventario/eliminar-categoria/${this.formData.id}/`;method='DELETE'}
          else{url=`/api/${plural}/${this.formData.id}/`;method='DELETE'}
        }

        await this.safeApiFetch(url,method,payload)
        alert(`${this.accion} completado con éxito`)
        bus?.emit?.('inventario-actualizado')
        this.cerrarFormulario()
        await this.obtenerInventario(this.tipoFormulario)
        if(this.tipoFormulario==='Categorias')await this.cargarCategorias()
      }catch(e){
        console.error(e)
        const detalle=e?.payload?JSON.stringify(e.payload):e?.message||'Error'
        alert(`Error en la operación: ${detalle}`)
      }
    },
    async obtenerInventario(tipo){
      try{
        const data=await apiFetch(`/api/${tipo.toLowerCase()}/`)
        this.inventarios[tipo]=(Array.isArray(data)?data:[]).map(item=>
          tipo==='Uniformes'?{...item,material_nombre:item.material_nombre||'N/A',categoria_nombre:item.categoria_nombre||'N/A'}:item)
      }catch(e){console.error(`Error al obtener ${tipo}:`,e)}
    },
    async cargarCategorias(){
      try{this.categoriasOptions=await apiFetch('/api/categorias/')}
      catch(e){console.error('Error cargando categorías',e)}
    }
  }
}
</script>

<style scoped>
.inventory-container{min-height:100vh;display:flex;flex-direction:column;}
.close-btn-top{position:absolute;top:10px;left:10px;background:#2B5CA8;border:none;color:#fff;width:40px;height:40px;border-radius:10px;cursor:pointer;font-size:18px;font-weight:800;}
</style>
