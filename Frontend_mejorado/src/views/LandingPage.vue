<template>
  <!-- Landing con carrusel y scrollspy -->
  <div class="landing-container" :class="{ 'menu-open': menuOpen }">
    <!-- Menú lateral (scrollspy) -->
    <nav class="menu-lateral">
      <a
        v-for="item in sections"
        :key="item.id"
        :href="`#${item.id}`"
        :class="{ active: activeSection === item.id }"
      >
        <span class="icon">•</span>
        <span class="label">{{ item.label }}</span>
      </a>
    </nav>

    <!-- HERO -->
    <header id="hero" class="hero">
      <div class="hero-bg">
        <img :src="heroImage" alt="Abril Uniformes" />
      </div>
      <div class="hero-overlay" />
      <div class="hero-content">
        <div class="brand">
          <img src="@/assets/logo_bof_blanco.png" alt="Logo Abril Uniformes" class="logo-header" />
          <h1>Abril Uniformes</h1>
        </div>
        <p class="subtitle">Uniformes que combinan estilo, comodidad y funcionalidad</p>
        <div class="cta">
          <a class="btn btn-primary" :href="whatsappCta" target="_blank" rel="noopener">Cotizar ahora</a>
          <a class="btn btn-ghost" href="#productos">Ver catálogo</a>
        </div>
      </div>
    </header>

    <!-- Misión y Visión -->
    <section class="landing-section mision-vision" id="mision">
      <div class="info-box fade-in">
        <div class="texto">
          <h2>Misión</h2>
          <p>
            Ofrecer bordados personalizados y confección de uniformes médicos e institucionales de alta calidad,
            combinando diseño, funcionalidad y confort. Nos comprometemos a brindar soluciones únicas que reflejen la
            identidad de nuestros clientes y fortalezcan su imagen, con un servicio cercano, profesional y puntual.
          </p>
        </div>
        <img src="@/assets/images/mision.jpg" alt="Imagen de misión" />
      </div>
    </section>

    <section class="landing-section mision-vision" id="vision">
      <div class="info-box reverse fade-in">
        <div class="texto">
          <h2>Visión</h2>
          <p>
            Ser una empresa reconocida en bordados profesionales y confección de uniformes en nuestra región y a nivel
            nacional, reconocida por la calidad, el diseño y la confiabilidad de nuestros productos. Aspiramos a vestir
            e inspirar a profesionales e instituciones con prendas que transmitan identidad, profesionalismo y estilo.
          </p>
        </div>
        <img src="@/assets/images/vision.jpg" alt="Imagen de visión" />
      </div>
    </section>

    <!-- Productos -->
    <section id="productos" class="landing-section productos fade-in">
      <div class="section-head">
        <h2>Nuestros productos</h2>
        <div class="chips">
          <button
            v-for="cat in categorias"
            :key="cat"
            class="chip"
            :class="{ active: filtro === cat }"
            @click="filtro = cat; resetAutoScroll()"
          >
            {{ cat }}
          </button>
        </div>
      </div>

      <!-- Controles del carrusel (desktop) -->
      <button class="car-arrow left" @click="scrollPrev" aria-label="Anterior">‹</button>
      <button class="car-arrow right" @click="scrollNext" aria-label="Siguiente">›</button>

      <!-- Grid desktop / carrusel móvil -->
      <div ref="track" class="productos-track" :class="{ carousel: isMobile }">
        <div
          v-for="producto in productosFiltrados"
          :key="producto.nombre"
          class="producto-card"
          @click="ampliarImagen(producto.imagen)"
        >
          <div class="img-wrap">
            <img :src="producto.imagen" :alt="producto.nombre" />
            <div class="overlay"><span>Ver</span></div>
          </div>
          <p class="nombre">{{ producto.nombre }}</p>
          <span class="tag">{{ producto.categoria }}</span>
        </div>
      </div>
    </section>

    <!-- Modal imagen -->
    <div v-if="imagenAmpliada" class="modal" @click.self="cerrarImagen">
      <img :src="imagenAmpliada" alt="Imagen ampliada" class="imagen-ampliada" />
      <button class="close" @click="cerrarImagen">×</button>
    </div>

    <!-- Contacto -->
    <section id="contacto" class="landing-section contacto fade-in">
      <h2>Contáctanos</h2>

      <div class="contact-grid">
        <form class="contact-form" @submit.prevent="enviarFormulario">
          <div class="row">
            <input v-model="form.nombre" type="text" placeholder="Nombre" required />
            <input v-model="form.email" type="email" placeholder="Email" required />
          </div>
          <textarea v-model="form.mensaje" rows="4" placeholder="Mensaje" required></textarea>
          <button type="submit" class="btn btn-primary">Enviar</button>
        </form>

        <div class="panel-redes">
          <div class="redes redes-iconos">
            <a href="https://www.facebook.com/abriluniformesybordados" target="_blank" aria-label="Facebook"><IconFc /></a>
            <a href="https://www.instagram.com/abril_uniformesborda2" target="_blank" aria-label="Instagram"><IconIg /></a>
            <a href="https://wa.me/message/HDT3ABF7BPCHB1" target="_blank" aria-label="WhatsApp"><IconWs /></a>
          </div>
          <div class="mapa">
            <iframe
              title="Ubicación"
              loading="lazy"
              allowfullscreen
              referrerpolicy="no-referrer-when-downgrade"
              src="https://www.google.com/maps?q=Abril%20Uniformes%20Huehuetenango&output=embed"
            ></iframe>
          </div>
        </div>
      </div>
    </section>

    <!-- Botón login flotante -->
    <router-link to="/login" class="btn-login floating">
      <IconUser class="icono-login" />
      <span>Login</span>
    </router-link>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import IconFc from '@/components/icons/fc.vue'
