<template>
  <div class="page-container">
    <NavBar title="PEDIDOS">
      <template #actions>
        <input v-model="tablaQuery" class="input-dark" placeholder="Buscar pedidos…" style="max-width: 300px;" />
      </template>
    </NavBar>

    <div class="page-content">
      <section class="module">
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
                  <button class="icon-btn edit" @click="abrirFormulario('editar', fila)">✎</button>
                  <button class="icon-btn delete" @click="abrirFormulario('eliminar', fila)">✕</button>
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
      <div class="modal-content-dark modal-wide">
        <h3 v-if="accion==='agregar'">Agregar Nuevo Pedido</h3>
        <h3 v-else-if="accion==='editar'">Editar Pedido #{{ formData.id }}</h3>
        <h3 v-else>Eliminar Pedido #{{ formData.id }}</h3>

        <!-- AGREGAR / EDITAR -->
        <form v-if="accion!=='eliminar'" @submit.prevent="submitFormulario">
          <div class="form-grid" style="grid-template-columns: 2fr 1fr 1fr; margin-bottom: 1.5rem;">
            <div class="form-group">
              <label class="form-label">Cliente</label>
              <select v-model.number="formData.cliente" class="form-input" required>
                <option :value="''" disabled>Selecciona un cliente</option>
                <option v-for="c in clientes" :key="c.id" :value="c.id">{{ c.nombre }}</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Fecha</label>
              <input type="date" v-model="formData.fecha" class="form-input" />
            </div>
            <div class="form-group">
              <label class="form-label">Método de pago</label>
              <select v-model="formData.metodo_pago" class="form-input" required>
                <option value="efectivo">Efectivo</option>
                <option value="transferencia">Transferencia</option>
                <option value="tarjeta">Tarjeta</option>
                <option value="otro">Otro</option>
              </select>
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

          <div v-for="(d, i) in formData.detalles" :key="i" class="details-grid">
            <select v-model.number="d.producto" class="form-input" @change="onProductoSelectChange(i)">
              <option :value="null" disabled>Selecciona un producto</option>
              <option v-for="u in todosUniformes" :key="u.id" :value="u.id">{{ u.tipo }} (Stock: {{ u.stock }})</option>
            </select>
            <input type="number" min="1" v-model.number="d.cantidad" class="form-input" @input="recalcularTotales" />
            <input type="number" step="0.01" min="0" v-model.number="d.precio_unitario" class="form-input" @input="recalcularTotales" />
            <div class="details-grid-cell total">Q{{ toMoney((d.cantidad || 0) * (d.precio_unitario || 0)) }}</div>
            <button type="button" class="icon-btn delete" @click="quitarDetalle(i)">✕</button>
          </div>

          <button type="button" class="btn btn-secondary" @click="agregarDetalle" style="margin-top: 1rem;">+ Agregar línea</button>

          <div class="totals-section">
            <div class="totals-row"><span>Subtotal:</span><strong>Q{{ toMoney(subtotal) }}</strong></div>
            <div class="totals-row final"><span>Total:</span><strong>Q{{ toMoney(formData.precio_total) }}</strong></div>
          </div>

          <div class="modal-actions">
            <button type="button" class="btn btn-secondary" @click="cerrarFormulario">Cancelar</button>
            <button type="submit" class="btn btn-primary">{{ accion==='agregar' ? 'Guardar' : 'Actualizar' }}</button>
          </div>
        </form>

        <!-- ELIMINAR -->
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
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { apiFetch } from '@/utils/api';
import NavBar from '@/components/NavBar.vue';

const tablaQuery = ref('');
const verTodosVisible = ref(false);
const formVisible = ref(false);
const accion = ref('agregar');
const filas = ref([]);
const clientes = ref([]);
const todosUniformes = ref([]);

const columns = [
  { key: 'cliente_nombre', label: 'Cliente' },
  { key: 'fecha_fmt', label: 'Fecha' },
  { key: 'metodo_pago', label: 'Método' },
  { key: 'producto', label: 'Producto' },
  { key: 'total_fmt', label: 'Total' }
];

const formData = reactive({
  id: null, cliente: '', fecha: '', metodo_pago: 'efectivo', detalles: [], precio_total: 0
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
  } catch(e) { console.error("Error cargando clientes", e); }
};

const cargarTodosUniformes = async () => {
  try {
    const data = await apiFetch('/api/uniformes/');
    todosUniformes.value = Array.isArray(data) ? data : (data?.results || []);
  } catch (e) { console.error("Error cargando uniformes", e); }
};

const cargarFilas = async () => {
  try {
    const data = await apiFetch('/api/ventas/detalles/');
    const list = Array.isArray(data) ? data : (data?.results || []);
    
    filas.value = list.map(venta => ({
      key: venta.id,
      id: venta.id,
      cliente_nombre: venta.cliente_nombre || 'N/A',
      fecha: venta.fecha,
      fecha_fmt: formatFecha(venta.fecha),
      metodo_pago: venta.metodo_pago,
      producto: venta.detalles?.map(d => d.producto.nombre).join(', ') || 'N/A',
      total: venta.total,
      total_fmt: `Q${toMoney(venta.total)}`
    })).sort((a, b) => new Date(b.fecha) - new Date(a.fecha));

  } catch(e) { console.error("Error cargando pedidos", e); }
};

const onProductoSelectChange = (index) => {
  const detalle = formData.detalles[index];
  const productoSeleccionado = todosUniformes.value.find(u => u.id === detalle.producto);
  if (productoSeleccionado) {
    detalle.precio_unitario = productoSeleccionado.stock || 0; 
  }
  recalcularTotales();
};

const recalcularTotales = () => { formData.precio_total = subtotal.value; };

const abrirFormulario = async (acc, row = null) => {
  accion.value = acc;
  if (acc === 'agregar') {
    Object.assign(formData, {
      id: null, cliente: '', fecha: new Date().toISOString().slice(0, 10),
      metodo_pago: 'efectivo', detalles: [{ producto: null, cantidad: 1, precio_unitario: 0 }], precio_total: 0
    });
  } else if (row) {
    const data = await apiFetch(`/api/ventas/${row.id}/recibo/`);
    Object.assign(formData, {
      id: data.id,
      cliente: data.cliente.id,
      fecha: data.fecha,
      metodo_pago: data.metodo_pago,
      detalles: data.detalles.map(d => ({...d, producto: d.producto.id})),
      precio_total: data.total
    });
  }
  formVisible.value = true;
};

const cerrarFormulario = () => { formVisible.value = false; };
const agregarDetalle = () => { formData.detalles.push({ producto: null, cantidad: 1, precio_unitario: 0 }); };
const quitarDetalle = (i) => { formData.detalles.splice(i, 1); recalcularTotales(); };
const abrirVerTodos = () => { verTodosVisible.value = true; };
const cerrarVerTodos = () => { verTodosVisible.value = false; };

const submitFormulario = async () => {
  try {
    if (accion.value === 'eliminar') {
      await apiFetch(`/api/ventas/eliminar/${formData.id}/`, 'DELETE');
    } else {
      const payload = {
        ...formData,
        detalles: formData.detalles.filter(d => d.producto && d.cantidad > 0)
      };
      if (payload.detalles.length === 0) {
        alert("Agregue al menos un producto válido.");
        return;
      }
      if (accion.value === 'editar') {
        await apiFetch(`/api/ventas/editar/${formData.id}/`, 'PUT', payload);
      } else {
        await apiFetch(`/api/ventas/crear/`, 'POST', payload);
      }
    }
    cerrarFormulario();
    await cargarFilas();
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
</style>