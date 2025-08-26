// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// Vistas
import Home from '../views/home.vue'
import MiInventario from '../views/mi_inventario.vue'
import Accounting from '../views/accounting.vue'
import Billpage from '../views/billpage.vue'
import Forgotpass from '../views/forgotpass.vue'
import Login from '../views/login.vue'
import Register from '../views/register.vue'
import ReporteVentas from '../views/ReporteVentas.vue'
import Clientes from '../views/clientes.vue'
import ClientesRegistro from '../views/clientesregistro.vue'
import Proveedores from '../views/proveedores.vue'
import LandingPage from '@/views/LandingPage.vue'
import Envios from '../views/envios.vue' 

const routes = [
  // Redirige raíz a LandingPage (se bloqueará si no hay login)
  { path: '/', redirect: '/LandingPage' },

  // 🔒 PRIVADAS (todas menos /login)
  { path: '/home', name: 'home', component: Home, meta: { requiresAuth: true } },
  { path: '/mi_inventario', name: 'mi_inventario', component: MiInventario, meta: { requiresAuth: true } },
  { path: '/accounting', name: 'accounting', component: Accounting, meta: { requiresAuth: true } },
  { path: '/billpage', name: 'billpage', component: Billpage, meta: { requiresAuth: true } },
  { path: '/forgotpass', name: 'forgotpass', component: Forgotpass, meta: { requiresAuth: true } },
  { path: '/register', name: 'register', component: Register, meta: { requiresAuth: true } },
  { path: '/ReporteVentas', name: 'ReporteVentas', component: ReporteVentas, meta: { requiresAuth: true } },
  { path: '/clientes', name: 'clientes', component: Clientes, meta: { requiresAuth: true } },
  { path: '/clientesregistro', name: 'clientesregistro', component: ClientesRegistro, meta: { requiresAuth: true } },
  { path: '/proveedores', name: 'proveedores', component: Proveedores, meta: { requiresAuth: true } },
  { path: '/LandingPage', name: 'inicio', component: LandingPage, meta: { requiresAuth: false } },
  { path: '/envios', name: 'Envios', component: Envios, meta: { requiresAuth: true } },

  // 🟢 PÚBLICA: solo login
  { path: '/login', name: 'login', component: Login, meta: { requiresAuth: false } },

  // 404 (pública)
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    meta: { requiresAuth: false },
    component: {
      template: `<div style="text-align:center; padding: 2rem;">
        <h1>404 - Página no encontrada</h1>
        <p>La ruta ingresada no existe.</p>
        <router-link to="/login">Volver al login</router-link>
      </div>`
    }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

// 🔐 Guard global: bloquea todo si no hay "login" en localStorage
router.beforeEach((to, from, next) => {
  const logged = localStorage.getItem('isLoggedIn') === 'true'

  // si la ruta requiere auth y no estás loggeado -> a /login
  if (to.meta?.requiresAuth && !logged) {
    return next({ path: '/login', query: { next: to.fullPath } })
  }

  // si ya estás loggeado e intentas ir a /login -> manda a lo que pedía o /home
  if (logged && to.name === 'login') {
    const nextRoute = to.query?.next || '/home'
    return next(nextRoute)
  }

  next()
})

export default router
