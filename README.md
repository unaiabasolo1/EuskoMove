<div align="center">

# EuskoMove

### Sistema web seguro para la gestión, reserva y compra de billetes de autobús

[![Estado](https://img.shields.io/badge/Estado-En%20Desarrollo-yellow?style=flat-square)](https://github.com/unaiabasolo1/EuskoMove)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-green?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Azure](https://img.shields.io/badge/Azure-Deployed-0078D4?style=flat-square&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com)
[![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?style=flat-square&logo=terraform&logoColor=white)](https://terraform.io)

<br/>

> **EuskoMove** es una plataforma web completa que permite a los usuarios consultar rutas, horarios y reservar o comprar billetes de autobús de forma segura, con un panel de administración para gestionar toda la operativa del servicio.

<br/>

[Ver Proyecto](https://github.com/unaiabasolo1/EuskoMove) &nbsp;·&nbsp;
[Pull Requests](https://github.com/unaiabasolo1/EuskoMove/pulls) &nbsp;·&nbsp;
[Issues](https://github.com/unaiabasolo1/EuskoMove/issues) &nbsp;·&nbsp;
[Reportar Bug](https://github.com/unaiabasolo1/EuskoMove/issues/new) &nbsp;·&nbsp;
[Solicitar Feature](https://github.com/unaiabasolo1/EuskoMove/issues/new)

</div>

---

## Tabla de Contenidos

- [Características](#características)
- [Tecnologías](#tecnologías)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Uso](#uso)
- [Roles del Sistema](#roles-del-sistema)
- [Seguridad](#seguridad)

---

## Características

- **Gestión de rutas** — Administración completa de rutas de autobús con origen, destino y paradas intermedias
- **Horarios dinámicos** — Consulta y gestión de horarios en tiempo real
- **Reserva y compra de billetes** — Flujo completo de reserva con selección de asiento y pago
- **Sistema de bonos** — Descuentos aplicados automáticamente en la reserva
- **Sistema de avisos** — Notificaciones para usuarios sobre cambios, retrasos o incidencias
- **Autenticación segura** — Sistema de login con control de acceso por roles
- **Panel de administración** — Dashboard completo para gestionar rutas, horarios y usuarios
- **Observabilidad** — Logs centralizados en Azure Application Insights
- **Diseño responsive** — Interfaz adaptada a dispositivos móviles y escritorio

---

## Tecnologías

| Capa | Tecnología |
|------|-----------|
| **Frontend** | HTML5, CSS3, JavaScript, Jinja2 |
| **Backend** | Python 3.12, Flask 3.x, Gunicorn |
| **Base de datos** | PostgreSQL 16 (Azure Database for PostgreSQL) |
| **ORM** | SQLAlchemy 2.0 |
| **Infraestructura** | Azure App Service, Key Vault, Application Insights |
| **IaC** | Terraform |
| **CI/CD** | GitHub Actions |
| **Seguridad** | Flask-Talisman, bcrypt, Azure Key Vault |

---

## Estructura del Proyecto

```
EuskoMove/
├── app.py                        # Entrada a la aplicación
├── requirements.txt
├── backend/
│   ├── db.py                     # Modelos SQLAlchemy y conexión a BD
│   ├── auth.py                   # Lógica de autenticación y validación
│   └── routes/
│       ├── auth_routes.py        # Login, logout, registro
│       ├── public_routes.py      # Rutas públicas y búsqueda
│       ├── reservation_routes.py # Reserva y gestión de billetes
│       ├── admin_routes.py       # Panel de administración
│       ├── bono_routes.py        # Gestión de bonos
│       ├── notice_routes.py      # Avisos
│       └── avisos_routes.py
├── frontend/
│   ├── templates/                # Plantillas HTML (Jinja2)
│   └── static/                   # CSS y assets
├── infra/
│   ├── main.tf                   # Recursos principales de Azure
│   ├── variables.tf
│   ├── outputs.tf
│   ├── providers.tf
│   └── modules/
│       └── monitoring/
│           └── main.tf           # Log Analytics + Application Insights
└── tests/
    ├── test_unitarios.py
    ├── test_integracion.py
    └── test_caracteristicas.py
```

---

## Instalación

1. **Clona el repositorio**
```bash
   git clone https://github.com/unaiabasolo1/EuskoMove.git
   cd EuskoMove
```

2. **Despliega la infraestructura en Azure**

   Ve a GitHub → **Actions** → `terraform-deploy` → **Run workflow** → selecciona `apply`

   Esto crea automáticamente todos los recursos en Azure:
   - Resource Group, App Service, PostgreSQL
   - Key Vault con los secretos configurados
   - Log Analytics Workspace y Application Insights

3. **El código se despliega solo**

   Al finalizar el `terraform apply`, el propio workflow ejecuta el deploy de la aplicación automáticamente.

4. **Obtener la URL de la app**
```bash
   az webapp list --resource-group euskomove-dev-rg --query "[].defaultHostName" -o tsv
```

---

## Uso

### Usuario

1. Accede a la página principal
2. Busca tu ruta introduciendo origen y destino
3. Selecciona el horario disponible
4. Reserva o compra tu billete
5. Consulta tus billetes en **"Mis Billetes"**

### Administrador

1. Accede al panel en `/admin`
2. Gestiona rutas, horarios y avisos desde el dashboard
3. Consulta reservas y estadísticas de uso

---

## Roles del Sistema

| Rol | Permisos |
|-----|----------|
| **Usuario** | Buscar rutas, reservar y comprar billetes, ver avisos, usar bonos |
| **Administrador** | Gestión completa de rutas, horarios, avisos, bonos y usuarios |

---

## Seguridad

EuskoMove implementa las siguientes medidas de seguridad:

- Validación y saneamiento de datos de entrada (reglas NIST)
- Protección contra inyección SQL mediante ORM con consultas preparadas
- Gestión de sesiones segura con Flask-Talisman (HTTPS forzado en producción)
- Control de acceso por roles
- Contraseñas almacenadas con bcrypt
- Secretos gestionados en Azure Key Vault (sin credenciales en el código)
- Escaneo automático de secretos en cada commit con Gitleaks

---

<div align="center">

Hecho por [unaiabasolo1](https://github.com/unaiabasolo1)

</div>
