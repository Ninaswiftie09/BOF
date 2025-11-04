<template>
  <div class="dashboard-container">
    <aside class="sidebar">
      <img src="@/assets/logo_bof_blanco.png" alt="logo del cliente" class="logo" />
      <nav class="sidebar-nav">
        <router-link
          v-for="item in navItems"
          :key="item.label"
          :to="item.route"
          class="sidebar-nav-item"
        >
          <div class="sidebar-nav-icon">
            <component v-if="item.icon" :is="item.icon" />
            <span v-else>🔸</span>
          </div>
          <span>{{ item.label }}</span>
        </router-link>
      </nav>
    </aside>

    <main class="main-area">
      <header class="topbar">
        <div class="view-name">HOME</div>
        <button
          class="user-circle"
          aria-label="Abrir menú de incidencias"
          @click="showHelp=!showHelp"
          ref="helpBtnEl"
        ></button>
      </header>

      <section class="content">
        <div class="dashboard-panel chart-area" ref="chartAreaEl">
          <canvas id="myPieChart"></canvas>
        </div>

        <div class="side-panels">
          <div class="dashboard-panel panel--calendar">
            <v-calendar
              is-inline
              class="vc-dark"
              color="gray"
              :attributes="calendarAttrs"
              :month-format="{ month: 'long', year: 'numeric' }"
            />
          </div>

          <div class="dashboard-panel kpi-panel">
            <h3>Clientes nuevos</h3>
            <p class="value">{{ clientesNuevos }}</p>
            <small class="muted-text">en el mes</small>
          </div>
        </div>
      </section>
    </main>

    <transition name="fade-scale">
      <aside
        v-if="showHelp"
        class="popover-menu"
        role="dialog"
        aria-modal="true"
        aria-label="Menú de incidencias y soporte"
        ref="helpPanelEl"
        style="right: 20px; top: 80px; width: 320px;"
      >
        <header class="popover-header">
          <strong>Incidencias & soporte</strong>
          <button class="icon-btn" aria-label="Cerrar" @click="showHelp=false" style="font-size: 1.2rem;">✕</button>
        </header>

        <div class="popover-item">
          <span>Ayuda por texto</span>
          <a href="https://wa.me/50236902623" target="_blank" rel="noopener">+502 36902623</a>
        </div>

        <div class="popover-item">
          <span>Llamada de ayuda</span>
          <a href="tel:+50236902623">+502 36902623</a>
        </div>
        
        <hr style="border-color: rgba(255, 255, 255, 0.15); margin: 8px 0;" />

        <button @click="logout" class="btn btn-danger">
          Cerrar sesión
        </button>
      </aside>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed, watch } from 'vue'
import Chart from 'chart.js/auto'
import { bus } from '@/event-bus'
import { apiFetch } from '@/utils/api'
import { useAuthStore } from '@/stores/auth'
import { usePermissionsStore } from '@/stores/permissions'
import IconClientes from '@/components/icons/IconClientes.vue'
import IconFacturas from '@/components/icons/IconFacturas.vue'
import IconContabilidad from '@/components/icons/IconContabilidad.vue'
import IconInventario from '@/components/icons/IconInventario.vue'
import IconReporteVentas from '@/components/icons/IconRVentas.vue'
import IconUser from '@/components/icons/IconUser.vue'
import { useRouter } from 'vue-router'


const router = useRouter()

async function logout () {
  try {
    // await fetch('/api/logout/', { method: 'POST', credentials: 'include' })
  } catch (err) {
    console.warn('No se pudo contactar el backend en logout:', err)
  }
  showHelp.value = false
  sessionStorage.clear()
  localStorage.removeItem('isLoggedIn')
  router.push('/login')
}

const authStore = useAuthStore()
const permissions = usePermissionsStore()

const allNavItems = [
  { label: 'Clientes y Proveedores', icon: IconClientes, route: '/clientes', requiredModule: 'clientes', requiredAction: 'ver' },
  { label: 'Facturas', icon: IconFacturas, route: '/billpage', requiredModule: 'facturas', requiredAction: 'ver' },
  { label: 'Contabilidad', icon: IconContabilidad, route: '/accounting', requiredModule: 'metricas', requiredAction: 'ver', adminOnly: true },
  { label: 'Inventario', icon: IconInventario, route: '/mi_inventario', requiredModule: 'inventario', requiredAction: 'ver' },
  { label: 'Reporte de ventas', icon: IconReporteVentas, route: '/ReporteVentas', requiredModule: 'ventas', requiredAction: 'reportes', adminOnly: true },
  { label: 'Gestión de Usuarios', icon: IconUser, route: '/register', adminOnly: true },
  { label: 'Pedidos', icon: IconUser, route: '/envios', requiredModule: 'ventas', requiredAction: 'ver' }
]

const navItems = computed(() => {
  return allNavItems.filter(item => {
    if (item.adminOnly && !authStore.isAdmin) return false
    if (item.requiredModule && item.requiredAction) {
      if (!permissions.can(item.requiredModule, item.requiredAction)) return false
    }
    return true
  })
})

