import { createRouter, createWebHistory } from 'vue-router'
import home from '../views/home.vue'
import mi_inventario from '../views/mi_inventario.vue'
import accounting from '../views/accounting.vue'
import billpage from '../views/billpage.vue'
import calculadora from '../views/calculadora.vue'
import forgotpass from '../views/forgotpass.vue'
import login from '../views/login.vue'
import register from '../views/register.vue'
import ReporteVentas from '../views/ReporteVentas.vue'


const routes = [
  { path: '/', name: 'home', component: home },
  { path: '/mi_inventario', name: 'mi_nventario', component: mi_inventario },
  { path: '/accounting', name: 'accounting', component: accounting },
  { path: '/billpage', name: 'billpage', component: billpage },
  { path: '/calculadora', name: 'calculadora', component: calculadora },
  { path: '/forgotpass', name: ',orgotpass', component: forgotpass },
  { path: '/login', name: 'login', component: login },
  { path: '/register', name: 'register', component: register },
  { path: '/ReporteVentas', name: 'ReporteVentas', component: ReporteVentas },

]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router


