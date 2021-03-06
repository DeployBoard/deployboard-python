terraform {
  backend "s3" {}
}

variable "pr" {
  description = "GitHub Pull Request Number."
  type = string
}

module "ci" {
  source = "git@github.com:DeployBoard/terraform-infrastructure//ci"
  env = "ci"
  pr = var.pr
}
