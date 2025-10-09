<template>
  <div class="dashboard-container">
    <aside class="sidebar">
      <img src="@/assets/logo_bof_blanco.png" alt="logo del cliente" class="logo" />
      <nav class="nav-links">
        <router-link
          v-for="item in navItems"
          :key="item.label"
          :to="item.route"
          class="nav-item"
        >
          <div class="icon-circle">
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
        <!-- le agregamos ref para observar tamaño -->
        <div class="chart-area" ref="chartAreaEl">
          <canvas id="myPieChart"></canvas>
        </div>

        <!-- hay un color en template, no hace nada -->
        <div class="side-panels">
          <div class="panel panel--calendar">
            <v-calendar
              is-inline
              :is-dark="true"
              color="gray"
              :attributes="calendarAttrs"
              :month-format="{ month: 'long', year: 'numeric' }"
            />
          </div>

          <div class="panel">
            <div class="kpi">
              <h3>Clientes nuevos</h3>
              <p class="value">{{ clientesNuevos }}</p>
              <small>en el mes</small>
            </div>
          </div>
        </div>
      </section>
    </main>

    <transition name="fade-scale">
      <aside
        v-if="showHelp"
        class="help-popover"
        role="dialog"
        aria-modal="true"
        aria-label="Menú de incidencias y soporte"
        ref="helpPanelEl"
      >
        <header class="help-hdr">
          <strong>Incidencias & soporte</strong>
          <button class="help-close" aria-label="Cerrar" @click="showHelp=false">✕</button>
        </header>

        <div class="help-item">
          <div class="help-label">Ayuda por texto</div>
          <a class="help-value" href="https://wa.me/50236902623" target="_blank" rel="noopener">
            +502 36902623
          </a>
        </div>

        <div class="help-item">
          <div class="help-label">Llamada de ayuda</div>
          <a class="help-value" href="tel:+50236902623">+502 36902623</a>
        </div>

        <div class="help-item">
          <div class="help-label">Correos de contacto</div>
          <div class="help-list">
            <a href="mailto:soporte@abriluniformes.com">soporte@abriluniformes.com</a>
            <a href="mailto:incidencias@abriluniformes.com">incidencias@abriluniformes.com</a>
          </div>
        </div>

        <footer class="help-ft">
          <small>Horario: Lun–Vie 9:00–18:00</small>
        </footer>
      </aside>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import Chart from 'chart.js/auto'
import { bus } from '@/event-bus'
import { apiFetch } from '@/utils/api'

import IconClientes from '@/components/icons/IconClientes.vue'
import IconFacturas from '@/components/icons/IconFacturas.vue'
import IconContabilidad from '@/components/icons/IconContabilidad.vue'
import IconInventario from '@/components/icons/IconInventario.vue'
import IconReporteVentas from '@/components/icons/IconRVentas.vue'
import IconUser from '@/components/icons/IconUser.vue'

const navItems = [
  { label: 'Clientes y Proveedores', icon: IconClientes, route: '/clientes' },
  { label: 'Facturas', icon: IconFacturas, route: '/billpage' },
  { label: 'Contabilidad', icon: IconContabilidad, route: '/accounting' },
  { label: 'Inventario', icon: IconInventario, route: '/mi_inventario' },
  { label: 'Reporte de ventas', icon: IconReporteVentas, route: '/ReporteVentas' },
  { label: 'Gestión de Usuarios', icon: IconUser, route: '/register' },
  { label: 'Pedidos', icon: IconUser, route: '/envios' }
]

const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim()
const inventarioData = ref({ Telas:0, Hilos:0, Productos:0 })
const calendarAttrs = ref([{ key: 'hoy', highlight: true, dates: new Date() }])

let pieChart=null
const showHelp = ref(false)
const helpPanelEl = ref(null), helpBtnEl = ref(null)

/* KPI Clientes nuevos */
const clientesNuevos = ref(0)
function pickDateField(sample) {
  if (!sample) return null
  const preferred = [
    'created_at','fecha_registro','creado','fecha_creacion',
    'fecha','fecha_alta','f_creacion','created','createdAt'
  ]
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

/* Popover handler */
const onGlobalClick = e => {
  if (!showHelp.value) return
  const p = helpPanelEl.value, b = helpBtnEl.value
  if (p && !p.contains(e.target) && b && !b.contains(e.target)) showHelp.value = false
}

/* Inventario */
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

/* Chart */
function renderPie(){
  const ctx=document.getElementById('myPieChart')?.getContext('2d');
  if(!ctx) return;
  pieChart?.destroy()

  /* se extraen las claves/nombres de los objetos*/
  const etiquetas = Object.keys(inventarioData.value);

  /*se extraen los valores/inventarioData.value de los objetos*/
  const datos = Object.values(inventarioData.value);

  pieChart=new Chart(ctx,{
    type:'pie',
    data:{
      labels: etiquetas,
      datasets:[{
        data: datos,
        /* se añaden color en script */
        backgroundColor:[css('--color-tertiary')||'#84C8C0',css('--color-septenary')||'#cbd5e1',css('--color-quinary')||'#2B5CA8'],
        borderColor:css('--color-novenary')||'#fff',
        borderWidth:1
      }]
    },
    options:{
      maintainAspectRatio:false,
      plugins:{ legend:{ position:'top' }, title:{ display:true, text:'Inventario' } }
    }
  })
}

/* === NUEVO: ResizeObserver para redimensionar el chart si cambia el contenedor === */
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
  document.removeEventListener('click', onGlobalClick, true)
  ro?.disconnect()
})
/* Live updates */
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
</script>

