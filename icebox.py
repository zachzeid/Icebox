#!/usr/bin/env python

import boto
import boto.ec2
import time
instance_list = []
conn = boto.ec2.EC2Connection()
region_list = conn.get_all_regions()
def region_connections(region_list):
	conn_list = []
	for region in region_list:
		r_conn = boto.ec2.connect_to_region(region.name)
		conn_list.append(r_conn)
		#print region, r_conn, len(conn_list)
	return conn_list

def check_state(instanceList):
	instance_state = []
	for list in instanceList:
		for instance in list:
			if instance.state == "running":
				#print instance.state, instance.id
				instance_state.append(instance.id)
				instance.stop()
				instance.update()
	return instance_state
def stop_instance(instanceId):
	pass	


conn_list = region_connections(region_list)

for connection in conn_list:
	instances = connection.get_all_instances()
	for res in instances:
		instance_list.append(res.instances)

check = check_state(instance_list)

for instance in check:
	print instance
