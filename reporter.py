# Imports
import socket
import subprocess
import os
import requests
from prettytable import PrettyTable
import CONFIG

def send_message(text):
    try:
        requests.post('https://slack.com/api/chat.postMessage', {
        'token': CONFIG.SLACK_TOKEN,
        'channel': CONFIG.SLACK_CHANNEL_INFO,
        'text': text,
        'username': CONFIG.SLACK_BOT_NAME,
})
    except ConnectionError:
        exit("Connection Error.")

def get_hostname():
    return socket.gethostname()

def get_local_ip():
    local_ip_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    local_ip_socket.connect(('10.255.255.255', 1))
    local_ip_address = local_ip_socket.getsockname()[0]

    local_ip_socket.close()
    return local_ip_address

def get_connected_network():
    output = str(subprocess.check_output(['iwgetid']))
    network= output.split('"')[1]
    return network

def get_using_interface():
    output = str(subprocess.check_output(['iwgetid']))
    network = output.split(' ')[0]
    return network

def get_device_uptime():
    uptime_data = os.popen('uptime -p').read()[:-1]
    uptime_data = [f'{x.capitalize()} ' for x in uptime_data.split(' ')]
    uptime_data = ''.join(uptime_data).rstrip()
    return uptime_data

def get_ram_usage():
    total_m = os.popen('free -h').readlines()[1].split()[1]
    used_m= os.popen('free -h').readlines()[1].split()[2]
    return f'{used_m} of {total_m}'

hostname = get_hostname()
local_ip = get_local_ip()
wifi = get_connected_network()
interface = get_using_interface()
device_uptime = get_device_uptime()
ram = get_ram_usage()

INFORMATION = '''HOSTNAME: "{}"
LOCAL IP: "{}"
CONNECTED NETWORK: "{}"
USING NETWORK INTERFACE: "{}"
DEVICE UPTIME: "{}"
RAM USAGE: "{}"'''.format(hostname, local_ip, wifi, interface, device_uptime, ram)

table = PrettyTable(['Hostname', 'Local IP', 'Wi-Fi', 'Interface', 'Uptime', 'RAM'])
data = ([hostname, local_ip, wifi, interface, device_uptime, ram])
table.add_row(data)


print(table)
send_message(INFORMATION)
