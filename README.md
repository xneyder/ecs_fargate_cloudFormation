# Cloudformation + Docker + ECR + ECS + Fargate + CloudWatch + CodePipeline

![meow](https://github.com/xneyder/ecs_fargate_cloudFormation/blob/master/images/diagram1.png)

## What is the puropose of the exercise?

The purpose of this repository is to be able to build from a single script all the infrastructure to serve a dockerized web application. It also includes the pipeline so when developers push changes to the repository it will automatically build the docker image, push it to the ECR repository and then deploy it to the Fargate Service.

We defined a CloudWatch Alarm to monitor an SQS queue and if the threshold is reached it will trigger and autoscalling target to scale out adding more tasks, and in the other direction if the alarm is cleared it will trigger the scale in to remove ECS tasks.

## CloudFormation Templates
### 1. vpc.yml
- VPC
- 2 public subnets in 2 availability zones
- 2 private subnets in 2 availability zones
- Internet Gateway
- Public table and associations
- NAT Gateway
- Private table and associations
- ECR Repository
- ECS Cluster
- Security Groups
- Public Elastic Load Balancer
- Private Application Load Balancer
- ECS Role
- ECR Role
- Autoscalling Role

### 2. ecs.yml
- CloudWatch Log Group
- ECS Task definition
- ECS Service
- Load Balancer Target Group
- Load Balancer Rule
- Autoscalling Target
- Scaling Policies
- Cloud Watch Alarm
- SQS queue

### 3. pipeline.yml
- CodeBuild service role
- CodePipeline Service role
- CodeBuild
- CodePipeline

## Scripts
### 1. deploy.py
Main script that creates the image and builds the stacks on AWS
### 2. docker_image.sh
Created the initial Docker image and pushes it to the ECR repository
### 3. send_sqs_messages.py
Sends messages to the SQS queue in order to test the CloudWatch alarm and the scale out policy
### 4. consume_sqs_messages.py
Consumes messages from the SQS queue in order to test the CloudWatch alarm and scale in policy
### 5. destroy.py
Deletes the docker images and the AWS stacks

## Deploy to AWS
### 0. Prerequisites

- python 2.7
- boto3 (pip install boto3)
- python sh module (pip install sh)
- A copy of this repository (so that you can integrate with AWS Code Pipeline)
- [Docker](https://docs.docker.com/compose/)
- [AWS CLI](https://github.com/aws/aws-cli) version >= `1.14.11` configured to use the `us-east-1` as its default region (for Fargate support)
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

### 3. execute the deploy.py script

```console
cd scripts
python deploy.py
```

and follow the steps to create a personal access token for AWS Code Pipeline.
The token must have access to the `repo` scope. Store this token somewhere.

### 4. Get the ELB url


### 5. Test the webapp access

```console
curl ${ELB_ADDRESS}
```

### 6. Test the CodePipeline

Do some changes to the app.py script

```console
git add --all
git commit -m 'Changes on the app'
git push origin master
```

After a few minutes if you access the webapp you should see the changes done on the app.py script

```console
curl ${ELB_ADDRESS}
```

### 7. Test the autoscalling

We are going to fill the SQS with dummy messages

```console
cd scripts
python send_sqs_messages.py
```

After about 5 minutes the cloudwatch alarm will detect that the number of messages is more than 10 so it will trigger the scale out policy. To test it you can go to the console and see that the number of running tasks has increased.

Kill the send_sqs_messages.py and run the consume SQS messages to clear the alarm and scale in.

```console
cd scripts
python consume_sqs_messages.py
```

### TODO

- [ ] SSL
- [ ] Route53
- [ ] ensure that the ALB path is configured correctly (add more paths to app)
- [x] Code Pipeline + Code Deploy
- [ ] RDS instance + app to read database
- [x] deploy script
- [x] destroy script


