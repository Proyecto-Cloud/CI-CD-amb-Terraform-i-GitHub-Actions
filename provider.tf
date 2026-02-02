terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # CONFIGURACIÓN DEL BACKEND REMOTO
  backend "s3" {
    # 1. El nombre del bucket
    bucket         = "fila2-terraform-state-2026-project" 
    
    # 2. La ruta dentro del bucket donde se guardará el archivo
    key            = "global/s3/terraform.tfstate"
    
    # 3. Región y Tabla de bloqueo
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = "us-east-1"
}