import IconIg from '@/components/icons/ig.vue'
import IconWs from '@/components/icons/ws.vue'
import IconUser from '@/components/icons/IconUser.vue'

// Hero
const heroImage = new URL('@/assets/images/ep2.jpg', import.meta.url).href

// Productos
const productos = [
  { nombre: 'Uniformes Médicos', categoria: 'Médico', imagen: new URL('@/assets/images/model2.jpg', import.meta.url).href },
  { nombre: 'Gorros Quirúrgicos', categoria: 'Accesorios', imagen: new URL('@/assets/images/gorro.jpg', import.meta.url).href },
  { nombre: 'Uniformes Empresariales', categoria: 'Empresarial', imagen: new URL('@/assets/images/ep2.jpg', import.meta.url).href },
  { nombre: 'Bordados Personalizados', categoria: 'Bordado', imagen: new URL('@/assets/images/bordado1.jpg', import.meta.url).href },
  { nombre: 'Toallas Personalizadas', categoria: 'Bordado', imagen: new URL('@/assets/images/toalla.jpg', import.meta.url).href },
  { nombre: 'Uniformes', categoria: 'Médico', imagen: new URL('@/assets/images/uniformes1.jpg', import.meta.url).href },
]

const categorias = ['Todos', 'Médico', 'Empresarial', 'Bordado', 'Accesorios']
const filtro = ref('Todos')
const imagenAmpliada = ref(null)
const isMobile = ref(false)
const track = ref(null)
let autoTimer = null

const productosFiltrados = computed(() =>
  filtro.value === 'Todos' ? productos : productos.filter(p => p.categoria === filtro.value)
)

const ampliarImagen = (src) => (imagenAmpliada.value = src)
const cerrarImagen = () => (imagenAmpliada.value = null)

const whatsappCta = 'https://wa.me/message/HDT3ABF7BPCHB1'

