<template>
  <div class="module">
    <!-- Toolbar -->
    <div class="toolbar" style="display:flex;gap:12px;align-items:center;justify-content:space-between;">
      <input
        v-if="searchable"
        class="input--white"
        :placeholder="searchPlaceholder"
        :value="search"
        @input="$emit('update:search', $event.target.value)"
        style="max-width:300px"
      />
      <button
        v-if="showAddButton"
        class="btn"
        @click="$emit('add')"
      >
        {{ addLabel }}
      </button>
    </div>

    <!-- Estados -->
    <div v-if="loading" class="muted">Cargando…</div>
    <div v-else-if="error" class="muted" style="color:#ff7b7b">Error: {{ error }}</div>

    <!-- Tabla -->
    <div v-else class="table-wrapper">
      <table class="table dark-table">
        <thead>
          <tr>
            <th v-for="col in columns" :key="col.key">{{ col.label }}</th>
            <th v-if="hasActions" style="width:140px">Acciones</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="row in limitedRows" :key="row[rowKey] ?? JSON.stringify(row)">
            <td v-for="col in columns" :key="col.key">
              <slot :name="`cell:${col.key}`" :row="row" :value="row[col.key]">
                {{ col.format ? col.format(row[col.key], row) : row[col.key] }}
              </slot>
            </td>

            <td v-if="hasActions" class="table-actions" style="justify-content:center">
              <button
                v-if="actions.edit"
                class="icon-btn"
                title="Editar"
                @click.stop="$emit('edit', row)"
              >✎</button>
              <button
                v-if="actions.delete"
                class="icon-btn danger"
                title="Eliminar"
                @click.stop="$emit('delete', row)"
              >✕</button>
            </td>
          </tr>

          <tr v-if="renderedRows.length === 0">
            <td :colspan="columns.length + (hasActions?1:0)" class="muted" style="text-align:center;padding:1.2rem 0;">
              No hay datos para mostrar
            </td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

defineOptions({ name: 'Tablas' })

const props = defineProps({
  /* Datos */
  columns: { type: Array, required: true }, // [{ key, label, format?, searchable? }]
  rows:    { type: Array, required: true },

  /* Opciones */
  rowKey:        { type: String, default: 'id' },
  actions:       { type: Object, default: () => ({ edit:true, delete:true }) },
  searchable:    { type: Boolean, default: true },
  search:        { type: String, default: '' },      // v-model:search
  searchPlaceholder: { type: String, default: 'Buscar…' },
  useLocalFilter: { type: Boolean, default: true },  // true: filtra aquí; false: la vista filtra/consulta

  /* Autolímite */
  maxVisible:    { type: [Number, null], default: 6 }, // null para desactivar

  /* Botones extra */
  showAddButton: { type: Boolean, default: false },
  addLabel:      { type: String, default: 'Agregar' },
  showSeeAll:    { type: Boolean, default: false },

  /* Estado opcional */
  loading: { type: Boolean, default: false },
  error:   { type: [String, null], default: null },
})

const emit = defineEmits(['update:search','add','edit','delete','seeAll'])

const hasActions = computed(
  () => !!props.actions && Object.values(props.actions).some(Boolean)
)

/* Filtrado local */
const renderedRows = computed(() => {
  if (!props.useLocalFilter) return props.rows
  const needle = (props.search || '').trim().toLowerCase()
  if (!needle) return props.rows

  const keys = props.columns
    .filter(c => c.searchable !== false)
    .map(c => c.key)

  return props.rows.filter(r =>
    keys.some(k => String(r?.[k] ?? '').toLowerCase().includes(needle))
  )
})

/* Autolímite */
const expanded = ref(false)
const shouldShowExpand = computed(() =>
  props.maxVisible != null &&
  !expanded.value &&
  renderedRows.value.length > props.maxVisible
)

const limitedRows = computed(() => {
  const base = renderedRows.value
  if (props.maxVisible != null && !expanded.value && base.length > props.maxVisible) {
    return base.slice(0, props.maxVisible)
  }
  return base
})

watch(() => [props.search, props.rows.length], () => {
  expanded.value = false
})
</script>
