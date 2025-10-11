provider "aws" {
  region = "us-east-1"
}


resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = { Name = "ecommerce-vpc" }
}


resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  tags = { Name = "ecommerce-subnet" }
}

resource "aws_internet_gateway" "ecommerce-igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "ecommerce-igw"
  }
}


resource "aws_route_table" "public-rt" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.ecommerce-igw.id
  }

  tags = {
    Name = "ecommerce-public-rt"
  }
}


resource "aws_route_table_association" "public_assoc" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public-rt.id
}


resource "aws_security_group" "allow_http_ssh" {
  vpc_id = aws_vpc.main.id

  ingress {
    description = "Allow HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}



resource "aws_instance" "ecommerce_server" {
  ami           = "ami-052064a798f08f0d3"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.public.id   
  key_name      = "ecommerce-key"
  vpc_security_group_ids = [aws_security_group.allow_http_ssh.id]

  tags = { Name = "ecommerce-app-server" }
}


