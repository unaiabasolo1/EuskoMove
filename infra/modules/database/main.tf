variable "resource_group_name" {}
variable "location" {}
variable "db_password" { sensitive = true }

resource "azurerm_postgresql_flexible_server" "db" {
  name                   = "psql-euskomove"
  resource_group_name    = var.resource_group_name
  location               = var.location
  version                = "15"
  administrator_login    = "admineusko"
  administrator_password = var.db_password
  sku_name               = "B_Standard_B1ms"
  storage_mb             = 32768
  backup_retention_days  = 7
}

resource "azurerm_postgresql_flexible_server_database" "db" {
  name      = "euskomove"
  server_id = azurerm_postgresql_flexible_server.db.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

resource "azurerm_storage_account" "st" {
  name                     = "steuskomove001"
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  min_tls_version          = "TLS1_2"
}

resource "azurerm_storage_container" "billetes" {
  name                  = "billetes"
  storage_account_name  = azurerm_storage_account.st.name
  container_access_type = "private"
}

resource "azurerm_storage_queue" "reservas" {
  name                 = "cola-reservas"
  storage_account_name = azurerm_storage_account.st.name
}

output "db_host" {
  value = azurerm_postgresql_flexible_server.db.fqdn
}

output "storage_account_name" {
  value = azurerm_storage_account.st.name
}

output "storage_account_key" {
  value     = azurerm_storage_account.st.primary_access_key
  sensitive = true
}
