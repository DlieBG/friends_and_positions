output "function_app_hostname" {
    value       = azurerm_linux_function_app.function_app.default_hostname
    description = "Deployed function app hostname"
}
