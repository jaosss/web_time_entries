-- ============================================================
-- Schema corregido: empresas_vendors debe crearse ANTES de
-- empleados, ya que empleados tiene una FK hacia esa tabla.
-- ============================================================

CREATE TABLE IF NOT EXISTS cat_eventos (
    id_evento SERIAL PRIMARY KEY,
    nombre_evento VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO cat_eventos (nombre_evento) VALUES
('ENTRADA'), ('SALIDA_COMIDA'), ('REGRESO_COMIDA'), ('SALIDA')
ON CONFLICT (nombre_evento) DO NOTHING;

CREATE TABLE IF NOT EXISTS ubicaciones_autorizadas (
    id_ubicacion SERIAL PRIMARY KEY,
    nombre_ubicacion VARCHAR(100) NOT NULL,
    coordenadas POINT NOT NULL,
    radio_tolerancia_metros INT DEFAULT 50 NOT NULL,
    activo BOOLEAN DEFAULT TRUE NOT NULL
);

DO $$ BEGIN
    CREATE TYPE tipo_personal_enum AS ENUM ('INTERNO', 'VENDOR');
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

-- empresas_vendors se crea ANTES de empleados
CREATE TABLE IF NOT EXISTS empresas_vendors (
    id_empresa_vendor SERIAL PRIMARY KEY,
    nombre_empresa VARCHAR(100) UNIQUE NOT NULL,
    rfc_o_tax_id VARCHAR(20),
    contacto_nombre VARCHAR(100),
    contacto_telefono VARCHAR(20),
    activo BOOLEAN DEFAULT TRUE NOT NULL,
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS empleados (
    id_empleado SERIAL PRIMARY KEY,
    codigo_empleado VARCHAR(50) UNIQUE NOT NULL,
    tipo_personal tipo_personal_enum DEFAULT 'INTERNO' NOT NULL,
    id_empresa_vendor INT REFERENCES empresas_vendors(id_empresa_vendor) ON DELETE SET NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    puesto VARCHAR(100),
    id_ubicacion_asignada INT REFERENCES ubicaciones_autorizadas(id_ubicacion),
    activo BOOLEAN DEFAULT TRUE NOT NULL,
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS registro_asistencias (
    id_asistencia BIGSERIAL PRIMARY KEY,
    id_empleado INT NOT NULL REFERENCES empleados(id_empleado) ON DELETE CASCADE,
    id_evento INT NOT NULL REFERENCES cat_eventos(id_evento),
    fecha_hora TIMESTAMP WITH TIME ZONE NOT NULL,
    id_ubicacion_marcada INT REFERENCES ubicaciones_autorizadas(id_ubicacion),
    coordenadas_gps POINT,
    dispositivo_origen VARCHAR(100),
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_empleado_evento_hora UNIQUE (id_empleado, id_evento, fecha_hora)
);

CREATE INDEX IF NOT EXISTS idx_asistencias_fecha_hora ON registro_asistencias(fecha_hora);
