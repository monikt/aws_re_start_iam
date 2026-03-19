# Desafío 3: Infraestructura Web con CloudFormation

Este proyecto despliega una aplicación web altamente disponible en AWS utilizando CloudFormation. Incluye una VPC con subnets públicas y privadas, NAT Gateway, Application Load Balancer, Auto Scaling Group con instancias EC2 que sirven una página "Hola Mundo".

## Arquitectura

```mermaid
graph TB
    subgraph "VPC (10.0.0.0/16)"
        subgraph "AZ A"
            PubSubA["Subnet Pública A<br/>10.0.1.0/27"]
            PrivSubA["Subnet Privada A<br/>10.0.3.0/27"]
        end
        subgraph "AZ B"
            PubSubB["Subnet Pública B<br/>10.0.2.0/27"]
            PrivSubB["Subnet Privada B<br/>10.0.4.0/27"]
        end

        IGW["Internet Gateway"]
        NAT["NAT Gateway"]
        ALB["Application Load Balancer"]
        ASG["Auto Scaling Group"]
        Web1["EC2 Web 1"]
        Web2["EC2 Web 2"]

        IGW --> PubSubA
        IGW --> PubSubB
        NAT --> PubSubA
        NAT --> PrivSubA
        NAT --> PrivSubB

        ALB --> PubSubA
        ALB --> PubSubB
        ALB --> ASG

        ASG --> PrivSubA
        ASG --> PrivSubB
        ASG --> Web1
        ASG --> Web2
    end

    User(("Usuario")) --> IGW
    User --> ALB