-- Script para crear las tablas del sistema de laboratorio
-- Fecha: 2025-01-01

-- Tabla para fisicoquímica (vapor y agua)
CREATE TABLE IF NOT EXISTS mediciones_fisicoquimica (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('vapor', 'agua')),
    punto VARCHAR(20) NOT NULL,
    parametro VARCHAR(50) NOT NULL,
    fecha DATE NOT NULL,
    dato DECIMAL(10, 4) NOT NULL,
    nota TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para microbiología
CREATE TABLE IF NOT EXISTS mediciones_microbiologia (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    punto VARCHAR(50) NOT NULL,
    parametro VARCHAR(50) NOT NULL,
    fecha DATE NOT NULL,
    dato DECIMAL(10, 4) NOT NULL,
    nota TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_fisico_fecha ON mediciones_fisicoquimica(fecha);
CREATE INDEX IF NOT EXISTS idx_fisico_punto ON mediciones_fisicoquimica(punto);
CREATE INDEX IF NOT EXISTS idx_fisico_parametro ON mediciones_fisicoquimica(parametro);
CREATE INDEX IF NOT EXISTS idx_fisico_tipo ON mediciones_fisicoquimica(tipo);

CREATE INDEX IF NOT EXISTS idx_micro_fecha ON mediciones_microbiologia(fecha);
CREATE INDEX IF NOT EXISTS idx_micro_tipo ON mediciones_microbiologia(tipo);

-- Comentarios para documentación
COMMENT ON TABLE mediciones_fisicoquimica IS 'Mediciones de parámetros fisicoquímicos (vapor y agua)';
COMMENT ON TABLE mediciones_microbiologia IS 'Mediciones microbiológicas';

COMMENT ON COLUMN mediciones_fisicoquimica.tipo IS 'Tipo: vapor o agua';
COMMENT ON COLUMN mediciones_fisicoquimica.punto IS 'Punto de muestreo (PMV001-008 o PA001-018)';
COMMENT ON COLUMN mediciones_fisicoquimica.parametro IS 'Parámetro medido (PH, TOC, CONDUCTIVIDAD, etc)';
COMMENT ON COLUMN mediciones_fisicoquimica.dato IS 'Valor numérico de la medición';


