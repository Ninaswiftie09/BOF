import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/styles.css'

// 1) importa V-Calendar y sus estilos
import VCalendar from 'v-calendar'
import 'v-calendar/dist/style.css'

const app = createApp(App)

// 2) usa Vue Router
app.use(router)

// 3) registra el plugin de V-Calendar
app.use(VCalendar, {
  componentPrefix: 'V'  
})

app.mount('#app')
