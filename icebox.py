#!/usr/bin/env python

import boto
import boto.ec2
from boto.ec2.autoscale import AutoScaleConnection
import time
import argparse


instance_list = []
conn = boto.ec2.EC2Connection()
asg_conn = AutoScaleConnection()
region_list = conn.get_all_regions()


parser = argparse.ArgumentParser(description='Start and stop instances')
parser.add_argument('--stop', action="store_true", help="Stop instances", required=False)
parser.add_argument('--start', action="store_true", help="Start instances", required=False)
args = parser.parse_args()

def disable_asg(asg_list):
	for asg in asg_list:
		for group in asg:
			group.suspend_processes()
	return asg

def enable_asg(asg_list):
	for asg in asg_list:
		for group in asg:
			group.resume_processes()
	return asg
def region_connections(region_list):
	conn_list = []
	for region in region_list:
		r_conn = boto.ec2.connect_to_region(region.name)
		conn_list.append(r_conn)
	return conn_list

def asg_region_connections(region_list):
	conn_list = []
	for region in region_list:
		asg_conn = boto.ec2.autoscale.connect_to_region(region.name)
		conn_list.append(asg_conn)
	return conn_list

def stop_state(instanceList):
	instance_state = []
	for list in instanceList:
		for instance in list:
			if instance.state == "running":
				instance_state.append(instance.id)
				instance.stop()
	return instance_state


def start_state(instanceList):
	instance_state = []
	for list in instanceList:
		for instance in list:
			if instance.state == "stopped":
				instance_state.append(instance.id)
				instance.start()
				#instance.update()
			else:
				print "%s is in %s state, no action taken" % (instance.id, instance.state)
	return instance_state


conn_list = region_connections(region_list)
for connection in conn_list:
	instances = connection.get_all_instances()
	for res in instances:
		instance_list.append(res.instances)

asg_list = []
connection_list = asg_region_connections(region_list)
for conn in connection_list:
	asg_groups = conn.get_all_groups()
	asg_list.append(asg_groups)


if args.start:
	start_instance = start_state(instance_list)
	print "Starting instances", start_instance 
	resume_asg = enable_asg(asg_list)
	print "Resuming ASG", resume_asg
if args.stop:
	stop_instance = stop_state(instance_list)
	suspend_asg = disable_asg(asg_list)	
	print "Stopping instances", stop_instance
	print "Pausing ASGs", suspend_asg

