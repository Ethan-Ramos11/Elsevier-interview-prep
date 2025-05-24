# Terraform Infrastructure as Code Learning Project

A comprehensive Terraform workflow demonstrating Infrastructure as Code principles, built as part of interview preparation for a Systems Engineering role at Elsevier.

## 🎯 Project Goals

This project was developed as **Day 2** of a comprehensive 5-day interview preparation plan, with the following objectives:

### **Learning Objectives:**

- Learn Infrastructure as Code fundamentals including declarative configuration, version control, reproducibility, and idempotency
- Gain hands-on experience with Terraform workflow and core commands
- Develop understanding of remote state management and its critical role in team environments
- Continue interfacing with AWS through Infrastructure as Code rather than imperative scripting

### **Technical Goals:**

- Create Terraform resources, variables, and outputs with proper configuration
- Implement remote state management with S3 backend and DynamoDB locking
- Design and build reusable Terraform modules for multi-environment deployment

## 📚 Learning Reflection

Day two provided a solid foundation in Infrastructure as Code technologies. Key accomplishments included:

**Infrastructure as Code Fundamentals:**

- Gained understanding of IaC concepts including declarative configuration, version control integration, reproducibility across environments, and idempotency
- Learned why enterprise environments leverage IaC tools for consistency, scalability, and risk reduction
- Understood the critical difference between imperative scripting (Day 1 Python) and declarative infrastructure definition

**Terraform Core Concepts:**

- **Declarative Configuration**: Defining desired infrastructure state rather than step-by-step creation process
- **State Management**: Understanding how Terraform tracks and manages infrastructure changes
- **Plan-Apply Workflow**: Preview changes before execution for safe infrastructure modifications
- **Remote State & Locking**: Team collaboration patterns using S3 backend and DynamoDB state locking
- **Modular Design**: Creating reusable infrastructure components for consistent multi-environment deployment

**Practical Implementation Challenges:**

- Successfully built end-to-end Terraform workflow from basic resources to modules
- Overcame initial complexity with Terraform documentation through systematic learning approach
- Experienced the satisfaction of seeing infrastructure deployed consistently across multiple environments

The theoretical benefits of Infrastructure as Code became clear through practical implementation, though Terraform's comprehensive feature set initially presented a learning curve that was overcome through structured practice.

## 🏗️ Project Architecture

This project demonstrates Infrastructure as Code progression:

### **Phase 1: Basic Resources (`resources/`)**

- **Purpose**: Foundation Terraform skills with variables, outputs, and basic S3 bucket creation
- **Demonstrates**: Core Terraform workflow, variable usage, and resource configuration
- **Learning Focus**: Understanding declarative infrastructure and basic Terraform commands

### **Phase 2: Remote State Management (`remote-state/`)**

- **Purpose**: Team collaboration infrastructure using S3 backend and DynamoDB locking
- **Demonstrates**: Shared state management, state locking, and bootstrap infrastructure patterns
- **Learning Focus**: Understanding how teams safely collaborate on infrastructure changes

### **Phase 3: Reusable Modules (`s3-modules/`)**

- **Purpose**: Modular, reusable infrastructure components for multi-environment deployment
- **Demonstrates**: Module design, environment separation, and scalable infrastructure patterns
- **Learning Focus**: Creating maintainable, reusable infrastructure code

### Directory Structure

```
terraform-basics/
├── remote-state/           # Bootstrap infrastructure for shared state
│   ├── backend.tf         # S3 backend configuration
│   ├── main.tf            # S3 bucket and DynamoDB table creation
│   └── variables.tf       # Regional and naming configuration
├── resources/             # Basic S3 resource example
│   ├── backend.tf         # Remote state configuration
│   ├── main.tf            # S3 bucket with variable interpolation
│   ├── variables.tf       # Comprehensive variable definitions
│   └── outputs.tf         # Resource information outputs
└── s3-modules/            # Modular infrastructure design
    ├── main.tf            # Module usage for dev/prod environments
    └── modules/
        └── s3-operations/ # Reusable S3 bucket module
            ├── main.tf    # Module resource definitions
            ├── variables.tf # Module input interface
            └── outputs.tf # Module return values
```

## ⚙️ How to Use

### Prerequisites

- **Terraform CLI** installed (version >= 1.2.0)
- **AWS CLI** configured with appropriate permissions
- **AWS Account** with S3 and DynamoDB access

### Bootstrap Process (Remote State Setup)

```bash
# 1. Create remote state infrastructure first
cd terraform-basics/remote-state/
terraform init
terraform plan
terraform apply

# 2. Use basic resources with remote state
cd ../resources/
terraform init  # Will prompt for state migration
terraform plan
terraform apply

# 3. Deploy modular infrastructure
cd ../s3-modules/
terraform init
terraform plan
terraform apply
```

### Key Terraform Commands Demonstrated

```bash
terraform init      # Initialize providers and backend
terraform validate  # Check configuration syntax
terraform plan      # Preview infrastructure changes
terraform apply     # Execute planned changes
terraform show      # Display current infrastructure state
terraform destroy   # Clean up created resources
```

### Variable Design Philosophy

- **Required vs Optional**: Clear interface for module consumers
- **Environment Awareness**: Built-in support for multi-environment deployment
- **Feature Flags**: Configurable bucket capabilities (versioning, encryption, logging)
- **Sensible Defaults**: Working configuration without extensive customization

## 🚀 Future Enhancements

Potential expansions for continued learning:

- **Advanced Modules**: Cross-service modules with dependencies (S3, CloudFront, Route53)
- **Policy as Code**: IAM policies and bucket policies defined in Terraform
- **Multi-Region Deployment**: Geographic distribution and disaster recovery patterns
- **CI/CD Integration**: Automated infrastructure deployment pipelines
- **Monitoring Integration**: CloudWatch, alerting, and observability as code
- **Security Scanning**: Integration with security tools for infrastructure validation

---

_Built as part of Elsevier Systems Engineering interview preparation - demonstrating Infrastructure as Code mastery and enterprise-ready development practices._
