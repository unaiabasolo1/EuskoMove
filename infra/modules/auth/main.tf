variable "resource_group_name" {}
variable "location" {}

data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "kv" {
  name                = "kv-euskomove-001"
  location            = var.location
  resource_group_name = var.resource_group_name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"

  access_policy {
    tenant_id          = data.azurerm_client_config.current.tenant_id
    object_id          = data.azurerm_client_config.current.object_id
    secret_permissions = ["Get", "Set", "List", "Delete"]
  }
}

output "key_vault_id" {
  value = azurerm_key_vault.kv.id
}
