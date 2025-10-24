import { createApp } from 'vue'
import { createPinia } from 'pinia'  
import App from './App.vue'
import router from './router'
import './assets/styles.css'

// Importa V-Calendar y sus estilos
import VCalendar from 'v-calendar'
import 'v-calendar/dist/style.css'

const app = createApp(App)
const pinia = createPinia()  

app.use(pinia)  // Activar Pinia


// Usa Vue Router
app.use(router)

// Registra el plugin de V-Calendar con el prefijo 'V'
app.use(VCalendar, {
  componentPrefix: 'V'
})


//deshabilitar devtools en desarrollo y produccion  
app.config.devtools = false 
app.config.performance = false 



// Monta la app
app.mount('#app')
