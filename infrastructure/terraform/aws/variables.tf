variable "aws_region" {
  default = "us-east-1"
}

variable "env" {
  default = "prod"
}

variable "db_password" {
  sensitive = true
}
