<div align="center">

# EuskoMove — Backend

### Servidor web del sistema de gestión y reserva de billetes de autobús

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=flat-square)](https://sqlalchemy.org)
[![Azure](https://img.shields.io/badge/Azure-Deployed-0078D4?style=flat-square&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com)

<br/>

> Servicio backend de **EuskoMove** construido con Flask. Gestiona rutas, horarios, usuarios, reservas, bonos y avisos del sistema. Desplegado en Azure App Service con logs centralizados en Application Insights.

<br/>

[Ver Proyecto](https://github.com/unaiabasolo1/EuskoMove) &nbsp;·&nbsp;
[Pull Requests](https://github.com/unaiabasolo1/EuskoMove/pulls) &nbsp;·&nbsp;
[Issues](https://github.com/unaiabasolo1/EuskoMove/issues) &nbsp;·&nbsp;
[Reportar Bug](https://github.com/unaiabasolo1/EuskoMove/issues/new)

</div>

---

## Tabla de Contenidos

- [Tecnologías](#tecnologías)
- [Estructura](#estructura)
- [Instalación](#instalación)
- [Variables de entorno](#variables-de-entorno)
- [Rutas principales](#rutas-principales)

---

## Tecnologías

| Capa | Tecnología |
|------|-----------|
| **Lenguaje** | Python 3.12 |
| **Framework** | Flask 3.x + Gunicorn |
| **Base de datos** | PostgreSQL 16 (Azure Database for PostgreSQL) |
| **ORM** | SQLAlchemy 2.0 |
| **Seguridad** | Flask-Talisman, bcrypt, Azure Key Vault |
| **Observabilidad** | Azure Application Insights (opencensus-ext-azure) |
| **Dependencias** | requirements.txt |

---

## Estructura

```
backend/
├── db.py                     # Modelos SQLAlchemy y conexión a BD
├── auth.py                   # Lógica de autenticación y validación
├── database.py               # Configuración de la sesión
├── requirements.txt
└── routes/
    ├── auth_routes.py        # Login, logout, registro
    ├── public_routes.py      # Página principal y búsqueda de rutas
    ├── reservation_routes.py # Reserva, mis viajes, cancelación
    ├── admin_routes.py       # Panel de administración
    ├── bono_routes.py        # Compra y uso de bonos
    ├── notice_routes.py      # Gestión de avisos (admin)
    └── avisos_routes.py      # Visualización de avisos (usuario)
```

---

## Instalación

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/unaiabasolo1/EuskoMove.git
   cd EuskoMove
   ```

2. **Despliega en Azure vía GitHub Actions**

   Ve a GitHub → **Actions** → `terraform-deploy` → **Run workflow** → selecciona `apply`

   Esto crea toda la infraestructura y despliega el backend automáticamente.

3. **Accede a la aplicación**

   [https://euskomove-dev-uu0enx.azurewebsites.net](https://euskomove-dev-uu0enx.azurewebsites.net)

4. **Para desarrollo local**
   ```bash
   pip install -r requirements.txt
   python app.py
   ```

---

## Variables de entorno

En producción las gestiona Azure Key Vault. Para desarrollo local crea un `.env` en la raíz:

```env
FLASK_SECRET_KEY=tu_clave_secreta
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/euskomovedb
FLASK_ENV=development
LOG_LEVEL=INFO
```

---

## Rutas principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Página principal |
| `GET` | `/search` | Búsqueda de rutas y horarios |
| `GET/POST` | `/login` | Autenticación de usuario |
| `GET/POST` | `/register` | Registro de usuario |
| `POST` | `/logout` | Cierre de sesión |
| `GET` | `/book/<id>` | Formulario de reserva |
| `POST` | `/book/<id>` | Confirmar reserva |
| `GET` | `/my-trips` | Mis viajes |
| `POST` | `/cancel/<id>` | Cancelar reserva |
| `GET` | `/avisos` | Listado de avisos activos |
| `GET` | `/bonos` | Bonos disponibles |
| `GET` | `/admin` | Panel de administración |

---

<div align="center">

Hecho por [unaiabasolo1](https://github.com/unaiabasolo1)

</div>
