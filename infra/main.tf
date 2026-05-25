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

resource "random_string" "suffix" {
  length  = 6
  upper   = false
  special = false
  numeric = true
}

resource "azurerm_resource_group" "this" {
  name     = local.rg_name
  location = var.location
  tags     = local.common_tags
}

resource "azurerm_service_plan" "this" {
  name                = "${local.name_prefix}-plan"
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  os_type             = "Linux"
  sku_name            = var.app_service_plan_sku
  tags                = local.common_tags
}

resource "azurerm_linux_web_app" "this" {
  name                = "${local.name_prefix}-${random_string.suffix.result}"
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
}

# ─── Contraseña aleatoria para la BD ─────────────────────────────────────────

resource "random_password" "db_password" {
  length           = 24
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

# ─── Key Vault ────────────────────────────────────────────────────────────────

data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "this" {
  name                       = "${var.project_name}-${var.environment}-kv"
  location                   = azurerm_resource_group.this.location
  resource_group_name        = azurerm_resource_group.this.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  soft_delete_retention_days = 7
  purge_protection_enabled   = false
  tags                       = local.common_tags
}

resource "azurerm_role_assignment" "kv_terraform" {
  scope                = azurerm_key_vault.this.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = "927bb819-e8cd-4bf6-a766-80f4f25d3625"
}

resource "azurerm_key_vault_secret" "db_password" {
  name         = "db-password"
  value        = random_password.db_password.result
  key_vault_id = azurerm_key_vault.this.id
  depends_on   = [azurerm_role_assignment.kv_terraform]
}

resource "azurerm_key_vault_secret" "db_connection_string" {
  name         = "db-connection-string"
  value        = "postgresql://${var.db_admin_username}:${random_password.db_password.result}@${azurerm_postgresql_flexible_server.this.fqdn}:5432/${var.db_name}?sslmode=require"
  key_vault_id = azurerm_key_vault.this.id
  depends_on   = [azurerm_role_assignment.kv_terraform]
}

# ─── PostgreSQL ───────────────────────────────────────────────────────────────

resource "azurerm_postgresql_flexible_server" "this" {
  name                   = "${local.name_prefix}-psql"
  resource_group_name    = azurerm_resource_group.this.name
  location               = azurerm_resource_group.this.location
  version                = "16"
  administrator_login    = var.db_admin_username
  administrator_password = random_password.db_password.result
  storage_mb             = 32768
  sku_name               = var.db_sku
  backup_retention_days  = 7
  tags                   = local.common_tags

  authentication {
    active_directory_auth_enabled = false
    password_auth_enabled         = true
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