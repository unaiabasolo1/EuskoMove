<div align="center">

# EuskoMove — Backend

### API REST del sistema de gestión y reserva de billetes de autobús

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Framework-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://mysql.com)

<br/>

> Servicio backend de **EuskoMove** construido con Flask. Expone la API REST que gestiona rutas, horarios, usuarios, reservas y avisos del sistema.

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
- [Endpoints principales](#endpoints-principales)
- [Licencia](#licencia)

---

## Tecnologías

| Capa | Tecnología |
|------|-----------|
| **Lenguaje** | Python 3.x |
| **Framework** | Flask |
| **Base de datos** | MySQL |
| **Dependencias** | requirements.txt |

---

## Estructura

```
backend/

```

---

## Instalación


1. **Clona el repositorio y accede a la carpeta**
   ```bash
   git
   ```


---

## Variables de entorno

Crea un archivo `.env` en la raíz del backend con las siguientes variables:

```env
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=mysql://usuario:contraseña@localhost/euskomove
SECRET_KEY=tu_clave_secreta
```

---

## Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/rutas` | Listado de rutas disponibles |
| `GET` | `/horarios` | Horarios por ruta |
| `POST` | `/reservas` | Crear una reserva |
| `GET` | `/reservas/:id` | Consultar una reserva |
| `POST` | `/auth/login` | Autenticación de usuario |
| `GET` | `/avisos` | Listado de avisos activos |


---

<div align="center">

Hecho por [unaiabasolo1](https://github.com/unaiabasolo1)

</div>