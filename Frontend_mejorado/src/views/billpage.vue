<template>
  <div class="page-container">
    <NavBar title="OPCIONES DE FACTURACIÓN" />

    <div class="page-content">
      <section class="module">
        <div class="module-header">
          <h2 class="module-title">LISTADO DE FACTURAS</h2>
          <input
            v-model="search"
            class="input-dark"
            placeholder="Buscar facturas…"
            style="max-width: 320px;"
          />
        </div>

        <ul class="invoice-list">
          <li
            v-for="invoice in filteredInvoices"
            :key="invoice.id"
            class="list-item-card"
          >
            <span class="list-item-card-description">
              Factura #{{ invoice.no_recibo || '—' }}
              — Cliente: {{ invoice.cliente_nombre || 'N/A' }}
              — Total: Q{{ Number(invoice.total || 0).toLocaleString() }}
            </span>

            <button class="btn btn-secondary" @click="onDownloadPDF(invoice)">
              Descargar PDF
            </button>
          </li>

          <li v-if="filteredInvoices.length === 0" class="muted-text" style="text-align: center; padding: 1.5rem;">
            No hay facturas que coincidan con la búsqueda
          </li>
        </ul>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { apiFetch } from '@/utils/api'
import NavBar from '@/components/NavBar.vue'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'

const router = useRouter()
const invoices = ref([])
const search = ref('')

const filteredInvoices = computed(() => {
  const q = search.value.trim().toLowerCase()
  if (!q) return invoices.value

  return invoices.value.filter(inv =>
    [inv.no_recibo, inv.cliente_nombre, inv.cliente_nit, inv.total, inv.fecha]
      .map(v => (v ?? '').toString().toLowerCase())
      .some(txt => txt.includes(q))
  )
})

async function fetchInvoices() {
  try {
    const data = await apiFetch('/api/ventas/detalles/')
    invoices.value = Array.isArray(data) ? data : []
  } catch (error) {
    console.error('Error cargando facturas:', error)
    invoices.value = []
  }
}

async function onDownloadPDF(invoice) {
  try {
    const venta = await apiFetch(`/api/ventas/${invoice.id}/recibo/`)
    const doc = new jsPDF()

    // Lógica de generación de PDF
    doc.setFontSize(16)
    doc.text('Abril Uniformes y Bordados', 20, 20)
    doc.setFontSize(10)
    doc.text('Ciudad, Huehuetenango 13001', 20, 26)
    doc.setFontSize(11)
    doc.text(`Recibo No: ${venta.no_recibo}`, 150, 20, { align: 'right' })
    doc.text(`Fecha: ${venta.fecha}`, 150, 26, { align: 'right' })
    doc.setFontSize(12)
    const cliente = venta.cliente || {}
    const clienteNombre = cliente.nombre || 'Cliente no registrado'
    const clienteNit = cliente.nit || 'C/F'
    const clienteDireccion = cliente.direccion || cliente.direccion_entrega || 'Sin dirección'
    const clienteTelefono = cliente.telefono || 'Sin teléfono'
    const clienteCorreo = cliente.email || 'Sin correo'
    doc.text(`Cliente: ${clienteNombre}`, 20, 40)
    doc.text(`NIT: ${clienteNit}`, 20, 46)
    doc.text(`Dirección: ${clienteDireccion}`, 20, 52)
    doc.text(`Teléfono: ${clienteTelefono}`, 20, 58)
    doc.text(`Correo: ${clienteCorreo}`, 20, 64)
    doc.text(`Método de pago: ${venta.metodo_pago || 'No especificado'}`, 20, 74)
    doc.text(`Estado: ${venta.estado || 'No especificado'}`, 20, 80)
    const rows = (venta.detalles || []).map(d => [d.producto?.nombre ?? '', d.cantidad, `Q${d.precio_unitario}`, `Q${d.subtotal}`])
    autoTable(doc, {
      head: [['Producto', 'Cantidad', 'Precio U.', 'Subtotal']],
      body: rows,
      startY: 90
    })
    const y = (doc.lastAutoTable?.finalY ?? 90) + 10
    doc.setFontSize(12)
    doc.text(`Total: Q${venta.total}`, 150, y, { align: 'right' })
    doc.save(`recibo_${venta.no_recibo}.pdf`)

  } catch (error) {
    console.error('Error generando recibo:', error)
    alert('No se pudo generar el recibo')
  }
}

onMounted(fetchInvoices)
</script>

<style scoped>
.page-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.module-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.module-title {
  font-family: 'Archivo Black', sans-serif;
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--color-text-light-primary);
  text-transform: uppercase;
  margin: 0;
  line-height: 1;
}

.invoice-list {
  list-style: none;
  margin: 0;
  padding: 0;
}
</style>