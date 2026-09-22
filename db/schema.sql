CREATE TABLE IF NOT EXISTS cat_eventos (
    id_evento SERIAL PRIMARY KEY,
    nombre_evento VARCHAR(50) NOT NULL UNIQUE -- 'ENTRADA', 'SALIDA', etc.
);

INSERT INTO cat_eventos (nombre_evento) VALUES 
('ENTRADA'), ('SALIDA_COMIDA'), ('REGRESO_COMIDA'), ('SALIDA');

CREATE TABLE IF NOT EXISTS ubicaciones_autorizadas (
    id_ubicacion SERIAL PRIMARY KEY,
    nombre_ubicacion VARCHAR(100) NOT NULL, -- Ej: 'Oficina Central', 'Planta Zapopan'
    coordenadas POINT NOT NULL, -- Guardado como (longitud, latitud)
    radio_tolerancia_metros INT DEFAULT 50 NOT NULL, -- Distancia a la redonda permitida
    activo BOOLEAN DEFAULT TRUE NOT NULL
);

-- Creamos un enumerador para evitar errores de dedo al insertar el tipo
CREATE TYPE tipo_personal_enum AS ENUM ('INTERNO', 'VENDOR');

CREATE TABLE IF NOT EXISTS empleados (
    id_empleado SERIAL PRIMARY KEY,
    codigo_empleado VARCHAR(50) UNIQUE NOT NULL, 
    tipo_personal tipo_personal_enum DEFAULT 'INTERNO' NOT NULL, -- Diferencía Empleado vs Vendor
    
    -- Llave foránea a la nueva tabla (será NULL si el empleado es INTERNO)
    id_empresa_vendor INT REFERENCES empresas_vendors(id_empresa_vendor) ON DELETE SET NULL, 
    
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    puesto VARCHAR(100),
    id_ubicacion_asignada INT REFERENCES ubicaciones_autorizadas(id_ubicacion), 
    activo BOOLEAN DEFAULT TRUE NOT NULL,
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS empresas_vendors (
    id_empresa_vendor SERIAL PRIMARY KEY,
    nombre_empresa VARCHAR(100) UNIQUE NOT NULL, -- Ej: 'Seguridad Privada S.A.', 'Limpieza Express'
    rfc_o_tax_id VARCHAR(20), -- Opcional: Para temas fiscales o de contratos
    contacto_nombre VARCHAR(100), -- Nombre del supervisor de esa empresa
    contacto_telefono VARCHAR(20),
    activo BOOLEAN DEFAULT TRUE NOT NULL,
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS registro_asistencias (
    id_asistencia BIGSERIAL PRIMARY KEY,
    id_empleado INT NOT NULL REFERENCES empleados(id_empleado) ON DELETE CASCADE,
    id_evento INT NOT NULL REFERENCES cat_eventos(id_evento),
    fecha_hora TIMESTAMP WITH TIME ZONE NOT NULL,
    
    -- Campos de Ubicación y Validación
    id_ubicacion_marcada INT REFERENCES ubicaciones_autorizadas(id_ubicacion), -- Si checa en una sucursal física fija
    coordenadas_gps POINT, -- Si checa con app móvil, guardamos su (longitud, latitud) en ese instante
    
    dispositivo_origen VARCHAR(100), -- Ej: 'Reloj_Biometrico_A', 'App_Android'
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT uq_empleado_evento_hora UNIQUE (id_empleado, id_evento, fecha_hora)
);

-- Índice para acelerar los reportes de asistencia por fecha
CREATE INDEX  IF NOT EXISTS idx_asistencias_fecha_hora ON registro_asistencias(fecha_hora);



SELECT 
    ra.fecha_hora,
    ce.nombre_evento,
    e.nombre AS empleado_nombre,
    e.tipo_personal,
    COALESCE(ev.nombre_empresa, 'NUESTRA EMPRESA (INTERNO)') AS empresa -- Si es null, muestra que es interno
FROM registro_asistencias ra
JOIN empleados e ON ra.id_empleado = e.id_empleado
JOIN cat_eventos ce ON ra.id_evento = ce.id_evento
LEFT JOIN empresas_vendors ev ON e.id_empresa_vendor = ev.id_empresa_vendor
ORDER BY ra.fecha_hora DESC;


SELECT 
    -- 1. Agrupamos por el DÍA (truncando la fecha_hora)
    ra.fecha_hora::DATE AS dia_laborado,
    
    -- 2. Jalamos los datos del empleado asociado
    e.codigo_empleado,
    e.nombre || ' ' || e.apellido AS empleado,
    e.tipo_personal,
    
    -- 3. Buscamos la hora MÍNIMA (Entrada) y la MÁXIMA (Salida) de ese día
    MIN(CASE WHEN ce.nombre_evento = 'ENTRADA' THEN ra.fecha_hora::TIME END) AS hora_entrada,
    MAX(CASE WHEN ce.nombre_evento = 'SALIDA' THEN ra.fecha_hora::TIME END) AS hora_salida

FROM registro_asistencias ra
JOIN empleados e ON ra.id_empleado = e.id_empleado
JOIN cat_eventos ce ON ra.id_evento = ce.id_evento
GROUP BY 
    ra.fecha_hora::DATE, 
    e.id_empleado, 
    e.codigo_empleado, 
    e.nombre, 
    e.apellido, 
    e.tipo_personal
ORDER BY 
    dia_laborado DESC, 
    empleado ASC;

