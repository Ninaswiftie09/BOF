import { mount } from '@vue/test-utils'
import Login from '../login.vue'

// Busca en la pagina Login todos los elementos tipo "input" y que al menos hayan 2: usuario y contraseña mínimo
test('El componente Login se monta y muestra inputs', () => {
  const wrapper = mount(Login)
  const inputs = wrapper.findAll('input')
  expect(inputs.length).toBeGreaterThanOrEqual(2)
})