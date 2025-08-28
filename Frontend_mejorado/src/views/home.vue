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
        <div class="chart-area">
          <canvas id="myPieChart"></canvas>
        </div>

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
            <canvas id="bestMonthChart"></canvas>
          </div>

          <div class="panel">
            <div class="kpi">
              <h3>Clientes nuevos</h3>
              <p class="value">45</p>
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
const MONTHS = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
const inventarioData = ref({ Telas:0, Hilos:0, Uniformes:0 })
const ventasPorMes = ref(Object.fromEntries(MONTHS.map(m => [m,0])))
const calendarAttrs = ref([{ key: 'hoy', highlight: true, dates: new Date() }])

let pieChart=null, barChart=null
const showHelp = ref(false)
const helpPanelEl = ref(null), helpBtnEl = ref(null)

const onGlobalClick = e => {
  if (!showHelp.value) return
  const p = helpPanelEl.value, b = helpBtnEl.value
  if (p && !p.contains(e.target) && b && !b.contains(e.target)) showHelp.value = false
}

async function fetchInventarioData(){
  const endpoints=[['Telas','/api/telas/'],['Hilos','/api/hilos/'],['Uniformes','/api/uniformes/']]
  try{
    const datasets = await Promise.all(endpoints.map(([,p])=>apiFetch(p)))
    datasets.forEach((data,i)=>{
      const k=endpoints[i][0]
      inventarioData.value[k]=Array.isArray(data)?data.reduce((s,it)=>s+(+it.stock||0),0):0
    })
  }catch(e){ console.error('Inventario:',e) }
}

async function fetchVentasMensuales(){
  try{
    const data = await apiFetch('/api/ventas/evolucion/')
    MONTHS.forEach(m=>ventasPorMes.value[m]=0)
    data.forEach(v=>{
      const m=new Date(v.dia).toLocaleString('es-ES',{month:'short'})
      const k=(m[0]?.toUpperCase()||'')+m.slice(1)
      if(k in ventasPorMes.value) ventasPorMes.value[k]+= +v.total||0
    })
  }catch(e){ console.error('Ventas:',e) }
}

function renderPie(){
  const ctx=document.getElementById('myPieChart')?.getContext('2d'); if(!ctx) return
  pieChart?.destroy()
  pieChart=new Chart(ctx,{type:'pie',data:{
    labels:['Telas','Hilos','Uniformes'],
    datasets:[{data:[inventarioData.value.Telas,inventarioData.value.Hilos,inventarioData.value.Uniformes],
      backgroundColor:[css('--color-tertiary')||'#84C8C0',css('--color-septenary')||'#cbd5e1',css('--color-quinary')||'#2B5CA8'],
      borderColor:css('--color-novenary')||'#fff',borderWidth:1}]},
    options:{maintainAspectRatio:false,plugins:{legend:{position:'top'},title:{display:true,text:'Inventario'}}}
  })
}

function renderBar(){
  const ctx=document.getElementById('bestMonthChart')?.getContext('2d'); if(!ctx) return
  barChart?.destroy()
  const labels=MONTHS, values=labels.map(m=>ventasPorMes.value[m]), now=new Date().getMonth()
  barChart=new Chart(ctx,{type:'bar',data:{labels,datasets:[{label:'Ventas',data:values,
    backgroundColor:(c)=>c.dataIndex===now?(css('--color-quinary')||'#2B5CA8'):(css('--color-tertiary')||'#84C8C0'),
    borderColor:css('--color-novenary')||'#fff',borderWidth:1}]},
    options:{maintainAspectRatio:false,plugins:{title:{display:true,text:'Ventas por mes'}}}
  })
}

onMounted(async ()=>{
  document.addEventListener('click', onGlobalClick, true)
  document.addEventListener('keydown', e=>e.key==='Escape'&&(showHelp.value=false))
  await Promise.all([fetchInventarioData(), fetchVentasMensuales()])
  renderPie(); renderBar()
})
setTimeout(() => { pieChart?.resize(); barChart?.resize(); }, 0);

onBeforeUnmount(()=>{
  document.removeEventListener('click', onGlobalClick, true)
})

bus.on('inventario-actualizado', async ()=>{
  await fetchInventarioData()
  if(pieChart){ pieChart.data.datasets[0].data=[inventarioData.value.Telas,inventarioData.value.Hilos,inventarioData.value.Uniformes]; pieChart.update() }
  else renderPie()
})

