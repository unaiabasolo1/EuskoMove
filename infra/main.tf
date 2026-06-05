locals {
  name_prefix = "${var.project_name}-${var.environment}"
  rg_name     = coalesce(var.resource_group_name, "${local.name_prefix}-rg")

  common_tags = merge(
    var.tags,
    {
      environment = var.environment
    },
  )
}

# ─── Sufijo fijo para nombres globalmente únicos (Key Vault, Web App) ───
locals {
  suffix = "uu0enx"
}

resource "azurerm_resource_group" "this" {
  name     = local.rg_name
  location = var.location
  tags     = local.common_tags
}

# ─── Monitoring: Log Analytics + Application Insights ─────────────────

module "monitoring" {
  source              = "./modules/monitoring"
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
}

# ─────────────────────────────────────────────────────────────────────────────

resource "azurerm_service_plan" "this" {
  name                = "${local.name_prefix}-plan"
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  os_type             = "Linux"
  sku_name            = var.app_service_plan_sku
  tags                = local.common_tags
}

resource "azurerm_linux_web_app" "this" {
  name                = "${local.name_prefix}-${local.suffix}"
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  service_plan_id     = azurerm_service_plan.this.id
  https_only          = var.https_only
  tags                = local.common_tags

  site_config {
    always_on           = var.app_service_plan_sku != "F1" && var.app_service_plan_sku != "D1"
    ftps_state          = "Disabled"
    http2_enabled       = true
    minimum_tls_version = "1.2"

    application_stack {
      python_version = var.python_version
    }

    app_command_line = var.startup_command
  }

  app_settings = merge(
    {
      SCM_DO_BUILD_DURING_DEPLOYMENT = "true"
      ENABLE_ORYX_BUILD              = "true"
      FLASK_ENV                      = var.environment == "prod" ? "production" : "development"
      PYTHONUNBUFFERED               = "1"
      WEBSITES_PORT                  = "8000"
      DATABASE_URL                   = "@Microsoft.KeyVault(VaultName=${azurerm_key_vault.this.name};SecretName=db-connection-string)"
      # ─── Secreto de Flask añadido desde Key Vault ───
      FLASK_SECRET_KEY               = "@Microsoft.KeyVault(VaultName=${azurerm_key_vault.this.name};SecretName=flask-secret-key)"
      # ─── Azure Monitor / Application Insights ─────────────────────
      APPLICATIONINSIGHTS_CONNECTION_STRING = module.monitoring.connection_string
    },
    var.app_settings,
  )

  identity {
    type = "SystemAssigned"
  }

  logs {
    http_logs {
      file_system {
        retention_in_days = 7
        retention_in_mb   = 35
      }
    }
    application_logs {
      file_system_level = "Information"
    }
  }

  lifecycle {
    ignore_changes = [
      app_settings["WEBSITE_RUN_FROM_PACKAGE"],
    ]
  }

  depends_on = [
    azurerm_key_vault.this,
    azurerm_key_vault_secret.flask_secret_key,
    azurerm_key_vault_secret.db_connection_string
  ]
}

# ─── Key Vault ────────────────────────────────────────────────────────────────

data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "this" {
  name                       = "${var.project_name}-${var.environment}-kv-${local.suffix}"
  location                   = azurerm_resource_group.this.location
  resource_group_name        = azurerm_resource_group.this.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  soft_delete_retention_days = 7
  purge_protection_enabled   = false
  enable_rbac_authorization  = true
  tags                       = local.common_tags

  lifecycle {
    ignore_changes = [soft_delete_retention_days]
  }
}

# ─── Espera para que la asignación de rol RBAC se propague antes de crear secretos ───
resource "time_sleep" "wait_for_rbac" {
  depends_on      = [azurerm_role_assignment.kv_terraform]
  create_duration = "60s"
}

resource "azurerm_role_assignment" "kv_terraform" {
  scope                = azurerm_key_vault.this.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = data.azurerm_client_config.current.object_id
}

# ─── 3c) Contraseña fija desde variable ──────────────────────────────────────

resource "azurerm_key_vault_secret" "db_password" {
  name         = "db-password"
  value        = var.db_password
  key_vault_id = azurerm_key_vault.this.id
  depends_on   = [time_sleep.wait_for_rbac]
}

resource "azurerm_key_vault_secret" "db_connection_string" {
  name         = "db-connection-string"
  value        = "postgresql://${var.db_admin_username}:${var.db_password}@${azurerm_postgresql_flexible_server.this.fqdn}:5432/${var.db_name}?sslmode=require"
  key_vault_id = azurerm_key_vault.this.id
  depends_on   = [time_sleep.wait_for_rbac]
}

# ─── Secreto para FLASK_SECRET_KEY en Key Vault ───────────────────────────────

resource "azurerm_key_vault_secret" "flask_secret_key" {
  name         = "flask-secret-key"
  value        = "euskomove-secret-2025-eus"
  key_vault_id = azurerm_key_vault.this.id
  depends_on   = [time_sleep.wait_for_rbac]
}

# ─── PostgreSQL ───────────────────────────────────────────────────────────────

resource "azurerm_postgresql_flexible_server" "this" {
  name                   = "${local.name_prefix}-psql"
  resource_group_name    = azurerm_resource_group.this.name
  location               = azurerm_resource_group.this.location
  version                = "16"
  administrator_login    = var.db_admin_username
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = var.db_sku
  backup_retention_days  = 7
  tags                   = local.common_tags

  authentication {
    active_directory_auth_enabled = false
    password_auth_enabled         = true
  }

  lifecycle {
    ignore_changes = [zone, high_availability]
  }
}

resource "azurerm_postgresql_flexible_server_database" "this" {
  name      = var.db_name
  server_id = azurerm_postgresql_flexible_server.this.id
  collation = "en_US.utf8"
  charset   = "utf8"
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "azure_services" {
  name             = "allow-azure-services"
  server_id        = azurerm_postgresql_flexible_server.this.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

# ─── Permiso para que la Web App lea secretos del Key Vault ──────────────────

resource "azurerm_role_assignment" "kv_webapp" {
  scope                = azurerm_key_vault.this.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_linux_web_app.this.identity[0].principal_id
}