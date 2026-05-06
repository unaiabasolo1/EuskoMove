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

# Random suffix keeps the web app's globally-unique hostname unique
# across re-creates without forcing the user to pick a name.
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
      # Tell Oryx to install requirements.txt during deployment.
      SCM_DO_BUILD_DURING_DEPLOYMENT = "true"
      ENABLE_ORYX_BUILD              = "true"

      # Flask sane defaults. Override via var.app_settings if needed.
      FLASK_ENV        = var.environment == "prod" ? "production" : "development"
      PYTHONUNBUFFERED = "1"
      WEBSITES_PORT    = "8000"
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
      # The deploy workflow updates the running package; don't fight it.
      app_settings["WEBSITE_RUN_FROM_PACKAGE"],
    ]
  }
}
