import requests
import json
from pprint import pprint
from flask import Flask, jsonify, render_template
import glob
import sys
import re
import ipaddress


app = Flask(__name__)

#@app.route('/')
#@app.route('/index')
#def index():
#    return "Справка об использовании: "

@app.route("/")
def index():
    return render_template("topology.html")

@app.route('/configs')
def p_configs():
    return values_hosts

@app.route('/config/<hostname>')
def p_hostname(hostname):
    value_ip = str(host_ip_in[hostname]).strip("[]").replace('\'', '')
    return "THIS HOST " + "\"" + hostname + "\"" + " has IP-addresses: " + value_ip

@app.route('/api/topology')
def p_topology():
    return jsonify(ticket)

def new_ticket():
    url = 'https://sandboxapic.cisco.com/api/v1/ticket'
    payload = {
        "username": "devnetuser","password": "Cisco123!"}
    header = {"content-type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers = header, verify = False)
    return response.json()['response']['serviceTicket']

if __name__ == '__main__':

    ticket = new_ticket()
    #controller = "devnetapi.cisco.com/sandbox/apic_em"
    url = "https://devnetapi.cisco.com/sandbox/apic_em/api/v1/topology/physical-topology"
    header = {"content-type": "application/json", "X-Auth-Token": ticket}

    responce = requests.get(url, headers=header, verify=False)
    #responce.json()
    #print("Hosts = ")
    our_ticket = responce.json()
    ticket = our_ticket["response"]
    #print(ticket)
    app.run(debug=True)
