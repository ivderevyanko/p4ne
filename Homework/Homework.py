import ipaddress
import glob
import re
from tabulate import tabulate
from openpyxl import Workbook

def parse_file(new_file):
    ip_addr = {}
    intf = {}
    host_dic = {}
    regex_intf = (r"^interface (?P<intf>\S+)$")
    regex_ip = (r"^ ip address (?P<ip>\d+.\d+.\d+.\d+) (?P<mask>\d+.\d+.\d+.\d+)$")
    regex_host = (r"^hostname (?P<hostname>\S+)")
    with open(new_file) as next_file:
        flag_intf = 1
        flag_ip = 1
        for line in next_file:
            if re.search(regex_host, line):
                host_dic["hostname"] = str(re.search(regex_host, line).groups()).lstrip("(").rstrip(")").rstrip(",").strip("'")
            elif re.search(regex_intf, line):
                flag_yes = True
                value_intf = str(re.search(regex_intf, line).groups()).lstrip("(").rstrip(")").rstrip(",").strip("'")
            elif re.search(regex_ip, line) and "dhcp" not in line and flag_yes:
                intf_sequence = "intf" + str(flag_intf)
                intf[intf_sequence] = value_intf
                flag_intf += 1
                ip_sequence = "ip/mask" + str(flag_ip)
                ip_address = re.search(regex_ip, line).group(1)
                ip_mask = re.search(regex_ip, line).group(2)
                ip_addr[ip_sequence] = ipaddress.IPv4Interface((ip_address, ip_mask))
                flag_ip += 1
                flag_yes = False
            else:
                flag_yes = False
        return host_dic, intf, ip_addr

list_files = glob.glob("c:/Users/iv.derevyanko/Seafile/p4ne_training/config_files/*.txt")

all_ip_mask = []
all_ip = []
all_mask = []
for file in list_files:
    host_dic, intf, ip_addr = parse_file(file)
    ip_addr = list(ip_addr.values())
    for item in ip_addr:
        all_ip_mask.append(item)

for item in all_ip_mask:
    all_ip.append(item.network)

all_ip = set(all_ip)
dict_ip = {}

for item in all_ip:
   ip_net = str(item.network_address)
   dict_ip[ip_net] = str(item.netmask)

print(tabulate(dict_ip.items(), headers=["Network", "Netmask"], tablefmt='grid'))

# To Excel
workbook = Workbook()
sheet = workbook.active

sheet["A1"] = "Network"
sheet["B1"] = "Netmask"

for row, (key, value) in enumerate(dict_ip.items(), start=2):
    sheet [f"A{row}"] = key
    sheet [f"B{row}"] = value

workbook.save("Ip-Mask.xlsx")




