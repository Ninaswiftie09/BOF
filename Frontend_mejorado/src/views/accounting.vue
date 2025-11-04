<template>
  <div class="page-container">
    <NavBar title="SISTEMA DE CONTABILIDAD">
      <template #actions>
        <input v-model="search" class="input-dark" placeholder="Buscar operaciones…" />
      </template>
    </NavBar>

    <div class="page-content">
      <!-- Resumen -->
      <section class="summary-grid">
        <div class="summary-card">
          <h3>INGRESOS</h3>
          <p>Q{{ summary.ingresos.toLocaleString() }}</p>
        </div>
        <div class="summary-card">
          <h3>GASTOS</h3>
          <p>Q{{ summary.egresos.toLocaleString() }}</p>
        </div>
        <div class="summary-card">
          <h3>BALANCE</h3>
          <p>Q{{ summary.balance.toLocaleString() }}</p>
        </div>
        <div class="summary-card">
          <h3>OPERACIONES</h3>
          <p>{{ summary.total }}</p>
        </div>
      </section>

      <!-- Tabla principal -->
      <section class="module">
        <div class="module-header">
          <h2 class="module-title">OPERACIONES RECIENTES</h2>
          <div class="flex-group">
            <button class="btn btn-secondary" @click="abrirVerTodos">VER TODO</button>
            <button class="btn btn-primary" @click="openNew">AGREGAR MOVIMIENTO</button>
          </div>
        </div>

        <div class="table-wrapper">
          <table class="table">
            <thead>
              <tr>
                <th v-for="col in columns" :key="col.key">{{ col.label }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in tableRows.slice(0,6)" :key="row.id">
                <td v-for="col in columns" :key="col.key">{{ row[col.key] }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>

    <!-- Modal: nueva operación -->
    <div v-if="modalOpen" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content-dark">
        <h3>NUEVA OPERACIÓN</h3>
        <form @submit.prevent="addOperation">
          <div class="form-group">
            <label class="form-label">Tipo</label>
            <select class="form-input" v-model="newOperation.tipo" required>
              <option value="ingreso">Ingreso</option>
              <option value="egreso">Egreso</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Monto (Q)</label>
            <input class="form-input" type="number" step="0.01" min="0.01" v-model.number="newOperation.monto" required />
          </div>

          <div class="form-group">
            <label class="form-label">Concepto</label>
            <textarea class="form-input" v-model="newOperation.concepto" maxlength="250" required style="min-height: 80px;"></textarea>
          </div>

          <div class="modal-actions">
            <button type="button" class="btn btn-secondary" @click="closeModal">Cancelar</button>
            <button type="submit" class="btn btn-primary">Guardar</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal: Ver Todo -->
    <div v-if="verTodosVisible" class="modal-overlay" @click.self="cerrarVerTodos">
      <div class="modal-content-dark modal-wide">
        <div class="modal-header">
          <h3>OPERACIONES - LISTA COMPLETA</h3>
          <button class="icon-btn" @click="cerrarVerTodos" title="Cerrar">✕</button>
        </div>
        <div class="table-wrapper" style="max-height: 70vh; overflow-y: auto;">
          <table class="table">
            <thead>
              <tr>
                <th v-for="col in columns" :key="col.key">{{ col.label }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in tableRows" :key="row.id">
                <td v-for="col in columns" :key="col.key">{{ row[col.key] }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch, onBeforeUnmount } from 'vue'
import { apiFetch } from '@/utils/api'
import NavBar from '@/components/NavBar.vue'

const operations = ref([])
const summary = reactive({ ingresos: 0, egresos: 0, balance: 0, total: 0 })
const search = ref('')
const modalOpen = ref(false)
const verTodosVisible = ref(false)
const newOperation = reactive({ tipo: 'ingreso', monto: '', concepto: '' })

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'tipo', label: 'TIPO' },
  { key: 'concepto', label: 'CONCEPTO' },
  { key: 'monto', label: 'MONTO' },
  { key: 'fecha', label: 'FECHA' },
]

const filteredOperations = computed(() => {
  const q = search.value.trim().toLowerCase()
  if (!q) return operations.value
  return operations.value.filter(op => {
    const monto = Number(op.monto)?.toString() ?? ''
    return [op.tipo, op.concepto, op.fecha, monto]
      .some(v => v.toString().toLowerCase().includes(q))
  })
})

const tableRows = computed(() =>
  filteredOperations.value.map(op => ({
    ...op,
    tipo: op.tipo === 'ingreso' ? 'Ingreso' : 'Egreso',
    monto: `Q${Number(op.monto).toLocaleString()}`,
  }))
)

const calculateSummary = () => {
  let ingresos = 0, egresos = 0
  operations.value.forEach(op => {
    if (op.tipo === 'ingreso') ingresos += Number(op.monto)
    else if (op.tipo === 'egreso') egresos += Number(op.monto)
  })
  summary.ingresos = ingresos
  summary.egresos = egresos
  summary.balance = ingresos - egresos
  summary.total = operations.value.length
}

const fetchOperations = async () => {
  try {
    const data = await apiFetch('/api/operaciones/')
    operations.value = Array.isArray(data) ? data : (data?.results || [])
    calculateSummary()
  } catch (error) {
    console.error('Error cargando operaciones:', error)
  }
}

const openNew = () => { modalOpen.value = true }
const closeModal = () => { modalOpen.value = false }
const abrirVerTodos = () => {
  document.body.classList.add('modal-open');
  verTodosVisible.value = true;
};
const cerrarVerTodos = () => {
  document.body.classList.remove('modal-open');
  verTodosVisible.value = false;
};

const addOperation = async () => {
  if (!newOperation.monto || !newOperation.concepto.trim()) {
    alert('Completa todos los campos'); return
  }
  try {
    const payload = {
      tipo: newOperation.tipo,
      monto: parseFloat(newOperation.monto),
      concepto: newOperation.concepto,
      fecha: new Date().toISOString().slice(0, 10),
    }
    const data = await apiFetch('/api/operaciones/', 'POST', payload)
    operations.value.push(data)
    calculateSummary()
    closeModal()
    Object.assign(newOperation, { tipo: 'ingreso', monto: '', concepto: '' })
  } catch (error) {
    console.error('Error agregando operación:', error)
    alert('Error al agregar la operación')
  }
}

onMounted(fetchOperations);

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

.module-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.module-title {
  font-family: 'Archivo Black', sans-serif;
  font-size: 1.2rem;
}

.form-group + .form-group {
  margin-top: var(--spacing-md);
}
</style>