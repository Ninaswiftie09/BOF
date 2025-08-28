// cypress/e2e/inventario_telas.cy.js
// Hecho a la medida de tu inventario.vue (solo Telas).
// Llena SIEMPRE el formulario y espera las llamadas a la API reales.

const pageUrl = 'http://localhost:5173/mi_inventario';

// -------- helpers ----------
const formModal = () => cy.get('.modal-content:visible').first();
const fullListModal = () => cy.get('.full-table-modal:visible').first();

function net() {
  cy.intercept('GET', '**/api/telas/').as('getTelas');
  cy.intercept('POST', '**/api/inventario/agregar-nueva-tela/').as('postTela');
  cy.intercept('PUT', '**/api/inventario/editar-tela/*/').as('putTela');
  cy.intercept('DELETE', '**/api/inventario/eliminar-tela/*/').as('deleteTela');
}

function openAdd() {
  cy.contains('div.inventory-section h2', /^Telas$/i)
    .parents('.inventory-section')
    .within(() => cy.contains('button', /^Agregar producto$/i).click({ force: true }));
  formModal().should('be.visible').contains('h3', /Agregar nuevo Telas/i);
}

function openEdit() {
  cy.contains('div.inventory-section h2', /^Telas$/i)
    .parents('.inventory-section')
    .within(() => cy.contains('button', /^Editar Producto$/i).click({ force: true }));
  formModal().should('be.visible').contains('h3', /Editar Telas/i);
}

function openDelete() {
  cy.contains('div.inventory-section h2', /^Telas$/i)
    .parents('.inventory-section')
    .within(() => cy.contains('button', /^Eliminar Producto$/i).click({ force: true }));
  formModal().should('be.visible').contains('h3', /Eliminar Telas/i);
}

function openViewAll() {
  cy.contains('div.inventory-section h2', /^Telas$/i)
    .parents('.inventory-section')
    .within(() => cy.contains('button', /^Ver Todos$/i).click({ force: true }));
  fullListModal().should('be.visible').contains('h3', /Telas - Lista Completa/i);
}

function typeByLabel(labelText, value) {
  formModal().contains('label', labelText).next('input, textarea').clear().type(String(value), { force: true });
}

function clickPrimary(actionRegex = /^Guardar|Actualizar|Eliminar$/i) {
  formModal().contains('button.btn-primary', actionRegex).click({ force: true });
}

function idFromFirstCellOfRowWithName(nombre) {
  return cy.contains('table tbody tr', nombre)
    .find('td')
    .first()
    .invoke('text')
    .then((t) => t.trim());
}

function crearTelaBase() {
  const now = Date.now();
  const t = {
    nombre: `Tela Cypress ${now}`,
    tipo: 'Algodón',
    composicion: '100% Algodón',
    color: 'Azul',
    codigo: `TCY-${now}`,
    stock: 12,
    descripcion: 'Creada por Cypress',
  };

  openAdd();
  typeByLabel('Nombre', t.nombre);
  typeByLabel('Tipo', t.tipo);
  typeByLabel('Composición', t.composicion);
  typeByLabel('Color', t.color);
  typeByLabel('Código', t.codigo);
  typeByLabel('Stock', t.stock);
  typeByLabel('Descripción', t.descripcion);
  clickPrimary(/^Guardar$/i);

  cy.wait('@postTela');
  cy.wait('@getTelas'); // la vista vuelve a pedir telas tras cerrar
  openViewAll();
  cy.contains('table tbody tr', t.nombre).should('exist');

  return cy.wrap(t);
}
// ---------------------------

describe('Inventario > Telas (CRUD + ver columnas)', () => {
  beforeEach(() => {
    net();
    cy.visit(pageUrl);
    // la vista hace GET telas/hilos/uniformes al montar; aseguremos Telas cargado
    cy.wait('@getTelas');
  });

  it('Crear tela (llena y guarda)', () => {
    crearTelaBase().then((t) => {
      cy.contains('table tbody tr', t.nombre)
        .should('exist')
        .within(() => {
          cy.contains(t.color).should('exist');
          cy.contains(String(t.stock)).should('exist');
        });
    });
  });

  it('Editar tela (ingresando ID, llena y guarda)', () => {
    crearTelaBase().then((t) => {
      // obtenemos el ID desde la tabla de "Ver Todos"
      idFromFirstCellOfRowWithName(t.nombre).then((id) => {
        // abrir modal de edición y llenar
        cy.get('button.btn-cancel').contains(/Cerrar/i).click({ force: true }); // cerrar "Ver Todos"
        openEdit();
        // campo "ID del producto:"
        formModal().contains('label', 'ID del producto').next('input').clear().type(id, { force: true });

        const edit = { ...t, nombre: `${t.nombre} Editada`, color: 'Verde', stock: 20 };
        typeByLabel('Nombre', edit.nombre);
        typeByLabel('Color', edit.color);
        typeByLabel('Stock', edit.stock);
        clickPrimary(/^Actualizar$/i);

        cy.wait('@putTela');
        cy.wait('@getTelas');

        openViewAll();
        cy.contains('table tbody tr', edit.nombre)
          .should('exist')
          .within(() => {
            cy.contains(/Verde/i).should('exist');
            cy.contains(/\b20\b/).should('exist');
          });
      });
    });
  });

  it('Eliminar tela (ingresando ID y confirmando)', () => {
    crearTelaBase().then((t) => {
      idFromFirstCellOfRowWithName(t.nombre).then((id) => {
        cy.get('button.btn-cancel').contains(/Cerrar/i).click({ force: true }); // cerrar "Ver Todos"
        cy.on('window:alert', () => {}); // tu vista usa alert() al terminar
        openDelete();
        formModal().contains('label', 'ID del producto').next('input').clear().type(id, { force: true });
        clickPrimary(/^Eliminar$/i);

        cy.wait('@deleteTela');
        cy.wait('@getTelas');

        openViewAll();
        cy.contains('table tbody tr', t.nombre).should('not.exist');
      });
    });
  });

  it('Ver Todos muestra columnas correctas', () => {
    openViewAll();
    fullListModal().find('thead').within(() => {
      cy.contains(/^id$/i).should('exist');
      cy.contains(/^Nombre$/i).should('exist');
      cy.contains(/^Tipo$/i).should('exist');
      cy.contains(/^Composición$/i).should('exist');
      cy.contains(/^Color$/i).should('exist');
      cy.contains(/^Código$/i).should('exist');
      cy.contains(/^Stock$/i).should('exist');
      cy.contains(/^Descripción$/i).should('exist');
    });
  });
});
