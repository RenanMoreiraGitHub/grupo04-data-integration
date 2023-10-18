locals {
  tags = {
    Environment = var.environment
    Application = var.project_name
  }
}