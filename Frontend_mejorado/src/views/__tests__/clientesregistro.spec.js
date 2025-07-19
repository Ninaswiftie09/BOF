import { mount } from '@vue/test-utils'
import ClientesRegistro from '../clientesregistro.vue'

test('El componente ClientesRegistro se monta correctamente', () => {
  const wrapper = mount(ClientesRegistro)
  expect(wrapper.exists()).toBe(true)
})

test('Renderiza la tabla de clientes si hay datos', async () => {
  const wrapper = mount(ClientesRegistro)
  await new Promise(resolve => setTimeout(resolve, 1000)) // espera el fetch real
  const filas = wrapper.findAll('tbody tr')
  expect(filas.length).toBeGreaterThan(0)
})

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