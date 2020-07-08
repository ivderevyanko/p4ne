import paramiko
import time
from pprint import pprint


BUF_SIZE = 70000
TIMEOUT = 1
# Создаем объект — соединение по ssh
ssh_connection = paramiko.SSHClient()
ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Инициируем соединение по ssh
ssh_connection.connect('10.31.72.160', username='restapi', password='j0sg1280-7@', look_for_keys=False, allow_agent=False)
session = ssh_connection.invoke_shell()
session.send("\n")
session.recv(BUF_SIZE)
session.send("terminal length 0\n")
time.sleep(TIMEOUT)

session.send("\n\n")
session.recv(BUF_SIZE)
session.send("show interfaces\n")
time.sleep(TIMEOUT)
out = session.recv(BUF_SIZE)
str_result = out.decode()
time.sleep(TIMEOUT*2)
session.close()

input = {}
output = {}
flag_intf = False
str_result = str_result.split("\n")
for line in str_result:
    if "line protocol" in line:
        line = line.split()
        for item in line:
            intf = item
            flag_intf = True
            break
    elif flag_intf == True and "packets input" in line:
        line = line.split()
        for value in line:
            value = value.rstrip(",")
            in_pb = "input: " + line[0] + " " + line[1] + "; " + line[3] + " " + line[4]
            input["interface "+ intf] = in_pb
    elif flag_intf == True and "packets output" in line:
        line = line.split()
        for value in line:
            value = value.rstrip(",")
            out_pb = "output: " + line[0] + " " + line[1] + "; " + line[3] + " " + line[4]
            output["interface " + intf] = out_pb
            flag_intf = False


pprint(input)
pprint(output)


