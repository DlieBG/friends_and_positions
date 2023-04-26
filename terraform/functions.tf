resource "azurerm_storage_account" "storage_account" {
    name                        = "${var.project}sa"
    location                    = azurerm_resource_group.resource_group.location
    resource_group_name         = azurerm_resource_group.resource_group.name

    account_tier                = "Standard"
    account_replication_type    = "LRS"
}

resource "azurerm_service_plan" "service_plan" {
    name                = "${var.project}sp"
    location            = azurerm_resource_group.resource_group.location
    resource_group_name = azurerm_resource_group.resource_group.name

    os_type             = "Linux"
    sku_name            = "Y1"
}

data "archive_file" "zip" {
    type = "zip"
    source_dir = "../functions"
    output_path = "functions.zip"
}

resource "azurerm_linux_function_app" "function_app" {
    name                        = "${var.project}fa"
    location                    = azurerm_resource_group.resource_group.location
    resource_group_name         = azurerm_resource_group.resource_group.name
    
    storage_account_name        = azurerm_storage_account.storage_account.name
    storage_account_access_key  = azurerm_storage_account.storage_account.primary_access_key
    service_plan_id             = azurerm_service_plan.service_plan.id

    app_settings = {
        ENABLE_ORYX_BUILD              = true
        SCM_DO_BUILD_DURING_DEPLOYMENT  = true 
        MONGO_URI                       = azurerm_cosmosdb_account.cosmosdb_account.connection_strings[0]
    }

    site_config {
        application_stack {
            python_version = "3.9"
        }
    }

    zip_deploy_file = data.archive_file.zip.output_path
}
