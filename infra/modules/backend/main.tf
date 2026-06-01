variable "resource_group_name" {}
variable "location" {}
variable "db_host" {}
variable "storage_account" {}
variable "storage_key" { sensitive = true }

resource "azurerm_service_plan" "plan" {
  name                = "plan-euskomove"
  resource_group_name = var.resource_group_name
  location            = var.location
  os_type             = "Linux"
  sku_name            = "F1"
}

resource "azurerm_linux_web_app" "api" {
  name                = "api-euskomove-001"
  resource_group_name = var.resource_group_name
  location            = var.location
  service_plan_id     = azurerm_service_plan.plan.id
  https_only          = true

  site_config {
    always_on = false
    application_stack {
      python_version = "3.11"
    }
  }

  app_settings = {
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "true"
    "DB_HOST"                        = var.db_host
    "DB_NAME"                        = "euskomove"
    "DB_SSL"                         = "true"
    "STORAGE_ACCOUNT_NAME"           = var.storage_account
    "AZURE_STORAGE_KEY"              = var.storage_key
  }
}

output "api_url" {
  value = "https://${azurerm_linux_web_app.api.default_hostname}"
}
