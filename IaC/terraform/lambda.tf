data "archive_file" "code" {
  count       = length(var.lambdas_names)
  type        = "zip"
  source_file = "src/iot/${element(var.lambdas_names, count.index)}/${element(var.lambdas_names, count.index)}.py"
  output_path = "src/outputs/${element(var.lambdas_names, count.index)}_payload.zip"
}
data "archive_file" "layer" {
  count       = length(var.lambdas_names)
  type        = "zip"
  source_dir  = "src/iot/layer"
  output_path = "src/outputs/${element(var.lambdas_names, count.index)}_layer.zip"
}

resource "aws_lambda_layer_version" "this" {
  count                    = length(var.lambdas_names)
  filename                 = data.archive_file.layer[count.index].output_path
  layer_name               = "lambda_layer_name"
  source_code_hash         = data.archive_file.layer[count.index].output_base64sha256
  compatible_runtimes      = ["python3.9"]
  compatible_architectures = ["x86_64"]
}

resource "aws_lambda_function" "lambda" {
  count            = length(var.lambdas_names)
  function_name    = element(var.lambdas_names, count.index)
  role             = var.role_for_lambda
  handler          = "${element(var.lambdas_names, count.index)}.main"
  runtime          = var.runtime
  filename         = data.archive_file.code[count.index].output_path
  source_code_hash = data.archive_file.code[count.index].output_base64sha256
  memory_size      = 512
  timeout          = 180
  layers           = [var.layer_arn, aws_lambda_layer_version.this[count.index].arn]
  environment {
    variables = {
      USER_BD = "soybean"
      PASS_BD = "soybean123"
      HOST_BD = "terraform-20231020122938937900000001.cerbmnica18k.us-east-1.rds.amazonaws.com"
    }
  }
}

resource "aws_lambda_permission" "allow_bucket" {
  count         = length(var.lambdas_names)
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda[count.index].arn
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.bucket[count.index].arn
}