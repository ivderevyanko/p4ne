import glob
import os
from pprint import pprint

list_files = glob.glob("c:/Users/iv.derevyanko/Seafile/p4ne_training/config_files/*.txt")
ip_addresses = []
find_words = " ip address"
find_key = "address"

for newfile in list_files:
    with open(newfile) as next_file:
        for line in next_file:
            if line.startswith(find_words) and "dhcp" not in line:
                ip_index_start = find_words.find(find_key) + 8
                ip_mask = line[ip_index_start:].strip()
                ip_addresses.append(ip_mask)

pprint(list(set(ip_addresses)))