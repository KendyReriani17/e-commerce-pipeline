<div align="center">

# 🚀 Tech Stack

![Flask](https://img.shields.io/badge/Flask-Python-blue?style=for-the-badge&logo=flask)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?style=for-the-badge&logo=docker)
![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?style=for-the-badge&logo=terraform)
![AWS](https://img.shields.io/badge/AWS-EC2-orange?style=for-the-badge&logo=amazon-aws)
![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?style=for-the-badge&logo=jenkins)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-E6522C?style=for-the-badge&logo=prometheus)
![Grafana](https://img.shields.io/badge/Grafana-Dashboard-F46800?style=for-the-badge&logo=grafana)
![Git](https://img.shields.io/badge/Git-Version_Control-F05032?style=for-the-badge&logo=git)
![GitHub](https://img.shields.io/badge/GitHub-Repo-181717?style=for-the-badge&logo=github)

</div>

# MyBasket – E-Commerce DevOps Pipeline  

## Overview  
MyBasket is a containerized **e-commerce web application** built with **Flask**, integrated with a full **DevOps pipeline** for automated infrastructure provisioning, CI/CD, and monitoring.  

The project demonstrates modern DevOps practices — from **Infrastructure as Code (IaC)** with Terraform to **continuous integration** using Jenkins and **real-time monitoring** with Prometheus and Grafana.  

---

##  Tech Stack  

| Category | Tools Used |
|-----------|-------------|
| **App Framework** | Flask (Python) |
| **Containerization** | Docker |
| **Infrastructure as Code** | Terraform (AWS EC2, VPC, Security Groups, Subnets) |
| **CI/CD** | Jenkins |
| **Monitoring** | Prometheus, Grafana |
| **Version Control** | Git & GitHub |
| **Cloud Provider** | AWS (EC2) |

---

---

## Project Workflow  

### 1️. Infrastructure Setup (Terraform + AWS)
- Terraform provisions:
  - VPC, Subnet, Internet Gateway  
  - Security Group (HTTP & SSH access)
  - EC2 Instance  
- Ensures a **reproducible**, **secure** and **scalable** cloud environment.  

### 2️. Application Containerization (Docker)  
- Flask app is containerized using a **Dockerfile**.  
- `.dockerignore` excludes sensitive/unnecessary files.  
- Docker Compose supports local setup of app + monitoring stack.  

### 3️. Continuous Integration & Deployment (Jenkins)  
- Jenkinsfile automates:
  - Code checkout  
  - Docker image build  
  - Container run and cleanup steps  
- Each push to GitHub triggers build & deployment automatically.  

### 4️. Monitoring (Prometheus + Grafana)  
- Flask exposes metrics at `/metrics` using `prometheus_client`.  
- Prometheus scrapes metrics from the app.  
- Grafana visualizes:
  - Request count  
  - Response time  
  - Container uptime and health  

---

## How to Run Locally  

```bash
# 1. Clone the repository
git clone https://github.com/KendyReriani17/e-commerce-pipeline.git
cd e-commerce-pipeline

# 2. Build and run the app
docker build -t ecommerce-app .
docker run -d -p 8000:8000 --name ecommerce-app ecommerce-app

# 3. (Optional) Start monitoring stack
docker-compose -f monitoring/docker-compose.yml up -d

 


