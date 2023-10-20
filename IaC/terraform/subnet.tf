resource "aws_subnet" "public_subnets" {
  count                                          = length(var.public_subnet_cidrs)
  vpc_id                                         = aws_vpc.main.id
  cidr_block                                     = element(var.public_subnet_cidrs, count.index)
  availability_zone                              = element(var.azs, count.index)
  enable_resource_name_dns_a_record_on_launch    = true
  map_public_ip_on_launch                        = true
  tags = {
    Name = "Public Subnet ${count.index + 1}"
  }
}

resource "aws_subnet" "private_subnets" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = element(var.private_subnet_cidrs, count.index)
  availability_zone = element(var.azs, count.index)

  tags = {
    Name = "Private Subnet ${count.index + 1}"
  }
}