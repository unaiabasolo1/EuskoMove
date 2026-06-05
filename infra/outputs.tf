output "resource_group_name" {
  description = "Name of the created resource group."
  value       = azurerm_resource_group.this.name
}

output "web_app_name" {
  description = "Name of the Linux web app. Use this in the GitHub Actions deploy step."
  value       = azurerm_linux_web_app.this.name
}

output "web_app_default_hostname" {
  description = "Default hostname of the deployed Flask app."
  value       = azurerm_linux_web_app.this.default_hostname
}

output "web_app_url" {
  description = "Full HTTPS URL where the app is reachable."
  value       = "https://${azurerm_linux_web_app.this.default_hostname}"
}

output "service_plan_id" {
  description = "ID of the App Service Plan."
  value       = azurerm_service_plan.this.id
}

output "principal_id" {
  description = "System-assigned managed identity principal ID. Use for Key Vault / DB role assignments."
  value       = azurerm_linux_web_app.this.identity[0].principal_id
}

output "key_vault_name" {
  value = azurerm_key_vault.this.name
}

output "postgresql_fqdn" {
  value = azurerm_postgresql_flexible_server.this.fqdn
}

output "application_insights_connection_string" {
  description = "Connection string de Application Insights. Inyectada automáticamente en la Web App."
  value       = module.monitoring.connection_string
  sensitive   = true
}

output "log_analytics_workspace_name" {
  description = "Nombre del Log Analytics Workspace donde se centralizan los logs."
  value       = "law-euskomove"
}