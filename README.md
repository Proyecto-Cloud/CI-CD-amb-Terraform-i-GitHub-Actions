<<<<<<< HEAD
# 🚀 CI/CD amb Terraform i GitHub Actions

[![Terraform CI/CD](https://github.com/Proyecto-Cloud/CI-CD-amb-Terraform-i-GitHub-Actions/actions/workflows/terraform.yml/badge.svg)](https://github.com/Proyecto-Cloud/CI-CD-amb-Terraform-i-GitHub-Actions/actions/workflows/terraform.yml)
[![App CI/CD](https://github.com/Proyecto-Cloud/CI-CD-amb-Terraform-i-GitHub-Actions/actions/workflows/deploy-app.yml/badge.svg)](https://github.com/Proyecto-Cloud/CI-CD-amb-Terraform-i-GitHub-Actions/actions/workflows/deploy-app.yml)

Aquest projecte implementa un flux **CI/CD complet i desacoblat** per desplegar infraestructura a **AWS** utilitzant **Terraform** i una aplicació de demostració en **Kubernetes (EKS)**, tot governat automàticament mitjançant **GitHub Actions** i seguint bones pràctiques de treball en equip.

---

## 🎯 Objectiu
Automatitzar la validació, revisió i desplegament, tant de la infraestructura com del programari, mitjançant Pull Requests. D'aquesta manera s'eviten canvis manuals directes i errors en producció, assegurant un entorn robust, traçable i reproduïble.

---

## 🏗️ Arquitectura del Projecte

El repositori està dividit lògicament en dues parts independents, cadascuna amb el seu propi cicle de vida:

### 1. Infraestructura com a Codi (Terraform)
Desplega tota la base necessària a AWS per suportar l'aplicació:
- **Xarxa**: VPC, Subnets Públiques/Privades, Internet Gateway i NAT Gateway.
- **Còmput**: Clúster d'Amazon EKS (`democluster`) amb un Node Group de màquines `t3.medium`.
- **Seguretat**: Security Groups per al *Control Plane* de Kubernetes i comunicació node-pod.

### 2. Aplicació de Demostració (`demo-app/`)
Una aplicació web didàctica programada en **Python (Flask)**:
- Genera una interfície visual (Glassmorphism) que depèn del nom del pod on s'està executant.
- S'empaqueta en **Docker** i s'escala a 3 rèpliques a EKS.
- Exposada mitjançant un manifest de `Service` de tipus LoadBalancer que crea automàticament un **Network Load Balancer (NLB)** d'AWS per evidenciar el balanceig de càrrega visualment.

---

## 🔄 Flux de treball (CI/CD)

El projecte utilitza l'estratègia *GitHub Flow*. Hi ha dos pipelines separats per evitar que els canvis a la web afectin la infraestructura i viceversa:

### 📁 Terraform Pipeline (`.github/workflows/terraform.yml`)
1. Cada canvi en la infraestructura es fa en una **branca feature**.
2. En obrir una **Pull Request** cap a `main`:
   - S’executa el CI: `terraform fmt`, `terraform validate` i `terraform plan`.
   - El resultat del `terraform plan` es comenta automàticament a la PR gràcies a l'Action `github-script`.
3. Després de l’aprovació verbal/tècnica, en fer **merge a `main`**:
   - S’executa el CD: `terraform apply -auto-approve` de forma automàtica.
4. L’estat de Terraform es guarda en un **backend remot (S3 + DynamoDB)** per garantir el bloqueig (*State Locking*) i poder col·laborar en equip.

### 📁 App Pipeline (`.github/workflows/deploy-app.yml`)
- Aquest pipeline només s'executa si es modifiquen fitxers dins la carpeta `demo-app/`.
- En fer merge cap a `main`, el pipeline **construeix la imatge Docker**, puja la nova versió a **Docker Hub**, autèntica el clúster d'EKS i aplica els manifests amb `kubectl` automàticament.

---

## 🛠️ Com llançar una Demo Ràpida?

Si la infraestructura de Terraform ja està desplegada en el teu entorn (amb `terraform apply`), pots forçar el desplegament manual de la Demo App localment utilitzant l'script automatitzat:

```bash
chmod +x deploy_demo.sh
./deploy_demo.sh
```
L'script connectarà amb el teu clúster EKS, desplegarà els recursos de Kubernetes, es quedarà a l'espera i t'imprimirà per pantalla la URL final de balancejador d'AWS un cop estigui creat.

---

## 📋 Requisits
Per replicar o treballar amb aquest repositori, necessitaràs:
- **Compte AWS** actiu.
- Bucket **S3** (i taula DynamoDB, opcional) per emmagatzemar el *backend* de Terraform.
- **Secrets d’AWS configurats a GitHub Actions**:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_SESSION_TOKEN` (si fas servir comptes de laboratori educatiu)
- **Secrets de Docker configurats a GitHub Actions**:
  - `DOCKERHUB_USERNAME`
  - `DOCKERHUB_TOKEN`
- **Terraform** instal·lat (per a l'execució i proves locals).

---

## ⚠️ Notes Importants
- La branca `main` està **protegida** contra escriptura.
- **No es permeten pushes directes** sota cap concepte; tot desplegament a producció passa obligatòriament per una Pull Request.

---

### Autors
Projecte realitzat com a pràctica tècnica de CI/CD amb Terraform, EKS i GitHub Actions.
\n## ⚙️ Backend Setup (Para nuevos laboratorios AWS)\n\nSi utilitzes comptes d'estudiant d'AWS Academy (o les teves credencials canvien a sovint), executar aquest script et crearà automàticament un **Bucket de S3 únic** basat en el teu Account ID i una taula **DynamoDB** per al *State Locking*. Finalment sobreescriurà el fitxer `backend.tf` de Terraform i el migrarà automàticament.\n\n```bash\nchmod +x setup_backend.sh\n./setup_backend.sh\n```\n
=======
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

>>>>>>> origin/main
