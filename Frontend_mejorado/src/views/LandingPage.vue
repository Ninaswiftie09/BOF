<template>
  <div class="landing-container">
    <header class="landing-header">
      <img src="@/assets/logo_bof_blanco.png" alt="Logo de la empresa" class="landing-logo" />
      <h1 class="landing-title">Uniformes</h1>
      <p class="landing-subtitle">Que hablan bien de ti </p>
      <router-link to="/login" class="landing-login-btn">Acceder al sistema</router-link>
    </header>

    <section class="landing-section">
      <h2>Quiénes somos</h2>
      <p>
        Uniformes XYZ es una empresa dedicada a la confección de uniformes escolares, empresariales y deportivos.
        Con más de 20 años en el mercado, ofrecemos productos de alta calidad y diseños personalizados.
      </p>
    </section>

    <section class="landing-section">
      <h2>Misión</h2>
      <p>
        Brindar soluciones textiles que reflejen identidad, profesionalismo y compromiso, adaptadas a las necesidades
        de nuestros clientes.
      </p>
    </section>

    <section class="landing-section">
      <h2>Visión</h2>
      <p>
        Ser líderes nacionales en confección de uniformes, reconocidos por nuestra calidad, puntualidad y atención al cliente.
      </p>
    </section>

    <section class="landing-products">
      <h2>Algunos de nuestros productos</h2>
      <div class="product-gallery">
     <!--  <img src="@/assets/uniforme1.jpg" alt="Producto 1" />
        <img src="@/assets/uniforme2.jpg" alt="Producto 2" />
        <img src="@/assets/uniforme3.jpg" alt="Producto 3" /> -->
      </div>
    </section>

    <footer class="landing-footer">
      <p>&copy; 2025 Abril Uniformes y Bordados. Todos los derechos reservados.</p>
    </footer>
  </div>
</template>

<script setup>
// No necesitas lógica compleja aquí, solo navegación a login
</script>

<style scoped>
.landing-container {
  font-family: 'Kollektif', sans-serif;
  background-color: var(--color-octonary);
  color: var(--color-novenary);
  text-align: center;
  padding: 2rem;
}

.landing-header {
  background-color: var(--color-primary);
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
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

.landing-login-btn {
  display: inline-block;
  margin-top: 1.5rem;
  background-color: var(--color-secondary);
  color: white;
  padding: 10px 20px;
  border-radius: 6px;
  text-decoration: none;
  font-weight: bold;
}

.landing-login-btn:hover {
  background-color: var(--color-tertiary);
}

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
}

.landing-footer {
  margin-top: 3rem;
  font-size: 0.9rem;
  color: var(--color-septenary);
}
</style>
