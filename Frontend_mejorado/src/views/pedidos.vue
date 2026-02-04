<template>
  <div class="page-container">
    <NavBar title="PEDIDOS">
    </NavBar>

    <div class="page-content">
      <section class="module">

        <div class="toolbar">
           <input v-model="tablaQuery" class="input-dark" placeholder="Buscar pedidos…" style="max-width: 300px;" />
        </div>

        <h2 class="module-title">Historial de pedidos</h2>

        <div class="table-wrapper">
          <table class="table">
            <thead>
              <tr>
                <th v-for="col in columns" :key="col.key">{{ col.label }}</th>
                <th class="text-right">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="fila in filasMostradas" :key="fila.key">
                <td v-for="col in columns" :key="col.key">{{ fila[col.key] }}</td>
                <td class="actions">
                  <button class="icon-btn" title="Ver detalle" @click="abrirFormulario('ver', fila)">+</button>
                  <button class="icon-btn edit" title="Editar" @click="abrirFormulario('editar', fila)">✎</button>
                  <button class="icon-btn delete" title="Eliminar" @click="abrirFormulario('eliminar', fila)">✕</button>
                </td>
              </tr>
              <tr v-if="!filas.length && !cargando">
                <td :colspan="columns.length + 1" class="muted-text" style="text-align:center; padding: 1.5rem;">
                  No se encontraron pedidos.
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="footer-actions">
          <button class="btn btn-secondary" @click="abrirVerTodos">Ver Todos</button>
          <button class="btn btn-primary" @click="abrirFormulario('agregar')">Agregar Pedido</button>
        </div>
      </section>
    </div>

    <!-- Modal CRUD -->
    <div v-if="formVisible" class="modal-overlay" @click.self="cerrarFormulario">
      <div class="modal-content-dark modal-wide" style="max-height: 90vh; overflow-y: auto;">
        <h3 v-if="accion==='agregar'">Agregar Nuevo Pedido</h3>
        <h3 v-else-if="accion==='editar'">Editar Pedido #{{ formData.id }}</h3>
        <h3 v-else-if="accion==='ver'">Detalle del Pedido #{{ formData.id }}</h3>
        <h3 v-else>Eliminar Pedido #{{ formData.id }}</h3>

        <form v-if="accion!=='eliminar'" @submit.prevent="submitFormulario">
          <div class="form-grid" style="grid-template-columns: 2fr 1fr 1fr; margin-bottom: 1.5rem;">
            <div class="form-group">
              <label class="form-label">Cliente</label>
              <select  v-model.number="formData.cliente"  class="form-input"  :disabled="soloLectura"  required>
                <option :value="''" disabled>Selecciona un cliente</option>
                <option v-for="c in clientes" :key="c.id" :value="c.id">{{ c.nombre }}</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Fecha</label>
              <input  type="date"  v-model="formData.fecha"  class="form-input"  :disabled="soloLectura"/>
            </div>
            <div class="form-group">
              <label class="form-label">Método de pago</label>
              <select  v-model="formData.metodo_pago"  class="form-input"  :disabled="soloLectura"  required>
                <option value="efectivo">Efectivo</option>
                <option value="transferencia">Transferencia</option>
                <option value="tarjeta">Tarjeta</option>
                <option value="otro">Otro</option>
              </select>
            </div>
            <div class="form-grid" style="margin-bottom: 1.5rem;">
              <div class="form-group full-width">
                <label class="form-label">Descripción</label>
                <textarea class="form-input" v-model="formData.descripcion" placeholder="Escribe una descripción opcional…" :readonly="soloLectura"></textarea>
              </div>

              <div class="form-group">
                <label class="form-label">Anticipo (Q)</label>
                <input type="number" min="0" class="form-input" v-model.number="formData.anticipo" @input="recalcularTotales" :disabled="soloLectura" />
              </div>

              <div class="form-group">
                <label class="form-label">Estado</label>
                <select v-model="formData.estado" class="form-input" :disabled="soloLectura">
                  <option value="en_proceso">En proceso</option>
                  <option value="cerrado">Cerrado</option>
                  <option value="cancelado">Cancelado</option>
                </select>
              </div>
            </div>
          </div>

          <h4 class="module-title" style="font-size: 1.2rem; margin-bottom: 1rem;">Detalles del Pedido</h4>
          <div class="details-grid details-grid-header">
            <span>Producto</span>
            <span>Cantidad</span>
            <span>Precio Unitario</span>
            <span>Total</span>
            <span></span>
          </div>
          
          <div style="max-height: 300px; overflow-y: auto;">
            <div v-for="(d, i) in formData.detalles" :key="i" class="details-grid">
              <select v-model.number="d.producto" class="form-input" @change="onProductoSelectChange(i)" :disabled="soloLectura">
                <option :value="null" disabled>Selecciona un producto</option>
                <option v-for="u in todosUniformes" :key="u.id" :value="u.id">{{ u.tipo }} (Stock: {{ u.stock }})</option>
              </select>
              <input type="number" min="1" v-model.number="d.cantidad" class="form-input" @input="recalcularTotales" :disabled="soloLectura" />
              <input type="number" step="0.01" min="0" v-model.number="d.precio_unitario" class="form-input" @input="recalcularTotales" placeholder="Q0.00" :disabled="soloLectura"/>
              <div class="details-grid-cell total">Q{{ toMoney((d.cantidad || 0) * (d.precio_unitario || 0)) }}</div>
              <button type="button" class="icon-btn delete" @click="quitarDetalle(i)">✕</button>
            </div>
          </div>

          <button v-if="!soloLectura" type="button" class="btn btn-secondary" @click="agregarDetalle" style="margin-top: 1rem;">+ Agregar línea</button>

          <div class="totals-section">
            <div class="totals-row"><span>Subtotal:</span><strong>Q{{ toMoney(subtotal) }}</strong></div>
            <div class="totals-row">
              <span>Anticipo:</span>
              <strong>Q{{ toMoney(formData.anticipo || 0) }}</strong>
            </div>
            <div class="totals-row final">
              <span>Total a pagar:</span>
              <strong>Q{{ toMoney((subtotal || 0) - (formData.anticipo || 0)) }}</strong>
            </div>
          </div>
                                                                                                                                                                                             

          <div class="modal-actions">
            <button type="button" class="btn btn-secondary" @click="cerrarFormulario">Cancelar</button>
            <button type="submit" class="btn btn-primary">{{ accion==='agregar' ? 'Guardar' : 'Actualizar' }}</button>
          </div>
        </form>

        <div v-else>
          <p>¿Seguro que deseas eliminar el pedido <strong>#{{ formData.id }}</strong>?</p>
          <div class="modal-actions">
            <button type="button" class="btn btn-secondary" @click="cerrarFormulario">Cancelar</button>
            <button class="btn btn-danger" @click="submitFormulario">Confirmar Eliminación</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal VER TODOS -->
    <div v-if="verTodosVisible" class="modal-overlay" @click.self="cerrarVerTodos">
      <div class="modal-content-dark modal-wide">
        <div class="modal-header">
          <h3>Pedidos - Lista Completa</h3>
          <button class="icon-btn" @click="cerrarVerTodos" title="Cerrar">✕</button>
        </div>
        <div class="table-wrapper" style="max-height: 70vh; overflow-y: auto;">
          <table class="table">
            <thead>
              <tr>
                <th v-for="c in columns" :key="c.key">{{ c.label }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="r in filasFiltradas" :key="r.key">
                <td v-for="c in columns" :key="c.key">{{ r[c.key] }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch, onBeforeUnmount } from 'vue';
import { apiFetch } from '@/utils/api';
import NavBar from '@/components/NavBar.vue';

const tablaQuery = ref('');
const verTodosVisible = ref(false);
const formVisible = ref(false);
const accion = ref('agregar');
const cargando = ref(false);
const filas = ref([]);
const clientes = ref([]);
const todosUniformes = ref([]);
const soloLectura = computed(() => accion.value === 'ver');

const columns = [
  { key: 'cliente_nombre', label: 'Cliente' },
  { key: 'fecha_fmt', label: 'Fecha' },
  { key: 'metodo_pago', label: 'Método' },
  { key: 'producto', label: 'Producto' },
  { key: 'faltante', label: 'Faltante' },
  { key: 'estado', label: 'Estado' }
];

const formData = reactive({
  id: null, cliente: '', fecha: '', metodo_pago: 'efectivo', estado: 'en_proceso', descripcion: '', anticipo: 0, detalles: [], precio_total: 0
});

const toMoney = (n) => Number(n || 0).toLocaleString('es-GT', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const formatFecha = (iso) => iso ? new Date(iso).toLocaleDateString('es-GT') : '';

const filasFiltradas = computed(() => {
  const q = tablaQuery.value.trim().toLowerCase();
  if (!q) return filas.value;
  return filas.value.filter(r =>
    Object.values(r).some(v => String(v).toLowerCase().includes(q))
  );
});

const filasMostradas = computed(() => filasFiltradas.value.slice(0, 6));

const subtotal = computed(() =>
  (formData.detalles || []).reduce((acc, d) => acc + (Number(d.cantidad) || 0) * (Number(d.precio_unitario) || 0), 0)
);

watch(subtotal, (val) => { formData.precio_total = val; });

const cargarClientes = async () => {
  try {
    const data = await apiFetch('/api/clientes/');
    clientes.value = Array.isArray(data) ? data : (data?.results || []);
  } catch (e) { console.error("Error cargando clientes", e); }
};

const cargarTodosUniformes = async () => {
  try {
    const data = await apiFetch('/api/uniformes/');
    todosUniformes.value = Array.isArray(data) ? data : (data?.results || []);
  } catch (e) { console.error("Error cargando uniformes", e); }
};

const cargarFilas = async () => {
  cargando.value = true;
  try {
    const data = await apiFetch('/api/ventas/detalles/');
    const list = Array.isArray(data) ? data : (data?.results || []);

    filas.value = list.map(venta => {
      const faltante = Number(venta.total || 0) - Number(venta.anticipo || 0);

      return {
        key: `venta-${venta.id}`,
        id: venta.id,
        cliente_nombre: venta.cliente_nombre || 'N/A',
        fecha: venta.fecha,
        fecha_fmt: formatFecha(venta.fecha),
        metodo_pago: venta.metodo_pago,
        estado: venta.estado || 'N/A',
        producto: venta.detalles?.map(d =>
          d.producto.nombre || d.producto.tipo
        ).join(', ') || 'N/A',
        total: venta.total,
        total_fmt: `Q${toMoney(venta.total)}`,
        faltante: `Q${toMoney(faltante)}`
      };
    }).sort((a, b) => new Date(b.fecha) - new Date(a.fecha));

  } catch (e) {
    console.error("Error cargando pedidos", e);
  } finally {
    cargando.value = false;
  }
};



// Lógica para autocompletar precio (cuando ya haya una tabla de precios en backend)
const onProductoSelectChange = (index) => {
//1. encontrar detalle y producto
const detalle = formData.detalles[index];
const productoSeleccionado = todosUniformes.value.find(u => u.id === detalle.producto);
//2. si se encontro se asigna
if (productoSeleccionado) {
    // cambiar 'precio' por nombre real del campo en backend
    detalle.precio_unitario = productoSeleccionado.precio || 0; 
}
      recalcularTotales();
};


const recalcularTotales = () => { formData.precio_total = subtotal.value; };

const abrirFormulario = async (acc, row = null) => {
  document.body.classList.add('modal-open');
  accion.value = acc;

  // RESET LIMPIO SIEMPRE
  Object.assign(formData, {
    id: null,
    cliente: '',
    fecha: new Date().toISOString().slice(0, 10),
    metodo_pago: 'efectivo',
    descripcion: '',
    estado: 'en_proceso',
    anticipo: 0,
    detalles: [],
    precio_total: 0
  });

  if (acc === 'agregar') {
    formData.detalles.push({
      producto: null,
      cantidad: 1,
      precio_unitario: 0
    });
  }
  
  if (acc === 'ver' && row) {
    const data = await apiFetch(`/api/ventas/${row.id}/recibo/`);

    Object.assign(formData, {
      id: data.id,
      cliente: data.cliente.id,
      fecha: data.fecha,
      metodo_pago: data.metodo_pago,
      descripcion: data.descripcion || '',
      estado: data.estado || 'en_proceso',
      anticipo: Number(data.anticipo) || 0,
      detalles: data.detalles.map(d => ({
        id: d.id,
        producto: d.producto.id,
        cantidad: Number(d.cantidad),
        precio_unitario: Number(d.precio_unitario)
      })),
      precio_total: Number(data.total)
    });
  }


  if (acc === 'editar' && row) {
    const data = await apiFetch(`/api/ventas/${row.id}/recibo/`);

    Object.assign(formData, {
      id: data.id,
      cliente: data.cliente.id,
      fecha: data.fecha,
      metodo_pago: data.metodo_pago,
      descripcion: data.descripcion || '',
      estado: data.estado || 'en_proceso',
      anticipo: Number(data.anticipo) || 0,
      detalles: data.detalles.map(d => ({
        id: d.id,
        producto: d.producto.id,
        cantidad: Number(d.cantidad),
        precio_unitario: Number(d.precio_unitario)
      })),
      precio_total: Number(data.total)
    });
  }

  if (acc === 'eliminar' && row) {
    formData.id = row.id;
  }

  formVisible.value = true;
};


const cerrarFormulario = () => { document.body.classList.remove('modal-open'); formVisible.value = false; };
const agregarDetalle = () => { formData.detalles.push({ producto: null, cantidad: 1, precio_unitario: 0 }); };
const quitarDetalle = (i) => { formData.detalles.splice(i, 1); recalcularTotales(); };
const abrirVerTodos = () => { document.body.classList.add('modal-open'); verTodosVisible.value = true; };
const cerrarVerTodos = () => { document.body.classList.remove('modal-open'); verTodosVisible.value = false; };


const actualizarInventario = async (detalles) => {
  try {
    for (const d of detalles) {
      const idUniforme = Number(d.producto);
      const cantidadVendida = Number(d.cantidad);
      if (!idUniforme || cantidadVendida <= 0) continue;

      // Obtener uniforme actual
      const uniforme = await apiFetch(`/api/uniformes/${idUniforme}/`);
      if (!uniforme || typeof uniforme.stock !== 'number') continue;

      // Calcular y actualizar stock
      const nuevoStock = Math.max(0, uniforme.stock - cantidadVendida);
      await apiFetch(`/api/uniformes/${idUniforme}/`, 'PUT', { ...uniforme, stock: nuevoStock });
    }
  } catch (error) {
    console.error("Error actualizando inventario:", error);
  }
};

const estadoMap = {
  en_proceso: 'pendiente',
  cerrado: 'completada',
  cancelado: 'cancelada'
};


const submitFormulario = async () => {
  try {
    if (accion.value === 'eliminar') {
      await apiFetch(`/api/ventas/eliminar/${formData.id}/`, 'DELETE');
    } else {
      const detalles = (formData.detalles || []).filter(d => d.producto && d.cantidad > 0 && d.precio_unitario >= 0);
      if (detalles.length === 0) {
        alert("Agregue al menos un producto válido con cantidad y precio."); return;
      }
      
      for (const d of detalles) {
        const uniforme = todosUniformes.value.find(u => u.id === d.producto);
        if (!uniforme) {
          alert(`El producto con ID ${d.producto} no existe.`); return;
        }
        if (d.cantidad > uniforme.stock) {
          alert(`No hay suficiente stock para "${uniforme.tipo}". Solo quedan ${uniforme.stock} unidades.`); return;
        }
      }

      const payload = {
        cliente: formData.cliente,
        fecha: formData.fecha,
        metodo_pago: formData.metodo_pago,
        estado: estadoMap[formData.estado] || 'pendiente',
        descripcion: formData.descripcion,
        anticipo: Number(formData.anticipo) || 0,
        detalles: detalles.map(d => ({
          producto: Number(d.producto),
          cantidad: Number(d.cantidad),
          precio_unitario: Number(d.precio_unitario) || 0,
          ...(accion.value === 'editar' && d.id && { id: d.id })
        }))
      };



      if (accion.value === 'editar') {
        await apiFetch(`/api/ventas/editar/${formData.id}/`, 'PUT', payload);
      } else {
        await apiFetch(`/api/ventas/crear/`, 'POST', payload);
        //Descontar stock después de crear la venta
        await actualizarInventario(detalles);
      }
    }
    cerrarFormulario();
    await cargarFilas();
    await cargarTodosUniformes();
  } catch (e) {
    console.error("Error al guardar pedido:", e);
    alert("Ocurrió un error. Verifique los datos.");
  }
};

onMounted(async () => {
  await cargarClientes();
  await cargarTodosUniformes();
  await cargarFilas();
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
.footer-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-lg);
}
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--spacing-md);
}
.toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: var(--spacing-md);
}

.productos-scroll {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 1rem;
}
</style>