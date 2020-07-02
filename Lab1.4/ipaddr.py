import ipaddress
import random
import pprint

class IPv4RandomNetwork(ipaddress.IPv4Network):
    def __init__(self, start, stop):
        ipaddress.IPv4Network.__init__(self, (random.randint(0x0B000000, 0xDF000000), random.randint(start, stop)), strict=False)

    def regular(self):
        return not (self.is_private |
                    self.is_unspecified |
                    self.is_reserved |
                    self.is_loopback |
                    self.is_link_local)

def key_function(address_mask):
    ip = int(address_mask.network_address)
    mask = int(address_mask.netmask)
    result = mask * 2**32 + ip
    return result

random_net = []
for value in range(0, 10):
    random_net.append(IPv4RandomNetwork(8, 24))

random_net = sorted(random_net, key=key_function)

for items in random_net:
    print(items)

