// cypress/e2e/proveedores.cy.js
// Hecho a la medida de tu componente de Proveedores.
// Llena SIEMPRE el formulario dentro del modal y espera las llamadas reales:
//  - GET  /api/proveedores/
//  - POST /api/proveedores/
//  - PUT  /api/proveedores/:id/
//  - DELETE /api/proveedores/:id/
// Incluye: crear, editar, eliminar y búsqueda.

const pageUrl = 'http://localhost:5173/proveedores';

const modal = () => cy.get('.modal-window:visible').first();
const rowByText = (t) => cy.contains('table tbody tr', t);

function net() {
  cy.intercept('GET', '/api/proveedores/**').as('getProv');
  cy.intercept('POST', '/api/proveedores/').as('postProv');
  cy.intercept('PUT', /\/api\/proveedores\/\d+\/$/).as('putProv');
  cy.intercept('DELETE', /\/api\/proveedores\/\d+\/$/).as('delProv');
}

function openCreate() {
  cy.contains('button.add-button', /^Agregar Proveedores$/i).click({ force: true });
  // Si el botón tuviera un tipo equivocado, el modal no se abriría; afirmamos visibilidad.
  modal().should('be.visible').contains('h3', /Nuevo Proveedor|Editar Proveedor/i);
  // Si abre en modo "editar" por defecto, limpiamos campos para crear.
  modal().within(() => {
    cy.contains('label', 'Nombre').find('input').clear();
    cy.contains('label', 'Correo').find('input').clear();
    cy.contains('label', 'Teléfono').find('input').clear();
    cy.contains('label', 'Dirección').find('input').clear();
  });
}

function typeIn(label, value) {
  modal().contains('label', label).find('input').clear().type(value, { force: true });
}

function save() {
  modal().contains('button.save-big', /^Guardar$/i).click({ force: true });
}

function createProveedorBase(sufijo = 'QA') {
  const now = Date.now();
  const p = {
    nombre: `Proveedor ${sufijo} ${now}`,
    correo: `prov${now}@mail.com`,
    telefono: `55${String(now).slice(-6)}`,
    direccion: 'Zona 1',
  };

  openCreate();
  typeIn('Nombre', p.nombre);
  typeIn('Correo', p.correo);
  typeIn('Teléfono', p.telefono);
  typeIn('Dirección', p.direccion);
  save();

  cy.wait('@postProv');
  cy.wait('@getProv');
  rowByText(p.nombre).should('exist');

  return cy.wrap(p);
}

describe('Proveedores (CRUD + búsqueda llenando formularios)', () => {
  beforeEach(() => {
    net();
    cy.visit(pageUrl);
    cy.wait('@getProv');
  });

  it('Crear proveedor', () => {
    createProveedorBase('Crear').then((p) => {
      rowByText(p.nombre)
        .should('exist')
        .within(() => {
          cy.contains(p.correo).should('exist');
          cy.contains(p.telefono).should('exist');
        });
    });
  });

  it('Editar proveedor', () => {
    createProveedorBase('Editar').then((p) => {
      const edit = { ...p, nombre: `${p.nombre} Editado`, telefono: '5551111' };

      // Abrir modal en modo edición desde su fila
      rowByText(p.nombre).then(($row) => {
        cy.wrap($row).find('.edit-btn').click({ force: true });
      });

      modal().should('be.visible').contains('h3', /Editar Proveedor/i);
      typeIn('Nombre', edit.nombre);
      typeIn('Teléfono', edit.telefono);
      save();

      cy.wait('@putProv');
      cy.wait('@getProv');

      rowByText(edit.nombre).should('exist').within(() => {
        cy.contains('5551111').should('exist');
      });
    });
  });

  it('Eliminar proveedor', () => {
    createProveedorBase('Eliminar').then((p) => {
      cy.on('window:confirm', () => true);
      rowByText(p.nombre).then(($row) => {
        cy.wrap($row).find('.remove-btn').click({ force: true });
      });
      cy.wait('@delProv');
      cy.wait('@getProv');
      rowByText(p.nombre).should('not.exist');
    });
  });

  it('Buscar proveedor', () => {
    createProveedorBase('Buscar').then((p) => {
      // La barra usa v-model="searchQuery" con placeholder "Buscar proveedores…"
      const termino = p.nombre.split(' ')[1]; // "Buscar"
      cy.get('input.search').clear().type(termino, { force: true });
      // El filtrado es local (computed filteredProveedores). No hay espera de red.
      rowByText(p.nombre).should('exist');
    });
  });
});
