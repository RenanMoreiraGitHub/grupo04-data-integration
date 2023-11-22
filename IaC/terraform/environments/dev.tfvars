environment = "dev"

project_name = "soybean"

cidr_block_vpc = "10.0.0.0/16"

public_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]

private_subnet_cidrs = ["10.0.3.0/24", "10.0.4.0/24"]

azs = ["us-east-1a", "us-east-1b"]

cidr_block_all_public = "0.0.0.0/0"


lambdas_names = ["raw_to_staged", "staged_to_consumed"]

role_for_lambda = "arn:aws:iam::479480645395:role/LabRole"

layer_arn = "arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python39:2"

runtime = "python3.9"

buckets_names = ["raw-soybean-bucket", "staged-soybean-bucket", "consumed-soybean-bucket"]

username_db_instance = "soybean"

password_db_instance = "soybean123"

db_subnet_group_name = ["Public Subnet 1", "Public Subnet 2"]

tags = {
  Name = "soybean-dev"
}

