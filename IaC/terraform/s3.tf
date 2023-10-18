resource "aws_s3_bucket" "bucket" {
  count  = length(var.buckets_names)
  bucket = element(var.buckets_names, count.index)

  tags = {
    Environment = var.environment
  }
}

resource "aws_s3_bucket_notification" "aws-lambda-trigger" {
  count  = length(var.lambdas_names)
  bucket = aws_s3_bucket.bucket[count.index].id
  lambda_function {
    lambda_function_arn = aws_lambda_function.lambda[count.index].arn
    events              = ["s3:ObjectCreated:*"]
  }
}