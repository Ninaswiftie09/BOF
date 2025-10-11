import { defineStore } from 'pinia'
import { computed } from 'vue'
import { useAuthStore } from './auth'

export const usePermissionsStore = defineStore('permissions', () => {
  const authStore = useAuthStore()

  // Definición de permisos por módulo y rol
  const permissions = {
    inventario: {
      admin: ['ver', 'crear', 'editar', 'eliminar'],
      empleado: ['ver', 'crear']
    },
    clientes: {
      admin: ['ver', 'crear', 'editar', 'eliminar'],
      empleado: ['ver', 'crear', 'editar']
    },
    proveedores: {
      admin: ['ver', 'crear', 'editar', 'eliminar'],
      empleado: ['ver', 'crear', 'editar']
    },
    ventas: {
      admin: ['ver', 'crear', 'editar', 'eliminar', 'reportes'],
      empleado: ['ver', 'crear', 'reportes']
    },
    facturas: {
      admin: ['ver', 'subir', 'eliminar'],
      empleado: ['ver']
    },
    metricas: {
      admin: ['ver'],
      empleado: ['ver']
    }
  }

  // Getter: Verificar si tiene un permiso específico
  const can = computed(() => {
    return (modulo, accion) => {
      const userRole = authStore.role
      
      if (!userRole || !permissions[modulo]) {
        return false
      }

      const rolePermissions = permissions[modulo][userRole] || []
      return rolePermissions.includes(accion)
    }
  })

  // Getters específicos para cada módulo
  const canEditInventario = computed(() => can.value('inventario', 'editar'))
  const canDeleteInventario = computed(() => can.value('inventario', 'eliminar'))
  
  const canEditClientes = computed(() => can.value('clientes', 'editar'))
  const canDeleteClientes = computed(() => can.value('clientes', 'eliminar'))
  
  const canEditProveedores = computed(() => can.value('proveedores', 'editar'))
  const canDeleteProveedores = computed(() => can.value('proveedores', 'eliminar'))
  
  const canEditVentas = computed(() => can.value('ventas', 'editar'))
  const canDeleteVentas = computed(() => can.value('ventas', 'eliminar'))
  const canViewReportes = computed(() => can.value('ventas', 'reportes'))
  
  const canUploadFacturas = computed(() => can.value('facturas', 'subir'))
  const canDeleteFacturas = computed(() => can.value('facturas', 'eliminar'))

  return {
    // Getters
    can,
    canEditInventario,
    canDeleteInventario,
    canEditClientes,
    canDeleteClientes,
    canEditProveedores,
    canDeleteProveedores,
    canEditVentas,
    canDeleteVentas,
    canViewReportes,
    canUploadFacturas,
    canDeleteFacturas
  }
})