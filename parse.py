#!/usr/bin/python

__author__ = 'rbuzatu'
import yaml
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--env_name', required=True,
                        help='env name', type=str)
parser.add_argument('--os_version', required=True,
                        help='openstack version', type=str)
parser.add_argument('--db_engine', required=True,
                        help='database engine', type=str)
parser.add_argument('--msg_queue_engine', required=True,
                        help='messaging queue', type=str)
parser.add_argument('--reset', required=True,
                        help='reset type', type=str)
parser.add_argument('--debug', required=True,
                        help='debug enabled', type=str)
parser.add_argument('--upgrade', required=True,
                        help='upgrade enabled', type=str)

args = parser.parse_args()
print args
salt_env_dir='/etc/salt/openstack/pillar_root/'+args.env_name+'/'
print salt_env_dir

with open(salt_env_dir+"environment.sls", "r") as f:
    config = yaml.load(f)

config["environment_name"] = args.env_name
config["openstack_version"] = args.os_version
config["db_engine"] = args.db_engine
config["message_queue_engine"] = args.msg_queue_engine
config["system_upgrade"] = args.upgrade
config["reset"] = args.reset
config["debug"] = args.debug
#config["hosts"] = {args.debug:}

with open(salt_env_dir+"environment.sls", "w") as f:
    f.write(yaml.dump(config, default_flow_style=False))