// Scrollspy
const sections = [
  { id: 'hero', label: 'Inicio' },
  { id: 'mision', label: 'Misión' },
  { id: 'vision', label: 'Visión' },
  { id: 'productos', label: 'Productos' },
  { id: 'contacto', label: 'Contacto' },
]
const activeSection = ref('hero')
let observer

function updateIsMobile() {
  isMobile.value = matchMedia('(max-width: 760px)').matches
}

onMounted(() => {
  updateIsMobile()
  window.addEventListener('resize', updateIsMobile)

  const options = { root: null, rootMargin: '0px', threshold: 0.6 }
  observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) activeSection.value = entry.target.id
    })
  }, options)

  sections.forEach((s) => {
    const el = document.getElementById(s.id)
    if (el) observer.observe(el)
  })

  startAutoScroll()
})

onBeforeUnmount(() => {
  if (observer) observer.disconnect()
  window.removeEventListener('resize', updateIsMobile)
  stopAutoScroll()
})

// Carrusel auto-scroll
function startAutoScroll() {
  stopAutoScroll()
  autoTimer = setInterval(() => {
    if (!track.value) return
    const el = track.value
    const maxScroll = el.scrollWidth - el.clientWidth
    const step = Math.max(220, el.clientWidth * 0.4)

    if (Math.ceil(el.scrollLeft) >= maxScroll - 4) {
      el.scrollTo({ left: 0, behavior: 'smooth' })
    } else {
      el.scrollBy({ left: step, behavior: 'smooth' })
    }
  }, 3500)
}
function stopAutoScroll() {
  if (autoTimer) { clearInterval(autoTimer); autoTimer = null }
}
function resetAutoScroll() { startAutoScroll() }

function scrollNext() {
  if (!track.value) return
  const step = Math.max(260, track.value.clientWidth * 0.6)
  track.value.scrollBy({ left: step, behavior: 'smooth' })
}
function scrollPrev() {
  if (!track.value) return
  const step = Math.max(260, track.value.clientWidth * 0.6)
  track.value.scrollBy({ left: -step, behavior: 'smooth' })
}

// Formulario de contacto → WhatsApp
const form = ref({ nombre: '', email: '', mensaje: '' })
const enviarFormulario = () => {
  const msg = `Hola, soy ${form.value.nombre}. ${form.value.mensaje} (Email: ${form.value.email})`
  window.open(`${whatsappCta}?text=${encodeURIComponent(msg)}`, '_blank')
}

// Menú responsive (si lo usas después)
const menuOpen = ref(false)
</script>

<style scoped>
html { scroll-behavior: smooth; }

:root {
  --bg-1: #0a0f2c;
  --bg-2: #1e293b;
  --brand: #2AA68F;
  --brand-2: #22b893;
  --ink: #e2e8f0;
  --card: #334155;
}

.landing-container {
  font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
  color: white;
  background: linear-gradient(135deg, var(--bg-1), var(--bg-2));
  min-height: 100vh;
  padding-bottom: 6rem;
  position: relative;
}

/* MENÚ LATERAL */
.menu-lateral {
  position: fixed; right: 0.75rem; top: 40%; transform: translateY(-40%);
  display: flex; flex-direction: column; gap: 0.5rem; z-index: 20;
}
.menu-lateral a {
  display: flex; align-items: center; gap: 0.5rem;
  background: rgba(30,41,59,.7); backdrop-filter: blur(6px);
  padding: 0.4rem 0.6rem; border-radius: 999px; text-decoration: none;
  color: #fff; font-weight: 600; font-size: .9rem; transition: .2s ease;
}
.menu-lateral a:hover { background: var(--brand); }
.menu-lateral a.active { background: var(--brand); box-shadow: 0 0 0 3px rgba(42,166,143,.25); }
.menu-lateral .icon { font-size: 1.1rem; line-height: 1; }

