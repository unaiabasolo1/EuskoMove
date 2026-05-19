<div align="center">

# EuskoMove — Frontend

### Interfaz web del sistema de reserva y compra de billetes de autobús

[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

<br/>

> Interfaz de usuario de **EuskoMove** desarrollada con HTML, CSS y JavaScript. Permite a los usuarios buscar rutas, consultar horarios, reservar billetes y recibir avisos del servicio.

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
- [Vistas principales](#vistas-principales)
- [Conexión con el backend](#conexión-con-el-backend)

---

## Tecnologías

| Capa | Tecnología |
|------|-----------|
| **Maquetación** | HTML5 |
| **Estilos** | CSS3 |
| **Interactividad** | JavaScript (vanilla) |

---

## Estructura

```
frontend/

```

---

## Instalación

El frontend es estático, no requiere instalación de dependencias. Basta con abrirlo en el navegador o servirlo con cualquier servidor HTTP.

1. **Clona el repositorio y accede a la carpeta**
   ```bash
   git clo
   ```


---

## Vistas principales

| Vista | Descripción |
|-------|-------------|
| `index.html` | Página de inicio y bienvenida |
| `buscar.html` | Búsqueda de rutas por origen y destino |
| `reservar.html` | Selección de horario y compra de billete |
| `mis-billetes.html` | Historial de reservas del usuario |
| `avisos.html` | Avisos e incidencias del servicio |

---

## Conexión con el backend

Las peticiones al backend se realizan mediante `fetch` apuntando a la API REST. Configura la URL base en el archivo de configuración:

```javascript
// assets/js/config.js
const API_BASE_URL = 'http://localhost:5000';
```

---


<div align="center">

Hecho por [unaiabasolo1](https://github.com/unaiabasolo1)

</div>