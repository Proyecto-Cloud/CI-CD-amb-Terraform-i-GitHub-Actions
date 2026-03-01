# CI/CD con Terraform y GitHub Actions

Este proyecto implementa un pipeline **CI/CD automatizado** para desplegar infraestructura en **AWS** utilizando **Terraform** y **GitHub Actions**, siguiendo buenas prácticas de trabajo en equipo

## Objetivo

Automatizar la validación, revisión y despliegue de infraestructura mediante Pull Requests, evitando cambios manuales y errores en producción.

## Tecnologías Utilizadas

- **Terraform** (v1.14.5): Infraestructura como código
- **GitHub Actions**: Orquestación del pipeline CI/CD
- **AWS EKS**: Cluster de Kubernetes gestionado
- **AWS S3 + DynamoDB**: Backend remoto para estado de Terraform


## Estructura del Proyecto

```
├── .github/workflows/
│   └── terraform.yml          # Pipeline CI/CD
├── terraform/
│   ├── main.tf               # Recursos AWS principales
│   ├── variables.tf          # Variables de entrada
│   ├── providers.tf          # Configuración provider AWS
│   ├── backend.tf            # Configuración backend remoto
│   └── output.tf             # Salidas de la infraestructura
├── bootstrap/
│   └── main.tf               # Creación inicial de backend
└── README.md                 # Este archivo
```

## Flujo de Trabajo

1. Cada cambio se realiza en una **rama feature**
2. Al abrir una **Pull Request** hacia `main`:
   - Se ejecuta el CI (`fmt`, `validate`, `plan`)
   - El resultado del `terraform plan` se comenta automáticamente en la PR
3. Después de la aprobación, al hacer **merge a `main`**:
   - Se ejecuta el CD (`terraform apply`) automáticamente
4. El estado de Terraform se guarda en un **backend remoto (S3 + DynamoDB)**

## Infraestructura Desplegada

El proyecto crea la siguiente infraestructura en AWS:

- **VPC** con CIDR `10.0.0.0/16`
- **Subnets públicas y privadas** en 2 Availability Zones
- **Internet Gateway** y **NAT Gateway** para conectividad
- **EKS Cluster** llamado `democluster` 
- **Node Group** con 2 instancias `t3.medium`
- **Security Groups** para el control plane de EKS

## Cómo Probarlo

### Prerrequisitos

- Cuenta AWS con permisos adecuados
- Terraform instalado localmente (opcional, para pruebas)
- Git y GitHub configurados
- Roles IAM preexistentes: `LabEksClusterRole` y `LabEksNodeRole` 

### Configuración Inicial

1. **Crear backend remoto** (ejecutar una vez):
   ```bash
   cd bootstrap
   terraform init
   terraform apply
   ```
   Esto crea el bucket S3 y tabla DynamoDB para el estado.

2. **Configurar secrets en GitHub**:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY` 
   - `AWS_SESSION_TOKEN`

### Probar el Pipeline

1. **Crear una rama feature**:
   ```bash
   git checkout -b feature/test
   ```

2. **Hacer cambios** en la configuración de Terraform

3. **Abrir Pull Request** hacia `main`:
   - GitHub Actions ejecutará automáticamente `terraform plan`
   - El resultado se publicará como comentario en la PR

4. **Revisar el plan** y hacer merge si es correcto:
   - Al hacer merge, se ejecutará `terraform apply` automáticamente

### Pruebas Locales (Opcional)

Para probar cambios localmente antes de crear la PR:

```bash
cd terraform
terraform init
terraform plan
terraform apply  # Solo si estás seguro
```

