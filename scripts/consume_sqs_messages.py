#!/usr/bin/python2
import sys
import time
import boto3

SQS_NAME='AutoScallingQueue.fifo'

# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue
try:
	queue = sqs.get_queue_by_name(QueueName=SQS_NAME)
except:
	print('SQS Queue {SQS_NAME} not found'.format(SQS_NAME=SQS_NAME))
	sys.exit(1)

while True:
	message=False
	for message in queue.receive_messages():
		# Print out the message
		print(message)
		# Let the queue know that the message is processed
		message.delete()
	if message==False:
		break
	#time.sleep(1)
