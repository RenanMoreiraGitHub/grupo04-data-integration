resource "aws_iot_thing" "thing" {
  name = "thing_soybean"
}

output "thing_name" {
  value = aws_iot_thing.thing.name
}

resource "tls_private_key" "key" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

resource "tls_self_signed_cert" "cert" {
  private_key_pem = tls_private_key.key.private_key_pem

  validity_period_hours = 240

  allowed_uses = [
  ]

  subject {
    organization = "test"
  }
}

resource "aws_iot_certificate" "cert" {
  active = true
}

resource "aws_iot_thing_principal_attachment" "attachment" {
  principal = aws_iot_certificate.cert.arn
  thing     = aws_iot_thing.thing.name
}

output "cert" {
  value = tls_self_signed_cert.cert.cert_pem
}

output "key" {
  value     = tls_private_key.key.private_key_pem
  sensitive = true
}


data "aws_arn" "thing" {
  arn = aws_iot_thing.thing.arn
}
resource "aws_iot_policy" "policy" {
  name = "thingpolicy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "*",
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

resource "aws_iot_policy_attachment" "attachment" {
  policy = aws_iot_policy.policy.name
  target = aws_iot_certificate.cert.arn
}

data "aws_iot_endpoint" "iot_endpoint" {
  endpoint_type = "iot:Data-ATS"
}

output "iot_endpoint" {
  value = data.aws_iot_endpoint.iot_endpoint.endpoint_address
}

data "http" "root_ca" {
  url = "https://www.amazontrust.com/repository/AmazonRootCA1.pem"
}

output "ca" {
  value = data.http.root_ca.response_body
}