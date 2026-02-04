<template>
  <div class="page-container">
    <NavBar title="INVENTARIO">
      <template #actions>
        <input v-model="search" class="input-dark" placeholder="Buscar en inventario…" style="max-width: 300px;" />
      </template>
    </NavBar>

    <div class="page-content">
      <div
        v-for="(items, tipo) in filteredInventarios"
        :key="tipo"
        class="module"
      >
        <div class="module-header">
          <h2 class="module-title">{{ titulosVisibles[tipo] || tipo }}</h2>
        </div>

        <!-- Tabla de Inventario -->
        <div class="table-wrapper">
          <table class="table">
            <thead>
              <tr>
                <th v-for="col in columnsByTipo[tipo]" :key="col.key">{{ col.label }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in items.slice(0, 6)" :key="item.id">
                <td v-for="col in columnsByTipo[tipo]" :key="col.key">
                  {{ item[col.key] || 'N/A' }}
                </td>
              </tr>
              <tr v-if="items.length === 0">
                <td :colspan="columnsByTipo[tipo].length" class="muted-text" style="text-align: center; padding: 1rem;">
                  No hay elementos en esta categoría.
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Botonera -->
        <div class="footer-actions">
          <button class="btn btn-secondary" @click="abrirFormulario('editar', tipo)">Editar</button>
          <button class="btn btn-danger" @click="abrirFormulario('eliminar', tipo)">Eliminar</button>
          <button class="btn btn-primary" @click="abrirFormulario('agregar', tipo)">Agregar</button>
          <button class="btn btn-secondary" @click="abrirVerTodos(tipo)">Ver Todos</button>
        </div>
      </div>
    </div>

    <!-- ============== Modal Formulario (Agregar/Editar/Eliminar) ============== -->
    <div v-if="formVisible" class="modal-overlay" @click.self="cerrarFormulario">
      <div class="modal-content-dark">
        <h3 v-if="accion === 'agregar'">Agregar: {{ titulosVisibles[tipoFormulario] }}</h3>
        <h3 v-else-if="accion === 'editar'">Editar: {{ titulosVisibles[tipoFormulario] }}</h3>
        <h3 v-else-if="accion === 'eliminar'">Eliminar: {{ titulosVisibles[tipoFormulario] }}</h3>

        <form @submit.prevent="submitFormulario" class="form-grid">
          <!-- Selector para Editar o Eliminar -->
          <template v-if="accion === 'editar' || accion === 'eliminar'">
            <div class="form-group full-width">
              <label class="form-label">Seleccionar elemento</label>
              <select class="form-input" v-model.number="seleccionId" @change="autoCompletarProducto" required>
                <option :value="null" disabled>Seleccione una opción...</option>
                <option v-for="item in inventarios[tipoFormulario]" :key="item.id" :value="item.id">
                  {{ formatearProducto(item) }}
                </option>
              </select>
            </div>
          </template>

          <!-- Campos del formulario (solo para Agregar/Editar) -->
          <template v-if="accion !== 'eliminar'">
            <template v-if="tipoFormulario === 'Telas'">
              <div class="form-group"><label class="form-label">Nombre</label><input class="form-input" v-model="formData.nombre" /></div>
              <div class="form-group"><label class="form-label">Tipo</label><input class="form-input" v-model="formData.tipo" /></div>
              <div class="form-group"><label class="form-label">Composición</label><input class="form-input" v-model="formData.composicion" /></div>
              <div class="form-group"><label class="form-label">Color</label><input class="form-input" v-model="formData.color" /></div>
              <div class="form-group"><label class="form-label">Código</label><input class="form-input" v-model="formData.codigo" /></div>
              <div class="form-group"><label class="form-label">Stock</label><input type="number" class="form-input" v-model.number="formData.stock" /></div>
              <div class="form-group full-width"><label class="form-label">Descripción</label><textarea class="form-input" v-model="formData.descripcion"></textarea></div>
            </template>

            <template v-else-if="tipoFormulario === 'Hilos'">
              <div class="form-group"><label class="form-label">Nombre</label><input class="form-input" v-model="formData.nombre" /></div>
              <div class="form-group"><label class="form-label">Material</label><input class="form-input" v-model="formData.material" /></div>
              <div class="form-group"><label class="form-label">Código Color</label><input class="form-input" v-model="formData.codigo_color" /></div>
              <div class="form-group"><label class="form-label">Color</label><input class="form-input" v-model="formData.color" /></div>
              <div class="form-group"><label class="form-label">Código</label><input class="form-input" v-model="formData.codigo" /></div>
              <div class="form-group"><label class="form-label">Stock</label><input type="number" class="form-input" v-model.number="formData.stock" /></div>
              <div class="form-group full-width"><label class="form-label">Descripción</label><textarea class="form-input" v-model="formData.descripcion"></textarea></div>
            </template>

            <template v-else-if="tipoFormulario === 'Uniformes'">
              <div class="form-group"><label class="form-label">Tipo</label><input class="form-input" v-model="formData.tipo" /></div>
              <div class="form-group"><label class="form-label">Talla</label><input class="form-input" v-model="formData.talla" /></div>
              <div class="form-group"><label class="form-label">Color</label><input class="form-input" v-model="formData.color" /></div>
              <div class="form-group"><label class="form-label">Stock</label><input type="number" class="form-input" v-model.number="formData.stock" /></div>
              <div class="form-group">
                <label class="form-label">Tela relacionada</label>
                <select class="form-input" v-model.number="formData.material">
                  <option :value="null" disabled>Seleccione una tela</option>
                  <option v-for="t in inventarios.Telas" :key="t.id" :value="t.id">{{ t.nombre || `${t.tipo} (${t.color})` }}</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Categoría</label>
                <select class="form-input" v-model.number="formData.categoria">
                  <option :value="null" disabled>Seleccione una categoría</option>
                  <option v-for="c in categoriasOptions" :key="c.id" :value="c.id">{{ c.nombre }}</option>
                </select>
              </div>
            </template>

            <template v-else-if="tipoFormulario === 'Categorias'">
              <div class="form-group full-width">
                <label class="form-label">Nombre</label>
                <input class="form-input" v-model="formData.nombre" required />
              </div>
            </template>
          </template>

          <div class="modal-actions full-width">
            <button type="button" class="btn btn-secondary" @click="cerrarFormulario">Cancelar</button>
            <button type="submit" class="btn" :class="{ 'btn-primary': accion !== 'eliminar', 'btn-danger': accion === 'eliminar' }">
              {{ accion === 'agregar' ? 'Guardar' : accion === 'editar' ? 'Actualizar' : 'Confirmar Eliminación' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Ver Todos -->
    <div v-if="verTodosVisible" class="modal-overlay" @click.self="cerrarVerTodos">
      <div class="modal-content-dark modal-wide">
        <div class="modal-header">
          <h3>{{ titulosVisibles[tipoVerTodos] || tipoVerTodos }} - Lista Completa</h3>
            <button class="icon-btn" @click="cerrarVerTodos" title="Cerrar">✕</button>
        </div>
        
        <div class="table-wrapper" style="max-height: 70vh; overflow-y: auto;">
          <table class="table">
            <thead>
              <tr>
                <th v-for="col in columnsByTipo[tipoVerTodos]" :key="col.key">{{ col.label }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in inventarios[tipoVerTodos]" :key="item.id">
                <td v-for="col in columnsByTipo[tipoVerTodos]" :key="col.key">{{ item[col.key] || 'N/A' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onBeforeUnmount } from 'vue';
import { bus } from '@/event-bus';
import NavBar from '@/components/NavBar.vue';
import { apiFetch } from '@/utils/api';

const search = ref('');
const inventarios = reactive({ Telas: [], Hilos: [], Uniformes: [], Categorias: [] });
const titulosVisibles = { Telas: 'Telas', Hilos: 'Hilos', Uniformes: 'Productos', Categorias: 'Categorías' };

const columnsByTipo = {
  Telas: [
    { key: 'id', label: 'ID' },
    { key: 'nombre', label: 'Nombre' },
    { key: 'tipo', label: 'Tipo' },
    { key: 'color', label: 'Color' },
    { key: 'codigo', label: 'Código' },
    { key: 'stock', label: 'Stock' }
  ],
  Hilos: [
    { key: 'id', label: 'ID' },
    { key: 'nombre', label: 'Nombre' },
    { key: 'material', label: 'Material' },
    { key: 'color', label: 'Color' },
    { key: 'codigo', label: 'Código' },
    { key: 'stock', label: 'Stock' }
  ],
  Uniformes: [
    { key: 'id', label: 'ID' },
    { key: 'tipo', label: 'Tipo' },
    { key: 'talla', label: 'Talla' },
    { key: 'color', label: 'Color' },
    { key: 'stock', label: 'Stock' },
    { key: 'categoria_nombre', label: 'Categoría' },
    { key: 'material_nombre', label: 'Tela' }
  ],
  Categorias: [
    { key: 'id', label: 'ID' },
    { key: 'nombre', label: 'Nombre' }
  ]
};

const formVisible = ref(false);
const tipoFormulario = ref('');
const accion = ref('');
const formData = reactive({});
const seleccionId = ref(null);
const categoriasOptions = ref([]);

const verTodosVisible = ref(false);
const tipoVerTodos = ref('');

const abrirFormulario = (acc, tipo) => {
  accion.value = acc;
  tipoFormulario.value = tipo;
  formVisible.value = true;
  Object.keys(formData).forEach(k => delete formData[k]);
  seleccionId.value = null;
  if (tipo === 'Uniformes' || tipo === 'Categorias') cargarCategorias();
};

const cerrarFormulario = () => {
  formVisible.value = false;
};

const abrirVerTodos = (tipo) => {
  tipoVerTodos.value = tipo;
  verTodosVisible.value = true;
};
const cerrarVerTodos = () => {
  verTodosVisible.value = false;
};

const formatearProducto = (item) => {
  return tipoFormulario.value === 'Uniformes'
    ? `${item.id} - ${item.tipo} ${item.talla}`
    : `${item.id} - ${item.nombre || item.tipo}`;
};

const autoCompletarProducto = () => {
  if (!seleccionId.value) return;
  const item = inventarios[tipoFormulario.value]?.find(p => p.id === seleccionId.value);
  if (item) Object.assign(formData, item);
};

const submitFormulario = async () => {
  try {
    const tipo = tipoFormulario.value.toLowerCase().slice(0, -1);
    let method = '', url = '', body = { ...formData };

    if (tipo === 'categoria') {
      if (accion.value === 'agregar') {
        await apiFetch('/api/inventario/agregar-nueva-categoria/', 'POST', body);
      } else if (accion.value === 'editar') {
        await apiFetch(`/api/inventario/editar-categoria/${formData.id}/`, 'PUT', body);
      } else if (accion.value === 'eliminar') {
        await apiFetch(`/api/inventario/eliminar-categoria/${seleccionId.value}/`, 'DELETE');
      }
    } else {
      const plural = tipoFormulario.value.toLowerCase();
      if (accion.value === 'agregar') {
        url = `/api/${plural}/`;
        method = 'POST';
      } else if (accion.value === 'editar') {
        url = `/api/${plural}/${formData.id}/`;
        method = 'PUT';
      } else if (accion.value === 'eliminar') {
        url = `/api/${plural}/${seleccionId.value}/`;
        method = 'DELETE';
        body = null;
      }

      await apiFetch(url, method, body);
    }

    bus.emit('inventario-actualizado');
    cerrarFormulario();
    alert('Operación completada correctamente');
  } catch (err) {
    console.error('Error en operación:', err);
    alert(err?.payload?.message || err.message || 'Error desconocido');
  }
}



const cargarCategorias = async () => {
  try {
    categoriasOptions.value = await apiFetch('/api/categorias/');
  } catch (e) {
    console.error('Error cargando categorías', e);
  }
};

const obtenerInventario = async (tipo) => {
  try {
    const data = await apiFetch(`/api/${tipo.toLowerCase()}/`);
    inventarios[tipo] = Array.isArray(data) ? data.map(item =>
      tipo === 'Uniformes'
        ? {
            ...item,
            material_nombre: item.material_nombre || 'N/A',
            categoria_nombre: item.categoria_nombre || 'N/A'
          }
        : item
    ) : [];
  } catch (e) {
    console.error(`Error obteniendo ${tipo}:`, e);
  }
};

const filteredInventarios = computed(() => {
  const q = search.value.toLowerCase().trim();
  if (!q) return inventarios;
  const result = {};
  for (const tipo in inventarios) {
    result[tipo] = inventarios[tipo].filter(item =>
      Object.values(item).some(val =>
        String(val).toLowerCase().includes(q)
      )
    );
  }
  return result;
});

onMounted(() => {
  const tipos = ['Telas', 'Hilos', 'Uniformes', 'Categorias'];
  tipos.forEach(obtenerInventario);
  cargarCategorias();

  bus.on('inventario-actualizado', () => {
    tipos.forEach(obtenerInventario);
    cargarCategorias();
  });
});

onBeforeUnmount(() => {
  document.body.classList.remove('modal-open');
});
</script>


<style scoped>
.page-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.page-content .module + .module {
  margin-top: var(--spacing-xl);
}

.module-header {
  margin-bottom: var(--spacing-md);
}

.module-title {
  font-family: 'Archivo Black', sans-serif;
  font-size: 1.5rem;
}

.footer-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-lg);
  flex-wrap: wrap;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--spacing-md);
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.modal-actions.full-width {
  grid-column: 1 / -1;
}
</style>