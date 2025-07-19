import { mount } from '@vue/test-utils'
import Login from '../login.vue'

test('El componente Login se monta y muestra inputs', () => {
  const wrapper = mount(Login)
  const inputs = wrapper.findAll('input')
  expect(inputs.length).toBeGreaterThanOrEqual(2) // usuario y contraseña mínimo
})