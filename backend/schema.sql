-- =============================================
-- EuskoMove — Esquema de base de datos
-- PostgreSQL
-- =============================================

CREATE TABLE IF NOT EXISTS usuarios (
    id              SERIAL PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    apellidos       VARCHAR(150) NOT NULL,
    email           VARCHAR(255) UNIQUE NOT NULL,
    password_hash   TEXT NOT NULL,
    rol             VARCHAR(20) DEFAULT 'usuario',  -- 'usuario' | 'admin'
    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS horarios (
    id              SERIAL PRIMARY KEY,
    linea           VARCHAR(10) NOT NULL,
    origen          VARCHAR(100) NOT NULL,
    destino         VARCHAR(100) NOT NULL,
    hora_salida     TIME NOT NULL,
    hora_llegada    TIME NOT NULL,
    plazas_totales  INT DEFAULT 40,
    activo          BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS reservas (
    id                  SERIAL PRIMARY KEY,
    usuario_id          INT REFERENCES usuarios(id),
    horario_id          INT REFERENCES horarios(id),
    fecha               DATE NOT NULL,
    asientos            INT[] NOT NULL,
    nombre_pasajero     VARCHAR(100) NOT NULL,
    apellidos_pasajero  VARCHAR(150) NOT NULL,
    email_pasajero      VARCHAR(255) NOT NULL,
    dni_pasajero        VARCHAR(20) NOT NULL,
    estado              VARCHAR(20) DEFAULT 'confirmada',  -- 'confirmada' | 'cancelada'
    localizador         VARCHAR(20) UNIQUE NOT NULL,
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS avisos (
    id              SERIAL PRIMARY KEY,
    tipo            VARCHAR(20) NOT NULL,  -- 'aviso' | 'urgente' | 'info'
    titulo          VARCHAR(200) NOT NULL,
    descripcion     TEXT NOT NULL,
    lineas          VARCHAR(100),
    autor_id        INT REFERENCES usuarios(id),
    created_at      TIMESTAMP DEFAULT NOW()
);

-- Datos de ejemplo
INSERT INTO horarios (linea, origen, destino, hora_salida, hora_llegada) VALUES
    ('L-12', 'Vitoria-Gasteiz', 'Bilbao',           '08:00', '09:15'),
    ('L-12', 'Vitoria-Gasteiz', 'Bilbao',           '10:30', '11:45'),
    ('L-07', 'Vitoria-Gasteiz', 'San Sebastián',    '09:00', '10:30'),
    ('L-03', 'Bilbao',          'Pamplona',          '11:00', '12:45'),
    ('L-18', 'San Sebastián',   'Vitoria-Gasteiz',  '14:15', '15:45');