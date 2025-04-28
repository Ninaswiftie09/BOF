-- Tabla de Empresas
CREATE TABLE empresas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    nit VARCHAR(50) UNIQUE
);

-- Tabla de Clientes
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    codigo_cliente VARCHAR(50) UNIQUE NOT NULL,
    empresa_id INTEGER REFERENCES empresas(id) ON DELETE SET NULL,
    estado BOOLEAN NOT NULL DEFAULT TRUE, -- TRUE = Activo, FALSE = Inactivo
    nombre VARCHAR(255) NOT NULL,
    contacto VARCHAR(255),
    nit VARCHAR(50) UNIQUE,
    direccion TEXT,
    direccion_entrega TEXT,
    telefono VARCHAR(50),
    email VARCHAR(255),
    cartera DECIMAL(12,2) DEFAULT 0.0
);

CREATE INDEX idx_clientes_nombre ON clientes(nombre);
CREATE INDEX idx_clientes_telefono ON clientes(telefono);
CREATE INDEX idx_clientes_nit ON clientes(nit);