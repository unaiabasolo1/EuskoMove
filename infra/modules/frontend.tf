variable "resource_group_name" {}
variable "location" {}

resource "azurerm_static_site" "frontend" {
  name                = "web-euskomove"
  resource_group_name = var.resource_group_name
  location            = var.location
  sku_tier            = "Free"
  sku_size            = "Free"
}

output "url" {
  value = "https://${azurerm_static_site.frontend.default_host_name}"
}
