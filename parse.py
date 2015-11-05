#!/usr/bin/python
__author__ = 'rbuzatu'

import yaml
import sys
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--env_name', required=True, help='env name', type=str)
parser.add_argument('--os_version', required=True, help='openstack version', type=str)
parser.add_argument('--db_engine', required=True, help='database engine', type=str)
parser.add_argument('--msg_queue_engine', required=True, help='messaging queue', type=str)
parser.add_argument('--reset', required=True, help='reset type', type=str)
parser.add_argument('--debug', required=True, help='debug enabled', type=str)
parser.add_argument('--upgrade', required=True, help='upgrade enabled', type=str)
parser.add_argument("--db_password", required=True, type=str)
parser.add_argument("--message_queue_user", required=True, type=str)
parser.add_argument("--message_queue_password", required=True, type=str)
parser.add_argument("--nova_db_name", required=True, type=str)
parser.add_argument("--nova_db_username", required=True, type=str)
parser.add_argument("--nova_db_password", required=True, type=str)
parser.add_argument("--keystone_db_name", required=True, type=str)
parser.add_argument("--keystone_db_user", required=True, type=str)
parser.add_argument("--keystone_db_password", required=True, type=str)
parser.add_argument("--cinder_db_name", required=True, type=str)
parser.add_argument("--cinder_db_user", required=True, type=str)
parser.add_argument("--cinder_db_password", required=True, type=str)
parser.add_argument("--glance_db_name", required=True, type=str)
parser.add_argument("--glance_db_user", required=True, type=str)
parser.add_argument("--glance_db_password", required=True, type=str)
parser.add_argument("--neutron_db_name", required=True, type=str)
parser.add_argument("--neutron_db_user", required=True, type=str)
parser.add_argument("--neutron_db_password", required=True, type=str)
parser.add_argument("--heat_db_name", required=True, type=str)
parser.add_argument("--heat_db_user", required=True, type=str)
parser.add_argument("--heat_db_password", required=True, type=str)
parser.add_argument("--neutron_metadata_secret", required=True, type=str)
parser.add_argument("--keystone_admin_token", required=True, type=str)
parser.add_argument("--overwrite_all_password", required=True, type=str)
parser.add_argument("--keystonerc_location", required=True, type=str)
parser.add_argument("--cinder_volumes_group_name", required=True, type=str)
parser.add_argument("--cinder_volumes_path", required=True, type=str)
parser.add_argument("--cinder_volumes_group_size", required=True, type=str)
parser.add_argument("--cinder_loopback_device", required=True, type=str)
parser.add_argument("--cpu_allocation_ratio", required=True, type=str)
parser.add_argument("--ram_allocation_ratio", required=True, type=str)
parser.add_argument("--glance_copy_from", required=True, type=str)
parser.add_argument("--glance_disk_format", required=True, type=str)
parser.add_argument("--glance_container_format", required=True, type=str)
parser.add_argument("--glance_is_public", required=True, type=str)
parser.add_argument("--glance_protected", required=True, type=str)
parser.add_argument("--neutron_integration_bridge", required=True, type=str)
parser.add_argument("--neutron_external_bridge", required=True, type=str)
parser.add_argument("--network_interface_name", required=True, type=str)
parser.add_argument("--vlan_range", required=True, type=str)
parser.add_argument("--tunelling_enabled", required=True, type=str)
parser.add_argument("--tunelling_type", required=True, type=str)
parser.add_argument("--tunneling_bridge", required=True, type=str)
parser.add_argument("--public_subnet_cidr", required=True, type=str)
parser.add_argument("--public_subnet_allocation_pool_start", required=True, type=str)
parser.add_argument("--public_subnet_allocation_pool_end", required=True, type=str)
parser.add_argument("--public_subnet_dhcp_enabled", required=True, type=str)
parser.add_argument("--public_subnet_gateway_ip", required=True, type=str)
parser.add_argument("--private_subnet_cidr", required=True, type=str)


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

with open(salt_env_dir+"environment.sls", "w") as f:
    f.write(yaml.dump(config, default_flow_style=False))

with open(salt_env_dir+"credentials.sls", "r") as f:
    config = yaml.load(f)

config["environment_name"] = args.env_name
config["openstack_version"] = args.os_version
config["db_engine"] = args.db_engine
config["message_queue_engine"] = args.msg_queue_engine
config["system_upgrade"] = args.upgrade
config["reset"] = args.reset
config["debug"] = args.debug
#config["hosts"] = {args.debug:}

with open(salt_env_dir+"credentials.sls", "w") as f:
    f.write(yaml.dump(config, default_flow_style=False))

with open(salt_env_dir+"networking.sls", "r") as f:
    config = yaml.load(f)

config["environment_name"] = args.env_name
config["openstack_version"] = args.os_version
config["db_engine"] = args.db_engine
config["message_queue_engine"] = args.msg_queue_engine
config["system_upgrade"] = args.upgrade
config["reset"] = args.reset
config["debug"] = args.debug
#config["hosts"] = {args.debug:}

with open(salt_env_dir+"networking.sls", "w") as f:
    f.write(yaml.dump(config, default_flow_style=False))

subprocess.call(["salt-call", "--local", "saltutil.refresh_pillar"])
subprocess.call(["salt-call", "--local", "saltutil.sync_all"])
subprocess.call(["salt-call", "--local", "state.highstate"])
