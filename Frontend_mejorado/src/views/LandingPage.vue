<template>
  <div class="landing-container">
    <!-- HERO -->
    <header class="landing-header">
      <img src="@/assets/logo_bof_blanco.png" alt="Logo de la empresa" class="landing-logo" />
      <h1 class="landing-title">Uniformes</h1>
      <p class="landing-subtitle">Que hablan bien de ti</p>

      <!-- Botón de acceso como ícono SVG  -->
      <router-link to="/login" class="access-icon-btn" title="Acceder al sistema">
        <svg height="21" viewBox="0 0 21 21" width="21" xmlns="http://www.w3.org/2000/svg">
          <g fill="none" fill-rule="evenodd" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" transform="translate(3 3)">
            <path d="m6.5 10.5 3-3-3-3"/>
            <path d="m5 3v9" transform="matrix(0 1 -1 0 12.5 2.5)"/>
            <path d="m1.5 5.5v-3.0079176c0-1.10147263.89060277-1.99561512 1.99206673-1.99998427l7.95228497-.03160773c1.1045608-.00432011 2.0035361.8875515 2.0079175 1.99211231l.0398162 10.02918369c.0043323 1.1045608-.8875404 2.003535-1.9921012 2.0079309-.0026436 0-.0052873 0-.0079309 0h-7.9920533c-1.1045695 0-2-.8954305-2-2v-2.9897173"/>
          </g>
        </svg>
      </router-link>
    </header>

    <!-- QUIÉNES SOMOS -->
    <section class="landing-section">
      <h2>¿Quiénes somos?</h2>
      <p>
        En Abril Uniformes y Bordados nos especializamos en la confección de uniformes médicos, escolares e institucionales,
        así como en bordados personalizados de alta calidad. Combinamos diseño, funcionalidad y confort para ofrecer soluciones textiles únicas
        que reflejan la identidad y profesionalismo de nuestros clientes. Con un compromiso firme con la puntualidad, la cercanía y la excelencia,
        aspiramos a ser una empresa reconocida a nivel regional y nacional por la confiabilidad y estilo de nuestros productos.
      </p>
    </section>

    <!-- MISIÓN -->
    <section class="landing-section">
      <h2>Misión</h2>
      <p>
        Ofrecer bordados personalizados y confección de uniformes médicos e institucionales de alta calidad, combinando diseño,
        funcionalidad y confort. Nos comprometemos a brindar soluciones únicas que reflejen la identidad de nuestros clientes y fortalezcan su imagen,
        con un servicio cercano, profesional y puntual.
      </p>
    </section>

    <!-- VISIÓN -->
    <section class="landing-section">
      <h2>Visión</h2>
      <p>
        Ser una empresa reconocida en bordados profesionales y confección de uniformes en nuestra región y a nivel nacional,
        reconocida por la calidad, el diseño y la confiabilidad de nuestros productos. Aspiramos a vestir e inspirar a profesionales e instituciones
        con prendas que transmitan identidad, profesionalismo y estilo.
      </p>
    </section>

    <!-- PRODUCTOS -->
    <section class="landing-products">
      <h2>Algunos de nuestros productos</h2>
      <div class="product-gallery">
        <!-- ✅ imagenes de los productos falta agregarlos -->
        <!-- <img src="@/assets/uniforme1.jpg" alt="Producto 1" /> -->
        <!-- <img src="@/assets/uniforme2.jpg" alt="Producto 2" /> -->
        <!-- <img src="@/assets/uniforme3.jpg" alt="Producto 3" /> -->
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="landing-footer">
      <p>&copy; 2025 Abril Uniformes y Bordados. Todos los derechos reservados.</p>
    </footer>
  </div>
</template>

<style scoped>
.landing-container {
  font-family: 'Kollektif', sans-serif;
  background-color: var(--color-octonary);
  color: var(--color-novenary);
  text-align: center;
  padding: 2rem;
}

/* Encabezado con fondo primario */
.landing-header {
  background-color: var(--color-primary);
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  position: relative;
}

.landing-logo {
  width: 200px;
  margin-bottom: 1rem;
}

.landing-title {
  font-family: 'Archivo Black', sans-serif;
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: var(--color-novenary);
}

.landing-subtitle {
  font-size: 1.2rem;
  color: var(--color-septenary);
}

/* Botón de acceso ícono SVG */
.access-icon-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  color: var(--color-quinary);
  opacity: 0.6;
  transition: opacity 0.3s ease;
}

.access-icon-btn:hover {
  opacity: 1;
}

/* Secciones */
.landing-section {
  background-color: var(--color-senary);
  margin: 1.5rem auto;
  padding: 1.5rem;
  border-radius: 10px;
  max-width: 800px;
  text-align: left;
}

.landing-section h2 {
  color: var(--color-novenary);
  font-family: 'Archivo Black', sans-serif;
}

/* Galería de productos */
.landing-products {
  margin-top: 2rem;
}

.product-gallery {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
  margin-top: 1rem;
}

.product-gallery img {
  width: 200px;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(255, 255, 255, 0.1);
  transition: transform 0.3s ease;
}

.product-gallery img:hover {
  transform: scale(1.05);
}

/* Footer */
.landing-footer {
  margin-top: 3rem;
  font-size: 0.9rem;
  color: var(--color-septenary);
}
</style>
