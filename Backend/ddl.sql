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

-- Tabla de Pedidos (Ventas)
CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER REFERENCES clientes(id) ON DELETE CASCADE,
    fecha TIMESTAMP NOT NULL DEFAULT NOW(),
    precio_total DECIMAL(12,2) NOT NULL
);

-- Detalle de Pedidos
CREATE TABLE pedido_detalle (
    id SERIAL PRIMARY KEY,
    pedido_id INTEGER REFERENCES pedidos(id) ON DELETE CASCADE,
    descripcion_producto TEXT,
    cantidad INTEGER,
    precio_unitario DECIMAL(12,2)
);

-- Tabla de Cuentas a Pagar
CREATE TABLE cuentas_pagar (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER REFERENCES clientes(id) ON DELETE CASCADE,
    monto DECIMAL(12,2),
    fecha_vencimiento DATE,
    estado_pago BOOLEAN DEFAULT FALSE -- FALSE = pendiente, TRUE = pagado
);

-- Tabla de Cuentas Pagadas
CREATE TABLE cuentas_pagadas (
    id SERIAL PRIMARY KEY,
    cuenta_pagar_id INTEGER REFERENCES cuentas_pagar(id) ON DELETE CASCADE,
    fecha_pago TIMESTAMP DEFAULT NOW(),
    monto_pagado DECIMAL(12,2)
);

-- Tabla de Proveedores
CREATE TABLE proveedores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    contacto VARCHAR(255),
    telefono VARCHAR(50),
    email VARCHAR(255),
    direccion TEXT,
    nit VARCHAR(50) UNIQUE
);

-- Tabla de Compras a Proveedores
CREATE TABLE compras (
    id SERIAL PRIMARY KEY,
    proveedor_id INTEGER REFERENCES proveedores(id) ON DELETE CASCADE,
    fecha TIMESTAMP NOT NULL DEFAULT NOW(),
    monto_total DECIMAL(12,2) NOT NULL
);

-- Detalle de Compras
CREATE TABLE compra_detalle (
    id SERIAL PRIMARY KEY,
    compra_id INTEGER REFERENCES compras(id) ON DELETE CASCADE,
    descripcion_producto TEXT,
    cantidad INTEGER,
    precio_unitario DECIMAL(12,2)
);