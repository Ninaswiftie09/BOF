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
    <h2 class="title">LISTADO DE FACTURAS</h2>
    <ul class="invoice-list">
      <li v-for="invoice in invoices" :key="invoice.id" class="invoice-card">
        <div class="invoice-info">
          <span class="invoice-description">{{ invoice.description }}</span>
          <button class="btn-download" @click="onDownloadPDF(invoice)">
            DESCARGAR PDF
          </button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'

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
      invoices: [
        { id: 1, description: 'Factura #001', pdfUrl: '/pdfs/factura001.pdf' },
        { id: 2, description: 'Factura #002', pdfUrl: '/pdfs/factura002.pdf' },
        { id: 3, description: 'Factura #003', pdfUrl: '/pdfs/factura003.pdf' }
      ]
    }
  },
  methods: {
    onDownloadPDF(invoice) {
      console.log('DESCARGAR PDF (PENDIENTE DE IMPLEMENTACIÓN EN EL BACKEND)', invoice)
    },
    uploadInvoice() {
      console.log('SUBIR FACTURA (PENDIENTE DE IMPLEMENTACIÓN)')
    },
    viewSavedInvoices() {
      console.log('VER FACTURAS GUARDADAS (PENDIENTE DE IMPLEMENTACIÓN)')
    }
  }
}
</script>

<style scoped>
.billpage-container {
  /* sin padding-top porque NavBar NO es fijo */
  min-height: 100vh;
  background: var(--color-octonary);
  padding: 20px;
}

/* === CUERPO DE LA VISTA === */
.actions-row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 20px;
}
.action-box {
  flex: 1 1 200px;
  background-color: var(--color-quaternary);
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: background-color 0.3s;
}
.action-box:hover { background-color: var(--color-tertiary); }

.title {
  font-size: 1.5rem;
  margin: 16px 0 12px;
  color: var(--color-novenary);
  text-transform: uppercase;
}

.invoice-list { list-style: none; padding: 0; margin: 0; }
.invoice-card {
  background-color: var(--color-quaternary);
  margin-bottom: 15px;
  border-radius: 5px;
  padding: 15px;
  transition: background-color 0.3s;
}
.invoice-card:hover { background-color: #8cafdc; }

.invoice-info { display: flex; justify-content: space-between; align-items: center; }
.invoice-description { font-weight: 500; color: var(--color-primary); text-transform: uppercase; }

.btn-download {
  background-color: var(--color-secondary);
  color: #fff;
  padding: 10px 20px;
  border: none;
  font-family: 'Kollektif', sans-serif;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s;
  text-transform: uppercase;
}
.btn-download:hover { background-color: var(--color-tertiary); }
</style>
