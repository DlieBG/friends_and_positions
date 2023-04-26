resource "azurerm_cosmosdb_account" "cosmosdb_account" {
    name                = "${var.project}ca"
    location            = azurerm_resource_group.resource_group.location
    resource_group_name = azurerm_resource_group.resource_group.name

    offer_type          = "Standard"
    kind                = "MongoDB"

    capabilities {
        name = "EnableMongo"
    }

    capabilities {
        name = "EnableServerless"
    }

    consistency_policy {
        consistency_level       = "BoundedStaleness"
        max_interval_in_seconds = 300
        max_staleness_prefix    = 100000
    }

    geo_location {
        location          = var.cosmosdb_location
        failover_priority = 0
    }
}
