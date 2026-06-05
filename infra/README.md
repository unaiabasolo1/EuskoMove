<div align="center">

# EuskoMove — Infraestructura

### Definición y aprovisionamiento de infraestructura cloud con Terraform

[![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?style=flat-square&logo=terraform&logoColor=white)](https://terraform.io)
[![Azure](https://img.shields.io/badge/Azure-Cloud-0078D4?style=flat-square&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-2088FF?style=flat-square&logo=githubactions&logoColor=white)](https://github.com/features/actions)

<br/>

> Infraestructura como código de **EuskoMove**. Contiene la definición Terraform para aprovisionar y gestionar todos los recursos cloud del sistema en Azure, con despliegue automatizado mediante GitHub Actions y autenticación OIDC sin credenciales estáticas.

<br/>

[Ver Proyecto](https://github.com/unaiabasolo1/EuskoMove) &nbsp;·&nbsp;
[Pull Requests](https://github.com/unaiabasolo1/EuskoMove/pulls) &nbsp;·&nbsp;
[Issues](https://github.com/unaiabasolo1/EuskoMove/issues) &nbsp;·&nbsp;
[Reportar Bug](https://github.com/unaiabasolo1/EuskoMove/issues/new)

</div>

---

## Tabla de Contenidos

- [Tecnologías](#tecnologías)
- [Recursos desplegados](#recursos-desplegados)
- [Estructura](#estructura)
- [CI/CD con GitHub Actions](#cicd-con-github-actions)

---

## Tecnologías

| Herramienta | Uso |
|-------------|-----|
| **Terraform** | Aprovisionamiento de infraestructura (IaC) |
| **Azure App Service** | Hospedaje de la aplicación Flask |
| **Azure Database for PostgreSQL** | Base de datos relacional |
| **Azure Key Vault** | Gestión de secretos (RBAC) |
| **Azure Application Insights** | Monitorización y logs |
| **Azure Log Analytics Workspace** | Centralización de logs |
| **GitHub Actions** | Pipeline de CI/CD |
| **OIDC** | Autenticación sin credenciales estáticas |

---

## Recursos desplegados

**Resource Group `euskomove-dev-rg`**
- App Service Plan (Linux, B1)
- App Service `euskomove-dev-uu0enx` — Flask + Gunicorn, Python 3.12
- Key Vault `euskomove-dev-kv-uu0enx` — secretos: `db-connection-string`, `flask-secret-key`, `db-password`
- Azure Database for PostgreSQL `euskomove-dev-psql` — v16, base de datos `euskomovedb`
- Log Analytics Workspace `euskomove-logs`
- Application Insights `ai-euskomove`

**Resource Group `euskomove-tfstate-rg`**
- Storage Account `euskomovtfstate` — estado remoto de Terraform
- Managed Identity `euskomove-github-mi` — autenticación OIDC para GitHub Actions

---

## Estructura

```
infra/
├── main.tf                   # Recursos principales (App Service, Key Vault, PostgreSQL)
├── variables.tf              # Variables configurables
├── outputs.tf                # Outputs (URL, nombre de la Web App, etc.)
├── providers.tf              # Provider de Azure y versiones
├── terraform.tfvars          # Valores de las variables
└── modules/
    └── monitoring/
        └── main.tf           # Log Analytics Workspace + Application Insights
```

---

## CI/CD con GitHub Actions

El workflow `terraform-deploy` automatiza el despliegue completo. Usa **OIDC** para autenticarse con Azure sin almacenar credenciales en los secrets del repositorio.

| Acción | Resultado |
|--------|-----------|
| `plan` | Muestra los cambios que se aplicarían sin tocar nada |
| `apply` | Despliega la infraestructura y el código de la app |
| `destroy` | Elimina todos los recursos de Azure |

Para lanzarlo: GitHub → **Actions** → `terraform-deploy` → **Run workflow**

La app queda disponible en: [https://euskomove-dev-uu0enx.azurewebsites.net](https://euskomove-dev-uu0enx.azurewebsites.net)

---

<div align="center">

Hecho por [unaiabasolo1](https://github.com/unaiabasolo1)

</div>
