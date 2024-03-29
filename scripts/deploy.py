#!//usr/bin/python2
import os
import argparse
import sh
import traceback

def parse_args():
	"""
	Parse input arguments
	"""
	global github_key
	parser = argparse.ArgumentParser()

	parser.add_argument('-k','--key',
		help='Github token key',
		required=True,
		type=str)

	args=parser.parse_args()
	github_key=args.key

def wait_for_creation(stack_name):
	"""
	Waits for the given stack to be created
	"""
	try:
		print("Waiting for stack {stack_name} to be created".format(
			stack_name=stack_name))
		sh.aws("cloudformation",
			"wait",
			"stack-create-complete",
			"--stack-name",
			stack_name
		)
		print("stack {stack_name} created".format(
			stack_name=stack_name))
	except Exception as e:
		print(traceback.format_exc())
	

def main():
	"""
	main function
	"""
	#Create the vpc stack
	print("Creating stack {vpc_stack_name}".format(
		vpc_stack_name=vpc_stack_name))
	try:
		sh.aws("cloudformation",
			"create-stack",
			"--stack-name",
			vpc_stack_name,
			"--template-body",
			"file://{vpc_file_location}".format(vpc_file_location=vpc_file_location),
			"--capabilities",
			"CAPABILITY_IAM"
		)

		#Wait for stack to be created
		wait_for_creation(vpc_stack_name)
	except Exception as e:
		print(traceback.format_exc())

	#Get the ECR Url
	try:
		ecrUrl=sh.aws("cloudformation",
			"describe-stacks",
			"--stack-name",
			vpc_stack_name,
			"--query",
			"Stacks[0].Outputs[?OutputKey=='ECRRepositoryUrl'].OutputValue",
			"--output",
			"text"
		)
	except Exception as e:
		print(traceback.format_exc())

	#Build the image and push it to ECR
	print('Building Docker image and pushing it to {ecrUrl}'.format(
		ecrUrl=ecrUrl))
	print(sh.bash("docker_image.sh",ecrUrl))
	
	#Create the ecs stack
	print("Creating stack {ecs_stack_name}".format(
		ecs_stack_name=ecs_stack_name))
	try:
		sh.aws("cloudformation",
			"create-stack",
			"--stack-name",
			ecs_stack_name,
			"--template-body",
			"file://{ecs_file_location}".format(ecs_file_location=ecs_file_location)
		)

		#Wait for stack to be created
		wait_for_creation(ecs_stack_name)
	except Exception as e:
		print(traceback.format_exc())

	#Create the pipeline stack
	print("Creating stack {pipeline_stack_name}".format(
		pipeline_stack_name=pipeline_stack_name))
	try:
		sh.aws("cloudformation",
			"create-stack",
			"--stack-name",
			pipeline_stack_name,
			"--template-body",
			"file://{pipeline_file_location}".format(pipeline_file_location=pipeline_file_location),
			"--parameters",
			"ParameterKey=GitHubToken,ParameterValue={github_key}".format(github_key=github_key),
			"--capabilities",
			"CAPABILITY_IAM"
		)

		#Wait for stack to be created
		wait_for_creation(pipeline_stack_name)
	except Exception as e:
		print(traceback.format_exc())

if __name__ == "__main__":
	INFRA_DIR='../infra/'
	vpc_file_location = os.path.join(INFRA_DIR,'vpc.yml')
	vpc_stack_name = 'vpc'
	ecs_file_location = os.path.join(INFRA_DIR,'ecs.yml')
	ecs_stack_name = 'ecs'
	pipeline_file_location = os.path.join(INFRA_DIR,'pipeline.yml')
	pipeline_stack_name = 'pipeline'
	github_key=""
	parse_args()
	main()
