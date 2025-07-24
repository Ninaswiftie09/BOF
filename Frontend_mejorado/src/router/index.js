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


const routes = [
  { path: '/', redirect: '/login' },
  { path: '/home', name: 'home', component: Home },
  { path: '/mi_inventario', name: 'mi_inventario', component: MiInventario },
  { path: '/accounting', name: 'accounting', component: Accounting },
  { path: '/billpage', name: 'billpage', component: Billpage },
  { path: '/forgotpass', name: 'forgotpass', component: Forgotpass },
  { path: '/login', name: 'login', component: Login },
  { path: '/register', name: 'register', component: Register },
  { path: '/ReporteVentas', name: 'ReporteVentas', component: ReporteVentas },
  { path: '/clientes', name: 'clientes', component: Clientes },
  { path: '/clientesregistro', name: 'clientesregistro', component: ClientesRegistro },
  { path: '/proveedores', name: 'proveedores', component: Proveedores },
  { path: '/LandingPage', name: 'inicio', component: LandingPage },


  // Manejo de rutas inexistentes (404)
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
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
  routes
})

export default router
