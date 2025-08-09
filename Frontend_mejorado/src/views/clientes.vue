<script setup>
import { useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'

const router = useRouter()
const go = (path) => router.push(path)

const clientesRecientes = [
  { name:'Comercial Rivera S.A.', meta:'Última compra: 12/06 · Condición 30 días', badge:'Activo' },
  { name:'Boutique La Estación',  meta:'Saldo pendiente: $3,250',               badge:'Seguimiento' },
  { name:'Distribuciones Norte',  meta:'Pedidos últimos 30 días: 5',            badge:'VIP' }
]
const proveedoresRecientes = [
  { name:'Textiles Andinos',   meta:'Entrega 48h · Calidad A',               badge:'Preferente' },
  { name:'Hilaturas del Sur',  meta:'Condición: 30/60 · Respuesta rápida',   badge:'Verificado' },
  { name:'Botones y Más',      meta:'Calificación ★★★★☆',                    badge:'Nuevo' }
]
</script>

<template>
  <div class="crm-home">
    <NavBar title="CLIENTES Y PROVEEDORES" />

    <div class="wrap">
      <main class="cards">
        <!-- CLIENTES -->
        <button class="card card--click" @click="go('/clientesregistro')">
          <header>
            <div class="chip">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>
              </svg>
              Clientes
            </div>
            <span class="count">24 registrados</span>
          </header>

          <ul class="list">
            <li class="row" v-for="c in clientesRecientes" :key="c.name">
              <div>
                <strong>{{ c.name }}</strong><br><small>{{ c.meta }}</small>
              </div>
              <span class="badge">{{ c.badge }}</span>
            </li>
          </ul>

          <div class="footer" @click.stop>
            <button class="btn btn--primary" @click="go('/clientesregistro')">Ver más</button>
          </div>
        </button>

        <!-- PROVEEDORES -->
        <button class="card card--click" @click="go('/proveedores')">
          <header>
            <div class="chip chip--green">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                <path d="M9 3v18M15 3v18M3 9h18M3 15h18"/>
              </svg>
              Proveedores
            </div>
            <span class="count">18 activos</span>
          </header>

          <ul class="list">
            <li class="row" v-for="p in proveedoresRecientes" :key="p.name">
              <div>
                <strong>{{ p.name }}</strong><br><small>{{ p.meta }}</small>
              </div>
              <span class="badge">{{ p.badge }}</span>
            </li>
          </ul>

          <div class="footer" @click.stop>
            <button class="btn btn--green" @click="go('/proveedores')">Ver más</button>
          </div>
        </button>
      </main>
    </div>
  </div>
</template>

<style scoped>
/* === Paleta y tipografías === */
:root {
  --color-primary: #1e293b;
  --color-tertiary: #84C8C0;
  --color-quaternary: #C9E8F5;
  --color-quinary: #2B5CA8;
  --color-senary: #374666;
  --color-septenary: #83A4CC;
  --color-octonary: #0f172a;
  --color-novenary: #ffffff;
  --colo-texto-negro: #000000;
  --colo-texto-blanco: #ffffff;
}

@font-face {
  font-family: 'Archivo Black';
  src: url('./fonts/ArchivoBlack-Regular.ttf') format('truetype');
}
@font-face {
  font-family: 'Kollektif';
  src: url('./fonts/Kollektif.ttf') format('truetype');
}
@font-face {
  font-family: 'Kollektif';
  src: url('./fonts/Kollektif-Bold.ttf') format('truetype');
  font-weight: bold;
}
@font-face {
  font-family: 'Kollektif';
  src: url('./fonts/Kollektif-Italic.ttf') format('truetype');
  font-style: italic;
}
@font-face {
  font-family: 'Kollektif';
  src: url('./fonts/Kollektif-BoldItalic.ttf') format('truetype');
  font-weight: bold;
  font-style: italic;
}

/* === Fondo general === */
.crm-home{
  min-height:100vh;
  background:var(--color-octonary);
  display:flex; flex-direction:column;
  color:var(--color-novenary);
  font-family: 'Kollektif', sans-serif;
}

.wrap{max-width:1280px; margin:0 auto; padding:28px 20px 80px}

/* === Cards grandes === */
.cards{
  display:grid;
  grid-template-columns: repeat(2, minmax(0, 560px));
  justify-content:center;
  gap:28px;
}
@media (max-width:1200px){
  .cards{ grid-template-columns:1fr; }
}
.card{
  background:rgba(255,255,255,.06);
  border-radius:18px;
  border:1px solid rgba(255,255,255,.18);
  padding:24px;
  transition:transform .2s ease;
}
.card--click{cursor:pointer}
.card--click:hover{transform:translateY(-4px)}

.card header{
  display:flex; align-items:center; justify-content:space-between;
  margin-bottom:14px;
  font-family: 'Archivo Black', sans-serif;
}
.chip{
  display:inline-flex; align-items:center; gap:10px;
  padding:12px 14px; border-radius:999px; font-weight:800;
  background:rgba(255,255,255,.14); color:var(--color-novenary);
}
.chip--green{ background:rgba(255,255,255,.14); color:#f5f8f6; }
.count{ color:var(--color-septenary); font-weight:800 }

.list{list-style:none; margin:0; padding:8px 0 4px}
.row{
  display:grid; grid-template-columns:1fr auto; align-items:center;
  padding:14px 8px; border-top:1px dashed rgba(255,255,255,.25);
}
.row:first-child{ border-top:0 }
.row small{ color:var(--color-septenary) }
.badge{
  font-size:.86rem; padding:6px 12px; border-radius:999px;
  background:rgba(255,255,255,.18); color:var(--color-novenary);
}

.footer{ margin-top:18px; display:flex; gap:12px; flex-wrap:wrap }

/* Botones */
.btn{
  padding:12px 16px; border-radius:12px; font-weight:800;
  border:none; cursor:pointer;
  font-family:'Kollektif', sans-serif;
}
.btn--primary{
  background:linear-gradient(180deg,#2B5CA8,#83A4CC);
  color:var(--color-novenary);}
.btn--green{
  background:linear-gradient(180deg,#2B5CA8,#83A4CC);
  color:var(--color-novenary);
}
.btn:hover{ background:var(--color-quaternary); color:var(--colo-texto-negro) }
</style>
