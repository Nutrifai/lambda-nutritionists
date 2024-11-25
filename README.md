# NutrifAI - Nutritionist Scheduling Lambda
This repository contains an AWS Lambda function that handles scheduling actions for nutritionists. It provides endpoints to fetch available time slots, confirm bookings, and update nutritionist availability in real-time. The function integrates with DynamoDB to manage nutritionist data and availability.

## Key Features

- Fetch a list of nutritionists and their available time slots.
- Book a time slot for a specific nutritionist and update their availability.
- Update information from an appointment with a nutritionist 
- Serverless architecture using AWS Lambda.
- Integration with DynamoDB for storing nutritionist data and time slots.

## Requirements

To use this project, ensure you have the following installed:
- [Terraform](https://www.terraform.io/downloads)
- [AWS CLI](https://aws.amazon.com/cli/) configured with appropriate permissions

Ensure that your AWS credentials are configured correctly using `aws configure`

## Instructions to Deploy Locally

### 1. Clone the repository
```bash
git clone https://github.com/Nutrifai/lambda-nutritionists.git
cd infra
```

### 2. Initialize Terraform
Before running any commands, initialize Terraform in the project directory.
```bash
terraform init
```

### 3. Plan the Deployment
Generate and review an execution plan to understand the resources that will be created or updated.
```bash
terraform plan
```

### 4. Apply the Configuration
To deploy the resources to AWS, run:
```bash
terraform apply -auto-approve
```

### Outputs
After deploying the infrastructure, Terraform will output useful information such as the API Gateway URL and Lambda function ARN. You can customize these outputs in the `outputs.tf` files.