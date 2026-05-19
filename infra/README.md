<div align="center">

# EuskoMove — Infraestructura

### Definición y aprovisionamiento de infraestructura cloud con Terraform

[![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?style=flat-square&logo=terraform&logoColor=white)](https://terraform.io)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-2088FF?style=flat-square&logo=githubactions&logoColor=white)](https://github.com/features/actions)

<br/>

> Infraestructura como código de **EuskoMove**. Contiene la definición Terraform para aprovisionar y gestionar todos los recursos cloud del sistema, con despliegue automatizado mediante GitHub Actions y autenticación OIDC.

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
- [Uso](#uso)
- [CI/CD con GitHub Actions](#cicd-con-github-actions)

---

## Tecnologías

| Herramienta | Uso |
|-------------|-----|
| **Terraform** | Aprovisionamiento de infraestructura (IaC) |
| **GitHub Actions** | Pipeline de CI/CD para apply/destroy automático |
| **OIDC** | Autenticación sin credenciales estáticas |

---

## Estructura

```
infra/

```


---

## Uso

1. **Accede a la carpeta**
   ```bash
   cd EuskoMove/infra
   ```


---

## CI/CD con GitHub Actions

El workflow en `.github/workflows/` automatiza el despliegue de infraestructura. Utiliza **OIDC** para autenticarse con el proveedor cloud sin necesidad de almacenar credenciales estáticas como secrets.

| Evento | Acción |
|--------|--------|
| Push a `master` | `terraform apply` automático |
| Pull Request | `terraform plan` como revisión previa |

---


<div align="center">

Hecho por [unaiabasolo1](https://github.com/unaiabasolo1)

</div>