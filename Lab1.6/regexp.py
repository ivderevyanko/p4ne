import ipaddress
import glob
import re
from pprint import pprint

def parse_file(new_file):
    ip_addr = {}
    intf = {}
    host_dic = {}
    nothing = {}
    regex_intf = (r"^interface (?P<intf>\S+)$")
    regex_ip = (r"^ ip address (?P<ip>\d+.\d+.\d+.\d+) (?P<mask>\d+.\d+.\d+.\d+)$")
    regex_host = (r"^hostname (?P<hostname>\S+)")
    with open(new_file) as next_file:
        flag_intf = 1
        flag_ip = 1
        flag_host = 1
        for line in next_file:
            if re.search(regex_intf, line):
                intf_sequence = "intf" + str(flag_intf)
                intf[intf_sequence] = str(re.search(regex_intf, line).groups()).lstrip("(").rstrip(")").rstrip(",").strip("'")
                flag_intf += 1
            elif re.search(regex_ip, line):
                ip_sequence = "ip/mask" + str(flag_ip)
                ip_address = re.search(regex_ip, line).group(1)
                ip_mask = re.search(regex_ip, line).group(2)
                ip_addr[ip_sequence] = ipaddress.IPv4Interface((ip_address, ip_mask))
                flag_ip += 1
            elif re.search(regex_host, line):
                host_sequence = "host" + str(flag_host)
                host_dic[host_sequence] = str(re.search(regex_host, line).groups()).lstrip("(").rstrip(")").rstrip(",").strip("'")
                flag_host += 1
            else:
                nothing = {}

        return intf, ip_addr, host_dic, nothing

list_files = glob.glob("c:/Users/iv.derevyanko/Seafile/p4ne_training/config_files/*.txt")

for file in list_files:
    intf, ip_addr, host_dic, nothing = list(parse_file(file))
    print(intf, ip_addr, host_dic)