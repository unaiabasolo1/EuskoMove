terraform {
  required_version = ">= 1.5.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }

  # Optional: store remote state in an Azure Storage Account.
  # Uncomment and configure if you want shared state.
  #
  # backend "azurerm" {
  #   resource_group_name  = "tfstate-rg"
  #   storage_account_name = "tfstateeuskomove"
  #   container_name       = "tfstate"
  #   key                  = "euskomove.tfstate"
  # }
}

provider "azurerm" {
  features {}
}

provider "random" {}
