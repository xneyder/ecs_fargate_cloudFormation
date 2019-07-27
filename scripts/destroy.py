#!//usr/bin/python2
import sys
import os
import sh
import traceback
import json

def delete_images(ecrName):
	"""
	Deletes the images in a given ecr repository
	"""
	print("Deleting images from {ecrName}".format(
		ecrName=ecrName))
	try:
		#Get the image list from repository
		imageList=sh.aws("ecr",
			"list-images",
			"--repository-name",
			ecrName
		)	
		#Remove all images
		imageList=json.loads(str(imageList))
		for image in imageList['imageIds']:
			print("Removing image {imageDigest}".format(imageDigest=image['imageDigest']))
			sh.aws("ecr",
				"batch-delete-image",
				"--repository-name",
				ecrName,
				"--image-ids",
				"imageDigest={imageDigest}".format(imageDigest=image['imageDigest']),
			)
	except Exception as e:
		print(traceback.format_exc())

def delete_stack(stack_name):
	"""
	Deletes the given cloudFormation stack
	"""
	print("Deleting stack {stack_name}".format(
		stack_name=stack_name))
	try:
		sh.aws("cloudformation",
			"delete-stack",
			"--stack-name",
			stack_name,
		)

		#Wait for stack to be deleted
		print("Waiting for stack {stack_name} to be deleted".format(
			stack_name=stack_name))
		sh.aws("cloudformation",
			"wait",
			"stack-delete-complete",
			"--stack-name",
			stack_name
		)
		print("stack {stack_name} deleted".format(
			stack_name=stack_name))
	except Exception as e:
		print(traceback.format_exc())


def main():
	"""
	main function
	"""
	#Delete the pipeline stack
	delete_stack(pipeline_stack_name)
	#Delete the ecs stack
	delete_stack(ecs_stack_name)
	#Get the ECR name
	try:
		ecrName=sh.aws("cloudformation",
			"describe-stacks",
			"--stack-name",
			vpc_stack_name,
			"--query",
			"Stacks[0].Outputs[?OutputKey=='ECRRepositoryName'].OutputValue",
			"--output",
			"text"
		)
		delete_images(ecrName)
	except Exception as e:
		print(traceback.format_exc())
	#Delete the vpc stack
	delete_stack(vpc_stack_name)

if __name__ == "__main__":
	vpc_stack_name = 'vpc'
	ecs_stack_name = 'ecs'
	pipeline_stack_name = 'pipeline'
	answer=raw_input("Are you sure to delete the stacks vpc, ecs, and pipeline ? [y/n]: ")
	if answer.upper() == "Y":
		main()
