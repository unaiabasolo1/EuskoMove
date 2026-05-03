variable "project_name" {
  description = "Short name used as a prefix for all Azure resources."
  type        = string
  default     = "euskomove"

  validation {
    condition     = can(regex("^[a-z0-9]{3,18}$", var.project_name))
    error_message = "project_name must be 3-18 chars, lowercase letters and digits only."
  }
}

variable "environment" {
  description = "Environment name (dev, staging, prod). Used in resource naming and tags."
  type        = string
  default     = "dev"
}

variable "location" {
  description = "Azure region for all resources."
  type        = string
  default     = "spaincentral"
}

variable "resource_group_name" {
  description = "Name of the resource group. Defaults to <project>-<env>-rg."
  type        = string
  default     = null
}

variable "app_service_plan_sku" {
  description = "App Service Plan SKU. B1 is the cheapest dedicated Linux tier suitable for Flask."
  type        = string
  default     = "B1"
}

variable "python_version" {
  description = "Python runtime version on App Service Linux."
  type        = string
  default     = "3.12"
}

variable "startup_command" {
  description = "Startup command for the Flask app. Override if your entrypoint differs."
  type        = string
  default     = "gunicorn --bind=0.0.0.0:8000 --timeout 600 app:app"
}

variable "https_only" {
  description = "Force HTTPS on the web app."
  type        = bool
  default     = true
}

variable "app_settings" {
  description = "Additional app settings injected into the Web App. Do not put secrets here in plain text — use Key Vault references."
  type        = map(string)
  default     = {}
}

variable "tags" {
  description = "Tags applied to every resource."
  type        = map(string)
  default = {
    project   = "EuskoMove"
    managedBy = "terraform"
  }
}
