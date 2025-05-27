<script setup>
import { reactive, ref, computed, onMounted } from 'vue'

const search = ref('')
const modal = reactive({ visible: false, type: '' })
const clientes = ref([])

const clienteForm = reactive({
  empresa_id: null,
  nombre: '',
  contacto: '',
  nit: '',
  direccion: '',
  direccion_entrega: '',
  telefono: '',
  email: '',
  estado: true
})

const resetForm = () => {
  Object.keys(clienteForm).forEach(k => {
    clienteForm[k] = (typeof clienteForm[k] === 'boolean') ? true : ''
  })
  clienteForm.empresa_id = null
}

const open = t => { modal.type = t; modal.visible = true }
const close = () => { modal.visible = false }

const filteredClientes = computed(() =>
  clientes.value.filter(c =>
    [c.nombre, c.contacto, c.telefono].some(v =>
      v?.toLowerCase().includes(search.value.toLowerCase())
    )
  )
)

function saveCliente() {
  if (!clienteForm.nombre) {
    alert('El nombre es obligatorio.')
    return
  }

  fetch('https://abriluniformes.shop/api/clientes/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(clienteForm)
  })
    .then(res => {
      if (!res.ok) throw new Error('Error al guardar el cliente')
      return res.json()
    })
    .then(data => {
      clientes.value.push(data)
      resetForm()
      close()
    })
    .catch(err => {
      console.error('❌ Error:', err)
      alert('Hubo un error al guardar el cliente.')
    })
}

onMounted(() => {
  fetch('https://abriluniformes.shop/api/clientes/')
    .then(res => res.json())
    .then(data => {
      clientes.value = data
    })
    .catch(err => {
      console.error('❌ Error al cargar clientes:', err)
    })
})
</script>

<template>
  <div class="clientes">
    <input v-model="search" placeholder="Buscar clientes..." />

    <button @click="open('clientes')">Nuevo Cliente</button>

    <table>
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Contacto</th>
          <th>Teléfono</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(c, i) in filteredClientes" :key="i">
          <td>{{ c.nombre }}</td>
          <td>{{ c.contacto }}</td>
          <td>{{ c.telefono }}</td>
        </tr>
      </tbody>
    </table>

    <div v-if="modal.visible" class="modal">
      <form @submit.prevent="saveCliente">
        <h3>Nuevo Cliente</h3>
        <label>Nombre<input v-model="clienteForm.nombre" required /></label>
        <label>Contacto<input v-model="clienteForm.contacto" /></label>
        <label>NIT<input v-model="clienteForm.nit" /></label>
        <label>Dirección<input v-model="clienteForm.direccion" /></label>
        <label>Dirección Entrega<input v-model="clienteForm.direccion_entrega" /></label>
        <label>Teléfono<input v-model="clienteForm.telefono" /></label>
        <label>Email<input type="email" v-model="clienteForm.email" /></label>
        <button type="submit">Guardar</button>
        <button type="button" @click="close">Cancelar</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.clientes {
  padding: 2rem;
}
table {
  width: 100%;
  border-collapse: collapse;
}
td, th {
  padding: 0.5rem;
  border: 1px solid #ccc;
}
.modal {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal form {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  min-width: 300px;
}
</style>
