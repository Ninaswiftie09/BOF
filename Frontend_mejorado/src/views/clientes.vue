<template>
  <div class="page-container">
    <NavBar title="CLIENTES Y PROVEEDORES" />

    <div class="page-content">
      <main class="cards-layout">
        
        <!-- CLIENTES -->
        <router-link to="/clientesregistro" class="card-link">
          <div class="module module-interactive">
            <header class="card-header">
              <div class="chip">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>
                </svg>
                <span>Clientes</span>
              </div>
              <span class="muted-text">{{ clientesCount }} registrados</span>
            </header>

            <ul class="dashed-list" style="flex-grow: 1;">
              <li class="dashed-list-item" v-for="c in clientesRecientes" :key="c.name">
                <div>
                  <strong>{{ c.name }}</strong><br><small>{{ c.meta }}</small>
                </div>
                <span class="badge">{{ c.badge }}</span>
              </li>
            </ul>

            <footer class="card-footer">
              <button class="btn btn-primary" @click.prevent="go('/clientesregistro')">Ver más</button>
            </footer>
          </div>
        </router-link>

        <!-- PROVEEDORES -->
        <router-link to="/proveedores" class="card-link">
          <div class="module module-interactive">
            <header class="card-header">
              <div class="chip">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                  <path d="M9 3v18M15 3v18M3 9h18M3 15h18"/>
                </svg>
                <span>Proveedores</span>
              </div>
              <span class="muted-text">{{ proveedoresCount }} activos</span>
            </header>

            <ul class="dashed-list" style="flex-grow: 1;">
              <li class="dashed-list-item" v-for="p in proveedoresRecientes" :key="p.name">
                <div>
                  <strong>{{ p.name }}</strong><br><small>{{ p.meta }}</small>
                </div>
                <span class="badge">{{ p.badge }}</span>
              </li>
            </ul>

            <footer class="card-footer">
              <button class="btn btn-primary" @click.prevent="go('/proveedores')">Ver más</button>
            </footer>
          </div>
        </router-link>

      </main>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ref, computed, onMounted } from 'vue'
import NavBar from '@/components/NavBar.vue'
import { apiFetch } from '@/utils/api'

const router = useRouter()
const go = (path) => router.push(path)

// Datos reales
const clientes = ref([])
const proveedores = ref([])

// Conteos para los encabezados
const clientesCount = computed(() => clientes.value.length)
const proveedoresCount = computed(() => proveedores.value.length)

// “Recientes” (top 3)
const clientesRecientes = computed(() =>
  clientes.value.slice(0, 3).map(c => ({
    name: c.nombre || c.name || `Cliente ${c.id ?? ''}`,
    meta: c.nit ? `NIT: ${c.nit}` : (c.telefono ? `Tel: ${c.telefono}` : ''),
    badge: 'Activo',
  }))
)

const proveedoresRecientes = computed(() =>
  proveedores.value.slice(0, 3).map(p => ({
    name: p.nombre || p.name || `Proveedor ${p.id ?? ''}`,
    meta: p.telefono ? `Tel: ${p.telefono}` : (p.correo ? `Email: ${p.correo}` : ''),
    badge: 'Preferente',
  }))
)

async function fetchData() {
  try {
    clientes.value = await apiFetch('/api/clientes/')
  } catch (e) {
    console.error('Error cargando clientes:', e)
    clientes.value = []
  }
  try {
    proveedores.value = await apiFetch('/api/proveedores/')
  } catch (e) {
    console.error('Error cargando proveedores:', e)
    proveedores.value = []
  }
}

onMounted(fetchData)
</script>

<style scoped>

.page-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.cards-layout {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  justify-content: center;
  gap: var(--spacing-xl);
  max-width: 1280px;
  margin: 0 auto;
}

.card-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.card-header, .card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-footer {
  margin-top: var(--spacing-md);
}
</style>