<template>
  <div class="billpage-container page">
    <!-- Header sin buscador (lo ponemos en el módulo para que siempre se vea) -->
    <NavBar title="OPCIONES DE FACTURACIÓN" />

    <!-- Opciones -->
    <div class="actions-row">
      <div class="action-box" @click="uploadInvoice">
        <h3>SUBIR FACTURA</h3>
        <p>Selecciona o arrastra y suelta el PDF aquí</p>
      </div>
      <div class="action-box" @click="viewSavedInvoices">
        <h3>FACTURAS GUARDADAS</h3>
        <p>Revisa todas las facturas guardadas</p>
      </div>
    </div>

    <!-- Listado -->
    <section class="module">
      <div class="module-head">
        <h2 class="module-title">LISTADO DE FACTURAS</h2>
        <!-- 🔍 Buscador estilo “Tabla” -->
        <input
          v-model="search"
          class="input input--white"
          placeholder="Buscar facturas…"
        />
      </div>

      <ul class="invoice-list">
        <li
          v-for="invoice in filteredInvoices"
          :key="invoice.id"
          class="invoice-card"
        >
          <div class="invoice-info">
            <span class="invoice-description">
              Factura #{{ invoice.no_recibo || '—' }}
              — Cliente: {{ invoice.cliente_id ?? '—' }}
              — Total: Q{{ Number(invoice.total || 0).toLocaleString() }}
            </span>

            <button class="btn" @click="onDownloadPDF(invoice)">
              Descargar PDF
            </button>
          </div>
        </li>

        <li v-if="filteredInvoices.length === 0" class="invoice-empty">
          No hay facturas que coincidan con la búsqueda
        </li>
      </ul>
    </section>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { apiFetch } from '@/utils/api'
import NavBar from '@/components/NavBar.vue'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'

export default {
  name: 'BillPage',
  components: { NavBar },
  setup() {
    const router = useRouter()
    const goHome = () => router.push({ name: 'home' })
    return { goHome }
  },
  data() {
    return {
      invoices: [],
      search: '' // 🔍 buscador
    }
  },
  mounted() {
    this.fetchInvoices()
  },
  computed: {
    filteredInvoices() {
      const q = this.search.trim().toLowerCase()
      if (!q) return this.invoices
      return this.invoices.filter(inv =>
        [
          inv.no_recibo,
          inv.cliente_id,
          inv.total,
          inv.fecha
        ]
          .map(v => (v ?? '').toString().toLowerCase())
          .some(txt => txt.includes(q))
      )
    }
  },
  methods: {
    async fetchInvoices() {
      try {
        const data = await apiFetch('/api/ventas/detalles/')
        this.invoices = Array.isArray(data) ? data : []
      } catch (error) {
        console.error('Error cargando facturas:', error)
        this.invoices = []
      }
    },

    async onDownloadPDF(invoice) {
      try {
        const venta = await apiFetch(`/api/ventas/${invoice.id}/recibo/`)

        const doc = new jsPDF()

        // Encabezado
        doc.setFontSize(16)
        doc.text('Abril Uniformes y Bordados', 20, 20)
        doc.setFontSize(10)
        doc.text('Ciudad, Huehuetenango 13001', 20, 26)

        doc.setFontSize(11)
        doc.text(`Recibo No: ${venta.no_recibo}`, 150, 20, { align: 'right' })
        doc.text(`Fecha: ${venta.fecha}`, 150, 26, { align: 'right' })

        // Cliente
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

        // Tabla
        const rows = (venta.detalles || []).map(d => [
          d.producto?.nombre ?? '',
          d.cantidad,
          `Q${d.precio_unitario}`,
          `Q${d.subtotal}`
        ])
        autoTable(doc, {
          head: [['Producto', 'Cantidad', 'Precio U.', 'Subtotal']],
          body: rows,
          startY: 65
        })

        // Total
        const y = (doc.lastAutoTable?.finalY ?? 65) + 10
        doc.setFontSize(12)
        doc.text(`Total: Q${venta.total}`, 150, y, { align: 'right' })

        doc.save(`recibo_${venta.no_recibo}.pdf`)
      } catch (error) {
        console.error('Error generando recibo:', error)
        alert('No se pudo generar el recibo')
      }
    },

    uploadInvoice() {
      console.log('SUBIR FACTURA (pendiente de implementar)')
    },
    viewSavedInvoices() {
      console.log('VER FACTURAS GUARDADAS (pendiente de implementar)')
    }
  }
}
</script>

<style scoped>
.billpage-container {
  min-height: 100vh;
  background: var(--color-octonary);
  display: flex;
  flex-direction: column;
  color: var(--color-novenary);
}

/* Opciones superiores */
.actions-row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin: 20px;
}
.action-box {
  flex: 1 1 240px;
  background: var(--color-quaternary);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: background-color .2s ease;
}
.action-box:hover { background: var(--color-tertiary); }

/* Cabecera del módulo con buscador a la derecha */
.module { margin: 20px; }
.module-head{
  display:flex; align-items:center; justify-content:space-between; gap:12px;
  margin-bottom: 12px;
}
.module-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #fff;
  text-transform: uppercase;
  margin: 0;
  line-height: 1;
}
.module-head .input { max-width: 320px; }

/* Listado */
.invoice-list { list-style: none; margin: 0; padding: 0; }
.invoice-card {
  background: var(--color-quaternary);
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 12px;
}
.invoice-info {
  display: flex;
  gap: 12px;
  justify-content: space-between;
  align-items: center;
}
.invoice-description { font-weight: 600; text-transform: uppercase; }

.invoice-empty {
  padding: 14px;
  text-align: center;
  color: var(--color-septenary);
  background: #0b1326;
  border-radius: 8px;
}
</style>
