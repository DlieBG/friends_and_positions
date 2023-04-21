resource "azurerm_storage_account" "storage_account" {
    name                        = "${var.project}sa"
    location                    = azurerm_resource_group.resource_group.location
    resource_group_name         = azurerm_resource_group.resource_group.name
    account_tier                = "Standard"
    account_replication_type    = "LRS"
}

resource "azurerm_app_service_plan" "app_service_plan" {
    name                = "${var.project}asp"
    location            = azurerm_resource_group.resource_group.location
    resource_group_name = azurerm_resource_group.resource_group.name
    kind                = "Linux"
    reserved            = true

    sku {
        tier = "Dynamic"
        size = "Y1"
    }

    lifecycle {
        ignore_changes = [
            kind
        ]
    }
}

resource "azurerm_function_app" "function_app" {
    name                        = "${var.project}fa"
    location                    = azurerm_resource_group.resource_group.location
    resource_group_name         = azurerm_resource_group.resource_group.name
    app_service_plan_id         = azurerm_app_service_plan.app_service_plan.id
    storage_account_name        = azurerm_storage_account.storage_account.name
    storage_account_access_key  = azurerm_storage_account.storage_account.primary_access_key
    os_type                     = "linux"
    version                     = "~4"

    app_settings = {
        FUNCTIONS_WORKER_RUNTIME = "python"
        MONGO_URI = azurerm_cosmosdb_account.cosmosdb_account.connection_strings[0]
    }

    site_config {
        linux_fx_version = "python|3.10"
    }
}
