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

-- INSERTS
INSERT INTO empresas (nombre, nit) VALUES
('Textiles Aurora', 'EMP-TX-001'),
('Hilos y Tramas S.A.', 'EMP-HT-002'),
('Tejidos Lunares', 'EMP-TL-003'),
('Fibras Mayas', 'EMP-FM-004'),
('Tramas del Sur', 'EMP-TS-005'),
('Uniformes Elite', 'EMP-UE-006'),
('Hilandería Nacional', 'EMP-HN-007'),
('Colores de Tela', 'EMP-CT-008'),
('Industria Textil Maya', 'EMP-IT-009'),
('Confecciones Abril', 'EMP-CA-010');


INSERT INTO clientes (codigo_cliente, empresa_id, estado, nombre, contacto, nit, direccion, direccion_entrega, telefono, email, cartera) VALUES
('CLT001', 1, TRUE, 'Telas Finas Guatemala', 'Sofía Méndez', 'CL-NIT-001', 'Zona 5, Calle 6', 'Zona 7, Bodega 2', '54121234', 'ventas@tfg.com', 0.00),
('CLT002', 2, TRUE, 'Almacén Hilos de Oro', 'Luis Palacios', 'CL-NIT-002', 'Zona 1, 4ta Avenida', 'Zona 3, Local 11', '58231455', 'contacto@hilosoro.com', 100.50),
('CLT003', 3, TRUE, 'Distribuidora Trama Perfecta', 'Carmen Reyes', 'CL-NIT-003', 'Zona 10, Edificio Jade', 'Zona 12, Oficina 6', '56991234', 'info@tramaperfecta.com', 50.00),
('CLT004', 4, TRUE, 'Hilos y Telas Centro', 'José Ramos', 'CL-NIT-004', 'Zona 6, Local 8', 'Zona 6, Bodega B', '55443322', 'servicio@htcentro.com', 0.00),
('CLT005', 5, TRUE, 'Tramas & Colores', 'Andrea Linares', 'CL-NIT-005', 'Zona 9, Calle Real', 'Zona 11, Local 21', '55667788', 'tramas@colores.com', 75.25),
('CLT006', 6, TRUE, 'Comercial Textil Xela', 'Juan Morales', 'CL-NIT-006', 'Quetzaltenango, Av. Central', 'Quetzaltenango, Bodega 5', '55331122', 'ventas@textilxela.com', 0.00),
('CLT007', 7, TRUE, 'Moda y Tela', 'Luisa Figueroa', 'CL-NIT-007', 'Zona 18, Centro Norte', 'Zona 18, Plaza Futura', '55669988', 'contacto@modaytela.com', 20.00),
('CLT008', 8, TRUE, 'Hilados Deluxe', 'Fernando Díaz', 'CL-NIT-008', 'Mixco, Plaza Azul', 'Mixco, Local B2', '55224466', 'info@hiladosdeluxe.com', 10.00),
('CLT009', 9, TRUE, 'Trama Ideal', 'Karina Salguero', 'CL-NIT-009', 'Zona 8, Edificio B', 'Zona 8, Bodega 3', '55887766', 'ventas@tramaideal.com', 33.33),
('CLT010', 10, TRUE, 'Telas de Occidente', 'Miguel Estrada', 'CL-NIT-010', 'Chimaltenango, Calle 3', 'Chimaltenango, Lote 2', '55001122', 'servicio@telasoccidente.com', 0.00);


INSERT INTO proveedores (nombre, contacto, telefono, email, direccion, nit) VALUES
('Proveeduría Textil Maya', 'David Hernández', '55112233', 'ventas@textilmaya.com', 'Zona 4, Bodega C', 'PV-NIT-001'),
('Hilos y Telas del Sur', 'Gloria López', '55334455', 'contacto@htsur.com', 'Zona 6, Local B9', 'PV-NIT-002'),
('Comercial de Fibras', 'Elena Jiménez', '55221133', 'comercial@fibras.com', 'Zona 3, Calle F', 'PV-NIT-003'),
('Textiles Premium', 'Carlos Ríos', '55887766', 'ventas@textilespremium.com', 'Zona 1, Av. Reforma', 'PV-NIT-004'),
('Hilos de Oriente', 'Ana Contreras', '55009988', 'info@hilosoriente.com', 'Chiquimula, Plaza Central', 'PV-NIT-005'),
('Telas Industriales SA', 'Luis Ramos', '55998877', 'ventas@telaindsa.com', 'Zona 12, Parque Tecno', 'PV-NIT-006'),
('Hilandería Imperial', 'Silvia Martínez', '55773322', 'ventas@imperial.com', 'Escuintla, Zona 2', 'PV-NIT-007'),
('Central Textil', 'Marco Álvarez', '55446677', 'soporte@centraltextil.com', 'Cobán, Bodega 1', 'PV-NIT-008'),
('Tramas SA', 'Daniela López', '55880011', 'tramas@sa.com', 'Zona 15, Av. Las Rosas', 'PV-NIT-009'),
('Fábrica de Hilos Xelajú', 'Mario Pérez', '55119900', 'contacto@hilosxelaju.com', 'Xela, Calle C', 'PV-NIT-010');


