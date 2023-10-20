variable "project_name" {
  type        = string
  description = "Default project name"
}

variable "environment" {
  type        = string
  description = "Default environment project"
}

variable "tags" {
  type        = map(string)
  description = "Default tags"
}

variable "cidr_block_vpc" {
  type        = string
  description = "Default cidr_block_vpc"
}

variable "public_subnet_cidrs" {
  type        = list(string)
  description = "Public Subnet CIDR values"
}

variable "private_subnet_cidrs" {
  type        = list(string)
  description = "Private Subnet CIDR values"
}

variable "azs" {
  type        = list(string)
  description = "Availability Zones"
}

variable "cidr_block_all_public" {
  type        = string
  description = "Default cidr_block_all_public"
}

variable "lambdas_names" {
  type        = list(string)
  description = "Names of lambdas"
}

variable "role_for_lambda" {
  type        = string
  description = "Default role for lambda"
}

variable "runtime" {
  type        = string
  description = "Default runtime for lambda"
}

variable "layer_arn" {
  type        = string
  description = "Default layer for lambda"
}

variable "buckets_names" {
  type        = list(string)
  description = "Names of buckets"
}

variable "username_db_instance" {
  type        = string
  description = "Username of database instance"
}

variable "password_db_instance" {
  type        = string
  description = "Password of database instance"
}

variable "db_subnet_group_name" {
  type        = list(string)
  description = "Name of database subnet group"
}