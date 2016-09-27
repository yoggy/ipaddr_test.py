#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# ipaddr_test.py - IPアドレスに関する情報を取得するテスト。
#
# github:
#     https://github.com/yoggy/ipaddr_test.py
#
# license:
#     Copyright (c) 2016 yoggy <yoggy0@gmail.com>
#     Released under the MIT license
#     http://opensource.org/licenses/mit-license.php;
#
import commands

def exec_cmd(cmd):
  result = commands.getoutput(cmd)
  #print("exec_cmd: cmd=" + cmd)
  #print("exec_cmd: result=" + result)
  return result

def get_ip_addr():
  cmd = "/usr/sbin/ip addr show | grep 'inet ' | grep -v 127.0.0.1 | awk '{print $2'} | sed 's/^\\(.*\\)\\/\\(.*\\)$/\\1/' | head -1"
  return exec_cmd(cmd)

def get_subnet_cidr():
  cmd = "/usr/sbin/ip addr show | grep 'inet ' | grep -v 127.0.0.1 | awk '{print $2'} | sed 's/^\\(.*\\)\\/\\(.*\\)$/\\2/' | head -1"
  return int(exec_cmd(cmd))

def get_subnet_mask():
  num = get_subnet_cidr()
  b = "1" * num + "0" * (32 - num)
  m0 = int(b[ 0: 8], 2)
  m1 = int(b[ 8:16], 2)
  m2 = int(b[16:24], 2)
  m3 = int(b[24:31], 2)
  return "{0}.{1}.{2}.{3}".format(m0, m1, m2, m3)

def get_network_addr():
  ip_str    = get_ip_addr()
  mask_str  = get_subnet_mask()
  ip_nums   = list(map(lambda x:int(x), ip_str.split(".")))
  mask_nums = list(map(lambda x:int(x), mask_str.split(".")))

  a = []
  for i in range(4):
    a.append(ip_nums[i] & mask_nums[i])

  return ".".join(list(map(lambda x:str(x), a)))

def get_broadcast_addr():
  cmd = "/usr/sbin/ip addr show | grep 'inet ' | grep -v 127.0.0.1 | awk '{print $4'} | head -1"
  return exec_cmd(cmd)

ip         = get_ip_addr()
subnetmask = get_subnet_mask()
cidr       = get_subnet_cidr()
network    = get_network_addr()
broadcast  = get_broadcast_addr()

print("ip={0}, subnetmask={1}, cidr={2}, network={3}, broadcast={4}".format(ip, subnetmask, cidr, network, broadcast))