INSERT INTO pedidos (cliente_id, fecha, precio_total) VALUES
(1, '2024-05-01 10:00:00', 450.00),
(2, '2024-05-02 11:30:00', 275.75),
(3, '2024-05-03 09:45:00', 150.00),
(4, '2024-05-04 14:15:00', 680.20),
(5, '2024-05-05 12:00:00', 330.90),
(6, '2024-05-06 15:30:00', 110.00),
(7, '2024-05-07 13:20:00', 520.50),
(8, '2024-05-08 10:10:00', 305.25),
(9, '2024-05-09 08:50:00', 140.40),
(10, '2024-05-10 17:00:00', 789.99);


INSERT INTO pedido_detalle (pedido_id, descripcion_producto, cantidad, precio_unitario) VALUES
(1, 'Tela algodón premium blanca', 30, 15.00),
(2, 'Hilo poliéster azul 500m', 25, 5.50),
(3, 'Tela lino natural', 10, 15.00),
(4, 'Hilo de bordado rojo 300m', 50, 3.20),
(5, 'Tela denim oscura', 20, 12.50),
(6, 'Tela jersey suave', 15, 7.30),
(7, 'Hilo seda negra 250m', 10, 9.50),
(8, 'Tela canvas color beige', 12, 8.40),
(9, 'Tela popelina azul claro', 8, 10.30),
(10, 'Tela tipo franela gris', 40, 8.00);


INSERT INTO cuentas_pagar (cliente_id, monto, fecha_vencimiento, estado_pago) VALUES
(1, 200.00, '2024-06-01', FALSE),
(2, 300.00, '2024-06-05', TRUE),
(3, 180.00, '2024-06-10', FALSE),
(4, 150.00, '2024-06-15', TRUE),
(5, 400.00, '2024-06-20', FALSE),
(6, 100.00, '2024-06-22', FALSE),
(7, 220.00, '2024-06-25', TRUE),
(8, 310.00, '2024-06-28', FALSE),
(9, 190.00, '2024-06-30', TRUE),
(10, 500.00, '2024-07-02', FALSE);


INSERT INTO cuentas_pagadas (cuenta_pagar_id, fecha_pago, monto_pagado) VALUES
(2, '2024-05-06 10:30:00', 300.00),
(4, '2024-05-10 14:45:00', 150.00),
(7, '2024-05-12 12:00:00', 220.00),
(9, '2024-05-15 13:15:00', 190.00),
(2, '2024-05-17 09:30:00', 50.00),
(4, '2024-05-18 11:10:00', 25.00),
(7, '2024-05-19 15:00:00', 80.00),
(9, '2024-05-20 16:45:00', 60.00),
(4, '2024-05-21 10:00:00', 20.00),
(7, '2024-05-22 14:20:00', 100.00);


INSERT INTO compras (proveedor_id, fecha, monto_total) VALUES
(1, '2024-04-25 10:00:00', 800.00),
(2, '2024-04-26 11:00:00', 1200.50),
(3, '2024-04-27 12:15:00', 950.75),
(4, '2024-04-28 09:30:00', 400.00),
(5, '2024-04-29 14:40:00', 780.00),
(6, '2024-04-30 13:10:00', 500.00),
(7, '2024-05-01 15:45:00', 650.60),
(8, '2024-05-02 16:00:00', 300.00),
(9, '2024-05-03 17:30:00', 430.20),
(10, '2024-05-04 10:50:00', 910.99);


INSERT INTO compra_detalle (compra_id, descripcion_producto, cantidad, precio_unitario) VALUES
(1, 'Rollos de lino', 20, 40.00),
(2, 'Cajas de hilo poliéster', 15, 50.00),
(3, 'Tela stretch negra', 25, 38.03),
(4, 'Tela jersey algodón', 30, 13.33),
(5, 'Tela oxford blanca', 40, 19.50),
(6, 'Hilo bordado multicolor', 18, 11.11),
(7, 'Tela drill caqui', 20, 32.53),
(8, 'Hilo encerado', 12, 25.00),
(9, 'Tela rayón celeste', 22, 19.55),
(10, 'Tela polar gruesa', 16, 45.00);