<template>
  <div class="landing-container">
    <!-- Menú flotante -->
    <nav class="menu-lateral">
      <a href="#mision">Misión</a>
      <a href="#productos">Productos</a>
      <a href="#contacto">Contacto</a>
    </nav>

    <!-- Título principal -->
    <header class="titulo-principal">
      <h1>Abril Uniformes</h1>
      <p>Soluciones textiles personalizadas para tu empresa</p>
    </header>

    <!-- Misión y Visión -->
    <section id="mision" class="landing-section">
      <h2>Misión</h2>
      <p>
        Nuestra misión es brindar soluciones textiles personalizadas y de calidad para empresas,
        instituciones y emprendedores, destacando por nuestro compromiso con la innovación,
        el servicio y la satisfacción del cliente.
      </p>
      <h2>Visión</h2>
      <p>
        Ser reconocidos como líderes en el sector de la confección y productos promocionales,
        expandiendo nuestra presencia a nivel nacional y consolidando relaciones duraderas
        con nuestros clientes.
      </p>
    </section>

    <!-- Productos que ofrecemos -->
    <section id="productos" class="landing-section productos">
      <h2>Productos que ofrecemos</h2>
      <div class="productos-grid">
        <div v-for="producto in productos" :key="producto.nombre" class="producto-card">
          <img :src="producto.imagen" :alt="producto.nombre" />
          <p>{{ producto.nombre }}</p>
        </div>
      </div>
    </section>

    <!-- Contacto redes -->
    <section id="contacto" class="landing-section">
      <h2>Contáctanos</h2>
      <div class="redes redes-iconos">
        <a href="https://facebook.com" target="_blank" aria-label="Facebook">
          <IconFc />
        </a>
        <a href="https://instagram.com" target="_blank" aria-label="Instagram">
          <IconIg />
        </a>
        <a href="https://wa.me/1234567890" target="_blank" aria-label="WhatsApp">
          <IconWs />
        </a>
      </div>
    </section>

    <!-- Botón para ir al login -->
    <div class="ingreso-login">
      <router-link to="/login" class="btn-login">Ingresar al sistema</router-link>
    </div>
  </div>
</template>

<script setup>
// Íconos personalizados
import IconFc from '@/components/icons/fc.vue'
import IconIg from '@/components/icons/ig.vue'
import IconWs from '@/components/icons/ws.vue'

// Lista de productos con rutas relativas a /assets/images
const productos = [
  { nombre: 'Gorras Personalizadas', imagen: new URL('@/assets/images/gorra.jpg', import.meta.url).href },
  { nombre: 'Borradores con logo', imagen: new URL('@/assets/images/borrador.jpg', import.meta.url).href },
  { nombre: 'Uniformes Médicos', imagen: new URL('@/assets/images/uniforme.jpg', import.meta.url).href },
  { nombre: 'Delantales', imagen: new URL('@/assets/images/delantal.jpg', import.meta.url).href },
  { nombre: 'Camisetas estampadas', imagen: new URL('@/assets/images/camiseta.jpg', import.meta.url).href },
  { nombre: 'Bolsas ecológicas', imagen: new URL('@/assets/images/bolsa.jpg', import.meta.url).href },
  { nombre: 'Tazas personalizadas', imagen: new URL('@/assets/images/taza.jpg', import.meta.url).href },
  { nombre: 'Lanyards', imagen: new URL('@/assets/images/lanyard.jpg', import.meta.url).href },
]
</script>

<style scoped>
html {
  scroll-behavior: smooth;
}

.landing-container {
  font-family: 'Segoe UI', sans-serif;
  padding-bottom: 4rem;
  background: #f8fafc;
  color: #1e293b;
}

/* Título principal */
.titulo-principal {
  text-align: center;
  padding: 2rem 1rem 1rem;
  background-color: #e2e8f0;
  border-bottom: 2px solid #cbd5e1;
}

.titulo-principal h1 {
  font-size: 2.5rem;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.titulo-principal p {
  font-size: 1.2rem;
  color: #475569;
}

/* Secciones */
.landing-section {
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
}

.landing-section:nth-child(even) {
  background: linear-gradient(to right, #f1f5f9, #e2e8f0);
}

h2 {
  font-size: 1.8rem;
  color: #0f172a;
  margin-bottom: 0.5rem;
}

p {
  font-size: 1.1rem;
  line-height: 1.6;
}

/* Productos */
.productos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.producto-card {
  background: white;
  padding: 1rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.producto-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.producto-card img {
  width: 100%;
  height: 140px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 0.5rem;
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
  background: #1e293b;
  padding: 0.5rem;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  transition: background 0.3s ease;
}

.redes-iconos a:hover {
  background: #2563eb;
}

.redes-iconos svg {
  fill: white;
  width: 24px;
  height: 24px;
}

/* Botón login */
.ingreso-login {
  text-align: center;
  margin-top: 2rem;
}

.btn-login {
  background: #1e293b;
  color: white;
  padding: 0.75rem 2rem;
  border-radius: 8px;
  font-weight: bold;
  text-decoration: none;
}

/* Menú lateral fijo */
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
</style>
