<template>
  <div class="landing-container">
    <!-- Menú flotante -->
    <nav class="menu-lateral">
      <a href="#mision">Misión</a>
      <a href="#vision">Visión</a>
      <a href="#productos">Productos</a>
      <a href="#contacto">Contacto</a>
    </nav>

    <!-- Título principal -->
    <header class="titulo-principal fade-in">
      <div class="titulo-con-logo">
        <img src="@/assets/logo_bof_blanco.png" alt="Logo de Abril Uniformes" class="logo-header" />
        <h1>Abril Uniformes</h1>
      </div>
      <p>Uniformes que distinguen</p>
    </header>

    <!-- Misión y Visión -->
    <section class="landing-section mision-vision">
      <div id="mision" class="info-box fade-in">
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

      <div id="vision" class="info-box reverse fade-in">
        <div class="texto">
          <h2>Visión</h2>
          <p>
            Ser una empresa reconocida en bordados profesionales y confección de uniformes en nuestra región y a nivel nacional,
             reconocida por la calidad, el diseño y la confiabilidad de nuestros productos. Aspiramos a vestir e inspirar a profesionales
              e instituciones con prendas que transmitan identidad, profesionalismo y estilo.
          </p>
        </div>
        <img src="@/assets/images/vision.jpg" alt="Imagen de visión" />
      </div>
    </section>

    <!-- Productos -->
    <section id="productos" class="landing-section productos fade-in">
      <h2>Nuestros productos</h2>
      <div class="productos-grid">
        <div
          v-for="producto in productos"
          :key="producto.nombre"
          class="producto-card"
          @click="ampliarImagen(producto.imagen)"
        >
          <img :src="producto.imagen" :alt="producto.nombre" />
          <p>{{ producto.nombre }}</p>
        </div>
      </div>
    </section>

    <!-- Modal para ampliar imagen -->
    <div v-if="imagenAmpliada" class="modal" @click.self="cerrarImagen">
      <img :src="imagenAmpliada" alt="Imagen ampliada" class="imagen-ampliada" />
    </div>

    <!-- Contacto -->
    <section id="contacto" class="landing-section fade-in">
      <h2>Contáctanos</h2>
      <div class="redes redes-iconos">
        <a href="https://www.facebook.com/abriluniformesybordados" target="_blank" aria-label="Facebook"><IconFc /></a>
        <a href="https://www.instagram.com/abril_uniformesborda2" target="_blank" aria-label="Instagram"><IconIg /></a>
        <a href="https://wa.me/message/HDT3ABF7BPCHB1" target="_blank" aria-label="WhatsApp"><IconWs /></a>
      </div>
    </section>

    <!-- Botón login -->
    <div class="ingreso-login fade-in">
      <router-link to="/login" class="btn-login">
  <IconUser class="icono-login" />
  Login
</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import IconFc from '@/components/icons/fc.vue'
import IconIg from '@/components/icons/ig.vue'
import IconWs from '@/components/icons/ws.vue'
import IconUser from '@/components/icons/IconUser.vue'



const productos = [
  { nombre: 'Uniformes Médicos', imagen: new URL('@/assets/images/model2.jpg', import.meta.url).href },
  { nombre: 'Gorros Quirúrgicos', imagen: new URL('@/assets/images/gorro.jpg', import.meta.url).href },
  { nombre: 'Uniformes Empresariales', imagen: new URL('@/assets/images/ep2.jpg', import.meta.url).href },
  { nombre: 'Bordados Personalizados', imagen: new URL('@/assets/images/bordado1.jpg', import.meta.url).href },
  { nombre: 'Toallas Personalizadas', imagen: new URL('@/assets/images/toalla.jpg', import.meta.url).href },
  { nombre: 'Uniformes ', imagen: new URL('@/assets/images/uniformes1.jpg', import.meta.url).href },
  
]

const imagenAmpliada = ref(null)
const ampliarImagen = (src) => {
  imagenAmpliada.value = src
}
const cerrarImagen = () => {
  imagenAmpliada.value = null
}
</script>

<style scoped>
html {
  scroll-behavior: smooth;
}

.landing-container {
  font-family: 'Segoe UI', sans-serif;
  padding-bottom: 4rem;
  background: #0a0f2c;
  color: white;
}

/* Título principal */
.titulo-principal {
  text-align: center;
  padding: 2rem 1rem 1rem;
  background-color: #1e293b;
  border-bottom: 2px solid #334155;
}

.titulo-con-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.logo-header {
  height: 60px;
  width: auto;
  filter: drop-shadow(0 0 4px rgba(0, 0, 0, 0.4));
}

.titulo-principal h1 {
  font-size: 3rem;
  color: #2AA68F;
  text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.5);
  margin: 0;
}

.titulo-principal p {
  font-size: 1.2rem;
  color: #cbd5e1;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
}

/* Misión y visión */
.mision-vision .info-box {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 2rem;
  margin-bottom: 3rem;
  flex-wrap: wrap;
  background-color: #1e293b;
  padding: 2rem;
  border-radius: 12px;
}

.mision-vision .info-box.reverse {
  flex-direction: row-reverse;
}

.mision-vision .texto {
  flex: 1;
  min-width: 280px;
}

.mision-vision img {
  width: 300px;
  max-width: 100%;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

/* Secciones */
.landing-section {
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
}

.landing-section h2 {
  font-size: 1.8rem;
  color: #2AA68F;
  border-bottom: 2px solid #2AA68F;
  padding-bottom: 0.3rem;
  margin-bottom: 0.5rem;
}

.landing-section p {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #e2e8f0;
}

/* Productos */
.productos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.producto-card {
  background: #334155;
  padding: 1rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  color: white;
}

.producto-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.producto-card img {
  width: 100%;
  height: 140px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

/* Modal imagen */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.imagen-ampliada {
  max-width: 90%;
  max-height: 90%;
  border-radius: 12px;
  box-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
}

/* Redes sociales */
.redes {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 1rem;
}

.redes-iconos a {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #334155;
  padding: 0.5rem;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  transition: background 0.3s ease;
}

.redes-iconos a:hover {
  background: #2AA68F;
}

.redes-iconos svg {
  fill: white;
  width: 24px;
  height: 24px;
}

/* Botón login */
.btn-login {
  background: #2AA68F;
  color: white;
  padding: 0.75rem 2rem;
  border-radius: 8px;
  font-weight: bold;
  text-decoration: none;
  transition: background 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-login:hover {
  background: #22b893;
}

.icono-login {
  width: 20px;
  height: 20px;
  fill: white;
}


/* Menú lateral */
.menu-lateral {
  position: fixed;
  top: 40%;
  right: 0;
  background-color: #1e293b;
  padding: 0.5rem 1rem;
  border-radius: 8px 0 0 8px;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  z-index: 100;
}

.menu-lateral a {
  color: #ffffff;
  text-decoration: none;
  font-weight: bold;
  font-size: 0.9rem;
}

.menu-lateral a:hover {
  color: #2AA68F;
}

/* Animación fade in */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in {
  animation: fadeIn 1s ease-out;
}
</style>
