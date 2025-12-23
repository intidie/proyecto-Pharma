-- Crear tablas para el sistema de laboratorio
-- Fecha: 2025-12-22

-- Tabla TOC
CREATE TABLE IF NOT EXISTS mediciones_toc (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    dato DECIMAL(10, 2) NOT NULL,
    pu VARCHAR(3) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notas TEXT
);

-- Tabla pH
CREATE TABLE IF NOT EXISTS mediciones_ph (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    dato DECIMAL(10, 2) NOT NULL,
    pu VARCHAR(3) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notas TEXT
);

-- Tabla Conductividad
CREATE TABLE IF NOT EXISTS mediciones_conductividad (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    dato DECIMAL(10, 2) NOT NULL,
    pu VARCHAR(3) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notas TEXT
);

-- Tabla Microbiología
CREATE TABLE IF NOT EXISTS mediciones_microbiologia (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    dato DECIMAL(10, 2) NOT NULL,
    pu VARCHAR(3) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notas TEXT
);

-- Índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_toc_fecha ON mediciones_toc(fecha);
CREATE INDEX IF NOT EXISTS idx_ph_fecha ON mediciones_ph(fecha);
CREATE INDEX IF NOT EXISTS idx_cond_fecha ON mediciones_conductividad(fecha);
```