const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim()
const inventarioData = ref({ Telas:0, Hilos:0, Productos:0 })
const calendarAttrs = ref([{ key: 'hoy', highlight: true, dates: new Date() }])
let pieChart=null
const showHelp = ref(false)
const helpPanelEl = ref(null), helpBtnEl = ref(null)
const clientesNuevos = ref(0)
function pickDateField(sample) {
  if (!sample) return null
  const preferred = ['created_at','fecha_registro','creado','fecha_creacion','fecha','fecha_alta','f_creacion','created','createdAt']
  for (const k of preferred) if (sample[k] && !isNaN(Date.parse(sample[k]))) return k
  for (const [k,v] of Object.entries(sample)) {
    if (typeof v === 'string' && !isNaN(Date.parse(v)) && /fecha|date|crea|alta|reg/i.test(k)) return k
  }
  return null
}
async function fetchClientesCount() {
  try {
    const data = await apiFetch('/api/clientes/')
    const list = Array.isArray(data) ? data : (Array.isArray(data?.results) ? data.results : [])
    if (!list.length) { clientesNuevos.value = Number.isFinite(data?.count) ? data.count : 0; return }
    const field = pickDateField(list[0])
    const start = new Date(); start.setDate(1); start.setHours(0,0,0,0)
    const end = new Date(start); end.setMonth(start.getMonth()+1)
    clientesNuevos.value = field
      ? list.filter(c => { const t=Date.parse(c[field]); return !isNaN(t) && t>=+start && t<+end }).length
      : list.length
  } catch (e) { console.error('KPI clientes nuevos:', e); clientesNuevos.value = 0 }
}
const onGlobalClick = e => {
  if (!showHelp.value) return
  const p = helpPanelEl.value, b = helpBtnEl.value
  if (p && !p.contains(e.target) && b && !b.contains(e.target)) showHelp.value = false
}
async function fetchInventarioData(){
  const endpoints=[['Telas','/api/telas/'],['Hilos','/api/hilos/'],['Productos','/api/uniformes/']]
  try{
    const datasets = await Promise.all(endpoints.map(([,p])=>apiFetch(p)))
    datasets.forEach((data,i)=>{
      const k=endpoints[i][0]
      inventarioData.value[k]=Array.isArray(data)?data.reduce((s,it)=>s+(+it.stock||0),0):0
    })
  }catch(e){ console.error('Inventario:',e) }
}
function renderPie(){
  const ctx=document.getElementById('myPieChart')?.getContext('2d');
  if(!ctx) return;
  pieChart?.destroy()
  const etiquetas = Object.keys(inventarioData.value);
  const datos = Object.values(inventarioData.value);
  pieChart=new Chart(ctx,{
    type:'pie',
    data:{
      labels: etiquetas,
      datasets:[{
        data: datos,
        backgroundColor:[css('--color-action-primary'),css('--color-action-secondary'),css('--color-icon-edit')],
        borderColor: '#fff',
        borderWidth:1
      }]
    },
    options:{
      maintainAspectRatio:false,
      plugins:{ legend:{ position:'top' }, title:{ display:true, text:'Inventario' } }
    }
  })
}
const chartAreaEl = ref(null)
let ro
function initResizeObserver(){
  if (!chartAreaEl.value) return
  ro = new ResizeObserver(() => { pieChart?.resize() })
  ro.observe(chartAreaEl.value)
}
onMounted(async ()=>{
  document.addEventListener('click', onGlobalClick, true)
  document.addEventListener('keydown', e=>e.key==='Escape'&&(showHelp.value=false))
  await Promise.all([fetchInventarioData(), fetchClientesCount()])
  renderPie()
  initResizeObserver()
})
onBeforeUnmount(()=>{
  document.removeEventListener('click', onGlobalClick, true);
  document.body.classList.remove('modal-open');
  ro?.disconnect();
})
bus.on('clientes-actualizados', ({ nuevosMes }) => {
  if (typeof nuevosMes === 'number') clientesNuevos.value = nuevosMes
})
bus.on('inventario-actualizado', async ()=>{
  await fetchInventarioData()
  if(pieChart){
    pieChart.data.datasets[0].data=Object.values(inventarioData.value)
    pieChart.update()
  } else
    renderPie()
})

watch(showHelp, (isOpen) => {
  if (isOpen) {
    document.body.classList.add('modal-open');
  } else {
    document.body.classList.remove('modal-open');
  }
});



</script>

<style scoped>
.dashboard-container {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 260px;
  background: var(--color-surface-sidebar);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--spacing-lg) var(--spacing-md);
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  flex-shrink: 0;
}

.logo {
  width: 140px;
  height: auto;
  margin-bottom: var(--spacing-lg);
}

.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-sm) var(--spacing-lg);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  background: var(--color-surface-topbar);
  backdrop-filter: blur(4px);
  flex-shrink: 0;
}

.view-name {
  font-weight: 900;
  letter-spacing: 0.04em;
}

.user-circle {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  background-color: var(--color-action-primary);
}

.content {
  display: grid;
  grid-template-columns: minmax(0, 3fr) minmax(260px, 1fr);
  gap: var(--spacing-lg);
  padding: var(--spacing-lg);
  flex-grow: 1;
}

@media (max-width: 1200px) {
  .content {
    grid-template-columns: 1fr;
  }
}

.chart-area {
  height: clamp(520px, 70vh, 900px);
}

.chart-area canvas {
  width: 100% !important;
  height: 100% !important;
}

.side-panels {
  display: grid;
  gap: var(--spacing-lg);
  grid-auto-rows: min-content;
  align-self: start;
}

.panel--calendar :deep(.vc-container) {
  width: 100%;
}

.kpi-panel {
  display: grid;
  gap: 6px;
  align-items: center;
  justify-items: center;
  text-align: center;
}

.fade-scale-enter-active, .fade-scale-leave-active{ transition: all .16s ease; }
.fade-scale-enter-from, .fade-scale-leave-to{ opacity:0; transform: scale(.98); }
</style>