/* HERO */
.hero { position: relative; height: 72vh; min-height: 520px; overflow: hidden; }
.hero-bg { position: absolute; inset: 0; }
.hero-bg img { width: 100%; height: 100%; object-fit: cover; filter: saturate(1) contrast(1.05) brightness(.75); }
.hero-overlay { position: absolute; inset: 0; background: radial-gradient(60% 60% at 50% 40%, rgba(255,255,255,.05), transparent), linear-gradient(180deg, rgba(10,15,44,.6), rgba(10,15,44,.9)); }
.hero-content { position: relative; z-index: 1; height: 100%; display: grid; place-items: center; text-align: center; padding: 0 1rem; }
.brand { display: inline-flex; align-items: center; gap: .8rem; flex-wrap: wrap; justify-content: center; }
.logo-header { height: 64px; width: auto; filter: drop-shadow(0 0 4px rgba(0,0,0,.4)); }
.brand h1 { font-size: clamp(2.2rem, 5vw, 3.4rem); margin: 0; letter-spacing: .5px; color: #fff; }
.subtitle { color: var(--ink); margin: .5rem 0 1.2rem; font-size: clamp(1.1rem, 2.8vw, 1.35rem); font-weight: 500; opacity: .95; }
.cta { display: flex; gap: .75rem; justify-content: center; flex-wrap: wrap; }

.btn { border: 2px solid transparent; padding: .75rem 1.2rem; border-radius: 10px; font-weight: 700; text-decoration: none; display: inline-flex; align-items: center; gap: .5rem; }
.btn-primary { background: var(--brand); color: #fff; }
.btn-primary:hover { background: var(--brand-2); }
.btn-ghost { background: transparent; color: #fff; border-color: rgba(255,255,255,.45); }
.btn-ghost:hover { background: rgba(255,255,255,.1); }

/* SECCIONES */
.landing-section { padding: 3rem 1rem; max-width: 1100px; margin: 0 auto; position: relative; }
.landing-section h2 { font-size: 1.9rem; color: var(--brand); border-bottom: 2px solid var(--brand); padding-bottom: .35rem; margin-bottom: .8rem; }
.landing-section p { font-size: 1.08rem; line-height: 1.65; color: var(--ink); }

/* MISIÓN/VISIÓN */
.mision-vision .info-box { display: flex; align-items: center; gap: 2rem; flex-wrap: wrap; background: var(--bg-2); padding: 2rem; border-radius: 16px; box-shadow: 0 10px 24px rgba(0,0,0,.25); }
.mision-vision .info-box.reverse { flex-direction: row-reverse; }
.mision-vision .texto { flex: 1; min-width: 280px; }
.mision-vision img { width: 360px; max-width: 100%; border-radius: 12px; box-shadow: 0 6px 16px rgba(0,0,0,.35); }

/* PRODUCTOS */
.section-head { display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap; }
.chips { display: flex; gap: .5rem; flex-wrap: wrap; }
.chip { background: var(--card); color: #fff; border: 1px solid rgba(255,255,255,.1); border-radius: 999px; padding: .45rem .85rem; font-weight: 600; cursor: pointer; transition: .2s; }
.chip:hover { background: #3b4b63; }
.chip.active { background: var(--brand); }

.productos-track { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.2rem; margin-top: 1.2rem; }
.productos-track.carousel { display: grid; grid-auto-flow: column; grid-auto-columns: 70%; gap: 0.8rem; overflow-x: auto; scroll-snap-type: x mandatory; padding-bottom: .4rem; }
.productos-track.carousel .producto-card { scroll-snap-align: start; }

/* Flechas carrusel (desktop) */
.car-arrow { position: absolute; top: 50%; transform: translateY(-50%); border: none; background: rgba(0,0,0,.3); color: #fff; font-size: 2rem; width: 40px; height: 40px; border-radius: 50%; display: grid; place-items: center; cursor: pointer; z-index: 5; backdrop-filter: blur(4px); }
.car-arrow:hover { background: rgba(0,0,0,.45); }
.car-arrow.left { left: -6px; }
.car-arrow.right { right: -6px; }
@media (max-width: 760px) { .car-arrow { display: none; } }

.producto-card { background: var(--card); border-radius: 14px; padding: .9rem; text-align: center; box-shadow: 0 6px 14px rgba(0,0,0,.25); transition: transform .25s ease, box-shadow .25s ease; cursor: pointer; color: white; }
.producto-card:hover { transform: translateY(-6px); box-shadow: 0 10px 20px rgba(0,0,0,.35); }
.img-wrap { position: relative; border-radius: 10px; overflow: hidden; }
.img-wrap img { width: 100%; height: 180px; object-fit: cover; display: block; transition: transform .35s ease; }
.producto-card:hover .img-wrap img { transform: scale(1.05); }
.overlay { position: absolute; inset: 0; display: grid; place-items: center; background: linear-gradient(180deg, transparent, rgba(0,0,0,.45)); opacity: 0; transition: .25s; font-weight: 700; letter-spacing: .5px; }
.producto-card:hover .overlay { opacity: 1; }
.nombre { margin: .6rem 0 .15rem; font-weight: 700; }
.tag { font-size: .8rem; opacity: .85; background: rgba(255,255,255,.08); border: 1px solid rgba(255,255,255,.12); padding: .2rem .5rem; border-radius: 999px; }

/* MODAL */
.modal { position: fixed; inset: 0; background: rgba(0,0,0,.85); display: grid; place-items: center; z-index: 50; }
.imagen-ampliada { max-width: 92%; max-height: 92%; border-radius: 12px; box-shadow: 0 0 24px rgba(255,255,255,.2); }
.modal .close { position: fixed; top: 1.2rem; right: 1.2rem; font-size: 2rem; background: transparent; border: none; color: #fff; cursor: pointer; }

/* CONTACTO */
.contact-grid { display: grid; grid-template-columns: 1.2fr .8fr; gap: 1.2rem; }
.contact-form { background: var(--bg-2); padding: 1.2rem; border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,.25); }
.contact-form .row { display: grid; grid-template-columns: 1fr 1fr; gap: .8rem; }
.contact-form input, .contact-form textarea { width: 100%; background: #0f172a; border: 1px solid rgba(255,255,255,.1); color: #fff; border-radius: 10px; padding: .75rem .9rem; font-size: .95rem; }
.contact-form textarea { resize: vertical; }
.contact-form button { margin-top: .8rem; }
.panel-redes { display: grid; gap: 1rem; align-content: start; }

/* Íconos redes */
.redes-iconos a { display: inline-flex; align-items: center; justify-content: center; background: #334155; padding: 0.5rem; border-radius: 50%; width: 40px; height: 40px; transition: background 0.3s ease; }
.redes-iconos a:hover { background: var(--brand); }
.redes-iconos svg { fill: white; width: 20px; height: 20px; }

.mapa iframe { width: 100%; height: 240px; border: 0; border-radius: 12px; box-shadow: 0 6px 16px rgba(0,0,0,.25); }

/* LOGIN FLOTANTE */
.btn-login.floating { position: fixed; bottom: 1rem; right: 1rem; background: var(--brand); color: #fff; padding: .7rem 1rem; border-radius: 999px; font-weight: 800; display: inline-flex; align-items: center; gap: .5rem; z-index: 40; text-decoration: none; box-shadow: 0 10px 16px rgba(42,166,143,.35); }
.btn-login.floating:hover { background: var(--brand-2); }
.icono-login { width: 20px; height: 20px; fill: white; }

/* Utilidades */
.fade-in { animation: fadeIn .9s ease both; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: translateY(0); } }

/* Responsive */
@media (max-width: 980px) { .contact-grid { grid-template-columns: 1fr; } }
@media (max-width: 760px) {
  .menu-lateral { right: .4rem; }
  .hero { height: 64vh; }
  .productos-track.carousel { grid-auto-columns: 82%; }
}
</style>
