<div align="center">

# EuskoMove — Tests

### Suite de pruebas automatizadas del sistema

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Pytest](https://img.shields.io/badge/Pytest-Framework-0A9EDC?style=flat-square&logo=pytest&logoColor=white)](https://pytest.org)
[![SQLite](https://img.shields.io/badge/SQLite-In--Memory-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)

<br/>

> Suite de pruebas de **EuskoMove** organizada en tres niveles: unitarios, integración y características. Todos los tests usan SQLite en memoria, por lo que no requieren conexión a la base de datos de Azure.

<br/>

[Ver Proyecto](https://github.com/unaiabasolo1/EuskoMove) &nbsp;·&nbsp;
[Pull Requests](https://github.com/unaiabasolo1/EuskoMove/pulls) &nbsp;·&nbsp;
[Issues](https://github.com/unaiabasolo1/EuskoMove/issues) &nbsp;·&nbsp;
[Reportar Bug](https://github.com/unaiabasolo1/EuskoMove/issues/new)

</div>

---

## Tabla de Contenidos

- [Estructura](#estructura)
- [Tipos de tests](#tipos-de-tests)
- [Ejecución](#ejecución)
- [Resultados esperados](#resultados-esperados)

---

## Estructura

```
tests/
├── test_unitarios.py         # Tests de funciones aisladas
├── test_integracion.py       # Tests de capas trabajando juntas
└── test_caracteristicas.py   # Tests de flujos completos de usuario
```

---

## Tipos de tests

### Unitarios (`test_unitarios.py`) — 31 tests
Comprueban funciones aisladas sin dependencias externas:
- Hash y verificación de contraseñas (bcrypt)
- Validación de registro (nombre, email, contraseña, confirmación)
- Rutas HTTP básicas (códigos de respuesta, redirecciones)
- Login y logout

### Integración (`test_integracion.py`) — 13 tests
Comprueban que varias capas funcionan juntas correctamente (BD ↔ lógica ↔ rutas HTTP):
- Flujo completo de autenticación
- Registro crea usuario en base de datos
- Control de acceso por roles
- Sesiones de usuario

### Características (`test_caracteristicas.py`) — 16 tests
Comprueban el comportamiento completo desde el punto de vista del usuario:
- Escenario de registro exitoso
- Escenario de login fallido
- Acceso restringido a rutas de administrador
- Flujos de reserva y cancelación

---

## Ejecución

**Todos los tests:**
```bash
pytest
```

**Por tipo:**
```bash
pytest tests/test_unitarios.py -v
pytest tests/test_integracion.py -v
pytest tests/test_caracteristicas.py -v
```

**Con resumen de cobertura:**
```bash
pytest --tb=short -q
```

Los tests se ejecutan automáticamente antes de cada commit gracias al hook de Git configurado en `.git_hooks/pre-commit`.

---

## Resultados esperados

```
31 passed   ← unitarios
13 passed   ← integración
16 passed   ← características
─────────────────────────
60 passed en total
```

No se requiere ninguna variable de entorno ni conexión a Azure — los tests usan SQLite en memoria de forma automática.

---

<div align="center">

Hecho por [unaiabasolo1](https://github.com/unaiabasolo1)

</div>
