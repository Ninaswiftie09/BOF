// cypress/e2e/clientes.cy.js
// Hecho a la medida de tu componente clientesregistro.vue
// - Selecciona inputs por el TEXTO DEL <label> (no hay placeholders)
// - Usa el modal visible (.modal-window:visible)
// - Espera las llamadas a la API reales de tu código (GET/POST/PUT/DELETE)
// - Incluye crear, editar, eliminar y búsqueda

const pageUrl = 'http://localhost:5173/clientesregistro';
const modal = () => cy.get('.modal-window:visible').first();
const rowByText = (t) => cy.contains('table tbody tr', t);

function net() {
  cy.intercept('GET', '/api/clientes/').as('getClientes');
  cy.intercept('POST', '/api/clientes/').as('postCliente');
  cy.intercept('PUT', /\/api\/clientes\/\d+\/$/).as('putCliente');
  cy.intercept('DELETE', /\/api\/clientes\/\d+\/$/).as('deleteCliente');
}

function openCreate() {
  cy.contains('button.add-button', 'Agregar Cliente').click({ force: true });
  modal().should('be.visible');
}

function typeIn(labelText, value) {
  modal().contains('label', labelText).find('input').clear().type(value, { force: true });
}

function save() {
  modal().contains('button', /^Guardar$/i).click({ force: true });
}

function createClient(suffix = 'QA') {
  const now = Date.now();
  const c = {
    nombre: `Cliente ${suffix} ${now}`,
    contacto: 'Contacto QA',
    nit: `CF-${now}`,
    direccion: 'Calle 1',
    entrega: 'Bodega 2',
    telefono: '5550000',
    email: `qa${now}@mail.com`,
  };

  openCreate();
  typeIn('Nombre', c.nombre);
  typeIn('Contacto', c.contacto);
  typeIn('NIT', c.nit);
  typeIn('Dirección', c.direccion);
  typeIn('Dirección Entrega', c.entrega);
  typeIn('Teléfono', c.telefono);
  typeIn('E-mail', c.email);
  save();

  cy.wait('@postCliente');
  cy.wait('@getClientes');
  rowByText(c.nombre).should('exist');

  return cy.wrap(c);
}

describe('Clientes (CRUD + búsqueda)', () => {
  beforeEach(() => {
    net();
    cy.visit(pageUrl);
    cy.wait('@getClientes');
  });

  it('Crear cliente', () => {
    createClient('Crear').then((c) => {
      rowByText(c.nombre).within(() => cy.contains(c.telefono).should('exist'));
    });
  });

  it('Editar cliente', () => {
    createClient('Editar').then((c) => {
      const nuevoNombre = `${c.nombre} Editado`;
      const nuevoTel = '5551111';

      rowByText(c.nombre).then(($row) => {
        cy.wrap($row).find('td').last().find('.edit-btn').click({ force: true });
      });

      modal().should('be.visible');
      typeIn('Nombre', nuevoNombre);
      typeIn('Teléfono', nuevoTel);
      save();

      cy.wait('@putCliente');
      cy.wait('@getClientes');

      rowByText(nuevoNombre).should('exist').within(() => {
        cy.contains(nuevoTel).should('exist');
      });
    });
  });

  it('Eliminar cliente', () => {
    createClient('Eliminar').then((c) => {
      cy.on('window:confirm', () => true);
      rowByText(c.nombre).then(($row) => {
        cy.wrap($row).find('td').last().find('.remove-btn').click({ force: true });
      });
      cy.wait('@deleteCliente');
      cy.wait('@getClientes');
      rowByText(c.nombre).should('not.exist');
    });
  });

  it('Buscar cliente (barra superior de la tabla)', () => {
    createClient('Buscar').then((c) => {
      const termino = c.nombre.split(' ')[1]; // "Buscar"
      cy.get('input.search-clientes').clear().type(termino, { force: true });
      cy.contains('table tbody tr', c.nombre).should('exist');
    });
  });
});
