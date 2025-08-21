<template>
  <div class="dashboard-container">
    <aside class="sidebar">
      <img src="@/assets/logo_bof_blanco.png" alt="logo del cliente" class="logo" />
      <nav class="nav-links">
        <router-link v-for="item in navItems" :key="item.label" :to="item.route" class="nav-item">
          <div class="icon-circle"><component v-if="item.icon" :is="item.icon" /><span v-else>🔸</span></div>
          <span>{{ item.label }}</span>
        </router-link>
      </nav>
    </aside>

    <main class="main-area">
      <header class="topbar">
        <div class="view-name">HOME</div>
        <button class="user-circle" aria-label="Abrir menú de incidencias" @click="showHelp=!showHelp" ref="helpBtnEl"></button>
      </header>

      <section class="content">
        <div class="chart-area"><canvas id="myPieChart"></canvas></div>
        <div class="side-panels">
          <div class="panel panel--calendar">
            <v-calendar is-inline :is-dark="true" color="gray" :attributes="calendarAttrs" :month-format="{ month: 'long', year: 'numeric' }"/>
          </div>
          <div class="panel"><canvas id="bestMonthChart"></canvas></div>
          <div class="panel"><div class="kpi"><h3>Clientes nuevos</h3><p class="value">45</p><small>en el mes</small></div></div>
        </div>
      </section>
    </main>

    <transition name="fade-scale">
      <aside v-if="showHelp" class="help-popover" role="dialog" aria-modal="true" aria-label="Menú de incidencias y soporte" ref="helpPanelEl">
        <header class="help-hdr"><strong>Incidencias & soporte</strong><button class="help-close" aria-label="Cerrar" @click="showHelp=false">✕</button></header>
        <div class="help-item"><div class="help-label">Ayuda por texto</div><a class="help-value" href="https://wa.me/50236902623" target="_blank" rel="noopener">+502 36902623</a></div>
        <div class="help-item"><div class="help-label">Llamada de ayuda</div><a class="help-value" href="tel:+50236902623">+502 36902623</a></div>
        <div class="help-item"><div class="help-label">Correos de contacto</div><div class="help-list">
          <a href="mailto:soporte@abriluniformes.com">soporte@abriluniformes.com</a>
          <a href="mailto:incidencias@abriluniformes.com">incidencias@abriluniformes.com</a>
        </div></div>
        <footer class="help-ft"><small>Horario: Lun–Vie 9:00–18:00</small></footer>
      </aside>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import Chart from 'chart.js/auto'
import { bus } from '@/event-bus'
import { BASE_URL } from '@/config'

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
    const resps=await Promise.all(endpoints.map(([,p])=>fetch(`${BASE_URL}${p}`)))
    const datasets=await Promise.all(resps.map(r=>r.json()))
    datasets.forEach((data,i)=>{
      const k=endpoints[i][0]
      inventarioData.value[k]=Array.isArray(data)?data.reduce((s,it)=>s+(+it.stock||0),0):0
    })
  }catch(e){ console.error('Inventario:',e) }
}

async function fetchVentasMensuales(){
  try{
    const res=await fetch(`${BASE_URL}/api/ventas/evolucion/`)
    const data=await res.json()
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
