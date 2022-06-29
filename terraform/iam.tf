data "aws_caller_identity" "current" {}

resource "aws_iam_role" "user_role" {
  name = "${var.app}-${var.env}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid = ""
        Principal = {
          AWS = data.aws_caller_identity.current.arn
        }
      }
    ]
  })
}

# Policies go here
# ...