# Cloudformation + Docker + ECR + ECS + Fargate + CloudWatch + CodePipeline

![meow](https://github.com/xneyder/ecs_fargate_cloudFormation/blob/master/images/diagram1.png)

## What is the puropose of the exercise?

The purpose of this repository is to be able to build from a single script all the infrastructure to serve a dockerized web application. It also includes the pipeline so when developers push changes to the repository it will automatically build the docker image, push it to the ECR repository and then deploy it to the Fargate Service.

We defined a CloudWatch Alarm to monitor an SQS queue and if the threshold is reached it will trigger and auto scaling target to scale out adding more tasks, and in the other direction if the alarm is cleared it will trigger the scale in to remove ECS tasks.

## CloudFormation Templates
### 1. vpc.yml
- VPC
- 2 public subnets in 2 availability zones
- 2 private subnets in 2 availability zones
- Internet Gateway
- Public routing table and associations
- NAT Gateway
- Private routing table and associations
- ECR Repository
- ECS Cluster
- Security Groups
- Public Elastic Load Balancer
- Private Application Load Balancer
- ECS Role
- ECR Role
- Auto scaling Role

### 2. ecs.yml
- CloudWatch Log Group
- ECS Task definition
- ECS Service
- Load Balancer Target Group
- Load Balancer Rule
- Auto scaling Target
- Auto Scaling Policies
- Cloud Watch Alarm
- SQS queue

### 3. pipeline.yml
- CodeBuild service role
- CodePipeline service role
- CodeBuild
- CodePipeline

## Scripts
### 1. deploy.py
Main script which uses the aws cli for creating the stacks on AWS. Here are the main steps:
- Creates the vpc stack.
- Builds and pushes to ecr the Docker image using the docker_image.sh script mentioned below.
- Creates the ecs stack.
- Creates the pipeline stack.

### 2. docker_image.sh
Receives the ecr repository Url as parameter, then it builds the docker image using the Dockerfile found in the root of this repository, once the image is built it is pushed to the ecr repository.

### 3. send_sqs_messages.py
Uses the boto3 python module to send messages to the SQS queue in order to test the CloudWatch alarm and the auto scale out policy.

### 4. consume_sqs_messages.py
Uses the boto3 python module to consume messages from the SQS queue in order to test the CloudWatch clear alarm and the auto scale in policy.

### 5. destroy.py
This script uses the aws cli and it's purpose is to delete all the stacks and the docker images.
- Deletes the pipeline stack.
- Deletes the ecs stack.
- Deletes all the images pushed to the ecr repository.
- Deletes the vpc stack.


## Deploy to AWS
### 0. Prerequisites

- python 2.7
- boto3 (pip install boto3)
- python sh module (pip install sh)
- A copy of this repository (so that you can integrate with AWS Code Pipeline)
- [Docker](https://docs.docker.com/compose/)
- [AWS CLI](https://github.com/aws/aws-cli) version >= `1.14.11` configure with the user keys.
- an AWS [access key id and secret access key](http://docs.aws.amazon.com/general/latest/gr/managing-aws-access-keys.html) which has admin-level permissions for your AWS account

### 1. Fork the GitHub repository

[Fork](https://help.github.com/articles/fork-a-repo/) the [Amazon ECS sample
app](https://github.com/xneyder/ecs_fargate_cloudFormation) GitHub repository into
your GitHub account.

From your terminal application, execute the following command (make sure to
replace `<your_github_username>` with your actual GitHub username):

```console
git clone https://github.com/<your_github_username>/ecs_fargate_cloudFormation
```

This creates a directory named `ecs_fargate_cloudFormation` in your current
directory, which contains all the required files.

### 2. Create a GitHub Personal Token used for the CI Pipeline
Go [here](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/)
and follow the steps to create a personal access token for AWS Code Pipeline.
The token must have access to the `repo` scope. Store this token somewhere.

### 3. execute the deploy.py script

```console
cd scripts
python deploy.py -k [Github Token key]
```

### 4. Test the webapp access

```console
curl `aws cloudformation describe-stacks --stack-name vpc --query "Stacks[0].Outputs[?OutputKey=='ExternalUrl'].OutputValue" --output text`
```

### 5. Test the CodePipeline

Do some changes to the app.py script

```console
git add --all
git commit -m 'Changes on the app'
git push origin master
```

After a few minutes if you access the webapp you should see the changes done on the app.py script

```console
curl `aws cloudformation describe-stacks --stack-name vpc --query "Stacks[0].Outputs[?OutputKey=='ExternalUrl'].OutputValue" --output text`
```

### 6. Test the Auto scaling

We are going to fill the SQS with dummy messages

```console
cd scripts
python send_sqs_messages.py
```

After about 5 minutes the cloudwatch alarm will detect that the number of messages is more than 10 so it will trigger the scale out policy. To test it you can go to the AWS console and see that the number of running tasks has increased by 2.

Kill the send_sqs_messages.py and run the consume SQS messages script to clear the alarm and trigger the scale in policy.

```console
cd scripts
python consume_sqs_messages.py
```

### TODO

- [ ] SSL
- [ ] Route53


