import json
import math
import sys
import time

import boto3
import logging

import pika
from fabric import task
import requests

# use loggers right from the start, rather than 'print'
logger = logging.getLogger(__name__)
# this will log boto output to std out
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

from dotenv import dotenv_values

config = dotenv_values(".env")

# Step #1: Connect to RabbitMQ
password = config['password']
username = config['username']

credentials = pika.PlainCredentials(username, password)
parameters = pika.ConnectionParameters(credentials=credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

phases = int(config['phases'])
max_phase_msg_count = int(config['max_phase_msg_count'])
total_time = int(config['total_time'])

phase_duration = total_time / phases

start_time = time.time()
end_time = start_time + total_time


def get_payload():
    ip_address = '123.456.789.101'
    return {"address": ip_address}


for p in range(1, phases + 1):

    phase_count = math.ceil(p * max_phase_msg_count / phases)
    logger.info(f"starting message phase {p} at {phase_count}")

    for i in range(phase_count):
        channel.basic_publish(exchange='',
                              routing_key='stream',
                              body=json.dumps(get_payload()))

    spec_phase_end_time = start_time + p * phase_duration
    phase_time_delta = spec_phase_end_time - time.time()
    if phase_time_delta < 0:
        logger.warning("sending rate lower than specified message rate")
    else:
        time.sleep(phase_time_delta)