<style scoped>
/* Layout base */
.dashboard-container{
  display:flex;
  min-height:100vh;
  background: var(--color-octonary, #0f172a); /*nada*/
  color: var(--color-novenary, #fff); /*nada*/
  font-family: 'Kollektif', sans-serif;
}

/* Sidebar */
.sidebar{
  width: 260px;
  background: var(--color-primary, #1e293b); /*nada*/
  display:flex; flex-direction:column; align-items:center;
  padding: 24px 16px;
  border-right: 1px solid rgba(255,255,255,.08); /*borde izquierdo vertical de submenu*/
}
.logo{ width: 140px; height:auto; margin-bottom: 18px; }

.nav-links{ display:flex; flex-direction:column; gap:8px; width:100%; }

/*no pasa nada si se elimina*/
.nav-item{
  display:flex;
  align-items:center;
  gap:12px;
  padding:12px; border-radius:12px;
  color:#e5e7eb; /*nada*/
  text-decoration:none;
  transition: background-color .2s, transform .12s; /*nada*/
}
.nav-item:hover{
  background: rgba(255,255,255,.06); /*color opciones pantallas con cursor arriba*/
  transform: translateX(2px);
}
.nav-item.router-link-active{
  background: rgba(255,255,255,.14); /*nada*/
  color:#fff; /*nada*/
}

.icon-circle{
  width:36px; height:36px;
  border-radius:999px;
  display:grid;
  place-items:center;
  background: rgba(255,255,255,.12); /*fondo circulo opciones pantallas*/
}

/* Main area */
.main-area{ flex:1; display:flex; flex-direction:column; }
.topbar{
  display:flex; align-items:center; justify-content:space-between;
  padding: 14px 20px;
  border-bottom: 1px solid rgba(255,255,255,.1); /*linea inferior de barra superior home*/
  background: rgba(255,255,255,.04); /*fondo de barra superior home*/
  backdrop-filter: blur(4px);
}
.view-name{
  font-weight: 900;
  letter-spacing:.04em;
}

.user-circle{
  width:36px; height:36px; border-radius:999px;border:none; cursor:pointer;
  background: var(--color-quinary, #2B5CA8); /*background: (nada,nada)*/
}

/* Content grid — MÁS espacio para el chart */
.content{
  display:grid;
  grid-template-columns: minmax(0, 3fr) minmax(260px, 1fr); /* antes 2fr 1fr */
  gap: 20px;
  padding: 20px;
}
@media (max-width: 1200px){
  .content{ grid-template-columns: 1fr; }
}

/* Paneles */
.chart-area, .panel{
  background: rgba(255,255,255,.06); /*fondo de fichas items*/
  border: 1px solid rgba(255,255,255,.12); /*borde de fichas items*/
  border-radius: 14px;
  padding: 16px;
}

/* ALTURA GRANDE Y FLUIDA DEL CHART */
.chart-area{
  /* más alto, y además responde a viewport */
  height: clamp(520px, 70vh, 900px);
}
.chart-area canvas, .panel canvas{
  width:100% !important;
  height:100% !important;
}

/* Side panels */
.side-panels{
  display:grid; gap: 20px; grid-auto-rows: minmax(140px, auto);
  align-self: start; /* evita estirar los paneles y roba menos altura al chart */
}

/* Calendar panel */
.panel--calendar :deep(.vc-container){ width:100%; }

/* KPI */
.kpi{ display:grid; gap:6px; align-items:center; justify-items:center; text-align:center; }
.kpi h3{ margin:0; color:#e2e8f0; } /*texto item clientes nuevos*/
.kpi .value{
  font-size:2rem;
  font-weight:900;
  color:#fff; /*nada*/
}

/* Help popover */
.help-popover{
  position: fixed;
  right: 20px; top: 80px;
  width: 320px; max-width: 90vw;
  background:#0b1226; /*fondo tarjeta usuario y fondo de su equis*/
  color:#e5e7eb; /*titulo tarjeta usuario "incidencias & soporte" */
  border:1px solid #223043; /*borde tarjeta de usuario*/
  border-radius: 14px;
  box-shadow: 0 12px 28px rgba(0,0,0,.35); /*sombreado tarjeta de usuario*/
  padding: 14px; z-index: 60;
}
.help-hdr{
  display:flex; align-items:center; justify-content:space-between;
  padding-bottom:8px;
  border-bottom:1px dashed rgba(255,255,255,.15); /*linea entrecortada tarjeta usuario*/
}
.help-close{
  background:transparent; border:none;
  color:#e5e7eb; /*color equis tarjeta usuario*/
  font-size:18px; cursor:pointer;
}
.help-item{ display:grid; grid-template-columns: 1fr auto; gap:8px; padding:10px 0; }
.help-label{ color:#9fb3c8; } /*texto subtitulo tarjeta usuario "ayuda por texto, llamada de ayuda, correo de contacto"*/
.help-value{
  color:#cbd5e1; /*nada*/
  text-decoration:none;
}

.help-value:hover{ text-decoration:underline; }
.help-list{ display:flex; flex-direction:column; gap:6px; }
.help-ft{
  padding-top:8px;
  border-top:1px dashed rgba(255,255,255,.15); /*linea entrecortada parte inferior tarjeta usuario*/
  color:#93a3b8; /*color texto horario en tarjeta usuario*/
}

/* Popover transition */
.fade-scale-enter-active, .fade-scale-leave-active{ transition: all .16s ease; }
.fade-scale-enter-from, .fade-scale-leave-to{ opacity:0; transform: scale(.98); }
</style>
