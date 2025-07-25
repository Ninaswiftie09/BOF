// función que monta componentes Vue para los test
import { mount } from '@vue/test-utils'
// importa el componente a probar: la página clientesregistro
import ClientesRegistro from '../clientesregistro.vue'


// La constante Wrapper indica si el componente (la página) carga correctamente y sin problemas
test('El componente ClientesRegistro se monta correctamente', () => {
  const wrapper = mount(ClientesRegistro)
  expect(wrapper.exists()).toBe(true)
})

// Simula una carga real de clientes desde la API que usamos y verifica que las tablas lo muestren
test('Renderiza la tabla de clientes si hay datos', async () => {
  const wrapper = mount(ClientesRegistro)
  await new Promise(resolve => setTimeout(resolve, 1000)) // espera el fetch real
  const filas = wrapper.findAll('tbody tr')
  expect(filas.length).toBeGreaterThan(0)
})

// Prueba el hacer clic en el botón clientes, y verifica que el formulario de registro abra correctamente
test('Abre el formulario de cliente al hacer clic en "Clientes"', async () => {
  const wrapper = mount(ClientesRegistro)

  // Esperamos que cargue la vista
  await new Promise(resolve => setTimeout(resolve, 500))

  // Buscar el botón "Clientes" dentro del texto ACTUALIZACIÓN
  const botonClientes = wrapper.find('section.big-card ul li')
  await botonClientes.trigger('click')

  // Verificamos que se abre la ventana del modal
  expect(wrapper.find('.modal-window').exists()).toBe(true)
  expect(wrapper.find('form.modal-form').exists()).toBe(true)
})