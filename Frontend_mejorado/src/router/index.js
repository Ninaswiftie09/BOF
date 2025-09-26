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

// ---------- Mini helper para /api/me/ ----------
let ME = null
async function fetchMe () {
  // Usa cookies de sesión del backend (SessionAuthentication)
  const res = await fetch('/api/me/', { credentials: 'include' })
  if (!res.ok) throw new Error('No authenticated')
  return res.json()
}

const routes = [
  // Redirige raíz a LandingPage
  { path: '/', redirect: '/LandingPage' },

  // 🔒 PRIVADAS (empleado y admin tienen acceso, salvo 3 rutas solo-admin)
  { path: '/home', name: 'home', component: Home, meta: { requiresAuth: true } },
  { path: '/mi_inventario', name: 'mi_inventario', component: MiInventario, meta: { requiresAuth: true } },
  { path: '/billpage', name: 'billpage', component: Billpage, meta: { requiresAuth: true } },
  { path: '/clientes', name: 'clientes', component: Clientes, meta: { requiresAuth: true } },
  { path: '/clientesregistro', name: 'clientesregistro', component: ClientesRegistro, meta: { requiresAuth: true } },
  { path: '/proveedores', name: 'proveedores', component: Proveedores, meta: { requiresAuth: true } },
  { path: '/envios', name: 'Envios', component: Envios, meta: { requiresAuth: true } },

  // 🔒 SOLO ADMIN
  { path: '/accounting', name: 'accounting', component: Accounting, meta: { requiresAuth: true, requiresRole: 'admin' } },
  { path: '/ReporteVentas', name: 'ReporteVentas', component: ReporteVentas, meta: { requiresAuth: true, requiresRole: 'admin' } },
  { path: '/register', name: 'register', component: Register, meta: { requiresAuth: true, requiresRole: 'admin' } },

  // 🟢 PÚBLICAS
  { path: '/LandingPage', name: 'inicio', component: LandingPage, meta: { requiresAuth: false } },
  { path: '/login', name: 'login', component: Login, meta: { requiresAuth: false } },
  { path: '/forgotpass', name: 'forgotpass', component: Forgotpass, meta: { requiresAuth: false } },


  // 🚫 FORBIDDEN (403)
  {
    path: '/forbidden',
    name: 'forbidden',
    meta: { requiresAuth: false },
    component: {
      template: `<div style="text-align:center; padding: 2rem;">
        <h1>403 - Acceso denegado</h1>
        <p>No tienes permisos para ver esta página.</p>
        <router-link to="/home">Ir al inicio</router-link>
      </div>`
    }
  },

  // 404
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

// Puente localStorage -> sessionStorage 
if (localStorage.getItem('isLoggedIn') === 'true' && !sessionStorage.getItem('isLoggedIn')) {
  sessionStorage.setItem('isLoggedIn', 'true')
  localStorage.removeItem('isLoggedIn')
}

// 🔐 Guard global
router.beforeEach(async (to, from, next) => {
  const logged = sessionStorage.getItem('isLoggedIn') === 'true'
  const requiresAuth = to.meta?.requiresAuth
  const requiresRole = to.meta?.requiresRole // 'admin' | 'empleado' | ['admin','empleado']


  console.debug('[guard]', {
  to: to.fullPath,
  name: to.name,
  requiresAuth: !!to.meta?.requiresAuth,
  requiresRole: to.meta?.requiresRole,
  logged
  })

  // 1) Necesita auth y no hay login -> /login
  if (requiresAuth && !logged) {
    return next({ path: '/login', query: { next: to.fullPath } })
  }

  // 2) Ya logueado y va a /login -> redirigir
  if (logged && to.name === 'login') {
    const nextRoute = to.query?.next || '/home'
    return next(nextRoute)
  }

  // 3) Si la ruta pide rol, validar contra /api/me/ (cache en ME)
  if (requiresRole) {
    try {
      if (!ME) ME = await fetchMe() // { role, ... }
      const role = ME?.role // "admin" | "empleado" | "ninguno"
      const ok = Array.isArray(requiresRole)
        ? requiresRole.includes(role)
        : role === requiresRole
      if (!ok) return next({ name: 'forbidden' })
    } catch {
      if (requiresAuth) return next({ path: '/login', query: { next: to.fullPath } })
    }
  }

  return next()
})

export default router
