resource "aws_db_subnet_group" "default" {
  name       = "main"
  subnet_ids = [aws_subnet.public_subnets[0].id, aws_subnet.public_subnets[1].id]
  tags = {
    Name = "My DB subnet group"
  }
}

resource "aws_db_instance" "default" {
  allocated_storage    = 10
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t2.micro"
  username             = var.username_db_instance
  password             = var.password_db_instance
  parameter_group_name = "default.mysql8.0"
  skip_final_snapshot  = true
  db_subnet_group_name = aws_db_subnet_group.default.name
  availability_zone    = "us-east-1a"
  publicly_accessible  = true

  tags = {
    Name : "soybean-db-instance"
  }
}