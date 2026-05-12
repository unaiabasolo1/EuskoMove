<div align="center">

# EuskoMove

### Sistema web seguro para la gestión, reserva y compra de billetes de autobús

[![Estado](https://img.shields.io/badge/Estado-En%20Desarrollo-yellow?style=flat-square)](https://github.com/unaiabasolo1/EuskoMove)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-green?style=flat-square)](LICENSE)
[![PHP](https://img.shields.io/badge/PHP-8.x-777BB4?style=flat-square&logo=php&logoColor=white)](https://php.net)
[![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://mysql.com)
[![HTML5](https://img.shields.io/badge/HTML5-Frontend-E34F26?style=flat-square&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)

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
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

---

## Características

- **Gestión de rutas** — Administración completa de rutas de autobús con origen, destino y paradas intermedias
- **Horarios dinámicos** — Consulta y gestión de horarios en tiempo real
- **Reserva y compra de billetes** — Flujo completo de reserva con selección de asiento y pago
- **Sistema de avisos** — Notificaciones para usuarios sobre cambios, retrasos o incidencias
- **Autenticación segura** — Sistema de login con control de acceso por roles
- **Panel de administración** — Dashboard completo para gestionar rutas, horarios y usuarios
- **Diseño responsive** — Interfaz adaptada a dispositivos móviles y escritorio

---

## Tecnologías

| Capa | Tecnología |
|------|-----------|
| **Frontend** | HTML5, CSS3, JavaScript |
| **Backend** | PHP 8.x |
| **Base de datos** | MySQL |
| **Servidor** | Apache (XAMPP / WAMP) |
| **Estilos** | Bootstrap |

---

## Estructura del Proyecto

```
EuskoMove/
└── README.md
```

---

## Instalación


1. **Clona el repositorio**
   ```bash
   ghjhyj
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
| **Usuario** | Buscar rutas, reservar y comprar billetes, ver avisos |
| **Administrador** | Gestión completa de rutas, horarios, avisos y usuarios |

---

## Seguridad

EuskoMove implementa las siguientes medidas de seguridad:

- Validación y saneamiento de datos de entrada
- Protección contra inyección SQL mediante consultas preparadas
- Gestión de sesiones segura
- Control de acceso por roles
- Contraseñas almacenadas con hash