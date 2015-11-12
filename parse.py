#!/usr/bin/python
__author__ = 'rbuzatu'

import yaml
import sys
import argparse
import subprocess

parser = argparse.ArgumentParser()
# Envoronment options
parser.add_argument('--env_name', required=True, help='env name', type=str)
parser.add_argument('--os_version', required=True, help='openstack version', type=str)
parser.add_argument('--db_engine', required=True, help='database engine', type=str)
parser.add_argument('--msg_queue_engine', required=True, help='messaging queue', type=str)
parser.add_argument('--reset', required=True, help='reset type', type=str)
parser.add_argument('--debug', required=True, help='debug enabled', type=str)
parser.add_argument('--upgrade', required=True, help='upgrade enabled', type=str)
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

# Credentials options
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

# Networking options
parser.add_argument("--neutron_integration_bridge", required=True, type=str)
parser.add_argument("--neutron_external_bridge", required=True, type=str) # also sets type_drivers bridge
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
config["cinder"]["volumes_group_name"] = args.cinder_volumes_group_name
config["cinder"]["volumes_path"] = args.cinder_volumes_path
config["cinder"]["volumes_group_size"] = args.cinder_volumes_group_size
config["cinder"]["loopback_device"] = args.cinder_loopback_device
config["nova"]["cpu_allocation_ratio"] = args.cpu_allocation_ratio
config["nova"]["ram_allocation_ratio"] = args.ram_allocation_ratio
config["glance"]["images"]["cirros"]["parameters"]["copy_from"] = args.glance_copy_from
config["glance"]["images"]["cirros"]["parameters"]["disk_format"] = args.glance_disk_format
config["glance"]["images"]["cirros"]["parameters"]["container_format"] = args.glance_container_format
config["glance"]["images"]["cirros"]["parameters"]["is_public"] = args.glance_is_public
config["glance"]["images"]["cirros"]["parameters"]["protected"] = args.glance_protected

with open(salt_env_dir+"environment.sls", "w") as f:
    f.write(yaml.dump(config, default_flow_style=False))


with open(salt_env_dir+"credentials.sls", "r") as f:
    config = yaml.load(f)
config["mysql"]["root_password"] = args.db_password
config["rabbitmq"]["user_name"] = args.message_queue_user
config["rabbitmq"]["user_password"] = args.message_queue_password
config["databases"]["nova"]["nova_db_name"] = args.nova_db_name
config["databases"]["nova"]["nova_db_username"] = args.nova_db_username
config["databases"]["nova"]["nova_db_password"] = args.nova_db_password
config["databases"]["keystone"]["keystone_db_name"] = args.keystone_db_name
config["databases"]["keystone"]["keystone_db_user"] = args.keystone_db_user
config["databases"]["keystone"]["keystone_db_password"] = args.keystone_db_password
config["databases"]["cinder"]["cinder_db_name"] = args.cinder_db_name
config["databases"]["cinder"]["cinder_db_user"] = args.cinder_db_user
config["databases"]["cinder"]["cinder_db_password"] = args.cinder_db_password
config["databases"]["glance"]["glance_db_name"] = args.glance_db_name
config["databases"]["glance"]["glance_db_user"] = args.glance_db_user
config["databases"]["glance"]["glance_db_password"] = args.glance_db_password
config["databases"]["neutron"]["neutron_db_name"] = args.neutron_db_name
config["databases"]["neutron"]["neutron_db_user"] = args.neutron_db_user
config["databases"]["neutron"]["neutron_db_password"] = args.neutron_db_password
config["databases"]["heat"]["heat_db_name"] = args.heat_db_name
config["databases"]["heat"]["heat_db_user"] = args.heat_db_user
config["databases"]["heat"]["heat_db_password"] = args.heat_db_password
config["neutron"]["metadata_secret"] = args.neutron_metadata_secret
config["keystone"]["admin_token"] = args.keystone_admin_token
#config["overwrite_all_password"] = args.overwrite_all_password
config["keystone"]["tenants"]["admin"]["users"]["admin"]["keystonerc"]["path"] = args.keystonerc_location


with open(salt_env_dir+"credentials.sls", "w") as f:
    f.write(yaml.dump(config, default_flow_style=False))


with open(salt_env_dir+"networking.sls", "r") as f:
    config = yaml.load(f)
config["neutron"]["integration_bridge"] = args.neutron_integration_bridge
config["neutron"]["external_bridge"] = args.neutron_external_bridge
config["neutron"]["single_nic"]["interface"] = args.network_interface_name
config["neutron"]["type_drivers"]["vlan"]["physnets"]["physnet1"]["vlan_range"] = args.vlan_range
config["neutron"]["tunelling"]["enable"] = args.tunelling_enabled
config["neutron"]["tunelling"]["types"] = args.tunelling_type
config["neutron"]["tunneling"]["bridge"] = args.tunneling_bridge
config["neutron"]["networks"]["public"]["subnets"]["public_subnet"]["cidr"] = args.public_subnet_cidr
config["neutron"]["networks"]["public"]["subnets"]["public_subnet"]["allocation_pools"]["start"] = args.public_subnet_allocation_pool_start
config["neutron"]["networks"]["public"]["subnets"]["public_subnet"]["allocation_pool"]["end"] = args.public_subnet_allocation_pool_end
config["neutron"]["networks"]["public"]["subnets"]["public_subnet"]["subnet_dhcp_enabled"] = args.public_subnet_dhcp_enabled
config["neutron"]["networks"]["public"]["subnets"]["public_subnet"]["subnet_gateway_ip"] = args.public_subnet_gateway_ip
config["neutron"]["networks"]["private"]["subnets"]["private_subnet"]["cidr"] = args.private_subnet_cidr
with open(salt_env_dir+"networking.sls", "w") as f:
    f.write(yaml.dump(config, default_flow_style=False))


subprocess.call(["salt-call", "--local", "saltutil.refresh_pillar"])
subprocess.call(["salt-call", "--local", "saltutil.sync_all"])
subprocess.call(["salt-call", "--local", "state.highstate"])
subprocess.call(["salt-call", "--local", "state.highstate"])

