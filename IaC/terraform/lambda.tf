data "archive_file" "lambda" {
  count       = length(var.lambdas_names)
  type        = "zip"
  source_file = "src/${element(var.lambdas_names, count.index)}.py"
  output_path = "src/${element(var.lambdas_names, count.index)}_payload.zip"
}

resource "aws_lambda_function" "lambda" {
  count            = length(var.lambdas_names)
  function_name    = element(var.lambdas_names, count.index)
  role             = var.role_for_lambda
  handler          = "${element(var.lambdas_names, count.index)}.main"
  runtime          = var.runtime
  filename         = data.archive_file.lambda[count.index].output_path
  source_code_hash = data.archive_file.lambda[count.index].output_base64sha256
  memory_size      = 512
  timeout          = 180
  layers           = [var.layer_arn]

}

resource "aws_lambda_permission" "allow_bucket" {
  count         = length(var.lambdas_names)
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda[count.index].arn
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.bucket[count.index].arn
}