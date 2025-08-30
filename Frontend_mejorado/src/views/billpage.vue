<template>
  <div class="billpage-container">
    <!-- Header unificado -->
    <NavBar title="OPCIONES DE FACTURACIÓN" />

    <!-- OPCIONES DE FACTURACIÓN -->
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

    <!-- LISTADO DE FACTURAS -->
    <section class="module">
      <h2 class="module-title">LISTADO DE FACTURAS</h2>
      <ul class="invoice-list">
        <li v-for="invoice in invoices" :key="invoice.id" class="invoice-card">
          <div class="invoice-info">
            <span class="invoice-description">
              Factura #{{ invoice.no_recibo }} — Cliente: {{ invoice.cliente_id }} — Total: Q{{ invoice.total }}
            </span>
            <button class="btn-download" @click="onDownloadPDF(invoice)">
              DESCARGAR PDF
            </button>
          </div>
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
      invoices: []
    }
  },
  mounted() {
    this.fetchInvoices()
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
        doc.text(`Recibo No: ${venta.no_recibo}`, 150, 20)
        doc.text(`Fecha: ${venta.fecha}`, 150, 26)

        // Cliente
        doc.setFontSize(12)
        if (venta.cliente) {
          doc.text(`Cliente: ${venta.cliente.nombre}`, 20, 40)
          doc.text(`NIT: ${venta.cliente.nit || 'C/F'}`, 20, 46)
          doc.text(`Dirección: ${venta.cliente.direccion || ''}`, 20, 52)
        }

        // Tabla de productos
        const rows = (venta.detalles || []).map(d => [
          d.producto?.nombre ?? '',
          d.cantidad,
          `Q${d.precio_unitario}`,
          `Q${d.subtotal}`,
        ])

        autoTable(doc, {
          head: [['Producto', 'Cantidad', 'Precio U.', 'Subtotal']],
          body: rows,
          startY: 65,
        })

        // Total
        const y = (doc.lastAutoTable?.finalY ?? 65) + 10
        doc.setFontSize(12)
        doc.text(`Total: Q${venta.total}`, 150, y)

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
  font-family: 'Segoe UI', sans-serif;
  color: var(--color-novenary);
}

/* === CUERPO === */
.actions-row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin: 20px;
}
.action-box {
  flex: 1 1 200px;
  background-color: var(--color-quaternary);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: background-color 0.3s;
}
.action-box:hover { background-color: var(--color-tertiary); }

/* === MODULO LISTADO === */
.module {
  background:#0d1130;
  border:2px solid #1e2236;
  border-radius:16px;
  padding:1.5rem;
  margin: 20px;
}
.module-title {
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #fff;
  text-transform: uppercase;
}

/* === FACTURAS === */
.invoice-list { list-style: none; padding: 0; margin: 0; }
.invoice-card {
  background-color: var(--color-quaternary);
  margin-bottom: 15px;
  border-radius: 8px;
  padding: 15px;
  transition: background-color 0.3s;
}
.invoice-card:hover { background-color: #8cafdc; }

.invoice-info { display: flex; justify-content: space-between; align-items: center; }
.invoice-description { font-weight: 500; color: var(--color-novenary); text-transform: uppercase; }

.btn-download {
  background-color: var(--color-secondary);
  color: #fff;
  padding: 10px 20px;
  border: none;
  font-family: 'Kollektif', sans-serif;
  cursor: pointer;
  border-radius: 6px;
  transition: background-color 0.3s;
  text-transform: uppercase;
}
.btn-download:hover { background-color: var(--color-tertiary); }
</style>
