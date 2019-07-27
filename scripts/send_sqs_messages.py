#!/usr/bin/python2
import sys
import time
import random
import boto3

SQS_NAME='AutoScallingQueue.fifo'

# Get the service resource
sqs = boto3.resource('sqs')

queue = sqs.get_queue_by_name(QueueName=SQS_NAME)
# Get the queue
try:
	queue = sqs.get_queue_by_name(QueueName=SQS_NAME)
except:
	print('SQS Queue {SQS_NAME} not found'.format(SQS_NAME=SQS_NAME))
	sys.exit(1)


while True:
	# Create a new message
	response = queue.send_message(MessageBody=str(random.randint(1,1000)),MessageGroupId='1')
	print(response.get('MessageId'))
	time.sleep(5)
