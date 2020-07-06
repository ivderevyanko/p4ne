from flask import Flask, jsonify
import glob
from pprint import pprint
import sys
import re
import ipaddress


app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return "Справка об использовании: "

@app.route('/configs')
def p_configs():
    return values_hosts

@app.route('/config/<hostname>')
def p_hostname(hostname):
    value_ip = str(host_ip_in[hostname]).strip("[]").replace('\'', '')
    return "THIS HOST " + "\"" + hostname + "\"" + " has IP-addresses: " + value_ip

if __name__ == '__main__':
    def parse_file(new_file):
        ip_addr = {}
        host_ip_dic = {}
        ip_list = []
        intf = {}
        host_dic = {}
        hostname = None
        regex_intf = (r"^interface (?P<intf>\S+)$")
        regex_ip = (r"^ ip address (?P<ip>\d+.\d+.\d+.\d+) (?P<mask>\d+.\d+.\d+.\d+)$")
        regex_host = (r"^hostname (?P<hostname>\S+)")
        with open(new_file) as next_file:
            flag_intf = 1
            flag_ip = 1
            for line in next_file:
                if hostname:
                    host_ip_dic[hostname] = ip_list
                    hostname = None
                if re.search(regex_host, line):
                    host_dic["hostname"] = str(re.search(regex_host, line).groups()).lstrip("(").rstrip(")").rstrip(
                        ",").strip("'")
                    hostname = str(re.search(regex_host, line).groups()).lstrip("(").rstrip(")").rstrip(
                        ",").strip("'")
                elif re.search(regex_intf, line):
                    flag_yes = True
                    value_intf = str(re.search(regex_intf, line).groups()).lstrip("(").rstrip(")").rstrip(",").strip(
                        "'")
                elif re.search(regex_ip, line) and "dhcp" not in line and flag_yes:
                    intf_sequence = "intf" + str(flag_intf)
                    intf[intf_sequence] = value_intf
                    flag_intf += 1
                    ip_sequence = "ip/mask" + str(flag_ip)
                    ip_address = re.search(regex_ip, line).group(1)
                    ip_mask = re.search(regex_ip, line).group(2)
                    ip_addr[ip_sequence] = ipaddress.IPv4Interface((ip_address, ip_mask))
                    ip_list.append(ipaddress.IPv4Interface((ip_address, ip_mask)))
                    flag_ip += 1
                    flag_yes = False
                else:
                    flag_yes = False
            return host_dic, intf, ip_addr, host_ip_dic


    list_files = glob.glob("c:/Users/iv.derevyanko/Seafile/p4ne_training/config_files/*.txt")

    all_ip_mask = []
    all_ip = []
    all_mask = []
    values_hosts = {}
    host_ip_in = {}
    ip_m_list = []
    flag = 1
    flag_ip = False
    for file in list_files:
        host_dic, intf, ip_addr, host_ip_dic = parse_file(file)
        ip_addr = list(ip_addr.values())
        for item in ip_addr:
            all_ip_mask.append(item)
        for item, value in host_dic.items():
            item = "Hostname №" + str(flag)
            values_hosts[item] = value
            flag += 1
        for item, value in host_ip_dic.items():
            for ipv4 in value:
                ipv4 = str(ipv4)
                ip_m_list.append(ipv4)
                flag_ip = True
            if flag_ip:
                host_ip_in[item] = ip_m_list
                ip_m_list = []
                flag_ip = False

    for item in all_ip_mask:
        all_ip.append(item.network)

    all_ip = set(all_ip)
    dict_ip = {}

    for item in all_ip:
        ip_net = str(item.network_address)
        dict_ip[ip_net] = str(item.netmask)

    app.run(debug=True)