bus.on('ventas-actualizadas', async ()=>{
  await fetchVentasMensuales()
  if(barChart){ barChart.data.datasets[0].data=MONTHS.map(m=>ventasPorMes.value[m]); barChart.update() }
  else renderBar()
})
</script>

<style scoped>
/* Layout base */
.dashboard-container{
  display:flex;
  min-height:100vh;
  background: var(--color-octonary, #0f172a);
  color: var(--color-novenary, #fff);
  font-family: 'Kollektif', sans-serif;
}

/* Sidebar */
.sidebar{
  width: 260px;
  background: var(--color-primary, #1e293b);
  display:flex; flex-direction:column; align-items:center;
  padding: 24px 16px;
  border-right: 1px solid rgba(255,255,255,.08);
}
.logo{ width: 140px; height:auto; margin-bottom: 18px; }

.nav-links{ display:flex; flex-direction:column; gap:8px; width:100%; }
.nav-item{
  display:flex; align-items:center; gap:12px;
  padding:12px; border-radius:12px; color:#e5e7eb; text-decoration:none;
  transition: background-color .2s, transform .12s;
}
.nav-item:hover{ background: rgba(255,255,255,.06); transform: translateX(2px); }
.nav-item.router-link-active{ background: rgba(255,255,255,.14); color:#fff; }

.icon-circle{
  width:36px; height:36px; border-radius:999px;
  display:grid; place-items:center;
  background: rgba(255,255,255,.12);
}

/* Main area */
.main-area{ flex:1; display:flex; flex-direction:column; }
.topbar{
  display:flex; align-items:center; justify-content:space-between;
  padding: 14px 20px;
  border-bottom: 1px solid rgba(255,255,255,.1);
  background: rgba(255,255,255,.04);
  backdrop-filter: blur(4px);
}
.view-name{ font-weight: 900; letter-spacing:.04em; }
.user-circle{
  width:36px; height:36px; border-radius:999px; border:none; cursor:pointer;
  background: var(--color-quinary, #2B5CA8);
}

/* Content grid */
.content{
  display:grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  padding: 20px;
}
@media (max-width: 1200px){
  .content{ grid-template-columns: 1fr; }
}

/* Cards/panels */
.chart-area, .panel{
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.12);
  border-radius: 14px;
  padding: 16px;
}
.chart-area{ height: 340px; }
.chart-area canvas, .panel canvas{ width:100% !important; height:100% !important; }

.side-panels{ display:grid; gap: 20px; grid-auto-rows: minmax(140px, auto); }

/* Calendar panel */
.panel--calendar :deep(.vc-container){
  width:100%;
}

/* Simple KPI */
.kpi{ display:grid; gap:6px; align-items:center; justify-items:center; text-align:center; }
.kpi h3{ margin:0; color:#e2e8f0; }
.kpi .value{ font-size:2rem; font-weight:900; color:#fff; }

/* Help popover */
.help-popover{
  position: fixed;
  right: 20px; top: 80px;
  width: 320px; max-width: 90vw;
  background:#0b1226; color:#e5e7eb;
  border:1px solid #223043; border-radius: 14px;
  box-shadow: 0 12px 28px rgba(0,0,0,.35);
  padding: 14px; z-index: 60;
}
.help-hdr{
  display:flex; align-items:center; justify-content:space-between;
  padding-bottom:8px; border-bottom:1px dashed rgba(255,255,255,.15);
}
.help-close{
  background:transparent; border:none; color:#e5e7eb; font-size:18px; cursor:pointer;
}
.help-item{ display:grid; grid-template-columns: 1fr auto; gap:8px; padding:10px 0; }
.help-label{ color:#9fb3c8; }
.help-value{ color:#cbd5e1; text-decoration:none; }
.help-value:hover{ text-decoration:underline; }
.help-list{ display:flex; flex-direction:column; gap:6px; }
.help-ft{ padding-top:8px; border-top:1px dashed rgba(255,255,255,.15); color:#93a3b8; }

/* Popover transition */
.fade-scale-enter-active, .fade-scale-leave-active{
  transition: all .16s ease;
}
.fade-scale-enter-from, .fade-scale-leave-to{
  opacity:0; transform: scale(.98);
}
</style>
