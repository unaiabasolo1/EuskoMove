<div align="center">

# EuskoMove — Frontend

### Interfaz web del sistema de reserva y compra de billetes de autobús

[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Jinja2](https://img.shields.io/badge/Jinja2-Templates-B41717?style=flat-square)](https://jinja.palletsprojects.com)

<br/>

> Interfaz de usuario de **EuskoMove** desarrollada con HTML5, CSS3, JavaScript y plantillas Jinja2. Servida directamente por Flask, permite a los usuarios buscar rutas, consultar horarios, reservar billetes, gestionar bonos y recibir avisos del servicio.

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
- [Vistas principales](#vistas-principales)
- [Acceso](#acceso)

---

## Tecnologías

| Capa | Tecnología |
|------|-----------| 
| **Maquetación** | HTML5 |
| **Estilos** | CSS3 |
| **Interactividad** | JavaScript (vanilla) |
| **Plantillas** | Jinja2 (renderizado server-side por Flask) |

---

## Estructura

```
frontend/
├── templates/
│   ├── base.html             # Plantilla base (navbar, footer, estilos comunes)
│   ├── index.html            # Página principal
│   ├── search.html           # Búsqueda de rutas y horarios
│   ├── book.html             # Selección de asiento y confirmación de reserva
│   ├── my_trips.html         # Mis viajes y reservas
│   ├── login.html            # Inicio de sesión
│   ├── register.html         # Registro de usuario
│   ├── bonos.html            # Bonos disponibles y activos
│   ├── avisos.html           # Avisos e incidencias del servicio
│   └── admin.html            # Panel de administración
└── static/
    └── styles.css            # Estilos globales
```

---

## Vistas principales

| Vista | Ruta | Descripción |
|-------|------|-------------|
| `index.html` | `/` | Página de inicio y bienvenida |
| `search.html` | `/search` | Búsqueda de rutas por origen, destino y fecha |
| `book.html` | `/book/<id>` | Selección de asiento y confirmación de reserva |
| `my_trips.html` | `/my-trips` | Historial de reservas del usuario |
| `login.html` | `/login` | Inicio de sesión |
| `register.html` | `/register` | Registro de nuevo usuario |
| `bonos.html` | `/bonos` | Bonos disponibles y descuentos |
| `avisos.html` | `/avisos` | Avisos e incidencias del servicio |
| `admin.html` | `/admin` | Panel de administración (solo administradores) |

---

## Acceso

El frontend está integrado con el backend Flask y se despliega junto a él en Azure App Service.

Accede a la aplicación en: [https://euskomove-dev-uu0enx.azurewebsites.net](https://euskomove-dev-uu0enx.azurewebsites.net)

---

<div align="center">

Hecho por [unaiabasolo1](https://github.com/unaiabasolo1)

</div>
